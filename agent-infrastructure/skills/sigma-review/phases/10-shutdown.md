# Phase 10: Shutdown

**This is the final phase. Only execute after the orchestrator has returned is_terminal: true.**

## Steps

### Step 1: Verify Terminal State
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py status
```
Confirm `is_terminal: true`. If NOT terminal, do not proceed — go back and complete whatever phase is current.

### Step 2: Shutdown Agents
SendMessage to each teammate:
```
shutdown_request
```
Wait for `shutdown_response` from each agent.

### Step 3: Handle Stragglers
If any agent doesn't respond within reasonable time:
- Check their workspace section — did they complete their work?
- If yes: note forced shutdown in workspace convergence
- If no: flag incomplete work to user

### Step 4: Final Report
Report to user in plain English. Include:
- Review summary (task, tier, agents, rounds)
- Promotion summary (what was promoted, what was approved)
- Sync summary (what was synced, commit status)
- Any open items or anomalies

### Step 5: Checkpoint
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py checkpoint
```
Save final state for audit trail.

## Exit Checklist

- [ ] Orchestrator confirmed terminal
- [ ] All agents received shutdown_request
- [ ] All agents responded (or stragglers handled)
- [ ] Final report delivered to user
- [ ] Checkpoint saved

**Review complete.**
