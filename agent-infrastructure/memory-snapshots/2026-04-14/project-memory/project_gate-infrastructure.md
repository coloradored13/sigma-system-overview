---
name: Gate infrastructure
description: Mechanical gate enforcement via orchestrator-config.py validate/compute-belief — 23 gates, 8 bundles, replaces prose-only enforcement
type: project
originSessionId: 153cb2df-ac4e-430b-9ed2-bb85dbfe2974
---
Orchestrator-enforced gate system added 26.3.28, triggered by sigma-audit finding CB hard gate skipped.

**Why:** Prose-only gate instructions (G1-G11, CB protocol, contamination checks) depended on the lead remembering to execute them. The lead internalized protocol spirit but skipped format gates. Moving enforcement to code makes compliance mechanical.

**How to apply:** The lead calls `validate --check {bundle}` before `advance`. The orchestrator blocks phase transitions without the validated context flag. Gate enforcement is in `gate_checks.py` + `orchestrator-config.py` in `~/.claude/teams/sigma-review/shared/`.

**Key gates:**
- V9 (CB): circuit_breaker → challenge blocked without cb_validated
- V21 (TeamCreate): orchestrator start blocks without team_created in context
- V22 (session-end): archive → complete blocked without git clean + pushed
- V23 (synthesis artifact): archive → complete blocked without *-synthesis.md in archive
- V3-V8 (R1 convergence): agent output, source tags, XVERIFY, DB[], hypothesis matrix, persistence
- V13-V16 (pre-synthesis): contamination, provenance audit, sycophancy check, exit-gate format

**Belief computation:** `compute-belief --belief-mode {analyze|build-plan|build-quality}` mechanically derives belief state from workspace content. Divergence > 0.15 from declared value flagged.

**R16 bug fix (26.4.9):** 7 bugs found during R16 (gate enforcement ~50%). Fixed: advance crash (`.name` on str), V4 FINDING[] regex, V5 XVERIFY-PARTIAL, V6 DB-reconciled/DISCONFIRM, V10 DA-C[]+verbs+fallback, compute-belief fuzzy flag, 01-spawn arg order. Audit additions: round_limit(5) on all self-loops, atomic checkpoint writes, mode mismatch detection, session overwrite guard, stuck-phase diagnostic. Commit ae9ce2b.

**Files:** gate_checks.py (~1370 LOC), orchestrator-config.py (~640 LOC), test_gate_checks.py (~1060 LOC, 84 tests)
**SKILL condensation:** G1-G11 checklists replaced with validate table (~120 lines removed from sigma-build SKILL.md). Protocol steps and purpose preserved — only enforcement prose removed.
