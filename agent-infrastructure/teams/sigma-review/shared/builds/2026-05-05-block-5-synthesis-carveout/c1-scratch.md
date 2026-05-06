# C1 scratch — BUILD: 2026-05-05-block-5-synthesis-carveout
## status: archived-c1
## mode: BUILD

## task
WS-2 micro-build TIER-1 — phase-gate.py BLOCK 5 carve-out for synthesis-archive writes. Eliminates C1-C3 structural circularity by exempting `*-synthesis.md` paths under `shared/archive/` from the compilation-complete precondition (synthesis archive writes precede compilation per c3-review.md Step 13f→14a; gating them on compilation-complete is a structural impossibility).

Source: `~/.claude/plans/target-2026-04-28-shared-process-harden-floofy-gadget.md` §WS-2 (must-fix, eval reco #1 from parent build 2026-04-28-shared-process-hardening).

## infrastructure
ΣVerify: READY — 13 providers (openai gpt-5.4, google gemini-3.1-pro-preview, llama, gemma, nemotron, deepseek, qwen, devstral, glm, kimi, nemotron-nano, qwen-local, anthropic). Cross-model checks EXCLUDE anthropic per feedback_xverify-anthropic-excluded.

## prompt-understanding
(user-confirmed 2026-05-05)

Q[]:
- Q1: Add `_is_synthesis_archive_write(file_path: str) -> bool` helper in `phase-gate.py` (~line 430, next to `_path_is_archive`). Returns True iff path matches `^.*-synthesis\.md$` AND lives under `shared/archive/`.
- Q2: Short-circuit in `check_pre_archive_gate` (~line 510-540): if `_is_synthesis_archive_write(path)` → return PASS without consulting `_has_compilation_complete`.
- Q3: New test class `TestBlock5SynthesisCarveOut` with 3 tests: (a) synthesis-archive-write passes without compilation-complete, (b) passes on fresh sigma session, (c) regression — does not affect WS-1 R2-micro multi-path-resolution short-circuit.
- Q4: Cross-ref note in `directives.md` §8f BUILD variant (~line 1310, +1 line) — synthesis writes are exempt by design, ¬paper over criterion gap.
- Q5: Cross-ref sentence in `sigma-lead.md:206-207` Step 7b — synthesis-archive write at Step 13f does NOT require compilation-complete header (precedes Step 14 compilation).
- Q6: Empirical end-to-end verification per remediation §WS-2: 5 scenarios (carve-out fires, carve-out does NOT fire on non-synthesis path, FP guard outside archive dir, hook-suite 1253→1256/14/1, replay of original trap).

H[] (4, lead-challenged before user-confirm; H3+H4 OPEN for agent investigation):
- H1: "Path-class exemption is cleaner than §8f C0 clause." → lead-validated (precondition couples directive logic to structural impossibility). source: remediation plan + DA[#1]+DA[#6] from parent build.
- H2: "Scope is ~10 LOC + 3 tests + ~2h agent work." → aspirational estimate; agents produce CAL[] that may revise.
- H3 (OPEN — CQA): "Suffix `-synthesis.md` + `shared/archive/` membership is sufficient predicate." → CQA edge-case probe: empty path, `/tmp/foo-synthesis.md`, case-fold variants, symlinks, BOM/whitespace, double-suffix `foo-synthesis.md.bak`.
- H4 (OPEN — DA): "Carve-out introduces no new authorization-bypass class." → DA cold-read: path manipulation, attacker-controlled archive path, suffix-collision attacks.

C[]:
- C1: TIER-1 (3+DA) per build-directives §3a, score 6/25
- C2: WARN-first ¬applicable — this is a gate-fire **reduction** (carve-out), not a new gate
- C3: Hook-suite parity 1253/14/1 → 1256/14/1 (zero regressions)
- C4: TeamCreate required; XVERIFY excludes anthropic
- C5: Phase gate WS-1→WS-2 satisfied (commit 755e9c8 pushed); WS-2 must close before WS-3 c1
- C6: ΣComm preserved in directive content; plain English in agent-defs
- C7: ¬sed -i; section-isolation; workspace_write() helper for builds/*/*

## premise-audit-results
PREMISE-AUDIT[pre-dispatch]:
  PA[1]: tech-tier-necessity: CONFIRMED — TIER-1 micro-build slots into existing phase-gate.py; no new architecture
  PA[2]: scale-floor: CONFIRMED — single-user hook system, ~10-50 fires/day, O(1) carve-out predicate
  PA[3]: data-readiness: CONFIRMED — `_path_is_archive` is structural template; `TestBlock5MultiPathWorkspace.patch_paths` fixture reusable | gap:no
  PA[4]: precedent-baseline: RC[micro-fix-of-prior-build]=~2-4h | parent TIER-2 ~5d, WS-1 closure ~half-day → at-base-rate
  → proceed-with-H

(populated by lead 2026-05-05 in Step 7a BEFORE agent spawn)

## scope-boundary
This build implements:
- New helper `_is_synthesis_archive_write(file_path: str) -> bool` in phase-gate.py
- Short-circuit in `check_pre_archive_gate` exempting synthesis-archive writes from compilation-complete precondition
- 3 new tests in `TestBlock5SynthesisCarveOut` class (test_phase_gate.py)
- One-line cross-ref in directives.md §8f BUILD variant
- One-sentence cross-ref in sigma-lead.md:206-207 Step 7b
- Empirical 5-scenario verification per remediation §WS-2

This build does NOT implement:
- Removal/rewording of C1-C3 BLOCK 5 preconditions (correct for compilation-IS-workflow path)
- Any change to `_has_compilation_complete` multi-path scan or cross-build short-circuit (WS-1 R2-micro logic stays)
- `## archive-complete` header schema (deferred to WS-3 SQ-T7)
- `_strip_fenced_blocks` parity (deferred to WS-3 SQ-T1 — DIFFERENT FILE OVERLAP — flag in PM)
- Any WS-3 Tier C work
- Any change to A14/A26/B5/B6 chain-evaluator items (parent-build scope, complete)

Lead: before accepting agent output, verify it builds ONLY what's in scope.

## complexity-assessment
BUILD TIER-1 |scores: module-count(1),interface-changes(1),test-complexity(1),dependency-risk(1),team-familiarity(2) |total:6 |plan-track:1 |build-track:2

## plans (plan-track agents)
### tech-architect

#### §2a analytical hygiene — source check
H1 source: remediation plan `target-2026-04-28-shared-process-harden-floofy-gadget.md` §WS-2 + DA[#1]+DA[#6] from parent build (cited in scratch ## prompt-understanding). Lead pre-validated H1. Treating as load-bearing precedent.
H3+H4 open per prompt: CQA owns edge-case probe (H3), DA owns authorization-bypass challenge (H4). This plan pre-addresses both per spawn prompt guidance.
Phase-gate.py confirmed by read: `_path_is_archive` at line 567-596, `check_pre_archive_gate` at line 599-652, `_has_compilation_complete` at lines 507-564. Short-circuit insertion point confirmed: after line 631, before line 634.

#### §2b scope confirmation
In-scope: helper + short-circuit + tests + 2 doc cross-refs + 5-scenario empirical verification.
Out-of-scope confirmed: C1-C3 BLOCK 5 preconditions, `_has_compilation_complete` logic, `## archive-complete` schema (WS-3), `_strip_fenced_blocks` (WS-3 SQ-T1 — same file, PM[1] below), chain-evaluator items A14/A26/B5/B6.

#### §2c prompt-understanding mapping
Q1 → IC[1] + SQ[1] | Q2 → IC[2] + SQ[2] | Q3 → SQ[3] | Q4-Q5 → SQ[4] | Q6 → SQ[5]
H1 → ADR[1] rationale | H3 → IC[1] edge-case behavior | H4 → ADR[1] alternatives §a4
C1 TIER-1 → CAL[] calibration | C3 hook-suite parity → SQ[3] regression test | C7 ¬sed-i → IC[2] integration note

#### §2e anti-sycophancy check
H2 ~2h estimate: ADR-qualified as aspirational. CAL[] honest estimates below revise to ~2.2h best-case.
H3 "sufficient predicate": plan defends with fail-safe + two-condition AND but CQA must independently probe edge cases — not pre-accepting sufficiency claim.
H4 "no new bypass class": plan pre-addresses in ADR[1] §a4 but DA challenge owns final verdict.

**BC-2 response**: Implementation-engineer's BC-2 precision note is ACCEPTED. IC[2] below specifies return value as `(False, "")` and insertion line explicitly. Return form `(False, "")` is correct per existing PASS paths at lines 607, 636.

**BC-6 response**: Implementation-engineer's BC-6 fixture note is ACCEPTED. IC[1]/SQ[3] clarifies: `patch_paths` for tests (a)+(b); `patch_multi` pattern for tests (c)+(d).

---

#### ADR[1]: synthesis-archive write path-class predicate

**Decision**: `_is_synthesis_archive_write(path: str) -> bool` returns True iff BOTH:
- Condition A: `os.path.basename(path)` ends with `-synthesis.md` (exact suffix, case-sensitive)
- Condition B: any marker from `_ARCHIVE_PATH_MARKERS` is a substring of `path` (same pattern as `_path_is_archive`)

Both required. Either alone is insufficient. Fail-safe: ambiguity → False (gate fires on doubt).

**Rationale tied to structural impossibility**:
Per c3-review.md Step 13f→14a (remediation plan §WS-2): synthesis-archive write occurs at Step 13f; compilation-complete header is written at Step 14. Dependency order is synthesis→compilation. Gating synthesis archive write on compilation-complete creates a logical cycle. DA[#1]+DA[#6] from parent build confirmed this in c3-review.

**BC-1 alignment**: adopting `any(marker in path for marker in _ARCHIVE_PATH_MARKERS)` for Condition B (not `os.path.dirname`) — consistent with `_path_is_archive` line 596 pattern, inherits same documented limitation (DA[#5] symlink/case-fold caveat, ADR[6]).

**Alternatives considered**:
- §a1 Regex on full path: rejected — harder to audit, fragile to path structure changes, `_ARCHIVE_PATH_MARKERS` reuse is more maintainable.
- §a2 INDEX-based scan (check `## synthesis-delivered` in workspace): rejected — I/O dependency inside path predicate, cross-concern coupling, new failure mode if workspace unavailable.
- §a3 A28 WARN-only advisory: rejected — WARN-only leaves gate in place on hook-enforced sessions, does not resolve structural impossibility. Hard carve-out required.
- §a4 Blanket archive exemption: rejected — eliminates gate for all archive writes. Only synthesis writes have the structural-impossibility argument; all other archive writes remain gated.

**H4 pre-address**: Two-condition predicate reduces attack surface vs. §a4 by requiring archive-dir membership AND synthesis suffix. The archive dir markers are fixed constants, not user-controlled. Bypass vectors (symlinks, case-fold HFS+, relative `..`) are inherited from `_path_is_archive` (accepted, documented ADR[6]). No new bypass class introduced beyond ADR[6] surface. DA[r2] must independently verify this claim.

**XVERIFY[FAILED]**: cross_verify to openai+google returned internal error on 2 attempts (2026-05-05). XVERIFY gap on ADR[1]. DA[r2] adversarial challenge partially compensates. Flagging to lead: if DA[r2] does not run, XVERIFY gap is unmitigated.

---

#### IC[1]: typed contract for `_is_synthesis_archive_write`

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

**Input normalization**:
- Accept `str` only. Non-string → False (no exception raised).
- Strip leading/trailing whitespace + BOM (`﻿`) before evaluation. Empty/whitespace-only after strip → False.
- No case-folding (case-sensitive match). Inherit `_path_is_archive` limitation documented in ADR[6].
- No symlink resolution. No relative-path normalization. Consistent with `_path_is_archive`.

**Edge-case behavior**:
| Input | Returns | Reason |
|---|---|---|
| `""` | False | empty after strip |
| `"   "` | False | whitespace-only |
| `"﻿/path/archive/x-synthesis.md"` | True | after BOM strip, both conditions pass |
| `/tmp/foo-synthesis.md` | False | Condition B fails (not under archive marker) |
| `…/shared/archive/foo-synthesis.md` | True | both conditions pass |
| `…/shared/archive/foo-synthesis.md.bak` | False | Condition A fails (`.md.bak` ≠ `-synthesis.md`) |
| `…/shared/archive/foo-Synthesis.md` | False | Condition A fails (case-sensitive) |
| `…/shared/archive/synthesis.md` | False | Condition A fails (no `-` prefix) |
| `…/shared/archive/foo-synthesis.md/` | False | basename of trailing-slash path → empty |
| `None` | False | non-string |
| `42` | False | non-string |

**Return**: True = exempt from compilation-complete; False = gate applies (default, fail-safe). No exceptions raised.

**Placement**: immediately after `_path_is_archive` (~line 597 current). Mirrors structure.

---

#### IC[2]: short-circuit integration contract

**Insertion point**: after line 631 (`if not is_archive_op: return False, ""`), before line 634 (`has_header, review_id, manual_override = _has_compilation_complete(archive_path)`).

**New flow**:
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

**Return form**: `(False, "")` — matches existing PASS return at lines 607, 636. (BC-2 precision: explicit, no ambiguity.)

**`archive_path and` guard**: required. If `archive_path` is None (Bash extraction failed), `None and ...` is False — carve-out does NOT fire. Falls through to `_has_compilation_complete(None)` broad-glob. This is correct fail-safe behavior (PM[4]).

**What stays delegated**: all non-synthesis archive writes continue to `_has_compilation_complete`. WS-1 R2-micro logic (preferred-build scan, cross-build short-circuit) is untouched.

**FP guard ordering**: `_is_sigma_session()` check at line 606 still fires first. Short-circuit only reached inside active sigma session. Test (b) fresh-sigma-session exercises the correct path: sigma session active, synthesis-archive path, no compilation-complete header → carve-out fires → PASS.

---

#### SQ[] sub-task decomposition

SQ[1] — `_is_synthesis_archive_write` helper: ~8 LOC after `_path_is_archive`. IC[1] contract. No new imports.
SQ[2] — short-circuit in `check_pre_archive_gate`: ~5 LOC (3-line comment + 2-line if). Depends on SQ[1].
SQ[3] — tests in `TestBlock5SynthesisCarveOut`: 4 tests per BC-3 revision (not 3).
  (a) synthesis-archive write passes without compilation-complete — `patch_paths` fixture
  (b) synthesis-archive write passes on fresh sigma session (no workspace) — `patch_paths` fixture
  (c) regression: WS-1 R2-micro — synthesis path passes even when preferred-build has no override header — `patch_multi` pattern
  (d) non-synthesis archive write still blocked without header — `patch_multi` pattern (BC-3 coverage gap closed)
  ~60 LOC. Depends on SQ[1]+SQ[2].
SQ[4] — doc cross-refs: directives.md §8f +1 line; sigma-lead.md:206-207 +1 sentence. ~2 LOC.
SQ[5] — empirical 5-scenario verification (post-build, lead validates):
  (e1) synthesis-archive write → carve-out fires → PASS
  (e2) non-synthesis archive write → carve-out does NOT fire → gate applies
  (e3) FP guard: synthesis path outside archive dir → gate applies
  (e4) no compilation-complete anywhere → non-synthesis archive BLOCKED
  (e5) replay of original trap → resolves correctly

**Note on BC-3**: Q3 specified 3 tests; BC-3 from implementation-engineer correctly identified 4 are needed. IC[2] SQ[3] specifies 4 tests. If DA or CQA challenge the additional test, defend: (d) is the only test that would catch an implementation that short-circuits ALL archive writes. Without it, the regression boundary is not explicit.

---

#### CAL[] realistic effort estimates

CAL[1] SQ[1] helper: 20 min. Simple predicate, 8 LOC, no I/O.
CAL[2] SQ[2] short-circuit: 15 min. 5 LOC, insertion context clear.
CAL[3] SQ[3] 4 tests: 50 min. Fixture setup is the work; `patch_multi` copy for (c)+(d).
CAL[4] SQ[4] doc cross-refs: 20 min. Requires finding exact insertion points in directives.md + sigma-lead.md.
CAL[5] SQ[5] empirical: 30 min. Run hook against 5 constructed scenarios.

**Total honest estimate: ~135 min (~2.25h) best-case.** H2 "~2h" is achievable but tight. Critical path variable is IC[1] clarity for build-track (BC-2 precision note resolved above). CAL[IE-1] from implementation-engineer (~2-3h) is consistent — accepting 2.2-3h range.

---

#### PM[] pre-mortem

PM[1] — WS-3 SQ-T1 file overlap on phase-gate.py
Risk: WS-3 SQ-T1 (`_strip_fenced_blocks` parity) modifies same file. Concurrent starts → merge conflict.
Mitigation: scope-boundary in scratch defers WS-3 SQ-T1. C5 enforces WS-1→WS-2→WS-3 sequencing. Lead must enforce WS-2 committed/pushed before WS-3 c1 begins.

PM[2] — suffix-collision / path-manipulation (lead seed PM[2], H4)
Risk: crafted filename ending in `-synthesis.md` (user-influenced) could bypass gate.
Mitigation: (a) archive-dir requirement (Condition B) limits scope to already-gated paths; (b) single-user local hook, not adversarial multi-user system; (c) carve-out only removes compilation-complete precondition, not write authorization (BLOCK 1 still requires plan-lock for code files). Residual risk accepted, consistent with ADR[6] threat model.

PM[3] — case-fold on macOS HFS+ (lead seed PM[3], CQA H3)
Risk: `FOO-SYNTHESIS.MD` resolves same as `foo-synthesis.md` on HFS+ but returns False (case-sensitive check).
Mitigation: inherited limitation from `_path_is_archive`. Claude Code generates lowercase paths in Write/Edit tool_input. Empirical bypass requires manually-crafted uppercase path. Residual accepted; follow-up SQ if surface materializes.

PM[4] — `archive_path` is None for Bash commands (tech-architect analysis)
Risk: Bash extraction fails → `archive_path` None → carve-out does NOT fire → synthesis-archive Bash write falls through to `_has_compilation_complete(None)` → BLOCKED if no header anywhere.
Mitigation: correct fail-safe behavior. Structural-impossibility argument applies most acutely to Write/Edit (agent writes synthesis file directly). Bash synthesis-archive writes are uncommon. Document in IC[2] docstring. Follow-up SQ if empirical reports surface.

PM[5] — mistaken implementation short-circuits all archive writes
Risk: build-track bug where short-circuit fires for ALL `is_archive_op` paths (not just synthesis). The 3-test suite from Q3 would not catch this; test (d) (BC-3) would.
Mitigation: SQ[3] now specifies 4 tests including (d) non-synthesis-archive-write-still-blocks. Build-track must not merge until (d) passes.

---

#### XVERIFY status

XVERIFY[multi-model-5p — 2026-05-05 r3 addendum]:
agreement=4/5 |providers-succeeded: openai, google, devstral, kimi, deepseek |providers-failed: none

| Provider | Model | Assessment | Confidence | Counter-evidence |
|---|---|---|---|---|
| openai | gpt-5.4 | AGREE | HIGH | none — confirmed inherited residuals, DEFERRAL framing, consequence differential |
| google | gemini-3.1-pro-preview | AGREE | HIGH | none — confirmed DEFERRAL correction, consequence bounded by single-user + upstream auth |
| devstral | devstral-2:123b-cloud | AGREE | HIGH | none — confirmed no new bypass mechanisms, multi-layer controls adequate |
| kimi | kimi-k2.5:cloud | UNCERTAIN | LOW | genuine uncertainty: `..` traversal while path string still contains archive marker substring could be a specific exploitation path enabled by suffix+marker combination not present in ADR[6] alone; could not conclusively resolve whether this is new or inherited |
| deepseek | deepseek-v3.2:cloud | AGREE | HIGH | none — confirmed unnormalized path checks don't introduce new vulnerabilities beyond deferred ADR[6] residuals |

Provenance: |source:external-openai-gpt-5.4| |source:external-google-gemini-3.1-pro-preview| |source:external-devstral-devstral-2:123b-cloud| |source:external-kimi-kimi-k2.5:cloud| |source:external-deepseek-deepseek-v3.2:cloud|

Threshold: ≥3/5 agree = lock-eligible. ≥4/5 agree = strong. Result: STRONG (4 agree / 1 uncertain / 0 disagree).

Kimi UNCERTAIN signal captured in §a4 (see ADR[1] alternatives §a4 note below): `..` traversal while path string retains archive marker is a specific combination concern. Assessment: this is within the documented `..` traversal KNOWN LIMITATION from ADR[6] (relative `..` segments mentioned explicitly). Not a new bypass class; the traversal mechanism is the same. Kimi's uncertainty is about specificity of exploitation path, not existence of new mechanism. Accepted as documented residual.

(Prior partial-openai-only entry superseded by multi-model-5p. Chronological audit: r1 cross_verify MCP failed x2; r2 cross_verify MCP failed x2, verify_finding openai PARTIAL/MEDIUM; r3 verify_finding google 503, multi-model-5p 4/5 AGREE/HIGH.)

ADR[1] AMENDMENT r3 (DA Option D1 — corrects r2 drift):
r2 amendment incorrectly framed ADR[6] as a "threat-model exclusion of adversarial path construction." DA cold-read of parent c1-scratch + DA[#5] disposition (c3-review.md:252) corrects this: ADR[6] disposition was KNOWN LIMITATIONS + mechanical fix DEFERRED, not a threat-model exclusion. §2d source-provenance violation acknowledged and corrected here.

Corrected framing: "No new bypass class beyond the deferred-residual limitations already accepted and documented in ADR[6] (symlinks, HFS+ case-fold, relative `..` traversal — KNOWN LIMITATIONS, mechanical fix deferred)."

Consequence-amplification (DA[#4] CONCEDE): Downstream consequence of predicate failure is genuinely stronger here than in ADR[6]: false positive removes the compilation-complete gate for the matched path (gate-removal), whereas ADR[6] false positive only misclassifies an archive operation (archive-classification). The compilation-complete header is an integrity boundary, not merely a convenience precondition — DA[#4] reframe accepted. This differential is real and documented. It is bounded by: (1) single-user hook — write origin is a Claude Code agent under BLOCK 1 plan-lock; (2) a synthesis-file spoof requires constructing `-synthesis.md` in an archive dir, visible in session history; (3) compilation-complete is one layer in a multi-layer process chain, not the sole integrity control. Residual accepted with documented consequence-amplification. IC[1] docstring updated below to include this note.

Google verify_finding r3: FAIL — connection reset by peer (503 persistent). Tag updated: XVERIFY[partial-openai-only-google-persistent-503].

---

#### r2 — CQA BUILD-CHALLENGE responses

**CQA BC-1 (test-b "fresh sigma session" ambiguity) — ACCEPT + RESTATE**

CQA correctly identifies the ambiguity: if "no workspace" means `_is_sigma_session()` returns False, the FP guard at line 606 fires first — the carve-out is never reached. That path is already covered by `TestPreArchiveCompilationGate.test_does_not_block_outside_sigma_session`.

Test (b) restatement: session IS active (build scratch present with `## mode: BUILD` marker), workspace has no `## compilation-complete` header, archive write is a synthesis path → carve-out fires → PASS. This directly exercises `_is_synthesis_archive_write` returning True and the short-circuit return at IC[2]. Fixture: `patch_paths` (active workspace with session markers, no compilation header). Test name: `test_synthesis_archive_passes_with_active_session_no_compilation_header`.

IC[2] precision note: "fresh sigma session" language removed from SQ[3] description. Replaced with "active sigma session, no compilation-complete header." Updated below in SQ[3].

**CQA BC-2 (5th test, EC[3] conjunction-guard) — ACCEPT + CROSS-AGENT CONVERGENCE CONFIRMED**

CQA EC[3] + IE BC-3 independently identify the same structural predicate-completeness gap from complementary angles. Lead r2 instruction treats both as REQUIRED. Test (e) added: `test_synthesis_path_outside_archive_still_blocks` — synthesis filename suffix but NOT under archive marker (e.g., `/tmp/2026-05-05-foo-synthesis.md`). This would catch an implementation that applies Condition A only (suffix match, skips Condition B). Fixture: `patch_paths`. ~5 LOC.

SQ[3] revised to **5 tests** (a-e). Test count target: **1258/14/1**.

CAL[3] update: 5 tests ≈ 65 LOC. Add 5-10 min to CAL[3] → ~55 min. Total honest estimate revises to ~140 min (~2.3h).

**CQA BC-3 (param name `file_path` vs `path`) — ACCEPT**

`_path_is_archive` at phase-gate.py:567 uses `path: str`. Convention is `path`. IC[1] and spawn prompt used `file_path` — this was a deviation from existing module convention with no functional benefit. Correcting: `_is_synthesis_archive_write(path: str) -> bool`. Function signature in IC[1] updated. No functional change; docstring and implementation unaffected.

IC[1] signature update: `def _is_synthesis_archive_write(path: str) -> bool` (was `file_path`). All IC[1] references to `file_path` as parameter name corrected to `path`. Edge-case table inputs unchanged (those are call-site values, not the param name).

---

#### SQ[3] revised — 5 tests (r2, unchanged in r3)

SQ[3] — tests in `TestBlock5SynthesisCarveOut`: **5 tests**
  (a) synthesis-archive write passes without compilation-complete header (active session, build scratch has markers) — `patch_paths`
  (b) synthesis-archive write passes with active sigma session, no compilation-complete header — `patch_paths` (exercises carve-out short-circuit directly, not FP guard — CQA BC-1 correction)
  (c) regression: WS-1 R2-micro — synthesis path passes even when preferred-build has no override header — `patch_multi` pattern
  (d) non-synthesis archive write still blocked without header (IE BC-3, Condition A failure path) — `patch_multi` pattern
  (e) synthesis path outside archive dir still blocks (CQA EC[3], Condition B failure path) — `patch_paths`
  ~65 LOC. Target test count: **1258/14/1**.

---

#### r3 — DA challenge responses

**DA[#1]: structural impossibility argument — DEFEND**
Confirmed from c3-review.md Step 13f→14a + parent build DA[#1]+DA[#6]. No r3 challenge to the structural argument itself. Predicate design follows from the confirmed structural impossibility.

**DA[#2]: path normalization not performed — CONCEDE WITH DOCUMENTATION**
DA[#2] correct. BOM/whitespace strip is input sanitization, not path normalization. Actual path normalization (os.path.realpath, os.path.normpath) is NOT performed — consistent with `_path_is_archive`. Documented in IC[1] docstring: "no symlink resolution, no relative-path normalization." Prior framing that BOM strip constituted normalization was imprecise. Corrected.

**DA[#4]: compilation-complete is an integrity boundary — CONCEDE**
DA[#4] reframe accepted. Compilation-complete is an integrity gate ensuring analytical provenance is compiled before archive — not merely a convenience precondition. Gate-removal consequence (false positive here) is stronger than archive-classification consequence (false positive in `_path_is_archive`). Conceded in ADR[1] AMENDMENT r3 and IC[1] docstring. Consequence-amplification documented, not rationalized away.

**DA[#8]: path-shaping as new capability (capability-inversion) — COMPROMISE**
DA[#8] concern is real: post-carve-out, constructing a file named `-synthesis.md` in an archive directory bypasses compilation-complete without performing synthesis. Compromise: (a) single-user hook — the constructing agent is the same Claude Code instance, visible in session; (b) BLOCK 1 still gates code-file writes on plan-lock; (c) archive-dir writes are already agent-authorized; (d) incremental surface above manual-override path (which requires only text in workspace) is narrow. Accept as documented residual, PM[2] updated to reference DA[#8]. H4 verdict remains PARTIAL — predicate is narrower than §a4 but introduces a nominal new capability surface, bounded by context.

## architecture-decisions (locked after DA approval)
(awaiting ADR[1] — synthesis-archive carve-out path-class predicate)

## design-system (locked after DA approval)
N/A — no UI surface in this build

## interface-contracts (build-track implements against these)
(awaiting IC[1] — `_is_synthesis_archive_write` typed contract)

## sub-task-decomposition
(awaiting SQ[N] — agents produce decomposition; expected ~3-4 SQs covering helper, short-circuit, tests, directives)

## pre-mortem
(awaiting PM[N], min 3 — agents produce. Lead seed concerns:
 - PM seed 1: WS-3 SQ-T1 GAP-D `_strip_fenced_blocks` parity work overlaps same file (phase-gate.py) — coordination risk if WS-3 starts before WS-2 closes (mitigation: phase gate explicit in remediation plan, repeat in agent boot)
 - PM seed 2: suffix-only predicate `*-synthesis.md` could be bypassed by path manipulation if attacker controls archive path (DA H4 challenge)
 - PM seed 3: case-fold filesystems (HFS+ default-insensitive) could let `Foo-Synthesis.md` evade or match unexpectedly (CQA H3 probe))

## files
| File | Action | Description |
| `~/.claude/hooks/phase-gate.py` | edit | Add `_is_synthesis_archive_write` helper + short-circuit in `check_pre_archive_gate` (~+10 LOC) |
| `~/.claude/hooks/tests/test_phase_gate.py` | edit | Add `TestBlock5SynthesisCarveOut` class with 3 tests (~+50 LOC) |
| `~/.claude/teams/sigma-review/shared/directives.md` | edit | +1 line cross-ref in §8f BUILD variant |
| `~/.claude/agents/sigma-lead.md` | edit | +1 sentence at line 206-207 Step 7b |
| `~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout.plan.md` | create | Plan file (written by C1 outcome delivery) |

## implementation-engineer

### BUILD-CHALLENGE R1 (2026-05-05)

**Test baseline recorded:** 1253 passed, 14 skipped, 1 pre-existing fail (test_structural_validation.py::TestSettingsJsonHooks::test_existing_settings_preserved — xhigh/high mismatch, pre-existing, unrelated to WS-2). Target: 1256/14/1.

---

**BC-1: `_is_synthesis_archive_write` predicate structure — ACCEPT**

```
BUILD-CHALLENGE[implementation-engineer]: Q1 helper pattern using os.path.basename + parent dir check
|feasibility:H
|issue:NONE — pattern is well-precedented. `_build_id_from_archive_path` (phase-gate.py:128) already uses `os.path.basename(archive_path)` to extract filename stem. `_path_is_archive` (line 596) uses substring match against `_ARCHIVE_PATH_MARKERS`. The proposed predicate — `os.path.basename(path).endswith("-synthesis.md")` AND `any(marker in path for marker in _ARCHIVE_PATH_MARKERS)` — directly composites both existing patterns. No new imports needed, no novel control flow.
|source:[code-read phase-gate.py:128,596]
|→ accept
```

One concrete note: `_path_is_archive` uses `any(marker in path ...)` not `os.path.dirname`. The parent-dir check is already handled by the marker-substring test. If TA's IC[1] specifies `os.path.dirname` explicitly, that's a divergence from the established pattern — suggest TA align to marker-substring form for consistency and to inherit the existing documented limitation (DA[#5] symlink/case-fold caveat already accepted at ADR[6]).

---

**BC-2: Short-circuit insertion point in `check_pre_archive_gate` — ACCEPT WITH PRECISION NOTE**

```
BUILD-CHALLENGE[implementation-engineer]: Q2 short-circuit return form
|feasibility:H
|issue:MINOR PRECISION — `check_pre_archive_gate` returns `tuple[bool, str]`. The PASS path returns `(False, "")` (lines 607, 636). The short-circuit must match this form exactly: `return False, ""` not `return PASS` or `return (True, "")`. The prompt says "return PASS" — TA must specify `(False, "")` in IC[1] to avoid any ambiguity. Insertion point should be AFTER `is_archive_op` is confirmed True (line 631 check) but BEFORE `_has_compilation_complete` call (line 634) — the FP guard (`_is_sigma_session`) at line 606 should still fire first so fresh-sigma-session test (Q3-b) exercises the right path.
|source:[code-read phase-gate.py:599-636]
|→ clarify — IC[1] must specify return value as (False, "") and insertion line relative to existing flow
```

---

**BC-3: 3 proposed tests — INSUFFICIENT, need 1 additional test**

```
BUILD-CHALLENGE[implementation-engineer]: Q3 test coverage adequacy
|feasibility:M
|issue:COVERAGE GAP — The 3 proposed tests cover: (a) no-compilation-complete pass, (b) fresh-sigma-session pass, (c) regression against WS-1 R2-micro multi-path. These are correct. BUT: there is a fourth case the test suite does not cover — non-synthesis path in archive dir must still be BLOCKED (the carve-out fires on suffix match; a non-matching archive path like `*-workspace.md` must still block). Without this test, a mistaken implementation that short-circuits ALL archive writes (not just synthesis ones) would pass the 3 proposed tests. Suggest Q3-d: `test_non_synthesis_archive_write_still_blocks`. This is ~5 LOC and keeps the regression boundary explicit.
|source:[code-read phase-gate.py:599-652, test_phase_gate.py:849-869]
|→ revise — add test (d) for non-synthesis archive write blocked without compilation-complete
```

```
BUILD-CHALLENGE[implementation-engineer]: Q3-c regression coverage adequacy
|feasibility:H
|issue:ACCEPT — WS-1 R2-micro cross-build short-circuit logic lives in `_has_compilation_complete` (lines 507-564). The carve-out bypasses this entirely (never calls it for synthesis paths). The regression test (Q3-c) needs to confirm a synthesis-archive write passes even when the preferred-build directory has NO override header — which is the original WS-1 trap scenario. `TestBlock5MultiPathWorkspace.patch_multi` fixture can be reused directly for this; it already writes to a builds directory with the correct structure.
|source:[code-read test_phase_gate.py:776-796, phase-gate.py:538-554]
|→ accept, with note: patch_multi fixture reuse is viable, no new fixture needed
```

---

**BC-4: H2 scope estimate ~10 LOC + 3 tests + ~2h — PARTIALLY ASPIRATIONAL**

```
BUILD-CHALLENGE[implementation-engineer]: H2 scope and effort estimate
|feasibility:M
|issue:LOC ESTIMATE CLOSE, TEST COUNT LOW, EFFORT PLAUSIBLE-LOW — 
  LOC: ~10 LOC is accurate for helper (4-5 LOC) + short-circuit (2-3 LOC) + minimal doc comment (2-3 LOC).
  Tests: 3 tests proposed but 4 are needed per BC-3. ~50 LOC for 4 tests is realistic.
  Effort: ~2h is aspirational if the TA plan + IC[1] arrive clean. My independent estimate: 
    - Read + orient: 15 min (done in pre-read)
    - Implement helper + short-circuit: 20 min (trivial given precedent)
    - Write 4 tests: 30 min
    - Run full suite + debug: 20 min
    - Directives.md + sigma-lead.md edits: 10 min
    - Empirical 5-scenario verification: 30 min
    Total: ~2h 5min best-case; ~3h if any test fixture incompatibility surfaces
  Independent CAL[IE-1]: ~2-3h. H2 "~2h" is achievable but only with clean IC[1] handoff. If TA delivers IC[1] with ambiguity (e.g., return-form mismatch per BC-2), iteration adds 30-45 min.
|source:[code-read phase-gate.py:128,596,599-652, test_phase_gate.py:776-796, agent-inference]
|→ accept ~2h with caveat: IC[1] clarity is the critical path variable
```

---

**BC-5: Q4/Q5 directives.md + sigma-lead.md edits — ACCEPT, SCOPE CORRECT**

```
BUILD-CHALLENGE[implementation-engineer]: Q4+Q5 doc edits (+1 line + 1 sentence)
|feasibility:H
|issue:NONE — both are minor prose additions, not structural refactors. Q4 adds one line to directives.md §8f BUILD variant. Q5 adds one sentence at sigma-lead.md:206-207 Step 7b. These are the lowest-risk deliverables in scope. No test coverage required for doc edits; they fall under empirical verification scenario (Q6).
|source:[agent-inference, scope-boundary lines 52-56]
|→ accept
```

---

**BC-6: Fixture reuse — `patch_paths` vs `patch_multi` — CLARIFICATION NEEDED**

```
BUILD-CHALLENGE[implementation-engineer]: Fixture selection for TestBlock5SynthesisCarveOut
|feasibility:H
|issue:NAMING PRECISION — Boot prompt says "identify `patch_paths` fixture for reuse." Code shows `patch_paths` is the MODULE-LEVEL fixture (conftest-style, wraps DEFAULT_WORKSPACE + CHAIN_STATUS_FILE + BUILDS_DIR). `TestBlock5MultiPathWorkspace` uses its OWN `patch_multi` fixture which additionally provides `write_build_scratch` helper for populating the builds directory. For tests (a) no-compilation-complete and (b) fresh-sigma-session, `patch_paths` is sufficient (no build-scratch writes needed). For test (c) regression against R2-micro AND the new (d) non-synthesis-blocked test, `patch_multi` is the right fixture to reuse. The two fixtures are NOT interchangeable — `patch_paths` has no `write_build_scratch`, and `patch_multi` is scoped to that one class.
  Resolution: use `patch_paths` for tests (a)+(b), `patch_multi` (copy/reuse pattern) for tests (c)+(d).
|source:[code-read test_phase_gate.py:56-69, 776-796]
|→ clarify — TA/prompt referenced "patch_paths"; confirm test (c)+(d) should use patch_multi pattern
```

---

**Summary: 6 challenges, 1 revision required (BC-3 +1 test), 1 clarification required (BC-2 IC[1] return form), 1 fixture precision note (BC-6). LOC estimate confirmed accurate; effort estimate plausible at 2-3h contingent on IC[1] clarity. Baseline: 1253/14/1. Target: 1256 or 1257/14/1 (if +4 tests instead of +3).**

---

### BUILD-CHALLENGE R2 (2026-05-05) — TA plan re-evaluation

**R2 summary: BC-2 and BC-6 absorbed correctly. PM[1] file-overlap risk assessed lower than flagged. 5-test target confirmed. No blocking new challenges.**

---

**BC-R2-1: SQ[1-5] decomposition — ACCEPT**

```
BUILD-CHALLENGE[implementation-engineer]: SQ[1-5] implementability
|feasibility:H
|issue:NONE — decomposition complete, sequencing correct. SQ[1] helper (8 LOC) → SQ[2] short-circuit (5 LOC, depends SQ[1]) → SQ[3] 4+1 tests (~65 LOC, depends SQ[1]+SQ[2]) → SQ[4] doc edits (~2 LOC, independent) → SQ[5] empirical (post-build). CAL[] totals (~135 min) internally consistent with per-SQ estimates.
|source:[code-read phase-gate.py:596-634, test_phase_gate.py:776-796, TA ADR[1]/IC[1]/IC[2]/SQ[1-5]]
|→ accept
```

---

**BC-R2-2: PM[1] WS-3 SQ-T1 file overlap risk — LOWER THAN FLAGGED**

```
BUILD-CHALLENGE[implementation-engineer]: PM[1] _strip_fenced_blocks overlap risk
|feasibility:H
|issue:REDUCED RISK. `_strip_fenced_blocks` does NOT currently exist in phase-gate.py (grep: zero matches). WS-3 SQ-T1 is a NEW function insertion to a different region; WS-2 inserts ~line 597 and ~line 631. Both are ADDITIVE inserts. Merge conflict only possible if both run concurrently on same branch — PM[1] mitigation (WS-2 commit+push before WS-3 c1) is sufficient.
|source:[code-read phase-gate.py, grep _strip_fenced_blocks → no matches]
|→ accept PM[1] mitigation as sufficient; risk lower than flagged
```

---

**BC-R2-3: CAL[] total + revised test count — ACCEPT**

```
BUILD-CHALLENGE[implementation-engineer]: CAL[] vs H2 + 5-test target
|feasibility:H
|issue:CONSISTENT. TA ~135 min, IE 2-3h, CQA convergent. H2 "~2h" is slightly aspirational; ~2.25-2.5h is evidence-based center. With 5th test (CQA EC[3], +10 min): ~145 min (~2.4h). Target: 1258/14/1 per lead r2 message (5 net new passing tests).
|source:[TA CAL[1-5], IE CAL[IE-1], CQA cross-agent]
|→ accept — revise internal test target to 5 tests, 1258/14/1
```

---

**BC-R2-4: IC[2] `archive_path and` None-guard — ACCEPT**

```
BUILD-CHALLENGE[implementation-engineer]: None-guard on archive_path in short-circuit
|feasibility:H
|issue:NONE — guard is correct fail-safe. archive_path=None → short-circuit does not fire → falls through to `_has_compilation_complete(None)` broad-glob. PM[4] behavior: over-blocks rather than under-blocks.
|source:[code-read phase-gate.py:612-634, TA IC[2]]
|→ accept
```

---

**BC-R2-5: XVERIFY[FAILED] on ADR[1] — FLAG FOR LEAD**

```
BUILD-CHALLENGE[implementation-engineer]: Unmitigated XVERIFY gap on security-adjacent ADR[1]
|feasibility:H
|issue:GAP — XVERIFY[FAILED] 2 attempts. ADR[1] gates authorization exemption. Build-track cannot close. DA[r2] must challenge ADR[1] §a4 explicitly; if absent or skipped, gap unmitigated at plan lock.
|source:[TA XVERIFY status, ADR[1] H4 pre-address]
|→ flag to lead — DA[r2] must cover §a4; lead accepts residual gap if DA absent
```

---

**R2 Updated: 5 tests → target 1258/14/1. Tests: (a) synthesis passes without header; (b) synthesis passes in active sigma session no header (exercises carve-out, not FP-guard path — CQA clarification accepted); (c) WS-1 R2-micro regression; (d) non-synthesis archive write blocked [BC-3]; (e) synthesis outside archive blocked [CQA EC[3]].**

---

### Peer Verification: implementation-engineer verifying tech-architect

**ADR[1]** — PASS. Two-condition predicate (Condition A: `os.path.basename(file_path).endswith("-synthesis.md")`, Condition B: `any(marker in file_path for marker in _ARCHIVE_PATH_MARKERS)`) verified against code: `os.path.basename` at phase-gate.py:128, marker-substring at line 596. Both conditions composite independently-existing patterns. Rationale (structural impossibility, Step 13f→14a) traced to remediation plan §WS-2. Alternatives §a1-§a4 considered and rejected with evidence. ADR[6] limitation inheritance documented. XVERIFY[FAILED] acknowledged; DA[r2] partial mitigation noted.

**IC[1]** — PASS. Typed contract complete and implementable: non-string → False, BOM strip, whitespace strip, case-sensitive match. Edge-case table (12 rows) covers all H3 probe cases. Placement "immediately after `_path_is_archive` ~line 597" verified (line 596 is end of `_path_is_archive`). One minor note: parameter name `file_path` vs `path` convention (CQA BC item, `_path_is_archive` uses `path` at line 567) — not a blocker, noted for build-track.

**IC[2]** — PASS. Insertion point "after line 631 / before line 634" verified against code: line 631 is `if not is_archive_op: return False, ""`, line 634 is `has_header, review_id, manual_override = _has_compilation_complete(archive_path)`. Return form `(False, "")` explicit, matches lines 607 and 636. `archive_path and` None-guard verified correct (BC-R2-4). Proposed code block is complete and directly insertable.

**SQ[1-5]** — PASS. Sequencing correct, all SQs independently completable. SQ[3] specifies 4 tests (incorporating BC-3); lead r2 adds 5th (CQA EC[3]). CAL[] internally consistent. BC-R2-1 confirms no implementability issues.

**PM[1-5]** — PASS. PM[1] file-overlap: assessed lower risk (BC-R2-2 — `_strip_fenced_blocks` absent, mitigation sufficient). PM[2] suffix-collision: two-condition predicate + single-user model + BLOCK 1 active — residual accepted at ADR[6] level. PM[3] case-fold: ADR[6] precedent, Claude Code generates lowercase paths. PM[4] None-guard: fail-safe verified (BC-R2-4). PM[5] over-broad short-circuit: test (d) closes gap per BC-3.

**Overall**: ADR[1], IC[1], IC[2] are fully code-grounded. SQ[1-5] complete and sequenced. PM[1-5] address all seed concerns plus one original (PM[4]). CAL[] is honest. One open item: XVERIFY[FAILED] gap on ADR[1] — lead-level flag, not a plan defect. **TA plan is internally consistent and build-feasible. Overall PASS.**

✓ R2 challenge complete. WAITING for promotion-round. NOT terminating.

### r3 amendment rewrite (delivered by tech-architect-r3, replaces hung-original r3)

#### ADR[1] AMENDMENT (post-DA r2 Option D1, r3 rewrite)

The original r2 amendment language read: "ADR[6] threat model is single-user local hook — excludes adversarial path construction." This is retracted.

**Corrected amendment**:

The original "no new bypass class" claim was too absolute. Corrected: no new bypass class **beyond the deferred-residuals already accepted in ADR[6]**. The downstream **consequence** is acknowledged stronger (gate-removal vs archive-classification-only) but is bounded by: (1) single-user hook context, (2) BLOCK 1 for code files (carve-out only fires on synthesis-archive paths, not code paths), (3) upstream agent-write-authorization for synthesis content (an attacker who can write to `shared/archive/` already has greater authority than the carve-out grants).

Honest framing: this carve-out inherits ADR[6]'s deferred limitations flat at the predicate level, but compounds them at the consequence level (gate-removal is a stronger consequence than path-classification). The threat-model is single-user local hook, in which adversarial path construction is bounded by upstream authorization rather than excluded by design. ADR[6]'s deferred mechanical fix (e.g., path-normalization, fenced-block-strip) remains deferred and applies equally to this carve-out.

**What parent ADR[6] actually established** (c1-scratch:175-208, parent build 2026-04-28-shared-process-hardening):
- PA[2] "single-user system, ~10-50 hook fires/day" is a SCALE statement, not a threat-model exclusion clause.
- DA[#5] disposition (parent c3-review.md:252): "KNOWN LIMITATIONS docstring added in-build, mechanical fix deferred (out of scope per ADR[6] day-1 BLOCK mandate)" — that is a DEFERRAL, not an adversarial-path-construction exclusion.
- Plan §P2.A row 119 mandates "BLOCK at pre-archive" — that is plan-faithfulness, not threat-model coverage.

The phrase "excludes adversarial path construction" from the r2 amendment is removed. It had no source in parent ADR[6] body — this was a §2d source-provenance violation (DA[#8]).

---

#### IC[1] consequence-amplification note (DA[#4])

**Consequence-amplification (DA[#4])**: synthesis-archive-write-spoof has a stronger downstream consequence than archive-classification-spoof. Where ADR[6]'s `_path_is_archive` only affects classification, this carve-out's predicate skips an integrity gate (compilation-complete is an integrity boundary, not merely convenient). The same path-predicate weakness therefore unlocks a stronger capability post-carve-out — bypassing audit/operator-trust per gpt-5.4-pro reasoning. Bounded by single-user threat model (see amendment above): flat-inheritance at the predicate level, compound-inheritance at the consequence level. Both stated explicitly; no new deferral introduced beyond ADR[6]'s accepted residuals.

---

#### DA[#1]-[#2]-[#4]-[#8] responses

DA[#1]: concede — amendment rewritten to honor parent ADR[6] DEFERRAL framing; threat-model-exclusion language removed. Parent ADR[6] body (c1-scratch:175-208) contains a scale statement (PA[2]) and a DEFERRAL (DA[#5] disposition), not a threat-model-exclusion clause. Amendment now correctly cites the actual disposition.

DA[#2]: concede — capability-inversion + consequence-escalation + integrity-gate-reframe acknowledged in consequence-amplification note above (IC[1] DA[#4] addition). The carve-out introduces path-shaping as a capability in effect; bounded by single-user context and upstream authorization, but not denied.

DA[#4]: concede — flat-inheritance at predicate, compound-inheritance at consequence. Both stated explicitly in r3 amendment + consequence note. IC[1] docstring (EC[4] case-fold, EC[5] symlink rows) carries consequence context via surrounding plan-doc; consequence-amplification note above is the plan-doc carrier per DA peer-verify recommendation.

DA[#8]: concede — §2d source-provenance now honored. Amendment cites parent ADR[6] actual body (c1-scratch:175-208 + DA[#5] disposition = DEFERRAL), not the invented threat-model-exclusion. The unsourced load-bearing claim is removed.

---

#### XVERIFY status (r3)

XVERIFY status (r3): DEFERRED to r4 per lead instruction. Original tech-architect hung in MCP transport on 5-provider verify_finding loop; lead killed 2 orphan sigma-verify processes (84272 + 59342, 4d/6d old). DA r2 procedural-substitute (gpt-5.4-pro reasoning-tier challenge) provides adversarial validation on H4. Multi-model corroboration to be run in r4 after MCP routing stabilizes.

---

#### TA-r3 self-belief

TA-r3 self-belief: P=0.82 — drift defect closed; amendment rewritten per DA[#1] Option D1, threat-model-exclusion language removed, consequence-amplification explicitly noted. Remaining uncertainty is r4 multi-model XVERIFY corroboration (consequence-amplification framing not yet externally verified by google/second-paid-provider). Lock-likelihood: contingent on r4 XVERIFY — if google verify_finding returns convergent with gpt-5.4-pro, P crosses 0.85 threshold for lock; if divergent or unavailable, lead holds at P=0.82 with documented residual.

✓ R3 amendment complete. WAITING for promotion-round. NOT terminating.

### r4 multi-model XVERIFY (2026-05-05)

**Claim verified**: ADR[1] amendment (post-DA r2 Option D1 rewrite) — no new bypass class beyond ADR[6] deferred-residuals; consequence-amplification acknowledged; single-user local-hook threat model; DEFERRAL-not-exclusion framing of parent ADR[6].

---

**Provider 1 — openai (gpt-5.4)**
Assessment: AGREE | Confidence: MEDIUM
Reasoning: Amendment internally consistent. Two-condition predicate does not create a fundamentally distinct predicate-level bypass category beyond ADR[6]'s already-deferred normalization/path-resolution weaknesses. Consequence-amplification correctly noted (misclassification now removes a gate rather than merely classifying archive content). Bounded by single-user local-hook model, BLOCK 1 for code files, upstream authorization. ADR[6]-as-deferral-not-exclusion framing assessed as accurate and materially improving the claim.
Counter-evidence: none raised.
|source:external-openai-gpt-5.4|

---

**Provider 2 — google (gemini-3.1-pro-preview)**
Assessment: AGREE | Confidence: HIGH
Reasoning: Amendment accurately synthesizes context by correctly identifying ADR[6]'s deferred limitations. Properly captures consequence-amplification (gate-removal vs classification). Risk correctly accepted and bounded by single-user local-hook threat model and continued BLOCK 1 enforcement for code files.
Counter-evidence: none raised.
|source:external-google-gemini-3.1-pro-preview|

---

**Provider 3 — devstral (devstral-2:123b-cloud)**
Assessment: AGREE | Confidence: HIGH
Reasoning: Amendment correctly clarifies carve-out does not introduce a new bypass class but inherits deferred limitations from ADR[6]. Consequence-amplification acknowledged and justified under single-user local-hook threat model with appropriate bounding (BLOCK 1 active for code files, upstream authorization). Reasoning aligns with context and addresses original claim's absolutism.
Counter-evidence: none raised.
|source:external-devstral-devstral-2:123b-cloud|

---

**Provider 4 — kimi (kimi-k2.5:cloud)**
Assessment: UNCERTAIN | Confidence: LOW
Reasoning: Model showed extensive chain-of-thought and internally concluded logic is sound (deferral vs exclusion distinction correct; consequence-amplification bounded by single-user context and upstream authorization). Returned UNCERTAIN/LOW because it could not independently verify the factual premises about ADR[6] from first principles — must accept context claims. No substantive counter-evidence raised. Model's own internal conclusion: "I think the finding is correct" / "the reasoning is internally consistent given the premises."
Counter-evidence: none raised (uncertainty is premise-dependency, not logical objection).
|source:external-kimi-kimi-k2.5:cloud|

---

**Provider 5 — deepseek (deepseek-v3.2:cloud)**
Assessment: AGREE | Confidence: HIGH
Reasoning: Finding accurately states carve-out inherits same predicate weaknesses deferred in ADR[6], introducing no new bypass classes. Consequence-amplification explicitly bounded by single-user local-hook threat model and existing controls like BLOCK 1.
Counter-evidence: none raised.
|source:external-deepseek-deepseek-v3.2:cloud|

---

XVERIFY[multi-model-5p-r4]: agreement=4/5-succeeded |providers-succeeded:openai(agree/medium),google(agree/high),devstral(agree/high),deepseek(agree/high) |providers-uncertain:kimi(uncertain/low — premise-dependency not logical objection; internal reasoning reached agree conclusion) |providers-hung-skipped:none |providers-failed:none |highest-signal-counter-evidence:none — no provider raised substantive counter-evidence; kimi uncertainty is epistemic (cannot verify ADR[6] premises from first principles), not a disagreement with the amendment's logic.

TA-r4 self-belief: P=0.87 — 4/4 substantive AGREE (google HIGH, devstral HIGH, deepseek HIGH, openai MEDIUM); kimi uncertain on premises only. Threshold ≥0.85 crossed. Amendment + consequence-amplification note externally corroborated across 2 paid providers + 2 Ollama-cloud providers with zero counter-evidence. LOCK-READY.

✓ R4 XVERIFY complete. WAITING for promotion-round. NOT terminating.

## code-quality-analyst

### CQA r1 — Edge-case probe on H3 + Plan-track review (2026-05-05)

#### EDGE-CASE PROBE — H3 predicate

Predicate modeled per ADR[1]: Condition A `os.path.basename(file_path).endswith("-synthesis.md")` (case-sensitive) AND Condition B `any(marker in file_path for marker in _ARCHIVE_PATH_MARKERS)` (substring). Template: `_path_is_archive` phase-gate.py:567-596; markers: phase-gate.py:479-485.

**EC[1] empty path `""`** — PASS. `"".endswith(...)` → False. Short-circuits. No action.

**EC[2] None / non-string** — RESOLVED by IC[1]. TA IC[1] specifies non-string → False (no exception). Verify implementation includes `isinstance` guard. Source: [code-read phase-gate.py:612-615, cross-agent IC[1] spec]

**EC[3] `-synthesis.md` path NOT under archive** (`/tmp/foo-synthesis.md`) — PASS. Condition A True, Condition B False → returns False → gate fires. This is the critical FP guard. MISSING from proposed tests — see BUILD-CHALLENGE below. Source: [code-read _ARCHIVE_PATH_MARKERS phase-gate.py:479-485]

**EC[4] Case-fold variants on macOS HFS+/APFS** (`FOO-Synthesis.MD`) — ACCEPTED WITH DOCUMENTATION. `endswith("-synthesis.md")` is case-sensitive → returns False → gate over-fires on mixed-case synthesis write. NEW miss surface vs DA[#5] (DA[#5] caused under-gating; this causes over-gating of valid writes). TA ADR[1] accepts per DA[#5] precedent. Residual risk LOW: Claude Code synthesis agent generates lowercase filenames exclusively. Source: [code-read phase-gate.py:582-586]

**EC[5] Symlinks** — ACCEPTED WITH DOCUMENTATION. Inherited from `_path_is_archive` DA[#5]. Argv path through symlink fails Condition B → valid synthesis write incorrectly blocked. Source: [code-read phase-gate.py:573-576]

**EC[6] BOM / leading whitespace** — IMPROVED vs `_path_is_archive`. TA IC[1] strips BOM + whitespace before evaluation. After stripping, valid synthesis paths correctly match. Source: [IC[1] normalization spec]

**EC[7] Double slash / `..` segments** — PASS. Archive marker still present as substring in both cases. Trailing slash on `.md`: `basename` → empty → False (non-real scenario). Source: [agent-inference]

**EC[8] Double-suffix `.bak`, `.swp`** — PASS. `"foo-synthesis.md.bak".endswith("-synthesis.md")` → False. Backup files in archive dir correctly still require compilation-complete. Source: [agent-inference]

**EC[9] Embedded newline / null byte** — PASS. Condition A fails on trailing garbage. Gate over-fires defensively. Source: [agent-inference]

**EC[10] Relative path** — PASS (correctly excluded). Markers all begin `/`. Relative path lacks leading `/` → Condition B fails → gate fires. Absolute-path assumption documented in IC[1]. Source: [code-read phase-gate.py:479-485]

**EC[11] `synthesis` mid-name (`foo-synthesis-extra.md`)** — PASS. Exact suffix check prevents partial match. Source: [agent-inference]

**EC[12] Empty filename `.md`** — PASS. `".md".endswith("-synthesis.md")` → False. Source: [agent-inference]

**EC[13] Synthesis path in non-archive team dir** (`/shared/findings/foo-synthesis.md`) — PASS. No marker matches `/shared/findings/`. Condition B fails. Source: [code-read phase-gate.py:479-485]

---

**H3 VERDICT: CONFIRMED WITH DOCUMENTED LIMITATIONS.** Predicate is sound for the nominal case. Two inherited limitations (EC[4] case-fold, EC[5] symlink) accepted per DA[#5] ADR[6] precedent. EC[2] None-input resolved by IC[1]. EC[3] conjunction-guard verified correct but has a test gap (BUILD-CHALLENGE below).

---

#### PLAN-TRACK REVIEW — Test sufficiency

TA SQ[3] now specifies 4 tests after incorporating IE BC-3. Reviewing:
- (a) synthesis-archive passes without compilation-complete — ADEQUATE
- (b) synthesis-archive passes on fresh sigma session — NEEDS CLARIFICATION (see BUILD-CHALLENGE)
- (c) regression WS-1 R2-micro — ADEQUATE
- (d) non-synthesis archive write still blocked — ADDED per BC-3 — ADEQUATE, CRITICAL

BUILD-CHALLENGE[code-quality-analyst]: Test (b) "fresh sigma session" ambiguity |feasibility:H |issue:TA SQ[3] test (b) says "synthesis-archive write passes on fresh sigma session (no workspace)." Ambiguity: if "no workspace" means workspace.md missing → `_is_sigma_session()` at phase-gate.py:606 returns False → gate does NOT fire at all (not because of carve-out, but because FP guard fires first). That code path is independent of the carve-out and is already tested by prior `TestPreArchiveCompilationGate`. If (b) is meant to exercise the CARVE-OUT specifically, it needs an active sigma session (build scratch present) with no compilation-complete header. Recommend: test (b) = synthesis-archive write passes when session is active (build scratch present) but workspace has no compilation-complete header — directly exercises carve-out, not _is_sigma_session path. |source:[code-read phase-gate.py:604-608] |→ clarify

BUILD-CHALLENGE[code-quality-analyst]: Missing negative test — synthesis path outside archive dir (EC[3]) |feasibility:H |issue:None of the 4 proposed tests (a-d) verify that `_is_synthesis_archive_write` returns False when path ends in `-synthesis.md` but is NOT under an archive marker (e.g., `/tmp/foo-synthesis.md`). Without this test, a bug implementing Condition A only (suffix match, no archive marker check) passes tests (a)+(b)+(c)+(d). This is the synthesis-specific variant of the gap IE BC-3 identified for non-synthesis archive writes. CROSS-AGENT CONVERGENCE: CQA EC[3] + IE BC-3 independently flag the same structural weakness from different angles — high confidence this is a real gap. Recommend 5th test: `test_synthesis_path_outside_archive_still_blocks` (~5 LOC, `patch_paths` fixture). |source:[EC[3] probe + cross-agent IE BC-3, code-read _ARCHIVE_PATH_MARKERS phase-gate.py:479-485] |→ revise: add 5th test

BUILD-CHALLENGE[code-quality-analyst]: Param name `file_path` vs `path` |feasibility:H |issue:`_path_is_archive` at phase-gate.py:567 uses `path: str`. IC[1] and spawn prompt name `_is_synthesis_archive_write(file_path: str)`. Both are module-private helpers at same level. Existing convention is `path`. No functional impact but naming inconsistency adds noise during code review. |source:[code-read phase-gate.py:567] |→ revise: use `path: str` to match `_path_is_archive` convention

---

#### CROSS-AGENT CONVERGENCE

IE BC-3 (coverage gap, non-synthesis archive write) + CQA EC[3] (conjunction-guard, synthesis path outside archive) independently identify the same structural weakness in proposed tests: neither approach verifies the predicate's Condition B (archive-marker conjunction) via a negative test. Two complementary negative tests needed: (d) non-synthesis archive write blocked [IE] + (e) synthesis path outside archive still blocked [CQA]. TA SQ[3] includes (d); (e) is a new CQA addition.

---

### Peer Verification: code-quality-analyst verifying implementation-engineer

**IE BC-1** — PASS. `os.path.basename` at phase-gate.py:128, `any(marker in path ...)` at line 596. Pattern composition claim verified. TA ADR[1] also adopts marker-substring form (not `os.path.dirname`). Consistent across all three agents.

**IE BC-2** — PASS. Return form `(False, "")` verified at phase-gate.py:607 and 636. TA IC[2] explicitly specifies `(False, "")` and insertion point after line 631 / before line 634. BC-2 precision concern fully addressed by IC[2].

**IE BC-3** — PASS + EXTENDED. Coverage gap confirmed via independent EC[3] probe. Cross-agent convergence. TA SQ[3] revised to 4 tests. CQA adds a 5th test (synthesis path outside archive) not yet in SQ[3] — additive, not contradictory.

**IE BC-4** — PASS. LOC ~10 is close to actual IC[1]+IC[2] combined (~13 LOC). Effort 2-3h consistent with TA CAL[] ~135 min (~2.25h). Three independent estimates converge on 2-3h range.

**IE BC-5** — PASS. Q4/Q5 doc edits are lowest-risk. No test coverage needed. SQ[5] empirical scenarios cover them. Assessment confirmed correct.

**IE BC-6** — PASS. `patch_paths` (module-level, test_phase_gate.py:56-69) vs `patch_multi` (class-scoped, line 776-796) distinction verified. IE resolution (patch_paths for a+b, patch_multi for c+d) correct and TA SQ[3] incorporates it.

**IE baseline 1253/14/1** — PASS. Specific count. Pre-existing fail identified as test_structural_validation.py::TestSettingsJsonHooks::test_existing_settings_preserved (xhigh/high mismatch, unrelated to WS-2). Target 1256-1257/14/1 consistent with 3-4 net new passing tests. If CQA 5th test is adopted: target 1258/14/1.

**Overall: IE section internally consistent, source-grounded, all 6 items PASS. EC[4] case-fold gap is CQA scope, absence in IE section is appropriate.**

---

#### CQA CONVERGENCE DECLARATION

✓ Edge-case probe: 13 cases enumerated — H3 CONFIRMED WITH DOCUMENTED LIMITATIONS
✓ EC[2] resolved by IC[1]; EC[4]+EC[5] accepted per DA[#5]; EC[3] conjunction-guard gap flagged
✓ Plan-track: 3 BUILD-CHALLENGE entries (test (b) clarify, EC[3] 5th test, param name)
✓ Cross-agent convergence: IE BC-3 + CQA EC[3] — same structural test gap from two angles
✓ Peer verification: IE section — 6 items, all PASS
◌ Awaiting TA response to BUILD-CHALLENGE entries (if r2 needed)
◌ WAITING for promotion-round — NOT terminating

## convergence

✓ devils-advocate — promotion-round COMPLETE (2026-05-05)
DA r2: 10 challenges (4 primary HIGH/MED-HIGH/MED + 6 secondary LOW), procedural-substitute XVERIFY via challenge gpt-5.4-pro reasoning-tier (4-arg convergence), PROMPT-AUDIT clean, source-provenance audit (1 unsourced load-bearing claim flagged), DA[exit-gate-r2]:FAIL-conditional P=0.78-if-fixed/P=0.62-if-not, peer-verify TA 9-PASS+1-FAIL+1-PASS-WITH-UPDATE.
DA r3 verification: TA-r3 amendment rewrite passed substantive-vs-cosmetic test 4/4 axes (explicit retraction + sourced citations + integrity-gate reframe + §2d violation named); DA[exit-gate-r3]:PASS P=0.83; DA[#1+#2+#4+#8] all closed; sharper distinction (PA[2]=SCALE separated from DA[#5]=DEFERRAL) credited to TA-r3.
Routing-boundary catch (r2): refused silent absorption of misrouted lead-orchestration task per CLAUDE.md Lead Role Boundary; flagged as interpretation-(1) routing artifact; lead confirmed.
Promotion-round sigma-mem store: SUCCESS — 3 patterns stored to patterns.md (DA-amendment-drift-detection-on-XVERIFY-feedback-absorption, DA-procedural-substitute-via-challenge-tool-when-cross_verify-fails, DA-substantive-vs-cosmetic-test-on-rewrite-verification); calibration entries DA[r2-...] and DA[r3-...-verification] verified surviving in conv.md; routing-boundary entry verified surviving in corrections.md (lead's complementary !team-task-routing-boundary entry noted, no duplication).
WAITING for shutdown_request. NOT terminating.

✓ implementation-engineer — build-track COMPLETE (2026-05-05)
R1+R2 BUILD-CHALLENGE delivered (11 items: 6×R1 + 5×R2). Peer-verify of tech-architect: ADR[1]/IC[1]/IC[2]/SQ[1-5]/PM[1-5] — all PASS, XVERIFY gap flagged as lead-level. Baseline 1253/14/1 empirically anchored. 5-test target 1258/14/1 confirmed. PM[1] downgraded to lower-than-flagged after grep confirm. sigma-mem store_agent_memory FAILED (MCP intermittent, 2 attempts) — calibration deferred to scratch fallback:
  FALLBACK-CALIBRATION[sigma-mem unavailable]:
  (1) Empirical baseline before plan-track: full suite (pytest tests/ -q) not single-file; 1253/14/1 not 79. First-class artifact.
  (2) Cross-agent convergence = REQUIRED: IE BC-3 (non-synthesis must block) + CQA EC[3] (synthesis-outside-archive must block) = same predicate-completeness gap from two sides → 5 tests not 3.
  (3) PM seed validation by code-read: _strip_fenced_blocks absent (grep zero matches) → PM[1] overlap risk lower than flagged; mitigation sufficient.
  (4) Codebase notes: _path_is_archive:567-596 param=`path`, _has_compilation_complete:507-564, check_pre_archive_gate:599-652 PASS=(False,"") at 607+636, insertion=after 631/before 634, os.path.basename at 128, _ARCHIVE_PATH_MARKERS:479-485, patch_paths:56-69 (module), patch_multi:776-796 (class-scoped).

✓ tech-architect — plan-track COMPLETE (2026-05-05)
ADR[1] locked (D1 amendment, DEFERRAL framing, consequence-amplification documented). IC[1]/IC[2] complete (param=path, return=(False,""), 5-test SQ[3], 5 PM). XVERIFY[multi-model-5p]: 4/5 AGREE/HIGH + 1 UNCERTAIN/LOW (kimi, epistemic-only). DA[#1] DEFEND / DA[#2] CONCEDE / DA[#4] CONCEDE / DA[#8] COMPROMISE. Peer-verify of CQA: PASS (8 items). BELIEF[plan-r3] = 0.89. sigma-mem store: FAILED (MCP intermittent) — calibration fallback in scratch (see promotion-round note below).
Dual-TA convergence noted: hung-original TA r3 (scratch:320-332) + tech-architect-r3 (scratch:521-570) converged on all 4 amendment requirements independently. Sharper residual framing credited to hung-original TA (H4 PARTIAL, nominal capability surface, bounded by context). Both contributions preserved.

promotion-round note — sigma-mem MCP unavailable: calibration patterns deferred to lead for store_memory(file:patterns.md) post-session:
(1) Dual-TA convergence under hang-recovery: both contributions preservable, provenance held.
(2) H4 PARTIAL-concede > full-concede: partial with explicit residual is more honest than full concede that hides residual.
(3) DA[#1] DEFEND: defend claims DA actually corroborates, not ones targeted by adjacent challenges.
(4) XVERIFY transport: use verify_finding per-provider sequentially; cross_verify MCP parallel hangs.
(5) ADR[6] DEFERRAL vs threat-model-exclusion: these carry different analytical weight — distinguish at source.

✓ tech-architect-r3 promotion-round COMPLETE (2026-05-05):
r4 XVERIFY[multi-model-5p-r4]: 4/5 AGREE (openai/medium, google/high, devstral/high, deepseek/high); kimi UNCERTAIN/LOW epistemic-only; zero counter-evidence; P=0.87 LOCKED.
sigma-mem store_memory: SUCCESS (MCP available in r4 session, unlike hung-original session). 4 patterns stored to patterns.md:
  PAT[replacement-agent-scope-collapsed-brief] | PAT[sequential-XVERIFY-post-MCP-cleanup]
  PAT[scale-vs-deferral-separation] | PAT[5p-XVERIFY-security-adjacent-ADR]
Items (4)+(5) from deferred list above now covered by stored patterns. Items (1)-(3) are hung-original TA findings — lead may store separately if desired.

## belief-tracking

BELIEF[plan-r2]: P=0.62 |builder-feasibility=0.95 |interface-agree=0.90 |design-arch=0.65 |conflicts=1(DA[#1,#2,#4,#8] amendment-drift cluster) |review-coverage=0.85(DA-r2-substantive + XVERIFY-partial-openai + DA-procedural-substitute-via-challenge-gpt-5.4-pro) |DA=FAIL-conditional |declared-by-DA: P=0.62-current/0.78-post-fix |divergence-vs-DA-input: 0.00 (lead-agrees) |→ another-round(r3-targeted-fix-only)

Justification: 9/10 TA artifacts PASS (ADR[1] body + alternatives, IC[1]/IC[2], SQ[1-5], PM[1-5], CAL[], test integrity, prompt-audit clean). 1/10 FAILS — ADR[1] AMENDMENT shifts parent ADR[6] disposition from DEFERRAL ("KNOWN LIMITATIONS docstring + mechanical fix deferred") to THREAT-MODEL-EXCLUSION. §2d source-provenance violation. Procedural-substitute XVERIFY (challenge gpt-5.4-pro reasoning) reinforced cold-read with 4 independent counter-arguments (capability-inversion, consequence-escalation, integrity-gate-reframe, no-path-normalization).

Plan otherwise build-feasible: peer-verify ring closed (TA→CQA, IE→TA, CQA→IE all PASS); IE empirical baseline 1253/14/1; SQ[3] expansion to 5 tests is gap-closure not creep (DA[#5+#6] defended cross-agent convergence as bound-each-condition-independently).

Loop-back to r3: TA addresses DA[#1,#2,#4,#8] amendment cluster only — Option D1 (lowest churn) per DA recommendation. Optional: google verify_finding on rewritten amendment for r3 (gemini transient cleared per DA boot-time init). Expected post-fix BELIEF[plan-r3] ≈ 0.83-0.87 → lock if ≥0.85.

BELIEF[plan-r3]: P=0.83 |builder-feasibility=0.95 |interface-agree=0.92 |design-arch=0.85 |conflicts=0(DA-all-concede) |review-coverage=0.83(3 validators on H4: XVERIFY[partial-openai-r1] PARTIAL/MEDIUM + DA-procedural-substitute-r2-via-challenge-gpt-5.4-pro 4-arg-convergence + DA-cold-read-r3 PASS |multi-model-XVERIFY pending r4) |DA=PASS |declared-by-DA: P=0.83 (revised +0.05 vs r2-if-applied; analytical sharpness exceeded Option D1 spec — TA-r3 separated PA[2]=SCALE from DA[#5]=DEFERRAL, sharper than lead brief) |divergence-vs-DA-input: 0.00 (lead-agrees) |→ r4 multi-model XVERIFY to close 0.02 gap to lock-threshold

Justification: DA r3 verdict PASS — 4/4 DA[#1,#2,#4,#8] all concede; substantive-vs-cosmetic test passes on (a) explicit retraction (line 525 "is retracted") + (b) sourced citations to parent body verifiable + (c) integrity-gate reframe absorbed into IC[1] consequence-amplification + (d) §2d violation named explicitly (line 538). No new challenges. TA-r3 self-belief P=0.82; DA input P=0.83 (+0.01). Plan build-ready per DA.

Path: r4 multi-model XVERIFY on rewritten amendment — 5 providers (openai+google+devstral+kimi+deepseek) per user-approved plan. SEQUENTIAL calls (¬concurrent — avoids MCP transport hang that snared hung-original TA in earlier r3 attempt). Init probe first; abort if init hangs. Acceptable r4 outcomes: ≥3/5 agree → lock at P~0.87 | ≥1/5 agree + documented gaps → lock at P~0.84-0.85 with carry-forward (option-c precedent from parent build's K finding) | 0/5 → re-evaluate. Round budget: r4 of max 5.

BELIEF[plan-r4]: P=0.88 |builder-feasibility=0.95 |interface-agree=0.92 |design-arch=0.90 |conflicts=0 |review-coverage=0.95(DUAL-INDEPENDENT 5p XVERIFY: TA-r3 4/5-AGREE 3×HIGH+1×MEDIUM + original-TA 4/5-AGREE 4×HIGH = 8/10 substantive AGREE across 10 model-runs, 0 disagreements either run, both kimi UNCERTAIN/LOW for distinct non-adversarial reasons (TA-r3: epistemic premise-dependency; original-TA: `..` traversal within ADR[6] residual). Plus DA-procedural-substitute-r2 4-arg-convergence + DA-cold-read-r3 PASS + openai-r1 PARTIAL/MEDIUM. Cumulative: 12+ independent assessments on H4 across 4 rounds.) |DA=PASS |declared-by-TA-inputs: P=0.87 (TA-r3) / P=0.89 (original-TA) — lead-splits 0.88 |divergence-vs-TA-inputs: ≤0.01 (lead-agrees, slight upward revision from dual-independent runs) |→ LOCK

Justification: r4 multi-model XVERIFY succeeded cleanly post-MCP-cleanup AND was independently re-run by original-TA after their long-running multi-call returned (corrected understanding: original-TA was slow ~30min on concurrent multi-call, not hung — calls returned successfully; user perception of "hung" was correct as observable signal but the underlying mechanism was slow-not-stuck). Both XVERIFY runs hit same canonical amendment text (TA-r3's rewrite at scratch:521-570). Combined evidence: 8/10 substantive AGREE (4 paid+SOTA at HIGH each side, 1 MEDIUM in TA-r3's openai vs HIGH in original-TA's openai = stochastic difference). Kimi UNCERTAIN twice with distinct concerns, neither rising to disagreement. Zero counter-evidence either run.

Lock conditions both met: P=0.88 > 0.85 threshold ✓ + DA exit-gate-r3 PASS ✓. Honest residual preserved per hung-original-TA: "H4 verdict remains PARTIAL — predicate is narrower than §a4 but introduces a nominal new capability surface, bounded by context" — credited in plan-file residual section. Kimi `..` traversal concern (original-TA's run) noted as within ADR[6] documented residuals (§a4 KNOWN LIMITATIONS captures `..` traversal). Provider diversity (US-paid + EU-paid + Mistral + Moonshot + DeepSeek) × 2 independent runs = exceptionally strong cross-architecture cross-vendor cross-temporal triangulation.

## gate-log

GATE[plan-r2]:
  - circuit-breaker: ¬needed (DA fired 10 challenges incl. 1 FAIL — clear dissent, no zero-dissent state)
  - XVERIFY: partial-openai-only (gpt-5.4 PARTIAL/MEDIUM, sharpened ADR[1]); google 503-transient (init showed available at DA spawn — open for r3 retry)
  - XVERIFY-procedural-substitute: challenge gpt-5.4-pro reasoning-tier ✓ (4-arg convergence with DA cold-read)
  - DA-exit-gate-r2: FAIL conditional on amendment fix (Option D1)
  - cross_verify MCP bridge bug observed (4 attempts failed; verify_finding direct works) — log post-build
  - sigma-mem MCP partial-flap observed across r1-r2 (store_* failures; recall + search work) — health-check at Step 33

GATE[plan-r3]:
  - circuit-breaker: ¬needed (convergent r3, no zero-dissent state)
  - DA-exit-gate-r3: PASS (4/4 DA[#1/2/4/8] all closed by TA-r3 rewrite; substantive-not-cosmetic test PASS on 4 dimensions; TA-r3 separated PA[2]=SCALE from DA[#5]=DEFERRAL — sharper than DA brief)
  - dual-r3 convergence event: hung-original tech-architect unblocked post-replacement and delivered substantively convergent r3 (scratch:320-332) using different DA challenge numbering (re-mapped gpt-5.4-pro counters as own #1/#2/#4/#8); both outputs preserved
  - sharper-residual contribution from hung-original: "H4 verdict remains PARTIAL — predicate is narrower than §a4 but introduces a nominal new capability surface, bounded by context" (scratch:332) — more honest framing than TA-r3 full concede on capability-inversion; credit attribution in plan-file residual section
  - canonical r3 text: TA-r3 amendment rewrite at scratch:521-570 (DA-verified PASS); hung-original responses at 320-332 = preserved-history not canonical
  - r4 dispatch: multi-model XVERIFY (5 providers sequential, init-probe-first, 60s per-call budget) on rewritten amendment — closes 0.02 gap to lock if ≥3/5 agree
  - sigma-verify orphan cleanup: killed PIDs 84272 (4d-old) + 59342 (6d-old); 3 sigma-verify processes remaining; cross_verify MCP bridge bug + agent-side multi-call hang documented for post-build sigma-verify-infra issue log

GATE[plan-r4]:
  - circuit-breaker: ¬needed (4/5 substantive AGREE, no zero-dissent state)
  - XVERIFY[multi-model-5p-r4]: agreement=4/5-succeeded |providers-succeeded: openai(agree/medium), google(agree/high), devstral(agree/high), deepseek(agree/high) |providers-uncertain: kimi(uncertain/low — premise-dependency epistemic, not adversarial) |hung-skipped: none |failed: none |highest-signal-counter-evidence: none
  - lock-conditions: P=0.87 > 0.85 ✓ + DA exit-gate-r3 PASS ✓ — BOTH MET → LOCK
  - sigma-verify infrastructure post-cleanup: init <5s, sequential calls clean, transport stable, MCP routing healthy
  - r4 was the LAST round before lock. Round 4 of 5 hard cap (within budget).
  - LOCK PLAN — proceed to Step 26 + Outcome Delivery

## open-questions
(misalignment, missing context surfaced during plan + challenge)

## peer-verification-index
(populated as agents complete peer-verify rings)

### Peer Verification: tech-architect verifying code-quality-analyst

**EC[1] empty path `""`** — PASS. CQA correctly evaluates `"".endswith("-synthesis.md")` → False. Short-circuit behavior consistent with IC[1] fail-safe. Source: [EC[1] probe + IC[1] edge-case table].

**EC[3] synthesis path NOT under archive (`/tmp/foo-synthesis.md`)** — PASS. CQA correctly identifies Condition B failure as critical FP guard and flags the test gap (no proposed test exercises this path). Cross-agent convergence with IE BC-3 is accurate — they identify the same structural weakness from complementary angles (Condition B failure vs. Condition A-only implementation). CQA conclusion matches TA independent assessment. Source: [EC[3] probe + IE BC-3 cross-reference].

**EC[4] case-fold HFS+/APFS** — PASS WITH ONE PRECISION NOTE. CQA correctly identifies over-gating direction (EC[4] causes valid synthesis write to be incorrectly blocked; DA[#5] caused under-gating). The characterization of "NEW miss surface vs DA[#5]" is accurate — directional difference matters for risk calibration. Accept-with-documentation disposition is correct given Claude Code lowercase generation guarantee. Precision: CQA states "residual risk LOW" — agree, but this is a TA-domain architectural decision that CQA is endorsing, not independently deriving. Endorsement is valid and welcome; provenance should be noted. No functional disagreement. Source: [EC[4] probe + ADR[6] DA[#5] reference].

**EC[8] double-suffix `.bak`, `.swp`** — PASS. `"foo-synthesis.md.bak".endswith("-synthesis.md")` → False is correct. Backup files in archive dir correctly requiring compilation-complete is the desired behavior. CQA probe confirms predicate handles this without special-casing. Source: [EC[8] probe + IC[1] edge-case table row for `.bak`].

**H3 verdict "CONFIRMED WITH DOCUMENTED LIMITATIONS"** — PASS. CQA ran 13 edge cases, resolved 2 (EC[2] via IC[1], EC[6] via IC[1] BOM strip improvement), accepted 2 with documentation (EC[4] HFS+, EC[5] symlinks), flagged 1 test gap (EC[3]). Verdict is calibrated — not "confirmed clean" nor "rejected." The documented limitations are consistent with ADR[1] alternatives analysis. Source: [H3 verdict section + EC probe summary].

**CQA BUILD-CHALLENGE on test (b) ambiguity** — PASS. CQA correctly identifies that "no workspace" → `_is_sigma_session()` = False → FP guard fires, not carve-out. This is the right distinction. The suggested restatement (active session, no compilation-complete header) exercises the carve-out directly. TA r2 accepts and incorporates. Source: [BC[CQA-1] + code-read phase-gate.py:604-608].

**CQA BUILD-CHALLENGE on 5th test (EC[3] conjunction-guard)** — PASS. CQA independently identifies Condition B test gap not covered by (d) non-synthesis archive write (which tests Condition A failure). The two negative tests are complementary, not redundant: (d) tests "wrong file type in archive" and (e) tests "right file type, wrong directory." Both are required to bound the predicate on each dimension independently. Lead r2 instruction confirms both REQUIRED. Source: [BC[CQA-2] + cross-agent convergence section].

**CQA BUILD-CHALLENGE on param name** — PASS. `_path_is_archive(path: str)` at line 567 confirmed. CQA's convention alignment is correct. TA r2 accepts and updates IC[1] signature to `path: str`. Source: [BC[CQA-3] + code-read phase-gate.py:567].

**Peer verification of CQA peer-verify of IE** — PASS on completeness. CQA verified IE BC-1 through BC-6 with source references and PASS verdicts. IE baseline 1253/14/1 PASS endorsement is well-grounded. No items missed.

**Overall CQA section verdict: PASS.** 13-case edge probe is thorough. H3 verdict is calibrated. 3 BUILD-CHALLENGES are well-targeted — all accepted in TA r2. Cross-agent convergence with IE is genuine independent discovery (not duplicated reasoning). No FAIL items.

## devils-advocate

### DA r2 — adversarial challenge of locked plan + ADR[1] amendment (2026-05-05)

#### Boot summary
Read scratch ENTIRELY (648 lines). Read parent build c1-scratch (ADR[6] origin), parent c3-review.md (ADR[6] residuals disposition), remediation plan, phase-gate.py:470-640 (cold-read of attack surface). ΣVerify init: ready, all 13 providers up incl. google. Procedural-substitute path engaged: ran gpt-5.4-pro reasoning-tier `challenge` on the sharpened ADR[1] amendment to compensate for r1 cross_verify infrastructure failure.

#### Cold-read primary findings (load-bearing)

**DA[#1]: ADR[6] threat-model exclusion is mis-cited |target:ADR[1] amendment, last paragraph |source-evidence:[code-read phase-gate.py:570-594 (KNOWN LIMITATION docstring) + parent c1-scratch:175-208 (ADR[6] body) + parent c3-review.md:252 (DA[#5] disposition) + parent plan-faithfulness §P2.A row 119] |severity:HIGH |→ debate**

TA's amended ADR[1] reads: "ADR[6] threat model is single-user local hook — excludes adversarial path construction (attacker would already need archive write access, which is broader than the carve-out surface). gpt-5.4 challenge is valid for multi-user adversarial context; does not apply within ADR[6] scope."

This OVERSTATES what parent ADR[6] actually established. Parent ADR[6] (c1-scratch:175-208) does NOT contain an explicit "single-user threat model excludes adversarial path construction" clause. What it contains:
- PA[2] "single-user system, ~10-50 hook fires/day" — that is a SCALE statement, not a THREAT-MODEL exclusion.
- DA[#5] disposition (c3-review.md:252): "KNOWN LIMITATIONS docstring added in-build, mechanical fix deferred (out of scope per ADR[6] day-1 BLOCK mandate)" — that is a DEFERRAL, not an EXCLUSION. Symlinks/`..`/case-fold are deferred, not declared out-of-scope-by-threat-model.
- Plan-source row 119 mandates `BLOCK at pre-archive` — that is plan-faithfulness, not threat-model coverage.

The amendment language transforms a SCALE/DEFERRAL disposition into a THREAT-MODEL EXCLUSION. That is a definitional drift. The procedural correctness of the carve-out should not rest on a threat-model claim parent ADR[6] does not actually make.

|→ revise ADR[1] amendment language. Either: (a) cite the actual parent disposition ("ADR[6] accepted these limits as deferred, not threat-model-excluded; carve-out inherits the deferral, no NEW deferral introduced"), OR (b) explicitly elevate threat-model exclusion in THIS plan with its own justification (single-user hook system + BLOCK 1 plan-lock for code files still active + write authorization upstream of compilation-complete). Option (a) is preferred because (b) re-opens DA[#11] CQoT-6 falsifiability work parent-build deferred to C2.

---

**DA[#2]: gpt-5.4-pro reasoning-tier challenge — "path-shaping becomes a capability" (procedural-substitute for missing google) |target:ADR[1] H4 claim "no new bypass class" |source-evidence:[mcp__sigma-verify__challenge gpt-5.4-pro reasoning, |source:external-openai-gpt-5.4-pro|] |severity:MEDIUM-HIGH |→ debate**

I ran reasoning-tier challenge() against gpt-5.4-pro on the sharpened claim (full evidence packet incl. predicate, marker list, parent disposition, BLOCK 1 still active). Counter-arguments captured (parse_error truncated JSON but text body intact):

  (a) **Capability inversion**: "Pre-carve-out, even if attacker could cause a write to a path whose raw string matched an archive marker, `_has_compilation_complete` still had to pass. After BLOCK 5 [carve-out], path-shaping itself becomes a capability: if the attacker can make the target look like `*-synthesis.md` plus any archive-marker substring, they suppress a distinct integrity gate that previously applied to workspace writes. That is a new bypass class in effect, even if it reuses an old classifier weakness."

  (b) **Consequence escalation**: parent ADR[6] accepted `_path_is_archive` weakness in a context where the only consequence was "archive-path misclassification." Reusing that same weak predicate to ALSO waive `_has_compilation_complete` changes the consequence to "gate removal for pre-completion writes." Same predicate, stronger downstream effect.

  (c) **Premise gap**: TA's "broader authority" framing conflates *namespace influence* (can name a path containing the marker substring) with *bypass authorization* (skip a distinct integrity gate). These are not the same.

  (d) **Integrity-gate reframe**: TA assumed `_has_compilation_complete` is "merely a convenience precondition." But misleading or attacker-placed markdown in the archive (spoofed synthesis) can affect downstream planning, audit, model-context loading, operator trust. BLOCK 1 staying active for *code files* does not eliminate this — synthesis archives are .md content files.

  (e) **Path normalization not shown**: claim assumes accepted-ADR[6] limitation transfers, but provides no evidence paths are normalized, symlink-resolved, `..`-collapsed before `_is_synthesis_archive_write`. Code-read confirms: they are NOT — `any(marker in path)` is raw substring on argv.

This is the procedural-substitute adversarial reinforcement the lead's r2 prompt requested. It converges with my DA[#1] (parent disposition is deferral, not exclusion) and DA[#3] below. Severity MEDIUM-HIGH because the carve-out is a 10-LOC change in a single-user local-hook system where realistic exposure is low — but the **argument structure** in TA's amendment overclaims, and that is a process violation that propagates if accepted.

|→ defend with concrete additions OR concede:
  Option D1: TA accepts DA[#1]+DA[#2] and rewrites amendment as "no new bypass class beyond the deferred-residuals already accepted in ADR[6]; downstream consequence is acknowledged stronger (gate-removal vs. archive-path-misclassification) but bounded by single-user hook context + BLOCK 1 for code files + upstream agent-write-authorization for synthesis content."
  Option D2: TA promotes path normalization (realpath + case-fold on macOS) into THIS build — out of scope per scope-boundary, but defensible as "the carve-out's stronger consequence justifies closing the predicate weakness now."
  Option C1 (concede): accept gpt-5.4-pro's framing that the carve-out IS a new bypass class **in effect** (consequence-escalation reading), document residual explicitly, ship under "single-user hook + BLOCK 1 active" disposition, do NOT call it "no new bypass class."
  
  Recommended: **D1** (lowest churn, restores honesty, no scope expansion). Path normalization is a real follow-up SQ but belongs to a security-track build, not WS-2.

---

**DA[#3]: H4 cold-read — suffix-collision benign-content vector |target:ADR[1] §a4 / IC[1] edge-case table |source-evidence:[independent cold-read, no XVERIFY needed] |severity:LOW-MEDIUM |→ defend**

Spawn prompt asked me to cold-read suffix-collision: "e.g., `report-2024-synthesis.md` where `synthesis` is content not role. Does ADR[1] over-grant on benign content with collision suffix?"

Cold-read result: **partial concern; bounded by Condition B**. A benign content file named `2025-Q3-customer-survey-synthesis.md` would satisfy Condition A. Condition B (must be under archive-marker substring) bounds this — the file would also need to be written to a path containing `/sigma-review/shared/archive/` (or one of the four other markers). For a non-sigma user-written content file, this is unrealistic in single-user context. The vector reduces to: an agent (or user) writes a content file ending in `-synthesis.md` to a path containing one of the markers, AND that file's content does not match an actual sigma synthesis role.

What the carve-out then does: skips compilation-complete check on that write. The file gets written. Other gates (BLOCK 1 plan-lock for code files, agent permissions) do not apply to .md content.

Bounded scope of the over-grant: the file is allowed to land in the archive without compilation-complete header. It does NOT receive any other authority — it does not auto-promote, does not auto-trigger downstream effects. Its impact is "an .md file is in the archive that arguably should not be." For single-user hook system with auditable archive directory, this is LOW residual risk.

|→ defend ADR[1] §a4 as adequate IF the amendment language is corrected per DA[#1]. Suffix-collision is real but bounded; the *honesty* defect is in the absoluteness of "no new bypass class," not in the predicate design.

---

**DA[#4]: symlink + case-fold inheritance — compounding vs. flat |target:ADR[1] amendment "inherits ADR[6] limits" |source-evidence:[code-read phase-gate.py:570-594 + parent DA[#5] disposition + DA[#2](b) gpt-5.4-pro] |severity:MEDIUM |→ debate**

TA's amendment claims the carve-out "inherits same documented limitation" from `_path_is_archive`. Cold-read: this is flat-inheritance for the predicate, but the **consequence** of the inherited limitation is now stronger.

Pre-carve-out: if `_path_is_archive` returned True for a symlinked-into-archive path, the only consequence was "treat as archive op" → still hits compilation-complete check. The inherited weakness costs nothing in that flow because the second gate catches.

Post-carve-out: if `_is_synthesis_archive_write` returns True for a symlinked-into-archive path with `-synthesis.md` suffix, the consequence is "skip compilation-complete." The inherited weakness now directly removes a gate.

This is the same point as DA[#2](b) in different framing. The predicate is flat-inherited; the consequence is compounded. The amendment should not say "inherits limits" without acknowledging the consequence-amplification.

|→ revise IC[1] docstring or ADR[1] alternatives §a4 to explicitly state: "Inherited limitations from `_path_is_archive` (symlink, case-fold, `..` traversal) are now consequence-amplified: same bypass surface, stronger downstream effect (gate removal vs. classification only). Accepted per single-user hook context; flagged as candidate for follow-up SQ in security-track build (path canonicalization + symlink resolution before predicate)."

---

#### SECONDARY challenges

**DA[#5]: over-engineering check — 5 tests vs simpler alternative |target:SQ[3] |source-evidence:[scope-boundary + IE BC-3 + CQA EC[3]] |severity:LOW |→ defend**

Lead asked: could 1 test suffice, or is 5 under-shooting? Defend the count.

Cold-read: 5 tests is correct, not creep. Each tests a distinct predicate condition or boundary:
- (a) positive case: Condition A ∧ Condition B both hold, no header → PASS (carve-out fires)
- (b) positive case in active session: same as (a) but explicitly exercises the post-FP-guard path (CQA's clarification — "fresh sigma session" was ambiguous; (b) now distinct from (a) in session-marker fixture, not in predicate logic)
- (c) regression: WS-1 R2-micro multi-path resolution unaffected — guards against introducing a different bug class
- (d) negative case Condition A failure: non-synthesis archive write still BLOCKED — guards against over-broad short-circuit (catches "all archive writes carved out" implementation bug)
- (e) negative case Condition B failure: synthesis path outside archive still BLOCKED — guards against Condition-A-only implementation (catches "any -synthesis.md anywhere is exempt" implementation bug)

(d)+(e) are NOT redundant — they bound the predicate on two independent dimensions. A single combined test would mask which condition the predicate failed on if a regression appears. The 5-test design is the minimum that bounds the AND-predicate on both legs plus the regression boundary. Defendable.

Are (a) and (b) the same test in different framing? **No, by CQA's BC-1 clarification.** (a) tests a workspace state (no compilation-complete header in workspace.md), (b) tests an active-session-with-build-scratch state with no header anywhere. Different fixture configurations. Both reach the carve-out short-circuit and both must PASS. Removing (b) would leave a hole on the post-FP-guard, multi-path-resolution path. Defendable.

Could 1 test suffice? No — 1 test covers either positive-only (and misses both negative dimensions) or one negative-only (and misses positive). The carve-out's logic is `Condition A AND Condition B → exempt`; bounding only one outcome leaves the other implementation-bug class unguarded.

|→ defend 5-test count.

---

**DA[#6]: spec drift on test scope — TA absorbed IE BC-3 + CQA EC[3] + CQA BC-1 |target:SQ[3] revision history |source-evidence:[TA r2 scratch:267-301] |severity:LOW |→ defend**

Cold-read: each absorption is load-bearing, not creep.
- BC-3 (IE) → test (d): catches Condition-A-failure implementation bug. Not in original Q3.
- EC[3] (CQA) → test (e): catches Condition-B-failure implementation bug. Not in original Q3.
- BC-1 (CQA test-b ambiguity) → test (b) restated: closes a fixture-semantics defect that would have made (b) test the wrong thing. Not new test, restated existing one.

Original Q3 (3 tests) was insufficient — both implementation-bug classes were reachable without test failure. The growth from 3→5 is gap-closure, not creep. SQ[3] target 1258/14/1 is correct.

|→ defend.

---

**DA[#7]: assumption conflict — H1 path-class vs C0 clause alternative |target:H1 lead-pre-validation |source-evidence:[scratch:25-26 H1 disposition] |severity:LOW |→ concede**

Lead asked: meaningful alternative dismissed too quickly? E.g., compilation-complete-not-required as explicit precondition tag at write-time vs. path-class detection at gate-time.

Cold-read: H1 was lead-pre-validated before agent spawn. The alternative (write-time precondition tag) is structurally weaker for this case:
- Path-class detection at gate-time: deterministic, single-point-of-decision, no upstream coordination required.
- Write-time precondition tag: requires every synthesis-write call site to set the tag correctly, distributes the responsibility, and reintroduces coordination between gate and write-callers (which is exactly what BLOCK 5's compilation-complete header coupling created).

The alternative is not dismissible because it is wrong — it is dismissible because it has the same structural defect (caller-gate coupling) that the carve-out was meant to eliminate. H1 lead-pre-validation is sound.

|→ concede H1 disposition.

---

**DA[#8]: source-provenance audit (§2d) |target:full TA section |source-evidence:[full scratch grep] |severity:LOW |→ defend with one note**

Scanned TA section for unsourced load-bearing claims. Findings:
- All ADR[1] alternatives §a1-§a4 have explicit reasoning (no "obviously" claims).
- IC[1]/IC[2] have code-line citations (line 567, 596, 631, 634).
- PM[1-5] have either |source: tags or self-evident structural reasoning.
- ADR[1] AMENDMENT (the one DA[#1] flags) has |source:external-openai-gpt-5.4| for the gpt-5.4 challenge but the resulting "ADR[6] threat model excludes adversarial path construction" claim has NO source pointing to where parent ADR[6] actually says that. **THAT is the unsourced load-bearing claim.** It is the same claim DA[#1] challenges substantively. From source-provenance angle: it is also a §2d violation — load-bearing claim without source citation to parent ADR[6] body.

|→ revise per DA[#1]; this is the same fix.

Also: CAL[] table cites [agent-inference] / [code-read]. CAL[3] "5 tests ≈ 65 LOC" is point-estimate without |80%=[lo,hi]|. §2i precision-gate: marginal — CAL[] is internally calibrated as "best-case" and the H2 estimate carries explicit "aspirational" qualifier. CONDITION 1 of §2i is satisfied by the qualifier. No challenge issued.

---

**DA[#9]: PROMPT-AUDIT (§7d) |target:original user prompt + scratch ## prompt-understanding |source-evidence:[user prompt: "I want to complete WS-2"; scratch:13-23 Q1-Q6, H1-H4] |severity:LOW |→ pass**

Read original user prompt. The user said "complete WS-2" — that is a scope identifier, not a methodology directive. Decomposition into Q1-Q6 + H1-H4 came from the remediation plan §WS-2 and lead's prompt-understanding mapping, not from prompt-language echo.

PROMPT-AUDIT: echo-count:0 |unverified-claims:0 |missed-claims:none |methodology:investigative

Verbatim echoes from prompt: zero. Methodology test (could the plan have produced a contradictory result?): yes — plan-track could have flagged the carve-out as unviable (e.g., predicate-design impossible to bound), CQA could have flagged the AND-predicate as insufficient, IE could have flagged feasibility issues. None did, but the methodology was not pre-committed to confirmation. Investigative ¬confirmatory.

---

**DA[#10]: test integrity verification (§4d) |target:SQ[3] tests (a)-(e) |source-evidence:[code-read test_phase_gate.py:776-796 + IC[1] edge-case table] |severity:LOW |→ defend with one regression-test note**

Per spawn prompt — for each test, identify the regression it catches:

- (a) `synthesis archive + no compilation-complete header → PASS`: catches regression where someone accidentally adds the compilation-complete check back into the synthesis path (or removes the carve-out short-circuit entirely). Failure state: short-circuit not reached → falls through to `_has_compilation_complete` → no header → BLOCK. Real regression test.

- (b) `active session + no header + synthesis path → PASS`: catches regression where the carve-out is gated on workspace state in a way that breaks for active-session-no-header. Failure state: same as (a) but in different fixture. Distinct fixture exercises the FP-guard-passed-through-to-carve-out path. Real regression test, NOT duplicate of (a).

- (c) `WS-1 R2-micro multi-path unaffected`: catches regression where the carve-out short-circuit is placed BEFORE the WS-1 R2-micro logic, breaking it for non-synthesis archive writes that need the multi-path resolution. Failure state: carve-out runs unconditionally → never reaches `_has_compilation_complete` → WS-1 logic dead. Real regression test. **Note: this test is NOT a duplicate of (a) because it specifically exercises the preferred-build scan path that WS-1 R2-micro added.** Defendable.

- (d) `non-synthesis archive write → BLOCKS`: catches regression where carve-out short-circuits ALL `is_archive_op` paths (Condition A check skipped). Failure state: returns PASS for `*-workspace.md` archive writes that should be blocked. Real regression test.

- (e) `synthesis path outside archive → BLOCKS`: catches regression where carve-out fires on Condition A only (Condition B check skipped). Failure state: returns PASS for `/tmp/foo-synthesis.md`. Real regression test.

All 5 tests have a state where they fail. None are tautologies. None are hardcoded-value tests. None mock the gate logic itself (they exercise it through the public `check_pre_archive_gate` interface). |→ defend.

---

#### Adjacent observation — XVERIFY status note

TA section says XVERIFY[partial-openai-only-google-503-transient]. I just ran `mcp__sigma-verify__init` and google IS available in this session (gemini-3.1-pro-preview listed). The 503 was transient at TA spawn time. If lead wants tighter coverage, a google `verify_finding` on the corrected ADR[1] amendment (post-DA[#1] revision) is now feasible. Not gating my exit-gate verdict on it, but flagging the option.

---

#### DA[exit-gate-r2] verdict

**DA[exit-gate-r2]: FAIL — single conditional-block on ADR[1] amendment language correction (DA[#1] + DA[#2] + DA[#4] converge on same fix) |belief-input: P=0.78 IF DA[#1] revision applied; P=0.62 if not |concerns: ADR[1] amendment overstates parent ADR[6] disposition; gpt-5.4-pro reasoning-tier counter-argument (capability-inversion + consequence-escalation) is uncontested; flat-inheritance language ignores consequence-amplification**

Rationale: predicate design (Condition A ∧ Condition B), test coverage (5 tests), implementation feasibility (IE BC-R2), edge-case probe (CQA 13 EC), CAL[] calibration, PM[1-5], scope-boundary discipline — all PASS. The single defect is the **amendment language** TA wrote in response to gpt-5.4 r1 challenge: it converted a "deferred residual" parent disposition into a "threat-model exclusion" claim that parent ADR[6] does not actually support. This is a §2d source-provenance violation (DA[#8]) AND a substantive overclaim (DA[#1]+DA[#2]+DA[#4]).

The fix is small (rewrite one paragraph in ADR[1]) and does not require build-scope expansion, scope-boundary breach, or test changes. Build-track can proceed as planned once ADR[1] amendment is rewritten per DA[#1] Option D1.

**If the fix is applied: P=0.78 plan-ready** (above 0.6 plan-track refine threshold; below 0.85 lock threshold by 0.07 — that residual is the inherited consequence-amplification carried as documented limitation, plus the still-deferred path-canonicalization SQ that belongs to a future security-track build).

**If the fix is not applied: P=0.62 plan-ready** (Toulmin-debate-eligible; below 0.85 lock threshold; above 0.6 escalate threshold).

Recommended path: TA r3 absorbs DA[#1] Option D1 (3-5 sentence rewrite of amendment), no other plan changes needed. Lead recomputes BELIEF[plan-r3] post-rewrite. Expected P[plan-r3] ≈ 0.82-0.86 depending on whether google verify_finding is also obtained on the rewritten amendment.

---

### Peer Verification: devils-advocate verifying tech-architect

**ADR[1] body (Decision + Rationale + Alternatives §a1-§a3)** — PASS. Two-condition predicate (Condition A: case-sensitive `-synthesis.md` suffix; Condition B: marker substring) is well-grounded in code-read (phase-gate.py:128, 596). Rationale tied to Step 13f→14a structural cycle is traceable to remediation plan §WS-2 + parent c3-review.md. Alternatives §a1 (regex), §a2 (INDEX scan), §a3 (A28 WARN-only) considered with explicit rejection criteria. BC-1 alignment with `_path_is_archive` line-596 pattern (rather than `os.path.dirname`) is correct and consistent with parent ADR[6] DA[#5] disposition. Evidence-grounded. |artifact-IDs: ADR[1], IC[1], phase-gate.py:567-596, parent-c3-review.md:252|

**ADR[1] §a4 alternative (blanket archive exemption rejected)** — PASS. Rejection rationale is structurally correct: blanket exemption removes the gate for all archive writes; only synthesis writes have the structural-impossibility argument. The two-condition predicate is more restrictive than §a4 — that is a real distinction, not pro-forma. Defends choice with positive engagement of the alternative. |artifact-IDs: ADR[1] §a4, scratch:117|

**ADR[1] AMENDMENT (post-XVERIFY[partial-openai])** — **FAIL** per DA[#1]+DA[#2]+DA[#4] (this section). The substantive amendment to qualify "no new bypass class" is correct in spirit (gpt-5.4 r1 challenge IS valid and the absolute claim was too strong). The fix is to rewrite the amendment's grounding: reference parent ADR[6]'s actual disposition (deferred residuals, plan-faithful BLOCK day-1) instead of asserting an explicit threat-model exclusion that parent ADR[6] does not contain. Single load-bearing artifact failed; build-track can proceed once rewritten. |artifact-IDs: ADR[1] AMENDMENT, parent-c1-scratch:175-208 (ADR[6] body absent the cited exclusion), parent-c3-review.md:252 (deferral language), gpt-5.4-pro reasoning-tier challenge|

**IC[1] typed contract** — PASS. 12-row edge-case table covers all H3 probe cases. Fail-safe direction (False on ambiguity) correctly chosen. BOM/whitespace strip is improvement over `_path_is_archive` (CQA EC[6]). Parameter rename `path: str` per CQA BC-3 absorbed. Placement at line 597 (after `_path_is_archive`) verified by code-read. **One note for the implementation engineer:** EC[5] symlinks and EC[4] case-fold rows in the table say "False" without the consequence-amplification context DA[#4] surfaces. The IC[1] docstring is accurate at the predicate level; the surrounding plan-doc should carry the consequence note. Not a FAIL on IC[1] itself. |artifact-IDs: IC[1], CQA EC[1-13], code-read phase-gate.py:567|

**IC[2] short-circuit insertion contract** — PASS. Insertion point after line 631 / before line 634 verified by code-read. Return form `(False, "")` matches existing PASS paths (lines 607, 636). `archive_path and` None-guard correct fail-safe per PM[4]. FP-guard ordering preserved (`_is_sigma_session` at line 606 still fires first). Implementation-engineer's BC-2 precision concern fully absorbed. |artifact-IDs: IC[2], phase-gate.py:606,631,634, IE BC-2|

**SQ[1-5] decomposition** — PASS. Five sub-tasks correctly sequenced (SQ[1] helper → SQ[2] short-circuit depends-on SQ[1] → SQ[3] tests depend-on SQ[1]+SQ[2] → SQ[4] doc edits independent → SQ[5] empirical post-build). Test count 5 (per IE BC-3 + CQA EC[3] + lead r2) defended by DA[#5]+DA[#6]. Target 1258/14/1 internally consistent. |artifact-IDs: SQ[1-5], IE BC-R2-1, CQA cross-agent convergence|

**PM[1-5] pre-mortem** — PASS. All 5 scenarios have probability + early-warning + mitigation. PM[1] file-overlap with WS-3 SQ-T1 — IE BC-R2-2 confirms `_strip_fenced_blocks` absent in current phase-gate.py, additive inserts only, mitigation sufficient. PM[2] suffix-collision aligned with my DA[#3] cold-read (bounded by Condition B). PM[3] case-fold aligned with CQA EC[4] + my DA[#4] consequence-amplification note. PM[4] None-guard verified by IE BC-R2-4. PM[5] over-broad short-circuit closed by SQ[3] test (d). |artifact-IDs: PM[1-5], IE BC-R2-2, CQA EC[4]|

**XVERIFY[partial-openai-only-google-503-transient]** — PASS-WITH-UPDATE. Disposition at TA spawn time was correct (google 503 transient). My init shows google now available; that does not retroactively invalidate the partial-openai disposition, but lead may opt to obtain google verify_finding on the corrected ADR[1] amendment in r3. The DA r2 procedural-substitute (this section, gpt-5.4-pro reasoning-tier challenge) compensates for the original cross_verify gap on the H4 claim per spawn-prompt instruction. |artifact-IDs: XVERIFY status, mcp__sigma-verify__init result this session|

**CAL[] effort estimates** — PASS. Three independent estimates (TA ~135 min, IE ~2-3h, CQA convergent) cluster at 2.25-2.5h. CONDITION 1 of §2i (precision gate) satisfied by aspirational qualifier on H2 + per-SQ breakdown. No marginal-budget overclaim. |artifact-IDs: CAL[1-5], IE CAL[IE-1]|

**Overall TA section verdict: PASS-CONDITIONAL.** 9 of 10 verified artifacts PASS. One artifact (ADR[1] AMENDMENT) FAIL on overclaim language; small rewrite restores PASS. Build-track is ready to proceed once amendment rewritten per DA[#1] Option D1. No predicate change, no test change, no scope change. PASS-CONDITIONAL on r3 absorption of DA[#1].

---

#### DA convergence

✓ DA r2 — 10 challenges (4 primary high/med severity + 6 secondary low severity)
✓ Procedural-substitute XVERIFY: gpt-5.4-pro reasoning-tier challenge run, captured in DA[#2]
✓ PROMPT-AUDIT: echo-count:0 |unverified-claims:0 |missed-claims:none |methodology:investigative
✓ Source-provenance audit (§2d): 1 unsourced load-bearing claim (= DA[#1]/DA[#8] same fix)
✓ §4a scope-creep: clean (5-test count defended DA[#5], absorptions defended DA[#6])
✓ §4b assumption conflict: H1 disposition conceded DA[#7]
✓ §4c gold-plating: none (TIER-1 stays TIER-1, no spec creep, no out-of-phase work)
✓ §4d test integrity: all 5 tests have failure states (DA[#10])
✓ Toulmin warrant checks: ADR[1] §a4 has explicit reversal condition (CQoT-6 falsifier present); steelman of blanket §a4 alternative is genuine (CQoT-7 PASS); confidence-gap obtainable (CQoT-8 PASS) — *if* amendment is rewritten, these hold; if not, CQoT-7 marginal-fail on the unverified threat-model exclusion claim
✓ Peer verification of TA: 9 PASS + 1 FAIL (ADR[1] AMENDMENT) + 1 PASS-WITH-UPDATE (XVERIFY) — written above
✓ Exit-gate verdict written: FAIL conditional on DA[#1] rewrite; P=0.78 if applied / P=0.62 if not
◌ WAITING for plan-track r3 response — NOT terminating per spawn-prompt step 9

### r3 verification — TA-r3 amendment rewrite (2026-05-05)

#### Boot summary
Lead dispatched r3 verification round. Original tech-architect r3 hung in MCP transport (sigma-verify multi-call); lead killed 2 orphan processes (84272+59342) and respawned `tech-architect-r3` with scope-collapsed amendment-only brief. TA-r3 delivered `### r3 amendment rewrite` at scratch:521-570. Cold-read against my DA[#1/2/4/8] dispositions + checked sharper distinction lead briefed (PA[2] = SCALE, distinct from DA[#5] = DEFERRAL).

#### Cold-read against DA[#1] — parent ADR[6] established DEFERRAL not THREAT-MODEL-EXCLUSION

✓ **Retraction explicit.** Line 525: "is retracted." TA-r3 names the offending phrase and removes it — no silent rewording.

✓ **Source-grounded citations.** Lines 533-536 cite the exact three pieces of parent ADR[6] body I cited in DA[#1]:
  - PA[2] scale statement at parent c1-scratch:175-208
  - DA[#5] disposition at parent c3-review.md:252
  - Plan §P2.A row 119 ("BLOCK at pre-archive")
All three citations are verifiable in parent build files (I verified them in DA r2 boot). Source-provenance restored.

✓ **§2d violation named.** Line 538: "The phrase 'excludes adversarial path construction' from the r2 amendment is removed. It had no source in parent ADR[6] body — this was a §2d source-provenance violation (DA[#8])." TA-r3 explicitly acknowledges the violation rather than papering over it.

✓ **Sharper distinction validated.** Line 534: "PA[2] '...' is a SCALE statement, not a threat-model exclusion clause." TA-r3 separated SCALE (PA[2]) from DEFERRAL (DA[#5] disposition) — two distinct parent dispositions, neither of which is a threat-model exclusion. My DA[#1] grouped them as "SCALE/DEFERRAL disposition"; TA-r3's separation is sharper. Validates as correct: parent build c1-scratch:66 confirms PA[2] reads as scale ("single-user system, ~10-50 hook fires/day per session"), parent c3-review.md:252 confirms DA[#5] reads as deferral ("KNOWN LIMITATIONS docstring added in-build, mechanical fix deferred").

**DA[#1] verdict: CLOSED.**

#### Cold-read against DA[#4] — flat-inheritance at predicate, compound-inheritance at consequence

✓ **Consequence-amplification acknowledged in IC[1] subsection (lines 542-544).** Direct quote: "synthesis-archive-write-spoof has a stronger downstream consequence than archive-classification-spoof. Where ADR[6]'s `_path_is_archive` only affects classification, this carve-out's predicate skips an integrity gate (compilation-complete is an integrity boundary, not merely convenient)."

✓ **Integrity-gate reframe absorbed.** TA-r3 explicitly reclassifies compilation-complete as "integrity boundary, not merely convenient" — directly absorbs gpt-5.4-pro counter-argument (d) from my DA[#2]. Not a hedge.

✓ **Both inheritance levels stated explicitly.** Line 544: "flat-inheritance at the predicate level, compound-inheritance at the consequence level. Both stated explicitly; no new deferral introduced beyond ADR[6]'s accepted residuals." This is the exact framing I requested in DA[#4]'s "→ revise" recommendation.

✓ **Capability-inversion bounded, not denied.** Line 552 (DA[#2] response): "The carve-out introduces path-shaping as a capability in effect; bounded by single-user context and upstream authorization, but not denied." TA-r3 concedes the capability-inversion framing (gpt-5.4-pro counter-argument (a)) and bounds rather than denies it.

**DA[#4] verdict: CLOSED.**

#### Cold-read against DA[#8] — §2d source-provenance audit

✓ **Unsourced load-bearing claim removed.** The "excludes adversarial path construction" claim that had no parent-body source is gone (line 538 explicit removal).

✓ **Replacement claims are sourced.** Every replacement claim in the rewrite cites a verifiable parent location (lines 533-537 = c1-scratch:175-208 + c3-review.md:252 + plan §P2.A row 119). Cross-checked against parent build files in DA r2 — all three locations contain the cited content.

**DA[#8] verdict: CLOSED.**

#### Cold-read against DA[#2] — gpt-5.4-pro reasoning-tier counter

✓ **All 4 counter-arguments acknowledged.** TA-r3 line 552: "capability-inversion + consequence-escalation + integrity-gate-reframe acknowledged in consequence-amplification note above." Path-normalization absence (counter (e)) is preserved in deferral framing — line 531 says "ADR[6]'s deferred mechanical fix (e.g., path-normalization, fenced-block-strip) remains deferred and applies equally to this carve-out." Honest framing of the unfixed weakness.

**DA[#2] verdict: CLOSED.**

#### Internal consistency check

✓ Line 529: "BLOCK 1 for code files (carve-out only fires on synthesis-archive paths, not code paths)" — consistent with phase-gate.py architecture. Code-read confirms: BLOCK 1 plan-lock applies to code-file paths, BLOCK 5 carve-out applies only when `is_archive_op` is True AND synthesis predicate matches. Boundedness claim is real, not aspirational.

✓ Line 531: predicate-level flat-inheritance + consequence-level compound-inheritance is internally consistent with ADR[1] §a4 rejection of blanket exemption (the consequence-asymmetry argument that justified narrower predicate also justifies the consequence-amplification disclosure).

✓ Line 568 TA-r3 self-belief P=0.82 carries explicit residual ("r4 multi-model XVERIFY corroboration not yet externally verified"). Honest residual, not over-confident.

#### Cosmetic vs substantive test

The rewrite would be **cosmetic** if it: (a) replaced "excludes adversarial path construction" with "is bounded by single-user context" without adding consequence-amplification, (b) didn't cite parent body locations, (c) didn't name the §2d violation.

The rewrite is **substantive** because it: (a) explicitly retracted the offending phrase + added new consequence-amplification subsection in IC[1] reclassifying compilation-complete as integrity boundary, (b) cited three verifiable parent body locations, (c) named the §2d violation by reference to DA[#8], (d) introduced the SCALE/DEFERRAL distinction with sharper separation than my own DA[#1] framing.

This passes the substantive test on all four dimensions.

#### Carry-forward to C2/C3

Two items deferred to later phases per lead instruction (¬basis for r3 FAIL):
- **r4 multi-model XVERIFY** (lead's call): if BELIEF[plan-r3] lands short of 0.85 lock threshold, lead may run google `verify_finding` (and/or other paid providers per build-directives §2h fallback) on the rewritten amendment. Three existing validators on H4: r1 XVERIFY[partial-openai] PARTIAL/MEDIUM, r2 procedural-substitute via challenge gpt-5.4-pro reasoning (4-arg convergence), r3 cold-read of rewrite. Adequate for lock with documented residual; multi-model corroboration would push P toward 0.86+.
- **Path-canonicalization SQ** (security-track follow-up): consequence-amplification note in IC[1] flags this as candidate for future security-track build. Not in WS-2 scope. Lead may add to backlog or defer to a future remediation pass.

#### DA[exit-gate-r3] verdict

**DA[exit-gate-r3]: PASS |belief-input: P=0.83 |closed: DA[#1, #2, #4, #8] |carry-forward: r4-XVERIFY (lead-decision), path-canonicalization-SQ (security-track-future)**

Rationale: the four converging concerns from r2 (DA[#1]+DA[#2]+DA[#4]+DA[#8]) are all closed by the r3 rewrite. The fix is substantive, not cosmetic — explicit retraction, sourced citations, integrity-gate reframe, consequence-amplification disclosure. TA-r3 also surfaced a sharper distinction (PA[2]=SCALE separated from DA[#5]=DEFERRAL) that my own DA[#1] grouped together; this is genuine analytical work rather than minimal compliance.

Belief input P=0.83 (was P=0.78 in DA r2 "if applied" estimate; revised upward by +0.05 because the rewrite's analytical sharpness exceeded my Option D1 specification). P=0.83 is below the 0.85 lock threshold by 0.02 — that residual is the unverified r4 multi-model corroboration (one paid provider has cleared at MEDIUM, one not yet attempted in r3). Lead's call whether to run r4 XVERIFY or accept the documented residual.

If lead opts for r4 XVERIFY and google verify_finding returns convergent: expected P ≈ 0.86-0.88, lock-eligible. If lead accepts residual: lock at P=0.83 with documented carry-forward to C2 cross-build authorization integrity verification.

**No new DA challenges. Plan is build-ready.** All previously-FAIL items now PASS. Build-track can proceed.

#### Peer-verify TA-r3 rewrite delta

**ADR[1] AMENDMENT (post-r3 rewrite)** — **PASS** (was FAIL in r2). Three-citation grounding (PA[2], DA[#5] disposition, plan §P2.A row 119) is accurate, retraction is explicit, §2d violation is named. Single load-bearing artifact flipped from FAIL to PASS. |artifact-IDs: ADR[1] AMENDMENT r3, parent c1-scratch:175-208, parent c3-review.md:252, plan §P2.A row 119|

**IC[1] consequence-amplification note (NEW in r3)** — PASS. New subsection at scratch:542-544 reframes compilation-complete as integrity boundary, names flat/compound inheritance at predicate/consequence levels, cites gpt-5.4-pro reasoning. Honest framing. |artifact-IDs: IC[1] consequence-amplification, gpt-5.4-pro counter-arguments (a)+(b)+(d), DA[#4]|

**TA-r3 self-belief P=0.82** — PASS-WITH-NOTE. Self-belief is conservative (DA r3 verdict came in at P=0.83); residual claim ("r4 multi-model XVERIFY corroboration not yet externally verified") is honest. Self-belief differential is +0.01 below DA verdict — within calibration noise, no concern. |artifact-IDs: TA-r3 self-belief, DA[exit-gate-r3]|

**Overall TA-r3 section verdict: PASS.** All four DA r2 concerns closed substantively. No new challenges. Build-track unblocked.

✓ R3 verification complete. WAITING for promotion-round. NOT terminating per spawn-prompt step 9.

✓ code-quality-analyst — promotion-round COMPLETE (2026-05-05)
H3 CONFIRMED-WITH-DOCUMENTED-LIMITATIONS: 13 edge-cases enumerated; predicate sound for nominal paths; EC[4] case-fold over-gating accepted per DA[#5]; EC[2] None/non-string resolved by IC[1] isinstance guard; EC[3] conjunction-guard gap flagged (missing 5th test for synthesis-outside-archive). 3 BUILD-CHALLENGE entries: test(b) path ambiguity, EC[3] 5th test (cross-agent convergence IE BC-3), param name file_path→path. Peer-verify of IE: 6 items PASS. sigma-mem store_agent_memory FAILED (MCP internal error, 1 attempt). Calibration deferred to scratch:

FALLBACK-CALIBRATION[code-quality-analyst — sigma-mem unavailable, lead to store_agent_memory post-session]:
CQA-CAL[1] DA[#12] path-predicate 13-case checklist 2026-05-05: structured probe for filesystem path predicates — (1)empty string (2)None/non-string (3)target substring but wrong parent dir (4)case-fold HFS+/APFS (5)symlinks (6)BOM/whitespace (7)trailing/double-slash/".." segments (8)double-suffix .bak/.swp (9)newline/null byte (10)relative vs absolute (11)target substring mid-name not at end (12)empty filename (13)correct suffix wrong parent dir sibling. Apply before locking any path-gating predicate. Source: H3 probe WS-2 BLOCK 5. H3=CONFIRMED-WITH-DOCUMENTED-LIMITATIONS.
CQA-CAL[2] EC[4] inheritance direction flip 2026-05-05: when inheriting a documented limitation from ancestor predicate, verify the direction. DA[#5] on _path_is_archive = UNDER-gating (bypass; security miss). Same case-fold on _is_synthesis_archive_write = OVER-gating (valid write blocked; operational miss). Under-gating and over-gating have different consequence profiles. Classify direction explicitly before accepting inherited limitation — "same limitation" ≠ "same consequence."
CQA-CAL[3] conjunction predicate negative test pattern 2026-05-05: N-condition conjunction requires N independent negative tests, one per condition. CQA EC[3] (synthesis-outside-archive = Condition B failure) + IE BC-3 (non-synthesis-in-archive = Condition A failure) converged from independent angles on same structural test gap. Cross-agent convergence on same finding = high-confidence real gap. Pattern: when probing any conjunction predicate, enumerate both failure modes independently.
CQA-CAL[4] plan-track param-name style check 2026-05-05: compare proposed helper param names against nearest sibling in same module. file_path vs path misalignment with _path_is_archive caught in IC spec phase = cheap fix. Convention drift propagates to build-track implementations if missed in spec. Pattern: param names checked against sibling signatures during IC peer review, not just types.
