#!/usr/bin/env python3
"""Shadow Mode (Skill A/B Testing) — PostToolUse hook on Read.

When a skill has a .shadow/ directory with an active config, logs
invocations and tracks comparison data for evaluating proposed changes.
Graduates or rejects after target_invocations reached.

Only fires when reading SKILL.md files that have an active shadow config.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime


SKILLS_DIR = Path.home() / ".claude" / "skills"


def get_shadow_config(skill_name):
    """Read shadow config for a skill. Returns dict or None."""
    config_path = SKILLS_DIR / skill_name / ".shadow" / "config.json"
    if not config_path.exists():
        return None

    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        if config.get("status") != "active":
            return None
        return config
    except (json.JSONDecodeError, KeyError):
        return None


def read_skill_version(skill_name, version):
    """Read current or proposed skill version."""
    shadow_dir = SKILLS_DIR / skill_name / ".shadow"
    version_file = shadow_dir / f"SKILL.md.{version}"
    if version_file.exists():
        return version_file.read_text(encoding="utf-8")
    return ""


def log_invocation(skill_name, config):
    """Log a shadow mode invocation."""
    config["invocations"] = config.get("invocations", 0) + 1

    config_path = SKILLS_DIR / skill_name / ".shadow" / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    return config["invocations"]


def compare_routing(current_content, proposed_content, context=""):
    """Simple comparison of routing differences between versions.

    This is a lightweight comparison — it checks for structural differences
    in trigger patterns, rigor levels, and routing tables.
    Returns a dict describing the comparison.
    """
    comparison = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "invocation": 0,  # filled by caller
    }

    # Check for trigger pattern differences
    import re
    current_triggers = set(re.findall(r"(?:trigger|fires?|match)\w*[:\s]+([^\n]+)", current_content, re.IGNORECASE))
    proposed_triggers = set(re.findall(r"(?:trigger|fires?|match)\w*[:\s]+([^\n]+)", proposed_content, re.IGNORECASE))

    if current_triggers != proposed_triggers:
        comparison["trigger_diff"] = True
        comparison["added_triggers"] = list(proposed_triggers - current_triggers)
        comparison["removed_triggers"] = list(current_triggers - proposed_triggers)
    else:
        comparison["trigger_diff"] = False

    # Check for rigor level differences
    current_rigor = re.findall(r"(?:rigor|rigorous|standard|quick)\s*(?:mode|level)?", current_content, re.IGNORECASE)
    proposed_rigor = re.findall(r"(?:rigor|rigorous|standard|quick)\s*(?:mode|level)?", proposed_content, re.IGNORECASE)

    comparison["rigor_diff"] = current_rigor != proposed_rigor

    # Check for mode/routing table differences
    current_modes = set(re.findall(r"##\s+(?:Mode|Route)[:\s]+(\w+)", current_content))
    proposed_modes = set(re.findall(r"##\s+(?:Mode|Route)[:\s]+(\w+)", proposed_content))

    comparison["mode_diff"] = current_modes != proposed_modes

    # Size comparison
    comparison["current_lines"] = len(current_content.splitlines())
    comparison["proposed_lines"] = len(proposed_content.splitlines())
    comparison["size_delta"] = comparison["proposed_lines"] - comparison["current_lines"]

    return comparison


def check_graduation(skill_name, config):
    """Check if shadow period is complete and generate verdict."""
    target = config.get("target_invocations", 5)
    invocations = config.get("invocations", 0)
    comparisons = config.get("comparisons", [])

    if invocations < target:
        return None

    started = config.get("started", "unknown")

    # Analyze comparisons
    trigger_diffs = sum(1 for c in comparisons if c.get("trigger_diff"))
    rigor_diffs = sum(1 for c in comparisons if c.get("rigor_diff"))
    mode_diffs = sum(1 for c in comparisons if c.get("mode_diff"))

    total_diffs = trigger_diffs + rigor_diffs + mode_diffs
    diff_rate = total_diffs / (len(comparisons) * 3) if comparisons else 0

    # Simple verdict logic
    if diff_rate > 0.5:
        verdict = "extend"
        reasoning = f"High divergence rate ({diff_rate:.0%}) — changes are significant, need more data"
    elif diff_rate < 0.1:
        verdict = "graduate"
        reasoning = "Minimal routing differences — proposed changes are safe to adopt"
    else:
        verdict = "extend"
        reasoning = f"Moderate divergence ({diff_rate:.0%}) — extending for {target} more invocations"

    report = {
        "skill": skill_name,
        "change": config.get("change_description", "unknown"),
        "period": f"{started} -> {datetime.now().strftime('%Y-%m-%d')}",
        "invocations": invocations,
        "trigger_diffs": trigger_diffs,
        "rigor_diffs": rigor_diffs,
        "mode_diffs": mode_diffs,
        "verdict": verdict,
        "reasoning": reasoning,
    }

    # Write report
    report_path = SKILLS_DIR / skill_name / ".shadow" / "report.md"
    report_md = f"""## Shadow Mode Report: {skill_name}

Change: {report['change']}
Period: {report['period']} ({invocations} invocations)

Results:
  Trigger differences: {trigger_diffs}/{len(comparisons)} invocations
  Rigor differences: {rigor_diffs}/{len(comparisons)} invocations
  Mode differences: {mode_diffs}/{len(comparisons)} invocations

Verdict: {verdict}
Reasoning: {reasoning}
"""
    report_path.write_text(report_md, encoding="utf-8")

    if verdict == "extend":
        config["target_invocations"] = invocations + target
        config_path = SKILLS_DIR / skill_name / ".shadow" / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    return report


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    if data.get("tool_name") != "Read":
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Quick exit: only watch SKILL.md reads
    if not file_path.endswith("SKILL.md"):
        sys.exit(0)

    skills_prefix = str(SKILLS_DIR) + "/"
    if not file_path.startswith(skills_prefix):
        sys.exit(0)

    # Extract skill name
    relative = file_path[len(skills_prefix):]
    skill_name = relative.split("/")[0]

    # Check for active shadow config
    config = get_shadow_config(skill_name)
    if not config:
        sys.exit(0)

    # Log invocation
    invocation_count = log_invocation(skill_name, config)

    # Read both versions and compare
    current = read_skill_version(skill_name, "current")
    proposed = read_skill_version(skill_name, "proposed")

    if current and proposed:
        comparison = compare_routing(current, proposed)
        comparison["invocation"] = invocation_count

        # Append comparison to config
        config.setdefault("comparisons", []).append(comparison)
        config_path = SKILLS_DIR / skill_name / ".shadow" / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    # Check graduation
    report = check_graduation(skill_name, config)

    # Output: if graduation report generated, include as system message
    output = {"continue": True}
    if report and report.get("verdict"):
        output["systemMessage"] = (
            f"Shadow mode for {skill_name}: {report['verdict']}. "
            f"{report['reasoning']}. See .shadow/report.md"
        )

    print(json.dumps(output))


if __name__ == "__main__":
    main()
