---
name: sigma-mem dream consolidation tool
description: BUILT and operational — dream() MCP action for ΣComm-aware memory consolidation. 4-phase cycle, dry-run by default, end-to-end verified 26.3.29.
type: project
---

**Status:** BUILT. Verified end-to-end 26.3.29: dream.py exists (828 LOC), tests pass (76/76, 91% coverage), registered in machine.py, MCP tool callable via recall→dream flow. Previous "NOT BUILT" entry was stale.

**Why:** Claude Code auto-dream consolidates project-scoped plain English memory but would corrupt ΣComm notation if it touched sigma-mem files. sigma-dream is the parallel consolidation system that understands compressed notation, checksums, anti-memories, and R[] freshness dates.

**Architecture:**
- Two-layer: auto-dream → project-scoped (plain English) | sigma-mem dream() → global+team (ΣComm)
- dry-run by default (produces "dream journal" report), apply=true only executes safe dedup
- 4 phases: consolidate (dedup), prune (stale R[], old C[]/F[] >90d), reorganize (promote C~→C, detect systemic patterns ≥3), index (integrity snapshot)
- Prune/reorganize are advisory — human reviews before acting

**Implementation:**
- `src/sigma_mem/dream.py` — core consolidation logic (828 LOC)
- `tests/test_dream.py` — 76 tests, 91% coverage
- Registered in `machine.py` via `@mem.on_action("dream")`, available from idle/returning/reviewing states
- Params: scope (personal|team|all), team_name (optional), apply (string, default "false")

**Infrastructure:**
- /sigma-dream skill: `~/.claude/skills/sigma-dream/SKILL.md` — parses args, invokes MCP, formats output
- Remote trigger: `trig_01EtnbDfEPYr2QeqbhUFMnPK` — Mondays 8am MDT
- HATEOAS flow: recall → state transition → dream becomes available

**Known issues (26.3.29):**
- R[] date parser doesn't recognize numbered format (R[1]:) or some undated R[] blocks — 39 false positives across 4 agents
- 4 checksum failures in personal memory (patterns.md×2, user.md×2)
