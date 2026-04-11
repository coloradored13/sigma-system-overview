---
name: data-analysis
description: >
  Use this skill whenever the user works with datasets, databases, or quantitative
  analysis. Triggers include: 'SQL', 'query', 'data analysis', 'dashboard', 'chart',
  'visualization', 'data exploration', 'statistical analysis', 'data quality', 'CSV',
  'dataset', 'build a dashboard', 'write a query', 'data validation', 'hypothesis test',
  'correlation', 'regression', 'outlier detection', 'p-value', or requests to profile
  a dataset, build interactive dashboards, write SQL queries across any dialect
  (Snowflake, BigQuery, Postgres, Databricks), run statistical tests, create
  visualizations with Python (matplotlib, seaborn, plotly), or QA an analysis before
  sharing. Also trigger when the user uploads a CSV or dataset and asks questions about
  it. Do NOT use for general research without data (use research-analysis). Do NOT use
  for financial statements (use finance-accounting). Do NOT use for report summaries
  without underlying data work (use reporting).
---

# Data Analysis

Exploration, querying, visualization, statistical analysis, and validation of data.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick lookup — "what's the count of X", "write a query for Y" | **Quick** | Write the query or answer. No framework needed. |
| Standard analysis — "analyze this dataset", "build a chart", "explore this" | **Standard** | Apply routing table below. Profile before analyzing. Note assumptions. |
| Decision-grade analysis — informs hiring, budget, strategy, or goes to stakeholders. OR user says "I'm presenting this", "this needs to be right", "decision-grade" | **Rigorous** | Full analytical discipline below. |

### Rigorous Analysis Protocol

**1. Profile before analyzing.** Run data-exploration FIRST. Document: row count, column types, null rates, cardinality, date ranges, obvious anomalies. Never skip this.

**2. State assumptions explicitly.** Every analysis makes assumptions (what counts as an "active user", which date range, how nulls are handled). Write them down before presenting results.

**3. Validate before sharing.** Run the data-validation checklist (in `references/data-validation.md`):
- Source correct? Filters correct? Joins not inflating? Denominators right?
- Numbers in plausible range? Trends continuous? Cross-references match?
- Parts sum to whole?

**4. Sensitivity check on key findings.** For your most important conclusion: what happens if your main assumption is wrong? Change one input (date range, filter, definition) and see if the conclusion holds. If it flips, that's the thing to flag.

**5. Alternative interpretations.** For correlations and trends: name at least one alternative explanation. "Revenue went up because of the campaign" — or because of seasonality, or because pricing changed, or because of a data collection change.

**6. Explicit limitations.** State what the data CAN'T tell you. "This shows correlation but not causation." "This covers Q1-Q3 but Q4 may differ." "Sample size is 47 — treat patterns as directional, not definitive."

**7. Reproducibility.** Could someone else get the same results from your query/code? If not, document what's missing (environment, parameters, manual steps).

---

## Routing

| If the user wants to... | Read |
|---|---|
| Profile and explore a new dataset — shape, quality, patterns | `references/data-exploration.md` |
| Create charts and visualizations with Python | `references/data-visualization.md` |
| QA an analysis before sharing — methodology, accuracy, bias checks | `references/data-validation.md` |
| Build an interactive HTML dashboard with Chart.js and filters | `references/interactive-dashboard-builder.md` |
| Write SQL queries across any dialect | `references/sql-queries.md` |
| Run statistical tests — hypothesis testing, correlations, regression | `references/statistical-analysis.md` |
| Generate or improve a company-specific data analysis skill | `references/data-context-extractor.md` |

## Gotchas

- **Rigor should match stakes.** A quick row count doesn't need sensitivity analysis. An analysis going into a board deck does. If unsure: "Is someone making a decision based on this?"
- Always ask which SQL dialect before writing queries — Snowflake, BigQuery, Postgres, and Databricks differ significantly.
- Data exploration should happen before analysis — never skip profiling to jump to conclusions.
- Dashboard design starts with the decision the viewer needs to make, not the data available.
- Statistical claims require checking assumptions (normality, independence, sample size) before running tests.
- Correlation ≠ causation. Always note this when presenting correlation findings.
- Validate before sharing. The data validation checklist exists because smart people ship wrong analyses regularly.
- **"The data shows X" is incomplete without "given assumptions Y."** Every number is conditional on methodology choices. Make the conditions visible.
- **A chart without context is a Rorschach test.** If the viewer can reach the wrong conclusion from your visualization, it's not their fault — it's yours.

## Cross-Reference

For data validation as part of a broader review (e.g., auditing someone else's analysis, QA before a stakeholder presentation), the review-critique skill's standards-based mode provides the evaluation framework — explicit criteria, severity levels, what you checked vs. didn't. Data-analysis provides the validation checklist; review-critique provides the structured review process around it.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.

## Entity Resolution

When analyzing data involving company names, people, or products, resolve entities before querying. The same entity may appear under different names (abbreviations, former names, subsidiaries). Failure to resolve produces split counts, missed joins, and wrong conclusions. See research-analysis skill for the full protocol.
