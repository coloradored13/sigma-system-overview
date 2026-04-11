---
name: loan-agency-payment-processing
description: Use when the user asks about payment processing, wire approvals, rate setting, debt service notices (DSN), borrowing requests, drawdowns, funding notices, rollovers, wire creation, payment files, or any workflow involving money movement in loan agency operations. Covers the complete payment cycle from rate determination through wire release, including TT/RM/RA handoffs, maker-checker controls, banking platform specifics, and day-count verification. Also trigger for questions about C&C notices, rate set notices, RFR calculator verification, assignment freeze rules near payment dates, or sub-agency DSN timing differences.
---

# Loan Agency Payment Processing

## Overview

This skill covers the end-to-end payment cycle for loan agency operations: rate setting, debt service notice generation, funds receipt and verification, wire creation and release, and borrowing/drawdown processing. It addresses the handoffs between Transaction Team (TT), Relationship Managers (RM), and Relationship Associates (RA), and the controls that prevent errors in the highest-risk operational workflow.

**Key principle:** Every payment touches at least three people (TT maker, TT checker, RM approver). No wire leaves without two-person approval in the banking platform. No lender receives cash without a validated tax form and completed callback on file.

**Systems involved:**
- **Loan System** (DLX / legacy platforms) — system of record for loan positions, accruals, rate sets, and notice generation
- **Banking platform(s)** — wire release and approval
- **Debt Service Schedule (DSS)** — spreadsheet tracking global accruals (visual aid only; Loan System is authoritative)
- **Task tracking system** — audit trail for approvals and ad hoc wire tickets

---

## Critical Controls (Read First)

### 1. No Payment Without Tax Form + Callback

Before ANY cash distribution to a lender:
- A valid, reviewed W-9 or W-8 must be on file (see `loan-agency-tax-form-review` skill)
- A callback must have been completed to verbally confirm the lender's wire instructions

If either is missing, the payment **cannot proceed**. Escalate to TT Manager.

### 2. Two-Person Wire Approval Is Mandatory

Every wire release requires two different Authorized Approvers in the banking platform:
- **First approval:** RM reviews wire count and total amount, approves in banking portal
- **Second approval:** RA (or another Authorized Approver) completes second approval
- First and second approver **must be different people**
- Approval is evidenced in the banking platform itself

### 3. Assignment Freeze Rule (5 Business Days)

If an Assignment & Assumption (AA) is received within **5 business days** of a payment date, TT must check whether the deal is on assignment freeze. Assignments should not close during freeze unless TT Manager or RM grants an explicit exception. Closing an assignment during freeze risks paying the wrong lender.

### 4. Day-Count Errors Are Expensive

Applying the wrong day-count convention on a $500M loan changes interest by ~$100,000+ per quarter.

| Currency | Convention | Denominator |
|----------|-----------|-------------|
| USD (SOFR) | Actual/360 | 360 (full-year interest exceeds stated rate by ~1.4%) |
| EUR (EURIBOR) | Actual/360 | 360 |
| GBP (SONIA) | Actual/365 (Fixed) | 365, even in leap years |

Always verify the convention against the credit agreement — do not assume from currency alone.

### 5. Floor Applies to Benchmark Only

Interest rate floors apply to the SOFR/benchmark component only, **not** to the all-in rate (benchmark + spread). Applying the floor to the all-in rate overstates interest.

Example: Floor = 1.00%, SOFR = 0.75%, Spread = 3.00%
- **Correct:** max(0.75%, 1.00%) + 3.00% = **4.00%**
- **Wrong:** max(0.75% + 3.00%, 1.00%) = 3.75% (underapplied floor) — or max(3.75%, 1.00%) + 3.00% = 6.75% (overapplied)

### 6. Pro Rata Shares Must Be Recalculated After Any Balance Change

After partial repayments, assignments, or PIK capitalization, lender shares change. Recalculate to sufficient decimal places before the next distribution. Rounding errors compound over the life of the loan.

---

## 1. Rate Setting & Rollover Workflow

### Timeline

| Step | Timing | Owner |
|------|--------|-------|
| Review Loan System for AA accuracy | 5+ BD before payment | TT |
| Check assignment freeze if AA pending | 5 BD window | TT |
| Receive C&C notice from borrower | Typically 3 BD before payment (SOFR); 1 BD (ABR) | RM |
| Rate determination / rate fix in Loan System | 2 BD before interest period start (or per loan docs) | TT |
| Rate Set Notice generated and sent | After rate fix | TT / Loan System |
| Compounded rate review (RFR deals) | Before end of Observation Period (~5 BD before payment) | RM |

### Continuation/Conversion (C&C) Notice Processing

1. **Borrower sends C&C notice** — typically an exhibit to the credit agreement specifying interest period election and rate type (Term SOFR tenor, ABR, conversion between types)
2. **RM reviews notice:** confirms form compliance, correct facility, permitted election, proper notice timing per credit agreement
3. **RM saves notice** to deal file and notifies TT via operations inbox
4. **TT updates DSS** with elections from C&C notice
5. If no C&C notice received by deadline → RM contacts borrower (named agent deals) or named agent (sub-agent deals). If no response, credit agreement typically defaults to rollover of same tenor

### Rate Determination

**Forward-looking rates (Term SOFR, EURIBOR):**
- Rate known at beginning of interest period
- Fixing date: **2 business days before** interest period start
- TT sets rate in Loan System based on C&C election and published rate
- Loan System presents rate from static data tables → TT accepts or overrides
- Rate Set Notice generated automatically and sent to borrower and lenders

**Compounded/simple rates (SONIA, Daily Simple SOFR):**
- Rate NOT known until near end of interest period
- SONIA: compounded in arrears with lookback (typically 5 BD)
- Daily Simple SOFR: overnight rate applied without compounding
- Approve Rollover Book Request in Loan System → no rate shown at period start → no rate fix notice at that point
- RM reviews rates prior to end of Observation Period
- Use **RFR Calculator** to verify system calculations for compounded rates

### Rate Fix Sequence

Rate fix can be completed before or after Rollover/IPD in the Loan System, but **always complete the rate fix** to avoid interest calculation errors. In DLX: Deal Actions > Rollover Deal triggers the rollover; rate fix is a separate step.

### Common Rate Setting Errors

| Error | Impact | Prevention |
|-------|--------|------------|
| Wrong SOFR tenor (1M vs 3M) | Materially different rate | Verify against C&C notice election; cross-check Loan System |
| Rate set on wrong date | Incorrect benchmark | Confirm fixing date = T-2 BD before period start |
| Missed C&C notice | Default rollover may not match borrower intent | Calendar C&C deadlines; follow up proactively |
| Rounding intermediates | Cascading errors | Carry max decimal precision; round only final amounts |

---

## 2. Debt Service Notice (DSN) Generation

The DSN informs the borrower of the upcoming payment amount, due date, accrual details, and wire instructions. It is the formal demand for payment.

### Timeline

| Deal Type | DSN Lead Time |
|-----------|--------------|
| Standard deals | **11+ business days** before payment date |
| Sub-agency deals | **Per named agent requirements** (may be longer, e.g., 13 BD) |

Always check the delegation agreement or services agreement for sub-agency deals — the named agent may require earlier DSN delivery than the standard timeline.

### Workflow

1. **TT generates DSN** in Loan System at the required lead time
2. **TT reviews DSN** — verifies amounts, dates, accrual calculations, wire instructions
3. **RM reviews and approves** DSN
4. **Loan System sends DSN** to borrower (and lenders, if applicable)

### Sub-Agency Additional Steps

For sub-agency deals, after DSN generation:
- Additional reporting may be required (e.g., loan accruals reports posted to the named agent's data room)
- DSN copies may need to be consolidated per deal for the named agent
- Check the sub-agency duties matrix for deal-specific posting and reporting obligations

### DSN Content (Typical)

- Deal name and facility reference
- Payment date
- Interest period (start/end dates)
- Outstanding principal balance
- Applicable interest rate (base rate + margin)
- Interest amount due
- Any scheduled principal payment
- Any fees due
- Total payment amount
- Wire instructions for payment to agent

---

## 3. Payment Receipt & Wire Release

### Funds Receipt

1. **RM/RA checks banking platform** for incoming funds on payment date
2. If funds **not received** by payment date:
   - Named agent deals → RM contacts borrower directly
   - Sub-agent deals → RM contacts named agent
3. Once funds confirmed: **RM notifies TT** via operations inbox to release wires

### Wire Creation

**Automated (Loan System → Banking Platform):**
- TT releases wires from Loan System directly to banking platform
- If automated push fails, fall back to wire upload templates

**Template-based (manual upload):**
- Banking platforms may have separate templates for domestic wires, international with IBAN, and international without IBAN
- Some platforms support deal-specific pre-populated templates

**Manual wires (ad hoc):**
- Reviewed by two TT members
- Evidenced via ad hoc wire ticket in the task tracking system
- Used for non-standard payments (fee payments, expense reimbursements, etc.)

### Wire Approval Sequence

1. TT creates wires (automated or template-based)
2. **RM reviews:** wire count + total amount in banking portal
3. **RM approves** (first approval) in banking portal
4. **RA (or second Authorized Approver) approves** (second approval) in banking portal
5. Wires release per banking platform cut-off times

**Banking platform cut-off times matter:** Wires released after the platform's daily cut-off will process on the next business day.

### Payment Verification

TT verifies in the Loan System that:
- Amount received matches amount expected per DSN
- Payment is applied to correct facility/loan
- Interest vs. principal allocation matches loan terms
- Any shortfall or overpayment is flagged to RM immediately

---

## 4. Borrowing / Drawdown Processing

### Notice Requirements

| Rate Type | Minimum Notice to Agent |
|-----------|------------------------|
| SOFR loans | Typically 3 business days |
| ABR (base rate) loans | Typically 1 business day |
| Swingline | Per credit agreement (often same-day) |

Actual notice periods are per the credit agreement — always verify.

### Workflow

1. **Borrower sends borrowing request** to RM (or to named agent for sub-agent deals)
2. **RM reviews request:** correct facility, permitted borrower, permitted currency, minimum draw amount, conditions precedent satisfied
3. **RM updates Deal Summary** with new borrowing details and notifies TT
4. **TT validates in Loan System:**
   - Correct facility identified
   - Available commitment sufficient for draw amount
   - Conditions precedent satisfied (per credit agreement / Deal Summary)
   - Minimum borrowing amount met
   - Permitted borrower and currency
5. **TT creates borrowing** in Loan System and updates DSS
6. **Second TT member reviews** DSS and Loan System setup
7. **RM reviews and approves** the borrowing
8. **TT generates and sends funding/borrowing notices** to lenders:
   - Named agent deals: generated and sent per Loan System
   - Sub-agent deals: coordinate with named agent on notice distribution
9. **On funding date:** lenders fund their pro rata share → agent verifies individual amounts → distributes aggregate to borrower

### Funds Flow Through Agent

If funds flow through the agent (typical for named agent deals):
- TT creates ad hoc wire ticket in the task tracking system for the outgoing borrower wire
- Same two-person wire approval requirement applies
- Verify total received from lenders matches expected before releasing to borrower

---

## 5. Payment Waterfall Reference

When distributing payments, follow the credit agreement's payment waterfall. The standard priority (absent default) is:

1. **Interest** — pro rata to all lenders based on share
2. **Scheduled principal** — per amortization schedule
3. **Fees** — commitment fees, LC fees, admin fees per agreement terms

**Mandatory prepayments** (asset sale sweeps, excess cash flow sweeps) have their own application order, typically inverse order of maturity. These provisions are heavily negotiated — always read the specific credit agreement.

**Post-acceleration (default) waterfall:**
1. Agent fees and expenses
2. Accrued and unpaid interest (pro rata)
3. Outstanding principal (pro rata)
4. All other obligations (pro rata)
5. Surplus to borrower

Amendments to payment priority or pro rata sharing require **all-lender consent** (sacred right).

---

## 6. [UK] Variations

### Rate Handling
- GBP loans reference **SONIA** (compounded in arrears, Actual/365 Fixed)
- Rate is NOT known until near end of interest period — requires lookback mechanism (typically 5 BD)
- No Rate Set Notice at period start; rate confirmed near period end
- Use RFR Calculator to verify compounding

### Settlement
- Payments via **CHAPS** (real-time GBP settlement, same-day)
- Business day conventions may differ — check credit agreement for London/New York business day definitions

### Transfer Mechanism
- UK/LMA uses **novation** (not assignment) — extinguishes and recreates the obligation
- Agent title: **Facility Agent** (not Administrative Agent)
- Collateral held by **Security Trustee** (on trust, not directly)

### Withholding
- Standard UK withholding on interest: **20%**
- DTTP scheme may apply for qualifying lenders
- Check current HMRC guidance before assuming gross payment is permissible

---

## 7. Quick Reference

### Standard Timelines
| Item | Timeline |
|------|----------|
| DSN generation (standard) | 11+ BD before payment |
| DSN generation (sub-agency) | Per named agent requirements (may be 13+ BD) |
| C&C notice from borrower | Typically 3 BD (SOFR), 1 BD (ABR) |
| Rate fixing date (Term SOFR) | 2 BD before period start |
| Assignment freeze check | Within 5 BD of payment |
| SONIA lookback | Typically 5 BD |

### Maker-Checker-Approver Chain
| Action | Maker | Checker | Approver |
|--------|-------|---------|----------|
| Rate set in Loan System | TT #1 | — | RM |
| DSN generation | TT #1 | — | RM |
| Borrowing setup in Loan System | TT #1 | TT #2 | RM |
| DSS update | TT #1 | TT #2 | RM |
| Wire release | TT creates | RM (1st approval) | RA (2nd approval) |
| Manual/ad hoc wire | TT #1 | TT #2 | RM (+ task tracker evidence) |

### Interest Calculation Quick Check
Formula: **Principal × Rate × (Days / Day-Count Denominator)**

Example: $100M, 7.25% all-in, 28-day February period, Actual/360:
$100,000,000 × 0.0725 × (28 / 360) = **$563,889**

Always verify: correct principal balance, correct all-in rate (benchmark + spread, floor applied to benchmark only), correct day count for the period, correct denominator for the currency.
