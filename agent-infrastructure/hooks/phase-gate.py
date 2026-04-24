#!/usr/bin/env python3
"""Phase Gate — minimal PreToolUse + PostToolUse hook for atomic checklist model.

Replaces phase-compliance-enforcer.py (841 lines → ~120 lines).

HARD BLOCKS (PreToolUse exit code 2):
  1. Code write authorization — default-deny on Write/Edit to code files
     during BUILD sessions unless workspace contains plan-lock evidence (ADR/IC).
  2. Git commit gate — blocks git commit/push unless chain-evaluator reports
     complete (reads .chain-status.json).
  3. Pre-shutdown promotion gate — blocks SendMessage shutdown_request
     unless workspace has promotion + contamination + sycophancy sections.
  4. sed -i workspace/hooks scope — blocks sed -i on workspace.md, shared/
     workspace files, or /.claude/hooks/ paths. Uses shlex.split() argv
     tokenization (CAL[4]) — not raw regex. Backup-extension forms
     (-i.bak, -i '' + path) are permitted (they write to separate files).

SOFT WARNS (PostToolUse systemMessage):
  5. Context firewall — warns when personal context detected in workspace writes.

Everything else (phase skip, DA exit-gate, BELIEF-on-advance, CB evidence,
synthesis write, SendMessage dispatch) is handled by the chain-evaluator.py
Stop hook which evaluates completeness at session end.
"""

import json
import os
import re
import shlex
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
# BLOCK 4: sed -i on workspace + /.claude/hooks/ (ADR[SS-1] + IC[1] + CAL[4])
# ---------------------------------------------------------------------------

# Path substrings that trigger the sed-i block. Match is substring-based
# so relative paths, absolute paths, and ~ expansions all hit the gate.
SED_I_PROTECTED_PATHS = [
    "workspace.md",
    "/.claude/teams/sigma-review/shared/",
    "/.claude/teams/sigma-optimize/shared/",
    "/.claude/hooks/",
    "/sigma-review/shared/",  # catches non-absolute path forms
    "/sigma-optimize/shared/",
]


def _sed_i_flag_has_backup(flag_token: str, next_token: str | None) -> bool:
    """Decide whether a sed -i invocation uses a backup-extension form.

    Conservative: only the ``-i<SUFFIX>`` joined form with a non-empty
    suffix is treated as a backup form. The separated ``-i '' file`` form
    is equivalent to in-place-no-backup on BSD sed (the empty string is
    the suffix) and is BLOCKED to stay safe across platforms. Likewise
    the bare ``-i`` flag (GNU form without suffix) is BLOCKED.

    CAL[4] note: backup-extension forms pass. We read that narrowly —
    the backup must be a real suffix, not an empty string, to count.
    """
    # Joined form: -i.bak, -iBACKUP
    if flag_token.startswith("-i") and len(flag_token) > 2:
        return True
    # Any other shape (-i alone, --in-place alone) is blocked
    return False


def check_sed_in_place(command: str) -> tuple[bool, str]:
    """BLOCK sed -i on workspace paths or /.claude/hooks/.

    Uses shlex.split() to tokenize argv — resistant to raw-regex bypass
    via env wrappers, shell quoting, and variable expansion within the
    argument list that resolves at parse time.

    Backup-extension forms (``sed -i.bak``) pass per CAL[4] rationale:
    a real suffix produces a recoverable .bak copy on both GNU and BSD
    sed. In-place-no-backup forms (``sed -i``, ``sed -i ''``, ``sed
    --in-place``) are blocked — those are the R19 silent-overwrite
    shapes that cause data loss under concurrent workspace writes.

    Scope (CAL[4]): workspace.md, teams/sigma-review/shared/, teams/
    sigma-optimize/shared/, and /.claude/hooks/. Tool calls outside
    these scopes are never blocked.

    KNOWN LIMITATION (ADR[SS-1] shlex.split argv scope):
    Paths supplied to sed via stdin — e.g. ``echo PATH | xargs sed -i
    'pattern'`` — are NOT visible to an argv scanner. They exist only
    at runtime, after this hook has decided. The following forms
    therefore bypass this check and could overwrite a protected path:

      - ``echo ~/.claude/teams/.../workspace.md | xargs sed -i 's/a/b/'``
      - ``find . -name '*.md' | xargs sed -i 's/a/b/'``
      - ``cat filelist.txt | xargs -n1 sed -i 's/a/b/'``

    Forms where the path IS in argv — including ``xargs -I{}`` with a
    literal operand after sed, ``env FOO=bar sed -i path``, and
    ``/abs/path/to/sed -i workspace.md`` — remain covered.

    Closing the stdin-piped gap requires runtime interception (a sed
    shim, a PreToolUse that re-parses stdin at exec time, or an OS
    monitor), all of which were explicitly out of ADR[SS-1] scope.
    If empirical incidents surface, a new SQ with ADR can address it.
    The CQA evasion-matrix test suite documents the bypass forms
    against this docstring (see ``test_phase_gate.py`` — xargs-stdin
    cases are marked as known-gap rather than removed so the contract
    is inspectable from the test side as well).
    """
    # Fast-path: no sed in the command at all
    if "sed" not in command:
        return False, ""

    # Tokenize. Raw regex can be fooled by quoting tricks — shlex
    # matches shell argv parsing (IC[1]).
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        # Malformed command (unbalanced quotes). Don't block on parse
        # error — let the shell fail naturally.
        return False, ""

    # Walk tokens looking for a sed invocation. Covers wrappers like
    # `env FOO=bar sed ...` and `xargs -I{} sed ... {}` where the sed
    # token appears literally in argv. Does NOT cover stdin-piped
    # forms (`echo path | xargs sed -i ...`) — those paths aren't in
    # argv, so the scanner cannot see them. See docstring KNOWN
    # LIMITATION block.
    n = len(tokens)
    for i, tok in enumerate(tokens):
        if tok != "sed" and not tok.endswith("/sed"):
            continue

        # Collect flags + operands for this sed invocation. Stop at
        # shell separators — they terminate the current command.
        invocation = []
        j = i + 1
        while j < n and tokens[j] not in (";", "&&", "||", "|", "&"):
            invocation.append(tokens[j])
            j += 1

        # Find the -i flag (if any)
        i_flag_idx = None
        for k, t in enumerate(invocation):
            if t == "-i" or t.startswith("-i") or t == "--in-place":
                # Must be a real flag, not a file that happens to start
                # with "-i" (unlikely but shlex.split preserves it).
                # Only treat tokens starting with "-" as flags.
                if t.startswith("-"):
                    i_flag_idx = k
                    break

        if i_flag_idx is None:
            continue  # no -i flag on this sed call — not our concern

        flag_tok = invocation[i_flag_idx]
        next_tok = invocation[i_flag_idx + 1] if i_flag_idx + 1 < len(invocation) else None

        if _sed_i_flag_has_backup(flag_tok, next_tok):
            continue  # backup form — permitted per CAL[4]

        # Check operand paths against protected scope. Operands are
        # all non-flag tokens after the -i flag.
        operands = [t for t in invocation[i_flag_idx + 1 :] if not t.startswith("-")]
        for path in operands:
            for marker in SED_I_PROTECTED_PATHS:
                if marker in path:
                    return True, (
                        f"SED IN-PLACE BLOCKED: 'sed -i' (no backup suffix) on "
                        f"protected path '{path}' denied. In-place edits without a "
                        f"backup extension cause silent overwrites under concurrent "
                        f"workspace writes (R19 data-loss incident). Use one of:\n"
                        f"  - sed -i.bak 'pattern' <file>  (creates backup, recoverable)\n"
                        f"  - Edit tool (atomic, no concurrency race)\n"
                        f"  - workspace_write() helper (atomic Python replace, IC[6])\n"
                        f"Protected scope: workspace.md, teams/sigma-*/shared/, /.claude/hooks/."
                    )

    return False, ""


# ---------------------------------------------------------------------------
# WARN 5: Context firewall
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
        should_block, reason = check_sed_in_place(command)
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
