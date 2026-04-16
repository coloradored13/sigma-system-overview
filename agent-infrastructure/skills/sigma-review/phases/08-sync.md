# Phase 08: Infrastructure Sync

**Every step below is mandatory. 12 agent memories drifted undetected because this phase was skipped.**

## Steps

### Step 1: Detect Drift
Compare installed files to sigma-system-overview repo:

| Installed | Repo |
|-----------|------|
| ~/.claude/agents/*.md | agent-infrastructure/agents/ |
| ~/.claude/skills/*/SKILL.md | agent-infrastructure/skills/ |
| ~/.claude/teams/sigma-review/shared/ | agent-infrastructure/teams/sigma-review/shared/ |
| ~/.claude/teams/sigma-review/agents/*/memory.md | agent-infrastructure/teams/sigma-review/agents/ |
| ~/.claude/teams/sigma-review/agents/*/*.md (extras) | agent-infrastructure/teams/sigma-review/agents/ |
| ~/.claude/teams/sigma-review/inboxes/*.md | agent-infrastructure/teams/sigma-review/inboxes/ |

Classify each file:
- **NEW** → auto-sync (copy installed → repo)
- **MODIFIED** → sync + flag for review
- **UNCHANGED** → skip

Skip repo-managed files: sigma-lead.md, sigma-comm.md, SIGMA-COMM-SPEC.md, _template.md

**Agent memory + inboxes + shared MUST sync every session** — no exceptions.

### Step 2: Sync Files
Copy new/modified files from installed location → repo.

### Step 3: Report to User
```
## Infrastructure Sync
{per new/modified file: what changed + where copied}
{or: "No infrastructure changes to sync."}
```

### Step 4: Offer Commit
If files were synced:
```
Commit sync changes? I can stage and commit, or you can review first.
```
Wait for user → git add + commit if approved.

### Step 5: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"sync_complete": true}'
```
Confirm returned phase = `archive`.

## Phase Verification

- [ ] Drift detection completed for all file categories
- [ ] Agent memory and inboxes synced (mandatory every session)
- [ ] Sync report delivered to user
- [ ] Commit offered and resolved (committed, user deferred, or no changes)
- [ ] Orchestrator advanced to archive

**All items verified → continue to `phases/09-archive.md` (session not complete — see SKILL.md Session Deliverables)**
