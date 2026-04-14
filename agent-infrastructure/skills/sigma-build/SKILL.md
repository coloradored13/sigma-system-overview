---
name: sigma-build
description: Run a sigma-build team review for code implementation tasks. Orchestrates specialist agents through plan→challenge→build→review across 3 separate conversations. Use when the user says "sigma-build", "build review", or asks for multi-agent implementation with adversarial quality gates. BUILD mode only — for analysis use /sigma-review.
argument-hint: "[build task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Build — 3-Conversation BUILD Orchestration

> BUILD mode separated from sigma-review on 2026-03-19.
> Restructured from 13-phase monolith to 3-conversation model on 2026-04-13.
> ANALYZE mode → /sigma-review skill.
> BUILD-specific directives → ~/.claude/teams/sigma-review/shared/build-directives.md
> DA agent definition → ~/.claude/agents/devils-advocate.md (serves both modes)

You are the sigma-build lead. Orchestrate a multi-agent BUILD of: **$ARGUMENTS**

## Architecture

Each build runs across 3 separate conversations. The conversation boundary IS the gate — you cannot skip DA challenge because Phase 2 requires a plan file that only exists after DA exit-gate PASS.

```
Conversation 1: PLAN    →  preflight, spawn, plan design, DA + build-track challenge → locked plan file
Conversation 2: BUILD   →  pure execution against locked plan → code + tests
Conversation 3: REVIEW  →  DA + plan-track review build, code fixes, synthesis, close-out
```

**Plan file** bridges conversations: `~/.claude/teams/sigma-review/shared/builds/{date}-{task-slug}.plan.md`
**sigma-mem** bridges institutional memory (calibration, patterns, lessons)
**Scratch workspace** is ephemeral per conversation: `builds/{build-id}/c{N}-scratch.md`

## Routing

Determine which conversation to run based on the plan file state.

### Step 1: Search for existing plan file

```
Search: ~/.claude/teams/sigma-review/shared/builds/*.plan.md
Match: $ARGUMENTS against plan file ## Meta build-id and ## Context
```

### Step 2: Route based on plan file status

```
No matching plan file found
  → This is a NEW build. Run Conversation 1 (PLAN).
  → Read phases/c1-plan.md now.

Match found — read ## Meta section:

  status: plan
    → C1 in progress or interrupted. Resume Conversation 1 (PLAN).
    → Read phases/c1-plan.md now.

  status: plan-locked AND plan-exit-gate: PASS
    → Plan approved. Run Conversation 2 (BUILD).
    → Read phases/c2-build.md now.

  status: built
    → Build complete. Run Conversation 3 (REVIEW).
    → Read phases/c3-review.md now.

  status: closing
    → C3 in progress or interrupted. Resume Conversation 3 (REVIEW).
    → Read phases/c3-review.md now.

  status: complete
    → Build already finished.
    → Report: "Build {build-id} complete. Archive at {archive-path}."
    → Offer: "Run /sigma-build {new task} to start a new build."
```

### Step 3: Handle multiple matches

If multiple plan files match $ARGUMENTS:
```
Multiple builds match "$ARGUMENTS":
1. {build-id-1} (status: {status}, plan-exit-gate: {gate})
2. {build-id-2} (status: {status}, plan-exit-gate: {gate})
Select build [1-N] or "new" to start fresh:
```

### Step 4: Handle --phase override (optional)

User can force a specific phase: `/sigma-build --phase plan {task}` or `/sigma-build --phase build {task}` or `/sigma-build --phase review {task}`.

## Why Every Step Matters

This build system produces code that humans ship to production. Every step exists because skipping it previously caused a specific failure:

- Skipped gate checks → herding went undetected for 7 reviews
- Skipped convergence verification → empty findings passed as complete
- Skipped prompt understanding → agents built the wrong thing
- Skipped plan challenge → scope creep discovered at build review instead of plan phase
- Skipped checkpoint → architectural drift caught too late to fix cheaply
- Skipped anti-contamination → lead bias leaked into "independent" analysis
- Skipped promotion → agent learnings lost, same mistakes repeated
- Skipped sync → 12 agent memories drifted undetected
- **Ran all phases in one conversation → context degraded, DA never spawned, build shipped unchallenged (B7 RED audit)**

**Skipping a step is not efficiency. It is a failure.** The user trusts this system because every step runs, every check fires, every gate validates. An incomplete build that ran every step is more valuable than a polished build that skipped checks. Completeness IS the product.

## Lead Role Boundary

You manage agents and phases. You do NOT:
- Call analytical tools directly (sigma-verify, WebSearch for research). Agents research, you organize.
- Write synthesis content. A separate synthesis agent does this (C3 only). Lead-written synthesis is provenance contamination.
- Skip conversation exit protocol. Every conversation has a formal exit that writes to the plan file.
- Dispatch implementation work before the plan is locked. The plan file with exit-gate: PASS is the build authorization.

## Paths

```
T=~/.claude/teams/sigma-review        # global tier
P={project}/.claude/teams/sigma-review # project tier (if exists)
B=T/shared/builds                     # plan files and scratch workspaces
```

project tier exists → use P/ for decisions,patterns,project-memory | T/ for global-memory,roster,agent-defs
¬project tier → all→T/

## Begin

Execute the routing logic above. Read ONLY the phase file for the determined conversation. Do not read any other phase file.
