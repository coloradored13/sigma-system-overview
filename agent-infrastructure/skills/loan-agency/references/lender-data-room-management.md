---
name: lender-data-room-management
description: Use when the user asks about lender data rooms, agency sites, document posting, lender notifications, public-side or private-side classification, MNPI (material non-public information), data room site creation, site closure, site archival, adding or removing lender access, broadcast notifications, document notifications, or any workflow involving lender document distribution platforms in loan agency operations.
---

# Lender Data Room Management

## Overview

The lender data room is the platform for distributing deal documents and notices to lenders. Each deal has its own site created from a standard template. RA manages the platform day-to-day; RM oversees content classification.

**Key principle:** Every document posted must be correctly classified as public-side or private-side. Misclassification is an MNPI compliance violation.

---

## Critical Rules (Read First)

### 1. Public-Side vs Private-Side Classification

| Classification | Definition | Who Can Access |
|---------------|------------|---------------|
| **Public-side** | Information available to all market participants. No trading restrictions. | All lenders |
| **Private-side** | Material Non-Public Information (MNPI). Receipt restricts trading. | Only lenders who have wall-crossed |

**When in doubt, classify as private-side.** Upgrading later is simple; downgrading after MNPI exposure is a compliance crisis.

Common classifications:
- Credit agreement, amendments, notices → typically **public-side**
- Financial statements, compliance certificates → typically **private-side**
- Borrowing base certificates → **private-side**
- Draft documents, working materials → **private-side**
- Fee letters → **private-side**

### 2. Site Creation Uses Standard Template

Every new deal site must be created from the standard agent template. Do not create from scratch.

---

## 1. Site Creation

### When: During post-closing (part of TT deal setup)

### Process
1. Create from standard template
2. Configure: deal name, description, active dates
3. Set up folder structure (template provides defaults): Deal Documents, Notices, Financial Reporting, Collateral, Correspondence, Administrative
4. Configure access levels: internal (full access), lender (per deal requirements, public/private controls)
5. Add lender contacts from Administrative Details Forms

---

## 2. Document Posting

1. Receive document for posting
2. **Classify: public-side or private-side** (RM determines if unclear)
3. Upload to correct folder with classification flag
4. Name clearly (include date and document type)
5. Select notification type
6. Post

---

## 3. Notification Types

### Document Notifications
- Triggered on document posting
- Email with document name and link
- Use for: credit agreements, amendments, notices, financial deliverables

### Broadcast Notifications
- Manual notification without specific document
- Use for: general announcements, reminders, action items

Respect public/private boundaries — private notifications only to private-side users.

---

## 4. User Management

### Adding (New Lender)
1. Create account with lender's contacts
2. Assign access: public-side only (default) or public + private-side (wall-crossed)
3. Send welcome notification

### Removing (Lender Exits)
1. Confirm zero position in register
2. Disable access (do not delete — audit trail)

### Modifying
- Public → private-side: lender acknowledges MNPI receipt and trading restrictions
- Private → public: generally not done (once private, always private for that deal)

---

## 5. Site Archival and Closure

1. Confirm deal fully terminated
2. Verify all documents posted
3. Set to read-only/archived
4. Notify users
5. Retain per records retention policy (minimum 10 years for OFAC/tax)
6. Close when retention period expires

---

## 6. Sub-Agency Data Room Requirements

Sub-agency deals may have additional posting obligations:
- Accruals reports posted to named agent's data room
- Consolidated DSN copies per deal
- Check sub-agency duties matrix for deal-specific requirements
