---
name: Multi-model agent vision
description: Long-term plan for model-agnostic sigma-review/sigma-build agents — any model (DeepSeek, Gemma, Llama, etc.) can fill any agent role across reviews
type: project
---

Vision: sigma-review/sigma-build agents are model-agnostic. DeepSeek is product-strategist in one review, Gemma in the next. Any model that can follow the protocol can participate.

**Why:** Reduces Claude dependency, enables cost optimization (cheaper models for simpler roles), cross-model diversity improves analytical quality (different training data = different priors = genuine independence).

**How to apply:** This shapes architecture decisions across several systems:

## Current state (what's already model-agnostic)
- Agent definitions (`~/.claude/agents/*.md`) — role/expertise/protocol, no Claude assumptions in content
- ΣComm protocol — injected via spawn prompt template, any model can receive it
- sigma-mem MCP — any model with MCP access can read/write memory
- `notation-reference.md` ships with sigma-mem (external model entry point)
- sigma-verify already routes to 13 providers — proof that multi-model works

## What needs to change
- **Spawn infrastructure**: TeamCreate + Agent tool are Claude Code primitives. Need model-agnostic spawn layer. ollama-mcp-bridge is heading toward this.
- **`_template.md`**: Has Claude-specific assumptions (TeamCreate, SendMessage) that need abstraction for non-Claude agents
- **MCP access routing**: External models need sigma-mem + workspace read/write access. ollama-mcp-bridge provides MCP routing.

## Gemma's suggestions (26.4.8, evaluated)
- "Distribution not definition" — correct framing. ΣComm is defined, challenge is handing it to new models at spawn time.
- **ΣComm verification loop**: Before a non-Claude model participates, test if it can encode/decode ΣComm correctly. Send natural language → ask for ΣComm translation → sigma-verify scores accuracy. If below threshold, flag "language impaired." Worth building — uses existing sigma-verify infrastructure.
- Move Rosetta to skills — unnecessary, sigma-comm.md already lives in agents/ and gets injected via spawn template. Not buried in CLAUDE.md.
- Hook into 01-spawn.md — already done (spawn template includes codebook). But explicit verification step for non-Claude models is a good addition.

## Architecture when built
```
orchestrator (lead) → reads agent def → selects model provider → 
  injects: role + ΣComm codebook + sigma-mem access + workspace path →
  optional: ΣComm verification loop (sigma-verify) →
  agent runs on {any model} with full protocol compliance
```

## F1 build impact (26.4.8)
- ΣComm translator (Q2) fully designed (ADR[2], IC[1-2]) but DEFERRED — DA challenged: no evidence small models can use expanded ΣComm. Empirical test defined before building.
- Signal codes (ToolSignalCode) on ToolCallRecord enable orchestrators to interpret tool outcomes model-agnostically
- Provenance (trace_id) enables cross-model audit trails
- Multi-implementation-engineer pattern discussed: SQ[] independence → parallel worktree builds → merge step. Enables faster TIER-2+ builds when ready.

## Connections
- ollama-mcp-bridge: F1 COMPLETE (810 tests, DA A-). Model-agnostic MCP routing with provenance + signal codes.
- chatroom: multi-model conversation (NOT STARTED, but architecturally related)
- sigma-verify: already proves multi-model verification works at finding level (13 providers)
- sigma-mem: shared brain across models (MCP-accessible)
