#!/usr/bin/env python3
"""Recall Reminder — PreToolUse hook on Read|Bash.

Fires once per session to nudge Claude to call sigma-mem recall at
conversation start. Also detects drift between auto-memory and sigma-mem
by comparing modification timestamps.

Behavior:
  - On first Read|Bash call of a session: check if recall has been done
  - If not: return systemMessage reminding to call recall
  - If recall already done (marked by PostToolUse on mcp__sigma-mem__recall):
    skip silently
  - Also: compare auto-memory vs sigma-mem freshness, flag significant drift

Session tracking via /tmp file — resets on reboot or after TTL (4 hours).
This is a NUDGE, not a BLOCK — exit code 0 always.
"""
import json
import os
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SESSION_STATE = Path("/tmp/.sigma-recall-session")
RECALL_TTL_SECONDS = 4 * 3600  # 4 hours — after this, nudge again

AUTO_MEMORY_DIR = Path.home() / ".claude" / "projects"
SIGMA_MEM_DIR = Path.home() / ".claude" / "memory"

# How many hours of drift between the two systems before we flag it
DRIFT_THRESHOLD_HOURS = 48


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def recall_done_recently():
    """Check if recall was called within the TTL window."""
    if not SESSION_STATE.exists():
        return False
    try:
        mtime = SESSION_STATE.stat().st_mtime
        age = time.time() - mtime
        return age < RECALL_TTL_SECONDS
    except OSError:
        return False


def mark_recall_done():
    """Mark that recall has been called in this session."""
    SESSION_STATE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_STATE.write_text(str(time.time()), encoding="utf-8")


def mark_nudge_sent():
    """Mark that we already sent the nudge this session (avoid spamming).

    Uses a separate file so mark_recall_done() can override it later.
    """
    nudge_file = Path("/tmp/.sigma-recall-nudged")
    nudge_file.write_text(str(time.time()), encoding="utf-8")


def nudge_already_sent():
    """Check if we already sent a nudge recently (within 30 minutes)."""
    nudge_file = Path("/tmp/.sigma-recall-nudged")
    if not nudge_file.exists():
        return False
    try:
        mtime = nudge_file.stat().st_mtime
        age = time.time() - mtime
        return age < 1800  # 30 minutes
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------

def get_newest_mtime(directory):
    """Get the most recent modification time of any .md file in a directory tree."""
    newest = 0
    if not directory.exists():
        return 0
    for md_file in directory.rglob("*.md"):
        try:
            mtime = md_file.stat().st_mtime
            if mtime > newest:
                newest = mtime
        except OSError:
            continue
    return newest


def check_memory_drift():
    """Compare auto-memory and sigma-mem freshness. Return warning or None."""
    auto_newest = get_newest_mtime(AUTO_MEMORY_DIR)
    sigma_newest = get_newest_mtime(SIGMA_MEM_DIR)

    if auto_newest == 0 or sigma_newest == 0:
        return None  # Can't compare if one doesn't exist

    drift_seconds = abs(auto_newest - sigma_newest)
    drift_hours = drift_seconds / 3600

    if drift_hours < DRIFT_THRESHOLD_HOURS:
        return None

    if auto_newest > sigma_newest:
        stale = "sigma-mem"
        fresh = "auto-memory"
    else:
        stale = "auto-memory"
        fresh = "sigma-mem"

    return (
        f"Memory drift detected: {stale} is {drift_hours:.0f}h behind {fresh}. "
        f"Consider syncing — decisions/corrections in one system may be missing from the other."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    event = hook_input.get("event")

    # --- PostToolUse: detect recall completion ---
    if event == "PostToolUse":
        tool_name = hook_input.get("tool_name", "")
        if tool_name == "mcp__sigma-mem__recall":
            mark_recall_done()
        sys.exit(0)

    # --- PreToolUse: nudge if recall not done ---
    if event == "PreToolUse":
        # Skip if recall was already done recently
        if recall_done_recently():
            sys.exit(0)

        # Skip if we already sent a nudge this session (avoid spam)
        if nudge_already_sent():
            sys.exit(0)

        # Build the nudge message
        messages = []
        messages.append(
            "Recall not yet called this session. Consider running "
            "mcp__sigma-mem__recall to load global memory (patterns, "
            "decisions, corrections) before proceeding."
        )

        # Check for drift
        drift_warning = check_memory_drift()
        if drift_warning:
            messages.append(drift_warning)

        mark_nudge_sent()

        # Output as systemMessage (nudge, not block)
        output = {"systemMessage": " | ".join(messages)}
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
