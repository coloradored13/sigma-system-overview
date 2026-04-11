# Quick Reference: Tax Withholding & Lender Onboarding

For full IRS form details, treaty networks, and regulatory analysis, see `Doc5_Tax_Withholding_and_Lender_Onboarding.md`.

## Tax Form Decision Tree

### Which Form Does the Lender Need?

| Lender Type | US Person? | Form | Withholding |
|-------------|-----------|------|-------------|
| US corporation, individual, LLC | Yes | **W-9** | 0% (backup withholding 24% if missing) |
| Foreign person, treaty country | No | **W-8BEN** (individual) or **W-8BEN-E** (entity) | Treaty rate (often 0%) |
| Foreign person, no treaty | No | **W-8BEN-E** | **30%** default |
| Foreign entity with US business | No | **W-8ECI** | 0% withholding (income taxed on net basis) |
| Foreign intermediary/flow-through | No | **W-8IMY** + withholding statement + underlying forms | Depends on beneficial owners |
| Foreign partnership | No | **W-8IMY** | Look-through to partners |

### Form Validity
- **W-9:** No expiration (but reverify if information changes)
- **W-8 forms:** Valid for **3 calendar years** from signing (through Dec 31 of 3rd year)
- **Must be on file BEFORE any payment.** No exceptions.

### Portfolio Interest Exemption (Key for Foreign Lenders)
Most foreign lenders in syndicated loans qualify for 0% withholding via the **portfolio interest exemption** (IRC §871(h)/881(c)) if:
- The loan is in **registered form** (syndicated loans qualify)
- The lender is not a **10% shareholder** of the borrower
- The lender is not a **controlled foreign corporation** related to the borrower
- The lender is not a **bank** receiving interest in the ordinary course (bank exception)
- The lender certifies non-US status on W-8BEN-E

**Banks cannot use portfolio interest exemption** — they must rely on treaty benefits or W-8ECI.

## Withholding Rates Summary
| Scenario | Rate |
|----------|------|
| US lender, W-9 on file | 0% |
| US lender, NO W-9 | 24% backup withholding |
| Foreign lender, portfolio interest exemption | 0% |
| Foreign lender, treaty rate | 0-15% (varies by treaty) |
| Foreign lender, no exemption/treaty | **30%** |
| FATCA non-compliant | **30%** |

## Gross-Up Provisions
If withholding applies, the credit agreement's **gross-up clause** may require the borrower to pay additional amounts so the lender receives the full contractual interest. Key points:
- Gross-up typically does NOT apply to withholding caused by lender's failure to provide proper tax forms
- Change-in-law provisions protect lenders from new withholding taxes imposed after closing
- FATCA withholding is typically excluded from gross-up (lender's responsibility)

## KYC/AML Quick Reference

### Required Screening
| Check | Database/Source | Timing |
|-------|----------------|--------|
| OFAC SDN list | OFAC | Every new party + ongoing monitoring |
| OFAC Sectoral Sanctions | OFAC | Same |
| OFSI sanctions | OFSI (UK) | If UK nexus |
| EU sanctions | EU Consolidated List | If EU nexus |
| PEP screening | Commercial databases | New parties |
| Adverse media | Commercial databases | New parties |

### KYC Expiration
- KYC approval valid **30 days** — if deal doesn't close, refresh required
- Ongoing monitoring: periodic refresh per firm policy (typically annual)
- CDD (Customer Due Diligence) requirements per FinCEN/BSA
- Enhanced due diligence for high-risk: PEPs, high-risk jurisdictions, complex structures

## Callback Requirement
Before ANY payment to a lender:
- Valid tax form on file (W-9 or W-8)
- Completed callback to verbally confirm wire instructions
- Both are **hard stops** — no payment without both
