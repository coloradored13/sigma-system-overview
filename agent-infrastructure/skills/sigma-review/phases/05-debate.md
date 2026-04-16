# Phase 05: Debate (Toulmin Structured)

**This phase only activates when belief < 0.6 during challenge. Every step is mandatory.**

## Purpose
Deep disagreement resolution via structured debate. Agents with opposing positions present Toulmin-structured arguments.

## Steps

### Step 1: Identify Disagreement
Read workspace for the specific disagreement(s) that drove belief below 0.6. Identify which agents are on opposing sides.

### Step 2: Structure Debate
SendMessage to opposing agents with debate format:
```
Toulmin structured debate on: {specific claim}
Present your position using:
- CLAIM: your position
- GROUNDS: evidence supporting it
- WARRANT: reasoning connecting evidence to claim
- BACKING: additional support for warrant
- QUALIFIER: degree of certainty (always, usually, possibly)
- REBUTTAL: conditions under which your claim would be wrong
```

### Step 3: Monitor Debate
Wait for both sides to present. Then facilitate one round of response to each other's rebuttals.

### Step 4: Record Resolution
Write debate outcome to workspace:
- If resolved: which position prevailed and why
- If narrowed: what the remaining disagreement is
- If unresolved: record both positions as open tension

### Step 5: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance
```
This returns to challenge phase for re-evaluation.

## Phase Verification

- [ ] Disagreement identified and articulated
- [ ] Both sides presented Toulmin-structured arguments
- [ ] Response round completed
- [ ] Resolution/outcome recorded in workspace
- [ ] Orchestrator advanced back to challenge

**All items verified → continue to `phases/04-challenge.md` (re-entering challenge — session not complete)**
