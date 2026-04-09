---
name: sigma-single
description: "Enhanced single-instance analysis for tasks below the sigma-review triage boundary. Uses Tetlock decomposition, reference class analysis, source tiers, dialectical self-challenge, and Toulmin warrants."
argument-hint: "[analysis question or task]"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Sigma Single — Enhanced Single-Instance Analysis

> For tasks that don't meet the sigma-review 3-condition triage boundary.
> Triage: stakes >=$1M/regulatory/12mo-strategy AND herding-risk AND calibration-matters → use /sigma-review instead.

You are conducting a structured single-instance analysis of: **$ARGUMENTS**

## Pre-flight
1→recall: "single-instance analysis task: $ARGUMENTS"
2→complexity check: does this meet sigma-review triage? (stakes AND herding-risk AND calibration-matters ALL required)
  if YES → recommend /sigma-review to user
  if NO → proceed with this template

## Analysis Protocol

### 1. Decompose (Tetlock)
Break the question into 3-7 independent sub-questions:
```
SQ[{N}]: {sub-question} |estimable: {yes/no} |method: {base-rate/analogue/data}
```

### 2. Reference Class
For each sub-question, identify the reference class:
```
RC[{question}]: reference-class={category} |base-rate={frequency} |sample-size={N} |src:{source:tier}
```

### 3. Analyze with Source Tiers
Research each sub-question. Tag all findings with source provenance AND quality tier:
- [independent-research:T1] — peer-reviewed, regulatory filing, official data
- [independent-research:T2] — preprint, industry report, corroborated company data
- [independent-research:T3] — company PR, blog, advocacy (flag if load-bearing)
- [agent-inference] — derived from reasoning across inputs

### 4. Dialectical Self-Challenge (Herzog & Hertwig)
For your top 2-3 findings, before finalizing:
```
DB[{finding}]:
  (1) initial: {your assessment}
  (2) assume-wrong: {what changes if this is wrong?}
  (3) strongest-counter: {best argument against your position}
  (4) re-estimate: {revised from opposite perspective}
  (5) reconciled: {final position integrating both}
```

### 5. Toulmin Warrant Structure
For each key conclusion, make the reasoning explicit:
```
CLAIM: {conclusion}
GROUNDS: {evidence supporting it}
WARRANT: {WHY the evidence supports the claim — the logical connection}
QUALIFIER: {confidence level and scope limitations}
REBUTTAL: {conditions under which this fails}
```

### 6. Calibrated Estimates
For key estimates, provide calibrated ranges:
```
CAL[{estimate}]: point={best} |80%=[{lo},{hi}] |90%=[{lower},{higher}] |assumptions:{what-must-be-true} |breaks-if:{condition}
```

### 7. Pre-Mortem
"3 years later, this failed. What happened?"
```
PM[{N}]: {failure-scenario} |probability:{%} |early-warning:{signal} |mitigation:{prevention}
```
Minimum 3 scenarios.

### 8. Outside-View Reconciliation
```
OV-RECONCILIATION: inside-view={your-analysis} |outside-view={base-rate-estimate} |gap={difference} |→ reconcile: {which is more trustworthy and why}
```

### 9. Analytical Hygiene Checks
Before finalizing, verify:
- §2a positioning: Who else recommends this? Is this already consensus?
- §2b calibration: Do your estimates match external sources? Divergence >15% must be justified.
- §2c cost: What does the recommendation cost? Is cost already elevated?
- §2e premise viability: What must be true? Is any required premise unverified?

Each check produces outcome 1 (changes analysis), 2 (confirms with risk), or 3 (reveals gap).

## Output
Present findings in plain language with:
- Key findings with source citations and quality tiers
- Calibrated estimates with ranges
- Counterarguments integrated (not in a separate section)
- Pre-mortem scenarios
- Explicit limitations and what you don't know
