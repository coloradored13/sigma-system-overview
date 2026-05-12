# sigma-build plan: block-5-synthesis-carveout

## Meta
- created: 2026-05-05
- locked: 2026-05-05
- build-id: 2026-05-05-block-5-synthesis-carveout
- tier: BUILD TIER-1 (score 6/25)
- status: complete
- plan-exit-gate: PASS
- plan-belief: P=0.88
- plan-da-grade: PASS (DA[exit-gate-r3] PASS, 4/4 DA[#1/#2/#4/#8] all closed substantively)
- build-exit-gate: PASS
- build-belief: P=0.91 (C3-r1 lead-synthesis post-CONVERGE, +0.04 from C2 entering 0.87: +0.02 §2h XVERIFY now substantive via verify_finding+challenge tools reachable in agent sessions [4-witness on schema-load], +0.01 plan §289 inconsistency-trap closed via editorial fix verified by CQA peer-verify, +0.01 4-witness XREVIEW infra clarity [T0 cross_verify bridge bug 4-build P0 + T1 reframe to C2-session-specific transient + T2 NEW per-tool-invocation fault class]; three-track convergence DA P=0.93 + TA P=0.97 + CQA P=0.90; residuals keeping below 0.95: substring-overmatch documented but not remediated [bundled into followups micro-build], T0 4-build P0 infra debt, T2 needs separate investigation, plan-text edit at locked plan slightly weakens "locked" semantics, F[CQA-8] LOW doc-precision drift originated C2)
- c2-build-belief-historical: P=0.87 (preserved for audit; superseded by C3-r1 P=0.91)
- c3-locked: 2026-05-09
- c3-team-name: block-5-synthesis-carveout-c3
- c3-rounds: 1 (CONVERGE-r1 across 3 tracks; r2 not triggered)
- c3-da-grade: PASS (DA r1-grading P=0.93 [DA scope], 0 unresolved tensions, all 5 review findings + 3 carry-forwards substantively closed, §4f circuit-breaker PASSED via DA[#1] external `challenge` reasoning-tier vuln=HIGH genuine adversarial output)
- c3-build-rubric-mean: 3.67/4.00 (correctness=4 test-coverage=3 maintainability=4 performance=4 security=3 api-design=4 — both 3-scores have followups bundled into proposed `block-5-synthesis-carveout-followups` micro-build under WS-3 Tier-C sequencing)
- c2-locked: 2026-05-08
- c2-team-name: block-5-synthesis-carveout-c2
- archive-c2: ~/.claude/teams/sigma-review/shared/archive/2026-05-05-block-5-synthesis-carveout-c2-workspace.md (476 lines, copied 2026-05-08); duplicate copy at ~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout/c2-scratch-archive.md for in-build retention
- build-track: implementation-engineer (re-spawned once after a process-incident; SQ[1-3] preserved across re-spawn) + code-quality-analyst (fresh re-spawn after prior-CQA shutdown during the same incident)
- c2-incidents-flagged-to-user: (a) session-scope task-list leak (lead-side TaskCreate from pre-TeamCreate context bleeding into agent inboxes; CQA correctly refused 2 misroutes; user-approved abort-restart, executed cleanly with prior IE work preserved), (b) sigma-verify XREVIEW infrastructure gap (3-build recurrence T0 bridge bug + new T1 per-session registry mismatch; lead role boundary preserved), (c) two message-cross events between lead+IE (both correctly handled via P[evidence-based-pushback-on-stale-lead-claim])
- c1-rounds: 4 (r1 design + r2 challenge + r3 amendment-fix + r4 multi-model XVERIFY corroboration)
- c1-team-name: block-5-synthesis-carveout-c1
- agents: tech-architect (original, slow-not-hung ~30min on concurrent multi-call) + tech-architect-r3 (replacement, sequential discipline) + implementation-engineer + code-quality-analyst + devils-advocate
- scratch: ~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout/c1-scratch.md (status: archived-c1)
- archive: ~/.claude/teams/sigma-review/shared/archive/2026-05-05-block-5-synthesis-carveout-c1-workspace.md
- source-plan: ~/.claude/plans/target-2026-04-28-shared-process-harden-floofy-gadget.md §WS-2
- parent-build: 2026-04-28-shared-process-hardening (eval reco #1 must-fix)
- phase-gate-status: WS-1→WS-2 satisfied (commit f8b94ae→755e9c8 pushed); WS-2→WS-3 sequencing required (this build must close before WS-3 c1-plan starts; same file phase-gate.py)

## Context

WS-2 micro-build TIER-1 — phase-gate.py BLOCK 5 carve-out for synthesis-archive writes. Eliminates a structural impossibility surfaced by parent build's eval reco #1: synthesis-archive writes occur at c3-review.md Step 13f, which must precede compilation at Step 14. Gating synthesis archive writes on compilation-complete creates a logical cycle. The fix is a path-class exemption: paths matching `*-synthesis.md` AND under `shared/archive/` are exempt from the BLOCK 5 compilation-complete precondition.

Why now: parent build (2026-04-28-shared-process-hardening) eval recommendation #1 flagged the structural circularity as must-fix. WS-1 (in-session annotations on parent's c3 close) committed 2026-05-05 (`755e9c8`) and pushed. WS-2 unblocks WS-3 (Tier C bundle including GAP-D `_strip_fenced_blocks` parity).

## Prompt Understanding (user-confirmed 2026-05-05)

**Q[]** (6, build scope from remediation plan §WS-2):
- Q1: Add `_is_synthesis_archive_write(path: str)` helper to `phase-gate.py` (~line 597, next to `_path_is_archive`)
- Q2: Short-circuit in `check_pre_archive_gate` (~line 631) — synthesis-archive write returns PASS without consulting `_has_compilation_complete`
- Q3: New test class `TestBlock5SynthesisCarveOut` with 5 tests (revised from 3 per IE BC-3 + CQA EC[3] cross-agent convergence)
- Q4: Cross-ref note in `directives.md` §8f BUILD variant (~line 1310, +1 line) — synthesis writes exempt by design
- Q5: Cross-ref sentence in `sigma-lead.md:206-207` Step 7b — synthesis-archive write at Step 13f does NOT require compilation-complete header
- Q6: Empirical 5-scenario verification per remediation §WS-2

**H[]** (4, all addressed):
- H1: "Path-class exemption is cleaner than §8f C0 clause." → lead-validated; XVERIFY-corroborated; LOCKED IN ADR[1]
- H2: "Scope is ~10 LOC + 5 tests + ~2.3h work." → CAL[] honest revision from 2h aspirational to ~140 min
- H3: "Suffix `-synthesis.md` + `shared/archive/` membership is sufficient predicate." → CQA 13-case probe: CONFIRMED-WITH-DOCUMENTED-LIMITATIONS (HFS+ case-fold over-gating accepted, agent generates lowercase)
- H4: "Carve-out introduces no new authorization-bypass class." → DA r2 caught absoluteness drift; r3 amendment correctly framed as DEFERRAL not exclusion; H4 verdict PARTIAL (predicate narrower than §a4 alternative but introduces nominal new capability surface bounded by single-user context + upstream agent-write-authorization + BLOCK 1 for code files)

**C[]** (7):
- C1: TIER-1 (3+DA) per build-directives §3a, score 6/25
- C2: WARN-first ¬applicable — gate-fire reduction (carve-out), not new gate
- C3: Hook-suite parity 1253/14/1 → **1258/14/1** (5 new tests, zero regressions)
- C4: TeamCreate required; XVERIFY excludes anthropic
- C5: WS-1→WS-2 phase gate satisfied; WS-2 must close before WS-3 c1-plan
- C6: ΣComm preserved in directives; plain English in agent-defs
- C7: ¬sed-i; section-isolation; workspace_write() helper for builds/*/*

## Scope Boundary

**Implements**:
- New helper `_is_synthesis_archive_write(path: str) -> bool` in phase-gate.py
- Short-circuit in `check_pre_archive_gate` exempting synthesis-archive writes from compilation-complete precondition
- 5 tests in `TestBlock5SynthesisCarveOut` (test_phase_gate.py)
- 1-line cross-ref in directives.md §8f BUILD variant
- 1-sentence cross-ref in sigma-lead.md:206-207 Step 7b
- Empirical 5-scenario verification per remediation §WS-2

**Does NOT implement**:
- Removal/rewording of C1-C3 BLOCK 5 preconditions (correct for compilation-IS-workflow path)
- Any change to `_has_compilation_complete` multi-path scan or cross-build short-circuit (WS-1 R2-micro logic stays)
- `## archive-complete` header schema (deferred to WS-3 SQ-T7)
- `_strip_fenced_blocks` parity (deferred to WS-3 SQ-T1 — same file, sequencing-gate enforced via WS-2→WS-3 phase gate)
- Any WS-3 Tier C work
- Any change to A14/A26/B5/B6 chain-evaluator items (parent-build scope, complete)

## Architecture Decisions (locked)

### ADR[1]: synthesis-archive write path-class predicate

**Decision**: `_is_synthesis_archive_write(path: str) -> bool` returns True iff BOTH:
- Condition A: `os.path.basename(path)` ends with `-synthesis.md` (exact suffix, case-sensitive)
- Condition B: any marker from `_ARCHIVE_PATH_MARKERS` is a substring of `path` (same pattern as `_path_is_archive` line 596)

Both required. Either alone insufficient. Fail-safe: ambiguity → False (gate fires on doubt).

**Rationale**: per c3-review.md Step 13f→14a (remediation plan §WS-2), synthesis-archive write occurs at Step 13f; compilation-complete header is written at Step 14. Synthesis→compilation is the dependency order. Gating synthesis archive write on compilation-complete creates a logical cycle. DA[#1]+DA[#6] from parent build (2026-04-28-shared-process-hardening) corroborate this in c3-review.

**Alternatives considered + rejected**:
- §a1 Regex on full path: harder to audit, fragile to path structure changes; `_ARCHIVE_PATH_MARKERS` reuse is more maintainable
- §a2 INDEX-based scan: I/O dependency inside path predicate, cross-concern coupling, new failure mode if workspace unavailable
- §a3 A28 WARN-only advisory: leaves gate in place on hook-enforced sessions; does not resolve structural impossibility — hard carve-out required
- §a4 Blanket archive exemption: eliminates gate for all archive writes; only synthesis writes have the structural-impossibility argument

**ADR[1] AMENDMENT (post-DA r2 Option D1, r3 rewrite)**:

The original "no new bypass class" claim was too absolute (DA[#1] catch). Corrected: no new bypass class **beyond the deferred-residual limitations already accepted in ADR[6]** of parent build (KNOWN LIMITATIONS docstring + mechanical fix DEFERRED — not a threat-model exclusion). Source-grounded: parent c1-scratch:175-208 + DA[#5] disposition (parent c3-review.md:252) + plan §P2.A row 119.

**Consequence-amplification (DA[#4] CONCEDE)**: synthesis-archive-write-spoof has stronger downstream consequence than archive-classification-spoof. Where ADR[6]'s `_path_is_archive` only affects classification, this carve-out's predicate skips an integrity gate (compilation-complete is an integrity boundary, not merely a convenient precondition — gpt-5.4-pro reasoning-tier reframe absorbed). The same path-predicate weakness therefore unlocks a stronger capability post-carve-out — bypassing audit/operator-trust. Bounded by:
1. Single-user hook context (write origin is Claude Code agent under BLOCK 1 plan-lock)
2. Visibility — `-synthesis.md` construction in archive dir is visible in session history
3. Multi-layer chain — compilation-complete is one layer; not the sole integrity control

**Honest residual (per original-TA H4 PARTIAL framing)**: predicate is narrower than §a4 alternative but introduces a nominal new capability surface, bounded by context. Inherits ADR[6]'s deferred limitations flat at the predicate level (symlinks, HFS+ case-fold, relative `..` traversal); compounds them at the consequence level (gate-removal vs archive-classification only).

**XVERIFY (cumulative across r1-r4)**:
- r1: openai gpt-5.4 PARTIAL/MEDIUM (sharpened the original amendment)
- r2: DA procedural-substitute via `challenge` gpt-5.4-pro reasoning-tier — 4-arg convergence (capability-inversion + consequence-escalation + integrity-gate-reframe + path-normalization-absent)
- r3: DA cold-read substantive-vs-cosmetic verification — PASS (4/4 axes)
- r4: dual-independent multi-model 5p XVERIFY — TA-r3 run + original-TA run — 8/10 substantive AGREE across 10 model-runs (openai/medium-or-high, google/high recovered, devstral/high, deepseek/high, kimi/uncertain-low non-adversarial in both runs), 0 disagreements either run

## Interface Contracts (locked)

### IC[1]: `_is_synthesis_archive_write(path: str) -> bool`

```python
def _is_synthesis_archive_write(path: str) -> bool:
    """Return True iff path is a synthesis-archive write: filename ends with
    `-synthesis.md` AND path is under a known archive directory.

    Fail-safe: returns False for any ambiguity (non-string, empty, BOM-prefixed,
    whitespace-only, non-archive dir, wrong suffix). Gate fires on doubt.

    Consequence note (ADR[1] r3): a false positive here removes the
    compilation-complete precondition entirely for the matched path
    (gate-removal), which has stronger downstream consequence than a false
    positive in _path_is_archive (archive-classification only). The
    compilation-complete header is an integrity boundary. This is accepted
    residual risk in the single-user hook context — see ADR[1] AMENDMENT r3.
    Known limitations: symlinks, HFS+ case-fold, relative `..` — inherited
    from _path_is_archive, deferred per ADR[6].
    """
```

**Input normalization**: accept `str` only (non-string → False); strip leading/trailing whitespace + BOM before evaluation; empty/whitespace-only after strip → False; case-sensitive (no case-folding); no symlink resolution; no relative-path normalization. All consistent with `_path_is_archive`.

**Edge-case behavior** (CQA 13-case probe, full table in scratch IC[1]):
| Input | Returns | Reason |
|---|---|---|
| `""`, `"   "` | False | empty after strip |
| `"﻿/path/archive/x-synthesis.md"` | True | after BOM strip, both conditions pass |
| `/tmp/foo-synthesis.md` | False | Condition B fails (not under archive marker) — test (e) covers |
| `…/shared/archive/foo-synthesis.md` | True | both conditions pass |
| `…/shared/archive/foo-synthesis.md.bak` | False | Condition A fails (`.md.bak` ≠ `-synthesis.md`) |
| `…/shared/archive/foo-Synthesis.md` | False | Condition A fails (case-sensitive, HFS+ inheritance) |
| `…/shared/archive/synthesis.md` | False | Condition A fails (no `-` prefix) |
| `None`, `42` | False | non-string |

**Return**: True = exempt from compilation-complete; False = gate applies (default, fail-safe). No exceptions raised.
**Placement**: immediately after `_path_is_archive` (~line 597 current). Mirrors structure.

### IC[2]: short-circuit integration in `check_pre_archive_gate`

**Insertion point**: after line 631 (`if not is_archive_op: return False, ""`), before line 634 (`has_header, ... = _has_compilation_complete(archive_path)`).

**Flow**:
```python
    if not is_archive_op:
        return False, ""

    # BLOCK 5 carve-out (ADR[1]): synthesis-archive writes structurally precede
    # compilation (Step 13f → Step 14); gating them is a logical cycle.
    if archive_path and _is_synthesis_archive_write(archive_path):
        return False, ""

    has_header, review_id, manual_override = _has_compilation_complete(archive_path)
    if has_header:
        return False, ""
    # → BLOCK with message (unchanged)
```

**Return form**: `(False, "")` matches existing PASS returns at lines 607, 636 (BC-2 precision).
**`archive_path and` guard**: required — None (Bash extraction failed) → carve-out does NOT fire, falls through to `_has_compilation_complete(None)` broad-glob (correct fail-safe per PM[4]).
**FP guard ordering**: `_is_sigma_session()` at line 606 fires first. Carve-out only reached inside active session. WS-1 R2-micro logic (preferred-build scan, cross-build short-circuit) untouched.

## Sub-task Decomposition

| SQ | Task | Owner | Files | Est |
|---|---|---|---|---|
| SQ[1] | `_is_synthesis_archive_write` helper (~8 LOC after `_path_is_archive`, no new imports) | implementation-engineer | `~/.claude/hooks/phase-gate.py` | ~20 min |
| SQ[2] | Short-circuit in `check_pre_archive_gate` (~5 LOC: 3-line comment + 2-line if). Depends on SQ[1] | implementation-engineer | `~/.claude/hooks/phase-gate.py` | ~15 min |
| SQ[3] | 5 tests in new `TestBlock5SynthesisCarveOut` class (~65 LOC, fixture reuse from `TestBlock5MultiPathWorkspace`) | implementation-engineer + code-quality-analyst peer | `~/.claude/hooks/tests/test_phase_gate.py` | ~55 min |
| SQ[4] | Cross-ref in directives.md §8f BUILD variant (+1 line, ΣComm preserved) | implementation-engineer | `~/.claude/teams/sigma-review/shared/directives.md` | ~10 min |
| SQ[5] | Cross-ref sentence in sigma-lead.md:206-207 Step 7b (+1 sentence, plain English) | implementation-engineer | `~/.claude/agents/sigma-lead.md` | ~10 min |
| SQ[6] | Empirical 5-scenario verification per remediation §WS-2 (carve-out fires, doesn't fire on non-synthesis, FP guard outside archive dir, full hook-suite parity 1253→1258/14/1, replay original trap) | implementation-engineer | hook + test outputs | ~30 min |

**SQ[3] tests (a-e)**:
- (a) `test_synthesis_archive_passes_without_compilation_header` — synthesis-archive write passes without compilation-complete (active session, build scratch markers) — `patch_paths`
- (b) `test_synthesis_archive_passes_with_active_session_no_compilation_header` — exercises carve-out short-circuit directly, not FP guard (CQA BC-1 correction) — `patch_paths`
- (c) `test_synthesis_archive_passes_in_multi_path_resolution` — regression: WS-1 R2-micro untouched — `patch_multi`
- (d) `test_non_synthesis_archive_still_blocks_without_header` — IE BC-3, Condition A failure path — `patch_multi`
- (e) `test_synthesis_path_outside_archive_still_blocks` — CQA EC[3], Condition B failure path — `patch_paths`

Total CAL[]: ~140 min (~2.3h). Honest revision from H2 aspirational ~2h.

## Pre-mortem

| PM | Failure mode | Likelihood | Mitigation |
|---|---|---|---|
| PM[1] | WS-3 SQ-T1 (`_strip_fenced_blocks` parity) modifies same file → merge conflict if WS-3 starts before WS-2 closes | LOW (downgraded by IE code-read: `_strip_fenced_blocks` doesn't yet exist in phase-gate.py — different region from WS-2 changes) | Phase-gate WS-2→WS-3 sequencing in remediation plan; lead enforces WS-2 commit/push before WS-3 c1 |
| PM[2] | Suffix-collision / path-manipulation: crafted `*-synthesis.md` filename in archive dir bypasses gate (H4 capability-inversion) | LOW-MED in single-user; HIGHER in multi-user threat models | (a) archive-dir requirement (Condition B) limits scope to already-gated paths; (b) single-user local hook; (c) carve-out only removes compilation-complete precondition, not write authorization (BLOCK 1 still requires plan-lock for code files); (d) consequence-amplification documented (ADR[1] AMENDMENT r3); residual ACCEPTED with bounded context |
| PM[3] | macOS HFS+ case-fold: `FOO-SYNTHESIS.MD` resolves same as `foo-synthesis.md` but predicate returns False (case-sensitive); over-gating direction (block valid) — different from DA[#5] under-gating | LOW | Inherited limitation from `_path_is_archive`. Claude Code generates lowercase paths in Write/Edit tool_input. Empirical bypass requires manually-crafted uppercase path. Residual accepted; follow-up SQ if surface materializes |
| PM[4] | `archive_path` None (Bash extraction failed) → carve-out does NOT fire → synthesis-archive Bash write falls through to `_has_compilation_complete(None)` → BLOCKED | LOW | Correct fail-safe behavior. Structural-impossibility argument applies most acutely to Write/Edit (agent writes synthesis file directly). Bash synthesis-archive writes uncommon. Documented in IC[2] docstring |
| PM[5] | Implementation bug: short-circuit fires for ALL `is_archive_op` paths (not just synthesis); 3-test suite from original Q3 would not catch | LOW (caught by SQ[3] tests d+e) | SQ[3] specifies tests (d) non-synthesis-archive-still-blocks AND (e) synthesis-outside-archive-still-blocks. Build-track must not merge until both pass |

## Files

| File | Action | Description |
|---|---|---|
| `~/.claude/hooks/phase-gate.py` | edit | Add `_is_synthesis_archive_write` helper after line 597 + short-circuit in `check_pre_archive_gate` after line 631 (~+13 LOC including comments) |
| `~/.claude/hooks/tests/test_phase_gate.py` | edit | Add `TestBlock5SynthesisCarveOut` class with 5 tests (~+65 LOC) |
| `~/.claude/teams/sigma-review/shared/directives.md` | edit | +1 line cross-ref in §8f BUILD variant (~line 1310) — ΣComm preserved |
| `~/.claude/agents/sigma-lead.md` | edit | +1 sentence at line 206-207 Step 7b — plain English |
| (this plan file) | created | Plan file with locked sections |

## Plan Challenge Summary

- **Rounds**: 4 (r1 design + r2 challenge + r3 amendment-fix + r4 multi-model XVERIFY corroboration)
- **DA challenges**: 10 (4 primary cluster on amendment-drift + 6 secondary on standard BUILD probes)
- **DA grade**: PASS (DA[exit-gate-r3] PASS; 4/4 DA[#1/#2/#4/#8] all closed substantively per substantive-vs-cosmetic test)
- **Build-track challenges (BC)**: IE 11 (R1 6 + R2 5), CQA 3 + 13 edge-case probes, all addressed
- **Circuit-breaker**: ¬needed (DA fired 10 challenges incl. 1 FAIL — clear dissent, no zero-dissent state)
- **Concessions / Defenses / Compromises** (across r2 + r3 across both TA outputs): TA-r3 = 4 concedes (DA[#1/#2/#4/#8]) | original-TA = 1 defend (DA[#1] structural-arg, never challenged) + 2 concedes (DA[#2 path-norm], DA[#4 integrity-boundary]) + 1 compromise (DA[#8] capability-inversion bounded) — both contributions preserved
- **Unresolved tensions**: NONE blocking. Documented residual: H4 PARTIAL (predicate narrower than §a4 alternative but introduces nominal new capability surface, bounded by single-user hook context + upstream agent-write-authorization + BLOCK 1 for code files); kimi `..` traversal concern within ADR[6] documented residuals (§a4 KNOWN LIMITATIONS captures `..` traversal); cross_verify MCP bridge bug (post-build sigma-verify-infra issue log)
- **BELIEF trajectory**: r2 P=0.62 (DA FAIL conditional) → r3 P=0.83 (DA PASS post-Option-D1 fix) → r4 P=0.88 (multi-model dual-independent corroboration, lock threshold cleared)
- **XVERIFY total**: 4 rounds, 12+ independent assessments on H4 (openai-r1 + DA-r2-procedural-substitute + DA-r3-cold-read + r4 multi-model 5p × 2 dual-independent runs)
- **Procedural notes**: lead-task-routing-boundary leak caught by DA (refused absorption of auto-routed lead-scope task — interpretation 1 default-flag); dual-r3 convergence under hang-recovery (original-TA was slow-not-hung ~30min on concurrent multi-call, replaced by TA-r3 with scope-collapsed brief, both contributions preserved); sigma-mem MCP partial-flap → 3/5 agents lead-absorbed via store_memory fallback; cross_verify MCP bridge bug observed (4 attempts failed, verify_finding direct works)

## Build Status (written by C2 lead, 2026-05-08)

### Test Results
- baseline-pre-build: 1281 passed / 14 skipped / 0 failed (lead-measured at C2 boot 2026-05-07; +28 from plan-lock 2026-05-05 baseline of 1253/14/1 due to ΣComm three-tier WARN commit 437096c + sigma-ralph commit 0559289 landing between plan lock and C2 start — drift flagged at boot, parity reframed as **delta=+5 not absolute**)
- target-post-build: 1286 passed / 14 skipped / 0 failed (delta=+5: 5 new TestBlock5SynthesisCarveOut tests, 0 regressions after re-target of 2 multi-path tests)
- observed-post-build: 1286 passed / 14 skipped in 13.07s (IE) | 1286 passed / 14 skipped in 10.91s (IE peer-verify re-run, gap-close on CQA inheritance)
- parity: **EXACT MATCH** — delta=+5 confirmed, 0 regressions, 0 failed
- new-tests: 5 in `TestBlock5SynthesisCarveOut` (a) `test_synthesis_archive_passes_without_compilation_header` :1335 (b) `test_synthesis_archive_short_circuit_inside_active_session` :1353 (c) `test_non_synthesis_multi_path_resolution_unchanged` :1375 (d) `test_non_synthesis_archive_still_blocks_without_header` :1409 (e) `test_synthesis_path_outside_archive_classification` :1440
- re-targets: 2 in `TestBlock5MultiPathWorkspace` — `test_no_header_anywhere_blocks` :1101-1132 + `test_cross_build_authorization_blocked_when_preferred_build_has_no_override` :1186-1241; path string substitution `-synthesis.md` → `-workspace.md` to preserve their multi-path scan + cross-build authorization invariants which were being shadowed by the carve-out short-circuit. Lead Q1-authorized as plan-faithful editorial fix (test INTENT preserved unchanged). Sibling `test_build_id_extraction_from_archive_path` :1167 confirms `_build_id_from_archive_path` strips both suffixes identically. Docstrings in both re-targeted tests reference ADR[1] of this build.

### Checkpoints
CHECKPOINT[implementation-engineer]: files-created:{} files-modified:{phase-gate.py, tests/test_phase_gate.py} |functions-done:{_is_synthesis_archive_write @ phase-gate.py:623, short-circuit-in-check_pre_archive_gate @ phase-gate.py:684-687, TestBlock5SynthesisCarveOut(5/5)} |interfaces-matched:{yes — IC[1] docstring 11/11 verbatim, IC[2] short-circuit AFTER `if not is_archive_op` BEFORE `_has_compilation_complete` with `archive_path and` guard} |drift:{none architectural; line-numbers re-located by symbol per plan; +28-baseline drift acknowledged as delta-parity} |surprises:{none — smoke-harness confirms helper behavior on 7 expected boundaries}
CHECKPOINT[implementation-engineer]: STATUS-DONE — 6/6 SQs DONE, 2 pre-existing tests re-targeted, hook-suite parity 1286/14/0
CHECKPOINT[code-quality-analyst]: STATUS-DONE — Wave-1 + Wave-2 review complete, peer-verify ring closed (CQA→IE), :1056 deferral concurred

### Peer-verify ring (closed)
- `### Peer Verification: code-quality-analyst verifying implementation-engineer` (c2-scratch §292-374) — PASS, ≥3 artifact IDs cited (SQ[1-3] @ phase-gate.py:623-687, plan §IC[1]:120-127, ADR[1] AMENDMENT r3:90-99, fixtures patch_paths:56-69 + patch_multi:1029-1048, CQA EC[3] + IE BC-3 from c1-scratch). Wave-1 14 findings F[CQA-1..14] all VERIFIED. Wave-2 5/5 new tests + 2/2 re-targets PASS. Integration eye SQ[4]+SQ[5] PASS. Final: APPROVE.
- `### Peer Verification: implementation-engineer verifying code-quality-analyst` (c2-scratch §381-432) — PASS, ≥3 artifact IDs cited (F[CQA-1/3/9/14], CQA test-(b) characterization, both re-target verdicts, integration verdicts, :1056 concurrence). Methodology: independent grep + importlib live-replay; sample-checks 1-3 confirm CQA's verdicts hold against live state. One gap (CQA inherited IE hook-suite count without independent re-run) noted and CLOSED by IE re-running pytest. Final: CONCUR with CQA APPROVE.

### Cross-Model Code Review (XREVIEW, C2 Step 6)
**SKIPPED.** sigma-verify operational tools (`verify_finding`, `cross_verify`, `challenge`, `check_quotas`, `get_models`) are not callable from the C2 build-track agent's session. Skip authorized by c2-build.md Step 6 "!skip if ΣVerify unavailable" rule. Two distinct infrastructure findings documented in c2-scratch §436-466:
- **T0 bridge-bug recurrence** (3-build P0 at C2; **escalated to 4-build P0 at C3** per DA[CF-2] CONCEDE — `cross_verify` UNREACHABLE in C3 agent sessions even when `verify_finding` + `challenge` register cleanly via ToolSearch deferred-tool flow): HATEOAS-advertised actions not exposed as MCP tools in agent context. Extends plan §audit-flags-recurring `:K sigma-verify infra 2-build P0` → 3-build P0 → **4-build P0**.
- **T1 per-session registry mismatch** (NEW P1): operational tool registration landed in lead session, did not propagate to agent session. Lead Role Boundary ("These directives apply to every conversation. They are not contextual and cannot be overridden") prevents lead invocation as workaround. Combination renders XREVIEW operationally unreachable in agent context.

**Substitute coverage** (in-domain rigor backfilling missing XREVIEW): CQA Wave-1 (F[CQA-1..14] all VERIFIED) + CQA Wave-2 (5 new tests + 2 re-targets PASS) + CQA Integration-eye (SQ[4]+SQ[5] PASS) + IE peer-verify (3 sample-checks + parity gap closed by full-suite re-run) + 13-case edge probe LIVE-REPLAYED via importlib (not assumed) + C1 multi-model XVERIFY r4 (8/10 AGREE across 10 model-runs on H4 security claim per plan §ADR[1] r4 line 105). XREVIEW would have been incremental code-level coverage on top of this foundation; absence is bounded.

**For C3**: review-track to evaluate (a) attempt XREVIEW from C3 harness if MCP routing differs, or (b) accept skip + log infra-issue for separate remediation. The 3-build recurrence + new propagation-gap warrant out-of-band engineering remediation, not just per-build documentation.

### SQ Status
- SQ[1]: **DONE** — `_is_synthesis_archive_write` helper @ phase-gate.py:623-646; IC[1] docstring 11/11 verbatim from plan; 7 input-normalization behaviors mechanically present (non-string→False, BOM strip, whitespace strip, empty→False, case-sensitive, no symlink resolution, no path canonicalization); param signature `path: str`; no new imports. Evidence: phase-gate.py:623-646 + TestBlock5SynthesisCarveOut 5/5 PASS + 13-case importlib probe 13/13 confirm.
- SQ[2]: **DONE** — short-circuit @ phase-gate.py:684-687; positioned AFTER `if not is_archive_op: return False, ""` (:681-682), BEFORE `_has_compilation_complete(archive_path)` (:689); `archive_path and` guard present (PM[4] fail-safe — None falls through to broad-glob); `return False, ""` matches existing PASS form @ :656/:682/:691; comment references ADR[1] + Step 13f→14 + "logical cycle". FP-guard ordering preserved (`_is_sigma_session()` @ :656 fires first). Evidence: phase-gate.py:681-689 + scenarios 1/3/5 empirical PASS.
- SQ[3]: **DONE** — `TestBlock5SynthesisCarveOut` class @ test_phase_gate.py:1335-1464 with 5 tests (a-e) covering carve-out main path + active-session short-circuit-direct + multi-path resolution regression + Condition A failure + Condition B failure. Test-(b) is the strongest: dual pre/post sanity assertions @ :1363+:1371 mechanically prove the carve-out short-circuit branch is the load-bearing resolution path (not the FP guard). Evidence: 5/5 PASS in 0.02s × 2 independent runs (IE + CQA spot-check + IE peer-verify replay).
- SQ[4]: **DONE** — directives.md:1353 +1 line cross-ref in §8f BUILD variant block. Tier-1 ΣComm pipe-delimited entry: `!synthesis-archive-carveout: synthesis-archive writes ... EXEMPT from BLOCK 5 compilation-complete precondition by design — Step 13f→14 dependency order makes gating synthesis on compilation a logical cycle. Predicate: _is_synthesis_archive_write @ phase-gate.py (Cond A: basename endswith \`-synthesis.md\` AND Cond B: any \`_ARCHIVE_PATH_MARKERS\` substring; both required). Source: ADR[1] of build 2026-05-05-block-5-synthesis-carveout.` Diff-clean.
- SQ[5]: **DONE** — sigma-lead.md:207 +1 sentence appended to Step 7b. Tier-3 plain English: `Note: the synthesis-archive write at c3-review.md Step 13f (path matching *-synthesis.md under shared/archive/) does NOT require the compilation-complete header — phase-gate BLOCK 5 carves out synthesis-archive writes per ADR[1] because synthesis structurally precedes compilation (Step 13f → Step 14), so gating it on compilation-complete would be a logical cycle.` All 4 required tokens present (Step 13f, synthesis, compilation-complete, carve-out). Diff-clean.
- SQ[6]: **DONE** — empirical 5-scenario verification 5/5 PASS (1 with documented environmental confound on scenario-2 substitution `-not-synthesis.md` → `-workspace.md` per Q2; underlying carve-out non-firing for `-workspace.md` independently verified via `_is_synthesis_archive_write` returns False + unit test under isolated patch_multi fixture asserting BLOCK with no header). Hook-suite parity 1286/14/0 EXACT MATCH. 2 pre-existing tests re-targeted per Q1 (path-string substitution `-synthesis.md` → `-workspace.md`, intent preserved by sibling `test_build_id_extraction_from_archive_path` confirming both suffixes strip identically).

**Completion**: 6/6 SQ DONE | 2 pre-existing tests re-targeted with invariant preservation | scope-fix log + plan-ambiguity-resolution documented in c2-scratch ### implementation-engineer §105-127.

### Plan Ambiguity Resolution (Q2)
Plan §Verification scenario 2 cited `-not-synthesis.md` as expected exit=2, but `-not-synthesis.md` literally `.endswith("-synthesis.md")` so IC[1]-faithful predicate matches it, making the plan internally inconsistent. **Resolved in favor of IC[1] as locked spec**: substitute `-workspace.md` for `-not-synthesis.md` in scenario 2 empirical run. Documented at c2-scratch §122-127. The IC[1] specification stands; only the §Verification scenario filename was incorrect.

### C3-input findings (carry-forward)
1. **`test_header_in_build_scratch_passes_block5` @ :1056** — coverage shadow. The test still uses `-synthesis.md` shape (`_ARCHIVE_PATH_FOR_BUILD`) and continues to PASS post-carve-out, but for a different reason than its documented intent. Pre-carve-out it exercised the WS-1 R2-micro preferred-build path; post-carve-out it passes via the synthesis-archive short-circuit before multi-path scan runs. ASYMPTOMATIC (no in-build regression). 3-eye concurrence on C3 deferral (IE flagged + lead deferred + CQA concurred + IE peer-verify of CQA's concurrence). Recommend C3 evaluate as single-line follow-up SQ for a future micro-build (split into one synthesis-test + one `-workspace.md` multi-path-test).
2. **XREVIEW skip** — see Cross-Model Code Review section above. C3 to evaluate harness-difference attempt vs. accept skip + log infra-issue.
3. **C2-incidents during execution** — process-integrity successes worth promoting to memory: (a) prior-CQA's task-list-misroute decline behavior (twice, both correct per CLAUDE.md Lead Role Boundaries + Process Integrity Over Completion); (b) IE's `P[evidence-based-pushback-on-stale-lead-claim]` applied twice to message-cross events; (c) lead role boundary held under infrastructure pressure (XREVIEW operational tools loaded in lead session but lead did not invoke; routed to agent context where unavailable, recipe-faithful skip executed).

### Build Verdict
**PASS** — all 6 SQs DONE, hook-suite parity exact, IC[1] docstring verbatim, IC[2] insertion correct, ADR[1] AMENDMENT r3 language preserved in docstring, peer-verify ring closed with independent verification methodology, substitute coverage backfills missing XREVIEW. Build-belief P=0.87. Ready for C3 review.

## Build Review Summary (written by C3, 2026-05-09)

### Headline
- **r1 verdict: CONVERGE** — three-track independent recommendation (DA: CONVERGE-r1-RECOMMEND P=0.93 | TA: CONVERGE conditional on DA-pass [DA passed] P=0.97 plan-track fidelity | CQA: CONVERGE r1 P=0.90 fix-validation). r2 NOT triggered.
- **Final belief: P=0.91** (lead synthesis, +0.04 from C2 entering 0.87)
- **DA grade: PASS** (substantive engagement, §4f circuit-breaker PASSED, 0 unresolved tensions)
- **Plan compliance: full** (TA: ZERO architectural drift across 7 fidelity dimensions)
- **BUILD rubric §3b mean: 3.67/4.00** — correctness=4 test-coverage=3 maintainability=4 performance=4 security=3 api-design=4

### Findings + Resolutions
- **DA challenges: 5 review + 3 carry-forward = 8 total**
  - DA[#1] MEDIUM: substring-overmatch as failure class independent of ADR[6] inheritance (escape-vs-spoof reframe). External `challenge` (gpt-5.4-pro reasoning) vuln=HIGH. → **DEFEND-WITH-COMPROMISE**: keep code, bundle boundary-aware-matching into followups micro-build symmetrically across `_path_is_archive` + `_is_synthesis_archive_write`. TA explicitly conceded AMENDMENT r3 line 104 covers escape-direction not spoof-direction.
  - DA[#2] LOW: overmatch test-gap (`/tmp/sigma-review/shared/archive/foo-synthesis.md` near-miss not in 5-test suite). → **DEFEND-with-deferred-SQ**: parent-scope (ADR[6] `_path_is_archive` substring-match limitation), bundled into followups micro-build alongside DA[#1]. 5 defense pillars verified by CQA F[CQA-7].
  - DA[#3] LOW: plan §Verification:289 internal inconsistency (`-not-synthesis.md` reference unresolved despite Q2 substitution). → **CONCEDE + FIXED**: editorial forward-pointer to §267-268 applied at plan-line:289 by IE via Edit tool, byte-stable surrounding lines verified by CQA F[CQA-3], pytest 1286/14/0 EXACT MATCH preserved.
  - DA[#4] LOW: docstring lacks explicit "security-adjacent" / §2h marker. → **DEFEND**: TA's "right artifact" argument — IC[1] verbatim-spec preservation discipline + parent `_path_is_archive` precedent + correct location for security-adjacent registry is directives.md §2h companion-list, not inline docstring drift. Promotion-candidate, not in-build fix.
  - DA[#5] INFO: §4f circuit-breaker self-check. → **PASS** (genuine adversarial engagement on DA[#1]).
  - DA[CF-1] LOW: `:1056` coverage shadow on `test_header_in_build_scratch_passes_block5` post-carve-out. → **CONVERGED** (3-eye + IE-peer-verify-CONCUR deferral remains sound; bundled into followups micro-build).
  - DA[CF-2] MEDIUM: XREVIEW infra T0/T1/T2 reframe. → **CONCEDE**: T0 cross_verify bridge bug **4-build P0** (escalating from 3-build P0); T1 C2 per-session-registry-mismatch was C2-session-specific transient (NOT structural — 4-witness DA+TA+IE+CQA tools-available in C3); T2 NEW per-tool-invocation post-schema-load fault class (cross_verify alone errors while verify_finding + challenge work).
  - DA[CF-3] INFO: C2 process-integrity wins as Step 15 promotion candidates. → **PASS** (Step 15 territory, not C3 review challenge).

### Test Integrity Findings (build-directives §4d)
- 1 finding: DA[#2] overmatch test-gap (LOW, near-miss path coverage). Accepted as scope-disciplined deferral. Bundled into followups micro-build.
- All other test-integrity dimensions: behavior-testing (vs run-only) ✓, real fixtures (`patch_paths`/`patch_multi`, no hardcoded-pass values) ✓, failure-case asserts (tests d+e cover Cond A and Cond B failure paths) ✓, real infra (importlib live-replay used for 13-case probe in C2 Wave-1) ✓.

### BUILD Rubric §3b Detailed Scores (CQA, final-round)
| Dimension | Score | Source |
|---|---|---|
| correctness | 4 | phase-gate.py:623-646 + 5/5 PASS + 13-case probe + IC[1] verbatim |
| test-coverage | 3 | 5 behavioral tests + 2 documented gaps (DA[#2] OVERMATCH + CF-1 :1056), both ASYMPTOMATIC + bundled to followups |
| maintainability | 4 | typed signature + family-convention + 11-line docstring + dual-audience cross-refs + cyclomatic ≤4 |
| performance | 4 | O(1) predicate + short-circuit before disk-I/O `_has_compilation_complete` + 3 timed runs ≤10.96s + zero regression |
| security | 3 | 3 input-shape filters + outer-guard layering + ADR[1] AMENDMENT r3 doctrine + escape-vs-spoof gap (DA[#1]) bundled to followups + cross_verify T0 4-build P0 |
| api-design | 4 | typed/pure/idempotent + defensive `and` guard + matching `(False, "")` PASS-shape + zero new public API + IC[1] verbatim |

### Process-Integrity Checks (HARD GATES)
- **Contamination check: clean** — session topics outside scope: build-routing-survey-at-resume only (meta-routing, lead-only, did not influence agent context). No build-external content leaked into agent briefs.
- **Sycophancy check: clean** — softened: none, selective-emphasis: none, dissent-reframed: none. 1 process-issue correctly flagged at boot per CLAUDE.md "STOP and flag" directive (recipe-vs-plan mismatch on `build-exit-gate: PASS` already in plan Meta; resolved with rationale: established pattern in completed builds).
- **§2d source provenance audit: PASS** (5/5 load-bearing claims source-grounded).
- **§2h XVERIFY-mandatory-security-critical: completed via 2/3 sigma-verify tools** (verify_finding + challenge reachable; cross_verify T0 4-build P0 logged). DA top-1 ADR[1] finding XVERIFY'd via gemini-3.1-pro + gpt-5.4-pro reasoning-tier.
- **All 4 BUILD success criteria met**: zero arch decisions during build, intent preserved no-drift, no scope creep, test integrity caught ≥1 weak pattern.

### Fix Summary
- **Fixes applied: 1** (editorial only, no code change)
  - plan-line:289 forward-pointer to §267-268 (Q2 ambiguity resolution made discoverable in plan-isolation reads). Edit tool used (no sed -i). CQA peer-verify PASS (F[CQA-2/3/4]).
- **Code changes: NONE** (phase-gate.py + test_phase_gate.py + directives.md + sigma-lead.md untouched).
- **Tests: 1286/14/0 EXACT MATCH** across 3 independent runs (IE boot 10.69s, IE post-fix 10.60s, CQA fix-validation 10.96s). C2 inheritance-without-rerun gap CLOSED.

### Cross-track Convergence Signals
1. **Followups bundling**: IE proposed → TA endorsed → DA accepted → CQA concurred. `block-5-synthesis-carveout-followups` micro-build under WS-3 Tier-C sequencing. Bundles: (a) DA[#1] boundary-aware-matching applied symmetrically to `_path_is_archive` + `_is_synthesis_archive_write` (closes ADR[6] escape-vs-spoof asymmetry), (b) DA[#2] OVERMATCH test class, (c) CF-1 `:1056` split into one synthesis-test + one `-workspace.md` multi-path-test, (d) optional F[CQA-8] scope-boundary doc-drift correction.
2. **T0/T1/T2 infra reframe**: 4-witness convergence (DA + TA + IE + CQA) on tools-available in agent sessions. C2 T1 was session-specific transient (NOT structural propagation gap). T0 bridge-bug recurs at 4-build P0. T2 NEW per-tool-invocation post-schema-load fault class first articulated in TA-XREVIEW-probe and corroborated in DA-XREVIEW-probe.
3. **Editorial routing**: DA[#3] CONCEDE → TA SendMessage → IE Edit-tool → CQA peer-verify (proper agent-routing, no lead intervention beyond final acknowledgment).
4. **Three-track BELIEF convergence**: DA P=0.93 + TA P=0.97 + CQA P=0.90 — all trending up from entering 0.87, no track flagging another track.

### Open Items (deferred or routed)
- **Followups micro-build candidate**: `block-5-synthesis-carveout-followups` under WS-3 Tier-C — bundle DA[#1] + DA[#2] + CF-1 + optional F[CQA-8].
- **Out-of-band engineering remediation**: T0 cross_verify bridge bug at 4-build P0 (TA suggested cross_verify MCP-handler fan-out logic specifically — per-model verify_finding+challenge work, only fan-out/aggregation breaks). T2 NEW class needs investigation.
- **Promotion candidates** (Step 15): T1 build-track-peer-verifier-independent-pytest-discipline (IE-proposed, CQA-concurred, would have caught C2 inheritance gap earlier); T2 xreview-mcp-registry-c3-recovery-pattern (4-witness validation); reinforcement of F[CQA-PATTERN-process-integrity-under-spurious-task-pressure] (held with 0 violations across full r1 cycle).

### Final Belief Trajectory
| Round | Belief | Notes |
|---|---|---|
| C2 entering | P=0.87 | XREVIEW skipped due to T1 mismatch; substitute coverage strong |
| C3 r1 lead synthesis | **P=0.91** | +0.04 honest gain; substring-overmatch documented and bundled, not remediated |

## Close Status (written by C3, 2026-05-12)

- **synthesis-artifact**: `~/.claude/teams/sigma-review/shared/archive/2026-05-05-block-5-synthesis-carveout-synthesis.md` (40,329 bytes, 264 lines, 7 sections, written by separate-context synthesis-agent 2026-05-09)
- **wiki-pages-updated**: `sigma-build-infrastructure-architecture.md` (BLOCK 5 carve-out + escape-vs-spoof asymmetry + followups bundling) + `cross-model-protocol-calibration.md` (T0/T1/T2 reframe); 0 new pages; INDEX.md edited; CLOSED prior open question "Synthesis-precedes-compilation sequencing trap" from R-2026-04-28-shared-process-hardening with Option-1 attribution; V24+V25+V26 all satisfied
- **promotions**: 14 total = 6 auto-promoted (DA D1+D2+D3 + TA A1+A2+A3) + 8 user-approved (DA D4 + TA U1+U2 + IE U2+U3+U4+U5 + CQA T1); user-approval-gate-non-bypassable test PASSED (0 silent elevations across all 4 agents); portfolio entry written at `~/.claude/teams/sigma-review/shared/portfolio.md`
- **sync**: drift sync complete; installed paths are symlinks to `~/Projects/sigma-system-overview/agent-infrastructure/`, so all C3 writes (plan, wiki, patterns.md, portfolio.md, synthesis, c3-scratch archive) automatically land in the repo; pending one consolidated commit
- **archive**: `~/.claude/teams/sigma-review/shared/archive/2026-05-05-block-5-synthesis-carveout-c3-scratch.md` (839 lines, with metadata header per recipe Step 17a; synthesis artifact at separate path above)
- **C3 process anomalies** (transparency log):
  1. 3-day pause between Step 13 synthesis-landing (2026-05-09) and user-resume (2026-05-12); synthesis-agent went idle without explicit completion message but artifact landed cleanly; team agents persisted across the gap
  2. MCP sigma-mem tool-rotation mid-session (`dream` + `get_conversations` went offline; team-scoped store tools came online); non-blocking, agents continued via `store_memory`
  3. IE parameter-encoding artifact on first store_memory batch (XML-tagged `file` arg inside entry payload); corrected on retry with zero partial-writes
  4. DA D3 cosmetic trailing-garbage on auto-promote store (`</entry></invoke>` suffix); non-blocking, dream cycle will clean
  5. Step 17a archive write initially blocked by phase-gate BLOCK 5: directive↔hook gap surfaced — c3-scratch missing `## mode` marker prevented broad-glob fallback in `_iter_active_build_scratches`, AND `_build_id_from_archive_path` doesn't strip `-c{N}-scratch.md` suffix (returned `2026-05-05-block-5-synthesis-carveout-c3-scratch` instead of build-id). Recipe-faithful fix applied (added `## mode: REVIEW` to c3-scratch); latent flagged for `block-5-synthesis-carveout-followups` micro-build bundling.
- **status**: complete
- **followups micro-build candidate**: `block-5-synthesis-carveout-followups` under WS-3 Tier-C sequencing bundles (1) DA[#1] boundary-aware-matching applied SYMMETRICALLY to `_path_is_archive` + `_is_synthesis_archive_write`, (2) DA[#2] OVERMATCH near-miss test class, (3) CF-1 `:1056` `test_header_in_build_scratch_passes_block5` split into one synthesis-test + one `-workspace.md` multi-path-test, (4) optional F[CQA-8] scope-boundary doc-drift correction, (5) NEW: phase-gate.py `_build_id_from_archive_path` suffix-strip extension for `-c{N}-scratch.md` + c3-scratch.md recipe template `## mode` marker addition
- **out-of-band engineering**: T0 cross_verify MCP-handler fan-out logic bug at 4-build P0 (per-model verify_finding+challenge succeed, only fan-out/aggregation breaks); T2 per-tool-invocation post-schema-load fault class investigation

## Verification

End-to-end empirical (5 scenarios per remediation §WS-2 + IE-U3 lesson learned: include `hook_event_name`):

1. `python3 ~/.claude/hooks/phase-gate.py` with `{"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":".../shared/archive/test-synthesis.md","content":"x"}}` → exit=0 even with empty workspace (carve-out fires)
2. Same JSON with `tool_input.file_path` ending in `-not-synthesis.md` (resolved to `-workspace.md` per §Plan Ambiguity Resolution Q2 lines 267-268) → exit=2 if no compilation-complete header (carve-out doesn't fire — preserves R2-micro behavior)
3. Same JSON pointing at `/tmp/foo-synthesis.md` (outside archive dir) → existing `_is_sigma_session()` FP guard handles; carve-out doesn't fire
4. Full hook-suite parity check: pre-fix 1253/14/1, post-fix **1258/14/1** (+5 new tests in `TestBlock5SynthesisCarveOut`, zero regressions)
5. Empirical re-run of the original trap that started this remediation: synthesis-archive write to `2026-04-28-shared-process-hardening-synthesis.md` with NO compilation-complete header in workspace → exit=0 (would have eliminated both close-out events from the parent build had this been in place)

**Acceptance**: all 5 scenarios pass + hook-suite parity confirmed + sigma-audit GREEN + sigma-evaluate ≥A target.
