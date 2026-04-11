---
name: loan-agency-billing-invoicing
description: Use when the user asks about billing, invoicing, agency fees, ad hoc fees, named agent fees, fee letters, fee proposals, invoice generation, billing ticklers, outstanding invoice follow-up, fee collection, or any workflow involving fee billing and invoice management in loan agency operations. Also trigger for questions about fee letter creation, fee structures, or sub-agency billing arrangements.
---

# Loan Agency Billing & Invoicing

## Overview

This skill covers the fee billing lifecycle: fee types, tickler-driven billing workflow, invoice generation, fee letter structure, and outstanding invoice follow-up. Billing is an RA-led function with RM oversight.

**Key principle:** All billing is driven by ticklers — there is no automatic invoice generation. If the tickler is missed, the fee goes unbilled.

---

## Critical Rules (Read First)

### 1. Three Fee Types

| Fee Type | Definition | Frequency |
|----------|-----------|-----------|
| **Agency Fees** | Routine administrative fees per Fee Letter | Annual, quarterly, or monthly |
| **Ad Hoc Fees** | One-time fees for services outside Fee Letter scope | Per event (amendments, terminations, assignments) |
| **Named Agent Fees** | Fees payable to a named agent other than the sub-agent | Per agreement |

### 2. Financial System Customer Must Exist Before First Invoice

Set up the borrower as a customer in the financial management system during deal onboarding.

---

## 1. Fee Letter Structure

- **Agency Fee:** amount, frequency, payment terms
- **Ad Hoc Fee schedule:** rates for specific services
- **Expense reimbursement:** scope of reimbursable expenses
- **Fee payment timing:** in advance, in arrears, or upon event
- **Fee escalation:** annual increase provisions
- **Sub-agency:** Fee Letter may be addendum to master agreement

---

## 2. Billing Workflow (Tickler-Driven)

### Recurring Agency Fees
1. Tickler fires at billing period start
2. RA confirms with RM — fee amount, no amendments to Fee Letter, deal active
3. RA reviews Deal Summary for billing contact and terms
4. RA generates invoice
5. RA sends to fee contact
6. Track in task tracker

### Ad Hoc Fees
1. Triggering event occurs (amendment, assignment, etc.)
2. RM determines fee amount per Fee Letter or negotiation
3. RM notifies RA → RA generates and sends invoice

---

## 3. Invoice Generation

1. Navigate to customer in financial system
2. Create invoice: customer, date, due date, line items, deal reference
3. Review for accuracy → submit/approve
4. Generate PDF → send to billing contact
5. Record in task tracker

---

## 4. Outstanding Invoice Follow-Up

| Days Outstanding | Action |
|-----------------|--------|
| Due + 15 BD | First reminder |
| Due + 30 BD | Escalate to RM for direct contact |
| Due + 60 BD | Escalate to management |
| Due + 90 BD | Consider formal demand; senior escalation |

---

## 5. Sub-Agency Billing

- Fee Letter typically addendum to Master Sub-Agency Agreement
- Billing may be to named agent (not borrower)
- Follow-up routes through named agent relationship

---

## 6. Common Ad Hoc Fee Triggers

| Event | Notes |
|-------|-------|
| Amendment processing | Per Fee Letter |
| Assignment processing | $3,500 standard (LSTA); paid by buyer |
| Waiver/consent | Per Fee Letter |
| Deal termination | Per Fee Letter |
| Escrow services | Per Fee Letter |
| Successor agent transition | Per Fee Letter |
