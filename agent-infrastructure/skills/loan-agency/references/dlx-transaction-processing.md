---
name: dlx-transaction-processing
description: Use when the user asks about processing a drawdown in DLX, rollover in DLX, IPD (interest payment date) processing, rate fix in Oneiro, deal amendment in DLX, editing a loan, continuation notice processing in DLX, capitalisation or PIK processing, bulk trading in DLX, or any day-to-day transaction processing in the Oneiro DLX platform. Covers the DLX UI workflows for drawdowns, rollovers, rate fixes, amendments, and loan edits. Also trigger for questions about forward-looking vs RFR rate handling differences in DLX, activity approval workflows, or DLX Deal Actions menu options.
---

# DLX Transaction Processing

## Overview

This skill covers day-to-day transaction processing in the Oneiro DLX platform: drawdowns, rollovers/IPDs, rate fixes, deal amendments, loan edits, PIK capitalization, and bulk trading.

**Key principle:** Every transaction follows Create → Review → Approve, mirroring maker-checker-approver controls. Activities generate workflow tasks completed in sequence.

---

## Critical Gotchas (Read First)

### 1. Forward-Looking vs RFR Rate Handling

| Rate Type | Examples | Known at Period Start? | Rate Fix Timing | Rate Set Notice? |
|-----------|----------|----------------------|-----------------|-----------------|
| Forward-looking | Term SOFR, EURIBOR | Yes | At or before period start | Yes |
| RFR (backward-looking) | SONIA, compounded SOFR | No | Near period end | No |

**Forward-looking:** System presents rate → user accepts or overrides → Rate Set Notice generated.
**RFR:** Approve Rollover Book Request → no rate shown → rate determined at period end.

### 2. Always Complete Rate Fix

Leaving a rate fix incomplete causes cascading interest calculation errors.

### 3. Rollover Is Triggered from Deal Actions

Deal Actions > Rollover Deal — initiated at deal level, not individual loan/facility.

### 4. Amendment Changes Are Permanent

Verify all changes against the executed amendment document before approving.

---

## 1. Drawdown Processing

### Prerequisites
- Borrowing request received and approved by RM
- Available commitment sufficient
- Conditions precedent satisfied

### DLX Workflow

1. Navigate to facility → Initiate drawdown
2. **Financing date** — draw date
3. **Request details:** amount, currency, loan type, interest period
4. **Documents** — attach borrowing request
5. **Review** — verify against borrowing request and Deal Summary
6. **Share adjustments** — verify lender pro rata shares
7. **Submit for approval**
8. **Approval** — RM reviews and approves
9. **Rate fix** — set applicable rate (forward-looking: now; RFR: later)
10. **Release funds** — generate funding notices, process disbursement

Drawdown creates a new LoanV2 child under FacilityV2 in DLX's transaction tree.

---

## 2. Rollover / IPD Processing

1. **Deal Actions > Rollover Deal** — initiates for all loans with payments due
2. **Review:** current/new period dates, interest amount, principal payment
3. **Payment options:** interest only, interest + scheduled principal, interest + prepayment, full repayment
4. **Submit** → second TT review → RM approval
5. **Notices:** DSN, Rate Set Notice, payment notices
6. **Rate fix** (if not already completed)
7. **Release payments**

### Rollover Book Request (RFR Loans)
- System creates request → approve to roll into new period
- Rate not set at this point
- No Rate Set Notice generated

---

## 3. Rate Fix

### Forward-Looking (Term SOFR, EURIBOR)
1. Navigate to interest cycle
2. System presents rate from data tables
3. **Verify:** correct benchmark/tenor, correct fixing date (T-2 BD), matches published source
4. Accept or override (document reason for override)
5. Rate Set Notice generated and sent

### RFR (SONIA, Compounded SOFR)
1. Rate determinable near end of interest period
2. System calculates based on daily observations and compounding method
3. Verify using RFR Calculator
4. Approve rate fix → interest amount finalizes

---

## 4. Deal Amendment in DLX

1. Navigate to deal → Amend Deal
2. Select changes: facility terms, rates, lender shares, fees, parties
3. Enter new values per executed amendment
4. Attach executed amendment document
5. Submit → maker-checker review → RM approval

| Action | When to Use |
|--------|-------------|
| **Amend Deal** | Permanent structural changes from executed amendments |
| **Edit Loan** | Corrections or adjustments to existing loans |

---

## 5. PIK (Capitalisation) Processing

1. At IPD, system identifies PIK-eligible interest
2. Interest capitalizes into principal (no cash payment)
3. Review PIK amount calculation
4. Approve → principal balance increases
5. **Post-PIK:** Pro rata shares may need recalculation

---

## 6. Bulk Trading

For processing multiple assignments simultaneously:
1. Navigate to Bulk Trading function
2. Upload/enter multiple assignment details
3. System processes as batch with individual validation
4. Review results, fix failures, approve valid assignments

See `loan-agency-assignments` skill for full assignment workflow.

---

## 7. Activity Processing and Notices

### Activity Statuses
- **Pending** → **In Progress** → **Completed** or **Rejected**

### Notice Types

| Notice | Triggered By | Sent To |
|--------|-------------|---------|
| Rate Set Notice | Rate fix (forward-looking) | Borrower + lenders |
| Debt Service Notice | DSN generation | Borrower |
| Funding/Borrowing Notice | Drawdown | Lenders |
| Payment Notice | Payment processing | Internal |
| Preliminary Notice | Various activities | Per configuration |
| Activity Notice | Activity completion | Subscribed users |
