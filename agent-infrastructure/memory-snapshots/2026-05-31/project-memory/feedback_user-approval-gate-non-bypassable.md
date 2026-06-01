---
name: User-approval gate is non-bypassable even when MCP flaps
description: When lead persists agent learnings on behalf of agents (MCP-flap fallback), the auto-vs-user-approve classification gate STILL APPLIES; lead-attribution does not bypass user-approval; conflating those is a contamination vector
type: feedback
originSessionId: aed6a849-4d9f-46ed-9dda-4ee49715e05e
---
When sigma-mem MCP flaps and lead invokes the c1-plan.md:587 fallback ("lead persists from scratch with source attribution"), the lead must STILL:
1. Classify each entry as auto-promote (calibration-self-update | pattern-confirms-existing | research-supplement) or user-approve (new-principle | anti-pattern-new | contradicts-global | new-global-decision | behavior-change)
2. Write user-approve entries as P-candidates to scratch ## promotion section with reason-why-generalizable
3. Surface to user with explicit ask for approval
4. Wait for disposition before writing to global memory tier

**Why:** the MCP-fallback path is meant to PRESERVE agent learnings when MCP is unavailable for the agent's own write. It is NOT meant to BYPASS the auto-vs-user-approve classification and user-approval gate. These are two independent concerns — the classification gate exists because "is this a durable team principle" is a judgment call requiring human review, regardless of who writes the bytes. Silently elevating new-principle entries to global memory without user approval is a contamination vector: future agents read global memory as established team practice; principles compound across builds; the user loses control of their own behavior-system evolution. User caught this at end of shared-process-hardening C1 build (2026-04-28) and explicitly flagged it as "huge contamination vector, not something to lightly skip."

**How to apply:**
- Lead's Step 33 promotion checklist when MCP is flapping: read each agent's section + scratch ## promotion candidates + classify each into auto-promote vs user-approve. Do NOT collapse classification into the persistence transport choice.
- For user-approve items, write P-candidate entries to scratch ## promotion with `reason:` field. Surface in lead-to-user report with explicit ask. Do not auto-elevate.
- For auto-promote items, lead-attribution to patterns.md is fine; tag with `|source:{agent}-c1-{date}|`.
- Watch for the rationalization "MCP failed, just write everything from scratch with attribution" — that's the failure mode. The transport-failure does not authorize a classification skip.
- Mechanical reinforcement (proposed): future chain-evaluator gate detecting lead-attribution writes to patterns.md without matching ## promotion P-candidate entries → WARN-first calibration → BLOCK promotion. The gate should be mechanical so it can't be lost to completion-pressure.

**Related:**
- Process integrity > completion (CLAUDE.md Behavioral Rails)
- Process over momentum (feedback_process-over-momentum.md)
- Lead role boundary — lead doesn't absorb agent work, but inverse also holds: lead doesn't bypass agent-protocol gates either
