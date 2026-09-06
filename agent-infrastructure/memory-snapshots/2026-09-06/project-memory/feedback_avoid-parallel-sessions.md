---
name: Avoid parallel sessions on shared state
description: User prefers not to run concurrent Claude Code sessions that write to shared sigma-system-overview infrastructure (memory files, team workspace, decisions.md, patterns.md). Confirmed 26.4.28 after parallel commits collided.
type: feedback
originSessionId: 9f1a80bc-5aee-479d-ac06-d1182791bb06
---
Avoid running concurrent Claude Code sessions that touch shared sigma-system-overview infrastructure (`agent-infrastructure/teams/sigma-review/shared/`, `memory-snapshots/`, etc.). The user has noted parallel runs cause commit collisions and noisy git history.

**Why:** On 26.4.28 a sigma-audit session landed commit `930ab90` (audit verdict + 2 patterns) ~25s before this session's own commit on the same files. Both sessions wrote the same content via sigma-mem MCP, so no data was lost, but the resulting git log is duplicated and harder to read. The user confirmed: "that was expected, but will try to avoid the parallel run in the future."

**How to apply:**
- Before starting work that will write to `~/Projects/sigma-system-overview/` (sigma-mem MCP calls, team file edits, memory-snapshot runs), check `git log -3 --oneline` and recent file mtimes. If commits within the last few minutes look AI-authored on overlapping paths, surface that to the user before proceeding rather than racing.
- If a concurrent session is detected mid-task, finish the current task but flag the collision in the close-out, not silently.
- This applies to sigma-audit, sigma-review, sigma-build, and any /loop or scheduled agent that might be writing to the same shared directories.
