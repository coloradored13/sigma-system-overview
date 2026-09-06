---
name: Parallel implementation engineers
description: sigma-build can spawn multiple implementation-engineer agents (1, 2, N) for independent SQ[] items — use worktree isolation + merge step
type: feedback
---

User suggested spinning up multiple implementation engineers for parallel build work when SQ[] items are independent. No structural reason this can't work.

**Why:** Single implementation-engineer is a bottleneck when build items touch different files. This build (F1) had 5 independent items that could have been 2-3 parallel engineers.

**How to apply:**
- TIER-2+: evaluate SQ[] independence at plan-lock. If 2+ items touch different files → spawn parallel engineers with `isolation: "worktree"`.
- Naming: implementation-engineer-1, -2, -N. Each gets subset of ADRs + ICs.
- File ownership: assign primary file per engineer to avoid merge conflicts.
- Merge step: code-quality-analyst or dedicated merge agent integrates worktrees after individual builds pass.
- Integration tests run AFTER merge, not just per-worktree.
- Watch for: shared file edits (types.py touched by multiple items), integration testing after merge.
