---
name: dlx-deal-onboarding
description: Use when the user asks about setting up a new deal in DLX, creating parties in Oneiro, onboarding a facility, configuring pricing rules, fee builder setup, SSI (standard settlement instructions) configuration, repayment schedule setup, financial date rules, groups and permissions, roles and subscriptions, or any Oneiro DLX deal onboarding workflow. Covers the full party setup through facility configuration to deal approval sequence. Also trigger for questions about Cashless Deal vs Cashless Draw types, Conversion Deal flags for migrations, lender share setup, margin rules, PIK toggle, or multi-currency facility configuration in DLX.
---

# DLX Deal Onboarding

## Overview

This skill covers the end-to-end process of onboarding a new deal in the Oneiro DLX platform, from party creation through deal approval. It translates the Deal Summary (created by RM per `loan-agency-deal-lifecycle` skill) into the DLX system structure.

**Prerequisites:** Before starting in DLX, you need a completed and RM-approved Deal Summary. TT performs all DLX setup; RM reviews and approves the final configuration.

**DLX transaction hierarchy:** Deal → Facility → Loan → Interest Cycle. Everything in DLX is a "transaction" organized in a parent-child tree. See `dlx-api` skill for the full product hierarchy.

---

## Critical Gotchas (Read First)

### 1. Party Types Are Fixed Categories

DLX has exactly three party types. Using the wrong type breaks SSI rules and downstream workflows:

| Party Type | Maps To | SSI Requirement |
|------------|---------|-----------------|
| **Owner** | The agent entity | Must have BOTH interbank and non-interbank SSI |
| **Customer** | Borrower | Must have non-interbank SSI only |
| **Counterparty** | Lender, guarantor, legal counsel, other parties | Must have interbank SSI |

Getting SSI type wrong prevents payment processing.

### 2. Cashless Deal vs Cashless Draw — Choose Correctly

| Type | Meaning | When to Use |
|------|---------|-------------|
| **Cashless Deal** | No cashflows at all except agency fees | Deals where the agent has a collateral-only or similar non-cash role |
| **Cashless Draw** | Only drawdowns are cashless (interest/principal payments still flow) | Deals where initial funding happened outside the agent but ongoing servicing flows through |
| **Standard** | All cashflows process normally | Most deals |

### 3. Conversion Deal Flag Is Required for Migrations

When migrating a deal from another system into DLX, enable the **Conversion Deal** flag. This allows DLX to process facilities with expired availability dates.

### 4. Users Must Be Individuals

DLX Users (who log in, receive workflow tasks, approve activities) must be individual people — not shared/team email addresses. **Contacts** (who receive notices but don't log in) can use shared addresses.

### 5. Contract Name Can Be Changed Later

The first step asks for a Contract Name. This is a placeholder — it can be changed after submission.

---

## 1. Party Setup

Parties must exist in DLX before they can be assigned to a deal. Parties are global — once created, they're available across all deals.

### Creating a Party

**Fields:**
- **Name** — Short display name
- **Full Name** — Full legal name (as it appears in credit agreement)
- **Profile** — Description/notes
- **Self Onboard** toggle — If enabled, party can self-register users
- **Parent Party** — For fund families or corporate hierarchies
- **Logo** — Optional

All fields remain editable after creation.

### Setting Up SSIs (Standard Settlement Instructions)

Each SSI requires:
- **Currency** — which currency this SSI handles
- **Method** — ISO standard payment method
- **Use as Default** — whether this is the default SSI for this currency
- **Interbank Payment** toggle — CRITICAL: must match party type rules (see gotcha #1)

**Rules:**
- Counterparty (lender): Interbank = Yes
- Customer (borrower): Interbank = No
- Owner (agent): Must have both interbank AND non-interbank SSIs

### Users vs Contacts

| | Users | Contacts |
|---|-------|----------|
| Can log in to DLX | Yes | No |
| Receive workflow tasks | Yes | No |
| Receive notices/documents | Yes | Yes |
| Must be individual person | Yes | No (can be shared inbox) |
| Role assignment | Yes (via Roles/Subscriptions) | N/A |

---

## 2. Deal Onboarding Workflow (9 Steps)

### Step 1: Contract Name
- Enter contract name (can be placeholder) → Submit unlocks the full form

### Step 2: Contract Details
- **ISIN** — if applicable
- **Classification** — deal classification
- **Cashflow Type** — Cashless / Cashless Draw / Standard (see gotcha #2)
- **Lender Majority %** — voting threshold for Required Lenders (typically 50%+)
- **External ID** — reference number from external systems
- **Conversion Deal** — enable for deals migrating from another system (see gotcha #3)

### Step 3: Currencies and Commitments
- Set **Aggregate Deal Currency** (the reporting currency)
- Add commitment amounts per currency and per facility

### Step 4: Commitment FX Rates
- **Spot** — use market rate with configurable lag days
- **Fixed** — use a specific fixed rate

### Step 5: Dates and Calendars
- **Jurisdiction calendars** — determines business day definitions
- **IPD (Interest Payment Date) rules** — frequency and timing
- **Contract date** — closing/effective date
- **Expiry date** — final maturity

### Step 6: Add Parties
- **Servicing Agent** — select from Owner parties
- **Borrower** — select from Customer parties
- **Lenders** — select from Counterparty parties
- **Additional Parties** — guarantors, counsel, other parties as needed

### Step 7: Documents and Conditions
- Conditions Precedent and Subsequent
- Drawdown documents, repayment rules, pricing rules, fees, securities

### Step 8: Facility Setup
For each facility:
- **Facility name and type** — Revolving or Term
- **Primary currency and commitment amount**
- **Available date / Expiry date**
- **Schedule type** — amortization schedule
- **Maturity date**
- **Lender shares** — commitment amount, percentage, withholding tax rates
- **Facility borrowers**
- **Margin rules** — spread over benchmark, ratchet if applicable
- **PIK toggle** — if interest can be paid-in-kind
- **Applicable currencies** — for multi-currency facilities
- **Facility fees** — commitment fees, utilization fees, etc.

### Step 9: Submit → Review → Approve
- **Submit** — locks configuration for review
- **Review** — second TT member reviews against Deal Summary
- **Approve** — RM gives final approval; deal becomes active
- If issues found: reject back for amendment, then resubmit

---

## 3. Repayment Schedules

- **Bullet** — single payment at maturity
- **Amortizing** — periodic payments (TLA: 5-10% annual; TLB: ~1% annual)
- **Custom** — per credit agreement
- Revolver: no scheduled amortization

---

## 4. Pricing Rules

- **Benchmark** — Term SOFR, SONIA, EURIBOR, ABR, Daily Simple SOFR
- **Tenor** — 1M, 3M, 6M (must match permitted interest period elections)
- **Margin/Spread** — fixed or ratchet
- **Floor** — minimum benchmark rate (applies to benchmark only, not all-in rate)
- **Day-count convention** — Actual/360 (USD, EUR) or Actual/365 Fixed (GBP)
- **Default rate** — additional spread on overdue amounts (typically +200 bps)
- **PIK rate** — if applicable

---

## 5. Fee Builder

- **Agency fee** — per Fee Letter
- **Commitment fee** — on undrawn revolver amounts (typically 25-50 bps)
- **Utilization fee** — triggered at utilization thresholds
- **Letter of credit fees** — if LC sub-facility exists
- **Ticking fee** — on undrawn DDTL amounts
- Each fee: amount/rate, frequency, day-count, accrual basis, payment timing

---

## 6. Financial Date Rules

- **Anchor day** — day of month for recurring dates
- **Business day modifier** — Modified Following (standard)
- **Calendar** — which jurisdiction calendars apply
- **End-of-month convention** — handling months with different lengths

---

## 7. Groups, Permissions, Roles

- **Groups and Permissions** — control user access at deal level
- **Roles** — define functions (RM, TT, RA equivalents)
- **Subscriptions** — control notification delivery

---

## 8. Post-Onboarding Verification

| Check | Against |
|-------|---------|
| All facilities created with correct type | Deal Summary |
| Commitment amounts match | Deal Summary / credit agreement |
| Lender shares sum to 100% per facility | Deal Summary |
| Rate provisions correct | Deal Summary / credit agreement |
| Payment dates and schedules correct | Deal Summary |
| All parties assigned with correct roles | Deal Summary |
| SSIs entered for all lenders | Administrative Details Forms |
| Fee schedules configured | Fee Letter |

Second TT member reviews, then RM gives final sign-off.
