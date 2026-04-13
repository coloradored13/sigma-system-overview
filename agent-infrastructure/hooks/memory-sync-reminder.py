#!/usr/bin/env python3
"""Memory Sync Reminder — PostToolUse hook on Write|Edit.

Detects writes to auto-memory (Claude Code's built-in memory system at
~/.claude/projects/*/memory/) and reminds Claude to also store the
information in sigma-mem if it's globally relevant.

Also detects writes to sigma-mem files directly (bypassing MCP) and warns.

Behavior:
  - Write to auto-memory path → remind about sigma-mem sync
  - Write to sigma-mem path directly → warn (should use MCP tools)
  - Max 2 reminders per session to avoid noise

This is a NUDGE, not a BLOCK — exit code 0 always.
"""
import json
import os
import re
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

AUTO_MEMORY_PATTERN = "/.claude/projects/"
SIGMA_MEM_PATTERN = "/.claude/memory/"
STATE_FILE = Path("/tmp/.sigma-memory-sync-state")
MAX_REMINDERS = 2

# Content patterns that suggest globally-relevant information
GLOBAL_PATTERNS = [
    r"feedback_",       # Corrections / feedback
    r"reference_",      # Reference material
    r"project_",        # Project state changes
    r"user_",           # User profile updates
]

# Content keywords suggesting decisions/corrections
DECISION_KEYWORDS = [
    "decision", "correction", "feedback", "pattern",
    "established", "enforced", "settled", "recurring",
]


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def read_state():
    """Read sync reminder state. Returns dict."""
    if not STATE_FILE.exists():
        return {"reminder_count": 0, "last_reset": time.time()}
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        # Reset counter if more than 4 hours old
        if time.time() - state.get("last_reset", 0) > 4 * 3600:
            return {"reminder_count": 0, "last_reset": time.time()}
        return state
    except (json.JSONDecodeError, OSError):
        return {"reminder_count": 0, "last_reset": time.time()}


def write_state(state):
    """Write sync reminder state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(STATE_FILE) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, str(STATE_FILE))


# ---------------------------------------------------------------------------
# Detection logic
# ---------------------------------------------------------------------------

def is_auto_memory_write(file_path):
    """Check if this write targets auto-memory."""
    return AUTO_MEMORY_PATTERN in file_path and file_path.endswith(".md")


def is_sigma_mem_direct_write(file_path):
    """Check if this write targets sigma-mem files directly (bypassing MCP)."""
    return SIGMA_MEM_PATTERN in file_path and file_path.endswith(".md")


def is_globally_relevant(file_path, content=""):
    """Heuristic: does this auto-memory write contain globally-relevant info?"""
    basename = os.path.basename(file_path)

    # Check filename patterns
    for pattern in GLOBAL_PATTERNS:
        if re.match(pattern, basename):
            return True

    # Check content for decision/correction keywords
    content_lower = content.lower()
    matches = sum(1 for kw in DECISION_KEYWORDS if kw in content_lower)
    return matches >= 2


def classify_write(file_path, content=""):
    """Classify a write and return appropriate reminder or None."""
    if is_sigma_mem_direct_write(file_path):
        return (
            "Direct write to sigma-mem file detected. Use sigma-mem MCP tools "
            "(store_memory, log_decision, log_correction) instead of writing "
            "files directly — MCP handles format validation and integrity."
        )

    if is_auto_memory_write(file_path):
        if is_globally_relevant(file_path, content):
            basename = os.path.basename(file_path)
            if basename.startswith("feedback_"):
                return (
                    f"Auto-memory feedback saved ({basename}). If this is a "
                    "correction that should persist globally, also call "
                    "mcp__sigma-mem__log_correction to store in sigma-mem."
                )
            elif basename.startswith("project_"):
                return (
                    f"Auto-memory project update saved ({basename}). If this "
                    "contains decisions or patterns relevant across sessions, "
                    "also store via mcp__sigma-mem__log_decision or "
                    "mcp__sigma-mem__store_memory."
                )
            else:
                return (
                    f"Auto-memory updated ({basename}). Consider whether this "
                    "information also belongs in sigma-mem for cross-session "
                    "persistence (store_memory, log_decision, log_correction)."
                )

    return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    event = hook_input.get("event")
    if event != "PostToolUse":
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    # For Write tool, content is in tool_input; for Edit, use new_string
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    if not file_path:
        sys.exit(0)

    # Check state — avoid spamming
    state = read_state()
    if state.get("reminder_count", 0) >= MAX_REMINDERS:
        sys.exit(0)

    # Classify the write
    reminder = classify_write(file_path, content)
    if not reminder:
        sys.exit(0)

    # Update state
    state["reminder_count"] = state.get("reminder_count", 0) + 1
    write_state(state)

    # Output as systemMessage
    output = {"systemMessage": reminder}
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
