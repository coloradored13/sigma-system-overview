#!/usr/bin/env python3
"""Chain evaluator for sigma-review / sigma-build atomic checklist enforcement.

Replaces the phase-based orchestrator + 11-bundle gate-check routing with a
single flat checklist evaluated at session end (Stop hook) or on demand (CLI).

Architecture:
  - Reuses check functions from gate_checks.py (imported as a library)
  - Adds peer-verification checks (A16-A18) — new to V2
  - Writes evaluation results to workspace as ## Chain Evaluation (A19)
  - Tracks rejection history for monotonicity enforcement

Usage:
  Stop hook:  python3 chain-evaluator.py              (auto-evaluates, writes to workspace)
  CLI:        python3 chain-evaluator.py evaluate      (full chain, stdout JSON)
  CLI:        python3 chain-evaluator.py status         (mechanical-only quick check)
  CLI:        python3 chain-evaluator.py item A5        (single item)
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Import gate_checks as a library — reuse all 30 check functions
# ---------------------------------------------------------------------------

GATE_CHECKS_PATH = Path(__file__).resolve().parent.parent / "teams/sigma-review/shared"
if str(GATE_CHECKS_PATH) not in sys.path:
    sys.path.insert(0, str(GATE_CHECKS_PATH))

try:
    import gate_checks as gc  # noqa: E402
except ImportError:
    # Fallback: try symlinked path
    _alt = Path.home() / ".claude/teams/sigma-review/shared"
    if str(_alt) not in sys.path:
        sys.path.insert(0, str(_alt))
    import gate_checks as gc  # noqa: E402


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

VERSION = "2.0.0"
STATE_FILE = Path.home() / ".claude/hooks/.chain-status.json"
DEFAULT_WORKSPACE = gc.DEFAULT_WORKSPACE


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass
class ChainItem:
    """Single checklist item result."""
    item_id: str
    name: str
    passed: bool
    category: str  # "agent-work", "peer-verification", "chain-closure"
    details: dict[str, Any] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "passed": self.passed,
            "category": self.category,
            "details": self.details,
            "issues": self.issues,
        }


@dataclass
class ChainResult:
    """Full chain evaluation result."""
    mode: str  # ANALYZE or BUILD
    complete: bool
    items: list[ChainItem] = field(default_factory=list)
    timestamp: str = ""
    version: str = VERSION

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    @property
    def passed_count(self) -> int:
        return sum(1 for i in self.items if i.passed)

    @property
    def failed_count(self) -> int:
        return sum(1 for i in self.items if not i.passed)

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "complete": self.complete,
            "passed": self.passed_count,
            "failed": self.failed_count,
            "total": len(self.items),
            "timestamp": self.timestamp,
            "version": self.version,
            "items": [i.to_dict() for i in self.items],
        }

    def summary_text(self) -> str:
        """Human-readable summary for workspace / systemMessage."""
        lines = [
            f"## Chain Evaluation",
            f"",
            f"Mode: {self.mode} | Status: {'COMPLETE' if self.complete else 'INCOMPLETE'} "
            f"| {self.passed_count}/{len(self.items)} items passed",
            f"Evaluator: chain-evaluator v{self.version} | {self.timestamp}",
            f"",
        ]
        for item in self.items:
            status = "PASS" if item.passed else "FAIL"
            lines.append(f"- [{status}] {item.item_id}: {item.name}")
            for issue in item.issues:
                lines.append(f"  - {issue}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Checklist items: ANALYZE chain (A1-A19)
# Each function wraps a gate_checks check or implements new logic.
# ---------------------------------------------------------------------------

def _wrap_gc(item_id: str, name: str, category: str, check_result: gc.CheckResult) -> ChainItem:
    """Convert a gate_checks.CheckResult to a ChainItem."""
    return ChainItem(
        item_id=item_id,
        name=name,
        passed=check_result.passed,
        category=category,
        details=check_result.details,
        issues=check_result.issues,
    )


def check_a1(content: str) -> ChainItem:
    """A1: Agent findings — non-empty workspace sections."""
    return _wrap_gc("A1", "Agent findings", "agent-work",
                     gc.check_agent_output_non_empty(content))


def check_a2(content: str) -> ChainItem:
    """A2: Source provenance on all findings."""
    return _wrap_gc("A2", "Source provenance", "agent-work",
                     gc.check_source_provenance(content))


def check_a3(content: str) -> ChainItem:
    """A3: Dialectical bootstrapping — DB[] with 5-step substructure."""
    result = gc.check_dialectical_bootstrapping(content)
    # Enhance: check for 5-step substructure markers in DB[] entries
    agents = gc.extract_agents_from_workspace(content)
    shallow_db = []
    for agent in agents:
        section = gc._get_agent_section(content, agent)
        db_entries = re.findall(r"DB\[.*?\].*?(?=DB\[|\Z|###)", section, re.DOTALL | re.IGNORECASE)
        for entry in db_entries:
            steps_found = sum(1 for marker in ["initial", "assume.wrong", "counter", "re.estimate", "reconcile"]
                             if re.search(marker, entry, re.IGNORECASE))
            if steps_found < 3 and len(entry.strip()) > 10:  # has content but shallow structure
                shallow_db.append(f"{agent}: DB entry missing {5 - steps_found} of 5 steps")

    if shallow_db:
        result.issues.extend(shallow_db)
        # Don't fail for shallow structure yet — flag as warning
        result.details["shallow_db_entries"] = shallow_db

    return _wrap_gc("A3", "Dialectical bootstrapping", "agent-work", result)


def check_a4(content: str) -> ChainItem:
    """A4: Circuit breaker evidence."""
    return _wrap_gc("A4", "Circuit breaker", "agent-work",
                     gc.check_circuit_breaker(content))


def check_a5(content: str) -> ChainItem:
    """A5: DA challenges + agent responses."""
    return _wrap_gc("A5", "DA challenges + responses", "agent-work",
                     gc.check_cross_track_participation(content))


def check_a6(content: str) -> ChainItem:
    """A6: BELIEF state present."""
    return _wrap_gc("A6", "BELIEF state", "agent-work",
                     gc.check_belief_state_written(content))


def check_a7(content: str) -> ChainItem:
    """A7: Exit-gate format and criteria."""
    return _wrap_gc("A7", "Exit-gate", "agent-work",
                     gc.check_exit_gate_format(content))


def check_a8(content: str) -> ChainItem:
    """A8: Contamination check."""
    return _wrap_gc("A8", "Contamination check", "agent-work",
                     gc.check_contamination(content))


def check_a9(content: str) -> ChainItem:
    """A9: Source provenance audit."""
    return _wrap_gc("A9", "Source provenance audit", "agent-work",
                     gc.check_source_provenance_audit(content))


def check_a10(content: str) -> ChainItem:
    """A10: Anti-sycophancy check."""
    return _wrap_gc("A10", "Anti-sycophancy check", "agent-work",
                     gc.check_anti_sycophancy(content))


def check_a11(content: str) -> ChainItem:
    """A11: Synthesis artifact in archive."""
    return _wrap_gc("A11", "Synthesis artifact", "chain-closure",
                     gc.check_synthesis_artifact(content))


def check_a12(content: str) -> ChainItem:
    """A12: Workspace archive."""
    result = gc.check_session_end(content)
    # Extract just the archive portion
    return ChainItem(
        item_id="A12",
        name="Workspace archive",
        passed=result.details.get("archive_file_found", False),
        category="chain-closure",
        details={k: v for k, v in result.details.items() if "archive" in k.lower()},
        issues=[i for i in result.issues if "archive" in i.lower()],
    )


def check_a13(content: str) -> ChainItem:
    """A13: Promotion evidence."""
    return _wrap_gc("A13", "Promotion evidence", "chain-closure",
                     gc.check_promotion_content(content))


def check_a14(content: str) -> ChainItem:
    """A14: Git clean."""
    result = gc.check_session_end(content)
    return ChainItem(
        item_id="A14",
        name="Git clean",
        passed=result.details.get("git_clean", False),
        category="chain-closure",
        details={k: v for k, v in result.details.items() if "git" in k.lower() or "commit" in k.lower()},
        issues=[i for i in result.issues if "git" in i.lower() or "commit" in i.lower() or "push" in i.lower()],
    )


def check_a15(content: str) -> ChainItem:
    """A15: XVERIFY coverage (conditional on availability)."""
    return _wrap_gc("A15", "XVERIFY coverage", "agent-work",
                     gc.check_xverify_coverage(content))


# ---------------------------------------------------------------------------
# Peer verification checks (A16-A18) — NEW
# ---------------------------------------------------------------------------

_PEER_VERIFY_HEADER = re.compile(
    r"^### Peer Verification:\s*(\S+)\s+verifying\s+(\S+)",
    re.MULTILINE | re.IGNORECASE,
)


def _extract_peer_verifications(content: str) -> list[dict[str, str]]:
    """Extract all peer verification sections from workspace.

    Returns list of {verifier, verified, section_text}.
    """
    verifications = []
    matches = list(_PEER_VERIFY_HEADER.finditer(content))

    for i, m in enumerate(matches):
        start = m.end()
        # Section runs until next ### or ## or end
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        # Also stop at next ## or ### that isn't a peer verification
        next_header = re.search(r"^#{2,3}\s", content[start:end], re.MULTILINE)
        if next_header:
            end = start + next_header.start()

        verifications.append({
            "verifier": m.group(1).lower().strip(),
            "verified": m.group(2).lower().strip(),
            "text": content[start:end].strip(),
        })

    return verifications


def check_a16(content: str) -> ChainItem:
    """A16: Peer verification sections exist.

    Each non-DA agent must have at least one ### Peer Verification: section
    where they verify another agent.
    """
    agents = gc.extract_agents_from_workspace(content)
    verifications = _extract_peer_verifications(content)
    verifier_names = {v["verifier"] for v in verifications}

    agents_without_verification = [a for a in agents if a not in verifier_names]

    return ChainItem(
        item_id="A16",
        name="Peer verification sections",
        passed=len(agents_without_verification) == 0,
        category="peer-verification",
        details={
            "agents": agents,
            "verifications_found": len(verifications),
            "agents_without_verification": agents_without_verification,
        },
        issues=[
            f"Agent '{a}' has no peer verification section" for a in agents_without_verification
        ],
    )


def check_a17(content: str) -> ChainItem:
    """A17: Verification specificity.

    Each peer verification must reference >=3 specific artifact IDs from the
    verified agent's workspace section. Generic confirmations fail.
    """
    verifications = _extract_peer_verifications(content)
    insufficient = []

    # Patterns that count as specific artifact references
    artifact_patterns = [
        r"DB\[[\w-]+\]",           # DB[finding-name]
        r"F\[[\w-]+\]",            # F[finding-id]
        r"FINDING\[[\w-]+\]",      # FINDING[id]
        r"XVERIFY\[[\w:-]+\]",     # XVERIFY[provider:model]
        r"H\d+",                    # H1, H2, etc.
        r"CB\[\d\]",               # CB[1], CB[2]
        r"BELIEF\[[\w]+\]",        # BELIEF[rN]
        r"DA\[#?\d+\]",            # DA[#1]
        r"ADR\[\d+\]",             # ADR[1]
        r"SQ\[\d+\]",              # SQ[1]
        r"IC\[\d+\]",              # IC[1]
        r"\|source:[\w-]+",        # |source:code-read
        r"T[123][-\s]",            # T1, T2, T3 quality tier
    ]

    for v in verifications:
        text = v["text"]
        refs_found = 0
        for pattern in artifact_patterns:
            refs_found += len(re.findall(pattern, text, re.IGNORECASE))

        if refs_found < 3:
            insufficient.append(
                f"{v['verifier']} verifying {v['verified']}: "
                f"only {refs_found} specific artifact references (need >=3)"
            )

    return ChainItem(
        item_id="A17",
        name="Verification specificity",
        passed=len(insufficient) == 0,
        category="peer-verification",
        details={
            "verifications_checked": len(verifications),
            "insufficient": insufficient,
        },
        issues=insufficient,
    )


def check_a18(content: str) -> ChainItem:
    """A18: Verification coverage matrix.

    Every agent must be verified by at least 2 others (1 ring peer + DA).
    Build an NxN verification matrix and check full row coverage.
    """
    agents = gc.extract_agents_from_workspace(content)
    verifications = _extract_peer_verifications(content)

    # Also count DA challenges as verification of all agents
    da_section = gc._get_agent_section(content, "devils-advocate")
    da_verifies_all = bool(re.search(
        r"(?:DA\[#?\d+\]|exit-gate|challenge)", da_section, re.IGNORECASE
    ))

    # Build coverage: who verified whom
    verified_by: dict[str, set[str]] = {a: set() for a in agents}
    for v in verifications:
        if v["verified"] in verified_by:
            verified_by[v["verified"]].add(v["verifier"])

    # DA counts as a verifier for all agents
    if da_verifies_all:
        for a in agents:
            verified_by[a].add("devils-advocate")

    # Check coverage: each agent needs >=2 verifiers
    under_covered = []
    for agent, verifiers in verified_by.items():
        if len(verifiers) < 2:
            under_covered.append(
                f"Agent '{agent}' verified by only {len(verifiers)}: {verifiers or 'none'}"
            )

    return ChainItem(
        item_id="A18",
        name="Verification coverage matrix",
        passed=len(under_covered) == 0,
        category="peer-verification",
        details={
            "agents": agents,
            "coverage": {a: list(v) for a, v in verified_by.items()},
            "da_verifies_all": da_verifies_all,
            "under_covered": under_covered,
        },
        issues=under_covered,
    )


# ---------------------------------------------------------------------------
# BUILD-specific checks (B1-B4)
# ---------------------------------------------------------------------------

def check_b1(content: str) -> ChainItem:
    """B1: Plan lock — ADR/DS/IC sections populated."""
    return _wrap_gc("B1", "Plan lock", "agent-work",
                     gc.check_plan_lock(content))


def check_b2(content: str) -> ChainItem:
    """B2: Build checkpoints."""
    return _wrap_gc("B2", "Build checkpoints", "agent-work",
                     gc.check_checkpoint(content))


def check_b3(content: str) -> ChainItem:
    """B3: Merge verified (if parallel engineers)."""
    return _wrap_gc("B3", "Merge verified", "agent-work",
                     gc.check_merge_verified(content))


def check_b4(content: str) -> ChainItem:
    """B4: Build-track source tags."""
    return _wrap_gc("B4", "Build-track source tags", "agent-work",
                     gc.check_build_track_source_tags(content))


# ---------------------------------------------------------------------------
# Chain evaluation: run all items
# ---------------------------------------------------------------------------

ANALYZE_CHAIN = [
    check_a1, check_a2, check_a3, check_a4, check_a5,
    check_a6, check_a7, check_a8, check_a9, check_a10,
    check_a15,  # XVERIFY (conditional)
    # Peer verification
    check_a16, check_a17, check_a18,
    # Chain closure
    check_a11, check_a12, check_a13, check_a14,
]

BUILD_EXTRAS = [check_b1, check_b2, check_b3, check_b4]


def evaluate_chain(workspace_path: str | Path | None = None,
                   mode: str | None = None) -> ChainResult:
    """Evaluate the full atomic chain against workspace content.

    Args:
        workspace_path: Path to workspace file (default: shared/workspace.md)
        mode: ANALYZE or BUILD (auto-detected from workspace if None)

    Returns:
        ChainResult with per-item pass/fail
    """
    content = gc.read_workspace(workspace_path)
    if mode is None:
        mode = gc.get_mode(content)

    checks = list(ANALYZE_CHAIN)
    if mode == "BUILD":
        checks.extend(BUILD_EXTRAS)

    items = [fn(content) for fn in checks]
    complete = all(item.passed for item in items)

    return ChainResult(mode=mode, complete=complete, items=items)


def evaluate_single(item_id: str, workspace_path: str | Path | None = None) -> ChainItem:
    """Evaluate a single checklist item by ID."""
    content = gc.read_workspace(workspace_path)

    # Map item IDs to functions
    all_checks = {
        "A1": check_a1, "A2": check_a2, "A3": check_a3, "A4": check_a4,
        "A5": check_a5, "A6": check_a6, "A7": check_a7, "A8": check_a8,
        "A9": check_a9, "A10": check_a10, "A11": check_a11, "A12": check_a12,
        "A13": check_a13, "A14": check_a14, "A15": check_a15,
        "A16": check_a16, "A17": check_a17, "A18": check_a18,
        "B1": check_b1, "B2": check_b2, "B3": check_b3, "B4": check_b4,
    }

    fn = all_checks.get(item_id.upper())
    if fn is None:
        return ChainItem(
            item_id=item_id, name="Unknown", passed=False,
            category="error", issues=[f"Unknown item ID: {item_id}"],
        )
    return fn(content)


# ---------------------------------------------------------------------------
# Rejection monotonicity — prevent brute-force retries
# ---------------------------------------------------------------------------

def _content_hash(content: str) -> str:
    """Hash workspace content for change detection."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _load_state() -> dict:
    """Load chain status tracking state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_state(state: dict) -> None:
    """Save chain status tracking state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def check_monotonicity(result: ChainResult, workspace_path: str | Path | None = None) -> ChainResult:
    """Apply rejection monotonicity: items that previously failed require
    material workspace changes before re-evaluation.

    Modifies result in-place if a previously-failed item hasn't changed.
    """
    content = gc.read_workspace(workspace_path)
    current_hash = _content_hash(content)
    state = _load_state()

    prev_hash = state.get("last_content_hash", "")
    prev_failures = state.get("failed_items", {})

    if current_hash == prev_hash:
        # No workspace changes — all previously failed items stay failed
        for item in result.items:
            if item.item_id in prev_failures and item.passed:
                item.passed = False
                item.issues.append(
                    f"Monotonicity: previously failed, workspace unchanged since last evaluation"
                )

    # Update state with current failures
    state["last_content_hash"] = current_hash
    state["last_evaluation"] = result.timestamp
    state["last_complete"] = result.complete
    state["failed_items"] = {
        item.item_id: item.issues[0] if item.issues else "failed"
        for item in result.items if not item.passed
    }
    _save_state(state)

    return result


# ---------------------------------------------------------------------------
# Workspace writer — A19: Chain evaluation output as artifact
# ---------------------------------------------------------------------------

def write_evaluation_to_workspace(result: ChainResult,
                                   workspace_path: str | Path | None = None) -> None:
    """Write ## Chain Evaluation section to workspace.

    This is checklist item A19 — the evaluator's output IS part of the chain.
    """
    p = Path(workspace_path) if workspace_path else DEFAULT_WORKSPACE
    if not p.exists():
        return  # No workspace to write to — not a sigma session

    content = p.read_text(encoding="utf-8")

    # Remove existing ## Chain Evaluation section if present
    content = re.sub(
        r"^## Chain Evaluation\n.*?(?=^## |\Z)",
        "",
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Append new evaluation
    summary = result.summary_text()
    content = content.rstrip() + "\n\n" + summary + "\n"

    p.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Hook dispatch (Stop hook entry point)
# ---------------------------------------------------------------------------

def enforce_stop(data: dict) -> dict:
    """Stop hook handler: evaluate chain, write to workspace, return systemMessage.

    Non-looping design: returns informational messages only, never actionable
    demands that would cause Claude to retry and trigger the Stop hook again.
    Idempotent: skips re-evaluation if workspace hasn't changed since last eval.
    """
    # Only evaluate if a workspace exists (we're in a sigma session)
    if not DEFAULT_WORKSPACE.exists():
        return {}

    try:
        content = gc.read_workspace()
    except FileNotFoundError:
        return {}

    # Check if this is a sigma-review or sigma-build session
    # (workspace must have ## task or ## mode section)
    if "## task" not in content.lower() and "## mode" not in content.lower():
        return {}

    # Idempotency: skip if workspace hasn't changed since last evaluation
    current_hash = _content_hash(content)
    state = _load_state()
    if state.get("last_content_hash") == current_hash and "## Chain Evaluation" in content:
        # Already evaluated this exact workspace content — no-op
        return {}

    result = evaluate_chain()
    result = check_monotonicity(result)
    write_evaluation_to_workspace(result)

    # Update state hash to reflect post-write workspace content.
    # Without this, the idempotency guard fails on the next call because
    # write_evaluation_to_workspace changed the workspace content.
    try:
        post_write_content = gc.read_workspace()
        post_write_hash = _content_hash(post_write_content)
        state = _load_state()
        state["last_content_hash"] = post_write_hash
        _save_state(state)
    except (FileNotFoundError, OSError):
        pass

    # Informational messages only — do NOT phrase as demands or instructions.
    # The lead runs chain-evaluator.py evaluate explicitly before declaring done.
    if result.complete:
        return {"systemMessage": f"[chain-eval] {result.passed_count}/{len(result.items)} items passed. Chain complete."}

    return {"systemMessage": (
        f"[chain-eval] {result.passed_count}/{len(result.items)} items passed. "
        f"Results written to workspace ## Chain Evaluation."
    )}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """CLI and hook dispatch."""
    # Check CLI args FIRST — they take priority over stdin detection.
    # When run via Claude Code's Bash tool, stdin is piped (not a tty)
    # even for CLI invocations, so stdin-first detection misroutes CLI
    # calls to the hook path where they silently exit 0.
    args = sys.argv[1:]

    if args:
        # Explicit CLI invocation — skip stdin detection entirely
        pass
    elif not sys.stdin.isatty():
        # No CLI args + stdin is piped → likely a hook invocation
        try:
            data = json.loads(sys.stdin.read())
        except (json.JSONDecodeError, EOFError):
            data = {}

        event = data.get("hook_event_name", "")
        if event == "Stop":
            output = enforce_stop(data)
            if output:
                print(json.dumps(output))
            sys.exit(0)
        else:
            # Not a Stop event — chain-evaluator only runs on Stop
            sys.exit(0)
    else:
        # No args, stdin is a tty — show usage
        print("Usage: chain-evaluator.py [evaluate|status|item <ID>]", file=sys.stderr)
        sys.exit(1)

    if not args:
        sys.exit(0)

    cmd = args[0].lower()
    # evaluate/status accept workspace path as args[1]; item uses args[1] as the item ID
    # and args[2] (if present) as the workspace path.
    if cmd in ("evaluate", "status"):
        workspace = args[1] if len(args) > 1 else None
    elif cmd == "item":
        workspace = args[2] if len(args) > 2 else None
    else:
        workspace = None

    if cmd == "evaluate":
        result = evaluate_chain(workspace)
        result = check_monotonicity(result, workspace)
        print(json.dumps(result.to_dict(), indent=2))
    elif cmd == "status":
        # Quick mechanical-only check — skip analytical checks
        result = evaluate_chain(workspace)
        summary = {
            "complete": result.complete,
            "passed": result.passed_count,
            "failed": result.failed_count,
            "total": len(result.items),
            "failed_items": [
                {"id": i.item_id, "name": i.name}
                for i in result.items if not i.passed
            ],
        }
        print(json.dumps(summary, indent=2))
    elif cmd == "item":
        if len(args) < 2:
            print("Usage: chain-evaluator.py item <ID> [workspace]", file=sys.stderr)
            sys.exit(1)
        item = evaluate_single(args[1], workspace)
        print(json.dumps(item.to_dict(), indent=2))
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
