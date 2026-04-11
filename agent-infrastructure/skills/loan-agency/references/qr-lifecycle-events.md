# Quick Reference: Lifecycle Events & Agent Administration

For full agent role analysis, restructuring mechanics, and regulatory details, see `Doc6_Lifecycle_Events_Agent_Administration_Revised.md`.

## Agent Roles

| Role | Core Responsibility | Key Risk |
|------|-------------------|----------|
| Administrative Agent | Payments, notices, amendments, KYC, register | Payment errors, missed notices |
| Collateral Agent | Hold liens, UCC filings, collateral release | Lien perfection failures |
| Escrow Agent | Hold funds, enforce release conditions | Premature/improper release |

**The AA is NOT a fiduciary** (most US credit agreements). Acts mechanically per the agreement. Protected by exculpation, indemnification, and reliance-on-documents provisions.

## Amendment Processing Workflow

| Step | Owner | Timeline |
|------|-------|----------|
| Receive amendment request from borrower/counsel | RM | Day 0 |
| Review provisions, identify voting threshold | RM | 1-2 BD |
| Draft consent solicitation | RM + counsel | 2-5 BD |
| Distribute to lender syndicate | RM/Agent | Day 5 |
| Consent period | Lenders | 10-15 BD typical |
| Tally votes, confirm threshold met | RM | At deadline |
| Execute amendment | RM + parties | 1-3 BD after |
| Update loan system (DLX) | TT | Same day |
| Distribute executed amendment | RM | Same day |

## Refinancing vs Repricing
| Feature | Refinancing | Repricing |
|---------|------------|-----------|
| What changes | New credit agreement or facility | Spread reduction on existing facility |
| Documentation | Full new docs or amendment & restatement | Amendment only |
| Call protection | Applies (101 if within soft-call period) | **101 if within soft-call period** |
| Lender choice | Extend or get repaid | Accept lower spread or get taken out |
| Agent work | Full new deal onboarding | Amendment processing + rate update |

## Default & Workout Essentials
- **Payment default** typically has a 1-3 BD grace period (or none for principal)
- **Cross-default** triggers when the borrower defaults on other debt above a threshold
- Agent's role: deliver default notice as directed by Required Lenders, NOT to independently determine default
- **Standstill agreements:** Agent should not agree without lender direction
- Agent may resign during workout — successor agent appointment follows credit agreement process

## UCC Filing Essentials
| Filing Type | Duration | Action Required |
|-------------|----------|----------------|
| Initial UCC-1 | 5 years | File at closing |
| Continuation (UCC-3) | Extends 5 years | File within 6 months before expiration |
| Amendment (UCC-3) | N/A | File for debtor name change, collateral change |
| Termination (UCC-3) | N/A | File at deal termination/collateral release |

**Missing a continuation filing = loss of perfected security interest.** This is one of the highest-risk agent errors.

## Compliance Certificate Processing
- Borrower delivers quarterly/annual financial statements + compliance certificate
- Agent reviews for completeness (NOT accuracy — agent is not auditing)
- Post to lender data room/portal
- Track delivery deadlines via tickler system
- Flag if late — may constitute covenant breach

## Deal Onboarding Checklist (Key Items)
1. KYC approval for all parties (borrower, guarantors, lenders)
2. Credit agreement review — agent provisions, fees, mechanics
3. Fee letter execution
4. Tax form collection from all lenders
5. Callback completion for all lenders
6. Deal Summary drafted (RM, within 10 BD of closing)
7. Secondary RM review (within 30 BD of closing)
8. DLX system setup (TT, from Deal Summary)
9. Lender data room setup
10. Tickler setup (financial reporting, insurance, UCC continuation)
11. Collateral documents recorded/filed
12. Notices sent (closing notice, initial funding notice)
