#!/usr/bin/env python3
"""Convert a YAML agent config to a full ΣComm agent .md definition.

Usage:
  python3 yaml-to-agent.py config.yaml                     # print to stdout
  python3 yaml-to-agent.py config.yaml -o agents/           # write to directory
  python3 yaml-to-agent.py config.yaml -o agents/name.md    # write to specific file
  python3 yaml-to-agent.py config.yaml --roster             # also print roster entry
  python3 yaml-to-agent.py config.yaml --install            # write to ~/.claude/agents/ + update roster
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def generate_agent_md(cfg: dict) -> str:
    """Generate a full ΣComm agent .md file from a YAML config."""
    name = cfg["name"]
    role = cfg["role"]
    expertise = cfg["expertise"].strip()
    review_steps = cfg.get("review_steps", [])
    build_steps = cfg.get("build_review_steps", [])
    weight_primary = cfg.get("weight_primary", cfg.get("domain", ""))
    weight_principle = cfg.get("weight_principle", "")
    extra = cfg.get("extra_sections", "")

    # Build review section
    review_lines = []
    for i, step in enumerate(review_steps, 1):
        review_lines.append(f"{i}→{step}")
    review_section = "\n".join(review_lines)

    build_section = ""
    if build_steps:
        build_lines = []
        for i, step in enumerate(build_steps, 1):
            build_lines.append(f"{i}→{step}")
        build_section = f"""
## Review (BUILD)
{chr(10).join(build_lines)}
"""

    extra_section = ""
    if extra and extra.strip():
        extra_section = f"\n{extra.strip()}\n"

    md = f"""# {_title_case(name)} Agent

## Role
{role}

## Expertise
{expertise}

## Boot (FIRST)
self-sufficient: read own state from paths.
1→sigma-comm.md — comms protocol
2→memory.md — identity+findings+calibration
3→inbox — process unread→summarize(ΣComm)→clear
4→workspace.md — task+peer-findings
5→decisions.md — settled choices
6→directives.md — team directives (adversarial layer + dynamic agent orchestration)

## Comms
peers→ΣComm via inbox (include ¬,→,#count) | user→plain in open-questions | workspace→YOUR section, ΣComm

## Review (ANALYZE)
{review_section}
{build_section}
## Persistence (before ✓, no direct file writes)
1. store_agent_memory(tier:project, agent:{name}, team:sigma-review) → codebase findings ΣComm
2. store_agent_memory(tier:global, agent:{name}, team:sigma-review) → R[]/C[]/identity if updated
3. store_team_decision(by:{name}, weight:primary|advisory, team:sigma-review) → domain decisions
4. store_team_pattern(team:sigma-review, agents:[names]) → cross-agent patterns
persist complete → 5. promotion (if lead signals promotion-round) → declare ✓

## Promotion (when lead signals promotion-round)

### classify your findings
auto-promote: calibration-self-update | pattern-confirms-existing | research-supplement
user-approve: new-principle | anti-pattern-new | contradicts-global | new-global-decision | behavior-change

### check global memory
get_agent_memory(team:sigma-review, agent:{name}) → read global P[]/C[]/R[]
¬duplicate: skip if P[] with same finding exists
contradicts existing P[]/C[]/R[] → reclassify as user-approve

### auto-promote
per auto item:
  distill: compress finding→generalizable learning (¬project-specific detail, keep project name as src)
  store_agent_memory(tier:global, agent:{name}, team:sigma-review):
    P[{{distilled}}|src:{{project-name}}|promoted:{{date}}|class:{{pattern|calibration}}]

### submit for approval
per user-approve item:
  workspace ## promotion → candidates:
    P-candidate[{{distilled}}|class:{{type}}|agent:{name}|reason:{{why-generalizable}}]
  SendMessage(recipient:lead): ◌ promotion: {{N}} auto-stored, {{M}} need-approval |→ workspace ## promotion

## Research
memory ## research: ΣComm domain knowledge. reference during reviews.
verify needed → flag:
```
→ want-to-research: {{topic}} |reason: {{why this matters for the current review}}
```
lead surfaces to user. ¬research inline — flag+continue.

## Convergence
When done, write your status to workspace convergence section:
```
{name}: ✓ {{summary}} |{{key-findings}} |→ {{what-you-can-do-next}}
```

## Weight
primary: {weight_primary} | outside domain→advisory, defer to expert
{weight_principle}

## Domain Gap Reporting
if domain gap found → lead inbox:
  "agent-request: [role] |domain: [expertise] |gap: [uncovered question] |trigger: [workspace entry] |impact: [deliverable change] |→ lead: approve|deny|merge"
¬request for: single-web-search answers | existing-agent domains | >3 dynamic per task

## Analytical Hygiene (mandatory — all reviews, all builds)

before declaring convergence (ANALYZE) or plan-complete (BUILD), verify:
  □ positioning/consensus check completed — result is outcome 1, 2, or 3 (see directives.md §2)
  □ calibration/precedent check completed — result is outcome 1, 2, or 3
  □ cost/complexity check completed — result is outcome 1, 2, or 3

every check MUST produce one of:
  1→ CHECK CHANGES THE ANALYSIS → revise finding BEFORE workspace write
     format: "[finding] — revised from [original] because §2[a/b/c] found [evidence]"
  2→ CHECK CONFIRMS WITH ACKNOWLEDGED RISK → write finding WITH counterweight
     format: "[finding] — §2[a/b/c] flag: [concern]. Maintained because: [specific evidence, ¬reassurance]"
     !test: would DA accept your justification, or would they challenge it?
  3→ CHECK REVEALS GAP → flag for DA/lead/specialist
     format: "[finding] — §2[a/b/c] gap: [what you can't assess]. Flagged for: [DA/lead/specialist]"

!rule: no finding goes to workspace without its check result attached
¬optional — DA will flag missing or perfunctory checks as process violation
{extra_section}"""

    return md.strip() + "\n"


def generate_roster_entry(cfg: dict) -> str:
    """Generate a roster.md entry from config."""
    name = cfg["name"]
    domain = cfg.get("domain", "")
    wake = cfg.get("wake-for", "")
    return f"{name} |domain: {domain} |wake-for: {wake}"


def _title_case(name: str) -> str:
    """Convert hyphenated name to title case."""
    return " ".join(w.capitalize() for w in name.split("-"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert YAML agent config to ΣComm agent .md"
    )
    parser.add_argument("config", help="Path to YAML config file")
    parser.add_argument("-o", "--output", help="Output path (directory or file)")
    parser.add_argument(
        "--roster", action="store_true", help="Also print roster entry"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install to ~/.claude/agents/ and append to roster",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)

    # Validate required fields
    for field in ("name", "role", "expertise", "domain", "wake-for"):
        if field not in cfg:
            print(f"Error: missing required field '{field}'", file=sys.stderr)
            sys.exit(1)

    md = generate_agent_md(cfg)
    roster_entry = generate_roster_entry(cfg)

    if args.install:
        # Write agent file
        agent_path = Path.home() / ".claude" / "agents" / f"{cfg['name']}.md"
        agent_path.write_text(md)
        print(f"Installed: {agent_path}")

        # Append to roster
        roster_path = (
            Path.home()
            / ".claude"
            / "teams"
            / "sigma-review"
            / "shared"
            / "roster.md"
        )
        if roster_path.exists():
            content = roster_path.read_text()
            # Insert before the → actions footer
            if "→ actions:" in content:
                content = content.replace(
                    "→ actions:",
                    f"{roster_entry}\n\n→ actions:",
                )
            else:
                content = content.rstrip() + f"\n{roster_entry}\n"
            roster_path.write_text(content)
            print(f"Roster updated: {roster_path}")
        else:
            print(f"Warning: roster not found at {roster_path}", file=sys.stderr)

        print(f"\nRoster entry:\n  {roster_entry}")

    elif args.output:
        out = Path(args.output)
        if out.is_dir():
            out = out / f"{cfg['name']}.md"
        out.write_text(md)
        print(f"Written: {out}")
    else:
        print(md)

    if args.roster and not args.install:
        print(f"\n# Roster entry:\n{roster_entry}")


if __name__ == "__main__":
    main()
