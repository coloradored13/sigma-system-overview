# Phase 00: Preflight

**Every step below is mandatory. Complete them in order. Do not proceed to Phase 01 until the exit checklist passes.**

## Steps

### Step 1: Memory Recall
```
recall: "sigma-build task: $ARGUMENTS"
```
This grounds your context with team history, past patterns, and relevant decisions.

### Step 2: System Validation
```
validate_system(team:sigma-review) → confirm defs+memory+inboxes
```
Verify agent definitions, memory files, and inbox files exist and are readable.

### Step 3: Sigma-Verify Availability
```
sigma-verify init → check cross-model verification availability
```
- Log available providers (e.g. openai:gpt-5.4)
- Report: "ΣVerify: {providers} available" or "ΣVerify: unavailable (no API keys)"
- ¬blocking: build proceeds without cross-model verification if unavailable
- Record availability — you will write this to workspace in Phase 01

### Step 4: Read Roster
```
read: ~/.claude/teams/sigma-review/shared/roster.md
```

### Step 5: Complexity Assessment
Per build-directives §3a BUILD complexity tiers:
```
evaluate: module-count(1-5), interface-changes(1-5), test-complexity(1-5), dependency-risk(1-5), team-familiarity(1-5)
sum < 12 → TIER-1 (3+DA)
12-18    → TIER-2 (4-5+DA)
>18      → TIER-3 (6-9+DA)
```
Tier composition:
- TIER-1: plan-track(tech-architect) + build-track(primary-builder + reviewer) + DA
- TIER-2: plan-track(tech-architect + product-designer) + build-track(2-3 builders) + DA
- TIER-3: plan-track(tech-architect + product-designer + product-strategist) + build-track(3-5 builders + integration-specialist) + DA

### Step 6: Semantic Route
Match task → agent domains from roster.

### Step 7: Report + User Confirmation
Report to user:
```
"Complexity: BUILD TIER-{N} (score:{sum}/25). Waking {agents}: {reasons}"
```
**WAIT for user confirmation before proceeding.** Do not spawn agents without approval.

### Step 8: Prompt Understanding (HARD GATE)
sigma-build is self-contained. Any prompt enters here and gets broken down before agents see it.

a) EXTRACT from user prompt:
   - Q[]: what needs to be built (define build scope)
   - H[]: claims/assumptions about scale, tech, architecture (become hypotheses to test ¬requirements)
   - C[]: constraints/boundaries (stack, timeline, scope limits)
   - BUILD detection heuristics for H[]:
     - scale assumptions without evidence
     - technology assertions ("we need microservices")
     - user behavior claims ("primarily mobile")
     - performance requirements without measurement
     - architecture claims ("monolith won't scale")

b) CHALLENGE (lead pushes back before agents spawn):
   - Each H[]: "You assume X — validated or aspirational? What evidence?"
   - Scope: "X, Y, Z — all in scope, or should we phase?"
   - Feasibility: "Obvious blockers? Does the codebase support this?"
   - Prior art: if prompt references existing code, read it to verify claims match reality

c) CLARIFY (lead asks for missing info):
   - Ambiguous terms, missing context, success criteria, users

d) USER CONFIRMS refined Q[]/H[]/C[]
   !gate: user confirms BEFORE spawning agents
   !gate: confirmed understanding written to workspace ## prompt-understanding BEFORE spawn

Report: `"PROMPT-UNDERSTANDING: Q:{count} |H:{count}(challenged:{count}) |C:{count} |clarifications:{count} |user-confirmed: {yes/pending}"`

### Step 9: Cost Estimate
- Anthropic: {agent-count} agents × ~{rounds} rounds × ~2K tokens/round × pricing
- sigma-verify (if available): {agent-count} × {providers} XVERIFY calls × ~1K tokens each
- Estimated total: report to user
- ⚠ If estimated > $10: warn user, get confirmation

## Exit Checklist

- [ ] Memory recall completed
- [ ] System validation passed
- [ ] Sigma-verify status recorded
- [ ] Roster read
- [ ] Complexity tier assessed and reported
- [ ] Agent selection reported to user
- [ ] User confirmed agent selection
- [ ] Prompt understanding (Q/H/C) completed with challenge + clarify
- [ ] User confirmed prompt understanding
- [ ] Cost estimate reported (and confirmed if > $10)

**All items checked → read `phases/01-spawn.md`**
**Any item unchecked → complete it before proceeding**
