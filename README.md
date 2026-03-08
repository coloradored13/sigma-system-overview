# Sigma System

**Persistent, self-sufficient AI agent teams built on deterministic tool discovery.**

This repository documents a system of four interlocking components that together create AI agent teams with persistent memory, compressed communication, and deterministic behavior — all running on markdown files with zero infrastructure.

## Components

### [hateoas-agent](./hateoas-agent/)
A Python framework (~2,000 LOC, 250 tests) that applies HATEOAS to AI agent tool use. The agent starts with one tool; each response tells it exactly what actions are available next. The server decides what's valid, not the LLM.

### [sigma-mem](./sigma-mem/)
A persistent memory system for Claude (~1,100 LOC, 57 tests), exposed as an MCP server. Memory retrieval is itself a HATEOAS state machine — call `recall`, describe your context, get state-dependent actions.

### [ΣComm Protocol](./agent-infrastructure/agents/sigma-comm.md)
Compressed agent-to-agent communication. Format: `[STATUS] BODY |¬ ruled-out |→ actions |#count`. Forces agents to declare what they ruled out (¬) and what they can do next (→).

### [Agent Team Infrastructure](./agent-infrastructure/)
File-based infrastructure for self-sufficient agent teams. Agents boot themselves, read their own memory, communicate via ΣComm inboxes, share a workspace, and declare convergence — all on markdown files.

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full system design, including how the components connect, key design decisions, and what's novel.

## Case Study

See [case-study/REVIEW-6-WALKTHROUGH.md](./case-study/REVIEW-6-WALKTHROUGH.md) for a documented run of the full team protocol — three agents reviewing a codebase with research-grounded expertise, peer communication via ΣComm, and self-declared convergence.

## Getting Started

```bash
git clone --recurse-submodules https://github.com/coloradored13/sigma-system-overview.git
```

If you already cloned without `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

## Structure

```
sigma-system-overview/
  ARCHITECTURE.md                    # System design document
  README.md                         # This file
  hateoas-agent/                    # → git submodule (github.com/coloradored13/hateoas-agent)
  sigma-mem/                        # → git submodule (github.com/coloradored13/sigma-mem)
  agent-infrastructure/
    agents/                         # Agent definitions + protocols
      sigma-lead.md                 # Orchestrator protocol
      sigma-comm.md                 # Communication protocol
      tech-architect.md             # Agent definition
      product-strategist.md         # Agent definition
      ux-researcher.md              # Agent definition
    teams/sigma-review/             # Live team instance
      shared/                       # Workspace, decisions, patterns, roster
      agents/                       # Individual agent persistent memory
      inboxes/                      # ΣComm inbox files
  case-study/
    REVIEW-6-WALKTHROUGH.md         # Documented protocol run
```

## What's novel

1. **HATEOAS for AI agents** — deterministic tool selection via server-side state machines (no other framework does this)
2. **Self-navigating memory** — memory retrieval as a HATEOAS state machine with context-dependent actions
3. **Compressed notation as working memory** — notation designed to give a single Claude instance persistent working memory within limited context, which then evolved into inter-agent communication (ΣComm)
4. **Anti-memories (¬)** — explicitly tracking what is NOT true to prevent false assumptions
5. **Self-sufficient agent teams on files** — agents boot, communicate, and maintain memory with zero infrastructure
6. **Research-grounded agents** — periodic web research stored in compressed notation for current, sourced expertise

## Stats

| Component | Source | Tests | Test Count |
|-----------|--------|-------|------------|
| hateoas-agent | 2,042 LOC | 5,217 LOC | 250 |
| sigma-mem | 1,102 LOC | 426 LOC | 57 |
| ΣComm + agents | 415 lines | — | — |
| Team infra | 510 lines | — | — |
| **Total** | **~4,000 LOC** | **~5,600 LOC** | **307** |
