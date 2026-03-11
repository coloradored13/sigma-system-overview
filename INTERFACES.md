# Cross-Repo Interface Contract

This document defines the coupling points between sigma-system-overview, sigma-mem, and hateoas-agent. Changes to any interface listed here require coordinated updates across repos.

Last verified: 2026-03-11

## Dependency Chain

```
sigma-system-overview (agent definitions, setup, skills)
    └── sigma-mem (MCP server, memory tools, integrity checks)
            └── hateoas-agent (StateMachine, serve())
```

## Version Pinning

setup.sh pins both dependencies to specific commit hashes:
- `HATEOAS_AGENT_PIN` — hateoas-agent commit
- `SIGMA_MEM_PIN` — sigma-mem commit

**Upgrade procedure:**
1. Update the pin hash in setup.sh
2. Run `./setup.sh` (forces reinstall when pin changes)
3. Run sigma-mem tests: `~/.claude/sigma-venv/bin/python -m pytest`
4. If tests pass, commit the new pin

## sigma-mem MCP Tool Interface

These tool names and parameters are referenced in agent definitions (sigma-lead.md, all agent Boot/Persistence sections). Renaming any tool or parameter breaks all agents.

### Universal tools
| Tool | Parameters | Referenced by |
|------|-----------|---------------|
| `recall` | `context` | CLAUDE.md, all agents (Boot) |
| `search_memory` | `query` | CLAUDE.md |
| `store_memory` | `entry`, `file` | CLAUDE.md, all agents |
| `check_integrity` | — | session-end checklist |
| `get_meta` | — | — |

### Project tools
| Tool | Parameters | Referenced by |
|------|-----------|---------------|
| `get_project` | `name` | CLAUDE.md |
| `get_decisions` / `log_decision` | `choice`, `rationale`, `alternatives` | CLAUDE.md, sigma-lead |
| `get_failures` / `log_failure` | `what`, `why` | CLAUDE.md |
| `get_corrections` / `log_correction` | `error`, `fix` | CLAUDE.md |
| `update_belief` | `old`, `new` | — |
| `verify_beliefs` | — | — |

### Team tools (all require `team_name`)
| Tool | Additional Parameters | Referenced by |
|------|----------------------|---------------|
| `get_roster` | — | sigma-lead |
| `get_team_decisions` | — | sigma-lead, all agents |
| `get_team_patterns` | — | sigma-lead, all agents |
| `get_agent_memory` | `agent_name` | all agents (Boot, Promotion) |
| `wake_check` | `task` | sigma-lead |
| `validate_system` | — | sigma-lead |
| `store_team_decision` | `decision`, `by`, `context`, `weight` | all agents (Persistence) |
| `search_team_memory` | `query` | sigma-lead |
| `store_agent_memory` | `entry`, `agent_name` | all agents (Persistence, Promotion) |
| `store_team_pattern` | `pattern`, `agents` | all agents (Persistence) |

### Critical parameters
- **`tier`** — `"global"` or `"project"`. Routes to `~/.claude/teams/` or `<project>/.claude/teams/`. Used in all `store_*` and `get_*` team tools.
- **`weight`** — `"primary"` or `"advisory"`. Used in `store_team_decision`.
- **`team_name`** — defaults to `"sigma-review"`. Hardcoded in all agent definitions.

## Memory Block Types

Recognized by sigma-mem integrity checker (`extract_confidence()`):

| Prefix | Confidence | Description |
|--------|-----------|-------------|
| `C[` | confirmed | Confirmed beliefs |
| `C~[` | tentative | Tentative beliefs |
| `~[` | tentative | Alternative tentative marker |
| `P[` | promoted | Promoted learnings (project → global) |
| `R[` | research | Research entries with sources |
| `¬[` | anti | Anti-memories (what is NOT true) |
| other | unknown | Unrecognized format |

**Adding a new block type** requires:
1. Document in SIGMA-COMM-SPEC.md
2. Add pattern to `sigma_mem/integrity.py:extract_confidence()`
3. Add test in `sigma_mem/tests/test_integrity.py`
4. Update this table

## hateoas-agent API Surface

sigma-mem imports and uses:

```python
from hateoas_agent import StateMachine, serve

# StateMachine methods used:
StateMachine.gateway()
StateMachine.action()
StateMachine.on_gateway()
StateMachine.on_action()
StateMachine.validate()
StateMachine.get_gateway()
StateMachine.get_actions_for_state()
StateMachine.get_all_action_names()
StateMachine.get_handler()
StateMachine.get_transition_metadata()

# Server entry point:
serve(machine, name="sigma-mem")
```

Changes to any of these method signatures break sigma-mem at runtime.

## File Path Conventions

Both repos assume these paths:

| Path | Purpose | Used by |
|------|---------|---------|
| `~/.claude/teams/sigma-review/` | Global team tier | setup.sh, all agents |
| `~/.claude/teams/sigma-review/agents/{name}/memory.md` | Agent memory | all agents (Boot) |
| `~/.claude/teams/sigma-review/agents/{name}/inbox/` | Agent inbox | sigma-lead, all agents |
| `~/.claude/teams/sigma-review/shared/` | Team shared files | setup.sh, sigma-lead |
| `~/.claude/teams/sigma-review/shared/portfolio.md` | Project portfolio | sigma-lead (Promotion) |
| `<project>/.claude/teams/sigma-review/` | Project team tier | setup-project.sh, agents with tier:project |
| `~/.claude/sigma-venv/` | Python venv | setup.sh, ~/.claude.json MCP config |

## ~/.claude/CLAUDE.md

setup.sh injects a "recall-first behavior" block (search for `RECALL_MARKER`). The file may contain additional user-managed content. setup.sh checks for the marker before appending to avoid duplication.

Referenced tool names in CLAUDE.md: `recall`, `search_memory`, `get_project`, `store_memory`, `log_decision`, `log_correction`, `log_failure`, `check_integrity`.

## Sync Mechanisms

| Direction | Mechanism | Scope |
|-----------|-----------|-------|
| repo → installed | `./setup.sh` | agents, skills, shared files, venv, MCP config |
| installed → repo | `./setup.sh pull` | agents, skills, shared files |
| sigma-mem changes | Update `SIGMA_MEM_PIN` in setup.sh, rerun | venv package |
| hateoas-agent changes | Update `HATEOAS_AGENT_PIN` in setup.sh, rerun | venv package |

## Breaking Change Checklist

Before changing any interface:

- [ ] Grep agent definitions for the tool/parameter name being changed
- [ ] Check CLAUDE.md for references
- [ ] Check sigma-lead.md orchestration steps
- [ ] Check SKILL.md files for references
- [ ] Update INTERFACES.md (this file)
- [ ] Update version pin if changing sigma-mem or hateoas-agent
- [ ] Run sigma-mem tests
- [ ] Run `./setup.sh` to redeploy
