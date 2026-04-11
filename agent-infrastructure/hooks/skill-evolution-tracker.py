#!/usr/bin/env python3
"""Skill Evolution Tracker — PostToolUse hook on Read.

Logs which skill files are loaded, how often, by which agents.
Writes to ~/.claude/skills/.skill-usage.jsonl for periodic analysis.
Generates monthly usage reports on demand.
"""
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime


SKILLS_DIR = Path.home() / ".claude" / "skills"
USAGE_LOG = SKILLS_DIR / ".skill-usage.jsonl"


def extract_skill_info(file_path):
    """Extract skill name and file type from a file path.
    Returns (skill_name, file_name, tier) or None if not a skill file.
    """
    skills_prefix = str(SKILLS_DIR) + "/"
    if not file_path.startswith(skills_prefix):
        return None

    relative = file_path[len(skills_prefix):]
    parts = relative.split("/")
    if not parts:
        return None

    skill_name = parts[0]

    # Skip non-skill files (INDEX.md, hidden files)
    if skill_name.startswith(".") or skill_name == "INDEX.md":
        return None

    file_name = "/".join(parts[1:]) if len(parts) > 1 else parts[0]

    # Determine tier
    tier = "router"  # SKILL.md
    if file_name.startswith("references/"):
        if file_name.startswith("references/qr-"):
            tier = "T1"
        elif file_name.startswith("references/Doc"):
            tier = "T3"
        else:
            tier = "T2"

    return skill_name, file_name, tier


def detect_context():
    """Try to detect if we're in a sigma-review or sigma-build context."""
    review_workspace = Path.home() / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"
    build_workspace = Path.home() / ".claude" / "teams" / "sigma-build" / "shared" / "workspace.md"

    if review_workspace.exists():
        try:
            content = review_workspace.read_text(encoding="utf-8")[:500]
            if "## convergence" in content.lower() or "## task" in content.lower():
                return "sigma-review"
        except (PermissionError, OSError):
            pass

    if build_workspace.exists():
        try:
            content = build_workspace.read_text(encoding="utf-8")[:500]
            if "## build-track" in content.lower() or "## plan-track" in content.lower():
                return "sigma-build"
        except (PermissionError, OSError):
            pass

    return "standalone"


def log_usage(skill_name, file_name, tier, context):
    """Append usage entry to JSONL log."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "skill": skill_name,
        "file": file_name,
        "tier": tier,
        "context": context,
    }

    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    if data.get("tool_name") != "Read":
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    if not file_path:
        sys.exit(0)

    skill_info = extract_skill_info(file_path)
    if not skill_info:
        sys.exit(0)

    skill_name, file_name, tier = skill_info
    context = detect_context()

    log_usage(skill_name, file_name, tier, context)

    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
