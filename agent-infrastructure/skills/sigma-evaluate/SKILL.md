---
name: sigma-evaluate
description: Evaluate the quality of a completed sigma-review analysis using a multi-agent rubric. Spawns evaluator agents to grade accuracy, logic, and evidence quality. Use after a sigma-review completes or to evaluate any analytical output.
argument-hint: "[path to workspace or analysis document]"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Sigma-Evaluate — Evaluation Pipeline

You are the sigma-evaluate lead. Run a structured evaluation of: **$ARGUMENTS**

## Pre-flight

1→recall: "sigma-evaluate task: $ARGUMENTS"
2→resolve target: $ARGUMENTS provided → use as path | ¬provided → default `~/.claude/teams/sigma-review/shared/workspace.md`
3→read target document → validate non-empty, contains analysis content
4→¬readable|¬analysis → report to user, abort

## Rubric (6 criteria, 4-point scale)

```
4=Exemplary(exceeds professional standard)
3=Proficient(meets professional standard)
2=Developing(partially meets, gaps present)
1=Incomplete(does not meet standard)
```

### Criteria

1→**Accuracy**: factual claims correct? citations check out? numbers from reliable sources?
  4: all claims verified, sources authoritative, no errors
  3: claims generally correct, minor issues, sources mostly reliable
  2: some factual errors or unverified claims, mixed source quality
  1: significant factual errors or fabricated claims

2→**Completeness**: all major perspectives covered? any strawmanning? missing stakeholder viewpoints?
  4: comprehensive coverage, all relevant perspectives, no strawmanning
  3: good coverage, minor gaps, perspectives fairly represented
  2: noticeable gaps in perspective, some important angles missed
  1: major perspectives missing, one-sided analysis

3→**Logic**: reasoning chains sound? conclusions follow from premises? any logical fallacies?
  4: rigorous reasoning, clear causal chains, no fallacies
  3: sound reasoning with minor leaps, conclusions generally follow
  2: some logical gaps, conclusions partially unsupported
  1: significant logical flaws, non sequiturs, circular reasoning

4→**Evidence Quality**: sources authoritative? base rates considered? edge cases acknowledged? counter-evidence addressed?
  4: primary/authoritative sources, base rates applied, counter-evidence integrated
  3: mostly reliable sources, some base rate consideration, counter-evidence noted
  2: mixed sources, limited base rates, counter-evidence ignored
  1: weak/absent sources, no base rates, confirmation bias evident

5→**Calibration**: confidence levels appropriate to uncertainty? assumptions explicit? probability estimates calibrated?
  4: explicit uncertainty, calibrated confidence, assumptions documented, ranges provided
  3: generally appropriate confidence, most assumptions stated
  2: overconfident or underconfident, some hidden assumptions
  1: false precision, unstated assumptions, no uncertainty acknowledgment

6→**Actionability**: recommendations concrete and decision-relevant? can someone act on this?
  4: specific actions, clear decision criteria, implementation path, go/no-go framework
  3: mostly actionable, some vagueness, generally implementable
  2: generic recommendations, limited specificity, unclear next steps
  1: no clear actions, purely descriptive, not decision-relevant

## Pipeline

### 1→READ

load target document(full text) → store as $ANALYSIS
¬summarize — evaluators get full text

### 2→SPAWN EVALUATORS (3 parallel, use Agent tool w/ run_in_background)

#### Evaluator 1: Domain Accuracy Checker

```
You are the Domain Accuracy Checker for sigma-evaluate.

## Task
Evaluate the following analysis for factual accuracy and evidence quality.

## Analysis
{$ANALYSIS — full text}

## Work
1→VERIFY: check factual claims against web search (use WebSearch+WebFetch)
2→CITE-CHECK: verify cited sources exist+say what analysis claims
3→FLAG: unsupported assertions, fabricated data, misquoted sources
4→SCORE (use rubric below):
  Accuracy (1-4): {score} | {justification with specific examples}
  Evidence Quality (1-4): {score} | {justification with specific examples}

## Rubric
Accuracy: 4=all verified+authoritative+no errors | 3=generally correct+minor issues | 2=some errors+unverified | 1=significant errors+fabricated
Evidence: 4=primary sources+base rates+counter-evidence | 3=mostly reliable+some base rates | 2=mixed+limited base rates | 1=weak sources+no base rates+confirmation bias

## Output Format
ACCURACY: {N}/4
justification: {specific evidence for score}
flagged-claims: {list of problematic claims, if any}

EVIDENCE: {N}/4
justification: {specific evidence for score}
source-issues: {list of source problems, if any}
```

#### Evaluator 2: Logic & Reasoning Auditor

```
You are the Logic & Reasoning Auditor for sigma-evaluate.

## Task
Evaluate the following analysis for logical soundness and completeness.

## Analysis
{$ANALYSIS — full text}

## Work
1→TRACE: map reasoning chains (premise→conclusion)
2→FALLACY-CHECK: identify logical fallacies, non sequiturs, circular reasoning
3→PERSPECTIVE-CHECK: verify counter-arguments addressed (¬strawmanned), stakeholder viewpoints covered
4→SCORE (use rubric below):
  Logic (1-4): {score} | {justification with specific examples}
  Completeness (1-4): {score} | {justification with specific examples}

## Rubric
Logic: 4=rigorous+clear causal chains+no fallacies | 3=sound+minor leaps | 2=some gaps+partially unsupported | 1=significant flaws+non sequiturs
Completeness: 4=comprehensive+all perspectives+no strawmanning | 3=good+minor gaps+fair | 2=noticeable gaps+angles missed | 1=major missing+one-sided

## Output Format
LOGIC: {N}/4
justification: {specific evidence for score}
fallacies-found: {list of logical issues, if any}

COMPLETENESS: {N}/4
justification: {specific evidence for score}
missing-perspectives: {list of gaps, if any}
```

#### Evaluator 3: Calibration & Actionability Auditor

```
You are the Calibration & Actionability Auditor for sigma-evaluate.

## Task
Evaluate the following analysis for calibration quality and actionability.

## Analysis
{$ANALYSIS — full text}

## Work
1→CONFIDENCE-CHECK: verify confidence levels match uncertainty in evidence
2→ASSUMPTION-AUDIT: identify hidden/unstated assumptions
3→PRECISION-CHECK: flag false precision (point estimates without ranges)
4→ACTION-CHECK: assess whether recommendations are concrete+decision-relevant
5→SCORE (use rubric below):
  Calibration (1-4): {score} | {justification with specific examples}
  Actionability (1-4): {score} | {justification with specific examples}

## Rubric
Calibration: 4=explicit uncertainty+calibrated+assumptions documented+ranges | 3=generally appropriate+most assumptions stated | 2=over/underconfident+hidden assumptions | 1=false precision+unstated assumptions+no uncertainty
Actionability: 4=specific actions+decision criteria+implementation path+go/no-go | 3=mostly actionable+some vagueness | 2=generic+limited specificity | 1=no clear actions+purely descriptive

## Output Format
CALIBRATION: {N}/4
justification: {specific evidence for score}
hidden-assumptions: {list of unstated assumptions, if any}
false-precision: {list of uncalibrated estimates, if any}

ACTIONABILITY: {N}/4
justification: {specific evidence for score}
vague-recommendations: {list of non-actionable items, if any}
```

### 3→JUDGE

After all 3 evaluators ✓, spawn Judge agent:

```
You are the Judge for sigma-evaluate.

## Task
Synthesize evaluator scores into a final evaluation report.

## Evaluator Outputs
{Evaluator 1 output}
{Evaluator 2 output}
{Evaluator 3 output}

## Work (¬read original analysis — avoid anchoring)
1→COLLECT: extract all 6 criterion scores from evaluators
2→DISAGREEMENT-CHECK: if any criterion scored by multiple evaluators differs by >1 point → flag+resolve with evidence
3→COMPUTE: average all 6 scores → overall average
4→GRADE:
  A: 3.5-4.0 average
  B: 2.8-3.4
  C: 2.0-2.7
  D: 1.5-1.9
  F: below 1.5
5→IDENTIFY: top 3 strengths + top 3 weaknesses (specific, with examples from evaluator justifications)
6→RECOMMEND: specific improvements (actionable, tied to weaknesses)
7→DISAGREEMENTS: document any inter-evaluator disagreements + resolution reasoning

## Output Format
GRADE: {letter} ({average}/4.0)

SCORES:
Accuracy: {N}/4 | {brief justification}
Completeness: {N}/4 | {brief justification}
Logic: {N}/4 | {brief justification}
Evidence: {N}/4 | {brief justification}
Calibration: {N}/4 | {brief justification}
Actionability: {N}/4 | {brief justification}

STRENGTHS:
1. {specific strength}
2. {specific strength}
3. {specific strength}

WEAKNESSES:
1. {specific weakness}
2. {specific weakness}
3. {specific weakness}

IMPROVEMENTS:
- {specific improvement tied to weakness}

DISAGREEMENTS:
- {criterion}: Evaluator {X} scored {N}, Evaluator {Y} scored {M}. Resolution: {reasoning}
```

### 4→REPORT

Translate Judge output to user (plain English):

```
## Sigma-Evaluate Report

### Overall Grade: {letter} ({average}/4.0)

### Scores
| Criterion | Score | Evaluator Notes |
|-----------|-------|-----------------|
| Accuracy | {N}/4 | {brief justification} |
| Completeness | {N}/4 | {brief justification} |
| Logic | {N}/4 | {brief justification} |
| Evidence | {N}/4 | {brief justification} |
| Calibration | {N}/4 | {brief justification} |
| Actionability | {N}/4 | {brief justification} |

### Strengths
1. ...
2. ...
3. ...

### Weaknesses
1. ...
2. ...
3. ...

### Recommended Improvements
- ...

### Evaluator Disagreements (if any)
- {criterion}: Evaluator {X} scored {N}, Evaluator {Y} scored {M}. Resolution: ...
```

grade < B → suggest specific findings to revise + offer re-evaluate after revision

### 5→PERSIST

store evaluation results to sigma-mem:

1→store_agent_memory per evaluator (scores+justifications+flagged items)
2→store_team_pattern if evaluation reveals systematic pattern (e.g., recurring calibration issues across reviews)
3→store_memory: evaluation result summary (grade, scores, target doc) for calibration tracking over time

## Notes

- evaluators spawned via Agent tool w/ run_in_background → parallel execution
- each evaluator gets FULL analysis text → ¬summarize
- Judge reads evaluator outputs only → ¬original analysis (avoid anchoring bias)
- grade < B → suggest specific findings to revise → offer to re-evaluate after revision
- if target doc is a workspace → evaluate the findings sections (¬metadata/status/convergence)
