---
name: sub-agency-operations
description: Use when the user asks about sub-agency, sub-agent duties, delegation agreements, named agent relationships, sub-agency DSN timing, sub-agency accruals reporting, sub-agency payment process, sub-agency communication protocols, master sub-agency agreements, or any workflow specific to operating as a sub-agent rather than named agent. This skill covers all operational differences when acting as sub-agent versus named agent on loan deals.
---

# Sub-Agency Operations

## Overview

When an agent serves as **sub-agent** (not the named agent in the credit agreement), the operational scope and authority differ significantly. The sub-agent performs delegated administrative functions under a services agreement with the named agent — not under the credit agreement directly.

**Key principle:** The delegation agreement (Master Sub-Agency Agreement + deal-specific Addendum), not the credit agreement, defines the sub-agent's authority, obligations, and limitations.

---

## Critical Rules (Read First)

### 1. Authority Comes from the Delegation Agreement

The sub-agent's scope is defined by the services/delegation agreement, not the credit agreement. Before performing any action, verify it falls within the delegated scope. Actions outside scope require named agent approval.

### 2. Communication May Require Named Agent Approval

Direct communication with the borrower may require named agent approval. Some communications flow through the named agent rather than directly from the sub-agent. Check the delegation agreement.

### 3. DSN Timelines May Differ

Named agents may require earlier DSN delivery than the standard 11 BD. Common sub-agency requirement: **13 business days** before payment. Always check the deal-specific addendum.

---

## 1. Sub-Agency Relationship Structure

```
Named Agent (in the credit agreement)
  └── Sub-Agent (performs delegated functions)
        └── Governed by: Master Sub-Agency Agreement + Deal Addendum
```

### Governing Documents

| Document | Purpose |
|----------|---------|
| Master Sub-Agency Agreement | Governs overall relationship, standard terms |
| Master Cash Management Agreement | Governs funds flow |
| Deal-specific Addendum | Defines scope for each individual deal |
| Sub-Agency Duties Matrix | Enumerates which functions are delegated |

---

## 2. Operational Differences from Named Agent

### DSN Timeline

| Role | DSN Lead Time |
|------|--------------|
| Named agent (standard) | 11+ BD before payment |
| Sub-agent | **Per named agent requirements** — often 13+ BD |

The entire payment cycle shifts forward accordingly. Ticklers must be set to the sub-agency timeline, not standard.

### Accruals Reporting

Sub-agency deals may require additional reporting not needed for named-agent deals:
- Loan accruals reports pulled from Loan System and posted to named agent's data room
- DSN copies consolidated per deal for the named agent
- Frequency and format per the duties matrix

### Data Room Posting

| Document | Named Agent Deals | Sub-Agent Deals |
|----------|------------------|-----------------|
| DSN | Generated and sent to borrower | Generated, sent, AND copies posted to named agent's data room |
| Accruals report | Not typically posted | Posted to named agent's data room |
| Other notices | Standard distribution | Standard + named agent data room if required |

---

## 3. Communication Protocols

### With Borrower
- Direct communication may require named agent approval
- Some communications flow through the named agent
- Standard notices (DSN, rate set) may be sent by sub-agent on behalf of named agent, or named agent may forward

### With Lenders
- May flow through named agent or directly, per delegation agreement
- Data room access managed per named agent instructions

### With Named Agent
- Regular reporting per delegation agreement
- Accruals and DSN copies posted (not just emailed)
- Payment confirmations and reconciliation as required

---

## 4. Payment Process Differences

### Funds Flow
- Payment instructions may flow through named agent rather than directly from borrower
- Verify cash management arrangement per the Cash Management Agreement

### Funds Not Received
- Sub-agent contacts **named agent** (not borrower directly) when funds are not received on payment date

### Reconciliation
- Additional reconciliation reporting to named agent may be required beyond standard internal reconciliation

---

## 5. Sub-Agency Duties Matrix

The duties matrix defines exactly which functions are delegated. Two versions may exist: with pricing (includes fee schedule) and without pricing (duties only).

### Typically Delegated Functions
- Loan System maintenance (register, positions, rate resets)
- DSN generation and distribution
- Payment processing (receipt, allocation, distribution)
- Assignment processing
- Lender communications and data room management
- Financial reporting receipt and distribution
- Tax form collection and review

### Functions Typically Requiring Named Agent Approval
- Amendment/consent processing (named agent has authority under credit agreement)
- Direct borrower correspondence on non-routine matters
- Collateral actions (may be retained or delegated)
- Fee billing to borrower (may be billed through named agent)

Refer to the deal-specific addendum for the definitive scope on each deal.

---

## 6. Tickler Configuration for Sub-Agency Deals

Adjust standard timelines:

| Tickler | Standard | Sub-Agency |
|---------|----------|------------|
| DSN generation | 11+ BD | Per named agent (e.g., 13 BD) |
| Rate set | Align with DSN | Start earlier to support sub-agency DSN timeline |
| Accruals report | N/A | Align with DSN timing |
| Payment cycle | Standard | Shift forward per DSN requirements |

All other ticklers (billing, collateral, compliance) follow standard timelines unless the duties matrix specifies otherwise.

---

## 7. Fee Letter and Billing

- Fee Letter is typically an addendum to the Master Sub-Agency Agreement
- Billing may be to the named agent (not directly to borrower)
- Fee structure per the duties matrix pricing schedule
- Payment flow: borrower → named agent → sub-agent, OR borrower → sub-agent directly (per agreement)
- Follow-up for unpaid fees routes through the named agent relationship

---

## 8. Information Barriers

If the named agent is also a lender in the deal:
- Information barriers may be needed between the agent function and the lending function
- The sub-agent should be aware of what information can be shared and with whom
- Public-side vs private-side classification becomes even more critical
- Check the delegation agreement for confidentiality provisions
