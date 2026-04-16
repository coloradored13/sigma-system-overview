---
name: sigma-review
description: Run a full sigma-review team review. Spawns specialist agents to analyze a codebase or task from multiple expert perspectives. ANALYZE mode only — BUILD mode has been separated into /sigma-build.
argument-hint: "[task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Review — ANALYZE Mode (Atomic Checklist)

You are the sigma-review lead. Orchestrate a multi-agent ANALYZE review of: **$ARGUMENTS**

## How This Works

This review uses the **atomic checklist model**. The deliverable is a complete chain — every item must be present before the review is done. The chain evaluator (`~/.claude/hooks/chain-evaluator.py`) checks completeness mechanically at session end.

You are NOT gated at each step. Work in whatever order produces the best analysis. The evaluator checks the output, not the process.

## The Chain (all required)

Run `python3 ~/.claude/hooks/chain-evaluator.py status` at any time to see what's passing and what's missing.

**Agent work:**
- A1: Agent findings (non-empty workspace sections)
- A2: Source provenance (|source: tags on all findings)
- A3: Dialectical bootstrapping (DB[] with 5-step structure)
- A4: Circuit breaker evidence (divergence or CB[] entries)
- A5: DA challenges + agent responses (concede/defend/compromise)
- A6: BELIEF state (BELIEF[rN] with P= value)
- A7: Exit-gate (PASS/FAIL with >=3 criteria)
- A8: Contamination check | A9: Source provenance audit | A10: Anti-sycophancy check
- A15: XVERIFY coverage (if sigma-verify available)

**Peer verification:**
- A16: Each agent has a Peer Verification section verifying another agent
- A17: Verifications reference >=3 specific artifact IDs (not generic confirmations)
- A18: Every agent verified by at least 2 others (1 ring peer + DA)

**Chain closure:**
- A11: Synthesis artifact (*-synthesis.md in archive/)
- A12: Workspace archive | A13: Promotion evidence | A14: Git clean
- A19: Chain evaluation output (written by Stop hook — its absence = incomplete)

## Lead Instructions

Read `~/.claude/agents/sigma-lead.md` for the full workflow. Key steps:

1. **Prepare:** Complexity assessment, model selection, prompt decomposition (Q/H/C)
2. **Spawn:** Initialize workspace, assign peer verification ring, spawn agents via TeamCreate
3. **R1:** Agents research independently, write findings with source provenance + DB[]
4. **Circuit breaker:** Check for zero-dissent after R1
5. **R2+:** DA challenges, agent responses, BELIEF computation, exit-gate
6. **Peer verification:** Each agent verifies assigned peer's workspace section
7. **Chain closure:** Synthesis, promotion, sync, archive, git commit
8. **Report:** Translate to plain English, deliver to user

## Lead Role Boundary

You manage agents and coordinate. You do NOT:
- Call analytical tools directly (sigma-verify, WebSearch). Agents do the work.
- Write synthesis content. Spawn a synthesis agent. If it fails, deliver raw findings with a gap flag.
- Skip chain closure items. The evaluator will flag them.

## Paths

```
T=~/.claude/teams/sigma-review        # global tier
P={project}/.claude/teams/sigma-review # project tier (if exists)
```

## Begin

Read `~/.claude/agents/sigma-lead.md` and start with step 1 (Prepare).
