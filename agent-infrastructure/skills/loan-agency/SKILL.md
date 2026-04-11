---
name: loan-agency
description: >
  Use this skill for loan administration, loan agency operations, administrative/collateral/escrow agent workflows, payment processing, wire approvals, rate setting, debt service notices, SOFR/SONIA/EURIBOR mechanics, day-count conventions, payment waterfalls, credit agreement interpretation, amendments, consent solicitation, secondary trading, assignments, settlement, tax withholding (W-8/W-9, FATCA), KYC/AML, deal lifecycle, collateral management, UCC filings, escrow, sub-agency, billing, tickler management, lender data rooms, or any loan facility administration. Triggers: 'loan agency', 'administrative agent', 'payment waterfall', 'DSN', 'A&A', 'LSTA', 'LMA', 'DLX', 'deal summary', 'gross-up', 'KYC', 'wire approval', 'maker-checker', 'pro rata share', 'syndicated loan', 'private credit', 'BDC', 'CLO', 'credit agreement'. Also for competitive landscape, charter strategy, NH NDTC, or market entry questions. Do NOT use for fund administration, NAV calculations, equity markets, or general corporate banking.
---

# Loan Agency Operations

Third-party loan administration covering broadly syndicated loans (BSL) and private credit
from the perspective of an administrative agent, collateral agent, and escrow agent.

## Three-Tier Reference System

This skill has three levels. **Start at the top; go deeper only if needed.**

### Tier 1 — Quick References (read first)

Condensed operational essentials: tables, decision rules, key numbers. Usually sufficient.

| Topic | Read |
|-------|------|
| Key terms, abbreviations, role definitions | `references/qr-glossary.md` |
| Market size, loan products, conventions | `references/qr-market-landscape.md` |
| Sacred rights, amendments, LSTA vs LMA, EBITDA add-backs, erroneous payments | `references/qr-credit-agreements.md` |
| SOFR/day-count, payment systems, waterfalls, defaulting lenders | `references/qr-operational-mechanics.md` |
| Trade types, settlement timelines, ClearPar, BISO, delayed comp | `references/qr-secondary-trading.md` |
| Tax form decision tree, withholding rates, KYC, callbacks | `references/qr-tax-withholding.md` |
| Agent roles, amendment workflow, UCC filings, deal onboarding checklist | `references/qr-lifecycle-events.md` |

### Tier 2 — Operational Skills (for "how do I do this" tasks)

Step-by-step workflows with controls, handoffs, and checklists.

| Task | Read |
|------|------|
| Payment processing, wire approval, rate setting, DSN, rollovers | `references/loan-agency-payment-processing.md` |
| Deal closing, deal summary, amendments, termination | `references/loan-agency-deal-lifecycle.md` |
| Deal onboarding into DLX, facility setup, position entry | `references/dlx-deal-onboarding.md` |
| DLX transactions: drawdowns, repayments, rate conversions, PIK | `references/dlx-transaction-processing.md` |
| Tickler management, compliance deadlines, tracking | `references/dlx-tickler-management.md` |
| Tax form review (W-8/W-9), withholding determination | `references/loan-agency-tax-form-review.md` |
| Assignment processing, A&A, position transfers, freeze rules | `references/loan-agency-assignments.md` |
| KYC/AML screening, sanctions, lender approval | `references/loan-agency-kyc-process.md` |
| Collateral management, UCC filings, pledges, DACAs | `references/loan-agency-collateral-management.md` |
| Escrow administration, setup, release, termination | `references/loan-agency-escrow.md` |
| Billing, invoicing, fee collection | `references/loan-agency-billing-invoicing.md` |
| Lender data room, document distribution | `references/lender-data-room-management.md` |
| Sub-agency operations, appointment, information flow | `references/sub-agency-operations.md` |

### Tier 3 — Full Domain Docs (for deep dives only)

Comprehensive reference with market data, case law, sourcing. 48-124KB each — only load when Tier 1 and 2 don't answer the question.

| Document | Read |
|----------|------|
| **Strategic wiki** — tech landscape, charter path, private credit market, competitors, calibrated estimates (April 2026) | `references/strategic-wiki.md` |
| **Full strategic analysis** — sigma-review of technology opportunities, competitive moats, unit economics, build sequence, regulatory path, agent memory | `references/strategic-analysis-bundle.md` |
| Full glossary (213 terms) + KB conventions | `references/Doc0_Glossary_and_KB_Preface.md` |
| Market structure, BSL/private credit, CLO mechanics, all product types | `references/Doc1_Market_Landscape_and_Loan_Products.md` |
| Credit agreement trends, LME litigation, covenant mechanics | `references/Doc2_Credit_Agreement_Interpretation_Revised.md` |
| SOFR methodology, payment systems, ECF sweeps, LC, swingline, multi-currency | `references/Doc3_Operational_Mechanics_Revised.md` |
| Secondary trading docs, settlement workflows, platforms, BISO, delayed comp | `references/Doc4_Secondary_Trading_and_Settlement.md` |
| Tax forms, withholding regimes, treaty networks, KYC/AML, ERISA | `references/Doc5_Tax_Withholding_and_Lender_Onboarding.md` |
| Agent roles, amendments, workouts, regulatory, tech stack | `references/Doc6_Lifecycle_Events_Agent_Administration_Revised.md` |

---

## Gotchas

- **Day-count errors are the most expensive mistake.** Verify convention against credit agreement — never assume from currency. Wrong convention on $500M = $100K+ per quarter.
- **Floor applies to benchmark only, not the all-in rate.** Single most common rate calculation error.
- **No payment without tax form + callback.** Hard stop, not soft control.
- **Two-person wire approval mandatory.** Different people for first and second approval. No exceptions.
- **Assignment freeze: 5 business days before payment date.** Closing during freeze risks paying wrong lender.
- **Deal Summary is the central artifact.** If wrong, everything downstream breaks — rates, payments, notices, assignments.
- **KYC expires in 30 days.** If deal doesn't close in time, refresh required.
- **Pro rata shares recalculate after ANY balance change.** Rounding errors compound.
- **Admin agent is NOT a fiduciary** (most US agreements). Acts mechanically per the credit agreement.
- **Missing a UCC continuation filing = loss of perfected security interest.** Highest-risk collateral agent error.
- **BSL and private credit differ operationally** — fewer lenders, bespoke terms, less standardized docs, longer settlement, often no ClearPar.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
