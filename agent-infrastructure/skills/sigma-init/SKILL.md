---
name: sigma-init
description: Initialize the sigma-review system for the current project. Creates two-tier memory structure, project CLAUDE.md with sigma instructions, and validates the setup. Use when starting a new project with sigma-review.
argument-hint: "[project description]"
disable-model-invocation: true
allowed-tools: Read, Bash, Write, Edit, Glob, Grep
---

# Sigma Init — Project Kickoff

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
# Find setup-project.sh — check common locations
SCRIPT=$(find ~/Projects/sigma-system-overview -name "setup-project.sh" -maxdepth 1 2>/dev/null | head -1)
if [ -z "$SCRIPT" ]; then
  # Try to locate it via the sigma-mem package
  SCRIPT=$(python3 -c "import sigma_mem, os; print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sigma_mem.__file__)))), 'setup-project.sh'))" 2>/dev/null)
fi
bash "$SCRIPT"
```

If setup-project.sh is not found, create the structure manually:

```
.claude/teams/sigma-review/
  shared/decisions.md     — "# project decisions — expertise-weighted"
  shared/patterns.md      — "# project patterns — cross-agent"
  shared/workspace.md     — "# workspace\n## status: idle\n## task"
  agents/{name}/memory.md — "# {name} — project memory"  (for each agent in roster)
  inboxes/{name}.md       — "# inbox — {name}\n## processed\n## unread"
```

Add `.claude/teams/` to `.gitignore` if not already present.

## Step 2: Create Project CLAUDE.md

Create or append to `.claude/CLAUDE.md` in the project root. Check for existing content first — append sigma section if file exists, create if not.

Only add this section if the marker `# Sigma System` is not already present:

```markdown
# Sigma System

This project uses sigma-review for multi-agent expert reviews.

## Commands
- `/sigma-review <task>` — Full team review (e.g., `/sigma-review Review the authentication flow`)
- `/sigma-research [agent-name]` — Refresh domain research for one or all agents
- `@agent-name question` — Direct question to a specific agent

## Agents available
- **tech-architect** — architecture, security, performance, API design
- **product-strategist** — market, growth, prioritization, launch readiness
- **ux-researcher** — usability, accessibility, mental models, learnability
- **code-quality-analyst** — code quality, test coverage, style, edge cases
- **technical-writer** — documentation, narrative, examples, onboarding

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
3→report any issues

## Step 4: Report

Tell the user:

```
Sigma-review initialized for this project.

Created:
  .claude/teams/sigma-review/   — project-tier team data
  .claude/CLAUDE.md             — sigma system instructions (appended)

You can now run:
  /sigma-review <task>     — full multi-agent review
  /sigma-research          — refresh agent domain research
  @agent-name question     — ask a specific agent

Project context: {$ARGUMENTS if provided}
```

If the user provided a project description via $ARGUMENTS, suggest an initial review:
"Want me to run `/sigma-review` on this project now?"
