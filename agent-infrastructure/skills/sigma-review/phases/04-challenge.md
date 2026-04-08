# Phase 04: Challenge (R2+)

**Every step below is mandatory. This phase may loop. Complete the full cycle each round.**

## Purpose
DA joins and challenges agent findings. Agents integrate DA feedback, defend or revise. This is where analytical quality is forged.

## Steps (execute this full cycle per round)

### Step 1: Spawn DA (first entry only)
On first entry to this phase:
1. Read `~/.claude/agents/devils-advocate.md`
2. Spawn DA via TeamCreate with model="opus"
3. DA reads workspace (including R1 findings + circuit breaker results)
4. DA also reads prior challenge round findings (if looping)

If already in a loop (round 3+), DA is already alive — skip to Step 2.

### Step 2: DA Challenge Round
DA reads all agent findings and produces challenges. Wait for DA to write challenges to workspace.

### Step 3: Agent Integration
All agents read DA challenges and respond:
- Concede with evidence
- Defend with evidence
- Compromise with revised position

Monitor agent workspace sections for updates. Agents interact via workspace and inboxes — they may trigger each other (e.g., product-strategist's revision triggers tech-architect to re-evaluate).

### Step 4: Wait for Convergence
Monitor convergence section. All agents (including DA) must declare status.
- If agents are actively interacting via workspace/inbox, let them work
- Prod stuck agents per Phase 02 Step 3 pattern

### Step 5: Validate Challenge Round
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check challenge-round --round N
```
This runs V10+V11. Address any failures.

### Step 6: Compute Belief State
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py compute-belief --belief-mode analyze --round N
```
Review belief components. Write: `BELIEF[r{N}]: P={posterior} |→ {action}`

If |declared - computed| > 0.15: must justify divergence in workspace.

### Step 7: Check Exit Gate
Read DA's exit-gate declaration in workspace. DA controls exit:
- **DA: PASS** + belief ≥ 0.85 → proceed to pre-synthesis validation (Step 8)
- **DA: FAIL** + belief ≥ 0.6 + round < 5 → loop back to Step 2 (another round)
- **DA: FAIL** + belief < 0.6 → proceed to Phase 05 (debate)
- Round ≥ 5 (hard cap) → proceed to pre-synthesis validation (Step 8)

### Step 8: Pre-Synthesis Validation (only when exiting to synthesis)
Run anti-contamination and pre-synthesis checks:
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check pre-synthesis
```
This runs V13+V14+V15+V16. Address any failures before advancing.

Also execute anti-contamination check:
1. Re-read workspace ## scope-boundary
2. Identify topics in this conversation OUTSIDE review scope
3. Write: `CONTAMINATION-CHECK: session-topics-outside-scope: {list} |scan-result: clean|contaminated({terms})`
4. Write: `SYCOPHANCY-CHECK: softened:{list|none} |selective-emphasis:{list|none} |dissent-reframed:{list|none} |process-issues:{list|none}`

### Step 9: Advance Orchestrator

**If exiting to synthesis:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"exit_gate": "PASS", "belief_state": X.XX, "round": N, "pre_synthesis_validated": true}'
```

**If looping (another challenge round):**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"exit_gate": "FAIL", "belief_state": X.XX, "round": N}'
```
Then return to Step 2.

**If going to debate:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"exit_gate": "FAIL", "belief_state": X.XX, "round": N}'
```
Orchestrator routes to debate phase.

## Exit Checklist (when leaving this phase)

- [ ] DA spawned and participated
- [ ] All challenge rounds completed with agent responses
- [ ] Each round validated (challenge-round check passed)
- [ ] Belief state computed for each round
- [ ] Exit gate evaluated (PASS or hard cap)
- [ ] If exiting to synthesis: pre-synthesis validation passed
- [ ] If exiting to synthesis: contamination + sycophancy checks written
- [ ] Orchestrator advanced

**Exiting to synthesis → read `phases/06-synthesis.md`**
**Exiting to debate → read `phases/05-debate.md`**
**Looping → re-execute this phase from Step 2**
