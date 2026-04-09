---
name: sigma-init
description: Initialize the sigma-review system for the current project, or create a new agent from YAML config. Use "/sigma-init" for project setup, "/sigma-init agent <name>" to create agent from YAML template.
argument-hint: "[project description] or 'agent <name>'"
disable-model-invocation: true
allowed-tools: Read, Bash, Write, Edit, Glob, Grep
---

# Sigma Init — Project Kickoff & Agent Creation

## Route

Parse $ARGUMENTS:
- starts with "agent" → go to **Agent Creation** section
- otherwise → go to **Project Setup** section

---

## Agent Creation

Create a new sigma-review agent from YAML config.

### If user provides agent name only: `/sigma-init agent supply-chain-analyst`

1→copy template: `~/Projects/sigma-system-overview/agent-infrastructure/templates/agent-config.yaml`
2→create working copy at `/tmp/{name}-config.yaml`
3→pre-fill name field with provided name
4→present to user:
  "I've created a YAML config template for **{name}**. Edit the fields below:"
  show the YAML with comments explaining each field
5→wait for user edits (or ask field-by-field interactively)
6→run conversion:
  ```bash
  python3 ~/Projects/sigma-system-overview/agent-infrastructure/scripts/yaml-to-agent.py /tmp/{name}-config.yaml --install
  ```
7→report: show generated agent file path + roster entry
8→offer: "Run research for this agent? (`/sigma-research {name}`)"

### If user provides YAML path: `/sigma-init agent /path/to/config.yaml`

1→validate YAML has required fields (name, role, expertise, domain, wake-for)
2→run conversion:
  ```bash
  python3 ~/Projects/sigma-system-overview/agent-infrastructure/scripts/yaml-to-agent.py /path/to/config.yaml --install
  ```
3→report results

### Two modes
- **Standard mode**: YAML config → auto-generated .md (for new users, quick agent creation)
- **Power mode**: edit .md files directly with full ΣComm (for optimization, custom protocols)

The YAML template handles all ΣComm boilerplate. Users only write: name, role, expertise, domain, wake-for, review steps, weight.

---

## Project Setup

Initialize sigma-review for this project. Project context: **$ARGUMENTS**

## Pre-flight

1→verify global setup exists:
  - `~/.claude/teams/sigma-review/` directory
  - `~/.claude/teams/sigma-review/shared/roster.md`
  - `~/.claude/agents/sigma-lead.md`
  - `~/.claude/skills/sigma-review/SKILL.md`
  ¬exists → tell user: "Run setup.sh from sigma-system-overview first"

2→check if project already initialized:
  - `.claude/teams/sigma-review/` exists → report "already initialized" + verify integrity
  - ¬exists → proceed with setup

## Step 1: Create Project Team Structure

Run the setup-project.sh script from sigma-system-overview:

```bash
SCRIPT=~/Projects/sigma-system-overview/setup-project.sh
[ -f "$SCRIPT" ] && bash "$SCRIPT" || echo "setup-project.sh not found"
```

If setup-project.sh is not found, create the structure manually:

```
.claude/teams/sigma-review/
  shared/decisions.md     — "# project decisions — expertise-weighted"
  shared/patterns.md      — "# project patterns — cross-agent"
  shared/portfolio.md     — "# portfolio — review history"
  shared/workspace.md     — (see workspace template below)
  shared/wiki/INDEX.md    — "# Knowledge Wiki Index"
  shared/archive/         — (empty directory for workspace archives)
  shared/snapshots/       — (empty directory for orchestrator snapshots)
  agents/{name}/memory.md — "# {name} — project memory"  (for each agent in roster)
  inboxes/{name}.md       — "# inbox — {name}\n## processed\n## unread"
```

Workspace template (shared/workspace.md):
```markdown
# workspace
## status: idle
## mode: ANALYZE
## task
## infrastructure
## prompt-decomposition
## findings
## convergence
## compilation
## promotion
## open-questions
```

Also copy orchestrator infrastructure if available:
```bash
SRC=~/Projects/sigma-system-overview/agent-infrastructure/teams/sigma-review/shared
[ -f "$SRC/orchestrator-config.py" ] && cp "$SRC/orchestrator-config.py" .claude/teams/sigma-review/shared/
[ -f "$SRC/gate_checks.py" ] && cp "$SRC/gate_checks.py" .claude/teams/sigma-review/shared/
[ -f "$SRC/protocols.md" ] && cp "$SRC/protocols.md" .claude/teams/sigma-review/shared/
```

Add `.claude/teams/` to `.gitignore` if not already present.

## Step 2: Create Project CLAUDE.md

Create or append to `.claude/CLAUDE.md` in the project root. Check for existing content first — append sigma section if file exists, create if not.

Only add this section if the marker `# Sigma System` is not already present.

Read the roster at `~/.claude/teams/sigma-review/shared/roster.md` to get the current agent list. Then generate:

```markdown
# Sigma System

This project uses sigma-review for multi-agent expert reviews.

## Commands
- `/sigma-review <task>` — Full ANALYZE team review (phase-based, multi-agent)
- `/sigma-build <task>` — Full BUILD team review (plan→challenge→build→review)
- `/sigma-single <task>` — Enhanced single-instance analysis (below triage boundary)
- `/sigma-audit [workspace]` — Independent process quality audit of a review
- `/sigma-feedback [correction]` — Post-review calibration loop
- `/sigma-evaluate [workspace]` — Multi-agent rubric evaluation of analysis quality
- `/sigma-research [agent-name]` — Refresh domain research for one or all agents
- `/sigma-dream [scope] [apply]` — Memory consolidation cycle

## Agents available
{read from roster — list each agent with domain summary}

## Memory
Two-tier memory is active:
- **Global** (`~/.claude/teams/sigma-review/`): agent identity, research, calibration
- **Project** (`.claude/teams/sigma-review/`): findings, decisions, patterns specific to this codebase

recall via sigma-mem MCP auto-detects the project tier.
```

## Step 3: Validate

1→call validate_system(team:sigma-review) via sigma-mem MCP
2→verify all agents have:
  - global memory file
  - project memory file
  - inbox file
3→verify infrastructure:
  - shared/wiki/INDEX.md exists
  - shared/archive/ directory exists
  - shared/workspace.md has required sections (## status, ## task, ## infrastructure, ## findings, ## convergence, ## promotion)
  - orchestrator-config.py exists (warn if missing — phase advancement won't work)
4→report any issues

## Step 4: Report

Tell the user:

```
Sigma system initialized for this project.

Created:
  .claude/teams/sigma-review/   — project-tier team data
  .claude/CLAUDE.md             — sigma system instructions (appended)

Infrastructure:
  workspace.md    — phase-based workspace with all required sections
  wiki/           — persistent knowledge wiki (compounding across reviews)
  archive/        — workspace archives (for audit + feedback)
  orchestrator    — {installed|missing — install from sigma-system-overview}

You can now run:
  /sigma-review <task>     — full ANALYZE team review
  /sigma-build <task>      — full BUILD team review
  /sigma-single <task>     — enhanced single-instance analysis
  /sigma-research          — refresh agent domain research

Project context: {$ARGUMENTS if provided}
```

If the user provided a project description via $ARGUMENTS, suggest an initial review:
"Want me to run `/sigma-review` on this project now?"
