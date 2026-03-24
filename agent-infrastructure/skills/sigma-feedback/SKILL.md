---
name: sigma-feedback
description: Post-review calibration loop. Routes user corrections through datum track (pushback-once→accept) for factual fixes or concept track (DA-tested mini-review) for structural corrections. Run after reading sigma-review synthesis.
argument-hint: "[correction] or blank for interactive"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch, SendMessage
---

# Sigma Feedback — Post-Review Calibration

> Post-delivery correction loop. User provides ground truth after reading synthesis.
> Two tracks: datum (verify-once) | concept (adversarial mini-review)
> Corrections update agent calibration + amend archived workspace.
> Protocol reference: directives.md §9

You are the sigma-feedback lead. Process user correction(s) for: **$ARGUMENTS**

## Pre-flight

1→recall: "sigma-feedback task: $ARGUMENTS"
2→locate workspace:
  $ARGUMENTS contains path → use as workspace
  ¬path → scan `~/.claude/teams/sigma-review/shared/archive/` → present most recent to user
  ¬archive → check `~/.claude/teams/sigma-review/shared/workspace.md` (active/just-completed)
  ¬any → ask user for workspace path
3→read workspace → extract: ## task, ## findings, ## convergence, ## prompt-decomposition
4→identify agents from workspace findings sections
5→if $ARGUMENTS contains correction → proceed to classification
  ¬correction in args → ask user: "What needs correcting? Reference the specific finding if possible."

## Classification

Classify each correction into exactly one track:

**datum** — verifiable factual fix
  signals: specific number|date|name|fact, binary right/wrong, source-checkable
  examples: "revenue is 6B not 6M" | "CEO is Smith not Jones" | "deadline is March not April" | "3 subsidiaries not 5"

**concept** — structural/interpretive correction
  signals: how-something-works|why-something-happens|framework|mechanism|model, multiple valid framings possible
  examples: "waterfall payments work differently" | "regulatory framework is actually X" | "competitive dynamics are wrong because..."

1→classify each correction: `CLASSIFY[{N}]: {correction-summary} → datum|concept |signal: {why}`
2→present classification to user → confirm|override
3→mixed ("the number is wrong AND the framework is wrong") → split into separate corrections, one per track
4→process order: all datums first (fast), then concepts (slower)
  rationale: datum corrections may provide updated facts that inform concept review

## Track 1: Datum (pushback-once → accept)

!purpose: prevent casual/wrong corrections from degrading calibration | once confirmed, accept immediately ¬second-guess

### 1→Identify
- which finding: `F[{agent}:{finding-ref}]`
- current value: what the review says + source it cited
- proposed value: what the user says it should be

### 2→Pushback (exactly once — ¬interrogation, ¬rubber-stamp)
Present to user (plain English):
```
The review has [{current-value}], sourced from [{source-description}].
You're correcting to [{proposed-value}].

{one of — lead selects most appropriate:}
a) Source says [{current-value}] — was the source wrong, or is there a different/better source?
b) I can't verify [{source}] right now — where does [{proposed-value}] come from?
c) [{source}] actually says [{what-it-says}] — the review may have misread it. [if lead can check inline]
```
!rule: pushback MUST reference the original source ¬just restate the finding
!rule: if lead can verify the correction inline (public data, file in codebase) → verify before pushback
  verified-correct → skip pushback: "Verified: [{proposed-value}] correct per [{source}]. Accepting."
  verified-wrong → "Checked [{source}]: confirms [{current-value}]. Still want to correct?"

### 3→Accept (after user confirms)
!rule: ¬second pushback. user confirmed → accept + update. done.

### 4→Cascade Check
Does changing this datum affect other findings?
1→scan workspace for references to corrected value
2→flag: `CASCADE[{N}]: F[{agent}:{finding}] references [{old-value}] → may need update`
3→cascade found → report to user: "This correction may affect {N} other findings: {list}. Trace implications?"
  user confirms → trace each cascaded finding, apply datum or concept track as appropriate
  user declines → log cascade as unresolved in addendum

### 5→Update
1→agent calibration: `log_correction` via sigma-mem
  `C[datum|{date}]: F[{agent}:{finding}] {old}→{new} |source:{user-source} |error-class:{class} |cascade:{N|none}`
  error classes:
    `factual-error` — wrong number/fact (source was correct, review got it wrong)
    `source-misread` — right source, wrong reading of it
    `stale-data` — source outdated, newer data available
    `transcription` — typo, unit error, copy mistake
2→workspace addendum: append to archived workspace ## post-review-calibration
  ```
  DC[{N}|{date}]: F[{agent}:{finding}] {old}→{new} |confirmed-by:user |error-class:{class} |cascade:{refs|none}
  ```
3→if datum affects a calibrated estimate (CAL[] in workspace):
  report: "CAL[{estimate}] used [{old-value}]. With [{new-value}], the estimate may shift. Flag for recalibration?"

## Track 2: Concept (adversarial mini-review)

!purpose: user's reframing gets same rigor as any review finding | ¬accepted because user said it

### 1→Formulate
- which finding/framework: identify the review's current understanding
- user's correction as hypothesis: `H[user-correction]: {the user's proposed framing}`
- identify: which agent(s) produced the finding being corrected

### 2→Present Framing to User (plain English)
```
I'll test your correction against the review's original position:

Review's framing: [{original — what the team concluded}]
Your correction: [{H[user-correction]}]

This goes through a mini-review: domain agent researches independently,
DA challenges both positions. Accepted only if evidence supports it.

Proceed?
```
!gate: user confirms before spawning

### 3→Spawn Mini-Review (2 agents)

**Domain agent**: agent whose finding is being corrected (or closest domain match)
  model: same tier as original review

**DA**: devils-advocate
  model: opus

#### Domain Agent Spawn Prompt
```
You are {name} on a sigma-feedback concept review.

## Context
Your team completed a review of [{task}]. A post-review correction has been submitted.

## The Correction
Review's framing: [{original-finding — full text from workspace}]
User's correction: [{H[user-correction]}]

## Your Task
1→Research the user's framing independently
  same standards as full review: source provenance (§2d), quality tiers (§2d+)
  DO NOT just confirm the user — investigate whether their framing is accurate
2→Compare: your original framing vs user's framing vs what independent research shows
3→Produce one of:
  ACCEPT: user's framing better supported |evidence: {sources with tiers} |what-changes: {implications}
  REJECT: original framing holds |evidence: {sources with tiers} |why-user-framing-fails: {specific}
  SYNTHESIZE: both partially correct |evidence: {sources with tiers} |revised-framing: {new understanding}
4→Source-tag all findings (§2d mandatory)
5→Write findings to workspace
```

#### DA Spawn Prompt
```
You are the devil's advocate on a sigma-feedback concept review.

## Context
Review completed for [{task}]. User submitted a conceptual correction.

## The Positions
ORIGINAL (review's framing): [{original-finding}]
CORRECTION (user's framing): [{H[user-correction]}]

## Your Task
1→Steelman the original review position
  What evidence supports the original framing? Why might the review have been right?
2→Challenge the user's correction
  What evidence contradicts the user's framing?
  What assumptions does the user's correction rely on?
  Could the user have a partial or context-specific understanding?
3→Challenge the original too (fairness)
  What weaknesses in the original does the correction expose?
4→Verdict:
  CORRECTION-STRONGER: user's framing better supported |evidence-gap: {what original missed}
  ORIGINAL-STRONGER: review's framing better supported |user-weakness: {where correction fails}
  MIXED: neither fully correct |→ synthesis needed: {what each gets right/wrong}
```

### 4→Convergence
Read both agents' findings:
- both ACCEPT/CORRECTION-STRONGER → accept correction
- both REJECT/ORIGINAL-STRONGER → reject correction (present evidence to user)
- mixed/SYNTHESIZE → present synthesis to user for confirmation

!rule: rejecting → explain WHY with evidence ¬"the team disagrees"
  show specific evidence that contradicts the user's framing
  user may provide additional evidence → one additional round max (domain agent re-evaluates, DA reviews)
!rule: domain agent and DA disagree → present both positions with evidence, user decides
  this is the one place user judgment is final — they may have domain context agents lack

### 5→Update (if accepted or synthesized)
1→agent calibration: `log_correction` via sigma-mem
  `C[concept|{date}]: F[{agent}:{finding}] |original:{summary} |corrected:{summary} |evidence:{key-sources} |error-class:{class} |DA-verdict:{verdict}`
  error classes:
    `framing-error` — wrong model/mechanism
    `omission` — missed key mechanism or factor
    `oversimplification` — right direction, wrong nuance
    `domain-gap` — outside agent's expertise
2→workspace addendum: append to archived workspace
  ```
  CC[{N}|{date}]: F[{agent}:{finding}]
    original: {summary}
    corrected: {accepted-framing}
    evidence: {key sources with tiers}
    DA-verdict: {verdict}
    error-class: {class}
    affected-findings: {findings that relied on corrected concept}
  ```
3→concept correction affects multiple findings → trace cascade (same as datum Track 1 §4)

### 6→Rejection Path
1→present to user (plain English):
```
The correction was tested and evidence supports the original framing:

Your framing: [{H[user-correction]}]
Evidence against: [{DA's specific evidence}]
Evidence for original: [{domain agent's evidence}]

The original finding stands. Provide additional evidence, or accept the original?
```
2→user provides more evidence → one additional round (domain agent re-evaluates, DA reviews)
3→still rejected → log: `C[concept-rejected|{date}]: F[{agent}:{finding}] |user-framing:{summary} |rejected-because:{evidence} |original-maintained`
4→user insists after second rejection → accept with flag:
  `C[concept-user-override|{date}]: F[{agent}:{finding}] |user-framing:{summary} |evidence-inconclusive |user-override:true`
  !note: user-override is legitimate — they may have domain context that can't be independently researched

### Escalation: Datum → Concept
During datum pushback, if lead realizes correction implies a different framework ¬just a different number:
→ report: "This looks like a structural correction, not just a data fix. Run through concept track instead?"
→ user confirms → reclassify + run concept track
→ user declines → proceed as datum

## Pattern Detection

After all corrections processed:

### Per-Correction Entry
```
FEEDBACK[{date}|{review-slug}]:
  track: datum|concept
  agent: {name}
  finding: {ref}
  error-class: {class}
  cascade: {N findings affected}
  resolution: accepted|synthesized|rejected|user-override
```

### Systemic Pattern Check
1→get_agent_memory(team:sigma-review, agent:{corrected-agent}) → read C[] entries
2→count by error-class across reviews:
  same agent + same error-class ≥ 3 reviews → flag systemic:
    `SYSTEMIC[{agent}|{error-class}]: {count} across {reviews} |→ review agent weight/review-steps/research`
  same error-class across multiple agents ≥ 3 → flag process:
    `SYSTEMIC[process|{error-class}]: {count} across {agents} |→ review directives §{relevant}`
3→store patterns: store_team_pattern(team:sigma-review)

### Longitudinal Calibration (when ≥5 corrections accumulated per agent)
  accuracy = 1 - (corrections / total-findings)
  by-class breakdown: which error types dominate
  report: `CALIBRATION[{agent}]: accuracy={%} |top-error:{class}({count}) |trend:{improving|stable|degrading}`

## Report

After all corrections processed, present to user (plain English):

```
## Feedback Summary

### Corrections Applied
{per correction: finding, old→new or old→revised-framing, track, resolution}

### Cascade Effects
{downstream findings affected, if any}

### Calibration Notes
{error patterns detected, systemic flags, if any}

### Updated
- Agent memory: {agents updated with C[] entries}
- Workspace: {archive path} amended with ## post-review-calibration
```

## Notes

- concept mini-review agents spawned via Agent tool → fresh context, no review conversation contamination
- concept track agents read workspace findings + correction only — not full conversation
- datum track is fast (single pushback round) — concept track is slower (2-agent mini-review)
- all datums processed before concepts (updated facts may inform concept review)
- correction to a finding that was already corrected → update existing correction entry ¬duplicate
- /sigma-feedback can be run multiple times against the same workspace — addendum accumulates
