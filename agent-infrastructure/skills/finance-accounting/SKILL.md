---
name: finance-accounting
description: >
  Use this skill whenever the user asks about accounting, financial reporting,
  or audit workflows requiring domain-specific knowledge. Triggers include:
  'income statement', 'balance sheet', 'cash flow statement', 'journal entry',
  'reconciliation', 'variance analysis', 'SOX', 'SOX 404', 'audit', 'month-end
  close', 'GAAP', 'IFRS', 'financial statements', 'debits and credits',
  'accruals', 'trial balance', 'general ledger', or requests to prepare journal
  entries, reconcile accounts, analyze financial variances, prepare financial
  statements with GAAP presentation, support SOX compliance, or manage month-end
  close. Requires accounting-specific knowledge (double-entry mechanics, GAAP
  presentation standards, audit documentation). Do NOT use for product metrics
  or business KPIs (use data-analysis or reporting). Do NOT use for financial
  modeling or forecasting (use planning-prioritization). Do NOT use for loan
  administration finance (use loan-agency).
---

# Finance & Accounting

Accounting operations, financial reporting, and audit workflows requiring GAAP/IFRS domain knowledge.

## Routing

| If the user wants to... | Read |
|---|---|
| Prepare income statements, balance sheets, or cash flow statements | `references/financial-statements.md` |
| Prepare journal entries with proper debits, credits, and documentation | `references/journal-entry-prep.md` |
| Reconcile accounts — GL to subledger, bank, or third-party data | `references/reconciliation.md` |
| Analyze financial variances — volume, rate/price, mix decomposition | `references/variance-analysis.md` |
| Support SOX 404 compliance — control testing, sample selection, documentation | `references/audit-support.md` |
| Manage month-end close — task sequencing, dependencies, status tracking | `references/close-management.md` |

## Gotchas

- Always confirm accounting standard (GAAP vs IFRS) and jurisdiction before preparing statements.
- Journal entries must balance — verify debits equal credits before presenting.
- Variance analysis should decompose into volume, rate/price, and mix components where applicable.
- SOX testing requires documented sample selection methodology — random must be truly random.
- Reconciliation differences should be investigated, not just noted. Timing ≠ error ≠ fraud — but all require documentation.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
