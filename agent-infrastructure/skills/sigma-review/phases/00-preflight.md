# Phase 00: Preflight

**Every step below is mandatory. Complete them in order. Do not proceed to Phase 01 until the exit checklist passes.**

## Steps

### Step 1: Memory Recall
```
recall: "sigma-review team task: $ARGUMENTS"
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
- Log available providers (e.g. openai:gpt-5.1)
- Report: "ΣVerify: {providers} available" or "ΣVerify: unavailable (no API keys)"
- ¬blocking: review proceeds without cross-model verification if unavailable
- Record availability — you will write this to workspace in Phase 01

### Step 4: Read Roster
```
read: ~/.claude/teams/sigma-review/shared/roster.md
```

### Step 5: Complexity Assessment
Per directives §3a ANALYZE complexity tiers:
```
evaluate: domain-count(1-5), precedent(1-5), stakes(1-5), ambiguity(1-5), uncertainty(1-5)
sum < 12 → TIER-1 (3+DA)
12-18    → TIER-2 (4-5+DA)
>18      → TIER-3 (5-8+DA)
```
Rules:
- reference-class-analyst wakes for ALL tiers
- DA always joins from R2

### Step 6: Semantic Route
Match task → agent domains from roster.
- direct-match → wake
- indirect → wake
- uncertain → wake (perspective > tokens)

### Step 7: Report + User Confirmation
Report to user:
```
"Complexity: ANALYZE TIER-{N} ({sum}/25). Waking {agents}: {reasons}"
```
**WAIT for user confirmation before proceeding.** Do not spawn agents without approval.

### Step 8: Prompt Decomposition (HARD GATE)
Per directives §7 — this step cannot be skipped:

**IF workspace ## socratic-session exists:**
  → decomposition already completed during socratic-grill handoff
  → read workspace ## socratic-session for pre-populated Q/H/C
  → present to user for re-confirmation (they may have refined thinking since)
  → skip cold extraction — go straight to confirmation
  → Report: `"PROMPT-DECOMPOSITION (socratic-warm): Q:{count} |H:{count} |C:{count} |user-confirmed: {yes/pending}"`

**IF no socratic-session:**
1. Read directives §7a
2. Extract from user prompt:
   - Q[]: questions user wants answered (define research scope)
   - H[]: claims/assumptions user makes (become hypotheses to test, ¬facts)
   - C[]: constraints/boundaries (narrow agent search)
3. Present structured decomposition to user (§7b format)
4. **WAIT for user to confirm Q/H/C** — do not proceed without confirmation
5. Report: `"PROMPT-DECOMPOSITION: Q:{count} |H:{count} |C:{count} |user-confirmed: {yes/pending}"`

### Step 9: Cost Estimate
Before spawning agents:
- Anthropic: {agent-count} agents × ~{rounds} rounds × ~2K tokens/round × pricing
- sigma-verify (if available): {agent-count} × {providers} XVERIFY calls × ~1K tokens each
- Estimated total: report to user
- ⚠ If estimated > $10: warn user, get confirmation before proceeding

## Exit Checklist

Before moving to Phase 01, confirm ALL of the following. If any item is incomplete, go back and complete it.

- [ ] Memory recall completed
- [ ] System validation passed (defs + memory + inboxes)
- [ ] Sigma-verify status recorded
- [ ] Roster read
- [ ] Complexity tier assessed and reported
- [ ] Agent selection reported to user
- [ ] User confirmed agent selection
- [ ] Prompt decomposition (Q/H/C) completed
- [ ] User confirmed prompt decomposition
- [ ] Cost estimate reported (and confirmed if > $10)

**All items checked → read `phases/01-spawn.md`**
**Any item unchecked → complete it before proceeding**
