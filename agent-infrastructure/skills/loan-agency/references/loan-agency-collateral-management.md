---
name: loan-agency-collateral-management
description: Use when the user asks about collateral, UCC filings, UCC continuation statements, collateral spreadsheet, collateral issues log, collateral receipt, collateral release, collateral review, semi-annual collateral review, collateral custodian, physical collateral, security interests, pledge agreements, mortgages, DACAs, stock certificates, or any workflow involving collateral document management in loan agency operations. Also trigger for questions about UCC state-specific filing requirements.
---

# Loan Agency Collateral Management

## Overview

This skill covers the receipt, tracking, review, and release of collateral documents. Collateral management is an RM/RA function with periodic review cycles and specific handling for physical vs. non-physical collateral.

**Key principle:** The agent (as Collateral Agent or Security Trustee) holds security interests on behalf of all secured parties. Errors here are only discovered when they matter most — at default/enforcement.

**Key artifacts:**
- **Collateral Spreadsheet** — tracks all collateral documents for a deal
- **Collateral Issues Log** — tracks known potential issues

---

## Critical Rules (Read First)

### 1. Physical vs Non-Physical Handling

| Type | Examples | Storage | Handling |
|------|----------|---------|----------|
| **Physical** | Stock certificates, promissory notes, original signed docs | Secure collateral custodian (US); secure storage (UK) | Inventory, chain of custody |
| **Non-Physical** | UCC filings, filed mortgages, DACAs, security agreements (copies) | Electronic deal file | Tracked in Collateral Spreadsheet |

### 2. UCC Continuation Deadlines Are Absolute

UCC financing statements effective for **5 years**. Continuation must be filed in the **6-month window** before expiration. Missing this deadline = lapsed filing = unperfected security interest. **Irrecoverable.**

### 3. Collateral Issues Log Must Be Actively Managed

Items open >12 months without progress should be escalated during annual review.

---

## 1. Collateral Document Types

- **Security Agreements / Pledges** — grant security interest
- **UCC Filings** — UCC-1 (initial), UCC-3 Continuation/Amendment/Termination
- **Mortgages / Deeds of Trust** — real property liens
- **DACAs** — deposit account control agreements
- **IP Security Agreements** — filed with USPTO/Copyright Office
- **Guarantees, Subordination/Intercreditor Agreements**
- **Insurance Certificates** — agent as loss payee/additional insured

---

## 2. Receipt of Collateral

### Physical
1. Receive via courier/hand delivery → inventory immediately
2. Log in Collateral Spreadsheet
3. Store at collateral custodian (US) or secure storage (UK)
4. Send written receipt acknowledgment

### Non-Physical
1. Receive documents → review for completeness
2. Log in Collateral Spreadsheet → save to deal file
3. Track filing status for UCC/mortgages

### UCC Filing Tracking
- Record: jurisdiction, filing number, filing date, expiration (filing + 5 years)
- Calculate continuation window (6 months before expiration)
- Set tickler for continuation deadline
- **State-specific gotchas:** Name formatting rules, processing times, search logic vary by state

---

## 3. Release of Collateral

### Triggers
- Deal termination, partial release per credit agreement, amendment authorizing release

### Workflow
1. Release request received
2. **RM reviews:** authorized under credit agreement? Consents obtained? Release of all/substantially all = **all-lender consent** (sacred right)
3. Coordinate release documentation with External Counsel (UCC-3 terminations, mortgage releases, DACA terminations)
4. Execute and file/record releases
5. Return physical collateral (verify recipient, obtain signed receipt)
6. Update Collateral Spreadsheet and Issues Log
7. Notify TT if release affects system records

---

## 4. Semi-Annual Collateral Review

**Timing:** Every 6 months. RA performs; RM reviews and approves.

### Checklist

1. **Collateral Spreadsheet accuracy** — all documents listed, descriptions current?
2. **UCC filing status** — all current? Continuations filed? Amendments needed?
3. **Physical collateral verification** — inventory matches Collateral Spreadsheet?
4. **Collateral Issues Log** — status updates, follow-ups, escalate items >12 months
5. **Insurance tracking** — certificates current? Agent named? Renewals tracked?
6. **Post-closing items** — all deliverables received?

Document completed checklist, update task tracker, obtain RM sign-off.

---

## 5. UCC Filing Management

### Key Deadlines

| Event | Deadline |
|-------|----------|
| UCC-1 effectiveness | 5 years from filing |
| Continuation window opens | 6 months before expiration |
| Missed continuation | Filing lapses — irrecoverable |

### Continuation Process
1. Identify filings approaching window
2. Coordinate with counsel → prepare UCC-3 continuation
3. File in same jurisdiction as original UCC-1
4. Confirm filing, update Collateral Spreadsheet with new expiration
5. Set new tickler for next continuation

---

## 6. [UK] Security Trustee Differences

- Collateral Agent (US) → **Security Trustee** (UK) — holds on trust
- Physical collateral stored at secure UK location
- Security interests registered at **Companies House** (21-day deadline from creation — strict)
- Fixed vs floating charge with different priority rules
- Deregistration at Companies House upon release

---

## 7. Collateral Issues Log Reference

| Issue Type | Example |
|-----------|---------|
| Missing document | Security agreement for subsidiary not delivered |
| Filing gap | UCC-1 filed in wrong jurisdiction |
| Name mismatch | Debtor name on UCC-1 doesn't match current legal name |
| Post-closing outstanding | Mortgage recording pending 90+ days |
| Insurance lapse | Certificate expired, renewal not received |
| DACA gap | Bank account without DACA coverage |
