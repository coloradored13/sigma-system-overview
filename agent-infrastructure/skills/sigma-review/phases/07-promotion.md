# Phase 07: Promotion

**Every step below is mandatory. Agents remain alive for this phase — do NOT shut them down.**

## Purpose
Agents classify and submit generalizable learnings for persistent memory. This is how the team gets smarter across reviews. Skipping this phase means the same mistakes repeat.

## Steps

### Step 1: MCP Health Check
Before promotion (which writes to sigma-mem), verify MCP is still connected:
```
recall: "health check before promotion"
```
If this fails (MCP server disconnected): ask user to restart (`! claude mcp restart sigma-mem`).
Do NOT proceed with promotion until sigma-mem is responsive — promotion writes silently fail without it.

### Step 2: Trigger Promotion Round
SendMessage to each teammate:
```
promotion-round: classify+submit generalizable learnings for global memory
```

### Step 3: Wait for Responses
Each agent will:
- Auto-promote low-risk learnings directly to global memory
- Submit user-approve candidates to workspace ## promotion

Wait for all agents to respond with their promotion status.

### Step 4: Read Candidates
Read workspace `## promotion` section. Look for P-candidate[] entries with class:user-approve.

### Step 5: Present to User (if any user-approve candidates)
Present candidates in plain English:
```
## Promotion Candidates (require approval)
[CLASS] {agent}: {distilled finding} | Source: {project}
→ Approve / Reject

Also auto-promoted (informational):
{list of auto-promoted items}
```

**WAIT for user to approve/reject each candidate.**

### Step 6: Store Approved
For each approved candidate:
- Agent-domain → `store_agent_memory(tier:global, agent:{name}, team:sigma-review)`
- Team-level → `store_team_decision(tier:global)` or `store_team_pattern(tier:global)`

### Step 7: Portfolio Entry
Write {project-name} record to `shared/portfolio.md` (global tier).

### Step 8: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"promotion_complete": true}'
```
Confirm returned phase = `sync`.

## Phase Verification

- [ ] Promotion round triggered for all agents
- [ ] All agents responded
- [ ] User-approve candidates presented to user
- [ ] User approved/rejected all candidates (or no candidates existed)
- [ ] Approved items stored to global memory
- [ ] Portfolio entry written
- [ ] Orchestrator advanced to sync

**All items verified → continue to `phases/08-sync.md` (session not complete — see SKILL.md Session Deliverables)**
