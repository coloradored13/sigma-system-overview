# workspace — private-target M&A deal terms analysis
## status: active
## mode: ANALYZE

## task
Analyze prevailing market-standard terms in private-target M&A transactions using the SRS Acquiom 2025 M&A Deal Terms Study (2,200+ deals, $505B, 2019-2024). For each major deal term category, determine:
1. What is "market" (prevailing standard) based on 2024 data
2. Realistic best outcome for SELLER (sell-side win)
3. Realistic best outcome for BUYER (buy-side win)
4. Realistic compromise position where both sides can live with the result
5. How RWI presence/absence shifts achievable outcomes

## scope-boundary
This review analyzes: private-target M&A deal terms and negotiation positioning based on SRSA 2025 empirical data
This review does NOT cover: public company M&A, life sciences deals (except where study explicitly includes), specific deal advice for any particular transaction, legal opinions or recommendations
temporal-boundary: none (study covers 2019-2024 closed deals, current as of publication)

## prompt-decomposition
### Q[] (confirmed)
Q1: What are the prevailing "market standard" terms across each major deal term category based on 2024 data?
Q2: For each term, what is the realistic best outcome a SELLER can achieve (sell-side win)?
Q3: For each term, what is the realistic best outcome a BUYER can achieve (buy-side win)?
Q4: For each term, what is the realistic compromise between buyer and seller positions?
Q5: How does RWI presence/absence shift achievable outcomes for each side?

### H[] (to test, not assume)
H1: A definable "market standard" exists for each term — data converges enough to identify prevailing norms rather than being too dispersed
H2: 2024 data represents conditions applicable to a negotiation today (2026)
H3: Buyer/seller "best realistic outcomes" can be identified from data distribution (not just medians — the tails matter)
H4: The "compromise" is distinguishable from the statistical median — meaningful space exists between what each side realistically wins vs. where they meet

### C[] (constraints)
C1: SRSA 2025 Deal Terms Study (2,200+ deals, 2019-2024) is the primary source
C2: Private-target M&A only
C3: Non-Life Sciences unless noted
C4: Data reflects closed-deal outcomes, not opening positions — we see where negotiations landed, not where they started
C5: Analysis must be framed from both buyer AND seller perspectives, plus compromise

## infrastructure
ΣVerify: available | providers: openai(gpt-5.4), google(gemini-3.1-pro-preview)
reasoning-models: openai(gpt-5.4-pro), google(gemini-3.1-pro-preview thinking)

## primary-source
SRS Acquiom 2025 M&A Deal Terms Study
- 2,200+ private-target acquisitions, $505B aggregate value
- Deals closed 2019-2024 (focus on 2024)
- Database of 4,500+ deals (MarketStandard)
- RWI identified on ~42% of 2024 deals
- Mostly non-public deals
- File: /Users/bjgilbert/SRSA_2025_Deal_Terms_Study.pdf (119 pages)

## agent-assignments
| Agent | Scope | Slides |
|---|---|---|
| loan-ops-tech-specialist | Financial mechanics: PPAs, escrow sizing, holdbacks, caps, baskets, consideration structure, working capital, earnout mechanics | 9-29, 68-86 |
| product-strategist | Market context: deal structure trends, buyer types, valuation multiples, RWI adoption dynamics, seller/buyer market power signals | 7-17, 96-99 |
| m-and-a-deal-counsel (dynamic) | Legal deal terms: reps/warranties, MAE/MAC, closing conditions, sandbagging, materiality scrape, survival periods, fraud, dispute resolution, exclusive remedy | 30-67, 87-95 |
| reference-class-analyst | Calibration: cross-validate all positions against distributional data, test H1-H4, identify where "realistic" sits per percentile ranges | Cross-cutting all slides |
| devils-advocate (r2+) | Stress-test: challenge whether proposed wins are data-supported or aspirational | R2 onward |

## findings
### loan-ops-tech-specialist

#### XVERIFY LOG
- F1 (RWI escrow collapse): XVERIFY[openai:gpt-5.4] + XVERIFY[google:gemini-3.1-pro-preview] → both PARTIAL. Core data confirmed (0.35% vs 10.0% median). Correction: "substitutes" overstates causation — data shows association. "RWI-identified deals are associated with median seller-funded general indemnity escrow of 0.35% vs 10.0% for non-identified deals" is the precise formulation. Sample contamination acknowledged (buyers don't always disclose RWI).
- F2 (Earnout mechanics): XVERIFY[openai:gpt-5.4] → PARTIAL. Core stats confirmed (22%, 31%, 24mo, 65% revenue). Correction: CRE "30%+" for 2023 is imprecise — slide 27 footnote states CRE was "over 30%" in 2023, now 10% in 2024. Formulation corrected to "down materially from 2023 levels."

---

#### DB[] BOOTSTRAPPING NOTES (pre-write)
DB[RWI-escrow]: FOR=28x gap confirmed across slides 80,82,83,84 consistently | AGAINST=sample contamination both directions (non-ID includes some RWI; RWI-ID may miss deals) | VERDICT=direction and magnitude hold, precise language required
DB[earnout-CRE]: FOR=slide 27 footnote explicitly states "noticeable decrease from 2023 deals, when CRE was included on over 30% of earnouts" | AGAINST=footnote language vs chart data | VERDICT=formulation adjusted to match footnote language
DB[basket-types]: FOR=first-dollar basket at 39% stable 3yr; deductible declining 46%→38% | AGAINST=RWI split inverts entirely (44% no-basket with RWI vs 8% without) | VERDICT=RWI creates two distinct basket-type markets, not one

---

#### H[] ADDRESSABILITY
H1 (market standard exists): CONFIRMED for most terms. Exceptions: earnout covenants (dispersed), PPA cap structure (three competing structures ~equal). Median is identifiable for escrows/caps/baskets.
H3 (tails identify best outcomes): CONFIRMED. Distribution data on slides 70,74,75,76,82,83,84 shows clear percentile ranges allowing sell-side/buy-side positioning.
H4 (compromise ≠ median): CONFIRMED for escrows (sell-side win = no escrow/RWI path; buy-side win = 10%+ escrow; compromise = median 10%). For baskets: first-dollar vs deductible split makes compromise meaningful.

---

```
TERM: POST-CLOSING PURCHASE PRICE ADJUSTMENTS (PPAs)
MARKET (2024): 92% of deals include a PPA provision. Working capital (85%), cash (85%), and debt (92%) are the dominant adjustment metrics — 98% of PPAs use more than one metric. Buyer prepares final calculations in 99% of deals. 86% of PPA provisions exclude tax-related items. Working capital methodology: 37% GAAP-consistent-with-past-practices, 35% specific calculation schedule, 19% GAAP only, 7% other.
SELL-SIDE WIN: No PPA threshold required (86% of deals have no threshold). If PPA must be included, position working capital using GAAP-consistent-with-past-practices methodology (37% market, familiar/auditable, limits manipulation). Maximize sell-side information rights: 85% of deals require buyer to provide supporting information/reasonable detail beyond just final calculations. Right to request other relevant information (61%), meet with buyer reps (44%), and request workpapers (42%) are all achievable. No separate PPA escrow: the 22% of deals without separate PPA escrow rely on indemnification escrow — sellers in those deals avoid a second lockup.
BUY-SIDE WIN: Retain right to review PPA estimate at or near closing (achieved in 14% of 2024 deals — a new data point, growing from 12-16% range). Require a specific calculation methodology schedule (35% of deals) rather than GAAP-consistent-with-past-practices, giving buyer definitional control. Separate PPA escrow (78% of deals in 2024, median 0.98% of TV) — creates dedicated ring-fenced recovery fund. Cap buyer-favorable PPA claims at PPA escrow amount only (36% of deals, 2023 data) rather than the general indemnification cap, limiting seller exposure above the PPA escrow fund.
COMPROMISE: PPA provision included (near-universal market standard). Buyer prepares final calculations (99% market). Methodology: GAAP-consistent-with-past-practices or specific schedule (combined ~72% of market). Seller receives supporting information and can request relevant data (92%+ of deals). Separate PPA escrow at ~1% of TV (median 0.98%). No threshold (86% of market — threshold is a seller ask that rarely succeeds). Cap: PPA escrow amount or indemnification escrow (combined 54% of 2023 deals).
RWI IMPACT: Strong. 91% of RWI-identified deals with PPA include a separate PPA escrow vs 66% of no-RWI deals. RWI buyers are more likely to insist on separate PPA escrow ring-fencing (they need certainty on the indemnification side). No-RWI deals more often route PPA adjustment through indemnification escrow (67% of no-separate-PPA-escrow deals use indemnity escrow as backstop).
TREND: PPA frequency stable at ~92%. Separate PPA escrow growing: 72% (2021) → 78% (2024). Median PPA escrow size grew 2021-2023 (0.62%→1.00%) then slightly compressed to 0.98% in 2024. Buyer review-at-closing right slowly growing (12%→14%).
|source:direct-read:T1 (slides 19-24, SRSA 2025 Deal Terms Study, n=2200+ closed deals)
```

```
TERM: EARNOUTS (Non-Life Sciences)
MARKET (2024): 22% of non-LS deals include an earnout, down from 2023 peak of 33%. 68% of earnout deals have multiple earnouts (32% single earnout). Revenue is dominant metric (65%), earnings/EBITDA at 13% (down from 22-23%), other at 22%. Median earnout potential: 31% of closing payment. Median earnout length: 24 months. Distribution: 24% ≤1 year, 31% >1-2 years, 31% >2-3 years, 15% >3-4 years, 0% beyond 4 years.
SELL-SIDE WIN: Resist earnout inclusion entirely (78% of deals don't have one — absence is the norm, not the exception). If earnout required: revenue metric (65% market — hardest for buyer to manipulate vs EBITDA), short duration ≤1 year (24% of market supports this), inclusion of non-interference covenant "buyer shall take no action the primary purpose of which is to harm earnout achievement" (90% of earnout deals include this — effectively market standard). Seek acceleration on change of control (39% of deals include this). Resist offset of indemnification claims against future earnout payments: "express yes" to buyer offset is only 65% of deals — 33% silent + 2% express no creates negotiating room.
BUY-SIDE WIN: EBITDA/earnings metric (13% of 2024 deals, down from 22%) — more controllable by buyer, reflects actual profitability. Longer earnout (>2-3 years: 31% of market). No covenant to run business consistent with seller's past practices (97% of deals exclude this — almost never granted). No CRE standard (90% of deals exclude this in 2024 — sharp decline from 2023's 30%+). Express right to offset indemnification claims against future earnout payments (65% of deals). Include "earnout is not a security" provision (45% of 2024 deals, rising trend from 30% in 2021).
COMPROMISE: Revenue metric (market standard at 65%). Median 24-month duration. Non-interference covenant included (90% market — near-non-negotiable for sellers). No affirmative CRE covenant (90% market standard favors buyer on this). Acceleration on change of control (39% — split market, reasonable compromise point). Offset right: silent (33% of deals) rather than express yes or express no — avoids crystallizing the issue. Fiduciary disclaimer: not included (63% of deals omit — seller can push back on this).
RWI IMPACT: Not directly measured for earnouts in the study data shown. Earnouts are a separate risk allocation mechanism from RWI (which covers rep/warranty breach). RWI does not substitute for earnout protection.
TREND: Earnout frequency volatile: 15% (2019) → 33% (2023 peak) → 22% (2024). Revenue as metric stable ~62-65%. EBITDA declining (22%→13%). CRE covenant collapsed (30%+→10%) — significant buyer win in 2024. "Not a security" provision rising (30%→45%). Median earnout potential compressed slightly from 2023 peak (34%→31%).
|source:direct-read:T1 (slides 25-29, SRSA 2025 Deal Terms Study)
XVERIFY[openai:gpt-5.4]: PARTIAL — core stats confirmed, CRE 2023 baseline adjusted to "30%+" per footnote language
```

```
TERM: INDEMNIFICATION BASKETS — DEFINITIONS AND TYPES
MARKET (2024): 78% of deals have a basket (22% have no basket — rising from 15% in 2021). Of deals with baskets: deductible 38% (declining from 46% in 2021), first-dollar 39% (stable), combination 0% (effectively eliminated from 2% in 2021). Coverage: 97% of basket deals cover breaches of seller R&W, 3% cover covenant breaches, 10% cover other indemnity claims.
SELL-SIDE WIN: No basket (22% of 2024 deals — growing trend, best seller outcome). If RWI present: 44% of RWI deals have no basket — RWI dramatically increases probability of no-basket outcome. If basket required: deductible structure (seller only pays claims exceeding threshold, not dollar-one of claims above it). Basket size ≤0.5% of TV (59% of basket deals in 2024 are at this size or less). Basket excludes as many reps as possible via carveouts: capitalization (87%), due authority (84%), due organization (83%), broker fees (82%), ownership of shares (82%), fraud (81%) most commonly carved out of the basket.
BUY-SIDE WIN: First-dollar basket (39% of market in 2024) — all losses above basket threshold recoverable from dollar one. Larger basket (>1% of TV: only 10% of market — genuinely rare). If no RWI: first-dollar basket achieved in 61% of no-RWI deals (strong data support). Eligible claim threshold inclusion (28% of basket deals in 2024 — filters out nuisance claims below minimum threshold before counting toward basket).
COMPROMISE: Basket included (78% market). Deductible structure (slight market preference at 38% vs first-dollar's 39% — effectively tied). Size at 0.5% or less of TV (59% of market). Standard carveout package: capitalization, due authority, due organization, broker fees, ownership, fraud (all at 76%+ of deals with caps that carve them out). No eligible claim threshold (72% of basket deals don't include one).
RWI IMPACT: Dramatic. With RWI: 44% no-basket, 50% deductible, 6% first-dollar. Without RWI: 8% no-basket, 31% deductible, 61% first-dollar. RWI is the single largest determinant of basket type. RWI effectively purchases the deductible outcome for sellers.
TREND: No-basket frequency rising (15%→22% 2021-2024). Deductible declining (46%→38%). First-dollar stable (~39%). Combination eliminated. Direction: seller-favorable drift on basket definitions.
|source:direct-read:T1 (slides 68-73, SRSA 2025 Deal Terms Study)
```

```
TERM: INDEMNIFICATION CAPS
MARKET (2024 all deals): Average cap 11.1% of TV, median 10.0% of TV. 55% of deals with escrows/holdbacks set the cap equal to the escrowed amount. Distribution: 33% in the 5-10% range, 21% in 10-15% range, 24% ≤0.5% (these are predominantly RWI deals). Second-level caps: fundamentals capped at purchase price in 93% of deals with that carveout; taxes capped at purchase price in 83%; IP at ≤50% of TV in 56% (split between ≤25% at 21% and >25-50% at 35%); fraud/intentional misrepresentation: 60% capped at purchase price, 32% silent, 7% unlimited.
NO-RWI DEALS (2024): Average cap 14.6%, median 10.0%. Distribution concentrated: 44% in 5-10% range, 29% in 10-15% range. Upper tail meaningful: 10% at 15-20%, 6% at 20-50%, 3% above 50%.
RWI-IDENTIFIED DEALS (2024): Average cap 2.9%, median 0.35%. 80% of deals fall in the ≤0.5% range. This is the "survival" cap for seller direct liability — RWI policy provides the primary coverage above this.
SELL-SIDE WIN (no RWI): Cap = escrow/holdback amount in 55% of deals — effectively limits seller exposure to amounts already locked up. Cap at 5-10% of TV (33% of deals achieve this) rather than higher. Seek purchase-price cap on fundamentals (93% market — effectively non-negotiable at this point). Negotiate IP representations cap at ≤25% of TV (21% vs the 35% who accept up to 50%).
SELL-SIDE WIN (with RWI): Cap at 0.35% of TV or less (median for RWI deals) — dramatically superior outcome. RWI policy covers the buyer's recovery above this level.
BUY-SIDE WIN (no RWI): Cap at 10-15% of TV (29% of no-RWI deals achieve this — above the median). Hold out for 15%+ in higher-risk transactions (16% of no-RWI deals achieve 15%+). Fraud/intentional misrepresentation: unlimited liability or purchase price cap (7% unlimited, 60% purchase price — push for unlimited). IP cap closer to 50% of TV.
COMPROMISE (no RWI): 10% of TV (median, market convergence point). Cap equals escrow amount (55% of deals with escrows — natural structural tie). Standard fundamentals carveout at purchase price. Taxes at purchase price. IP at ≤50% of TV. Fraud at purchase price.
RWI IMPACT: Transformative on cap structure. XVERIFY confirmed: RWI-identified deals show median cap of 0.35% vs 10.0% for non-identified deals — strong association (not proven causation; sample contamination acknowledged). The practical effect: RWI shifts the indemnification burden from seller to insurer, allowing seller cap to compress to near-zero for seller direct liability.
TREND: Median all-deals cap stable at 10.0% (2022-2024). Average trending up slightly (10.1%→11.1%) — skewed by no-RWI deals with larger caps. RWI cap median declining (0.5%→0.35% 2022-2024). Gap between RWI and no-RWI widening as RWI market matures.
|source:direct-read:T1 (slides 74-79, SRSA 2025 Deal Terms Study)
XVERIFY[openai:gpt-5.4] + XVERIFY[google:gemini-3.1-pro-preview]: PARTIAL on RWI escrow association finding — data confirmed, causation language corrected
```

```
TERM: DEAL ESCROWS — FREQUENCY, SIZES, TYPES
MARKET (2024): 89% of deals have at least one escrow/holdback. 52% have two or more. By type: indemnification escrow 59%, PPA escrow 63%, other special escrows 29%. Aggregate size of all escrows (deals with indemnification escrow): average 10.25% of TV, median 10.0% of TV.
NO-RWI DEALS: 84% have one or more escrows (lower than RWI at 96% — counterintuitive, explained by RWI deals having more PPA escrows). Aggregate: average 13.2%, median 11.3%.
RWI-IDENTIFIED DEALS: 96% have one or more escrows (high because PPA escrow drives this). Aggregate escrow: average 4.1%, median 2.1% — dramatically lower, driven by minimal indemnification escrow.
SELL-SIDE WIN: Minimize indemnification escrow — achievable at 0.35% median in RWI context. In no-RWI context, hold to 5-10% range where 52% of no-RWI deals cluster. Avoid a second "other special escrow" (29% of deals have these — push back). Minimize escrow duration (study does not show duration data in scope, but shorter = better for seller). With RWI: aggregate escrow of ~2.1% of TV (median) represents practical target — still requires PPA escrow but indemnification escrow near-zero.
BUY-SIDE WIN: Full 10% indemnification escrow (median for all deals, 10%+ achievable in 29% of no-RWI deals at >10-15%). Special escrow for identified risks (29% of deals include these). PPA escrow separate and funded (78% of 2024 deals). Aggregate escrow above 10% of TV achievable in meaningful portion of no-RWI deals.
COMPROMISE: One escrow with both indemnification and PPA functions (or two separate escrows). Aggregate at ~10% of TV. Indemnification component at median. PPA component at ~1% of TV. Special escrows only for identified, specified risks.
RWI IMPACT: Already analyzed — the primary lever. RWI compresses aggregate escrow from median 11.3% (no-RWI) to 2.1% (RWI-identified). The driver is near-elimination of indemnification escrow (0.35% median vs 10.0%).
TREND: 2023 vs 2024 comparison (slides 80-81): Overall escrow frequency stable (~89-91.5%). Indemnification escrow frequency declining slightly (67%→59%). PPA escrow growing (60%→63%). Other special escrows declining (37%→29%). Aggregate size: slight compression (median 10.0% stable, average declining from 11.1% to 10.25%).
|source:direct-read:T1 (slides 80-81, SRSA 2025 Deal Terms Study)
```

```
TERM: GENERAL INDEMNIFICATION ESCROWS/HOLDBACKS — SIZES BY RWI STATUS
MARKET (2024, all deals with indemnification escrow): Average 7.8% of TV, median 9.0% of TV. Note: 41% of 2024 deals have no general escrow/holdback (up from 33% in 2023, 34% in 2022) — this is the subset that DOES have one. Distribution: 37% in 5-10% range, 21% in 10-15%, 12% at 1-5%, 21% at >0.5-1% (likely PPA-only or token escrows), 4% at 15-20%, 3% at 20-50%.
NO-RWI IDENTIFIED (2024): Average 10.9%, median 10.0%. Highly concentrated: 52% in 5-10% range, 29% at 10-15%. Very stable at 10% median across 2022-2024.
RWI IDENTIFIED (2024): Average 1.4%, median 0.35%. 66% at ≤0.5% of TV. 19% at 1-5%. Median declining: 0.5% (2022) → 0.5% (2023) → 0.35% (2024).
SELL-SIDE WIN: No indemnification escrow (41% of 2024 deals have none — growing). If escrow required without RWI: 5-10% range (52% of no-RWI deals). With RWI: 0.35% or less (achievable as median). Push for escrow = cap (55% of deals with escrows achieve this structuring).
BUY-SIDE WIN (no RWI): 10% indemnification escrow (median) or above. Target 10-15% range (29% of no-RWI deals). Avoid having cap exceed escrow amount.
COMPROMISE: No-RWI: 10% escrow = 10% cap (market convergence). RWI: token escrow of ~1-3% of TV for seller direct liability, RWI policy covers above. No-escrow structure: when RWI is confirmed and parties agree RWI provides sufficient coverage.
RWI IMPACT: Dominant. Median 0.35% (RWI) vs 10.0% (no-RWI). Association confirmed by XVERIFY (both models). Causation framing adjusted: RWI-identified deals are associated with dramatically smaller seller-funded indemnification escrows; the mechanism is that RWI policy absorbs the primary coverage function.
TREND: No-indemnification-escrow frequency rising markedly: 34% (2022) → 33% (2023) → 41% (2024). Median holding at 10% for no-RWI deals. RWI median compressing (0.5%→0.35%). Direction: fewer deals requiring any escrow; when required in RWI context, size declining.
|source:direct-read:T1 (slides 82-84, SRSA 2025 Deal Terms Study)
XVERIFY[openai:gpt-5.4] + XVERIFY[google:gemini-3.1-pro-preview]: PARTIAL — data confirmed, causation language corrected to association framing
```

```
TERM: SOURCES OF RECOVERY
MARKET (2024): Escrow dominates (59% of deals with post-closing indemnification use escrow as primary recovery source). Holdback at 19%. Earnout setoff only 2%. Clawback only 8%. RWI only 9%. Other 4%.
SELL-SIDE WIN: RWI-only structure (9% of deals) — seller has no escrowed funds, no holdback, recovery comes entirely from insurance policy. This is the cleanest seller exit. Alternatively, holdback structure (19%) — buyer retains portion of proceeds rather than third-party escrow, potentially simpler administration.
BUY-SIDE WIN: Escrow structure (59% — dominant) with full escrow amount at 10% of TV and clear drawdown mechanics. Clawback provisions (8%) — allow buyer to recover from sellers post-distribution, though enforcement is practically difficult.
COMPROMISE: Third-party escrow (59% market standard). Sized at ~10% of TV. Professional escrow agent (SRSA and similar). Clear claim procedures and timeline.
RWI IMPACT: RWI-only at 9% of deals. RWI identified deals more likely to rely on insurance as primary source and minimal escrow as backstop. Trend: RWI-only growing (4% in 2021 → 9% in 2024), holdback declining slightly (16%→19% then varying), escrow as primary source stable (~57-68%).
TREND: Escrow declining as sole/primary source (68% in 2021 → 59% in 2024). RWI-only growing (4%→9%). Holdback usage fluctuating (16%→19%). Overall recovery source mix shifting toward insurance.
|source:direct-read:T1 (slide 85, SRSA 2025 Deal Terms Study)
```

```
TERM: POST-CLOSING EXPENSE FUND SIZES
MARKET (2024): 96% of all 2024 deals include a post-closing expense fund. Average size 0.36% of TV, median 0.22% of TV — declining from 2022 peak (0.53% average, 0.25% median). Dollar amounts: deals without earnouts average $227,000 (up from $194,000 in 2023); deals with earnouts average $337,000 (up from $332,000 in 2023). Earnout deals require larger expense funds due to longer post-closing period and earnout administration complexity.
SELL-SIDE WIN: Expense fund sized at median 0.22% of TV — minimum necessary to cover seller representative costs. Resist buyer pressure to minimize the fund (99% frequency means nearly zero deals close without one — focus is on size). Right-size based on expected complexity: no-earnout deals closer to $200K-$230K; earnout deals closer to $335K-$340K.
BUY-SIDE WIN: Buyer preference is neutral on expense fund size (funds belong to sellers for their own administrative costs). Buyer may prefer smaller fund to ensure more proceeds are available for escrow. This is primarily a seller-controlled term.
COMPROMISE: Fund included (96% market standard — non-negotiable). Size: 0.22% of TV median for no-earnout deals, ~0.30-0.36% for earnout deals. Dollar floors make sense at smaller deal sizes.
RWI IMPACT: Not directly segmented in data. RWI-identified deals likely have smaller expense funds (less post-closing administration needed without large indemnification escrow to manage).
TREND: Declining as % of TV (0.33%→0.22% median, 2021-2024) but rising in dollar terms ($194K→$227K for non-earnout deals). Consistent with overall deal size inflation — the fund is right-sizing to actual costs rather than scaling proportionally with TV.
|source:direct-read:T1 (slide 86, SRSA 2025 Deal Terms Study)
```

#### CROSS-CUTTING OBSERVATIONS
1. RWI IS THE DOMINANT STRUCTURING VARIABLE: Across every financial mechanic analyzed, RWI presence/absence produces the single largest divergence in outcomes. The RWI vs no-RWI difference is larger than any negotiation position a party can take within its category. This addresses H2 — 2024 data remains applicable to 2026 negotiations, but the RWI adoption rate (~42% of 2024 deals) is the key context variable.
2. MEDIAN ≠ MARKET STANDARD IN BIFURCATED MARKETS: For caps and escrows, the all-deals median (10%) masks two distinct sub-markets: no-RWI (10% median) and RWI (0.35% median). Reporting only the median without RWI segmentation would give misleading negotiating guidance. This confirms H3 (tails matter) and partially complicates H1 (market standard requires RWI-conditioning).
3. SELLER-FAVORABLE DRIFT 2021-2024: Multiple terms show seller-favorable movement: basket no-basket rate rising (15%→22%), indemnification escrow-free deals rising (34%→41%), RWI-only recovery growing (4%→9%), earnout CRE covenants declining (30%+→10%). Direction: sellers incrementally improving their position across most financial mechanics.
4. EARNOUT RISK ASYMMETRY: The data shows buyers winning on covenants (CRE at 10%, past-practices covenant at 3%) while sellers win on metrics (revenue dominant at 65%). This creates a structural tension: revenue earnout without buyer obligation to maximize revenue. The non-interference covenant (90%) is the seller's practical protection.
|source:direct-read:T1 (slides 19-29, 68-86)

### product-strategist
◌→✓ ANALYZE complete | slides 7-18, 94-99 | XVERIFY run on 2 load-bearing findings | DB[] applied

#### XVERIFY LOG
- F1 (market direction): XVERIFY[openai:gpt-5.4] PARTIAL + XVERIFY[google:gemini-3.1-pro-preview] DISAGREE. Both flag causal overreach. Calibrated: "mixed market with structural buyer advantage on economics, seller gains on legal mechanics."
- F2 (escrow/size correlation): XVERIFY[openai:gpt-5.4] PARTIAL + XVERIFY[google:gemini-3.1-pro-preview] AGREE. Negative correlation confirmed; causation hedged.

#### DB[] NOTES
DB[1]: Market direction — seller-favorable legal framing vs buyer-favorable economics. Multiple compression (52% reduction in median return 2021-2024) outweighs legal mechanic improvements in $ impact. Net: buyer structural advantage.
DB[2]: PE portco buyer at $282.6M avg vs US Public at $250.5M — counterintuitive. Possible bolt-on synergy premium OR sample selection. Verdict: use directionally, not as precise benchmark.
DB[3]: Multiple compression (2.5x median) — equilibrium vs seller selection effect. Average also declining (6.3x→5.6x), confirming real compression not purely selection effect.

---

TERM: TRANSACTION VALUE MIX AND BUYER TYPE POWER (slide 10)
MARKET (2024): Jumbo (>$750M)=10% of SRSA sample (3% in 2023 — SRSA sample only; XVERIFY disputed as broader market claim); ≤$25M=22%; $25-50M=19%; $50-100M=12%; $100-250M=22%; $250-750M=15%. US Public=35%; US PE=15%; US Private PE-backed=21%; US Private non-PE=14%; Non-US=14%. Financial buyers total ~36%.
SELL-SIDE WIN: Target US Public strategic buyer — 6.9x avg return on seller equity (vs 4.9x PE, 4.8x US Private). Competitive auction with multiple strategics maximizes leverage on all downstream terms.
BUY-SIDE WIN: US Private buyer in sub-$50M deal — lowest absolute deal values ($114.2M avg for US Private overall), least competition, strongest leverage on all terms.
COMPROMISE: Mid-market with strategic or PE portco buyer. PE portco pays highest absolute prices ($282.6M avg) but seller returns (4.9x) trail strategic buyer returns (6.9x).
RWI IMPACT: PE's ~36% deal share at 42% overall RWI rate implies PE-associated deals are disproportionately RWI-covered. RWI reduces escrow demands; doesn't change price dynamics.
TREND: PE buyer share stable 2021-2024 (~35-39%). Permanent norm-setter, not cyclical.
|source:independent-research[SRSA primary]|T1

---

TERM: TRANSACTION STRUCTURE AND SIGN/CLOSE TIMING (slide 11)
MARKET (2024): Merger=72%; Stock Purchase=26%; Asset Purchase=2%. Sign-then-Close=59%; Simultaneous=41%.
SELL-SIDE WIN: Merger + simultaneous sign/close (41% achievable) — eliminates gap risk, no MAE walk right exposure, no interim covenant period.
BUY-SIDE WIN: Sign-then-Close (59% market norm) — financing time, additional diligence, closing conditions. Asset purchase (2%) is buyer-optimal for liability isolation but near-impossible to achieve.
COMPROMISE: Merger with sign-then-close + tight outside date and seller walk rights. MAE definition is the primary negotiation battleground.
RWI IMPACT: RWI deals more likely to achieve simultaneous sign/close — RWI process completes during diligence, removing gap period need. Understated seller benefit of RWI adoption.
TREND: Merger stable (~72%). Simultaneous sign/close holding at ~41% — not growing despite RWI availability.
|source:independent-research[SRSA primary]|T1

---

TERM: VALUATION MULTIPLES — RETURN ON EQUITY CAPITAL INVESTED (slide 12)
MARKET (2024): Median=2.5x; Average=5.6x. Down from 2022 peak (4.0x median, 9.1x avg). Median flat vs 2023; average declining.
SELL-SIDE WIN: Top-quartile outcomes at 5x+ (scatter right tail to 75x for outliers). Sellers with differentiated IP/market position in competitive auction can target above 5x.
BUY-SIDE WIN: Buyers clearing deals at 2.5x median — recapturing valuation discipline post-ZIRP. Down from 5.2x median in 2021; 52% reduction in seller returns over 3 years.
COMPROMISE: 2.5x median IS the cleared-market compromise. Sellers below this should question timing; buyers above this are paying above-median prices.
RWI IMPACT: Neutral on multiples. RWI-enabled deals may command slight seller premium by reducing escrow holdbacks that reduce effective seller proceeds.
TREND: Secular decline (2021 5.2x → 2022 4.0x → 2023-2024 2.5x median). Most significant buyer-favorable structural shift in dataset. Average also declining (8.5x→5.6x).
DB[3]: 2.5x persistence could reflect seller selection (only acceptable-return sellers transact). Average decline (6.3x→5.6x) suggests real compression, not purely selection effect.
|source:independent-research[SRSA primary]|T1

---

TERM: INVESTMENT EXIT TIMING (slide 13)
MARKET (2024): Median hold=6.9 years (up from 6.0 in 2019); Average=8.2. Median equity financing rounds=4.0. Median equity capital invested=$34M; Average=$91M.
SELL-SIDE WIN: Extended hold data supports premium pricing argument. >50% of 2024 deals exit at 9+ years per chart — long holds earn premium expectation.
BUY-SIDE WIN: Rising hold periods signal seller exit pressure. Average $91M capital at work creates urgency to transact at any reasonable multiple.
COMPROMISE: 6.9 year median hold creates natural alignment — sellers at median hold have reasonable duration; buyers can price on current multiples without fear of continued holding.
RWI IMPACT: Neutral.
TREND: Hold periods extending (6.0→6.9 median 2019-2024). Equity capital rising ($27M→$34M median). Structural pressure toward exit builds.
|source:independent-research[SRSA primary]|T1

---

TERM: CLOSING CONSIDERATION STRUCTURE (slide 14)
MARKET (2024): All cash=59%; Cash+Management Rollover=18%; Cash/Stock combo=17%; All stock=6%. Cash-dominant total=77%.
SELL-SIDE WIN: All-cash deal (59% market) — clean exit, no equity risk, no lock-up. Achievable in majority of deals.
BUY-SIDE WIN: Cash+Management Rollover (18%, rising from 15% in 2023) — management alignment, lower cash outlay, key-person risk mitigation. Rising trend signals increasing buyer success normalizing this.
COMPROMISE: Cash/Stock combo (17%) — cash certainty on majority, some equity exposure. Down from 24% in 2021; middle ground shrinking as market bifurcates.
RWI IMPACT: RWI-covered deals more frequently all-cash — RWI removes need for escrow holdbacks that complicate consideration structure. Understated seller benefit.
TREND: Bifurcation emerging. Cash+rollover rising. Cash/stock combo declining (24%→17%). Market polarizing between clean cash exit and management-stays-in structures.
|source:independent-research[SRSA primary]|T1

---

TERM: MANAGEMENT CARVEOUTS — FREQUENCY (slide 15)
MARKET (2024): 5.1% of deals include carveout (down from 6.0% peak 2023). Size-dependent: ≤$50M=7.8%; $50-100M=5.2%; >$100M=1.4%.
SELL-SIDE WIN: For distressed management (<1x equity return), 50% market precedent makes carveout effectively "market standard" for true distress.
BUY-SIDE WIN: 5.1% overall frequency supports declining as non-standard. In >$100M deals, 1.4% frequency is near-categorical precedent for refusal.
COMPROMISE: Carveout appropriate only when return is sub-1x OR 1-3x with documented management contribution. >3x: categorically refuse (0% market precedent, absolute gate).
RWI IMPACT: Neutral. Carveouts address liquidation preference waterfall, not rep/warranty risk.
TREND: Volatile (4.5%→3.6%→6.0%→5.1%). Linked to distress conditions. Not directional.
|source:independent-research[SRSA primary]|T2

---

TERM: MANAGEMENT CARVEOUTS — SIZE (slide 16)
MARKET (2024): Median carveout size=12.7% of TV (highest 2021-2024; up from 6.8% in 2023).
SELL-SIDE WIN: 12.7% is 2024 anchor. Rising from 6.8% trough supports "market moving up" argument.
BUY-SIDE WIN: Use 2023 precedent (6.8%) as counter-anchor. Carveout should cover guaranteed floor, not windfall.
COMPROMISE: 8-10% of TV — between 2023 trough and 2024 peak.
RWI IMPACT: Neutral.
TREND: High volatility (small-sample effect — ~5% of deals, so each year driven by handful of transactions). Do not over-read year-to-year swings as directional signals.
|source:independent-research[SRSA primary]|T2

---

TERM: MANAGEMENT CARVEOUTS — RETURN RELATIONSHIP (slide 17)
MARKET (2024): <1x return: 50% include carveout (up from 42% 2023). 1-3x return: 50% include carveout (down from 58% 2023). >3x return: 0% (absolute, consistent 2023-2024).
SELL-SIDE WIN: <1x return: 50% precedent is effectively "market standard" for true distress. Trend moved favorable (42%→50%) in one year.
BUY-SIDE WIN: >3x return: categorically refuse — 0% historical precedent, absolute. 1-3x zone: 50% of deals don't grant carveout — negotiate hard for the no-carveout outcome.
COMPROMISE: 1-3x zone at 50% frequency IS the contestable middle. Size proportional to gap between management equity value and market-competitive retention economics.
RWI IMPACT: Neutral.
TREND: Gatekeeping strengthening — carveouts increasingly reserved for true distress.
|source:independent-research[SRSA primary]|T2

---

TERM: TREATMENT OF OPTIONS (slide 18)
MARKET (2024): Not assumed=86% (reverting from 78% in 2023). Assumed=14%. Optionholders contribute to escrow=42% (up from 36% in 2023). Full vesting acceleration=14% (up from 8% in 2023).
SELL-SIDE WIN: No escrow contribution (58% of deals — majority position and achievable norm). Full vesting acceleration (14% achievable). Push for both.
BUY-SIDE WIN: No assumption (86% market — overwhelming precedent). No acceleration (86% market norm). Escrow contribution from optionholders (42%, trending up). All three simultaneously achievable with strong data support.
COMPROMISE: No assumption + no acceleration + proportional escrow contribution — statistical market center.
RWI IMPACT: RWI reduces overall escrow; optionholder absolute dollars in escrow decrease correspondingly.
TREND: Assumption declining back to norm (14%). 2023 spike to 22% anomalous. Escrow contribution recovering (36%→42%). Acceleration recovering (8%→14%).
|source:independent-research[SRSA primary]|T1

---

TERM: RWI ADOPTION AND STRUCTURAL MARKET EFFECTS
MARKET (2024): 42% of SRSA deals identified with RWI. Caveat: SRSA dataset skews larger/more sophisticated; lower-middle market penetration likely lower (per XVERIFY flag). Materially affects: baskets (44% no-basket with RWI vs 8% without — per loan-ops data), escrow (0.35% vs 10.0% median), survival, sandbagging, materiality scrape.
SELL-SIDE WIN: RWI deal achieves: near-zero indemnification escrow (0.35% median), shorter/no survival, potential elimination of sandbagging, narrower materiality scrape. Fastest, cleanest exit.
BUY-SIDE WIN: Cleaner deal process; rep protection maintained through insurer (not removed, redirected); tighter initial reps; special escrows for known risks still available.
COMPROMISE: RWI where deal economics support it (typically $50M+ where premium proportionate). 42% market rate represents current equilibrium.
KEY STRUCTURAL FINDING: Even non-RWI deals shifting toward seller-favorable terms because RWI has reset buyer expectations. RWI norms leaking into entire market — non-RWI deals get shorter survival, narrower baskets, less sandbagging than 5 years ago. This is the secondary-order market power shift.
TREND: 42% in 2024; accelerating per SRSA commentary. RWI spillover to non-RWI deals is the key 2024 structural development (per slide 8).
|source:independent-research[SRSA primary]|T1

---

TERM: TERMINATION FEES (slides 94-95)
MARKET (2024): No fee=79%. Buyer pays=18%. Seller pays=2%. Two-way=2%. Buyer-paid size: Median=5.3%, Average=5.5% of TV. History: 2022 (6.2% avg / 5.0% median) → 2023 trough (3.8% / 4.1%) → 2024 recovery (5.5% / 5.3%).
SELL-SIDE WIN: Buyer-paid termination fee at 5%+ (achievable in 18% of deals; 2024 median=5.3% supports anchor). Most achievable in competitive auction context.
BUY-SIDE WIN: No termination fee (79% market — overwhelming data support). If forced: push below 5% using 2023 trough (3.8%) as anchor. Categorically resist seller-pays or two-way structure (combined 4% market).
COMPROMISE: Buyer-paid at 3.5-4.5% — below 2024 median (5.3%), above 2023 trough (3.8%). Covers deal costs and lost opportunity without being punitive.
RWI IMPACT: Inferred — RWI-covered deals may support higher seller demand for termination fee (seller invested in RWI process, making buyer walk more costly). Not directly measured.
TREND: U-shaped recovery. 2024 rebound to 5.3% median near 2022 levels. Direction: seller-favorable in 2024. Fee size is an elastic term.
|source:independent-research[SRSA primary]|T1

---

CORRELATIONS: TRANSACTION VALUE VS BUYER TYPE (slide 97)
Average TV: US Public=$250.5M; US PE=$282.6M; US Private=$114.2M; Non-US=$259.9M. Average return multiple: US Public=6.9x; US PE=4.9x; US Private=4.8x; Non-US=4.8x.
SELL-SIDE WIN: Target US Public buyer — 6.9x avg return (40% premium over PE at 4.9x), $250.5M avg TV.
BUY-SIDE WIN: US Private buyer — $114.2M avg (lowest), 4.8x return, least competition.
COMPROMISE: PE portco buyer ($282.6M avg, 4.9x return) — highest absolute prices, moderate returns. Portco premium doesn't translate proportionally to seller returns.
XVERIFY NOTE: GPT-4 flags deal selection bias — PE portco deals at higher values may reflect target maturity, not buyer generosity. Use directionally.
|source:independent-research[SRSA primary]|T1

---

CORRELATIONS: TRANSACTION VALUE VS ESCROW SIZE (slides 98-99)
Negative correlation confirmed (2021-2024 combined dataset). Sub-$50M (teal): median ~10-13% escrow, wide variance (2-48%+). $50-200M (orange): cluster 5-10%, tighter distribution. $200M+: trend line approaches 3-5%. Sub-$50M segment has steeper negative slope within it than $50M+ segment.
SELL-SIDE WIN: Larger deals — cite trend line to resist high escrow. $100M+: sub-5% market-supported. $250M+: 3% defensible. RWI amplifies further.
BUY-SIDE WIN: Small deals (<$50M) — wide variance to 30-50%+ in outlier cases supports above-median escrow demand.
COMPROMISE: Size-indexed escrow framework: ≤$25M=10-12%; $25-50M=8-10%; $50-100M=5-8%; $100-250M=4-6%; >$250M=2-4%. Mirrors data distribution; principled anchor for both sides.
XVERIFY: GPT-4 PARTIAL (correlation confirmed, causation hedged). Gemini AGREE (correlation and standard market rationale confirmed). XVERIFY-PARTIAL overall.
|source:independent-research[SRSA primary]|T1 |source:external-openai-gpt-5.4| |source:external-google-gemini-3.1-pro-preview|

---

META: NET MARKET DIRECTION 2024
FINDING: Bifurcated. Legal/indemnification terms: seller-favorable. Economics/valuation: buyer-favorable. These vectors run in opposite directions.
BUYER LEVERAGE (structural): Multiple compression 52% (5.2x→2.5x median 2021-2024); PE permanence as norm-setter (~36% deal share); extended seller hold periods (6.9yr median, rising); management rollover rising (15%→18%); option non-assumption holding (86%).
SELLER LEVERAGE (incremental): Walk-away deal rate increasing; survival periods shortening (50% more sub-12mo deals); earnout periods capping at 4 years; termination fee recovery (5.3% median); RWI spillover to non-RWI deals; 50% carveout frequency in <1x return deals.
NET DIRECTION: Mixed with structural buyer advantage on economics. Multiple compression loses full turns of value; legal term improvements recover basis points. On economic fundamentals, buyers hold structural advantage. Sellers winning incremental legal improvements — likely accepting lower economics for cleaner legal structures.
XVERIFY CALIBRATION: Gemini disputed blanket "seller-favorable" framing with high confidence. Calibrated formulation: "mixed market with structural buyer advantage on economics, seller gains on legal mechanics."
|source:independent-research[SRSA primary]|T1

META: STICKY VS ELASTIC TERMS
STICKY (stable 2019-2024): Merger structure dominance (~72%); no termination fee in 79%; option non-assumption (~86%); management carveout frequency (~4-6%); no-carveout in >3x return deals (0%, absolute); PE buyer share (35-39%).
ELASTIC (shift with conditions): Valuation multiples (5.2x→2.5x); carveout size (6.8%→12.7% in one year); termination fee size (3.8%→5.3% recovery); optionholder escrow contribution (65%→36%→42%); management rollover (15%→18%); earnout frequency (15%→33%→22%); RWI adoption rate.
STRATEGIC IMPLICATION: Reserve negotiating leverage for elastic terms. Arguing for sticky terms (option assumption, carveouts in >3x return deals) is expensive signaling with data-certain losses.
|source:agent-inference|T2

META: PE AS PERMANENT MARKET NORM-SETTER
FINDING: PE buyers ~36% of deals + PE-backed portcos as sellers = significant PE-on-PE dynamic. This concentrates RWI adoption and sophisticated term negotiation at the deal type shaping "market standard" for all transactions.
BUYER LEVERAGE: PE standardized playbook (RWI, clean escrow, walk-away, rollover) sets expectations market-wide. Non-PE sellers face sophistication gap.
SELLER LEVERAGE: PE-backed sellers have matching sophistication. PE-on-PE deals resolve faster and cleaner.
NET DIRECTION: PE dominance is buyer-favorable for non-PE sellers. Non-PE sellers should invest in experienced M&A counsel who know PE norms to close the asymmetry.
|source:agent-inference|T2

---

H1 CONFIRMED for most terms. RWI bifurcation requires dual-standard for financial terms (caps, escrows, baskets). Single pooled median misleading without RWI conditioning.
H2 PARTIAL CONFIRM. Structural trend directions durable. Specific bps may have shifted 2025-2026. Use 2024 as floor for elastic terms, hard anchor for sticky terms.
H3 CONFIRMED. Tails show meaningful variance (escrow to 48%+ in small deals, carveout size year-to-year swings). Tails are where sell-side wins live.
H4 CONFIRMED. Median is resolved compromise; sell-side and buy-side win positions identifiably different in both directions for each term.

**product-strategist → CONVERGE ✓**

### m-and-a-deal-counsel

**SCOPE:** Legal deal term provisions — slides 30-67, 87-95 | SRSA 2025 (2,200+ private-target deals, $505B, 2019-2024)
**XVERIFY-LB1** (no-survival/RWI, slide 57): PARTIAL — 54% vs 18% data confirmed; precision required: applies to GENERAL reps only; seller retains exposure for fundamental reps, taxes, fraud, specific indemnities. |source:external-openai-gpt-5.4|
**XVERIFY-LB2** (materiality scrape, slides 60-61): AGREE high confidence — all percentages confirmed. |source:external-openai-gpt-5.4|

---

#### A: PERVASIVE QUALIFIERS

```
TERM: MAE Definition — Forward-Looking Language and "Prospects"
MARKET (2024): 98% of deals with MAE definition include forward-looking language. Of those: 86% "would be"; 10% "could be"; 4% other. "Prospects" included: 10% (stable 2020-2024 at 9-12%).
SELL-SIDE WIN: "Would be" standard (86%) + no "prospects" (90% exclude). "Would be" requires buyer to show effect definitively would be material — high bar. Excluding "prospects" avoids liability for speculative future performance degradation.
BUY-SIDE WIN: "Could be" standard (10%) + "prospects" inclusion (10%). Lower materiality threshold; MAE exposure extended to forward-looking business trajectory.
COMPROMISE: "Would be" without "prospects" — where 86-90% of deals land.
RWI IMPACT: MAE definition governs closing condition walk right; RWI operates post-closing. Largely independent dynamics.
TREND: STABLE. "Would be" at 86%, "prospects" exclusion at ~90% across 2020-2024.
SETTLED vs NEGOTIATED: SETTLED. Forward-looking language (98%) and "would be" (86%) are settled seller-favorable norms. "Prospects" genuinely negotiated at the margin — 10% inclusion rate.
|source:independent-research|:T1
```

```
TERM: MAE Definition — Carveouts and Disproportionate Effect Qualifier
MARKET (2024): 96% of MAE definitions include carveouts. Frequency (2024): war/terrorism 99%, economic conditions 98%, industry conditions 92%, changes in law 92%, accounting standards 91%, financial market downturn 88%, pandemic 81%, actions required by agreement 71%, announcement of deal 67%. Disproportionate effect qualifier: 96% of carveout deals include at least one.
SELL-SIDE WIN: Full nine-category carveout suite. War/terrorism (99%), economic conditions (98%), industry conditions (92%) are effectively non-negotiable. Pandemic (81%) achievable. Minimize scope of disproportionate effect qualifier — narrow its application.
BUY-SIDE WIN: Omit pandemic (19% exclude), financial market downturn (12% exclude), announcement of deal (33% exclude). Insist on broad disproportionate effect qualifier on all carveouts — recaptures MAE protection when seller is disproportionately hit by general market event.
COMPROMISE: Full nine-category suite (de facto standard) with disproportionate effect qualifier included but negotiated in scope and application.
RWI IMPACT: Closing condition mechanism; RWI operates post-closing. Largely independent.
TREND: Pandemic carveout declined (89% in 2023 → 81% in 2024) — normalizing post-COVID.
SETTLED vs NEGOTIATED: War/terrorism, economic conditions, industry conditions, changes in law — SETTLED (91-99%). Pandemic, financial market downturn — GENUINELY NEGOTIATED (81-88%). Disproportionate effect qualifier scope — GENUINELY NEGOTIATED even though inclusion is settled (96%).
|source:independent-research|:T1
```

```
TERM: Knowledge Standards
MARKET (2024): 93% constructive; 6% actual only; 1% undefined. Among constructive deals: 54% "reasonable or due inquiry"; 49% "reasonable or due inquiry of knowledgeable persons"; 10% role-based. 17% include multiple elements.
SELL-SIDE WIN: Actual knowledge only (6%) — no inquiry obligation. If constructive unavoidable: narrowest definition, limited named individuals, no "of knowledgeable persons" extension.
BUY-SIDE WIN: Constructive with "reasonable or due inquiry of knowledgeable persons" (49%) + role-based overlay (10%) — broadest attribution, imputing what officers/directors in relevant roles should have known.
COMPROMISE: Constructive with "reasonable or due inquiry" (54% modal) without "of knowledgeable persons." Inquiry duty without organization-wide attribution.
RWI IMPACT: Knowledge standard governs seller's personal liability on fundamental reps and fraud carveouts even in RWI deals. Less central to general rep analysis (flows to insurer in no-survival RWI deals).
TREND: SETTLED. 93% constructive rate stable throughout study period.
SETTLED vs NEGOTIATED: SETTLED that constructive applies (93%). GENUINELY NEGOTIATED: "of knowledgeable persons" inclusion; role-based overlay; knowledge group composition.
|source:independent-research|:T1
```

---

#### B: SELLER'S REPS, WARRANTIES, AND COVENANTS

```
TERM: "No Undisclosed Liabilities" Representation
MARKET (2024): 97% inclusion. Party favored: 81% buyer-favorable (up from 69% in 2021); 19% seller-favorable. Knowledge-qualified: 1.9% of 2024 deals.
SELL-SIDE WIN: Seller-favorable definition (19%) — narrower scope, GAAP balance-sheet limitation, knowledge qualification (1.9% achieve). Best: balance-sheet-only + knowledge qualifier.
BUY-SIDE WIN: Buyer-favorable definition (81%) without knowledge qualification (98.1%). Broad scope covering all undisclosed liabilities not on financial statements or disclosure schedules.
COMPROMISE: Buyer-favorable definition (81% norm) without knowledge qualification. Seller protects through adequate disclosure schedules.
RWI IMPACT: Near-universal (97%); heavily scrutinized by underwriters. In no-survival RWI deals, seller's general rep exposure eliminated.
TREND: MOVING BUYER-FAVORABLE. 69% → 81% buyer-favorable (2021-2024), 12-point shift. Stabilized at 81% in 2023-2024.
SETTLED vs NEGOTIATED: SETTLED as to inclusion (97%). GENUINELY NEGOTIATED: definition scope.
|source:independent-research|:T1
```

```
TERM: "Compliance with Laws" Representation
MARKET (2024): 99% inclusion. 98% cover past AND present compliance; 90% include notice of violation language.
SELL-SIDE WIN: Present-only scope (2% of deals without past compliance) + no notice of violation language (10% exclude). Eliminates liability for remediated historical violations.
BUY-SIDE WIN: Past and present (98%) + notice of violation (90%). Full temporal coverage plus notification obligation.
COMPROMISE: Past and present + notice of violation — market standard (~88% have both). Real negotiation is on materiality qualifiers within the rep text.
RWI IMPACT: Universal rep (99%); heavily scrutinized by underwriters.
TREND: SETTLED. 99% inclusion, 98%/90% subsidiary rates — no movement.
SETTLED vs NEGOTIATED: SETTLED as to inclusion, scope, and notice. Negotiation is on internal qualifiers and disclosure schedule adequacy.
|source:independent-research|:T1
```

```
TERM: "10b-5" and "Full Disclosure" Representations
MARKET (2024): 89% neither rep; "10b-5" only 10%; both 1%; full disclosure only 0%. RWI: 93% neither / 4% 10b-5. No-RWI: 85% neither / 15% 10b-5. Knowledge-qualified: 18% of "10b-5"-only deals.
SELL-SIDE WIN: Neither rep (89%). In RWI deals: 93% "neither" achievable. If buyer insists on 10b-5: knowledge qualify it (18% of such deals achieve this).
BUY-SIDE WIN: "10b-5" rep unqualified (82% of 10b-5 deals). Catch-all for material misstatements/omissions in any document provided to buyer.
COMPROMISE: No 10b-5 rep — the market norm (89%). Non-RWI: meaningful 15% buyer inclusion rate.
RWI IMPACT: SIGNIFICANT AND CONSISTENT. RWI suppresses 10b-5 by 11 percentage points (4% vs 15%), stable 2021-2024. RWI insurers cannot price open-ended catch-all liability. One of clearest RWI-driven term shifts in the dataset.
DB[] DIALECTICAL-1: Does 10b-5 absence matter if buyer has common law fraud? YES — the contractual rep matters: (1) operates within indemnification framework; (2) can be scrape-proofed; (3) may have longer survival; (4) shifts burden vs common law fraud's scienter requirement.
TREND: MOVING SELLER-FAVORABLE. Non-RWI "neither": 74% (2021) → 85% (2024). RWI "neither" stable at 93%.
SETTLED vs NEGOTIATED: SETTLED in RWI deals (93%). GENUINELY NEGOTIATED in non-RWI deals — 15% buyer inclusion rate is meaningful.
|source:independent-research|:T1
```

```
TERM: "No Other Representations" and "Non-Reliance" Clauses
MARKET (2024): Both: 68%; "no other reps" only 14%; "non-reliance" only 3%; neither 16%. RWI: 82% "both" vs 60% "both" (no-RWI). Fraud carveout: 33% of "both" deals include one.
SELL-SIDE WIN: Both clauses without fraud carveout (67% of "both" deals lack carveout). Seller disclaims reps beyond four corners; buyer contractually acknowledges non-reliance on extra-contractual information. Strongest protection against extra-contractual fraud claims. In RWI deals: 82% "both" achievable.
BUY-SIDE WIN: Neither clause (16%). If unavoidable: broad fraud carveout (33% of "both" deals preserve buyer's fraud remedies).
COMPROMISE: Both clauses without fraud carveout. Note: Delaware courts generally will not enforce non-reliance to bar intentional fraud even without express carveout — practical reality moderates both sides' positions.
RWI IMPACT: SIGNIFICANT. RWI increases "both clauses" from 60% to 82% (22-point gap in 2024, up from 15-point gap in 2021). RWI insurers require comprehensive contractual framework.
TREND: MOVING SELLER-FAVORABLE, driven by RWI market growth.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 16% "neither" and 33% fraud carveout rates confirm live territory. In RWI deals, "both without carveout" approaches settled (82%).
|source:independent-research|:T1
```

```
TERM: Privacy Representation
MARKET (2024): 98% inclusion (up from 97% in 2023).
SELL-SIDE WIN: Rep unavoidable (98%). Focus: narrow scope — knowledge-qualified, materiality-qualified, prospective-only, disclosure schedule carving known issues.
BUY-SIDE WIN: Unqualified broad-scope rep covering all applicable privacy laws, past and present compliance, past incidents, security program adequacy.
COMPROMISE: Rep included (non-negotiable). Negotiation on scope qualifications and disclosure schedule adequacy.
RWI IMPACT: RWI underwriters conduct specific privacy diligence. Privacy breaches are among the most-litigated post-closing claims.
TREND: SETTLED AND INCREASING. 97% → 98%. Mandatory for years.
SETTLED vs NEGOTIATED: SETTLED as to inclusion. GENUINELY NEGOTIATED as to scope.
|source:independent-research|:T2
```

```
TERM: Cybersecurity Representation
MARKET (2024): 95% inclusion (down from 97% in 2023).
SELL-SIDE WIN: Narrow scope — knowledge-qualified, materiality-qualified, no incident history, disclosure schedule carving known vulnerabilities.
BUY-SIDE WIN: Broad unqualified rep covering security programs, incident history (including unreported), breach notification compliance.
COMPROMISE: Rep included (95%) with materiality qualification and disclosure schedule exceptions.
RWI IMPACT: High-priority underwriting concern; underwriters may require penetration tests, SOC 2 reports for coverage.
TREND: STABLE (97% → 95% — likely consolidation into privacy rep rather than trend).
SETTLED vs NEGOTIATED: SETTLED as to inclusion (95%). GENUINELY NEGOTIATED as to scope.
|source:independent-research|:T2
```

```
TERM: Sexual Misconduct Representation
MARKET (2024): 74% inclusion (up from 68% in 2023). Among rep-deals: covers settlement agreements 61% (up from 43% in 2023); covers allegations 95%; corrective action language 17%.
SELL-SIDE WIN: Rep not included (26% of deals — realistic objective where seller has leverage). If included: no settlement agreement coverage (39% exclude), no corrective action (83% exclude), limited to formal allegations.
BUY-SIDE WIN: Rep included (74%) covering allegations (95%), settlement agreements (61%), corrective action (17%).
COMPROMISE: Rep included; limited to formal allegations (95%) and settlement agreements (61%); without corrective action (83% exclude).
RWI IMPACT: Not broken out. Underwriters will require disclosure of known matters regardless.
TREND: MOVING BUYER-FAVORABLE. 68% → 74%. Settlement coverage: 43% → 61% — substantial scope expansion in one year.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 26% non-inclusion and significant scope variation confirm active negotiation.
|source:independent-research|:T2
```

```
TERM: Covenant — Seller's Duty to Notify Buyer of Pre-Closing Breaches
MARKET (2024): R&W breaches: 53% express duty / 47% no express duty / 1% seller may update. Covenant breaches: 48% express duty / 52% no express duty. Excludes sign-and-close.
SELL-SIDE WIN: No express duty for R&W or covenant breaches (47% and 52% of deals, respectively).
BUY-SIDE WIN: Express duty to notify for both R&W and covenant breaches. Enables renegotiation or exercise of walk rights before closing.
COMPROMISE: Market genuinely split (53/47 and 48/52). Express duty for R&W breaches (53% slight majority) without right to update disclosure schedules is the practical middle ground.
RWI IMPACT: Not broken out. Known breach not disclosed to insurer at underwriting may void RWI coverage — practical dynamic may compel notification regardless of contractual duty.
TREND: 2024 data only — no multi-year trend available.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. Near-perfect split on both measures.
|source:independent-research|:T2
```

```
TERM: No-Shop/No-Talk Covenant
MARKET (2024): 95% included (excludes sign-and-close). Of those: 98% no fiduciary exception; 2% fiduciary exception.
SELL-SIDE WIN: Covenant not included (5%) or fiduciary exception preserved (2%). Rare — requires significant auction leverage.
BUY-SIDE WIN: No-shop/no-talk (95%) without fiduciary exception (98%). Full lockup until closing.
COMPROMISE: No-shop/no-talk (95% — essentially unavoidable) without fiduciary exception (98%).
RWI IMPACT: Standard regardless of RWI.
TREND: SETTLED. 95% inclusion with 98% no-fiduciary-exception.
SETTLED vs NEGOTIATED: SETTLED.
|source:independent-research|:T1
```

---

#### C: CLOSING CONDITIONS

```
TERM: Accuracy of Seller's Representations — Timing and Materiality Standard
MARKET (2024): Timing: 71% signing AND closing; 29% closing only; 1% signing only. Materiality at closing: MAE qualifier 62%; "in all material respects" 34%; "in all respects" 5%. At signing: MAE 54%; material respects 41%; all respects 4%. Materiality scrape frequency (where qualifiers exist): 96% at signing, 94% at closing.
SELL-SIDE WIN: MAE qualifier at closing (62%) — the highest bar. Delaware courts have set extremely high threshold to establish MAE as a closing condition failure (Akorn, Channel Medsystems). Practically very difficult for buyer to exercise walk right.
BUY-SIDE WIN: "In all respects" at closing (5%) — any inaccuracy triggers condition failure. Rare; maximalist.
COMPROMISE: MAE qualifier at closing (62% — market norm and genuine convergence point). Buyer gets closing condition; seller gets high MAE bar. Materiality scrape (96% where qualifiers exist) operates at indemnification level, not closing condition level.
RWI IMPACT: In no-survival RWI deals, the closing condition on accuracy is seller's primary remaining risk allocation mechanism — importance of MAE qualifier may increase since there is no post-closing indemnification fallback.
TREND: MOVING SELLER-FAVORABLE at closing. MAE qualifier at closing (62%) exceeds signing (54%).
SETTLED vs NEGOTIATED: SETTLED that both-timing structure applies (71%). GENUINELY NEGOTIATED: MAE vs "in all material respects" vs "in all respects" — real variation across all three options.
|source:independent-research|:T1
```

```
TERM: "Material Adverse Change" Condition (MAC)
MARKET (2024): Stand-alone condition only: 42%. Both stand-alone and back-door: 51%. Back-door only: 4%. Neither: 4%.
SELL-SIDE WIN: No MAC condition (4%). If unavoidable: stand-alone only (42%) — avoids double-coverage.
BUY-SIDE WIN: Both stand-alone AND back-door (51%). Stand-alone gives explicit walk right; back-door flows through accuracy condition's MAE qualifier.
COMPROMISE: Stand-alone MAC only (42% — modal outcome absent "both"). Explicit walk right without back-door redundancy.
RWI IMPACT: Closing condition mechanism; independent of RWI's post-closing dynamics.
TREND: STABLE. Distribution consistent; no directional shift.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 42% vs 51% is a live negotiation point.
|source:independent-research|:T1
```

```
TERM: "No Legal Proceedings" Condition
MARKET (2024): 95% include condition. Of those: 87% any legal proceeding; 8% government only.
SELL-SIDE WIN: Government proceedings only (8%) or condition not included (5%).
BUY-SIDE WIN: Any legal proceeding (87%) — any pending litigation potentially triggers walk right.
COMPROMISE: Any legal proceeding coverage (87%) with standard qualification that proceeding must restrain closing or seek material damages.
TREND: MOVING BUYER-FAVORABLE. Any-proceeding scope: 83% → 87% (2023-2024). Government-only: 11% → 8%.
SETTLED vs NEGOTIATED: SETTLED as to inclusion (95%). GENUINELY NEGOTIATED: any vs government-only scope.
|source:independent-research|:T2
```

```
TERM: Legal Opinions from Seller's Counsel (Non-Tax)
MARKET (2024): Required as closing condition: 1% (down from 8% in 2019). Effectively extinct.
SELL-SIDE WIN: No legal opinion required (99% of deals). Standard.
BUY-SIDE WIN: Legal opinion required (1%). Counsel's professional assessment as condition.
COMPROMISE: No opinion required — this IS the market (99%).
TREND: STRONGLY MOVING SELLER-FAVORABLE. 8% → 1% (2019-2024). Consistently declining — effectively extinct.
SETTLED vs NEGOTIATED: SETTLED. 99% non-inclusion.
|source:independent-research|:T1
```

```
TERM: Appraisal Rights Condition (Mergers Only)
MARKET (2024): 56% of merger deals include condition. Among those: "not exercised by" % of shareholders 42%; "neither available to nor exercised by" 18%; minimum shareholder approval only 37%; "not available to" 4%. Threshold for "not exercised by": up to 4% (53%), >4-7% (31%), >7-10% (12%), >10% (4%).
SELL-SIDE WIN: No appraisal condition (44% of merger deals). If unavoidable: minimum shareholder approval approach (37%) at high threshold (>7-10%).
BUY-SIDE WIN: Condition included (56%); "not exercised by" at threshold up to 4% (53% of such deals). Maximum protection against appraisal overhang.
COMPROMISE: Condition included (56% norm); "not exercised by" at 4-7% threshold — moderate protection without hair-trigger walk right.
TREND: MIXED. Peak 72% (2020) → 56% (2024) — returning to pre-COVID baseline.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 56%/44% split and significant type/threshold variation.
|source:independent-research|:T2
```

---

#### D: INDEMNIFICATION STRUCTURE

```
TERM: General Survival of Seller's Reps and Warranties
MARKET (2024): 33% of all deals are "no survival." RWI breakdown: RWI — 54% no survival / 46% survival. No RWI — 18% no survival / 82% survival. RWI trend: 37% no-survival (2021) → 54% (2024).
SELL-SIDE WIN: No survival of general reps and warranties. In RWI deals: 54% no-survival achievable — seller has zero post-closing indemnification obligation for general R&W breaches; insurer steps in. Most seller-favorable outcome possible.
BUY-SIDE WIN: Survival (82% of non-RWI deals). Buyer retains right to assert breach claims against seller.
COMPROMISE: In RWI deals: 46%/54% split — the defining negotiation, neither outcome settled. In non-RWI deals, survival is standard (82%); debate shifts to period length.
RWI IMPACT: CRITICAL — LOAD-BEARING FINDING. 36-point differential (82% vs 46% survival) is the single largest RWI-driven term shift in the dataset. Trend accelerating.
PRECISION (XVERIFY-LB1 PARTIAL): "No survival" applies to GENERAL reps only. Seller retains exposure for fundamental reps (taxes, capitalization, due org/authority, ownership, broker fees), fraud carveouts, and specific stand-alone indemnities regardless of no-survival structure.
DB[] DIALECTICAL-1: Does no-survival truly protect sellers if insurers have subrogation rights? CONFIRMED YES — standard RWI anti-subrogation provisions bar insurer recourse against selling shareholders except for fraud.
TREND: STRONGLY MOVING SELLER-FAVORABLE in RWI deals. 37% → 54% no-survival (2021-2024). Non-RWI slowly trending (16% → 18%).
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. The 46/54 RWI split is the central indemnification negotiation.
|source:independent-research|:T1 | XVERIFY-LB1 PARTIAL
```

```
TERM: Stand-Alone Indemnities
MARKET (2024 vs 3-yr avg): Taxes 86% (75% avg). Capitalization 72% (65%). Litigation 72% (65%). Closing cert accuracy 65% (57%). Transaction expenses 57% (56%). Fraud/willful misrep 56% (55%). Dissenting shareholders 55% (55%). PPA/leakage 23%. Lower: employee comp 20%, fees/costs 20%, IP 17%, authority 12%, 280G 7%, data protection 5%, regulatory 3%, ERISA 3%.
SELL-SIDE WIN: Minimal list — accept taxes (86%, unavoidable) and fraud/willful misrepresentation (56%). Resist capitalization, litigation, dissenting shareholder, and closing certificate accuracy indemnities. CRITICAL IN RWI CONTEXT: stand-alone indemnities are typically excluded from RWI policy coverage — they represent seller's primary retained obligations in no-survival RWI deals.
BUY-SIDE WIN: Full suite at 55-86% (taxes, capitalization, litigation, closing certs, transaction expenses, fraud/willful misrep, dissenting shareholders). These survive outside basket/cap with potentially longer survival periods.
COMPROMISE: Accept taxes (86%), fraud/willful misrepresentation (56%), transaction expenses (57%). Negotiate specifically on capitalization, litigation, and dissenting shareholder indemnities.
RWI IMPACT: Stand-alone indemnities typically excluded from policy. In no-survival RWI deals, these are seller's primary residual obligations — negotiation shifts from general rep survival to stand-alone indemnity scope.
TREND: MOVING BUYER-FAVORABLE. Taxes +11pp, capitalization +7pp, litigation +7pp above 3-year averages.
SETTLED vs NEGOTIATED: Taxes — SETTLED (86%). Fraud — APPROACHING SETTLED (56%). Others — GENUINELY NEGOTIATED.
|source:independent-research|:T2
```

```
TERM: "Sandbagging" Provisions
MARKET (2024): Pro-sandbagging: 50%; Silent: 48%; Anti-sandbagging: 2%. RWI breakdown: RWI — pro 33% / silent 64% / anti 2%. No RWI — pro 55% / silent 43% / anti 2%.
SELL-SIDE WIN: Anti-sandbagging express provision (2% — explicit seller win; very rare). Realistic best: express anti-sandbagging in Delaware deals where silence defaults to pro-sandbagging. In RWI deals: 64% silent majority achievable; RWI makes sandbagging commercially less important.
BUY-SIDE WIN: Pro-sandbagging provision (50% overall; 55% non-RWI). Expressly preserves buyer's right to claim breach even with pre-closing knowledge.
COMPROMISE: Silent provision (48% overall). CRITICAL NUANCE: Under Delaware law, silence generally favors buyer — courts allow sandbagging absent express anti-sandbagging language (Cobalt Operating v. James Crystal). Sellers accepting "silent" in Delaware deals accept a buyer-favorable default.
RWI IMPACT: SIGNIFICANT. Pro-sandbagging drops from 55% (non-RWI) to 33% in RWI deals — 22-point gap. Silent: 43% → 64%. RWI insurers prefer silent/anti-sandbagging because known pre-closing breaches are excluded from coverage; pro-sandbagging creates structural disconnect with policy terms.
DB[] DIALECTICAL-2: Is "silent-in-Delaware" truly pro-buyer? Prevailing professional understanding: YES under Cobalt Operating, Allied Defense, and subsequent Delaware cases. Sellers accepting silence in Delaware deals accept buyer-favorable default.
TREND: MOVING SELLER-FAVORABLE in RWI deals (silent from 43% to 64%). STABLE in non-RWI deals (55% pro-sandbagging consistent).
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 50%/48%/2% split — the most evenly contested provision in the study. No settled market standard.
|source:independent-research|:T1
```

```
TERM: "Materiality Scrape" Inclusion
MARKET (2024): 86% include scrape. Of those: breach AND damages 60% (up from 57% in 2023); breach only 15% (up from 9%); damages only 11% (down from 19%); no scrape 14%. RWI: 80.4% include scrape — breach+damages 69.1%; breach only 8.8%; damages only 2.4%; no scrape 19.6%. No-RWI: 88.8% — breach+damages 55.1%; breach only 17.8%; damages only 16.0%; no scrape 11.2%.
SELL-SIDE WIN: No materiality scrape (14% — achievable). If unavoidable: damages-only scrape (11%) — preserves materiality qualifiers for breach determination; buyer must still show material breach to trigger any claim.
BUY-SIDE WIN: Scrape for breach AND damages (60% of scrape deals). Removes all materiality/MAE qualifiers from both breach determination and damages calculation.
COMPROMISE: Breach-only scrape (15% of scrape deals) — buyer asserts smaller breaches; seller limits resulting damages. Intermediate position.
RWI IMPACT: PARADOXICAL — XVERIFY-LB2 CONFIRMED. RWI deals: LOWER scrape inclusion (80.4% vs 88.8%) but where included, HIGHER "breach and damages" form (69.1% vs 55.1%). Interpretation: in no-survival RWI deals (54%), scrape is moot — no general rep indemnification exists. Among survival RWI deals, insurer needs trigger clarity → breach+damages form dominates.
DB[] DIALECTICAL-3: RWI scrape paradox — 80.4% includes moot no-survival cases. Among survival-only RWI deals, scrape inclusion likely much higher; breach+damages dominates for insurer clarity. Flag for reference-class-analyst cross-validation.
TREND: MOVING BUYER-FAVORABLE on scope. Breach+damages: 57% → 60%. Damages-only: 19% → 11%.
SETTLED vs NEGOTIATED: SETTLED as to inclusion (86%). GENUINELY NEGOTIATED as to form (60%/15%/11% distribution — no single form dominant).
|source:independent-research|:T1 | XVERIFY-LB2 AGREE (high confidence)
```

```
TERM: Reductions Against Buyer's Indemnification Claims
MARKET (2024): Insurance proceeds reduction: 83% (stable). Tax benefits reduction: 17% (down from 24% in 2022). Buyer required to mitigate: 57% (stable).
SELL-SIDE WIN: All three reductions — insurance proceeds (83% achievable), tax benefits (17% — achievable though declining), mitigation obligation (57%).
BUY-SIDE WIN: No tax benefit reduction (83% already exclude — buyer's default outcome). No mitigation obligation (43% exclude). Insurance proceeds essentially unavoidable (83%).
COMPROMISE: Insurance proceeds reduction (83% — settled). No tax benefit reduction (settled in buyer's favor). Mitigation obligation included (57% — slight market lean).
RWI IMPACT: Moot for general rep claims in no-survival RWI deals. Relevant in survival RWI deals and for specific indemnities.
TREND: Tax benefit reduction declining (24% → 17%, 2022-2024) — buyer-favorable.
SETTLED vs NEGOTIATED: Insurance proceeds — SETTLED. Tax benefit reduction — SETTLED in buyer's favor. Mitigation — GENUINELY NEGOTIATED (57%/43%).
|source:independent-research|:T2
```

```
TERM: General Survival Period / Time to Assert Claims
MARKET (2024): Median 12 months; average 12.7 months. Distribution: <12 months 21%; exactly 12 months 31%; >12 to <18 months 11%; 18 months 27%; 24 months 7%; >24 months 1%.
SELL-SIDE WIN: Sub-12 months (21% achieve) or exactly 12 months (31%). Combined 52% of deals close at 12 months or below.
BUY-SIDE WIN: 18 months (27%) or 24 months (7%). Combined 35% achieve 18+ months.
COMPROMISE: 12 months — the median and modal outcome (31%). Clearest convergence point in the dataset.
RWI IMPACT: Moot in no-survival RWI deals (54%). In survival RWI deals: contractual survival period and RWI policy coverage period are different questions (RWI policies: typically 3 years general reps, 6 years fundamental reps/taxes).
TREND: MOVING SELLER-FAVORABLE. Sub-12-month cohort: 13% (2020) → 21% (2024). Average: 13.8 months → 12.7 months.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED but converging. 12 months (31%) is modal; 18 months (27%) creates live negotiating band.
|source:independent-research|:T1
```

```
TERM: Second-Level Survival — Carveouts to General Survival Period
MARKET (2024): Carveout frequency: taxes 84%, capitalization 84%, due organization 83%, due authority 82%, ownership of shares 79%, broker/finder fees 78%, fraud 73%, no conflicts 54%, IP 37%, ERISA 13%, related-party 12%. Fundamental rep second-level: SOL 41%; >4 years 38%; >3-4 years 7%; >1-2 years 6%; ≤1 year 1%. 97% defined period (not indefinitely) in merger deals. Tax rep second-level: SOL 80%; >4 years 11%.
SELL-SIDE WIN: Narrow list — core fundamentals only (taxes, cap, org, authority, ownership, broker fees); shortest additional period (>1-2 years, 6%). Avoid IP (37%), no-conflicts (54%), ERISA (13%), related-party (12%).
BUY-SIDE WIN: Broad list including IP (37%), no-conflicts (54%), related-party (12%), fraud (73%), plus core fundamentals. SOL period for taxes (80%); >4 years for fundamental reps (38%).
COMPROMISE: Core fundamentals (78-84%) + fraud (73%) with SOL for taxes (80%) and defined >4-year period for fundamental reps (38%). Fraud survival itself is contested — 40% "indefinitely" is a meaningful buyer win where achieved.
RWI IMPACT: In no-survival RWI deals, carveout framework governs seller's residual exposure. Core fundamentals and fraud remain as seller obligations in both RWI and non-RWI structures.
SETTLED vs NEGOTIATED: SETTLED: core fundamentals (78-84%). GENUINELY NEGOTIATED: IP (37%), no-conflicts (54%), second-level period for fundamentals (SOL 41% vs >4 years 38% — near-tie).
|source:independent-research|:T1
```

```
TERM: Second-Level Survival — IP Representations and Fraud
MARKET (2024): IP additional survival: ≤1 year 16%; >1-2 years 46%; >2-3 years 5%; >3-4 years 6%; >4 years 10%; SOL 16%. Fraud additional survival: indefinitely 40%; SOL 24%; silent/unspecified 28%; >4 years 7%; short periods <1%.
SELL-SIDE WIN: IP: ≤1 year (16%) or >1-2 years (46% — modal). Fraud: SOL (24%) or defined period (>4 years, 7%) — avoids "indefinitely" (40%).
BUY-SIDE WIN: IP: SOL (16%) or >4 years (10%). Fraud: indefinitely (40%).
COMPROMISE: IP: >1-2 years additional (46% — clear modal). Fraud: fragmented 40%/28%/24% (indefinitely/silent/SOL) — no clear single compromise point.
RWI IMPACT: Fraud survival terms define seller's personal exposure floor. Critical in both RWI and non-RWI deals since fraud exposure survives no-survival structures.
SETTLED vs NEGOTIATED: IP — GENUINELY NEGOTIATED but converging on 1-2 years. Fraud — GENUINELY NEGOTIATED; indefinitely/silent/SOL tripartite split reflects unresolved disagreement.
|source:independent-research|:T1
```

```
TERM: Indemnification as Exclusive Remedy
MARKET (2024): 92% exclusive remedy; 8% silent; 0% non-exclusive. Carveouts (exclusive remedy deals): equitable remedies 94%; fraud 71%; intentional misrepresentation 4%; breach of covenants 4%; willful breach of covenants 3%; intentional breach 0%.
SELL-SIDE WIN: Exclusive remedy (92% achievable) with ONLY equitable remedies carveout but WITHOUT fraud carveout (29% of exclusive remedy deals omit fraud carveout). Limits buyer to specific performance/injunctive relief without preserving extra-contractual fraud claims.
BUY-SIDE WIN: Exclusive remedy with equitable remedies AND fraud carveouts (71% of exclusive deals). Preserves right to pursue common law fraud claims and potentially unlimited recovery outside the indemnification cap.
COMPROMISE: Exclusive remedy (92%) + equitable remedies (94%) + fraud carveout (71%). This IS the market standard. Negotiation then shifts to the definition of "fraud."
RWI IMPACT: In no-survival RWI deals, exclusive remedy requires careful analysis — "indemnification" may flow to the insurer. Fraud carveout is particularly significant in RWI deals where fraud represents seller's largest remaining personal exposure.
TREND: SETTLED. 92% exclusive remedy consistent. Non-exclusive (0%) eliminated.
SETTLED vs NEGOTIATED: SETTLED as to exclusivity (92%). GENUINELY NEGOTIATED: whether fraud carveout included (71% vs 29%).
|source:independent-research|:T1
```

```
TERM: Definition of Fraud
MARKET (2024): Among deals with fraud carved out from exclusive remedy — intentional fraud 47% (up from 45%); actual fraud 35% (up from 24%); intent to deceive 31% (stable); intentional misrepresentation 8% (down from 12%); constructive/negligent fraud 0%; undefined 11% (down from 16%). Delaware law definition: 25% of such deals.
SELL-SIDE WIN: Narrowest definition — "actual fraud" (35%) or "intentional fraud" (47%), both requiring scienter. Best: "actual fraud" with Delaware law definition (25% achieve this). Delaware common law fraud requires: false statement of material fact, knowledge of falsity, intent to induce reliance, actual reliance, damages — excludes negligent and reckless misrepresentation.
BUY-SIDE WIN: Broad or undefined definition (11% — buyer-favorable because courts may import broader standards). "Intent to deceive" (31%) can be read expansively. Avoiding "intentional" qualifier preserves reckless misrepresentation arguments.
COMPROMISE: "Intentional fraud" (47% — market modal) without Delaware law limitation but with scienter requirement.
RWI IMPACT: CRITICALLY IMPORTANT IN RWI DEALS. In no-survival RWI structures, fraud is often seller's PRIMARY remaining personal exposure. Fraud definition stakes are HIGHER in RWI deals than non-RWI deals — the opposite of intuition. Sellers should strongly pursue Delaware law definition and "actual fraud"/"intentional fraud" standard in RWI deals. Buyers in RWI deals should resist Delaware law limitation.
DB[] DIALECTICAL-3: In RWI no-survival deals, stakes of fraud definition are inverted from intuition — they matter MORE because fraud is seller's primary residual liability, not less. This is the most counterintuitive finding in the legal analysis.
TREND: MOVING SELLER-FAVORABLE. "Actual fraud": 24% → 35% (2023-2024) — significant jump. "Undefined": 16% → 11%. "Intentional misrepresentation" (broader): 12% → 8%.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. 47%/35%/31% distribution — no single definition commands majority.
|source:independent-research|:T1
```

---

#### E: DISPUTE RESOLUTION

```
TERM: Waivers — Legal Representation Conflict and Jury Trial
MARKET (2024): Legal representation conflict waiver (allowing seller's pre-closing counsel to represent selling shareholders post-closing in acquisition-related matters): 69.8% (recovering from 63% in 2023; prior high 70.3% in 2022). Jury trial waiver: 90% (up from 82% in 2019).
SELL-SIDE WIN: Legal representation conflict waiver included (69.8%). Without it, buyer as new entity owner could disqualify seller's deal counsel from representing shareholders in post-closing disputes — loss of institutional knowledge and significant cost. Critical and underappreciated seller protection.
BUY-SIDE WIN: No legal representation conflict waiver (30%). Buyer retains ability to disqualify seller's counsel. Jury trial waiver: both sides generally prefer it for predictability.
COMPROMISE: Legal representation conflict waiver included (69.8% norm) + jury trial waiver (90% — approaching settled). The realistic outcome includes both.
RWI IMPACT: Not broken out. Legal rep waiver particularly important in RWI deals where fraud and fundamental rep exposure may generate post-closing disputes.
TREND: Legal rep waiver: RECOVERING SELLER-FAVORABLE (70.3% in 2022 → 63% in 2023 → 69.8% in 2024). Jury trial waiver: STRONGLY TOWARD SETTLED (82% → 90%, 2019-2024).
SETTLED vs NEGOTIATED: Legal rep waiver — GENUINELY NEGOTIATED (70%/30%). Jury trial waiver — APPROACHING SETTLED (90%).
|source:independent-research|:T2
```

```
TERM: Alternative Dispute Resolution (ADR)
MARKET (2024): ADR inclusion (general disputes): 16.5% (stable from 16.5% in 2023; down from 19.4% in 2019). Among ADR deals (2024): binding arbitration 100%; mediation-then-arbitration 0%; mediation only 0%. Institution (2024): JAMS 36%; other/ICC 33%; AAA 31%. Expense allocation (2024): loser pays 38%; determined by arbitrator 33%; silent 16%; evenly split 7%; apportioned 7%.
SELL-SIDE WIN: No ADR (83.5% of deals — market majority). If unavoidable: JAMS (36%) with arbitrator-determined expense allocation (33%).
BUY-SIDE WIN: No ADR preference is symmetric with sellers. If ADR: loser-pays allocation (38%) creates deterrent against meritless claims.
COMPROMISE: Courts (83.5% — the overwhelming norm). For ADR minority: binding arbitration (100% — settled); JAMS or AAA; loser-pays or arbitrator-determined expenses.
RWI IMPACT: ADR governs general contract disputes; RWI claim resolution has its own policy-specific process. No RWI-specific ADR pattern.
TREND: DECLINING. 19.4% (2019) → 16.5% (2024). Court resolution increasingly preferred.
SETTLED vs NEGOTIATED: SETTLED that courts dominate (83.5%). ADR type SETTLED (100% binding). Institution and expense GENUINELY NEGOTIATED.
|source:independent-research|:T2
```

```
TERM: Sell-Side Attorney-Client Privilege
MARKET (2024): Ownership: selling shareholders 28%; shareholder representative 22%; both 7%; buyer or silent 44% (31% silent). Control: shareholder representative 31%; selling shareholders 15%; both 7%; buyer 4%; silent 44%. Savings clause: 17% (up from 16% in 2023).
SELL-SIDE WIN: Selling shareholders and/or shareholder representative own AND control privilege (7% achieve both; higher if allocated separately) with savings clause (17%). Without express allocation, attorney-client privilege typically transfers to buyer as new entity owner under entity transaction doctrine in most jurisdictions.
BUY-SIDE WIN: Silent on privilege (44% for both ownership and control) — silence means privilege transfers to buyer under most states' entity transaction doctrine. Or: expressly name buyer as owner/controller (4%).
COMPROMISE: Shareholder representative named as owner and/or controller (22-31%) with or without savings clause. Protects seller communications without full shareholder-by-shareholder assignment.
RWI IMPACT: Not broken out. Particularly important in RWI deals where post-closing disputes about pre-closing knowledge (fraud carveout) affect both policy coverage and seller's personal liability.
TREND: Savings clause slightly increasing (16% → 17%). Gradual seller-favorable movement. 44% silent rate for both dimensions is the dominant data point — nearly half of deals default to buyer-favorable legal rule.
SETTLED vs NEGOTIATED: GENUINELY NEGOTIATED. Fragmented distribution with large silent category. 44% silent rate is the most consequential market data point — sellers who do not address privilege accept buyer's default legal outcome.
|source:independent-research|:T2
```

---

#### DB[] SUMMARY — DIALECTICAL BOOTSTRAPPING

DB[1] NO-SURVIVAL/ANTI-SUBROGATION: No-survival truly protects sellers in RWI deals — standard anti-subrogation provisions bar insurer recourse against selling shareholders except for fraud. CONFIRMED.

DB[2] SILENT-SANDBAGGING-IN-DELAWARE: "Silent" is buyer-favorable under Delaware case law (Cobalt Operating, Allied Defense). Sellers accepting silence in Delaware deals accept buyer-favorable default. CONFIRMED.

DB[3] MATERIALITY SCRAPE PARADOX: RWI lower inclusion (80.4%) but higher aggressiveness (69.1% breach+damages). Hypothesis: 80.4% diluted by no-survival RWI deals where scrape is moot. Among survival-only RWI deals, inclusion likely higher; breach+damages dominates for insurer trigger clarity. OPEN — flag for reference-class-analyst.

DB[4] FRAUD DEFINITION / RWI STAKES INVERSION: Fraud definition stakes are HIGHER in RWI no-survival deals than non-RWI deals — fraud is seller's primary residual exposure. Sellers should prioritize narrow fraud definitions in RWI deals; buyers should resist Delaware law limitation in RWI deals. CONFIRMED — counterintuitive but well-supported.

---

#### H[] ASSESSMENT (this agent's scope)

H1: CONFIRMED for legal/structural terms. Exceptions: sandbagging (50/48/2 — genuinely three-way split), fraud definition (47/35/31 — multiple viable standards), attorney-client privilege (44% silent — no clear norm).
H2: CONFIRMED WITH CAVEAT. Structural provisions reliable baseline; RWI no-survival trend acceleration may have continued. Directional trends more reliable than point-in-time percentages.
H3: CONFIRMED. Every "sell-side win" grounded in deals that actually closed at those percentages.
H4: CONFIRMED. On sandbagging, RWI survival/no-survival, fraud definition, attorney-client privilege, MAC — real negotiating space exists between tail outcomes and the statistical median.

---

#### OPEN ISSUES FOR DA / CROSS-AGENT VALIDATION

OI-1: Materiality scrape paradox (DB[3]) — reference-class-analyst: validate whether 80.4% RWI scrape rate is diluted by no-survival RWI deals where the question is moot.
OI-2: Delaware law fraud definition (25%) — reference-class-analyst: check whether this rate differs significantly between RWI and non-RWI deal populations.
OI-3: RWI no-survival 2024 jump (36% → 54%) — DA: stress-test whether this jump is statistically meaningful or a deal-year composition artifact.
OI-4: Sexual misconduct rep scope expansion (settlements 43% → 61%) — DA: examine whether this reflects a genuine buyer-push trend or deal composition shifts.

**m-and-a-deal-counsel → CONVERGE ✓**
STATUS: R1 COMPLETE
SLIDES: 30-67, 87-95
TERMS COVERED: #30 (MAE forward-looking/prospects, MAE carveouts/disproportionate effect, knowledge standards, no-undisclosed-liabilities, compliance-with-laws, 10b-5/full-disclosure, no-other-reps/non-reliance, privacy, cybersecurity, sexual misconduct, duty-to-notify, no-shop, accuracy-of-reps/timing/materiality, MAC condition, no-legal-proceedings, legal-opinions, appraisal-rights, general-survival, stand-alone-indemnities, sandbagging, materiality-scrape, reductions, general-survival-period, second-level-survival-carveouts, second-level-survival-IP-fraud, exclusive-remedy, fraud-definition, conflict-waiver/jury-waiver, ADR, attorney-client-privilege)
XVERIFY: 2 load-bearing findings cross-verified (LB1 PARTIAL — scope narrowed to general reps; LB2 AGREE high confidence)
DB[]: 4 bootstrapping checks completed (1 confirmed, 2 confirmed, 3 open/flagged, 4 confirmed)
H[]: H1 confirmed with exceptions (sandbagging, fraud definition, attorney-client privilege unsettled); H2-H4 confirmed with caveats
OPEN-ISSUES-FOR-DA: OI-1 through OI-4 flagged above

### reference-class-analyst

#### HYPOTHESIS TESTS

```
H-TEST[1]: A definable "market standard" exists for each term
EVIDENCE FOR: Strong convergence (>85%) on procedural/structural terms: PPAs 92%, MAE forward-looking 98%, compliance-with-laws 99%, privacy rep 98%, exclusive remedy 92%, jury waiver 90%. Survival median=12mo stable 5yr. Cap median=10% stable 2022-2024.
EVIDENCE AGAINST: RWI bifurcation destroys financial-term standards — caps 10% vs 0.35% (28x gap). Escrow 10% vs 0.35%. Baskets: 8% no-basket (no-RWI) vs 44% (RWI). "No RWI" subsets contaminated. TV creates further stratification.
VERDICT: partially-confirmed | CONFIDENCE: 72%
IMPLICATION: Valid ONLY for procedural/structural terms. Financial terms require TWO parallel standards (RWI/no-RWI) + deal-size segmentation. Single "market standard" for caps/escrows/baskets without bifurcation is misleading.
|source:independent-research|T1
DB[1]: Steelman — pooled median gives weighted average. Counter: pooling 0.35% and 10% → ~5-7% reflecting NEITHER sub-market.
```

```
H-TEST[2]: 2024 data applicable to 2026 negotiations
EVIDENCE FOR: Structural provisions stable 2019-2024. Survival 12mo x5yr. Cap 10% x3yr. PPA ~92%. Legal provisions flat.
EVIDENCE AGAINST: RWI adoption non-monotonic (44%→40%→38%→42%). Deal-size mix shifted (3x jumbo). Earnout volatile (18%→38%→22%). Macro 2024→2026 unknown.
VERDICT: partially-confirmed | CONFIDENCE: 65%
IMPLICATION: Structural terms reliable as baseline. Financial terms show cyclicality requiring macro adjustment.
|source:independent-research+SRSA-data|T2
```

```
H-TEST[3]: Best outcomes identifiable from distributions
EVIDENCE FOR: Distributional data enables range ID. Caps range >0% to >50% TV with clusters. Basket sizes 90% <=1%. RWI/no-RWI split creates natural boundaries.
EVIDENCE AGAINST: Data = endings not possibilities. 5%-of-deals term could be demanded-50%-won-10% OR demanded-5%-won-100%. Terms correlated — independent optimization creates impossible composite.
VERDICT: partially-confirmed | CONFIDENCE: 55%
IMPLICATION: Data defines existing outcomes ¬achievability. Best realistic ≈ 20-25th pctl favorable. Critical gap: term interdependence.
|source:independent-research|T1
DB[2]: 20-25th pctl heuristic unverified. Competitive auction → 10th achievable. Distressed → median aspirational.
```

```
H-TEST[4]: Compromise distinguishable from median
EVIDENCE FOR: Asymmetric distributions create distinction. Sandbagging: 50%/2%/48% — "silent" is modal, not midpoint. Caps: bimodal distribution.
EVIDENCE AGAINST: Continuous terms (caps, escrows as %TV) → median IS natural compromise.
VERDICT: partially-confirmed | CONFIDENCE: 60%
IMPLICATION: Distinction meaningful only when: (1) bimodal (RWI/no-RWI), (2) categorical with intermediate (silent sandbagging), (3) package trades.
|source:independent-research|T2
```

#### CALIBRATION: KEY TERMS

```
CAL[indemnification-cap]:
  market-median=10.0% TV (stable 2022-2024)
  no-RWI-median=10.0% | RWI-median=0.35%
  sell-side-realistic=5-7% (no-RWI) | 0.1-0.25% (RWI)
  buy-side-realistic=15-20% (no-RWI) | 1-2% (RWI)
  data-dispersion=HIGH (28x sub-market gap)
  NOTE: 55% of escrow deals had cap=escrow — not independent variables
  |source:SRSA-data(slides 74-76,80)|T1

CAL[general-escrow-size]:
  market-median=8.0% TV (2024)
  no-RWI=10.0% | RWI=0.35%
  sell-side-realistic=5-7% (no-RWI) | 0.1-0.25% (RWI)
  buy-side-realistic=12-15% (no-RWI) | 1-3% (RWI)
  data-dispersion=HIGH (bimodal; 41% of 2024 had NO general escrow)
  |source:SRSA-data(slides 80-84)|T1

CAL[basket-size]:
  market-median=<=0.5% TV (59% of deals)
  sell-side-realistic=0.75-1.0% (~90th pctl seller-favorable)
  buy-side-realistic=0.25-0.5% (within 59% majority)
  data-dispersion=LOW (stable 2022-2024)
  |source:SRSA-data(slide 70)|T2

CAL[survival-period]:
  market-median=12mo (stable, avg 12.7)
  sell-side-realistic=<12mo (37% of 2024; up from 13% 2020)
  buy-side-realistic=18mo (27%)
  data-dispersion=MEDIUM
  KEY-TREND: <12mo 13%→37% = strongest directional shift in entire study
  |source:SRSA-data(slide 63)|T1

CAL[sandbagging]:
  market: pro=50%, anti=2%, silent=48%
  RWI: pro=33%, silent=64% | no-RWI: pro=55%, silent=43%
  sell-side-realistic=pro-sandbagging (50%)
  buy-side-realistic=silent (48%); anti (2%) aspirational
  data-dispersion=MEDIUM
  |source:SRSA-data(slide 59)|T1

CAL[materiality-scrape]:
  market: included 86%; breach+damages 60%
  sell-side-realistic=breach+damages (60%)
  buy-side-realistic=no scrape (14%) or breach-only (15%)
  data-dispersion=LOW (strong consensus)
  |source:SRSA-data(slides 60-61)|T2

CAL[earnout-inclusion]:
  market: 22% non-LS (2024)
  sell-side-realistic=no earnout (78%); if exists <=2yr (55%)
  buy-side-realistic=earnout with 2-3yr (62% of earnout deals >1yr)
  data-dispersion=HIGH (most cyclical: 18%→38%→22% over 2019-2024)
  |source:SRSA-data(slides 25-26)|T2
```

#### RWI CROSS-CUTTING ANALYSIS

```
RWI creates two distinct deal-term markets:

ESSENTIAL bifurcation (>2x outcome difference):
- Cap: 10.0% vs 0.35% (28x) | Escrow: 10.0% vs 0.35% (28x)
- Basket presence: 8% none (no-RWI) vs 44% none (RWI)
- Sandbagging: pro 55% (no-RWI) vs 33% (RWI)
- Survival: 82% survive (no-RWI) vs 46% (RWI)
- 10b-5 reps: 15% (no-RWI) vs 6% (RWI)

UNNECESSARY bifurcation (similar outcomes):
- MAE carveouts, knowledge standards, compliance-with-laws, PPA, exclusive remedy, jury waiver

XVERIFY: GPT-5.4=partial | Gemini-3.1-pro=agree(high confidence)
|source:independent-research+SRSA-data|T1
```

#### DISCONFIRMATION (R1 MANDATORY)

```
DISCONFIRM[1]: "Market standard" validity across multi-axis variation
→ Useful but dangerously imprecise. 3 stratification axes: (1) RWI, (2) TV, (3) buyer type. Safest framing: "observed in X% of comparable deals." |source:independent-research|T1

DISCONFIRM[2]: SRSA dataset representativeness
→ Moderate selection bias (skews PE-backed, middle-market, larger). "No RWI" subsets contaminated. But 10%+ US M&A coverage = directionally valid.
XVERIFY: GPT-5.4=partial | Gemini-3.1-pro=agree |source:independent-research+SRSA(slide 4)|T1

DISCONFIRM[3]: Closed-deal outcomes ≠ negotiation positions
→ YES, most important caution. Data shows endings not possibilities. Frequencies ≠ achievability rates. Correct framing: "X% of closed deals contained this term." |source:independent-research|T1
```

#### PRE-MORTEM

```
PM[failure modes if someone relies on this analysis]:
PM1: Used all-deals numbers for RWI/no-RWI deal → wrong baseline up to 28x
PM2: Treated frequencies as achievability → demanded rare term, burned credibility
PM3: Optimized each term independently → impossible composite position
PM4: 2024 data for 2026 without macro adjustment → cyclical terms shifted
PM5: Ignored deal-size stratification → wrong reference class
PM6: "Silent" sandbagging as "win" without jurisdictional analysis
PM7: SRSA data as universal → client base may not match their deal
```

#### OUTSIDE-INSIDE VIEW RECONCILIATION

```
OUTSIDE: Base rates show terms are path-dependent, convention-driven. "Market" persists for years. Outlier outcomes (5th/95th pctl) = unique dynamics, not replicable through advocacy.
INSIDE: Skilled attorney adjusts median → ~25th pctl favorable on 2-3 priority terms via package tradeoffs.
RECONCILED: Outside view sets range. Inside view determines position within range. Best use of SRSA: establish range, adjust for RWI/deal-size/buyer-type/competitive-dynamics/seller-alternatives.
```

#### SUMMARY TABLE (2024, non-LS)

| Term | Market | Seller Win | Buyer Win | Compromise | Dispersion |
|---|---|---|---|---|---|
| Cap (no-RWI) | 10.0% | 5-7% | 15-20% | 10% | Med |
| Cap (RWI) | 0.35% | 0.1-0.25% | 1-2% | 0.35% | Med |
| Escrow (no-RWI) | 10.0% | 5-7% | 12-15% | 10% | Med |
| Escrow (RWI) | 0.35% | 0.1-0.25% | 1-3% | 0.35% | Med |
| Basket size | <=0.5% | 0.75-1.0% | 0.25-0.5% | 0.5% | Low |
| Survival | 12mo | <12mo (37%) | 18mo (27%) | 12mo | Med |
| Sandbagging | pro50/silent48 | pro | silent | silent | Med |
| Mat. scrape | 86% included | breach+dmg 60% | no scrape 14% | breach-only | Low |
| Earnout (if any) | 24mo | <=1yr (24%) | 2-3yr (46%) | 24mo | High |

#### CONFIDENCE

```
>80%: RWI bifurcation mandatory for financial terms | structural-term temporal stability | selection bias exists but non-invalidating
60-75%: 20-25th pctl "realistic win" heuristic | 2024→2026 for stable terms
50-60%: compromise vs median distinction | term-by-term vs package dynamics
<50%: precise percentile assignments (data granularity insufficient)
```

◌ R1 complete | awaiting convergence

### devils-advocate

#### R2 CHALLENGE ROUND — FULL FRAMEWORK

---

**DA#1 — CROWDING: RWI-IS-TRANSFORMATIVE NARRATIVE**

All 4 agents converge on the same master narrative: RWI is the dominant structuring variable that creates two distinct deal-term markets. Loan-ops calls it "THE DOMINANT STRUCTURING VARIABLE" (caps in original). Product-strategist identifies "RWI spillover to non-RWI deals" as a structural development. M-and-a-deal-counsel labels RWI no-survival as a "CRITICAL — LOAD-BEARING FINDING." Reference-class-analyst builds the entire calibration framework around essential vs unnecessary bifurcation.

CHALLENGE: What is this convergence missing?

(a) RWI is a PROXY, not an independent variable. RWI adoption correlates with deal size, buyer sophistication, PE involvement, competitive process intensity, and target quality. The team treats RWI as causal when it may be a MARKER for deals where sellers have more leverage anyway. A PE-backed target in a competitive auction with $200M+ TV gets better terms across the board — RWI is one expression of that leverage, not the source. The 28x cap gap (0.35% vs 10.0%) may overstate RWI's independent effect because it conflates RWI with all the other variables that travel with it.

(b) RWI FAILURE MODES are entirely absent from the analysis. None of the 4 agents discuss: RWI claim denial rates, coverage exclusions (known matters, forward-looking statements, pre-existing litigation, cybersecurity/environmental sublimits), retention amounts, or the gap between policy and practice. Seller accepting 0.35% cap with RWI is betting on the INSURER'S willingness to pay — a bet none of the agents evaluated. This is a material analytical gap.

(c) RWI COST ALLOCATION is undiscussed. Who pays the RWI premium? The study doesn't segment this, but it directly affects whether RWI is a "seller win" or merely a cost shift. If seller bears the premium (common in competitive processes), the net economic benefit is reduced by 1-3% of TV in premium costs.

|engagement: all 4 agents must address (a) proxy vs causal, (b) RWI failure modes, (c) cost allocation
|severity: HIGH — shapes every downstream recommendation

---

**DA#2 — BASE RATES: FREQUENCIES ≠ ACHIEVABILITY**

Reference-class-analyst correctly flags this in DISCONFIRM[3] — "closed-deal outcomes ≠ negotiation positions." But the other three agents systematically conflate the two. Examples:

(a) Loan-ops: "No basket (22% of 2024 deals — growing trend, best seller outcome)" — 22% of closed deals had no basket. This does NOT mean a seller requesting no basket achieves it 22% of the time. It means 22% of deals that CLOSED happened to have no basket. Selection bias: deals where buyer insisted on a basket and seller walked away are invisible in this data.

(b) M-and-a-deal-counsel: "Actual fraud (35% — achievable)" — same conflation. 35% of deals defined fraud as "actual fraud." This does not tell us the SUCCESS RATE of a seller requesting this definition. Every "sell-side win" and "buy-side win" framing in the workspace commits this error.

(c) Product-strategist: "All-cash deal (59% market) — clean exit, no equity risk, no lock-up. Achievable in majority of deals" — 59% frequency presented as achievability. Cash consideration correlates with deal type, buyer type, and market conditions — not negotiation skill.

CHALLENGE: The entire buy-side/sell-side win framework is built on a category error. Observed frequency in closed deals is a LOWER BOUND on demand and an UNKNOWN relationship to achievability. A term appearing in 5% of deals could be demanded in 50% and won 10% of the time, OR demanded in 5% and won 100%. The data cannot distinguish these scenarios.

|engagement: all 3 non-reference-class agents must acknowledge this limitation in their findings OR provide evidence for why frequency approximates achievability
|severity: HIGH — undermines the core deliverable structure

---

**DA#3 — ANCHORING: SRSA DATA TO EXCLUSION OF CRITICAL CONTEXT**

The team's analysis is anchored exclusively on the SRSA dataset. No agent discusses:

(a) POST-CLOSING DISPUTE DATA: What happens AFTER these deals close? Indemnification claim rates, average claim sizes, claim success rates, time-to-claim — all directly relevant to whether "market standard" terms actually protect the parties. AIG, Euclid Transactional, and other RWI insurers publish claims data. None cited.

(b) LITIGATION OUTCOMES: Delaware Chancery Court rulings on MAE (Akorn is mentioned once), sandbagging, fraud definitions, and materiality — these define how contractual terms PERFORM in practice. The team discusses "Delaware law fraud definition" at 25% without examining whether that definition has actually protected sellers in litigation.

(c) INSURANCE MARKET DATA: RWI premium trends, coverage terms, retention shifts, claim payment statistics. The team treats RWI as a binary (present/absent) when it exists on a spectrum of coverage quality.

(d) DEAL VOLUME AND MARKET CYCLE CONTEXT: 2024 M&A volume, competitive dynamics, interest rates, credit availability — all affect which terms are achievable in practice. The SRSA data captures closed deals but not the MARKET CONDITIONS that produced them.

CHALLENGE: An analysis of deal terms without performance data is like evaluating insurance policies by reading coverage summaries without examining claims history. The team should acknowledge this as a structural limitation of the SRSA source.

|engagement: all agents should note this gap. m-and-a-deal-counsel has the strongest obligation given legal expertise
|severity: MEDIUM — structural limitation, not fixable within scope, but must be acknowledged

---

**DA#4 — CONFIRMATION BIAS: SELECTIVE DATA FRAMING**

Several findings frame data points in buyer- or seller-favorable ways while ignoring contradictory signals:

(a) SELLER-FAVORABLE DRIFT NARRATIVE: Loan-ops identifies "seller-favorable drift 2021-2024" across multiple terms. Product-strategist then CONTRADICTS this with "mixed market with structural buyer advantage on economics" — 52% multiple compression. These two findings are in tension. The team has not resolved whether the market is seller-favorable (legal mechanics) or buyer-favorable (economics). Product-strategist's correction via XVERIFY is buried rather than elevated.

(b) SANDBAGGING "COMPROMISE": M-and-a-deal-counsel presents "silent" sandbagging as the compromise position, then immediately notes that silence favors buyers under Delaware law (Cobalt Operating). This is presenting a buyer-favorable outcome as a "compromise" — misleading framing that the synthesis must correct.

(c) EARNOUT CRE COLLAPSE: Loan-ops presents CRE dropping from 30%+ to 10% as a "buyer win" without examining whether the 30%+ figure was itself anomalous (2023 was a peak year for many terms). If 2023 was the outlier, 10% may be reversion to norm rather than a "collapse."

(d) NO-GENERAL-ESCROW at 41%: Presented as a growing trend (34%→41%). But reference-class-analyst's H-TEST[2] notes RWI adoption is non-monotonic (44%→40%→38%→42%). If no-escrow tracks RWI adoption, the "growth" may be cyclical, not structural.

|engagement: each agent must address their specific framing challenge
|severity: MEDIUM — affects synthesis framing

---

**DA#5 — MISSING SECOND-ORDER EFFECTS**

The team is NOT discussing:

(a) TERM INTERDEPENDENCE / IMPOSSIBLE COMPOSITE: Reference-class PM3 flags this correctly. Every agent presents "sell-side win" positions per term as if they are independently achievable. But a seller cannot simultaneously achieve: no basket + 5% cap + no survival + no sandbagging + no materiality scrape + revenue-only earnout + no PPA escrow. These terms TRADE against each other. The synthesis must present package tradeoffs, not independent optimization. I challenge all 3 domain agents to identify which of their "sell-side wins" must be SACRIFICED to achieve their other "sell-side wins."

(b) INFORMATION ASYMMETRY IN RWI: The study notes RWI identification is imperfect — buyer doesn't always disclose RWI to seller. This creates adverse selection: sellers in "no-RWI" deals may actually have RWI they don't know about. The contamination runs BOTH directions. The "no-RWI" comparison group is impure.

(c) NEGOTIATION DYNAMICS: The data captures outcomes, not process. Terms achieved early in negotiation (easy wins) vs terms requiring significant leverage expenditure (hard wins) look identical in the data. A sophisticated user needs to know which terms are CHEAP to ask for vs which are EXPENSIVE.

(d) TEMPORAL RELEVANCE GAP: H2 was confirmed at only 65% confidence by reference-class-analyst. The team is analyzing 2024 data for use in a 2026 context. Two years of market evolution — interest rate changes, RWI market maturation, potential regulatory changes, deal volume shifts — could move multiple terms. The analysis should be explicit about which terms are STABLE anchors vs VOLATILE targets.

|engagement: (a) is mandatory for all domain agents; (b)-(d) should be acknowledged
|severity: HIGH for (a), MEDIUM for (b)-(d)

---

**DA#6 — IMPOSSIBLE COMPOSITE TEST**

Extending PM3 from reference-class-analyst. I construct two hypothetical "optimal" packages from the agents' findings:

SELLER OPTIMAL (per workspace):
- No basket (22%) + no escrow (41%) + no survival (54% RWI) + 0.35% cap (RWI median) + no materiality scrape (14%) + anti-sandbagging (2%) + actual fraud definition (35%) + revenue earnout (65% if any) + no 10b-5 (89%) + both non-reliance clauses without fraud carveout (67% of "both" deals)

JOINT PROBABILITY (naive independence): 0.22 × 0.41 × 0.54 × 0.50 × 0.14 × 0.02 × 0.35 × 0.89 × 0.67 ≈ 0.000016 = 0.0016% of deals

Even with generous correlation adjustments (RWI terms travel together), the probability of achieving ALL seller-optimal terms simultaneously is vanishingly small. The team's term-by-term framing creates the illusion that these outcomes are independently achievable when they are collectively impossible.

BUYER OPTIMAL (per workspace):
- First-dollar basket (39%) + 15%+ cap (16%) + 18mo+ survival (35%) + pro-sandbagging (55%) + breach+damages scrape (60%) + EBITDA earnout (13%) + "could be" MAE (10%) + 10b-5 rep (10%) + undefined fraud (11%)

JOINT PROBABILITY: similarly vanishingly small.

CHALLENGE: The synthesis MUST present a realistic PACKAGE framework showing 3-5 achievable combinations, not 30+ independently optimized terms.

|engagement: mandatory for lead to address in synthesis structure
|severity: HIGH — structural

---

#### CONVERGENCE FLAG CHALLENGES (per task assignment)

**OI-1: Materiality scrape paradox (m-and-a-deal-counsel DB[3])**

M-and-a-deal-counsel correctly identifies that the 80.4% RWI scrape inclusion rate is likely DILUTED by no-survival deals where scrape is moot. Among the 54% of RWI deals with no general rep survival, a materiality scrape has no operative effect — there is no general rep indemnification to scrape. So the 19.6% "no scrape" in RWI deals may largely consist of no-survival deals where the question is irrelevant, not deals where scrape was actively negotiated away.

CHALLENGE ACCEPTED — DB[3] is well-reasoned. The denominator problem is real. Among survival-only RWI deals (46% of RWI sample), scrape inclusion is likely well above 80.4%, potentially approaching 95%+. The team should present scrape data CONDITIONAL ON survival status, not pooled across survival/no-survival.

However, I ADD: the same denominator problem affects MULTIPLE other RWI statistics. Sandbagging provisions in no-survival deals are similarly moot for general reps. Basket definitions in no-survival deals are moot. The team has not systematically identified which RWI-segmented statistics suffer from this survival-conditional contamination. M-and-a-deal-counsel and reference-class-analyst should audit all RWI-segmented findings for survival-conditional relevance.

---

**OI-2: Delaware fraud definition (25%)**

M-and-a-deal-counsel reports 25% of fraud-carveout deals use Delaware law definition. The question: does this differ between RWI and non-RWI populations?

CHALLENGE: Logically, it SHOULD differ. In RWI no-survival deals, fraud is seller's primary residual exposure (per DB[4] — the stakes inversion finding). Sellers in RWI deals have HIGHER incentive to narrow fraud definition via Delaware law limitation. If the 25% rate does NOT differ by RWI status, that would be counterintuitive and worth investigating — it might indicate seller counsel is not consistently identifying the stakes inversion. The data is not in the workspace; this is a genuine gap that the synthesis should flag as unknown rather than assume.

---

**OI-3: RWI no-survival 2024 jump (36%→54%)**

An 18-percentage-point jump in one year for a structural term is dramatic. I stress-test:

(a) COMPOSITION ARTIFACT hypothesis: If the RWI deal mix shifted toward larger deals or PE deals in 2024 (jumbo deals went from 3% to 10% of sample), these deals may disproportionately include no-survival provisions. The jump could reflect SAMPLE COMPOSITION rather than market shift.

(b) STATISTICAL SIGNIFICANCE: SRSA identifies RWI on ~42% of 2024 deals. If 2024 sample is ~500 deals (rough estimate from 2,200+ total over 6 years), that's ~210 RWI deals. 54% of 210 = ~113 no-survival. Standard error for a proportion at 54% with n=210 is ~3.4%. The 36% figure from 2023 would need a similar sample. The gap is ~5 standard errors — statistically significant IF the samples are independent and composition-matched. But if the 2023 RWI sample was smaller (SRSA sample grew), the significance weakens.

(c) TREND vs STEP FUNCTION: The progression is 37%→36%→36%→54% (2021-2024 per workspace). Flat for 3 years then jumping 18pp suggests a regime change, not a smooth trend. This is more consistent with a market tipping point (RWI insurer willingness to accept no-survival + seller counsel learning curve) than composition artifact. But composition should still be tested.

VERDICT: Likely genuine market shift, but composition artifact cannot be ruled out from available data. Synthesis should present as "probable trend acceleration" not "confirmed structural shift."

---

**OI-4: Sexual misconduct rep scope expansion (43%→61%)**

Settlement agreement coverage jumping 18pp in one year.

CHALLENGE: This could be:
(a) GENUINE TREND driven by post-#MeToo maturation — buyer counsel increasingly sophisticated about hidden settlement liabilities. Plausible and consistent with 68%→74% overall inclusion growth.
(b) COMPOSITION — if 2024 sample over-indexed on industries with higher misconduct exposure (tech, entertainment, finance), the scope expansion could be sample-driven.
(c) INSURER PUSH — RWI underwriters increasingly requiring disclosure of settlements as condition of coverage, which creates contractual pressure to include in reps.

Without industry-segmented data, cannot distinguish. But the DIRECTIONAL signal is strong across both frequency and scope. VERDICT: Treat as genuine trend with composition caveat.

---

**Loan-ops: CRE covenant collapse (30%+→10%)**

CHALLENGE: 2023 was a peak year for earnout frequency (33% of deals, up from prior years). If CRE prevalence correlates with earnout frequency (more earnout deals = more CRE discussion), then the CRE rate in 2023 is inflated by the larger earnout denominator. In 2024, earnout frequency dropped to 22% — fewer earnout deals = smaller denominator. But the CRE rate WITHIN earnout deals also dropped, suggesting genuine decline within the relevant population.

ADDITIONAL NOTE: The source for "30%+" is a footnote, not a chart data point (per XVERIFY correction). Footnote language ("over 30%") is imprecise. The magnitude of the drop may be less dramatic than 30%→10% if the baseline was 31% vs 35%.

VERDICT: Real decline within earnout deals, but magnitude uncertain due to imprecise 2023 baseline. Do not present as "collapse" — present as "significant decline."

---

**Loan-ops: 41% no-general-escrow rate**

CHALLENGE: Is this RWI-driven or independent?

Analysis: 34% (2022) → 33% (2023) → 41% (2024). RWI adoption: 38% (2022) → ~40% (2023) → 42% (2024). If all RWI deals had no general escrow, that would explain ~42% no-escrow rate. But not all RWI deals are escrow-free — workspace shows RWI deals have 0.35% median escrow, implying most still have SOME escrow. So the 41% no-escrow rate EXCEEDS what RWI alone explains. Some non-RWI deals are also going escrow-free, suggesting an independent trend layered on top of RWI.

VERDICT: Partially RWI-driven, partially independent. The 8pp jump (33%→41%) in one year exceeds the 2pp RWI adoption increase (40%→42%), confirming independent driver. Synthesis should not attribute entirely to RWI.

---

**Loan-ops: IP second-level cap**

CHALLENGE: The split (21% at ≤25% TV, 35% at >25-50% TV, presumably remainder at higher levels) genuinely lacks a market standard. Reference-class-analyst's framework would classify this as H1-FAILED for this specific term. The synthesis should present this as a "genuinely contested" term where deal-specific factors (IP centrality to target value, buyer's IP-intensive acquisition thesis, insurer coverage availability) determine outcome, not market norms.

---

**Reference-class: H3 at 55% — "realistic win" at 20-25th percentile**

CHALLENGE: The 20-25th percentile heuristic is unverified and potentially misleading.

(a) The "right" percentile is CONTEXT-DEPENDENT. In a competitive auction with 5+ bidders, a seller can push to the 10th percentile favorable on priority terms. In a distressed sale or single-bidder scenario, MEDIAN is aspirational. The synthesis presenting a fixed percentile as "realistic" without contextualizing by competitive dynamics is false precision.

(b) The heuristic conflates INDEPENDENT TERMS. Even if 20-25th percentile is achievable per individual term, achieving it on MULTIPLE terms simultaneously is exponentially harder (returning to DA#6 impossible composite).

(c) No empirical validation exists for this heuristic. Reference-class-analyst acknowledges this (DB[2]: "unverified"). The synthesis should present ranges (e.g., "competitive auction: 10-25th pctl on priority terms; single-bidder: 40-60th pctl") rather than a single percentile target.

---

#### PROMPT AUDIT (§7d — mandatory)

**1→ Echo detection: near-verbatim prompt language in findings**

The prompt asked for "realistic best outcome for SELLER (sell-side win)" and "realistic best outcome for BUYER (buy-side win)" — every agent's findings are structured around these exact terms. This is NOT echo contamination — these are the requested analytical categories and were confirmed in Q2/Q3. The framing is appropriate.

However, the prompt phrase "realistic compromise position where both sides can live with the result" introduces a NORMATIVE judgment ("can live with") that agents have not independently validated. Several agents' "compromise" positions are simply medians or modal outcomes — which is statistically appropriate but does not validate the "can live with" framing. A median outcome is where deals SETTLE, not necessarily where both parties are satisfied.

**2→ Unverified prompt claims: [prompt-claim] tagged findings**

Source provenance audit across all 4 agents:

- Loan-ops: 8 term analyses, all tagged |source:direct-read:T1 — CLEAN. No [prompt-claim] findings detected. All data traced to specific slides.
- Product-strategist: 12 term analyses, all tagged |source:independent-research[SRSA primary] — CLEAN. One meta-finding ("mixed market with structural buyer advantage") is |source:agent-inference|T2 — appropriate tagging.
- M-and-a-deal-counsel: 30 term analyses, all tagged |source:independent-research|:T1 or T2 — CLEAN. DB[] notes carry independent reasoning.
- Reference-class-analyst: calibration framework is |source:independent-research+SRSA-data| or |source:independent-research| — CLEAN.

Source distribution: approximately 95% T1/T2, 5% agent-inference. Zero [prompt-claim] without corroboration. No echo cluster detected. This is a STRONG source provenance performance.

**3→ Missed implicit claims**

The prompt decomposition extracted H1-H4, Q1-Q5, C1-C5. I check for missed implicit assumptions:

MISSED IMPLICIT CLAIM — H5 (not extracted): The prompt implicitly assumes that SRSA data represents a sufficiently unbiased sample of the private M&A market to serve as the basis for "market standard" determinations. Reference-class-analyst identified this as DISCONFIRM[2] (SRSA dataset representativeness) with "moderate selection bias" — but it was not extracted as a testable hypothesis in the prompt decomposition. It should have been H5: "The SRSA dataset is representative enough of the private-target M&A market to define 'market standard' across the term categories."

MISSED IMPLICIT CLAIM — H6 (not extracted): The prompt assumes that "both buyer and seller" perspectives can be independently analyzed from the same dataset. But the SRSA data captures JOINT outcomes (what the deal actually looked like), not separated negotiation positions. The "sell-side win" category requires imputing what sellers specifically wanted from what they got — a different analytical task than reading closed-deal terms.

**4→ Methodology: could research have produced contradictory results?**

YES — but only partially. The methodology (reading SRSA empirical data) could have found:
- Terms with no clear market standard (H1 could have been rejected — and was, partially, for sandbagging/fraud/privilege)
- Terms where RWI made no difference (possible — and was found for MAE/knowledge standards/compliance)
- Terms with buyer-favorable drift (found — undisclosed liabilities, legal proceedings scope)

However, the methodology COULD NOT have produced:
- Evidence that SRSA data is unrepresentative (would require external data comparison)
- Evidence on term achievability vs frequency (would require negotiation process data)
- Evidence on term performance (would require post-closing dispute data)

The methodology was INVESTIGATIVE within its scope (SRSA data reading) but STRUCTURALLY LIMITED by single-source design. This is not confirmatory bias — the team did extract genuine nuance from the data — but the scope limitation means the analysis is data-descriptive, not strategically prescriptive.

PROMPT AUDIT VERDICT: PASS with caveats. Source provenance clean. Two missed implicit claims (H5, H6) that agents partially addressed through DISCONFIRM and cross-cutting analysis but were not formally extracted. Methodology investigative within scope but structurally limited.

---

#### EXIT-GATE VERDICT

```
exit-gate: PASS
|engagement: loan-ops=A-, product-strategist=B+, m-and-a-deal-counsel=A, reference-class-analyst=A
|unresolved: [
  (1) RWI-as-proxy-vs-causal — agents treat as causal; may overstate independent RWI effect,
  (2) frequencies-vs-achievability — systematic conflation in domain agent findings; reference-class identified but peers did not integrate,
  (3) impossible-composite — no package framework exists; term-by-term optimization is misleading,
  (4) RWI-failure-modes — zero coverage of claim denial, exclusions, retention,
  (5) survival-conditional-contamination — multiple RWI-segmented statistics suffer from pooling survival/no-survival deals
]
|untested-consensus: [
  (1) "RWI is transformative" — accepted by all 4 agents without examining RWI as proxy for other leverage factors,
  (2) "20-25th percentile = realistic win" — unverified heuristic presented as calibrated
]
|hygiene: pass — §2d source provenance strong (95% T1/T2); §2g DB[] applied by 3 of 4 agents; §2h XVERIFY completed on load-bearing findings
|prompt-contamination: pass-with-caveats — two missed implicit claims (H5 dataset representativeness, H6 joint-outcome-as-separated-positions); source distribution clean
|cqot: pass — falsifiable claims present (RWI no-survival at 54% is testable); steelman positions acknowledged (DB[] dialectical notes); confidence gaps identified (H3 at 55%, H2 at 65%)
|xverify: pass — 6 total XVERIFY runs across 3 agents; partial results appropriately noted; causation language corrected per XVERIFY feedback; no process violations
```

SYNTHESIS REQUIREMENTS (for lead):
1→ Present ALL financial terms as RWI-segmented (not pooled). This is non-negotiable per RWI bifurcation finding.
2→ Add explicit caveat: "Frequencies represent closed-deal outcomes, not negotiation success rates."
3→ Include package framework showing 3-5 realistic term combinations (competitive auction seller, distressed seller, strategic buyer, financial buyer, compromise), not 30+ independent optimizations.
4→ Acknowledge structural gaps: post-closing dispute data, RWI claims experience, litigation outcomes — analysis describes deal terms, not deal term performance.
5→ Address impossible composite: note that achieving sell-side win on any term comes at cost on other terms.
6→ Agents must respond to DA#1-DA#6 with concede|defend|compromise before synthesis.

---

◌→✓ R2 COMPLETE | challenges issued | exit-gate PASS with 5 unresolved items requiring agent response before synthesis

## convergence
### loan-ops-tech-specialist ✓
STATUS: R1 COMPLETE
SLIDES: 19-29 (PPAs, earnouts), 68-86 (baskets, caps, escrows, sources of recovery, expense funds)
TERMS COVERED: #8 (PPA, earnout, baskets-definitions, baskets-carveouts, caps-all/no-RWI/RWI, caps-carveouts, second-level-caps, deal escrows, general indemnification escrows, sources of recovery, post-closing expense funds)
XVERIFY: 2 findings cross-verified (both partial — data confirmed, language corrected)
PERSIST: 2 team decisions stored, agent memory updated
DB[]: 3 bootstrapping checks completed
H[]: H1 confirmed with caveat (RWI bifurcation means single "market standard" requires segmentation), H3 confirmed, H4 confirmed
OPEN-ISSUES-FOR-DA: (1) Earnout CRE collapse (30%+→10%) is statistically dramatic — DA should challenge whether this is sample composition shift or genuine buyer-win trend. (2) 41% no-general-escrow rate is high — DA should verify whether this reflects RWI penetration or independent trend. (3) Second-level IP cap distribution (35% at 25-50% vs 33% at purchase price) — genuinely split market, no clear "market standard."

### reference-class-analyst ✓
STATUS: R1 COMPLETE
SCOPE: Cross-cutting calibration — H1-H4 tests, term-by-term calibration (8 terms), RWI bifurcation analysis, disconfirmation (3 challenges), superforecasting protocol (decomposition, reference class, temporal stability, pre-mortem 7 failure modes, OV-IV reconciliation)
XVERIFY: 2 load-bearing findings cross-verified (RWI bifurcation: GPT-5.4=partial/Gemini=agree | dataset bias: GPT-5.4=partial/Gemini=agree)
PERSIST: 2 team decisions stored (RWI bifurcation mandatory, frequencies ≠ achievability), agent memory updated
KEY OUTPUTS FOR DA:
(1) H3 at only 55% confidence — "realistic win" heuristic (20-25th pctl) is unverified; competitive vs distressed dynamics shift which percentile is achievable
(2) DISCONFIRM[3] — closed-deal outcomes presented as negotiation positions is a methodological error all peer agents should be challenged on
(3) Pre-mortem PM3 — independently optimizing each term creates impossible composite position; peer agents presenting best-case per term without package tradeoff acknowledgment should be challenged
(4) Loan-ops-tech-specialist confirms H1 with RWI caveat — ALIGNED with reference-class H-TEST[1] (72%)
(5) Dataset selection bias is real but not invalidating — DA should probe whether SRSA's 10%+ market share claim is sufficient for representativeness

### m-and-a-deal-counsel ✓
STATUS: R1 COMPLETE
SLIDES: 30-67, 87-95
TERMS COVERED: #30 (MAE forward-looking/prospects, MAE carveouts/disproportionate-effect, knowledge standards, no-undisclosed-liabilities, compliance-with-laws, 10b-5/full-disclosure, no-other-reps/non-reliance, privacy, cybersecurity, sexual misconduct, duty-to-notify, no-shop, accuracy-of-reps/timing/materiality, MAC condition, no-legal-proceedings, legal-opinions, appraisal-rights, general-survival, stand-alone-indemnities, sandbagging, materiality-scrape, reductions, general-survival-period, second-level-survival-carveouts, second-level-survival-IP-fraud, exclusive-remedy, fraud-definition, conflict-waiver/jury-waiver, ADR, attorney-client-privilege)
XVERIFY: 2 load-bearing findings cross-verified (LB1 no-survival/RWI: PARTIAL — data confirmed, scope narrowed to general reps only; LB2 materiality scrape: AGREE high confidence, all percentages confirmed)
PERSIST: 3 team decisions stored (TD-1 no-survival RWI differential, TD-2 fraud definition stakes inversion in RWI deals, TD-3 materiality scrape paradox)
DB[]: 4 bootstrapping checks (DB1 CONFIRMED anti-subrogation protects sellers; DB2 CONFIRMED Delaware silence is buyer-favorable; DB3 OPEN scrape paradox flagged for reference-class-analyst; DB4 CONFIRMED fraud definition stakes are higher in RWI no-survival deals)
H[]: H1 confirmed with exceptions (sandbagging, fraud definition, attorney-client privilege are genuinely unsettled); H2-H4 confirmed with caveats
KEY FINDINGS FOR DA:
(1) RWI no-survival trend jumped from 36% (2023) → 54% (2024) in RWI deals — DA should stress-test whether this is statistically meaningful or deal-year composition artifact (OI-3)
(2) Sexual misconduct rep scope expansion (settlements 43%→61% in one year) — DA should examine whether this is genuine trend or composition shift (OI-4)
(3) Materiality scrape paradox (DB3) — DB3 hypothesis requires reference-class-analyst cross-validation: whether 80.4% RWI scrape rate is diluted by no-survival deals where question is moot
(4) Fraud definition Delaware law qualification (25% of fraud-carveout deals) — DA should examine whether this rate differs between RWI and non-RWI populations (OI-2)
(5) Sandbagging remains the most evenly contested legal term (50/48/2) — DA should probe whether the Delaware silent-as-buyer-favorable default is consistently understood by practitioners or whether negotiating parties may not appreciate the legal default
CROSS-AGENT ALIGNMENT NOTES:
- ALIGNED with reference-class-analyst: RWI bifurcation is essential (not optional) for legal term analysis just as for financial terms; single "market standard" requires RWI segmentation
- ALIGNED with loan-ops-tech-specialist: Stand-alone indemnities in RWI no-survival deals are the critical residual seller obligation (parallel to indemnification escrow structure in financial analysis)
- NEW FINDING NOT IN OTHER AGENTS: Fraud definition stakes inversion in RWI no-survival deals — this is a purely legal insight that has no parallel in financial mechanics analysis

## open-questions

## promotion
