# Phase 04: Build (Build-Track Implements)

**Every step below is mandatory. Complete them in order.**

## Purpose
Build-track agents implement against the locked plan. You monitor progress, enforce checkpoints, and run cross-model code review before advancing to the review phase.

## Steps

### Step 0: Parallel Engineer Check (before build starts)
Evaluate SQ[] independence per build-directives §3a.1:
1. Map SQ[] items to primary files
2. Identify independent clusters (zero shared files)
3. If ≥2 clusters: spawn additional implementation-engineer-N with `isolation: "worktree"`
4. Write file ownership to workspace ## build-assignments
5. If 1 cluster: single engineer (skip this step)

### Step 1: Confirm Build-Track Agents Have Locked Plan
Verify ALL build-track agents (including parallel engineers) can read:
- ## architecture-decisions (ADRs)
- ## interface-contracts (typed contracts)
- ## build-assignments (if parallel engineers spawned)

!rule: these are BUILD CONSTRAINTS. Agents implement against them, ¬redesign.

### Step 2: Monitor Build Progress
Track build-track agent status via workspace ## build-status and ## findings:
- ◌ (building) → wait
- ? (needs clarification) → check if question is about plan interpretation → route to plan-track agent or answer from workspace
- ! (blocked) → surface to user

### Step 3: Enforce Checkpoint at ~50%
Each build-track agent MUST write a checkpoint:
```
CHECKPOINT[{agent}]: {files-created} |{functions-done} |{interfaces-matched: yes/no} |drift: {none|{description}} |surprises: {none|{description}}
```

If any agent reports drift or surprises at checkpoint:
- Minor drift → note in workspace, continue
- Scope creep → flag immediately, discuss with user before continuing
- Architectural drift → STOP, this should have been caught in plan phase

### Step 4: Wait for Build Complete
All build-track agents (including parallel engineers) must:
- Write findings to workspace ## findings (prefixed with agent name)
- Write checkpoint to workspace ## build-status
- Persist memory
- Declare ✓ in convergence

If parallel engineers: after all engineers ✓, run merge step:
1. Code-quality-analyst or lead merges worktrees
2. Run FULL test suite on merged result (individual passes ¬guarantee combined)
3. If merge conflicts → route to owning engineer, re-merge, re-test
4. Write to workspace ## build-status:
   `MERGE-VERIFIED: {test-count} passed |conflicts:{none|resolved({files})} |worktrees-merged:{list}`
   !gate: MERGE-VERIFIED MUST be in workspace before advancing to Step 5. No merge verification = no build review.

### Step 5: Validate Build Checkpoint
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check build-checkpoint
```
This runs V19. If fails: SendMessage agents requiring checkpoint completion.

### Step 6: Cross-Model Code Review (when ΣVerify available)
!rule: advisory weight — informs review, ¬automatic overwrite
!skip if workspace ## infrastructure shows ΣVerify unavailable

1. Select review targets: key files (max 8-10), priority: cross-agent integration, complex logic, security
2. CODE-REVIEW prompt: correctness, maintainability, performance, security
   UI-REVIEW prompt: usability, state management, accessibility, error states
3. Write to workspace ## cross-model-code-review:
   `"XREVIEW[{provider}:{model}][{file}]: {assessment} |issues:{count} |severity:{H/M/L}"`
4. Route to build-track agents: `"XREVIEW[{file}]: accept|note|reject — {reasoning}"`
5. DA + plan-track read XREVIEW findings as advisory input to build review

### Step 7: Re-spawn Plan-Track for Review
Plan-track agents (tech-architect, product-designer, product-strategist) are re-spawned with workspace context for the build review phase.

### Step 8: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"build_complete": true, "checkpoint_validated": true}'
```
Confirm returned phase = `review`.

## Exit Checklist

- [ ] Build-track agents confirmed access to locked plan
- [ ] All agents wrote checkpoints at ~50%
- [ ] Drift/scope issues handled (if any)
- [ ] All agents declared build complete with findings
- [ ] If parallel engineers: MERGE-VERIFIED written to workspace (HARD GATE)
- [ ] Build checkpoint validation passed (V19)
- [ ] Cross-model code review completed (if ΣVerify available)
- [ ] Plan-track agents re-spawned for review
- [ ] Orchestrator advanced to review

**All items checked → read `phases/05-build-review.md`**
