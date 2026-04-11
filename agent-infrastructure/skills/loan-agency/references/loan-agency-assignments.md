---
name: loan-agency-assignments
description: Use when the user asks about assignments, trade settlement, assignment and assumption agreements (AA), ClearPar workflow, lender transfers, assignment fees, assignment checklists, secondary loan trading, BISO (buy-in/sell-out), delayed compensation, par or distressed trades, assignment freeze rules, DQ lists (disqualified lenders), minimum assignment amounts, or any workflow involving processing a lender transfer in loan agency operations. Also trigger for questions about LMA novation procedures for UK deals.
---

# Loan Agency Assignments

## Overview

This skill covers the end-to-end workflow for processing secondary loan trade assignments — from receipt of the Assignment and Assumption agreement (AA) through register update and post-closing steps. Assignments are high-volume (driven heavily by CLO trading activity) and involve coordination between TT, RM, and external parties.

**Key principle:** The agent maintains the official register of lenders. An assignment is not effective until the agent processes it and updates the register. Getting the register wrong means paying the wrong lender.

**Systems involved:**
- **ClearPar** (S&P Global) — trade settlement platform
- **Loan System** — official register of record
- **Assignment Tracker** — centralized spreadsheet tracking all assignments
- **Task tracking system** — audit trail

---

## Critical Rules (Read First)

### 1. Assignment Freeze (5 Business Days Before Payment)

If an AA is received within **5 business days** of a payment date, TT must check whether the deal is on assignment freeze. Assignments should **not** close during freeze unless TT Manager or RM grants an explicit exception.

### 2. Agent Consent May Be Required

Check the credit agreement for:
- Whether agent consent is required (and whether it can be unreasonably withheld)
- Whether borrower consent is required (typically only when no event of default exists)
- Minimum assignment amount (typically $1M for term loans)
- Whether the buyer is on the **DQ List** — if so, assignment is prohibited

### 3. Standard Assignment Fee Is $3,500

Per LSTA MCAPs. Typically paid by the buyer. Verify the credit agreement.

### 4. Tax Form + Callback Before First Payment to New Lender

New lenders must provide: Administrative Details Form, valid tax form (W-9 or W-8), and complete a wire instruction callback before any payment.

---

## 1. Receiving Assignments

### Via ClearPar
- Most BSL assignments arrive through ClearPar
- Agent receives notification in ClearPar's Agent User Interface (CUI)
- Agent retrieves AA documentation from ClearPar

### Via Email/Direct
- Some assignments (particularly private credit) arrive as PDF AAs via email

### Initial Logging
- TT #1 records on Assignment Tracker
- Creates deal folder, saves all received documents

---

## 2. Pre-Closing Checklist Review

TT uses the **Assignment Checklist (AC)** — a deal-specific conditions checklist.

### TT #1 Reviews
- **Buyer eligibility:** Not on DQ List, meets lender qualification requirements
- **Minimum assignment amount:** Meets credit agreement threshold
- **Agent consent:** Required? RM must approve
- **Borrower consent:** Required? Consented or deemed consent period (typically 10 BD) elapsed?
- **Documentation:** AA properly completed — correct deal, facility, amounts, effective date, signatures
- **Assignment fee:** Received or confirmed
- **Pro rata calculations:** Amounts correct and sum properly
- **Effective date:** Reasonable and not during assignment freeze

### TT #2 Verification
- Independently reviews TT #1's work
- Confirms all AC conditions checked
- Updates Assignment Tracker

---

## 3. Assignment Freeze Check

| Condition | Action |
|-----------|--------|
| AA received >5 BD before payment | Process normally |
| AA received ≤5 BD before payment | Check freeze status |
| Deal on freeze | Do NOT close unless exception granted |
| Exception granted | Document in task tracker, proceed with caution |

---

## 4. Closing Process

1. **TT #1 completes closing section** of Assignment Checklist
2. **Effective date confirmed**
3. **Agent executes AA** (if agent signature required)
4. **Closing notice distributed** to relevant parties

---

## 5. Post-Closing

### Register Update
- TT updates lender register in Loan System
- Verify pro rata shares recalculate correctly
- Second TT member reviews → RM approves

### New Lender Setup (if buyer is new to the deal)
1. Solicit Administrative Details Form
2. Collect and review tax form (see `loan-agency-tax-form-review` skill)
3. Set up lender in Loan System
4. Complete callback for wire instructions
5. Add to lender data room with appropriate access level

### Exiting Lender Cleanup (if seller fully exits)
- Verify zero position
- Archive or remove data room access

---

## 6. Settlement Timeline Reference

### US (LSTA)

| Item | Timeline |
|------|----------|
| Par settlement target | T+7 |
| Distressed settlement target | T+20 |
| Buyer document execution deadline | T+5 |
| Par BISO trigger | T+15 BD |
| Distressed BISO trigger | T+50 BD |
| Par BISO cure period | 5 BD |
| Distressed BISO cure period | 20 BD |
| Cover transaction window | 10 BD |
| Delayed compensation (par) | Accrues from T+7 at Daily Simple SOFR + 11.448 bps |
| Borrower deemed consent period | Typically 10 BD |

### UK/EU (LMA)

| Item | Timeline |
|------|----------|
| Par delayed compensation start | T+10 |
| Distressed delayed compensation start | T+20 |

### BISO (Buy-In/Sell-Out)

Remedy for settlement failure:
- Par: trigger at T+15 BD; Distressed: trigger at T+50 BD
- Cure period allows completion; if not cured: cover transaction (10 BD window)

---

## 7. ClearPar Workflow Summary

### Agent Role
- Receive and review allocation notifications
- Confirm agent consent (if required)
- Track settlement status
- Confirm closing/settlement
- Monitor for BISO triggers

---

## 8. [UK] LMA Novation Differences

- Novation **extinguishes** existing rights and **recreates** for new lender
- Uses **Transfer Certificate** (not AA)
- Agent title: Facility Agent
- Settlement targets differ (T+10 par delayed comp start)
- Register update mechanics are the same
- Same post-closing steps (tax form, admin details, callback, data room)

---

## 9. Common Issues and Escalation

| Issue | Action |
|-------|--------|
| Buyer on DQ List | Reject. Notify parties. |
| Below minimum amount | Reject unless waiver permitted. RM decision. |
| Missing borrower consent (required, no EOD) | Cannot close. Start deemed consent clock if applicable. |
| Assignment during freeze | Exception required. Document in task tracker. |
| Delayed settlement approaching BISO | Flag to RM. Monitor ClearPar. |
| Seller's position doesn't match register | Reconcile before processing. |
| Multiple assignments same deal/date | Process in order received. Verify cumulative shares. |
