# Quick Reference: Secondary Trading & Settlement

For full trade documentation, platform details, and case studies, see `Doc4_Secondary_Trading_and_Settlement.md`.

## Trade Types
| Type | When Used | Settlement | Documentation |
|------|-----------|------------|---------------|
| Par/Near Par | Trading ≥ 90 cents | T+7 target (median T+11 actual) | LSTA standard terms |
| Distressed | Trading < 80 cents | T+20 | LSTA distressed terms |
| 80-90 range | Negotiated | Either T+7 or T+20 | Buyer/seller agree |

## Settlement Methods
| Method | Mechanism | When Used |
|--------|-----------|-----------|
| Assignment | Transfer via A&A, buyer joins syndicate directly | **Default for US par trades** |
| Participation | Seller retains legal position, buyer gets economic interest | When assignment blocked (DQ list, consent issues) |
| Novation (LMA) | Old contract cancelled, new one created | **Default for UK/EU trades** |

## Settlement Timeline (US Par Trade)
| Step | Timing | Owner |
|------|--------|-------|
| Trade execution | T+0 | Buyer/seller via dealer |
| Trade confirmation (ClearPar) | T+1 | Both parties confirm |
| Documentation drafting | T+1 to T+3 | Seller's counsel |
| KYC/tax form collection | Parallel | Agent + buyer |
| A&A execution | T+3 to T+5 | Both parties + agent |
| Agent processing & register update | T+5 to T+7 | Agent |
| Funds settlement | T+7 target | Agent |

## Key Operational Rules

**Assignment Freeze:** No assignments close within **5 business days** of a payment date unless TT Manager/RM grants explicit exception.

**Delayed Compensation:** If settlement extends past T+7, the buyer owes the seller per-diem interest on the trade amount from T+7 to actual settlement. Calculated at the loan's current interest rate. Paid outside the agent — bilateral between buyer/seller.

**BISO (Buy-In/Sell-Out):** If settlement delayed past **20 business days** (par) or **30 business days** (distressed), the non-defaulting party can force close at market price. The defaulting party pays the difference plus costs.

**DQ Lists:** Agent must check every assignee against the deal's Disqualified Lender list before processing. DQ lists now used tactically — some include competitor names, affiliate definitions, debt fund exclusions.

**Eligible Assignee:** Credit agreement defines who can hold loans. Common requirements: minimum commitment amount ($1-5M), institutional investor status, borrower consent (sometimes). Agent consent almost always required.

## Platforms
| Platform | Function | Volume |
|----------|----------|--------|
| ClearPar (S&P Global) | Settlement, trade confirmation | 2M+ allocations/yr, 9,300+ facilities |
| Octaura | Electronic trading | ~6% of secondary volume |
| Versana | Loan data/analytics | Data aggregation |
