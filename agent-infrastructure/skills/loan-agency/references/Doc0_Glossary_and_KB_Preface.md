# Glossary and Knowledge Base Preface

> *Document 0 of 6 — Loan Administration Knowledge Base*
> *This document is current as of February 16, 2026.*
> *Related documents: Doc 1 (Market Landscape); Doc 2 (Credit Agreement Interpretation); Doc 3 (Operational Mechanics); Doc 4 (Secondary Trading); Doc 5 (Tax Withholding); Doc 6 (Lifecycle Events)*

---

## Knowledge Base Preface

### 1. Purpose and Scope

This knowledge base is the foundational reference for [organization]'s loan administration operations. It covers both broadly syndicated loans (BSL) and private credit markets from the perspective of a third-party administrative agent, collateral agent, and escrow agent.

This KB does **not** cover fund administration — that is, NAV calculations, investor reporting for funds, or portfolio-level regulatory reporting for investment vehicles. Fund administration focuses on the investment fund holding the loans; loan agency focuses on the credit facility itself — managing cashflows, holding collateral, facilitating lender communications, processing trades, and administering the credit agreement.

This is a pure knowledge base. A separate training curriculum with exercises, case studies, and assessments will be built from this KB.

### 2. Audience

This knowledge base is designed for professionals joining [organization] across operations, relationship management, engineering, and product roles. It assumes:

- **General financial literacy:** understanding of interest rates, credit, basic accounting concepts, and financial market structure at a level consistent with a business degree or equivalent professional experience
- **No assumed loan market expertise:** the KB introduces syndicated lending concepts from foundational principles
- **No assumed legal expertise:** legal concepts (credit agreements, covenants, security interests) are explained in operational context, not as legal analysis
- **No assumed tax expertise:** tax withholding mechanics are explained procedurally for the agent's operational role, not as tax advisory content

Depth target: each document progresses from accessible foundations to full professional-grade detail. A reader who completes all six documents should possess near-expert knowledge of third-party loan administration operations.

### 3. Role-Based Reading Guide

| Role | Primary Documents | Secondary Documents |
|------|------------------|-------------------|
| Operations | Docs 3, 4, 5, 6 | Docs 1, 2 |
| Relationship Management | Docs 1, 2, 6 | Docs 3, 4, 5 |
| Engineering | Docs 3, 4, 6 (especially §12) | Docs 1, 2, 5 |
| Product | Docs 1, 2 | Docs 3, 4, 5, 6 |

While designed to be read in sequence, each document is independently useful as a reference.

### 4. Document Map

- **Doc 1: Market Landscape and Loan Products** — Market structure and size ($1.5T BSL, $1.7–3.5T private credit), product types (TLA, TLB, revolver, DDTL, unitranche, PIK, ABL), CLO mechanics and their operational implications, investor base composition, primary market syndication, industry infrastructure (ClearPar, Octaura), and the BSL/private credit convergence trend.

- **Doc 2: Credit Agreement Interpretation** — Documentation trends and the borrower-lender tension, EBITDA add-back mechanics and their credit risk implications, erroneous payment provisions (post-Citibank/Revlon), liability management transactions and landmark litigation (Serta, Mitel, Incora, J.Crew), DQ lists, amendment mechanics and sacred rights, negative covenant basket structures, and LSTA/LMA documentation architecture differences.

- **Doc 3: Operational Mechanics** — SOFR and benchmark rate mechanics (Term SOFR, SONIA, EURIBOR), day-count conventions (Actual/360, Actual/365), credit spread adjustments, payment system infrastructure (Fedwire, CHIPS, CHAPS, T2), borrowing request processing, excess cash flow sweeps, payment waterfalls, call protection conventions, ABL borrowing base administration, letter of credit mechanics, swingline lending, multi-currency facility operations, and loan identifier systems.

- **Doc 4: Secondary Trading and Settlement** — Par and distressed trade types, LSTA and LMA trade documentation, settlement workflows and timelines (T+7 target for par, T+20 for distressed), delayed compensation mechanics, buy-in/sell-out (BISO) provisions, settlement platforms (ClearPar, Octaura), DQ list and eligible assignee operational impact, and private credit secondary trading.

- **Doc 5: Tax Withholding and Lender Onboarding** — IRS form requirements (W-8BEN, W-8BEN-E, W-8IMY, W-8ECI, W-9), US withholding tax mechanics (Chapter 3, FATCA/Chapter 4), portfolio interest exemption, international withholding and treaty networks, UK/EU withholding regimes, HMRC DTTP scheme, 1042-S reporting, QI agreements, KYC/AML and CDD requirements, sanctions screening (OFAC, OFSI), ERISA considerations, and gross-up provisions.

- **Doc 6: Lifecycle Events and Agent Administration** — Administrative agent, collateral agent, and escrow agent roles and responsibilities, amendment and consent solicitation processing, refinancing and repricing operations, restructuring and workout mechanics, UCC filing and collateral monitoring, regulatory landscape (Basel III, BSA/AML, leveraged lending guidance), financial reporting and compliance certificate processing, deal onboarding checklists, lender portal management, insurance and hedge monitoring, agent technology stack, and professional development.

### 5. Document Conventions

The following conventions are used throughout the knowledge base:

**Jurisdiction tags:** Content specific to legal or regulatory jurisdictions is marked with tags:
- **[US]** — United States law, regulation, or market convention
- **[UK]** or **[UK/EU]** — United Kingdom and/or European Union law, regulation, or market convention
- **[EU]** — European Union specifically
- **[JURISDICTION-SPECIFIC]** — Content that varies materially by jurisdiction
- **[INTERNATIONAL]** — Content applicable across multiple jurisdictions

**Source citations:** Sources are cited in parentheses within the text. Key sources include the LSTA (Loan Syndications and Trading Association), LMA (Loan Market Association), PitchBook LCD, Octus/Covenant Review, and leading law firm publications (Mayer Brown, Cleary Gottlieb, White & Case, Cadwalader, Proskauer, and others).

**Cross-references:** References between documents use the format "Doc N, §M" (e.g., "Doc 3, §1" refers to Document 3, Section 1). Within a document, internal cross-references use "§M" or "Section M."

**BSL and Private Credit:** Content covers both markets in an integrated format. Where operational mechanics differ materially between BSL and private credit, differences are called out with **[PRIVATE CREDIT]** markers or dedicated subsections. Where no marker appears, the content applies to both markets.

### 6. [VERIFY] Tag Policy

This knowledge base is a living reference document. Data points that may change over time are tagged with [VERIFY] markers using a three-tier system:

**Tier 1 — Time-Sensitive** `[VERIFY: time-sensitive — reason]`
Data that changes with market conditions, regulatory action, or periodic updates. Examples: interest rates, trading volumes, market share percentages, regulatory deadlines, inflation-adjusted penalty amounts. Recommended verification cadence: quarterly for rates and volumes, annually for structural data.

**Tier 2 — Event-Driven** `[VERIFY: event-driven — pending event]`
Data contingent on a specific future event — litigation outcome, regulatory rulemaking, or legislative action. Monitor for resolution; when the event occurs, update the data and remove or reclassify the tag.

**Tier 3 — Stable Convention** (no tag)
Well-established market conventions, legal standards, or structural facts unlikely to change absent major market disruption. These are included in annual full-KB reviews but are not individually tagged.

Recommended verification sources by category:
- **Market data:** LSTA, PitchBook LCD, Bloomberg, Morningstar
- **Rates:** NY Fed (SOFR), CME Group (Term SOFR), Bank of England (SONIA), EMMI (EURIBOR)
- **US regulatory:** IRS, FinCEN, OFAC, OCC, SEC, CFTC
- **UK/EU regulatory:** HMRC, FCA, ECB, ESMA, AMLA
- **Legal developments:** Octus/Reorg, law firm client alerts

Tax and regulatory sections should be verified at least quarterly given the pace of change.

### 7. Regulatory Note

[Organization] currently operates as a non-trust-company, non-bank third-party loan agent. Regulatory obligations and compliance requirements described in this KB reflect this entity status. Content related to trust company chartering and bank-subsidiary models is included for context — particularly relevant when interacting with counterparties who operate under those frameworks, and as background for potential future entity structure decisions.

### 8. Update History

| Date | Sections Updated | Summary |
|------|-----------------|---------|
| February 16, 2026 | All | Initial publication |

---

## Glossary

The following terms are organized alphabetically. Each entry provides a concise operational definition and a reference to where the term is first introduced or most thoroughly discussed in the knowledge base.

---

### A

**ABL (Asset-Based Lending)** — A lending structure where borrowing capacity is determined by the value of specific collateral assets (receivables, inventory, equipment) rather than cash flow or enterprise value. The borrower's available credit fluctuates with the borrowing base calculation. *(First introduced: Doc 1, §9)*

**Accordion Facility** — See *Incremental/Accordion Facility*.

**Actual/360** — A day-count convention used for USD and EUR loan interest calculations. Interest accrues based on the actual number of days in the period divided by 360, meaning a full calendar year of interest exceeds the stated annual rate by approximately 1.4%. The standard convention for SOFR-based and EURIBOR-based loans. *(First introduced: Doc 3, §2)*

**Actual/365 (Fixed)** — A day-count convention used for GBP (SONIA-based) loan interest calculations. Interest accrues based on the actual number of days in the period divided by 365, regardless of whether the year is a leap year. *(First introduced: Doc 3, §2)*

**ADFlow** — An S&P Global entity data management platform supporting the loan trade settlement process by maintaining standardized entity identification data. Part of the ClearPar ecosystem. *(First introduced: Doc 1, §14)*

**Administrative Agent** — The entity appointed under the credit agreement to serve as the operational hub of a syndicated loan — processing payments, distributing notices, maintaining the lender register, coordinating amendments, and facilitating trade settlement. Called "Facility Agent" in LMA (UK/EU) documentation. The most operationally significant post-closing role in a syndicated facility. *(First introduced: Doc 1, §13; detailed treatment: Doc 6, §1)*

**Advance Rate** — In ABL facilities, the percentage of eligible collateral value that can be borrowed against. Standard advance rates are 80–85% for eligible receivables and 50–65% for eligible inventory (at net orderly liquidation value). *(First introduced: Doc 1, §9)*

**Agreed Currencies** — In multi-currency credit agreements under LSTA convention, the defined universe of currencies in which the borrower may draw loans. Called "Optional Currencies" under LMA convention, with the primary currency designated as the "Base Currency." *(First introduced: Doc 3, §10)*

**Agreement Among Lenders (AAL)** — The unitranche equivalent of an intercreditor agreement, governing the internal allocation between first-out and last-out tranches. The borrower sees a single blended rate and is typically unaware of the AAL's terms, which are confidential. Enforceability in bankruptcy remains untested. *(First introduced: Doc 1, §9)*

**Alternate Base Rate (ABR)** — A reference rate used for USD loans as an alternative to Term SOFR, typically defined as the highest of: the prime rate, the federal funds rate plus 50 basis points, and one-month Term SOFR plus 100 basis points. Used for swingline loans and as a fallback when SOFR is unavailable. *(First introduced: Doc 3, §9)*

**AMLA (Anti-Money Laundering Authority)** — The EU's new centralized AML supervisory authority, established under the AML Package adopted May 30, 2024, headquartered in Frankfurt. Will begin direct supervision of select high-risk obliged entities from July 2028. *(First introduced: Doc 5, §5)*

**Amendment** — A modification to the terms of a credit agreement, requiring consent from a specified percentage of lenders (typically Required Lenders for most changes, or all affected lenders for sacred rights matters). The administrative agent coordinates the consent solicitation, tabulation, and execution process. *(First introduced: Doc 2, §6; operational treatment: Doc 6, §2)*

**Anti-Cooperation Provision** — A credit agreement provision attempting to restrict lenders from entering into cooperation agreements with each other. Borrower response to the rise of lender cooperation agreements as a defensive tool against LME transactions. At least 13 attempts documented in 2025, with only 3 successful. *(First introduced: Doc 2, §4)*

**ARRC (Alternative Reference Rates Committee)** — The Federal Reserve-convened body that recommended SOFR as the replacement for USD LIBOR and developed the transition framework, including fallback language and credit spread adjustments. *(First introduced: Doc 3, §1)*

**Assignment and Assumption Agreement** — The standard document used to transfer a loan position from one lender (assignor) to another (assignee) in the US market. Upon execution and recording by the administrative agent, the assignee becomes a direct lender under the credit agreement. Contrasted with a participation, which does not create a direct lender relationship. *(First introduced: Doc 4, §3)*

**Assignment Fee** — A fee (typically $3,500) paid to the administrative agent to process a secondary market assignment. Covers the administrative cost of updating the lender register, collecting KYC/tax documentation, and recording the transfer. *(First introduced: Doc 4, §5)*

### B

**Backup Withholding** — US tax withholding at 24% applied to payments to US persons who fail to provide a valid W-9 or whose TIN cannot be verified. Distinct from NRA (nonresident alien) withholding under Chapters 3 and 4 of the IRC. *(First introduced: Doc 5, §2)*

**Base Rate** — See *Alternate Base Rate (ABR)*.

**BDC (Business Development Company)** — A publicly registered closed-end investment company under the Investment Company Act of 1940 that provides financing to small and mid-sized private companies. BDCs must invest 70% of assets in eligible portfolio companies and distribute 90%+ of taxable income. Total BDC industry assets reached approximately $475 billion as of Q1 2025. *(First introduced: Doc 1, §8)*

**Benchmark Replacement** — The contractual mechanism in credit agreements providing for automatic or streamlined transition from a discontinued benchmark rate to a successor rate. Post-LIBOR agreements include waterfall provisions specifying the replacement rate hierarchy. *(First introduced: Doc 3, §5)*

**Beneficial Owner** — For CDD purposes, any individual who owns 25% or more of a legal entity (ownership prong) or exercises significant management responsibility (control prong). For tax treaty purposes, the person with economic ownership of income — not merely a conduit or nominee. *(First introduced: Doc 5, §5)*

**BISO (Buy-In/Sell-Out)** — The LSTA's contractual remedy for failed trade settlements. If a trade remains unsettled beyond the trigger date (T+15 for par, T+50 for distressed), the performing party may initiate BISO to force economic settlement through a cover transaction. *(First introduced: Doc 4, §11)*

**Borrowing Base** — In ABL facilities, the calculation that determines the maximum amount a borrower may draw at any given time, based on the value of eligible collateral assets multiplied by their respective advance rates, less reserves. Borrowers submit periodic borrowing base certificates (typically monthly; weekly in stressed situations). *(First introduced: Doc 1, §9)*

**Borrowing Base Certificate** — A periodic report submitted by an ABL borrower to the administrative agent certifying the current value of eligible collateral and the resulting borrowing capacity. Includes detailed aging schedules and inventory reports. *(First introduced: Doc 1, §9)*

**Borrowing Request** — A formal notice from the borrower to the administrative agent requesting a new loan drawdown, specifying the amount, date, interest period, and applicable benchmark rate. Subject to conditions precedent including no-default certification and representation bring-down. *(First introduced: Doc 3, §6)*

**BSA/AML (Bank Secrecy Act / Anti-Money Laundering)** — The US regulatory framework requiring financial institutions to assist government agencies in detecting and preventing money laundering. Includes CIP, CDD, SAR filing, and CTR reporting obligations. *(First introduced: Doc 5, §5)*

**BSL (Broadly Syndicated Loan)** — A loan originated by one or more arranging banks and distributed to a broad group of institutional investors (CLOs, mutual funds, hedge funds, insurance companies, BDCs). Distinguished from private credit/direct lending by the breadth of the investor base, secondary market tradability, and standardized LSTA documentation. The US BSL market exceeds $1.5 trillion in outstanding volume. *(First introduced: Doc 1, §1)*

**Builder Basket** — A covenant basket that accumulates capacity over time based on Consolidated Net Income (CNI) or a similar measure, allowing the borrower to make restricted payments or investments as the company generates earnings. Present in over 91% of 2024 European SFAs. *(First introduced: Doc 2, §7)*

### C

**Call Protection** — Contractual provisions that impose a premium (soft call or hard call) on early repayment, compensating lenders for lost interest income. BSL standard: 101 soft call for 6 months on repricing transactions. Private credit standard: 102/101 hard call (2% year 1, 1% year 2) on any voluntary prepayment. *(First introduced: Doc 3, §7)*

**Cash Dominion** — An ABL mechanism where the borrower's cash collections are swept directly against the outstanding revolver balance, rather than remaining in the borrower's operating accounts. May be "full" (always active) or "springing" (activated when availability drops below a defined trigger). *(First introduced: Doc 1, §9)*

**CDD (Customer Due Diligence)** — The regulatory requirement under FinCEN's CDD Rule (31 CFR § 1010.230) for financial institutions to identify and verify the beneficial owners of legal entity customers. Distinct from the CTA/BOI reporting requirement, which is a separate parallel regime. *(First introduced: Doc 5, §5)*

**CEI (CUSIP Entity Identifier)** — A free, open-source 10-character code for identifying legal entities in the loan market, launched by CUSIP Global Services in August 2023 in collaboration with the LSTA and Versana. Competes with the Markit Entity Identifier (MEI). *(First introduced: Doc 3, §11)*

**Certain Funds** — A feature of UK/EU acquisition finance requiring committed financing at announcement with severely limited lender withdrawal rights, originating from the UK City Code on Takeovers and Mergers. The US equivalent relies on commitment papers with SunGard limited-conditionality provisions. *(First introduced: Doc 2, §8)*

**Change of Control** — A credit agreement event — typically an Event of Default — triggered when a specified ownership threshold changes hands. The exact definition is heavily negotiated and varies by deal. *(First introduced: Doc 2, §9)*

**CHAPS (Clearing House Automated Payment System)** — The UK's real-time gross settlement system for GBP payments, operated by the Bank of England. Operating hours: 6:00 a.m.–6:00 p.m. UK time. *(First introduced: Doc 3, §4)*

**CHIPS (Clearing House Interbank Payments System)** — A private-sector US payment system handling approximately $1.8 trillion in daily volume. Uses multilateral netting (settling roughly $1.8 trillion in payments against approximately $350 billion in actual fund transfers) and is critical for international USD payments. *(First introduced: Doc 3, §4)*

**CIM (Confidential Information Memorandum)** — The marketing document prepared by the arranger for prospective lenders during primary syndication. Maintained in "public side" (excluding MNPI) and "private side" (including management projections) versions. *(First introduced: Doc 1, §13)*

**CIP (Customer Identification Program)** — A BSA/AML requirement for financial institutions to verify the identity of customers opening accounts. LSTA guidelines establish that agent banks are generally not required to perform CIP on primary lenders, though many exceed legal requirements as a matter of policy. *(First introduced: Doc 5, §5)*

**ClearPar** — The dominant US secondary loan trade settlement platform, owned by S&P Global Market Intelligence. Processes over 2 million allocations annually across 4,400+ credits and 9,300+ facilities. Handles trade matching, allocation, documentation generation, and settlement workflow tracking — not trading itself. *(First introduced: Doc 1, §14; detailed treatment: Doc 4, §12)*

**CLO (Collateralized Loan Obligation)** — A securitization vehicle that pools syndicated loans and issues tranched debt securities (AAA through equity) backed by the loan portfolio's cash flows. CLOs hold 66–74% of all institutional leveraged loans and create layered operational complexity for loan agents through individually negotiated indentures with distinct OC/IC tests, concentration limits, and quality matrices. *(First introduced: Doc 1, §3; mechanics: Doc 1, §12)*

**CLO Blackout Period** — A period (maximum 5 consecutive business days) during which a CLO manager may not execute secondary trades, typically around quarterly reporting or payment dates. *(First introduced: Doc 4, Appendix)*

**Club Deal** — A syndicated loan pre-marketed to a small group of relationship lenders (typically $25M–$150M per lender) rather than broadly distributed. Features no market flex and is marketed as borrower-friendly. *(First introduced: Doc 1, §13)*

**CNI (Consolidated Net Income)** — The financial metric used as the basis for builder basket calculations. Different credit agreements define CNI differently, making precise calculation dependent on the specific agreement's definitions section. *(First introduced: Doc 2, §7)*

**Collateral Agent** — The entity holding security interests in the borrower's assets for the benefit of all secured parties. Under US (New York) law, the collateral agent holds liens directly; under UK/EU law, a security trustee holds security on trust. Core responsibilities include UCC filing maintenance, collateral release processing, and lien priority management. *(First introduced: Doc 6, §1)*

**Commitment Fee** — A fee paid by the borrower on the undrawn portion of a revolving credit facility, typically 25–50 basis points per annum (40–50% of the drawn spread margin). Compensates lenders for maintaining availability. Distinguished from a facility fee, which applies to the full commitment. *(First introduced: Doc 1, §9)*

**Compliance Certificate** — A formal borrower deliverable — typically signed by the CFO — certifying compliance with financial covenants and delivered with quarterly and annual financial statements. The agent reviews for completeness and timeliness, not for credit quality assessment. *(First introduced: Doc 6, §8)*

**Compounded in Arrears** — A rate-setting methodology where the benchmark rate is calculated by compounding daily overnight rates over the interest period, with the final rate not known until near the end of the period. Used for SONIA (GBP) and SARON (CHF). Contrasted with forward-looking term rates (Term SOFR, EURIBOR). *(First introduced: Doc 3, §3)*

**Concentration Limit** — In CLO indentures, restrictions on portfolio composition. Common limits include single obligor exposure (typically 2–2.5%), CCC-rated assets (typically 7.5%), and single industry caps across 33–40 industries. Each CLO has independently negotiated limits. *(First introduced: Doc 1, §12)*

**Consent Solicitation** — The process by which the administrative agent distributes a proposed amendment or waiver to lenders, collects votes, and tabulates results against the required approval threshold. Time-critical — missed deadlines can cause amendments to fail. *(First introduced: Doc 6, §2)*

**Continuation Vehicle** — In private credit secondaries, a structure where a GP creates a new vehicle, acquires a loan portfolio from an existing fund, and offers existing LPs the choice of cashing out or rolling into the new vehicle. The most common structure for private credit secondary transactions. *(First introduced: Doc 4, §14)*

**Cooperation Agreement** — An agreement among lenders to act collectively in responding to or defending against LME transactions. Emerged as lenders' primary defensive tool against creditor-on-creditor violence. Borrowers have responded with anti-cooperation provisions. *(First introduced: Doc 2, §4)*

**Covenant-Lite (Cov-Lite)** — A loan structure with no financial maintenance covenants, containing only incurrence-based tests that are triggered by specific borrower actions (e.g., incurring new debt) rather than tested periodically. Approximately 90%+ of new BSL institutional loans are cov-lite. *(First introduced: Doc 1, §6; detailed treatment: Doc 2, §1)*

**Credit Spread Adjustment (CSA)** — A fixed spread added to SOFR-based rates during the LIBOR transition to account for the structural difference between SOFR (a secured overnight rate) and LIBOR (an unsecured term rate that included bank credit risk). Standard values: 11.448 bps (1-month), 26.161 bps (3-month), 42.826 bps (6-month). Established via ISDA median calculation over March 2021. *(First introduced: Doc 3, §5)*

**Cross-Acceleration** — An Event of Default that triggers only upon actual acceleration or payment default under another debt agreement exceeding a threshold amount. More borrower-friendly than cross-default, which triggers upon default itself even without acceleration. Prevails in leveraged loans with strong sponsors. *(First introduced: Doc 2, §9)*

**Cross-Default** — An Event of Default triggered when the borrower defaults (or becomes entitled to acceleration) under another debt agreement exceeding a threshold amount, even if the other lender has not actually accelerated. More protective for lenders than cross-acceleration. *(First introduced: Doc 2, §9)*

**CRS (Common Reporting Standard)** — The OECD's global standard for automatic exchange of financial account information between tax authorities. Over 100 jurisdictions participate. Not a withholding regime — it is a reporting and information exchange framework. *(First introduced: Doc 5, §3)*

**CUSIP** — A 9-character alphanumeric identifier assigned to loan instruments by CUSIP Global Services (now managed by FactSet). The primary instrument-level identifier in the US syndicated loan market. Can only be initiated by the administrative agent for corporate loans. *(First introduced: Doc 3, §11)*

### D

**Daily Simple SOFR** — An overnight SOFR rate applied without compounding, used for swingline loans and certain short-duration borrowings where the administrative burden of compounding is impractical. Distinguished from compounded SOFR (used in some bond markets) and Term SOFR (forward-looking, used for most syndicated loans). *(First introduced: Doc 3, §1)*

**DDTL (Delayed Draw Term Loan)** — A term loan commitment that allows the borrower to draw funds during a specified availability period (12–24 months in BSL, up to 3–4 years in private credit), typically to fund add-on acquisitions. Unlike a revolver, amounts repaid cannot be reborrowed. Ticking fees apply on undrawn commitments. *(First introduced: Doc 1, §9)*

**Debt Domain** — A lender data room platform (now part of Citco) used for document management and communication in syndicated loan facilities. One of three major platforms alongside Intralinks and SyndTrak. *(First introduced: Doc 6, §10)*

**Defaulting Lender** — A lender that has failed to fund its share of a borrowing, is insolvent, or has been declared in default under the credit agreement. Defaulting lender provisions reallocate risk participations, require borrower cash collateralization of fronting exposure, and may strip voting rights. A centerpiece of the LSTA MCAPs. *(First introduced: Doc 3, §9)*

**Delayed Compensation** — Interest-like payments that accrue on the par amount of a secondary loan trade from the expected settlement date to the actual settlement date, compensating the party bearing cost-of-carry risk during settlement delays. Standard SOFR-based spread: Daily Simple SOFR plus 11.448 basis points. *(First introduced: Doc 4, §8)*

**Delta-One Transaction** — For purposes of Section 871(m), a derivative transaction with a delta of exactly 1.0 (i.e., its value moves one-for-one with the underlying US equity). Only delta-one transactions entered into on or after January 1, 2017 are currently in scope for dividend equivalent withholding. *(First introduced: Doc 5, §4)*

**DIP Loan (Debtor-in-Possession Loan)** — Financing provided to a company during Chapter 11 bankruptcy proceedings, enjoying superpriority administrative expense status. Subject to CLO concentration limits when held by CLO vehicles. *(First introduced: Doc 1, §12)*

**Discharge-for-Value Defense** — A legal defense (from *Banque Worms v. BankAmerica Int'l*, 1991) holding that a party receiving an erroneous payment need not return it if the payment discharged a valid debt and the recipient had no notice of the error. Largely neutralized by the LSTA erroneous payment provision, which requires lenders to expressly waive this defense. *(First introduced: Doc 2, §3)*

**Disqualified Lender (DQ)** — A person or entity prohibited from receiving assignments or participations of the borrower's loans under the credit agreement. Originally limited to competitors, DQ lists have expanded to include distressed debt investors, special situations funds, and "loan-to-own" funds. Assignments to DQ entities are typically not void but trigger borrower remedies. *(First introduced: Doc 2, §5; operational treatment: Doc 4, §13)*

**Diversity Score** — A CLO portfolio quality metric measuring obligor and industry diversification. Used in conjunction with WARF and WAS through the collateral quality matrix to determine compliance with indenture quality tests. *(First introduced: Doc 1, §12)*

**Dollar Equivalent** — The USD-converted value of non-USD borrowings in a multi-currency facility, used for availability calculations, covenant compliance testing, and pro rata sharing. Typically determined using the agent's spot rate at approximately 11:00 a.m. London time. *(First introduced: Doc 3, §10)*

**Dropdown** — An LME technique where assets (typically IP or other valuable collateral) are transferred from a loan party to an unrestricted subsidiary, removing them from the secured creditor group's collateral pool. The J.Crew transaction (2016–2017) was the landmark example. *(First introduced: Doc 2, §4)*

**DTTP (Double Taxation Treaty Passport)** — A UK HMRC scheme allowing foreign lenders to obtain a reference number that simplifies the process of securing treaty relief from UK withholding tax on interest payments. Passport validity is five calendar years. *(First introduced: Doc 5, §3)*

**Dutch Auction** — A mechanism in credit agreements allowing the borrower to repurchase its own loans through a reverse auction process where lenders submit prices at which they are willing to sell. Distinguished from open market purchases and privately negotiated transactions. *(First introduced: Doc 2, §4)*

### E

**EBITDA Add-Back** — An adjustment to the credit agreement definition of EBITDA that increases the calculated figure by adding back specified items (non-cash charges, restructuring costs, projected synergies). S&P research shows add-backs cause projected EBITDA to exceed actual realized EBITDA by approximately 30% on average. Caps at 25% of EBITDA are now present in 86% of deals. *(First introduced: Doc 2, §2)*

**ECF (Excess Cash Flow) Sweep** — A mandatory prepayment mechanism requiring the borrower to apply a percentage of excess cash flow (as contractually defined) to repay outstanding term loans. Typically uses tiered step-downs based on net leverage (75%/50%/25%/0%). Calculated annually and due approximately 90–130 days after fiscal year-end. *(First introduced: Doc 3, §7)*

**Eligible Assignee** — A credit agreement-defined class of entities permitted to receive loan assignments. The current market standard broadly permits any entity "regularly engaged in or established for the purpose of making, purchasing, or investing in loans, securities, or other financial assets." More restrictive definitions may apply to revolving commitments. *(First introduced: Doc 4, §13)*

**Equity Cure** — A right allowing a sponsor to inject equity into the borrower to cure a financial covenant breach. Near-universal in private credit sponsor-backed deals but largely irrelevant in BSL due to cov-lite dominance. Typically capped at 4–5 times over the facility life with no consecutive-quarter usage. *(First introduced: Doc 2, §9)*

**Erroneous Payment Provision** — A credit agreement clause (now effectively market standard post-Citibank/Revlon) giving the administrative agent sole discretion to determine whether a payment was erroneous, requiring lenders to return funds within two business days, and expressly waiving the discharge-for-value defense. *(First introduced: Doc 2, §3)*

**Escrow Agent** — An agent holding funds or documents in trust pending satisfaction of specified conditions. In loan administration, typically holds closing proceeds, collateral release payments, or amendment fees pending completion of conditions precedent. *(First introduced: Doc 6, §1)*

**EURIBOR (Euro Interbank Offered Rate)** — The benchmark rate for euro-denominated loans, administered by EMMI (European Money Markets Institute). Unlike LIBOR, EURIBOR has been reformed rather than replaced, with a hybrid methodology combining transaction data and expert judgment (Level 3 eliminated as of September 2024). Published for 1-week, 1-, 3-, 6-, and 12-month tenors. *(First introduced: Doc 3, §3)*

**Event of Default (EOD)** — A defined occurrence under the credit agreement that, upon notice or lapse of a cure period, entitles lenders to accelerate the loan and exercise remedies. Standard categories include non-payment, covenant breach, cross-default, insolvency, and change of control. *(First introduced: Doc 2, §9)*

**Excluded Taxes** — Under the LSTA gross-up framework, taxes that the borrower is not obligated to gross up. Four standard categories: net income taxes based on lender nexus, US withholding taxes in effect when the lender acquired its interest, taxes from lender documentation failure, and FATCA withholding. *(First introduced: Doc 5, §6)*

### F

**Facility Agent** — See *Administrative Agent*. The LMA (UK/EU) equivalent term.

**Facility Fee** — A fee paid on the full commitment amount (drawn plus undrawn) of a credit facility. Standard in investment-grade deals (10–25 bps), contrasted with commitment fees (paid only on undrawn amounts) which are standard in leveraged deals. *(First introduced: Doc 1, §10)*

**FATCA (Foreign Account Tax Compliance Act)** — US legislation (IRC §§ 1471–1474, Chapter 4) imposing 30% withholding on FDAP payments to foreign financial institutions and NFFEs that fail to meet reporting and documentation requirements. FATCA withholding is universally carved out from borrower gross-up obligations because compliance is within the lender's control. *(First introduced: Doc 5, §2)*

**FDAP (Fixed, Determinable, Annual, or Periodical Income)** — The category of US-source income subject to NRA withholding at 30% under IRC §§ 871(a)/881(a). Includes interest, dividends, rents, and royalties. Syndicated loan interest is FDAP unless a statutory exemption (portfolio interest, treaty) applies. *(First introduced: Doc 5, §2)*

**Fedwire** — The Federal Reserve's real-time gross settlement system for USD payments, processing approximately $4.7 trillion daily. Planned expansion to 22x6 operations by 2028–2029. The primary payment system for domestic syndicated loan payments. *(First introduced: Doc 3, §4)*

**FFI (Foreign Financial Institution)** — Under FATCA, a non-US financial institution subject to Chapter 4 obligations. Must register with the IRS, obtain a GIIN, and agree to due diligence and reporting requirements — or face 30% FATCA withholding on US-source payments. *(First introduced: Doc 5, §2)*

**Field Examination** — In ABL facilities, a periodic on-site audit of the borrower's collateral (receivables, inventory) conducted by the agent or a third-party firm. Required before initial funding and typically 1–2 times per year thereafter, with increased frequency when liquidity thresholds are breached. *(First introduced: Doc 1, §9)*

**FIGI (Financial Instrument Global Identifier)** — An open-source instrument identifier promoted by Bloomberg as an alternative to CUSIP. The LSTA has expressed concern because agents are not the exclusive applicants, creating risk of inaccurate data for frequently amended loans. *(First introduced: Doc 3, §11)*

**First-Out / Last-Out** — The internal tranche structure within a unitranche loan, governed by the AAL. First-out lenders (typically the revolver provider and a portion of the term loan) receive payment priority and accept a lower interest rate; last-out lenders (typically private credit providers) accept subordination in exchange for a higher rate. The borrower sees only a single blended rate. *(First introduced: Doc 1, §9)*

**Flex** — See *Market Flex*.

**Fronting Exposure** — The risk borne by an LC issuing bank or swingline lender when it advances 100% of funds to the beneficiary or borrower but holds only a portion of the ultimate credit risk, with the remainder participated to other syndicate lenders. Materializes when a participating lender fails to fund its share. *(First introduced: Doc 3, §8)*

### G

**GIIN (Global Intermediary Identification Number)** — A unique identifier assigned by the IRS to FFIs and their branches for FATCA compliance purposes. Required on W-8BEN-E forms. *(First introduced: Doc 5, §1)*

**Grower Basket** — A covenant basket formulated as the greater of a fixed dollar amount and a percentage of EBITDA or total assets, allowing capacity to grow with the borrower's earnings. Present in 96% of 2024 deals, with the average free-and-clear basket at 78% of pro forma adjusted EBITDA. *(First introduced: Doc 2, §7)*

**Gross-Up** — A contractual obligation requiring the borrower to increase a payment so the lender receives the same net amount it would have received absent withholding tax. Under the LSTA Indemnified Taxes/Excluded Taxes framework, the borrower grosses up for Indemnified Taxes but not for Excluded Taxes. *(First introduced: Doc 5, §6)*

### H

**Hard Call Protection** — A prepayment premium applicable to any voluntary repayment, regardless of purpose. Standard in private credit: 102/101 (2% in year 1, 1% in year 2). Distinguished from soft call protection, which applies only to repricing transactions. *(First introduced: Doc 3, §7)*

### I

**IC Test (Interest Coverage Test)** — A CLO compliance test verifying that interest income from the collateral portfolio is sufficient to cover interest obligations on the CLO's debt tranches. Formula: IC Ratio = Interest Income / Interest Due on Relevant Tranche plus All Senior Tranches. Failure triggers cash flow diversion. *(First introduced: Doc 1, §12)*

**Incurrence Covenant** — A covenant tested only when the borrower takes a specified action (e.g., incurring new debt, making an investment, paying a dividend), as opposed to a maintenance covenant tested periodically. The standard covenant structure in cov-lite loans. *(First introduced: Doc 1, §6)*

**Incremental/Accordion Facility** — Provisions allowing the borrower to add additional debt capacity to an existing credit facility. Works through three components: a fixed dollar "free and clear" basket (typically ~1.0x EBITDA), a prepayments prong, and an unlimited ratio-based basket subject to pro forma leverage compliance. *(First introduced: Doc 1, §9)*

**Indemnified Taxes** — Under the LSTA gross-up framework, all taxes imposed on or with respect to payments under the loan documents other than Excluded Taxes. The borrower bears the economic burden through a gross-up obligation. *(First introduced: Doc 5, §6)*

**Intercreditor Agreement (ICA)** — An agreement governing the relative rights, priorities, and remedies of different classes of creditors holding liens on the same collateral. In European transactions, the LMA intercreditor agreement is a standalone document with distinct structural features including turnover provisions. *(First introduced: Doc 2, §8)*

**Interest Diversion Test** — A CLO test distinct from OC/IC tests that applies during the reinvestment period with a higher trigger. Rather than paying down debt, diverted cash is used to purchase additional collateral. If the adjusted par balance drops below 102.5% of the AAA class, an event-of-default liquidation may be triggered. *(First introduced: Doc 1, §12)*

**Interest Period** — The discrete period (typically 1, 3, or 6 months) for which a SOFR-based or EURIBOR-based loan accrues interest at a fixed rate. At the end of each interest period, the borrower pays interest and elects a new interest period for the next accrual cycle. *(First introduced: Doc 3, §1)*

**Intralinks** — A lender data room platform (now part of SS&C Technologies) used as the primary document repository and communication channel between the administrative agent and the syndicate. Manages public-side/private-side information classification. *(First introduced: Doc 6, §10)*

**IRIS (Information Returns Intake System)** — The IRS's electronic filing platform that will become the sole system for 1042-S and other information return filings after FIRE is retired on December 31, 2026. Uses XML format and requires a TCC starting with "D." *(First introduced: Doc 5, §4)*

### J

**J.Crew Blocker** — A credit agreement provision designed to prevent the borrower from transferring valuable assets (particularly intellectual property) to unrestricted subsidiaries beyond the reach of secured creditors. Named after J.Crew's 2016–2017 transaction that exploited a "trap door" to transfer 72% of collected trademarks. Present in 39% of HY bond deals as of 2024. *(First introduced: Doc 2, §4)*

**Judgment Currency Clause** — A provision in multi-currency agreements requiring the borrower to indemnify lenders for any shortfall if a court renders judgment in a currency other than the agreement currency. Protects against redenomination risk. *(First introduced: Doc 3, §10)*

### K

**KYC (Know Your Customer)** — The identity verification and due diligence process performed on new lenders joining a syndicate or on borrowers at deal origination. Encompasses CIP (identity verification), CDD (beneficial ownership), and ongoing monitoring. *(First introduced: Doc 5, §5)*

### L

**LC (Letter of Credit)** — A bank's undertaking to pay a beneficiary upon presentation of conforming documents. In syndicated facilities, LCs are issued by a designated issuing bank with risk participated pro rata among all revolving lenders. Standby LCs (governed by ISP98) serve as performance guarantees; commercial LCs (governed by UCP 600) facilitate trade. *(First introduced: Doc 3, §8)*

**Lead Left Arranger / Bookrunner** — The bank that controls the syndication process — structuring the deal, maintaining the order book, controlling allocation, and setting price talk. The highest-ranking title in the arranger hierarchy. *(First introduced: Doc 1, §13)*

**LEI (Legal Entity Identifier)** — A 20-character alphanumeric code assigned to legal entities for regulatory reporting purposes, including under the Financial Data Transparency Act. Managed by the Global Legal Entity Identifier Foundation (GLEIF). *(First introduced: Doc 3, §11)*

**Lender Register** — The official record maintained by the administrative agent of all lenders, their commitment amounts, outstanding loan balances, and contact/payment information. The register is the definitive record of who owns what in the syndicate. *(First introduced: Doc 6, §1)*

**LMA (Loan Market Association)** — The UK/EU equivalent of the LSTA, publishing standard form documentation for European syndicated loans. Key structural differences from LSTA documentation include 66-2/3% voting thresholds, security trustee architecture, novation-based transfers, and "certain funds" provisions. *(First introduced: Doc 2, §8)*

**LME (Liability Management Exercise / Transaction)** — A transaction in which a borrower and cooperating majority lenders restructure debt in a manner that disadvantages minority lenders — sometimes called "creditor-on-creditor violence." Types include uptier exchanges (Serta), dropdowns (J.Crew), vote manipulation (Incora), and double-dip structures (At Home). *(First introduced: Doc 2, §4)*

**LSTA (Loan Syndications and Trading Association)** — The principal US trade association for the syndicated loan market, publishing standard form documentation (MCAPs, trade confirmations, standard terms), market data, and best practices. Membership includes banks, institutional investors, law firms, and service providers. *(First introduced: Doc 1, §1)*

**LSTA-ST (Standard Terms and Conditions)** — The LSTA's standardized terms governing secondary loan trade confirmations, published in separate versions for par/near-par trades and distressed trades. Trade confirmations incorporate these standard terms by reference. *(First introduced: Doc 4, §3)*

**LXID (LoanX ID)** — An S&P Global instrument identifier covering over 70,000 broadly syndicated loan instruments. Expanded to private credit instruments in June 2025. Linked to ISINs, RED Codes, and ratings data. *(First introduced: Doc 3, §11)*

### M

**MAC (Material Adverse Change)** — A significant negative change in the borrower's business, operations, or financial condition. Rarely viable as a standalone Event of Default — only one Delaware case (Akorn v. Fresenius, 2018) has ever found that a MAC occurred. *(First introduced: Doc 2, §9)*

**Maintenance Covenant** — A financial covenant tested periodically (typically quarterly) regardless of borrower actions, as opposed to an incurrence covenant tested only upon specified events. Standard in private credit, revolving facilities (via springing covenants), and ABL facilities. Examples: maximum leverage ratio, minimum interest coverage ratio. *(First introduced: Doc 1, §15)*

**Make-Whole Premium** — A prepayment premium calculated as the present value of future interest payments, discounted at the Treasury rate plus a spread (typically 50 bps). Common in high-yield notes and mezzanine debt, less common in syndicated loans. *(First introduced: Doc 3, §7)*

**Market Flex** — The contractual right of an arranger to modify loan terms (pricing, structure, covenants) to ensure successful syndication. Found exclusively in confidential fee letters. Typical pricing flex for first-lien TLBs: approximately 125–150 bps. Absent in club deals and private credit. *(First introduced: Doc 1, §13)*

**MCAPs (Model Credit Agreement Provisions)** — The LSTA's standardized provisions for US syndicated loan credit agreements, covering tax, yield protection, agency, assignment, defaulting lender, and other provisions. Most recently finalized May 1, 2023. *(First introduced: Doc 2, §1)*

**MEI (Markit Entity Identifier)** — A 10-digit code identifying legal entities across the loan ecosystem, now owned by S&P Global. Used in ClearPar for trade allocation and settlement. Faces competition from the newer CEI. *(First introduced: Doc 3, §11)*

**MFN (Most Favored Nation)** — A provision protecting existing lenders when incremental debt is added at a higher yield. If incremental all-in yield exceeds existing yield by more than a pricing cushion (typically 50 bps), the existing facility's margin automatically steps up. MFN sunset periods, when included, range from 6–18 months. *(First introduced: Doc 1, §9)*

**MNPI (Material Non-Public Information)** — Information about a borrower that is both material to an investment decision and not publicly available. The agent's classification of documents as public-side or private-side directly affects whether lender personnel can receive them without being "walled" from securities trading. *(First introduced: Doc 6, §10)*

### N

**Named Agent** — A third-party firm that appears directly in the credit agreement as the administrative agent, as opposed to a sub-agent operating behind a bank that retains the named role. The named agent model gives the third party full authority and visibility. *(First introduced: Doc 1, §11)*

**Negative Consent** — An amendment approval mechanism where lenders are deemed to consent unless they affirmatively object within a specified period (typically 5 business days). Used for Benchmark Replacement Conforming Changes and certain administrative amendments. *(First introduced: Doc 3, §10)*

**NFFE (Non-Financial Foreign Entity)** — Under FATCA, a foreign entity that is not an FFI. Active NFFEs (with less than 50% passive income) face reduced reporting obligations; passive NFFEs must certify their controlling persons. *(First introduced: Doc 5, §2)*

**Nostro Account** — An account held by a bank in a foreign currency at a correspondent bank in the relevant financial center. Multi-currency loan agents maintain nostro accounts in each approved currency for payment processing and require daily reconciliation. *(First introduced: Doc 3, §10)*

**Novation** — The LMA's primary transfer mechanism, which terminates the existing lender's obligations and recreates them in the name of the new lender. Contrasted with assignment (which preserves the original obligation). Novation can create security priority complications — a key structural difference from US assignment and assumption. *(First introduced: Doc 2, §8)*

### O

**OC Test (Overcollateralization Test)** — A CLO compliance test ensuring the par value of collateral assets exceeds the outstanding principal of CLO debt tranches. Uses an adjusted par balance that haircuts CCC-rated assets exceeding 7.5% of the portfolio. Failure triggers redirection of cash flows from junior to senior tranches. *(First introduced: Doc 1, §12)*

**Octaura** — A bank-backed electronic trading platform for secondary loans, founded April 2022. Grew from 0.6% to approximately 6% of secondary market volume between early 2024 and August 2025, with 27 dealers and 162 buy-side partners. The primary disruptor to the traditional voice-brokered market. *(First introduced: Doc 1, §14)*

**OFAC (Office of Foreign Assets Control)** — The US Treasury agency administering and enforcing economic sanctions programs. Maintains the SDN List and other sanctions lists that administrative agents must screen against at lender onboarding, payment processing, and periodically on an ongoing basis. *(First introduced: Doc 5, §5)*

**OFSI (Office of Financial Sanctions Implementation)** — The UK equivalent of OFAC, within HM Treasury. Maintains the UK Sanctions List and enforces autonomous UK sanctions post-Brexit as well as UN Security Council measures. *(First introduced: Doc 5, §5)*

**OID (Original Issue Discount)** — The discount from par at which a loan is initially issued, functioning as an upfront fee to lenders. BSL TLB OID typically ranges from 50–100 bps (issue price of 99.0–99.5). Private credit/BDC OID is typically 2–3% inclusive of fees. *(First introduced: Doc 1, §9)*

**Omni-Blocker** — A catch-all LME blocker provision prohibiting all forms of non-pro rata liability management transactions. The broadest category in the seven-type LME blocker taxonomy identified by White & Case. *(First introduced: Doc 2, §4)*

**Open Market Purchase** — A credit agreement provision historically permitting the borrower to repurchase its own loans "on the open market." The Fifth Circuit's Serta ruling held this requires purchase "on the secondary market for syndicated loans" — not via private negotiation. The Mitel decision distinguished this where the agreement used plain "purchase" language without an "open market" qualifier. *(First introduced: Doc 2, §4)*

### P

**Parallel Debt** — A structural device in European (particularly continental) secured lending where the security agent creates a mirror obligation owed to it individually, equal to the syndicate's aggregate claims. Security is then granted to secure this parallel debt, sidestepping problems arising from novation-based transfers and fluctuating beneficiary groups. *(First introduced: Doc 2, §8)*

**Par Trade** — A secondary loan trade priced at or near par value (typically 90 cents and above), settled using LSTA par/near-par trade documentation. The seller does not make representations about the creditworthiness of the borrower. Settlement target: T+7. *(First introduced: Doc 4, §2)*

**Participation** — A beneficial interest in a loan position where the participant does not become a direct lender under the credit agreement. The grantor (an existing lender of record) retains the legal position and votes; the participant has economic exposure but no direct relationship with the borrower or agent. LSTA participations are intended as true sales; LMA participations create a debtor-creditor relationship. *(First introduced: Doc 4, §4)*

**Payment Waterfall** — The contractual hierarchy specifying the order in which available funds are applied to various obligations (fees, interest, principal, by tranche seniority). In CLOs, the waterfall governs distribution of cash flows from the collateral pool through the capital structure. Ambiguous waterfalls are a major operational red flag. *(First introduced: Doc 6, §7)*

**PIK (Payment-in-Kind)** — A loan structure that capitalizes interest into principal rather than paying cash. Three main structures: full PIK, split/partial PIK, and PIK toggle (borrower elects cash or PIK each period). Approximately 14% of private credit loans in Q4 2024 included PIK optionality from inception. Primarily a private credit product. *(First introduced: Doc 1, §9)*

**Pillar Two (GloBE Minimum Tax)** — The OECD's global minimum corporate tax framework (15% effective rate). Does not directly alter withholding tax rates or mechanics but reshapes lender economics. Over 50 jurisdictions have implementing rules in effect. *(First introduced: Doc 5, §6)*

**Portfolio Interest Exemption** — An exemption from 30% US withholding tax under IRC § 871(h)/881(c) for interest paid on obligations that are "in registered form" and held by foreign persons who are not 10% shareholders, controlled foreign corporations receiving interest from a related person, or banks receiving interest on ordinary course loans. The cornerstone of cross-border syndicated lending tax efficiency. *(First introduced: Doc 5, §2)*

**Presumption Rules** — US tax provisions requiring withholding agents to apply a default withholding rate (typically 30%) when a payee's documentation is missing, invalid, or expired. An agent that fails to apply presumption rules bears independent liability under § 1461. *(First introduced: Doc 5, §2)*

**Price Talk** — The indicative pricing range communicated by the arranger to prospective lenders during primary syndication, signaling expected spread, OID, and other economic terms. *(First introduced: Doc 1, §13)*

**Private Credit** — Non-bank lending by institutional investors (direct lending funds, BDCs, insurance companies) directly to borrowers, typically without broad syndication. The market ranges from $1.7 to $3.5 trillion depending on definitional scope. Characterized by relationship-based lending, limited secondary liquidity, and (in most cases) stronger covenant protections than BSL. *(First introduced: Doc 1, §2)*

**Pro Rata** — The principle that payments and other distributions are shared proportionally among lenders based on their respective commitment or outstanding loan amounts. Pro rata sharing is a sacred right that historically could not be modified without unanimous consent — though LME transactions have tested this principle. *(First introduced: Doc 2, §6)*

**PSA (Purchase and Sale Agreement)** — The detailed agreement governing a distressed secondary loan trade, containing representations, warranties, and covenants beyond those in the standard trade confirmation. Required for distressed trades because the trade confirmation alone does not adequately address the complexities of distressed settlement. *(First introduced: Doc 4, §4)*

**PTE (Prohibited Transaction Exemption)** — A DOL exemption allowing ERISA-regulated entities to engage in transactions that would otherwise constitute prohibited transactions. Key PTEs for syndicated lending: QPAM (PTE 84-14), VCOC, and INHAM (PTE 96-23). *(First introduced: Doc 5, §5)*

**Public-Side / Private-Side** — The information classification system used in syndicated lending to manage MNPI. Public-side documents contain no material non-public information and can be accessed by lender trading desks. Private-side documents may contain MNPI and are restricted to personnel who have been "walled." Misclassification by the agent can taint trading personnel. *(First introduced: Doc 6, §10)*

### Q

**QI (Qualified Intermediary)** — A foreign intermediary that has entered into an agreement with the IRS (under Rev. Proc. 2022-43, current term through December 31, 2028) to assume primary withholding responsibility and report on a pooled basis rather than disclosing individual payee information. Simplifies intermediary chains in cross-border lending. *(First introduced: Doc 5, §4)*

**QPAM (Qualified Professional Asset Manager)** — Under PTE 84-14, an institutional manager (bank, insurance company, investment adviser with AUM exceeding $85 million) that enables ERISA-regulated entities to participate in syndicated loans without triggering prohibited transaction rules. *(First introduced: Doc 5, §5)*

### R

**Register** — See *Lender Register*.

**Reinvestment Period** — The initial period of a CLO's life (typically 4–5 years) during which the CLO manager actively trades — buying and selling loans and reinvesting principal repayments. After the reinvestment period, trading is severely restricted and proceeds pay down debt sequentially. *(First introduced: Doc 1, §12)*

**Repricing** — A transaction in which a borrower reduces the interest rate spread on an existing loan without changing other material terms. Typically requires soft-call protection periods to expire. The 2024 repricing wave saw $757 billion in institutional term loans repriced. *(First introduced: Doc 3, §7)*

**Required Lenders** — The approval threshold for most credit agreement amendments, typically defined as lenders holding more than 50% of aggregate commitments or outstandings (effectively 50.01%). Defaulting lenders and borrower-held loans are excluded from the denominator. The LMA equivalent ("Majority Lenders") is 66-2/3%. *(First introduced: Doc 2, §6)*

**Restricted Subsidiary** — A subsidiary whose assets, earnings, and activities are subject to the credit agreement's covenant restrictions. Distinguished from unrestricted subsidiaries, which are excluded from covenant calculations — creating potential for value leakage. *(First introduced: Doc 2, §7)*

**Reverse Flex** — The arranger's right to improve loan terms for the borrower (tighter spread, less OID) when a syndication is oversubscribed. The mirror image of market flex. *(First introduced: Doc 1, §13)*

**RFR (Risk-Free Rate)** — A category of benchmark rates based on overnight, near-risk-free transactions rather than term bank lending rates. SOFR, SONIA, SARON, and TONA are all RFRs that replaced or supplemented LIBOR-family rates. *(First introduced: Doc 3, §1)*

### S

**Sacred Rights** — Fundamental credit agreement provisions that require unanimous or all-affected-lender consent to modify. Typically cover: extending maturity, reducing interest, releasing substantially all collateral or guarantors, changing voting thresholds, and modifying pro rata sharing. Post-LME expansions have added lien subordination and "directly or indirectly" language. *(First introduced: Doc 2, §6)*

**SAR (Suspicious Activity Report)** — A BSA/AML filing required when a financial institution detects activity that may involve money laundering, terrorist financing, or other suspicious conduct. Filing obligations remain in effect regardless of CDD or CTA enforcement posture changes. *(First introduced: Doc 5, §5)*

**SARON (Swiss Average Rate Overnight)** — The overnight secured benchmark rate for Swiss franc, administered by SIX Swiss Exchange. Used on a compounded-in-arrears basis for CHF-denominated loans, with day-count convention Actual/360. *(First introduced: Doc 3, §10)*

**SDN List (Specially Designated Nationals and Blocked Persons List)** — OFAC's primary sanctions list. Administrative agents must screen against the SDN List at lender onboarding, payment processing, and periodically. The 50% Rule requires aggregation: entities 50%+ owned by SDN-listed persons are also blocked. *(First introduced: Doc 5, §5)*

**Section 163(j)** — The IRC provision limiting the deductibility of business interest expense to 30% of adjusted taxable income. The OBBBA permanently restored the EBITDA basis (adding back depreciation, amortization, and depletion), effective for tax years beginning after December 31, 2024, significantly increasing deductible interest capacity for leveraged borrowers. *(First introduced: Doc 5, §6)*

**Security Trustee** — In UK/EU (LMA) documentation, the entity holding security on trust for a fluctuating body of lender beneficiaries. The equivalent of the US collateral agent, but structured differently due to the English law trust framework. May require parallel debt mechanics in continental European jurisdictions. *(First introduced: Doc 2, §8)*

**Serta Blocker** — A credit agreement provision requiring affected-lender consent for uptier transactions — designed to prevent a Serta-style exchange where majority lenders cooperate with the borrower to subordinate minority lenders. Present in approximately 70.9% of loans as of Q2 2024. *(First introduced: Doc 2, §4)*

**Snooze/Lose** — An LMA provision (not typical in US documentation) under which a lender that fails to respond to an amendment request within the specified period is deemed to have consented. *(First introduced: Doc 2, §6)*

**SOFR (Secured Overnight Financing Rate)** — The primary benchmark rate for USD syndicated loans, published daily by the NY Fed based on approximately $2 trillion in daily repo transactions. SOFR is a secured overnight rate — structurally different from LIBOR, which was an unsecured term rate. Overnight SOFR was 3.65% as of February 2026. *(First introduced: Doc 3, §1)*

**SOFR Floor** — A minimum SOFR rate specified in the credit agreement, below which the rate cannot fall for interest calculation purposes. Standard in leveraged loan documentation (typically 0% or 0.50–0.75%), though generally not in-the-money at current rate levels. *(First introduced: Doc 1, §5)*

**Soft Call Protection** — A prepayment premium (typically 101, or 1%) applicable only to repricing transactions within a specified period after closing (6 months in 53% of deals, 12 months in 40%). Distinguished from hard call protection, which applies to any voluntary prepayment. *(First introduced: Doc 1, §9)*

**SONIA (Sterling Overnight Index Average)** — The overnight unsecured benchmark rate for GBP, published by the Bank of England based on overnight wholesale deposit transactions. Used on a compounded-in-arrears basis for sterling-denominated loans, with day-count convention Actual/365 Fixed. *(First introduced: Doc 3, §3)*

**Springing Covenant** — A financial maintenance covenant in a revolving credit facility that activates only when utilization exceeds a specified threshold (typically 35–40% of commitments) at quarter-end. Only revolving lenders can enforce the springing covenant; term loan lenders have no rights. *(First introduced: Doc 1, §9)*

**Sub-Agent** — A third-party firm that performs loan administration functions under delegation from the named agent bank, rather than appearing directly in the credit agreement. The named agent retains the legal role and certain approval authorities. *(First introduced: Doc 1, §11)*

**Successor Agent** — A new administrative agent that steps in when the existing agent resigns or is replaced. Increasingly common during restructurings and LME transactions. The transition requires rigorous position reconciliation, document transfer, and parallel processing periods. *(First introduced: Doc 1, §11; operational treatment: Doc 6, §9)*

**SunGard Provisions** — Limited-conditionality provisions in US acquisition financing commitment papers (named after the 2005 SunGard Data Systems deal) that restrict the conditions under which a lender can decline to fund. The US equivalent of the European "certain funds" concept. *(First introduced: Doc 2, §8)*

**Swingline Loan** — A short-term borrowing (typically 1–10 business days) funded by a single designated lender (usually the administrative agent bank) for same-day liquidity within a revolving credit facility. Bears interest at ABR or Daily Simple SOFR (not Term SOFR). Sublimits are generally 5–10% of total revolving commitments. *(First introduced: Doc 3, §9)*

**SyndTrak** — A lender data room and syndicated loan workflow platform (now part of Finastra) used for document management and communication in loan facilities. *(First introduced: Doc 6, §10)*

### T

**T2 (TARGET2)** — The Eurosystem's real-time gross settlement system for EUR payments, operating 7:00 a.m.–6:00 p.m. CET. *(First introduced: Doc 3, §4)*

**Term Loan A (TLA)** — A pro rata loan tranche with 5–10% annual amortization, 5–6 year maturity, and financial maintenance covenants. Held by commercial and investment banks as part of relationship lending. Spreads tighter than TLB. *(First introduced: Doc 1, §9)*

**Term Loan B (TLB)** — The dominant leveraged loan product. Features minimal amortization (typically 1% per annum with 93%+ as a bullet at maturity), 5–7 year maturity, and institutional investor base (CLOs, mutual funds, hedge funds, BDCs). Approximately 90%+ are covenant-lite. *(First introduced: Doc 1, §9)*

**Term SOFR** — A forward-looking term rate derived from SOFR futures, published by CME Group for 1-, 3-, 6-, and 12-month tenors. The dominant benchmark for USD syndicated loans because it is known at the start of each interest period, enabling straightforward borrower notification and accrual. CME's Term SOFR license requires annual fees. *(First introduced: Doc 3, §1)*

**Ticking Fee** — A fee charged on undrawn DDTL commitments, typically starting at 50% of the applicable margin and ratcheting to 100% after 6–12 months. Some deals feature a 3–6 month ticking fee holiday. *(First introduced: Doc 1, §9)*

**TONA (Tokyo Overnight Average Rate)** — The overnight unsecured benchmark rate for Japanese yen, used for JPY-denominated loans. Published by the Bank of Japan. *(First introduced: Doc 3, §10)*

**Trade Confirmation** — The document memorializing a secondary loan trade, incorporating the applicable LSTA Standard Terms by reference. The LSTA publishes separate confirmation forms for par/near-par and distressed trades. The LMA uses a single confirmation with checkbox elections for par or distressed. *(First introduced: Doc 4, §3)*

**Turnover Provision** — In LMA intercreditor agreements, a provision requiring a creditor that receives a payment in excess of its entitled share to "turn over" the excess to the security trustee for redistribution according to the agreed priority waterfall. *(First introduced: Doc 2, §8)*

### U

**UCC (Uniform Commercial Code) Filing** — A public notice filed under UCC Article 9 to perfect a security interest in personal property collateral. Initial UCC-1 filings must be continued every five years through UCC-3 continuation statements, or the security interest lapses. A missed continuation filing can destroy hundreds of millions of dollars in collateral value. *(First introduced: Doc 6, §1)*

**UCP 600 (Uniform Customs and Practice for Documentary Credits)** — The ICC rules governing commercial (documentary) letters of credit, requiring presentation of specified shipping documents as a condition of payment. Distinguished from ISP98, which governs standby LCs. *(First introduced: Doc 3, §8)*

**Unitranche** — The dominant product in private credit/direct lending, providing single-tranche financing with a blended senior/junior interest rate. The borrower sees one rate; the internal first-out/last-out allocation is governed by the AAL. Routinely supports $1 billion+ deals. *(First introduced: Doc 1, §9)*

**Unrestricted Subsidiary** — A subsidiary designated as outside the credit agreement's covenant framework. Assets, earnings, and activities of unrestricted subsidiaries are excluded from financial covenant calculations. Can be exploited for asset transfers (the J.Crew "trap door") — hence the emergence of J.Crew blocker provisions. *(First introduced: Doc 2, §7)*

**Uptier Exchange** — An LME transaction in which majority lenders exchange their existing debt for new superpriority debt that ranks ahead of non-participating lenders' claims. The Serta Simmons transaction (2020) was the landmark example, subsequently reversed by the Fifth Circuit. *(First introduced: Doc 2, §4)*

**Upstream Shield** — A BISO provision unique to distressed trades that protects a seller who has performed all obligations but cannot settle because its own upstream counterparty has not delivered. The open upstream trade must have a trade date not later than 5 business days after the downstream trade date. *(First introduced: Doc 4, §11)*

### V

**Versana** — A loan data and analytics platform working with the LMA and industry participants on loan data standardization and digitization initiatives. *(First introduced: Doc 1, §14)*

### W

**W-8BEN** — IRS form used by foreign individuals to claim treaty benefits and certify non-US tax status for Chapter 3 purposes. Expires at the end of the third succeeding calendar year. *(First introduced: Doc 5, §1)*

**W-8BEN-E** — IRS form used by foreign entities to certify non-US status, claim treaty benefits, and provide FATCA classifications (Chapter 4 status, GIIN). The most operationally complex of the W-8 series, with 30 parts covering multiple entity types and FATCA categories. *(First introduced: Doc 5, §1)*

**W-8ECI** — IRS form used by foreign persons receiving income effectively connected with a US trade or business (ECI). ECI is exempt from NRA withholding but subject to net-basis US income tax. Valid for three calendar years. *(First introduced: Doc 5, §1)*

**W-8IMY** — IRS form used by foreign intermediaries, flow-through entities, and certain US branches to provide withholding information. Must be accompanied by a withholding statement allocating payments to beneficial owners, with underlying W-8 or W-9 forms attached. *(First introduced: Doc 5, §1)*

**W-9** — IRS form used by US persons to certify their taxpayer identification number. Required from all US lenders in a syndicate. Failure to provide a valid W-9 triggers 24% backup withholding. *(First introduced: Doc 5, §1)*

**WAL Test (Weighted Average Life Test)** — A CLO portfolio quality test limiting the maximum weighted average remaining maturity of the loan portfolio, with the cap typically stepping down as the CLO ages. Prevents the manager from loading the portfolio with long-dated assets late in the CLO's life. *(First introduced: Doc 1, §12)*

**WARF (Weighted Average Rating Factor)** — A Moody's credit quality metric used in CLO compliance testing. Lower WARF indicates higher portfolio quality. Typical range: 2,000–3,000. Interacts with WAS and diversity score through the collateral quality matrix. *(First introduced: Doc 1, §12)*

**WAS Test (Weighted Average Spread Test)** — A CLO portfolio quality test requiring the portfolio to maintain a minimum weighted average interest rate spread. Ensures the portfolio generates sufficient income to service the CLO's debt tranches and equity distributions. *(First introduced: Doc 1, §12)*

**Waterfall** — See *Payment Waterfall*.

**White-Label** — An arrangement where a third-party loan agent provides administrative services under the branding of a bank or other financial institution. A hybrid between the named agent and sub-agent models. *(First introduced: Doc 1, §11)*

**Withholding Agent** — Under IRC § 7701(a)(16), any person required to deduct and withhold tax from payments to foreign persons. Administrative agents in syndicated loans serve as withholding agents and bear independent statutory liability for correct withholding under § 1461. *(First introduced: Doc 5, §2)*

**WSO (Wall Street Office)** — An S&P Global loan servicing platform that is industry-dominant for loan accounting, payment processing, and position management. Handles interest accrual, payment waterfall processing, position tracking, rate resets, fee billing, and register maintenance. *(First introduced: Doc 6, §12)*

### Y

**Yank-a-Bank** — A credit agreement provision allowing the borrower to replace a lender that has defaulted, become insolvent, requested increased costs, or refused to approve an amendment approved by Required Lenders on a sacred rights matter. The replaced lender assigns at par. Seldom deployed in practice — functions primarily as a deterrent to holdout behavior. *(First introduced: Doc 2, §6)*

**Yankee Loan** — A loan structured by European sponsors to access the US institutional investor market, typically using NY law-governed, HY bond-style covenant packages as schedules to an English law LMA-form loan agreement. A key example of LSTA/LMA documentation convergence. *(First introduced: Doc 2, §8)*

---

*Cross-references: All terms reference their primary document and section. For comprehensive treatment of any topic, consult the referenced document section.*
