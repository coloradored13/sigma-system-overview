# Loan Administration Agent — Technology Opportunities & Differentiators

## Analysis Bundle | sigma-review v2 Specialist Team | 2026-03-12

---

## 1. About This Document

This document is a complete analysis bundle produced by the **sigma-review** multi-agent team system. The system works as follows:

- **Agents**: Specialized AI analysts with distinct domains of expertise, each maintaining persistent memory across sessions
- **ΣComm**: A compressed notation protocol used for agent-to-agent communication (see §11 for full spec)
- **Expertise-weighted decisions**: Domain experts have primary weight on decisions in their area; others contribute advisory weight
- **Convergence**: Agents independently analyze, then declare convergence (✓) in a shared workspace when findings are complete
- **DA challenges**: A devil's advocate agent stress-tests all findings through structured challenge rounds with severity ratings
- **Dynamic agent creation**: The DA can identify domain gaps and request specialist agents be created mid-review
- **Promotion**: Generalizable learnings are promoted from project-level to global agent memory for use in future reviews

### Key Notation Guide

| Symbol | Meaning |
|--------|---------|
| ✓ | Done/complete |
| ◌ | In progress |
| ! | Blocked or critical |
| ? | Need input |
| ¬ | Explicitly NOT (prevents assumptions) |
| → | Leads to / next action |
| \| | Section separator |
| #N | Item count (checksum) |
| §2a | Positioning/consensus check |
| §2b | Calibration/precedent check |
| §2c | Cost/complexity check |
| F[N] | Finding number N |
| DA[#N] | Devil's advocate challenge N |
| R[] | Research entry |
| C[] | Calibration entry |
| P[] | Pattern entry |
| H/M/L | Severity: High/Medium/Low |

---

## 2. Task Context

> Source: workspace.md ## task + ## context

### Original User Prompt

Analyze the main technology opportunities and differentiators for a third-party loan admin agent in the broadly syndicated and private credit market. Identify what technology capabilities create competitive advantage, what market gaps exist, and what architectural/product decisions matter most for differentiation.

### Domain Context Provided to Agents

- **Broadly syndicated loans (BSL)**: Higher volume, more standardized, LSTA conventions
- **Private credit**: Lower volume, bespoke structures, direct lending, BDCs, fund finance
- **Competitive landscape**: Alter Domus, CSC, Citco, Virtus, GLAS, Kroll, MUFG Loan Partners, Wilmington Trust
- **Key functions**: Waterfall calculations, covenant tracking, investor reporting, agent notices, consent solicitation, amendment processing, borrowing base calculations
- **Market dynamics**: Private credit AUM explosion outpacing admin infrastructure, SOFR transition tail, aging tech stacks at incumbents
- **GLAS**: Independent loan agency provider, NH trust company charter (2016). Oakley Capital backed. Grew $120B to $850B AUA in 4 years. 100+ jurisdictions.
- **Kroll**: Cloud-native loan agency platform. 8-day settlement vs 47-day average. Agency + trustee focus, not full admin.

### Experimental Conditions

This was a **v2 trial** comparing specialist team composition against the v1 generalist team:
- **v1 team**: tech-architect + product-strategist + regulatory-licensing-specialist + devils-advocate (4 rounds, DA-gated)
- **v2 team**: product-strategist (generalist) + loan-ops-tech-specialist (NEW specialist) + regulatory-licensing-specialist (specialist) + devils-advocate (2 rounds, DA-gated)

The hypothesis: domain specialists produce sharper, more operationally grounded analysis than generalists.

---

## 3. Team Roster

> Source: ~/.claude/teams/sigma-review/shared/roster.md

### Active Agents for This Review

| Agent | Type | Domain | Wake Triggers | Rounds Active | Final Grade |
|-------|------|--------|---------------|---------------|-------------|
| product-strategist | Generalist | market, growth, monetization, prioritization | feature decisions, positioning, competitive analysis | r1, r2 | B+ |
| loan-ops-tech-specialist | Specialist (NEW) | waterfall engines, credit agreements, settlement, Loan IQ, payment processing, CLO/BDC ops | loan administration, waterfall calculations, settlement, covenant tracking | r1, r2 | A- |
| regulatory-licensing-specialist | Specialist | trust chartering, loan agent licensing, fiduciary duties, banking regulations, compliance infrastructure | regulatory requirements, licensing, trust company, compliance costs | r1, r2 | A- |
| devils-advocate | Adversarial | bias detection, assumption stress-testing, contrarian analysis, crowding risk | consensus challenge, groupthink, stress test | r2 | N/A (exit-gate controller) |

### Dynamic Agent: loan-ops-tech-specialist

- **Trigger**: Created for v2 trial to provide operational depth that tech-architect (generalist) could not deliver in v1
- **Impact**: Produced genuine operational specificity absent in v1 — waterfall DSL with PIK/shadow default data, settlement benchmarks with LSTA waterfall mechanics, BBC fraud cases, cross-vehicle operational complexity. Most notably, correctly distinguished three types of waterfall calculations (fund distribution ≠ loan admin payment ≠ CLO compliance) — a distinction the v1 generalist team missed entirely.

---

## 4. Review Process Summary

### Round-by-Round

| Round | Focus | Agents Active | Key Outputs |
|-------|-------|---------------|-------------|
| r1 | Independent research | LOT, PS, RLS | 28 findings (LOT:10, PS:10+7v2, RLS:8v1+8v2) |
| r2 | DA challenge round | DA → LOT, PS, RLS | 10 challenges issued, all agents responded, exit-gate PASS |

### DA Challenge Statistics (r2)

| # | Severity | Target Agent | Topic | Verdict |
|---|----------|-------------|-------|---------|
| 1 | HIGH | LOT-F1 | Waterfall dual-mode vs 5+ competitors | **Held-compromise**: claim narrowed to admin payment waterfall |
| 2 | HIGH | PS-F5, LOT-F10 | Incumbent AI accelerating faster than modeled | **Held-compromise**: window compressed to 12-18mo |
| 3 | HIGH | PS-F1, PS-F8, LOT-F5 | Credit cycle stress absent from analysis | **Held-compromise**: bear case added with research backing |
| 4 | HIGH | PS-F2, RLS-F16 | Hypercore threat underscoped | **Held-compromise**: upgraded to Tier-4.5 |
| 5 | MEDIUM | ALL | Zero divergence = herding signal | **Held-compromise**: 2 genuine divergences surfaced |
| 6 | MEDIUM | RLS-F9, F12 | Compliance-native relabeled (v1 correction reversed) | **Held-compromise**: split 2/3 internal, 1/3 external |
| 7 | MEDIUM | ALL | Cost model fragmented across 3 agents | **Conceded**: integrated model produced ($23-37M/$28-47M) |
| 8 | MEDIUM | LOT-F2, F6, PS-F2 | S&P DataXchange platform risk underweighted | **Fell**: S&P defense held (charter-gated functions) |
| 9 | MEDIUM | LOT-F8, PS-F7 | Loan IQ GAP most consequential unresolved | **Held-compromise**: phased hybrid resolved |
| 10 | LOW | Team composition | v2 specialist depth uneven | **Noted** |

**Challenge held ratio**: 8/10 (80%) — high ratio indicates genuine r1 analytical gaps, not DA overperformance.

### Convergence Trajectory

- r1: 28 findings, 0 disagreements across 3 agents = HIGH herding signal (repeat of v1 pattern)
- r2: DA issued 10 challenges → 2 genuine divergences surfaced (build sequence + breakeven timeline), 4 major gaps resolved (cost model, Loan IQ, credit stress, Hypercore charter), 1 correction held (compliance split)
- Exit-gate: **PASS** — synthesis authorized

### Agent Grades Across Rounds

| Agent | r1 | r2 (post-DA response) |
|-------|----|-----------------------|
| loan-ops-tech-specialist | B+ | A- (best defense: waterfall type distinction) |
| product-strategist | B | B+ (owned confirmation bias, cost model produced) |
| regulatory-licensing-specialist | A- | A- (maintained; charter surge research, KYC precedents, breakeven dissent) |

---

## 5. Synthesis Report

*This section is written in plain English for human readers. No ΣComm notation.*

### Executive Summary

A third-party loan administration agent targeting the broadly syndicated and private credit market represents a viable but capital-intensive opportunity. The analysis identified genuine technology differentiators (loan-admin payment waterfall, integrated AI workflows, cross-vehicle operations), a credible regulatory path (NH nondepository trust company charter), and a compressed competitive window (12-18 months gross, 0-6 months net of regulatory setup). The market is entering a consolidation phase with 5 major moves in Q1 2026 alone. A specialist team review produced sharper operational depth than the prior generalist review, with 3 genuine divergences surfaced versus zero in v1.

### Market Opportunity

| Metric | Value | Source |
|--------|-------|--------|
| Private credit AUM (2026) | $2T+ (AIMA: $3.5T already) | AIMA, Morgan Stanley |
| Private credit AUM (2029-2030) | $4-5T | Morgan Stanley |
| BDC nontraded (today) | $200B (from zero since 2021) | Industry data |
| BDC nontraded (2030) | $1T | Morgan Stanley IM |
| Pure agency market (2024) | $1.45B | Intel Market Research |
| Pure agency market (2032) | $2.19B (6.4% CAGR) | Intel Market Research |
| Addressable mid-market (base) | $150-300M | Team estimate |
| Addressable mid-market (bear) | $100-200M | Team estimate (stress scenario) |
| BDC capital formation trend | -40% YoY (2026 forecast) | RA Stanger |
| BDC sales Jan 2026 | $3.2B (-49% from Mar 2025 peak) | InvestmentNews |

The market exhibits a structural tension: secular growth in private credit AUM (which survived the GFC and COVID) combined with cyclical stress in BDC capital formation. This creates a pipeline mix shift — fewer greenfield mandates (40% → 15-20%) but more successor and restructuring opportunities (combined 60-80% in bear case).

### Technology Differentiators — What IS and IS NOT a Differentiator

**IS a differentiator (pressure-tested, post-DA):**

1. **Loan admin payment waterfall** — The priority-of-application waterfall (fees → interest → principal → default interest → protective advances, with pro-rata syndicate sharing) is a distinct calculation type from fund distribution waterfalls (PE carry/promote/hurdle) and CLO compliance waterfalls (OC/IC, sequential tranche). The DA identified 5+ waterfall platform competitors; the loan-ops-tech-specialist correctly demonstrated all serve fund distribution or CLO compliance, not loan admin payment allocation. No platform spans all three types.

2. **Integrated AI workflow** — Extraction of credit agreement data directly into operational system configuration (waterfall rules, covenant parameters, payment schedules) rather than standalone document parsing. Standalone parsing is commodity with 6+ competitors shipping. The differentiation is the closed loop: extract → configure → monitor → alert → report, all on a purpose-built core.

3. **Cross-vehicle modular architecture** — CLO (rules-based waterfall), BDC (SEC quarterly valuation under ASC 820), and evergreen (continuous NAV calculation) each require fundamentally different operational models. No competitor has a modular vehicle-specific architecture. Phased build: CLO/BSL first (standardized, volume) → PC/BDC (bespoke, growing) → evergreen (smallest, highest complexity).

4. **Charter-gated fiduciary functions** — Payment waterfall distribution, trade settlement and processing, borrowing base monitoring, collateral management, and consent solicitation execution all require trust charter or fiduciary capacity. S&P's DataXchange and AmendX explicitly serve agents (confirmed by press release: "centralized platform for agents to deliver notices to lenders") — they cannot replace agents.

**IS NOT a differentiator:**

1. **AI document parsing** — Table stakes by end of 2026. Six or more competitors already shipping: S&P DataXchange, AD domusAI, Allvue Andi, Hypercore, timveroOS, Kroll Decision Intelligence. Window is closed.

2. **Compliance-by-design as external competitive advantage** — Emerging best practice across all fintech, not unique to loan admin. Only 1/3 of the claimed mechanisms is truly external (KYC-as-service, validated by 5 precedent firms: CSC, Apex, Vistra, Kroll, Eastern Point Trust). The other 2/3 (faster onboarding, better exam scores) is internal operational efficiency worth $50-100K/yr in savings.

3. **Settlement speed alone** — Kroll already achieves 8-day average versus 47-day industry average. Must be combined with full admin capabilities (waterfall, covenant, reporting) that Kroll does not offer.

4. **Data flywheel at zero AUA** — Incumbents have 1,000x more data. Network effects become meaningful only above $50B+ AUA, which takes 3-5+ years. Do not claim data moats pre-scale.

### Revised Competitive Moat (Ordered by Durability)

1. **Trust charter + regulatory standing** — 18-24 month temporary advantage that converts to permanent lock-in via 3-7 year facility lifecycles and relationship accumulation. GLAS proof point: NH NDTC (2016) enabled independent growth from $120B to $850B AUA.

2. **Law firm referral network** — 2-3 year build, self-reinforcing once established. Law firms select the agent in 60%+ of private credit deals during credit agreement drafting. GLAS achieves 40% organic growth through referrals.

3. **PE sponsor relationships** — SRS Acquiom model: 88% of business from PE channel. Requires dedicated BD team of 2-4 people minimum.

4. **Operational track record** — Settlement speed, zero-miss rate on payments, clean audit history. Takes 12-24 months to establish.

5. **AI-native architecture** — 12-18 months before incumbents match on core admin ops (document processing window already closed; analytics 6-12 months; core admin ops 18-24 months due to legacy integration debt as binding constraint). Temporary advantage only.

### Competitive Landscape

| Competitor | Scale | Key Strength | Key Weakness | Likely Response |
|-----------|-------|-------------|-------------|-----------------|
| Alter Domus | $2.5T AUA, $5.3B EV | Scale leader, Agency360, domusAI in production | Integration debt from 6 acquisitions, Vega = presentation layer consolidation | Bain-backed AI investment, "good enough" response by end-2027 |
| GLAS | $750B+ AUA, $1.35B valuation | 40% organic growth, Oakley+LaCaisse backing | AI strategy announced but no product shipped (confirmed Mar 2026) | M&A expansion (LAS Italy Jan 2026), technology investment |
| Kroll | #3 Bloomberg agent | 8-day settlement, cloud-native platform | Agency + trustee only, not full admin | APAC expansion (Madison Pacific), AI (Decision Intelligence Jan 2026) |
| Hypercore | $20B AUM, $13.5M Series A | "AI Admin Agent", 12-18mo head start, SOC2, 3.5x CARR | No trust charter (SaaS ceiling), $2M avg deal ≠ mid-market BDC, 20 employees | Charter acquisition possible via Insight ($5-20M, 9-18mo) |
| S&P Global | DataXchange + AmendX | Free for lenders, zero adoption friction, AI categorization | Data/workflow layer only, cannot provide fiduciary functions | Commoditize non-charter-gated workflows |
| Wilmington Trust | M&T Bank subsidiary | CLO trustee, parent balance sheet self-insurance | Bank legacy, conflict of interest | Automation for reporting, LME processing |
| Versana | $5T+ notional, bank consortium | Real-time BSL data, cashless roll (JPM Oct 2025) | BSL only, no private credit coverage | Expanding digital infrastructure, CEI standard |

### Regulatory Path

**Recommended approach**: NH Nondepository Trust Company (NDTC)

**Precedent**: GLAS obtained NH NDTC in 2016 and grew to $850B AUA. Crypto.com received OCC conditional approval in 5 months (Oct 2025 application). 11 companies received OCC charter approvals in 83 days in 2025 — most favorable charter environment in a decade.

**Why charter is a multi-solving instrument**: A single trust company charter simultaneously solves (a) TIA §310 trustee eligibility, (b) CSBS MTMA payment processing exemption across 31 states covering 99% of money transmission activity, (c) regulatory moat against fast-followers, and (d) institutional credibility requirement. Cost per problem solved: ~$350K.

**Critical insight**: Conditional charter ≠ operational readiness. There is a 12-18 month gap post-approval for AML program buildout, BSA officer hiring, board composition, insurance placement, trust account setup, and first examiner readiness. Charter approval represents only 30-40% of the total regulatory timeline.

| Phase | Jurisdiction | Cost | Timeline | Enablement |
|-------|-------------|------|----------|------------|
| 1 | NH NDTC | $1.25M + $5K app fee | 4-6 months | US operations, TIA §310 trustee |
| 2 | UK FCA | $100-300K | 6-12 months | English law (40-50% cross-border BSL) |
| 3 | EU selective (DE BaFin + LU CSSF) | $150-300K each | 6-18 months | Fund finance, continental BSL |
| 4 | APAC (SG MAS, HK TCSP, AU ASIC) | Variable | Not until $200B+ AUA | Not priority |
| **Total 4-phase** | | **$1.5-3M over 4 years** | | Phase 1 = 67% of cost |

**CRD6 status**: Loan agency/trustee is likely outside "core banking" scope (lending + deposits + guarantees only), supported by 5 major law firms (Mayer Brown, DLA Piper, Norton Rose, Hogan Lovells, BCLP). Confidence: MEDIUM-HIGH. Grandfathering for pre-July 2026 contracts provides buffer.

### Unit Economics

| Metric | Base Case | Bear Case (defaults 5-8%, BDC launches -50%) |
|--------|-----------|-----------------------------------------------|
| Agency fees per facility | $15-75K/yr (BSL lower, PC higher) | Same range, higher avg (distress complexity) |
| Target portfolio for $5M ARR | 140 facilities @ $35K avg | 190-364 facilities |
| Breakeven month | 30-42 (PS estimate) / 36-48 (RLS estimate) | 36-54 |
| Initial gross margin | 46% (service-heavy) | 46% |
| 24-36 month gross margin | 56-61% (AI automation reduces ops headcount) | 50-55% |
| Aspirational gross margin (48-60mo) | 70% (LOW confidence) | Uncertain |
| Series A | $15-20M | $15-20M |
| Series B (month 18-24) | $10-20M | $10-20M |
| Bear case Series C | Not needed | $5-10M |
| Total to breakeven | $23-37M | $28-47M |

**Note on breakeven disagreement**: The product strategist models 30-42 months; the regulatory licensing specialist models 36-48 months. The difference is scope — PS excludes regulatory operations ($1-2.5M/yr), charter expansion ($1.5-3M/4yr), and distribution build ($3-5M/yr) from burn calculations. The all-in burn is $9.5-18.2M/yr, requiring 190-364 facilities at $5M ARR. GLAS took 4 years to reach hundreds of facilities. This is a material disagreement for the fundraising narrative.

### 3-Year Integrated Cost Model

| Component | Year 1 | Year 2 | Year 3 |
|-----------|--------|--------|--------|
| Technology | $2.5-4M | $2-3M | $2-3.5M |
| Charter/regulatory | $1.5-2.5M | $1-2M | $1.1-2.3M |
| Insurance | $25-80K | $40-150K | $100-400K |
| Distribution | $1-1.5M | $2-3M | $2.5-3.5M |
| Operations | $1-1.5M | $1.5-2.5M | $2-3M |
| RegTech/compliance | $200-400K | — | — |
| G&A | $500K-1M | $750K-1.25M | $1-1.5M |
| **Total (base)** | **$6.7-11M** | **$7.4-12.2M** | **$8.85-14M** |
| **Total (bear +15-20%)** | **$7.7-12.7M** | **$8.9-14.6M** | **$10.6-16.8M** |
| Revenue (base) | $0-250K | $1-2.5M | $3-5M |
| Revenue (bear) | $0-100K | $500K-1.5M | $1.5-3M |

**Cumulative base**: $23-37M spend, $4-7.75M revenue, net burn $15.5-33.2M
**Cumulative bear**: $27.2-44.1M spend, $2-4.6M revenue, net burn $22.6-42.1M

### Build Sequence

| Phase | Timeline | Focus | Key Milestones | Burn |
|-------|----------|-------|----------------|------|
| P1 | Mo 0-12 | Charter + MVP waterfall + accruals + notices | NH charter (mo 4-6), first mandate (mo 12-15), SOC2 Type II initiated | $6.7-11M |
| P2 | Mo 12-24 | Settlement + BBC + amendment + own core begins at ≥50 facilities | UK FCA (mo 12-24), Series B (mo 18-24), Loan IQ migration begins | $7.4-12.2M |
| P3 | Mo 24-36 | Full own core at ≥100 + BSL entry with insurance tower | EU selective, BSL mandates with $50-250M insurance tower | $8.85-14M |

**Build sequence resolution**: The product strategist advocated distribution-first with minimum viable waterfall; the loan-ops-tech-specialist advocated waterfall-first (calculation error = legal liability = existential). Resolution: staggered concurrent — MVP waterfall build starts month 0 ($3-5M), distribution BD hiring starts month 3-6. Not either/or. Law firms will not refer an agent who cannot calculate on day 1 (GP criteria: 72% weight "timely accurate reporting"). GLAS built working operations before scaling.

**Loan IQ strategy**: Phased hybrid — license existing platforms (Allvue for CLO compliance, Cardo AI for covenant) at <50 facilities while building proprietary payment waterfall from day 1. Begin own core migration at ≥50 facilities. Full own core at ≥100 facilities. No third-party has ever built a Loan IQ alternative — phased approach manages this unprecedented risk.

### Key Risks and Blind Spots

1. **Credit cycle stress** — Private credit defaults at record 9.2% (Fitch 2025). BDC sales down 49% from peak. Pimco warns of "full-blown default cycle." Bear case shifts greenfield pipeline from 40% to 15-20%. Restructuring capability must be built from Phase 1, not treated as afterthought.

2. **Hypercore with charter** — Insight Partners ($90B+ AUM) has the capital to acquire an NH trust company for $5-20M in 9-18 months. Would narrow new entrant's competitive advantage significantly, though SaaS DNA ≠ trust culture (real integration risk) and $2M average deal size ≠ mid-market BDC ($100M-1B).

3. **Fundraising narrative challenge** — 46% gross margin positions as managed services (3-5x revenue multiple), not SaaS (10-15x). Growth VC pitch weakened by BDC decline. Must position as "countercyclical infrastructure" for PE/infrastructure investors. GLAS's $1.35B Oakley deal in Q1 2026 stress validates PE appetite.

4. **Insurance gaps in hard market** — Excess layer coverage ($25-100M) may be unavailable for 12-18 months during credit stress, creating a deal ceiling compression from $500M to $250M. E&O claims up 57% per decade. Underwriting tightening with bankruptcy exclusions emerging (AmWins 2026).

5. **Adjacent platform risk** — S&P DataXchange (free for lenders) commoditizes non-fiduciary notice management and amendment workflows. Versana digitizes BSL data with zero adoption friction (every lender already uses LCD). Both are infrastructure to integrate, not compete against.

6. **Breakeven disagreement** — Product strategist: 30-42 months. Regulatory specialist: 36-48 months. Difference is $4.6-8.1M in regulatory costs excluded from the PS model. Material for fundraising and runway planning.

7. **Build sequence tension** — Resolved as staggered concurrent, but "minimum viable waterfall" for PC deals remains undefined. This definition gates capital allocation of $3-5M.

### Recommended Next Actions

1. **Begin NH NDTC charter application immediately** — Every month of delay = $500K-1M in lost pipeline. Charter environment is most favorable in a decade (11 approvals in 83 days, 20 filings in 2025 = all-time high).

2. **Define "minimum viable waterfall" for private credit deals** — Resolves the PS/LOT build sequence disagreement. Must include: payment priority-of-application, interest/fee accrual (day-count, SOFR), notice generation and distribution.

3. **Model integrated bear case for fundraising deck** — Use researched data: RA Stanger 40% BDC decline, Fitch 9.2% defaults, Pimco "full-blown default cycle," Blackstone $3.7B redemptions. Position as countercyclical infrastructure.

4. **Monitor Hypercore charter activity** — Watch Insight Partners M&A patterns, NH Banking Department filings, and any trust company acquisition announcements.

5. **Hire 2-4 ex-law-firm BD personnel** — Target Latham, Kirkland, and Paul Weiss (top 3 private credit firms). Use systematic CRM approach (GLAS uses Insightly). Budget $800K-1.5M/yr for channel build.

6. **License Allvue (CLO compliance) + Cardo AI (covenant) for <50 facility phase** — Build proprietary payment waterfall from day 1. This is the one function no platform provides and it is existential for credibility.

7. **Integrate S&P DataXchange and Versana as infrastructure partners** — DataXchange handles notice distribution; Versana provides BSL data. Both strengthen chartered agent position.

8. **Build restructuring/workout capability from Phase 1** — Credit stress increases demand for complex administration (LME, amendments, consent, restructuring). Incumbents will be overwhelmed. Counter-cyclical opportunity.

### Strategic Questions for Decision-Makers

1. Can you fund $25-40M to breakeven, with a realistic bear case extending to $28-47M across Series A + B + potential C?

2. Are you willing to operate as a regulated trust company with fiduciary obligations, examiner relationships, and board governance — fundamentally different from running a SaaS company?

3. What is your Hypercore contingency if Insight Partners acquires a charter within 18 months?

4. Do you have existing relationships at Latham, Kirkland, or Paul Weiss sufficient to generate initial mandates?

5. Is the founding team willing to spend 12-18 months pre-revenue building regulatory infrastructure before administering the first facility?

6. In a credit stress scenario where BDC launches decline 40-50%, can you pivot the fundraising narrative from "ride the growth wave" to "countercyclical infrastructure" and find PE/infrastructure investors rather than growth VCs?

---

## 6. Shared Workspace

> Source: ~/.claude/teams/sigma-review/shared/workspace.md (747 lines)

### Workspace Header

```
# workspace — loan admin agent technology opportunities and differentiators (v2: specialist team)
## status: active
## mode: ANALYZE
## round: r2 (DA-challenges-delivered, awaiting-agent-responses)
## rounds: r1(research),r2(DA-challenge),r3(agent-deepening),r4(second-DA-challenge)
## directives: adversarial-layer v2.0 + dynamic-agent-orchestration v1.0
## team-composition: 1-generalist(PS) + 2-specialists(loan-ops-tech,RLS) + DA | trial: generalist+specialist hybrid
```

### Agent Findings Summary

#### loan-ops-tech-specialist (10 findings)

| Finding | Severity | Topic | §2 Outcome |
|---------|----------|-------|------------|
| F1 | HIGH | Waterfall engine as core differentiator (dual-mode BSL+PC) | §2a: outcome-2 (maintained); §2b: outcome-2; §2c: outcome-2 |
| F2 | HIGH | Credit agreement AI → admin workflow integration | §2a: outcome-2 (standalone=commodity, workflow-integrated=differentiated); §2b: outcome-2; §2c: outcome-2 |
| F3 | HIGH | Settlement optimization → T+7 | §2a: outcome-1 REVISED (speed alone insufficient, combine w/ full admin); §2b: outcome-2; §2c: outcome-2 |
| F4 | HIGH | Cross-vehicle complexity → architecture decision | §2a: outcome-2; §2c: outcome-1 REVISED (phased rollout) |
| F5 | MED-HIGH | Borrowing base engine → continuous monitoring | §2a: outcome-2; §2c: outcome-1 REVISED (BBC as premium tier) |
| F6 | MED-HIGH | Amendment lifecycle automation | §2a: outcome-2; §2c: outcome-2 |
| F7 | MEDIUM | Investor reporting → integrated transparency | §2a: outcome-1 REVISED (standalone=commodity); §2c: outcome-2 |
| F8 | MEDIUM | Loan IQ ecosystem strategy | §2a: outcome-2; §2c: outcome-3 GAP (flagged DA/lead) |
| F9 | MEDIUM | Versana integration → market infrastructure | §2a: outcome-1 REVISED (integration≠differentiating); §2b: outcome-2 |
| F10 | MEDIUM | AI-augmented operations model | §2a: outcome-2; §2c: outcome-2 |

**Hygiene grade: B+** (4 outcome-1 revisions, 1 outcome-3 gap, 5 outcome-2 maintained; 2 outcome-2s need stronger evidence on F1 and F4)

#### product-strategist (10 v1 + 7 v2 findings)

v2 NEW findings:
- F1v2: Competitive moat evolution Q1 2026 (5 moves in 90 days, tech window 6-12mo)
- F2v2: Go-to-market sequencing (3 phase)
- F3v2: Pricing/monetization (3 models: flat/AUA-bps/hybrid)
- F4v2: Channel playbook (5-step: hire BD → target 3 firms → prove → CRM → expand)
- F5v2: PLG vs relationship (RELATIONSHIP wins, 0 PLG examples institutional finserv)
- F6v2: Platform vs point solution (deep vertical platform wins)
- F7v2: AI positioning beyond table stakes (parsing=table-stakes, TRUE: closed-loop + real-time + predictive + amendment)

v1 retained: F1-F10 (TAM, competitive landscape, market entry, distribution moat, incumbent tech, pricing, alternatives, market timing, moat architecture, growth dynamics)

**Hygiene grade: B** (1 clear FAIL on F1 §2b confirmation bias in TAM calibration, rest PASS)

#### regulatory-licensing-specialist (8 v1 + 8 v2 findings)

v2 NEW findings:
- F9: RegTech as differentiator (3 mechanisms, split: 2/3 internal + 1/3 external KYC)
- F10: Charter expansion sequenced (NH→UK→EU→APAC)
- F11: Insurance tower deep dive (PC Day-1 $25-80K, BSL 3-5yr gate $100-400K)
- F12: AML/BSA as product (AI 70-90% detection, KYC-as-service $5-15K/client)
- F13: Successor agent mechanics (contractual, migration tech $50-100K)
- F14: Regulatory cost optimization ($190-390K/yr savings)
- F15: NH examiner URSIT expectations (4 components mapped)
- F16: Regulatory moat quantified (SaaS→charter = 28-45mo + $2-4.5M)

**Hygiene grade: B+** (1 regression on DA correction for F9, otherwise strong sourcing)

### DA Challenges and Responses

See §4 for challenge table. Key outcomes:

- **Best LOT defense**: Waterfall type distinction (DA[#1]) — correctly identified that fund distribution, loan admin payment, and CLO compliance waterfalls are categorically different. DA missed this distinction.
- **Best PS honesty**: Owned confirmation bias on TAM calibration (DA[#3]) — selected only upward sources, zero downside = textbook confirmation bias.
- **Best RLS research**: OCC charter surge (DA[#4]) — 11 companies in 83 days, 20 filings in 2025 = all-time high.
- **Most impactful challenge**: DA[#3] credit cycle stress — forced bear case modeling that was entirely absent from 28 findings.

### Convergence Declarations

```
loan-ops-tech-specialist: ✓ r2 DA-responses complete |7 challenges addressed(4H+3M)
product-strategist: ✓ r2 DA-responses complete(RESEARCH-ENHANCED) |7 challenges addressed(4H+3M)
regulatory-licensing-specialist: ✓ r2-UPDATED |5 challenges(2H+3M)
devils-advocate: ✓ promotion-complete |exit-gate:PASS |→lead:synthesis-authorized
```

### Open Questions

1. CRD6 member state transposition (FR/DE/NL specific)
2. Hypercore charter probability → Insight M&A monitor
3. Insurance hard market cycle → excess availability 2027-2028
4. FinCEN IA-AML (Jan 2028) → trust company scope
5. Credit stress BDC pipeline → greenfield bear case

---

## 7. Team Decisions

> Source: ~/.claude/teams/sigma-review/shared/decisions.md (relevant entries for this review)

### Loan Admin Agent v1 Review Decisions (26.3.11)

```
assessment:r4-SYNTHESIZE-recommendation |proceed-to-r5-synthesis,¬additional-agent-response-round |by:devils-advocate |weight:primary
assessment:convergence-trajectory-acceptable |r1(HIGH-herd)→r2(DECREASED)→r3(SLIGHTLY-INCREASED)→overall-acceptable |by:devils-advocate |weight:primary
challenge:gross-margin-46%=fundraising-risk |must-model-explicit-path-to-70%+gross-margin-with-AI-automation-milestones |by:devils-advocate |weight:primary
challenge:compliance-native-overweight-as-differentiator |reframe-as-internal-efficiency(lower-tech-debt)→¬external-competitive-advantage |by:devils-advocate |weight:advisory
market-entry:mid-market-PC-via-greenfield-BDC-launches |pipeline:40%-greenfield+30%-successor+30%-sponsor-mandate |by:product-strategist |weight:primary
moat-architecture:charter+distribution-primary,technology-secondary |¬data-flywheel-at-zero-AUA(anti-pattern) |by:product-strategist |weight:primary
alternatives:BUILD-primary(charter+tech+ops,$25-40M-to-breakeven,18-24mo-to-first-facility) |ACQUIRE-Hypercore-DEFER |WHITE-LABEL-REJECT |NULL-kept-as-benchmark |by:product-strategist |weight:primary
regulatory:effective-window-2-8mo |gross-18-24mo-minus-regulatory-14-20mo=2-8mo-effective |by:regulatory-licensing-specialist |weight:primary
regulatory:MTMA-31-states-99%-validates-trust-charter-payment-path |by:regulatory-licensing-specialist |weight:primary
ops-tech:waterfall-engine=core-product-decision |dual-mode(BSL+PC)required |by:loan-ops-tech-specialist |weight:primary
ops-tech:cross-vehicle-phased-rollout |CLO+BSL first→PC+BDC second→evergreen third |by:loan-ops-tech-specialist |weight:primary
ops-tech:Loan-IQ-strategy=own-core+API-integration |by:loan-ops-tech-specialist |weight:primary
```

### Loan Admin Agent v2 Review Decisions (26.3.12)

```
ops-tech:waterfall-claim-NARROWED |¬"no-platform-spans-BSL+PC"→"no-platform-integrates-loan-payment-waterfall+fund-distribution+CLO-compliance-in-single-admin-stack" |by:loan-ops-tech-specialist |weight:primary
ops-tech:Loan-IQ-GAP→PHASED-HYBRID |<50-facilities=license+proprietary-payment-waterfall |≥50=begin-own-core |≥100=full-own-core |by:loan-ops-tech-specialist |weight:primary
build-sequence:DIVERGENCE-LOGGED |PS:distribution-first vs LOT:waterfall-first |RESOLUTION:staggered-concurrent |by:product-strategist+loan-ops-tech-specialist |weight:split
D[build-sequence]:waterfall+distribution=STAGGERED-CONCURRENT¬sequential |by:loan-ops-tech-specialist |weight:HIGH
D[credit-cycle-pipeline-mix]:bear-case-pipeline=greenfield-15-20%+successor-40-50%+restructuring-20-30%+sponsor-10-15% |by:loan-ops-tech-specialist |weight:HIGH
regulatory:breakeven-mo-36-48(¬PS-30-42) |divergence-with-PS-logged |by:regulatory-licensing-specialist |weight:primary
regulatory:Hypercore-charter-moat-REDUCED |acquisition-path=9-18mo+$5-20M |moat:"significant"→"moderate" |by:regulatory-licensing-specialist |weight:primary
exit-gate:PASS(r2)|synthesis-authorized |engagement:LOT(A-)+PS(B+)+RLS(A-) |challenges:8/10-held(80%) |by:devils-advocate |weight:primary
```

---

## 8. Cross-Agent Patterns

> Source: ~/.claude/teams/sigma-review/shared/patterns.md

### Patterns Relevant to This Review (v2, 26.3.12)

```
regulatory-timeline-eats-competitive-window: in-regulated-markets,gross-competitive-window-must-be-reduced-by-regulatory-setup-time=effective-window. Loan-admin: 18-24mo-gross→6-12mo-effective |agents: devils-advocate,regulatory-licensing-specialist

regulatory-specialist-mandatory-from-r1-in-regulated-markets: late-arriving-agents-anchor-to-existing-findings(herding-amplifier) |agents: devils-advocate,regulatory-licensing-specialist

consensus-crowding-in-markets: when-10+-competitors-build-same-features→table-stakes-within-12mo. Differentiation-must-come-from-integration-depth+structural-advantages |agents: tech-architect,product-strategist,devils-advocate

compliance-native-overweight-as-external-differentiator: compliance-by-design=emerging-best-practice-across-ALL-fintech. Reframe-as-operational-cost-advantage¬competitive-moat |agents: regulatory-licensing-specialist,devils-advocate,tech-architect

credit-cycle-blind-spot=systematic: teams-model-growth-exclusively→DA-MUST-force-bear-case-scenario-in-r2 |agents: devils-advocate,product-strategist,loan-ops-tech-specialist

relabeling-evasion-pattern: agent-accepts-DA-correction→new-finding-reintroduces-same-thesis-with-different-label |agents: devils-advocate,regulatory-licensing-specialist

adjacent-giant-platform-risk: specialist-teams-systematically-underweight-threats-from-adjacent-platforms(S&P-free-tools,Versana-data-layer) |agents: devils-advocate,product-strategist,loan-ops-tech-specialist
```

### Confirmed Patterns from Prior Reviews

```
2-agent-teams-herd-faster |DA from r2 minimum always
5-round-ANALYZE-effective |DA at r2 AND r4 caught different issues
dynamic-agent-creation-valuable |DA identifies gaps→lead creates specialist
consensus-replacement-under-pressure |team replaces one consensus with another→DA must stress-test NEW consensus too
```

---

## 9. Agent Memory Files

> Source: sigma-mem MCP → get_agent_memory for each active agent

### loan-ops-tech-specialist

```markdown
# loan-ops-tech-specialist — personal memory

## identity
role: loan operations technology specialist
domain: waterfall-engines,loan-admin-platforms,settlement,credit-agreement-tech,covenant-monitoring,LSTA/LMA-standards,CLO/BDC-ops,SOFR,borrowing-base,payment-processing
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## research
R[waterfall-calc-engines:BSL=standardized waterfalls(OC/IC tests,interest diversion,sequential tranche priority)|PC=bespoke per-deal(unitranche splits,PIK toggle,delayed-draw,custom EBITDA addbacks)|key-complexity:30/360 vs actual/360 day counts,compounding intervals,split/toggle/full PIK,multiple waterfall paths(ordinary/prepay/acceleration)|deterministic:BSL CLO indentures define exact rules,self-curing on OC/IC breach|configurable:PC per-deal config,eligibility as code,versioned inputs|audit:every calc reproducible+versioned,CLO trustees(US Bank,Wilmington)provide compliance test+cashflow modeling|tech:Allvue=CLO compliance calc engine+waterfall modeling,Cascata=PE waterfall,Covercy=debt waterfall|spreadsheet-risk:PC firms still heavily dependent,unacceptable risk driving platform adoption|2025-change:PIK surge 14.8%→22.2% Q2-Q3 2025,shadow defaults 3x 2021,waterfall complexity increasing w/restructuring wave|src:IQ-EQ,Carta,Allvue,US Bank,Covercy,TCW,Octus|refreshed:26.3.12|next:26.4]

R[finastra-loan-iq-ecosystem:market-share ~70% global syndicated volume,9/10 top agent banks,21/25 top global banks|IDC MarketScape 2025 Leader|caps:multicurrency,flexible repayment,complex pricing,interest+fee accruals,automated billing/collections|Nexus:open API integration layer→pre-configured integrations→OCR loan onboarding→LaserPro Connect→nCino/Abrigo|limits:slow issue resolution bleeds over reporting periods(Gartner),not fully customizable,implementation needs partners(Luxoft)|alt-BSL:Temenos,Fiserv LoanServ,nCino|alt-PC:Allvue,Cardo AI($90B AUT),Arcesium(UBOR+FactSet Dec 2025)|FIS:Loanet→Loanext transition|src:Finastra,Capterra,Gartner,IDC,Allvue,Chartis,Cardo AI,FIS,Arcesium|refreshed:26.3.12|next:26.4]

R[settlement-trade-processing:current median par T+11(Aug 2025)|Kroll avg 8 days vs industry 47(6x faster)|LSTA:settlement waterfall Sec 1→mandatory→delayed compensation from T+7|Versana:real-time digital data→cashless roll(JP Morgan Oct 2025)→CEI integration|McKinsey:best-in-class STP 80-90%,most banks below 50%|src:LSTA,Kroll,Versana,LMA,McKinsey|refreshed:26.3.12|next:26.4]

R[credit-agreement-technology:AI/NLP parsing 200-500pg docs→iterative phased approach|CovenantIQ,Ontra,Cardo AI,S&P DataXchange+AmendX(Mar 2026),V7 Labs,LMA Automate|77% NA institutional investors using/planning genAI|src:CovenantIQ,Ontra,S&P,Cardo AI,LMA|refreshed:26.3.12|next:26.4]

R[investor-reporting-notice-systems:Dynamo 2026:66% cite reporting+manual entry as top challenge|75% prefer all-in-one|S&P DataXchange:centralized notice delivery|Versana:real-time digital notices|src:Dynamo,S&P,Versana,Alter Domus|refreshed:26.3.12|next:26.4]

R[LSTA-LMA-standards:LSTA=US standard terms|LMA=EMEA→LMA:Automate(free 2025)|joint LMA/LSTA/APLMA:Oct 2025 Transition Loan Guide|CUSIP/CEI enabling digital connectivity|gap:PC lacks equivalent standardization|src:LSTA,LMA,CUSIP|refreshed:26.3.12|next:26.4]

R[CLO-BDC-evergreen-ops:CLO=sequential tranche waterfall+OC/IC|BDC=SEC quarterly valuation Level 3(ASC 820)|evergreen=continuous LP entries/exits at NAV|cross-vehicle=three distinct operational models|src:IQ-EQ,Wilmington Trust,US Bank,SEC|refreshed:26.3.12|next:26.4]

R[SOFR-transition:status:substantially complete by Mar 2026|Term SOFR licensing free through end 2026→KEY deadline|operational impact:5% reduction credit line commitments|src:ARRC,NY Fed,CME|refreshed:26.3.12|next:26.4]

R[borrowing-base-calculations:platforms:timveroOS,ABLSoft,Setpoint,Cascade Debt,Finley|automation benefits:faster credit decisions,real-time risk visibility|gap:many lenders still manual quarterly|src:timveroOS,ABLSoft,Setpoint|refreshed:26.3.12|next:26.4]

R[payment-processing-syndicated:models:trust company,bank partnership,third-party agent|reconciliation:best STP 80-90%,most banks <50%|Basel III/IV impact|Versana digitizing|src:McKinsey,Wilmington,Versana|refreshed:26.3.12|next:26.4]

R[market-context-2025-26:PC AUM expected +50% by 2028|2025 default wave→UBS worst-case 15%|PIK 14.8%→22.2%|shadow defaults 3x|LME wave|BSL-PC convergence|src:multiple|refreshed:26.3.12|next:26.4]

## findings
F[26.3.12] r1: 10 findings(4H,2MH,4M) |key: dual-mode-waterfall=core, AI→ops-workflow=differentiated, settlement-alone-insufficient, cross-vehicle-phased, BBC-premium-tier, Loan-IQ-GAP
F[26.3.12] r2-DA-responses: 7 challenges |DA[#1]:compromise—waterfall-narrowed |DA[#2]:concede-partially |DA[#3]:defend+addendum—bear-case-strengthened |DA[#5]:defend—2-disagreements |DA[#7]:concede—cost-model-provided |DA[#8]:defend—S&P=data-layer |DA[#9]:compromise—phased-hybrid

## calibrations
C[waterfall-type-taxonomy:fund-distribution≠loan-admin-payment≠CLO-compliance|platforms-serve-1-rarely-2-never-3|DA-validated|26.3.12]
C[AI-doc-processing-commoditization:standalone=commodity-end-2026(8+-players)|window-closed|differentiated=workflow-integrated-ONLY|26.3.12]
C[credit-cycle-counter-cyclical-demand:stress=BOTH-risk+opportunity|BDC-sales-down-49%|bear-pipeline:greenfield-15-20%+successor-40-50%+restructuring-20-30%|26.3.12]
C[incumbent-AI-dual-timeline:doc-processing→end-2026|core-admin-ops→2028-29(legacy=binding)|26.3.12]
C[STP-rates-institutional:best=80-90%|most<50%|persistent-multi-year|26.3.12]

## patterns
P[settlement=coordination¬tech:barriers=structural|STP<50%-despite-tech|Kroll-8day=process-innovation|26.3.12]
P[loan-admin-payment-waterfall-as-moat: 3-waterfall-types. No-platform-spans-all-3. DA-validated |promoted:26.3.12]
P[build-sequence-staggered-concurrent: ¬either/or. MVP-waterfall-mo-0+distribution-mo-3-6 |promoted:26.3.12]
P[phased-core-vs-license-volume-threshold: <50=license,≥50=own,≥100=full |promoted:26.3.12]
```

### product-strategist

*(Full memory: ~450 lines — includes identity, known products, 10 past review findings, 20+ calibrations, strategic insights, 20+ research entries, review-9-v2 findings, promotion logs. See sigma-mem MCP `get_agent_memory(team:sigma-review, agent:product-strategist)` for complete content.)*

Key entries for this review:

```
## review-9-v2 findings
- 7 NEW findings (F1v2-F7v2): competitive moat evolution, GTM sequencing, pricing, channel playbook, PLG vs relationship, platform vs point, AI positioning
- 10 v1 retained (F1-F10)
- r2 DA responses: incumbent AI tiered, credit stress bear case, Hypercore Tier-4.5, build sequence disagreement, integrated cost model, S&P defense

## key calibrations (this review)
C[GP-selection-weights: technology=21% vs service=72%+relationships=69%]
C[competitive-landscape-entering-consolidation: 5 moves in 90 days Q1 2026]
C[tech-differentiation-window-shorter-than-v1: 12-18mo→6-12mo]
C[confirmation-bias-in-TAM-calibration: selected ONLY upward sources = DA correct]
C[charter-race-framing-more-useful-than-moat-framing]

## promoted patterns
P[distribution>technology-for-finserv-moat]
P[alternatives-analysis-essential-from-r1]
P[data-flywheel-moat-claims-at-zero-scale=anti-pattern]
P[incumbent-narrative-framing-discipline]
P[margin-path-milestones-as-standard-§2c]
P[incumbent-AI-tiered-assessment-mandatory]
P[stress-scenario-research-backed=standard]
```

### regulatory-licensing-specialist

*(Full memory: ~350 lines — includes identity, research R1-R7, calibrations, patterns, r2 integration, open questions, v2 findings F9-F16, v2 calibrations, r2 DA responses, promotion round. See sigma-mem MCP for complete content.)*

Key entries for this review:

```
## v2 findings (F9-F16)
F9: regtech-as-differentiator (SPLIT: 2/3 internal + 1/3 external KYC)
F10: charter-expansion-sequenced (NH→UK→EU→APAC, $1.5-3M/4yr)
F11: insurance-tower-detailed (PC Day-1 $25-80K, BSL 3-5yr gate)
F12: AML/BSA-as-product (AI 70-90% detection, $250K-3M/yr revenue)
F13: successor-mechanics-resolved (contractual, migration tech)
F14: regulatory-cost-optimization ($190-390K/yr savings)
F15: NH-examiner-URSIT (4 components mapped)
F16: regulatory-moat-quantified (SaaS→charter = 28-45mo)

## key calibrations
C[Fitch-PC-defaults-9.2%: record-level-2025|confidence:HIGH]
C[Hypercore-charter-acquisition-9-18mo: plausible-but-no-precedent|confidence:MEDIUM]
C[breakeven-mo-36-48: all-in-burn-exceeds-PS-model|confidence:MEDIUM-HIGH]
C[charter-environment-2025-2026: MOST-favorable-in-decade]
C[KYC-as-service-precedent: 5-firms-actively-selling|confidence:HIGH]

## promoted patterns
P[charter-as-multi-solving-instrument]
P[conditional-charter≠operational-readiness: 12-18mo gap post-approval]
P[stress-shifts-pipeline-mix-not-volume]
P[AI-regulatory-language-precision: "AI-assisted"≠"AI-generated"]
```

### devils-advocate

*(Full memory: ~500 lines — includes identity, calibration from Iran conflict debate, patterns, research (crowding, base rates, ceasefire, defense valuations), loan admin v1 challenges (r1→r4), v2 challenges, exit gate verdicts. See sigma-mem MCP for complete content.)*

Key entries for this review:

```
## v2 challenges (10 issued)
DA[#1-#10] — see §4 for full table and outcomes

## v2 exit-gate: PASS
engagement:LOT(A-)+PS(B+)+RLS(A-)
challenges:8/10-held(80%)
4-gaps-resolved, 2-divergences-logged, 1-correction-held

## key lessons (v2)
- challenge-hit-rate-80% = r1 had real gaps (cost-model, credit-stress, Loan-IQ)
- LOT waterfall distinction BEAT DA → domain specialist adds unique value at category boundaries
- PS owning bias = rare + valuable → note for calibration
- RLS breakeven divergence = most valuable dissent in review

## promoted patterns
P[domain-specialist-category-error-detection: specialists identify categorical boundaries DA misses]
P[specialist-depth-without-thesis-challenge = anti-pattern: DA irreplaceable for strategic stress test]
P[buried-dissent-detection: scan for findings where one agent's reframe was not engaged by peers]
P[burn-multiple-check = standard §2c for startup analysis]
P[limitation-inflation-anti-pattern: managing a constraint ≠ differentiator]
P["good-enough" competitive-response-modeling: benchmark against MINIMUM VIABLE response]
```

---

## 10. Agent Inboxes

> Source: ~/.claude/teams/sigma-review/inboxes/*.md

All 11 inbox files have been processed — no unread content remains for this review. Inter-agent communication for this review was conducted via the shared workspace and direct messaging through the native Agent Teams system rather than markdown inboxes.

---

## 11. ΣComm Protocol Reference

> Source: ~/.claude/agents/sigma-comm.md

```markdown
# ΣComm — Compressed Agent Communication Protocol

## Message Format

[STATUS] BODY |¬ ruled-out |→ actions |#count

### Status Codes
✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry

### Body Notation
|=section-sep ,=item-sep >=pref/should-be →=leads-to +=and !=critical

### Sections
- ¬ = what was NOT found/NOT the issue (prevents assumptions)
- → = what you CAN do next (HATEOAS: state-dependent actions)
- #N = item count checksum (verify decode matches count)

### Rules
1→agent-to-agent: this format
2→include ¬ — ruled-out
3→include → — next actions
4→include #count — decode-verify
5→ambiguous → ask sender, ¬assume
6→user→plain | peers→ΣComm

## Codebook (for agent system prompts)

Messages use compressed notation. Format: [STATUS] BODY |¬ not-found |→ can-do-next |#count
Status: ✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry
Body: |=sep >=pref →=next +=and !=critical ,=items
¬=explicitly NOT (prevents assumptions)
→=available actions (HATEOAS: what you can do based on current state)
#N=item count (checksum: verify you decoded correctly)

## Inbox Format

Agents communicate via markdown inbox files at ~/.claude/teams/{team}/inboxes/{name}.md.
Processing: read ## unread → process → compress to ## processed → clear ## unread

## Workspace Format

Shared workspace at ~/.claude/teams/{team}/shared/workspace.md.
Rules: YOUR section only, ¬edit peers. Peer findings → agreements in convergence.

## Boundary

| Surface | Format | Why |
|---------|--------|-----|
| agent instructions | ΣComm | read by agents every spawn |
| memory writes | ΣComm | stored+recalled across sessions |
| agent-to-agent messages | ΣComm | peer inbox format |
| workspace findings | ΣComm | agent-written, agent-read |
| agent Role/Expertise | plain | identity framing |
| open-questions | plain | user reads these |
| user-facing docs | plain | human audience |

## Examples

Agent-to-agent:
✓ auth-review: jwt-expiry-no-validate(!), pwd-md5>bcrypt, no-rate-limit-login |¬ session-mgmt, cors |→ fix-jwt(small), fix-hash(needs-db-migration) |#3

Convergence:
tech-architect: ✓ review-complete |resolved: 4/6, new: 3 |→ ready-for-synthesis
```

---

## 12. Token Spend Summary

> Source: Runtime observation (exact per-agent metrics not available)

| Agent | Status | Rounds | Notes |
|-------|--------|--------|-------|
| loan-ops-tech-specialist | Completed (2 spawns) | r1, r2 | Original + re-spawn after context loss |
| product-strategist | Completed (3 spawns) | r1, r2 | Original + 2 re-spawns |
| regulatory-licensing-specialist | Completed (2 spawns) | r1, r2 | Original + re-spawn |
| devils-advocate | Completed (1 spawn) | r2 | Single spawn for challenge round |

**Session characteristics**:
- Context recovery occurred mid-session (conversation exceeded context window)
- All agents re-spawned successfully with full state recovery via workspace + agent memory
- Duplicate agents from pre-context-loss completed late and were shut down cleanly
- Total session: ~3 hours wall clock, 2 rounds completed

**Promotion phase**: 29 total promotions (19 auto-promoted + 10 user-approved) stored to global agent memory via sigma-mem MCP.

---

## 13. Repository Diffs

### sigma-system-overview

> Path: ~/Projects/sigma-system-overview

```
 INTERFACES.md                                      | 154 ++++
 agent-infrastructure/agents/loan-ops-tech-specialist.md | 90 +++
 agent-infrastructure/agents/sigma-lead.md          |  38 +-
 agent-infrastructure/skills/sigma-review/SKILL.md  |  19 +-
 agent-infrastructure/teams/sigma-review/shared/decisions.md | 151 ++++
 agent-infrastructure/teams/sigma-review/shared/patterns.md  |  25 +
 agent-infrastructure/teams/sigma-review/shared/portfolio.md |  10 +
 agent-infrastructure/teams/sigma-review/shared/roster.md    |   1 +
 agent-infrastructure/teams/sigma-review/shared/workspace.md | 817 +++++++++++++---
 setup.sh                                           |  60 +-
 10 files changed, 1239 insertions(+), 126 deletions(-)
```

Full diff >500 lines. Available at `~/Projects/sigma-system-overview` via `git diff HEAD~5`.

### sigma-mem

> Path: ~/Projects/sigma-mem

```
 .github/workflows/ci.yml          |   4 +-
 pyproject.toml                    |   2 +-
 src/sigma_mem/handlers.py         | 257 +++++++++++++++++++++++++++++---------
 src/sigma_mem/integrity.py        |  28 +++--
 src/sigma_mem/machine.py          |   8 +-
 tests/test_bridge.py              |  16 ++-
 tests/test_handlers.py            |  50 +++++++-
 tests/test_integrity.py           |  27 +++-
 tests/test_machine_integration.py |   5 +-
 tests/test_teams.py               |  73 +++++++----
 10 files changed, 356 insertions(+), 114 deletions(-)
```

Full diff >500 lines. Available at `~/Projects/sigma-mem` via `git diff HEAD~5`.

### hateoas-agent

> Path: ~/Projects/hateoas-agent

```
 .env.example                           |  10 +
 .github/workflows/ci.yml               |  51 +++
 .gitignore                             |  40 +++
 LICENSE                                |  21 ++
 README.md                              | 254 ++++++++++++-
 examples/ (12 files)                   | 2845 ++++++++++++++++++
 pyproject.toml                         |  67 ++++
 src/hateoas_agent/ (13 files)          | 1662 +++++++++++
 tests/ (18 files)                      | 6137 +++++++++++++++++++++++++++
 51 files changed, 10644 insertions(+), 1 deletion(-)
```

Full diff >500 lines. Available at `~/Projects/hateoas-agent` via `git diff HEAD~5`.

---

*Bundle generated 2026-03-12 by sigma-review lead. 29 promotions stored to global memory. All agents shut down cleanly. Infrastructure synced to sigma-system-overview repo (commit 7335cdf).*
