# sigma-build plan: shared-process-hardening

## Meta
- created: 2026-04-28
- locked: 2026-04-28
- build-id: 2026-04-28-shared-process-hardening
- tier: BUILD TIER-2 (score 16/25)
- status: plan-locked
- plan-exit-gate: PASS (DA effective PASS post-fix)
- plan-belief: P=0.88
- plan-da-grade: B+ CONDITIONAL-PASS r1 with all 4 BLOCKING resolved → effective PASS
- post-c1-audit-verdict: **YELLOW** (11 PASS / 3 PARTIAL / 1 FAIL of 15 rows). FAIL = K (XVERIFY criterion-9 single-provider routing — sigma-verify infrastructure 2-build pattern; recovery option-c: defer XVERIFY redo to C2 build-track on load-bearing implementation findings). 3 PARTIALs (LOW): B H[] presentation merge, C dual-test-SQ doc gap (now addressed below), G PM-track plan-vs-build distinction (directive-update candidate).
- audit-flags-recurring: :K sigma-verify infra 2-build P0; :promotion-gate auto-vs-user-approve same-session recurrence (pre-shutdown hook gap); :gate-log-prose-parsing schema needed
- audit-disclosure-status: gate-log entry written to scratch ## gate-log "post-C1 sigma-audit verdict" section. C1 truly-closed status conditional on user accepting recovery option-c; alternatives (a) re-run XVERIFY now or (b) accept gap as documented.
- build-exit-gate: PENDING
- build-belief: P=0.00
- output-label: P2.A 10-item shared process-hardening bundle (sigma-build c1/c2 mechanics + shared chain-evaluator/workspace conventions + sigma-review workflow placement)
- source-plan: ~/.claude/plans/which-of-the-suggestions-mellow-anchor.md (P2.A)
- scratch: ~/.claude/teams/sigma-review/shared/builds/2026-04-28-shared-process-hardening/c1-scratch.md (status: archived-c1)
- archive: ~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-c1-workspace.md
- quality-targets: GREEN sigma-audit + A sigma-evaluate (≥3.5/4.0) — beats recurring B 3.14 weakness profile from R18+R19. P3.1-P3.5 corrections active across C1+C2+C3.

## Context

P2.A from the merged closeout-and-enforcement plan: 10 process-hardening items spanning sigma-build c1/c2 mechanics (4 items), shared chain-evaluator + workspace conventions (5 items), and one sigma-review-specific workflow placement (item 10). Originally framed as "sigma-build-process-hardening" before 2026-04-28 sigma-review coverage audit revealed 5 of 9 items affect sigma-review via shared chain-evaluator and one sigma-review-specific gap (item 10) was missing. Items 8-9 added from sigma-audit re-audit of 26.4.22 archive (verdict GREEN). Item 10 added to close R19 #21 premise-audit Step 7a placement gap.

**Why now**: per source-plan §P3, this build mechanizes lead-side discipline that produced the recurring B 3.14 weakness profile in R18+R19 sigma-evaluate runs. P3.3 (operationalize-before-naming) directly addresses Logic + Completeness + Calibration + Actionability which all scored 3/4 in both prior evaluations. P2.D verdict-citation enforcement is sequenced AFTER this build (chain-evaluator stabilization first).

**A27 mechanical follow-on for item #8 is OUT of scope** (deferred to post-calibration; only the directive ships in this build).

## Prompt Understanding (user-confirmed 2026-04-28)

- **Q[]** (11): Q1 A26 plan-completeness | Q2 B5 C2 boot validation | Q3 TW Gap-Handling Rules | Q4 B6 C2 exit-gate diff | Q5 A14 race fix (exclude calibration-log) | Q6 A25 template-drift detection | Q7 _XVERIFY_ANY_RE regex tightening | Q8 Post-exit-gate workspace-headers directive | Q9 06b compilation pre-archive gate | Q10 Premise-audit Step 7a sigma-review placement | Q11 Tests for all of the above
- **H[]** (7): H1 WARN-first ramp for items 1/2/4/6/8 (path β+) | H2 parser robustness incrementally normalizable (partially falsified at C1 — keyword=value canonical, prose fallback) | H3 B5 boot-prompt format un-standardized (validated; new IC[8] schema created) | H4 A14 race fix has no behavioral side effects (validated wrapper-level only) | H5 item #9 marker vs INDEX scan (resolved → workspace-header) | H6 10 items in one TIER-2 build (user-confirmed) | H7 Step 7a verbatim reuse (partially falsified — label dropped, structure survived)
- **C[]** (10): see archived workspace ## prompt-understanding for full text. Key: C2 A14 race-fix MUST ship before A14 promotion event (out-of-scope); C3 WARN-first default for new BLOCK gates; C4 A27 deferred; C5 P2.D follows P2.A; C6 zero regression on archived workspaces; C10 TeamCreate required, XVERIFY excludes anthropic.

## Premise Audit (Step 7a §2p)

- PA[1] tech-tier-necessity: CONFIRMED (slots into existing chain-evaluator + phase-gate)
- PA[2] scale-floor: CONFIRMED (single-user, ~10-50 hook fires/day, O(1))
- PA[3] data-readiness: **CONFIRMED-IN-SCOPE-CREATION** (existing surfaces + 3 new headers this build CREATES: ## agent-assignments [IC[8]], ## compilation-complete [ADR[6]/IC[6]], ## sync [DC[2]] — re-labeled per DA[#5] r1 P3.1 honesty)
- PA[4] precedent-baseline: RC = R19 (4d/TIER-3) + F1 (1d/TIER-2) → at-base-rate (slight upside risk per +43% scope-creep PM)
- decision: → proceed-with-H

## Scope Boundary

**Implements**: A26 plan-completeness check (chain-evaluator.py, WARN-first); B5 C2 boot validation (chain-evaluator.py, WARN-first at C2 boot transition); B6 C2 exit-gate diff (chain-evaluator.py, WARN-first at C2 status:built; extends gc.check_checkpoint); TW Gap-Handling Rules section (technical-writer.md agent-def); A14 race fix (chain-evaluator.py check_a14 wrapper-level — exclude *calibration-log.md); A25 template-drift detection (chain-evaluator.py + sync-script + hash-identity); _XVERIFY_ANY_RE regex tightening (bracket-only); Post-exit-gate workspace-headers directive (## sync new mandate; ## promotion already gated); 06b compilation pre-archive gate (phase-gate BLOCK 5 via ## compilation-complete: [R-{id}] workspace-header with manual-override recovery form); Premise-audit Step 7a sigma-review placement (sigma-review/SKILL.md + sigma-lead.md, mirrors c1-plan.md:62 structure with "Step 7a" label dropped for ANALYZE side); Tests (extend test_hooks.py + new validator/parser tests + TestArchivedWorkspacePassthrough on 3 real archives).

**Does NOT implement**: A14 WARN→BLOCK promotion event (gated on post-race-fix calibration); A27 mechanical hook for post-exit-gate workspace headers (deferred to post-calibration; directive only); P2.D verdict-citation enforcement on sigma-audit + sigma-evaluate (sequenced AFTER this build); Wiki INDEX restructuring beyond R19 baseline; Any directive/hook for files outside the scope above.

## Architecture Decisions (locked)

| ADR | Decision | Source / Rationale |
|---|---|---|
| ADR[1] | A14 race fix in `check_a14` **wrapper ONLY** (NOT `gc.check_session_end`); wrapper re-runs `git status --porcelain` independently for full untruncated list (cap-at-10 fix) | A12 protection — gc helper shared. \|source: TA + IE BC[IC[1]]\| |
| ADR[2] | New `## agent-assignments` workspace section (NOT `## agents` — H3 understated). Format: `SQ[N]: owner=AGENT \|cluster=FILE,FILE2,...`. Fallback to `## sub-task-decomposition` with explicit zero-parse WARN if neither populated. | TA + CQA BC[Q2] + IE BC[IC[8]] |
| ADR[3] | A26 `## plan-file` header detection regex: anchored `^## plan-file\s*$` (excludes `## plans`, `## plan-file:`, `### plan-file`, fenced blocks) | TA + CQA BC[Q1] |
| ADR[4] | B6 CHECKPOINT parser: keyword=value canonical (per IE finding 2 — R19 c2-scratch is structured), prose fallback for legacy only | TA r2 absorption of IE pre-read |
| ADR[5] | A25 sync-script + hash-identity: LF normalize, BOM strip, rstrip lines before hash. Recovery: re-run script + commit sidecar. | TA + CQA BC[Q6] |
| ADR[6] | 06b pre-archive gate via NEW workspace header `## compilation-complete: [R-{review-id}]` checked by phase-gate BLOCK 5. INDEX scan rejected (coupling). A28 WARN rejected (sequencing-gate semantics favor hard enforcement; concession-strengthens-thesis acknowledged via DB[ADR[6]] v2). Manual-override recovery form: `## compilation-complete: [R-{id}, manual-override, reason: {reason}]`. **plan-faithful** (plan §P2.A row 119 mandates BLOCK; lead F1 framing-inversion was self-corrected via DA[#1]). XVERIFY: openai gpt-5.4 agree-high. | TA + CQA r2 + DA[#1] + DA[#6] |
| ADR[7] | _XVERIFY_ANY_RE: bracket-required form `\bXVERIFY(?:-(?:FAIL\|PARTIAL))?\[` (bracket-only); covers XVERIFY[timeout]/XVERIFY[unavailable] (no colon required); single consumer A24:1021. SQ[7] step 1 = grep-audit. | TA r1 absorption of CQA BC[Q7] + IE BC[IC[7]] |
| ADR[8] | A26+B6 parsers: keyword=value primary, prose fallback for legacy, parse-fail exit. WARN-first calibration. | TA r2 IE-pre-read absorption |
| ADR[9] | IC[8] edge cases: BOM-strip, empty-section→WARN-not-crash, fenced-code-exclusion-before-section-search | TA + CQA r2 MEDIUM-3 |
| ADR[10] | A27 eligibility threshold: ≥3 reviews where `## sync` absent + ≤20% FP per β+ precedent (A20, §2i). NOT "2+" — precedent-aligned. | TW r2 peer-verify + TA reconciliation R1 |

## Interface Contracts (locked)

| IC | Contract | Notes |
|---|---|---|
| IC[1] | A14 race-fix wrapper signature: re-runs `git status --porcelain`, applies `r"calibration-log\.md$"` exclusion (NOT .bak), recomputes git_clean from filtered list; falls back to gc capped list if subprocess fails (with limitation noted) | Wrapper-only per ADR[1] |
| IC[2] | A26 `^## plan-file\s*$` regex anchored, case-sensitive, BOM-aware | Per ADR[3] |
| IC[3] | B5 reads `## agent-assignments`; falls back to `## sub-task-decomposition`; emits explicit zero-parse WARN on schema gap | Per ADR[2] + IE BC[IC[8]] |
| IC[4] | B6 CHECKPOINT parser 3-pass: keyword=value primary → prose fallback → parse-fail | Per ADR[4] |
| IC[5] | A25 sync-script: normalize (LF, strip-BOM, rstrip-lines) → SHA256 → compare baseline → diff on drift | Per ADR[5] |
| IC[6] | 06b pre-archive header detection: `^## compilation-complete: \[R-([^,\]]+)(?:, manual-override, reason: ([^\]]+))?\]$`; phase-gate accepts both standard and manual-override forms; BLOCK message includes recovery instructions; stale-workspace FP guard via `_is_sigma_session()` | Per ADR[6] |
| IC[7] | _XVERIFY_ANY_RE: `r"\bXVERIFY(?:-(?:FAIL\|PARTIAL))?\["` | Per ADR[7]; SQ[7] step 1 = grep-audit before replace |
| IC[8] | `## agent-assignments` schema with edge-case handling (BOM-strip, empty→WARN, fenced-code exclusion) | Per ADR[9] |

## Sub-task Decomposition

| SQ | Task | Owner | Files | Est (80%) |
|---|---|---|---|---|
| SQ[1] | A26 plan-completeness ChainItem (WARN-first) | IE | chain-evaluator.py | 1.0h [0.75, 1.5] |
| SQ[2] | B5 C2 boot validation ChainItem (WARN-first) | IE | chain-evaluator.py | 1.5h [1.0, 2.5] |
| SQ[3] | TW Gap-Handling Rules section (after `## Weight`, before `## Workspace Edit Rules`) | TW | technical-writer.md | 0.5h [0.25, 0.75] |
| SQ[4] | B6 C2 exit-gate diff ChainItem extending gc.check_checkpoint (WARN-first) | IE | chain-evaluator.py | 1.0h [0.75, 2.0] (post-IE-pre-read revision) |
| SQ[5] | A14 race fix in check_a14 wrapper (greenfield clean-add) + tests | IE | chain-evaluator.py + tests/test_chain_evaluator.py | 0.75h [0.5, 1.25] |
| SQ[6] | A25 template-drift ChainItem + sync-templates.sh + hash baseline | IE | chain-evaluator.py + scripts/sync-templates.sh | 1.5h [1.0, 2.5] |
| SQ[7] | _XVERIFY_ANY_RE regex replace (step 1 = grep-audit; step 2 = replace; step 3 = test) | IE | chain-evaluator.py + test_chain_evaluator.py TestA24 | 0.75h [0.5, 1.25] |
| SQ[8] | §8f post-exit-gate workspace-headers directive (## sync mandate; ## promotion already gated cross-ref) + DC[3] §2p ANALYZE cross-ref | TW | directives.md | 0.5h [0.25, 0.75] |
| SQ[9] | 06b pre-archive phase-gate BLOCK 5 + compilation-agent prompt update at sigma-lead.md:176 (single-owner per B1 option-i) | IE | phase-gate.py + agents/sigma-lead.md (lines ~176) + tests | 1.5h [1.0, 2.5] |
| SQ[10] | Premise-audit sigma-review placement (¬Step 7a — sub-step of Step 1; grep-audit first per BC[Q10]) | TW | sigma-review/SKILL.md (Step 1 extension) + agents/sigma-lead.md (sub-step) | 1.0h [0.75, 1.5] |
| SQ[11] | TestArchivedWorkspacePassthrough on 3 archives (r19-remediation + 26.4.22 ai-agent-rollout-playbook-vet + sigma-chatroom-m1ab); WARN-only mode for new gates A25/A26/B5/B6 (assert passed=True; log issues count); depends-on SQ[1-10] all merged atomically | CQA | tests/test_archived_workspaces.py | 1.5h [1.0, 2.5] |
| SQ[TW-6] | Directive cross-ref grep-test (verifies "Step 7a" appears only in BUILD contexts after item-10 ANALYZE-side insertion; companion test to SQ[11]) — dual-test-SQ structure documented per audit PARTIAL-C remediation | TW | tests/ (cross-ref grep audit) | 0.25h [0.15, 0.5] |

**Total estimate**: ~11.75h [7.9h, 19.5h] across C2 BUILD execution.

## Pre-mortem (≥3 per §3 BUILD)

- PM[1] (TA): A26+B5+B6 false-positives on archived workspaces silently accumulate, eroding signal — **mitigation**: SQ[11] WARN-only mode + counts-logged + ≥3 archives covered
- PM[2] (TA): SQ[7] _XVERIFY_ANY_RE replacement breaks existing test fixtures — **mitigation**: SQ[7] step 1 grep-audit before replace
- PM[3] (TA): A14 race-fix overly-broad glob accidentally excludes legitimate dirty files — **mitigation**: precise regex `r"calibration-log\.md$"` + .bak non-exclusion test (SQ[5] case d)
- PM[4] (TA): A25 sync-script hash drifts on macOS LF vs Windows CRLF — **mitigation**: normalize before hash (LF, BOM-strip, rstrip)
- PM[5] (TA): item #9 phase-gate.py addition introduces new BLOCK that misfires on non-sigma sessions — **mitigation**: `_is_sigma_session()` guard + manual-override recovery form
- PM[6] (TA): SQ[9] split risks one-of-pair shipping without sibling — **mitigation**: B1 option-i (single-owner consolidation) eliminates split
- PM[7] (TW): directive ambiguity → agent misinterpretation — **mitigation**: paraphrase test in DC review; canonical-wording in gate-log
- PM[8] (TW): workflow-step renumbering breaks cross-refs in directives.md/wiki/agent-defs — **mitigation**: SQ[10] grep-audit step
- PM[9] (TW): ΣComm/plain-English boundary violation in directive content — **mitigation**: sigmacomm skill compliance check at C2 review

(All probabilities are agent-subjective likelihoods, not measured base rates per P3.5.)

## Files

| File | Action | Description |
|---|---|---|
| ~/.claude/hooks/chain-evaluator.py | modify | Add A26, A25, B5, B6; modify check_a14 wrapper; tighten _XVERIFY_ANY_RE; register in ANALYZE_CHAIN/BUILD_EXTRAS |
| ~/.claude/hooks/phase-gate.py | modify | Add BLOCK 5 for 06b pre-archive (item 9) |
| ~/.claude/agents/technical-writer.md | modify | Insert ## Gap-Handling Rules section (after ## Weight, before ## Workspace Edit Rules) |
| ~/.claude/agents/sigma-lead.md | modify | Insert premise-audit pre-dispatch sub-step in Step 1 (mirrors c1-plan.md:62 structure; ¬"Step 7a" label) + update line ~176 compilation-agent spawn instruction (per SQ[9] consolidation) |
| ~/.claude/skills/sigma-review/SKILL.md | modify | Insert workflow Step matching c1-plan.md:62 Step 7a HARD GATE structure |
| ~/.claude/teams/sigma-review/shared/directives.md | modify | (a) §8f post-exit-gate workspace-headers (## sync NEW; ## promotion already gated cross-ref); (b) §2p ANALYZE-mode cross-ref |
| ~/.claude/hooks/tests/test_hooks.py | modify | Extend with end-to-end tests for new chain items |
| ~/.claude/hooks/tests/test_*_new.py | new | Validator unit tests per chain item |
| ~/.claude/hooks/tests/test_archived_workspaces.py | new | TestArchivedWorkspacePassthrough on 3 archives, WARN-only mode |
| ~/Projects/sigma-system-overview/agent-infrastructure/scripts/sync-templates.sh | new | A25 sync-script + hash-identity utility |

## Plan Challenge Summary

- **DA challenges** (round 1): 13 (1 HIGH, 4 MED, 6 LOW, 1 PROMOTION-cand, 1 self-conceded)
- **DA grade**: B+ CONDITIONAL-PASS r1 → effective PASS post-fix (all 4 BLOCKING resolved)
- **Build-track BCs**: CQA 16 (r1=9, r2=7) + IE 8 = 24 total feasibility challenges
- **Lead reconciliations**: 11 (R1-R11) cross-track conflicts resolved before lock
- **Lead self-corrections**: 1 (F1 framing-inversion via DA[#1] anti-sycophancy — plan §P2.A row 119 mandates BLOCK; ADR[6] is plan-faithful)
- **Concessions/Defenses**: TA conceded 7/7 r2 CQA items + 4/4 r1 IE items + 2/2 lead reconciliation requests = 13 concessions; 3 defends-with-revision (BC[Q9] DEFEND, BC[Q11] UPHOLD, B3 DB rerun)
- **CB**: not-needed (zero-dissent never fired — substantive challenges throughout)
- **Unresolved tensions**: none. All 4 r1 BLOCKING resolved. Carry-forwards (DA[#11] CQoT-6/7/8 strengthening on ADR[6] → C2; DA[#12] CQA universal edge-case single-pass → promotion + C2 instructions).
- **Peer-verify ring**: TW↔TA (r1 honest-FAIL + r2 CONDITIONAL-PASS post-population) | IE↔CQA (PASS, both directions) | DA peer-verify N/A by convention.
- **XVERIFY**: TA ADR[6] agree-high (openai gpt-5.4); TW WP[2] PARTIAL¬DISAGREE (openai); DA challenge() reasoning-tier on top-1 returned MED with substantive counter. cross_verify infrastructure flapping documented as INFRASTRUCTURE FOLLOW-UP for sigma-verify maintenance.

## Build Status

(empty — written by C2)

## Build Review Summary

(empty — written by C3)

## Close Status

(empty — written by C3)

## C2 Handoff Notes

- **Quality targets carry-forward**: GREEN audit + A evaluation. P3.1-P3.5 corrections active (see archived workspace ## quality-targets).
- **DA[#11] carry-forward**: TA C2 pre-build pass should strengthen CQoT-6/7/8 on ADR[6] (falsifiability "IF [evidence] THEN [would-reconsider]" reachability; steelman A28-WARN with evidence; confidence-gap obtainable evidence).
- **DA[#12] PROMOTION-CANDIDATE for C2**: CQA r1 should run universal edge-case checklist (empty/BOM/unicode/fenced/trailing-WS) against ALL new ICs in single pass at end of r1 (¬per-gate ad-hoc).
- **B1 option-i consolidation**: SQ[9] is single-owner IE; covers phase-gate.py + agents/sigma-lead.md:176 (~2-3 lines text) + tests. TW reviews sigma-lead.md change via SQ[10] natural review checkpoint.
- **C2 sequencing**: SQ[5] A14 race-fix MUST land before any test that checks "calibration-log only dirty"; SQ[1-10] all merged atomically before SQ[11] begins; SQ[7] step 1 grep-audit before regex replace.
- **Infrastructure follow-up (OUT-OF-SCOPE this build)**: sigma-verify cross_verify reliability + verify_finding provider-routing param not honored. Logged in sigma-mem failures.md as P2 follow-up. NOT a blocker for C2/C3.
- **MCP persistence**: lead persisted 8 patterns + 1 failure to sigma-mem on behalf of all agents at C1 Step 33 due to MCP flapping during build. Each entry tagged `|src:shared-process-hardening-c1-2026-04-28|`. C2/C3 agents should not assume their own persistence will succeed without MCP health check.

## Verification

End-to-end validation per archived workspace + plan §P2.A:
1. **A14 race**: scratch-only `## sync` mandate honored; A14 PASSes when calibration-log.md is the only dirty file (test in SQ[5])
2. **A25 hash drift**: macOS-CRLF cross-platform parity (test in SQ[6])
3. **A26 false-positive**: `## plans` section (real scratch section) does NOT trigger; `## plan-file` does (test in SQ[1])
4. **B5 schema gap**: explicit zero-parse WARN, NOT silent empty (test in SQ[2])
5. **B6 keyword=value canonical**: parses R19 c2-scratch CHECKPOINT format (test in SQ[4])
6. **_XVERIFY_ANY_RE** prose mention does NOT suppress; bracket-form does (test in test_chain_evaluator.py TestA24 per SQ[7])
7. **06b pre-archive**: BLOCK fires when `## compilation-complete: [R-{id}]` absent; manual-override form unblocks; non-sigma-session does NOT trigger (test in SQ[9])
8. **Step 7a sigma-review placement**: chain-evaluator §2p presence-check passes when `## premise-audit-results` written; SKILL.md and sigma-lead.md cross-refs grep clean (test in SQ[10])
9. **Archived-workspace regression**: TestArchivedWorkspacePassthrough on 3 real archives — A1-A24 + B1-B4 still pass; new gates WARN-only with counts logged (test in SQ[11])
10. **TW Gap-Handling**: paraphrase test — agent reading directive raises BUILD-CONCERN on Files-table entry with no owning cluster SQ (manual review in C3)

**Final acceptance**: `python3 ~/.claude/hooks/chain-evaluator.py status` returns CLEAN at C2 status:built and C3 close-out (per c1-plan.md/c2-build.md/c3-review.md exit-gate templates).
