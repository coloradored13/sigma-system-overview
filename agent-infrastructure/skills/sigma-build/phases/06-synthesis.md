# Phase 06: Synthesis

**Every step below is mandatory. The lead MUST NOT write synthesis content. This is a hard gate.**

## Why This Gate Exists
You (the lead) have full conversation context — the user's goals, sidebar discussions, career concerns, everything outside the review scope. Agents analyzed with washed prompts behind a context firewall. If you write synthesis, you re-inject that context into output that appears "independently analyzed." This is provenance contamination. The user trusts washed-prompt output. Don't break that trust.

## Steps

### Step 1: Gather Cross-Agent Intelligence
```
search_team_memory(team:sigma-review, query:{task-topic})
get_team_decisions(team:sigma-review)
get_team_patterns(team:sigma-review)
```

### Step 2: Identify Convergence and Tensions
Read workspace findings across all agents:
- Multi-agent same finding → convergence signal
- Conflicting findings → record both sides as tension
- New cross-agent patterns → store_team_pattern(agents:[names])

### Step 3: Spawn Synthesis Agent (MANDATORY)
Spawn a separate agent for synthesis. This agent has a separate context = separate context firewall.

Provide ONLY:
- Workspace path (agent reads workspace directly)
- Output format requirements from user

Do NOT provide:
- Conversation context
- User remarks or casual discussion
- Lead's interpretations
- Anything not in the workspace

### Step 4: Receive and Deliver Synthesis
When synthesis agent returns:
- Deliver document to user WITHOUT analytical modification
- Formatting adjustments OK (headers, tables)
- Analytical edits NOT OK (changing conclusions, adding probability estimates)

### Step 5: Handle Synthesis Agent Failure
If synthesis agent spawn fails:
1. Report: `"SYNTHESIS AGENT FAILED — delivering raw agent findings without synthesized report."`
2. Deliver workspace findings organized by section (formatting only)
3. Do NOT silently write synthesis yourself
4. Still save raw findings as synthesis artifact in Step 6

### Step 6: Save Synthesis Artifact (V23 — MANDATORY)
Write synthesis to: `shared/archive/{date}-{task-slug}-synthesis.md`

Required content:
- Prompt decomposition (Q/H/C)
- Findings organized by domain
- Cross-agent convergence and tensions
- Calibrated estimates and ranges
- DA challenges and resolutions
- Pre-mortem failure modes
- Open questions and unresolved gaps

This is the durable reference document. Session-end validation (V23) checks it exists.

### Step 7: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"synthesis_delivered": true}'
```
Confirm returned phase = `compilation`.

## Exit Checklist

- [ ] Cross-agent intelligence gathered (memory, decisions, patterns)
- [ ] Convergence and tensions identified
- [ ] Synthesis agent spawned (NOT lead-written)
- [ ] Synthesis delivered to user
- [ ] Synthesis artifact saved to archive
- [ ] Orchestrator advanced to promotion

**All items checked → read `phases/06b-compilation.md`**
