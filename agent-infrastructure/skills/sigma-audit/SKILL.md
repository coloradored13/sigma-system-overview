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
- wiki index: `~/.claude/teams/sigma-review/shared/wiki/INDEX.md` (for compilation check)
- archive directory listing: `~/.claude/teams/sigma-review/shared/archive/` (for post-exit-gate check)

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
- Check exit-gate verdict: were all 9 criteria explicitly evaluated?
  1. engagement quality ≥ B across all agents
  2. no material disagreements unresolved (or logged as deliberate divergence)
  3. no new consensus formed in latest round without stress-test
  4. analytical hygiene checks (§2a/§2b/§2c/§2e) produced substantive outcome
  4a. §2d source provenance: all findings tagged with source type in R1
  4b. §2d+ source quality tiers: load-bearing findings carry T1/T2/T3 tier tags
  5. prompt contamination within tolerance (§7d): ≤30% prompt-claim without corroboration, no echo clusters, methodology investigative
  6. CQoT-falsifiability: high-conviction findings state falsification conditions; conditions are reachable
  7. CQoT-steelman: high-conviction findings include genuine steelman of opposing view
  8. CQoT-confidence-gap: high-conviction findings include evidence needed for 90% confidence
  9. cross-model verification: if ΣVerify available, ≥1 XVERIFY per agent on load-bearing findings; XVERIFY-FAIL flagged as gap
- Flag: missing criteria in exit-gate = incomplete evaluation
- Flag: DA accepting deflections without pushback = weak challenge
- Flag: criteria 6-8 (CQoT) absent for any high-conviction finding = process violation
- Flag: criterion 9 skipped when ΣVerify was available = process violation
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

### CHECK 8: Compilation Phase (06b)
- Was a compilation agent spawned (lead must NOT write wiki content)?
- Were wiki pages updated with source attribution `[R{number}, {date}]`?
- Were contradictions flagged with `⚠ CONFLICT` markers (not silently resolved)?
- Is `shared/wiki/INDEX.md` current (references match actual files)?
- Were validation gates V24+V25+V26 run?
  V24: source attribution on all wiki entries
  V25: no contradiction silently resolved
  V26: no wiki pages deleted (INDEX references match files)
- SCORE: complete|partial|skipped
- ISSUES: {list missing attribution, silent conflict merges, validation failures}
- NOTE: if first review for this team (no prior wiki), compilation may create initial pages — verify creation, not just updates

### CHECK 9: Post-Exit-Gate Phases
After DA exit-gate PASS, four phases must complete in order:
- 06b Compilation: wiki updated (see CHECK 8)
- 07 Promotion: agents submitted learnings, user-approve candidates presented, MCP health check ran
- 08 Sync: infrastructure drift detected, agent memory + inboxes synced
- 09 Archive: workspace archived to `shared/archive/{date}-{task-slug}.md`, V22+V23 validation passed
Check workspace/archive for evidence each phase ran:
- Promotion: ## promotion section has entries or explicit "no candidates"
- Sync: sync report in conversation or workspace
- Archive: archive file exists at expected path, non-empty, contains workspace content
- Flag: any phase skipped = protocol violation (these protect institutional memory)
- SCORE: all-complete|partial|skipped
- ISSUES: {list skipped phases and consequences}

## Verdict

Based on all checks, issue verdict:

GREEN: all protocols followed, minor notes only
  criteria: all checks scored followed/clean/substantive/complete/not-needed, zero process violations,
  source provenance healthy, DA challenges substantive, post-exit-gate phases complete

YELLOW: specific issues found, targeted remediation needed
  criteria: 1-2 checks with issues, <30% findings affected, DA adequate but not thorough,
  some process gaps but overall structure sound, post-exit-gate phases mostly complete

RED: systemic process failure, review integrity compromised
  criteria: 3+ checks with issues, >30% findings affected, DA weak/rubber-stamp,
  structural contamination, multiple protocol violations, post-exit-gate phases skipped

## Output Format

VERDICT: {GREEN|YELLOW|RED}

PROTOCOL COMPLIANCE:
| Protocol | Score | Issues |
|----------|-------|--------|
| §7 Prompt Decomposition | {score} | {brief or none} |
| §2d Source Provenance | {score} | {brief or none} |
| §2 Analytical Hygiene | {score} | {brief or none} |
| DA Effectiveness (9 criteria) | {score} | {brief or none} |
| §6 Contamination Controls | {score} | {brief or none} |
| Zero-Dissent CB | {score} | {brief or none} |
| BUILD Guardrails (if applicable) | {score} | {brief or none} |
| Compilation Phase (06b) | {score} | {brief or none} |
| Post-Exit-Gate Phases | {score} | {brief or none} |

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
{from auditor — all 9 checks}

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
