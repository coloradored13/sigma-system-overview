# sigma-mem Session Summary — 2026.3.7

## What Was Built

### sigma-mem v0.2.0 (~/Projects/sigma-mem/)
HATEOAS-navigated memory system for AI agents, exposed as an MCP server. Two layers:

**Personal memory** — Compressed notation in ~/.claude/memory/. Gateway (`recall`) detects conversation context via weighted keyword scoring, transitions to one of 8 states (idle, project_work, team_work, correcting, debugging, returning, reviewing, philosophical), and surfaces only relevant memory with state-dependent actions.

**Team memory** — Persistent agent teams in ~/.claude/teams/{team-name}/. Each agent has personal memory (past findings, calibration, patterns). Team has shared memory (expertise-weighted decisions, cross-agent patterns, roster with domain/wake-for rules).

### Architecture
```
src/sigma_mem/
  machine.py    — Declarative HATEOAS state machine (states, actions, handler bindings)
  handlers.py   — All read/write ops for personal + team memory
  integrity.py  — Checksums, confidence markers, anti-memory verification
  server.py     — MCP server entry point (--memory-dir, --teams-dir)
```
~550 LOC, 57 passing tests, depends on hateoas-agent >= 0.1.0.

### Key Capabilities

| Capability | Implementation |
|-----------|---------------|
| Personal memory recall | `recall(context)` → state detection → relevant memory + available actions |
| Team-aware recall | `recall("working with sigma-review")` → roster + team context auto-loaded |
| Agent boot (one call) | `recall("I'm tech-architect on sigma-review, reviewing code")` → personal memory + team decisions + patterns + roster + teammates |
| Wake check | `wake_check(task, team)` → matches task against roster wake-for fields → returns which agents to spawn |
| Expertise-weighted decisions | `store_team_decision(decision, by, context, team)` → attributed, dissent preserved |
| Path traversal protection | `_validate_path()` using resolve() + is_relative_to() on all file operations |
| State detection | Weighted keyword scoring (phrases > single words), known project/team name matching |
| Integrity | Checksums on compressed blocks, confidence markers (~=tentative), anti-memories (¬=NOT true) |
| Agent memory read | `get_agent_memory(team, agent)` → cross-agent visibility |

### File Structure Created

```
~/.claude/
  memory/                          # personal memory (ΣMem compressed notation)
    MEMORY.md                      # core identity, always loaded
    projects.md, decisions.md, corrections.md, patterns.md, ...
  teams/
    sigma-review/
      shared/
        roster.md                  # 3 agents, domains, wake-for rules
        decisions.md               # expertise-weighted, attributed
        patterns.md                # cross-agent observations
      agents/
        tech-architect/memory.md   # 3 rounds of review history
        product-strategist/memory.md
        ux-researcher/memory.md
  agents/
    sigma-lead.md                  # orchestrator with boot/persistence protocol
    sigma-comm.md                  # compressed communication protocol
    tech-architect.md              # specialist definition
    product-strategist.md
    ux-researcher.md
  CLAUDE.md                        # directive: call sigma-mem recall before reading files
```

### ΣComm Protocol (docs/sigma-comm-protocol.md)
Compressed agent-to-agent communication format:
```
[STATUS] body |¬ ruled-out |→ can-do-next |#count
✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry
```
Tested across 3 review rounds with 3 agents. Protocol works; team messaging infra was lossy (idle notification summaries delivered, full message bodies did not).

### How Persistent Teams Work

1. User says "spin up sigma-review to review X"
2. Lead calls `wake_check` to decide who to spawn based on task
3. Lead calls `recall("I'm {agent} on sigma-review, {task}")` for each agent
4. Recall returns agent boot package: personal memory + team decisions + patterns + roster + teammates
5. Lead injects boot package into agent spawn prompt
6. Agents work with full history — past findings, calibration, known codebases
7. At session end, lead persists new findings to agent memory files + shared decisions

Agents don't need MCP access. Lead mediates all memory operations.

### What Was Fixed During Session

| Fix | File | Details |
|-----|------|---------|
| Path traversal vulnerability | handlers.py | Added `_validate_path()` with resolve + is_relative_to |
| State detection brittleness | handlers.py | Replaced first-match keywords with weighted scoring system |
| Checksum docstring mismatch | integrity.py | Aligned docstring to actual split-on-pipe-and-comma behavior |
| Dead code | handlers.py | Removed unused `_extract_actions()` |
| Missing memory_dir passthrough | handlers.py | `_detect_state(context)` → `_detect_state(context, memory_dir)` |
| Unused import | handlers.py | Removed `import re` after dead code removal |

### Test Coverage (57 tests)

```
tests/test_handlers.py  — 19 tests: path validation, state detection, recall, store, search, update belief
tests/test_integrity.py — 13 tests: checksums, confidence, anti-memories, file integrity
tests/test_teams.py     — 25 tests: roster, team decisions, patterns, agent memory, wake check,
                           store team decision, agent identity detection, agent boot, team-aware recall
```

### Design Decisions Made

1. **Who writes shared memory** → Expertise-weighted. Domain expert has primary authority. Dissent recorded as |ctx.
2. **What triggers persistence** → Each agent has own memory. Lead persists findings at session end.
3. **Agent visibility** → Full cross-agent read access. More visibility = richer collaboration.
4. **Memory hierarchy** → User sigma-mem > Team shared memory > Agent personal memory.
5. **Selective wake** → Not all agents for all tasks. Roster wake-for fields drive matching.
6. **Lead mediates boot** → Agents don't call MCP directly. Lead injects boot package into spawn prompt.

### What's NOT Done / Known Gaps

- No git remote / not published to GitHub or PyPI
- hateoas-agent dependency is local editable install (must publish before sigma-mem can pip install externally)
- Substring keyword matching in state detection ("fix" matches "prefix") — word-boundary regex would be better
- No automatic checksum recalculation on memory edits
- No memory consolidation/pruning automation
- Team messaging infra doesn't reliably deliver full message bodies (only idle summaries arrive)
- No integration test exercising the full MCP serve() path

### Lineage
This session continued from a prior conversation that built:
- ΣMem compressed notation system
- HATEOAS memory navigation pattern
- sigma-mem MCP server (v0.1.0)
- Integrity safeguards (checksums, anti-memories, confidence markers)

This session added:
- ΣComm agent communication protocol
- Persistent team memory architecture
- Agent boot loop (one-call recall with identity detection)
- 3 rounds of agent team reviews (each building on previous)
- Security hardening, state detection rewrite, 57 tests
- README, LICENSE, git init, v0.2.0 commit
