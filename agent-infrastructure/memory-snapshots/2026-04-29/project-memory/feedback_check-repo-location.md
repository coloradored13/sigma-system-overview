---
name: Check repo location before editing
description: Always check project memory for file locations before editing — repos may have moved (e.g., sigma-optimize moved into sigma-verify)
type: feedback
---

Always check project memory for current file locations before making edits. Repos move.

**Why:** Edited files in ~/Projects/sigma-optimize/ (stale non-repo copy) instead of ~/Projects/sigma-verify/optimize/ (actual repo). Had to copy files over afterward. Would have been caught by reading project memory first.

**How to apply:** At session start, read project memory for any project being modified. The `!start→recall` rule in CLAUDE.md exists for this reason. For sigma-optimize specifically: harness code lives in sigma-verify/optimize/, infra lives in sigma-system-overview (via symlinks).
