#!/usr/bin/env python3
"""Phase Gate — minimal PreToolUse + PostToolUse hook for atomic checklist model.

Replaces phase-compliance-enforcer.py (841 lines → ~120 lines).
Only three checks survive from the original 8 BLOCKs + 6 WARNs:

HARD BLOCKS (PreToolUse exit code 2):
  1. Code write authorization — default-deny on Write/Edit to code files
     during BUILD sessions unless workspace contains plan-lock evidence (ADR/IC).
  2. Git commit gate — blocks git commit/push unless chain-evaluator reports
     complete (reads .chain-status.json).

SOFT WARNS (PostToolUse systemMessage):
  3. Context firewall — warns when personal context detected in workspace writes.

Everything else (phase skip, DA exit-gate, BELIEF-on-advance, CB evidence,
synthesis write, SendMessage dispatch) is handled by the chain-evaluator.py
Stop hook which evaluates completeness at session end.
"""

import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHAIN_STATUS_FILE = Path.home() / ".claude/hooks/.chain-status.json"
DEFAULT_WORKSPACE = Path.home() / ".claude/teams/sigma-review/shared/workspace.md"

# Paths that are always writable (infrastructure, not code)
INFRASTRUCTURE_PATH_MARKERS = [
    "/.claude/teams/",
    "/.claude/plans/",
    "/.claude/memory/",
    "/.claude/projects/",
    "/.claude/hooks/",
    "/.claude/skills/",
    "/.claude/agents/",
    "/.claude/cache/",
    "/tmp/",
]

# Personal context keywords for firewall detection
CONTEXT_FIREWALL_KEYWORDS = [
    r"\bmy career\b", r"\bmy role\b", r"\bmy experience\b",
    r"\bmy salary\b", r"\bmy family\b", r"\bmy job\b",
    r"\bI should\b.*(?:career|job|position|role)",
    r"\bpersonally I\b",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_sigma_session() -> bool:
    """Check if current workspace indicates an active sigma session."""
    try:
        content = DEFAULT_WORKSPACE.read_text(encoding="utf-8").lower()
        return "## task" in content or "## mode" in content
    except (FileNotFoundError, OSError):
        return False


def _is_build_session() -> bool:
    """Check if current workspace is a BUILD session."""
    try:
        content = DEFAULT_WORKSPACE.read_text(encoding="utf-8")
        return "mode: BUILD" in content or "mode: build" in content
    except (FileNotFoundError, OSError):
        return False


def _workspace_has_plan_lock() -> bool:
    """Check if workspace contains plan-lock evidence (ADR/IC sections populated)."""
    try:
        content = DEFAULT_WORKSPACE.read_text(encoding="utf-8")
        has_adr = bool(re.search(r"ADR\[\d+\]", content))
        has_ic = bool(re.search(r"IC\[\d+\]", content))
        return has_adr and has_ic
    except (FileNotFoundError, OSError):
        return False


def _chain_is_complete() -> bool:
    """Check if the chain-evaluator last reported complete.

    Also returns True if the ONLY failing item is A14 (git clean) —
    since the commit IS the action that satisfies A14, blocking commit
    on A14 creates a circular dependency.
    """
    try:
        data = json.loads(CHAIN_STATUS_FILE.read_text())
        if data.get("last_complete", False):
            return True
        # A14-only exception: if the only failure is git clean, allow commit
        failed = data.get("failed_items", {})
        if failed and all(k == "A14" for k in failed):
            return True
        return False
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False


def _workspace_section_has_content(section_name: str) -> bool:
    """Check if a workspace ## section has non-empty content."""
    try:
        content = DEFAULT_WORKSPACE.read_text(encoding="utf-8")
        pattern = rf"^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)"
        m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if not m:
            return False
        section_content = m.group(1).strip()
        return len(section_content) > 0
    except (FileNotFoundError, OSError):
        return False


# ---------------------------------------------------------------------------
# BLOCK 1: Code write authorization
# ---------------------------------------------------------------------------

def check_code_write_authorization(file_path: str) -> tuple[bool, str]:
    """BLOCK Write/Edit to code files in BUILD sessions without plan-lock evidence.

    In the atomic checklist model, this replaces the phase-based authorization.
    Code writes are blocked unless the workspace contains ADR[] and IC[] entries
    (evidence that a plan was locked before implementation started).
    Infrastructure paths are always writable.
    """
    if not _is_build_session():
        return False, ""  # Not a BUILD session — no restriction

    if _workspace_has_plan_lock():
        return False, ""  # Plan is locked — code writes authorized

    # Allow infrastructure writes in any state
    for marker in INFRASTRUCTURE_PATH_MARKERS:
        if marker in file_path:
            return False, ""

    basename = os.path.basename(file_path)
    return True, (
        f"CODE WRITE BLOCKED: Write/Edit to '{basename}' denied — "
        f"workspace does not contain plan-lock evidence (ADR[] + IC[]). "
        f"Lock the plan before writing code. "
        f"Infrastructure paths (/.claude/*, /tmp/*) are always writable."
    )


# ---------------------------------------------------------------------------
# BLOCK 2: Git commit gate
# ---------------------------------------------------------------------------

def check_premature_git_operation(command: str) -> tuple[bool, str]:
    """BLOCK git commit/push unless chain-evaluator reports complete.

    Irreversible action protection. In the atomic checklist model, git operations
    are blocked until the chain is complete — not until specific phases finish.
    Only applies during active sigma sessions (workspace has ## task or ## mode).
    """
    if not re.search(r'\bgit\s+(commit|push)\b', command):
        return False, ""

    # Only enforce during active sigma sessions
    if not _is_sigma_session():
        return False, ""

    if _chain_is_complete():
        return False, ""

    return True, (
        "GIT OPERATION BLOCKED: Cannot run git commit/push — "
        "chain evaluation is not complete. Run 'python3 ~/.claude/hooks/chain-evaluator.py evaluate' "
        "to check status. Complete all chain items before committing."
    )


# ---------------------------------------------------------------------------
# BLOCK 3: Pre-shutdown promotion gate
# ---------------------------------------------------------------------------

def check_premature_shutdown(tool_input: dict) -> tuple[bool, str]:
    """BLOCK SendMessage shutdown_request unless promotion round is complete.

    Prevents the recipe skip where lead sends shutdown before chain closure
    (promotion, compilation, sync) is done. The visible deliverable (synthesis)
    is not the full deliverable — the completed chain is.
    """
    # Only check SendMessage with shutdown_request
    message = tool_input.get("message", "")
    if isinstance(message, str):
        return False, ""  # Plain text message, not a shutdown request
    if not isinstance(message, dict):
        return False, ""
    if message.get("type") != "shutdown_request":
        return False, ""  # Not a shutdown request

    # Only enforce during active sigma sessions
    if not _is_sigma_session():
        return False, ""

    missing = []
    if not _workspace_section_has_content("promotion"):
        missing.append("## promotion (run promotion round)")
    if not _workspace_section_has_content("contamination-check"):
        missing.append("## contamination-check (run pre-synthesis checks)")
    if not _workspace_section_has_content("sycophancy-check"):
        missing.append("## sycophancy-check (run pre-synthesis checks)")

    if missing:
        return True, (
            "SHUTDOWN BLOCKED: Chain closure incomplete. "
            f"Missing sections: {', '.join(missing)}. "
            "Complete the full recipe (promotion, pre-synthesis checks) "
            "before sending shutdown requests. The synthesis document is "
            "one step in the recipe, not the deliverable."
        )

    return False, ""


# ---------------------------------------------------------------------------
# WARN 4: Context firewall
# ---------------------------------------------------------------------------

def detect_context_firewall_leak(file_path: str, content: str) -> str | None:
    """WARN if personal context markers detected in workspace writes."""
    if "workspace" not in file_path.lower():
        return None

    for pattern in CONTEXT_FIREWALL_KEYWORDS:
        if re.search(pattern, content, re.IGNORECASE):
            return (
                "CONTEXT FIREWALL: Possible personal context leak detected in workspace "
                "write. Personal context (career, role, family, salary) must not appear "
                "in analytical workspace — it contaminates agent analysis. Review and "
                "strip before writing."
            )
    return None


# ---------------------------------------------------------------------------
# Hook dispatch
# ---------------------------------------------------------------------------

def enforce_pre_tool_use(data: dict) -> tuple[int, dict]:
    """PreToolUse enforcement. Returns (exit_code, output_dict)."""
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        should_block, reason = check_code_write_authorization(file_path)
        if should_block:
            return 2, {"reason": reason}

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        should_block, reason = check_premature_git_operation(command)
        if should_block:
            return 2, {"reason": reason}

    elif tool_name == "SendMessage":
        should_block, reason = check_premature_shutdown(tool_input)
        if should_block:
            return 2, {"reason": reason}

    return 0, {}


def enforce_post_tool_use(data: dict) -> dict:
    """PostToolUse enforcement. Returns output_dict with optional systemMessage."""
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "") if tool_name == "Write" else tool_input.get("new_string", "")
        warn = detect_context_firewall_leak(file_path, content)
        if warn:
            return {"systemMessage": warn}

    return {}


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    event = data.get("hook_event_name", "")

    if event == "PreToolUse":
        exit_code, output = enforce_pre_tool_use(data)
        if output:
            print(json.dumps(output))
        sys.exit(exit_code)

    elif event == "PostToolUse":
        output = enforce_post_tool_use(data)
        if output:
            print(json.dumps(output))
        sys.exit(0)

    # No Stop handler — chain-evaluator.py handles Stop
    sys.exit(0)


if __name__ == "__main__":
    main()
