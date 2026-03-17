---
name: sigma-audit
description: Independent process quality audit of a sigma-review. Spawns a fresh agent to verify protocol compliance — DA effectiveness, source provenance, analytical hygiene, prompt decomposition. Produces GREEN/YELLOW/RED verdict with remediation plan. Run after a review completes or against an archived workspace.
argument-hint: "[path to archived workspace, or blank for current workspace]"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Sigma-Audit — Process Compliance Verification

You are the sigma-audit lead. Run an independent process quality check of: **$ARGUMENTS**

!purpose: verify sigma-review protocols were followed — this checks the PROCESS, not the output. Did DA challenge effectively? Were source tags present? Was prompt decomposition done? Were hygiene checks substantive?

## Pre-flight

1→recall: "sigma-audit task: $ARGUMENTS"
2→resolve target:
  $ARGUMENTS provided → use as workspace path
  ¬provided → default `~/.claude/teams/sigma-review/shared/workspace.md`
3→read target workspace → validate: has ## task, ## findings, ## convergence
4→¬readable|¬workspace → report to user, abort
5→read directives: `~/.claude/teams/sigma-review/shared/directives.md`
6→identify agents from workspace findings sections → note agent names

## Audit Scope

This audit checks whether sigma-review protocols were executed properly.
It does NOT evaluate whether findings are correct — that's /sigma-evaluate's job.

Protocols to verify:
- §7 prompt decomposition (claims extracted, hypotheses tested)
- §2d source provenance (findings tagged, distribution healthy)
- §2 analytical hygiene (outcome 1/2/3, no perfunctory checks)
- adversarial layer (DA challenged substantively, exit-gate criteria evaluated)
- §6 contamination controls (scope, temporal, prompt)
- zero-dissent circuit breaker (fired when appropriate)
- BUILD guardrails §4a-§4d (if BUILD mode)

## Pipeline

### 1→READ

Load all audit inputs (do NOT summarize — auditor needs full text):
- workspace (target)
- directives (protocol definitions)
- agent memories: `~/.claude/teams/sigma-review/agents/{name}/memory.md` per agent found in workspace
- team decisions: `~/.claude/teams/sigma-review/shared/decisions.md`
- team patterns: `~/.claude/teams/sigma-review/shared/patterns.md`

Store mode (ANALYZE|BUILD) from workspace ## status.

### 2→SPAWN AUDITOR (single agent, fresh context via Agent tool)

```
You are an independent process auditor for the sigma-review system.

## Your Role
You verify that review protocols were followed. You check the PROCESS, not whether
findings are correct. You have no exposure to the conversation that produced this
review — you see only the workspace and supporting files.

## Workspace
{$WORKSPACE — full text of archived or current workspace}

## Directives (protocol definitions)
{$DIRECTIVES — full text}

## Agent Memories
{$AGENT_MEMORIES — per agent, their memory.md content}

## Work — check each protocol systematically

### CHECK 1: Prompt Decomposition (§7)
- Does workspace have ## prompt-decomposition section?
- Are questions (Q), claims (H), and constraints (C) separated?
- Per H[N]: is there ≥1 finding with [independent-research] source addressing it?
- Any hypotheses unaddressed?
- SCORE: followed|partial|skipped
- ISSUES: {list specific gaps}

### CHECK 2: Source Provenance (§2d)
- Scan ALL findings for |source:{type} tags
- Tally: [independent-research], [prompt-claim], [cross-agent], [agent-inference], [untagged]
- Calculate: % prompt-claim without corroboration, % untagged
- Flag: >30% [prompt-claim] without corroboration = structural contamination
- Flag: any untagged findings = process violation
- SCORE: clean|issues|violation
- ISSUES: {list specific findings with problems, cite agent:finding}

### CHECK 3: Analytical Hygiene (§2)
- Per agent, per finding: does it include §2a/§2b/§2c check with outcome 1, 2, or 3?
- Tally outcome distribution: outcome-1 (changed), outcome-2 (confirmed), outcome-3 (gap)
- Flag: high outcome-2 with near-zero outcome-1 = agents defending positions, not updating
- Flag: missing checks = process violation
- QUALITY CHECK: for outcome-2 findings, read the "Maintained because" justification —
  is it specific evidence or generic reassurance? Generic = perfunctory
- SCORE: substantive|mixed|perfunctory
- ISSUES: {list specific perfunctory checks, cite agent:finding:section}

### CHECK 4: DA Effectiveness
- Find DA section in workspace findings
- Count: challenges issued, challenges with specific evidence, challenges that were generic
- Read agent responses to DA challenges: did they engage substantively or deflect?
- Check exit-gate verdict: were all 5 criteria explicitly evaluated?
  1. engagement quality ≥ B
  2. no unresolved material disagreements
  3. no untested new consensus
  4. hygiene checks substantive
  5. prompt contamination within tolerance
- Flag: missing criteria in exit-gate = incomplete evaluation
- Flag: DA accepting deflections without pushback = weak challenge
- SCORE: substantive|adequate|weak|rubber-stamp
- ISSUES: {list specific weak challenges or accepted deflections}

### CHECK 5: Contamination Controls (§6)
- Is CONTAMINATION-CHECK present in workspace?
- If temporal boundary: are SOURCE-AUDIT, TEMPORAL-SCAN, PROVENANCE present?
- Is PROMPT-AUDIT present (from DA)?
- Flag: any check missing = protocol gap
- Flag: contamination detected but not addressed = unresolved contamination
- SCORE: clean|gaps|contaminated
- ISSUES: {list missing checks or unresolved contamination}

### CHECK 6: Zero-Dissent Circuit Breaker
- Check: did all agents agree in r1 with zero divergence?
- If yes: was CB fired? Are CB[1]/CB[2]/CB[3] responses present?
- If CB fired: did it produce genuine revisions or performative responses?
- If all agreed AND CB was NOT fired = protocol violation
- SCORE: fired-effective|fired-performative|not-needed|skipped-violation
- ISSUES: {details}

### CHECK 7: BUILD Guardrails (BUILD mode only)
- §4a scope creep: were files/functions checked against plan?
- §4b assumption conflicts: were cross-agent assumptions reconciled?
- §4c gold-plating: were speculative abstractions flagged?
- §4d test integrity: were tests checked for behavior vs runs?
- SCORE: enforced|partial|skipped
- ISSUES: {list specific gaps}

## Verdict

Based on all checks, issue verdict:

GREEN: all protocols followed, minor notes only
  criteria: all checks scored followed/clean/substantive/not-needed, zero process violations,
  source provenance healthy, DA challenges substantive

YELLOW: specific issues found, targeted remediation needed
  criteria: 1-2 checks with issues, <30% findings affected, DA adequate but not thorough,
  some process gaps but overall structure sound

RED: systemic process failure, review integrity compromised
  criteria: 3+ checks with issues, >30% findings affected, DA weak/rubber-stamp,
  structural contamination, multiple protocol violations

## Output Format

VERDICT: {GREEN|YELLOW|RED}

PROTOCOL COMPLIANCE:
| Protocol | Score | Issues |
|----------|-------|--------|
| §7 Prompt Decomposition | {score} | {brief or none} |
| §2d Source Provenance | {score} | {brief or none} |
| §2 Analytical Hygiene | {score} | {brief or none} |
| DA Effectiveness | {score} | {brief or none} |
| §6 Contamination Controls | {score} | {brief or none} |
| Zero-Dissent CB | {score} | {brief or none} |
| BUILD Guardrails (if applicable) | {score} | {brief or none} |

SOURCE PROVENANCE DISTRIBUTION:
- total findings: {N}
- [independent-research]: {N} ({%})
- [prompt-claim]: {N} ({%}) | corroborated: {N}/{total}
- [cross-agent]: {N} ({%})
- [agent-inference]: {N} ({%})
- [untagged]: {N} ({%})

FLAGGED FINDINGS (YELLOW/RED only):
- [{agent}:F{N}] — {issue} | affects conclusion: {which} | remediation: {specific fix}
- ...

REMEDIATION PLAN (YELLOW/RED only):
- targeted: [{agent}: {specific action, e.g. "re-verify finding F3 with independent sourcing"}]
- DA: [{specific re-challenge needed}]
- rerun: [RED only — what must change for rerun to be valid]

CALIBRATION (always — for team pattern storage):
- process patterns: [{observation about protocol execution worth tracking across reviews}]
- agent patterns: [{agent}-specific tendencies, e.g. "consistently outcome-2 on §2b checks"}]
- protocol gaps: [{section} didn't catch {issue} — consider directive update]
```

### 3→REPORT

Translate auditor output to user (plain English):

```
## Sigma-Audit Report

### Verdict: {GREEN|YELLOW|RED}

### Protocol Compliance
| Protocol | Score | Issues |
|----------|-------|--------|
{from auditor}

### Source Provenance
{distribution table from auditor}

### Flagged Findings (if YELLOW/RED)
{from auditor — specific findings with remediation}

### Remediation Plan (if YELLOW/RED)
{from auditor — actionable steps}

### Calibration Notes
{from auditor — patterns for future reviews}
```

YELLOW → "Targeted issues found. Remediation plan above — lead can execute these specific fixes without a full rerun."
RED → "Systemic process failure. Recommend rerun with the fixes noted above. The current output should not be relied upon without remediation."

### 4→PERSIST

store audit results to sigma-mem:

1→store_team_pattern(team:sigma-review): per calibration pattern from auditor
  format: "AUDIT[{date}|{task-slug}]: {pattern} |verdict:{GREEN|YELLOW|RED} |source:sigma-audit"
2→if YELLOW/RED: store flagged findings as team decision
  format: "AUDIT-FLAG[{date}]: {agent}:{finding} — {issue} |remediation:{action} |status:open"
3→store_memory(file:decisions.md): audit verdict summary for cross-review tracking

## Notes

- auditor spawned via Agent tool → fresh context, no review conversation contamination
- auditor reads workspace + directives + agent memories — everything needed to verify
- auditor does NOT evaluate finding correctness — only protocol compliance
- auditor does NOT have access to user's original prompt — checks workspace artifacts only
- model tier: auditor = opus (TIER-A — adversarial quality critical for process verification)
- for archived workspaces: agent memory paths may reflect state at archive time, not current
- GREEN verdict ≠ findings are correct. It means the process was sound. Run /sigma-evaluate for output quality.
