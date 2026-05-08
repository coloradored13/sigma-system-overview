---
name: TaskCreate before TeamCreate leaks tasks into agent inboxes
description: Lead-side TaskCreate calls made before TeamCreate land in session-scope task list and bleed into spawned agent contexts as misrouted assignments
type: feedback
originSessionId: 89cd1e94-772c-498d-9a5c-dc471d22a04d
---
Don't call TaskCreate before TeamCreate when running a sigma-build or any team-scoped workflow.

**Why:** During build 2026-05-05-block-5-synthesis-carveout C2 (26.5.8), I created 7 lead-tracking tasks (TaskCreate IDs 1-7) before calling TeamCreate to spin up the build team. After TeamCreate, my own TaskUpdate calls returned "Task not found" — the tasks were stranded in session scope (`~/.claude/tasks/{session-uuid}/`). The team-scope task list at `~/.claude/tasks/{team-name}/` was correctly empty. But spawned agents (CQA in particular) saw the orphaned session tasks AS IF they were team assignments, twice receiving lead-track tasks ("C2 Step 6: Cross-model code review", "C2 Step 7-8: Build Status close") routed to them. CQA correctly refused to absorb (process integrity worked), but each refusal cost a turn and risked an eventual sycophantic absorb-instead-of-flag from a less-disciplined agent.

**How to apply:** call TeamCreate FIRST, then TaskCreate inside the team scope. Lead-only mental tracking that doesn't need to surface to agents can stay in conversation context (TodoWrite-style internal notes), or skip task tracking entirely for short build flows. If you genuinely need lead-tracking tasks visible only to lead, consider whether the team-scope is the right home — but never the session scope when a team is about to spawn. Hygiene step: after a session involving leaks, `rm -rf ~/.claude/tasks/{session-uuid}/` to evict stranded entries before next session.

**Recovery if leak occurs:** instruct agents via SendMessage to ignore any task-list assignments matching specific subjects ("C2 Step N", "Cross-model code review", "Build Status", "C3 Step N"); SendMessage > task-list when contradictory; new-class misroutes get one flag, same-class repeats stay silent. CQA's two refusals during this build were calibrated correctly per CLAUDE.md Lead Role Boundaries + Process Integrity Over Completion.
