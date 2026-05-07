---
name: Never-advance loophole
description: RESOLVED 26.4.16 — loophole eliminated by removing phase-based enforcement entirely; atomic checklist model evaluates deliverables not transitions
type: feedback
originSessionId: 76c5468f-a7a0-451e-b3c3-63637a10d184
---
Gate infrastructure bypassed when lead dispatched work without running orchestrator advance — "never advance = never get blocked."

**Why:** Discovered in B7 sigma-predict audit (RED). Lead sent implementation tasks to IE without advancing orchestrator phase. All hard blocks were structurally bypassed because they guarded phase TRANSITIONS, not agent ACTIONS.

**Resolution (26.4.16):** Atomic checklist model eliminates the loophole by design. There are no phase transitions to skip. The chain-evaluator checks deliverables at session end — if the work wasn't done, the chain is incomplete regardless of what phases were or weren't advanced. The only hard blocks are code-write-auth (requires plan lock evidence in workspace) and git-commit-gate (requires chain complete), both enforced via phase-gate.py on actual tool calls.

**How to apply:** The correction itself is now structural, not behavioral. No lead discipline required — the enforcement is in the deliverable check, not the process gate.
