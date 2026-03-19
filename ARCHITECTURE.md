# Sigma System Architecture

**A system for persistent, self-sufficient AI agent teams built on deterministic tool discovery.**

## What this is

Four interlocking components that together create AI agent teams with persistent memory, compressed communication, and deterministic behavior:

1. **hateoas-agent** — A Python framework that applies HATEOAS (Hypermedia As The Engine Of Application State) to AI agent tool use
2. **sigma-mem** — A persistent memory system for Claude, built on hateoas-agent, exposed as an MCP server
3. **ΣComm** — A compressed communication protocol for agent-to-agent messaging
4. **Agent Team Infrastructure** — File-based infrastructure for self-sufficient agent teams with persistent identity

## The core insight

LLM agents today get a flat list of tools and guess which one to call. With 10 tools this works. With 100, accuracy drops. The industry response has been probabilistic — RAG over tool descriptions, semantic search, etc.

hateoas-agent takes a different approach: **make the wrong choice impossible**. The agent starts with one gateway tool. Each response tells it exactly which actions are available right now, based on the current state. The server decides what's valid, not the LLM.

This principle — **deterministic state-driven navigation** — is then applied recursively:
- hateoas-agent uses it for tool discovery
- sigma-mem uses it for memory retrieval (recall → state-dependent actions)
- Agent teams use it for coordination (each agent advertises what they can do next)

## Component details

### hateoas-agent

A Python library (~3,323 LOC, 439 tests) that implements HATEOAS for AI agent tool use.

**How it works:**
```
Agent starts → calls gateway tool → gets result + "Available actions for this state"
           → calls an action → gets result + new available actions
           → state changes → different actions appear
```

The framework handles:
- **Declarative state machines** — define states and transitions, framework enforces them
- **Three API styles** — action-centric (recommended), state-centric, class-based (Resource)
- **Security** — server-side state validation, phantom tool detection, parameter filtering
- **Discovery mode** — run wide open, observe transitions, auto-generate the state machine
- **MCP server adapter** — expose any state machine as an MCP tool server
- **Startup validation** — catch misconfiguration before the first API call
- **Visualization** — generate Mermaid diagrams from state machines
- **Persistence** — checkpoint and restore state machine state

```
~/Projects/hateoas-agent/
  src/hateoas_agent/
    state_machine.py    # Declarative API
    resource.py         # Class-based API
    registry.py         # Routes tool calls, manages state
    runner.py           # Agent loop (Claude API)
    mcp_server.py       # MCP adapter
    validation.py       # Action validation
    visualization.py    # Mermaid diagram generation
    persistence.py      # Checkpoint/restore
    composite.py        # Multi-resource composition
    errors.py           # Error hierarchy
    types.py            # Data types
    advertisement.py    # Result formatting
  tests/                # 261 tests across 19 test files
  examples/             # 12 working examples
```

**Key design decisions:**
- Library, not framework — integrates with LangChain, CrewAI, or standalone
- Zero hard dependencies — anthropic and mcp are optional
- `_state` convention — handlers return `{"result": ..., "_state": "current_state"}`, framework strips `_state` before sending to LLM
- Server-side enforcement — the LLM never sees invalid options, can't call them even if it tries

### sigma-mem

A persistent memory system for Claude (~1,724 LOC, 186 tests), exposed as an MCP server. Built on hateoas-agent.

**How it works:**
The memory system is itself a HATEOAS state machine. Claude calls `recall` (the gateway), describes the current context, and the system detects the conversation type (project work, debugging, being corrected, team work, etc.) and returns relevant memories with state-dependent actions.

```
Claude calls recall("reviewing hateoas-agent with the team")
  → system detects: team_work
  → returns: core identity + team roster + relevant project memories
  → advertises: get_team_decisions, get_agent_memory, wake_check, store_team_decision...

Claude calls get_team_decisions("sigma-review")
  → returns: expertise-weighted decisions from past reviews
  → advertises: same actions (state unchanged)
```

**Memory architecture:**
- **Core memory** — compressed identity, user model, behavioral rules (~200 lines)
- **Topic files** — decisions, corrections, failures, patterns, projects, conversations
- **Team memory** — persistent agent teams with shared decisions and individual agent memory
- **Compressed notation** — pipe-separated fields, checksums, confidence scores

```
~/Projects/sigma-mem/
  src/sigma_mem/
    __init__.py     # Package init
    server.py       # MCP server entry point
    machine.py      # State machine definition (26 actions across 8 states)
    handlers.py     # Handler implementations
    integrity.py    # Memory integrity checks
  docs/
    sigma-comm-protocol.md  # ΣComm specification
```

**Key design decisions:**
- HATEOAS navigation — no static routing table, follow → links
- Compressed notation — fits more signal into limited context windows
- Anti-memories (¬) — explicitly track what is NOT true to prevent false assumptions
- Human-auditable — all memory is markdown files, no database

### ΣComm Protocol

A compressed notation system that originated as **working memory for a single Claude instance**, then evolved into an inter-agent communication protocol.

**Origin:** Claude's persistent memory is ~2,000 lines across ~10 files. Every line loaded into context costs tokens. Compressed notation (pipe-separated fields, checksums, confidence scores, anti-memories) was developed to pack maximum signal into that limited space — giving a single Claude instance something resembling working memory rather than just file reads. When agent teams needed efficient communication, the same notation was already battle-tested. ΣComm is the inter-agent application of this same system.

**Two applications of one system:**
1. **Working memory** — sigma-mem's memory files use compressed notation to maximize the value of every line loaded into context (the single-instance origin)
2. **Agent communication** — ΣComm applies the same notation to inbox messages, workspace entries, and peer-to-peer messaging

**Format:**
```
[STATUS] BODY |¬ ruled-out |→ actions |#count
```

**Status codes:** ✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry

**Example — prose vs ΣComm:**
```
Prose (35+ tokens):
"I reviewed the auth module and found 3 issues: JWT expiry not checked,
MD5 passwords, no rate limiting. Session management and CORS look fine."

ΣComm (~25 tokens):
✓ auth-review: jwt-expiry-unchecked(!), pwd-md5>bcrypt, no-rate-limit
  |¬ session-mgmt, cors |→ fix-jwt(small), fix-hash(needs-migration) |#3
```

**Key innovations:**
- **Anti-messages (¬)** — forces agents to say what they ruled out, preventing assumption-based errors
- **Action advertisements (→)** — HATEOAS-style: each message declares what the sender can do next
- **Checksums (#)** — receiver verifies they decoded the right number of items
- **Structured forcing** — the format requires information that prose tends to bury or omit

### Agent Team Infrastructure

File-based infrastructure for self-sufficient agent teams with persistent identity.

**Architecture:**
```
~/.claude/agents/              # 21 global agent definitions
  sigma-lead.md                # Orchestrator protocol
  sigma-comm.md                # Communication protocol
  devils-advocate.md           # Adversarial analyst (exit-gate authority)
  reference-class-analyst.md   # Superforecasting / calibration specialist
  tech-architect.md            # Architecture specialist
  product-strategist.md        # Product/market specialist
  ux-researcher.md             # Developer experience specialist
  code-quality-analyst.md      # Code quality specialist
  technical-writer.md          # Documentation specialist
  + 5 market-domain agents     # macro-rates, sanctions-trade, energy, geopolitical, portfolio
  + 3 regulatory-domain agents # regulatory, tech-industry, economics
  + 2 dynamic agents           # created mid-review when DA identifies domain gaps
  _template.md                 # Canonical agent definition template

~/.claude/skills/              # 7 orchestration skills
  sigma-review/                # ANALYZE mode — multi-agent research with adversarial rounds
  sigma-build/                 # BUILD mode — plan→challenge→build→review
  sigma-evaluate/              # Rubric-based output evaluation (3 evaluators + judge)
  sigma-audit/                 # Independent process quality verification
  sigma-retrieve/              # Agentic RAG pipeline
  sigma-research/              # Agent domain research refresh
  sigma-init/                  # Team initialization

~/.claude/teams/sigma-review/  # Team instance
  shared/
    roster.md                  # 17 agents with domains + wake-for rules
    directives.md              # ANALYZE governance (902 lines)
    build-directives.md        # BUILD governance (341 lines)
    decisions.md               # Expertise-weighted decisions with attribution
    patterns.md                # Cross-agent observations (142 lines, growing)
    workspace.md               # Current task (agents read/write collaboratively)
    orchestrator-config.py     # Automated phase transition CLI
    archive/                   # 7 archived review workspaces
  agents/{name}/
    memory.md                  # Persistent personal memory (agent self-maintains)
  inboxes/{name}.md            # Markdown/ΣComm inbox (summarize-and-clear)
```

**How a review works:**

```
Round 0 (boot):
  Lead reads roster → wake_check → which agents does this task need?
  Lead initializes workspace with task description
  Lead spawns agents in parallel with boot prompt (paths only — no memory injection)

  Each agent (self-sufficient):
    1. Reads their own agent definition
    2. Reads ΣComm protocol
    3. Reads their own persistent memory (including domain research)
    4. Reads their inbox, processes messages, summarizes in ΣComm, clears
    5. Reads shared workspace (task + what peers have written)
    6. Does their analysis
    7. Writes findings to their workspace section
    8. Sends ΣComm messages to peer inboxes
    9. Updates their own memory
    10. Declares convergence status in workspace

Round N (communication):
  Lead checks workspace convergence section
  Any agent with ◌ or unread inbox → re-spawn
  Agents read peer messages, respond, update convergence
  Repeat until all ✓

User interaction:
  @agent-name → message written to agent's inbox, agent spawned with shared context
```

**Key design decisions:**
- **Self-sufficient agents** — agents read their own files at boot, no memory injection by the lead
- **Markdown inboxes** — ΣComm messages with summarize-and-clear pattern
- **Shared workspace** — single source of truth for current task, agent-declared convergence
- **Expertise-weighted decisions** — domain expert has primary weight, dissent preserved
- **Selective wake** — not every task needs every agent, wake-for matching reduces cost
- **Research protocol** — agents do web research to ground expertise in current sources, stored as ΣComm in memory, refreshed periodically

**Known limits:**
- **Concurrent writes** — agents write to named subsections they own in workspace, which avoids collisions in practice. For shared files (decisions, patterns), the lead serializes writes. This works for ~5 agents; beyond that, a write-coordination protocol would be needed.

## How the pieces connect

```
┌─────────────────────────────────────────────────┐
│                   User                          │
│            (plain language)                      │
└─────────────┬───────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│              ΣLead (orchestrator)                │
│  Reads roster, wakes agents, manages rounds     │
│  Translates ΣComm ↔ plain language for user     │
└──────┬──────────┬──────────┬────────────────────┘
       │          │          │
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  tech-   │ │ product- │ │   ux-    │
│architect │ │strategist│ │researcher│
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │ ΣComm      │ ΣComm      │ ΣComm
     └────────────┼────────────┘
           (peer inboxes)
              │
     ┌────────┴────────┐
     ▼                 ▼
┌──────────┐    ┌──────────┐
│  Shared  │    │  Agent   │
│Workspace │    │ Memory   │
│decisions │    │(personal)│
│ patterns │    │ research │
└──────────┘    └──────────┘
              │
              ▼
┌─────────────────────────────────────────────────┐
│              sigma-mem (MCP server)              │
│     HATEOAS-navigated memory retrieval           │
│     Compressed notation, anti-memories           │
└─────────────┬───────────────────────────────────┘
              │ built on
              ▼
┌─────────────────────────────────────────────────┐
│            hateoas-agent (framework)             │
│     Deterministic tool discovery for AI agents   │
│     State machines, security, MCP adapter        │
└─────────────────────────────────────────────────┘
```

## Evidence it works

The system has completed 7+ reviews across codebases, market analyses, and stress tests. Team composition has grown from 3 core agents to 17 roster agents with adversarial layer.

**Review history:**
- Reviews 1-3 (sigma-mem): correctness issues → polish → architecture review
- Review 4 (hateoas-agent): 9 findings, grades arch A-, security A, DX B+
- Review 5 (hateoas-agent delta): 6 resolved, 3 remaining, DX A-
- Review 6 (full protocol test): all agents self-sufficient, ΣComm operational, research-grounded. Ship decision: GO
- Review 7 (Iran conflict / geopolitical): 5 market-domain agents, DA identified herding in R1 (zero-dissent across all agents), stress test round caught 3 biases. Led to zero-dissent circuit breaker protocol
- Reviews 8-9 (loan-admin tech landscape): 5+DA agents, dynamic agent creation (regulatory-licensing-specialist created mid-review per DA gap identification), 5-round review, /sigma-audit run post-review (YELLOW→remediated to GREEN)
- Review 10 (VDR market analysis): 5+DA, 3 rounds, CAGR scope-inflation pattern confirmed cross-review
- Review 11 (biotech healthcare M&A): 6+DA, 3 rounds, AI-as-structural-accelerant framework, doc-generation-heredoc pattern discovered
- Review 12 (workflow automation): highest R3 engagement grades observed (A-/A across all agents), genuine analytical shift under DA pressure (automation-first→PI-first-conditional)

**Observed patterns (from patterns.md, 142 lines):**
- Review severity decreases with iteration (correctness → polish → acceptance)
- Independent agents converge on the same issues from different domain angles
- 2-agent teams herd faster than 5-agent teams — always include DA from R2
- Data-backed DA challenges produce behavioral change; rhetorical challenges produce performative concession
- Teams replace old consensus with new consensus under DA pressure → DA must stress-test new consensus too
- Herding detected and addressed in 3+ reviews (Iran, loan-admin, workflow-automation)
- Dynamic agent creation fills genuine domain gaps (regulatory-licensing-specialist, loan-ops-tech-specialist)

## What's novel

1. **HATEOAS for AI agents** — deterministic tool selection via server-side state machines.

2. **Self-navigating memory** — memory retrieval as a HATEOAS state machine where available actions change based on detected context. No static routing table.

3. **Compressed notation as working memory** — a notation system designed to give a single Claude instance persistent working memory within its ~2,000-line budget, which then naturally extended to inter-agent communication (ΣComm). One system, two applications.

4. **Anti-memories and anti-messages** — explicitly tracking what is NOT true (¬) to prevent false assumptions. Applied to both persistent memory and agent communication.

5. **Self-sufficient agent teams on files** — persistent agent teams that boot themselves, communicate through inboxes, maintain their own memory, and declare convergence — all on markdown files with zero infrastructure.

6. **Adversarial exit-gate** — Devil's Advocate agent controls synthesis timing via mandatory challenge rounds. Agents must concede, defend, or compromise on each DA challenge with evidence. DA grades engagement quality and can FAIL the exit-gate to force additional rounds.

7. **Analytical hygiene forcing function** — every finding must produce outcome 1 (changes analysis), 2 (confirms with evidence), or 3 (reveals gap). No fourth option. Prevents checks from being checkboxes.

8. **Zero-dissent circuit breaker** — mandatory self-challenge when all agents agree without tension in R1. Addresses documented herding pattern (7 consecutive reviews with zero R1 dissent).

9. **Cross-session calibration** — agents accumulate patterns, anti-memories, and failure logs across reviews via persistent memory. Each review makes future reviews more informed.

## Stats

| Component | Source LOC | Test LOC | Tests | Files |
|-----------|-----------|----------|-------|-------|
| hateoas-agent | 3,323 | 7,630 | 439 | 19 modules, 25 test files, 12 examples |
| sigma-mem | 1,724 | 1,749 | 186 | 5 modules, 5 test files |
| Agent definitions | 2,890 | — | — | 21 agent files |
| Skills | 1,641 | — | — | 7 skills |
| Directives | 1,243 | — | — | ANALYZE (902) + BUILD (341) |
| **Total** | **~10,800** | **~9,400** | **625** | |

**Team scale:** 17 roster agents, 7 skills, 7 archived reviews, 142-line cross-agent pattern log
