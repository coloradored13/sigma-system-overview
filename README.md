# Sigma System

**Persistent, self-sufficient AI agent teams built on deterministic tool discovery.**

This repository documents a system of interlocking components that together create AI agent teams with persistent memory, compressed communication, adversarial quality control, and deterministic behavior — all running on markdown files with zero infrastructure.

## Components

### [hateoas-agent](./hateoas-agent/) v0.2.0
A Python framework (~3,354 LOC, 452 tests) that applies HATEOAS to AI agent tool use. The agent starts with one tool; each response tells it exactly what actions are available next. The server decides what's valid, not the LLM. v0.2 adds multi-agent orchestration: `Orchestrator`, `AsyncRunner`, composable guard conditions, persistence, and visualization.

### [sigma-mem](./sigma-mem/)
A persistent memory system for Claude (~2,672 LOC, 302 tests), exposed as an MCP server. Memory retrieval is itself a HATEOAS state machine — call `recall`, describe your context, get state-dependent actions.

### [sigma-verify](./sigma-verify/)
A cross-model verification system (~1,776 LOC, 300 tests), exposed as an MCP server. Gateway tool is `init`; available actions are `get_models`, `verify_finding`, `cross_verify`, `challenge`, `check_quotas`. Lets agents stress-test findings against alternative models before accepting them.

### [ΣComm Protocol](./agent-infrastructure/agents/sigma-comm.md)
Compressed agent-to-agent communication. Format: `[STATUS] BODY |¬ ruled-out |→ actions |#count`. Forces agents to declare what they ruled out (¬) and what they can do next (→).

### [Agent Team Infrastructure](./agent-infrastructure/)
File-based infrastructure for self-sufficient agent teams. 29 agent definitions, 22 agents on the active roster, and a shared governance system (directives, patterns, decisions, calibration gates). Agents boot themselves, read their own memory, communicate via ΣComm inboxes, share a workspace, and declare convergence — all on markdown files. Counts are validated in CI by `validate-docs.sh`.

### [Skills Ecosystem](./agent-infrastructure/skills/)
The system ships **11 sigma-prefixed orchestration skills** (plus ~30 auxiliary capability and domain skills). The 7 core lifecycle skills:

| Skill | When to use | What it does |
|-------|-------------|--------------|
| `/sigma-review` | You want a multi-perspective analysis of a market, technology, strategy, or codebase | Spawns domain agents (3-8 based on complexity), runs adversarial challenge rounds with DA exit-gate, produces synthesized findings with calibrated estimates |
| `/sigma-build` | You want to build software with multi-agent plan→build→review cycle | Agents plan independently, DA challenges plans before code is written, checkpoint at 50%, adversarial code review at completion |
| `/sigma-evaluate` | After a review completes and you want to score its quality | 3 evaluator agents grade output on 8-criteria rubric (accuracy, completeness, logic, evidence, calibration, actionability, scope-integrity, source-provenance). Judge resolves disagreements |
| `/sigma-audit` | After a review completes and you want to verify process compliance | Fresh opus agent reads archived workspace, checks DA effectiveness, source provenance, analytical hygiene. Produces GREEN/YELLOW/RED verdict with remediation plan |
| `/sigma-retrieve` | During a review when an agent needs deep research on a specific topic | Agentic RAG — decomposes query, runs parallel retrieval, scores sources on relevance/authority/recency, cross-validates, filters noise |
| `/sigma-research` | Before a major review to refresh agent domain knowledge | Agents conduct web research in their expertise areas, store compressed findings in memory for use during reviews |
| `/sigma-init` | Setting up sigma-review for a new project or first-time installation | Initializes team structure, creates project-tier files, validates system configuration |

Additional sigma orchestration skills: `/sigma-feedback` (post-review calibration loop), `/sigma-optimize` (evolutionary prompt optimization), `/sigma-dream` (memory consolidation cycle), `/sigma-single` (enhanced single-instance analysis). The auxiliary layer includes capability skills (research-analysis, structured-writing, review-critique, data-analysis, etc.), passive always-on skills (skill-improver, assumption-surfacer, memory-compiler, etc.), and domain skills (loan-agency, engineering, legal, finance-accounting, bio-research). See [skills/INDEX.archived.md](./agent-infrastructure/skills/INDEX.archived.md) for the full categorized inventory.

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
  sigma-verify/                     # → git submodule (github.com/coloradored13/sigma-verify)
  agent-infrastructure/
    agents/                         # 29 agent definitions (+ orchestrator, protocol, template, spec)
                                    # See teams/sigma-review/shared/roster.md for the 22 currently active
                                    # Counts validated by validate-docs.sh in CI
    skills/                         # 42 skills — 11 sigma orchestration + auxiliary ecosystem
      sigma-review/                 # ANALYZE mode orchestration
      sigma-build/                  # BUILD mode orchestration
      sigma-evaluate/               # Rubric-based evaluation
      sigma-audit/                  # Independent process verification
      sigma-feedback/               # Post-review calibration loop
      sigma-retrieve/               # Agentic RAG pipeline
      sigma-research/               # Domain research refresh
      sigma-optimize/               # Evolutionary prompt optimization
      sigma-dream/                  # Memory consolidation cycle
      sigma-single/                 # Enhanced single-instance analysis
      sigma-init/                   # Team initialization
      ...                           # + capability, behavioral, passive, protocol, domain skills
      INDEX.archived.md             # Categorized inventory
    teams/sigma-review/             # Live team instance
      shared/                       # Workspace, decisions, patterns, directives, gates, calibration
        directives.md               # ANALYZE governance
        build-directives.md         # BUILD governance
        gate_checks.py              # Pre/post-round gate checks
        audit-calibration-gate.py   # Calibration gate enforcement
        archive/                    # 59 archived review workspaces
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
| hateoas-agent | 3,354 | 7,776 | 452 |
| sigma-mem | 2,672 | 2,677 | 302 |
| sigma-verify | 1,776 | 3,697 | 300 |
| Agent definitions | 4,399 (29 files) | — | — |
| **Total (Python)** | **7,802** | **14,150** | **1,054** |

**Reviews completed:** 59 archived in `agent-infrastructure/teams/sigma-review/shared/archive/`. Topics include hateoas-agent code reviews, loan-admin tech landscape, VDR market analysis, biotech healthcare M&A, workflow automation, SVB stress test, Iran conflict / geopolitical, enterprise AI rollout, sigma-chatroom internal product review, sigma-predict cross-pollination, K-shape economic opportunities, plus multiple meta-reviews of sigma itself (process hardening, architecture, audit remediation).

> Submodule code stats are auto-checked by `validate-docs.sh` (run in CI). Submodule freshness is auto-managed by the `update-submodules.yml` workflow (daily cron) — run `check-freshness.sh` locally to verify.
