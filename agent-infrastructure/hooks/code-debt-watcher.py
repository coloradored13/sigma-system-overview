#!/usr/bin/env python3
"""Code Debt Watcher — PostToolUse hook on Write|Edit.

Background detection of fragile code patterns during sigma-build.
Only fires during build phases (checks for build workspace).
Flags Honnibal patterns: implicit ordering, shared mutable state,
coincidental correctness, load-bearing defaults, error swallowing.

Max 3 flags per build phase. Medium/high risk only.
"""
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime


TEAM_DIR = Path.home() / ".claude" / "teams" / "sigma-build" / "shared"
WORKSPACE = TEAM_DIR / "workspace.md"
STATE_FILE = TEAM_DIR / ".debt-watch-count"

# Only watch code files
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb", ".sh"}

# Max flags per build session
MAX_FLAGS = 3


PATTERNS = [
    {
        "name": "error-swallowing",
        "risk": "high",
        "patterns": [
            # Python bare except
            (r"except\s*:", "Bare except — catches SystemExit, KeyboardInterrupt. Specify exception types."),
            # Python except with pass
            (r"except\s+\w+.*:\s*\n\s*pass\b", "Exception caught and silently discarded. Log or re-raise."),
            # JS empty catch
            (r"catch\s*\([^)]*\)\s*\{\s*\}", "Empty catch block — errors silently swallowed."),
            # Go error ignored
            (r"\b\w+,\s*_\s*:?=\s*\w+\(", "Error return value discarded with _. Handle or propagate."),
        ],
    },
    {
        "name": "shared-mutable-state",
        "risk": "medium",
        "patterns": [
            # Python global keyword
            (r"\bglobal\s+\w+", "Global mutable state — multiple functions can modify. Consider passing as parameter."),
            # Module-level mutable (Python)
            (r"^[A-Z_]+\s*=\s*\[", "Module-level mutable list — shared across imports. Use tuple or function."),
            (r"^[A-Z_]+\s*=\s*\{", "Module-level mutable dict — shared across imports. Consider frozen or function."),
        ],
    },
    {
        "name": "coincidental-correctness",
        "risk": "medium",
        "patterns": [
            # Assert True/False without condition
            (r"assert\s+True\b", "assert True — test always passes. This tests nothing."),
            (r"assert\s+.*is\s+not\s+None\s*$", "Weak assertion — only checks existence, not correctness."),
            # Mock everything pattern
            (r"@mock\.patch.*\n.*@mock\.patch.*\n.*@mock\.patch", "Triple mock — test may not reflect real behavior."),
        ],
    },
    {
        "name": "implicit-ordering",
        "risk": "medium",
        "patterns": [
            # Sequential operations without explicit ordering
            (r"time\.sleep\(\d+\)", "Sleep-based synchronization — fragile ordering. Use explicit sync primitives."),
            # Relying on dict ordering in older patterns
            (r"for\s+\w+\s+in\s+\w+\.keys\(\)", "Iterating dict keys — order may not be guaranteed in all contexts."),
        ],
    },
    {
        "name": "load-bearing-defaults",
        "risk": "medium",
        "patterns": [
            # Default mutable argument (Python)
            (r"def\s+\w+\([^)]*=\s*\[\]", "Mutable default argument (list) — shared across calls. Use None + create inside."),
            (r"def\s+\w+\([^)]*=\s*\{\}", "Mutable default argument (dict) — shared across calls. Use None + create inside."),
            # Hardcoded magic numbers
            (r"(?:timeout|retry|max_attempts|limit)\s*=\s*\d{2,}", "Hardcoded numeric constant — consider named constant or config."),
        ],
    },
    {
        "name": "invisible-invariants",
        "risk": "high",
        "patterns": [
            # Type: ignore without explanation
            (r"#\s*type:\s*ignore(?!\[)", "Blanket type: ignore without specific code — hides invariant violations."),
            # noqa without code
            (r"#\s*noqa(?!\s*:\s*[A-Z])", "Blanket noqa — hides specific linting violations without justification."),
            # nosec without explanation
            (r"#\s*nosec\b", "Security check suppressed — document why this is safe."),
        ],
    },
]


def get_flag_count():
    """Read current flag count for this build session."""
    try:
        return int(STATE_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return 0


def increment_flag_count():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    count = get_flag_count() + 1
    STATE_FILE.write_text(str(count), encoding="utf-8")
    return count


def scan_content(content, file_path):
    """Scan content for fragile patterns. Return list of findings."""
    findings = []
    lines = content.split("\n")

    for category in PATTERNS:
        for pattern_re, suggestion in category["patterns"]:
            for i, line in enumerate(lines, 1):
                if re.search(pattern_re, line):
                    findings.append({
                        "file": file_path,
                        "line": i,
                        "pattern": category["name"],
                        "risk": category["risk"],
                        "suggestion": suggestion,
                        "code": line.strip()[:80],
                    })

    # Sort by risk (high first) and deduplicate by pattern+line
    findings.sort(key=lambda f: (0 if f["risk"] == "high" else 1, f["line"]))

    # Only return medium+ risk
    return [f for f in findings if f["risk"] in ("medium", "high")]


def append_to_workspace(findings):
    """Append debt watch entries to build workspace."""
    if not WORKSPACE.exists():
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entries = []
    for f in findings:
        entries.append(
            f"- {f['file']}:{f['line']} -- {f['pattern']}: {f['suggestion']}\n"
            f"  risk: {f['risk']} | `{f['code']}`"
        )

    section = f"\n## code-debt-watch ({timestamp})\n" + "\n".join(entries) + "\n"

    with open(WORKSPACE, "a", encoding="utf-8") as wf:
        wf.write(section)


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Quick exit: only watch code files
    ext = os.path.splitext(file_path)[1]
    if ext not in CODE_EXTENSIONS:
        sys.exit(0)

    # Quick exit: only during sigma-build (check workspace exists)
    if not WORKSPACE.exists():
        sys.exit(0)

    workspace_content = WORKSPACE.read_text(encoding="utf-8") if WORKSPACE.exists() else ""
    # Only fire during build phase (04-build or later, not plan phase)
    if "## build-track" not in workspace_content.lower() and "04-build" not in workspace_content.lower():
        sys.exit(0)

    # Rate limit: max 3 flags per build
    if get_flag_count() >= MAX_FLAGS:
        sys.exit(0)

    # Get the content that was written/edited
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        content = tool_input.get("new_string", "")
    else:
        sys.exit(0)

    if not content:
        sys.exit(0)

    findings = scan_content(content, file_path)
    if not findings:
        sys.exit(0)

    # Limit to avoid noise
    findings = findings[:2]

    append_to_workspace(findings)
    increment_flag_count()

    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
