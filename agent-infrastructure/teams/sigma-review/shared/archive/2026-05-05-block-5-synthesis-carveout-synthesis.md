# Synthesis Artifact: 2026-05-05-block-5-synthesis-carveout

- build-id: 2026-05-05-block-5-synthesis-carveout
- tier: BUILD TIER-1 (score 6/25)
- conversations: C1 (plan, 4 rounds) → C2 (build, 1 incident-recovered cycle) → C3 (review, 1 round CONVERGE)
- final-belief: P=0.91 (C3-r1 lead synthesis, +0.04 from C2 entering 0.87)
- DA-grade: PASS (DA r1 P=0.93, 0 unresolved tensions)
- BUILD rubric §3b mean: 3.67/4.00
- artifact-source: plan file + c3-scratch + c2-scratch + c1-scratch
- written: 2026-05-09 by synthesis-agent (separate context firewall)

---

## 1. Prompt Decomposition

The plan §Prompt Understanding (plan.md:40-64) committed to six questions (Q[]), four hypotheses (H[]), and seven constraints (C[]). All Q[] became sub-tasks with locked Interface Contracts. All H[] resolved with sourced verdicts. All C[] were honored or amended honestly.

### Q[] (six work items, all addressed)

| ID | Scope | Resolution path | Outcome |
|---|---|---|---|
| Q1 | Add `_is_synthesis_archive_write(path: str) -> bool` helper near `_path_is_archive` | ADR[1] + IC[1] (plan §85-156) → SQ[1] | DONE @ phase-gate.py:623-646 (IC[1] docstring 11/11 verbatim, 7 input-normalization behaviors mechanically present) — c2-scratch §264 (F[CQA-1]), c3-scratch §241-245 (TA PLAN-REVIEW VERIFIED) |
| Q2 | Short-circuit in `check_pre_archive_gate` exempting synthesis-archive writes | IC[2] (plan §158-180) → SQ[2] | DONE @ phase-gate.py:684-687 (positioned AFTER `is_archive_op` guard, BEFORE `_has_compilation_complete`, with `archive_path and` PM[4] fail-safe) — c2-scratch §280-282 (F[CQA-9/10]), c3-scratch §247-251 (TA VERIFIED) |
| Q3 | New `TestBlock5SynthesisCarveOut` test class (revised 3→5 per IE BC-3 + CQA EC[3]) | SQ[3] (plan §185-198) | DONE — 5/5 PASS in `TestBlock5SynthesisCarveOut` @ test_phase_gate.py:1293-1464; tests (a)/(b)/(c)/(d)/(e) cover main path, carve-out short-circuit DIRECTLY, WS-1 R2-micro regression, Condition A failure, Condition B failure — c2-scratch §297-326, c3-scratch §358 |
| Q4 | Cross-ref in `directives.md` §8f BUILD variant | SQ[4] | DONE @ directives.md:1353 — Tier-1 ΣComm pipe-delimited entry naming predicate + both Conditions + ADR[1] source-tag (c2-scratch §348-353, c3-scratch §255) |
| Q5 | Cross-ref sentence at `sigma-lead.md:206-207` Step 7b | SQ[5] | DONE @ sigma-lead.md:207 — Tier-3 plain English, all 4 required tokens (Step 13f, synthesis, compilation-complete, carve-out) (c2-scratch §355-360, c3-scratch §257) |
| Q6 | Empirical 5-scenario verification per remediation §WS-2 | SQ[6] | DONE — 5/5 PASS (1 with documented environmental confound on scenario-2; underlying invariant verified via unit test). Hook-suite parity 1286/14/0 EXACT MATCH (delta=+5 from 1281 baseline) — c2-scratch §129-162 |

### H[] (four hypotheses, all addressed)

- H1 "Path-class exemption is cleaner than §8f C0 clause." — lead-validated; XVERIFY-corroborated (4 rounds in C1); LOCKED IN ADR[1] (plan §52, c1-scratch §107).
- H2 "Scope is ~10 LOC + 5 tests + ~2.3h work." — CAL[] honest revision from 2h aspirational to ~140 min (plan §53, c1-scratch §224-235).
- H3 "Suffix `-synthesis.md` + `shared/archive/` membership is sufficient predicate." — CQA 13-case probe at C1 (c1-scratch §669-705) + IE peer-verify importlib live-replay at C2 (c2-scratch §397-401, 5/13 EXACT MATCH); CONFIRMED-WITH-DOCUMENTED-LIMITATIONS (HFS+ case-fold over-gating accepted, agent generates lowercase).
- H4 "Carve-out introduces no new authorization-bypass class." — DA r2 (c1-scratch §876-907) caught absoluteness drift; r3 amendment correctly framed as DEFERRAL not exclusion (c1-scratch §564-582); H4 verdict PARTIAL — predicate narrower than §a4 alternative but introduces nominal new capability surface bounded by single-user context + upstream agent-write-authorization + BLOCK 1 for code files.

### C[] (seven constraints, all honored)

- C1 TIER-1 (3+DA) per §3a; score 6/25 maintained through close.
- C2 WARN-first ¬applicable — gate-fire reduction, not new gate.
- C3 Hook-suite parity reframed at C2 boot: plan-lock baseline 1253/14/1 → measured C2-boot baseline 1281/14/0 (+28 from commits 437096c + 0559289 between plan-lock and C2-start) → final 1286/14/0 (delta=+5). Plan §C3 expectation 1253→1258/14/1 superseded by honest delta-parity.
- C4 TeamCreate used at all three conversations; XVERIFY excluded anthropic per feedback_xverify-anthropic-excluded (c1-scratch §11).
- C5 WS-1→WS-2 phase gate satisfied (commit f8b94ae→755e9c8); WS-2→WS-3 sequencing held (this build closes before WS-3 c1-plan starts).
- C6 ΣComm preserved in directives (Tier-1 @ directives.md:1353); plain English in agent-defs (Tier-3 @ sigma-lead.md:207).
- C7 ¬sed-i discipline held; section-isolation maintained; Edit tool used for the C3 plan-line:289 fix per `:sed-i` audit-flags-recurring ban (c3-scratch §461 F[CQA-4]).

---

## 2. Findings Organized by Domain

Three tracks operated independently with cross-track convergence at C3-r1: plan-track (TA) for fidelity, build-track (IE+CQA) for implementation+verification, adversarial (DA) for challenge. Findings retain their track-of-origin attribution.

### 2.1 Plan-track (tech-architect)

**C1 plan design (4 rounds: r1 design + r2 challenge + r3 amendment-fix + r4 multi-model XVERIFY corroboration).**

- ADR[1] decision (plan §85-99, c1-scratch §99-118): two-condition predicate (Condition A: basename `-synthesis.md`; Condition B: any `_ARCHIVE_PATH_MARKERS` substring). Both required. Fail-safe: ambiguity → False. Three alternatives explicitly rejected (§a1 regex, §a2 INDEX-based scan, §a3 A28 WARN-only); §a4 (blanket archive exemption) rejected as removing gate for all archive writes when only synthesis writes have the structural-impossibility argument.
- ADR[1] AMENDMENT (plan §101-110, c1-scratch §564-582): post-DA r2 Option D1 rewrite. Original "no new bypass class" claim was too absolute (DA[#1] catch). Corrected to "no new bypass class **beyond the deferred-residual limitations already accepted in ADR[6]** of parent build." Source-grounded to parent c1-scratch:175-208 + DA[#5] disposition + plan §P2.A row 119. Consequence-amplification (DA[#4] CONCEDE): synthesis-archive-write-spoof has stronger downstream consequence than archive-classification-spoof — gate-removal vs. classification-only.
- IC[1] typed contract (plan §122-156, c1-scratch §124-168): 11-line docstring locked verbatim; 7 input-normalization behaviors specified; 13-row edge-case table.
- IC[2] short-circuit integration (plan §158-180, c1-scratch §172-198): exact insertion point AFTER `if not is_archive_op: return False, ""` BEFORE `_has_compilation_complete`; `archive_path and` guard required (PM[4]).
- 5 pre-mortem failure modes (plan §202-210, c1-scratch §236-258): WS-3 sequencing (PM[1]), suffix-collision (PM[2]), HFS+ case-fold over-gating (PM[3]), `archive_path` None fall-through (PM[4]), over-broad short-circuit caught by SQ[3] tests d+e (PM[5]).
- XVERIFY (cumulative across r1-r4, plan §112-117): r1 openai gpt-5.4 PARTIAL/MEDIUM; r2 DA procedural-substitute via gpt-5.4-pro reasoning-tier; r3 DA cold-read substantive-vs-cosmetic verification PASS (4/4 axes); r4 dual-independent multi-model 5p XVERIFY — 8/10 substantive AGREE across 10 model-runs, 0 disagreements either run.

**C3 plan-track fidelity sweep (TA, c3-scratch §228-263, 14 PLAN-REVIEW findings).** All seven fidelity dimensions VERIFIED full: ADR[1] Conditions A+B + AMENDMENT r3 docstring preservation + IC[1] signature/normalization/placement/docstring-verbatim + IC[2] insertion-point/code-form/FP-guard ordering + WS-1 R2-micro regression + cross-refs + WS-2→WS-3 sequencing + :1056 carry-forward (compliance:partial → CONVERGED via 3-eye deferral). Only line-number drift relative to plan (e.g., :597→:623, :631→:684) — explained by +28-test commit drift between plan-lock and C2-start (commits 437096c + 0559289), NOT architectural drift.

### 2.2 Build-track (implementation-engineer + code-quality-analyst)

**C2 implementation (IE, c2-scratch §47-176).**

- Symbol relocation at boot (c2-scratch §52-56): plan-cited line numbers re-located by symbol — `_path_is_archive`=:591 (plan said :597, drift -6), `check_pre_archive_gate`=:623 (plan said :631, drift -8), `if-not-is_archive_op-return`=:655 (plan said :631, drift +24 because return is post the elif Bash block).
- SQ[1] DONE: `_is_synthesis_archive_write` helper @ phase-gate.py:623-646; IC[1] docstring 11/11 verbatim; 7 input-normalization behaviors mechanically present; param signature `path: str`; no new imports.
- SQ[2] DONE: short-circuit @ phase-gate.py:684-687; positioned AFTER `is_archive_op` guard BEFORE `_has_compilation_complete`; `archive_path and` guard present; `return False, ""` matches existing PASS form; comment references ADR[1] + Step 13f→14 + "logical cycle".
- SQ[3] DONE: 5 tests in `TestBlock5SynthesisCarveOut` class @ test_phase_gate.py covering carve-out main path, active-session short-circuit-direct (test-(b) is the strongest with dual pre/post sanity assertions @ :1363+:1371 mechanically proving carve-out branch is the load-bearing resolution path), multi-path resolution regression, Condition A failure, Condition B failure.
- SQ[4]+SQ[5] DONE: directives.md:1353 Tier-1 ΣComm cross-ref + sigma-lead.md:207 Tier-3 plain English cross-ref.
- SQ[6] DONE: empirical 5-scenario verification 5/5 PASS (1 with documented environmental confound on scenario-2 substitution `-not-synthesis.md` → `-workspace.md` per Q2; underlying carve-out non-firing for `-workspace.md` independently verified via unit test under isolated `patch_multi` fixture asserting BLOCK with no header). Hook-suite parity 1286/14/0 EXACT MATCH.
- Re-target authorized at lead Q1: 2 pre-existing tests in `TestBlock5MultiPathWorkspace` shifted from `-synthesis.md` to `-workspace.md` to preserve invariants shadowed by carve-out short-circuit. Path-string substitution preserves intent per sibling `test_build_id_extraction_from_archive_path` confirming `_build_id_from_archive_path` strips both suffixes identically. Docstrings updated to reference ADR[1].
- Plan-ambiguity Q2 resolved (c2-scratch §122-127): `-not-synthesis.md` literally `.endswith("-synthesis.md")` so IC[1]-faithful predicate matches it; substitute `-workspace.md` for empirical scenario-2.

**C2 review + peer-verify (CQA, c2-scratch §178-373).** 14 Wave-1 findings F[CQA-1..14] all VERIFIED: docstring 11/11 verbatim, 7/7 normalization behaviors, 13-case probe live-replayed via importlib (5/13 spot-checked by IE peer-verify), AND-not-OR enforced, return-bool-no-exceptions, placement after `_path_is_archive`, no new imports, param-name `path: str`, IC[2] insertion correct, `archive_path and` guard, return form `(False, "")`, comment references ADR[1] + Step 13f→14 + "logical cycle", FP-guard ordering preserved, ADR[1] AMENDMENT r3 5/5 required language elements present (gate-removal @ :632, stronger downstream consequence @ :632, integrity boundary @ :634, accepted residual risk + single-user hook context @ :634, deferred per ADR[6] @ :637). Wave-2 5/5 new tests + 2/2 re-targets PASS. Integration-eye SQ[4] (Tier-1 ΣComm) + SQ[5] (Tier-3 plain) PASS.

**C2 peer-verify ring closed PASS in both directions** (c2-scratch §292-432): CQA→IE Wave-1+Wave-2+Integration PASS-CONFIRMED via independent grep + importlib live-replay; IE→CQA HIGH findings sample-checked 1-3 confirm CQA verdicts; one gap (CQA inherited IE hook-suite count without independent re-run) noted and CLOSED by IE re-run 1286/14/0 in 10.91s.

**C3 build-track responses (c3-scratch §151-225).** IE r1: DEFEND with deferred follow-up SQ on DA[#2] (OVERMATCH near-miss test gap is parent-scope, ADR[6] inheritance, asymptomatic; logging as `:1056`-class follow-up SQ for `block-5-synthesis-carveout-followups` micro-build). One IE-routed editorial fix from TA's response to DA[#3]: forward-pointer at plan-line:289 added via Edit tool (not sed -i), pytest 1286/14/0 EXACT MATCH preserved.

**C3 fix-validation (CQA, c3-scratch §453-490).** PASS verdict on IE single fix at plan-line:289 (F[CQA-2/3/4/5/6/7] all VERIFIED). Independent pytest re-run from CQA agent session: 1286 passed / 14 skipped in 10.96s — closes C2 inheritance-without-rerun gap. F[CQA-8] doc-precision drift in c3-scratch §scope-boundary line 91 (says `:1335-1464` while class-def begins at :1293) RESTATE — record-only, originated C2.

### 2.3 Adversarial (devils-advocate)

**C1 challenge rounds (c1-scratch §871-1058 r2 + §1099-1188 r3 verification, 10 challenges).**

Primary cluster (4 challenges on amendment-drift):
- DA[#1] HIGH: ADR[6] threat-model exclusion mis-cited — TA's amendment converted SCALE/DEFERRAL into THREAT-MODEL EXCLUSION; that is definitional drift.
- DA[#2] MED-HIGH: gpt-5.4-pro reasoning-tier challenge surfaced capability-inversion + consequence-escalation + integrity-gate reframe + path-normalization-absent.
- DA[#4] MED: symlink + case-fold inheritance is flat-at-predicate but compound-at-consequence.
- DA[#8] LOW: §2d source-provenance violation — the threat-model-exclusion claim has no source pointing to where parent ADR[6] actually says that.

Secondary cluster (6 standard BUILD probes): DA[#3] LOW suffix-collision benign-content vector (defended via Condition B bound), DA[#5] LOW 5-test count justification (defended), DA[#6] LOW spec-drift on test scope (defended), DA[#7] LOW H1 alternative dismissal (conceded), DA[#9] LOW prompt-audit (PASS, echo-count:0), DA[#10] LOW test-integrity per-test regression-catch (defended).

DA[exit-gate-r2] FAIL → r3 TA-r3 amendment rewrite (c1-scratch §562-606) → DA[exit-gate-r3] PASS via cold-read substantive-vs-cosmetic verification (c1-scratch §1168-1188).

**C3 review challenges (DA, c3-scratch §111-149, 5 review + 3 carry-forward = 8 total).**

- DA[#1] MEDIUM (ext vuln=HIGH via openai gpt-5.4-pro reasoning): substring-overmatch as failure class independent of ADR[6] inheritance (escape-vs-spoof reframe). AMENDMENT r3 line 104 covers escape-direction (ADR[6] inheritance) but not spoof-direction (predicate-overmatch as separate failure class). Concrete example: `/tmp/sigma-review/shared/archive/foo-synthesis.md` (a /tmp path containing the marker as substring) returns True from `_is_synthesis_archive_write`.
- DA[#2] LOW: overmatch test-coverage gap — the 5 new tests do NOT cover the OVERMATCH near-miss case.
- DA[#3] LOW: plan §Verification:289 internal-inconsistency residual — Q2 resolution applied but plan §289 source list still reads `-not-synthesis.md` → exit=2.
- DA[#4] LOW: §2h security-adjacent marker absence in docstring (Consequence note names "gate-removal" + "integrity boundary" + "accepted residual risk" + "deferred per ADR[6]" but does NOT explicitly state "security-adjacent" or cite §2h).
- DA[#5] INFO: §4f circuit-breaker self-check PASS — DA[#1] is genuine adversarial output (zero-dissent NOT triggered).
- DA[CF-1] LOW: `:1056` coverage shadow on `test_header_in_build_scratch_passes_block5` post-carve-out — CONVERGED at 3-eye + IE-peer-verify CONCUR deferral.
- DA[CF-2] MEDIUM: XREVIEW infra T0/T1/T2 reframe.
- DA[CF-3] INFO: C2 process-integrity wins as Step 15 promotion candidates.

**§2d source-provenance audit C3-r1**: 5/5 load-bearing claims source-grounded → PASS (c3-scratch §113-121).
**§2h XREVIEW MANDATORY**: completed via 2/3 sigma-verify tools (`verify_finding` gemini-3.1-pro + `challenge` gpt-5.4-pro reasoning-tier) on top-1 finding DA[#1]; `cross_verify` errored — see T0 4-build P0 below.

---

## 3. Cross-agent Convergence and Tensions

### 3.1 Convergence

1. **Followups micro-build bundling** (c3-scratch §332+, §444). IE proposed → TA endorsed → DA accepted → CQA concurred. Single proposed `block-5-synthesis-carveout-followups` micro-build under WS-3 Tier-C sequencing bundles four items: (a) DA[#1] boundary-aware-matching applied symmetrically to `_path_is_archive` + `_is_synthesis_archive_write` (closes parent ADR[6] escape-vs-spoof asymmetry), (b) DA[#2] OVERMATCH test class, (c) DA[CF-1] `:1056` split into one synthesis-test + one `-workspace.md` multi-path-test, (d) optional F[CQA-8] scope-boundary doc-drift correction.
2. **XREVIEW infra T0/T1/T2 four-witness reframe** (c3-scratch §29-78, §301). IE+CQA+TA+DA all probed sigma-verify availability in C3 agent context. Schemas LOAD cleanly across all four (T1 from C2 NOT reproduced — was C2-build-track-session-specific transient, NOT structural propagation gap). Per-tool invocation behavior is heterogeneous (TA + DA both witness): `cross_verify` errors with "An internal error occurred"; `verify_finding` (gemini-3.1-pro) and `challenge` (openai gpt-5.4-pro reasoning-tier) return substantive output. Reframe: T0 (cross_verify bridge bug) escalating to **4-build P0**; T1 reframed as transient C2-only event; T2 (per-tool-invocation-failure post-schema-load) NEW failure-mode class first articulated in TA-XREVIEW-probe and corroborated in DA-XREVIEW-probe.
3. **Three-track BELIEF convergence** (c3-scratch §492-508). DA P=0.93 + TA P=0.97 + CQA P=0.90 — all trending up from C2 entering 0.87, no track flagging another track. Lead synthesis P=0.91 honest blend (above 0.85 threshold cleanly; below 0.95 due to documented residuals).
4. **Editorial DA[#3] routing** (c3-scratch §289-298, §453-465). DA CONCEDE → TA SendMessage → IE Edit-tool fix at plan-line:289 → CQA peer-verify PASS — proper agent-routing pipeline, no lead intervention beyond final acknowledgment.

### 3.2 Tensions and resolutions

| Tension | Origin | Surface | Resolution |
|---|---|---|---|
| AMENDMENT scoping completeness on DA[#1] (escape-vs-spoof) | C3 DA r1 (c3-scratch §125) — ext gpt-5.4-pro reasoning-tier vuln=HIGH on substring-overmatch as separate failure class | TA initially defended AMENDMENT r3 framing as already covering substring-overmatch via "compounded inheritance" language at plan §104 | TA DEFEND-WITH-COMPROMISE (c3-scratch §269-283): explicitly conceded AMENDMENT r3 line 104 covers escape-direction (ADR[6] inheritance) but not spoof-direction (predicate-overmatch as separate failure class). Compromise: keep code, bundle boundary-aware-matching into followups micro-build symmetrically across `_path_is_archive` + `_is_synthesis_archive_write` (unified architectural unit closing parent ADR[6] symmetry gap). DA ACCEPTED (c3-scratch §426). |
| OVERMATCH test gap — fix in-build vs defer | C3 DA[#2] LOW (c3-scratch §127) IE-routed | DA framed as "concede-or-defend"; IE could have added 1-2 tests inside carve-out class to document inherited limitation | IE DEFEND with deferred follow-up SQ (c3-scratch §157-184). Five-pillar defense: (1) mechanism confirmation, (2) scope-ownership inherited from `_path_is_archive` ADR[6] day-1 deferral, (3) §scope-boundary fidelity excludes WS-3 Tier-C work, (4) DA's own framing ("likely DECLINED in-build per scope discipline") supports defend, (5) §4c gold-plating-avoidance + §4a scope-discipline favor defer. DA ACCEPTED-FINAL (c3-scratch §428). |
| DA[#4] §2h marker absence — inline docstring vs separate registry | C3 DA[#4] LOW (c3-scratch §131) | DA proposed inline docstring marker; would be 12th line drift from IC[1] verbatim 11-line spec | TA DEFEND (c3-scratch §301-313): existing language ("integrity boundary" + "accepted residual risk" + "single-user hook context" + ADR[1] AMENDMENT r3 reference) is functionally equivalent. The right place for "this predicate is security-adjacent" marker is a directives.md §2h companion-list registry, not inline in every docstring. Promotion-candidate, NOT in-build fix. DA ACCEPTED (c3-scratch §432). |
| Plan §Verification:289 inconsistency — patch in-place vs accept resolved-in-record | C3 DA[#3] LOW (c3-scratch §129) | DA framed "concede or defend"; in-place plan-text edit weakens "locked plan" semantics | TA CONCEDE (c3-scratch §286-297): editorial forward-pointer "(resolved to `-workspace.md` per §Plan Ambiguity Resolution Q2 lines 267-268)" appended at line 289. Preserves plan-as-record while breaking inconsistency-trap for future agents reading plan in isolation. Editorial-only, not scope-change. IE applied via Edit tool; CQA peer-verify PASS. Note: plan-text edit at locked plan slightly weakens "locked" semantics — kept in residuals-keeping-below-0.95 list (plan §13). |

No unresolved tensions blocking r1 close-out. r2 NOT triggered.

---

## 4. DA Challenges and Resolutions

### 4.1 C1 challenges (10 total: 4 primary cluster + 6 secondary)

| ID | Severity | Challenge | Response | Resolution | Source |
|---|---|---|---|---|---|
| DA[#1] | HIGH | ADR[6] threat-model exclusion mis-cited (SCALE/DEFERRAL → THREAT-MODEL EXCLUSION drift) | TA-r3: CONCEDE — amendment rewritten to honor parent ADR[6] DEFERRAL framing; threat-model-exclusion language removed | CONVERGED-r3 | c1-scratch §876-890 + §591 |
| DA[#2] | MED-HIGH | gpt-5.4-pro reasoning-tier: capability-inversion + consequence-escalation + integrity-gate reframe + path-normalization-absent | TA-r3: CONCEDE — capability-inversion + consequence-escalation acknowledged in IC[1] consequence-amplification note | CONVERGED-r3 | c1-scratch §893-915 + §593 |
| DA[#3] | LOW-MED | Suffix-collision benign-content vector (`2025-Q3-survey-synthesis.md`) | TA-r3: DEFEND ADR[1] §a4 as adequate post-DA[#1] correction; bounded by Condition B archive-marker requirement | DEFENDED | c1-scratch §918-928 |
| DA[#4] | MED | Symlink + case-fold inheritance is flat-at-predicate but compound-at-consequence | TA-r3: CONCEDE — flat-inheritance at predicate, compound-inheritance at consequence; both stated explicitly in r3 amendment + consequence note | CONVERGED-r3 | c1-scratch §932-942 + §595 |
| DA[#5] | LOW | 5 tests over-engineered? | DEFEND — each test bounds AND-predicate on independent dimension or boundary | DEFENDED | c1-scratch §948-965 |
| DA[#6] | LOW | Spec drift on test scope (3→5 absorption) | DEFEND — gap-closure not creep | DEFENDED | c1-scratch §969-978 |
| DA[#7] | LOW | H1 alternative dismissed too quickly? | CONCEDE — H1 lead-pre-validation sound; alternative has same caller-gate coupling defect | CONCEDED | c1-scratch §982-992 |
| DA[#8] | LOW | §2d source-provenance violation in amendment | TA-r3: CONCEDE — amendment cites parent ADR[6] actual body | CONVERGED-r3 | c1-scratch §996-1004 + §597 |
| DA[#9] | LOW | PROMPT-AUDIT (§7d) | PASS — echo-count:0, methodology investigative ¬confirmatory | PASS | c1-scratch §1010-1016 |
| DA[#10] | LOW | Test integrity verification (§4d) — per-test regression-catch | DEFEND with one regression-test note — all 5 tests have a state where they fail; none tautologies | DEFENDED | c1-scratch §1020-1034 |

C1 BELIEF trajectory: r2 P=0.62 (DA FAIL conditional) → r3 P=0.83 (DA PASS post-Option-D1 fix) → r4 P=0.88 (multi-model dual-independent corroboration, lock threshold cleared) — plan §231.

### 4.2 C3 review challenges (5 review + 3 carry-forward = 8 total)

| ID | Severity | Challenge | Response | Resolution | Source |
|---|---|---|---|---|---|
| DA[#1] | MEDIUM (ext vuln=HIGH) | Substring-overmatch as failure class independent of ADR[6] inheritance (escape-vs-spoof reframe) | TA: DEFEND-WITH-COMPROMISE — keep code, bundle boundary-aware-matching into followups micro-build symmetrically across `_path_is_archive` + `_is_synthesis_archive_write` | CONVERGED — DA ACCEPTED | c3-scratch §125 + §269-283 + §426 |
| DA[#2] | LOW | Overmatch test-coverage gap (no near-miss test for `/tmp/sigma-review/shared/archive/foo-synthesis.md`) | IE: DEFEND-with-deferred-SQ — parent-scope (ADR[6]); 5 defense pillars verified by CQA F[CQA-7] | CONVERGED — DA ACCEPTED-FINAL | c3-scratch §127 + §157-184 + §428 |
| DA[#3] | LOW | Plan §Verification:289 internal-inconsistency (`-not-synthesis.md` reference unresolved) | TA: CONCEDE — editorial forward-pointer applied via IE Edit tool at plan-line:289; CQA peer-verify F[CQA-2/3/4] PASS | CONVERGED — FIXED | c3-scratch §129 + §286-297 + §457-465 |
| DA[#4] | LOW | Docstring lacks explicit "security-adjacent" / §2h marker | TA: DEFEND — IC[1] verbatim-spec preservation discipline + parent `_path_is_archive` precedent + correct location is directives.md §2h companion-list registry, not inline drift. Promotion-candidate. | DEFENDED — DA ACCEPTED | c3-scratch §131 + §301-313 + §432 |
| DA[#5] | INFO | §4f circuit-breaker self-check (have I engaged adversarially?) | PASS — DA[#1] external `challenge` reasoning-tier vuln=HIGH is genuine adversarial output | PASS | c3-scratch §133 + §434 |
| DA[CF-1] | LOW | `:1056` coverage shadow on `test_header_in_build_scratch_passes_block5` post-carve-out | 3-eye deferral remains sound (IE flag + lead defer + CQA concur + IE peer-verify CONCUR); bundled into followups micro-build | CONVERGED | c3-scratch §137 + §436 |
| DA[CF-2] | MEDIUM | XREVIEW infra T0/T1/T2 reframe + 4-build P0 escalation | TA: CONCEDE — T0 cross_verify bridge bug 4-build P0; T1 was C2-session-specific transient (NOT structural — 4-witness DA+TA+IE+CQA tools-available in C3); T2 NEW per-tool-invocation post-schema-load fault class | CONVERGED | c3-scratch §139 + §317-330 + §438 |
| DA[CF-3] | INFO | C2 process-integrity wins as Step 15 promotion candidates | PASS — Step 15 territory, not C3 review challenge | PASS | c3-scratch §141 + §440 |

**§4f circuit-breaker (c3-scratch §133 + §502)**: PASSED via DA[#1] external `challenge` reasoning-tier vuln=HIGH genuine adversarial output. Zero-dissent state NOT triggered (4 PENDING findings, 1 with HIGH external vulnerability score).

**DA r1-grading (c3-scratch §422-451)**: P=0.93 (entering build-belief 0.87 + 0.06 from r1 substantive engagement). 0 unresolved tensions; all 5 review findings + 3 carry-forwards substantively closed; recommend CONVERGE r1.

---

## 5. BUILD Rubric §3b Scores (CQA, final-round, c3-scratch §350-416)

Per build-directives.md:351-362, scoring on 6 dimensions, 1-4 scale. Final-round triggered by team-lead final-round signal (build-r1=CONVERGE, BELIEF[review-r1] P=0.91, all 4 BUILD success criteria met, 3-agent independent CONVERGE).

| Dimension | Score | Source evidence |
|---|---|---|
| **correctness** | **4** | phase-gate.py:623-646 + phase-gate.py:684-687 + test_phase_gate.py:1293-1464 + pytest 1286/14/0 across 3 independent runs (IE C3-boot 10.69s, IE post-fix 10.60s, CQA fix-validation 10.96s). Predicate fail-safe on type/empty/whitespace/wrong-suffix; both Cond A + Cond B independently required. Short-circuit double-enforced via outer `is_archive_op` guard. test-(b) dual pre/post sanity assertions @ :1363+:1371 mechanically prove carve-out branch is load-bearing, not FP guard. ADR[1] AMENDMENT r3 doctrine: synthesis structurally precedes compilation. Importlib live-replay 13/13 (CQA F[CQA-3]). Every documented case handled, fail-safe defaults, mechanical proof of resolution path. |
| **test-coverage** | **3** | test_phase_gate.py:1293-1464 + DA[#2] OVERMATCH gap + carry-forward #1 `:1056` + build-directives §4d audit. 5/5 behavioral tests with real fixtures (`patch_paths`/`patch_multi`), no hardcoded-pass-flag pattern, asymmetric `True`/`False` failure-case asserts, integration parity 1286/14/0 ×3. Documented gap (-1 from 4): DA[#2] OVERMATCH near-miss not covered (deferred to followups micro-build per IE DEFEND-with-deferred-SQ); secondary `:1056` coverage shadow (3-eye concurred deferral). Both ASYMPTOMATIC + bundled to followups. **3 = solid coverage with documented forward-pointers**. |
| **maintainability** | **4** | phase-gate.py:623-646 (predicate docstring) + phase-gate.py:684-687 (short-circuit comment) + IC[1] verbatim 11-line docstring + test_phase_gate.py:1293-1302 (class docstring). Intention-revealing private-prefix naming (`_is_synthesis_archive_write` matches `_path_is_archive`/`_has_compilation_complete` family). Self-documenting architectural decisions (ADR[1] reachable without leaving file). Cross-references at all 3 reference points (directives.md:1353 Tier-1 + sigma-lead.md:207 Tier-3). Cyclomatic complexity ≤ 4. |
| **performance** | **4** | pytest timing 10.60s/10.69s/10.96s across 3 runs. O(1) predicate (isinstance + lstrip + strip + os.path.basename + endswith + any() over 5-element marker list); no I/O, no regex compilation in hot path. Hot-path placement: short-circuit fires BEFORE `_has_compilation_complete` disk I/O — net performance IMPROVEMENT for synthesis-write path. Hook-suite parity 1286/14/0 EXACT MATCH zero regression. |
| **security** | **3** | phase-gate.py:624-637 (Consequence note ADR[1] r3 + Known limitations) + DA[#1] predicate-overmatch finding + ADR[6] parent-scope inheritance + DA[#2] OVERMATCH gap + plan §247-255 Cross-Model Code Review. Defense layers: fail-safe defaults + double-condition gate + outer-guard layering + explicit Consequence note documenting gate-removal residual. Three input-shape filters before semantic check. Documented residual (-1 from 4): three KNOWN LIMITATIONS (symlinks, HFS+ case-fold, relative `..`) inherited from parent `_path_is_archive` (ADR[6]). DA[#1] surfaced "escape-vs-spoof" reframe (overmatch direction not covered by AMENDMENT r3); TA DEFEND-WITH-COMPROMISE bundled boundary-aware-matching hardening into followups micro-build for symmetric correction. §2h XVERIFY-mandatory completed via 2/3 sigma-verify tools (verify_finding + challenge; cross_verify T0 4-build P0 logged). **3 = strong-but-not-exemplary**, with parent-scope hardening explicitly bundled into followups for symmetric correction. |
| **api-design** | **4** | phase-gate.py:623 (signature) + phase-gate.py:649 (consumer) + IC[1] verbatim spec + IC[2] insertion correctness + cross-refs. Typed input, typed output, single-purpose, no side effects, no exceptions raised. Underscore-prefix declares private; matches `_path_is_archive` family pattern. Defensive `archive_path and` guard; `(False, "")` return shape exactly matches existing PASS branches; no new return-type variant. Backward-compatible: zero callers external to phase-gate.py module; zero behavior change on non-synthesis paths; zero new public API surface. Cross-reference contract at directives.md:1353 (machine-readable) + sigma-lead.md:207 (human-readable). |

**Mean: 3.67 / 4.00.**

Both `3` scores have followups bundled (test-coverage: DA[#2] OVERMATCH + CF-1 `:1056`; security: DA[#1] boundary-aware-matching + symmetric `_path_is_archive` hardening) → both targeted at the same `block-5-synthesis-carveout-followups` micro-build under WS-3 Tier-C sequencing. Net §3b verdict: **PASS for r1 close-out at TIER-1 P=0.91 build-belief; followups micro-build is the residual-handling vehicle, not an r2 trigger.**

---

## 6. Pre-mortem Failure Modes

Plan §Pre-mortem (plan §202-210) committed five PMs. Post-mortem assessment of which fired vs which did not:

| PM | Likelihood | Failure mode | Outcome | Source |
|---|---|---|---|---|
| PM[1] | LOW | WS-3 SQ-T1 (`_strip_fenced_blocks` parity) modifies same file → merge conflict if WS-3 starts before WS-2 closes | **Did not fire** — TA C3 PLAN-REVIEW (c3-scratch §259) confirmed `_strip_fenced_blocks` does not yet exist in phase-gate.py; WS-2 changes scoped to :623-646 + :684-687, conflict surface minimized to "same-file co-existence". WS-2→WS-3 sequencing-gate held. | plan §206 + c3-scratch §259 |
| PM[2] | LOW-MED | Suffix-collision / path-manipulation: crafted `*-synthesis.md` filename in archive dir bypasses gate (H4 capability-inversion) | **Partially fired post-mortem** — DA[#1] C3 surfaced predicate-overmatch as separate failure class (escape-vs-spoof reframe), surfacing the spoof-direction not covered by AMENDMENT r3. Concrete vector: `/tmp/sigma-review/shared/archive/foo-synthesis.md` returns True. Bounded by single-user hook context + BLOCK 1 plan-lock for code files + visibility in session history. Bundled into followups micro-build for symmetric `_path_is_archive` + `_is_synthesis_archive_write` boundary-aware-matching hardening. Residual ACCEPTED with bounded context. | plan §207 + c3-scratch §125 + §269-283 |
| PM[3] | LOW | macOS HFS+ case-fold over-gating direction (block valid uppercase paths) | **Did not fire** — confirmed empirically (probe-case-9 `foo-Synthesis.md`=False, probe-case-13 `foo-synthesis.MD`=False). Inherited limitation from `_path_is_archive`. Claude Code generates lowercase paths in Write/Edit tool_input. Empirical bypass requires manually-crafted uppercase path. Residual accepted. | plan §208 + c2-scratch §372 |
| PM[4] | LOW | `archive_path` None (Bash extraction failed) → carve-out does NOT fire → falls through to `_has_compilation_complete(None)` broad-glob → BLOCKED | **Did not fire / verified working** — `archive_path and` guard at phase-gate.py:686 confirmed by F[CQA-10] (c2-scratch §282); structural-impossibility argument applies most acutely to Write/Edit (agent writes synthesis file directly). Bash synthesis-archive writes uncommon. Documented in IC[2] docstring. | plan §209 |
| PM[5] | LOW | Implementation bug: short-circuit fires for ALL `is_archive_op` paths (over-broad short-circuit) | **Did not fire** — caught by SQ[3] tests (d) non-synthesis-archive-still-blocks AND (e) synthesis-outside-archive-still-blocks. Both PASSED in C2 (c2-scratch §316-326). | plan §210 |

**New failure modes surfaced post-mortem:**
- **T2: per-tool-invocation-failure post-schema-load** (NEW failure-mode class first articulated at C3) — sigma-verify schemas LOAD cleanly via deferred-tool ToolSearch flow but `cross_verify` invocation errors with "An internal error occurred" while `verify_finding` and `challenge` work. Two-witness corroborated (TA + DA, c3-scratch §57-78). Out-of-band engineering remediation needed: targeted fix to `cross_verify` MCP-handler concurrency/fan-out logic since per-model paths work.
- **C2 process incidents** (c2-scratch §incidents-flagged-to-user, plan §24): (a) session-scope task-list leak (lead-side TaskCreate from pre-TeamCreate context bleeding into agent inboxes; CQA correctly refused 2 misroutes; user-approved abort-restart, executed cleanly with prior IE work preserved), (b) sigma-verify XREVIEW infrastructure gap (3-build recurrence T0 bridge bug + new T1 per-session registry mismatch; lead role boundary preserved), (c) two message-cross events between lead+IE (both correctly handled via P[evidence-based-pushback-on-stale-lead-claim]).

---

## 7. Open Questions and Unresolved Gaps

### 7.1 Followups micro-build candidate

**Proposed: `block-5-synthesis-carveout-followups`** under WS-3 Tier-C sequencing (3-witness convergence: IE proposed → TA endorsed → DA accepted → CQA concurred). Bundling rationale: all four items share the parent ADR[6] symmetry boundary or are doc-correctness companions to it.

| Item | Origin | Severity | Bundling rationale |
|---|---|---|---|
| (a) DA[#1] boundary-aware-matching applied symmetrically to `_path_is_archive` + `_is_synthesis_archive_write` | C3 DA[#1] DEFEND-WITH-COMPROMISE | MEDIUM | Closes parent ADR[6] escape-vs-spoof asymmetry (TA's "right artifact" argument: a unified predicate hardening would close DA[#1] + DA[#2] + the parent ADR[6] symmetry gap). Architectural unit. |
| (b) DA[#2] OVERMATCH test class | C3 DA[#2] DEFEND-with-deferred-SQ | LOW | Coverage layer for (a); near-miss path coverage (`/tmp/sigma-review/shared/archive/foo-synthesis.md`). |
| (c) DA[CF-1] `:1056` split into one synthesis-test + one `-workspace.md` multi-path-test | C3 DA[CF-1] CONVERGED-deferral | LOW | Same coverage-shadow pattern as (b); split-test fix restores intent-traceability. |
| (d) F[CQA-8] scope-boundary doc-drift correction (optional) | C3 CQA RESTATE | LOW | c3-scratch §scope-boundary line 91 says `:1335-1464` while class-def actual `:1293`; record-only, originated C2 Build Status attestation. Optional bundle if followups is doc-track-inclusive. |

### 7.2 Out-of-band engineering remediation

- **T0 cross_verify bridge bug at 4-build P0** (escalated from 3-build P0 in C2). TA suggested targeted fix to cross_verify MCP-handler fan-out/aggregation logic specifically (per-model `verify_finding` and `challenge` work, only fan-out/aggregation breaks). Plan §audit-flags-recurring entry update from "3-build P0" → "4-build P0" (c3-scratch §330 + §438).
- **T2 per-tool-invocation-failure post-schema-load** — NEW fault class needs separate investigation; cross_verify alone errors while verify_finding + challenge work.

### 7.3 Promotion candidates (Step 15 — lead curation pending, c3-scratch §564-587)

- **T1 `T[build-track-peer-verifier-independent-pytest-discipline]`** (MEDIUM, IE-proposed, CQA-concurred) — build-track peer-verifier MUST run independent pytest from own session, not inherit numerator from build-engineer claim. Would have caught the C2 inheritance-without-rerun gap earlier had it been formalized at C2-spawn. Three-witness baseline (IE C3-boot 10.69s + IE post-fix 10.60s + CQA 10.96s, all 1286/14/0) is gold standard.
- **T2 `T[xreview-mcp-registry-c3-recovery-pattern]`** (LOW) — XREVIEW MCP tool registry behaves cleanly via ToolSearch deferred-tool flow on first probe in fresh agent sessions, even when prior session had registry contamination (e.g., C2 T1 mismatch). Four-witness validation (IE+CQA+TA+DA at schema-load layer in C3).
- **T3 `F[CQA-PATTERN-process-integrity-under-spurious-task-pressure]`** (already-promoted-via-IE-one-time-delegation, restated) — agent declines task-list assignments outside role brief; SendMessage from team-lead supersedes task-list when contradictory; same-class repeats stay silent. Held this round (0 violations across full r1 cycle).
- **C2 process-integrity wins** (DA[CF-3] INFO/PASS, c3-scratch §141): (a) prior-CQA refused 2 task-list misroutes; (b) IE applied evidence-based-pushback-on-stale-lead-claim ×2; (c) lead role boundary held under XREVIEW infra pressure.

### 7.4 Deferred items with citations

- **`## archive-complete` header schema** — deferred to WS-3 SQ-T7 (plan §78).
- **`_strip_fenced_blocks` parity** — deferred to WS-3 SQ-T1, sequencing-gate enforced via WS-2→WS-3 phase gate (plan §79).
- **A14/A26/B5/B6 chain-evaluator items** — parent-build scope, complete (plan §81).
- **Path canonicalization SQ** (`os.path.realpath` + symlink resolution + `..` collapse before predicate) — belongs to security-track build, not WS-2 (c1-scratch §911-914 D2 alternative).
- **directives.md §2h companion-list "security-adjacent named predicates" registry** — promotion-candidate observation surfaced from DA[#4] DEFEND, NOT in-build fix (c3-scratch §313).

### 7.5 Genuine residuals keeping belief below 0.95 (lead synthesis, c3-scratch §515-520)

- Substring-overmatch documented but NOT remediated (followups micro-build = recommendation, not fix).
- T0 cross_verify bridge bug recurs at 4-build P0 (compounding infra debt).
- T2 NEW fault-mode class needs separate investigation.
- Plan-text edit at locked plan slightly weakens "locked" semantics, even if process-integrity oriented.
- F[CQA-8] LOW doc-precision drift originated C2 (cosmetic only).

---

## Provenance Summary

This synthesis was assembled from:
- Plan file: `~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout.plan.md` (lines 1-361)
- C3 scratch: `~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout/c3-scratch.md` (681 lines)
- C2 scratch: `~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout/c2-scratch.md` (483 lines)
- C1 scratch: `~/.claude/teams/sigma-review/shared/builds/2026-05-05-block-5-synthesis-carveout/c1-scratch.md` (1199 lines)

Dual-track distinctions preserved throughout: plan-track (TA) vs build-track (IE+CQA) vs adversarial (DA). Multi-agent attribution retained — no collapse into "the team". P=0.91 lead synthesis is the load-bearing belief; per-track scores DA P=0.93 / TA P=0.97 / CQA P=0.90 retained for posterior reconciliation visibility. No probability estimates added beyond those already in scratch.
