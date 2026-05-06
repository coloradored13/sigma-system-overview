# sigma-build plan: block-5-synthesis-carveout

## Meta
- created: 2026-05-05
- locked: 2026-05-05
- build-id: 2026-05-05-block-5-synthesis-carveout
- tier: BUILD TIER-1 (score 6/25)
- status: plan-locked
- plan-exit-gate: PASS
- plan-belief: P=0.88
- plan-da-grade: PASS (DA[exit-gate-r3] PASS, 4/4 DA[#1/#2/#4/#8] all closed substantively)
- build-exit-gate: PENDING
- build-belief: P=0.00
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

## Build Status
{empty — written by C2}

## Build Review Summary
{empty — written by C3}

## Close Status
{empty — written by C3}

## Verification

End-to-end empirical (5 scenarios per remediation §WS-2 + IE-U3 lesson learned: include `hook_event_name`):

1. `python3 ~/.claude/hooks/phase-gate.py` with `{"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":".../shared/archive/test-synthesis.md","content":"x"}}` → exit=0 even with empty workspace (carve-out fires)
2. Same JSON with `tool_input.file_path` ending in `-not-synthesis.md` → exit=2 if no compilation-complete header (carve-out doesn't fire — preserves R2-micro behavior)
3. Same JSON pointing at `/tmp/foo-synthesis.md` (outside archive dir) → existing `_is_sigma_session()` FP guard handles; carve-out doesn't fire
4. Full hook-suite parity check: pre-fix 1253/14/1, post-fix **1258/14/1** (+5 new tests in `TestBlock5SynthesisCarveOut`, zero regressions)
5. Empirical re-run of the original trap that started this remediation: synthesis-archive write to `2026-04-28-shared-process-hardening-synthesis.md` with NO compilation-complete header in workspace → exit=0 (would have eliminated both close-out events from the parent build had this been in place)

**Acceptance**: all 5 scenarios pass + hook-suite parity confirmed + sigma-audit GREEN + sigma-evaluate ≥A target.
