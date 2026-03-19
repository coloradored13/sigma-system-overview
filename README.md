# Sigma System

**Persistent, self-sufficient AI agent teams built on deterministic tool discovery.**

This repository documents a system of interlocking components that together create AI agent teams with persistent memory, compressed communication, adversarial quality control, and deterministic behavior — all running on markdown files with zero infrastructure.

## Components

### [hateoas-agent](./hateoas-agent/) v0.2.0
A Python framework (~3,323 LOC, 439 tests) that applies HATEOAS to AI agent tool use. The agent starts with one tool; each response tells it exactly what actions are available next. The server decides what's valid, not the LLM. v0.2 adds multi-agent orchestration: `Orchestrator`, `AsyncRunner`, composable guard conditions, persistence, and visualization.

### [sigma-mem](./sigma-mem/)
A persistent memory system for Claude (~1,724 LOC, 186 tests), exposed as an MCP server. Memory retrieval is itself a HATEOAS state machine — call `recall`, describe your context, get state-dependent actions.

### [ΣComm Protocol](./agent-infrastructure/agents/sigma-comm.md)
Compressed agent-to-agent communication. Format: `[STATUS] BODY |¬ ruled-out |→ actions |#count`. Forces agents to declare what they ruled out (¬) and what they can do next (→).

### [Agent Team Infrastructure](./agent-infrastructure/)
File-based infrastructure for self-sufficient agent teams. 21 agent definitions, 17 agents on the roster, 7 skills, and a shared governance system (directives, patterns, decisions). Agents boot themselves, read their own memory, communicate via ΣComm inboxes, share a workspace, and declare convergence — all on markdown files.

### [Skills Ecosystem](./agent-infrastructure/skills/)
7 orchestration skills covering the full lifecycle:

| Skill | When to use | What it does |
|-------|-------------|--------------|
| `/sigma-review` | You want a multi-perspective analysis of a market, technology, strategy, or codebase | Spawns domain agents (3-8 based on complexity), runs adversarial challenge rounds with DA exit-gate, produces synthesized findings with calibrated estimates |
| `/sigma-build` | You want to build software with multi-agent plan→build→review cycle | Agents plan independently, DA challenges plans before code is written, checkpoint at 50%, adversarial code review at completion |
| `/sigma-evaluate` | After a review completes and you want to score its quality | 3 evaluator agents grade output on 8-criteria rubric (accuracy, completeness, logic, evidence, calibration, actionability, scope-integrity, source-provenance). Judge resolves disagreements |
| `/sigma-audit` | After a review completes and you want to verify process compliance | Fresh opus agent reads archived workspace, checks DA effectiveness, source provenance, analytical hygiene. Produces GREEN/YELLOW/RED verdict with remediation plan |
| `/sigma-retrieve` | During a review when an agent needs deep research on a specific topic | Agentic RAG — decomposes query, runs parallel retrieval, scores sources on relevance/authority/recency, cross-validates, filters noise |
| `/sigma-research` | Before a major review to refresh agent domain knowledge | Agents conduct web research in their expertise areas, store compressed findings in memory for use during reviews |
| `/sigma-init` | Setting up sigma-review for a new project or first-time installation | Initializes team structure, creates project-tier files, validates system configuration |

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
  INTERFACES.md                     # Cross-repo interface contract
  SETUP.md                          # Installation guide
  README.md                         # This file
  setup.sh / setup-project.sh       # Installation scripts
  check-freshness.sh                # Submodule freshness validator
  hateoas-agent/                    # → git submodule (github.com/coloradored13/hateoas-agent)
  sigma-mem/                        # → git submodule (github.com/coloradored13/sigma-mem)
  agent-infrastructure/
    agents/                         # 21 agent definitions + protocols
      sigma-lead.md                 # Orchestrator protocol
      sigma-comm.md                 # Communication protocol
      devils-advocate.md            # Adversarial analyst (exit-gate authority)
      reference-class-analyst.md    # Superforecasting / calibration
      tech-architect.md             # Architecture specialist
      product-strategist.md         # Market / competitive specialist
      ux-researcher.md              # Developer experience specialist
      code-quality-analyst.md       # Code quality specialist
      technical-writer.md           # Documentation specialist
      + 5 market-domain analysts    # macro-rates, sanctions-trade, energy, geopolitical, portfolio
      + 3 regulatory-domain analysts # regulatory, tech-industry, economics
      + 2 dynamic agents            # regulatory-licensing, loan-ops-tech
      _template.md                  # Agent definition template
    skills/                         # 7 orchestration skills
      sigma-review/                 # ANALYZE mode orchestration
      sigma-build/                  # BUILD mode orchestration
      sigma-evaluate/               # Rubric-based evaluation
      sigma-audit/                  # Independent process verification
      sigma-retrieve/               # Agentic RAG pipeline
      sigma-research/               # Domain research refresh
      sigma-init/                   # Team initialization
    teams/sigma-review/             # Live team instance
      shared/                       # Workspace, decisions, patterns, directives, roster
        directives.md               # ANALYZE governance (902 lines)
        build-directives.md         # BUILD governance (341 lines)
        archive/                    # 7 archived review workspaces
      agents/                       # Individual agent persistent memory
      inboxes/                      # ΣComm inbox files
    knowledge-graphs/               # Structured domain knowledge
  case-study/
    REVIEW-6-WALKTHROUGH.md         # Documented protocol run
```

## What's novel

1. **HATEOAS for AI agents** — deterministic tool selection via server-side state machines
2. **Self-navigating memory** — memory retrieval as a HATEOAS state machine with context-dependent actions
3. **Compressed notation as working memory** — notation designed to give a single Claude instance persistent working memory within limited context, which then evolved into inter-agent communication (ΣComm)
4. **Anti-memories (¬)** — explicitly tracking what is NOT true to prevent false assumptions
5. **Self-sufficient agent teams on files** — agents boot, communicate, and maintain memory with zero infrastructure
6. **Adversarial exit-gate** — Devil's Advocate agent controls synthesis timing via mandatory challenge rounds with concede/defend/compromise responses
7. **Analytical hygiene forcing function** — every finding must produce outcome 1 (changes analysis), 2 (confirms with evidence), or 3 (reveals gap). No fourth option.
8. **Zero-dissent circuit breaker** — mandatory self-challenge when all agents agree without tension in R1
9. **Cross-session calibration** — agents accumulate patterns, anti-memories, and failure logs across reviews via persistent memory

## Stats

| Component | Source LOC | Test LOC | Tests |
|-----------|-----------|----------|-------|
| hateoas-agent | 3,323 | 7,630 | 439 |
| sigma-mem | 1,724 | 1,749 | 186 |
| Agent definitions | 2,890 (21 files) | — | — |
| Skills | 1,641 (7 skills) | — | — |
| Directives | 1,243 (ANALYZE + BUILD) | — | — |
| **Total** | **~10,800** | **~9,400** | **625** |

**Reviews completed:** 7 archived (hateoas-agent code reviews, loan-admin tech landscape, VDR market analysis, biotech healthcare M&A, workflow automation, SVB stress test)

> Stats auto-checked by `check-freshness.sh` — run it to verify submodules are current.
