# Loan Agency Persona Research Package

**Source:** Owner-built v1.2 personas at `/Users/bjgilbert/Documents/personas-audit/` (May 12, 2026)
**Context:** Audit of SRS Acquiom v1 proto-personas evolved into v1.2 with 13 personas + evidence-basis tagging
**Use case:** Future loan-agency conversations, persona-design references, B2B long-cycle market patterns

## What this package is

A research-anchored persona system for US private credit + BDC + CLO administrative agency products. Built without primary user research; gaps closed via multi-agent secondary research (sigma-retrieve + sigma-single). Every load-bearing claim carries an evidence-basis tag.

## Personas (13 in v1.2)

**Daily Operators (9):**
- Maya Patel — Lender Loan Operations Specialist (notice reconciliation, break investigation)
- David Chen — Lender Treasury / Cash Operations (wire matching, cash break investigation — durable bet; remittance structure declining due to ISO 20022 July 2025)
- Jordan Reyes — Buyside Portfolio Administrator (multi-source recon, amendment voting)
- Sasha Kim — Third-Party Fund Administrator (multi-client SLA, post-selection retention influence ONLY)
- Alex Hoffman — Borrower Treasurer (transaction submission, day-to-day agent relationship)
- Riley Chen — Trade Settlement / Assignment Ops *(NEW v1.2; LSTA T+7, delayed-comp, BISO)*
- Drew Park — Lead Arranger Ops Desk *(NEW v1.2; promoted from buyer-side influencer; bank-side role with asset-manager downstream customer)*
- Sky Patel — Tax / Withholding Ops *(NEW v1.2; W-8 lifecycle, FATCA, Section 871(m), 1042-S filing)*
- Morgan Lopez — KYC / AML Coordinator *(NEW v1.2; lender onboarding, sanctions screening, UBO trace)*

**Plus Priya-Bank — Head of Loan Ops at bank** (Influencer, NOT Champion; OCC 2023-17 distributed vendor authority).

**Champions (2 of 13):**
- Priya-PC — Head of Loan Ops at Private Credit (scoped to sub-agency + operational, NOT named-agent designation)
- Marcus Bennett — Sponsor Capital Markets Professional (Conditional Champion: Champion on influence axis; Recommender on admin agent portals; sub-segmented MD vs VP/Associate; AUM threshold $1B+ typical)

**Informed:**
- Sam Williams — Senior Credit Analyst (episodic deep user, amendment cycles)
- Quinn Harper — Hands-On Borrower CFO (Informed at LBO closing; Engaged Influencer at refinancings — NOT Conditional Champion per sigma refutation)

## Cross-cutting findings (with sources)

### Decision rights — named agent vs sub-agent

Two different decisions with different decision-rights structures:

- **Named admin agent in credit agreement:** appointed by lender syndicate via lead arranger structuring. Borrower has consultative input, not authority. [secondary-converged]
- **Sub-agent appointment:** administrative-agent unilateral. No borrower or lender vote required.

The original v1 persona doc conflated these decisions, producing the Champion misclassification. v1.2 makes the distinction foundational.

**Sources:**
- LSTA Model Credit Agreement Provisions (MCAPs) [T1]
- ABA Business Law Today, "Liability Management Transactions: The Role of the Administrative Agent" (Apr 2025) [T1]
- Proskauer Rose, "Navigating the Club in Private Credit Deals" [T1]
- SRS Acquiom market resources (own materials acknowledge the distinction)
- Mayer Brown, Bloomberg Law treatise [T2]

### B2B vendor memory durability and asymmetry

Established empirical pattern relevant to all long-cycle B2B markets:

- **Loss aversion:** 2-2.5× multiplier (gains must exceed losses by this ratio) — Kahneman & Tversky, prospect theory [T1 foundational]
- **Positive:negative ratio for sustained B2B performance:** 3:1 (couples research generalizes to business relationships)
- **Memory persistence (routine interactions):** 3-6 month half-life
- **Memory persistence (critical failures):** 18-36+ months in B2B contexts
- **NPS detractor churn:** 50% within 90 days
- **Detractor share of WOM:** 80%+ of negative word-of-mouth from detractor cohort
- **Pre-RFP vendor preference:** 97% of B2B decision-makers know preferred vendor before formal selection process

**Design implications:** Downside protection > upside generation. Peak-end rule applies — invest disproportionately in onboarding (peak) and renewal-stage workflows (end). Memorable negative experiences dominate cumulative experience memory regardless of total relationship duration.

**Sources:**
- Kahneman & Tversky prospect theory [T1 peer-reviewed]
- Springer Experimental Economics, asymmetric memory recall [T1 peer-reviewed]
- McKinsey B2B Customer Experience research [T2]
- Forrester 2026 State of Business Buying [T2]
- Qualtrics / Listen360 NPS detractor research [T2]

### B2B operator advocacy mechanism

Daily-operator dissatisfaction influences vendor decisions but with mechanism specifics:

- Operates through **vendor scorecards + renewal-cycle re-evaluation**, NOT initial vendor selection
- Decision weight structurally low: 11-stakeholder average B2B buying group; procurement / IT / clinical leadership dominate initial selection
- No documented mechanism for operator-initiated vendor switch
- Formal escalation channels exist but address performance under existing contract, not vendor identity

**Strategic implication:** "Cultivate Daily Operators as advocates" is valid for renewal-cycle retention, NOT for new-deal acquisition. Equip operators with scorecard-ready data (exception reports, comparison metrics) that survive procurement scrutiny.

**Sources:**
- ScienceDirect, multi-stakeholder vendor decision research [T1 peer-reviewed]
- Ivalua / Order.co vendor scorecard methodology [T2]
- CIO Magazine, enterprise software selection [T2]
- AORN healthcare perioperative nurse purchasing-power research [T2]
- Venminder vendor management research [T2]

### US loan agency decision-rights mechanics

Detailed structure of agent appointment in US credit agreements:

- **At LBO closing:** Sponsor + lead arranger drive; borrower CFO typically post-transaction (hired after deal), inherits the agent.
- **At refinancings:** CFO operationally leads (EY, AlixPartners confirmed) but sponsor retains agent-identity authority via board / equity vetoes embedded in credit and org documents. CFO influence is *operational engagement*, not *agent-identity authority*.
- **In private credit deals:** Lead lender appoints (Proskauer explicit on this). Lead-lender status earned via largest allocation, most accommodating terms, or strongest sponsor relationship.
- **For sub-agents (SRS Acquiom, Alter Domus, Wilm Trust, Kroll, CSC, Ocorian):** Administrative agent appoints unilaterally; no lender or borrower vote.
- **Successor agent (post-resignation):** Majority lenders appoint; borrower consents if not in default.

**Sources:**
- LSTA MCAPs (May 2023 + Jun 2025 draft) [T1]
- ABA Business Law Today (Apr 2025) [T1]
- Proskauer "Navigating the Club in Private Credit Deals" [T1]
- S&P Capital IQ Syndicated Loan Primer [T1-T2]
- Mayer Brown "Issues for Administrative Agent to Consider" [T2]
- Federal Reserve FEDS Notes (Feb 2024 + May 2025) [T1]
- OCC Bulletin 2023-17 [T1 binding] for bank-side distributed vendor authority

### PE-backed CFO context

- **Post-acquisition CFO churn:** 75%+ within 18-24 months (Accordion T2; 2019 industry survey >80%; Heidrick & Struggles 2024/2025 PE-CFO surveys)
- **Sub-$100M revenue CFO scope:** JM Search 2025 Compensation & Insights Study (n=300+, 83% investor-backed): Legal & Compliance oversight >60%; HR 55%; Operations 33%. The "all-the-hats CFO" framing is empirically supported for small PortCos.
- **Sponsor portfolio size:** Mid-market funds typically 10-20 active platforms per fund; firm-level across multiple vintages can reach 25-40 platforms at upper-MM and mega-cap.

### LSTA notice format standardization gap

- **Standardized:** Secondary trading documents (Par/Distressed Trade Confirms, Standard Settlement Form, Purchase & Sale Agreement, A&A Agreement). Revised suite published July 2023.
- **NOT standardized at the form level:** Operational notices (Borrowing, Interest Election, Conversion/Continuation, Repayment, Prepayment, Commitment Reduction) — these are credit-agreement exhibits drafted off LSTA MCAPs precedent, vary per deal.
- **LSTA acknowledges as structural inefficiency** justifying the Versana / Octaura industry-utility approach.
- McKinsey "Modernizing corporate loan operations": "expansion of OCR technologies faces challenges because of nonstandardized notice templates."

### Fedwire ISO 20022 migration impact

- **Cutover date:** 14 July 2025 (single-day cutover; Federal Reserve Bank Services T1)
- **Pre-migration:** ERI field ~9,000 chars with three modes; operators don't validate content
- **Post-migration:** Structured remittance enabled but not enforced; loan-specific schemas not mandated
- **Implication for personas:** David's remittance-structure pain is **declining over 3-5 year horizon**. Investment in standalone remittance-structure tooling is depreciating; cash-break-investigation workflows remain durable.

### Tool adoption by segment (PC + BDC + CLO)

- **Private credit:** Allvue → Broadridge Sentry → SS&C → S&P Wall Street Office
- **BDC:** Allvue → Broadridge Sentry → SS&C
- **CLO:** S&P WSO (primary) → Broadridge Sentry → Allvue
- **Fund admin (multi-segment):** Citco, SS&C, Apex, Alter Domus → Allvue
- **Secondary trading:** Octaura → Versana → Bloomberg AIM → ClearPar
- **Lead arranger ops:** Loan IQ (FIS) → ACBS (Fiserv) → Versana → ClearPar
- **KYC/AML:** Refinitiv World-Check → LexisNexis WorldCompliance → Dow Jones Risk & Compliance
- **Tax/Withholding:** Sovos TRR → Thomson Reuters OneSource → Tipalti → TAINA Tech

### Sponsor Cap Markets function existence

- **AUM threshold (best-available bracket — no exact public number):** Cap Markets function typically present at $1B+ AUM; transition zone $500M-$2B; absent below ~$500M.
- **Dominant Cap Markets workflow tool:** Termgrid. Adopted at KKR, EQT, TA Associates, Apax (4 of top-5 global PE firms). 7,000+ users. $50B+ transactions managed since 2021.
- **Tool stack correction:** Allvue and eFront are wrong-function for Cap Markets MDs (credit monitoring + LP reporting respectively). Termgrid + Chronograph are right.
- **Critical hierarchical insight:** MD-level Cap Markets professionals don't routinely log into admin agent portals; data work done by VPs/Associates and PortCo CFO reports.

## Use cases for this wiki entry

- **Persona design at related firms** (other third-party loan agents: Alter Domus, Kroll, Wilm Trust, CSC, Computershare, Ocorian)
- **B2B long-cycle market analysis** (memory durability + advocacy mechanism patterns generalize)
- **Loan-agency product strategy** discussions
- **Sales-motion segmentation** for private credit infrastructure
- **Reference for "decision rights" distinctions** in financial services contracts

## Sources appendix

Tier-1 / authoritative:
- LSTA (lsta.org) — Model Credit Agreement Provisions, market advisories, FAQ
- ABA Business Law Today (businesslawtoday.org)
- Federal Reserve Bank Services + FEDS Notes
- OCC Bulletin 2023-17 (third-party relationships)
- FinCEN (BOI reporting, AML/KYC guidance, private fund AML rule)
- IRS (Form W-8 series, Form 1042-S, Chapter 3/4 regs)
- S&P Capital IQ Syndicated Loan Primer
- FRBNY Staff Report 922 (Lead Arrangers)

Tier-2 / industry research:
- Proskauer, Mayer Brown, Cadwalader, Sullivan & Cromwell, Latham, Cleary Gottlieb, Davis Polk, Cahill (law firms)
- McKinsey ("Modernizing Corporate Loan Operations"; Global Private Markets Reports)
- Bain & Company (PE reports)
- Heidrick & Struggles (PE-Backed CFO Compensation Surveys 2022/2024/2025)
- Russell Reynolds (Portfolio Company CFOs)
- AlixPartners (PE Leadership Surveys)
- JM Search (2025 CFO Compensation & Insights Study)
- Accordion ("The CFO's First 100 Days")
- ACAMS (KYC/AML guidance)
- Forrester (2026 State of Business Buying)
- Qualtrics / Listen360 (NPS research)
- LSTA secondary commentary

Tier-3 (flagged for structural bias):
- SRS Acquiom, Alter Domus, Wilm Trust, CSC, Kroll, Ocorian, Computershare (third-party loan agent vendor materials)
- Refinitiv, LexisNexis, Dow Jones, NICE Actimize (KYC/sanctions vendors)
- Sovos, Thomson Reuters OneSource, Tipalti, TAINA Tech (tax-tech vendors)
- Allvue, Broadridge Sentry, SS&C, Citco, Apex (loan admin platform vendors)
- Termgrid, Chronograph (PE Cap Markets platforms)
- Octaura, Versana (industry consortium platforms)

## Cross-reference

- `loan-admin-tech-landscape.md` — adjacent tool/landscape research
- `private-credit-market.md` — adjacent market analysis
- `key-competitors-loan-admin.md` — adjacent competitive landscape

---

*Compiled 2026-05-12 from owner-built v1.2 persona package. Update with primary research findings when v2.0 is published.*
