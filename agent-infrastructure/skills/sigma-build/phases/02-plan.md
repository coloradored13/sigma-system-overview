# Phase 02: Plan (Plan-Track Agents Design)

**Every step below is mandatory. Complete them in order.**

## Purpose
Plan-track agents independently design the system architecture, UX/UI, and priorities. You monitor convergence and validate quality before advancing to the challenge phase.

## Steps

### Step 1: Monitor Agent Progress
Poll workspace ## plans section. For each plan-track agent, track status:
- ◌ (in progress) → wait
- ? (needs input) → surface question to user → write answer to inbox
- ! (blocked) → surface blocker to user
- ✓ (plan written) → proceed to Step 2 verification

### Step 2: Pre-Accept Verification (per agent declaring plan complete)
Before accepting any agent's plan output:
1. Verify their workspace ## plans section is NOT empty
2. Check required outputs per agent role:
   - tech-architect: ADR[N] + IC[N] + tech stack decisions
   - product-designer: DS[] + IX[N] + component tree
   - product-strategist: priority sequencing + success criteria
   - all: SQ[] + CAL[] + PM[] (min 3) + prompt-understanding mapping
3. Check: has agent persisted memory? (`get_agent_memory`)
4. If plan incomplete: SendMessage to agent with specific missing items

### Step 3: Verify XVERIFY Coverage (mandatory-when-available for security-critical)
Each plan-track agent MUST verify top 1 load-bearing decision:
- tech-architect: top ADR (highest reversal cost)
- product-designer: top design system decision
- product-strategist: top priority sequencing assumption

Security-critical ADRs (IP normalization, permission architecture, injection defense, trust boundaries):
- ΣVerify available → XVERIFY MANDATORY on top-1 security-critical ADR. Not advisory.
- ΣVerify available + non-security ADR → advisory (recommended, not required)
- ΣVerify unavailable → neutral, no penalty

If XVERIFY missing on any agent: SendMessage reminder before advancing.
If XVERIFY missing on security-critical ADR with ΣVerify available: DO NOT advance. Hard gate.

### Step 4: Wait for All Plan-Track Agents ✓
Do not proceed until ALL plan-track agents have:
- Written complete plan output to workspace
- Persisted memory
- Declared ✓ in convergence section

### Step 5: Validate Plan Convergence
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check plan-convergence --workspace workspace.md
```
This runs V3+V4+V5+V6+V8. Review the output.

If validation FAILS: address each failure, re-run until it passes.

### Step 6: Lead Confirms Cross-Agent Coherence
Before advancing, verify:
- Interface contracts ↔ design system alignment
- Data model ↔ UI data flow consistency
- Dependency ordering makes sense

Flag any misalignment in workspace ## open-questions for challenge phase.

### Step 7: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"plans_ready": true, "plan_round_validated": true}'
```
Confirm returned phase = `challenge_plan`.

## Exit Checklist

- [ ] All plan-track agents wrote non-empty plans
- [ ] Required outputs present per agent role
- [ ] XVERIFY coverage checked (when available)
- [ ] All agents persisted memory
- [ ] Plan convergence validation passed
- [ ] Cross-agent coherence verified
- [ ] Orchestrator advanced to challenge_plan

**All items checked → read `phases/03-plan-challenge.md`**
