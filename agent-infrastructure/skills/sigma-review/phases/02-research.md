# Phase 02: Research (R1)

**Every step below is mandatory. Complete them in order.**

## Purpose
Agents perform independent domain analysis. You monitor convergence and ensure quality before advancing.

## Steps

### Step 1: Monitor Agent Progress
Poll workspace convergence section. For each agent, track status:
- ◌ (in progress) → wait
- ? (needs input) → surface question to user → write answer to inbox → agent continues
- ! (blocked) → surface blocker to user
- ✓ (converged) → proceed to Step 2 verification for that agent

### Step 2: Pre-Accept Verification (per agent declaring ✓)
Before accepting any agent's ✓:
1. Verify their workspace findings section is NOT empty
2. Check: has agent persisted memory? (`get_agent_memory` for that agent)
3. If ✓ but ¬persisted: SendMessage to agent: "persist before ✓"
4. If ✓ but findings empty: SendMessage to agent: "findings section empty — complete analysis before ✓"

### Step 3: Handle Stuck Agents
If an agent has been ◌ for an extended period with no workspace updates:
1. Read their workspace section — what have they written so far?
2. Read their inbox — any unanswered messages?
3. Draft a targeted prod message diagnosing the likely issue
4. SendMessage to agent with prod

### Step 4: Wait for All Agents ✓
Do not proceed until ALL agents have:
- Written non-empty findings to workspace
- Persisted memory
- Declared ✓ in convergence section

### Step 5: Run R1 Convergence Validation
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check r1-convergence --round 1
```
This runs V3+V4+V5+V6+V7+V8. Review the output.

If validation FAILS:
- Read which checks failed and why
- Address each failure (re-spawn agent, request missing data, etc.)
- Re-run validation until it passes
- Do NOT advance with failed validation

### Step 6: Compute Belief State
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py compute-belief --belief-mode analyze --round 1
```
Review components (prior, agreement, revisions, gaps, DA-factor).
Write to workspace: `BELIEF[r1]: P={posterior} |→ {action}`

### Step 7: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"r1_converged": true, "r1_validated": true}'
```
Confirm returned phase = `circuit_breaker`.

## Exit Checklist

- [ ] All agents declared ✓ with non-empty findings
- [ ] All agents persisted memory before ✓
- [ ] R1 convergence validation passed (V3+V4+V5+V6+V7+V8)
- [ ] Belief state computed and written to workspace
- [ ] Orchestrator advanced to circuit_breaker

**All items checked → read `phases/03-circuit-breaker.md`**
