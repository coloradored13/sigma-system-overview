# Phase 03: Plan Challenge (DA + Build-Track Evaluate Plan)

**Every step below is mandatory. This phase may loop. Complete the full cycle each round.**

## Purpose
DA joins and challenges the plan alongside build-track agents. Plan-track defends or revises. This is where design quality is forged before any code is written.

## Steps (execute this full cycle per round)

### Step 1: Spawn DA (first entry only)
On first entry to this phase:
1. Read `~/.claude/agents/devils-advocate.md`
2. Spawn DA via TeamCreate with model="opus"
3. DA reads workspace (plans, ADRs, design system, interface contracts)

If already in a loop (round 2+), DA is already alive — skip to Step 2.

### Step 2: Zero-Dissent Circuit Breaker (MANDATORY after first challenge round)
After receiving first round of challenges from DA + build-track:

**If zero pushback (all accept, no challenges):**
1. Report: `"Zero-dissent on plan: {N} reviewers, 0 challenges. Firing circuit breaker."`
2. Send targeted self-challenge to EACH reviewer:
   ```
   zero-dissent circuit breaker: your feasibility assessment of [{highest-risk plan element}] agrees with all peers.
   (1) Name the strongest reason this plan could fail in implementation.
   (2) If that failure occurs, what would you change?
   (3) Identify ONE interface contract or design spec you'd challenge.
   ```
3. Wait for responses, read additions.

**If challenges found:** Log divergence to workspace, proceed to Step 3.

### Step 3: Validate Circuit Breaker
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check cb
```
Address failures before advancing.

### Step 4: DA + Build-Track Challenge Round
DA challenges:
- Over-engineering, spec drift, assumption conflicts, premature abstraction
- Prompt-understanding alignment: do plans address Q[]/H[]/C[]?
- Source-provenance audit (§2d)
- Prompt audit (§7d): were BUILD claims from prompt tested or assumed?

Build-track challenges (feasibility focus):
- "Can I actually build this?" — framework constraints, complexity
- Interface contract feasibility, design system feasibility
- Effort reality: are CAL[] estimates realistic?
- Format: `"BUILD-CHALLENGE[{agent}]: {plan-element} |feasibility:{H/M/L} |issue:{description} |→ {revise|clarify|accept}"`

### Step 5: Plan-Track Responds
Plan-track agents respond to both DA and build-track:
- DA challenges: `"DA[#N]: concede|defend|compromise — [evidence]"`
- Build challenges: `"BC[#N]: concede|defend|compromise — [evidence]"`

Monitor workspace for updates. Allow inter-agent interaction.

### Step 6: Validate Challenge Round
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check challenge-round --round N
```
Address any failures.

### Step 7: Compute Belief State
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py compute-belief --belief-mode build-plan --round N
```
Write: `"BELIEF[plan-r{N}]: P={posterior} |builder-feasibility={score} |interface-agree={score} |design-arch={score} |conflicts={none|count} |review-coverage={score} |DA={grade} |→ {lock-plan|another-round({gaps})|Toulmin-debate}"`

If |declared - computed| > 0.15: must justify divergence.

### Step 8: Check Exit Condition
- **P > 0.85 + DA PASS** → lock plan, advance to build (Step 9)
- **P 0.6-0.85 or DA FAIL** + round < 5 → loop back to Step 4
- **P < 0.6** → proceed to Phase 05b (debate)
- **Round ≥ 5 (hard cap)** → lock plan, advance to build (Step 9)

### Step 9: Lock Plan + Validate (only when exiting to build)
Lock ADRs, design system, interface contracts in workspace.

```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check plan-lock
```
Plan-lock runs V17. If fails: plan-track agents complete missing output.

!rule: plan-track agents exit after plan locked. Re-spawned for build review (Phase 05).

### Step 10: Advance Orchestrator

**If exiting to build:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"exit_gate": "PASS", "belief_state": X.XX, "round": N, "plan_lock_validated": true}'
```

**If looping:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"exit_gate": "FAIL", "belief_state": X.XX, "round": N}'
```
Return to Step 4.

**If going to debate:**
Orchestrator routes to debate phase.

## Exit Checklist (when leaving this phase)

- [ ] DA spawned and participated
- [ ] Circuit breaker checked (mandatory after first round)
- [ ] All challenge rounds validated
- [ ] Belief state computed for each round
- [ ] Exit condition met (PASS, hard cap, or debate)
- [ ] If exiting to build: plan locked, plan-lock validation passed
- [ ] Orchestrator advanced

**Exiting to build → read `phases/04-build.md`**
**Exiting to debate → read `phases/05b-debate.md`**
**Looping → re-execute this phase from Step 4**
