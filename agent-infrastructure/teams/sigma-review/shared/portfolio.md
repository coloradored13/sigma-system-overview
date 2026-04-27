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
