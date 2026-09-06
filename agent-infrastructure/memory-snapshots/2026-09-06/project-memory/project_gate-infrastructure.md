---
name: Gate infrastructure
description: Atomic checklist model — chain-evaluator (A1-A19 + B1-B4) replaces orchestrator, phase-gate provides minimal hard blocks
type: project
originSessionId: 76c5468f-a7a0-451e-b3c3-63637a10d184
---
Atomic checklist model replaced phase-based orchestrator (26.4.16). The deliverable is a complete chain — every item must pass before the review/build is done.

**Why:** Phase-based orchestrator (orchestrator-config.py 1052 lines + phase-compliance-enforcer.py 841 lines) was fragile. Lead skipped phases under pressure, hooks caused infinite loops in regular conversations, and the 12-phase sequential pipeline created a single point of failure. Checklist model evaluates completeness at session end instead of gating every step.

**How to apply:** chain-evaluator.py runs as Stop hook (informational, non-looping) and via CLI (`chain-evaluator.py evaluate|status|item`). The lead works in whatever order produces the best analysis. The evaluator checks the output, not the process.

**ANALYZE chain (A1-A19):**
- A1-A10: Agent work (findings, provenance, DB[], circuit breaker, DA challenges, BELIEF, exit-gate, contamination, provenance audit, sycophancy)
- A11-A14: Chain closure (synthesis artifact, archive, promotion, git clean)
- A15: XVERIFY coverage (conditional)
- A16-A18: Peer verification (sections exist, specificity >=3 artifact IDs, coverage matrix >=2 verifiers)
- A19: Chain evaluation output (written by evaluator itself)

**BUILD adds B1-B4:** Plan lock (ADR+IC+SQ+exit-gate:PASS), checkpoints, merge verified, source tags.

**Files:** chain-evaluator.py (718 LOC), phase-gate.py (244 LOC, plus BLOCK 5 synthesis-archive carve-out shipped 26.5.8 via build 2026-05-05-block-5-synthesis-carveout — `_is_synthesis_archive_write` helper exempts `*-synthesis.md` writes under `shared/archive/` from compilation-complete precondition, resolving the Step 13f→14 logical cycle), gate_checks.py (1927 LOC, 28 check functions), test count: 1281 baseline → 1286 post-build (delta=+5 from `TestBlock5SynthesisCarveOut` a-e, 0 regressions, 2 pre-existing tests re-targeted to `-workspace.md` to preserve invariants).
