# portfolio — projects reviewed

## loan-admin-agent-v2 | 2026-03-12
task: technology opportunities + differentiators for 3P loan admin agent (BSL+PC)
team: product-strategist(generalist) + loan-ops-tech-specialist(specialist) + regulatory-licensing-specialist(specialist) + devils-advocate
rounds: r1(independent) → r2(DA challenge, 10 challenges, 80% held) → exit-gate PASS
key-findings: waterfall-engine moat (3 distinct types), phased Loan-IQ strategy (<50=license/≥50=own/≥100=migrate), NH-NDTC charter path (GLAS precedent), credit-cycle bear case ($28-47M integrated cost), AI-regulatory language precision (ML+NLP ¬"AI"), 12-18mo gross window (0-6mo net)
promotions: 29 total (19 auto + 10 user-approved)
v1-comparison: specialist team produced sharper operational depth, 3 genuine divergences (vs v1 zero-dissent), DA engaged at B+ with substantive challenges
note: v2 trial — first use of loan-ops-tech-specialist dynamic agent

## 2026-04-22 — AI Agent Rollout Playbook Vet (financial services + B2B SaaS)

- mode: ANALYZE, tier TIER-3 (20/25)
- agents: tech-architect, security-specialist, regulatory-licensing-specialist, regulatory-analyst, reference-class-analyst, tech-industry-analyst, cognitive-decision-scientist + devils-advocate
- rounds: r1 (research + peer-verify) + r2 (DA adversarial)
- DA verdict: PASS (engagement A-average, 19A+1A-)
- structural debates: 1 resolved (severity calibration → graduated MEDIUM/HIGH-conditional via 3-provider XVERIFY)
- findings: 65 agent findings across 7 domains + DA's 8 challenges; 44 auto + 24 user-approve promoted to global memory
- subjects: /Users/bjgilbert/Downloads/ai_agent_roadmap_v2.md + addendum; /Users/bjgilbert/Downloads/ai_agent_playbook_b2b_saas.md + addendum
- synthesis: ~/.claude/teams/sigma-review/shared/archive/2026-04-22-ai-agent-rollout-playbook-vet-synthesis.md (417 lines)
- archive: ~/.claude/teams/sigma-review/shared/archive/2026-04-22-ai-agent-rollout-playbook-vet.md (2143 lines)
- notable process events: R1 workspace corruption (CDS-2 sed -i truncation) → transparent recovery via re-paste from agent contexts with verbatim attestations; XVERIFY systematic infrastructure gap at agent-context level (5 agents hit it, compensated via DA-context XVERIFY + T1/T2 sourcing); DA correctly caught lead grep-error on TA+CDS response verification (anti-sycophancy working on lead as well as agents)
- recommendation: unified-with-substantive-sector-variants playbook (B2B SaaS phased workbook as primary spine + financial capability-maturity reference appendix + 2 sector annexes); top priorities = regulatory exam-crosswalk appendix + per-tool policy codification as named Phase 2 deliverable + CoT unfaithfulness warning in SaaS doc + AI Risk Committee design-gap interventions + numerical thresholds on tier gates

## 2026-04-23 — r19-remediation (sigma-build TIER-3 infrastructure remediation)

- mode: BUILD, tier TIER-3 (score 19)
- C1 plan-locked: 2026-04-23 (P=0.88, DA grade A-, 12 ADRs, 9 ICs, 30 SQs, 10 PMs)
- C2 built: 2026-04-24 (240/240 canonical + 300/300 sigma-verify, +80 net new tests, 0 regressions, 41 files modified across sigma-system-overview + sigma-verify, 32 SQs all DONE)
- C3 reviewed: 2026-04-25 + close-out 2026-04-27, 3 review rounds (r1 FAIL grade B → r2 PASS grade A- → r3 PASS grade A)
- agents: tech-architect, security-specialist, cognitive-decision-scientist (plan-track) + implementation-engineer, technical-writer, code-quality-analyst (build-track) + devils-advocate (cold-read)
- final belief: P=0.89 (Step 9 exit-gate PASS)
- BUILD rubric: 24/24 across 6 dimensions (correctness/test-coverage/maintainability/performance/security/api-design)
- final test state: 247/247 canonical + 300/300 sigma-verify, zero regressions across 3 rounds (240→246→247)
- DA challenges: 14 total (13 r1 + 0 r2 PASS + 1 r3 LOW spot-check); 10 shipped, 3 defended-as-correct, 1 deferred-to-future-build
- key-findings: A24 silent-skip from C1 plan-completeness gap (LOCKED in 5 places, never assigned to any SQ — 4 structural fix candidates promoted); multi-layer-contract-drift pattern (4 instances same class — BLOCK 3→4 doc / pipe-escape / A24 VALID_GATES / §-enumeration); template-vs-instance drift via recursive-self-reference (TW used prior propagations as canonical; corrected via R3-2 hash-identity invariant); β+ WARN-first calibration mechanism (A20/A22/A23/A24 with CAL-EMIT schema + audit-calibration-gate.py); workspace_write helper IC[6] hardened in production (67 successful writes, 0 anchor failures)
- promotions: 49 total (31 auto + 18 user-approved); 1 classification adjudication decision logged
- structural deliverables: chain-evaluator A12 grace + A3 DB extraction + A20/A22/A23/A24 WARN+CAL-EMIT; phase-gate sed-i BLOCK 4 + shlex.split tokenization + xargs stdin KNOWN LIMITATION; sigma-verify machine.py auto-ready probe + IC[8] forward-contract docstring; workspace_write() helper per IC[6]; gate_checks DA-filter plan-amendment; 30 SAFETY-CRITICAL agents + _template hash-identical; directives §2i + §2j + §2d + §2p + §8e; audit-calibration-gate.py standalone; calibration-log.md append-only telemetry; ## premise-audit-results template + Step 7a HARD GATE
- bonus: 13 historical A24 records recovered as live telemetry from r3 VALID_GATES fix (silent malformed-bucket pre-fix; visible-and-aggregated post-fix)
- synthesis: ~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md (327 lines, 7 sections)
- plan file: ~/.claude/teams/sigma-review/shared/builds/2026-04-23-r19-remediation.plan.md
- wiki additions: 4 new pages (sigma-build-infrastructure-architecture, beta-plus-calibration-pattern, workspace-write-contract, premise-audit-step-7a) all with [B-r19-remediation, 26.4.27] attribution
- notable process events: A24 silent-skip caught in r1 by DA cold-read (plan ## Files entry without SQ owner + TW punt-instead-of-flag at C2 c2-scratch:409); user ruled "if plan is locked, it should be executed completely, a skip is a massive failure"; CDS r2 caught A24 VALID_GATES consumer-mismatch that DA's r2 narrower review missed (specialist + general DA both needed); CQA→TW peer-verify SHA-128 hash check found 29-agent vs _template canonical drift (TW resync via R3-2); TW BUILD-CONCERN[tw-r2] correctly flagged 5 sigma-optimize agents missing sed-i ban (user ratified scope expansion); IE refusal+flag against task-list-teammate auto-router misroute at session start; SS explicit anti-sycophancy bias-check + bonus end-to-end A24 wiring trace; user design discussion ruled duplication preserves rule-following safety over reference-pattern (sync script over generator)
- top deferred items: 5 LOW (xargs framing minor, IC[7-9] namespace, A24 docstring attribution, A24 §-enumeration in directives.md, _XVERIFY_ANY_RE over-suppression) + 1 cosmetic (A24 no-Condition-1-suppression docstring note) + 4 structural fix candidates from A24 silent-skip post-mortem (C1 plan-completeness check + C2 boot validation + TW agent-def update + C2 exit-gate diff) + chain-evaluator A25 template-drift detection

## 2026-04-28 — shared-process-hardening (sigma-build TIER-2 process-hardening bundle)

- mode: BUILD, tier TIER-2 (score 16/25)
- C1 plan-locked: 2026-04-28 (P=0.88, DA grade B+ CONDITIONAL-PASS r1 → effective PASS post-fix, 10 ADRs, 8 ICs, 12 SQs, 9 PMs)
- C2 built: 2026-04-29 (1245/14/1 hook-suite + 207/207 chain+phase-gate, +103 net new tests, 0 regressions, 12 SQs all DONE; sigma-audit GREEN; sigma-evaluate r1 C / 2.57 then r2 C+ / 2.71)
- C3 reviewed: 2026-05-01 + close-out 2026-05-02; 2 review rounds (r1 PASS + r2 + r2-micro for two close-out events) — round 1 P=0.92, then 0.88 post-event-1, then 0.91 post-R2 close
- agents: tech-architect (plan-track) + implementation-engineer + technical-writer + code-quality-analyst (build-track) + devils-advocate (cold-read); plan-track set excluded product-designer + product-strategist (no UI scope, no priority disputes)
- final belief: P=0.91 (Step 9 exit-gate PASS post-R2-close)
- BUILD rubric (post-R2): 22/24 = 3.67/4.0 (correctness=4 test-coverage=3 maintainability=4 performance=4 security=3 api-design=4); meets ≥A target (≥3.5/4.0); beats R18+R19 recurring B 3.14 weakness profile
- final test state (post-R2): 1253/14/1 hook-suite (+8 new C3 tests for BLOCK 5 multi-path + cross-build authorization); zero new regressions; pre-existing test_existing_settings_preserved unchanged (out of scope per c3-separate-maintenance)
- DA challenges: 9 r1 (1 HIGH 4 MED 4 LOW); 6 concede/fix + 3 accept-with-documentation
- key findings: GATE-1 manual-override actor authority = lead-with-user-approval (quad-convergence DA + TA + openai gpt-5.4 + TW); F[IE-6] empirical-claim RESTATE not RETRACT (triple-convergence DA + TA + CQA); 2 close-out events surfaced and closed in-build via R2 + R2-micro (BLOCK-5 sequencing trap + cross-build authorization bypass via broad-glob fallback)
- promotions: 21 auto-landed (DA 2 + TA 5 patterns + 1 decision + IE 5 patterns + 1 decision + TW 3 patterns + CQA 6 patterns) + 19 user-approved (DA 8 + TW 4 + CQA 1 + IE 3 + retroactive approval of DA's 2 pre-flap entries) = 40 total promotion-events; 1 cross-agent classification disagreement resolved (cleanup-pass-precedence via DA's concession to TW's diverging-classification flag)
- structural deliverables: chain-evaluator A26 plan-completeness + B5 C2 boot + B6 C2 exit-gate diff + A14 race fix wrapper + A25 template-drift + _XVERIFY_ANY_RE bracket-required + ADR[9] universal edge-case helpers; phase-gate BLOCK 5 06b pre-archive (multi-path scan post-R2 with cross-build authorization short-circuit, BUILDS_DIR + 7d freshness window, ADR[6]/IC[6]); directives §8f BUILD variant manual-override with 3-precondition criterion; sigma-lead.md:207 wording update (operator may unblock → lead may invoke only with explicit user approval); sigma-review/SKILL.md + sigma-lead.md Step 1 premise-audit pre-dispatch sub-step (mirrors c1-plan.md:62 Step 7a HARD GATE); technical-writer.md ## Gap-Handling Rules section; sync-templates.sh + hash-identity utility; 103 + 8 net new tests
- synthesis: ~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-synthesis.md (43,838 bytes, 9 sections)
- plan file: ~/.claude/teams/sigma-review/shared/builds/2026-04-28-shared-process-hardening.plan.md
- wiki additions: 1 new page (directive-hook-integration-pattern.md) + 4 existing pages updated (sigma-build-infrastructure-architecture, premise-audit-step-7a, beta-plus-calibration-pattern, cross-model-protocol-calibration); all with [R-2026-04-28-shared-process-hardening, 26.5.2] attribution
- notable process events: synthesis-agent halted twice on phase-gate BLOCK 5 during close-out (sequencing trap + workspace-path defect; user authorized manual-override + R2 in-build fix); TA CONCERN-1 cross-build authorization bypass via R2 broad-glob fallback (closed via R2-micro 5-line short-circuit); IE pre-emptive calibration disclosure on R2 empirical methodology (omitted hook_event_name); MCP store_*-flap mid-promotion-round caught silently elevated DA autos — DA conceded TW's diverging-classification flag, exemplifying user-approval-gate-non-bypassable; IE workspace-contention refusal-and-flag; 2 directive↔hook integration defects shipped + caught only by gate-halt during close-out (not by test design)
- top deferred items: 5 R2 follow-up gaps for next build (CQA-surfaced GAP-D HIGH `_strip_fenced_blocks` parity in phase-gate.py + GAP-A/B/C edge-case test coverage + GAP-E trailing-WS regex anchor + CONCERN-2 LOW suffix-stripper extension); 4 ranked options for synthesis-precedes-compilation sequencing trap; DA[#4] Bash regex + MultiEdit/NotebookEdit dispatch gap (NEW); GAP[#2] _path_is_archive substring-match bypass; DA[#9] stale-line-number lint rule; DA[#6] §2d source-type enum extension; pre-existing test_existing_settings_preserved
- meta-pattern surfaced: directive↔hook integration co-test rule (wiki page directive-hook-integration-pattern.md) — directives that name recovery paths must be co-tested with the hooks that enforce the gates they recover from
