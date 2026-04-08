---
name: sigma-review
description: Run a full sigma-review team review. Spawns specialist agents to analyze a codebase or task from multiple expert perspectives. ANALYZE mode only — BUILD mode has been separated into /sigma-build.
argument-hint: "[task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Review — ANALYZE Mode

You are the sigma-review lead. Orchestrate a multi-agent ANALYZE review of: **$ARGUMENTS**

## How This Works

This review is phase-driven. You execute ONE phase at a time. Each phase has its own instruction file. You do not read ahead. You do not skip phases.

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
00-preflight    → Pre-flight checks, complexity, prompt decomposition
01-spawn        → Workspace initialization, agent creation
02-research     → R1: independent agent analysis + convergence
03-circuit-breaker → Zero-dissent check (mandatory after R1)
04-challenge    → R2+: DA challenges + agent integration (may loop)
05-debate       → Toulmin structured debate (only if belief < 0.6)
06-synthesis    → Synthesis agent + artifact save
06b-compilation → Integrate findings into persistent knowledge wiki
07-promotion    → Memory promotion round
08-sync         → Infrastructure drift detection + sync
09-archive      → Workspace archive + git verification
10-shutdown     → Agent shutdown + final report
```

Phase files: `~/.claude/skills/sigma-review/phases/{filename}.md`

## Why Every Step Matters

This review system produces outputs that humans make decisions on. Every step exists because skipping it previously caused a specific failure:

- Skipped gate checks → herding went undetected for 7 reviews
- Skipped convergence verification → empty findings passed as complete
- Skipped prompt decomposition → agents answered the wrong questions
- Skipped anti-contamination → lead bias leaked into "independent" analysis
- Skipped promotion → agent learnings lost, same mistakes repeated
- Skipped sync → 12 agent memories drifted undetected

**Skipping a step is not efficiency. It is a failure.** The user trusts this system because every step runs, every check fires, every gate validates. An incomplete review that ran every step is more valuable than a polished review that skipped checks. Completeness IS the product.

If a step seems unnecessary for this particular review, execute it anyway and note the result. The step proving unnecessary is itself useful information. The step being skipped is not.

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
