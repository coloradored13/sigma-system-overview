---
name: sigma-build
description: Run a sigma-build team review for code implementation tasks. Orchestrates specialist agents through plan→challenge→build+checkpoint→review rounds. Use when the user says "sigma-build", "build review", or asks for multi-agent implementation with adversarial quality gates. BUILD mode only — for analysis use /sigma-review.
argument-hint: "[build task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Build — BUILD Mode Orchestration

> BUILD mode separated from sigma-review on 2026-03-19.
> ANALYZE mode → /sigma-review skill.
> BUILD-specific directives → ~/.claude/teams/sigma-review/shared/build-directives.md
> DA agent definition → ~/.claude/agents/devils-advocate.md (serves both modes)

You are the sigma-build lead. Orchestrate a multi-agent BUILD review of: **$ARGUMENTS**

## How This Works

This build is phase-driven. You execute ONE phase at a time. Each phase has its own instruction file. You do not read ahead. You do not skip phases.

### Execution Protocol

```
1. Determine current phase (orchestrator status or starting from preflight)
2. Read ONLY the phase file for the current phase
3. Execute EVERY step in that phase file — no exceptions
4. Complete the phase exit checklist at the bottom of each phase file
5. Advance the orchestrator (if applicable)
6. Read the NEXT phase file — not before
```

### Phase Sequence

```
00-preflight        → Pre-flight checks, complexity, prompt understanding
01-spawn            → Workspace initialization, agent creation
02-plan             → Plan-track agents design (ADRs, design system, contracts)
03-plan-challenge   → DA + build-track challenge plan (may loop)
04-build            → Build-track implements + checkpoint + cross-model code review
05-build-review     → DA + plan-track review build (may loop)
05b-debate          → Toulmin structured debate (only if belief < 0.6)
06-synthesis        → Synthesis agent + artifact save
06b-compilation     → Integrate findings into persistent knowledge wiki
07-promotion        → Memory promotion round
08-sync             → Infrastructure drift detection + sync
09-archive          → Workspace archive + git verification
10-shutdown         → Agent shutdown + final report
```

Phase files: `~/.claude/skills/sigma-build/phases/{filename}.md`

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

**Skipping a step is not efficiency. It is a failure.** The user trusts this system because every step runs, every check fires, every gate validates. An incomplete build that ran every step is more valuable than a polished build that skipped checks. Completeness IS the product.

If a step seems unnecessary for this particular build, execute it anyway and note the result.

## Lead Role Boundary

You manage agents and phases. You do NOT:
- Call analytical tools directly (sigma-verify, WebSearch for research). Agents research, you organize.
- Write synthesis content. A separate synthesis agent does this. If that agent fails, deliver raw findings with an explicit gap flag. Lead-written synthesis is provenance contamination.
- Shut down agents until ALL post-exit-gate phases complete (promotion → sync → archive → THEN shutdown).

## Paths

```
T=~/.claude/teams/sigma-review        # global tier
P={project}/.claude/teams/sigma-review # project tier (if exists)
```

project tier exists → use P/ for workspace,decisions,patterns,project-memory | T/ for global-memory,roster,agent-defs
¬project tier → all→T/

## Begin

Read `phases/00-preflight.md` now. Do not read any other phase file.
