---
name: loan-agency-tax-form-review
description: Use when the user asks about reviewing tax forms, W-9 validation, W-8 review, W-8BEN, W-8BEN-E, W-8ECI, W-8EXP, W-8IMY, withholding determination, tax form expiration, FATCA classification review, Chapter 3 or Chapter 4 status, portfolio interest exemption, lender tax documentation, tax form tracking, or any workflow involving tax form validation for lenders. Covers line-by-line review checklists for each IRS form type, expiration tracking, withholding rate determination, and the general rule that no payment may be made without a valid reviewed form on file. Also trigger when the user asks what to check on a specific form, how to validate treaty claims, how to determine withholding rates, when forms expire, what makes a form invalid, what a specific W-8 line means, or when to reject a form.
---

# Loan Agency Tax Form Review

## Overview

This skill covers the line-by-line review of IRS tax forms (W-9 and W-8 series) for lenders, withholding rate determination, and form expiration tracking. Tax form review is a TT function and is a hard prerequisite for any cash distribution to a lender.

**General rule: No cash distribution may be made to any lender until a W-9 or W-8 has been received AND reviewed.**

**Default withholding:** 30% on any interest or fee payment to a foreign person (FDAP income under §§871(a)/881(a)) unless a valid form establishes a reduced rate or exemption.

---

## Critical Rules (Read First)

### 1. Undocumented Lender = 30% Withholding

If no valid tax form is on file, apply presumption rules: treat as foreign person, withhold 30%. No exceptions. The administrative agent is a **withholding agent** under IRC §7701(a)(16) with independent statutory liability under §1461.

### 2. Accept Only Current Revisions

| Form | Current Revision |
|------|-----------------|
| W-9 | **Rev. March 2024** |
| W-8BEN | Rev. October 2021 |
| W-8BEN-E | Rev. October 2021 |
| W-8ECI | Rev. October 2021 |
| W-8IMY | Rev. October 2021 |
| W-8EXP | Rev. October 2023 |

Reject any form on a superseded revision.

### 3. Expiration Rules Are Not Uniform

**General rule:** Valid from signature date through last day of **third succeeding calendar year** (signed any date in 2024 → expires Dec 31, 2027).

**Indefinite validity exceptions:**
- W-8IMY: Indefinite (but underlying certificates/withholding statements expire on their own schedules)
- W-8EXP: Indefinite for integral parts of foreign governments, central banks, international organizations
- Any W-8 with US TIN: Indefinite IF agent reports ≥1 payment annually on 1042-S
- W-8BEN/BEN-E paired with documentary evidence: Indefinite for foreign status claims (not treaty claims)

**Always 3-year:** Treaty claims on any form, W-8ECI

### 4. Electronic Signatures Are Permanently Permitted

Per T.D. 9890, electronic signatures are accepted on all W-8 forms. Must be: capable of verification, applied with intent to sign, attached to the form.

---

## 1. W-9 Review Checklist (US Persons)

| Line/Section | Check |
|-------------|-------|
| Revision | Must be **Rev. March 2024** |
| Line 1 | Name matches lender's legal name in deal documents |
| Line 2 | Business name / DBA (if different from Line 1) |
| Line 3 | Federal tax classification checked |
| Line 4 | Exemption codes (if applicable) |
| Line 5-6 | Address (must be US address for US person; foreign address → may need W-8) |
| Line 7 | Account number(s) — optional |
| **Part I** | **TIN (SSN or EIN)** — must be 9 digits. If missing or obviously invalid, reject |
| **Part II** | **Certification** — must be signed and dated |

**After review:** Save to depository. Update tax form tracking spreadsheet. Withholding rate: **0%**.

---

## 2. W-8BEN Review Checklist (Foreign Individuals)

| Line/Section | Check |
|-------------|-------|
| Revision | Must be **Rev. October 2021** |
| **Part I** | |
| Line 1 | Name of individual (must match deal documents) |
| Line 2 | Country of citizenship |
| Line 3 | Permanent residence address (must be in treaty country if claiming treaty) |
| Line 4 | Mailing address (if different) |
| Line 5 | US TIN (if any) — extends form validity if present |
| Line 6 | Foreign TIN |
| **Part II** | **Treaty claim (if applicable)** |
| Line 9a | Country of residence for treaty purposes |
| Line 9b | Treaty article claimed (e.g., Article 11 for interest) |
| Line 10 | Rate of withholding claimed and conditions |
| **Part III** | Certification: beneficial owner, not 10% shareholder, not receiving ECI |
| **Signature** | Signed, dated, capacity stated |

**Key check:** If treaty claimed, verify the country has a treaty with the US and the article/rate is valid for interest income.

**Withholding rate:** Per treaty claim if valid; otherwise 0% if portfolio interest exemption applies; otherwise 30%.

---

## 3. W-8BEN-E Review Checklist (Foreign Entities)

Most complex form — 30+ possible FATCA status classifications.

| Section | Check |
|---------|-------|
| Revision | Must be **Rev. October 2021** |
| **Part I — Identification** | |
| Line 1 | Name of organization (match to deal documents) |
| Line 2 | Country of incorporation/organization |
| Line 3 | Disregarded entity name (if applicable — triggers Part II) |
| Line 4 | **Chapter 3 status** — one box checked |
| Line 5 | **Chapter 4 (FATCA) status** — one box checked (30+ options) |
| Line 6-7 | Address |
| Line 8 | US TIN (if any) |
| Line 9a | **GIIN** — required for Participating FFI, Reporting Model 1/2 FFI. Verify against IRS FFI List |
| Line 9b | Foreign TIN |
| **Part II** | Disregarded entity details (only if Line 3 filled) |
| **Part III — Treaty Claim** | |
| Line 14a-c | Country, article, rate, conditions |
| Line 15 | **Limitation on Benefits (LOB)** — must check at least one box |
| **Parts IV-XXVIII** | FATCA status-specific certifications (only the relevant part) |
| **Part XXX** | Certification — signature, date, capacity |

**Key checks:**
- Chapter 3 and Chapter 4 statuses internally consistent
- If Participating FFI: GIIN present and valid on IRS FFI List
- If Nonparticipating FFI: flag for 30% FATCA withholding
- If treaty claimed: LOB completed
- If disregarded entity: Part II fully completed

---

## 4. W-8ECI Review Checklist (Effectively Connected Income)

| Line/Section | Check |
|-------------|-------|
| Revision | Rev. October 2021 |
| Part I | Name, country, address, US TIN (**required**) |
| Part II | Nature of income and US trade/business connection |
| Signature | Signed, dated |

**Always expires on 3-year rule.** Withholding rate: **0%** (ECI taxed on net basis).

---

## 5. W-8EXP Review Checklist (Foreign Governments/International Organizations)

| Line/Section | Check |
|-------------|-------|
| Revision | **Rev. October 2023** |
| Part I-II | Entity identification and type |
| Part III | Tax exemption claim — must identify applicable IRC section |
| Signature | Signed by authorized official |

**Expiration:** Integral parts of foreign governments, central banks, international organizations → **indefinite**. Controlled entities → 3-year rule.

---

## 6. W-8IMY Review Checklist (Foreign Intermediaries / Flow-Through)

| Line/Section | Check |
|-------------|-------|
| Revision | Rev. October 2021 |
| Part I | Intermediary identification and type |
| Part II-III | Status certifications |
| **Withholding Statement** | **Required attachment.** Must allocate income to each beneficial owner |
| **Underlying forms** | Each beneficial owner must have a valid W-8 or W-9 on file |

**Expiration:** W-8IMY itself: **indefinite**. Underlying forms: expire on their own schedules.

**Key gotcha:** A W-8IMY without valid underlying forms is useless — 30% withholding still applies to undocumented portions.

---

## 7. Form Expiration Tracking

### Tracking Process

Tax forms tracked in a centralized spreadsheet:
- Form type, revision, date received, date reviewed
- Signature date → calculated expiration date
- Flag forms approaching expiration (90-day advance warning recommended)
- Solicit replacement forms before expiration

### Change in Circumstances

- Existing form becomes invalid upon change in circumstances
- Lender has **30 days** to provide new form
- During 30-day window: may rely on existing form
- After 30 days without new form: 30% withholding

---

## 8. Withholding Rate Determination

### Decision Flow

1. **Valid W-9 on file?** → 0%. Done.
2. **No form on file?** → 30%. Stop — no payment until form received.
3. **Valid W-8BEN or W-8BEN-E with treaty claim?** → Apply treaty rate.
4. **Valid W-8 with portfolio interest exemption?** → 0% (confirm: registered obligation, not 10% shareholder, not bank receiving ordinary course interest, not CFC related person interest).
5. **Valid W-8ECI?** → 0%.
6. **Valid W-8EXP?** → 0%.
7. **Valid W-8IMY?** → Look through to underlying forms.
8. **Nonparticipating FFI (FATCA)?** → 30% FATCA withholding (universally carved out of gross-up).
9. **None of the above?** → 30%.

### Gross-Up Implications

If withholding applies and tax is an "Indemnified Tax" under the credit agreement, borrower must gross-up. **Excluded Taxes** (no gross-up): taxes from lender's own nexus, taxes in effect at acquisition (grandfathering), taxes from lender's failure to provide documentation, FATCA withholding.

---

## 9. Filing and Record-Keeping

- Save reviewed forms to secure depository
- Update tax form tracking spreadsheet
- **1042-S reporting:** Annual, filed by March 15. Furnish copy to recipient by March 15.
- **FIRE system retiring Dec 31, 2026** — migrate to **IRIS** for e-filing
- **Recordkeeping:** Maintain forms and documentation for at least **10 years**
