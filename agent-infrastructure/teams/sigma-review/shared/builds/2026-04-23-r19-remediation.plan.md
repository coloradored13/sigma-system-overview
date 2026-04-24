# sigma-build plan: r19-remediation

## Meta
- created: 2026-04-23
- build-id: 2026-04-23-r19-remediation
- tier: BUILD TIER-3 (score 19)
- status: built
- plan-exit-gate: PASS
- plan-belief: P=0.88
- DA-grade: A-
- build-exit-gate: PASS-PENDING-C3
- build-belief: P=0.00 (C3 computes)
- team-name: r19-remediation-c1
- c2-team-name: r19-remediation-c2
- c2-completed: 2026-04-24

## Context
Remediate the top-10 ROI infrastructure + protocol-layer issues surfaced in the R19 sigma-review post-mortem (2026-04-22 ai-agent-rollout-playbook-vet review — audit GREEN, eval B 3.14). Both code (chain-evaluator.py, phase-gate.py, sigma-verify MCP) and directives/spawn-templates/agent-defs are in scope. Memory source: `~/.claude/projects/-Users-bjgilbert/memory/project_sigma-review-infrastructure-issues.md`.

## Prompt Understanding
**Q[]** (build scope):
- Q1: Fix critical infra — #1 sed-i mechanical block, #3 ΣVerify agent-context tool inheritance, #4 A12 parser key-mismatch
- Q2: Fix high-priority infra — #5+#14 peer-verify regex + spawn template alignment, #19 A3 DB-step parser false negatives, #20 A12 archive timing window
- Q3: Add 4 protocol-layer gates — #21 premise-audit pre-dispatch, #22 §2i precision gate, #23 governance min-artifact, #24 §2d severity provenance
- Q4: Update directives + spawn templates + agent defs to enforce mechanically (not directive-only)

**H[]** (hypotheses; test results):
- H1 CONFIRMED: sigma-verify MCP source is user-controlled; `machine.py:17-128` is the fix location; root cause is HATEOAS state-gating not registry gap
- H2 PARTIALLY CONFIRMED: new analytical gates can be calibrated, but only scoped CONDITION 2 is code-detectable; CONDITION 1 defers to DA adjudication with β+ audit-calibration tracking toward future BLOCK-promotion
- H3 SUPPORTED: premise-audit fits as workflow Step 7a pre-spawn, not new agent role (TA+CDS convergence)
- H4 CONFIRMED: no circular dependencies across 30+ SQs; SQ[0] fixture prereq gates SQ[3]+SQ[13b-c]
- H5 FALSIFIED: live pytest discrepancy (TA 154, CQA 92 — C2 must reconcile); real regression floor is currently-passing tests after SQ[0] fixture fix

**C[]** (constraints):
- C1: Top-10 ROI only (MEDIUM/LOW R19 #6-#18 deferred, minus #2 which was promoted mid-build)
- C2: Both code + directives in scope
- C3: No regressions to chain-evaluator/phase-gate test suites
- C4: New gates with no legitimate override → hard BLOCK
- C5: When a gate over-fires, defend each invocation rather than add exceptions
- C6: All changes git-committed + pushed from sigma-system-overview per session-end checklist
- C7: 3 already-resolved R19 artifacts out of scope (UP-B, UP-C, MITRE ATLAS)
- C8: XVERIFY excludes anthropic — cross-model must be cross-family

## Scope Boundary
**Implements:**
- 11 original R19 tickets covering 9 ROI priorities (5 infrastructure + 4 protocol-layer)
- 4 in-scope expansions:
  1. `check_a3` DB-depth duplication bundled into #19 fix (chain-evaluator.py:162-183 layered authority clarified: gc=presence, chain-eval=depth, sequential not conflicting)
  2. A24 pre-flight chain-eval check for sigma-verify init compliance (renamed from A21 to avoid collision with CDS A20)
  3. β+ audit-calibration for #22/#23/#24 — WARN-first with empirical 3-review calibration tracking via append-only log + audit-calibration-gate
  4. R19 #2 targeted workspace-write-contract (promoted mid-build from deferred — 4+ session manifestations validated CRITICAL classification)

**Does NOT implement:**
- MEDIUM/LOW R19 #6–#18 (except #2 which was promoted)
- General concurrency infrastructure (only workspace.md + sigma shared files)
- sigma-verify default-anthropic-exclusion (deferred to separate build)
- Lost chain-eval/phase-gate test files (traced to deliberate consolidation per commits ea5ae97 + d9d21ad)
- Already-resolved R19 artifacts (UP-B, UP-C, MITRE ATLAS — resolved 2026-04-23)

## Architecture Decisions (locked)
**From tech-architect:**
- ADR[1] #3 ΣVerify: auto-ready at `build_machine()` startup when keys present | alternatives: spawn-prompt (SS secondary), hateoas-agent auto-init (out-of-scope) | rationale: R19 5-agent soft-control failure demonstrated compliance-reliance unsafe | source:[code-read machine.py:17-128] | XVERIFY: openai partial/medium-resolved + nemotron agree/high + google 503-gap (C8 honored) | DA[#2] compromise: TA auto-ready primary + SS spawn-prompt belt-and-suspenders + documented gateway semantics
- ADR[2] #4 A12 parser: rename chain-evaluator.py:241 `archive_exists` → `archive_file_found` (leaf consumer) | alternatives: rename gate_checks.py source key | rationale: gate_checks is source-of-truth API; leaf fix = zero downstream risk
- ADR[3] #20 A12 timing: 24h grace-window (CONCEDED post-CQA non-looping challenge) | rejected: signal-driven re-run in Stop hook (violates non-looping invariant per chain-evaluator.py:625-640)
- ADR[4] #21 premise-audit: workflow Step 7a pre-spawn | alternatives: DA framework extension, new agent role, CDS's initial Step 8.5 | rationale: anti-anchoring requires pre-Q/H/C-confirmation sequence
- ADR[5] #2 workspace-write-contract: atomic Python replace + section-isolation convention | rejected: (a) Edit-only (doesn't fix anchor-movement), (b) advisory .lock (compliance-reliant), (c) lead-proxy queue (bottleneck) | empirical evidence this session: 3x TA success vs 4x DA Edit anchor-failures

**From cognitive-decision-scientist (path β+ audit-monitored):**
- ADR[CDS-1] #21 premise-audit sequence constraint: lead answers PA[1-4] BEFORE user-confirms Q/H/C | placed at Step 7a per TA ADR[4] concession
- ADR[CDS-2] #22 §2i precision gate: CONDITION 2 code-detection (A20 WARN) + CONDITION 1 explicitly DEFERRED with code-comment | thresholds: ≥3 reviews + ≤20% FP + ≥5 DA-verdicted → promote WARN→BLOCK
- ADR[CDS-3] #23 governance min-artifact: TIER-A/B/C taxonomy + DA exit-gate artifact quality check (both required — format alone insufficient)
- ADR[CDS-4] #24 §2d severity provenance: 3-field severity-basis tag + DA explicit audit directive (absence of tag = process violation)

**From security-specialist:**
- ADR[SS-1] #1 sed-i BLOCK 3: workspace-path + `/.claude/hooks/` scope, shlex.split() argv tokenization, no-bypass-allowlist | XVERIFY post-refinement: scoped approach sound, raw regex insufficient
- ADR[SS-2] #3 ΣVerify belt-and-suspenders: spawn-prompt + agent-def instruction as defense-in-depth to TA ADR[1] server-side fix (SUPERSEDED as primary per SS peer-verify self-correction + DA[#2] compromise)
- ADR[SS-3] audit-trail for #22/#23: NO separate log — workspace gate-log + A12 archive sufficient; separate log deferred if framework becomes multi-user/compliance-audited

## Interface Contracts (locked)
**TA namespace:**
- IC[1] phase-gate ↔ Bash (sed-i BLOCK 3 condition + exit-code-2 + no-bypass)
- IC[2] spawn-prompt ↔ sigma-verify init (instruction → agent init call → ready state)
- IC[3] chain-evaluator ↔ workspace gate-log (#22/#23 fire → gate-log entry; CAL-EMIT format per β+)
- IC[4] DB-depth check layered authority: `gc.check_dialectical_bootstrapping` = PRESENCE; chain-evaluator `check_a3` = DEPTH; sequential, not redundant
- IC[5] peer-verify canonical format: c1-plan.md Step11 + sigma-lead.md §2 + c2-build.md + _template.md atomically same-commit; regex unchanged; 3-hash "verifying" canonical
- IC[6] workspace-write-contract: atomic Python replace + anchor selection (section header + first unique line) + `WorkspaceAnchorNotFound` error path + section-isolation scope (workspace.md + builds/*/*.md + shared/workspace.md)

**SS namespace (renumbered post-DIV[3] reconciliation):**
- IC[7] (was IC[1]): security contract on hook ↔ tool-call validation for sed-i BLOCK
- IC[8] (was IC[2]): MCP trust boundary — call-time authorization check for future state-gated tools (per DA[#2] compromise note)
- IC[9] (was IC[3]): audit-trail integrity — workspace gate-log is tamper-resistant via A16-A18 peer verification (no separate log needed)

## Sub-task Decomposition
Total: 30 SQs across 3 plan-track-owner scopes + 1 prerequisite + parallel-engineer-cluster mapping.

**Prerequisite (day-1 gate):**
- SQ[0] fixture-fix: MINIMAL_WORKSPACE fixture uses non-roster agent names → fix to use roster.md entries | owner: code-quality-analyst | est: 1-2h | blocks: SQ[3] + SQ[13b] + SQ[13c]

**TA cluster (~12h total):**
- SQ[1] #3 machine.py auto-ready: ~5 LOC in `build_machine()` | owner: IE | est: 1h | files: sigma-verify/src/sigma_verify/machine.py
- SQ[2] #20 A12 24h grace-window: ~20 LOC + deterministic datetime-mock tests | owner: IE | est: 1h | files: chain-evaluator.py
- SQ[3] #19+check_a3 DB extraction + layered authority: split-by-DB then require (1)(2)(3) within segment; preserve gc depth-presence layering | owner: IE | est: 2h | files: chain-evaluator.py:162-183
- SQ[4] #5+#14 peer-verify atomic: spawn template + sigma-lead.md §2 + c1-plan.md Step11 + c2-build.md + _template.md all same commit | owner: TW | est: 1-2h
- SQ[5] #3 spawn-prompt belt-and-suspenders instruction | owner: TW (coordinates with SS SQ[SS-3])
- SQ[6] sigma-verify test suite confirmation (separate repo, test ownership clarification) | owner: IE or CQA (C2 to resolve)
- SQ[7] #1 sed-i BLOCK 3 implementation | owner: IE | est: 2-3h | files: phase-gate.py; expanded scope per DA[#6] includes `/.claude/hooks/`
- SQ[8] agent-def propagation for #1 + #14 coordinated changes | owner: TW | est: 2-3h | files: ~/.claude/agents/*.md (24 files per CQA count), _template.md
- SQ[9] #21 c1-plan.md Step 7a insertion + workspace template `## premise-audit-results` section | owner: TW | est: 1h | files: c1-plan.md
- SQ[10] #22 directive text in directives.md + build-directives.md §2i sequential entry | owner: TW | est: 1h
- SQ[11] #23 governance min-artifact directive text | owner: TW | est: 1h
- SQ[12] #24 §2d severity-provenance extension | owner: TW | est: 1h
- SQ[13] (split into 13a-g per DA[#3] challenge — 10-13h total):
  - 13a fixture-fix tests (covered by SQ[0])
  - 13b A12 parser tests (2 tests)
  - 13c A16/A17/A18 peer-verify tests (8-12 tests)
  - 13d A3 chain-evaluator DB extraction tests (4-6 tests)
  - 13e A12 24h grace tests (2-3 deterministic datetime-mock tests)
  - 13f A20 §2i precision CONDITION 2 tests (4-5 tests scoped per CDS)
  - 13g SS BLOCK 3 sed-i detection tests + shlex.split evasion forms (8 tests)
- SQ[14] workspace_write() helper implementation per IC[6] | owner: IE | est: 2h | files: new helper + imports across chain-evaluator consumers + agent spawn template docs

**CDS cluster (β+ audit-calibration mechanics):**
- SQ[CDS-1] §2p premise-audit directive for directives.md | owner: TW | dependency: ADR[4]+ADR[CDS-1] | answers OQ-TW3
- SQ[CDS-2] §2i precision gate directive for directives.md (WARN-first + CONDITION 1 deferred) | owner: TW | dependency: ADR[CDS-2] | chain-eval-ID: A20 (TA confirmed)
- SQ[CDS-3] §2d-severity provenance sub-section | owner: TW | dependency: ADR[CDS-4]
- SQ[CDS-4] governance min-artifact TIER taxonomy + DA exit-gate quality check | owner: TW | dependency: ADR[CDS-3]
- SQ[CDS-5] c1-plan.md Step 7a + workspace template | owner: TW | dependency: ADR[CDS-1] (merge with SQ[9])
- SQ[CDS-6] chain-evaluator.py A20 §2i WARN + CAL-EMIT emission | owner: IE | 4-5 tests | ~20 LOC scoped CONDITION 2
- SQ[CDS-7] chain-evaluator.py §2i governance-artifact WARN + CAL-EMIT | owner: IE | ~20 LOC
- SQ[CDS-8] agent `_template.md` severity-provenance tag format addition + ~15-20 LOC check_a24_severity_provenance detection stub for CAL-EMIT | owner: TW + IE
- SQ[CDS-9] calibration-log.md append-only file at sigma-review/shared/ + backup-memory.sh addition | owner: IE | est: 0.5h
- SQ[CDS-10] audit-calibration-gate.py standalone script | owner: IE | est: 2h | reads calibration-log, evaluates thresholds, outputs PROMOTE/RECALIBRATE/CALIBRATING signal
- SQ[CDS-11] directive text for β+ calibration process | owner: TW
- SQ[CDS-12] DA verdict protocol extension to DA exit-gate format (CAL-EMIT PENDING → legitimate|false-positive|not-reviewed) | owner: TW (directives) + IE (chain-eval parse)

**SS cluster:**
- SQ[SS-1] phase-gate.py BLOCK 3 implementation (shlex.split, scope workspace + hooks, no-bypass) | owner: IE | est: 2-3h
- SQ[SS-2] test matrix for shlex.split evasion forms (env-wrapper, xargs-wrapper, -i.bak, -i '' combined forms) | owner: CQA | est: 2h
- SQ[SS-3] ΣVerify init instruction in spawn templates + agent defs (belt-and-suspenders documentation) | owner: TW | est: 1h

**Parallel engineer eligibility (per build-directives §3a.1):**
- Cluster A (TA SQ[1-7,14] + SS SQ[SS-1]): hooks/chain-evaluator/phase-gate/sigma-verify code surface — single engineer (shared file risk)
- Cluster B (TA SQ[8-12] + CDS SQ[CDS-1..5,11,12] + SS SQ[SS-3]): directive/template/agent-def edits — separate engineer via technical-writer ownership (no code-file overlap with Cluster A)
- Cluster C (TA SQ[13a-g] + CDS SQ[CDS-6..10] + SS SQ[SS-2]): test code — separate engineer for test expansion (isolated from production code until merge)
- 3 independent clusters → parallel-engineer-eligible per §3a.1; primary implementation-engineer + implementation-engineer-2 + implementation-engineer-3 recommended for C2

## Pre-mortem
- PM[1] (TA-1, 35% likelihood): #3 auto-ready regression in hateoas-agent upstream version bump breaks the fix silently | early-warning: CI tool-visibility test failure | mitigation: A24 chain-eval pre-flight check + regression test in sigma-verify CI
- PM[2] (TA-2, 25%): SQ[13] test surface explodes beyond 10-13h estimate once touch-points are measured | early-warning: SQ[13b-c] over-runs at 50% | mitigation: parallel engineer split + hard cap on test count per issue + re-estimation checkpoint
- PM[3] (TA-3, 35%): premise-audit Step 7a skipped under delivery pressure — same failure mode as directive-only | early-warning: audit sees missing `## premise-audit-results` section | mitigation: chain-eval presence check (BLOCK from day one — binary check, no calibration window needed)
- PM[4] (TA-4, 20%): atomic Python replace has edge-case failure in multi-byte-Unicode anchor | early-warning: silent corruption (worst case) | mitigation: test matrix includes emoji, accents, multi-line anchors; anchor validation asserts `old in file` before replace
- PM[CDS-1] (40%): §2i CAL-EMIT calibration data never reaches 3 reviews → WARN-only indefinitely | early-warning: audit-calibration-gate returns CALIBRATING 6+ reviews | mitigation: sigma-audit runs gate automatically + lead flags prolonged CALIBRATING
- PM[CDS-2] (25%): DA verdict protocol extension perceived as "extra DA work" → PENDING-never-resolved piles up | early-warning: not-reviewed count >30% after 3 reviews | mitigation: hard requirement at DA exit-gate to verdict all PENDING records
- PM[CDS-3] (30%): audit-calibration-gate script never run (lead forgets, sigma-audit integration stalls) | mitigation: sigma-audit auto-invokes per DA[#13] addendum
- PM[CDS-4] (30%): WARN→BLOCK promotion delayed beyond useful window because threshold too strict | mitigation: 20% FP threshold is C5-compatible starting point; revise after 2 promotions
- PM[SS-1] (20%): sed-i BLOCK over-fires on legitimate non-workspace files | mitigation: scope pattern match includes path + shlex.split tokenization; test matrix covers edge forms
- PM[SS-2] (15%): future state-gated sigma-verify tools relying on gateway gap reintroduce the bug | mitigation: documented gateway semantic contract in machine.py + DA[#2] compromise note

## Files
| File | Action | Description |
|---|---|---|
| `~/.claude/hooks/chain-evaluator.py` | modify | rename key (line 241), rewrite check_a3 (split-by-DB + require (1)(2)(3)), add A12 24h grace, add A20 §2i CONDITION 2 + CAL-EMIT, add A22 governance artifact, add A23 severity provenance, add A24 sigma-verify init pre-flight |
| `~/.claude/hooks/phase-gate.py` | modify | add BLOCK 3 for sed-i with workspace + hooks scope, shlex.split tokenization |
| `~/.claude/teams/sigma-review/shared/gate_checks.py` | preserve | leaf key unchanged (per ADR[2] direction); no edit |
| `~/Projects/sigma-verify/src/sigma_verify/machine.py` | modify | auto-ready at build_machine() startup (~5 LOC) + documented gateway semantic contract comment |
| `~/.claude/teams/sigma-review/shared/directives.md` | modify | add §2i precision gate, §2p premise-audit, extend §2d for severity provenance, add §8e corruption recovery template (ΣComm) |
| `~/.claude/teams/sigma-review/shared/build-directives.md` | modify | add BUILD variants of new §2i/§2p |
| `~/.claude/skills/sigma-build/phases/c1-plan.md` | modify | add Step 7a premise-audit, update Step 11 spawn prompt peer-verify canonical format |
| `~/.claude/skills/sigma-build/phases/c2-build.md` | modify | peer-verify canonical format propagation |
| `~/.claude/agents/_template.md` | modify | add sed-i workspace rule, severity-provenance tag, premise-audit reference |
| `~/.claude/agents/*.md` (24 files) | modify | safety-critical sed-i rule propagation per TW tier rule |
| `~/.claude/agents/sigma-lead.md` | modify | §2 peer-verify format + section-isolation convention |
| `~/.claude/teams/sigma-review/shared/calibration-log.md` | create | append-only file for β+ audit calibration |
| `~/.claude/teams/sigma-review/shared/audit-calibration-gate.py` | create | standalone script, reads calibration-log, outputs PROMOTE/RECALIBRATE/CALIBRATING |
| `~/Projects/sigma-system-overview/agent-infrastructure/scripts/backup-memory.sh` | modify | add calibration-log.md to backup set |
| `workspace_write()` helper | create | per IC[6] atomic Python replace pattern, callable from chain-evaluator + agents |
| `~/.claude/teams/sigma-review/shared/test_gate_checks.py` | modify | add 30+ new tests per SQ[13a-g] + SS SQ[SS-2] + CDS SQ[CDS-6..10] |

## Plan Challenge Summary
- **DA challenges:** 12 issued (DA[#1-#12]) + 1 addendum (DA[#13]) + 1 final (DA[#14]) = 14 total entries
- **DA grade:** A- (engagement upgraded from B+ post-team-substantive-response)
- **Circuit breaker:** NOT FIRED (significant dissent throughout — build-track issued 20 BUILD-CHALLENGEs across TW+CQA+IE + DA 12; plan-track responded with concede/defend/compromise per recipe)
- **Concessions:** TA 5 (DA[#1]+DA[#2]+DA[#7]+TW BC[#2]+CQA BC[#4]), SS 3 (DA[#2]+DA[#6]+DA[#11]), CDS 3 (DIV[2]+DA[#5]+DA[#3] accepted)
- **Defenses:** TA DA[#8] with engaged DB[4] rerun, CDS DA[#8] with DB[ADR[2]-r2] rerun ("concession-strengthens-thesis" pattern)
- **Unresolved tensions:** none blocking at r1. Pre-C2 items: DA[#10] C4-vs-C5 resolved by user (path β+ audit-monitored); DA[#11] A24 rename; DIV[3] IC namespace reconciled.
- **Process patterns promoted this session (sigma-mem ~30 entries):** P[team-self-correction-before-DA-pressure], P[concession-strengthens-thesis-via-DB-rerun], P[live-empirical-test-as-ADR-prerequisite], P[regex-empirical-verification-before-ADR-lock], P[build-meta-observation-validates-challenge], P[DOC-CHANGE-MAP as C1 build-track deliverable], P[atomicity-constraint naming], P[ΣComm-boundary-check as C1 feasibility gate], P[directive-propagation split by risk tier], P[workspace atomic Python replace + section-isolation], P[audit-calibration-gate], P[CAL-EMIT-schema], P[premise-audit-sequence-constraint], and more.

## Build Status (written by C2, 2026-04-24)

### Test Results
- total: 240 | passed: 240 | failed: 0 | new: +80 (cluster-C: 61 cycle-1 + 19 cycle-2)
- regressions: 0 (against 143/143 post-SQ[0] baseline; 11 SQ[0] pre-existing failures cleared)
- surface breakdown:
  - test_chain_evaluator.py: 82/82 (was 42 pre-session)
  - test_phase_gate.py: 59/59 (was 50 pre-session)
  - test_gate_checks.py: 68/68 (was 57 passing + 11 pre-existing fails)
  - test_audit_calibration_gate.py: 31/31 (new file, SQ[CDS-10])
- sigma-verify repo: 300/300 (ie-1 SQ[1] machine.py, coverage 90%)
- MERGE-VERIFIED: 240/240 post-merge (no worktrees used; file-ownership coordination, zero cluster overlap)

### Checkpoints
CHECKPOINT[ie-1] (final, post-extension): 5 files modified / 1 new file / 2 repos | 7 plan SQs + 3 extension SQs + 1 plan-amendment + 1 hygiene fix | interfaces-matched: yes (IC[1-6] all honored) | drift: none | surprises: 2 (ADR[1] interpretation gap via BUILD-CONCERN, BLOCK 3→4 renumber via C5) — both resolved clean
CHECKPOINT[tw] (final): 29 files modified / +686 TW-owned LOC | 10 plan SQs | interfaces-matched: yes (IC[5] peer-verify atomic set + CAL[9] 4-file, CAL-EMIT schema match, CAL[7] risk-tier split 23 agents) | drift: none (22→23 count-correction applied in-place) | surprises: none
CHECKPOINT[cqa] (final, cycle-2): 3 files modified + 3 new files / +80 tests | 12 cqa-owned SQs (incl SQ[0] gating) | interfaces-matched: yes (CAL-EMIT schema asserted, details.cal_emit_records consumed from ie-1 helper) | drift: none | surprises: 1 (xargs stdin bypass flagged as BUILD-CONCERN, resolved via option (a) docstring narrow + positive-contract test)

### Cross-Model Code Review
SKIPPED at C2 per c2-build.md Step 6 (advisory, ¬blocking C2 exit). Deferred to C3 where XREVIEW is structural. Rationale in c2-scratch ## cross-model-code-review.

### SQ Status (32 SQs total)
Cluster A (IE-1, 7 plan + 3 extension + 1 amendment + 1 hygiene):
- SQ[1] sigma-verify auto-ready: DONE — interpretation A (~8 LOC machine.py + docstring + forward-compat hint; 300/300 sigma-verify)
- SQ[2] A12 24h grace: DONE — synchronous mtime delta per CAL[1], both branches smoke-tested
- SQ[3] A3 DB extraction: DONE — split-by-DB + (1)(2)(3) requirement, IC[4] layered authority preserved
- SQ[6] sigma-verify test scope: DONE — read-only investigation, SQ[1] tests in sigma-verify repo per PF[5]
- SQ[7]+SS-1 sed-i BLOCK 4: DONE — renumbered from BLOCK 3 per C5 (existing code drift), 22/22 evasion matrix pass
- SQ[14] workspace_write helper: DONE — IC[6] exact signature, dogfooded in-production, WorkspaceAnchorNotFound raises on no-op
- SQ[CDS-6] A20 precision gate: DONE (scope-extension) — §2i CONDITION 2 + suppression heuristic, ~20 LOC
- SQ[CDS-7] A22 governance artifact: DONE (scope-extension) — TIER-A/B/C + ARTIFACT-GAP detection, ~20 LOC
- SQ[CDS-8 IE-portion] A23 severity provenance: DONE (scope-extension) — 3-field tag detection, native-domain no-fire, ~15 LOC
- PLAN-AMENDMENT gate_checks.py DA-filter: DONE — 1-line exclusion in _load_roster_agents:233 (user-ratified option C)
- HYGIENE xargs docstring narrow: DONE — phase-gate.py:300 KNOWN LIMITATION block + ADR[SS-1] cross-ref

Cluster B (TW, 10 plan SQs):
- SQ[4] #5+#14 peer-verify atomic: DONE — c1-plan Step 11 + sigma-lead §2 + c2-build + _template.md (4-file atomic per CAL[9])
- SQ[5]+SS-3 ΣVerify init belt-and-suspenders: DONE — spawn templates + _template boot step
- SQ[8] #1 sed-i ban propagation: DONE — 23 SAFETY-CRITICAL agents + _template (count corrected from 22 per CAL[7] risk-tier rule)
- SQ[9]+CDS-5 Step 7a premise-audit: DONE — c1-plan Step 7a + ## premise-audit-results template + preflight checklist
- SQ[10]+CDS-2+CDS-11 §2i precision gate: DONE — directives.md + build-directives.md BUILD variant, CONDITION 2 code + CONDITION 1 directive + β+ calibration + CAL-EMIT
- SQ[11]+CDS-4 §2j governance artifact: DONE — directives.md + TIER-A/B/C + DA ARTIFACT-REVIEW
- SQ[12]+CDS-3 §2d-severity provenance: DONE — directives.md + build-directives + _template checkbox (template-only per CAL[7])
- SQ[CDS-1] §2p premise-audit directive: DONE — directives.md non-sequential per CDS BC[TW-#5]
- SQ[CDS-12] DA CAL-EMIT verdict protocol: DONE — DA enforcement extension + PENDING handling
- §8e corruption recovery template: DONE — 7-step ΣComm conversion + sigma-lead cross-ref

Cluster C (CQA, 12 SQs incl gating):
- PF[1] baseline reconciliation: DONE — 154/143/11 authoritative, C1 "92" falsified, memory updated
- SQ[0] MINIMAL_WORKSPACE fixture fix: DONE — roster-valid names + combined with gate_checks DA-exclusion cleared all 11 pre-existing
- SQ[13b] A12 parser tests: DONE — 2 tests, TestA12ArchiveFileFoundKeyRename
- SQ[13c] A16/A17/A18 peer-verify: DONE — 10 tests, TestPeerVerifyRegexContract (IC[5] lock)
- SQ[13d] A3 DB extraction: DONE — 6 tests, TestA3DBGenuineVsReference (R19 #19 regression lock)
- SQ[13e] A12 24h grace: DONE — 3 tests, os.utime determinism (no datetime mocking)
- SQ[13f] A20 §2i precision CONDITION 2: DONE (cycle-2) — 6 tests, triggers + suppressors
- SQ[13g]+SS-2 sed-i evasion matrix: DONE — 9 tests (6 BLOCK 4 direct + 3 evasion) + 1 xargs positive-contract
- SQ[CDS-6] A20 WARN+CAL-EMIT: DONE (cycle-2) — 4 tests, schema compliance + no-fire + multi-fire + review-id fallback
- SQ[CDS-7] A22 governance TIER: DONE (cycle-2) — 4 tests, TIER/GAP/MEDIUM/non-gov
- SQ[CDS-8] A23 severity provenance: DONE (cycle-2) — 3 tests, native/extrapolated/tag-present
- SQ[CDS-9] calibration-log + backup: DONE — calibration-log.md created + backup-memory.sh $CALIBRATION_LOG block
- SQ[CDS-10] audit-calibration-gate.py: DONE — 240 LOC standalone script + 31 fixture-isolated tests

### Build Deltas
- 40 files in sigma-system-overview (+2683 insertions, -65 deletions)
- 1 file in sigma-verify (+31 LOC)
- 5 new files created: workspace_write.py, audit-calibration-gate.py, test_audit_calibration_gate.py, calibration-log.md, c2-scratch.md

### sigma-mem Persistence
19 patterns + 1 correction persisted across cluster agents:
- IE-1: 8 patterns (workspace_write, BLOCK renumber, shlex evasion matrix, BUILD-CONCERN flag, plan-scope amendment via user-ratification, auto-ready probe, DB split-by-marker, path β+ WARN-first)
- TW: 4 patterns (TW-C2 execution, ΣComm-conversion-not-label-swap, count-drift-spec-vs-filesystem, dogfood-new-IC-at-first-use)
- CQA: 6 patterns (dataclass py3.14 importlib, fenced-code-block parser-exclusion, positive-contract for known limitations, ask-before-route-on-analysis-ack, SQ effort budget recon+triage floor, WARN-gate test pattern details.cal_records) + 1 correction (lead-ack ≠ lead-ruling)

### Process Notes for C3 Review
- **ADR[1] semantic clarification**: ADR[1] ships probe + forward-compat hint (not literal auto-ready in MCP list_tools sense). Behavioral unlock pairs with SS spawn-prompt (SQ[SS-3]) as real primary today. Documented during C2 execution, flagged for C3 synthesis.
- **Plan-scope amendment (gate_checks.py)**: user-ratified option C added 1-line DA exclusion in _load_roster_agents. "Preserve | no edit" directive was scoped to ADR[2] A12 key-rename, not a blanket. Pre-existing latent bug (comment at 223 documented filter-intent never implemented, test at 189-194 asserted exclusion, roster.md addition 2026-04-11 broke it) surfaced only when SQ[0] fixture removed the synthetic-name cover. Not an ADR[2] violation.
- **BLOCK 3→4 renumber**: phase-gate.py had pre-shutdown BLOCK 3 from code drift post plan-authorship. IE-1 renumbered sed-i to BLOCK 4 to preserve existing semantics. Defended via C5 "defend the invocation". In-scope C2 hygiene, not plan amendment.
- **3 BUILD-CONCERNs surfaced + resolved**: SQ[1] ADR[1] interpretation gap (user ratified A), gate_checks.py DA-filter latent bug (user ratified C), xargs sed-i argv-vs-stdin bypass (lead ratified option a docstring narrow). All 3 used proper "flag + wait for ratification" protocol.
- **Process-integrity correction**: CQA initial overreach routed gate_checks fix to ie-1 before user ratification. Lead issued STOP + intervention, CQA engaged cleanly, persisted P[ask-before-route-on-analysis-ack] to sigma-mem. Subsequent xargs BUILD-CONCERN escalation handled correctly per learned mechanical check.
- **Scope extension mid-build**: SQ[CDS-6..8 IE-portion] chain-evaluator emissions (~55 LOC) + their tests (~19) were not in initial cluster-A assignment (lead's miss). User ratified extension mid-C2. Added 2h wall-time; calibration data captured as P[sq-effort-budget-recon-plus-triage-floor].
- **Count correction**: "22 SAFETY-CRITICAL agents" in CAL[7] was C1 DOC-CHANGE-MAP accounting error; actual count 23. TW flagged + applied correction in-place per rule-semantics over spec-number.

### Known Gaps (documented, not open for C2)
- xargs stdin-piped paths bypass phase-gate sed-i BLOCK 4 (documented in phase-gate.py KNOWN LIMITATION block + positive-contract test + scratch; scope expansion rejected, future SQ if incident surfaces)
- ADR[1] gateway-semantic contract requires future state-gated tools to add call-time authorization (documented in machine.py docstring per DA[#2] compromise)
- §2i CONDITION 1 full-semantic detection deferred per ADR[CDS-2]+DA[#5] (suppression heuristic same-line only in code)
- β+ calibration gate promotion remains deliberate lead action on PROMOTE signal (documented in audit-calibration-gate.py output handling)

## Build Review Summary
*(empty — written by C3)*

## Close Status
*(empty — written by C3)*

## Verification
How to verify the build end-to-end in C3 review:
1. **chain-evaluator A12 parser**: run `python3 ~/.claude/hooks/chain-evaluator.py evaluate` against an archived workspace with archive_file_found=true — verify A12 passes (previously failed silently)
2. **sed-i BLOCK 3**: attempt `sed -i 'pattern' ~/.claude/teams/sigma-review/shared/workspace.md` — verify phase-gate exits 2 with BLOCKED message; attempt `sed -i.bak 'pattern' ...` — verify passes (backup form)
3. **sigma-verify auto-ready**: spawn a new agent in a fresh session, have it call `verify_finding` without explicitly calling `init` first — verify ToolSearch returns verify_finding schema (auto-ready worked)
4. **A3 DB extraction**: provide workspace with 10 DB[] references (5 genuine exercises + 5 finding-refs/summaries) — verify chain-evaluator counts only the 5 genuine exercises per (1)(2)(3) marker requirement
5. **peer-verify canonical**: spawn agent with new spawn template, have it produce `### Peer Verification: X verifying Y` header — verify chain-evaluator _PEER_VERIFY_HEADER regex matches
6. **A12 24h grace**: create archive_file_found=false workspace, verify A12 does NOT fail if archive-created < 24h ago (grace-window applies); verify A12 DOES fail if archive missing for >24h
7. **§2i precision gate WARN**: write workspace finding with `>70% confidence` tag and no driver breakdown — verify chain-evaluator A20 emits WARN + CAL-EMIT line; verify no BLOCK (path β+ WARN-first)
8. **#21 premise-audit**: run c1-plan.md Step 7a through a real build — verify `## premise-audit-results` section populated before agent spawn; verify chain-evaluator presence check blocks on missing section (BLOCK day-one)
9. **workspace atomic Python replace**: run multi-agent session with concurrent writes — verify no anchor-not-found failures; verify section-isolation convention prevents collisions
10. **audit-calibration-gate.py**: after 3+ sessions with §2i fires, run `python3 ~/.claude/teams/sigma-review/shared/audit-calibration-gate.py` — verify output is PROMOTE/RECALIBRATE/CALIBRATING with empirical justification
11. **R19 regression**: re-run the 2026-04-22 ai-agent-rollout-playbook-vet review against new infrastructure — verify none of the R19 issues manifest again (sed-i corruption, XVERIFY-FAIL, A12 timing, etc.)
12. **Test suite regression**: run `python3 -m pytest` against entire test surface — verify 81-currently-passing baseline PLUS 30-46 new tests all pass, 11 pre-existing failures resolved by SQ[0] fixture fix

## C2 pre-requisites (must resolve before implementation begins)
- Test baseline reconciliation: TA 154 vs CQA 92 pytest count discrepancy — C2 first task is to establish authoritative count via `git ls-files` + recursive pytest collection from repo root (not per-subdirectory)
- A-check ID coordination locked: A20=precision gate (CDS), A21=unused (user-approved UP[TA-B3] reserves), A22=governance artifact, A23=severity provenance, A24=sigma-verify init pre-flight (renamed from A21 per DA[#11])
- SQ[0] fixture-fix runs BEFORE SQ[3], SQ[13b-c]
- sigma-verify repo (~/Projects/sigma-verify) treated as separate commit scope from sigma-system-overview
- Per user-approved UP[TA-B2]: section-isolation write convention applies to all C2 agent writes to workspace
