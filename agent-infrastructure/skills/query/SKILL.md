---
name: query
description: >
  Use this skill when the user wants to write SQL, explore a dataset hands-on,
  profile tables, or run statistical tests. Triggers include: 'write a query',
  'SQL', 'explore this dataset', 'profile this table', 'what does this data look
  like', 'validate this analysis', 'is this data clean', 'run a statistical test',
  'hypothesis test', 'correlation', 'regression', 'p-value', 'Snowflake', 'BigQuery',
  'Postgres', 'Databricks', 'CSV analysis', or requests to interact with data
  directly. Complements data-analysis: that skill provides analytical frameworks
  and rigor protocols; this skill provides hands-on execution. Do NOT use for
  building charts or dashboards (use visualize). Do NOT use for written summaries
  of findings (use reporting). Do NOT use for financial statement preparation
  (use financial-close).
---

# Query

Get answers from data. Write SQL, explore datasets, profile tables, validate
analyses, and run statistical tests. This is the hands-on execution complement
to data-analysis — that skill provides the analytical framework and rigor
protocols; this skill is where you touch the data.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick lookup — "count of X", "show me Y" | **Quick** | Write the query. Return the answer. No ceremony. |
| Standard query work — "explore this", "write me a query for", "analyze this CSV" | **Standard** | Profile first. State dialect. Note assumptions. |
| Decision-grade — results inform strategy, go to stakeholders, or drive spend. OR user says "this needs to be right" | **Rigorous** | Full data-analysis rigorous protocol: profile → assumptions → validate → sensitivity → limitations → reproducibility. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Profile a new dataset — shape, quality, nulls, distributions | Load `data-analysis` → reference `data-exploration` |
| Write SQL across any dialect (Snowflake, BigQuery, Postgres, Databricks) | Load `data-analysis` → reference `sql-queries` |
| Run statistical tests — hypothesis testing, correlations, outlier detection | Load `data-analysis` → reference `statistical-analysis` |
| Validate an analysis before sharing — QA, methodology, bias | Load `data-analysis` → reference `data-validation` |
| Generate a company-specific data context for better future queries | Load `data-analysis` → reference `data-context-extractor` |
| Query financial data — GL, trial balance, reconciliation | Load `finance-accounting` for domain context + `data-analysis` for query mechanics |
| Visualize query results as charts or dashboards | Hand off to `visualize` |

## Workflow

1. **Confirm dialect.** Always ask which SQL dialect before writing. Snowflake, BigQuery, Postgres, and Databricks differ on window functions, date handling, CTEs, and type casting.
2. **Profile before querying.** For new datasets: row count, column types, null rates, cardinality, date ranges. Never skip this.
3. **State the grain.** "One row per what?" is the most important question. Get this wrong and every aggregate is wrong.
4. **Check joins.** Joins are where analyses break. Verify: Is it 1:1, 1:many, or many:many? Are you inflating rows? Are you dropping unmatched records?
5. **Validate results.** Do the numbers make sense? Do parts sum to the whole? Are trends continuous? Cross-reference against known benchmarks.

## Gotchas

- **Ask dialect first.** Writing Snowflake SQL for a Postgres database wastes everyone's time.
- Entity resolution matters. "Acme Corp", "ACME", and "Acme Corporation" are the same company — or are they? See `research-analysis` for the full entity resolution protocol.
- Null handling is a methodology choice, not a technical detail. Document how nulls are treated.
- **CTEs over subqueries.** They're easier to read, debug, and modify. Use them by default.
- Window functions are powerful but easy to get wrong. Always verify the partition and order clauses produce what you expect.
- **Sample size matters for statistical tests.** n=47 is directional, not definitive. Say so.

## Relationship to data-analysis

`data-analysis` is the parent skill — it owns the analytical framework, rigor protocols, and reference files. This skill is the execution entry point for users who want to *do* data work rather than *think about* data work. When rigor escalates, this skill defers to `data-analysis` protocols. When the user just needs a query written, this skill handles it directly without loading the full analytical framework.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The SQL references cover analytical queries but not stored procedures in this dialect."
2. **Search.** Find authoritative sources. Apply tiers: T1 (official docs) > T2 (Stack Overflow accepted answers) > T3 (blog posts).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
