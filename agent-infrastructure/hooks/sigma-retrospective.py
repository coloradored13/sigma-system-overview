#!/usr/bin/env python3
"""Sigma-Review Retrospective — Stop hook.

Fires after every Stop event. Checks if a sigma-review just completed
(workspace has agent convergence markers). If so, analyzes the review
and appends a retrospective to shared/patterns.md.

Avoids duplicates by hashing the workspace convergence section.
"""
import json
import sys
import os
import re
import hashlib
from pathlib import Path
from datetime import datetime


TEAM_DIR = Path.home() / ".claude" / "teams" / "sigma-review" / "shared"
WORKSPACE = TEAM_DIR / "workspace.md"
PATTERNS = TEAM_DIR / "patterns.md"
RETRO_STATE = TEAM_DIR / ".retro-last-hash"


def read_file(path):
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def extract_section(text, heading):
    """Extract content under a ## heading."""
    pattern = rf"^## {re.escape(heading)}$(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def count_pattern(text, pattern):
    return len(re.findall(pattern, text, re.IGNORECASE))


def analyze_workspace(content):
    """Extract metrics from workspace content."""
    convergence = extract_section(content, "convergence")
    infrastructure = extract_section(content, "infrastructure")

    # Agent value-add: count agents that converged
    agents_converged = re.findall(r"^(\S+):\s*✓", convergence, re.MULTILINE)
    agents_timeout = re.findall(r"auto-shutdown", convergence, re.IGNORECASE)

    # Herding: check for circuit breaker
    cb_fired = bool(re.search(r"circuit.?breaker|CB.?fired|herding.?detected", content, re.IGNORECASE))

    # Analytical hygiene: count outcomes
    outcome_1 = count_pattern(content, r"outcome.?1|revised from|CHECK CHANGES")
    outcome_2 = count_pattern(content, r"outcome.?2|confirmed.*risk|CHECK CONFIRMS")
    outcome_3 = count_pattern(content, r"outcome.?3|gap:|CHECK REVEALS")
    total_checks = outcome_1 + outcome_2 + outcome_3

    perfunctory_risk = "low"
    if total_checks > 0:
        confirm_ratio = outcome_2 / total_checks
        if confirm_ratio > 0.8:
            perfunctory_risk = "high"
        elif confirm_ratio > 0.6:
            perfunctory_risk = "medium"

    # DA effectiveness: look for revision markers vs concession markers
    da_revisions = count_pattern(content, r"revised|changed|updated.*(?:after|following).*DA|challenge.?accepted")
    da_concessions = count_pattern(content, r"concede|accept.*challenge|acknowledge.*point")
    da_total = da_revisions + da_concessions
    revision_rate = round(da_revisions / da_total * 100) if da_total > 0 else 0
    concession_type = "genuine" if revision_rate > 40 else "performative" if da_total > 0 else "n/a"

    # Source quality: count tier tags — match :T1/:T2/:T3 followed by non-alphanumeric
    t1_count = count_pattern(content, r":T1(?=[|\]\s(]|$)")
    t2_count = count_pattern(content, r":T2(?=[|\]\s(]|$)")
    t3_count = count_pattern(content, r":T3(?=[|\]\s(]|$)")

    # XVERIFY usage
    xverify_used = count_pattern(content, r"XVERIFY\[")
    xverify_failed = count_pattern(content, r"XVERIFY-FAIL")
    xverify_available = bool(re.search(r"ΣVerify.*available|sigma.?verify.*available", infrastructure, re.IGNORECASE))

    # Complexity: look for TIER assessment
    tier_match = re.search(r"TIER-(\d)", content)
    tier_assessed = int(tier_match.group(1)) if tier_match else 0

    # Task slug
    task_match = re.search(r"##\s*task\s*\n+(.*?)(?:\n|$)", content, re.IGNORECASE)
    task_slug = task_match.group(1).strip()[:60] if task_match else "unknown"

    return {
        "task_slug": task_slug,
        "agents_converged": agents_converged,
        "agents_timeout": len(agents_timeout),
        "cb_fired": cb_fired,
        "outcome_1": outcome_1,
        "outcome_2": outcome_2,
        "outcome_3": outcome_3,
        "perfunctory_risk": perfunctory_risk,
        "revision_rate": revision_rate,
        "concession_type": concession_type,
        "t1": t1_count,
        "t2": t2_count,
        "t3": t3_count,
        "xverify_used": xverify_used,
        "xverify_failed": xverify_failed,
        "xverify_available": xverify_available,
        "tier_assessed": tier_assessed,
    }


def generate_recommendation(metrics):
    """One actionable suggestion based on metrics."""
    if metrics["perfunctory_risk"] == "high":
        return "High outcome-2 ratio — checks may be rubber-stamping. DA should probe specifics."
    if metrics["concession_type"] == "performative" and metrics["revision_rate"] < 20:
        return "DA challenges producing low revision rate — challenges may be formulaic or agents conceding without changing."
    if metrics["t3"] > metrics["t1"] + metrics["t2"]:
        return "T3 sources dominate — push agents toward T1/T2 primary sources for load-bearing findings."
    if metrics["xverify_available"] and metrics["xverify_used"] == 0:
        return "ΣVerify available but unused — check if agents are skipping cross-model verification."
    if len(metrics["agents_converged"]) <= 2:
        return "Low agent convergence count — check if agents are stalling or timing out."
    if not metrics["cb_fired"] and len(metrics["agents_converged"]) > 3:
        return "No circuit breaker with 4+ agents — verify genuine divergence exists (not just surface-level agreement)."
    return "Review metrics within normal ranges — no immediate action."


def write_retro(metrics):
    """Append retrospective to patterns.md."""
    date = datetime.now().strftime("%Y-%m-%d")
    review_num_match = re.search(r"R(\d+)", read_file(PATTERNS))
    last_num = int(review_num_match.group(1)) if review_num_match else 0
    review_num = last_num + 1

    agents_str = ", ".join(metrics["agents_converged"]) if metrics["agents_converged"] else "none detected"
    recommendation = generate_recommendation(metrics)

    entry = f"""
## Retro: R{review_num} — {metrics['task_slug']} ({date})
value: {agents_str} converged ({metrics['agents_timeout']} timeouts)
herding: {'CB fired' if metrics['cb_fired'] else 'not detected'}, CB fired: {'yes' if metrics['cb_fired'] else 'no'}
hygiene: outcome-1: {metrics['outcome_1']}, outcome-2: {metrics['outcome_2']}, outcome-3: {metrics['outcome_3']} — perfunctory risk: {metrics['perfunctory_risk']}
da-effectiveness: revision-rate: {metrics['revision_rate']}%, concession-type: {metrics['concession_type']}
sources: T1:{metrics['t1']} T2:{metrics['t2']} T3:{metrics['t3']}
xverify: used:{metrics['xverify_used']} failed:{metrics['xverify_failed']} available:{'yes' if metrics['xverify_available'] else 'no'}
complexity: tier-assessed: {metrics['tier_assessed']}
-> recommendation: {recommendation}
"""

    with open(PATTERNS, "a", encoding="utf-8") as f:
        f.write(entry)


def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        data = {}

    # Quick exit if not a Stop event
    if data.get("hook_event_name") != "Stop":
        sys.exit(0)

    # Check if workspace exists and has convergence markers
    workspace_content = read_file(WORKSPACE)
    if not workspace_content:
        sys.exit(0)

    convergence = extract_section(workspace_content, "convergence")
    if "✓" not in convergence:
        sys.exit(0)

    # Dedup: hash convergence section, skip if already retro'd
    content_hash = hashlib.sha256(convergence.encode()).hexdigest()[:16]
    last_hash = read_file(RETRO_STATE).strip()
    if content_hash == last_hash:
        sys.exit(0)

    # Run retrospective
    metrics = analyze_workspace(workspace_content)
    write_retro(metrics)

    # Save hash to prevent duplicate retros
    RETRO_STATE.write_text(content_hash, encoding="utf-8")

    # Non-blocking output
    print(json.dumps({"continue": True}))


if __name__ == "__main__":
    main()
