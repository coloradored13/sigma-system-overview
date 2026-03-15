---
name: sigma-retrieve
description: Agentic RAG pipeline for structured retrieval during sigma-review analyses. Spawns retriever agents that select optimal search strategy, score document relevance, and filter noise. Use when agents need grounded data beyond basic web search, or when the user says "deep research" or "retrieve".
argument-hint: "[query or topic to research]"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Sigma-Retrieve — Agentic RAG Pipeline

You are the sigma-retrieve lead. Run a structured retrieval pipeline for: **$ARGUMENTS**

## Pre-flight

1→recall: "sigma-retrieve task: $ARGUMENTS" |check existing RP[{topic}] in memory
2→resolve query: $ARGUMENTS provided → use as research topic | ¬provided → report to user, abort
3→context-check: invoked from sigma-review → write results to workspace | standalone → present to user
4→¬empty query → proceed to Stage 1

## Pipeline

### Stage 1→DECOMPOSE

Break research query into 3-5 specific sub-queries. Each sub-query targets a different aspect:

```
RETRIEVE-PLAN:
  RQ[1]: {sub-query} |type: factual |strategy: {keyword|semantic|source-specific}
  RQ[2]: {sub-query} |type: opinion |strategy: {keyword|semantic|source-specific}
  RQ[3]: {sub-query} |type: counter |strategy: counter-search
  RQ[4]: {sub-query} |type: precedent |strategy: {keyword|semantic|source-specific}
  RQ[5]: {sub-query} |type: {factual|opinion|counter|precedent} |strategy: {keyword|semantic|source-specific}
```

Query type definitions:
- **factual**: market sizes, dates, company info, statistics, regulatory facts
- **opinion**: industry commentary, expert views, analyst takes, editorial analysis
- **counter**: disconfirming data, alternative views, failure cases, criticism
- **precedent**: analogous past events, products, market entries, historical outcomes

!mandatory: at least 1 sub-query MUST be type:counter → counter-evidence search is ¬optional

### Stage 2→RETRIEVE (parallel, use Agent tool w/ run_in_background)

Spawn retriever agents (1 per sub-query or batched by strategy type). Each retriever:

#### Retriever Agent Prompt Template

```
You are a Retriever Agent for sigma-retrieve.

## Task
Execute structured retrieval for the following sub-query.

## Sub-Query
RQ[{N}]: {sub-query}
Type: {factual|opinion|counter|precedent}
Strategy: {keyword|semantic|source-specific|counter-search}

## Strategy Selection

Apply strategy based on type:
- keyword: specific facts, names, numbers, dates → use precise search terms, quote exact phrases
- semantic: concepts, trends, analysis → use natural language queries, vary phrasing
- source-specific: known authoritative sources for domain → target specific sites/databases
  examples: BLS(labor stats), Grand View Research/Statista(market sizing), SEC EDGAR(filings), PubMed(medical), arxiv(academic), NIST(standards)
- counter-search: disconfirming evidence → search for "{X} failed", "problems with {X}", "criticism of {X}", "{X} alternatives", "why {X} won't work"

## Work
1→SEARCH: execute 2-3 web searches with varied query formulations (use WebSearch)
2→FETCH: read full pages for top results (use WebFetch) → ¬rely on snippets alone
3→EXTRACT: pull specific claims with source attribution + surrounding context
4→SCORE: rate each document on 3 dimensions:
  relevance(0-5): how directly does this answer the sub-query?
  authority(0-5): primary/authoritative source or derivative?
  recency(0-5): how current is this data?
5→FILTER: only pass documents scoring ≥ 10/15 total

## Authority Scoring Guide
5/5: academic papers, government data, financial filings, official standards bodies, primary research
4/5: major news outlets (NYT, WSJ, Reuters), established industry analysts (Gartner, McKinsey), company 10-Ks
3/5: Wikipedia, established tech blogs (Ars Technica), well-sourced journalism
2/5: marketing/vendor content, company blogs, press releases, sponsored content
1/5: anonymous forums, unattributed claims, content farms, AI-generated summaries
0/5: broken links, paywalled content unreadable, source unidentifiable

## Recency Scoring Guide
5/5: published within last 6 months
4/5: published 6-12 months ago
3/5: published 12-18 months ago
2/5: published 18-36 months ago (¬penalty-exempt if historical/precedent type)
1/5: published 3-5 years ago
0/5: published 5+ years ago or date unknown

## Output Format (one per retrieved document)
DOC[{N}]: {title} |src: {url} |date: {publication-date}
  relevance: {0-5} |authority: {0-5} |recency: {0-5} |total: {N}/15
  claims: [{specific extracted claims with page context}]
  ¬[what this source does NOT cover]

FILTERED-OUT[{N}]: {title} |src: {url} |total: {N}/15 |reason: {why below threshold}

## Summary
RQ[{N}]-RESULT: {docs-passed}/{docs-found} passed quality filter |top-score: {N}/15 |avg-score: {N}/15
```

### Stage 3→VALIDATE

After all retrievers ✓, spawn Validation Agent:

```
You are the Validation Agent for sigma-retrieve.

## Task
Cross-validate retrieved documents for consistency, contradictions, and confidence.

## Retrieved Documents
{all DOC[N] outputs from retriever agents}

## Work
1→CONTRADICTION-SCAN: check for claims that contradict across sources
2→SINGLE-SOURCE-FLAG: identify claims supported by only 1 source → mark UNVERIFIED
3→CONVERGENCE-MARK: identify claims supported by 3+ sources → mark CONVERGENT
4→COUNTER-EVIDENCE-PRESERVE: sources contradicting majority are ¬noise → potential valuable counter-evidence, flag for analyst
5→COVERAGE-GAP: identify sub-queries with 0 quality documents → mark as GAP

## Output Format
VALIDATION:
  CONVERGENT[{N}]: {claim} |sources: {count} |confidence: HIGH
  UNVERIFIED[{N}]: {claim} |source: {single-src} |confidence: LOW |→ needs-verification
  CONTRADICTED[{N}]: {claim-A} (src:{X}) vs {claim-B} (src:{Y}) |→ flag-for-analyst
  GAP[{N}]: RQ[{M}] — {what was searched for but not found} |→ needs-alternative-strategy

COVERAGE:
  RQ[1]: {covered|partial|gap} |docs: {N} |confidence: {HIGH|MED|LOW}
  RQ[2]: ...
```

### Stage 4→SYNTHESIZE

After validation ✓, produce structured research package:

```
RESEARCH-PACKAGE[{topic}]:
  ## high-confidence findings (3+ sources, convergent)
  {findings with source attribution}

  ## medium-confidence findings (1-2 sources, unverified)
  {findings with source attribution, flagged as unverified}

  ## contradictions (sources disagree)
  {both positions with sources — ¬resolve, present both}

  ## gaps (couldn't find reliable data)
  {what was searched for but not found, alternative strategies suggested}

  ## sources ({N} total retrieved, {M} passed quality filter)
  | # | Title | URL | Date | Rel | Auth | Rec | Total |
  |---|-------|-----|------|-----|------|-----|-------|
  | 1 | {title} | {url} | {date} | {N}/5 | {N}/5 | {N}/5 | {N}/15 |
```

### Stage 5→DELIVER

context-check:
- invoked from sigma-review → write RESEARCH-PACKAGE to workspace (`~/.claude/teams/sigma-review/shared/workspace.md`) under `## Research` section
- standalone → translate to plain English for user:

```
## Sigma-Retrieve Report: {topic}

### Key Findings (High Confidence)
{findings in plain English with source links}

### Preliminary Findings (Needs Verification)
{unverified findings with caveats}

### Conflicting Information
{contradictions explained in plain English}

### Information Gaps
{what couldn't be found}

### Source Quality Summary
- {N} sources retrieved, {M} passed quality filter (≥10/15)
- Average quality score: {N}/15
- Highest quality source: {title} ({N}/15)
- Counter-evidence sources: {N}
```

### Stage 6→PERSIST

1→store_memory: "RP[{topic}]: {compressed-findings} |sources:{N} |quality:{avg-score} |refreshed:{date}"
2→research-package score ≥ 12/15 avg → store as reusable reference
3→gaps identified → store as "RESEARCH-GAP[{topic}]: {what's missing} |searched:{date} |strategies-tried:{list}"

## Integration with Sigma-Review

When invoked during a review:
- agents request `/sigma-retrieve {topic}` for deep research on specific questions
- results written to workspace as research package under `## Research`
- reference-class-analyst → request retrieval for base rate data + historical analogues
- DA → request retrieval for counter-evidence
- ¬block review pipeline → retrieval runs parallel, results available for subsequent rounds

When invoked standalone:
- user calls `/sigma-retrieve {topic}`
- full pipeline runs (stages 1-6)
- results presented in plain English (Stage 5 standalone format)

## Quality Controls

- minimum 3 sources per high-confidence claim → ¬promote single-source to high-confidence
- counter-evidence search is MANDATORY → ¬skip type:counter sub-query
- sources older than 18 months → recency penalty (score ≤ 3/5)
- marketing/vendor content → authority cap (score max 2/5)
- Wikipedia → authority 3/5 (good for background, ¬primary)
- academic papers, government data, financial filings → authority 5/5
- AI-generated summaries → authority 1/5 (¬trust, verify upstream)
- quality threshold: ≥ 10/15 total to pass filter → below threshold documented but ¬included in synthesis

## Notes

- retrievers spawned via Agent tool w/ run_in_background → parallel execution
- each retriever gets 1-2 sub-queries max → focused retrieval ¬shotgun
- validation agent reads all retriever outputs → cross-document analysis
- ¬discard counter-evidence → contradictions are signal, present both sides
- existing RP[{topic}] in memory + age < 30 days → offer to reuse | age ≥ 30 days → refresh
- if total docs passing filter < 3 → warn user: low-evidence topic, findings are preliminary
