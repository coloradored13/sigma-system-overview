---
name: loan-agency-deal-lifecycle
description: Use when the user asks about deal closing, deal onboarding, deal summaries, amendments, deal maintenance, deal termination, annual account review, successor agent transition, or any end-to-end deal lifecycle workflow in loan agency operations. Covers the RM-led workflow from business development handoff through closing, maintenance, and termination, including system setup handoffs to TT, CRM and system updates, secondary RM review requirements, and checklists. Also trigger for questions about Deal Summary creation, post-closing deliverables, amendment processing, payoff calculations, collateral release coordination at termination, or account termination checklists.
---

# Loan Agency Deal Lifecycle

## Overview

This skill covers the complete lifecycle of a loan agency deal from the RM's perspective: new deal closing, Deal Summary creation, TT handoff for system setup, ongoing maintenance (amendments), annual account review, deal termination, and successor agent transitions.

**Key principle:** The Deal Summary is the central operational artifact. TT relies on it for system setup. If the Deal Summary is wrong, everything downstream is wrong — rates, payments, notices, assignments.

**Lifecycle phases:** Closing → System Setup → Active Administration → Maintenance (Amendments) → Termination

---

## Critical Rules (Read First)

### 1. Deal Summary Timelines Are Hard Deadlines

- RM must draft Deal Summary within **10 business days** of closing
- Secondary RM review must be completed within **30 business days** of closing
- TT cannot properly set up the deal without a complete Deal Summary

### 2. Maker-Checker Applies to All System Changes

Every change in the Loan System follows maker-checker-approver:
- TT member #1 performs the action
- TT member #2 reviews
- RM approves

### 3. CRM Must Stay Current

The CRM system is the pipeline and status tracker. RM must update status at each phase transition (opportunity → mandate → closing → active → terminated). Business development-to-RM handoff happens at mandate stage.

### 4. Signature Authority Follows Policy

Document execution must follow the firm's signature authority policy. Non-standard provisions require escalation to senior leadership.

---

## 1. New Deal Closing

### Pre-Closing (RM Workflow)

1. **Business development hands off opportunity** → RM Manager assigns RM → RM opens CRM record
2. **KYC initiation:** RA fills KYC template → submits to compliance team → entered in KYC screening platform → link sent to borrower/parties. KYC approval valid **30 days** — if deal doesn't close in time, refresh required. See `loan-agency-kyc-process` skill.
3. **Credit agreement review:** RM reviews for agent-specific provisions:
   - Agent rights, protections, indemnification
   - Fee provisions
   - Amendment/consent mechanics and voting thresholds
   - Collateral provisions
   - Tax withholding and gross-up language
   - Sub-agency provisions (if applicable)
4. **Fee Letter negotiation:** RM drafts/negotiates Fee Letter documenting Agency Fees, Ad Hoc Fees, expense provisions. See `loan-agency-billing-invoicing` skill.
5. **Collateral Document review:** RM reviews security agreements, pledge agreements, mortgages, DACAs, UCC filings. See `loan-agency-collateral-management` skill.
6. **Deal Summary drafting:** Begin populating template with credit agreement terms.
7. **Task tracker ticket creation:** Create deal-level ticket for tracking all activities.

### Closing

1. **Execute documents** per signature authority policy — verify signer authority
2. **Save executed PDFs** to deal file
3. **Confirm fees received** — initial agency fee, any upfront fees per Fee Letter
4. **Update CRM** to active/closed-won status

### Post-Closing (10-30 Day Window)

| Deliverable | Deadline | Owner |
|-------------|----------|-------|
| Deal Summary (draft) | 10 BD after closing | RM |
| Secondary RM review of Deal Summary | 30 BD after closing | Second RM |
| Lender data room site creation | Post-closing | RA (from standard template) |
| Financial system customer setup | Post-closing | RA |
| Introductory emails to lender contacts | Post-closing | RM/RA |
| CRM record finalization | Post-closing | RM |

---

## 2. Deal Summary Creation

The Deal Summary is a spreadsheet containing **all information** TT needs for routine administration. It is the translation layer between the credit agreement and the Loan System.

### Creation Process

1. RM drafts using Deal Summary template + Deal Documents
2. Populate all applicable sections — mark N/A or delete rows for inapplicable sections
3. Include any additional TT-required info in appropriate sections
4. Sections typically cover: parties, facility terms (type, commitment, maturity, amortization), rate provisions (benchmark, margin, floor, day-count, interest periods), fee provisions, payment waterfall, collateral summary, consent/voting thresholds, key contacts, wire instructions, reporting requirements

### Secondary RM Review

- A different RM (not the drafter) reviews within 30 days
- Reviewer compares Deal Documents side-by-side against completed Deal Summary
- Any discrepancies flagged and corrected before TT relies on it
- Review evidenced in task tracker

### TT Handoff

Once Deal Summary is reviewed and approved, TT uses it to:
- Set up deal in Loan System (parties, facilities, rates, schedules)
- Create DSS (Debt Service Schedule)
- Create AC (Assignment Checklist)
- Solicit admin details and tax forms from lenders
- Set up lender data room site access

---

## 3. TT Deal Setup (System Onboarding)

After receiving the approved Deal Summary, TT performs system setup:

1. **Review Deal Summary** — flag any gaps or ambiguities back to RM
2. **Solicit administrative details + tax forms** from all lenders
3. **Tax form processing:** Save forms to review folder, add to tax form tracking spreadsheet. See `loan-agency-tax-form-review` skill.
4. **Lender setup in Loan System:** Enter lender details, admin contacts, wire instructions
5. **Callbacks:** Complete verbal callback to confirm wire instructions for every lender before first payment. See `loan-agency-payment-processing` skill.
6. **Lender data room site creation:** Create from standard template, add lender contacts with appropriate access levels. See `lender-data-room-management` skill.
7. **Create DSS** — reviewed and approved by RM
8. **Create Assignment Checklist (AC)** — reviewed by RM
9. **Deal setup in Loan System:** Enter deal structure, facilities, rates, schedules per Deal Summary
10. **Verification:** Second TT member reviews system setup against Deal Summary → RM final approval

For DLX-specific setup steps, see `dlx-deal-onboarding` skill.

---

## 4. Deal Maintenance (Amendments)

### Workflow

1. **Amendment notification received** — RM learns of proposed amendment from borrower, counsel, or named agent
2. **Task tracker ticket created** for amendment tracking
3. **Pre-closing review with External Counsel** — RM reviews amendment for:
   - Impact on agent provisions (indemnification, fees, scope, protections)
   - Correct voting threshold (Required Lenders >50%, Affected Lenders, or All Lenders for sacred rights)
   - Whether agent consent is required
   - Whether it impacts TT operations (rate changes, facility changes, maturity extensions, etc.)
4. **RM executes amendment** per signature authority (if agent signature required)
5. **Post-closing:**
   - Save executed amendment to deal file
   - Update Deal Summary with all changed provisions
   - Secondary RM review of Deal Summary updates
   - If amendment impacts TT operations: notify TT, provide updated Deal Summary sections
   - TT updates Loan System per maker-checker-RM approval chain

### Sacred Rights (All-Lender Consent Required)

These amendments cannot pass with Required Lenders alone:
- Rate reductions
- Maturity extensions
- Pro rata sharing modifications
- Payment priority / waterfall changes
- Release of all or substantially all collateral or guarantees

Agent must correctly identify the voting threshold. Getting this wrong is a significant liability risk.

### Sub-Agent Considerations

For sub-agent deals, amendments flow through the named agent. The sub-agent's role may be limited to system updates and notice distribution. Check the delegation agreement for scope.

---

## 5. Deal Termination

### Triggers

- Scheduled maturity (Loan System alerts)
- Voluntary prepayment of all outstanding amounts
- External party notification (borrower, named agent, counsel)

### Pre-Termination Workflow

1. **RM notifies RA and TT** of expected termination
2. **Account Termination Checklist** initiated (RM version and TT version)
3. **Payoff calculation:** TT calculates all outstanding amounts (principal, accrued interest, fees, expenses) → RM reviews and approves
4. **Document execution:** Payoff letter, release documents coordinated with External Counsel if needed
5. **Outstanding fees/expenses:** RM confirms all agency fees and expenses settled. Final billing processed.

### Termination Processing

1. **Final payment received and distributed** per `loan-agency-payment-processing` skill
2. **Collateral release:** RM coordinates release of all collateral documents and security interests. UCC terminations filed. Physical collateral returned. See `loan-agency-collateral-management` skill.
3. **Lender data room archival:** RA archives site per `lender-data-room-management` skill
4. **Bank account closure:** Close deal-specific accounts if any
5. **CRM update:** Status to terminated
6. **Loan System:** TT terminates deal in system
7. **Final billing:** Last invoice generated and sent

---

## 6. Annual Account Review

### Trigger and Timing

- Tickler-driven — fires annually within **30 days of closing anniversary**
- RM responsible; RA supports

### Review Checklist

1. **Deal Summary:** Current and accurate? Any amendments since last review reflected?
2. **Deal Documents:** All new documents (amendments, waivers, consents) saved to file?
3. **Secondary reviews:** All required secondary RM reviews completed?
4. **PDFs:** All executed documents saved as PDFs?
5. **TT notification:** TT informed of any updates since last review?
6. **Collateral Issues Log:** Review and follow up on any outstanding items
7. **Task tracker:** Review deal-level ticket for completeness — all tasks resolved or actively tracked?

### Collateral Issues Log Review

The Collateral Issues Log tracks known potential issues with Collateral Documents. During annual review:
- Review each open item
- Follow up with counsel or counterparties on resolution
- Update status
- Escalate items that have been open >12 months without progress

---

## 7. Successor Agent Transition

When the agent is replacing another agent (incoming) or being replaced (outgoing):

### Incoming Successor

1. **Successor Agent Checklist:** Obtain from outgoing agent:
   - Current lender positions and register
   - Accrued and unpaid interest/fees
   - All lender contacts and wire instructions
   - Complete set of Deal Documents and Collateral Documents
   - Outstanding items (pending assignments, borrowing requests, amendments)
2. **Reconciliation:** Verify positions and accruals against credit agreement and outgoing agent's records
3. **Parallel processing period:** May run parallel with outgoing agent during transition
4. **System setup:** Standard TT Deal Setup workflow (§3 above)
5. **Lender notification:** Distribute new agent contact details and wire instructions

### Outgoing Successor

- Reverse of above — provide all records, reconcile, coordinate transition date
- Account Termination Checklist applies

---

## 8. [UK] Variations

### Terminology
- Administrative Agent → **Facility Agent**
- Collateral Agent → **Security Trustee** (holds security on trust for secured parties)
- Assignment → **Novation** (extinguishes and recreates obligation under LMA)

### Documentation
- LMA documentation framework differs from LSTA
- Gross-up scope: Borrower takes **change-of-law risk** only (narrower than LSTA)
- DTTP scheme for qualifying lenders

### Operational Differences
- UK deals may require London + New York business day definitions
- Physical collateral stored at secure UK location (not US collateral custodian)
- GBP payment via **CHAPS**

---

## 9. Key Artifacts Reference

| Artifact | Owner | Purpose |
|----------|-------|---------|
| Deal Summary | RM (draft), RM #2 (review) | Central operational document — feeds TT system setup |
| Debt Service Schedule (DSS) | TT (create), RM (approve) | Visual accruals tracker (Loan System is system of record) |
| Assignment Checklist (AC) | TT (create), RM (review) | Conditions checklist for assignment processing |
| Collateral Spreadsheet | RM/RA | Tracks all collateral documents for a deal |
| Collateral Issues Log | RM/RA | Tracks known issues with collateral documents |
| Post-Closing Document Tracker | RM/RA | Tracks delivery of post-closing conditions |
| Assignment Tracker | TT | Centralized trade settlement tracking |
