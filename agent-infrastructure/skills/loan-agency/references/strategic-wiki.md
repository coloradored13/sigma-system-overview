# Loan Administration — Knowledge Wiki

Compiled from sigma-review R17 (April 9, 2026). 5-agent + DA multi-agent review of loan admin KB (7 docs) and technology analysis bundle for robustness.

---

# 1. Loan Admin Tech Landscape

Last updated: April 9, 2026

## Summary
The loan administration technology market serves private credit and syndicated loan operations, with competitive dynamics split between incumbent platforms (SyndTrak, Intralinks, Debt Domain) and newer specialized entrants. The space is experiencing consolidation and feature expansion, particularly around real-time data distribution, amendment workflows, and compliance automation. Technology is a floor for competitive entry, not a ceiling for differentiation — administrative quality and relationship trust remain primary selection criteria.

## Key Findings

### Market Structure
- Incumbent platforms for document management and distribution: SyndTrak, Intralinks, Debt Domain, with well-established market presence
- S&P's AmendX launched March 3, 2026 — amendment workflow tooling now joining the competitive set alongside Debt Domain and Intralinks
- GLAS (Global Loan Agency Services) is an established independent agent with completed deal activity; GLAS deal referenced as closed in competitive landscape
- Kroll expanded APAC operations, completed as of review date
- Hypercore confirmed active, no charter obtained

### CME SOFR Data Distribution (CRITICAL — Stale as of April 1, 2026)
- Doc3 Section 1 referenced a CME distribution fee waiver running "until April 1, 2026." That waiver has now expired.
- Agents redistributing Term SOFR data to third parties now face potential licensing fees from CME
- Action required: Confirm current CME fee schedule or direct agents to verify with CME directly

### S&P DataXchange + AmendX
- DataXchange and AmendX both confirmed launched as of review date
- AmendX (launched March 3, 2026) not yet in Doc0 glossary — entry should be added with verification flag

### Payment Waterfall Implementation
- KB Doc3 Section 13 is complete: 6-step non-default waterfall, 5-step default waterfall, 4-step defaulting lender waterfall all present
- 5 Mermaid diagrams well-integrated into documentation
- Cross-document referencing is consistent

---

# 2. Trust Charter Regulatory Path

Last updated: April 9, 2026

## Summary
The trust charter path for a loan administration entrant involves multiple intersecting regulatory regimes: NH NDTC (national trust company charter via OCC), CRD6 (EU banking licensing with a 93-day grandfathering window as of April 2026), and the current OCC environment that is described as "most favorable in a decade" for new charter applicants.

## Key Findings

### OCC Charter Environment
- OCC environment for new charter applications: "most favorable in a decade" — supported by evidence: 12 CFR 5.20 effective April 1, 2026 and the Coinbase conditional charter approval on April 2
- Charter timeline estimate: 4-6 months (conditional on application quality and no novel precedent issues) — calibrated at P=65-75%

### CRD6 — EU Banking Licensing (TIME-SENSITIVE)
- CRD6 core banking licensing effective January 11, 2027
- Grandfathering cutoff: contracts entered before July 11, 2026 are grandfathered
- As of April 9, 2026: **93 days remain** to the grandfathering cutoff
- Exemption from CRD6 is plausible but fact-specific — not a blanket safe harbor
- BELIEF[CRD6-exempt] = 0.68 — meaningful uncertainty remains

### Basel III Re-Proposal (FAVORABLE DEVELOPMENT)
- Original analysis bundle language: "capital-neutral re-proposal expected early 2026" — **superseded**
- Actual outcome: Basel III re-proposal issued March 19, 2026 — **capital-REDUCING** (~4.8-5.2% CET1 for large banks, ~7.8% for smaller institutions)
- Comment period runs through June 18, 2026
- Implication: MORE favorable for private credit than the bundle predicted

### HMRC Cross-Border Tax (CRITICAL — Stale as of April 5, 2026)
- Doc5 Section 3 referenced an HMRC URGENT callout for a deadline of April 5, 2026. **That deadline has passed.**
- Required update: change to post-deadline language

---

# 3. Private Credit Market

Last updated: April 9, 2026

## Summary
Private credit AUM stands at $3-3.5T (broad) or ~$2T (narrow corporate PC), with a Morgan Stanley projection of $5T by 2029. As of April 2026, the BDC capital formation stress modeled as a bear case in March 2026 has become the operative base case.

## Key Findings

### AUM Figures
- Broad private credit AUM (end-2024): $3.5T (AIMA), $3T start-2025 projected to $5T by 2029 (Morgan Stanley)
- Narrow corporate private credit AUM: ~$2T
- PC AUM 2030 recalibrated: $3-4T (80% CI: $2.8-4.5T) vs bundle's $4-5T — industry forecasts overshoot 20-30%

### BDC Capital Formation — Bear Case Is Now Base Case
- BDC January 2026 sales: $3.2B (-49% from March 2025 peak of $6.2B)
- RA Stanger 2026 forecast: -40% YoY
- Fitch PCDR: 5.8% (public credit), 9.2% (private credit)
- ~40% of private credit borrowers have negative free cash flow (IMF 2025 FSR)
- Q1 2026: several flagship semi-liquid BDC funds hit redemption limits
- April 2026 tariff/macro stress not captured in the March model

### Implications for Mandate Mix
- Greenfield mandate share: 40% (bundle) to **10-15%** (realistic near-term)
- Restructuring/workout mandates: rising to **25-35%** near-term
- "Countercyclical infrastructure" positioning: **required as base-case fundraising narrative**

### Calibrated Business Estimates (for Loan Admin Entrant)

| Metric | Bundle Figure | Recalibrated | Notes |
|--------|--------------|-------------|-------|
| Breakeven (primary) | 30-42 months | **36-48 months** | All-in, regulatory specialist calibration |
| Breakeven (stress) | 36-48 months | **42-60 months** | Reference class analysis |
| Total capital required | $23-37M base | **$30-55M realistic** | 80% CI |
| PC AUM 2030 | $4-5T | **$3-4T** | Industry forecasts overshoot 20-30% |
| Facility ramp (month 48) | 140 facilities | **60-90 facilities** | GLAS took 4yr with team+backing |
| Gross margin (48-60 months) | 70% aspirational | **50-60% realistic** | P(70%) = 10-20% |
| Addressable market | $150-300M | **$100-200M** more realistic initial | |

---

# 4. Key Competitors — Loan Administration

Last updated: April 9, 2026

## Summary
The loan administration competitive landscape includes established agents (Alter Domus, GLAS, Kroll), specialized data/tech entrants (Hypercore, S&P DataXchange, S&P AmendX), and infrastructure platforms (Versana).

## Key Findings

### Alter Domus
- Scale incumbent. **Cinven-backed** (majority, March 2024), EV $5.3B. NOT Bain-backed (original analysis error).

### GLAS
- Reference-class comparator for de novo entrant. ~4 years with experienced team + institutional backing to meaningful facility scale.

### Kroll
- Agency + trustee, not full admin. 8-day settlement. APAC expansion completed.

### Hypercore
- Active, no trust charter. SaaS ceiling remains.

### S&P DataXchange + AmendX
- Infrastructure layer. Cannot replace fiduciary functions (TIA §310 protection).

### Competitive Window
- **12-18 months** for differentiated new entrant. Cross-verified, most validated figure in the analysis.

### Strategic Paths
- **Path A**: De novo + experienced team (GLAS model) — highest probability
- **Path B**: Acquire + enhance — integration risk
- **Path C**: De novo + tech-first, no experienced team — **no successful precedent, P=0.15**

**Most material gap**: Founding team industry experience level — strongest predictor of breakeven timeline.
