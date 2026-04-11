# Quick Reference: Operational Mechanics

For full SOFR methodology, payment system details, and workflow specs, see `Doc3_Operational_Mechanics_Revised.md`.

## Rate Mechanics

### SOFR Variants
| Variant | Published By | Time | Use Case |
|---------|-------------|------|----------|
| Overnight SOFR | NY Fed | 8:00 AM ET (T+1) | Reference only |
| Term SOFR (1m, 3m, 6m, 12m) | CME Group | 6:00 AM ET (T+0) | **Dominant for new syndicated loans** |
| SOFR Averages (30d, 90d, 180d) | NY Fed | 8:00 AM ET (T+0) | Compounded in arrears |
| Daily Simple SOFR | NY Fed | 8:00 AM ET (T+1) | Set in arrears, 5-BD lookback |

### Day-Count Conventions (MEMORIZE THIS)
| Currency/Rate | Convention | Effect |
|---------------|-----------|--------|
| USD SOFR | **Actual/360** | Effective rate ~1.4% higher than stated |
| GBP SONIA | **Actual/365 Fixed** | 365 even in leap years |
| EUR EURIBOR | **Actual/360** | Same as USD |
| USD fixed-rate | 30/360 | Standard fixed-rate convention |

**Wrong day-count on $500M = $100K+ error per quarter.**

### Floor Rule
Floor applies to **benchmark only**, NOT all-in rate.
- SOFR = 0.75%, Floor = 1.00%, Spread = 3.00%
- **Correct:** max(0.75%, 1.00%) + 3.00% = **4.00%**
- **Wrong:** Applying floor to all-in = wrong answer

### Term SOFR Fixing
- Rate fixed **2 business days** before interest period start
- Rate set notice generated and sent after fixing
- CME license required for all parties using Term SOFR

## Payment Systems

| System | Currency | Customer Cutoff | Agent Should Target |
|--------|----------|-----------------|-------------------|
| Fedwire | USD | 6:45 PM ET | 1:00-2:00 PM ET |
| CHAPS | GBP | 5:40 PM UK | 3:00-5:00 PM UK |
| T2 | EUR | 5:00 PM CET | Before 5:00 PM CET |

Missing cutoff = next business day = potential late payment breach.

## Payment Waterfall (Non-Default)
1. Agent fees, costs, expenses, indemnification
2. Interest — pro rata by facility
3. Fee payments — commitment fees, LC fees — pro rata
4. Scheduled principal (amortization) — pro rata
5. Voluntary prepayments — pro rata within chosen facility
6. Other amounts (breakage, increased costs)

## Payment Waterfall (Default/Acceleration)
1. Agent fees and expenses
2. Accrued interest — pro rata among all secured parties
3. Outstanding principal — pro rata
4. All other obligations — pro rata
5. Surplus to borrower

## Mandatory Prepayment Application
- Asset sales: pro rata to term loans, reinvestment rights 12-18 months, leverage step-downs
- ECF sweep: annual, leverage-based step-downs
- Debt issuance: 100% of non-permitted
- Application order: typically **inverse order of maturity** (last payment first)

## Defaulting Lender Consequences
- Payments redirected: cure unfunded → cash collateralize LC → swingline → non-defaulting lenders → remainder to defaulter
- Loses voting rights, excluded from Required Lender calc
- Forfeits commitment fees
- Borrower may exercise yank-a-bank
