# Phase 05: Build Review (DA + Plan-Track Evaluate Build)

**Every step below is mandatory. This phase may loop. Complete the full cycle each round.**

## Purpose
DA and plan-track agents review the build for code quality, plan compliance, and design fidelity. Build-track fixes agreed issues. This is where implementation quality is verified.

## Steps (execute this full cycle per round)

### Step 1: DA + Plan-Track Review
DA reviews:
- Code quality: correctness, security, maintainability
- Test integrity (§4d): behavior vs runs, requirements vs implementation, failure cases, hardcoded values, real infra vs mocks
- Scope compliance (§4a): built only what's in scope
- Gold-plating detection (§4c)
- XREVIEW findings (advisory, from Phase 04 Step 6)
- §2d source provenance audit — ALL agents (plan-track AND build-track). Not just those DA challenged.
  !rule: DA must verify |source:{type}| tags on build-track findings, not just plan-track.

Plan-track reviews (intent fidelity):
- tech-architect: do implementations match ADRs? interface contracts correct? tech stack as designed?
- product-designer: does UI follow design system? tokens correct? interaction patterns match IX[]? accessibility implemented?
- product-strategist: does build address priority sequencing? success criteria achievable?
- Format: `"PLAN-REVIEW[{agent}]: {component} |compliance:{full|partial|drift} |issue:{description} |→ {accept|fix:{specific-change}}"`

§2h cross-model verification (when ΣVerify available):
- Plan-track agents verify top 1 load-bearing compliance finding
- This is IN ADDITION to the code review (quality vs compliance are separate)

### Step 2: Build-Track Responds + Fixes
Build-track agents respond:
- DA challenges: `"DA[#N]: concede|defend|compromise — [evidence]"`
- Plan-track findings: `"PR[#N]: fixed|justified|deferred — [evidence]"`
- Implement agreed changes → re-submit for review

### Step 3: Validate Review Round
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check challenge-round --round N
```
Address any failures.

### Step 4: Compute Belief State (HARD GATE — must write to workspace)
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py compute-belief --belief-mode build-quality --round N
```
Write to workspace ## belief-tracking:
`"BELIEF[build-r{N}]: P={posterior} |plan-compliance={score} |test-coverage={score} |design-fidelity={score} |code-quality={score} |scope={clean|creep} |DA={grade} |→ {done|another-round({issues})|escalate}"`

!gate: BELIEF[] MUST be written to workspace before advancing. Not optional. DA exit-gate grades are NOT a substitute.

### Step 5: Check Exit Condition
- **P > 0.85 + DA PASS** → proceed to pre-synthesis validation (Step 6)
- **P 0.6-0.85 or DA FAIL** + round < 5 → loop back to Step 1
- **P < 0.6** → escalate to user (fundamental plan-build mismatch)
- **Round ≥ 5 (hard cap)** → proceed to pre-synthesis validation (Step 6)

BUILD success criteria (check on exit):
- Zero architectural decisions during build that should have been in plan
- Plan-track confirms intent preserved (no silent drift)
- Scope creep caught at checkpoint, ¬at final review
- Test integrity catches ≥1 weak test pattern

### Step 6: Pre-Synthesis Validation (only when exiting)
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check pre-synthesis
```
This runs V13+V14+V15+V16. Address failures.

Anti-contamination check (HARD GATE — must write to workspace before advancing):
1. Re-read workspace ## scope-boundary
2. Identify topics in this conversation OUTSIDE build scope
3. Write to workspace ## contamination-check: `CONTAMINATION-CHECK: session-topics-outside-scope: {list} |scan-result: clean|contaminated({terms})`
4. Write to workspace ## contamination-check: `SYCOPHANCY-CHECK: softened:{list|none} |selective-emphasis:{list|none} |dissent-reframed:{list|none} |process-issues:{list|none}`
!gate: both checks MUST be written to workspace. Not optional. Skipping = audit YELLOW.

BUILD rubric evaluation (build-directives §3b, final round only):
1→ correctness | 2→ test-coverage | 3→ maintainability | 4→ performance | 5→ security | 6→ api-design

### Step 7: Advance Orchestrator

**If exiting to synthesis:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"exit_gate": "PASS", "belief_state": X.XX, "round": N, "pre_synthesis_validated": true}'
```

**If looping:**
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"exit_gate": "FAIL", "belief_state": X.XX, "round": N}'
```
Return to Step 1.

## Exit Checklist (when leaving this phase)

- [ ] DA + plan-track reviewed build
- [ ] All review rounds validated
- [ ] Belief state computed for each round
- [ ] Exit condition met (PASS or hard cap)
- [ ] Pre-synthesis validation passed
- [ ] Contamination + sycophancy checks written
- [ ] BUILD rubric evaluated (final round)
- [ ] Orchestrator advanced

**Exiting to synthesis → read `phases/06-synthesis.md`**
**Looping → re-execute this phase from Step 1**
