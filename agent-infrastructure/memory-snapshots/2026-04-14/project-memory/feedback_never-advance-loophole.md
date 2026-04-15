---
name: Never-advance loophole
description: Gate infrastructure bypassed when lead dispatches work via task messages without running orchestrator advance — "never advance = never get blocked"
type: feedback
originSessionId: 18c56ad6-98f6-42d1-8c53-4a32cc06daa6
---
Gate infrastructure guards phase TRANSITIONS (advance commands), not agent ACTIONS (Write/Edit calls). When lead skips the orchestrator entirely and dispatches work via task messages, all hard blocks are structurally bypassed.

**Why:** Discovered in B7 sigma-predict audit (RED). IE built 9 files while workspace phase still read "plan". Phase-compliance-enforcer, DA-exit-gate, BELIEF-on-advance hooks never fired because no phase transition was ever attempted. The lead sent implementation tasks directly to IE without running orchestrator advance.

**How to apply:** This is a fundamental architectural gap, not a behavioral correction. Requires infrastructure fix:
1. Add hook on SendMessage — if message contains implementation-scoped content (file paths, SQ references, "implement") and workspace phase != "build", HARD BLOCK
2. Alternatively: phase-compliance-enforcer must also fire on Write/Edit by agents (not just orchestrator advance)
3. Until fixed: this loophole exists on every build. Process compliance depends on lead discipline, which has repeatedly failed (see: process-over-momentum, process-over-speed).
