# Synthesis: r19-remediation (BUILD TIER-3)

- build-id: 2026-04-23-r19-remediation
- C1 plan exit-gate: PASS (P=0.88, DA grade A-)
- C2 build complete: 2026-04-24 (240/240 canonical + 300/300 sigma-verify)
- C3 review complete: 2026-04-25, 3 rounds (r1 FAIL → r2 PASS-with-CDS-NEW-HIGH → r3 PASS)
- C3 final belief: P=0.89
- Build rubric: 24/24 across 6 dimensions
- Final test state: 247/247 canonical + 300/300 sigma-verify, zero regressions
- Synthesis written: 2026-04-25 by synthesis-agent (separate-context provenance firewall per CLAUDE.md ## Lead Role Boundaries)

---

## 1. Prompt Decomposition

Source: plan file ## Prompt Understanding section.

### Q[] — build scope questions
- Q1: Fix critical infrastructure issues — R19 #1 sed-i mechanical block, #3 ΣVerify agent-context tool inheritance, #4 A12 parser key-mismatch.
- Q2: Fix high-priority infrastructure — R19 #5 + #14 peer-verify regex + spawn template alignment, #19 A3 DB-step parser false negatives, #20 A12 archive timing window.
- Q3: Add 4 protocol-layer gates — R19 #21 premise-audit pre-dispatch, #22 §2i precision gate, #23 governance min-artifact, #24 §2d severity provenance.
- Q4: Update directives + spawn templates + agent definitions to enforce mechanically (not directive-only).

### H[] — hypotheses with test results
- H1 CONFIRMED: sigma-verify MCP source is user-controlled; `machine.py:17-128` is the fix location; root cause is HATEOAS state-gating, not registry gap.
- H2 PARTIALLY CONFIRMED: new analytical gates can be calibrated, but only scoped CONDITION 2 is code-detectable; CONDITION 1 defers to DA adjudication with β+ audit-calibration tracking toward future BLOCK-promotion.
- H3 SUPPORTED: premise-audit fits as workflow Step 7a pre-spawn, not new agent role (TA + CDS convergence).
- H4 CONFIRMED: no circular dependencies across 30+ SQs; SQ[0] fixture prerequisite gates SQ[3] + SQ[13b-c].
- H5 FALSIFIED: live pytest discrepancy (TA reported 154, CQA reported 92 — C2 reconciled to 154/143/11 authoritative).

### C[] — constraints
- C1: Top-10 ROI only (MEDIUM/LOW R19 #6-#18 deferred, except #2 promoted mid-build).
- C2: Both code and directives in scope.
- C3: No regressions to chain-evaluator/phase-gate test suites.
- C4: New gates with no legitimate override → hard BLOCK.
- C5: When a gate over-fires, defend each invocation rather than add exceptions.
- C6: All changes git-committed and pushed from sigma-system-overview per session-end checklist.
- C7: 3 already-resolved R19 artifacts out of scope (UP-B, UP-C, MITRE ATLAS).
- C8: XVERIFY excludes anthropic — cross-model must be cross-family.

---

## 2. Findings Organized by Domain

### tech-architect (TA) — plan-track ADR/IC fidelity

**Round 1:**
- ADR[1] #3 ΣVerify auto-ready: compliance partial-documented-drift. Shipped code is a probe + stderr log + `_initial_state_hint='ready'` forward-compat attribute, not literal MCP auto-ready. Behavioral primary today is SS spawn-prompt belt-and-suspenders. Required-action: synthesis must state ADR[1] behavioral primary = SS spawn-prompt today, TA probe = operator-visibility + A24-enablement + forward-compat. Drift class: scope-clarification via user-ratification, not silent-scope-shift.
- ADR[2] A12 key rename: full compliance. `archive_file_found` rename pre-applied in commit a2a7fa8.
- ADR[3] A12 24h grace-window: full compliance. Literal 24.0h threshold at chain-evaluator.py:306, synchronous mtime delta, non-looping invariant preserved.
- ADR[4] Step 7a premise-audit: full compliance. Sequence-constraint load-bearing at c1-plan.md:62; chain-eval BLOCK day-one at line 88.
- IC[1] phase-gate sed-i BLOCK 3→4: compliance full at code, but flag — BLOCK-number drift across downstream documentation.
- IC[4] DB-depth layered authority: full compliance, no double-counting; `result = gc.check_dialectical_bootstrapping(content)` preserves upstream object, layer-2 augments details only.
- IC[6] workspace_write helper: full compliance. Signature exact to spec, WorkspaceAnchorNotFound double-guard (anchor-miss + no-op).
- TA-EXIT r1: plan-compliance full across 9 items + partial-documented-drift on ADR[1] only + 1 BLOCK-number-renumber-flag. needs-fixes: none-blocking (TA classification later overruled by lead based on DA evidence).

**Round 2 verification:**
- R2-CHECK[1-5] all PASS: phase-gate.py BLOCK 4 untouched; _PEER_VERIFY_HEADER regex unchanged; workspace_write.py signature unchanged with cumulative ~65 successful writes / 0 WorkspaceAnchorNotFound; ADR[1] gateway-semantic preserved with additive IC[8] forward-contract block at machine.py:33-37; check_a24 architectural pattern parity with A20/A22/A23 confirmed across 10 dimensions.
- TA-r2-EXIT: full compliance, fixes honor ADRs, no new architectural debt. Synthesis-update: IC[8] forward-contract docstring strengthens PM[SS-2] mitigation; A24 ships as per-finding β+ complement to A15 per-agent binary check.

### security-specialist (SS)

**Round 1:**
- ADR[SS-1] sed-i BLOCK 4 + shlex tokenization: full compliance at code layer. SS independently traced 7 empirical cases (BSD `-i ''`, joined `-i''`, env-wrapper, xargs-positional, absolute `/usr/local/bin/sed`, backup `-i.bak`, xargs-stdin) — most thorough evasion-matrix trace in C3.
- BLOCK 3→4 renumber under C5: full compliance at code layer, drift at docs layer. INDEPENDENT CONFIRMATION of DA[#2]: 27 stale "phase-gate BLOCK 3" citations across 23 SAFETY-CRITICAL agent files + _template + sigma-lead + c1-plan + c2-build. SS framing: documentation side of ADR[SS-1] failed atomicity test even though enforcement side is correct. Severity: high. Required: mechanical sweep before C3 sign-off.
- xargs stdin KNOWN LIMITATION: scope-boundary HONEST. Threat model is accidental silent corruption (R19 failure mode), not sophisticated-adversary evasion. SS dissents from DA[#4] framing concern: keep bypass enumeration in docstring as inspectable contract. Severity: low.
- IC[7-9] namespace: partial drift. Plan IC[7-9] namespace was created by DIV[3] reconciliation but never propagated to agent-defs or directives. Lower-severity cousin of DA[#2] — does not create wrong-destination risk. Recommend option-a (accept as plan-scoped, document in synthesis).
- IC[8] MCP trust boundary forward-contract: partial. Docstring describes current state-gating but does not specify that future state-gated tools must perform call-time authorization. Severity: low. Fix: add 1-sentence to machine.py docstring.
- ADR[SS-2] ΣVerify belt-and-suspenders: full compliance as superseded primary. Note: ADR[SS-2] is doing more load-bearing work than DA[#2]-compromise planned (latent strength surfaced).
- ADR[SS-3] audit-trail: partial-with-narrow-exception. calibration-log.md is a SIBLING log to workspace gate-log; agents/lead may conflate. Calibration-log integrity contract is separate from ADR[SS-3]'s DA-verdict trail scope.
- IC[9] audit-trail integrity via A16-A18 peer verification: full compliance.
- SS-EXIT r1: 3 SS-specific findings (BLOCK 3→4 propagation drift HIGH; IC[7-9] namespace non-propagation LOW-MEDIUM; IC[8] forward-contract gap LOW) + 1 convergent with DA[#2] + 1 convergent with CDS+DA[#3] + XVERIFY-FAIL documented.

**Round 2:**
- Blocker 2 (BLOCK 3→4 doc drift): CLOSED. Empirical grep verifies "phase-gate BLOCK 3" = 0 hits across agents+skills+teams; OPTION 2 phrasing "phase-gate enforces the sed-i BLOCK mechanically" appears across 31 files.
- A24 honors ADR[SS-2] + IC[8]: triggers only when ΣVerify available; reuses A20 load-bearing markers; 500-char window; tolerant of all three XVERIFY states per §2h; path-β+ WARN-first; IC[8] boundary respected (docstring disclaims runtime-authorization scope).
- IC[8] docstring at machine.py:36-39 ADEQUATE — conveys forward-contract, specifies independence-from-advertisement, disclaims tools/list as auth signal.
- R3-2 resync (6 sigma-optimize agents + zero-space evasion): align with user ruling, sed-i ban is consistency-grade safety. shlex.split(posix=True) collapses `-i""` into bare `-i`; existing coverage now locked as test-contract.
- SS-r2-EXIT: PASS on all 5 endpoints. Zero new attack vectors.

### cognitive-decision-scientist (CDS)

**Round 1:**
- ADR[CDS-1] #21 premise-audit Step 7a sequence: full compliance. PA[1-4] definitions match; BUILD/ANALYZE split done correctly.
- ADR[CDS-2] #22 §2i precision gate CONDITION 2 + CONDITION 1 deferral: full compliance. Code docstring at chain-evaluator.py:688-691 documents CONDITION 1 deferral with explicit ADR[CDS-2]+DA[#5] attribution; directive thresholds (≥3 reviews, ≤20% FP, ≥5 DA-verdicted) match audit-calibration-gate.py constants exactly.
- ADR[CDS-3] #23 §2j governance min-artifact: full compliance. TIER-A/B/C taxonomy + DA ARTIFACT-REVIEW format both shipped; scope narrowness via _GOVERNANCE_MARKERS_RE prevents over-fire on technical findings.
- ADR[CDS-4] #24 §2d severity provenance: full compliance with directive/code/template 3-layer consistency. 3-required-fields format character-for-character identical across directives.md, _template.md checkbox, and A23 regex.
- **β+ mechanics CAL-EMIT schema producer/consumer: PARTIAL — material defect.** chain-evaluator.py:613 producer formats `clean_excerpt = excerpt.replace("\n", " ").strip()[:50]` WITHOUT pipe-escape; audit-calibration-gate.py:34-41 consumer regex uses `[^|]+?` capture excluding pipes. Real findings routinely contain pipe-delimited inline tags per §2d source-tag notation. Failure mode: production records land in malformed bucket, audit-calibration-gate under-reports, biases PROMOTE/RECALIBRATE thresholds. XVERIFY: openai high-agree + google high-agree (C8-compliant). Severity: medium. Fix: producer-side sanitization at chain-evaluator.py:613.
- audit-calibration-gate.py threshold evaluation: full compliance. Decision ordering exhaustive without overlap.
- DA verdict protocol extension: full compliance.
- Lead-flag SQ[CDS-6..8] mid-build extension: faithful to CDS design; "scope extension" label was miscalibrated — assignment was the gap, not SQ scope.
- Lead-flag #21 premise-audit self-application: full compliance with acknowledged retroactive gap. C1 audit YELLOW flagged the self-apply gap; lead retroactively added section. Process-integrity-wise this is "legitimate gap, self-detected, closed before ship."
- CDS-EXIT-FINAL r1: pipe-escape was BLOCKER (escalated by lead+DA+XVERIFY). Empirical-XVERIFY-via-local-python-c flagged for promotion.

**Round 2:**
- pipe-escape fix at chain-evaluator.py:613-616: closes r1 BLOCKER cleanly. Code-comment correctly attributes fix to "CDS XVERIFIED openai+google high-agree; DA confirmed."
- A24 sigma-verify pre-flight at chain-evaluator.py:943-1057: HONORS β+ STRUCTURE but BREAKS β+ MECHANICS — **NEW HIGH-severity defect surfaced**. audit-calibration-gate.py:44 still reads `VALID_GATES = {"A20", "A22", "A23"}` — A24 is NOT registered. Empirically verified: A24 records bucket as malformed in parse_log; β+ promotion path mechanically broken for A24. Same class as r1 pipe-escape (producer/consumer schema decoupling). Fix: one-line VALID_GATES += A24 + docstring + argparse description.
- R3-2 template resync: NO IMPACT on §2i/§2j/§2d directive text or thresholds. Calibration-design-orthogonal.
- Cross-pattern signal: Blocker 2 (27-file BLOCK 3→4 doc drift) + r1 pipe-escape + r2 A24 gate-id mismatch = THREE instances of multi-layer contract drift. Promotion candidate P[multi-layer-contract-drift].

**Round 3 verify (CDS-r2-1 closure):**
- VALID_GATES updated to {A20, A22, A23, A24} with provenance comment at audit-calibration-gate.py:47-49.
- Module docstring lines 11-12 list all four gates with semantic roles.
- argparse choices auto-syncs from sorted(VALID_GATES); CLI accepts A24.
- Empirical pre-fix vs post-fix flip CONFIRMED: pre-fix `A24 in stats: False / malformed: [(1, 'unknown gate-id: A24')]`; post-fix `A24 in stats: True / malformed: []`.
- **Bonus telemetry recovery**: live calibration-log.md (210 records) had 13 historical A24 PENDING records previously silently malformed; fix recovers them as visible-and-aggregated.
- β+ promotion path now mechanically functional for A24.
- xverify-suppression-deferral OK for the WARN-first calibration window per CDS calibration-design lens.
- Synthesis-defer: 1-line note that A24 has no Condition-1-style suppression heuristic (intentionally — A20 catches false-precision via qualifiers; A24 catches missing-XVERIFY which qualifiers don't resolve).

### implementation-engineer (IE) — build-track

**C2 (cluster A): 7 plan SQs + 3 extension SQs + 1 plan-amendment + 1 hygiene fix.**
- SQ[1] sigma-verify auto-ready: shipped as interpretation-A (~8 LOC + docstring + forward-compat hint; 300/300 sigma-verify).
- SQ[2] A12 24h grace: synchronous mtime delta per CAL[1].
- SQ[3] A3 DB extraction: split-by-DB + (1)(2)(3) requirement, IC[4] layered authority preserved.
- SQ[7]+SS-1 sed-i BLOCK 4: renumbered from BLOCK 3 per C5 (existing code drift), 22/22 evasion matrix pass.
- SQ[14] workspace_write helper: IC[6] exact signature, dogfooded in production.
- SQ[CDS-6/7/8 IE-portion] A20/A22/A23: shipped as scope-extension (~55 LOC + 19 tests), user-ratified mid-C2.
- PLAN-AMENDMENT gate_checks.py DA-filter: 1-line exclusion in `_load_roster_agents:233`, user-ratified option C.
- HYGIENE xargs docstring narrow: phase-gate.py:300 KNOWN LIMITATION block.

**Round 2: 5 fixes shipped under budget (25min vs 60min).**
- F[ie-r2-1] check_a24_sigma_verify_coverage at chain-evaluator.py:943-1060.
- F[ie-r2-2] CAL-EMIT pipe-escape at chain-evaluator.py:613.
- F[ie-r2-3] IC[8] forward-contract docstring at machine.py:33-37.
- F[ie-r2-4] machine.py:144 orphan reference: NO-OP (FIX 1 made it resolve).
- Plus dispatch-dict A20/A22/A23 entries (DA[#5] coincidentally resolved).

**Round 3: 1 fix shipped under budget (8min vs 10min).**
- F[ie-r3-1] audit-calibration-gate.py producer/consumer schema sync: 3 atomic edits (VALID_GATES += A24 + docstring + argparse description). argparse choices auto-syncs from sorted(VALID_GATES).

### technical-writer (TW) — build-track

**C2 (cluster B): 10 plan SQs, 29 files modified, +686 TW-owned LOC.**
- SQ[4] peer-verify atomic: c1-plan Step 11 + sigma-lead §2 + c2-build + _template (4-file CAL[9]).
- SQ[8] sed-i ban propagation: 23 SAFETY-CRITICAL agents + _template (count corrected from 22 per CAL[7] risk-tier rule).
- SQ[9]+CDS-5 Step 7a premise-audit: c1-plan Step 7a + premise-audit-results template + preflight checklist.
- SQ[10/11/12]+CDS-2/3/4: §2i + §2j + §2d-severity directives.
- §8e corruption recovery template: 7-step ΣComm conversion.

**Round 2:**
- F[tw-r2-1] BLOCK 3→4 OPTION 2 sweep: 27 files swept, "phase-gate BLOCK 3 enforces mechanically" → "phase-gate enforces the sed-i BLOCK mechanically" (drops numeric identifier — block-number-agnostic phrasing). DA endorsed as superior to literal sweep.
- F[tw-r2-2] statistical-analyst.md sed-i ban: canonical block inserted.
- F[tw-r2-3] BUILD-CONCERN[tw-r2]: 5 sigma-optimize agents lack sed-i ban (DA[#9] premise falsified). Flagged to lead, not silently expanded — proper "Follow the Plan, Flag Disagreement" application.
- Self-audit: TW concedes own C2 CHECKPOINT "atomicity-constraints-still-coherent:yes" claim was scoped to CAL[9] only; BLOCK-number citation was a separate atomicity constraint TW did not track.

**Round 3 add-on (user-ratified BUILD-CONCERN[tw-r2] option a):**
- F[tw-r3-1]: 5 sigma-optimize workspace-writing agents propagated. End-state: 30 SAFETY-CRITICAL agents + _template = 31 files.

**Round 3-2 (CQA→TW peer-verify ratified):**
- F[tw-r3-2]: 29 agents resynced from _template.md:140-152 canonical via workspace_write helper. Root cause of original drift: TW used pre-R2 technical-writer.md block as reference instead of authoritative _template.md (recursive-self-reference rather than authoritative-source-reference). Post-resync hash-identity: 30 files content-byte-identical. CAL[R3-2-canonical-block-hash-identity] subsumes weaker CAL[R2-OPTION2-phrasing].
- 67 successful workspace_write helper writes through C3 (cumulative), 0 WorkspaceAnchorNotFound — IC[6] hardened in production.

### code-quality-analyst (CQA) — build-track

**C2 (cluster C): 12 SQs including SQ[0] gating.**
- PF[1] baseline reconciliation: 154/143/11 authoritative; C1 "92" falsified.
- SQ[0] MINIMAL_WORKSPACE fixture fix + gate_checks DA-exclusion: cleared all 11 pre-existing failures.
- SQ[13b-g] tests: 30+ new tests covering A12 parser, peer-verify regex, A3 DB extraction, A12 grace, A20 precision CONDITION 2, sed-i evasion matrix.
- SQ[CDS-6/7/8/10] tests: A20/A22/A23 WARN+CAL-EMIT, audit-calibration-gate (240 LOC standalone + 31 fixture-isolated tests).

**Round 2:**
- F[cqa-r2-1] test_cal_emit_survives_pipe_bearing_source_tag: realistic pipe-bearing fixture (HIGH-severity + |source:[T1(OCC SR-11-7)] + |severity-basis:regulatory-filing); 3 distinct behavioral assertions (consumer regex roundtrip + parse_log valid-bucket + sanitization-intent preservation). Would fail against pre-fix code — teeth-check explicit.
- F[cqa-r2-2] TestA24SigmaVerifyInitPreFlight: 5 tests covering XVERIFY-present no-fire, load-bearing-without-XVERIFY fire path with full record-format assertions, ΣVerify-unavailable skip gate, XVERIFY-FAIL also suppresses, evaluate_single dispatch.
- F[cqa-r2-3] grep-verify TW BLOCK 3→4 sweep: 6 sweeps confirm 0 stale "BLOCK 3" references in agents+skills, 27 normalized to OPTION 2 phrasing, archive immutability preserved.
- F[cqa-r2-4] full regression: 1264 passed + 14 skipped + 1 PRE-EXISTING env-drift (settings.json effortLevel) per lead spec.
- **Round 2 peer-verify of TW: material drift FLAG (item 4)**: TW's "canonical verbatim block" claim partially falsified via SHA-128 — 3 distinct hashes pre-R3-2 (29 propagated agents carry legacy block vintage vs current _template). Routed to lead per P[ask-before-route-on-analysis-ack]. RESOLVED post-R3-2 via TW resync.

**Round 3:**
- F[cqa-r3-1] test_cal_emit_a24_record_lands_in_valid_bucket: end-to-end producer/consumer test with regression-lock pre-flight assertion (`assert "A24" in acg.VALID_GATES` halts non-silently if fix is reverted). Three-layer robustness: pre-flight assertion + end-to-end exercise + three independent assertions on produced record.
- F[cqa-r2-5] post-R3-2 hash-identity re-verify: SHA reduces to 2 distinct hashes (cluster A 7 files including _template; cluster B 23 sigma-review AH agents); diff is single trailing-blank-line — non-material whitespace delta.
- BONUS finding: _XVERIFY_ANY_RE suppression heuristic at chain-evaluator.py:950-953 is overly broad (matches literal English word "XVERIFY" + whitespace including newline). Severity LOW, separate-build candidate.
- Final: 247/247 canonical + 300/300 sigma-verify, zero regressions across 3 rounds (240→246→247).

---

## 3. Cross-Agent Convergence and Tensions

### Convergences
- **DA[#3] + CDS pipe-escape**: DA independently confirmed CDS's CAL-EMIT schema producer/consumer defect via XVERIFY (openai + google high-agree). Both agents recommended producer-side sanitization at chain-evaluator.py:613.
- **DA[#2] + SS BLOCK 3→4 doc drift**: SS independently grepped 27 stale citations matching DA's count. SS adds the safety-critical framing DA did not reach (a reader tracing "BLOCK 3" finds the pre-shutdown block and may wrongly conclude the rule is unenforced or that BLOCK 3 is redundant).
- **CDS + DA cross-section pattern recognition**: CDS r2 caught A24 VALID_GATES gap (same class as r1 pipe-escape). DA r3 spot-check predicted the 4th instance of doc-enumeration-drift at directives.md:456+462 §-enumeration and found it exactly where the pattern said it should be.
- **TA + DA on ADR[1] semantic clarification**: TA's PLAN-REVIEW and DA[#7] independently converged on "ADR[1] behavioral primary = SS spawn-prompt today + TA probe = operator-visibility + A24-enablement + forward-compat." Both demanded synthesis remediation.
- **SS + CDS on calibration-log integrity**: SS carried CDS's prior OSError silent-skip concern forward correctly, classifying calibration-log as separate telemetry surface from DA-verdict audit-trail (consistent with ADR[CDS-2..3] design intent).

### Tensions
- **TA r1 "needs-fixes:none-blocking" vs DA r1 "3 blockers"**: TA classified ADR[1] documented-drift and BLOCK-number renumber as "accept with flag" / non-blocking. DA cold-read reached three blockers (A24 missing, 27-file BLOCK drift, CAL-EMIT pipe-escape). Lead ruled DA on evidence weight: A24 was a missing LOCKED plan item, the 27-file gap was empirically grounded by grep, the pipe-escape was XVERIFY-confirmed by an independent agent. Substantive divergence resolved by lead ruling, not by prompting TA to retract.
- **SS dissent from DA[#4] xargs framing**: DA preferred to move bypass-recipe enumeration to a sealed note rather than advertise it in the enforcement-layer docstring. SS dissented — listing specific bypass forms in the enforcement file IS the contract; concealing them would be worse security hygiene. Lead accepted SS's position.
- **A24 ship vs defer**: lead's initial recommendation leaned toward defer-with-belief-downgrade. SS made a stronger argument for ship (A24 closes IC[9] partial gap; β+ calibration pattern applies; catches a compliance gap not a safety violation). Lead-recommendation REVISED defer→ship after evidence — anti-sycophancy update based on stronger argument, not user-pleasing.

---

## 4. DA Challenges and Resolutions

14 total: 13 in r1, 0 new in r2 (PASS), 1 LOW spot-check finding in r3.

### Round 1
| # | Target | Severity | Resolution |
|---|---|---|---|
| DA[#1] | A24 sigma-verify init pre-flight ENTIRELY MISSING from shipped code | high | resolved-shipped (r2 IE F[ie-r2-1] + 5 CQA tests) |
| DA[#2] | BLOCK 3 → BLOCK 4 doc drift across 27 files | high | resolved-shipped (r2 TW OPTION 2 sweep, expanded to 31 files post-R3+R3-2) |
| DA[#3] | CAL-EMIT schema pipe-escape defect (independent confirmation of CDS) | medium-high | resolved-shipped (r2 IE F[ie-r2-2] producer-side fix + CQA pipe-fixture test) |
| DA[#4] | xargs stdin KNOWN LIMITATION framing — bypass enumeration in docstring | low | defended-as-defer-legitimate (SS dissented from framing concern; deferred to future build per gold-plating discipline) |
| DA[#5] | evaluate_single() CLI dispatch dict lacks A20/A22/A23 entries | low | resolved-shipped (r2 IE coincidentally fixed when adding A24) |
| DA[#6] | gate_checks.py DA-filter plan-amendment scoping + ratification | low | defended (legitimate plan amendment with proper user-ratification trail and minimal scope) |
| DA[#7] | ADR[1] semantic clarification — "auto-ready" shipped as probe + forward-compat | medium | resolved-via-synthesis-language (TA + DA convergent: SS spawn-prompt is real behavioral primary today) |
| DA[#8] | SQ[CDS-6..8] mid-build "scope extension" framing | low | defended (work was in-plan scope; "extension" label was miscalibrated — assignment was the gap, not SQ scope) |
| DA[#9] | 23-vs-22 SAFETY-CRITICAL agent count + statistical-analyst propagation gap | medium | resolved-shipped (r2 TW propagated statistical-analyst; r3 add-on propagated 5 sigma-optimize agents after BUILD-CONCERN[tw-r2] surfaced premise falsification) |
| DA[#10] | Premise-audit self-application | low | defended (legitimate bootstrap exception — C1 audit YELLOW self-detected, retroactively closed; not structural hypocrisy) |
| DA[#11] | Test integrity §4d gap on TestA20CALEmitSchema missing pipe-fixture | medium | resolved-shipped (r2 CQA pipe-bearing fixture test closes §4d gap) |
| DA[#12] | §2d source provenance audit across ALL agents — mixed compliance | medium | deferred-to-synthesis (retrospective |source: tags recommendation for plan-track ADRs in C3 synthesis to prevent gap propagation) |
| DA[#13] | XVERIFY-FAIL on top-1 security-critical finding (infra error at MCP layer) | medium | accepted-as-documented-gap (CDS succeeded on a different query; plan-layer XVERIFY at SS ADR[SS-1] already confirmed scoped approach sound; r1 XVERIFY-FAIL does not invalidate prior verification) |

### Round 2
- 0 new DA challenges. DA-r2-EXIT: PASS, grade A-. Three r1 blockers empirically resolved; one was even improved beyond DA's recommendation (TW's block-number-agnostic phrasing superior to literal sweep).
- 1 cosmetic minor finding: A24 docstring at chain-evaluator.py:959 attributes scope-narrowing to "SS recommendation" but the A24 missing-check was DA[#1] in r1 (attribution drift in code comment, not behavioral, lead-discretion fix). Synthesis-deferred.

### Round 3 spot-check
- DA-r3-SPOT-CHECK: PASS, grade A. Empirically verified VALID_GATES + docstring + argparse fix closes CDS-r2-1 cleanly. Regression-lock structure ROBUST (better than any test pattern DA had seen this build).
- 1 LOW-severity 4th-instance finding (predicted by pattern): directives.md:456 + 462 enumerate `(§2i/§2j/§2d-severity)` for path-β+ gates but A24's §-tier is missing. Same class as DA[#2] (doc lies about machine state) but smaller scope (2 lines, single file) and lower severity (DA verdict protocol still mechanically enforced via `da-verdict:PENDING` string match, not §-number lookup). Deferred to future build.
- Pattern is now 4-of-4 confirmed in this build: hardcoded enumeration in human-facing context that diverges from machine-enforced source of truth (BLOCK 3 doc drift + r1 pipe-escape + r2 A24 VALID_GATES + r3 §-enumeration). Promotion-worthy as P[doc-enumeration-drift-from-machine-source-of-truth].

---

## 5. BUILD Rubric Scores

Per build-directives §3b, 6 dimensions on /4 scale. Source: c3-scratch ## build-rubric (Step 10b).

- **correctness: 4/4** — all 3 r1 blockers + 1 r2 blocker resolved, empirically verified pre-fix-vs-post-fix on each (DA hasattr + grep + regex; CDS parse_log + acg-rerun against real 210-record log; SS shlex evasion matrix 7/7; IE pre/post empirical). 13 historical A24 records recovered as bonus. β+ promotion loop now mechanically functional for A24.
- **test-coverage: 4/4** — 247/247 canonical (+7 new: 1 pipe-fixture + 5 A24 + 1 A24-consumer-roundtrip), 300/300 sigma-verify unchanged, zero regressions throughout three rounds (240→246→247). Tests verify behavior not runs per §4d. Realistic-fixture pattern (pipe-bearing fixture + A24-consumer-roundtrip would have caught defects ex-ante if written first). Regression-lock pattern in CQA r3 test halts non-silently on contract-revert.
- **maintainability: 4/4** — workspace_write helper dogfooded 67 times across C3 (0 WorkspaceAnchorNotFound; IC[6] hardened in production); OPTION 2 block-number-agnostic phrasing future-renumber-immune; CAL[R3-2-canonical-block-hash-identity] subsumes weaker CAL[R2-OPTION2-phrasing]; argparse choices auto-sync from sorted(VALID_GATES) prevents future drift; A24 layered-authority complement to A15 cleanly extends pattern.
- **performance: 4/4** — pytest 1264 passed in <6s wall (full canonical surface); sigma-verify 300/300 in <2s; A24 probe lightweight (sigma-verify init + 500-char workspace window scan); zero performance regressions. workspace_write helper stdlib-only, no runtime deps. audit-calibration-gate.py O(N) parse_log holds.
- **security: 4/4** — sed-i BLOCK 4 evasion matrix 7/7 empirically traced (BSD/joined/env/xargs-argv/absolute/backup-pass/stdin-pass per SS); IC[8] forward-contract docstring codifies PM[SS-2] mitigation in machine.py (not just plan); SS PASS r2 with 0 new attack vectors; A24 audit-time detection of XVERIFY-skip closes IC[9] partial gap (audit-trail completeness restored); xargs stdin scope-boundary HONEST (positive-contract test locks the limitation as test-enforced); BLOCK 3→4 doc-drift documentation-integrity risk fully closed via OPTION 2 + R3-2 resync (31 SAFETY-CRITICAL files content-byte-identical).
- **api-design: 4/4** — IC[1-9] all honored at code/test layer; documented-drifts (ADR[1] semantic clarification + IC[7-9] namespace propagation) handled via synthesis recommendations not silent-shipped; workspace_write signature exact-to-spec with WorkspaceAnchorNotFound double-guard (PM[4]); CAL-EMIT schema producer/consumer fully reconciled across 4 surfaces (chain-evaluator producer, audit-calibration-gate consumer regex, VALID_GATES allowlist, argparse choices); 4-instance doc-enumeration-drift pattern visible for promotion; template canonical-block-hash-identity invariant established.

**OVERALL: 24/24.** All 5 deferred LOW items + 1 cosmetic synthesis-defer logged as future-build candidates / synthesis recommendations per gold-plating-failure-mode discipline.

---

## 6. Pre-Mortem Failure Modes

Source: plan file ## Pre-mortem section. 10 failure modes total.

### TA-cluster
- **PM[1] (35%)** — #3 auto-ready regression in hateoas-agent upstream version bump silently breaks the fix.
  - **Manifested partially**: ADR[1] semantic shipped as probe + forward-compat hint, not literal auto-ready. Mitigation worked: BUILD-CONCERN flagged by IE-1, user-ratified interpretation A, IC[8] forward-contract docstring strengthens PM[SS-2]. A24 chain-eval pre-flight regression test added in r2.
- **PM[2] (25%)** — SQ[13] test surface explodes beyond 10-13h estimate.
  - **Avoided**: parallel engineer split (cluster A/B/C) + hard cap on test count per issue + re-estimation checkpoint held. Final: 80 new tests at C2, +7 in C3.
- **PM[3] (35%)** — premise-audit Step 7a skipped under delivery pressure.
  - **Mitigated structurally**: chain-eval presence check BLOCK from day-one (not WARN); legitimate retroactive close of self-application gap detected by C1 audit YELLOW.
- **PM[4] (20%)** — atomic Python replace edge-case failure in multi-byte-Unicode anchor → silent corruption.
  - **Avoided**: workspace_write.py:95-99 anchor-presence pre-check + lines 106-110 no-op-guard post-check (double-defense). IE-1 smoke-tested unicode-anchor (αβγ + emoji). 67 successful writes in production with 0 WorkspaceAnchorNotFound.

### CDS-cluster
- **PM[CDS-1] (40%)** — §2i CAL-EMIT calibration data never reaches 3 reviews → WARN-only indefinitely.
  - **Status**: pending — calibration window is multi-session by design. Mitigation in place: sigma-audit auto-invokes audit-calibration-gate.
- **PM[CDS-2] (25%)** — DA verdict protocol perceived as "extra DA work" → PENDING-never-resolved piles up.
  - **Status**: pending — encoded in directives.md:469 (PENDING-at-exit = process violation) and audit-calibration-gate.py:160-165 (not-reviewed >30% stall warning fires automatically). 13 historical A24 PENDING records currently surfaced post-r3 fix.
- **PM[CDS-3] (30%)** — audit-calibration-gate script never run.
  - **Status**: pending — sigma-audit auto-invokes per DA[#13] addendum.
- **PM[CDS-4] (30%)** — WARN→BLOCK promotion delayed beyond useful window because threshold too strict.
  - **Status**: pending — 20% FP threshold is C5-compatible starting point; revise after 2 promotions.

### SS-cluster
- **PM[SS-1] (20%)** — sed-i BLOCK over-fires on legitimate non-workspace files.
  - **Avoided**: scope pattern match includes path + shlex.split tokenization; 7/7 evasion matrix passed empirically.
- **PM[SS-2] (15%)** — future state-gated sigma-verify tools relying on gateway gap reintroduce the bug.
  - **Mitigation strengthened in r2**: IC[8] forward-contract docstring at machine.py:33-37 codifies the contract in canonical location, not just plan file.

---

## 7. Open Questions and Unresolved Gaps

### 5 deferred LOW items (future-build candidates per gold-plating discipline)
1. **xargs framing minor concern** (DA[#4]): bypass enumeration in phase-gate.py docstring is unusual; SS dissented in favor of keeping it as inspectable contract. Consider stripping to private-followup note if framing concern strengthens.
2. **IC[7-9] namespace non-propagation** (SS): plan IC[7-9] namespace lives only in plan file, not in agent-defs or directives. Recommend option-a (accept as plan-scoped, document in synthesis) for current build; option-b (propagate to security-specialist.md + _template.md + directives.md §2 sed-i-governance, ~10 LOC) deferred to next touch of these files.
3. **A24 docstring attribution drift** (DA r2 cosmetic): chain-evaluator.py:959 attributes scope-narrowing to "SS recommendation" but A24 missing-check was DA[#1] in r1. Lead-discretion fix.
4. **A24 §-enumeration in directives.md** (DA r3 spot-check): directives.md:456 + 462 enumerate `(§2i/§2j/§2d-severity)` for path-β+ gates; A24's §-tier missing. 4th instance of doc-enumeration-drift pattern.
5. **A24 no-Condition-1-suppression docstring note** (CDS r3 synthesis-defer): 1-line note in audit-calibration-gate.py docstring header to prevent future readers from assuming behavioral parity with A20 (A24 intentionally has no Condition-1-style suppression heuristic — A20 catches false-precision via qualifiers; A24 catches missing-XVERIFY which qualifiers don't resolve).

Plus: **XVERIFY over-suppression regex** (CQA r3 bonus finding): _XVERIFY_ANY_RE at chain-evaluator.py:950-953 matches literal English word "XVERIFY" + whitespace including newline (false-suppression on "XVERIFY was not run" prose). Severity LOW, separate-build candidate.

### 4 structural fix candidates from A24 silent-skip post-mortem
A24 was LOCKED in plan at 5 layers (PF[4] + ## Files line 162 + PM[1] mitigation + ## Verification step 3 + Scope Boundary expansion 3) but shipped without a check_a24 function. Root cause: plan ## Files entry without an SQ owner + TW punt-instead-of-flag at c2-scratch:409 ("referenced only, implementation is IE-1/CDS scope") was scope demotion without plan amendment. 4 candidates flagged for promotion-round:

1. **C1 plan-completeness check**: structural fix that would require every ## Files entry to have an SQ owner before plan exit-gate PASS. Would prevent unowned LOCKED items.
2. **C2 boot validation**: each cluster owner asserts at boot that all ## Files entries assigned to them have explicit SQ coverage; raise BUILD-CONCERN otherwise.
3. **TW agent-def update** (already drafted as P-candidate by TW at c3-scratch:660): "if Files-table entry is unassigned to any cluster's SQ → raise BUILD-CONCERN; ¬punt." Punting on gap is sycophantic-silence disguised as scope-discipline.
4. **C2 exit-gate diff**: chain-evaluator-side check that diffs plan ## Files table entries against shipped CHECKPOINT files-touched lists; missing entries surface as exit-gate fail.

### Multi-layer-contract-drift pattern (DA's promotion candidate)
4 instances of the same class confirmed in this build:
1. r1 BLOCK 3→4: 27 files said "BLOCK 3" while code shipped BLOCK 4.
2. r1 CAL-EMIT pipe-escape: producer didn't sanitize delimiter; consumer regex assumed pre-sanitized input.
3. r2 A24 VALID_GATES: producer emitted A24; consumer allowlist excluded it.
4. r3 §-enumeration: directive enumerates 3 §-tiers; producer added a 4th gate without updating directive.

Pattern: **hardcoded enumeration in human-facing context that diverges from machine-enforced source of truth**. Promotion-worthy as P[doc-enumeration-drift-from-machine-source-of-truth] — when shipping a new gate-id / block-number / schema-element, audit ALL human-facing enumerations (directives, agent files, skill phase docs) for stale lists.

### Template-vs-instance drift design discussion
TW R3-2 surfaced that 29 propagated agents carried a legacy block vintage vs current _template (TW used pre-R2 technical-writer.md as reference instead of authoritative _template.md — recursive-self-reference anti-pattern). Layered approach discussed:
- **sync script**: explicit re-sync from canonical _template.md to all enumerated propagated agents.
- **chain-evaluator A25 detection**: hash-identity-based content drift detection on the canonical block.
- **User ruling**: duplication preserves rule-following safety (sync script over generator); mechanical detection prevents drift.

### Recursive-self-reference anti-pattern (TW)
TW used prior propagation as canonical reference instead of source-of-truth. Corrected via R3-2 hash-identity invariant. Persisted as P[propagate-from-source-not-prior-instance].

### 13 historical A24 records recovered (bonus telemetry)
The r3 VALID_GATES fix immediately surfaced 13 PENDING A24 records that had been silently malformed in calibration-log.md. Telemetry recovery beyond synthetic-fixture verification — fix delivered measurable production benefit.

### 67 successful workspace_write helper writes through C3
IC[6] hardened in production with 0 WorkspaceAnchorNotFound exceptions across C3 use. Helper signature exact-to-spec, section-isolation convention validated empirically.

### Process strengths surfaced
- TW BUILD-CONCERN-then-ratify protocol applied 2x cleanly (no silent absorption): scope-gap raised + lead relayed + user ratified + executed.
- IE refusal+flag against task-list-teammate misroute at session start (process-integrity-over-completion in action).
- SS explicit anti-sycophancy bias-check + bonus end-to-end A24 wiring trace.
- CQA regression-lock pre-flight assertion pattern (better than any test pattern DA had seen this build).
- DA pattern-recognition from 3 instances to predicted-and-found 4th instance.
- CDS empirical-XVERIFY-via-local-python-c technique caught material latent defect that synthetic-fixture unit/integration tests missed (promotion-worthy).

### Process gaps logged for sigma-mem
- A24 silent-skip root cause: plan ## Files entry without SQ owner + TW punt-instead-of-flag → 4 structural fix candidates for promotion-round.
- C1 audit YELLOW retroactive premise-audit close: legitimate self-detection but flagged for future builds to run Step 7a before C1 scratch drafting.
- task-list-teammate auto-router misroute at session start: mitigation pattern documented (IE correctly refused per CLAUDE.md ## Lead Role Boundaries).
