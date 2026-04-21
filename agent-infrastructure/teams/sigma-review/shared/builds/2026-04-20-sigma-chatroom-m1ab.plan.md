# sigma-build plan: sigma-chatroom-m1ab

## Meta
- created: 2026-04-20
- locked: 2026-04-21
- build-id: 2026-04-20-sigma-chatroom-m1ab
- tier: BUILD TIER-2
- status: plan-locked
- plan-exit-gate: PASS
- plan-belief: P=0.87
- plan-engagement-grade: A-
- plan-rounds-used: 2/5 (budget preserved)
- build-exit-gate: PENDING
- build-belief: P=0.00
- output-label: M1a (two-model streaming) + M1b (native tool-use + tool-exec loop), + preliminary Q3 forward plan for M1c→M4 with empirical revision hooks
- source-plan: ~/.claude/plans/look-for-the-plan-snazzy-giraffe.md
- scratch-workspace: ~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab/c1-scratch.md
- archive: ~/.claude/teams/sigma-review/shared/archive/2026-04-20-sigma-chatroom-m1ab-workspace.md
- infrastructure-known-gap: sigma-verify cross_verify hung 3x this session (DA-r1, TA-r1, TA-r2). XVERIFY[ADR3] documented as §2h infra-gap with compensating factors. Post-C1 troubleshoot queued.

---

## Context

Build M1a + M1b of sigma-chatroom — a local Streamlit web app (later M2+) where models from different providers (Anthropic API + Ollama cloud initially; 13 providers by M1c) participate in shared, streamed conversations with optional access to shared memory via native per-SDK tool-use. Research instrument, not product. Repo `~/Projects/sigma-chatroom/` does not exist; to be created by C2.

**M1a** — two-model streaming (Anthropic claude-opus-4-7 + Ollama cloud devstral-2:123b-cloud), RoundRobin policy, JSONL persistence with `schema_version="1"`, CLI streaming to stdout, NO tools. Proves the core streaming + persistence substrate.

**M1b** — native per-SDK tool-use (Anthropic content-blocks + Ollama OpenAI-compat tool_calls) with TurnEngine tool-exec loop (cap 5 calls/turn), YieldNext + Random policies, echo-tool fixture, MetricsCollector baseline, ToolCallRecord observability (preceding_text + position_in_turn + latency_ms + result), raw event capture default-on when `tool_use_reliability != "reliable"`. Proves the per-SDK tool-use adapter layer + cross-SDK integration.

**Q3 forward plan** — preliminary M1c → M2 → M3 → M4 planning with revision hooks tied to M1a/b empirical findings. Planning artifact only (not C2 code scope).

---

## Prompt Understanding

### Q[] — what to build
- **Q1:** M1a two-model streaming (Anthropic + Ollama cloud), RoundRobin, JSONL persist, CLI stdout, NO tools
- **Q2:** M1b native per-SDK tool-use + TurnEngine tool-exec loop (≤5 calls/turn), YieldNext + Random policies, ToolCallRecord observability, MetricsCollector baseline
- **Q3:** Preliminary forward build-out plan for M1c (other SDK families) → M2 (Streamlit MVP) → M3 (sigma-mem wiring + metrics panel + v1 ship) → M4 (more tools + embedding metrics) with revision hooks tied to M1a/b findings

### H[] — hypotheses TESTED, not assumed (all addressed in ADRs below)
- H1: Purpose-built `providers/` beats abstracting sigma-verify's `clients.py` → CONFIRMED (ADR[1])
- H2: Native per-SDK tool-use beats text-convention/ollama-mcp-bridge → CONFIRMED with feasibility gap (ADR[2], SQ6c smoke test added)
- H3: Tool-exec loop belongs in TurnEngine; Provider.stream() = one SDK call → CONFIRMED with DB re-run (ADR[3])
- H4: message_mapping.py is elevated-risk; per-SDK round-trip tests as merge gate → CONFIRMED + expanded to 3-tier (ADR[4])
- H5: 60% context budget + `len//4` estimate adequate for M1 → CONFIRMED with revision hook (ADR[5])
- H6: Raw event capture default-on when `tool_use_reliability != "reliable"` → CONFIRMED (ADR[6])
- H7: OpenAI-shaped canonical Message; adapters own translation → CONFIRMED with escape-hatches locked (ADR[4])

### C[] — constraints
- C1: TIER-2 BUILD, research instrument, NOT security-critical
- C2: `~/Projects/sigma-chatroom/` does not exist — C2 creates it
- C3: Study `~/Projects/sigma-verify/src/sigma_verify/clients.py` for patterns — DO NOT IMPORT (hard-stop)
- C4: No `ollama-mcp-bridge` — SDK native tool-use only (hard-stop)
- C5: Streaming from day 1 (M1a baseline), not M4
- C6: M1 seed pair: claude-opus-4-7 + devstral-2:123b-cloud (preferred); deepseek-v3.2:cloud + qwen3.5:cloud as alternates
- C7: SDK deps for M1a/b: `anthropic`, `openai` (for Ollama OpenAI-compat), `pydantic`. Streamlit + mcp deferred to M2/M3.
- C8: `schema_version: "1"` on every JSONL record from day 1 (not retrofitted)
- C9: Out-of-scope hard-stops: M1c, M2 (Streamlit), M3 (sigma-mem wiring; echo tool only in M1b), M4, ollama-mcp-bridge
- C10: `"memory"` NOT valid Turn.speaker value (vestigial). ProviderSpec.key or "human" only.

---

## Scope Boundary

### Implements (C2 code scope)
**M1a (~17.5h parallelized):**
- `providers/base.py` — Message, StreamEvent (5-kind), ToolSchema, CompleteResult, ToolCallRecord, Provider Protocol (no `complete()` per DA GP2)
- `providers/anthropic_client.py` — streaming via `messages.stream` context-manager
- `providers/ollama_client.py` — OpenAI-compat streaming via `openai.AsyncOpenAI` with `include_usage=True`
- `providers/message_mapping.py` — streaming-only paths (Anthropic content↔canonical expand/collapse; Ollama identity)
- `providers/errors.py` — error classification taxonomy
- `providers/__init__.py` — re-exports
- `roster.py` — ProviderSpec catalog + PROVIDERS dict + `registry.available()` helper (merged per DA GP1, no separate `registry.py`)
- `conversation.py` — Turn, ConversationState, PreambleVariant (Literal type)
- `turn_engine.py` — RoundRobinPolicy + `advance_stream`; context truncation helper
- `persistence.py` — JSONL write+replay, `schema_version="1"`, replay INVs
- `cli.py` — argparse, streaming tokens to stdout with flush, Ctrl-C flush, JSONL writes
- Tests cluster D (SQ12a-k)

**M1b (~23.5h parallelized):**
- `providers/tool_schema.py` — ToolSchema → Anthropic tool format + Ollama OpenAI-compat function format
- `providers/anthropic_client.py` — tool-use streaming (tool_use content-blocks → `kind="tool_call"`)
- `providers/ollama_client.py` — tool-use streaming (tool_calls delta → `kind="tool_call"`)
- `providers/message_mapping.py` — tool-use paths with `preceding_text_per_tool_call` escape-hatch
- `turn_engine.py` — tool-exec loop (cap 5, INV2 final-text-response, INV4 phase sequencing, INV6 `kind="tool_result"` emission)
- `turn_engine.py` — YieldNextPolicy (case-sensitive, trailing punctuation stripped, multiple @next: uses last, self-nom fallback) + RandomPolicy (optional seeded rng)
- `persistence.py` raw-sidecar expansion (default-on when `tool_use_reliability != "reliable"` OR `CHATROOM_CAPTURE_RAW=1`)
- `metrics.py` — MetricsCollector baseline (record_turn, record_tool_call, snapshot)
- `tests/fixtures/echo_tool.py`
- Tests cluster G (SQ22-28)

**Grand total: ~41h parallelized** (R1 32h + R2 delta +28%). Delta justified by merge-gate rigor + 4-agent IC[2] convergence + PM-mandated coverage + anti-mock-overconfidence live-smoke tests.

### Does NOT implement (hard-stops)
- M1c: OpenAI + Google + Ollama-local clients, 13-provider roster
- M2: Streamlit app, sidebar, transcript view, tool-call badges, autonomous/human-moderated modes
- M3: MemoryHelper + MCP client, SIGMA_MEM_RECALL tool, metrics panel, per-model context calibration
- M4: Additional tools (web search, calculator, code exec), embedding convergence, topic drift, speaker-influence graph
- ollama-mcp-bridge

### Produces (C1 planning scope, non-code)
- Locked ADRs/ICs/SQs/PMs/DS for M1a + M1b (primary plan deliverable — this file)
- Preliminary forward build-out plan for M1c → M2 → M3 → M4 with revision hooks tied to M1a/b findings (Q3)

---

## Architecture Decisions (locked)

### ADR[1] — Purpose-built `providers/` module; do NOT import/subclass sigma-verify clients.py
- **Alternatives considered:** ALT1 subclass `_OllamaClientBase`, ALT2 copy-verbatim, ALT3 purpose-built borrowing specific functions
- **Rationale:** sync/async mismatch — `clients.py.call()` sync returns tuple; chatroom `Provider.stream()` async yields StreamEvent. <20 LOC real reuse vs ~900 LOC divergent surface. Coupling to sigma-verify Apache-2.0 evolution = silent-break risk.
- **Mitigation:** copy-with-attribution of `_extract_content` + env-var naming convention
- **Prompted-by:** H1, C3
- **BELIEF:** 0.92
- **Source:** `[code-read sigma-verify/clients.py:266-288,247-264,221-236]`, `[agent-inference]`, `[source-plan]`

### ADR[2] — Native per-SDK tool-use; no text-convention, no ollama-mcp-bridge
- **Alternatives:** ALT1 text-convention regex, ALT2 ollama-mcp-bridge, ALT3 hybrid native+text-fallback
- **Rationale:** Anthropic SDK ≥0.40 emits `content_block_start/delta type="tool_use"` (structured, first-class). Ollama /v1 OpenAI-compat emits `tool_calls` when instruction-tuned. Text-convention strictly worse when structure available. `tool_use_reliability` taxonomy only meaningful on native SDK behaviors.
- **Gap:** Ollama /v1 streaming + tool_calls unverified → SQ6c smoke test pre-SQ14b
- **Prompted-by:** H2, C4
- **BELIEF:** 0.95
- **Source:** `[source-plan C4]`, `[independent-research Anthropic+Ollama]`, `[code-read ollama-mcp-bridge warning]`

### ADR[3] — Tool-exec loop lives in TurnEngine; Provider.stream() = exactly one SDK call
- **Alternatives:** ALT1 tool-exec inside Provider.stream (Provider-owned), ALT2 separate ToolExecutor service, ALT3 hybrid Provider-for-agent-mode + TurnEngine-cross-SDK
- **Rationale:** separation-of-concerns (Provider=wire, TurnEngine=policy) + ToolCallRecord needs conversation-level state Provider doesn't have + 5-call cap is chatroom policy not SDK feature. R2 DB re-run: LangChain AgentExecutor counter (Provider-owned loop industry mode for N=1 SDK) acknowledged; ADR defended on N>3 + observability grounds. Single-SDK case would flip decision. autogen/crewai N>1 location-separation precedent.
- **Prompted-by:** H3
- **BELIEF:** 0.88 → **0.84 R2** (DB re-run with stronger counter)
- **XVERIFY:** FAIL[infra-gap-documented — sigma-verify cross_verify hang x3; compensated by 4-agent consensus + DB re-run + industry precedent]
- **Source:** `[source-plan H3]`, `[agent-inference]`, `[industry-pattern autogen+crewai+LangChain]`

### ADR[4] — OpenAI-shaped canonical Message; message_mapping.py owns translation; escape-hatches LOCKED in ADR; 3-tier hand-golden MERGE GATE
- **Alternatives:** ALT1 Anthropic-shaped canonical, ALT2 per-provider subclasses, ALT3 union-type (zero-loss but N^2 adapters)
- **Rationale:** majority-provider (8/13 OpenAI-compat). OpenAI flat-list simpler for JSONL persistence. R2 DB re-run: ALT3 union-type = zero-loss but 12 vs 4 adapters + defeats replay determinism.
- **Escape-hatches (locked into ADR proper per DA[#2] R2):**
  - `Message.preceding_text_per_tool_call: list[str] | None` (impl-eng BC#5) — Anthropic interleaved content ordering reconstruction
  - `Message.content_blocks: list[dict] | None` — Anthropic fidelity for edge cases (cache_control, tool_result with image)
- **3-tier MERGE GATE:** Tier 1 hand-golden outbound + Tier 2 hand-golden inbound + Tier 3 round-trip smoke (derivative)
- **Prompted-by:** H4, H7
- **BELIEF:** 0.80 → **0.70 R2** (honest drop after escape-hatch lock; Gemini M1c+ uncertainty remains)
- **Source:** `[source-plan H4+H7]`, `[independent-research Anthropic+Gemini+OpenAI]`, `[cqa BC-cqa-1 F1-F8]`, `[impl-eng BC#14]`, `[DA[#2]+DA[#6]]`

### ADR[5] — Context budget = 60% `ProviderSpec.max_context_tokens`; estimator `len(text)//4`; per-model calibration deferred to M3 with revision hook
- **Alternatives:** ALT1 70% budget, ALT2 SDK-tokenizer per-call, ALT3 60% + SDK-tokenizer at truncation-decision
- **Rationale:** `len//4` ≈ 4 chars/token English; drift ≤15% absorbed by 60% buffer. M1 seed pair far exceeds 5-turn session.
- **Revision hook H1:** if M1a empirical shows `reported_input_tokens` diverges >15%, M3 calibration shifts LEFT to M1c
- **Prompted-by:** H5, source-plan risk-table
- **BELIEF:** 0.85 (load-bearing: no, config)

### ADR[6] — Raw SDK event capture default-on when `tool_use_reliability != "reliable"`; env override `CHATROOM_CAPTURE_RAW={0,1}`
- **Alternatives:** ALT1 always-on all providers, ALT2 opt-in only via env, ALT3 on M1a-learning + off M3+ except unreliable
- **Rationale:** "0 invocations ambiguity" distinguishes declined/malformed/SDK-swallowed. devstral-2:123b reliability=`"unknown"` → default-on captures first-run evidence.
- **Prompted-by:** H6, risk-table
- **BELIEF:** 0.90 (load-bearing: no)

### ADR[7] — Per-record `schema_version="1"` on every JSONL line + replay invariants
- **Alternatives:** ALT1 version in session_header only, ALT2 sidecar metadata file, ALT3 semver `"1.0.0"`
- **Rationale:** per-record = each line self-describing → replay tools version-check individual records. Critical for M3+ schema v2. OpenTelemetry + Jaeger pattern.
- **Replay invariants (R2-added):**
  - INV-replay-1: skip malformed trailing lines with warning log (partial-flush graceful)
  - INV-replay-2: partial turn records (`stop_reason="error"`) ARE INCLUDED in replayed state
  - INV-replay-3: session_header MUST be valid first line; if missing, raise `CorruptedSessionError`
  - INV-replay-4: `schema_version` forward-compat — v2 reader encountering "1" raises `SchemaVersionMismatch` with actionable message
- **Prompted-by:** C8
- **BELIEF:** 0.95

### ADR[8] — Streaming from day 1 (M1a baseline); Provider.stream() required; complete() REMOVED per DA GP2
- **Alternatives:** ALT1 defer streaming to M2, ALT2 streaming optional gated-by-flag
- **Rationale:** TTFT metric requires streaming; defer = force M2 Streamlit shim to integrate async + new-interface together.
- **R2 GP2:** `complete()` REMOVED from IC[1] Protocol for M1a/b (zero callers). `CompleteResult` dataclass retained for future.
- **Prompted-by:** C5, design-decision-2
- **BELIEF:** 0.92 (load-bearing: no)
- **Source:** `[source-plan C5]`, `[DA[#4] GP[2]+cqa BC-cqa-8 D1]`

---

## Interface Contracts (locked)

### IC[1] — Provider Protocol
```python
class Provider(Protocol):
    key: str                           # e.g. "claude-opus-4-7"
    display_name: str
    max_context_tokens: int
    supports_tools: bool               # SDK capability (binary)

    async def stream(
        self,
        messages: list[Message],
        system: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: list[ToolSchema] | None = None,
    ) -> AsyncIterator[StreamEvent]: ...
    # complete() REMOVED for M1a/b — zero callers. Add back when M1c materializes.
```

**Invariants:**
- INV1: `Provider.stream()` = exactly one SDK call; no tool-exec loop inside
- INV2: `Provider.stream()` emits exactly one `StreamEvent(kind="stop")` as final event (or `kind="error"`)
- INV3: errors ALWAYS emerge as `StreamEvent(kind="error", error=exc)`; no raised exceptions across async iterator boundaries
- INV4 (R2): `Provider.stream()` reconstruction state is WITHIN-CALL only; across-call state forbidden. SDK context-manager semantics required
- INV5 (R2): `Provider.stream()` MUST support early-termination cleanup via async-generator `close()` propagation

### IC[2] — StreamEvent taxonomy + error convention (R2 5-kind)
```python
@dataclass
class StreamEvent:
    kind: Literal["token", "tool_call", "stop", "tool_result", "error"]
    text: str = ""                     # kind="token"
    tool: dict | None = None           # kind="tool_call"; {"id", "name", "arguments"}
    stop_reason: str | None = None     # kind="stop"
    final_message: Message | None = None  # kind="stop" with stop_reason="tool_use" (R2)
    tool_call_record: ToolCallRecord | None = None  # kind="tool_result" (R2)
    error: Exception | None = None
    raw_event: dict | None = None      # optional raw SDK event for sidecar
```

**Event grammar (R2):** `token* → (tool_call+ → stop(stop_reason="tool_use", final_message=M) → tool_result+)* → token* → stop(stop_reason∈{end_turn,max_tokens,max_tool_calls,error})`

**Invariants:**
- INV1: errors ALWAYS emerge as `StreamEvent(kind="error", error=exc)`
- INV2: stop_reason taxonomy = `end_turn | max_tokens | tool_use | max_tool_calls | error | stop`
- INV3 (R2): multiple `kind="tool_call"` events MAY be emitted per stream when model requests parallel tools
- INV4 (R2): when `stop_reason="tool_use"`, Provider MUST populate `final_message` with reconstructed canonical assistant Message
- INV5 (R2): `kind="tool_result"` events emitted ONLY BY TurnEngine (never by Provider); after each tool execution, before re-invoking `Provider.stream()`. `tool_call_record.tool_call_id` correlates with prior `kind="tool_call"`
- INV6 (R2): orphan `kind="tool_result"` (no matching prior tool_call) is contract violation; TurnEngine MUST raise

### IC[3] — ToolSchema + ToolCallRecord
```python
@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: dict                   # JSON-schema; converted per-SDK by tool_schema.py

@dataclass
class ToolCallRecord:
    tool_call_id: str
    tool_name: str
    arguments: dict
    ts_started: str                    # ISO-8601
    ts_completed: str | None           # None if crashed pre-completion (replay-compat)
    latency_ms: int                    # monotonic_ns-derived
    result: str                        # string-coerced tool return
    result_chars: int
    error: str | None                  # error-class name if tool raised
    position_in_turn: int              # 0-indexed within this Turn
    preceding_text: str                # last 50 chars of text preceding this tool_call
```

### IC[4] — Canonical Message shape (R2-expanded)
```python
@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str                       # text content
    speaker: str | None = None         # ProviderSpec.key or "human"
    tool_call_id: str | None = None    # role="tool": result-of-tool-call-with-this-id
    tool_calls: list[dict] | None = None  # role="assistant" with tool use
    preamble_variant: Literal["neutral","identity-aware","research-framed"] | None = None
    preceding_text_per_tool_call: list[str] | None = None  # R2 (impl-eng BC#5)
    content_blocks: list[dict] | None = None  # R2 escape-hatch (DA[#2])
```

**Invariants:**
- INV1: `role="tool"` REQUIRES `tool_call_id`
- INV2: `role="assistant"` with `tool_calls` MAY have `content=""` (tool-only response)
- INV3: `speaker` populated for assistant role (multi-model sessions)
- INV4 (R2): `preceding_text_per_tool_call` length equals `tool_calls` length when both populated

### IC[5] — TurnEngine.advance_stream
```python
class TurnEngine:
    def __init__(
        self,
        policy: TurnPolicy,
        memory: MemoryHelper | None = None,
        metrics: MetricsCollector | None = None,
        max_tool_calls_per_turn: int = 5,
        tool_arg_validator: Callable[[ToolSchema, dict], dict] | None = None,  # GAP[3] seam
    ): ...

    async def advance_stream(
        self,
        state: ConversationState,
        tools: list[ToolSchema] | None = None,
    ) -> AsyncIterator[StreamEvent | Turn]: ...
```

**Tool-exec loop invariants:**
- INV1: each tool_call event from provider → execute tool → append tool_result Message → re-invoke provider.stream
- INV2 (R2): on `tool_count == max_tool_calls`, after executing Nth tool and yielding its tool_result, TurnEngine re-invokes `provider.stream(messages=updated, tools=None)` ONE FINAL TIME for text explanation. Overrides final `stop_reason="max_tool_calls"`
- INV3: ToolCallRecord populated between `ts_started` (pre-exec) and `ts_completed` (post-exec). `monotonic_ns()` for latency_ms
- INV4 (R2): phase sequencing — (1) provider.stream yields `tokens+tool_calls+stop(tool_use,final_message)`; (2) append final_message to state.messages; (3) for each tool_call: execute, build ToolCallRecord, yield `StreamEvent(kind="tool_result")`; (4) append tool_result Messages; (5) loop to (1) or hit max_tool_calls INV2

### IC[6] — TurnPolicy protocol + concrete policies
```python
class TurnPolicy(Protocol):
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...

class RoundRobinPolicy: ...  # M1a
class YieldNextPolicy: ...   # M1b — parses trailing "@next:<key>"; multi-@next uses LAST; self-nom/unknown → RoundRobin fallback
class RandomPolicy: ...      # M1b — excludes last speaker; optional seeded rng for determinism
```

### IC[7] — Persistence JSONL + replay contract
```jsonl
{"schema_version":"1","type":"session_header","session_id":"...","mode":"autonomous","roster":[...],"preamble_variant":"identity-aware","ts":"...","system_preamble":"..."}
{"schema_version":"1","type":"turn","speaker":"claude-opus-4-7","provider":"anthropic","content":"...","tokens_in":0,"tokens_out":0,"stop_reason":"end_turn","ttft_ms":450,"total_ms":2300,"ts":"...","tool_calls":[ToolCallRecord.to_dict(),...]}
{"schema_version":"1","type":"tool_call","turn_id":"...","speaker":"...","provider":"...","tool_name":"echo","arguments":{...},"ts_started":"...","ts_completed":"...","latency_ms":12,"result":"...","result_chars":24,"error":null,"position_in_turn":0,"preceding_text":"..."}
```

Replay invariants: see ADR[7].

---

## Sub-task Decomposition

Full 28-SQ decomposition with owners, estimates, files, dependencies is in the archived scratch workspace under `## sub-task-decomposition` (line 2643+). Summary:

- **M1a cluster A** (foundation): SQ1-SQ5 — pyproject, base types, roster, errors (~2.5h)
- **M1a cluster B** (clients, parallelizable): SQ6a (anthropic) + SQ6b (ollama) + SQ6c (Ollama /v1 smoke, BLOCKS SQ14b) + SQ7 (message_mapping streaming) (~4.25h)
- **M1a cluster C** (orchestration): SQ8a-b (conversation + preamble), SQ9 (TurnEngine RoundRobin), SQ10 (persistence + replay), SQ10b (replay robustness tests), SQ11 (cli), SQ11b (context truncation) (~5.75h)
- **M1a cluster D** (tests): SQ12a-k — mock provider, streaming, message_mapping 3-tier gate, turn engine, conversation, persistence, cli, live smoke m1a, error convention, context truncation (~13h; absorbs most of the +28% R2 delta)
- **M1b cluster E** (tool-schema + providers tool-use): SQ13, SQ14a, SQ14b, SQ15 (~9.5-10h)
- **M1b cluster F** (TurnEngine tool-exec + policies): SQ16-SQ21 — tool-exec loop, YieldNext, Random, echo fixture, MetricsCollector, raw capture (~6.75h)
- **M1b cluster G** (tests): SQ22-SQ28 — per-SDK tool-use, message_mapping 3-tier, turn engine tools + EG1-EG5, metrics, raw sidecar, yield-next, random, live smoke m1b (~10.5h)

**Parallel build opportunities:** SQ6a/SQ6b (2 impl-engs, cluster B) + SQ14a/SQ14b (2 impl-engs, cluster E) per `feedback_parallel-build-engineers` memory pattern. User confirmed for C2.

**Grand total:** ~41h parallelized (R1 32h + R2 delta +28%).

---

## Pre-mortem

### PM[1] — message_mapping.py Anthropic adapter explodes in scope
- **Likelihood:** M (0.55 R1 → **0.25 R2** after escape-hatch lock)
- **Reasoning:** Anthropic tool_use inside assistant content-blocks + tool_result inside user content-blocks with ID-linked pairs. Splitting into OpenAI sibling form is lossy on ordering without `preceding_text_per_tool_call`.
- **Detection:** test_message_mapping.py 3-tier MERGE GATE fails OR production ValidationError
- **Mitigation (R2, locked into ADR[4] not PM):** (a) `Message.preceding_text_per_tool_call` field; (b) `Message.content_blocks` escape-hatch for edge cases; (c) 3-tier hand-golden MERGE GATE; (d) known-lossy cases documented in `message_mapping.py` docstring
- **Escalation trigger:** ≥2 round-trip test fixtures fail at SQ15 boundary → consider Anthropic-native canonical for assistant messages (hybrid canonical)

### PM[2] — Ollama OpenAI-compat tool_calls reliability on devstral-2:123b unreliable
- **Likelihood:** M (0.40)
- **Reasoning:** Mistral function-calling training on Devstral lineage documented but Ollama cloud /v1 layer adds serialization round-trip. Historical pattern: intermittent malformed-JSON on nested objects. `tool_use_reliability="unknown"` per roster until M1b empirical test.
- **Detection:** SQ6c smoke (pre-SQ14b) + M1b integration echo round-trip (post-SQ16)
- **Mitigation:** (a) SQ6c tests BOTH devstral-2:123b AND deepseek-v3.2:cloud pre-SQ14b; pick better pair per empirical; (b) Raw event capture default-on; (c) MANUAL escalation policy per UD#2 — operator observes raw capture + updates roster.py
- **Escalation triggers (R2-QUANTIFIED, UD#2 policy):**
  - (i) 3/3 fail × 3 prompt phrasings → reliability=`"none"` → swap seed pair's Ollama to deepseek-v3.2:cloud via `--models` CLI flag
  - (ii) 1-2/3 malformed → reliability=`"nominal"` → keep devstral + annotate roster.py
  - (iii) 0/3 fail + 3/3 well-formed → reliability=`"reliable"` → lock in roster.py
  - AUTO-escalation deferred to M1c+ per impl-eng R2

### PM[3] — Streaming + async + tool-exec state-machine bug
- **Likelihood:** M (0.35)
- **Reasoning:** Tool-exec loop interleaves async-generator consumption → sync tool call → async-generator re-entry. Risks: (a) partial buffer from `provider.stream()` not flushed before re-invocation; (b) ToolCallRecord timestamps captured under wrong event-loop context; (c) exceptions during tool execution not surfaced into `StreamEvent(kind="error")` correctly; (d) R2 reconstructed `final_message` on `stop(tool_use)` mis-populated across parallel tool_calls.
- **Detection:** test_turn_engine_tools.py SQ24 T1-T9; adversarial test for (c); EG1 event-grammar conformance catches (d)
- **Mitigation:** (a) IC[5] INV1-INV4 explicit phase sequencing; (b) `monotonic_ns()` for latency_ms; (c) test_tool_exec_error_propagation in SQ24 T4; (d) IC[1] INV4+INV5 prevent state leak; EG2 parallel tool_call accumulation + EG3 final_message reconstruction fidelity in SQ22
- **Escalation trigger:** >1 async-state-machine bug in SQ24 review → pause + re-scope: simplify tool-exec to sync `await tool_coro()` inside async generator

### PM[4] — XVERIFY infrastructure hang blocks §2h gate
- **Likelihood:** H (1.0 — observed this session 3x: DA-r1, TA-r1, TA-r2)
- **Reasoning:** sigma-verify `cross_verify` + `verify_finding` fan out multi-provider calls without per-provider timeout; one slow provider blocks entire call
- **Detection:** tool call exceeds 90s → abort per boot directive (time-box)
- **Mitigation:** (a) XVERIFY[ADR3] marked NOT-ATTEMPTED with infra-gap doc in gate-log (not silently skipped per §2h); (b) compensating evidence via 4-agent cross-agent consensus + DB re-run + industry-pattern audit; (c) BELIEF[ADR3] dropped 0.88→0.84 to reflect XVERIFY miss honestly
- **Escalation trigger:** post-C1 troubleshoot session — fix `mcp__sigma-verify` cross_verify timeout + per-provider partial-result return; retry XVERIFY[ADR3] before M1b commits first line of tool-exec code

### PM[5] — Ollama /v1 streaming + tool_calls broken, blocks M1b
- **Likelihood:** M (~0.45)
- **Reasoning:** ollama-mcp-bridge inline warning on /v1 + GitHub issue #12557 closed (about `/api/chat` not `/v1`) + XVERIFY[openai:gpt-5.4] uncertain-low. Plan bets M1b on unverified SDK behavior.
- **Detection:** SQ6c 15-min smoke test BEFORE SQ14b commits 2h
- **Mitigation:** (a) SQ6c runs pre-SQ14b; if passes, proceed with openai SDK AsyncStream; if fails, pivot to `ollama` pypi AsyncClient (+0.5h SQ14b) OR constrain M1b tool-use to Anthropic-only; (b) Raw capture surfaces WHICH failure mode
- **Escalation trigger:** if SQ6c fails for BOTH devstral-2:123b AND deepseek-v3.2:cloud, M1b tool-use scope contracts to Anthropic-only; Ollama tool-use becomes M1c deliverable

---

## Files

Full file table is in the archived scratch workspace (line 2787+). Summary:

- **New source files:** 16 under `~/Projects/sigma-chatroom/src/sigma_chatroom/` (providers module ×7, roster, conversation, turn_engine, persistence, metrics, cli, __init__ ×2)
- **New test files:** 13 under `~/Projects/sigma-chatroom/tests/` + `tests/fixtures/` (+ 2 live-smoke tests under `tests/live/`)
- **New fixtures:** 2 under `~/Projects/sigma-chatroom/tests/fixtures/` (mock_providers, echo_tool)
- **New project files:** pyproject.toml, .gitignore, README.md (stub)
- **New script:** `scripts/smoke_ollama_v1.py` (SQ6c)
- **Read-only reference:** `~/Projects/sigma-verify/src/sigma_verify/clients.py` (pattern only, C3 hard-stop)

---

## Design System (M2+ forward plan only — M1a/b has no UI)

Summary — full detail in archived scratch line 2463+:
- DS[1] spacing-scale 4/8/12/16/24/32/48 px
- DS[2] typography hierarchy — speaker-name 16px/600 > tool-badge 12px/600 > message-body 14px/400 > metadata 11px/400
- DS[3] color-semantics — deterministic hash(provider_key) → 8 WCAG-AA hues + reserved semantic colors
- DS[4] tool-call-badge visual language — `[tool:name] ↻/✓/✗` pill with latency + expand
- DS[5] streaming-in-flight affordance — caret + pulse
- DS[6] status-icon set — Streamlit-native `:material/icon:` (TUI-swappable to rich symbols)
- DS[7] density-mode — medium default + dense toggle

---

## User Decisions (locked 2026-04-20)

1. **Q3 cadence:** ~2 weeks — revisit after M1a ships + before M1c scope locks
2. **devstral→deepseek escalation authority:** manual M1b, automatic M1c+ (impl-eng R2 counter accepted over lead's initial c→a reading)
3. **Rendering option (UI-1):** deferred to pre-M2 STEP-1 — M1a/b rendering-agnostic
4. **Streamlit vs Textual TUI (UI-2):** 2h pre-M2 comparison sketch (STEP-3b) — informed choice, not pre-committed
5. **Research question:** (a) memory-invocation coherence — pins M3 metrics + preamble-variant design
6. **A11Y[2] custom component:** M2 gap, document (moots if TUI path wins)
7. **Plan-track anchoring pre-check:** trust DA §2a positioning (validated — DA-r2 caught pro-forma DB bootstrapping)
8. **sigma-mem agent-scoped write-tool gap:** lead-proxy persistence + audit of impl-eng/ui-ux patterns.md writes (no contamination found). Root-cause fix deferred post-C1.

---

## Forward Plan (Q3 — preliminary, revisable per M1a/b findings)

!Planning artifact, NOT C2 code scope. Revised as M1a/b empirical findings arrive. Full revision hooks in archived scratch line 2709+.

### M1c — clone to remaining SDK families (~1-2 weeks after M1b)
- `providers/openai_client.py` (OpenAI SDK native + Ollama local as subclass per sigma-verify pattern)
- `providers/google_client.py` (google-genai SDK, Gemini function_declarations)
- `providers/message_mapping.py` Gemini parts adapter (hardest adapter)
- `providers/tool_schema.py` Gemini + OpenAI schema adapters
- `roster.py` expanded to 13 ProviderSpec entries
- Tests green across all 4 SDK families

**Revision hooks:** H1 (context calibration shifts LEFT if empirical drift >15%) · H2 (Ollama tool_use sweep expands if devstral fails) · H3 (content_blocks escape-hatch used if Anthropic fidelity loss)

### M2 — Streamlit MVP (~2-3 weeks after M1c)

**Pre-M2 hard gate (1-1.5 day):**
- STEP-0: verify tech-architect IC[2] `kind="tool_result"` + `final_message` acceptance (done — locked in IC[2])
- STEP-1: pin rendering option (a/b/c) with user per UD#3
- STEP-2: prototype chosen rendering option against 5-turn 2-model M1b JSONL fixture
- STEP-3: prototype pre-M2 Streamlit concurrency shim (2h original)
- STEP-3b (NEW per UD#4): 2h Textual TUI comparison sketch
- Exit: chosen option renders 5-turn fixture with ≥1 echo-tool round-trip per provider; user declares "feels right"

**M2a shell + transcript + autonomous** (~3 days): streamlit_app.py, sidebar (roster + mode + preamble picker, 1-variant), transcript view, controls (Start/Pause/Resume/Stop state machine), autonomous session runs end-to-end

**M2b tool-call badges + preamble + error handling** (~3-4 days): DS[4] badge states, IX[5] preamble picker (activates 2nd variant), error banners + retry/skip, A11Y[1-4] (documented gap on aria-live per UD#6)

**M2c human-moderated + session list + polish** (~2-3 days): human-moderated mode, session list + resume, conditional 3rd preamble variant, PERF Level-2 fragment isolation if M2b shows >30 turn overhead

**Revision hooks:** H4 (streaming fallback to CLI-only dual path if shim infeasible) · H5 (deferred ToolCallRecord field population if expensive) · UX-H1 to UX-H6 (6 UI-track hooks)

### M3 — sigma-mem wiring + metrics + v1 ship (~2-3 weeks after M2)
- `memory.py` + MCP client + `SIGMA_MEM_RECALL` tool
- Per-model context calibration using reported `input_tokens` → `ProviderSpec.context_correction_factor`
- Metrics panel prioritized around **memory-invocation coherence** (UD#5):
  - Priority 1: query clustering + cross-model similarity + per-model tool-invocation rate on memory queries
  - Priority 2: yield-next spontaneity supplement
- `test_live_smoke.py` gated by `CHATROOM_LIVE_TESTS=1`
- **v1 ship criterion:** 3-model autonomous session with real `sigma_mem_recall` works end-to-end

**Revision hooks:** H6 (metrics expansion if baseline insufficient for research-question) · H7 (research-question already pinned in UD#5)

### M4 — more tools + richer metrics (~2-3 weeks, post-v1)
- Additional tools: web_search, calculator, code_exec
- Embedding-based metrics (CORE for memory-invocation-coherence per UD#5)
- Transcript summarization for long sessions
- Per-model temperature in sidebar

**Revision hooks:** H8 (embedding scope confirmed core by UD#5)

---

## Plan Challenge Summary

- **DA challenges:** 11 DA + 3 gold-plating + 4 gaps + 3 conflicts (R1) + exit-gate re-evaluation with anti-sycophancy self-audit (R2)
- **Build-track challenges:** impl-eng 15 BCs (R1) + 4 R2 delta | cqa 11 BCs + 5 EC + 4 R2 delta + EG1-EG5 event-grammar suite
- **DA engagement grade:** A-
- **Rounds used:** 2 of 5 (budget preserved)
- **Circuit breaker:** not-needed (26+ challenges in R1 alone)
- **Concessions/defenses:** 5 BELIEF adjustments DOWNWARD (honest, not sycophantic): ADR3 0.88→0.84, ADR4 0.80→0.70, PM1 0.55→0.25, + 2 IC revisions
- **Cross-agent convergence:** 4-agent on IC[2] dual additions (impl-eng + ui-ux + cqa + DA) — strongest signal in build; validated as genuine independent convergence (different scoping perspectives), not anchoring
- **Anchoring probe:** H1-H7 7/7 initially all-consensus → DA §2a positioning check correctly identified pro-forma DB bootstrapping → R2 DB re-run produced honest BELIEF drops
- **XVERIFY:** NOT-ATTEMPTED[ADR3] due to sigma-verify cross_verify infra hang (3× this session). Documented as §2h infra-gap with compensating factors: (a) 4-agent cross-agent consensus on ADR[3]; (b) DB re-run with real counter (LangChain AgentExecutor); (c) industry precedent audit (autogen + crewai + LangChain). DA-r2 PASS-WITH-DOCUMENTED-GAP per anti-sycophancy self-audit.
- **Unresolved tensions:** none plan-blocking. 4 carry-forward flags for C2 (see below).

---

## Carry-forward Flags for C2 (non-blocking)

1. **`CHATROOM_MAX_SESSION_COST_USD` env for live tests** — cqa BC-cqa-6; set cost cap before running `tests/live/test_live_smoke_*.py`
2. **session_id collision handling** — currently defaults to timestamp; may collide under rapid session creation; add entropy in C2
3. **Input-validation seam in TurnEngine for tool-arg validator** — `tool_arg_validator: Callable[[ToolSchema, dict], dict] | None` added to IC[5] as seam; C2 must leave it unused but present for M3 retrofit
4. **T1/T2/T3 tier-tag consistency on source-provenance** — minor hygiene; some findings lack explicit tier tag

---

## Known Gaps

- **XVERIFY[ADR3]:** NOT-ATTEMPTED, infrastructure-blocked (sigma-verify `cross_verify` hang 3× this session: DA-r1, TA-r1, TA-r2). Documented per §2h with 3 compensating factors. Post-C1 troubleshoot queued before M1b first-line-of-tool-exec commit.
- **sigma-mem agent-scoped write-tools (`store_agent_memory`/`store_team_pattern`/`store_team_decision`):** Advertised in MCP HATEOAS but not exposed to agent tool permissions. Lead-proxy persistence applied for this build (8 agent memories + 1 team decision + 1 team pattern stored). Root-cause fix deferred post-C1.
- **Ollama /v1 streaming + tool_calls unverified:** covered by SQ6c smoke test blocking SQ14b. Fallback: `ollama` pypi AsyncClient (+0.5h) or Anthropic-only tool-use in M1b.

---

## Verification

### After M1a
```bash
cd ~/Projects/sigma-chatroom
pytest tests/ -q -k "not tool and not message_mapping_tool"
python -m sigma_chatroom.cli \
    --models claude-opus-4-7,devstral-2:123b-cloud \
    --turns 5 --topic "introduce yourselves"
# Expect: tokens stream to stdout; 5 turns alternating speakers;
# JSONL in sessions/ with Turn records (stop_reason, ttft_ms populated, schema_version=1);
# replay from JSONL reproduces transcript exactly.
```

### After M1b
```bash
pytest tests/ -q
python -m sigma_chatroom.cli \
    --models claude-opus-4-7,devstral-2:123b-cloud \
    --turns 5 --topic "use the echo tool to verify it works" --tool echo
# Expect: at least one echo-tool round-trip per provider; ToolCallRecord entries
# in JSONL with preceding_text + position_in_turn; raw sidecar written for
# devstral-2:123b-cloud (tool_use_reliability=unknown).
```

### Pre-SQ14b (blocking smoke)
```bash
python scripts/smoke_ollama_v1.py --model devstral-2:123b-cloud
python scripts/smoke_ollama_v1.py --model deepseek-v3.2:cloud
# Expect: tool_calls arrive in delta stream for at least one model.
# If both fail: PM[5] escalation — contract M1b tool-use to Anthropic-only.
```

---

## Build Status
*(empty — written by C2)*

## Build Review Summary
*(empty — written by C3)*

## Close Status
*(empty — written by C3)*
