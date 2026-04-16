# Phase 09: Archive

**Every step below is mandatory.**

## Steps

### Step 1: Copy Workspace to Archive
Copy workspace to: `shared/archive/{date}-{task-slug}.md`

Add header with review metadata (date, tier, agents, rounds, exit-gate result).

### Step 2: Verify Archive
Confirm:
- Archive file exists at expected path
- Archive contains workspace content
- Archive is non-empty

### Step 3: Session End Validation
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check session-end
```
This runs V22+V23:
- V22: Archive exists + git repo has no uncommitted changes
- V23: Synthesis artifact exists

If validation fails:
- If uncommitted changes: offer to commit
- If synthesis artifact missing: this is a serious error — go back to Phase 06 Step 6
- Re-run validation until it passes

### Step 4: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"archive_verified": true, "session_end_verified": true}'
```
Confirm returned state has `is_terminal: true`.

## Phase Verification

- [ ] Workspace archived with metadata header
- [ ] Archive file verified (exists, non-empty, contains content)
- [ ] Session-end validation passed (V22+V23)
- [ ] Orchestrator advanced to terminal state

**All items verified → continue to `phases/10-shutdown.md` (session not complete — see SKILL.md Session Deliverables)**
