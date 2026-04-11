---
name: financial-close
description: >
  Use this skill for accounting execution — journal entries, reconciliations, financial
  statements, variance analysis, SOX testing, and month-end close management. Triggers
  include: 'journal entry', 'book this accrual', 'reconciliation', 'reconcile this
  account', 'prepare the income statement', 'balance sheet', 'cash flow statement',
  'variance analysis', 'month-end close', 'close checklist', 'SOX', 'SOX 404',
  'audit prep', 'trial balance', 'depreciation', 'amortization', or any request to
  execute accounting tasks. This is the execution complement to finance-accounting —
  finance-accounting provides domain knowledge, this skill provides the workflow steps.
  Do NOT use for general financial discussion or strategy (use finance-accounting).
  Do NOT use for financial data visualization (use visualize). Do NOT use for
  financial reporting narratives (use reporting).
---

# Financial Close

Execute accounting workflows — journal entries, reconciliations, financial statements,
variance analysis, and audit support. This is the execution layer for finance-accounting;
that skill provides the domain knowledge, this skill provides the workflow steps.

## Relationship to finance-accounting

These two skills compose rather than compete:
- **finance-accounting** = domain knowledge: GAAP/IFRS standards, accounting principles, when to apply what
- **financial-close** = execution: step-by-step workflows for close tasks, sequencing, documentation standards

When both trigger, finance-accounting provides the knowledge and financial-close provides
the process. For domain questions ("what's the GAAP treatment for X"), finance-accounting
handles it alone. For execution tasks ("book this accrual", "reconcile this account"),
financial-close leads and pulls domain knowledge from finance-accounting as needed.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick task — "book this accrual", "what's the JE for prepaid amortization" | **Quick** | Generate the entry with proper debits/credits. Cite the basis. |
| Standard close task — "reconcile this account", "prepare the income statement" | **Standard** | Apply the relevant workflow below. Full documentation. |
| Audit-grade — SOX testing, external audit prep, material accounts. OR user says "this is for audit", "SOX control" | **Rigorous** | Full documentation chain: entry → support → review → sign-off. Cite GAAP/IFRS standards. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Prepare journal entries — accruals, depreciation, payroll, revenue recognition | Load `finance-accounting` → reference `journal-entry-prep` |
| Reconcile accounts — GL to subledger, bank rec, intercompany | Load `finance-accounting` → reference `reconciliation` |
| Generate financial statements with GAAP presentation | Load `finance-accounting` → reference `financial-statements` |
| Analyze variances — budget vs. actual, period-over-period | Load `finance-accounting` → reference `variance-analysis` |
| SOX 404 testing — sample selection, control testing, deficiency classification | Load `finance-accounting` → reference `audit-support` |
| Manage the close calendar — task sequencing, dependencies, status | Load `finance-accounting` → reference `close-management` |
| Visualize financial data — waterfall charts, trend lines, dashboards | Hand off to `visualize` |
| Write the variance commentary or close memo | Hand off to `reporting` |
| Query financial data — GL extracts, trial balance pulls | Hand off to `query` |

## Workflow Phases

### Month-End Close Sequence
1. **Pre-close** (Days 1-2): Cut off transactions. Complete sub-ledger closes. Run preliminary trial balance.
2. **Journal entries** (Days 2-4): Book standard entries (depreciation, amortization, accruals). Book non-standard/adjusting entries.
3. **Reconciliation** (Days 3-5): Reconcile all balance sheet accounts. Clear reconciling items. Document open items.
4. **Financial statements** (Days 4-6): Generate P&L, balance sheet, cash flow. Run analytical review. Prepare flux analysis.
5. **Review & sign-off** (Days 5-7): Variance commentary. Management review. Close the books.

### Journal Entry Standards
- Every entry balances (debits = credits).
- Every entry has: date, preparer, approver, description, supporting documentation reference.
- Reversing entries are flagged as such.
- Entries over materiality threshold require additional approval.

## Gotchas

- **Debits and credits are non-negotiable.** Every entry must balance. If it doesn't, something is wrong — don't force it.
- Reconciliation is not "the numbers match." It's "I can explain every difference and none of them are errors."
- GAAP presentation matters. Revenue before expenses. Current before non-current. Operating before non-operating.
- **SOX samples are not random picks.** Sample selection methodology must be documented and defensible.
- Variance analysis without root causes is just arithmetic. "Revenue is down 12%" is not analysis. "Revenue is down 12% driven by a 15% volume decline in Enterprise, partially offset by 8% price improvement" is analysis.
- Close management is about dependencies, not just dates. Journal entries must post before reconciliation. Reconciliation must clear before statements.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The finance references cover US GAAP but not IFRS 16 lease accounting specifics."
2. **Search.** Authoritative sources. T1 (FASB/IASB codification, Big 4 guidance) > T2 (CPA journals) > T3 (blog posts).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
