# Phase 03: Circuit Breaker

**Every step below is mandatory. Complete them in order.**

## Purpose
Detect herding. 10+ consecutive reviews produced zero R1 dissent — independent experts with 0 disagreements is a herding signal, not a quality signal.

## Steps

### Step 1: Scan for Divergence
Read workspace findings + convergence for ANY inter-agent tension, disagreement, or counter-estimate.

Look for:
- Different estimates for the same metric
- Conflicting recommendations
- Agents challenging each other's assumptions
- Different risk assessments

### Step 2: Branch on Result

**If tension found:**
1. Log: `"R1 divergence detected: {description}"` to workspace
2. Proceed to Step 4

**If zero divergence (all agents agree on everything):**
1. Report to user: `"Zero-dissent detected: {N} agents, {M} findings, 0 disagreements. Firing circuit breaker."`
2. Proceed to Step 3

### Step 3: Fire Circuit Breaker (only if zero divergence)
Send targeted self-challenge to EACH agent via SendMessage:

```
zero-dissent circuit breaker: your R1 finding on [{highest-conviction finding}] agrees with all peers.
(1) Name the strongest argument AGAINST your own position.
(2) If that argument is correct, would you change your conclusion?
(3) Identify ONE peer finding you would challenge, quantify differently, or add a caveat to.
Respond in workspace — append to your findings section. 3 focused responses only.
```

Wait for all agents to respond. Read their additions.

### Step 4: Validate Circuit Breaker
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check cb
```
If validation fails, address the failure before advancing.

### Step 5: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"cb_validated": true}'
```
Confirm returned phase = `challenge`.

## Exit Checklist

- [ ] Workspace scanned for inter-agent divergence
- [ ] If zero divergence: circuit breaker fired and all agents responded
- [ ] If divergence found: logged to workspace
- [ ] CB validation passed
- [ ] Orchestrator advanced to challenge

**All items checked → read `phases/04-challenge.md`**
