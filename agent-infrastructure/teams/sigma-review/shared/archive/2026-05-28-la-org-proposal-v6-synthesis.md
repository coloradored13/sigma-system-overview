# Loan Agency Product and Engineering Organization
## Building to Compete

**Prepared for:** Jessica Glaser, Head of Product, Loan Agency; Senior Director of Engineering; SRS Acquiom Executive Leadership
**Author:** Brad Gilbert, Senior Product Manager, Loan Agency Applications
**Date:** May 2026
**Status:** Draft for Alignment

---

## Executive Summary

The Loan Agency business line operates under a compounding constraint that this proposal addresses directly. Between year-end 2023 and April 2026, operations headcount grew from 22 to 45 people while active deal count grew from 237 to 483 — a consistent one-to-one ratio. At that rate, reaching 600 to 800 active deals implies an operations team of 56 to 76 people. Loan Agency Operations generates more than 6,200 support interactions per year — each one a client reaching for information or a routine action that a self-service portal would let them complete without contacting Operations. Tax operations alone consumes 40 to 50 hours per month in manual reconciliation, plus more than 80 hours at year-end. The engineering investment proposed here is sized to break those patterns before they compound further.

The same capabilities that eliminate the operational tax are the capabilities that close the competitive gap. The Loan Agency Dashboard today provides read-only access in a market where leading competitors offer write capability, proactive notifications, and customizable reporting. Named clients have stated that they cannot expand their relationship with SRS Acquiom until the technology closes that gap. The structural change proposed here — splitting the current single team into a Client Experience team and a Loan Operations Platform team — is what allows both tracks to execute in parallel rather than competing for attention in the same two-week sprint. The primary Year 1 ask is engineering capacity: six engineers per team at launch, growing toward eight to ten per team by end of Year 1, with a two-year target of 26 to 30 people across the full function.

---

## Strategic Context

### The Operational Case

SRS Acquiom's Loan Agency book stands at 461 active deals representing $84.3 billion in active commitments, served across more than 4,400 distinct lender participations.⁰ In the trailing twelve months, the business processed roughly 54,000 outgoing wire payments and closed 8,800 lender assignments. In the most recent six-month window, the Loan Agency Dashboard generated 1,400 notice resend requests and 1,740 position and reporting tickets — annualizing to roughly 6,280 across the lender base. Each of those interactions is a client doing by phone or email what a portal with current-generation capabilities would let them do themselves.

The 22-to-45 operations headcount growth over the past two and a half years is a visible, auditable record of what happens when deal volume grows without platform investment. Absent structural change, every 100 additional deals implies roughly 10 additional operations staff. At fully-loaded costs, that is $700,000 to $1 million per 100 deals in headcount the engineering investment is designed to avoid. The tax operations manual burden — 40 to 50 hours per month plus more than 80 hours at year-end — is separately quantifiable and does not depend on any competitive claim.

This is the primary approval basis for this proposal. The platform investment funds capabilities clients would self-serve; every capability shipped reduces the operational overhead of the current manual-response model.

### The Competitive Case

The operational investment also funds the competitive capability build the market requires. Client expectations have moved beyond reports delivered by email. Named clients have explicitly stated that technology gaps are blocking relationship expansion. The window in which platform investment can change competitive position is open, but the competitive landscape is not standing still.

Three external transitions sharpen the urgency. WSO sunsets in June 2026. The IRS retires the FIRE filing system in favor of IRIS on December 31, 2026 — making IRIS-native tax infrastructure a compliance requirement, not a competitive option, for Tax Year 2026 returns due March 15, 2027. And Versana, the real-time digital data platform backed by JP Morgan, Bank of America, Morgan Stanley, Citi, Wells Fargo, Deutsche Bank, Barclays, and BNP Paribas, closed a $43 million raise in April 2026 and is actively expanding into private credit and European markets. As Versana's network reaches SRS Acquiom's deal tier over the next 18 to 36 months, lenders holding positions across Versana-connected agents and SRS Acquiom-agented deals will experience a visible difference in real-time data access. Integration is an architecture priority in Year 1 and a production deliverable in Year 2.

### Alternatives Considered and Rejected

The proposal considered whether the competitive ambition could be met without structural change.

*Maintain the current single team with better prioritization.* The mixed-backlog pattern that paused Loan Agency Dashboard development for approximately twelve months during the DLX migration is structural, not disciplinary. A 45-person operations team generating more than 3,000 support interactions per six-month window competes for sprint capacity against external clients who are not present in planning — the internal team is physically present in standups; lenders are not. This incentive structure will reassert itself under the next operational urgency regardless of stated prioritization intent. The IRS IRIS transition is already queued.

*Add engineers to the existing team without splitting it.* This preserves the same incentive structure and produces the same outcome unless PM and track discipline enforces a separation that is, in practice, equivalent to the structural split proposed here — and that requires the same executive endorsement.

*Buy or partner for portal capability.* No white-label loan agency portal exists at the competitive depth required. Alter Domus's CorPro portal has been integrated into their platform since the 2018 Cortland acquisition. GLAS and Kroll operate proprietary platforms. Versana provides data distribution infrastructure that complements an agent portal but does not substitute for one.

*Process redesign, offshoring, or vendor automation.* Alternatives considered and rejected for material reasons — including process redesign, offshoring, and vendor automation — are addressed under Risks and Mitigations.

---

## Competitive Landscape

The loan agency market is consolidating around platform-driven competitors, and the competitive picture has accelerated meaningfully in the past twelve months. Three dynamics define the current landscape for any firm competing in middle-market BSL and direct lending.

**Alter Domus** is the largest third-party loan agent in the US and globally by assets under administration, a position it has held since its 2018 acquisition of Cortland Capital Market Services brought Cortland's loan agency operations, client portal (CorPro), and Agency360 platform fully under the Alter Domus umbrella. That integration has had eight years to mature. Agency CorPro — the dedicated portal for loan agency data — sits within Alter Domus's Vega technology suite alongside Agency360, CorTrade (trade settlement), and DealFact (covenant tracking), all accessible through a single client login. The firm processed more than 100,000 wire payments in a single peak day in 2025 and in February 2026 won a $30 billion CLO mandate from Bain Capital that required replacing two incumbent providers simultaneously.¹ The benchmark SRS Acquiom is competing against is not where Alter Domus was in 2018; it is where Alter Domus is today.

Alter Domus also competes as an integrated fund administration and loan agency provider — PE-backed clients can engage Alter Domus for both services through a single relationship. SS&C similarly offers loan administration for private debt funds as an active service line alongside its fund-administration business.¹³ For the PE-backed portion of SRS Acquiom's book, this creates a bundled-service competitive dynamic that a pure-agency provider cannot match without a partnership or product expansion: the client's fund administrator can offer to absorb the loan agency relationship as an add-on. Retaining these clients requires demonstrating loan-agency depth — portal capability, self-service workflow, data integration — that a fund administrator cannot replicate by adding an adjacent service line. The org expansion in this proposal is therefore a retention play against bundled competitors, not only a market-share play against pure-agency peers. Carta's October 2025 acquisition of private credit loan administrator Sirvatus, integrating loan operations directly into its fund accounting platform, signals that tech-native fund administrators are closing the distance between fund-side reporting and deal-level loan operations — a convergence path that could eventually extend to administrative agency services.¹⁷

**Kroll** competes directly in the US middle market, not only in Europe. Bloomberg ranked Kroll the third-largest administrative agent in the US in Q1 2025, and Kroll describes itself as the number-one third-party agent for loan settlements, with an average settlement time of eight days against a market median of eleven.² Kroll's middle-market private credit and BSL practice spans acquisition finance, unitranche, and syndicated structures. In November 2025, Kroll acquired Madison Pacific to build out APAC coverage, extending an international platform that already operates across the US and EMEA. Kroll's operating entity is UK-incorporated without a US trust charter, which is relevant to bank-lender TPRM documentation requirements on bank-arranged BSL transactions, but it is an active US competitor in private credit and direct lending.

**GLAS** completed a January 2026 recapitalization led by Oakley Capital (majority) and La Caisse (minority), valuing the firm at approximately $1.35 billion.³ The investment thesis was explicit: technology and AI capability development, M&A, and international expansion including the Americas. GLAS attributes 40% organic revenue growth to its tech-enabled platform and manages more than $750 billion in assets under administration daily across ten jurisdictions. Importantly, GLAS has operated as a US-chartered trust company (New Hampshire, regulated since 2017) for nine years — describing GLAS as a European competitor materially understates its US regulatory standing. Its January 2026 acquisition of LAS Italy added Rome and Milan operations. GLAS is moving toward the US middle market and is not a settled European-only competitor.

**Wilmington Trust** holds a position anchored in its M&T Bank trust charter and a team averaging more than fifteen years of industry experience across 1,100+ syndicated loan deals. The firm is investing in technology — a February 2025 partnership with AccessFintech's Synergy platform enables real-time data sharing across agents, lenders, CLO trustees, and administrators, and the firm has articulated six CLO technology themes for 2026 including electronification, STP, and LME processing efficiency. Wilmington is meaningfully behind Alter Domus and GLAS on external portal capability and lender self-service depth, but the gap is narrowing through partnerships rather than proprietary development.

**CSC**, a 125-year-old corporate services firm, operates as a third-party administrative agent across private credit, cross-border, and syndicated facilities — offering notice delivery, cash management, successor agent, and collateral agent services from a global footprint of more than 140 offices.¹⁴ CSC's December 2025 private credit report, citing that 88 percent of fund managers expect to increase use of third-party loan agents, signals an active push into the same middle-market and direct-lending client base SRS Acquiom serves. CSC's competitive advantage is multi-service client relationships spanning fund administration, SPV management, and loan agency; SRS Acquiom's is the depth of loan-agency specialization a multi-line corporate services firm cannot match.

**Ocorian**, a UK-headquartered loan agency provider, has expanded its US private markets footprint through two acquisitions in twelve months — EdgePoint Fund Services in December 2024 and E78 Fund Solutions in August 2025 — and explicitly markets loan agency services for middle-market direct lending and syndicated loans across the Americas.¹⁵ Ocorian operates without a US trust charter, the same regulatory posture as Kroll; its competitive momentum comes from acquisitive scale and cross-border footprint rather than chartered standing.

**Beyond the named six**, two additional competitive dynamics matter for SRS Acquiom's positioning.

The first is the expansion of trust-chartered bank custodians into the middle market. Computershare, having acquired Wells Fargo's corporate trust business in 2021, now administers $6.6 trillion in debt and is the largest CLO trustee in both the US and Europe.¹¹ Its US trust charter is the same TPRM-relevant credential Wilmington Trust holds — material for bank-arranged BSL where third-party-risk-management rules favor chartered counterparties. December 2025 industry research publication and active CTSLink portal investment signal that Computershare is treating middle-market CLO and BSL as growth segments, not maintenance segments. US Bank Global Corporate Trust holds the same CLO trustee position and scale. Neither firm competes with SRS Acquiom on exactly the same deal set today, but both are moving as private credit and BSL volume grows — and both arrive with chartered standing and existing lender relationships that SRS Acquiom would need to earn from scratch.

The second is the emergence of data infrastructure that sits between agents and their clients. **Versana**, backed by JP Morgan, Bank of America, Morgan Stanley, Citi, Wells Fargo, Deutsche Bank, Barclays, and BNP Paribas (which led a $43 million raise in April 2026 bringing total capital raised to over $125 million), has built a real-time digital data platform streaming position data, notice information, and reconciliation directly from agent ledgers to lender systems via API.⁴ Active facility coverage exceeds $4.1 trillion across more than 6,000 facilities. Versana's Reconciliation Module enables lenders to electronically match their positions against agents' source data in real time. For lenders holding positions across Versana-connected agents and SRS Acquiom-agented deals, SRS Acquiom's current absence from Versana creates a visible gap in portfolio data access. Versana's April 2026 raise is explicitly earmarked for expansion into private credit and Europe — SRS Acquiom's core deal tier — making integration an architecture priority in Year 1 and a production deliverable in Year 2.

**PactFi**, a private credit syndication network that has supported more than $300 billion in deal volume across 250+ counterparties and 3,000+ fund entities since 2023, raised a $25 million Series A in March 2026 and disclosed a funded roadmap to extend its workflow coverage beyond deal close into post-close servicing.¹⁶ PactFi today connects eight of the top twenty credit asset managers and is the de facto syndication rail for a significant segment of upper-middle-market direct lending. If its post-close roadmap reaches general availability before SRS Acquiom completes its lender-facing self-service build, the disintermediation risk is concrete: the same network that routes deal origination could absorb post-close agent workflow. The 24-to-36-month capability milestones in this proposal are explicitly designed to close that window.

**S&P Global's March 2026 launch of DataXchange and AmendX** — centralized notice delivery and amendment workflow management platforms — operates on a similar logic: standardized data infrastructure that lenders will increasingly expect agents to connect to.⁵ SRS Acquiom should have an explicit position on DataXchange adoption. Two paths are defensible: integrate with DataXchange (faster time-to-value on notice delivery, cedes the notice pipe to S&P) or build proprietary notice infrastructure in LAD (higher cost, full control, 12 to 18 month build). The amendment and consent portal work on the Year 2 roadmap represents the alternative to AmendX for that workflow.

**Lender-side infrastructure is automating independently of agent decisions.** Hypercore — backed by Insight Partners in a $13.5 million Series A in February 2026 — launched its AI Admin Agent in general availability in May 2026, covering the full post-close operational lifecycle: deal processing, payment reconciliation, covenant monitoring, draw requests, distributions, waterfall execution, and investor reporting.¹⁸ The platform manages more than $20 billion in AUM across 10,000+ loans and grew 3.5x on CARR in 2025. Hypercore sells to lenders, not to agents, so it does not compete for SRS Acquiom's mandate. But it raises the interoperability floor: lenders who have automated their own back-office now arrive at every agent interaction expecting API-level data exchange and real-time position visibility. The platform-capability investment in this proposal is the agent-side answer to that expectation.

The firms that hold competitive position through this consolidation period will be those whose platform investments compound rather than repeat. SRS Acquiom's current technology gap is not primarily against Alter Domus circa 2018; it is against a market that has continued moving while the team completed the DLX migration.

---

## The Technical Vision: Three Pillars

Loan Agency's product strategy organizes around three pillars articulated in the March 2026 Technical Vision and now canonical in the FY26 Epics database. They are the strategic spine of every roadmap decision in this proposal and the basis for the two-team structure that follows.

**Scale Without Breaking.** Internal automation and platform infrastructure that decouple deal growth from headcount growth. SRS Acquiom should be able to administer the next 100 deals without proportionally hiring an Operations team to match. The current constraint is the spreadsheet-and-email infrastructure that Loan Agency Operations runs on, not the people running it; this pillar replaces that infrastructure.

**Engage Your Way.** External self-service across the full client relationship. Lenders, borrowers, and their sponsors choose how they interact with SRS Acquiom: through the Loan Agency Dashboard, through integrations with the data utilities they already use, or through a human. Routine actions do not require waiting on Operations.

**On-Demand Data Accessibility.** Internal and external reporting that surfaces the right information to the right party at the right time. This pillar is cross-cutting: it sits inside every internal workflow that needs visibility and every external surface clients use.

The two-team structure proposed below is a direct mapping of these pillars onto execution. A Client Experience team drives Engage Your Way through the Loan Agency Dashboard. A Loan Operations Platform team drives Scale Without Breaking through internal automation. On-Demand Data Accessibility lives across both — external reporting inside Client Experience, internal analytics inside Loan Operations Platform, with a shared semantic layer above.

---

## Current State and the Gap

### One Team for the Entire Business Line

The Loan Agency business line is currently supported by a single product and engineering team of ten people: six engineers, one Product Manager, one Product Owner, one Product Designer, and one Engineering Manager. This team owns the Loan Agency Dashboard for external clients, the Bank Payments Application, the Tax Entity Application, and a range of internal tools used by Loan Agency Operations. Collectively these systems support 461 active deals representing $84.3 billion in active commitments, more than 4,400 distinct lender relationships, roughly 54,000 outgoing wire payments processed in the trailing twelve months, and 8,800 lender assignments closed over the same period.

By comparison, the M&A business line at SRS Acquiom operates seven product teams with eight product managers, three designers, and approximately fifty engineers. This contrast reflects the historical maturity of the M&A franchise versus a Loan Agency business line that has just emerged from a multi-year migration. It does raise a direct question: what does the Loan Agency function need to look like to compete at the top of its market?

### The Mixed-Backlog Problem

Operating with a single team has produced a recurring pattern that the current sprint cadence makes visible. The backlog is a rolling mix of external client-facing work and internal operations work, prioritized by whichever fire is most urgent in any given two-week cycle. This pattern is what paused LAD development through the DLX migration period; LAD work was deprioritized to support migration cleanup, and clients have not seen meaningful LAD enhancements as a result. The pause is now ending, but the same pattern will reassert itself the next time an operational fire surfaces unless the structure changes. The cost is visible: of the five epics in flight, two are migration completion work, two are client-facing efforts still in design, and one is internal reporting infrastructure in development. No new external LAD capability has reached lenders during the migration window.

### The Roadmap Already Exists

The FY26 Epics database catalogs 36 epics across three strategic pillars: 21 under Scale Without Breaking, 9 under Engage Your Way, and 6 under On-Demand Data Accessibility. Five are in flight today. The remaining work is scoped, sequenced, and in many cases has business requirements documents already written. The constraint is capacity and team structure, not vision. Six engineers cannot credibly execute against this roadmap in the time frame the market requires.

---

## Proposed Organization

The proposal is two purpose-built teams organized around distinct customers and strategic pillars. This structure is the right choice for Year 1: it maps directly to the two primary pillars, separates the mixed-backlog incentive structure that has historically deprioritized client-facing work, and meets the engineering resilience floor without the coordination overhead of a three-team launch. A third Platform Foundations team — responsible for the shared DLX substrate, workflow orchestration layer, and canonical data definitions — is the right structural evolution when shared substrate work grows to consume roughly one-fifth of either team's engineering capacity for two consecutive quarters. That transition is planned, not contingent.

### Team 1: Client Experience

**Customer.** Lenders and borrowers across LSTA and LMA markets — loan operations specialists at banks, BDCs, and CLO managers; portfolio administrators at private credit funds; treasury teams at PE-backed portfolio companies; and credit analysts. The current base of more than 4,400 distinct lender participations across 461 active deals represents the immediate addressable audience, with behind those 461 deals sitting hundreds of distinct borrower entities. Two distinct user populations share this team. Lenders interact continuously to monitor positions, reconcile data, and track deal activity. Borrowers interact at discrete deal events: drawdowns, rate elections, amendment votes, and compliance submissions. Combining both populations in one team is the right structure for Year 1. The underlying loan data is shared — the same credit agreements, notices, cashflows, and elections drive activity for both audiences — and borrower-specific workflow volume does not yet justify dedicated team capacity. The structure requires two operating disciplines: separate success metrics for lender deflection rate versus borrower time-to-action, and role-based navigation that routes each user type to their primary actions at login. The empirical trigger for reconsidering the combined structure is two engineers sustained on borrower-specific workstreams for two consecutive quarters.

**Mission.** The Loan Agency Dashboard becomes the complete self-service surface for the client relationship with SRS Acquiom. Today the Dashboard provides documents and position data. The Client Experience team's mandate is that a client choosing to do so can run their full relationship — reads, actions, notifications, and integrations — without calling or emailing Loan Agency Operations.

**Scope.** LAD reads (positions, documents, notices, reporting, historical data); LAD write workflows (SSI self-service, drawdown requests, rate elections, tax document upload, compliance certificate delivery, amendment voting); external party user management; proactive notifications; lender and borrower onboarding (KYC portal, entity setup); and the external data integration surface including Versana for BSL deal data and LendOS for direct lending portfolio data.

**Success measures.** Client self-service rate; support ticket deflection against the 3,140-ticket six-month baseline (1,400 notice resends plus 1,740 position and reporting); time-to-action for routine write workflows; client adoption; competitive parity on reporting depth and customizability against the Alter Domus CorPro benchmark.

**Strategic pillar.** Engage Your Way (primary). Contributes to On-Demand Data Accessibility through external reporting and integrations.

### Team 2: Loan Operations Platform

**Note on taxonomy.** The Loan Operations Platform team is misnamed if read as a platform team. It serves SRS Acquiom Loan Agency Operations directly as its primary customer — it is a domain-specialized team aligned to internal operators, not a team whose purpose is to enable other teams' work. The distinction matters for hiring, headcount expectations, and dependency planning: this team is owned by its customer's operational outcomes, not by making the Client Experience team's engineering easier. The empirical trigger for splitting the Loan Operations Platform further (any single workstream sustaining two engineers full-time for two consecutive quarters) applies at the workstream level, with Tax and Payments as the most likely candidates at roughly 600 to 800 active deals.

**Customer.** SRS Acquiom Loan Agency Operations across all functions — the Transaction Team for payments and tax operations, deal administration, collateral and sub-agency, and finance operations.

**Mission.** Replace the spreadsheet and email infrastructure that Loan Agency Operations has run on with platform automation that lets the business line grow without adding headcount in proportion to deal volume. Between year-end 2023 and April 2026, operations headcount grew from 22 to 45 people while active deal count grew from 237 to 483 — a one-to-one ratio. This team's purpose is to break that ratio.

**Scope.** Bank Payments Application capability expansion (Virtual Accounts, BofA API integration, BAI2 reconciliation, ADF and Wire Instruction Extraction); the full Tax Reporting and Compliance Platform (Tax Entity Management, Withholding Determination Engine, Tax Activity Ledger, Reconciliation and Remediation, Year-End Reporting); secure intake replacing email-based document exchange; deal lifecycle workflow automation; deliverable classification and routing; UCC and collateral tracking; credit agreement extraction; internal user and access management; and internal analytics and Power BI infrastructure.

**Success measures.** Hours reclaimed against current manual baselines — the immediate targets are the 40 to 50 hours per month and more than 80 hours at year-end currently absorbed by tax operations reconciliation, the manual touchpoints in a 54,000-wire-per-year payment operation, and error rate on regulatory filings; capacity headroom against deal volume growth.

**Strategic pillar.** Scale Without Breaking (primary). Contributes to On-Demand Data Accessibility through internal analytics and reporting.

---

## Design Principles

Three principles govern how the two teams work together and where complexity lives.

### One System of Record, Clearly Bounded Handoffs

Both teams build on DLX as the authoritative source for deal and lender data. Whether DLX serves as the direct integration substrate or whether a thin coordination layer sits in front of it depends on the outcome of a pre-launch validation: does DLX's current API surface provide stable versioned read APIs, event or change-data-capture notifications on write operations, schema versioning contracts, idempotency key support for exactly-once delivery, and audit-trail integration for regulated lender-executed actions? If yes, DLX is the substrate and both teams consume it directly. If not, a lightweight integration layer between the two teams carries those responsibilities, and DLX remains the system of record behind it.

Either way, the architecture principle is the same: when a lender submits an action through the Client Experience team's portal — an SSI change, a rate election, an amendment vote — that action passes to the Loan Operations Platform team through a defined, asynchronous interface. Neither team calls the other directly. Neither team blocks on the other's release schedule. The interface contract is explicit: what gets submitted, what confirmation comes back, and what happens if a step fails. Every regulated lender action generates a complete audit record at the point of submission, not reconstructed after the fact. This validation is the first deliverable of the Q2 2026 pre-launch architecture spike — both teams launch knowing which substrate path they are building against.

### Each Team Owns Its Data End to End

Rather than routing all data and reporting requests through a central team, Client Experience owns the data engineering that feeds external reporting and integrations. Loan Operations Platform owns the internal analytics and the Power BI infrastructure. A shared set of canonical definitions — for metrics like commitment balance, lender count, and payment status — sits above both teams as a maintained contract, not a separate organization. Ownership of that contract is explicit from Day 1 and lives with a named individual until the team structure matures to the point where a dedicated platform function makes sense.

### Integrations Belong to the Team That Depends on Them

Versana and LendOS sit within Client Experience because lenders are the primary consumer and the integration's value is measured in lender-facing outcomes. ClearPar and settlement-related integrations sit within Loan Operations Platform because settlement is an operations function. This prevents integrations from becoming orphaned capabilities that no team has a strong incentive to maintain.

---

## Resourcing Model

This proposal presents two distinct paths, sized to different roadmap scope, so executives choose the ambition level rather than approve or reject a single number. The ranges below are grounded in the prioritized epic backlog — 36 epics across the FY26 roadmap — and standard delivery productivity for a two-team structure carrying the technical scope described in this document, set against the operational and competitive timelines that define when the work must ship to matter.

### Target State — Competitive Footprint

The two-year target is 26 to 30 people across the full function. This range reflects two scope-conditional positions:

- **26 to 30 total** sizes the function to ship the full 36-epic FY26 roadmap on the 24-to-36-month competitive timeline. At the bottom of this range, the Tax Reporting and Compliance Platform completes in Year 2; at the top, there is modest slack for competitive response work.
- **23 to 25 total** is a defensible specialty-player position that ships the highest-leverage 80% of the roadmap by end of Year 2, with Tax Platform sub-epics extending into Year 3. This framing should be explicit if 26 to 30 is not approved — it is a strategic choice, not a constrained version of the same ambition.

Both ranges remain under half of the M&A function's current footprint within the same company. If actual delivery velocity in Year 1 exceeds the planning assumption by 25% or more — measured as completed roadmap weight against allocated capacity at end of Year 1 — the Target range should compress toward the lower bound or below. If engineering hiring lags planned dates by more than two quarters, the Year 2 capability parity milestones should be reset rather than the Target headcount expanded to compensate.

| Role | Client Experience | Loan Operations Platform |
|------|-------------------|--------------------------|
| Product Manager | 1 dedicated | 1 dedicated |
| Product Owner | 1 | 1–2 (workstream leads: Tax, Payments/Workflow) |
| Product Designer | 1 dedicated | 1 dedicated |
| Engineering Manager | 1 dedicated | 1 dedicated |
| Engineers (incl. 1 data engineer per team) | 7–8 | 7–9 |
| **Team total** | **11–13** | **12–15** |

### Year 1 Launch — Starting Position

The Year 1 launch redistributes current personnel into two teams and adds a focused engineering cohort. Leadership and product roles restructure rather than expand at launch. Brad Gilbert remains Senior Product Manager for one team and provides strategic oversight across both teams; day-to-day team-level product decisions move to the promoted Product Manager on the second team; cross-team prioritization and strategic trade-offs sit with the Lead PM. The current Product Designer covers both teams. The current Engineering Manager covers both teams.

| Role | Client Experience | Loan Operations Platform |
|------|-------------------|--------------------------|
| Product Manager | Brad Gilbert (Lead PM, strategic oversight across both teams) | Promoted from current PO; Lead PM holds strategic final call |
| Product Owner | None at launch | None at launch |
| Product Designer | Shared (≈50%) | Shared (≈50%) |
| Engineering Manager | Shared (≈50%) | Shared (≈50%) |
| Engineers | 6 (recommended) / 5 (floor) | 6 (recommended) / 5 (floor) |
| **Effective team total** | **≈8** | **≈8** |

Six engineers per team is the recommended launch floor. At five engineers per team — the absolute floor — sprint resilience is meaningful, but five engineers per team against the Year 1 priority backlog ships fewer than 40% of the candidate epic set within the target window. At six per team, the Year 1 position delivers roughly 60 to 70% of the prioritized Y1 epic set; Path-Between hiring during Year 1 closes toward the full set.

Sourcing for the second Product Designer, second Engineering Manager, and first wave of additional engineers must begin in Q2 2026 — in parallel with restructure planning, before the Q3 structural launch. With 5-to-7-month lead times for senior design and engineering management roles, Q4 2026 landing requires active sourcing before the restructure announcement.

---

## Roadmap Prioritization

The FY26 Epics database currently holds 36 epics: 21 under Scale Without Breaking, 9 under Engage Your Way, and 6 under On-Demand Data Accessibility. The distribution reflects ops debt paydown logic: the team has been carrying a migration and operational backlog. Under the two-team structure, both pillars execute in parallel for the first time. The prioritization below sequences within each team's backlog to lead with the highest competitive and operational leverage.

### Client Experience — Engage Your Way (Year 1–2 sequence)

**Priority 1 — Proactive Notifications (with Notices in LAD as a bundled delivery).** Directly addresses 2,800 annualized notice resend requests, the single largest ticket category. Every notice resend is a client reaching for information that a digital delivery channel would have surfaced automatically. Alter Domus Agency360 and Solifi's ABL portal both deliver proactive push notifications as standard capability.¹⁹ Estimated deflection: 65 to 80% of the notice resend category. One decision is required before committing build resources: S&P Global launched DataXchange in March 2026, a centralized notice delivery infrastructure targeting the same problem.⁵ SRS Acquiom should decide whether to integrate with DataXchange (faster time-to-value, cedes the notice pipe to S&P) or build proprietary infrastructure (full control, 12 to 18 month build) before the engineering sprint begins. Both paths are defensible; an explicit position belongs in this document.

**Priority 2 — Versana and LendOS Integration (recommended for addition as named epic — currently absent from the 36-epic roadmap).** Versana connects $4.1 trillion in active loan facility coverage across more than 6,000 facilities. Its Reconciliation Module lets lenders electronically match their positions against agent records in real time, identifying the specific transaction causing any discrepancy. For lenders holding positions across Versana-connected agents and SRS Acquiom-agented deals, SRS Acquiom's absence creates a visible gap in portfolio data access — and directly contributes to the 1,740 annualized position and reporting tickets. Year 1 scope: architecture and API scoping. Year 2 scope: production integration. LendOS (Blackstone Innovations Series A, September 2025) is the equivalent priority for the private credit and direct lending book.⁶

**Priority 3 — SSI Self-Service.** Standing settlement instructions determine where every wire payment goes. SSI errors contribute to position and reporting tickets. Every one of the 4,400 lender participations requires accurate SSI on file. Self-service SSI updates remove a routine operational touchpoint and reduce error-driven downstream volume. Implementation requires a change-authorization workflow, a full audit trail, and coordination with the payments infrastructure — the action-handoff architecture must be defined before UI development begins. This is the write-capability infrastructure on which all subsequent write-capability epics depend.

**Priority 4 — Historical Reporting.** Named clients describe the Dashboard as behind Alter Domus's CorPro portal on reporting depth and customizability. Historical reporting — deal-level and portfolio-level data back to deal inception, filterable and exportable — is the direct response to that feedback.

**Priority 5 — KYC and Onboarding Portal.** With 220 new deals closed in the trailing twelve months, onboarding quality determines data quality for the life of each deal. The only Engage Your Way epic that touches lenders, borrowers, and sponsors simultaneously.

**Priority 6 — Consent and Amendment Workflow.** Amendment coordination currently runs through email. A direct parity item: peer portals offer amendment workflow as standard functionality. S&P AmendX (March 2026) is a direct substitute for agents who do not build this. The proprietary build window is approximately 12 to 18 months before AmendX achieves broad agent adoption.

**Priority 7 — Deal Document Access.** Baseline portal parity.

**Priority 8 — AI Data Agent (Year 2 design scope).** Natural language query over deal data. Hypercore's AI Admin Agent — already in general availability on the lender side as of May 2026 (see Competitive Landscape) — signals this is a 24-to-36-month competitive expectation, not a later-phase consideration. Move to Year 2 design to avoid falling behind the expectation curve.⁷

### Loan Operations Platform — Scale Without Breaking (Year 1–2 sequence)

**Priority 1 — Tax Reporting and Compliance Platform (13-epic BRD, years 1–3).** The 40 to 50 hours per month plus more than 80 hours at year-end quantify an unambiguous automation opportunity. The IRS FIRE-to-IRIS transition on December 31, 2026 is a hard compliance deadline: Tax Year 2026 Form 1042-S returns due March 15, 2027 must use IRIS A2A for organizations filing 100 or more returns. Existing FIRE TCCs do not transfer; new TCC registration takes up to 45 days. Incorrect Chapter 3 and Chapter 4 withholding determination carries a 30% penalty on the incorrectly withheld amount under IRC Section 1461. At $84.3 billion in active commitments, the compliance stakes are quantifiable. Year 1 scope: first four of thirteen sub-epics (Tax Entity Management, Withholding Determination Engine baseline, IRIS registration and integration, Tax Activity Ledger foundation).

**Priority 2 — ADF and Wire Instruction Extraction.** 54,000 outgoing wire payments per year at current manual touchpoint rates. Extraction automation is the highest-volume ops leverage item in the Scale Without Breaking pillar and is a prerequisite for meaningful straight-through processing improvement.

**Priority 3 — Bank Payments capability expansion.** BofA API integration, BAI2 reconciliation, Virtual Accounts.

**Priority 4 — Credit Agreement Extraction.** Foundational for covenant monitoring automation and for any future AI-assisted deal lifecycle work.

**Priority 5 — Secure intake, deal lifecycle workflow automation, internal analytics.** Operational resilience items that reduce exception handling and improve visibility without directly determining competitive wins.

---

## Path Between

A sequenced hiring and capability roadmap closing the gap between Year 1 launch and target state, with milestones tied to specific deliverables and competitive parity checkpoints.

| Window | Action |
|--------|--------|
| **Q2 2026 (pre-launch prerequisite)** | Architecture validation. Engineering Manager and senior engineers conduct a focused review of DLX's current write-capability API surface: whether state-change events are emitted natively or require a thin orchestration layer; whether the SSI self-service workflow can be built to the intended submit-review-approve-execute pattern against the existing system. Four to six weeks. Produces two outputs: a confirmed interface contract for the async handoff pattern, and a decision on workflow orchestration approach. Both teams launch with this foundation in place. **Sourcing begins for second Product Designer, second Engineering Manager, and first wave of engineering hires — in parallel, before the structural launch.** |
| **Q3 2026** | Structural launch. Two teams begin operating with confirmed interface contract. No new hires required to execute the restructure. |
| **Q4 2026** | Second Product Designer hired (closes design queue). Second Engineering Manager hired (separate engineering leadership). Engineering hiring continues toward 6 per team. |
| **Q1–Q2 2027** | Continued engineering growth toward 7–8 per team. Add at least one Product Owner per team for workstream depth (Tax and Payments workstreams within Loan Operations Platform). |
| **H2 2027 onward** | Continued progression toward target state. Monitor whether shared substrate work — DLX contract maintenance, workflow orchestration evolution, semantic layer governance — is consuming more than roughly one-fifth of either team's engineering capacity for two consecutive quarters. When that threshold is crossed, the Platform Foundations team becomes the right next structural step: a dedicated team whose customers are the Client Experience and Loan Operations Platform teams and whose mission is to make the shared infrastructure invisible to both. |

### Capability Parity Milestones

The strategic ambition is to close the platform-capability gap with the market's leading independent agents on lender-facing self-service within 24 months, and to achieve full write-capability parity on amendment workflow and borrower-submitted actions within 36 months. Top-of-market parity across all capability dimensions is a multi-year North Star and is not the 24-to-36-month commitment. The milestones below make that commitment falsifiable and exec-trackable.

**Month 12 (Q3 2027):**
- Versana integration live — SRS Acquiom-agented deals are Versana-connected; lenders see real-time position data without contacting Loan Agency Operations *(Owner: Client Experience)*
- LAD Proactive Notifications in production — notice resend ticket bucket measurably reduced against H1 2026 baseline *(Owner: Client Experience)*
- SSI self-service live (read-first) — lenders can view and request SSI changes through the portal with a defined audit trail *(Owner: Joint — CX + LOP, led by Engineering Manager)*
- Tax Reporting and Compliance Platform first four sub-epics in production; IRIS-native for Tax Year 2026 returns *(Owner: Loan Operations Platform)*
- ADF and Wire Instruction Extraction in production across the 54,000-wire-per-year volume *(Owner: Loan Operations Platform)*

**Month 24 (Q3 2028):**
- SSI self-service fully write-capable — lenders can submit, authorize, and confirm SSI changes without Loan Agency Operations touchpoint, comparable to Alter Domus CorPro's self-service depth on settlement instruction management *(Owner: Joint — CX + LOP, led by Engineering Manager)*
- Historical reporting at competitive depth — deal-level and portfolio-level data back to deal inception, filterable and exportable *(Owner: Client Experience)*
- KYC and Onboarding Portal live — digital KYC, entity setup, and initial SSI load at 24-hour turnaround *(Owner: Client Experience)*
- Consent and Amendment Workflow in portal (or AmendX integration confirmed) — email-coordinated amendment process replaced *(Owner: Client Experience)*
- First evidence the 1:1 ops-to-deals growth ratio is bending — total ops headcount growth outpaced by deal volume growth in at least one trailing 12-month window *(Owner: Lead PM — strategic position claim)*

**Month 36 (Q3 2029):**
- Tax Reporting and Compliance Platform complete (13 of 13 sub-epics in production) *(Owner: Loan Operations Platform)*
- Drawdown and borrower write-capability live — PE-backed portfolio companies can submit drawdown requests, rate elections, and compliance certificates through the portal *(Owner: Client Experience)*
- AI Data Agent in production *(Owner: Client Experience)*
- Ops headcount decoupling demonstrated — deal volume can grow 25% or more with flat or sub-linear ops headcount, demonstrating the scalability thesis *(Owner: Lead PM — strategic position claim)*

---

## Risks and Mitigations

### Five Engineers per Team Is the Absolute Floor

Below that, any single person's absence materially affects sprint output, and the Year 1 priority backlog — Tax IRIS compliance, ADF extraction, SSI self-service, and Versana architecture — requires sustained parallel execution across both teams to ship within the window the operational and competitive cases require. The Year 1 recommended floor is six per team. Path-Between hiring continues through Year 1 and Year 2 to bring each team to target state.

### The Action-Handoff Architecture Is Greenfield

LAD writes that need internal approval workflows have no existing pattern at SRS Acquiom; LAD today only reads from DLX. The Q2 2026 architecture spike is the mitigation: the Engineering Manager and senior engineers from both teams define the DLX interface contract and workflow orchestration approach before the structural launch, so both teams launch with the coordination mechanism validated rather than inheriting an open architectural question. Initial scoping estimates this work at two weeks of focused architectural design across the Engineering Manager and senior engineers from both teams, with deliverables that include the interface contract, the workflow orchestration decision, and the audit-trail architecture. Whether DLX serves as the direct substrate or a thin integration layer sits in front of it, the architecture principle holds: async handoff, bounded interfaces, audit trail at submission.

### The Design Queue Closes in Q4 2026

A single designer split across two teams with materially different design vocabularies — external client-facing surfaces and internal workflow applications — will create a queue within one to two quarters. The second Product Designer hire is a Q4 2026 hard dependency for sustained Client Experience velocity, not an optional enhancement.

### Lender Adoption Requires Change Management, Not Just Capability

Write-capability shipping is necessary but not sufficient. Lender operations teams at PE funds and banks have embedded SSI, drawdown, and amendment workflows in their own internal systems. Self-service adoption requires change management on the lender side. Scope lender onboarding and workflow communication as a Client Experience workstream from Year 1, with explicit adoption rate targets tracked alongside shipment milestones.

### The Dual-PM Structure at Launch Requires Explicit Decision Rights

A Lead PM with strategic oversight across both teams alongside a primary-driver PM for the second team requires documented decision rights to function. Day-to-day team direction sits with each team's Product Manager; cross-team prioritization, strategic posture, and trade-offs against the overall Loan Agency portfolio sit with the Lead PM. This pattern works, but only when the decision rights are documented and revisited.

### The Competitive Moat Can Shift Before Parity Is Achieved

Versana's expansion into SRS Acquiom's middle-market deal tier is a 18-to-36-month trajectory, not an immediate threat. S&P DataXchange at 12 weeks since launch has an uncertain adoption curve. The risk is that the competitive frontier advances — to AI-assisted covenant monitoring, Versana-native API integration, or capabilities not yet visible — while the team is shipping 2025 table-stakes. Mitigation: competitive roadmap review every six months, Versana integration as a named Year 1 architecture priority, and explicit DataXchange position in this proposal rather than treating notice delivery as a fully proprietary build.

### Cheaper Substitutes Will Be Tested

A 2026 CFO review of any engineering headcount expansion will ask whether process redesign, offshoring, or vendor automation can achieve the same outcome at lower cost. Three credible answers: the 3,140 support interactions per six-month window are not operations inefficiency — they are clients doing by phone and email what a portal would let them do themselves; process redesign does not build the portal. Offshoring loan operations can reduce unit labor cost but does not break the one-to-one deal-to-headcount scaling problem and adds cross-border compliance complexity for regulated lender actions. Vendor automation — Versana for data distribution, S&P DataXchange for notice delivery, external KYC tooling — handles specific pieces, and this proposal recommends adopting each where build-versus-buy favors the vendor. What vendor automation does not provide is the integrated SRS Acquiom-branded portal surface — the authentication, workflow, reporting, customization, and bilateral action capabilities that constitute the full client experience. That surface requires SRS-specific engineering.

### Trust Company Chartering Is a Separate Decision, Not a Prerequisite

This proposal competes on platform capability — the dimension on which the current competitive gap exists and the dimension on which this investment closes it. A distinct question is whether SRS Acquiom should pursue trust company chartering, which would expand service scope to include indenture trustee mandates and escrow under trust law, and provide a direct regulatory credential that bank lenders reference when assessing third-party agents on bank-arranged transactions. Several competitors hold trust charters; others competing in the same market do not, and charter status does not explain the capability gap this proposal addresses — Alter Domus has built the largest independent loan agency platform without a US trust charter. At SRS Acquiom's current scale — 461 active deals and $84.3 billion in commitments — the economics of chartering are viable. The right sequencing is to establish the platform foundation this proposal funds, then initiate a chartering evaluation in 2027 targeting operational readiness by late 2028, aligned with the Target state timeline. This proposal does not commit to that path but names it as the logical next strategic step after Year 1 is complete.

---

## Decision and Asks

Three decisions are needed from this proposal.

### Decision 1: Strategic Ambition

The Loan Agency business line is being positioned to close the platform-capability gap with the market's leading independent agents on lender-facing self-service within 24 months, and to achieve full write-capability parity on amendment workflow and borrower-submitted actions within 36 months. Top-of-market parity across all capability dimensions is a multi-year North Star, not a 24-to-36-month commitment.

This framing defines what "yes" means. If the ambition is more modest — to remain a capable middle-market participant rather than invest at this level — the proposal should be revisited at a smaller scale before other decisions follow. The milestones in the Path Between section convert this ambition into checkable binary commitments at 12, 24, and 36 months.

### Decision 2: Approval of the Structural Change

The current single-team structure restructures into two teams (Client Experience and Loan Operations Platform) effective Q3 2026, with current personnel redistributed as described in the Year 1 Launch section. No new hires are required to execute this change. The Q2 2026 architecture spike is a pre-launch prerequisite and begins immediately upon approval.

### Decision 3: Approval of the Year 1 Engineering Hiring Ask

Each team operates at six engineers during Year 1 at launch, growing toward eight to ten per team by end of Year 1 through Path-Between hiring. Below five per team, the two-team structure does not function as intended — sprint resilience collapses and the Year 2 Target sizes to the full 36-epic roadmap on a 24-to-36-month timeline; the alternative path (23 to 25 total) delivers a focused subset with the remainder slipping into FY29. This proposal commits to five per team as the absolute floor and recommends six as the launch position; the Path-Between hires that follow (second Product Designer, second Engineering Manager, additional engineers and Product Owners through 2027) are not committed by this proposal but are surfaced here so they are not surprises when they appear in subsequent budget cycles.

Approval on these three points authorizes the Loan Agency function to begin the work the stated ambition requires.

---

## Sources

0. Internal SRS Acquiom operational metrics, May 2026. Deal counts, lender participations, ticket volumes, wire counts, and operations headcount drawn from the Loan Agency Operations management dashboard.

1. Alter Domus, "Bain Capital selects Alter Domus for $30 billion CLO mandate," BusinessWire, February 2026. https://alterdomus.com
2. Kroll Agency and Trustee Services, kroll.com/en/services/agency-and-trustee-services/loan-closing; Bloomberg Administrative Agent Rankings Q1 2025.
3. GLAS, "GLAS welcomes Oakley Capital and La Caisse as strategic investors," glas.agency, January 5, 2026. https://glas.agency
4. Versana, "Versana Closes $43 Million Capital Raise Led by BNP Paribas," PRNewswire, April 30, 2026. https://www.prnewswire.com/news-releases/versana-closes-43-million-capital-raise-led-by-bnp-paribas-with-fitch-ventures-massmutual-ventures-motive-partners-and-apollo-joining-as-investors-302758712.html
5. S&P Global, "S&P Global Launches DataXchange and AmendX," PRNewswire, March 3, 2026. https://press.spglobal.com
6. LendOS, "LendOS Closes Series A Led by Blackstone Innovations Investments," September 2025. https://lendos.io
7. Hypercore, "Hypercore AI Admin Agent Generally Available," PRNewswire, May 6, 2026. https://www.prnewswire.com
8. GLAS Trust Company LLC, New Hampshire Banking Department approval, March 2017. BusinessWire; Finextra.
9. Versana, "Morgan Stanley Agented BSL Deals Go Live on Versana's Real-Time Digital Data Platform," versana.io, April 2025. https://versana.io/morgan-stanley-agented-broadly-syndicated-loan-deals-go-live-on-versanas-real-time-digital-data-platform/
10. Wilmington Trust, AccessFintech Synergy Partnership, GlobeNewswire, February 2025.
11. Computershare Loan Administration and Agency Services, computershare.com.
12. US Bank Global Corporate Trust, Pivot Portal, usbank.com.
13. SS&C Technologies, Loan Services — loan administration for private debt funds and CLO managers. ssctech.com/solutions/alternatives/private-credit.
14. CSC Global Capital Markets, Administrative and Facility Agent Services. cscglobal.com/service/capital-markets/loan-agency/administrative-facility-agent-services/; CSC, "Cross-Border Private Credit Set to Surge," December 4, 2025. cscglobal.com/service/press/cross-border-private-credit-set-to-surge/
15. Ocorian, Loan Agency Services. ocorian.com/capital-markets/loan-agency-services; Ocorian acquisition of EdgePoint Fund Services, December 2024; Ocorian acquisition of E78 Fund Solutions, August 2025. ocorian.com/news-press-releases
16. PactFi, "$25 Million Series A," BusinessWire, March 10, 2026. businesswire.com; Fintech Global PactFi coverage, March 11, 2026. fintech.global
17. Carta, "Carta Acquires Sirvatus," BusinessWire, October 9, 2025. businesswire.com
18. Insight Partners, Hypercore Series A, February 26, 2026. insightpartners.com; Hypercore, "Hypercore AI Admin Agent Generally Available," PRNewswire, May 6, 2026. prnewswire.com
19. Solifi, "Why commercial self-service is essential in secured finance," solifi.com/blog/commercial-self-service-essential.

---

## Appendix: Approach to Sizing

The 26-to-30 and 23-to-25 headcount ranges are not derived from comparable-company benchmarks alone. They are grounded in the specific scope of work this proposal commits to delivering.

The FY26 Epics database contains 36 prioritized epics across three strategic pillars: 21 under Scale Without Breaking, 9 under Engage Your Way, and 6 under On-Demand Data Accessibility. Each epic carries an estimated delivery scope based on domain complexity and integration requirements. The highest-leverage 60 to 70 percent of this backlog constitutes the Year 1 candidate set; the remaining epics are Year 2 and Year 3 work under either path.

The two-team structure divides this backlog cleanly: Client Experience carries the Engage Your Way and external data integration epics; Loan Operations Platform carries Scale Without Breaking and internal automation. Each team's footprint is distinct enough that engineering capacity on one team does not substitute for capacity on the other.

The 24-to-36-month delivery window is set by external constraints, not internal preference: the IRS IRIS compliance deadline (December 31, 2026), the Versana network-effect timeline (18 to 36 months to critical penetration in SRS Acquiom's deal tier), and the S&P AmendX adoption curve (12 to 18 months before it becomes the default for agents who have not built their own amendment workflow). Work that does not ship within this window does not close the competitive gap; it arrives after the gap has hardened.

**Path A (26–30 total)** sizes the function to complete the full 36-epic roadmap within the 24-to-36-month window. At the lower end of this range, the Tax Reporting and Compliance Platform completes by end of Year 2; at the upper end, there is modest capacity for competitive-response work not yet visible in the current epic set.

**Path B (23–25 total)** delivers the highest-leverage 80 percent of the roadmap on the same timeline, with Tax Platform sub-epics completing in Year 3. This is a defensible specialty-player position and should be approved as a deliberate strategic choice, not treated as an underfunded version of Path A.
