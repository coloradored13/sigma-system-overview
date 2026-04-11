---
name: dlx-tickler-management
description: Use when the user asks about ticklers, creating a tickler in DLX, tickler types, tickler sub-types, recurring ticklers, resolving ticklers, tickler reminders, compliance reminders, deliverable tracking, IPD-aligned ticklers, tickler action date, trigger date, lead days, or any workflow involving tickler setup and management in the Oneiro DLX platform. Also trigger for questions about deferred ticklers, tickler statuses, or editing ticklers.
---

# DLX Tickler Management

## Overview

Ticklers are compliance and operational reminders in DLX — they track deliverables, recurring obligations, and time-sensitive actions. RM/RA create and manage ticklers; the system generates workflow tasks when triggered.

**Key principle:** Ticklers are the safety net for deadline-driven work. A missed tickler means a missed obligation.

---

## 1. Tickler Anatomy

| Field | Description |
|-------|-------------|
| **Action Date** | Date the action is due |
| **Lead Days** | Business days before Action Date to trigger |
| **Trigger Date** | Auto-calculated: Action Date - Lead Days |
| **Type** | Category (see §2) |
| **Sub-Type** | Specific classification within type |
| **Status** | Open, triggered, resolved, deferred, etc. |
| **Description** | What needs to happen |
| **Assigned To** | Responsible user(s) |
| **Deal/Facility** | Attachment level |

**Relationship:** Trigger Date = Action Date - Lead Days (in business days).

---

## 2. Tickler Type / Sub-Type Reference

| Type | Sub-Types (Examples) | Use |
|------|---------------------|-----|
| **Financial Reporting** | Annual/quarterly/monthly financials, compliance certificate | Borrower deliverable deadlines |
| **Billing** | Agency fee, ad hoc fee | Invoice generation triggers |
| **Collateral** | Semi-annual review, UCC continuation, insurance renewal | Collateral maintenance |
| **Account Review** | Annual account review | RM annual review |
| **Compliance** | KYC refresh, tax form expiration, sanctions re-screening | Regulatory renewals |
| **Payment** | Interest, principal, fee payment | Payment date reminders |
| **Assignment** | Pending follow-up | Open assignment tracking |
| **Deliverable** | Post-closing, borrower deliverable | Outstanding items |
| **Custom** | As needed | Deal-specific |

---

## 3. Creating a Tickler

1. Navigate to deal (or facility)
2. Select Create Tickler
3. Complete: Type/Sub-Type, Action Date, Lead Days, Description, Assigned To, Priority, Recurring settings
4. Verify Trigger Date calculates correctly
5. Save/Submit

**Best practices:**
- Generous Lead Days for items needing coordination (UCC continuations: 30+ days)
- Consistent descriptions for searchability
- Assign to the person who acts (not a shared inbox)
- Facility-level ticklers are more specific but don't show on deal dashboard

---

## 4. Recurring Ticklers

### Setup
- Enable recurring: frequency (monthly, quarterly, semi-annually, annually, custom)
- Recurrence pattern: specific day, nth business day, or IPD-aligned
- End date: deal maturity or open-ended

### IPD Alignment
- Ticklers trigger relative to each Interest Payment Date
- Lead Days calculated from each IPD
- Auto-adjust when IPD schedule changes

### How Recurrence Works
Resolving a recurring tickler auto-creates the next instance per schedule.

---

## 5. Resolving Ticklers

| Status | When to Use |
|--------|-------------|
| **Resolved** | Action fully completed |
| **Deferred** | Postponed (provide new target date + reason) |
| **Borrower Chased** | Deliverable requested, not yet received |
| **Awaiting Feedback** | Depends on third-party response |
| **On Hold** | Temporarily paused |

### Workflow
1. Navigate to triggered tickler
2. Select Resolve Tickler
3. Choose status, add notes, attach evidence
4. Submit → next instance auto-created if recurring

---

## 6. Editing Ticklers

Editable: Action Date, Lead Days, Type/Sub-Type, Description, Assigned To, Recurrence settings. Changes take effect immediately. Delete only for errors — use resolution statuses for completed/deferred items.

---

## 7. Reminder Configuration

| Type | When | Purpose |
|------|------|---------|
| Pre-Action Date | Configurable BD before | Advance warning |
| Post-Action Date | Configurable BD after | Escalation if not acted on |

---

## 8. Common Tickler Patterns

### New Deal Setup
- Financial reporting (quarterly + annual per credit agreement)
- Agency fee billing (per Fee Letter frequency)
- Annual account review (30 days from closing anniversary)
- Semi-annual collateral review
- Tax form expiration (per lender)
- UCC continuation reminders

### Payment Cycle (IPD-Aligned)
- DSN generation (11+ BD before payment; longer for sub-agency if required)
- Rate set reminder (2 BD before period start for Term SOFR)
- Wire approval reminder (payment date)

### Compliance
- KYC refresh (30 days before approval expiration)
- Insurance certificate renewal
- Sanctions re-screening
