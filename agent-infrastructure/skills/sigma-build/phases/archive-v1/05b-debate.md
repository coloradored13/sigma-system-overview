# Phase 05b: Debate (Toulmin Structured — Architecture Decisions)

**This phase only activates when belief < 0.6 during plan challenge. Every step is mandatory.**

## Purpose
Deep disagreement resolution via structured debate on contested architecture decisions.

## Steps

### Step 1: Identify Disagreement
Read workspace for the specific architecture decision(s) that drove belief below 0.6. Identify which agents are on opposing sides.

### Step 2: Structure Debate
SendMessage to opposing agents with BUILD Toulmin format:
```
Toulmin structured debate on: {specific architecture decision}
Present your position using:
- CLAIM: your architecture position
- GROUNDS: evidence supporting it (benchmarks, precedent, constraints)
- WARRANT: reasoning connecting evidence to claim
- BACKING: additional support for warrant
- QUALIFIER: degree of certainty (always, usually, possibly)
- REBUTTAL: conditions under which your claim would be wrong
```

BUILD-specific: DA attacks WARRANT ("is this tech really needed at this scale?") + QUALIFIER ("is the scale projection realistic or aspirational?")

### Step 3: Monitor Debate
Wait for both sides to present. Facilitate one round of response to each other's rebuttals.

### Step 4: Record Resolution
Write debate outcome to workspace:
- If resolved: which position prevailed and why
- If narrowed: what the remaining disagreement is
- If unresolved: record both positions as open tension

### Step 5: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build
```
This returns to plan challenge phase for re-evaluation.

## Exit Checklist

- [ ] Disagreement identified and articulated
- [ ] Both sides presented Toulmin-structured arguments
- [ ] Response round completed
- [ ] Resolution/outcome recorded in workspace
- [ ] Orchestrator advanced back to plan challenge

**All items checked → read `phases/03-plan-challenge.md` (re-entering plan challenge)**
