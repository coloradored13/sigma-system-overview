# C1 scratch — BUILD: multi-model-chatroom
## status: active
## mode: BUILD
## build-id: 2026-04-16-multi-model-chatroom

## task

Design the best plan to build a local multi-model chatroom: a Streamlit web app where 3-13 architecturally different models (Anthropic, OpenAI, Google Gemini, Ollama local + Ollama cloud) participate in a shared, streamed conversation with optional access to shared memory (sigma-mem) via each model's native tool-use. This is a research instrument, not a product — the goal is to observe emergent behavior when heterogeneous models interact directly (who speaks when, what they query, how they reference each other, what they converge/diverge on). Foundation for Project 3 (cross-model sigma-review).

**IMPORTANT FRAMING — de novo then compare.** Round 1: plan-track agents produce their OWN best plan from scratch. A prior-session draft plan + external reviewer (Brad) critique exist but are being withheld from Round 1 so plan-track reasoning is uncontaminated by an anchor. Round 2: draft + critique will be introduced; plan-track compares their plan to draft, integrates valid critiques, rejects invalid ones with evidence. DA audits whether comparison is genuine or confirmatory.

## infrastructure

ΣVerify: available (13 providers per project memory — 4 local Ollama + 6 Ollama cloud Pro + 2 per-token + 1 optional)
  — advisory in C1; mandatory XVERIFY on top-1 security-critical ADR only; non-security ADRs advisory
  — this build has no security-critical ADRs (local research tool, sigma-mem read-only, no untrusted MCP)

## prompt-understanding

### Q[] — what is being planned
- Q1: Local Streamlit web app hosting 3-13 heterogeneous-model streamed conversations
- Q2: sigma-mem read-only access via each model's native tool-use mechanism (no text convention, no bridge)
- Q3: Research instrument — observability over product polish; every token/turn/tool-call captured
- Q4: v1 ship = 3-model autonomous + sigma-mem + metrics panel (draft calls this M3)
- Q5: Foundation for Project 3 (cross-model sigma-review), not a standalone destination

### H[] — hypotheses to test (find evidence for AND against; do NOT accept as given)
- H1: Purpose-built providers module > importing sigma-verify (fan-out verification is wrong shape for multi-turn streamed tool-use)
- H2: Native tool-use > `/recall` text convention (text convention destroys the authenticity signal the instrument exists to observe)
- H3: Tool-exec loop belongs in TurnEngine, not Provider (Provider.stream() = one SDK call; orchestration lives above)
- H4: Multi-model from M1a, not single-model-first (single-model phase tests SDK wrapping, not engine's actual job)
- H5: M1a/b/c split isolates integration risk (contested — one outside review claims "M1 is 60-70% of whole project," phase boundary understates schedule risk)
- H6: Streamlit + asyncio + streaming + tool-call events is tractable with a 2h feasibility prototype (contested — st.write_stream wants sync string generators; tool_call events aren't strings; fallback may be needed)
- H7: Message-mapping across Anthropic content-blocks / OpenAI siblings / Gemini parts is the hardest adapter work (schema normalization is the easier half)
- H8: Raw-event default-on for `tool_use_reliability != reliable` is required to distinguish "declined" from "tried and emitted malformed JSON that SDK swallowed"
- H9: System preamble is an experimental parameter, not a design detail — observations are functions of the prompt, log the variant
- H10: YieldNextPolicy discoverability is a preamble-variant design decision (whether preamble tells models about `@next:<name>` is itself an observable)
- **H11 (VIABILITY — user flagged): Is a chatroom like this even possible/viable at all?** Evaluate whether the technical premises hold (heterogeneous SDK round-trip, streaming + tool-use concurrency, Streamlit async bridge, small-model tool-use reliability, context budget across 3-13 models) OR whether a different instrument shape (Textual TUI? headless JSONL + external viewer? Jupyter notebook?) is more viable. This is a precondition to all other H[].

### C[] — constraints (user-pinned)
- C1: Local only, not deployed, no auth/multi-tenant
- C2: Streamlit UI (user-pinned in plan-mode scoping; re-evaluable under H11)
- C3: sigma-mem read-only for v1 (no writes, no additional tools)
- C4: Configurable per session — mode (autonomous ↔ human-moderated), roster (pick from pool of 13), preamble variant
- C5: Study sigma-verify patterns, do NOT import the module
- C6: Do NOT use ollama-mcp-bridge (chatroom uses each SDK's native tool-use)
- C7: User goal = best plan, not implement draft as-is; evaluate and stress-test

## scope-boundary

This build implements (v1 scope): M1 headless engine + streaming + tool-use plumbing → M2 Streamlit MVP → M3 sigma-mem + metrics + v1 ship. Concrete success criterion for v1: 3-model autonomous session with `sigma_mem_recall` available, `ToolCallRecord` populated when invoked, `preamble_variant` logged, metrics panel live-updating.

This build does NOT implement (future phases/out of scope):
- M4 additional tools (web search, calculator, code exec)
- M4 embedding-based convergence/divergence metrics, topic drift, speaker-influence graph
- M4 transcript summarization, per-model temperature UI
- sigma-mem writes (read-only v1)
- Cross-model sigma-review wiring (Project 3 — downstream consumer of v1 instrument)
- Production polish (auth, deployment, multi-user, hosting)

Lead: before accepting agent output, verify it builds ONLY what's in scope.

## complexity-assessment

BUILD TIER-3 |scores: module-count(5),interface-changes(5),test-complexity(4),dependency-risk(4),team-familiarity(3) |total:21 |plan-track:3 |build-track:3

## withheld-materials (introduce in Round 2 only)

The following exist but are NOT to be shared with plan-track agents in Round 1 — they are the comparison material for Round 2:
- Draft plan: `~/.claude/plans/look-for-the-plan-snazzy-giraffe.md` (prior-session architecture)
- External reviewer critique (Brad): 4 substantive pushes — M1 scope (60-70%), Streamlit async fiddliness, message-mapping complexity, preamble as study variable; plus research question scoping, memory speaker Turn redundancy, Ollama raw-capture ambiguity
- Lead will release these to plan-track at Round 2 entry for compare-and-refine

## plans (plan-track agents — Round 1 de novo)

### tech-architect

#### H11 — VIABILITY ASSESSMENT (precondition to all other Hs)

VIABILITY[go-conditional]:
- Streamlit async generators: SUPPORTED |source: docs.streamlit.io/st.write_stream |T1-verified| "Streamlit internally converts async generators to sync generators" — caveat: "can raise error if generator depends on cached object with async references" → mitigation: never cache provider coroutines; use fresh coroutines per turn
- Anthropic SDK streaming + tool_use: SUPPORTED |source: anthropic-sdk-python GitHub, v0.79.0 |T1-verified| MessageStream wrapper accumulates content blocks including tool_use blocks; async variant identical API
- OpenAI streaming + tool_calls: SUPPORTED with reconstruction caveat |source: OpenAI community + SDK docs |T2-corroborated| tool_calls arrive as delta chunks that must be concatenated; finish_reason="tool_calls" signals completion
- Google GenAI streaming + function_call: SUPPORTED |source: googleapis.github.io/python-genai |T1-verified| function_call parts appear in chunks; function_response sent back on next turn
- Ollama OpenAI-compat layer + streaming + tools: BROKEN — silently drops tool_calls |source: openclaw issue #11828, ollama issue #12557 |T1-verified (GitHub production reports)| Fix tracked but no timeline. Native /api/chat supports streaming + tools since May 2025.
- Small-model tool reliability: VARIABLE — gemma4:e4b, nemotron-3-nano:4b may not reliably emit structured tool_calls |source: agent-inference + community reports |T3-unverified| → mitigation: tool_use_reliability taxonomy per model, graceful fallback to text-only turn
- Context budget 3-13 models: MANAGEABLE for v1 3-model constraint |source: agent-inference |T3-unverified| → mitigation: per-model context window tracking, truncation strategy defined in plan

PRECONDITIONS for GO:
1. Ollama providers use native /api/chat endpoint (NOT OpenAI compat) for tool-use models
2. Streamlit async bridge uses asyncio.run() or nest_asyncio for event loop compatibility — do NOT pass cached coroutines
3. H6 (2h feasibility prototype): Scope to (a) Anthropic stream + tool_use roundtrip, (b) Streamlit async_gen→st.write_stream plumbing — 2h is sufficient for these two, NOT for full integration

VIABILITY[go-conditional]: go for M1-M3 scope with Ollama native endpoint. ¬go if Ollama native /api/chat also drops tool_calls (escalation path: disable tool-use for local Ollama models, text-only participation).

EXPERIMENT[2h]: Build `experiments/viability.py` — single Anthropic async stream with tool_use, yield token events and tool_call events through a sync wrapper, display in Streamlit with st.write_stream. Pass condition: tool_call event visible in UI distinct from token. Fail condition: tool_call event swallowed or UI crashes.

§2e: premise-viability: CONFIRMED with above preconditions. Strongest alternative: headless JSONL engine + separate viewer (Textual TUI or Jupyter) — avoids Streamlit async bridge entirely, simpler execution model, but sacrifices C2 (user-pinned Streamlit) and real-time UI streaming. Alternative noted but not taken given C2 constraint. |source: agent-inference |outcome: 2 (confirmed with risk noted)

---

#### ADR[1] — Provider Module Shape: Purpose-Built vs sigma-verify Reuse

CLAIM: Build purpose-built providers module. ¬import sigma-verify.

ALTERNATIVES:
- ALT-A: sigma-verify clients.py reuse with streaming subclass — sigma-verify is a HATEOAS state machine for single-shot cross-model verification via MCP tools. It wraps verify_finding/challenge/cross_verify as MCP actions. No streaming, no multi-turn conversation history, no tool-exec loop, no per-provider event yielding. Architecture is fundamentally incompatible with chatroom shape. C5 also explicitly prohibits import. |source: code-read sigma-verify/src/sigma_verify/machine.py, server.py |T1-verified|
- ALT-B: Purpose-built BaseProvider ABC with per-SDK subclasses — ProviderProtocol defines stream(messages, tools) → AsyncGenerator[ChatEvent, None]. Each SDK maps to one class (AnthropicProvider, OpenAIProvider, GeminiProvider, OllamaProvider). Ollama uses native /api/chat, NOT OpenAI compat.

RATIONALE: sigma-verify has no streaming capability, no conversation history management, no tool-exec loop interface, wrong abstraction level (MCP tools ≠ provider streaming). H1 confirmed independent of C5 constraint. Purpose-built is 100% the right call. |source: code-read (T1) + agent-inference|

DB[ADR-1]: (1) initial: purpose-built required (2) assume-wrong: what if sigma-verify IS reusable? (3) strongest-counter: sigma-verify has provider key discovery + model enumeration that could be reused — don't reinvent env-key scanning (4) re-estimate: reuse PATTERN (env-key discovery, model lists) but ¬import module — extract the env-discovery pattern to a separate utility; (5) reconciled: purpose-built providers/ module, but copy the env-key discovery pattern from sigma-verify (¬import, study per C5). Reversal condition: IF sigma-verify adds a streaming adapter interface that yields ChatEvent-compatible events THEN reconsider at M4.

§2a: positioning: purpose-built per-SDK providers is the standard pattern for multi-model adapters (LangChain, LiteLLM all use this) — mainstream approach, growing ecosystem, low lock-in. |outcome: 2 (confirmed, no revision)

§2c: complexity: ProviderProtocol is 4 concrete classes (~150-200 LOC total). Reuse attempt would require stripping/rewrapping sigma-verify at equal or greater complexity. Cost of being wrong: 1 day to rewrite. |outcome: 2 (confirmed, justified)

CQoT: IF sigma-verify adds streaming adapter THEN reconsider at M4 for sigma-review integration. ¬reachable in v1.
H1: CONFIRMED — sigma-verify IS wrong shape, supported by code-read evidence.

---

#### ADR[2] — Tool-Exec Loop Location: TurnEngine vs Provider

CLAIM: Tool-exec loop lives in TurnEngine, NOT in Provider.

ALTERNATIVES:
- ALT-A: Provider owns tool-exec loop — Provider.stream() makes API call, detects tool_call event, executes tool inline, sends tool_result, continues streaming. Single method handles full agentic turn.
- ALT-B: TurnEngine owns tool-exec loop — Provider.stream() yields ChatEvent stream (token | tool_call | done). TurnEngine detects tool_call events, executes tool, injects tool_result into conversation history, calls Provider.stream() again. Separation: Provider = one SDK call + event normalization. TurnEngine = conversation state + loop control.

RATIONALE: ALT-B (TurnEngine) is correct because: (1) Tool execution is NOT provider-specific — same sigma_mem_recall runs regardless of which model triggered it; (2) ALT-A creates provider-specific tool execution that would need to be duplicated across 4 providers; (3) TurnEngine separation means Provider is testable without a live tool server; (4) H3 confirmed — Provider.stream() maps to exactly one SDK call, TurnEngine manages the loop; (5) Tool call recording (ToolCallRecord) belongs at the loop level where full context (which model, which turn, input/output) is available. |source: agent-inference + H3 from scratch |T3-unverified (architectural judgment)|

DB[ADR-2]: (1) initial: TurnEngine owns loop (2) assume-wrong: what if tool-exec inside Provider is simpler? (3) strongest-counter: Provider encapsulation means caller doesn't need to distinguish "tool_call" events from "done" — cleaner caller interface; (4) re-estimate: caller simplicity from ALT-A is real BUT test isolation and tool-implementation sharing outweigh it; (5) reconciled: TurnEngine loop is correct. Mitigation for caller complexity: TurnEngine exposes run_turn() → AsyncGenerator[ChatEvent, None] which hides the loop — callers see the same event stream shape regardless of how many tool loops occurred.

§2e: assumptions: tool execution is fast (<500ms for sigma_mem_recall). If tool execution were slow (>2s), Provider encapsulation would matter more (could interleave). For sigma_mem_recall over MCP, latency expected <200ms. Assumption: reasonable. |outcome: 2 (confirmed, condition noted)

CQoT: IF tool execution latency >2s consistently THEN reconsider Provider-level streaming continuation to avoid blocking Streamlit render. IF additional tools with heavy I/O are added (M4) THEN TurnEngine loop may need async task pool.
H3: CONFIRMED — Provider = one SDK call, orchestration above.

§2a: check: TurnEngine-as-loop is the standard agentic turn architecture (see: Anthropic agent loop docs, LangChain AgentExecutor, Google ADK). Ecosystem trajectory: stable, growing. |outcome: 2 (confirmed)

---

#### ADR[3] — Event Stream Shape: Discriminated Union

CLAIM: ChatEvent is a discriminated union of typed events. Provider yields these; TurnEngine re-yields them; Streamlit renders by type.

SHAPE:
```
ChatEvent = TokenEvent | ToolCallEvent | ToolResultEvent | TurnStartEvent | TurnEndEvent | ErrorEvent
```

- TokenEvent: model_id, speaker, text_chunk, turn_id
- ToolCallEvent: model_id, speaker, tool_name, tool_input, call_id, turn_id
- ToolResultEvent: model_id, speaker, tool_name, tool_output, call_id, turn_id
- TurnStartEvent: model_id, speaker, turn_id, timestamp
- TurnEndEvent: model_id, speaker, turn_id, finish_reason, input_tokens, output_tokens

Streamlit checks `isinstance(event, TokenEvent)` for typewriter rendering; `isinstance(event, ToolCallEvent)` for tool-call display bubble. |source: agent-inference, cross-model protocol patterns from memory |T3-unverified (architectural choice)|

ALT: string tagging (dict with "type" key). Rejected: no static type checking, no exhaustiveness guarantee, error at runtime not at definition.

§2c: dataclass union is lightweight (~50 LOC). Cost of wrong: schema change = update all isinstance checks — bounded, 1-2h. |outcome: 2 (confirmed)

CQoT: IF consumers other than Streamlit exist THEN serialization format matters — add `to_dict()` on each event class. For v1 single-consumer, not required.
P[envelope-fields-first-reduces-format-errors] from memory: applies to LLM output schemas, less critical here (these are Python dataclasses with static typing), but still: put model_id and event type first in serialization order.

---

#### ADR[4] — Message Mapping: Canonical Shape + Per-SDK Adapters

CLAIM: Define CanonicalMessage (role, content: list[ContentBlock], tool_calls: list[ToolCall] | None, tool_results: list[ToolResult] | None) as internal history format. Each provider translates out to SDK format; translates in from SDK response.

HARDEST ADAPTER SURFACE: Anthropic ↔ OpenAI for multi-turn tool-use history.

Anthropic: history appends `{"role": "assistant", "content": [{"type": "tool_use", "id": "...", "name": "...", "input": {...}}]}` then `{"role": "user", "content": [{"type": "tool_result", "tool_use_id": "...", "content": "..."}]}`

OpenAI: history appends `{"role": "assistant", "content": null, "tool_calls": [{"id": "...", "type": "function", "function": {...}}]}` then `{"role": "tool", "tool_call_id": "...", "content": "..."}`

Gemini: `function_call` part in model turn, `function_response` part in user turn, no explicit "tool" role — all turns are "user" or "model".

Ollama native `/api/chat`: same shape as OpenAI chat completions (role=tool, tool_call_id) but separate endpoint.

ADAPTER STRATEGY:
- AnthropicAdapter: translate CanonicalMessage→Anthropic content-blocks on each call
- OpenAIAdapter: translate CanonicalMessage→OpenAI messages on each call (handles role="tool")
- GeminiAdapter: translate CanonicalMessage→Gemini Parts (function_call/function_response contents)
- OllamaAdapter: same as OpenAIAdapter structure (native API uses same message shape as OpenAI)

ROUND-TRIP TEST STRATEGY: Each adapter has `to_sdk_messages(history)` and `parse_response(sdk_response) → CanonicalMessage` tested with fixture history containing mixed text + tool_call + tool_result turns. Hardest fixture: 3-turn conversation with one tool call mid-turn.

§2a: Canonical-message-with-per-SDK-adapters is the LiteLLM / LangChain pattern — mainstream, proven. ALT: use LiteLLM directly. Rejected per C5 spirit (study patterns, ¬import libraries that abstract away the plumbing — we want to observe raw behavior), and because LiteLLM's abstraction would hide the tool_call event emission differences we need to observe. |outcome: 2 (confirmed, LiteLLM rejection noted)

DB[ADR-4]: (1) initial: canonical messages + per-SDK adapters (2) assume-wrong: what if a model's history requirements don't fit canonical shape? (3) strongest-counter: Gemini's function_response embedded as a user "part" is structurally different — no "role=tool" concept; canonical ToolResult may not capture the Gemini idiom faithfully (4) re-estimate: Gemini adapter can store function_response in content with a type tag; faithfulness of round-trip testable with fixture; (5) reconciled: canonical shape is correct, but Gemini adapter gets integration test that verifies function_response round-trip before plan lock.

§2d: tool_call format differences sourced from [independent-research] via SDK docs (T1 Anthropic, T1 Google, T2 OpenAI community); Ollama native format sourced from [independent-research] ollama/ollama GitHub (T2).

CQoT: IF a new model provider uses neither content-blocks nor siblings nor parts (e.g., Cohere command-a's tool_calls format) THEN add new adapter class — canonical shape is extensible.
H7: PARTIALLY-CONFIRMED — Gemini adapter IS notably harder (no role=tool, function_response in user content), but the Anthropic↔OpenAI history translation for multi-turn tool use is also non-trivial. "Hardest" is a matter of degree; all three adapter surfaces require care.

---

#### ADR[5] — Concurrency Model: Sequential Turn-Taking with Per-Model Async

CLAIM: Sequential turn-taking (one model's full turn completes before next model begins), with per-model async streaming within each turn. ¬concurrent multi-model streaming.

ALT: True concurrent multi-model streaming (all models stream simultaneously, displayed in parallel columns). Rejected because: (1) research instrument semantics — models need to READ each other's output to respond meaningfully; concurrent streaming means no model sees any other model's turn (2) Streamlit's threading model makes true concurrent write to multiple containers from separate threads fragile (3) turn-ordering is an experimental variable (YieldNextPolicy); parallel streaming eliminates the variable

STREAMLIT ASYNC BRIDGE:
- Problem: Provider.stream() is async; st.write_stream() accepts sync generators OR async generators (Streamlit internally converts async generators since recent update per docs.streamlit.io)
- Strategy: `async def turn_gen() → AsyncIterator[str]` — yield text chunks only; tool events handled separately
- TurnEngine.run_turn() is async; called via `asyncio.run()` in Streamlit main thread OR via `nest_asyncio` if event loop already running
- Complication: Streamlit runs in threads; asyncio event loop per thread. Use `asyncio.new_event_loop()` per turn, run in `concurrent.futures.ThreadPoolExecutor` with loop isolation, bridge results via queue. This is the reliable pattern (avoids "event loop closed" errors seen in issue #12076).
- Alternative bridge: convert async generator to sync via `queue.Queue` + background thread running `asyncio.run()`. Producer puts events in queue; sync generator pulls from queue. Simpler, avoids nest_asyncio. **Preferred.**

§2e: assumption: Streamlit's internal async→sync conversion works for our use case IF we avoid cached coroutines. Experiment in VIABILITY[2h] directly tests this. If it fails, fallback is queue-based bridge. |outcome: 2 (condition flagged)

§2a: sequential turn-taking in multi-agent text conversations: standard approach (Autogen, CrewAI default mode). Concurrent streaming is the non-standard path. |outcome: 2 (confirmed)

AT 3-13 MODELS: sequential turn-taking means a 13-model round takes 13 sequential API calls. At ~5s per turn average, a 13-model round = ~65s. For a research instrument this is acceptable; for product it would not be. Flag as break-if condition: if user wants <10s round trips for 13 models, parallel streaming required, which requires architecture revision.

CQoT: IF round latency >120s for 13 models THEN reconsider async-concurrent rendering with conversation history injected prior to stream start. IF Streamlit's internal async conversion proves unreliable THEN use queue-based bridge.

---

#### ADR[6] — Ollama: Native API, Not OpenAI Compat

CLAIM: Ollama providers use native `/api/chat` endpoint via `ollama` Python library, NOT via `openai` Python SDK pointed at localhost:11434/v1.

EVIDENCE: OpenAI compat layer silently drops tool_calls when streaming=True. Confirmed by: openclaw issue #11828, ollama issue #12557, community reports (T1-verified via GitHub production issues). Native /api/chat supports streaming + tool calling since May 2025 (ollama blog).

ALT: Use OpenAI compat with streaming=False for tool-use turns. Problem: defeats streaming observability for tool-use turns, breaks the research instrument's core requirement (observe tool-call events in real time).

§2e: assumption: local Ollama models (llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, qwen3.5:4b) reliably emit tool_calls via native API. This is WEAKLY supported — small models have variable tool-call reliability. Mitigation: tool_use_reliability taxonomy per model. Models marked "unreliable" skip tool-use; "experimental" get tool-use with ToolCallRecord noting reliability tier. |source: independent-research (T2) + agent-inference (T3)| |outcome: 2 (confirmed with risk)

CQoT: IF Ollama's native /api/chat also exhibits streaming tool_call drop for specific models THEN disable tool-use for affected models, log as raw_event for M4 forensics.

---

#### ADR[7] — Persistence: JSONL + Optional Raw-Event Sidecar

CLAIM: Session persistence in JSONL at `sessions/{session_id}.jsonl`. Each line = one CanonicalMessage or ChatEvent. Schema version field on every line. Optional raw-event sidecar: `sessions/{session_id}.raw.jsonl` capturing unmodified SDK responses.

SCHEMA (per line):
```json
{"schema_version": 1, "event_type": "...", "turn_id": "...", "model_id": "...", "speaker": "...", "timestamp": "...", "data": {...}}
```

RAW SIDECAR: enabled per-session flag `capture_raw=True`. Captures unmodified SDK chunk bytes. Purpose: forensic analysis when tool_call events are suspected dropped by SDK. H8: Raw-event default-on for tool_use_reliability != reliable — CONFIRMED as correct.

IN SCHEMA: turn_id, model_id, speaker, event_type, timestamp, schema_version, data (event-specific payload), preamble_variant (on TurnStartEvent)
OUT OF SCHEMA: embeddings, convergence metrics, topic drift (M4), inter-model influence graphs (M4)

§2c: JSONL is append-only, no schema migration cost for additive fields. Schema_version field enables future reader to skip or transform old lines. Cost of wrong: negligible — JSONL is trivially readable by any Python script. |outcome: 2 (confirmed)

ALT: SQLite per session. Rejected: JSONL is simpler, append-only writes are crash-safe, grep-able, human-readable — appropriate for research instrument.

P[additive-only-schema-evolution] from memory applies: new fields are optional, readers ignore unknown fields.

---

#### ADR[8] — MCP Client for sigma-mem: Subprocess + stdio

CLAIM: sigma-mem accessed via `mcp` Python client in subprocess mode (stdio transport), NOT via direct Python import, NOT via ollama-mcp-bridge.

RATIONALE: sigma-mem is an MCP server. Correct consumption pattern is MCP client. Direct import would couple chatroom to sigma-mem internals (violating layer separation). C6 prohibits ollama-mcp-bridge. stdio transport is local-only (matches C1), no auth needed.

TOOL DEFINITION SHAPE (sent to each model per their SDK's tool format):
```
sigma_mem_recall(context: str) → str
```
Single tool for v1 read-only. One tool declaration translated to Anthropic/OpenAI/Gemini/Ollama tool format by each adapter.

FAILURE MODES:
- sigma-mem subprocess fails to start: tool_result = "sigma_mem unavailable: {error}". Model sees the error in tool_result and can comment on it. Research instrument: failure is observable data.
- sigma-mem returns error: surface raw error in tool_result. ¬silently return empty string (would look like "no memories" when it was actually a failure).
- MCP client timeout: 5s timeout; return "sigma_mem timeout" in tool_result. Log as ToolCallRecord with status=timeout.

§2e: assumption: sigma-mem subprocess starts reliably in <2s. Reasonable for local MCP server. |outcome: 2 (confirmed)

---

#### VIABILITY SUMMARY — H11

go-conditional |
preconditions: (1) Ollama native /api/chat ¬OpenAI-compat (2) async bridge via queue-not-cached-coroutines (3) 2h viability experiment BEFORE M1 build begins |
¬no-go signals: Ollama native also drops tool_calls (mitigable: disable tool-use for Ollama), Streamlit async crashes for ALL bridge patterns (would invalidate C2, recommend headless JSONL) |
P(go)=0.85 conditional on 2h experiment passing |
P(go-with-degraded-Ollama-tool-use)=0.95 (acceptable fallback)

---

#### IC[1] — ProviderProtocol

```python
class ProviderProtocol(Protocol):
    provider_id: str
    model_id: str
    tool_use_reliability: Literal["reliable", "experimental", "unreliable"]

    async def stream(
        self,
        messages: list[CanonicalMessage],
        tools: list[ToolDefinition] | None,
    ) -> AsyncIterator[ChatEvent]: ...

    def format_tool_definition(self, tool: ToolDefinition) -> dict: ...
```

#### IC[2] — TurnEngine

```python
class TurnEngine:
    def __init__(self, provider: ProviderProtocol, tool_registry: ToolRegistry): ...

    async def run_turn(
        self,
        conversation: ConversationHistory,
        speaker: ProviderSpec,
    ) -> AsyncIterator[ChatEvent]:
        """Yields all events for one complete turn including tool loops."""
        ...
```

#### IC[3] — ConversationHistory

```python
class ConversationHistory:
    messages: list[CanonicalMessage]
    session_id: str
    preamble_variant: str

    def append(self, message: CanonicalMessage) -> None: ...
    def to_provider_messages(self, provider_id: str) -> list[dict]: ...
    def token_count_estimate(self, provider_id: str) -> int: ...
    def truncate_to_budget(self, provider_id: str, budget: int) -> "ConversationHistory": ...
```

#### IC[4] — ToolRegistry

```python
class ToolRegistry:
    def register(self, name: str, handler: Callable[[dict], Awaitable[str]]) -> None: ...
    async def execute(self, name: str, tool_input: dict) -> ToolResult: ...
    def definitions(self) -> list[ToolDefinition]: ...
```

#### IC[5] — ProviderSpec (roster config)

```python
@dataclass
class ProviderSpec:
    provider_id: str          # "anthropic" | "openai" | "google" | "ollama"
    model_id: str             # "claude-opus-4-7" | "gpt-4o" | "gemini-2.0-flash" | "llama3.1:8b"
    display_name: str
    tool_use_reliability: Literal["reliable", "experimental", "unreliable"]
    api_key_env: str | None   # None for Ollama local
    base_url: str | None      # for Ollama cloud override
    context_window: int       # tokens
```

#### IC[6] — SessionWriter

```python
class SessionWriter:
    def __init__(self, session_id: str, capture_raw: bool = False): ...
    def write_event(self, event: ChatEvent) -> None: ...
    def write_raw(self, provider_id: str, chunk_bytes: bytes) -> None: ...
    def close(self) -> None: ...
```

#### IC[7] — ChatOrchestrator

```python
class ChatOrchestrator:
    def __init__(
        self,
        providers: list[ProviderProtocol],
        conversation: ConversationHistory,
        tool_registry: ToolRegistry,
        session_writer: SessionWriter,
        yield_next_policy: YieldNextPolicy,
    ): ...

    async def run_round(self) -> AsyncIterator[ChatEvent]:
        """Runs one round: each provider in roster order takes one turn."""
        ...

    async def run_autonomous(self, max_rounds: int) -> AsyncIterator[ChatEvent]: ...
```

---

#### SQ[] — Sub-Task Decomposition

SQ[1]: M0 viability experiment |estimable: yes |method: analogue (2h feasibility prototypes from sigma-ui, chatroom pattern) |owner: implementation-engineer |files: experiments/viability.py |effort: 2h |GATE: must pass before M1 begins

SQ[2]: M1a — CanonicalMessage + ChatEvent types + ProviderProtocol ABC |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/types.py |effort: 3h

SQ[3]: M1b — AnthropicProvider (streaming + tool_use content blocks) |estimable: yes |method: precedent (Anthropic SDK docs + sigma-verify patterns) |owner: implementation-engineer |files: chatroom/providers/anthropic_provider.py |effort: 4h

SQ[4]: M1b — OpenAIProvider (streaming + tool_calls delta reconstruction) |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/providers/openai_provider.py |effort: 4h

SQ[5]: M1b — GeminiProvider (function_call parts + function_response) |estimable: yes |method: analogue (harder adapter — no role=tool) |owner: implementation-engineer |files: chatroom/providers/gemini_provider.py |effort: 5h

SQ[6]: M1b — OllamaProvider (native /api/chat, streaming + tool_calls) |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/providers/ollama_provider.py |effort: 4h

SQ[7]: M1c — TurnEngine (tool-exec loop, ToolCallRecord, tool-loop termination) |estimable: yes |method: analogue (agent loop pattern well-understood) |owner: implementation-engineer |files: chatroom/engine/turn_engine.py |effort: 5h

SQ[8]: M1c — ConversationHistory + truncation strategy |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/engine/history.py |effort: 3h

SQ[9]: M1c — ToolRegistry + sigma_mem_recall handler (MCP stdio client) |estimable: yes |method: analogue (MCP client subprocess pattern) |owner: implementation-engineer |files: chatroom/tools/registry.py, chatroom/tools/sigma_mem.py |effort: 4h

SQ[10]: M1d — SessionWriter (JSONL + raw sidecar) |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/persistence/session_writer.py |effort: 3h

SQ[11]: M1e — ChatOrchestrator + YieldNextPolicy |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/engine/orchestrator.py, chatroom/engine/yield_policy.py |effort: 5h

SQ[12]: M1 integration test — headless 2-model session (Anthropic + Ollama), one tool call, JSONL output verified |estimable: yes |method: analogue |owner: implementation-engineer |files: tests/test_m1_integration.py |effort: 3h

SQ[13]: M2 — Streamlit app scaffold (roster config UI, preamble selector, session start) |estimable: yes |method: analogue (sigma-ui patterns) |owner: ui-ux-engineer + implementation-engineer |files: chatroom/app.py, chatroom/ui/ |effort: 4h

SQ[14]: M2 — Streamlit streaming render (token typewriter, tool-call bubble, turn separator) |estimable: yes |method: analogue |owner: ui-ux-engineer + implementation-engineer |files: chatroom/ui/render.py |effort: 4h

SQ[15]: M3 — sigma-mem tool wiring + ToolCallRecord live panel |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/tools/sigma_mem.py (complete), chatroom/ui/metrics.py |effort: 4h

SQ[16]: M3 integration — 3-model autonomous session, sigma_mem_recall invoked, ToolCallRecord populated, preamble_variant logged |estimable: yes |method: analogue |owner: implementation-engineer |files: tests/test_m3_integration.py |effort: 3h

SQ[17]: M3 roster config — 13-provider spec file (ProviderSpec YAML/JSON), env-key discovery, unavailable-model UX |estimable: yes |method: analogue |owner: implementation-engineer |files: chatroom/config/providers.yaml, chatroom/config/loader.py |effort: 3h

PARALLEL-ELIGIBILITY:
SQ[2] (types) → gate for SQ[3-11] (providers + engine)
SQ[3-6] (providers) → parallel cluster A (¬shared files)
SQ[7-11] (engine) → parallel cluster B (¬shared files with cluster A)
SQ[13-14] (UI) → parallel cluster C, can start after SQ[2] with stubs
Merge point: SQ[12] integration test (requires A+B complete)
SQ[15-17] → sequential after M2 complete

---

#### CAL[] — Effort Estimates

RC[chatroom-engine]: reference-class=multi-provider SDK adapter + async streaming + tool-loop (similar: LangChain multi-provider, Autogen backends) |base-rate=2-4 days for engine layer in Python async stack |sample-size=3 reference projects |src: agent-inference + community build reports |confidence: M

CAL[M0-viability]: point=2-4h |80%=[2h, 4h] |90%=[1.5h, 5h] |breaks-if: 4-criteria expanded scope reveals async-bridge fix takes full 4h
CAL[M1-engine]: point=6d |80%=[5d, 9d] |90%=[4d, 12d] |breaks-if: Gemini adapter round-trip fails fixture test (add 1-3d), Ollama native streaming chunk shape wrong (add 1d) |corroboration: Brad external review (60-70% of whole project) + BC[impl#11] SQ-sum + DA[#10] — 3-way convergence |M1-fraction: 6/11=55% point, 9/14=64% 80th-upper — within Brad's range
CAL[M2-streamlit]: point=2d |80%=[1.5d, 3.5d] |90%=[1d, 4d] |breaks-if: M0 BRANCH(b) fails (windowed render required adds 1d to M2)
CAL[M3-sigma-mem]: point=2d |80%=[1.5d, 3d] |90%=[1d, 4d] |breaks-if: MCP subprocess start unreliable (add 0.5d), metrics panel layout issues (add 0.5d)
CAL[total-v1]: point=11d |80%=[9d, 16d] |90%=[7d, 20d] |communicate-as: 14-18d not 10-11d |breaks-if: M1 Gemini+Ollama adapter both fail → 13-15d; Streamlit bridge requires architecture revision → +3d

NOTE: CAL[M1] revised from 4d→6d. 3-way corroboration: Brad external critique (60-70% of whole project) + BC[impl#11] SQ-sum (~47-52h ≈ 6-6.5d) + DA[#10] — revision accepted per DA[#10] concession. §2b gap resolved to outcome 1 (revised via corroboration). communicate to build-track: plan as 14-18d not 10-11d.

§2b: no direct precedent in this codebase for multi-provider streaming. Estimate revised to 6d point via 3-way corroboration. |outcome: 1 (revised from gap — corroboration sufficient)

---

#### PM[] — Pre-Mortem

PM[1]: Gemini adapter breaks after Google GenAI SDK minor update |probability: 35% |early-warning: CI test failures on Gemini fixture after pip update |mitigation: pin google-genai version; test against fixture, not live API; version bump = explicit decision
Why: Google GenAI SDK is in active development, function_call/function_response API has changed before (send() deprecated Q3 2025). Semver minor bumps have broken API shapes in 2024-2025.

PM[2]: Small-model tool reliability causes session deadlocks |probability: 40% |early-warning: TurnEngine timeout counter incrementing rapidly; session log shows repeated tool_call attempts with malformed JSON |mitigation: tool_use_reliability taxonomy enforced at session start; "unreliable" models get tools=None; tool-exec loop max_iterations=3 hard cap; TurnEndEvent always emitted even on loop exit
Why: gemma4:e4b, nemotron-3-nano:4b are 4B parameter models. Structured JSON tool_call emission at this scale is unreliable. If a model emits malformed tool_call JSON the SDK may swallow it (finish_reason=stop, empty content) — session hangs waiting for tool_result that was never requested.

PM[3]: ConversationHistory bloat makes later turns incoherent |probability: 50% |early-warning: input_tokens reported in TurnEndEvent approaching model context window; model outputs become incoherent or repetitive |mitigation: per-model context budget in ProviderSpec; truncation strategy (keep system preamble + last N messages); CAL[context-truncation]: token estimate via len(text)//4 as proxy, calibrate against reported input_tokens in first 5 turns
Why: 13-model round, 10 rounds = 130 messages. At 500 tokens/turn average, total history = 65K tokens. Exceeds gemma4:e4b 8K window in 16 turns.

PM[4]: Streamlit session state corruption between reruns causes duplicate turns |probability: 30% |early-warning: JSONL shows duplicate turn_ids; UI shows same message twice |mitigation: all mutable state in st.session_state; ChatOrchestrator created once and stored in st.session_state["orchestrator"]; generator state managed inside TurnEngine ¬in Streamlit global
Why: Streamlit reruns the entire script on every interaction. If orchestrator or conversation history is re-initialized on rerun, the session appears to restart. Standard Streamlit pattern: initialize once in st.session_state.

PM[5]: Async event loop interference between providers in rapid succession |probability: 25% |early-warning: "Event loop is already running" RuntimeError in Streamlit logs; turns fail silently after first model |mitigation: queue-based sync bridge (not asyncio.run() which creates new loops); explicit loop lifecycle management per turn; VIABILITY experiment tests this directly

---

#### Hypothesis Matrix (§2f) — Top architecture decisions with ≥3 competing approaches

Comparing H4 (multi-model from M1a vs single-model first):
E[1]: integration-risk=high |H4-multi-from-M1a:+/M |H4-single-first:-/M — single-first catches SDK issues before adding multi-model complexity
E[2]: research-instrument-validity=high |H4-multi-from-M1a:+/H |H4-single-first:0/M — multi-model engine is the core artifact; single-model test is testing SDK wrapping (useful but not the goal)
E[3]: debugging-ease=medium |H4-multi-from-M1a:-/M |H4-single-first:+/H — single-model is easier to debug
Verdict: H4 CONFIRMED with modification — M1a should test 2-provider combo (¬13-model from start), but DO build multi-provider engine from M1a, ¬single-provider stub. The point: engine handles multi-provider from day 1; roster can be 2 for M1 testing.

---

#### §2a Positioning Check (overall approach)

Purpose-built Python async multi-provider chatroom: NOT the default approach (most multi-model work uses LiteLLM, LangChain, or pre-built UI). This is intentionally lower-level to preserve observability (C5, instrument design). Ecosystem: growing (multi-model research tools proliferating). Migration cost if Streamlit wrong: medium (engine is UI-agnostic if IC[7] ChatOrchestrator has no Streamlit imports). §2a outcome: 2 — confirmed with acknowledged risk that going lower-level increases per-provider maintenance burden.

---

#### §2b External Calibration

No direct precedent in this codebase. Closest analogues: sigma-verify (single-shot multi-provider, ¬streaming), sigma-ui (async dispatch bridge, different shape). Industry norm for "multi-provider streaming chatroom" Python prototype: 2-5 days for engine, 1-2 days for UI, 1-2 days for integration hardening = 4-9 days. Our CAL[M1-engine] at 4d is at the optimistic end. §2b outcome: 3 — flagged gap: no precedent in codebase, estimate at optimistic end of industry range. DA should scrutinize M1 estimate.

---

#### XVERIFY — Top Load-Bearing ADR

Top-1 load-bearing ADR: ADR[6] (Ollama native /api/chat required). This is the most surprising finding with production impact — if wrong, Ollama providers appear to work but silently drop tool_calls.

XVERIFY[advisory]: ADR[6] claim that OpenAI compat layer silently drops tool_calls in streaming is sourced from production GitHub issues (T1-verified by user count + maintainer acknowledgment). ΣVerify available per infrastructure section. Advisory (¬security-critical). Confirming sources: openclaw/openclaw#11828 (maintainer confirms), ollama/ollama#12557 (open issue, no fix). Cross-validate with native API test in VIABILITY[2h] experiment. |XVERIFY-SKIP-REASON: advisory, non-security; viability experiment provides direct empirical confirmation which outweighs model-to-model verification| — flagging as outcome 2 (confirmed with risk) rather than formal XVERIFY call.

Note: §2h states ΣVerify advisory for non-security in C1. Viability experiment is a direct empirical test of this claim — stronger evidence than cross-model opinion. Proceeding without XVERIFY call per §2h advisory guidance.

---

#### Files Implied by Plan

| File | Action | Description |
|------|--------|-------------|
| chatroom/types.py | CREATE | CanonicalMessage, ChatEvent union, ToolDefinition, ToolResult, ProviderSpec |
| chatroom/providers/__init__.py | CREATE | ProviderProtocol ABC |
| chatroom/providers/anthropic_provider.py | CREATE | Anthropic streaming + tool_use adapter |
| chatroom/providers/openai_provider.py | CREATE | OpenAI streaming + tool_calls adapter |
| chatroom/providers/gemini_provider.py | CREATE | Gemini streaming + function_call adapter |
| chatroom/providers/ollama_provider.py | CREATE | Ollama native /api/chat streaming + tool adapter |
| chatroom/engine/turn_engine.py | CREATE | TurnEngine: tool-exec loop, ToolCallRecord |
| chatroom/engine/history.py | CREATE | ConversationHistory + truncation |
| chatroom/engine/orchestrator.py | CREATE | ChatOrchestrator + YieldNextPolicy |
| chatroom/tools/registry.py | CREATE | ToolRegistry |
| chatroom/tools/sigma_mem.py | CREATE | sigma_mem_recall MCP stdio client |
| chatroom/persistence/session_writer.py | CREATE | JSONL writer + raw sidecar |
| chatroom/config/providers.yaml | CREATE | 13-provider ProviderSpec roster |
| chatroom/config/loader.py | CREATE | env-key discovery, model availability check |
| chatroom/app.py | CREATE | Streamlit app entry point |
| chatroom/ui/render.py | CREATE | ChatEvent → Streamlit rendering |
| chatroom/ui/metrics.py | CREATE | live ToolCallRecord panel |
| experiments/viability.py | CREATE | M0 viability experiment (Anthropic stream + tool_use + Streamlit bridge) |
| tests/test_adapters.py | CREATE | round-trip adapter fixture tests |
| tests/test_m1_integration.py | CREATE | headless 2-model session test |
| tests/test_m3_integration.py | CREATE | 3-model autonomous session test |
| pyproject.toml | CREATE | dependencies: anthropic, openai, google-genai, ollama, mcp, streamlit |

### product-designer

#### VIABILITY[H11] — DESIGN VERDICT: CONDITIONAL GO

H11 addressed first per task instruction — precondition to all other design decisions.

VERDICT: Streamlit viable with explicit pattern constraints. NOT a clean go.

Evidence FOR:
- st.write_stream accepts non-string events: "String chunks use typewriter effect; other data types use st.write" |source:independent-research(WebFetch:docs.streamlit.io):T1| — tool_call badges are renderable inline via mixed-type generator
- st.fragment with run_every supports isolated reruns (0.5s documented minimum) without full-page rerun |source:independent-research(WebFetch:docs.streamlit.io):T1| — key enabler for per-speaker streaming isolation
- Streamlit SSE (v1.32+) outperforms Gradio polling for streaming: 500-token response 3.8s vs 4.2s |source:independent-research(WebFetch:markaicode.com):T2|
- Fragment auto-rerun pattern: "only the fragment updates, not the entire application" — multiple fragments could stream different data simultaneously |source:independent-research(WebFetch:docs.streamlit.io):T1|

Evidence AGAINST / risks:
- "One turn per rerun" constraint is real: autonomous mode = engine advances one speaker turn per Streamlit rerun cycle; not simultaneous parallel streaming |source:independent-research(WebFetch:discuss.streamlit.io):T1|
- Async generator caveats: "can raise error if generator depends on cached object with async references" |source:independent-research(WebFetch:docs.streamlit.io):T1|
- RuntimeError: Event loop is closed with astream generators — reported July 2025, async bridge remains fragile |source:independent-research(WebSearch):T2|
- Long transcripts: full script re-execution on rerun means O(n) render cost per turn for entire transcript list |source:agent-inference — flagged for DA challenge|
- Chainlit outperforms both Streamlit and Gradio for LLM chat observability (built-in streaming, per-message metadata, tool-use display) |source:independent-research(WebSearch):T2| — but contradicts C2 constraint

THREE CONDITIONS FOR GO:
1. Transcript rendering uses st.fragment to isolate rerun cost (not whole-page rerun per turn)
2. Autonomous mode implemented as "poll → render queued completed turn → rerun" — NOT "stream all speakers simultaneously"
3. Tool_call events filtered from write_stream generator, rendered as separate st.expander elements within chat_message container

If M1b feasibility prototype shows any of three conditions are unachievable → FALLBACK to Textual TUI.

FALLBACK: Textual TUI — asyncio-native, 120 FPS delta renders, worker pool for parallel API calls |source:independent-research(WebSearch+WebFetch):T2|. Build cost ~1.5x Streamlit. Chainlit excluded: adds FastAPI server dependency, contradicts C1 local simplicity.

§2e premise viability:
VIABILITY[H11] — §2e flag: load-bearing assumption = "researcher observes completed turns, not simultaneous token-by-token parallel streams." For v1 3-model autonomous, sequential-within-rerun at ≥500ms inter-turn is acceptable. IF M4 adds simultaneous parallel streaming requirement → Streamlit cannot support it without custom HTML component. Flagged: outcome 2, acknowledged risk. |source:agent-inference|

§2a positioning:
Streamlit is NOT the default for multi-speaker real-time chat. Chainlit is purpose-built for this shape. Streamlit is correct for research instrument Python apps with existing sigma-ui codebase precedent. C2 pins Streamlit; re-evaluable under H11 only. Outcome: 2 — confirmed with flagged risk.

---

#### DS[1] — TRANSCRIPT RENDERING: Fragment-isolated append-only list

DECISION: Transcript renders as append-only st.chat_message list inside @st.fragment. Fragment reruns on timer (run_every=1.0s when autonomous active) OR on session_state["turn_ready"] flag. Each turn = st.chat_message(name=speaker_name, avatar=speaker_color_circle). Within each message: st.write_stream for token chunks (sync generator reading from session_state["pending_chunks"]), then ToolCallBadge elements appended after stream completes.

ALTERNATIVES:
A: Full-page rerun on each turn (simplest) — rejected: O(n) re-render cost grows linearly with transcript length; 80-turn session = 80x full script execution
B: st.empty placeholder per speaker, updated in-place — rejected: Streamlit does not support true in-place async updates; placeholder overwrites not appends
C: Custom HTML/JS streaming component — rejected: complexity exceeds v1 scope; reserve for M4

RATIONALE: Fragment isolation is the documented Streamlit pattern for "display data that updates independently from the rest of the script" |source:independent-research(WebFetch:docs.streamlit.io):T1|. Append-only from session_state["transcript"] list means fragment reruns re-render the growing list — stateless re-renders from Python list, acceptable at <100 turns. sigma-ui precedent: fragment renders <50ms at 80 items |source:cross-agent(product-designer:memory.md):T2|.

DB[DS1]:
(1) initial: fragment-isolated list is correct
(2) assume-wrong: fragment rerun at 1s on 80-turn transcript = 80 st.chat_message renders each second — does this cause visible stutter?
(3) strongest-counter: Python loop over 80-item list + 80 st.chat_message calls — even at 50ms each = 4s loop, which exceeds 1s rerun interval → rerun queue backlog → Streamlit may hang
(4) re-estimate: 50ms per item estimate from sigma-ui is for monitoring-grade panels (fewer renders per item); chat_message may be more expensive with write_stream calls embedded
(5) reconciled: explicit 100-turn soft cap with st.warning at 80 turns. Feasibility prototype MUST benchmark at 50, 80, 120 turns before committing architecture. If render >300ms at 80 turns → windowed virtual render (show last 30 turns + "see full log" link). |source:cross-agent:T2 — revised by DB[DS1]|

DS[1] §2c: maintenance cost = medium (fragment timing bugs possible). Justified by current requirement. Reversal cost = 1 day. OUTCOME 2: confirmed with 100-turn cap acknowledgment.

---

#### DS[2] — SPEAKER IDENTITY: Color-ring avatar + name badge every message

DECISION: 13-step perceptual hue palette, HSL steps at: 0°, 28°, 55°, 83°, 110°, 138°, 165°, 193°, 220°, 248°, 276°, 303°, 331° (S=75%, L=45% on white — WCAG AA 4.5:1 math-verified). Avatar = colored circle with 2-char initials. Name badge = st.badge with display_name + model_family icon (A/O/G/L). Name badge visible on EVERY message (not just speaker-change turns — see DB[DS2] below).

ALTERNATIVES:
A: Background color per speaker — rejected: WCAG contrast fails for pastel backgrounds with dark text; cognitive load on long dense transcripts
B: Icon-only avatars per model family — rejected: 4 families × up to 4 models each = many duplicates; identity collapses
C: Color + positional layout (left/right per speaker) — rejected: Streamlit chat_message does not support positional variation; all left-aligned

RATIONALE: Color + text dual-cue satisfies WCAG non-color requirement. Production precedent: Poe Group Chats (up to 200 models), Otter.ai speaker labeling |source:independent-research(WebSearch):T2|. 13-step hue spacing is near-perceptually-equidistant (Munsell-approximate) without red-green adjacency for color-blind safety.

DB[DS2]:
(1) initial: 13-hue palette with name badge on speaker-change turns
(2) assume-wrong: researcher scanning dense autonomous stream — can they identify speaker 9 vs 11 by hue under time pressure?
(3) strongest-counter: after 20+ turns, hue mapping requires active recall, not pre-attentive recognition; researcher must scan back to legend — cognitive load accumulates
(4) re-estimate: hue is fast pre-attentive cue; text is verification. NAME BADGE ON EVERY MESSAGE is required for fast scan under time pressure; speaker-change-only badge creates ambiguity in long same-speaker runs
(5) reconciled: name badge on EVERY message. Hue = pre-attentive signal. Text = confirmation. Cost: denser transcript — acceptable for research instrument. |source:agent-inference — revised from initial|

DS[2] §2a: color-coding multi-speaker is industry standard (Slack, Discord, Poe). 13 colors at upper limit — WCAG requires non-color secondary cue, name badge on every message satisfies. OUTCOME 2: confirmed.

---

#### DS[3] — PREAMBLE VARIANT PICKER: Labeled session variable, not cosmetic toggle

DECISION: Preamble variant in sidebar section titled "Session Variables" (not "Experimental" — see DB[DS3]). Dropdown with description per option: ["neutral — no identity context", "identity-aware — tells models who they are", "research-framed — tells models this is a study", "custom — opens text area"]. Selected variant displayed as persistent st.badge in session header. Variant written to session_state["session_metadata"]["preamble_variant"] on "Start Session" click (not on init). Verbatim preamble text captured in JSONL header for "custom" variant.

RATIONALE (H9/H10): H9 states preamble is an experimental parameter. Cosmetic toggle treatment makes preamble variant unobservable in session analysis. Three UX signals communicate "this is a study variable": (a) section label "Session Variables," (b) persistent header badge, (c) JSONL header entry with verbatim text. H10 (YieldNext discoverability): "custom" text area lets researcher craft preamble that does/doesn't mention @next:<name> convention — captured verbatim in log, making H10 observable.

§2e: assumption that "Session Variables" label changes researcher behavior vs cosmetic toggle — [agent-inference:T3]. Maintained because the alternative definitively loses observability: wrong inference = minor UX friction; cosmetic treatment = lost experimental data. OUTCOME 2: acknowledged.

DB[DS3]:
(1) initial: section label "Experimental" to signal study variable status
(2) assume-wrong: "Experimental" label is patronizing — researcher knows preamble matters
(3) strongest-counter: "Experimental" may cause over-thinking on every session setup, adding friction
(4) re-estimate: badge + JSONL logging are non-negotiable (observability). Label itself is secondary
(5) reconciled: label = "Session Variables." Persistent badge + JSONL unchanged. |source:agent-inference — revised|

---

#### DS[4] — TOOL-CALL BADGES: Inline collapsed, click-to-expand, three-state visual

DECISION: When model invokes sigma_mem_recall, st.expander injected into chat_message container immediately after triggering text. Default: collapsed, single-line header = [TOOL: sigma_mem_recall | ⏱ {latency}ms | {status}]. Three visual states:
- INVOKED (awaiting result): amber badge, spinner
- SUCCEEDED: green badge, ✓, latency shown
- ERRORED: red badge, ✗, error_type shown

On expand: query sent + result_length + first 200 chars of result + "... [full result in session log]". Error expand: error type + message.

RATIONALE (H8): Three-state visual maps directly to H8 requirement — distinguish "declined" from "tried and emitted malformed JSON." Without INVOKED state, researcher cannot tell the difference. st.expander is correct Streamlit pattern for collapsed detail |source:cross-agent(product-designer:memory.md):T2 — sigma-ui B3 phase detail panels|.

§2a: tool-call inline visualization in Streamlit chat — NO established production precedent found for inline collapsed tool-call badges inside st.chat_message stream |source:independent-research(WebSearch):T2 → T3 risk — novel pattern|. Pattern extrapolated from sigma-ui expander usage. FLAG: T3 source on this specific pattern. OUTCOME 3 (gap): flagged for DA challenge and ui-ux-engineer validation in M1b prototype.

---

#### DS[5] — METRICS PANEL: Right-side fragment, three-tab hierarchy

DECISION: Metrics panel in right column (st.columns layout — Streamlit has no right sidebar natively; right column pinned via layout). @st.fragment with run_every=2.0s (slower than transcript, reduces CPU). Tab structure: [Per Speaker | Per Tool Call | Session]. 

Per Speaker tab: st.dataframe — Speaker | Turns | Tokens | TTFT_p50ms | Stop_reason | Tool_calls | Tool_lat_mean.
Per Tool Call tab: st.dataframe — Speaker | Query_preview | Latency_ms | Result_chars | Turn_pos.
Session tab: st.metric row — elapsed_time | truncation_events | yield_next_override_rate. Plus: "Pause metrics" toggle.

Event-driven trigger: session_state["turn_complete_flag"] = True → metrics fragment checks flag + runs immediately + clears flag. Hybrid run_every + event trigger eliminates 0-2s staleness on turn completion.

§2c: per-tool-call dataframe grows unbounded — at 100 tool calls: fine. At 1000: pagination needed. v1 local research = <100 calls. OUTCOME 2: confirmed for v1, noted for M4.

---

#### DS[6] — SIDEBAR CONTROLS: Three collapsible sections, disabled state matrix

DECISION: Sidebar in three st.expander sections (default expanded):
1. "Session Variables" — preamble variant picker, tools_enabled toggle, mode toggle (Autonomous ↔ Human-Moderated)
2. "Model Roster" — st.multiselect from pool of 13; each model shows: name, family icon, tool_use_reliability dot (green=reliable, amber=experimental, red=unreliable). Env-key-absent: struck-through name, tooltip "API key not found: set {ENV_VAR}". Min 2 models enforced. Roster LOCKED after session start.
3. "Session Controls" — Start / Pause / Resume (autonomous), Inject Message (human-moderated), Advance Turn (human-moderated). Inject opens st.chat_input inline.

Disabled state UX: st.multiselect option_disabled for unavailable models. Post-session-start: roster section shows "Locked — export and start new session to change models" notice.

---

#### DS[7] — SESSION MANAGEMENT: Minimal pre-session list, JSONL-native

DECISION: On app load before session started: last 10 sessions in st.dataframe — ID | Date | Roster | Turns | Preamble_variant. Actions: Load (read-only transcript view), Export (path to clipboard via st.code), Delete (st.dialog confirmation). No in-session resume. Session header persists during active session (session_id, roster, preamble_variant as badge, elapsed time as st.metric auto-update).

JSONL format per tech-architect ADR[7] — read-only view renders JSONL as transcript replay.

§2c: 100-session list = fine. 10K sessions = pagination needed. v1 ~50 sessions max. OUTCOME 2.

---

#### IX[] — Interaction Patterns

IX[1]: AUTONOMOUS MODE START
Select models → set session variables → click Start → session header appears → transcript fragment begins polling → first model's completed turn renders in chat_message → subsequent turns append as TurnEngine advances → researcher observes. Can Pause at any time (Pause button in Session Controls). 
Edge cases: <2 models selected → inline validation error in sidebar before Start enabled. All models unavailable → Start blocked with modal. Rate limit mid-session → st.toast + metrics event counter + session auto-pause at 3 consecutive failures.

IX[2]: HUMAN-MODERATED ADVANCE
Start session → first model speaks → Advance Turn button activates → researcher clicks to step to next speaker → Inject Message available via chat_input (renders as "researcher" speaker, distinct color: grey, no model badge). "Next Speaker" dropdown in controls (no drag-and-drop in Streamlit — explicit dropdown workaround).

IX[3]: MID-SESSION ROSTER EDIT
Intentionally not supported in v1. Roster picker disabled after session start with tooltip: "Roster locked — export and start new session to change models." Deliberate: roster changes invalidate turn-order and metrics context — clean experimental separation required.

IX[4]: PREAMBLE CHANGE
Only before session start. After start: read-only badge in session header. Change requires new session. Forces clean experimental separation between preamble conditions — directly serves H9/H10 observability.

IX[5]: TOOL-CALL EXPAND
Researcher clicks st.expander header → expander opens (query + result preview) → click to collapse. Does NOT trigger transcript fragment rerun (Streamlit manages expander state in session_state automatically).

IX[6]: METRICS DRILL-DOWN
v1: per-speaker dataframe row-click not wired (Streamlit dataframe row selection exists but requires session_state wiring — deferred to M4). Workaround: researcher filters per-tool-call tab by speaker column.

---

#### CT[] — Component Tree

```
chatroom/app.py               # entry: page config, layout, session_state init
├── chatroom/ui/sidebar.py    # left sidebar — all controls
│   ├── SessionVariablesPanel(preamble_variant, tools_enabled, mode)
│   ├── RosterPicker(model_pool, selected, locked)
│   └── SessionControls(mode, active, callbacks)
├── chatroom/ui/transcript.py # @st.fragment — transcript
│   ├── TranscriptFragment(transcript: list[Turn], run_every=1.0)
│   │   └── TurnView(turn: Turn)
│   │       ├── SpeakerBadge(name, color, model_family, tool_use_reliability)
│   │       ├── TokenStream(chunks: list[str])  # sync gen wrapper for write_stream
│   │       └── ToolCallBadge(record: ToolCallRecord)  # st.expander 3-state
│   └── EmptyTranscriptPlaceholder()  # pre-session
├── chatroom/ui/metrics_panel.py  # @st.fragment — metrics
│   ├── MetricsFragment(metrics: SessionMetrics, run_every=2.0)
│   │   ├── PerSpeakerTab(speaker_metrics: dict)
│   │   ├── PerToolCallTab(tool_call_records: list)
│   │   └── SessionTab(session_metrics: SessionMetrics)
│   └── MetricsPausedBanner()
├── chatroom/ui/session_manager.py  # pre-session list
│   └── SessionListView(sessions: list[SessionHeader])
└── chatroom/ui/controls.py   # shared primitives
    ├── SpeakerColorMap(provider_specs)  # deterministic palette assignment
    ├── StatusBadge(status, text)        # 3-state colored badge
    └── ToastNotifier(event_type)        # rate_limit, error, truncation
```

Props contracts (aligning with tech-architect IC[]):
- Turn = {speaker_id, speaker_name, speaker_color, model_family, chunks: list[str], tool_call_records: list[ToolCallRecord], stop_reason, token_count, ttft_ms, turn_index}
- ToolCallRecord (from IC[]) extended for UI: + status: invoked|succeeded|errored + result_preview: str + error_type?: str
- SessionMetrics = {per_speaker: dict, tool_calls: list[ToolCallRecord], elapsed_s, truncation_events, yield_next_override_rate}

---

#### EMPTY / LOADING / ERROR STATES

Pre-session: SessionListView (last 10 sessions) or "No sessions yet." Metrics: placeholder. Controls: all enabled except session-dependent buttons (greyed).

Model error mid-stream: partial token stream + st.error(f"{speaker} errored: {error_type}") in TurnView. Turn marked stop_reason=error. Session continues with next speaker unless all models errored.

Tool unavailable: ToolCallBadge ERRORED state (red). Session continues. metrics tool_error_count++.

Rate-limited: st.toast("Rate limited — retrying in {backoff}s"). If 3 consecutive: st.warning in transcript fragment header + auto-pause.

Long truncation: st.info divider in transcript — "Context truncated — {N} earlier turns removed. Full transcript in session log." metrics truncation_events++.

---

#### ACCESSIBILITY

Contrast: 13-hue palette at S=75%, L=45% — WCAG AA 4.5:1 claimed via HSL math. FLAGGED: T3 source (agent-inference calculation) — UI engineer must validate with contrast checking tool before ship. |outcome:3 — gap flagged|

Color-blind: dual-cue (hue + name badge every message) satisfies WCAG non-color requirement. Initials add third cue.

Keyboard: Streamlit sidebar Tab/Enter accessible. st.expander keyboard accessible. st.multiselect keyboard navigable. No custom JS required for v1.

Screen reader: st.chat_message renders semantic HTML (article element) — screen reader announces speaker name. write_stream typewriter: aria-live="polite" is Streamlit default — cannot override without custom component. Known gap for v1: repetitive announcements during streaming. Flagged.

Focus: Streamlit 1.32+ preserves focus across fragment reruns |source:independent-research(WebSearch):T1|.

Responsive: EXPLICIT NON-GOAL v1. Single researcher, local, 1440×900+. Acceptable breakage below 1200px.

---

#### ANALYTICAL HYGIENE CHECKLIST

§2a: OUTCOME 2 — Streamlit conditional confirmed; alternatives documented
§2b: OUTCOME 3 (gap) — no precedent for 13-speaker streaming instrument in this codebase; sigma-ui precedent is monitoring-grade (different render shape); effort estimate gap flagged for DA
§2c: OUTCOME 2 — O(n) transcript risk addressed with 100-turn cap; metrics dataframe v1 bounded
§2e: OUTCOME 2 — H11 conditional go with three explicit conditions; fallback path documented
Source provenance: all findings tagged T1/T2/T3 with source type. T3 findings (tool-call badge pattern, contrast math, sequential turn UX) flagged for DA challenge.

---

#### SQ[] — Design + Frontend Sub-tasks

SQ[D1]: Design token file — 13-hue palette, status colors, spacing scale, typography |CAL:2h|
SQ[D2]: SpeakerBadge spec — all 13 color variants + error + env-key-absent states |CAL:2h|
SQ[D3]: ToolCallBadge spec — 3 states, expand/collapse, full-query view spec |CAL:3h|
SQ[D4]: MetricsFragment layout — 3-tab structure, dataframe schemas, st.metric layout |CAL:3h|
SQ[D5]: SessionVariablesPanel spec — dropdown variants, persistent badge, JSONL hook |CAL:2h|
SQ[D6]: Sidebar IA — section order, disabled state matrix for all 13 model availability combinations |CAL:2h|
SQ[D7]: Empty/error/loading state specs for all 5 states |CAL:2h|
SQ[D8]: Accessibility audit checklist — contrast ratios (validate T3 math), keyboard nav, screen reader gaps |CAL:1h|

SQ[F1]: transcript.py — TranscriptFragment + TurnView + TokenStream + ToolCallBadge |CAL:4-8h| (H6 contested — budget 8h for async bridge work)
SQ[F2]: sidebar.py — 3 panels, disabled states, validation, roster lock |CAL:3-5h|
SQ[F3]: metrics_panel.py — MetricsFragment, 3-tab, pause toggle, event-driven trigger |CAL:3-5h|
SQ[F4]: session_manager.py — JSONL write, session list view, load/export/delete |CAL:2-4h|
SQ[F5]: controls.py — SpeakerColorMap, StatusBadge, ToastNotifier |CAL:2-3h|
SQ[F6 = M1b GATE]: Feasibility prototype — stream 1 model token through queue-bridge → st.write_stream, render ToolCallBadge inline, benchmark rerun cost at 50/80/120 turns |CAL:2-4h| — MUST run before F1-F5 commit

CAL design total: 17h | frontend total: 16-29h | feasibility-gated: F6 gates F1-F5

---

#### PM[] — Pre-Mortem (UI-specific failures)

PM[D1]: RERUN THRASH — transcript fragment at 1s interval on 80-turn session; render loop takes >500ms at 120 turns; rerun queue backlog; Streamlit hangs or stale transcript visible.
Mitigation: 100-turn soft cap (warning at 80); benchmark in F6 prototype; if >300ms at 80 turns → windowed render (last 30 turns).

PM[D2]: TOOL-CALL BADGE SILENT FAILURE — researcher observes 0 tool badges for model that attempted tool use; interprets as "model didn't use tool" — wrong conclusion. Root cause: H8 raw-event capture not implemented in TurnEngine → SDK swallows malformed tool_call JSON → no ToolCallRecord emitted → no badge rendered.
Mitigation: UI design is correct (3-state). Risk is backend non-implementation. Flag to tech-architect and implementation-engineer: raw_events_only mode is a DESIGN PRECONDITION for the 3-state badge, not an optional enhancement.

PM[D3]: PREAMBLE VARIANT NOT IN LOG — researcher runs 5 sessions varying preamble; variant not written to JSONL header due to session_state timing bug. All sessions log preamble_variant = "neutral." Comparative analysis invalidated.
Mitigation: JSONL header write on "Start Session" click, not on session_state init. Assert preamble_variant non-empty before write. Test: start without selecting → defaults to "neutral" not empty.

PM[D4]: SPEAKER COLOR COLLISION — deterministic color from model_id hash produces same color for two models if pool > 13. Two models visually indistinguishable.
Mitigation: color assigned from session-specific palette at session start; stored in session_state["color_map"]; deterministic within session not globally.

PM[D5]: METRICS STALENESS ERODES TRUST — researcher pauses to read metrics mid-session; turn_count shows 5 when 6 turns completed. Metrics fragment 2s lag.
Mitigation: event-driven trigger on turn_complete_flag alongside run_every. Benchmark: does flag-triggered rerun race with timer-triggered rerun? Test in F6 prototype.

---

#### BELIEF TRACKING

BELIEF[plan-r1]:
- H11 VIABILITY: P=0.65 conditional go | key uncertainty: O(n) transcript rerun cost at 80+ turns unmeasured; sigma-ui precedent partially applicable (monitoring-grade ≠ chat-streaming-grade)
- DS[1] fragment-isolated transcript: P=0.75 | async bridge fragility is live risk (RuntimeError reports July 2025)
- DS[3] preamble-as-study-variable: P=0.95 | directly grounded in H9/H10, no viable alternative that preserves observability
- DS[4] tool-call badge 3-state inline: P=0.70 | novel Streamlit pattern, no production precedent; feasibility prototype gates
- Textual TUI fallback probability: P=0.35 that it becomes necessary after M1b prototype

---

#### CONVERGENCE DECLARATION

product-designer: ✓ plan-r1 |VIABILITY[H11]:conditional-go(3 conditions: fragment-isolation+sequential-turn+mixed-type-gen)|DS:#7(transcript,speaker-identity,preamble-variant,tool-badge,metrics,sidebar,session-mgmt)|IX:#6(autonomous-start,human-moderated,roster-lock,preamble-change,tool-expand,metrics-drill)|CT:#6(app+sidebar+transcript+metrics+session-manager+controls)|PM:#5(rerun-thrash,badge-silent-fail,preamble-log-miss,color-collision,metrics-staleness)|key-gaps:tool-badge-pattern(T3-novel,DA-challenge),contrast-math(T3-validate-needed),O(n)-rerun-cost(F6-prototype-gates)|→ ready-for-build-track-challenge+DA-challenge

### product-strategist

#### VIABILITY[H11] — precondition gate (evaluated first)

§2e premise-viability — assumptions required for instrument shape to succeed:
(1) Streamlit async bridge tractable — CONTESTED. Tech-architect ADR[5] confirms st.write_stream accepts async generators internally, but queue-based sync bridge is the reliable pattern for tool_call events (which are NOT strings). Community production reports confirm "Event loop is already running" as most common Streamlit async error. Tractable with the right bridge — real friction, not fatal. |source:[independent-research]|T2-corroborated
(2) Native tool-use across heterogeneous models observable — VARIABLE. BFCL V4: 7B-32B open models exceed 70% tool-call pass rate under ReAct. FC vs. ReAct strategy matters as much as model size — same base model shows dramatically different rates by elicitation method. Small Ollama models likely sub-70%. Ollama OpenAI-compat layer confirmed to silently drop tool_calls when streaming=True (ollama/ollama#12557 T1-verified). Native /api/chat required (tech-architect ADR[6]). |source:[independent-research]|T1-verified
(3) Strategic reframe: variability in tool-use reliability is a FEATURE of the instrument, not a blocker. |source:[agent-inference]

§2e outcome: 2 (confirmed with risk acknowledged)
VIABILITY[H11]: CONDITIONAL GO — M1-M3 scope viable with two preconditions:
(a) M0 viability prototype (2h) confirms Streamlit async bridge BEFORE M1 full build
(b) Ollama uses native /api/chat per ADR[6]
Kill-switch: M0 failure → user decides instrument shape (headless JSONL + Jupyter viewer answers Q1/Q2 without Streamlit complexity). Engineer presents options, user decides. Not an abandon signal.

---

#### Research Question Pinning

Context: v1 ships M3: 3-model autonomous, sigma_mem_recall available, ToolCallRecord populated, preamble_variant logged, metrics panel live. Single researcher. 5-15 turns per session.

**Candidate (a): Memory-invocation coherence**
Metrics required: query text similarity (cosine/token-overlap) — NLP post-processing required.
At M3: raw query TEXT logged in ToolCallRecord. Analysis is M4 work.
Verdict: DATA LOGGED at M3, analysis deferred. SECONDARY. |source:[agent-inference]

**Candidate (b): Self-reference patterns**
Confound: severe. Preamble instructs models to address others by @name → all comply → signal is preamble-driven not architectural. Low inferential value for architectural differences.
Verdict: Surface stat, TERTIARY. |source:[agent-inference]

**Candidate (c): Yield-next spontaneity**
Metrics: @next: token presence/absence per turn per model under preamble-A (mentions @next:) vs. preamble-B (silent).
H10 already identifies preamble-variant as experimental parameter. This operationalizes H10 into a binary measurement.
Confound: training data leakage — models that saw @next: in training may echo it. Real but not fatal: all-yield / none-yield / mixed are all interpretable IF pre-registered.
Verdict: CLEAN BINARY MEASUREMENT, testable at M3, preamble-variant already tracked (C4). STRONG PRIMARY CANDIDATE. |source:[agent-inference]

**Candidate (d): Tool-use reliability vs. capability**
Metrics: ToolCallRecord (invoked, malformed_json, result_used) per model vs. model metadata.
External calibration: BFCL V4 provides single-model isolated baseline. Chatroom-context measurement is a DELTA from that baseline — this is the novel contribution.
Confound: FC vs. ReAct strategy conflated with model capability in this instrument. This is the instrument's design — not eliminable, but the DELTA from BFCL baseline remains observable.
Project 3 dependency: directly serves roster assignment for cross-model sigma-review.
Verdict: CLEANLY MEASURABLE at M3, directly serves Project 3, BFCL provides external anchor. STRONG PRIMARY CANDIDATE. |source:[independent-research]|T1-verified (BFCL V4)

**DB[Q1 as primary — tool-use reliability]:**
(1) Initial: Q1 serves Project 3 + cleanly measurable at M3
(2) Assume-wrong: BFCL already answers reliability — why rebuild the measurement?
(3) Strongest counter: BFCL measures single-turn, single-model, isolated context. Chatroom adds shared transcript + heterogeneous neighbors + multi-turn history. The DELTA between BFCL and chatroom context is unmeasured and potentially material.
(4) Re-estimate: Q1 framing must be "chatroom-context vs. BFCL baseline" not just "reliability spectrum" — otherwise we confirm what BFCL already shows.
(5) Reconciled: Q1 confirmed with revised framing. BFCL = external calibration anchor; v1 = chatroom-context measurement; delta is the contribution.
§2g outcome: 1 (framing revised — "chatroom-context vs. isolated baseline" is more precise and novel than "reliability spectrum") |source:[independent-research]|T1-verified

**DB[Q2 as primary — yield-next spontaneity]:**
(1) Initial: Q2 tests H10 with binary measurement under preamble-variant controlled comparison
(2) Assume-wrong: training data leakage makes Q2 uninterpretable
(3) Strongest counter: leakage affects interpretation not measurement. All-yield = training data. None-yield = finding. Mixed = architectural variation is signal. Pre-register all three.
(4) Re-estimate: Q2 confirmed. Pre-registration of null-result interpretations is required.
(5) Reconciled: Q2 confirmed with explicit null-result pre-registration.
§2g outcome: 2 (confirmed, null-result interpretations pre-registered) |source:[agent-inference]

**PINNED PRIMARY QUESTIONS:**
Q1: "Does conversational context (heterogeneous neighbors, shared transcript, multi-turn history) change tool-invocation patterns relative to single-model isolated benchmarks (BFCL), and does reliability ordering across model families hold in chatroom context?"
Q2: "When models are NOT explicitly instructed about turn-passing conventions (preamble-B), which model families (if any) spontaneously emit @next: coordination tokens, and does this vary systematically?"

SECONDARY (data logged at M3, analyzed at M4):
Q-sec-1: Memory query coherence — raw query text logged, similarity analysis M4
Q-sec-2: Speaker self-reference patterns — low analytical value per above
Q-sec-3: Cross-model convergence on factual vs. interpretive claims — embedding M4

---

#### Research-Question-Coverage Matrix

| Pinned Q | M3 Metric | Instrument Support | Confound | Coverage |
|---|---|---|---|---|
| Q1: chatroom-context vs. BFCL | ToolCallRecord (invoked, malformed_json, result_used) | Native tool-use, per-model logs, model metadata in ProviderSpec | FC vs. ReAct conflated; BFCL = external anchor | COVERED at M3 |
| Q1: External calibration | BFCL ranking for roster models | External T1 lookup | Small sample size at v1 launch | PARTIAL — acknowledged |
| Q2: Yield-next spontaneity | @next: token presence per turn, preamble_variant | preamble_variant in ConversationHistory (C4), raw turn output in JSONL | Training data leakage (pre-registered nulls mitigate) | COVERED at M3 |
| Q-sec-1: Query coherence | sigma_mem query text in ToolCallRecord | ToolCallRecord query field | Preamble anchor on phrasing | DATA LOGGED, analysis M4 |

Coverage verdict: Q1 and Q2 answerable from M3 instrument as designed. No metric gap for primary questions. Secondary questions generate data at M3 for M4 analysis.

§2a check: "Chatroom-context vs. BFCL" is novel — most prior work (AutoGen, LangGraph, AgentLens) measures task completion, not cross-architecture tool-use in conversational context. Ecosystem: BFCL V4 actively maintained (T1). Migration cost if Q1 framing wrong: instrument still generates ToolCallRecord data, pivot costs nothing. |source:[independent-research]|T1-verified
§2a outcome: 2 (confirmed, novelty acknowledged)

---

#### Metrics — Essential vs. Luxury

MUST-HAVE for M3 (v1 ship):

| Metric | Required For | Why Essential | Cost |
|---|---|---|---|
| ToolCallRecord: invoked (bool) | Q1 | Primary tool-use signal | 0: schema field |
| ToolCallRecord: malformed_json (bool) | Q1 + H8 | Distinguishes decline from silent failure | 0: schema field |
| ToolCallRecord: result_used (bool) | Q1 | Completes reliability chain | 0: schema field |
| ToolCallRecord: query_text (str) | Q-sec-1 data | Raw query for M4 | 0: schema field |
| preamble_variant (str) | Q2 treatment variable | Without this Q2 uninterpretable | 0: ConversationHistory field (C4) |
| raw turn output (str) | Q2 | Source for @next: detection | 0: JSONL persists turns |
| model metadata (provider, tool_use_reliability) | Q1 calibration | Enables BFCL correlation | 0: ProviderSpec fields planned |
| turn timestamps | Both | Sequencing + stability audit | 0: TurnStartEvent field |

§2c check: All M3 metrics are zero-cost schema fields in events already emitted by TurnEngine and ProviderSpec. No post-processing required at collection time. |source:[agent-inference]
§2c outcome: 2 (confirmed — cost genuinely zero beyond what plan already builds)

LUXURY — defer M4:

| Metric | Why Deferred | Deferral Risk |
|---|---|---|
| Embedding-based convergence/divergence | Requires NLP pipeline | Low — turn text already logged |
| Topic drift | Embedding-dependent | Low |
| Speaker-influence graph | Needs session corpus (multiple sessions) | Low |
| Speaker self-reference count | Low inferential value | Low — regex on logged text |
| Per-model temperature UI | No v1 question requires temperature variable | Low |
| Transcript summarization | Product feature, not research metric | Low |

§2c deferral check: All deferred are reversible (schema extension at M4). None required for Q1 or Q2. |source:[agent-inference]
§2c outcome: 2 (confirmed — deferral safe and reversible)

---

#### Milestone Sequencing

M0: 2h viability prototype — BEFORE M1 build begins (kill-switch for H11)
Scope: Single Anthropic async stream with tool_use + Streamlit bridge. NOT full implementation.
Success: tool_call event visible in Streamlit distinct from token, stream renders without crash, <2h.
Kill-switch: failure → user decides instrument shape. ¬engineer decides alone.

M1a: Types + ProviderProtocol (~3h) — schema-first enables parallel cluster build
Success: types.py importable, all SQ[] stubs compile against ProviderProtocol.

M1b: All 4 Provider Adapters + Engine (parallel clusters per tech-architect SQ[] map)
Success: headless 2-model integration test passes, ToolCallRecord populated.

M1c: Streamlit async bridge prototype (~1.5h, after M1b) — validates H6 separately
Success: live streaming tokens rendered, tool_call event distinct, <2h.
Kill-switch: failure → user decides UI technology.

M2: Streamlit MVP — config panel, live streaming, raw event log
Success: researcher configures + starts + watches 3-model session.

M3: v1 ship — sigma-mem + metrics + Q1/Q2 observable
Success (per scope-boundary): 3-model autonomous, sigma_mem_recall available, ToolCallRecord populated (including query_text), preamble_variant logged, @next: detection in metrics, 10-turn unattended stability.

Alternative phasings evaluated:
Alt-A Single-model-first: REJECTED. §2a outcome 1. Single-model tests SDK wrapping not turn-coordination. 2-model from M1 is correct minimum. |source:[independent-research]|T2-corroborated
Alt-B Skip M0/M1c: REJECTED. Streamlit async failure discovered in M2 wastes M1b effort. M0+M1c = ~4h insurance vs. 2+ days rework.
Alt-C Headless first, Streamlit as M4: VIABLE fallback if M0 fails. Headless JSONL answers Q1/Q2. Deferred Streamlit loses live observation (discovery value), not measurement value.

§2b precedent check: Tech-architect CAL[M1-engine] at 4d (80%: 3-6d) is at optimistic end of industry norm. No direct codebase precedent for streaming turn-loop (sigma-verify is one-shot ¬streaming). If M1 is 5-6d and total is 10-12d, ratio is 50-60% — aligns closer to Brad's "60-70%" than tech-architect's 40% ratio implies. Plan should use 90% band (6-8d) for M3 ship date planning, not point estimate. Flagged for DA challenge. |source:[prompt-claim (Brad 60-70%) + cross-agent (tech-architect CAL[])]
§2b outcome: 3 (gap — M1 effort at optimistic end, no codebase precedent; flag for DA scrutiny)

---

#### Success Criteria Per Milestone

| Milestone | Concrete Success Criterion | Explicitly NOT Required |
|---|---|---|
| M0 | tool_call event visible in Streamlit, stream renders without crash, <2h | full UI, 3 models, sigma-mem |
| M1a | types.py + ProviderProtocol compile, all SQ[] stubs importable | real API calls |
| M1b | headless 2-model session complete, ToolCallRecord populated (invoked + malformed_json + result_used), JSONL written | Streamlit, sigma-mem |
| M1c | live streaming tokens rendered from live TurnEngine (¬mocked), tool_call event distinct, <2h | full UI |
| M2 | researcher configures + starts + watches 3-model session, inspects raw events | sigma-mem, metrics |
| M3 (v1) | 3-model autonomous, sigma_mem_recall available, ToolCallRecord populated (query_text included), preamble_variant logged, @next: detection in metrics, 10-turn unattended stability | M4 metrics, >3 models/session, sigma-mem writes |

v1 Ship Gate — must ALL be true:
- M3 success criterion above met
- Q1 observable: ToolCallRecord shows ≥1 invocation per session, malformed_json field populated
- Q2 observable: preamble_variant logged, @next: detection queryable in metrics panel
- 10-turn unattended session stability (Project 3 precondition)
- No M4 features implemented (scope creep gate)
- `streamlit run chatroom/app.py` works on researcher's local machine, no deployment (C1)

v1 Ship Gate — explicitly NOT required:
- Perfect UI aesthetics
- >3 models per session
- Embedding or NLP-based metrics
- sigma-mem writes
- Speaker self-reference counts

---

#### PM[] Pre-Mortem (strategic failure modes)

PM-PS[1]: v1 ships, Q1 unanswerable — models never invoke tool |probability:20% |early-warning:ToolCallRecord all-null across 3+ sessions including Anthropic claude-class |mitigation: pre-register null-result interpretation ("all models declined tool in chatroom context" is a finding — not a measurement failure); ensure ≥1 cloud model per session with explicit tool-encouraging preamble; if claude-opus declines tool → instrument design failure (tool accessibility not reliability) |source:[independent-research]|T1-verified (BFCL: claude-opus >90% isolated)

PM-PS[2]: v1 answers something but not what Project 3 needs |probability:20% |early-warning:Q1 shows within-session context dominates model identity (confound > signal) |mitigation: context-suppression IS a Project 3 finding. If ALL models become less reliable in chatroom context vs. BFCL, Project 3 should use isolated MCP tool-use calls not conversational. Null result = still actionable for roster design. |source:[agent-inference]

PM-PS[3]: Streamlit async bridge becomes tar pit |probability:15% |early-warning:M0 takes >2h with no clean resolution |mitigation: fallback decision tree pre-committed before M1. User decides at M0 kill-switch: (a) headless JSONL + Jupyter; (b) Textual TUI; (c) queue-based Streamlit bridge. ¬engineer decides alone. |source:[independent-research + tech-architect ADR[5]]

PM-PS[4]: Small-model tool-use noise makes Q1 uninterpretable at v1 session count |probability:20% |early-warning: after 5 sessions, tool-use bimodal (cloud reliable, small-model zero), no middle range |mitigation: bimodal IS interpretable — confirms BFCL ordering holds in chatroom context. Pre-register: "if bimodal, conclusion is ordering-confirmed." Roster: always ≥1 cloud + ≥1 mid-size + ≥1 small per session to maximize range. |source:[independent-research]|T1-verified

PM-PS[5]: Project 3 blocked by v1 instability |probability:10% |early-warning: sessions above 10 turns show event-loop errors or context-budget exhaustion |mitigation: v1 ship gate includes 10-turn unattended stability. Project 3 uses v1 in controlled 5-7 turn sessions first. |source:[cross-agent — tech-architect PM[3,5]]

---

#### Decision Ramps for Project 3

Project 3 needs from v1:
1. Tool-use reliability roster (Q1 data) — which models reliably invoke sigma-mem in chatroom context? REQUIRED.
2. Provider adapter layer — ProviderProtocol reuse. REQUIRED.
3. Session stability at 10+ turns — v1 stability gate. REQUIRED.
4. Preamble as experimental parameter — Q2 informs sigma-review preamble design. USEFUL.

v1 is OK for Project 3: Q1 data + 10-turn stability + provider adapter reusable.
v1 is GREAT for Project 3: above PLUS Q2 spontaneous yield-next informs which models coordinate without explicit @next: — directly shapes sigma-review orchestration preamble design.

---

#### Analytical Hygiene Summary

§2a: Q1 "chatroom-context vs. BFCL" is novel, not default; justified by BFCL availability + chatroom-context delta being unmeasured. |outcome:2
§2b: M1 effort at optimistic end of industry range, no codebase precedent for streaming turn-loop. Gap flagged for DA. |outcome:3
§2c: All M3 metrics are zero-cost schema fields; M4 deferral reversible. |outcome:2
§2d: BFCL data = T1-verified. Streamlit async limitations = T2-corroborated. Instrument design reasoning = agent-inference. All findings tagged.
§2e: H11 conditional-go. M0+M1c as kill-switch milestones. Decision tree pre-committed. |outcome:2

XVERIFY: ΣVerify available per SCRATCH. No security-critical ADR in product-strategist domain (local research tool, read-only sigma-mem, no untrusted MCP). Per §2h: XVERIFY-SKIP (advisory, non-security). Neutral — ¬penalized.

H-coverage:
H1: Confirmed — sigma-verify wrong shape (tech-architect ADR[1]); strategist concurs (aligns with Q1 clean measurement requirement)
H2: Confirmed — native tool-use required; text convention destroys the tool-use authenticity signal Q1 exists to measure
H4: Confirmed with modification — 2-model from M1 (not 13-model), 2-model IS multi-model
H5: FLAGGED — 60-70% is a [prompt-claim], unverified; tech-architect CAL[M1] at 40% of total is optimistic end; §2b gap applies; schedule should use 90% band not point estimate
H6: Conditional on M0+M1c prototypes — confirmed tractable with queue-based bridge per ADR[5]
H9: Confirmed — preamble is Q2's treatment variable; preamble_variant must be logged per ship gate
H10: Confirmed — preamble-B (silent on @next:) is Q2 control condition; preamble-A is treatment
H11: CONDITIONAL GO per above

## build-track-feasibility (build-track challenge — after plan-track Round 1)

### implementation-engineer

BUILD-CHALLENGE[implementation-engineer→tech-architect]:

---

**BC[1]: Anthropic streaming tool_use content-block reassembly**

plan-element: Provider.stream() yields StreamEvent(kind="tool_call") from Anthropic SDK stream.
feasibility: M (possible but non-trivial)
issue: Anthropic SDK messages.stream() fires on_content_block_start / on_content_block_delta / on_content_block_stop callbacks (or async iteration yields RawContentBlockStartEvent etc.). The tool_use block is assembled across multiple events: (1) content_block_start signals type="tool_use" + block id + name, (2) content_block_delta events carry input_json_delta (partial JSON), (3) content_block_stop signals completion. The plan does not acknowledge that tool_use content-block reassembly IS the streaming loop — you cannot emit StreamEvent(kind="tool_call") until content_block_stop fires and input JSON is fully assembled. During reassembly, what does the provider emit? Nothing? Token events only? The plan implies a clean token→tool_call→stop sequence but the actual stream interleaves. Specific gap: if a model emits text THEN tool_use in the same response (valid Anthropic pattern), the text events must be emitted as tokens before the tool_call — the provider must buffer the tool_use input_json_delta until stop, then emit StreamEvent(kind="tool_call"). This buffering logic is not captured in SQ[3]'s 4h estimate.
evidence: [independent-research: Anthropic Python SDK streaming docs, anthropic-sdk-python/README.md#streaming-helpers + raw stream iteration docs] T1-verified. The SDK exposes both high-level MessageStream (with with_streaming_response()) and raw async iteration. Raw iteration requires manual content-block reassembly; MessageStream helper does it but changes the yield interface.
T2: 4h estimate may be tight if using raw iteration; using MessageStream helper reduces this but couples provider to the SDK's stream object lifecycle.
→ revise: SQ[3] should explicitly state whether AnthropicProvider uses MessageStream helper OR raw async iteration, and document the content-block accumulation pattern. If raw iteration, add 1h for reassembly logic. |source:[independent-research]|T1

---

**BC[2]: OpenAI streaming tool_calls delta reconstruction (SQ[4] estimate)**

plan-element: OpenAI streaming with include_usage=True, 4h estimate.
feasibility: M
issue: The plan acknowledges "tool_calls arrive as DELTAS" in H7 assessment but does NOT detail the reconstruction algorithm in SQ[4]. OpenAI tool_calls in streaming mode arrive as: (1) first chunk contains tool_calls=[{index:0, id:"call_xyz", type:"function", function:{name:"sigma_mem_recall", arguments:""}}], (2) subsequent chunks contain tool_calls=[{index:0, function:{arguments:"{\"context\""}}], (3) more chunks append arguments JSON incrementally. You must concatenate tool_calls[i].function.arguments across all chunks for each index, then parse the assembled JSON. Additionally: multiple tool_calls can arrive in parallel (OpenAI supports parallel function calling) — the plan's max_iterations=3 cap (PM[2]) is per-loop not per-turn, but the plan does not address how TurnEngine handles a single response containing multiple tool_calls. Does it execute them serially (one at a time, appending tool results before next loop)? Does it execute them in parallel? The plan is silent on this. This is a TurnEngine decision (IC[2]) with cross-provider implications (Anthropic also supports parallel_tool_use in preview).
evidence: [independent-research: OpenAI streaming tool_calls reconstruction pattern is documented in OpenAI cookbook, confirmed by community reports — assembling index-keyed deltas is required] T1-verified. Parallel tool_calls: OpenAI platform docs + Anthropic parallel_tool_use feature (preview, requires beta header). |source:[independent-research]|T1
→ clarify: SQ[4] must document the delta-accumulation algorithm. TurnEngine (SQ[7]) must specify policy for multi-tool_call responses: serial execution (safer, simpler, compatible with all providers) OR parallel (complex, may not be supportable on all SDK families). If serial: loop N times for N tool_calls in one response. If parallel: asyncio.gather, but Ollama native API behavior with multiple tool_calls in one response is unknown. Recommend serial for v1. |source:[independent-research]|T1

---

**BC[3]: Google GenAI function_call round-trip (SQ[5] — hardest adapter)**

plan-element: GeminiProvider with function_call parts + function_response, 5h estimate.
feasibility: M (conditional — hardest surface)
issue: The plan correctly identifies the asymmetry (no role=tool, function_response in user message content). But the specific adapter complexity is larger than 5h for a first implementation:
(a) In the google-genai Python SDK (v1.x), sending a function_response back requires constructing a `glm.Content(role="user", parts=[glm.Part(function_response=glm.FunctionResponse(name=..., response={"result": str}))])` — the response dict is wrapped, not a plain string. The canonical Message (role=tool, content=str) must be adapted to this wrapped structure.
(b) Multi-part responses: a Gemini response can contain BOTH a text part AND a function_call part. If text precedes function_call, the provider must emit token events for text, then a tool_call event for the function_call — same interleaving problem as Anthropic.
(c) The google-genai SDK went through a major API change in late 2024 (send() deprecated, response streaming changed shape). PM[1] captures this risk correctly but the estimate doesn't factor in the time to validate against CURRENT SDK v1.x API, not tutorial examples.
(d) round-trip test: function_response in user content means to_provider_messages() must detect that a "tool" role canonical message should become a "user" role message with function_response part — logic is asymmetric compared to all other providers.
evidence: [independent-research: google-genai Python SDK docs + migration guide + GitHub examples] T2-corroborated (API changed, some examples out of date). Hardest edge case: mixed text+function_call in single response — confirmed by community reports. |source:[independent-research]|T2
→ revise: SQ[5] should be 6-8h not 5h. The Gemini adapter requires a dedicated fixture test BEFORE the adapter is considered done (ADR[4] already requires round-trip fixtures as merge gate — this is correct, just undercounting the time). The to_provider_messages() function for Gemini is asymmetric and the asymmetry is not captured in IC[3]'s description. Flag: GeminiProvider cannot subclass or share message_mapping logic with other providers — it needs its own function_response construction path. |source:[independent-research]|T2

---

**BC[4]: OllamaProvider — native /api/chat streaming tool_calls (SQ[6])**

plan-element: Ollama native /api/chat streaming + tool_calls, 4h estimate.
feasibility: M (conditional — empirically uncertain)
issue: The `ollama` Python library's support for streaming + tool_calls via native /api/chat is less documented than the plan implies. Key unknowns:
(a) The `ollama` Python library's `chat()` method with `stream=True` returns an iterator of response chunks. Whether these chunks include `tool_calls` field while streaming is model-dependent. Ollama's docs confirm streaming + tool_calls support "since May 2025" (ADR[6]), but the exact chunk shape when a model emits a tool_call during streaming (is it in the last chunk before finish, or spread across chunks like OpenAI deltas?) is not documented in the plan.
(b) For Ollama cloud providers (deepseek-v3.2:cloud, devstral-2:123b-cloud), the behavior may differ from local model behavior. Ollama cloud routes through their infrastructure — whether the native /api/chat endpoint behaves identically for cloud vs. local is empirically untested.
(c) The plan conflates Ollama local and Ollama cloud into OllamaProvider with base_url differentiation (DIV[10] aligned). But the TOOL RELIABILITY may differ — cloud-routed large models (deepseek) likely more reliable than local 4B models. The tool_use_reliability="unknown" default handles this via empirical discovery, but the adapter code must not assume consistent behavior.
evidence: [independent-research: ollama/ollama GitHub native API docs + Python library docs] T2-corroborated (native /api/chat tool_call streaming confirmed since May 2025 but limited examples; chunk shape during streaming not explicitly documented). [agent-inference: cloud vs local behavioral difference is inference, not confirmed] |source:[independent-research]|T2 + [agent-inference]
→ clarify: SQ[6] MUST include in success criterion: verify that streaming tool_calls via ollama Python library yields tool_calls in response chunk (not just at stream completion). If tool_calls only appear in the final non-streaming response chunk, OllamaProvider's streaming loop is fundamentally simpler than AnthropicProvider's (no delta reconstruction) but the plan should document which model is correct. This is a SQ[1]-level empirical question. Recommend: SQ[1] viability experiment must test Ollama native streaming tool_call chunk shape. |source:[independent-research]|T2

---

**BC[5]: TurnEngine tool-exec loop — max_iterations=3 and multi-tool_call gap**

plan-element: PM[2] max_iterations=3 hard cap, TurnEngine tool-exec loop (SQ[7]).
feasibility: H (yes, buildable) with specific gaps
issue-A: The plan specifies max_iterations=3 for the tool-exec loop. This is per-loop-iteration (one tool_call → execute → re-invoke = 1 iteration). For YieldNextPolicy models that call tools multiple times across different questions, 3 may be too low. More critically: what is the exit semantics when the cap is hit? Does TurnEngine (a) send a final system-injected "max tool calls reached" message back to the model and request a final response, OR (b) force-terminate the turn with TurnEndEvent(finish_reason="max_tool_calls") without another model call? The plan says "TurnEndEvent always emitted even on loop exit" (PM[2]) but does not specify whether the model gets a chance to respond after the cap. If (b), the turn ends mid-thought — the model's final content in JSONL would be the incomplete tool-calling turn, not a text response. The draft uses "force stop_reason='max_tool_calls'" (5 iterations) — same ambiguity.
evidence: [independent-research: Anthropic agent loop docs specify "send tool_result then re-invoke" as the correct pattern; force-termination without final model response produces incomplete Turn.content] T2-corroborated. |source:[independent-research]|T2
issue-B (parallel tool_calls — see BC[2]): If a single model response contains N tool_calls (OpenAI supports this, Anthropic preview supports this), the loop must handle executing N tools before re-invoking. Does max_iterations=3 mean 3 TOOL CALLS total, or 3 LOOP ITERATIONS (where one iteration might execute N tool_calls)? This distinction matters: if 3 means 3 calls, OpenAI might hit the cap in one iteration; if 3 means 3 re-invocations, OpenAI could execute 3×N tools. The plan is ambiguous. Recommend: clarify as "max 3 re-invocations; within each re-invocation, execute all tool_calls in the response" — but this requires TurnEngine to handle N-tool_call batch.
→ revise: IC[2] TurnEngine.run_turn() docstring must specify: (1) max_iterations semantics (re-invocations, not individual calls), (2) exit behavior when cap hit (force-terminate vs. request final response — recommend request final response for clean JSONL), (3) multi-tool_call handling policy. |source:[agent-inference]|T3

---

**BC[6]: ConversationHistory to_provider_messages() — truncation and tool_call/tool_result pairing**

plan-element: IC[3] ConversationHistory.truncate_to_budget() + to_provider_messages(provider_id).
feasibility: M (one real gap)
issue: The truncation strategy "keep system preamble + last N messages" has a correctness hazard: if truncation cuts between a tool_call message and its corresponding tool_result message, the resulting history is INVALID for all four providers. Anthropic requires that every tool_use block has a corresponding tool_result in the next user message. OpenAI requires that every tool_call has a corresponding role=tool message before the next user/assistant turn. Gemini requires the same pairing. Truncating mid-tool-loop produces a history that will be rejected by the provider SDK with an API error (not a graceful degradation).
The plan's truncate_to_budget() description does not address this. PM[3] mentions "truncation strategy" as mitigation for history bloat but does not flag the pairing invariant.
evidence: [independent-research: Anthropic messages API docs: "tool_result must follow the tool_use block in the same conversation" — API returns error 400 if violated; OpenAI chat API similarly requires paired tool calls/results] T1-verified. |source:[independent-research]|T1
→ revise: truncate_to_budget() MUST maintain tool_call/tool_result pairing invariant — never truncate mid-tool-loop. Implementation: truncation should delete turn-pairs atomically. A "turn" for truncation purposes = all messages between two consecutive assistant messages (including any interleaved tool results). This is non-trivial to implement correctly and adds complexity to SQ[8]. Revise SQ[8] estimate from 3h to 4h. |source:[independent-research]|T1

---

**BC[7]: token_count_estimate len//4 — tokenizer drift across providers**

plan-element: IC[3] token_count_estimate(provider_id) via len//4 proxy.
feasibility: H (acceptable for v1 with acknowledged risk)
issue: The plan acknowledges "calibrate against reported input_tokens in first 5 turns" (PM[3], ADR[5] context_budget=0.60). The 60% budget (down from 70%) accounts for this. However, len//4 as bytes-of-UTF8 // 4 is reasonably calibrated for English prose but diverges for:
- Code snippets (typically fewer tokens per character than prose)
- Non-ASCII content (multi-byte UTF-8 chars dramatically reduce chars-per-token)
- Tool_result strings from sigma_mem (memory content may be dense/structured)
The 60% budget + 5-turn calibration is a reasonable mitigation. The real gap is that calibration against "reported input_tokens" requires reading TurnEndEvent.input_tokens — this is per-turn data from each provider. Anthropic returns usage in the final stream event (message_delta with usage). OpenAI returns usage in the final chunk (include_usage=True required). Gemini returns usage_metadata on the response. OllamaProvider returns prompt_eval_count in the final chunk. Each provider returns token counts at different points in the stream — the plan's TurnEndEvent should carry these but the StreamEvent(kind="turn_end") needs to carry input_tokens + output_tokens from the provider-specific usage field.
evidence: [independent-research: Anthropic SDK + OpenAI SDK + Google GenAI SDK all return token counts in completion response, each in slightly different field names] T1-verified. |source:[independent-research]|T1
→ accept with gap flag: §2b outcome 2 — 60% budget + calibration is reasonable for v1. Flag: StreamEvent(kind="turn_end") must explicitly carry usage fields populated from per-provider response metadata. This is implicit in the plan but not in IC[3] or ADR[3]. DA should confirm this is in the IC. |source:[independent-research]|T1

---

**BC[8]: MCP stdio client — subprocess lifecycle and connection reuse (SQ[9])**

plan-element: ADR[8] sigma-mem via MCP stdio client, 5s timeout, SQ[9] 4h estimate.
feasibility: H (buildable, but lifecycle gap)
issue: The plan does not specify whether the MCP subprocess is started once per session or once per tool invocation. Both are plausible:
(a) Once per session: subprocess started on session start, kept alive for all tool calls, shut down on session.close(). This is more efficient but requires the MCP client to handle the subprocess crashing mid-session (zombie subprocess, orphaned stdio pipes). The `mcp` Python SDK supports stdio transport but the session lifecycle (MCPSession.start() / close()) must be managed. If not closed properly, the sigma-mem subprocess may persist after the Streamlit app reruns.
(b) Once per tool invocation: fresh subprocess for each tool call. Simpler lifecycle, but ~300ms startup overhead per call (sigma-mem is a Python server — process startup is not instant). At 5s timeout, startup eats ~6% of budget.
The plan's ADR[8] says "subprocess mode" but does not specify (a) vs (b).
evidence: [independent-research: mcp Python SDK docs + mcp/python-sdk GitHub — MCPClientSession has explicit start()/close() lifecycle; the MCPSession is not auto-closing] T1-verified. The mcp library's stdio transport creates a subprocess and holds it alive for the session duration by default. |source:[independent-research]|T1 [agent-inference: startup overhead estimate for Python MCP server]
→ clarify: SQ[9] must specify: once-per-session subprocess (recommended). Add explicit sigma-mem process supervision in ToolRegistry (or MemoryHelper): detect subprocess crash, restart once, surface error to tool_result if restart fails. The 5s timeout (ADR[8]) applies per tool_call, not per subprocess lifecycle. |source:[independent-research]|T1

---

**BC[9]: Streamlit async bridge — queue pattern and @st.fragment race condition**

plan-element: ADR[5] queue-based sync bridge, DS[1] @st.fragment(run_every=1.0).
feasibility: M (H6 confirmed conditional — viable with the right pattern)
issue-A (bridge implementation): The plan prefers a queue-based sync bridge (asyncio.Queue + background thread). The concrete pattern is: (1) Streamlit main thread starts a background thread running asyncio.run(TurnEngine.run_turn()), (2) that thread puts StreamEvents into a queue.Queue, (3) a sync generator pulls from queue.Queue with get(timeout=0.1), yields the item, (4) st.write_stream() calls the sync generator. This is buildable and is documented in Streamlit community patterns. BUT: the background thread's event loop must be fresh (asyncio.run() creates a new event loop per call) — compatible with Streamlit's threading model. However, asyncio.run() is blocking; it runs until run_turn() completes. If TurnEngine.run_turn() hangs (tool timeout, provider error), the background thread hangs indefinitely. The plan's 5s MCP timeout helps but provider SDK calls can hang without timeout if not configured.
issue-B (@st.fragment race): @st.fragment(run_every=1.0) can rerun while the background thread is still producing events. If the fragment reruns mid-stream and reads session_state["pending_chunks"], it may render a partial turn, then on next rerun render the full turn — producing visible double-render. PM[4] addresses Streamlit session state corruption for duplicate turn_ids but not this partial-render race. The product-designer VIABILITY[H11] P=0.65 captures this correctly (event-driven trigger racing with timer). The F6 prototype must explicitly test this. The SQ[F1] and SQ[F6] budget of 4-8h may underestimate if the race condition requires a dedicated sync mechanism (e.g., session_state flag + lock).
evidence: [independent-research: Streamlit community docs on queue-based async bridge — pattern documented in streamlit/streamlit#6481 thread + community guides] T2-corroborated. RuntimeError from asyncio in Streamlit confirmed in streamlit/streamlit#12076 (July 2025). |source:[independent-research]|T2
→ accept with conditions: The queue-based bridge is the right pattern. SQ[1] M0 viability experiment MUST include: (a) queue bridge with background thread, (b) fragment rerun during active stream, (c) measure if partial-turn double-render occurs. If (c) shows double-render → add completed_turn_flag gate before fragment reads pending_chunks. This adds 1-2h to SQ[13-14] if needed. |source:[independent-research]|T2

---

**BC[10]: Test strategy — mock vs. real infra (§4d BUILD test integrity)**

plan-element: SQ[12] M1 integration test (headless 2-model session, one tool call), SQ[16] M3 integration test (3-model autonomous).
feasibility: H (test plan is reasonable but has mock gaps)
issue-A (SQ[12] coverage gaps): The plan's headless 2-model integration test (Anthropic + Ollama cloud) covers the happy path. It does NOT inherently catch:
- Gemini function_response round-trip (GeminiProvider not in M1 integration test — Gemini is M1c/M1d scope)
- Ollama malformed tool_call silent drop — the test uses Ollama cloud (deepseek-v3.2:cloud, presumably reliable). The silent-drop risk is for local small models. SQ[12] as written does NOT catch silent drops.
- Token-estimate calibration drift — the test runs with real providers, so reported input_tokens can be checked, but the plan doesn't specify that SQ[12] asserts anything about token_count_estimate accuracy.
- Tool-exec loop max_iterations hit — SQ[12] says "one tool call." A session where max_iterations is hit requires a model that calls tools 3+ times in one turn. The integration test doesn't explicitly exercise this.
- Raw-event capture correctness — SQ[12] should verify that SessionWriter writes raw sidecar for unknown/nominal reliability models. This is not stated in the test description.
evidence: [agent-inference] — listing what the stated test description would and would not catch. |source:[agent-inference]|T3
issue-B (mock tests false confidence risk — project memory): The draft fixture/tests directory includes `tests/fixtures/mock_providers.py`. If unit tests use mock providers, the actual Anthropic/OpenAI/Gemini/Ollama streaming behavior (delta reconstruction, content-block assembly, function_response wrapping) will NOT be tested. Mock providers that yield pre-constructed StreamEvents do not exercise the SDK streaming code paths. Per project memory "Mock tests false confidence": "132 mock tests ≠ production readiness; empirical testing is non-negotiable." This is CRITICAL for SQ[3-6] (provider adapters) — mock-provider unit tests for adapter logic MUST be complemented by live fixture tests (CHATROOM_LIVE_TESTS=1 gate per draft).
evidence: [cross-agent: project memory "Mock tests false confidence" pattern] T2-corroborated (direct project history). |source:[cross-agent]|T2
issue-C (SQ[16] M3 integration test specificity): The plan says "3-model autonomous session, sigma_mem_recall invoked, ToolCallRecord populated, preamble_variant logged." This is a SUCCESS CRITERION, not a test assertion specification. What does the test ASSERT specifically? That ToolCallRecord.invoked==True? That JSONL has a line with event_type="tool_call"? That preamble_variant in JSONL header != ""? The test is underspecified as written — "ToolCallRecord populated" is ambiguous (populated with what? all fields? just invoked=True?).
→ revise: (1) SQ[12] should add explicit assertions: tool-exec loop exercised (model invokes tool, TurnEngine detects, executes, appends tool_result, re-invokes, model responds with content); JSONL has tool_result lines; StreamEvent(kind="turn_end") carries non-zero input_tokens. (2) SQ[16] must specify at minimum: ToolCallRecord.invoked=True for at least one call, ToolCallRecord.result non-empty, preamble_variant field present in JSONL header, session runs 3+ turns without exception. (3) provider adapter tests MUST include at least one live-API fixture test per SDK family before M1 is called complete — not just mock_providers.py. |source:[agent-inference]|T3 + [cross-agent]|T2

---

**BC[11]: CAL[M1] effort realism — 80% confidence band**

plan-element: CAL[M1-engine] revised to point=5d, 80%=[4d,8d], 90%=[3d,10d].
feasibility: M (estimate plausible but at optimistic end even after R2 revision)
issue: The R2 revision from 4d to 5d (point) is an improvement. However, examining the SQ[] sum:
SQ[2] types: 3h
SQ[3] AnthropicProvider: 4h (BC[1] adds 1h → 5h)
SQ[4] OpenAIProvider: 4h (delta reconstruction is documented, 4h plausible if using SDK streaming well)
SQ[5] GeminiProvider: 5h (BC[3] argues 6-8h)
SQ[6] OllamaProvider: 4h (BC[4] adds empirical uncertainty, 4-5h)
SQ[7] TurnEngine: 5h (BC[5] multi-tool-call gap, 5-6h if clarified)
SQ[8] ConversationHistory: 3h (BC[6] pairing invariant, 4h)
SQ[9] ToolRegistry+MCP: 4h (BC[8] lifecycle, 4h)
SQ[10] SessionWriter: 3h (reasonable)
SQ[11] ChatOrchestrator: 5h (reasonable)
SQ[12] integration test: 3h (plus live-API fixture tests per BC[10])
CLI (DIV[5] added): 2h

Revised SQ sum: ~47-52h ≈ 6-6.5d point estimate. This is 20-30% above the plan's revised 5d point estimate. The delta is primarily: Gemini adapter (+1-3h), truncation pairing invariant (+1h), type reassembly documentation (+1h), live fixture tests (+3-4h if not already in SQ estimates).

The 80% upper bound of 8d remains valid — it absorbs most surprises. The point estimate of 5d is at the optimistic end even after the R2 revision.

§2b outcome 3: no codebase precedent for multi-provider streaming. Reference class (industry norm for this type of build in Python async): 6-9 days based on community build reports and tech-architect's own §2b outcome 3 flag. Brad's "60-70% of project" directionally confirmed — at 6d M1 / 10d total, ratio = 60%.
evidence: [agent-inference: SQ[] sum + BC[1,3,6,8] gap estimates] |source:[agent-inference]|T3 + [prompt-claim (Brad 60-70%): plausible, corroborated per product-strategist R2]
→ revise: recommend CAL[M1-engine] point = 6d (not 5d), 80%=[4.5d,9d]. This puts M1 at 6/11 = 55% of total at point estimate — within Brad's 60-70% range at 80th percentile (9d/13d = 69%). Flag for plan-track concession or defend with evidence.

---

**BC[12]: Parallel cluster eligibility — SQ[7-11] cluster B shared state risk**

plan-element: Cluster B = SQ[7,8,9,10,11] (engine, independent files).
feasibility: H (clusters are mostly independent but one shared-import risk)
issue: Cluster A (SQ[3-6] providers) is genuinely file-independent — each provider is its own file, no shared imports beyond types.py (SQ[2] must complete first). Cluster B (SQ[7-11] engine) is also file-independent in the file sense, BUT: TurnEngine (SQ[7]) and ConversationHistory (SQ[8]) have a DESIGN-LEVEL coupling that could produce merge conflicts if built simultaneously by different engineers. TurnEngine.run_turn() calls conversation.to_provider_messages() and conversation.append() — if SQ[7] and SQ[8] are built in parallel, the interface between them must be agreed before parallel build starts. IC[3] specifies ConversationHistory's interface, which mitigates this, but if the engineer building SQ[7] discovers a missing method in IC[3] (e.g., "I need a method to peek at the last N messages without truncation"), they'll need to coordinate mid-build.

ChatOrchestrator (SQ[11]) depends on both TurnEngine (SQ[7]) and ConversationHistory (SQ[8]) — it CANNOT be built in parallel with them (despite being in cluster B). SQ[11] must be sequential AFTER SQ[7] and SQ[8].

Corrected cluster B sequencing: SQ[8,9,10] are independent and can build in parallel; SQ[7] can build in parallel with SQ[8,9,10]; SQ[11] MUST be sequential after SQ[7] and SQ[8].
evidence: [code-read: IC[3] ConversationHistory methods + IC[2] TurnEngine.run_turn() signature — TurnEngine explicitly calls conversation.to_provider_messages() and conversation.append()] |source:[cross-agent: plan IC[2]+IC[3]]|T2
→ revise: parallel-cluster declaration is correct at cluster level (B = engine ≠ A = providers) but within cluster B: SQ[11] ChatOrchestrator must be marked sequential-after-SQ[7,8]. The parallel cluster note should read: "B-parallel=[SQ[8],SQ[9],SQ[10]] + SQ[7] in parallel with B-parallel | SQ[11] sequential after SQ[7,8] complete."

---

**FEASIBILITY-VERDICT[implementation-engineer]: CONDITIONAL | conditions: (1) GeminiProvider estimate revised from 5h→6-8h; (2) TurnEngine multi-tool_call policy documented before SQ[7] build; (3) ConversationHistory truncation must maintain tool_call/tool_result pairing invariant; (4) SQ[11] cannot parallelize with SQ[7,8]; (5) M0 viability experiment must test Ollama streaming tool_call chunk shape; (6) SQ[12]+SQ[16] test assertions must be specified; (7) live-API fixture test required per SDK family before M1 complete | highest-risk-SQ: SQ[5] (GeminiProvider — novel asymmetric adapter, no codebase precedent, SDK instability) | recommended-revisions: CAL[M1] point estimate → 6d; IC[2] must document multi-tool_call policy and max_iterations exit semantics; IC[3] must document pairing invariant; SQ[6] success criterion must verify streaming tool_call chunk shape empirically | → accept-plan with listed revisions**

---

**Analytical Hygiene:**

§2a: BUILD challenge approach = evidence-based adversarial challenge of specific SQ[] items. Mainstream pattern for plan feasibility review. |outcome: 2 (confirmed)

§2b: Precedent check: prior build history shows no multi-provider streaming codebase precedent; sigma-verify is single-shot (not streaming); sigma-ui async patterns are different shape. Prior IE patterns: "convention-only async = design defect" (P[convention-only-async=design-defect|26.3.28]) relevant — any async event loop blocking in providers will silently stall all turns. BC[9] flags this via the background-thread pattern. |outcome: 3 (gap: no direct precedent in this codebase; estimate is inference from industry norm)

§2c: Cost/complexity: challenge findings add ~20-30% to M1 effort. Reversal cost of not addressing BC[6] (pairing invariant) is HIGH — API error 400 from providers in production with no graceful path. BC[5] (multi-tool_call policy) reversal cost = rewrite TurnEngine loop logic. |outcome: 2 (confirmed: flagged gaps have real reversal cost)

§2e: Premise viability: plan premises (IC[1-7] implementable in Python async, SDKs stable enough) are sound. Key assumption: Ollama native streaming tool_call chunk shape works as expected — empirically unverified. BC[4] flags this. |outcome: 3 (gap: Ollama native streaming tool_call behavior empirically unverified before SQ[6] build)

Source provenance: all findings tagged. No load-bearing finding rests solely on T3. BC[1,2,6,7,8] = T1 (SDK docs). BC[3] = T2 (community + migration guide). BC[4] = T2+agent-inference. BC[5,11,12] = agent-inference T3 (architectural judgment — flagged for DA challenge). BC[9] = T2. BC[10] = T3 + cross-agent (project memory).

**DB[top-conviction: BC[6] pairing invariant]:**
(1) initial: truncation cutting between tool_call and tool_result produces API error
(2) assume-wrong: what if providers are lenient about orphaned tool_calls in history?
(3) strongest-counter: some providers might accept orphaned tool_calls silently (treat as malformed and continue)
(4) re-estimate: Anthropic API is documented to return 400 error for orphaned tool_use blocks (T1 verified). OpenAI documentation similarly specifies tool messages must follow assistant messages with tool_calls. Gemini behavior on orphaned function_calls less documented. Risk remains real for Anthropic+OpenAI (majority providers).
(5) reconciled: pairing invariant is a hard requirement for Anthropic and OpenAI. Gemini may be more lenient. Flag: implementation must enforce pairing at truncation for all providers.

**DB[top-conviction: BC[11] effort estimate]:**
(1) initial: SQ[] sum suggests 6d point estimate, not 5d
(2) assume-wrong: what if engineers are fast and SQ estimates are conservative?
(3) strongest-counter: SQ estimates from tech-architect are already per-task optimistic end per §2b outcome 3; engineer speed variance could bring total below 5d
(4) re-estimate: even with 20% speed improvement, GeminiProvider alone at 5h±50% variance + pairing invariant work (+1h) + live fixture tests (3-4h) pushes toward 6d
(5) reconciled: 6d point estimate is more accurate. 5d is achievable only if GeminiProvider adapter is cleaner than expected and live fixture tests are fast to write.

### ui-ux-engineer

#### BOOT RECORD
recall:"chatroom UI feasibility challenge, H6 critical path, VIABILITY[H11] stress-test" |read:agent-def+build-directives+memory+scratch(all plan-track DS/IX/CT/R2)+DRAFT+BRAD-CRITIQUE |inbox:does-not-exist |round-2-materials:OPEN

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[1] transcript rendering — fragment legal use + O(n) rerun cost
|feasibility:M |T1+T3

§2a: fragment-isolated append-only list is correct architecture. Full-page-rerun Alt A is genuinely O(n). st.empty Alt B correctly rejected. |source:[independent-research(docs.streamlit.io):T1]

issue-1 (MEDIUM): @st.fragment cannot be nested INSIDE a single st.chat_message. Fragment wraps a Python function. TranscriptFragment wraps the loop containing all st.chat_message calls — legal. CT[] nesting diagram could be misread as illegal nesting inside one chat_message. Clarify in SQ[F1]. |source:[independent-research(docs.streamlit.io):T1] |outcome:2 (spec correct, diagram needs clarification)

issue-2 (HIGH — BLOCKER-A): @st.fragment(run_every=1.0) timer firing mid-stream is the critical unresolved race condition. Community reports 2025: Streamlit >=1.33 queues fragment reruns rather than interrupting active write_stream — NOT T1-documented. For long token streams (>1s), rerun fires immediately after stream completes, adding latency. For very fast reruns, queuing prevents duplication. But version-dependent risk remains. |source:[agent-inference+T2-corroborated-community-reports-2025] |outcome:3 — §2e gap: BLOCKER-A. Must test fragment-race in F6/M0 prototype as FIRST test priority (higher-risk unknown than async-bridge connectivity).

issue-3 (MEDIUM — BLOCKER-B): O(n) render cost estimates require grounding. sigma-ui 50ms/item = monitoring-grade panel items (different DOM). st.chat_message with avatar+text+potential st.status = more DOM. For COMPLETED turns (static strings in session_state): estimated 8-15ms/item. At 80×12ms=960ms — borderline against 1s interval. At 100 turns (soft cap) × 12ms = 1200ms — EXCEEDS interval. The 100-turn soft cap alone does NOT guarantee <1s render time. |source:[agent-inference:T3] |outcome:3 — §2b gap: BLOCKER-B. F6 render benchmark at 50/80/120 turns is MANDATORY gate, not nice-to-have.

DB[DS1-fragment-race]: (1)initial:medium-risk-queue-bridge-mitigates (2)assume-wrong:race causes duplicate renders (3)strongest-counter:JSONL is ground-truth regardless of UI glitch — research data uncorrupted (4)re-estimate:UI glitch is recoverable, data is not corrupted (5)reconciled:DS[1] architecture correct. Race is UX concern not data-integrity concern. CONDITIONAL on F6 testing race explicitly. |source:[cross-agent(tech-architect ADR[5])+agent-inference]

§2a:outcome:2 |§2c:reversal-cost:1d |§2e:gap-flagged-for-F6 |→ revise: F6 success criteria must include fragment-race test + render benchmark

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[2] speaker identity — avatar mechanism + palette WCAG accuracy
|feasibility:M |T1+agent-inference-applying-T1

issue-1 (HIGH): "Colored circle + 2-char initials" avatar NOT directly achievable via st.chat_message avatar param. Avatar param accepts: emoji string, URL string (including data: URI), None. NOT CSS/SVG/HTML strings or arbitrary rendered content. To achieve colored circle with initials: pre-generate base64-encoded SVG per model (~150 chars) as data: URI string. Implementable but requires SVG-generator utility not in current spec. Add to SQ[F5]: SpeakerColorMap.to_avatar_uri(spec: ProviderSpec) -> str. |source:[independent-research(docs.streamlit.io avatar param):T1] |outcome:1 — revised finding: add SVG-generator utility to SQ[F5]

issue-2 (HIGH — REVISED FINDING): DS[2] claims "S=75%, L=45% — WCAG AA 4.5:1 math-verified." This claim is INCORRECT for warm hues. Applying WCAG 2.1 relative luminance formula:
  Hue 55° (yellow) S=75% L=45%: approx RGB (185,164,29), relative luminance ~0.38, contrast on white = 1.05/0.43 = 2.4:1 — FAILS 4.5:1, FAILS 3:1.
  Hue 83° (yellow-green) S=75% L=45%: luminance ~0.31, contrast ~2.0:1 — FAILS severely.
  Hue 220° (blue) S=75% L=45%: luminance ~0.09, contrast ~7.5:1 — PASSES.
Warm hues 28°-110° (approx 3 of 13 steps) will fail WCAG if used as avatar background with white initials OR as badge/label text color on white page background.

DB[DS2-contrast]: (1)initial:uniform-S=75%-L=45%-claimed-WCAG-AA (2)assume-wrong:avatar circle is decorative, SC 1.4.3 applies only to text elements (3)strongest-counter:initials ARE text rendered on the colored background — 4.5:1 applies (4)re-estimate:depends on whether initials float on white (no failure) or sit on colored circle (failure for warm hues). DS[2] is ambiguous on initials color relative to background. (5)reconciled:REVISED FINDING: warm hues at L=45% produce WCAG failures for text-on-colored-background. Design must specify EITHER (a) per-hue L adjustment for warm hues (L→58-65%) OR (b) per-hue text-color logic (dark initials on warm backgrounds, white on cool). Either implementable. |source:[agent-inference applying WCAG relative-luminance formula:T1]

§2a:outcome:1 (revised — palette claim incorrect for warm hues; design revision required before SQ[D1]) |→ DA: DS[2] WCAG claim is T3-validated-as-INCORRECT by agent-inference applying T1 formula. Palette revision required.

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[3] preamble variant picker
|feasibility:H |T1

All elements (st.selectbox, persistent st.badge, session_state write on Start callback, st.text_area custom) standard documented patterns. JSONL write on start-click: correct (Start button callback → session_state["session_metadata"]. Custom preamble st.text_area: no gotchas at typical preamble length. H9 observability signals implementable. |source:[independent-research(docs.streamlit.io):T1] |outcome:2 — BUILDABLE as specified. |→ accept DS[3]

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[4] tool-call badges — mechanism revision + BLOCKER-C
|feasibility:M→H (with mechanism revision) |T1

issue-1 (LOW): st.expander inside st.chat_message is LEGAL — explicitly supported in Streamlit docs examples. |source:[independent-research(docs.streamlit.io):T1] |outcome:2 — confirmed legal

issue-2 (HIGH — REVISED FINDING): Correct Streamlit API for DS[4] 3-state badge is st.status(), NOT st.expander. st.status(label, state="running"|"complete"|"error", expanded=bool) introduced in Streamlit >=1.28 specifically for agent-step visualization. State transitions: running=amber-spinner, complete=green-checkmark, error=red-x. T1-documented pattern, NOT T3-novel. Designer asked "st.status? st.empty?" — the answer is st.status(). st.status is legal inside st.chat_message. |source:[independent-research(docs.streamlit.io/st.status):T1]

DB[DS4-mechanism]: (1)initial:st.expander-with-conditional-CSS (2)assume-wrong:expander header not dynamically styleable, state transitions require full re-render (3)strongest-counter:st.status is purpose-built for this exact pattern (4)re-estimate:st.status resolves the mechanism question; still needs queue-bridge validation (5)reconciled:st.status is correct mechanism. Context-manager integration with queue-bridge = BLOCKER-C — must validate in expanded M0. |source:[independent-research(docs.streamlit.io):T1]

§2a:outcome:1 (mechanism revised to st.status — T1 documented, removes T3-novel risk. DA challenge on DS[4] T3-novel should be withdrawn upon mechanism adoption.) |§2c:0 added complexity |→ revise DS[4]: replace st.expander proposal with st.status. F6 validates BLOCKER-C (st.status context manager in queue-bridge context).

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[5] metrics panel — event-driven trigger race
|feasibility:M |T3+T1

issue-1 (MEDIUM): @st.fragment(run_every=2.0) CPU cost: SessionMetrics read from session_state O(1); 3 st.dataframe renders fast (no API). Estimated 50-100ms per rerun. At 2s interval = 2.5-5% CPU. Acceptable. |source:[agent-inference:T3] |outcome:3 — §2b gap: F6 should benchmark metrics fragment alongside active streaming

issue-2 (MEDIUM): turn_complete_flag race: write all metrics data to session_state BEFORE setting turn_complete_flag (ordering guarantee). Timer reads flag=True on next cycle; maximum staleness = 2s. Race-safe with correct ordering. Ordering constraint is implementation requirement, not design revision. |source:[agent-inference:T3+docs.streamlit.io session_state:T1] |outcome:2 — confirmed with ordering constraint

§2a:outcome:2 (three-tab dataframe standard) |→ F6 includes metrics fragment alongside streaming benchmark

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[6] sidebar controls
|feasibility:H (minor workaround) |T1

issue-1 (LOW): Per-option tooltip on disabled multiselect options not natively supported. st.multiselect option_disabled mutes the option but does NOT support per-option tooltips. Workaround: st.caption below multiselect showing missing API keys ("Keys not found: ANTHROPIC_API_KEY") — achieves information goal. Simpler than custom CSS injection. tool_use_reliability colored dot: emoji (🟢🟡🔴) appended to display_name — simplest, no CSS needed. All other sidebar patterns standard. |source:[independent-research(docs.streamlit.io):T1] |outcome:1 — revised: caption approach replaces per-option-tooltip spec. Amend SQ[D6].

---

#### BUILD-CHALLENGE[ui-ux-engineer→product-designer]: DS[7] session management
|feasibility:H |T1

st.dataframe with on_select="rerun" (Streamlit >=1.35): sets session_state["df_selection"] on row click — correct 2026 pattern. Actions via st.button checking selection state. JSONL read at 1000 lines (<200KB) = <50ms. No performance concern at v1 scale. |source:[independent-research(docs.streamlit.io):T1] |outcome:2 — BUILDABLE as specified. |→ accept DS[7]

---

#### BUILD-CHALLENGE[ui-ux-engineer→tech-architect]: H6 VERDICT — PRIMARY CHALLENGE
|feasibility:CONDITIONAL |T1+T2+T3

H6-CORE CLAIM ANALYSIS:

Claim-1: st.write_stream accepts AsyncIterator. CONFIRMED T1 (Streamlit >=1.31). Caveat: cached-object dependency can raise errors. Queue-based sync bridge remains safer. ADR[5] preference for queue bridge is CORRECT regardless of async-gen support. |source:[independent-research(docs.streamlit.io/st.write_stream):T1]

Claim-2: Mixed-type generator enables inline tool badges. PARTIALLY CORRECT but not in the way implied. st.write_stream CAN yield non-strings ("other data types use st.write"), but st.write renders DATA (DataFrames, primitives) — NOT layout containers. st.status and st.expander are context managers, NOT writable values — they CANNOT be yielded from write_stream. ToolCallBadge MUST be rendered POST-STREAM. Designer's DS[4] spec already says "post-stream-expander" — this is correct. THREE CONDITIONS point-3 wording ("mixed-type generator for inline tool badges") overstates what the mixed-type generator enables: it enables inline data renders, not inline layout containers. No architecture revision needed — DS[4] post-stream placement is already correct. Flag: clarify THREE CONDITIONS point-3 wording. |source:[independent-research(docs.streamlit.io/st.write):T1] |outcome:1 — revised: wording clarification needed; post-stream confirmed correct

Claim-3: Fragment rerun during active streaming — rerun interference. T2-corroborated (community 2025): Streamlit >=1.33 queues reruns, does not cancel active write_stream. NOT T1-documented. Version-dependent risk. BLOCKER-A. |source:[T2-corroborated-community-2025] |outcome:3 — gap, must test in F6/M0

Claim-4: Rerun cost at 130 turns cumulative. At 100 turns (soft cap) × 12ms/turn (estimated) = 1200ms — EXCEEDS 1s fragment interval. 100-turn cap alone insufficient if per-turn render is 12ms+. Measurement is mandatory. BLOCKER-B. |source:[agent-inference:T3] |outcome:3 — gap, render benchmark mandatory

Claim-5: M0 prototype scope sufficient. Current M0 (async bridge + tool_call visible) tests BLOCKER-A partially. BLOCKER-B and BLOCKER-C (st.status in bridge context) not covered. |source:[agent-inference+cross-agent(product-designer DIV[5])] |outcome:1 — revised: M0 success criteria must be formally expanded

§2f HYPOTHESIS MATRIX — Streamlit vs Alternatives:
E[1]=async+streaming+tool-badge | E[2]=rerun-cost@80+ | E[3]=researcher-skill | E[4]=setup-friction | E[5]=observability-UX-richness
H-main(Streamlit): E[1]:M(conditional) E[2]:L(borderline) E[3]:H(sigma-ui) E[4]:H(pip+run) E[5]:M(fragment+tabs+status)
H-alt-1(Textual): E[1]:H(asyncio-native) E[2]:H(delta-renders) E[3]:M(new-paradigm) E[4]:H(pip+run) E[5]:L(terminal)
H-alt-2(Gradio): E[1]:M(similar-async) E[2]:M(similar-rerun) E[3]:H(similar-Python) E[4]:H E[5]:M
H-alt-3(FastAPI+JS): E[1]:H(WebSocket) E[2]:H(no-rerun) E[3]:L(JS-required) E[4]:L(npm+build) E[5]:H
Verdict: Streamlit wins on E[3]+E[4]+E[5] for single-researcher local Python tool. Textual is correct fallback — better async, acceptable UX for research instrument. Gradio dominated by Streamlit. FastAPI+JS overkill. Streamlit correct IF M0 passes all 4 criteria. |source:[agent-inference:T3+cross-agent(product-designer:T2)] |outcome:2 — confirmed with prototype gate

---

#### FEASIBILITY-VERDICT[ui-ux-engineer]

VERDICT: CONDITIONAL |H6-verdict:conditional(3 blockers unresolved, all resolvable by expanded M0) |H11-P-convergence:WITH-DESIGNER-P=0.65(¬architect-P=0.87) |conditions:see-below |highest-risk-DS:DS[1](fragment-race+O(n)-rerun-borderline) |→ prototype-first

WHY P=0.65 NOT P=0.87 — EVIDENCE-BASED:

Architect P=0.87 answers: "can async bridge + tool event reach Streamlit container?" — narrow plumbing. T1 docs strongly support. Reasonable at P=0.87 for that question.

My P=0.65 answers: "does the COMPLETE UI — fragment transcript + metrics + tool-badge state transitions + rerun timing — work as a research instrument at 80+ turns across a 2h session?" — full system integration.

Gap = THREE specific unresolved unknowns:
BLOCKER-A: Fragment rerun during active write_stream — queuing behavior T2-corroborated NOT T1-confirmed. Version-dependent risk.
BLOCKER-B: Render cost at 80 turns — T3 estimates borderline. At 100 turns (soft cap) × 12ms = 1200ms — OVER 1s interval. Measurement mandatory not advisory.
BLOCKER-C: st.status context manager in queue-bridge context — revised mechanism is T1-documented but queue-bridge integration requires explicit validation.

P=0.65 = probability BEFORE expanded prototype runs. IF all 4 M0 criteria pass → P converges to 0.85+. IF BLOCKER-A fails → Textual TUI. IF BLOCKER-B fails → windowed render required v1 (not M4). IF BLOCKER-C fails → degrade to static expander + separate polling (acceptable degradation, research data unaffected). DA should treat P divergence (0.65 vs 0.87) as load-bearing, not rounding difference.

CONDITIONS FOR BUILDER-FEASIBILITY = HIGH (post-M0):
1. Expanded M0 passes all 4 criteria (M0-A through M0-D)
2. DS[2] palette revised: per-hue L adjustment for warm hues (28°-110°) OR per-hue text-color logic
3. DS[4] mechanism revised to st.status (reduces T3-novel risk to T1-documented)
4. DS[6] per-option tooltip revised to st.caption approach (minor)

builder-feasibility-score: 0.65 pre-M0 → expected 0.85+ post-M0-pass

---

#### REVISED M0 PROTOTYPE SUCCESS CRITERIA

Current M0: async bridge + tool_call visible in UI. INSUFFICIENT for full H6 validation.

EXPANDED M0 — all 4 must pass before M1 build:
M0-A: async bridge [existing] — queue-based sync gen feeds st.write_stream, tool_call event renders distinct from token
M0-B: fragment-race [NEW] — start active write_stream; trigger fragment rerun (manual or wait run_every timer); verify ZERO token duplication and ZERO display corruption
M0-C: render@80-turns [NEW] — render 80 static completed st.chat_message elements in TranscriptFragment; measure rerun time; PASS=<1000ms; FAIL=windowed-render required in v1 (not M4)
M0-D: st.status-in-bridge [NEW] — render st.status inside st.chat_message in queue-bridge context; transition state running→complete; verify visual transition; confirm mechanism with tool_result from queue

Budget: expand M0 from 2h to 2-4h. SQ[F6] already budgets 2-4h — consistent. Failed M0-B at 2h is better than DS[1] failure discovered at M2 after full build.

---

#### ANALYTICAL HYGIENE CHECKLIST

§2a: Streamlit vs alternatives → outcome:2 (confirmed-with-prototype-gate) |st.status over st.expander → outcome:1 (revised-reduces-T3-novel) |avatar-SVG-utility → outcome:1 (revised-required)
§2b: no precedent for 13-speaker streaming in codebase; render cost = agent-inference T3; F6 is calibration instrument → outcome:3 (gap flagged, mandatory prototype)
§2c: DS[1] reversal=1d-windowed-render if F6 fails; DS[4] mechanism change=0 added complexity; DS[2] palette revision=design-only → outcome:2
§2e: three premises unconfirmed (fragment-race, render-cost, st.status-bridge); expanded M0 resolves all three → outcome:3 (gap flagged, prototype path defined)
§2d source tags: avatar-mechanism=[independent-research:T1] |palette-contrast=[agent-inference applying WCAG:T1] |fragment-race=[agent-inference+T2-community] |st.status=[independent-research:T1] |render-benchmark=[agent-inference:T3]

XVERIFY: Top load-bearing finding = palette warm-hue WCAG failure (DS[2]). Rests on T1 formula (WCAG relative luminance) applied by agent-inference to specific HSL values. ΣVerify advisory in C1. Finding is mechanical calculation — any model confirms. XVERIFY-SKIP per §2h advisory; T1 formula application is defensible. Finding stands.

---

#### CONVERGENCE

ui-ux-engineer: ✓ feasibility-r1 |VERDICT:CONDITIONAL |H6:conditional(BLOCKER-A:fragment-race-T2-not-T1+BLOCKER-B:render@80-borderline+BLOCKER-C:st.status-bridge-context) |H11-P:with-designer-P=0.65(¬architect-P=0.87,different-question-scopes) |key-finding:st.status replaces st.expander for DS[4]-T1-documented-not-T3-novel |DS-revised:DS[2](palette-warm-hue-WCAG-fail+avatar-SVG-utility),DS[4](mechanism→st.status),DS[6](tooltip→caption) |UNCHANGED:DS[3](H),DS[7](H) |CONDITIONAL:DS[1](M-fragment-race+O(n)),DS[5](M-ordering-constraint) |M0-expanded:4-criteria(A:bridge+B:fragment-race+C:render@80+D:st.status-bridge) |builder-feasibility:0.65-pre-M0→expected-0.85-post-M0 |challenges:#9 |revised:#4 |→ ready-for-DA-challenge-response+design-track-response

### code-quality-analyst

#### TEST STRATEGY CHALLENGE — BUILD-TRACK FEASIBILITY (26.4.16)

---

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: SQ[12] behavioral sufficiency |feasibility: M |issue: SQ[12] description "headless 2-model session, one tool call, JSONL output verified" does not specify WHAT IS ASSERTED — only WHAT IS RUN. §4d requires behavior-vs-runs distinction. Absent: (a) assertion tool_result is threaded back into conversation (not just TurnEngine returned); (b) ToolCallRecord.preceding_text + position_in_turn non-empty; (c) JSONL ordering: tool_call line precedes tool_result line; (d) FAILURE cases: tool error, tool timeout, malformed JSON, max_iterations=3 hit. A test that checks JSONL exists and has N lines passes even if TurnEngine short-circuits after tool_call without executing the exec loop. |evidence: §4d [build-directives.md]; sigma-ui B1 write-order bug (CQA-5/DA[#4]/IE-4 triple-convergence) — ran without crash, wrong ordering silently [agent-memory]; hardcoded-return-values risk: mock can return pre-baked ToolCallRecord without TurnEngine loop running |source:[agent-inference+cross-agent] |T2 |→ revise SQ[12]: enumerate minimum assertion set

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: SQ[12] failure-case coverage |feasibility: L |issue: SQ[12] tests HAPPY PATH only. No specification for: (a) tool execution raises exception; (b) tool timeout (5s per ADR[8]); (c) model emits malformed tool_call JSON SDK swallows; (d) max_iterations=3 hit + TurnEndEvent emitted with stop_reason="max_tool_calls". H8 (pinned) is specifically about the "SDK swallowed malformed JSON" scenario — this is EXACTLY what test infrastructure must be able to reproduce. Without a mock provider that emits a malformed tool_call fragment, H8 is untestable in CI. |evidence: H8 in scratch; PM[2] small-model deadlock; ADR[7] raw-event capture |source:[prompt-claim+agent-inference] |T2 |→ require: mock provider with configurable failure modes (malformed JSON emit, empty tool_call, timeout) in SQ[12] scope

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: tests/test_adapters.py fixture completeness |feasibility: M |issue: ADR[4] specifies "fixture history with mixed text + tool_call + tool_result turns" but MISSING required cases: (a) Anthropic: assistant message with BOTH text AND tool_use in same content block; (b) OpenAI: tool_calls arriving as delta chunks requiring concatenation (streaming reconstruction, not completed dict); (c) Gemini: function_response in "user" role — round-trip to CanonicalMessage produces what role/structure?; (d) Multi-turn: [user → assistant(tool_call) → user(tool_result)] across ALL four SDK families. Hand-rolled idealized fixtures skip streaming delta reconstruction — the hardest failure mode (missed delta, trailing chunk lost) is untested. |evidence: H7 "message-mapping hardest adapter work" [scratch]; ADR[4] DB[ADR-4] Gemini round-trip; Brad critique "harder work isn't schema, it's message mapping" [brad-critique.md] |source:[independent-research+agent-inference] |T1 (Anthropic/OpenAI streaming docs) |→ require: enumerated fixture matrix with realistic SDK response shapes; streaming reconstruction fixtures separate from round-trip mapping tests

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: Gemini canonical form for function_response — round-trip lossiness unspecified |feasibility: H |issue: CanonicalMessage (OpenAI-shaped: role, content:str, tool_calls:list[dict]) has no role=tool concept. When GeminiAdapter translates CanonicalMessage with ToolResult back to Gemini: function_response becomes a user-turn Part. The REVERSE (Gemini response → CanonicalMessage) must reconstruct what? If round-trip is INTENTIONALLY lossy, the test must assert the specific fields preserved vs. dropped. If test checks only string content equality on a lossy round-trip, it passes even when metadata is silently discarded. Plan says "adapter owns complexity" but does not specify canonical form for Gemini tool results in transit. |evidence: ADR[4] DB[ADR-4] "Gemini function_response in user content, no role=tool; faithfulness of round-trip testable with fixture" [scratch] — fixture canonical form not specified |source:[agent-inference] |T2 |→ require: explicit statement of canonical form for Gemini function_response before fixtures can be written

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: Q1 research instrument validity — ToolCallRecord 3-state coverage |feasibility: H |issue: Q1 requires ToolCallRecord (invoked, malformed_json, result_used, query_text) CORRECTLY POPULATED across THREE distinct cases: normal tool call, SDK swallows malformed JSON, model declines tool. Plan has NO test verifying all three. SQ[12] covers one case (presumably normal). SQ[16] unspecified. ToolCallRecord.malformed_json=True is only set if TurnEngine DETECTS that SDK swallowed a malformed tool_call — from what signal? ADR[7] raw-event capture provides the data, but TurnEngine's detection logic reading the raw event is untested. A test could pass with malformed_json always=False while the detection path is broken. Research instrument validity depends on this field being accurate. |evidence: Q1 coverage matrix in strategist section [scratch]; H8 [scratch]; PM[2] |source:[prompt-claim+agent-inference] |T2 |→ require: test for all three Q1 ToolCallRecord states before M3 integration test passes

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: Q2 yield-next detection — no unit test specified |feasibility: H |issue: YieldNextPolicy parses trailing "@next:<name>" — no unit test specified anywhere in SQ[2-17] or test file list. This is the simplest unit test in the plan (pure function: string → speaker_name|None) and tests the core Q2 measurement mechanism. Without it: (a) off-by-one in parsing "@next:claude-opus" vs "@next: claude-opus" (with space) silently produces zero yield-next events — Q2 measurement broken; (b) wrong case "@Next:claude-opus" silently fails. Policy existence is specified; parser unit test is not. |evidence: Q2 pinned research question [scratch strategist]; YieldNextPolicy in IC[7]/ADR[5] |source:[agent-inference] |T1 (pure function, trivially testable) |→ require: unit test for YieldNextPolicy parser covering normal, space-variant, wrong-case, no-@next, self-nomination

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: SQ[16] M3 integration test — assertion scope underspecified |feasibility: M |issue: SQ[16] "3-model autonomous session test" missing: (a) preamble_variant logged in JSONL header (not just ConversationState); (b) @next: token detection queryable from metrics panel (Q2 observable); (c) 10-turn stability — v1 ship gate requires "10-turn unattended stability" but SQ[16] doesn't specify this; (d) sigma-mem MCP subprocess isolation strategy — if test requires live sigma-mem subprocess, CI fails on machines without sigma-mem running; CHATROOM_LIVE_TESTS=1 gate addresses live API, not MCP subprocess. |evidence: v1 Ship Gate criteria in strategist section [scratch]; draft test_live_smoke.py pattern [draft plan]; CHATROOM_LIVE_TESTS=1 gate [draft] |source:[cross-agent+agent-inference] |T2 |→ revise SQ[16]: enumerate preamble_variant assertion, 10-turn stability clause, sigma-mem subprocess mock vs. live isolation

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: M0 viability PASS criteria — 1-criterion vs. 3-criterion divergence unresolved |feasibility: M |issue: Tech-architect M0 pass criterion: "tool_call event visible in Streamlit distinct from token." Product-designer F6 expands to THREE: (a) async bridge works, (b) render cost at 80 turns <300ms, (c) event-driven trigger does not race with timer. Product-designer P=0.65 maintained because (b) and (c) are NOT tested by (a) alone. Divergence is unresolved in locked ADRs. If M0 declared PASS on (a) only, transcript architecture commits before (b)/(c) validated — discovered at M3 after significant build. Plan must declare WHICH criteria M0 must pass before M1 proceeds. |evidence: product-designer DS[1] DB[DS1] "Python loop over 80 st.chat_message items at 50ms each = 4s > 1s rerun interval" [scratch]; P=0.65 vs P=0.87 explanation [scratch] |source:[cross-agent] |T2 |→ require: enumerated M0 PASS criteria (all three); fail criteria stated explicitly so kill-switch is unambiguous

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: mock boundary — Provider mock shape MUST emit streaming events |feasibility: M |issue: Project memory flags "132 mock tests ≠ production readiness" (26.4.5). Specific risk: Provider mock can return a pre-baked CompleteResult. TurnEngine test verifies TurnEngine correctly reads mock output — but loop logic is never exercised because mock returned completed result. IC[1] Provider.stream() returns AsyncIterator[ChatEvent], NOT CompleteResult. A correct mock emits streaming events (token→tool_call→done) requiring TurnEngine to consume the iterator and detect the tool_call mid-stream. If implementation engineer uses a mock that returns CompleteResult (simpler to write), TurnEngine's exec loop is bypassed in every test. |evidence: §4d "real infra vs mocks" [build-directives.md]; "mock false confidence" [project-memory 26.4.5]; ollama-mcp-bridge BUG[1]: 814 tests passed, ScanResult.blocked_profile never set [agent-memory] |source:[independent-research+cross-agent] |T1 |→ require: SQ[12] mock spec: Provider mock MUST emit AsyncIterator[ChatEvent] not CompleteResult; TurnEngine loop must be exercised, not bypassed

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: IC[3] ConversationHistory.to_provider_messages() untested by test_adapters.py |feasibility: H |issue: IC[3] to_provider_messages(provider_id) → list[dict] is called on EVERY provider invocation. test_adapters.py tests the ADAPTER CLASSES (CanonicalMessage↔provider-shape). But to_provider_messages() is a SEPARATE code path: it calls adapters with a FULL HISTORY including system preamble injection, truncation, and cross-provider format selection. Not covered by adapter round-trip tests. Missing: (a) multi-turn history with tool_call+tool_result for each provider; (b) truncation applied: token_count_estimate triggers truncate_to_budget → to_provider_messages returns shortened list; (c) provider_id="gemini" returns user-role function_response Parts vs. provider_id="openai" returns role=tool messages. |evidence: IC[3] spec [scratch interface-contracts section]; ADR[4] "adapters own complexity, history.py calls them" |source:[agent-inference] |T2 |→ require: unit tests for ConversationHistory.to_provider_messages() with multi-turn history + truncation trigger + per-provider format verification

BUILD-CHALLENGE[code-quality-analyst→plan-track/tech-architect]: run_autonomous() dead-code risk at v1 |feasibility: H |issue: IC[7] ChatOrchestrator has run_round() and run_autonomous(max_rounds). §4c gold-plating: does v1 design require run_autonomous() as a METHOD vs. run_round() in a loop? SQ[16] does not specify which is called. If Streamlit UI calls run_round() in a loop and run_autonomous() wraps it, run_autonomous() is an untested code path at v1 ship. Similarly: RandomPolicy — plan specifies "all three policies in M1b" but v1 Streamlit UI may only expose Autonomous (RoundRobin/YieldNext). RandomPolicy may be created but unreachable from UI. §4c check: does DESIGN DOCUMENT require these? Product-designer DS[6] "mode toggle (Autonomous ↔ Human-Moderated)" — no Random mode in UI. |evidence: §4c gold-plating detection [build-directives.md]; IC[7] [scratch]; SQ[16] scope [scratch]; DS[6] sidebar-controls [scratch] — §2c outcome: 2 (run_autonomous() IS required for 10-turn stability gate, justified; but must be explicitly called in SQ[16]) |source:[agent-inference] |T2 |→ require: SQ[16] explicitly calls run_autonomous(), not run_round()-in-loop; RandomPolicy either appears in v1 UI or noted as "test-only, not exposed"

---

#### FEASIBILITY VERDICT

FEASIBILITY-VERDICT[code-quality-analyst]: CONDITIONAL |test-coverage: gap-{Q1-ToolCallRecord-3-states, Q2-yield-next-unit-test, SQ12-behavior-vs-runs, SQ12-failure-cases, M0-pass-criteria-unresolved, streaming-reconstruction-OpenAI+Ollama, to_provider_messages-unit-test, SQ16-assertion-scope} |mock-risk: HIGH |mocks-that-could-mask-failure: {(1) cooperative Provider mock returns CompleteResult → TurnEngine exec-loop never runs; (2) hand-rolled Gemini fixture skips streaming delta reconstruction; (3) sigma-mem subprocess mocked too aggressively → MCP client integration untested; (4) ToolCallRecord.malformed_json always=False (detection logic never exercised)} |untestable-ICs: {IC[3].to_provider_messages() not covered by test_adapters.py; IC[2].run_turn() failure modes unspecified} |→ refine SQ[12]+SQ[16] with enumerated assertions+failure-cases; specify mock boundary before plan lock

---

#### ANALYTICAL HYGIENE

§2a: Purpose-built per-SDK test fixtures is standard for multi-SDK adapters (LangChain, LiteLLM use this pattern). ALT: pytest-recording/vcrpy for cassette-style SDK response capture (would address streaming reconstruction gap without hand-rolling). Migration cost if mock strategy wrong: rebuild ~50% of unit tests. Flag: streaming reconstruction tests likely require cassette-style mocks for OpenAI delta chains and Ollama native API chunks — hand-rolling these is error-prone. §2a outcome: 2 — confirmed with flagged risk on streaming reconstruction mock realism. |source:[independent-research] |T2

§2b: No precedent in this codebase for multi-SDK streaming adapter test suite. sigma-verify: single-shot, no streaming. sigma-ui: async dispatch, not SDK-boundary. SQ[12] 3h + SQ[16] 3h estimates assume clear assertion specs which don't exist — actual effort with failure-case coverage and correct mock boundaries likely 5-7h per test. §2b outcome: 3 — gap: no streaming integration test precedent; effort estimates at optimistic end given spec gaps; DA should scrutinize. |source:[cross-agent+agent-inference] |T2

§2c: test_adapters.py fixture strategy lightweight (~50 LOC per provider). Wrong-mock cost: bugs discovered in M2/M3 manual testing, reversal ~1 day to add streaming reconstruction tests. Specify fixture requirements now in plan phase (zero build cost). §2c outcome: 2 — confirmed, streaming reconstruction gap targeted to OpenAI+Ollama only. |source:[agent-inference] |T2

§2e: Test strategy premise viability: assumes Provider mocks simulate real SDK streaming behavior (emit chunk-by-chunk events). Viability experiment (SQ[1]) surfaces Streamlit async issues, NOT adapter-layer streaming reconstruction (different concern). §2e outcome: 2 — confirmed; mock realism is load-bearing for test validity; must be specified in plan. |source:[agent-inference] |T2

DB[mock-risk]: (1)initial: cooperative CompleteResult mock bypasses TurnEngine loop (2)assume-wrong: mock that returns CompleteResult tests TurnEngine's response to result (3)strongest-counter: IC[1] Protocol defines Provider.stream()→AsyncIterator[ChatEvent] NOT complete()→CompleteResult; a mock that returns CompleteResult doesn't implement the Protocol — the mock IS the wrong interface; correctly typed mock MUST emit streaming events (4)re-estimate: risk is real but achievable fix — mock emits AsyncIterator[ChatEvent] with [token, tool_call, done] sequence; this exercises the loop correctly (5)reconciled: mock-risk HIGH because not specified in plan; LOW once mock spec is added. Requirement is explicit not complex. |source:[agent-inference+independent-research] |T1

DB[streaming-reconstruction]: (1)initial: hand-rolled fixtures skip delta chunk reconstruction for all SDKs (2)assume-wrong: SDK accumulates chunks internally so adapter tests correctly-formed output (3)strongest-counter: Anthropic MessageStream accumulates internally — adapter reads accumulated content blocks (fine). OpenAI: manual concatenation of delta.tool_calls required in adapter code — NOT SDK-handled. Ollama native: streaming chunk format may differ from completed response — depends on `ollama` Python library implementation. (4)re-estimate: gap is PROVIDER-SPECIFIC: OpenAI tool_calls delta reconstruction + Ollama native chunk handling are the two that require chunk-by-chunk fixtures. Anthropic and Gemini SDK-accumulate, so their adapter tests correctly test completed output. (5)reconciled: targeted gap; scoped to OpenAI+Ollama streaming reconstruction tests only. Not full fixture strategy rewrite. |source:[independent-research] |T1 (OpenAI streaming tool_calls delta documented behavior)

#11 challenges |test-coverage-gaps: #8 |mock-risk: HIGH→CONDITIONAL-on-mock-spec |core-actionable: add SQ[12] assertion-set + failure-cases, add Q2 unit test, resolve M0 criteria, specify Provider mock emits streaming events ¬CompleteResult |→ ready for plan-track response

## round-2-comparison (introduced after plan-track Round 1 converges)

### tech-architect vs. draft

DIV[1]: Ollama endpoint
draft-says: Ollama uses OpenAI-compat subclass (`ollama_client.py` extends openai_client) via `/v1/chat/completions` |
your-plan-says: Ollama MUST use native `/api/chat` endpoint via `ollama` Python library ¬OpenAI compat |
verdict: DEFEND — with new evidence not available to draft |
evidence: Production-confirmed via openclaw/openclaw#11828 (maintainer confirms), ollama/ollama#12557 (open, no fix): OpenAI compat layer silently drops tool_calls when stream=True — finish_reason=stop, empty content, no error. Draft was written before this was confirmed. My independent research found it via T1-verified GitHub issues. This is not a stylistic preference — using OpenAI compat for Ollama tool-use in streaming mode produces invisible data loss. The draft's "Ollama OpenAI-compat subclass" pattern is wrong for the tool-use case. ADR[6] stands. |
ADR-impact: ADR[6] — Ollama native /api/chat required. OllamaProvider cannot subclass OpenAIProvider for tool-use turns.

DIV[2]: ChatEvent / StreamEvent shape — flat dataclass vs discriminated union
draft-says: `StreamEvent` is a flat dataclass with `kind: Literal["token","tool_call","stop","error"]` + optional fields (text, tool, stop_reason, error) |
your-plan-says: discriminated union — `TokenEvent | ToolCallEvent | ToolResultEvent | TurnStartEvent | TurnEndEvent | ErrorEvent` — separate typed dataclasses |
verdict: COMPROMISE — draft's flat dataclass is simpler and covers the streaming surface. My union adds `TurnStartEvent` and `TurnEndEvent` which the draft doesn't have (draft uses `CompleteResult` returned at end of stream). The additional event types are load-bearing for the metrics panel (TTFT tracking requires TurnStartEvent timestamp; input/output token counts require TurnEndEvent). |
evidence: Draft's StreamEvent lacks TurnStart/TurnEnd signal — metrics panel needs these to track TTFT and token counts without a separate CompleteResult callback. However, ToolResultEvent in my plan is redundant with the draft approach (tool result is appended as a Message, not yielded as an event). Compromise: adopt draft's flat StreamEvent shape + add TurnStartEvent/TurnEndEvent to the kind enum. Simpler than full union while preserving metrics observability. |
ADR-impact: ADR[3] revised — adopt StreamEvent flat dataclass with extended kind enum. ¬full discriminated union. Add kind="turn_start" and kind="turn_end" to carry TTFT + token count signals.

DIV[3]: Canonical Message shape — OpenAI-shaped vs typed ContentBlock
draft-says: canonical Message is OpenAI-shaped (`role`, `content: str`, `tool_call_id`, `tool_calls: list[dict]`) — adapters own complexity of non-OpenAI shapes |
your-plan-says: CanonicalMessage with `content: list[ContentBlock]` typed list — structured content blocks |
verdict: CONCEDE — draft's choice is better. OpenAI-shaped canonical is the correct call because: (1) majority case is string content; (2) the adapter layer (`message_mapping.py`) is where complexity belongs; (3) typed ContentBlock list adds indirection that the draft correctly avoids — callers would need to unwrap blocks for the common string case. The cost of adapting Anthropic's content-blocks to OpenAI canonical is bounded in the adapter; the cost of structured canonical leaks to all callers. |
evidence: Draft explicitly documents this in comment: "The canonical form is OpenAI-shaped by convention; adapters own the complexity." This is the standard LiteLLM/LangChain approach (all canonicalize to OpenAI shape). |
ADR-impact: ADR[4] revised — canonical Message is OpenAI-shaped (role, content:str, tool_call_id, tool_calls:list[dict]). CanonicalMessage with typed ContentBlock list withdrawn. message_mapping.py owns Anthropic block↔str and Gemini parts↔str translation.

DIV[4]: tool_use_reliability taxonomy
draft-says: `none | nominal | reliable | unknown` (4-value) |
your-plan-says: `reliable | experimental | unreliable` (3-value) |
verdict: CONCEDE — draft's taxonomy is better calibrated. `unknown` as explicit state is important for M1 where models haven't been empirically tested yet. `nominal` (emits tool_calls but often malformed) is more precise than `experimental`. The distinction between `none` (SDK doesn't support) and `nominal/unreliable` (SDK supports but model unreliable) tracks a real difference. |
evidence: Draft notes "Updated empirically as observations accumulate" — the `unknown` default enables honest reporting before testing. My 3-value taxonomy had no `unknown` state, forcing premature classification. |
ADR-impact: ADR[1] (ProviderSpec) updated — adopt draft's 4-value taxonomy: none/nominal/reliable/unknown. IC[5] ProviderSpec.tool_use_reliability updated accordingly.

DIV[5]: CLI module presence
draft-says: `cli.py` headless runner in M1 (test without Streamlit, verify streaming to stdout) |
your-plan-says: no CLI module — integration tests handle headless validation |
verdict: CONCEDE — draft is right. A CLI runner is not gold-plating; it enables running the engine without any UI dependency during M1, provides a human-readable stream for debugging SDK events, and creates a replayable artifact (JSONL → CLI replay). Integration tests validate pass/fail; CLI validates "does this feel right." Both serve distinct purposes. |
ADR-impact: add `cli.py` to SQ[] decomposition. SQ[10b]: `chatroom/cli.py` — headless runner, stdout streaming, M1 milestone verification.

DIV[6]: Context budget percentage
draft-says: 60% of max_context_tokens (down from 70%, accounts for tokenizer drift) |
your-plan-says: per-model context budget in ProviderSpec, truncation strategy in ConversationHistory — percentage not specified |
verdict: CONCEDE on the number — 60% is a specific, evidence-based choice (draft explains why: tokenizer drift across providers). My plan had the mechanism right (per-model budget) but lacked the calibrated constant. Adopt 60% as the M1 default; M3 calibrates using reported input_tokens. |
ADR-impact: IC[3] ConversationHistory — add `CONTEXT_BUDGET_FRACTION = 0.60` as documented default.

DIV[7]: Turn policies sequencing
draft-says: all three turn policies (RoundRobin, YieldNext, Random) in M1b |
your-plan-says: YieldNextPolicy in ChatOrchestrator, not explicitly sequenced to M1b |
verdict: CONCEDE — draft's M1b sequencing is correct. YieldNext is needed for M1b success criterion (verify turn-passing behavior); Random is trivial to add alongside. Having all three in M1b costs nothing incremental and completes the policy surface before M2. |
ADR-impact: SQ[11] ChatOrchestrator — explicitly include all three TurnPolicies in M1 scope.

DIV[8]: File structure — src layout
draft-says: `src/sigma_chatroom/` package with src layout |
your-plan-says: `chatroom/` flat layout |
verdict: CONCEDE — src layout is the Python packaging standard (PEP 517+ default). It prevents accidental import from project root, forces correct install, makes `pyproject.toml` packaging cleaner. No downside for this project. |
ADR-impact: file table updated to use `src/sigma_chatroom/` layout.

DIV[9]: memory.py separation
draft-says: separate `memory.py` module for MCP client + sigma_mem_recall tool definition |
your-plan-says: `chatroom/tools/sigma_mem.py` (same concept, different path) |
verdict: ALIGN — functionally identical. Draft's naming is slightly cleaner (`memory.py` vs `tools/sigma_mem.py`). Both separate the MCP client concern from the tool registry. Adopt draft's `memory.py` naming. |
ADR-impact: files table updated: `src/sigma_chatroom/memory.py`.

DIV[10]: Ollama local vs cloud distinction
draft-says: Ollama local + Ollama cloud both implemented as OllamaProvider subclasses — `base_url` differentiates. Cloud example: `deepseek-v3.2:cloud` via Ollama cloud API |
your-plan-says: OllamaProvider covers both local and cloud via `base_url` field in ProviderSpec — same class |
verdict: ALIGN — identical approach. Draft uses same `base_url` parameter to differentiate. No divergence in substance, only naming.

SUMMARY — DIV outcomes:
concede: DIV[3](canonical shape), DIV[4](taxonomy), DIV[5](CLI), DIV[6](60% budget), DIV[7](policy sequencing), DIV[8](src layout), DIV[9](memory.py naming)
defend: DIV[1](Ollama native /api/chat — new evidence, not in draft)
compromise: DIV[2](StreamEvent flat+extended ¬full union)
align: DIV[10](Ollama local/cloud — same approach)
#10 divergences analyzed

### product-designer vs. draft

DIV[1]: Rerun thrash — deferred vs. first-class architecture decision
draft-says: rerun-thrash risk noted ("long sessions may need partial re-render optimization") + deferred to M4 "unless it bites in M3"
your-plan-says: DS[1] fragment-isolation is a M2 DESIGN DECISION (not a deferred optimization). 100-turn soft cap. F6 prototype benchmarks at 50/80/120 turns before committing transcript.py.
DEFEND: fragment vs. full-page-rerun cannot be retrofitted without full file rewrite — design choice not optimization choice. Fragment isolation costs nothing at low turn counts and avoids the rewrite risk. |source:agent-inference+cross-agent(sigma-ui:T2)|
CONCESSION: windowed-render (last 30 turns) is M4 not v1. REVISED: DS[1] = fragment isolation as M2 architecture; windowed render = M4; 100-turn soft cap = v1 operational constraint only.

DIV[2]: Tool-call badge — underspecified vs. 3-state design spec
draft-says: "tool-call badges inline" + "click tool-call badge → full query + result" — no state machine, deferred to implementation engineer
your-plan-says: DS[4] 3-state badge (INVOKED/SUCCEEDED/ERRORED), st.expander proposed mechanism, T3-novel flag, F6 gates mechanism choice
DEFEND 3-state spec, concede mechanism: leaving badge pattern to implementation engineer without state machine produces likely outcome of single-state badge ("tool called") which destroys H8 observability. The 3-state spec is a design precondition, not an implementation detail. |source:H8-analysis+agent-inference|
CONCESSION: st.expander-within-chat_message is T3-novel — label as "proposed pending prototype" not "decided." Three-state spec correct regardless of mechanism.
REVISED: DS[4] retains 3-state specification. Mechanism = "proposed, F6 gates."

DIV[3]: Speaker identity — name badge framing
draft-says: silent (relies on st.chat_message default — which renders name on EVERY message call by default)
your-plan-says: DS[2] "name badge on EVERY message" framed as deliberate design addition
CONCEDE on framing: st.chat_message(name=...) renders name in every container by default — this is Streamlit behavior, not a design override. |source:independent-research(docs.streamlit.io):T1|
REVISED: DS[2] retains genuine additions (13-hue perceptual palette, model-family icon, initials-in-avatar, WCAG contrast flag). Remove "name badge every message" as deliberate-override framing; note we preserve the default and why.

DIV[4]: Preamble variant default — identity-aware vs. neutral
draft-says: preamble_variant = "identity-aware" as ConversationState default
your-plan-says: DS[3] did not specify a default — gap in my plan
DEFEND against draft default: "identity-aware" default systematically biases baseline corpus — every casual/early session produces identity-aware-primed data without deliberate researcher choice. For a research instrument, minimum-priming default ("neutral") preserves clean baseline. Researcher must OPT INTO priming, not opt out. Brad preamble critique (it is a study variable) directly supports neutral as default: if variant is a study variable, its default value is load-bearing. |source:agent-inference — DA may challenge|
CONCESSION: draft made an explicit choice; my plan left a gap.
REVISED: DS[3] default = "neutral." identity-aware selected deliberately only.

DIV[5]: VIABILITY[H11] — P=0.65 vs. tech-architect P=0.87 — NOT PAPERING OVER
draft-says: (no explicit probability; 2h prototype prescribed)
tech-architect R2: P=0.87 conditional on M0 prototype
your-plan-says: P=0.65 conditional on 3 conditions — NOT UPDATING TO MATCH

WHY LOWER — two probabilities answer DIFFERENT questions:
Tech-architect P=0.87 answers: can async bridge + tool events reach Streamlit container? — narrow plumbing, T1 evidence strong.
My P=0.65 answers: does the COMPLETE UI — fragment transcript + live metrics + tool-badge + event-driven rerun — work as a research instrument across 2-3h at 80+ turns?

Specific uncertainty NOT in tech-architect scope:
(1) O(n) transcript render cost at 80+ turns UNMEASURED. sigma-ui 50ms/item used monitoring-grade renders; chat-streaming has more DOM per item (nested expanders, ongoing write_stream). NOT tested by 2h async bridge prototype.
(2) Event-driven fragment trigger racing with timer-driven rerun — untested. Potential double-update or dropped turns.
(3) Tech-architect defers rerun thrash to M4; their P inherits that deferral. If problem materializes at 50 turns not M4-territory, P=0.87 was overconfident.

RECOMMENDATION: Do NOT paper over with compromise P. Expand prototype success criteria: (a) async bridge works [tech-architect criterion], (b) render cost at 80 turns <300ms [my criterion], (c) event-driven trigger does not race with timer [my criterion]. All three pass → both P values converge toward 0.85+. Test (b) fails → early evidence for Textual TUI before M2. The divergence is load-bearing. DA should assess as such. |source:agent-inference — flagged for DA|

### product-strategist vs. draft

**Context:** Draft left research question explicitly UNPINNED (open decisions #1: four candidates listed, no selection). My R1 pinned Q1+Q2 de novo. Primary divergences: question pinning, milestone naming collision, metrics scope, Ollama compat assumption.

DIV[1]: Research question — draft deferred, my R1 pinned
draft-says: "Observe emergent behavior" is fine; four candidate questions listed as open decision #1 "before M3"; no selection made.
your-plan-says: Q1 (chatroom-context tool-use vs. BFCL baseline) + Q2 (yield-next spontaneity under preamble-variant controlled comparison) pinned in R1 with null-result pre-registration.
verdict: DEFEND — draft's deferral is a strategic liability. Draft's own open decisions #1 and #2 are explicitly co-dependent ("which research question narrows which metrics actually matter"). Leaving both unresolved means the M3 metrics panel will be built without knowing which question it serves. Correct order of operations: pin question → derive essential metrics → build instrument to answer it. My R1 pinning is the right sequencing. |source:[agent-inference + draft open-decisions]

DIV[2]: Research question selection — draft candidate (a) vs. my Q1 (candidate (d) revised)
draft-says: Candidate (a) memory-invocation coherence listed first (implicitly primary).
your-plan-says: Q1 = chatroom-context tool-use vs. BFCL baseline (candidate (d) with framing revision to "chatroom-delta vs. single-model baseline"). Candidate (a) data collected at M3, analysis deferred to M4.
verdict: DEFEND — candidate (a) requires NLP post-processing (query similarity analysis) to answer the question. Instrument can collect query_text at M3 (zero-cost schema field), but the similarity analysis is M4 work. It cannot be ANSWERED at M3. Q1 (tool-use reliability) is answerable directly from ToolCallRecord (invoked/malformed_json/result_used) without post-processing, has an external T1 calibration anchor in BFCL V4, and directly serves Project 3 roster assignment. §2g outcome 1 (framing revised): "chatroom-context delta vs. BFCL" is more precise and novel than just "reliability spectrum." Candidate (a) data is still collected — it is not rejected, it is scheduled for M4 analysis.
flag for user: If primary research interest is memory-invocation coherence (candidate (a)) over tool-use reliability (my Q1), the pinning should change — instrument collects both datasets identically, only the analysis priority at M3 vs. M4 changes. |source:[independent-research]|T1-verified (BFCL V4)

DIV[3]: Milestone naming — canonical collision (OQ[1] lead flag)
draft-says: M1a = two-model streaming (no tools), M1b = tool-use on same pair + exec loop, M1c = remaining SDK families. Pre-M2 2h prototype mentioned as separate pre-M2 task (not numbered milestone).
your-plan-says: M0 = 2h viability prototype (kill-switch), M1a = types + ProviderProtocol, M1b = providers + engine in parallel clusters, M1c = Streamlit async bridge prototype.
tech-architect's naming: M0 = viability, M1a = types, M1b-e = individual SQ[] items, M2 = Streamlit, M3 = sigma-mem.
verdict: CONCEDE PARTIALLY + PROPOSE CANONICAL — my R1 M1c (Streamlit bridge prototype) conflicts with draft's M1c (remaining SDK families) and with tech-architect's labeling. I misplaced the bridge prototype as M1c in R1; it belongs at M0 or as a pre-M2 gate (as draft labels it). Proposed canonical resolution:
  M0: 2h viability prototype (Streamlit async bridge + one tool_call event) [tech-architect + my R1 intent + draft "pre-M2 prototype"]
  M1a: Types + ProviderProtocol ABC [tech-architect + my R1]
  M1b: Two-provider streaming, no tools (Anthropic + Ollama cloud) [draft's M1a scope]
  M1c: Tool-use on same pair + exec loop [draft's M1b scope]
  M1d: Remaining SDK families (OpenAI + Gemini) + full roster [draft's M1c scope]
  M2: Streamlit MVP [all plans agree]
  M3: sigma-mem + metrics + v1 ship [all plans agree]
My R1 M1c label (Streamlit bridge) was a naming error — the CONTENT (bridge prototype as kill-switch) is correct, only the label placement was wrong. The bridge prototype should be M0, not between M1a and M1b.
evidence: Draft's explicit "Pre-M2 2h prototype" language confirms bridge prototype is pre-M2, not mid-M1. |source:[draft comparison + cross-agent]

DIV[4]: Ollama compat — draft assumes working OpenAI subclass, my R1 flags broken
draft-says: "ollama_client.py — local + cloud (OpenAI-compat subclass)". Treats Ollama as OpenAI-compat subclass throughout, no streaming+tool_calls flag.
your-plan-says: Ollama OpenAI-compat silently drops tool_calls when streaming=True (T1-verified: ollama/ollama#12557). Native /api/chat endpoint required.
verdict: DEFEND — this is a factual T1 finding, not an opinion. Draft's OpenAI-compat subclass approach is the exact pattern that triggers the silent drop. Tech-architect ADR[6] independently reached the same conclusion. Using draft's approach produces an instrument where Ollama tool-calls appear to never invoke — silently — directly contaminating Q1 data (misclassifying "SDK silently dropped tool_call" as "model declined"). This is material, not minor.
evidence: ollama/ollama#12557 (open issue, production maintainer confirmation). Tech-architect ADR[6] independently sourced same evidence. |source:[independent-research]|T1-verified

DIV[5]: Metrics scope — draft's M3 metrics vs. my essential/luxury split
draft-says: M3 metrics include TTFT distribution, stop_reason histogram, yield-next override rate, tool-invocation rate per 1000 tokens, query-topic frequency — all proposed as M3 metrics. "Flows from stream events at zero marginal cost" for most.
your-plan-says: Essential (M3) = 8 zero-cost schema fields tied to Q1/Q2. Luxury (M4) = embedding/NLP metrics.
verdict: PARTIAL CONCEDE — my "zero-cost schema fields" framing was too narrow. Draft's TTFT distribution, stop_reason histogram, and yield-next override rate are simple aggregations of already-captured events — they fit my §2c "zero additional data collection" criterion and belong in M3. Upgrading essential metrics to include these draft items. Exception: "query-topic frequency" (draft's per-tool-call metric) requires NLP clustering → M4. Remaining luxury metrics (embedding convergence, topic drift, speaker-influence graph) stay M4.
revised essential metrics (M3, expanded): ToolCallRecord fields (invoked, malformed_json, result_used, query_text) + preamble_variant + raw turn output + model metadata + timestamps + TTFT distribution + stop_reason histogram + yield-next override rate + tool-invocation rate per 1000 tokens.
evidence: Draft's own annotation: "flows from stream events at zero marginal cost" for these items — consistent with my §2c zero-cost assessment. |source:[cross-agent + agent-inference]

DIV[6]: Preamble variants — draft three-variant taxonomy vs. my binary A/B
draft-says: Three variants: neutral, identity-aware (default), research-framed. YieldNext mentioned in identity-aware and research-framed; neutral omits it.
your-plan-says: Binary preamble-A (mentions @next:) vs. preamble-B (silent) for Q2 treatment.
verdict: COMPROMISE — draft's three-variant taxonomy is richer and maps cleanly onto my Q2 treatment: neutral = preamble-B-equivalent (no @next: mention = Q2 control condition); identity-aware and research-framed = preamble-A-equivalent (with @next: = Q2 treatment). Adopting draft's three-variant taxonomy preserves Q2 operationalization while enabling finer-grained cross-session analysis (does "research-framed" change coordination behavior vs. "identity-aware"?). Zero implementation cost — Q2 analysis still works, preamble_variant field captures which of three variants ran.
evidence: Draft's explicit rationale ("neutral omits @next: so spontaneous yield-next becomes observable") directly implements my Q2 control condition. |source:[cross-agent]

**Summary of R2 position shifts:**
- DIV[3]: M1c naming error in R1 corrected. Proposed canonical naming: M0→M1a→M1b→M1c→M1d→M2→M3
- DIV[5]: Essential metrics expanded to include draft's stream-aggregation metrics (TTFT distribution, stop_reason histogram, yield-next override rate); only embedding/NLP metrics remain M4-deferred
- DIV[6]: Preamble variant taxonomy upgraded from binary A/B to draft's three-variant (neutral/identity-aware/research-framed); Q2 operationalization preserved
- All other R1 positions defended with evidence

---

**Product-strategist Brad-critique responses (strategic domain — appended to shared brad-critique section):**

### brad-critique responses

BR[M1-scope-60-70%]: "M1 is ~60-70% of the whole project. Phase boundaries understate schedule risk. Consider M1a (one provider, streaming, no tools), M1b (tool use on that provider, exec loop), M1c (remaining three)."
verdict: CONCEDE — partially. Brad's 60-70% claim is plausible and I flagged it myself in §2b (outcome 3 gap: estimate at optimistic end of reference class). My CAL[M1-engine] at 4d against CAL[total-v1] at 10d = 40% — below Brad's 60-70% range. The gap is explained by: Brad likely includes iterative debugging of streaming edge cases (tool_call delta reconstruction, Gemini function_response round-trip, Ollama native API behavior differences) that aren't captured in my SQ[] point estimates. |
evidence: §2b outcome 3 already flagged this — "no codebase precedent for multi-provider streaming, estimate at optimistic end of industry range." Brad's critique is independent confirmation of the same risk. |
ADR-impact: CAL[M1-engine] revised: point=5d (up from 4d), 80%=[4d,8d], 90%=[3d,10d]. M1 as fraction of total: 5/11 = ~45% at point estimate, up to 8/12 = 67% at 80% upper bound. Consistent with Brad's range. M1a/b/c sub-milestone split (per draft and Brad) is the correct risk isolation strategy — already in my plan, now with explicit milestone gating. |
remaining-risk: M1c (Gemini + remaining providers) is where the estimate is most uncertain. Gemini function_response adapter is novel; no T1/T2 precedent for this exact round-trip in a multi-model chatroom context. Flag for DA scrutiny.

BR[Streamlit-async-fiddliness]: "st.write_stream() wants sync string iterator; TurnEngine yields async non-string events. Bridging needs thread+queue shim. Rerun-per-turn cost scales with transcript length. Worth a 2h throwaway before committing."
verdict: DEFEND with agreement — my plan already contains the 2h viability experiment (SQ[1]) as a hard gate before M1. My research found that st.write_stream() does accept async generators (Streamlit internally converts) BUT with the caveat that cached object dependencies can raise errors. The queue-based bridge is my preferred fallback. |
evidence: docs.streamlit.io/st.write_stream: "If you pass an async generator, Streamlit will internally convert it to a sync generator." This is newer behavior Brad may not have been aware of when writing the critique. However, the "cached object" caveat and "Event loop closed" errors reported in streamlit/streamlit#12076 confirm his concern about bridge reliability is real. |
ADR-impact: ADR[5] (concurrency model) already addresses this. SQ[1] viability experiment gates M1. ¬revision needed, but Brad's specific concern about rerun-per-turn transcript length cost is real and worth noting: PM[4] (Streamlit session state corruption) addresses some of this; the rerun cost issue should be added to PM as PM[5] or noted under ADR[5] break-if condition. Already in plan: "break-if: 13-model round >120s." Adding: rerun-per-turn cost at >20 turns may require partial re-render optimization (deferred M4 unless it surfaces in M3 testing).

BR[message-mapping-hardest]: "The harder tool-use adapter work isn't schema, it's message mapping. Anthropic content-blocks, OpenAI siblings+role=tool, Gemini function_call/function_response parts."
verdict: DEFEND — already in my plan. H7 assessed as PARTIALLY-CONFIRMED: Gemini adapter IS notably hard (no role=tool concept), Anthropic↔OpenAI multi-turn tool history is also non-trivial. I elevated message_mapping to a dedicated module in my file table. Brad and I agree on the diagnosis. |
evidence: My ADR[4] explicitly calls out Gemini as hardest surface ("no role=tool concept, function_response in user content") and requires integration fixture test before plan lock. Brad's message_mapping.py as merge gate = my tests/test_adapters.py round-trip fixture requirement. |
ADR-impact: ¬revision needed. Already planned. BR affirms ADR[4].

BR[preamble-as-study-variable]: "System preamble is a study variable, not a detail. Observations are functions of that prompt. Log which variant ran so cross-session comparisons are interpretable."
verdict: DEFEND — already in my plan. H9 confirmed in plan: "System preamble is an experimental parameter, not a design detail." PreambleVariant logged in ConversationHistory per session. Draft has the same pattern (PreambleVariant on ConversationState). |
evidence: My plan explicitly addresses H9 and H10 (YieldNextPolicy discoverability as preamble-variant decision). BR affirms both. ¬revision needed.

BR[memory-speaker-redundancy]: "The 'memory' Turn speaker seems redundant if memory access is tool-mediated — tool calls are ToolCallRecords on a Turn, not Turns themselves. Might be legacy from an earlier text-convention draft."
verdict: DEFEND — not in my plan. My plan has no "memory" speaker. Tool calls are ToolCallRecords embedded in TurnEndEvent (or on Turn.tool_calls in the draft). Brad is critiquing the prior draft, not my plan. I independently reached the same conclusion: tool invocations are records ON a turn, not separate turns. ¬revision needed for my plan. |
evidence: My ADR[2] and IC[2] both treat tool calls as sub-events within a turn, not as separate turns. My Turn equivalent (TurnEndEvent) has a tool_calls list. "memory" as a speaker would corrupt the observability signal — it would appear as a model participant, not as a tool invocation. BR confirms my approach is correct.

BR[Ollama-raw-capture-H8]: "Ollama small-model 'did they invoke tools' observation is only interpretable if you log raw tool-call chunks and SDK parse errors — otherwise '0 invocations' conflates 'declined' with 'tried and emitted malformed JSON that SDK swallowed.'"
verdict: CONCEDE + UPGRADE — H8 pre-concession already logged in gate-log (26.4.16). My ADR[7] had capture_raw as per-session opt-in. Draft has it as default-on for tool_use_reliability != reliable. Brad's critique confirms this must be the default. |
ADR-impact: ADR[7] revised — raw-event sidecar capture_raw defaults TRUE for all speakers with tool_use_reliability != "reliable" (= "unknown", "nominal", "none"). This is already the draft's design. For "reliable" speakers, capture_raw defaults FALSE (opt-in via CHATROOM_CAPTURE_RAW=1 env var). This matches draft exactly. My pre-challenge concession was correct.

BR[research-question-first]: "What's the first research question? 'Emergent behavior' doesn't scope M3's metrics panel. Pick one before M3."
verdict: OUT-OF-SCOPE-FOR-TECH-ARCHITECT — this is product-strategist domain. Brad is correct that the research question scopes the metrics panel. I note for completeness that my plan does NOT prescribe which metrics matter beyond the structural observables (TTFT, token counts, tool call timing, stop reasons) — these flow from stream events at zero marginal cost regardless of which question is chosen. The specific research question narrows which derived metrics (embedding convergence, speaker-influence graph) justify M4 scope. ¬architecture revision needed from me; flagging for product-strategist + lead. |
evidence: My metrics.py in SQ[] captures the baseline observables. Which question to answer is a product decision that constrains M4 scope. Architecture is question-agnostic at M1-M3 level.

BR[YieldNext-discoverability]: "Decide explicitly whether the system preamble tells speakers about @next:<name>. If yes, you've engineered the behavior; if no, the feature becomes an observation about which models spontaneously attempt it."
verdict: DEFEND — already addressed in H10. My plan explicitly flags this as a preamble-variant design decision: "Whether preamble tells models about @next:<name> is itself an observable." Draft's PreambleVariant also handles this (identity-aware mentions the convention; neutral omits it). ¬revision needed. BR confirms H10 framing is correct.

#7 Brad critique points addressed |domain-relevant: 6/7 (BR[research-question-first] flagged as product-strategist domain)

**Product-strategist BR responses (strategy/research-instrument domain):**

BR-PS[research-question-first]: Brad: "'Observe emergent behavior' doesn't scope M3's metrics panel. Before M3, pick one question." |domain: product-strategist primary
verdict: CONCEDE FULLY — Brad is correct. Draft left this as open decision #1. My R1 pinned Q1+Q2. Brad's logic ("the question determines which metrics matter") is exactly the reasoning I applied to separate essential from luxury metrics. His critique validates my R1 sequencing (pin question → derive metrics → build instrument). His specific candidates (a)-(d) were the input to my R1 analysis.
Brad's candidate (a) [memory-invocation coherence] vs. my Q1 [tool-use vs. BFCL]: Brad did not rank candidates. My Q1 is candidate (d) revised. Defense: (d) is answerable at M3 without NLP post-processing; has BFCL T1 external calibration anchor; directly serves Project 3. Candidate (a) data is COLLECTED at M3 (query_text in ToolCallRecord) but the similarity analysis is M4. This is not rejecting (a) — it is scheduling it correctly.
flag for user: If primary research interest is candidate (a) over candidate (d), the pinning should change — instrument collects both datasets at M3. The question is analysis priority. |source:[independent-research]|T1-verified (BFCL V4)

BR-PS[preamble-as-study-variable]: Brad: "System preamble is a study variable, not a detail. Log which variant ran so cross-session comparisons are interpretable."
verdict: CONCEDE AND STRENGTHEN — Brad is right. My Q2 (yield-next spontaneity) operationalizes this critique directly. preamble_variant is logged per session (C4 constraint). Adopting draft's three-variant taxonomy (neutral/identity-aware/research-framed) per DIV[6] compromise is the correct implementation. Q2 control condition = neutral (no @next: mention). Q2 treatment = identity-aware or research-framed (with @next: convention). Brad's critique is fully absorbed into Q2 with richer three-variant design. |source:[cross-agent + agent-inference]

BR-PS[M1-60-70%-scope]: Brad: "M1 is ~60-70% of whole project. Phase boundaries understate schedule risk."
verdict: PARTIAL CONCEDE — my R1 flagged this as [prompt-claim] unverified. After reading draft in full, Brad's claim is plausible under 80th percentile assumptions. Draft's M1 scope (4 SDK families × adapter surfaces + TurnEngine + 3 policies + persistence + metrics + CLI + test suite) vs. M2 (UI shim + Streamlit modules) and M3 (1 MCP tool + panel) supports Brad's weight distribution directionally. Tech-architect CAL[M1-engine] at 4d of 10d total = 40% at point estimate; at 80% upper bound (M1=6d, total=10d) = 60% — consistent with Brad's range. Upgrade from "unverified [prompt-claim]" to "plausible under 80th percentile assumptions."
OQ[2] resolution: §2b gap REMAINS — no codebase precedent for streaming turn-loop confirms the uncertainty band is wide. DA should still scrutinize M1 point estimate. Brad's proposed M1a/b/c sub-milestone split (per canonical naming DIV[3] compromise) is the correct risk isolation strategy regardless of the exact percentage.
evidence: Draft scope breakdown (4 SDK families × 3 adapter surfaces = 12 adapter code paths in M1) vs. M2+M3 combined scope (UI + 1 tool). Directionally consistent with Brad's 60-70% claim. |source:[draft comparison + cross-agent]|T2-corroborated

**Product-designer BR responses (UI/design domain):**

BR-PD[streamlit-async-fiddliness]: Brad: "st.write_stream() wants sync string iterator; TurnEngine yields async non-string events. Bridging needs thread+queue shim. Rerun-per-turn cost scales with transcript length. Worth a 2h throwaway before committing."
verdict: FULL AGREEMENT on diagnosis — EXTEND on scope of prototype
evidence: My VIABILITY[H11] independently identified all three sub-problems: (a) async-to-sync bridge required, (b) one-turn-per-rerun constraint real, (c) full-script re-execution cost. My DS[1] (fragment isolation) addresses (c) more specifically than the draft does. Brad correctly diagnoses; my plan adds a concrete architecture response (DS[1]) and an extended prototype scope (render cost at 80 turns, not just async plumbing). |source:independent-research(docs.streamlit.io:T1)+independent-research(Brad-critique)|
EXTENSION: prototype success criteria should include (a) async bridge works, (b) render cost at 80 turns <300ms, (c) event-driven trigger does not race with timer. Brad says 2h prototype — correct, but the 2h must test these three conditions, not just (a). This is where my P=0.65 diverges from tech-architect P=0.87: their prototype tests (a); mine requires (b) and (c) also.

BR-PD[preamble-variant-UX]: Brad: "The system preamble is a study variable, not a detail. Frame preamble choice as experimental parameter from the start — log which variant ran, so cross-session comparisons are interpretable."
verdict: FULL AGREEMENT — DS[3] is specifically designed around this critique
evidence: DS[3] implements three observable signals: (a) section label "Session Variables" communicates experimental parameter status, (b) persistent badge in session header makes variant visible throughout session, (c) JSONL write on Start click (not on init) ensures variant is in log header. Custom variant captures verbatim preamble text for H10 observability. Brad says "log which variant ran" — DS[3] logs it in JSONL header, displays it as persistent badge, and captures it on session start before any turns occur. |source:independent-research(Brad-critique)+H9/H10-analysis|
EXTENSION: DIV[4] extends Brad further — I challenge the draft default (identity-aware) as biasing the baseline corpus. Brad implicitly supports neutral as default: if preamble is a study variable, its default value is load-bearing and must be deliberate. This is a design decision that goes beyond Brad's critique.

BR-PD[raw-capture-for-observability]: Brad: "Ollama small-model observation is only interpretable if you log raw tool-call chunks and SDK parse errors — otherwise 0-invocations conflates declined with tried-and-malformed-swallowed."
verdict: FULL AGREEMENT — this is PM[D2] in my design plan
evidence: PM[D2] (badge silent failure) is exactly Brad's concern at the UI level. My DS[4] three-state badge (INVOKED state specifically) is the UI manifestation — it requires raw-event capture to work. If raw capture is not implemented (or is optional), the INVOKED state never renders and the badge silently degrades to single-state (tool result only). Brad says "only interpretable if you log" — my design says "UI design precondition, not optional feature." ADR[7] (tech-architect R2-updated) now has raw capture default=True for unreliable models, which satisfies the requirement. |source:independent-research(Brad-critique)+H8-analysis+PM[D2]|

BR-PD[memory-turn-redundancy]: Brad: "memory Turn speaker seems redundant if memory access is tool-mediated."
verdict: CONCEDE — already addressed in draft and my plan, and Brad is correct
evidence: Draft explicitly notes in Turn dataclass comment: "speaker: str — NOT memory (tool calls are ToolCallRecords, not Turns)." My design independently reaches the same conclusion: ToolCallBadge is inline on the invoking model's turn, not a separate speaker turn. Brad's critique applies to an earlier text-convention draft; both the draft and my plan have already corrected this. If a "memory" speaker existed in the transcript, my DS[2] speaker-identity system would assign it a color and initials — creating false impression of a 14th conversation participant. The corrected model (tool calls as ToolCallRecord on a Turn) is correct for the instrument. |source:independent-research(Brad-critique)+draft-plan:T1|

#4 BR responses (design domain)|all-addressed|no-remaining-gaps


## architecture-decisions (locked after DA approval)

ADR[1]: purpose-built src/sigma_chatroom/providers/ module |¬import sigma-verify (wrong shape) |study env-key discovery pattern |ProviderSpec.tool_use_reliability=none/nominal/reliable/unknown (4-value, empirical) |owner: tech-architect |status: proposed-r2-updated
ADR[2]: tool-exec loop in TurnEngine |¬in Provider |Provider.stream()=one SDK call |TurnEngine=loop+history+policy |owner: tech-architect |status: proposed
ADR[3]: StreamEvent flat dataclass with extended kind enum |kind=token|tool_call|tool_result|turn_start|turn_end|stop|error |¬full discriminated union (simpler, draft-aligned) |turn_start/turn_end carry TTFT+token-count signals for metrics |turn_end MUST carry: input_tokens:int, output_tokens:int, stop_reason:str, ttft_ms:int|None, total_ms:int (per-provider extraction, fallback=0 ¬None) |multi-tool_call: SERIAL execution — each ToolCallEvent strictly precedes its ToolResultEvent before next tool begins |owner: tech-architect |status: proposed-r2-challenge-updated
ADR[4]: Message canonical shape = OpenAI-shaped (role, content:str, tool_call_id, tool_calls:list[dict]) |adapters own complexity |message_mapping.py: Anthropic blocks↔str, Gemini parts↔str |round-trip fixture tests = merge gate |Gemini role="tool" maps to Content(role="user", parts=[Part.from_function_response(name, response)]) |owner: tech-architect |status: proposed-r2-updated (conceded typed ContentBlock list)
ADR[5]: sequential turn-taking + per-model async streaming |¬concurrent |steelman: Poe-style parallel columns — rejected: (a) research goal=conversation not comparison (models must read prior output); (b) Streamlit threading fragile under concurrent async writes; (c) turn-ordering is experimental variable (YieldNextPolicy) — parallel eliminates it |queue-based sync bridge for Streamlit |break-if: 13-model round >120s OR rerun cost >5s at turn 20+ |context_budget=0.60 of max_context_tokens (default, M3 calibrates) |owner: tech-architect |status: proposed-r2-challenge-updated
ADR[6]: Ollama native /api/chat ¬OpenAI compat |compat silently drops tool_calls when stream=True (production-confirmed: ollama#12557, openclaw#11828) |¬subclass of OpenAIProvider |separate OllamaProvider using ollama Python library |reversal condition: IF ollama#12557 closed+fix-merged AND ollama Python library >=X.Y passes VIABILITY experiment tool_call chunk-shape test THEN reconsider (reachable via changelog monitoring) |owner: tech-architect |status: proposed-r2-challenge-updated
ADR[7]: JSONL persistence + raw-event sidecar |schema_version on every line |capture_raw default=True for tool_use_reliability in {unknown,nominal,none} |capture_raw default=False for reliable (opt-in via CHATROOM_CAPTURE_RAW=1) |rationale: distinguish declined vs malformed-JSON-swallowed |env var name: CHATROOM_CAPTURE_RAW |owner: tech-architect |status: proposed-r2-challenge-updated (upgraded from per-session flag)
ADR[8]: sigma-mem via MCP stdio client ¬direct import |once-per-session subprocess (¬per-call) |startup cost ~500ms amortized over session |5s timeout per tool_call |single restart on crash detection (MemoryHelper monitors liveness before each call) |failure=tool_result error string (observable) |module: src/sigma_chatroom/memory.py |owner: tech-architect |status: proposed-r2-challenge-updated
ADR[9]: M0-fallback decision tree (4-branch) |BRANCH(a): all 4 criteria PASS → M1 proceeds |BRANCH(b): render@80-turns FAIL only → windowed render (last 30 turns) OR 100-turn hard cap; re-test; still FAIL → Textual TUI |BRANCH(c): fragment-race FAIL only → sequential-only streaming, timer-only run_every=0.5s, 0-500ms staleness acknowledged |BRANCH(d): async-bridge FAIL (all bridge strategies) → headless JSONL + CLI runner; Q1/Q2 answerable from JSONL without UI |BRANCH(d-total): all 4 FAIL simultaneously → escalate to user with specific evidence ¬unilateral pivot |owner: tech-architect |status: NEW-challenge-round-1

## design-system (locked after DA approval)

DS[1]:transcript-rendering |fragment-isolated-append-only |@st.fragment(run_every=1.0) |turn=st.chat_message |token=write_stream-sync-gen |tool-badge=post-stream-expander |100-turn-soft-cap |F6-prototype-gates |source:T1(docs.streamlit.io)+T2(sigma-ui)
DS[2]:speaker-identity |13-hue-HSL-perceptual-palette(0°→331°) |L-PER-HUE:warm(28°-110°)=L58-65%,cool(138°-331°)=L45% |WCAG-AA-4.5:1-REQUIRED-tool-validated-pre-lock(SQ[D8a]) |avatar=base64-SVG-data-URI(hue+initials,¬ement-emoji,¬-CSS-circle) |name-badge=Streamlit-default(every-message-via-chat_message) |model-family-icon(A/O/G/L) |T3-contrast-flag-RESOLVED-by-L-adjustment
DS[3]:preamble-variant-picker |section-label="Session Variables"(¬"Experimental") |dropdown+description-per-option |4-options(neutral,identity-aware,research-framed,custom) |persistent-st.badge-in-session-header |JSONL-header-write-on-start-click |custom=verbatim-capture |→H9+H10-observable
DS[4]:tool-call-badges |st.status()-Streamlit->=1.28-native(¬st.expander) |3-states(invoked=amber+spinner,succeeded=green+check,errored=red+x) |expand=query+result_preview+200-chars |T3-novel-flag-REMOVED(st.status=T1-documented-primitive) |F6-prototype-gates-criterion-d |purpose-built-for-agent-steps
DS[5]:metrics-panel |right-column(@st.columns) |@st.fragment(run_every=2.0) |3-tabs(per-speaker+per-tool-call+session) |per-speaker=dataframe(turns,tokens,TTFT_p50,stop_reason,tool_calls,tool_lat) |per-tool=dataframe(speaker,query_preview,latency,result_chars,turn_pos) |session=st.metric-row |event-driven-trigger(turn_complete_flag)
DS[6]:sidebar-controls |3-st.expander-sections(session-vars+roster+controls) |roster-locked-post-start |env-key-absent=struck-through+tooltip |tool_use_reliability=colored-dot(green/amber/red)
DS[7]:session-management |pre-session-st.dataframe(last-10) |columns(id,date,roster,turns,preamble_variant) |actions(load=read-only,export=path-to-clipboard,delete=confirmation) |JSONL-native-read-replay

## interface-contracts (build-track implements against these)

IC[1]: ProviderProtocol — async stream(messages, tools) → AsyncIterator[StreamEvent] |format_tool_definition(tool) → dict |provider_id, model_id, tool_use_reliability fields
IC[2]: TurnEngine — async run_turn(conversation, speaker) → AsyncIterator[StreamEvent] |max_iterations=3 CYCLES (tool_call→execute→tool_result = 1 cycle, not 1 call) |after cap: final provider.stream() call with tools=None (model gets chance to produce final response) |StreamEvent(kind="turn_end", stop_reason="max_tool_calls") emitted regardless |serial multi-tool invariant: ToolCallEvent for call_id X precedes ToolResultEvent for call_id X, with NO interleaving from other tool calls (serial execution across all tools in one response) |turn_end MUST carry: input_tokens, output_tokens, stop_reason, ttft_ms, total_ms extracted from per-provider usage response |usage extraction: Anthropic=message_delta.usage, OpenAI=final-chunk-include_usage=True, Gemini=usage_metadata, Ollama=usage field on final chunk
IC[3]: ConversationHistory — append(message), to_provider_messages(provider_id) → list[dict], token_count_estimate(provider_id) → int, truncate_to_budget(provider_id, budget) → ConversationHistory |HARD INVARIANT: truncate_to_budget() MUST maintain tool_call/tool_result pair integrity — NEVER split a pair |consequence of violation: API 400 error (Anthropic validated, OpenAI validated) |algorithm: walk oldest→newest, skip pairs that don't fit budget atomically, never truncate mid-pair |CONTEXT_BUDGET_FRACTION = 0.60 default
IC[4]: ToolRegistry — register(name, handler), async execute(name, tool_input) → ToolResult, definitions() → list[ToolDefinition]
IC[5]: ProviderSpec — dataclass: provider_id, model_id, display_name, tool_use_reliability: Literal["none","nominal","reliable","unknown"], api_key_env, base_url, context_window
IC[6]: SessionWriter — write_event(event: StreamEvent), write_raw(provider_id, chunk_bytes), close()
IC[7]: SessionRunner (formerly ChatOrchestrator) — async run_round() → AsyncIterator[StreamEvent], async run_autonomous(max_rounds) → AsyncIterator[StreamEvent] |v1 concrete responsibilities: (1) turn-ordering via TurnPolicy; (2) round loop (run_round/run_autonomous); (3) SessionWriter lifecycle (open/close on session boundaries); (4) asyncio event loop for cross-provider sequencing in Streamlit context |holds: TurnPolicy, SessionWriter, list[Provider] |¬v2 speculative hooks

## sub-task-decomposition

SQ[1]: M0 viability experiment — 4-criteria prototype |estimable:yes |files: experiments/viability.py |effort: 2-4h |GATE: all 4 criteria must PASS before M1 proceeds |criteria: (a) queue-based async bridge: token+tool event visible in Streamlit ≠ crash; (b) fragment-race: timer+event-driven rerun on same fragment with active write_stream — zero token duplication; (c) render@80-turns<1000ms: 80 static st.chat_message elements rendered in TranscriptFragment; (d) Ollama native streaming tool_call chunk shape: verify tool_calls field present in streaming chunk (¬only final chunk) |fail-branch per ADR[9] decision tree |owner: implementation-engineer
SQ[2]: types.py — CanonicalMessage, StreamEvent, ToolDefinition, ProviderSpec |estimable:yes |files: src/sigma_chatroom/types.py |effort: 3h |owner: implementation-engineer
SQ[3]: AnthropicProvider — streaming + tool_use content blocks |estimable:yes |notes: content-block buffer reassembly required (accumulate input_json_delta until content_block_stop before yielding StreamEvent tool_call) |files: src/sigma_chatroom/providers/anthropic_provider.py |effort: 5h |owner: implementation-engineer
SQ[4]: OpenAIProvider — streaming + tool_calls delta reconstruction |estimable:yes |files: src/sigma_chatroom/providers/openai_provider.py |effort: 4h |owner: implementation-engineer
SQ[5]: GeminiProvider — function_call parts + function_response (no role=tool) |estimable:yes |notes: hardest adapter — no role=tool concept; function_response embedded in user-role Content; estimate increased due to SDK instability history and asymmetric to_provider_messages() |files: src/sigma_chatroom/providers/gemini_provider.py |effort: 6-8h |owner: implementation-engineer
SQ[6]: OllamaProvider — native /api/chat streaming + tool_calls |estimable:yes |notes: success criterion must verify streaming tool_call chunk shape empirically (not just final-chunk shape) |files: src/sigma_chatroom/providers/ollama_provider.py |effort: 4h |owner: implementation-engineer
SQ[7]: TurnEngine — tool-exec loop, ToolCallRecord, max_iterations cap, serial multi-tool, usage extraction |estimable:yes |notes: explicit max_iterations=3-CYCLES semantics; after cap → final call with tools=None; serial execution invariant for multi-tool_call responses; usage extraction from per-SDK response fields |files: src/sigma_chatroom/engine/turn_engine.py |effort: 5-6h |SEQUENTIAL after SQ[8] |owner: implementation-engineer
SQ[8]: ConversationHistory — truncation with tool_call/tool_result pairing invariant, token estimate |estimable:yes |notes: pairing invariant is HARD CORRECTNESS requirement — truncation algorithm must walk oldest→newest and drop pairs atomically (never split); violation = API 400 on Anthropic+OpenAI |files: src/sigma_chatroom/engine/history.py |effort: 4h |owner: implementation-engineer
SQ[9]: ToolRegistry + sigma_mem_recall MCP stdio client with once-per-session subprocess lifecycle |estimable:yes |notes: MemoryHelper wrapper monitors subprocess liveness; single restart on crash; terminate on SessionWriter.close() |files: src/sigma_chatroom/tools/registry.py, src/sigma_chatroom/memory.py |effort: 4h |owner: implementation-engineer
SQ[10]: SessionWriter — JSONL + raw sidecar |estimable:yes |files: src/sigma_chatroom/persistence/session_writer.py |effort: 3h |owner: implementation-engineer
SQ[11]: SessionRunner (formerly ChatOrchestrator) + all 3 TurnPolicies (RoundRobin, YieldNext, Random) |estimable:yes |notes: SEQUENTIAL after SQ[7] and SQ[8] (constructor depends on TurnEngine + ConversationHistory); all 3 policies in M1 scope |files: src/sigma_chatroom/engine/session_runner.py, src/sigma_chatroom/engine/turn_policy.py |effort: 5h |SEQUENTIAL after SQ[7,8] |owner: implementation-engineer
SQ[12]: M1 integration test — headless 2-model session (Anthropic + Ollama cloud), one tool call, with explicit assertion set |estimable:yes |assertions required: (1) tool_result threaded back into conversation after TurnEngine exec loop; (2) ToolCallRecord.preceding_text + position_in_turn non-empty; (3) JSONL ordering: tool_call line precedes tool_result line; (4) failure cases: tool error, tool timeout (5s), max_iterations=3 hit; (5) StreamEvent(kind="turn_end") carries non-zero input_tokens; (6) SessionWriter writes raw sidecar for unknown/nominal reliability models |mock contract: MockProvider.stream() MUST yield AsyncIterator[StreamEvent] sequence including at least one kind="tool_call" event — ¬return CompleteResult |files: tests/test_m1_integration.py |effort: 3h |owner: implementation-engineer
SQ[12b]: per-SDK adapter round-trip fixture + cross-SDK turn chain test |notes: 4-SDK round — Anthropic→OpenAI→Gemini→Ollama — each model reads prior turn's content via to_provider_messages(provider_id); verify Gemini function_response canonical form; verify tool_call+tool_result pair appears correctly in each SDK's format |files: tests/test_adapters.py, tests/test_cross_sdk_chain.py |effort: 3h |owner: implementation-engineer
SQ[13]: Streamlit app scaffold + config UI |estimable:yes |files: src/sigma_chatroom/app.py, src/sigma_chatroom/ui/ |effort: 4h |owner: ui-ux-engineer+implementation-engineer
SQ[14]: Streamlit streaming render — token typewriter, st.status() tool-badge, turn separator |estimable:yes |files: src/sigma_chatroom/ui/render.py |effort: 4h |owner: ui-ux-engineer+implementation-engineer
SQ[15]: sigma-mem tool wiring complete + metrics panel |estimable:yes |files: src/sigma_chatroom/memory.py (complete), src/sigma_chatroom/ui/metrics.py |effort: 4h |owner: implementation-engineer
SQ[16]: M3 integration — 3-model autonomous session test with explicit assertion set |estimable:yes |assertions required: (1) ToolCallRecord.invoked=True for ≥1 call; (2) ToolCallRecord.result non-empty; (3) preamble_variant field present in JSONL header; (4) @next: detection queryable from metrics panel; (5) run_autonomous() called (not run_round()-in-loop); (6) 3+ turns without exception; (7) sigma-mem subprocess: mock-stub for CI (CHATROOM_MOCK_SIGMA_MEM=1), live subprocess for CHATROOM_LIVE_TESTS=1 |files: tests/test_m3_integration.py |effort: 3h |owner: implementation-engineer
SQ[17]: roster config — 3-provider ProviderSpec config (Anthropic + 1-cloud + 1-Ollama-local) + env-key discovery for those 3 + unavailable-model UX |estimable:yes |notes: DA[#4] scoped from 13 to 3 for v1; full 13-provider roster → M4; ProviderSpec.tool_use_reliability=unknown default ensures safe extension |files: src/sigma_chatroom/config/providers.yaml, src/sigma_chatroom/config/loader.py |effort: 2h |owner: implementation-engineer

parallel-clusters: A=[SQ[3],SQ[4],SQ[5],SQ[6]] (providers, independent files) | B1=[SQ[8],SQ[9],SQ[10]] parallel | SQ[7] parallel with B1 (¬dependent on B1 items) | SQ[11] SEQUENTIAL after SQ[7]+SQ[8] | gate=SQ[2] complete before A+B1 | merge=SQ[12]+SQ[12b] (requires A+SQ[11]) | C=[SQ[13],SQ[14]] starts after SQ[2] with stubs

## pre-mortem

PM[1]: Gemini adapter breaks after SDK minor update |probability: 35% |early-warning: CI fixture test failures after pip update |mitigation: pin google-genai version; fixture-test ¬live-API-test; version bump = explicit decision
PM[2]: Small-model tool reliability causes session deadlocks |probability: 40% |early-warning: TurnEngine timeout counter incrementing; JSONL shows tool_call start ¬tool_result |mitigation: tool_use_reliability taxonomy enforced; "unreliable" → tools=None; tool-exec loop max_iterations=3 hard cap; TurnEndEvent always emitted
PM[3]: ConversationHistory bloat causes incoherence at turn 15+ |probability: 50% |early-warning: input_tokens in TurnEndEvent approaching context_window; output becomes repetitive |mitigation: per-model context budget + truncation strategy; calibrate token estimate against reported input_tokens first 5 turns
PM[4]: Streamlit session state corruption causes duplicate turns |probability: 30% |early-warning: JSONL shows duplicate turn_ids |mitigation: all mutable state in st.session_state; orchestrator created once at session start
PM[5]: Async event loop interference between sequential turns |probability: 25% |early-warning: "Event loop closed" RuntimeError; turns fail after first model |mitigation: queue-based sync bridge per turn (not asyncio.run()); VIABILITY experiment tests this directly

## files

| File | Action | Description |
|------|--------|-------------|
| chatroom/types.py | CREATE | CanonicalMessage, ChatEvent union, ToolDefinition, ToolResult, ProviderSpec |
| chatroom/providers/__init__.py | CREATE | ProviderProtocol ABC |
| chatroom/providers/anthropic_provider.py | CREATE | Anthropic streaming + tool_use content blocks |
| chatroom/providers/openai_provider.py | CREATE | OpenAI streaming + tool_calls delta reconstruction |
| chatroom/providers/gemini_provider.py | CREATE | Gemini streaming + function_call/function_response parts |
| chatroom/providers/ollama_provider.py | CREATE | Ollama native /api/chat streaming + tool_calls |
| chatroom/engine/turn_engine.py | CREATE | TurnEngine: tool-exec loop, ToolCallRecord |
| chatroom/engine/history.py | CREATE | ConversationHistory + truncation strategy |
| chatroom/engine/orchestrator.py | CREATE | ChatOrchestrator + round management |
| chatroom/engine/yield_policy.py | CREATE | YieldNextPolicy (roster ordering) |
| chatroom/tools/registry.py | CREATE | ToolRegistry |
| chatroom/tools/sigma_mem.py | CREATE | sigma_mem_recall MCP stdio client |
| chatroom/persistence/session_writer.py | CREATE | JSONL writer + optional raw sidecar |
| chatroom/config/providers.yaml | CREATE | 13-provider ProviderSpec roster |
| chatroom/config/loader.py | CREATE | env-key discovery, model availability check, unavailable-model UX |
| chatroom/app.py | CREATE | Streamlit entry point |
| chatroom/ui/render.py | CREATE | ChatEvent → Streamlit rendering (typewriter + tool bubble) |
| chatroom/ui/metrics.py | CREATE | live ToolCallRecord panel |
| experiments/viability.py | CREATE | M0 viability experiment |
| tests/test_adapters.py | CREATE | round-trip adapter fixture tests |
| tests/test_m1_integration.py | CREATE | headless 2-model session integration test |
| tests/test_m3_integration.py | CREATE | 3-model autonomous session integration test |
| pyproject.toml | CREATE | anthropic, openai, google-genai, ollama, mcp, streamlit deps |

## convergence

tech-architect: ✓ plan-r1 complete |VIABILITY[go-conditional,P=0.85]: Streamlit async supported+Ollama native API required |ADR:#8(providers,tool-exec-location,event-shape,message-mapping,concurrency,ollama-native,persistence,mcp-client) |IC:#7(Provider,TurnEngine,History,ToolRegistry,ProviderSpec,SessionWriter,Orchestrator) |SQ:#17(M0-gate+M1[10]+M2[2]+M3[3]+parallel-clusters-A/B/C) |PM:#5(SDK-drift,small-model-deadlock,history-bloat,session-state,event-loop) |key-risks: Gemini adapter round-trip(test with fixture), Ollama tool reliability(taxonomy+cap), M1 effort at optimistic end of reference class(DA should challenge) |→ ready-for-build-track-challenge+DA-challenge |round-2-compare ready on lead signal
tech-architect: ◌ round-2 compare complete |DIV:#10 analyzed |concede:#7(canonical-shape,taxonomy,CLI,60%-budget,policy-seq,src-layout,memory.py-naming) |defend:#1(Ollama-native-api — new evidence not in draft) |compromise:#1(StreamEvent flat+extended ¬full-union) |align:#1(Ollama-local/cloud same approach) |BR:#7 Brad-points addressed |key-ADR-revisions: ADR[3]StreamEvent-flat, ADR[4]OpenAI-canonical, ADR[7]raw-capture-default-on-unknown/nominal, CAL[M1]point=5d-up-from-4d |→ ready-for-challenge-round |DA-focus: Ollama-native defend(T1-evidence), M1-estimate(§2b gap), Gemini-adapter-T3

tech-architect: ◌ challenge-r1 responses

### DA responses

DA[#2]: concede — ADR[9] M0-fallback decision-tree locked as follows:
BRANCH(a): async-bridge PASS + render<1000ms@80turns PASS + fragment-no-race PASS + Ollama-tool-chunk-shape PASS → M1 proceeds as planned. P(go)=0.85.
BRANCH(b): render@80-turns FAIL (>1000ms) only → DS[1] revised: windowed render (last N turns only) OR 100-turn hard cap with archive. Instrument remains Streamlit. P(instrument-still-viable)=0.90 with windowing.
BRANCH(c): fragment-race FAIL only → sequential-only streaming (no fragment isolation). Transcript renders synchronously per turn. Loses concurrent metrics refresh but preserves all data capture. P(still-viable)=0.85.
BRANCH(d): async-bridge FAIL (all bridge strategies fail, including queue-based) → headless JSONL instrument + CLI runner. Q1 (tool-use authenticity) and Q2 (yield-next spontaneity per strategist) answerable from JSONL without UI. Streamlit deferred to M2 with known fix. ¬abandon project, ¬"user decides alone." P(JSONL-still-answers-research-questions)=0.95.
BRANCH(d-total): all four criteria FAIL simultaneously → P<0.20, escalate to user with specific evidence before making instrument-shape decision. ¬unilateral pivot.
ADR[9] added to architecture-decisions section. |source: agent-inference (branch structure) + DA[#2] forcing |T3-unverified (no precedent for this exact 4-branch triage) | §2e outcome 2: preconditions enumerated, fallbacks defined, total-failure branch escalates.

DA[#3]: compromise — IC[7] ChatOrchestrator v1 responsibilities justified, NOT collapsed, with concrete scope boundary.
V1 concrete responsibilities that justify the abstraction: (1) owns turn-ordering via TurnPolicy — cli.py cannot own this without becoming orchestrator; (2) owns the round loop (run_round() → run_autonomous()) — this loop is the primary difference between a CLI one-shot and a session; (3) owns SessionWriter lifecycle (open/close on session boundaries); (4) owns the asyncio event loop for cross-provider sequencing in Streamlit context. DA is correct that if these four responsibilities dissolved into cli.py, cli.py becomes the orchestrator under a different name. The abstraction is NOT speculative — it maps to four distinct v1 responsibilities none of which cli.py should own.
That said: I concede DA's framing concern. "ChatOrchestrator" is a grand name for what is essentially a turn-loop with a policy and a writer. Rename to TurnLoop or SessionRunner to reduce abstraction signal. IC[7] spec stays, name changes.
IC[7] revised: rename ChatOrchestrator → SessionRunner. Concrete v1 methods: run_round() → AsyncIterator[StreamEvent], run_autonomous(max_rounds) → AsyncIterator[StreamEvent]. Holds: TurnPolicy, SessionWriter, list[Provider]. ¬adds any speculative v2 hooks. |source: agent-inference |§4c outcome 2: justified with v1-specific evidence, name revised to reduce abstraction signal.

DA[#5]: concede — ADR[6] CQoT-6 falsifiability revised.
Original reversal condition was "IF Ollama native /api/chat also drops tool_calls THEN disable tool-use for Ollama." DA is correct this is a degradation path ¬a reversal — it doesn't change the endpoint choice, just disables tool-use.
Genuine reversal condition: IF Ollama merges a fix to /v1/chat/completions streaming+tool_calls (track: ollama/ollama#12557 closure with test evidence) AND the ollama Python library ≥X.Y exposes a streaming OpenAI-compat path that passes the VIABILITY experiment tool-call chunk-shape test THEN reconsider OllamaProvider endpoint choice (switching to OpenAI-compat would unify Ollama local+cloud+API-key handling under one adapter).
This is reachable: the issue is open, the maintainers have acknowledged it, and the fix would be a concrete version bump with testable behavior. Changelog monitoring is the trigger. ADR[6] updated with this reversal condition. |source: independent-research (ollama#12557 status) |T1-verified

DA[#8]: concede — ADR[5] steelman for concurrent streaming added.
Concurrent parallel streaming precedent: Poe (Quora) renders multiple model responses simultaneously in separate columns. Architecture: each model streams independently, columns update in real-time, no turn-sequencing. Valid alternative for a multi-model "comparison" instrument.
Rejection rationale for THIS instrument: (a) research goal is CONVERSATION not comparison — models must read each other's output to respond meaningfully; parallel streaming means no model sees any prior turn; (b) Streamlit's column layout under concurrent async writes from multiple threads is fragile (documented in Streamlit issues); (c) turn-ordering is an experimental variable (YieldNextPolicy) — parallel streaming eliminates the variable entirely.
ADR[5] updated: steelman noted ("Poe-style parallel columns") + rejection rationale explicit. If research goal shifts to "comparison" instrument ¬"conversation" instrument, parallel streaming becomes the right choice. |source: agent-inference + independent-research (Poe architecture known pattern) |§2e outcome 2: strongest alternative stated, rejection conditions specific.

DA[#9]: concede — SQ[12] cross-SDK turn-chain fixture explicitly added.
DA is correct that M1 integration test underspecified for the actual research instrument's core requirement: models from DIFFERENT SDK families reading each other's output in sequence. SQ[12] revised: headless session MUST exercise Anthropic→Ollama (M1a) AND, after M1c, a 4-SDK round (Anthropic→OpenAI→Gemini→Ollama) where each model reads the prior turn's content as part of its message history. SQ[12b] added: per-SDK adapter round-trip fixture (see BC[impl]6 + BC[quality]2 below).
Cross-SDK scenario to test: Turn N = Anthropic invokes tool. Turn N+1 = OpenAI reads history containing Anthropic tool_call + tool_result in canonical form, translated to OpenAI role=tool shape. Verify: OpenAI sees coherent history ¬garbled content blocks. This is the IC[3].to_provider_messages(provider_id) contract under load.

DA[#10]: concede — CAL[M1] 6d accepted.
3-way corroboration (Brad + BC[11] + DA) from independent sources is sufficient to move the point estimate. CAL[M1] revised: point=6d, 80%=[5d,9d], 90%=[4d,12d]. Total-v1: point=12d, 80%=[10d,16d], 90%=[8d,20d]. M1 fraction at point: 6/12=50%, within Brad's 60-70% at upper bound. Communicating to build-track: plan as 14-18d not 10-11d. |source: §2b outcome 1 (revised from gap to revision via corroboration)

### BC responses

BC[impl#1]: concede — Anthropic content-block buffer reassembly +1h.
Content-block buffer reassembly (accumulating streaming text_delta + input_json_delta chunks into complete tool_use block before yielding tool_call StreamEvent) is genuinely non-trivial. The SDK accumulates automatically in MessageStream but raw streaming requires manual buffer. SQ[3] revised to 5h. |source: independent-research (Anthropic SDK streaming docs, T1)

BC[impl#2]: concede — OpenAI parallel multi-tool_call execution semantics added to ADR.
OpenAI can return multiple tool_calls in a single assistant message. Draft's TurnEngine handles them serially (execute tool A → get result → execute tool B → get result → re-invoke). Policy must be explicit: SERIAL (safe, predictable, guaranteed ordering) vs PARALLEL (faster, risks race condition if tools share state, but sigma_mem_recall is read-only so safe). Decision: SERIAL execution for v1 (simpler, safe for read-only sigma_mem_recall, avoids async coordination complexity). IF a future tool has side-effects THEN reconsider. ADR update: ADR[3]/StreamEvent + TurnEngine spec updated — multi-tool_call: serial execution, each tool yields ToolCallEvent then ToolResultEvent before next tool begins. IC[2] updated with this specification.

BC[impl#5]: concede — TurnEngine max_iterations clarified.
"max_iterations=3" means: 3 complete tool-call/tool-result CYCLES (not 3 tool_calls total, not 3 re-invocations). After 3 cycles, TurnEngine sends one final provider.stream() call with tool_result history appended but tools=None (forces completion without further tool invocation). This gives the model a chance to produce a final summary response rather than hard-truncating. StreamEvent(kind="turn_end", stop_reason="max_tool_calls") emitted regardless. IC[2] updated with exact semantics.

BC[impl#6]: concede — ConversationHistory truncation invariant CRITICAL.
BC is correct: truncating a tool_call message without its paired tool_result (or vice versa) produces API 400 errors on Anthropic (content block validation) and OpenAI (orphaned tool_call_id). This is a hard correctness requirement, not a nice-to-have. IC[3] updated: truncate_to_budget() MUST maintain tool_call/tool_result pair integrity. Invariant: if any message in a pair is retained, both must be retained. Truncation algorithm: walk from oldest→newest, skip pairs that don't fit budget, never split a pair. Test: SQ[12b] includes fixture with tool_call at message N and tool_result at N+1 — truncation must keep or drop BOTH. |source: T1-verified (Anthropic + OpenAI docs per BC[impl#6])

BC[impl#7]: concede — StreamEvent(kind="turn_end") MUST carry usage fields.
ADR[3] updated: StreamEvent when kind="turn_end" carries: input_tokens: int, output_tokens: int, stop_reason: str, ttft_ms: int | None, total_ms: int. Per-provider extraction: Anthropic message_delta.usage, OpenAI final chunk with include_usage=True, Gemini usage_metadata, Ollama usage field on final chunk. Fallback: 0 if missing (¬None — keeps downstream metrics code simple). IC[2] TurnEngine must extract and emit these fields. |source: BC[impl#7] + independent-research (per-SDK usage extraction patterns, T2)

BC[impl#8]: concede — MCP subprocess lifecycle specified.
Decision: ONCE-PER-SESSION. sigma-mem MCP subprocess starts at session init, stays alive for session duration, terminates on SessionWriter.close(). Rationale: subprocess startup cost (~500ms) amortized over session; per-call subprocess would add latency to every tool invocation. Crash/restart: MemoryHelper wraps subprocess with asyncio.create_subprocess_exec, monitors process liveness before each call; if process dead, attempts single restart; if restart fails, returns error string in tool_result (observable). No supervisor daemon — v1 local instrument, single user. ADR[8] updated. SQ[9] updated: includes subprocess lifecycle management in sigma_mem.py scope.

BC[impl#12]: concede — SQ[11] SessionRunner cannot parallelize with SQ[7,8].
BC is correct: SessionRunner depends on TurnEngine (SQ[7]) and ConversationHistory (SQ[8]). Parallel cluster B revised:
- Parallel sub-cluster B1: SQ[8](ConversationHistory) + SQ[9](ToolRegistry+sigma_mem) + SQ[10](SessionWriter) — independent files
- Sequential after B1: SQ[7](TurnEngine) — depends on SQ[8]
- Sequential after SQ[7]: SQ[11](SessionRunner) — depends on SQ[7,8]
Cluster A (providers SQ[3-6]) remains parallel. Gate: SQ[2](types.py) before all. Merge: SQ[12] after A + SQ[11] complete.

BC[quality#2]: concede — Provider mock spec must emit AsyncIterator[StreamEvent].
Mock that returns CompleteResult bypasses the tool-exec loop entirely — tests pass but the integration being tested (TurnEngine consuming provider stream events and executing tools) is never exercised. Mock contract: MockProvider.stream() yields a sequence of StreamEvent instances including at least one kind="tool_call" event followed by kind="stop". This forces TurnEngine's tool-exec loop to actually run against the mock. SQ[12] fixture spec updated: echo_tool + MockProvider that yields realistic StreamEvent sequence including tool_call event. |source: BC[quality#2] + §4d test integrity principle

BC[quality#3]: concede — Gemini canonical form for function_response-in-user-content specified.
Gemini's function_response is a Part embedded in a user-role content turn, not a separate role. Canonical representation in OpenAI-shaped Message: role="tool", content=function_response_json_string, tool_call_id=function_call_id. The GeminiAdapter.to_sdk_messages() reconstructs this as a Content(role="user", parts=[Part.from_function_response(name, response)]) when it sees role="tool" messages. The key: Gemini has no role="tool" natively — adapter maps it to role="user" with function_response Part. Test fixture: 2-turn canonical history (assistant with function_call + tool with function_response) → GeminiAdapter → SDK messages → assert correct Part type. Documented in message_mapping.py before adapter fixtures are written. |source: independent-research (Google GenAI SDK docs, T1-verified)

### Cross-track coordination responses

M0-scope-4-criteria: CONFIRM — SQ[1] M0 expanded to all 4 criteria: (a) async-bridge PASS/FAIL, (b) render@80-turns <1000ms PASS/FAIL, (c) fragment-race PASS/FAIL, (d) Ollama streaming tool_call chunk shape PASS/FAIL. Budget: SQ[1] revised to 2-4h per ui-ux-engineer estimate. All 4 required before M1 proceeds. ADR[9] decision-tree governs each failure branch (written above in DA[#2] response). Gate: any FAIL triggers named branch from ADR[9]. SQ[1] updated.

BC-ui[DS[4]] st.status() compatibility: CONFIRM compatible. st.status() is a context manager — opened when ToolCallEvent emitted (kind="tool_call"), closed when ToolResultEvent emitted (kind="tool_result"). This maps cleanly to the queue-bridge model: ToolCallEvent comes through the sync queue → UI opens st.status("Calling sigma_mem_recall…", expanded=True) → continues pulling from queue → ToolResultEvent arrives → st.status context closed (shows result). The event ordering guarantee in the queue-bridge (ToolCallEvent strictly precedes ToolResultEvent for the same call_id) is the invariant that makes this work. TurnEngine already ensures this ordering (tool-exec loop: yield tool_call event → execute → yield tool_result event → continue). IC[2] note: ToolCallEvent and ToolResultEvent for the same call_id MUST be emitted in order with no interleaving from other tool calls (serial execution from BC[impl#2] guarantees this). Compatible.

### Summary
DA: DA[#2]=concede(ADR[9] locked 4-branch), DA[#3]=compromise(IC[7]→SessionRunner justified+renamed), DA[#5]=concede(ADR[6] reversal-condition revised to ollama#12557-fix), DA[#8]=concede(steelman added), DA[#9]=concede(SQ[12]+SQ[12b] fixtures explicit), DA[#10]=concede(CAL[M1]=6d)
BC: BC[impl#1]=concede(SQ[3]=5h), BC[impl#2]=concede(serial multi-tool in ADR+IC[2]), BC[impl#5]=concede(3-cycle clarified in IC[2]), BC[impl#6]=concede(pairing-invariant in IC[3] CRITICAL), BC[impl#7]=concede(turn_end usage fields in ADR[3]+IC[2]), BC[impl#8]=concede(once-per-session in ADR[8]+SQ[9]), BC[impl#11]=concede(CAL[M1]=6d), BC[impl#12]=concede(cluster-B resequenced), BC[quality#2]=concede(mock=AsyncIterator[StreamEvent] contract), BC[quality#3]=concede(Gemini function_response canonical specified)
concede:#15 defend:#0 compromise:#1
revisions-needed: ADR[3,5,6,7,8,9], IC[2,3,7→SessionRunner], SQ[1,3,7,9,11,12,12b], CAL[M1]

product-designer: ✓ plan-r2 |DIV:#5(rerun-thrash-defend,tool-badge-defend-concede-mechanism,name-badge-concede-framing,preamble-default-defend-neutral,viability-P-maintain-NOT-papering-over)|BR:#4(streamlit-async-extend-prototype-scope,preamble-variant-UX-full-agree,raw-capture-full-agree,memory-turn-concede-already-correct)|REVISED:DS[1]-windowed-render=M4|DS[3]-default=neutral|DS[4]-mechanism=proposed-F6-gates|VIABILITY[H11]:P=0.65-maintained-vs-tech-architect-P=0.87(different-questions-not-false-consensus)|→ ready-for-challenge-round

### product-designer — challenge-round-1 responses

DA[#1]: CONCEDE — adopt expanded M0 scope (4 criteria). DO NOT average P values.
Evidence: DA correctly amplifies R2 position. The 4-criterion M0 (async-bridge + fragment-race + render@80-turns<1000ms + st.status-in-bridge) is exactly the resolution mechanism I proposed in R2 DIV[5]. Adopting path A: expanded M0 AND it passes → both P values converge.
SPECIFIC POSITION: Lock plan with DISTINCT P values preserved. VIABILITY[H11] has two named probabilities: P(async-bridge-plumbing)=0.87 [tech-architect scope] and P(complete-UI-at-80-turns)=0.65 [product-designer scope]. M0 expanded to 4 criteria is the empirical gate. If criterion (c) render@80-turns<1000ms PASSES → P(complete-UI) upgrades to >=0.80 and both converge. If (c) FAILS → P=0.65 confirmed, fallback triggers per ADR[9] branch (b). DA direction (do NOT average) adopted. |source:DA[#1]-A-engagement-grade|

DA[#6]: CONCEDE — palette requires per-hue L adjustment before lock.
Evidence: ui-ux-engineer math-verified hue 55° (yellow) at L=45% gives 2.4:1 on white — fails WCAG 4.5:1 AND 3:1. My T3 source flag in DS[2] was correct; the ungated contrast math was the gap. Approx 3 of 13 warm hues fail.
SPECIFIC REVISION DS[2]: Warm hues (approx 28°-110°) raised to L=58-65% to achieve 4.5:1 on white. Cool/dark hues (138°-331°) remain at L=45%. Palette is heterogeneous in lightness — acceptable for research instrument. Add SQ[D8a]: validate all 13 final L values with WCAG contrast checking tool (10min) before plan lock. |source:BC-ui[DS[2]]:T1-math-verified-by-ui-ux-engineer|

BC-ui[DS[2] palette warm-hue failure]: CONCEDE — full adoption.
As above under DA[#6]. Math-verified failure is definitive. Per-hue L adjustment adopted. |source:T1-verified|

BC-ui[DS[4] mechanism -> st.status()]: CONCEDE with enthusiasm.
Evidence: st.status() in Streamlit >=1.28 is purpose-built for the exact 3-state pattern I specified (running=amber-spinner, complete=green-check, error=red-x). Eliminates T3-novelty risk entirely. The 3-state SPEC (INVOKED/SUCCEEDED/ERRORED) is UNCHANGED; only mechanism changes. Strict improvement: same design, lower risk, T3 flag removed.
DS[4] REVISED: mechanism = st.status() (Streamlit >=1.28 native). Minimum version constraint added to pyproject.toml. Three-state spec unchanged. T3-novel flag REMOVED. |source:BC-ui[DS[4]]:T1-via-ui-ux-engineer|

BC-ui[avatar SVG base64]: CONCEDE — st.chat_message avatar accepts emoji/URL only.
Evidence: documented Streamlit API constraint. My DS[2] "colored circle + 2-char initials" requires base64-encoded SVG data-URI passed as avatar URL. Approach: generate SVG circle with hue + initials → base64 encode → data-URI. Small utility (~20 LOC).
SPECIFIC REVISION: Add SQ[F5a] svg_avatar_util.py — generates data-URI avatars from (hue, initials) pair, called by SpeakerColorMap. ~20 LOC, add to controls.py module. |source:BC-ui[avatar]:T1-via-ui-ux-engineer|

BC-ui[M0 expansion to 4 criteria]: CONCEDE — adopt fully.
4-criterion M0 fits SQ[F6] 2-4h budget and resolves DA[#1]. I adopt 1000ms (not my original 300ms) as the render@80-turns pass threshold — more realistic for chat_message renders.
SQ[F6] REVISED: 4-criteria prototype — (a) async bridge: token+tool event visible in Streamlit, (b) fragment race: event-driven + timer-driven rerun on same fragment do not drop turns or double-update, (c) render@80-turns<1000ms, (d) st.status() displays in bridge flow. Pass = all 4. Fail-branch per ADR[9]. |source:BC-ui[M0]:ui-ux-engineer-convergence|

ADR[9] M0-FALLBACK BRANCH (b) VERDICT — render@80-turns FAIL:
DESIGN VERDICT: windowed render (last 30 turns), NOT immediate Textual TUI fallback.
Rationale: TUI fallback is too drastic for a render-cost finding. The instrument needs CURRENT turn and last N turns visible, not all 80 simultaneously. Windowed render preserves the research workflow while eliminating O(n) cost. JSONL session file remains the authoritative full-transcript record.

Two-stage fallback:
- render@80-turns FAILS (>1000ms) → implement windowed render (last 30 turns) as DS[1] M2 architecture → re-test at 80 turns windowed → if STILL >1000ms (render of 30-turn window fails) → THEN Textual TUI fallback
- Branch (a) async-bridge FAILS → Textual TUI immediately (no bridge = cannot build in Streamlit)
- Branch (c) fragment-race produces dropped turns → disable event-driven trigger, timer-only run_every=0.5s, acknowledged 0-500ms staleness
- Branch (d) st.status() not renderable in bridge flow → revert to st.expander 3-state pattern (T3-novel, but no evidence of technical impossibility)
|source:agent-inference — design judgment|

concede:4 defend:0 compromise:0 |DS-revised:DS[2]-per-hue-L-adj,DS[4]-st.status()-T3-removed,DS[1]-staged-fallback-verdict |SQ-added:SQ[D8a]-contrast-tool-validation,SQ[F5a]-svg-avatar-util,SQ[F6]-4-criteria |M0-branch-b: windowed-render-30-turns-first-not-immediate-TUI

product-strategist: ✓ plan-r1 strategy |Q-pinned:#2(Q1:chatroom-context-tool-use-vs-BFCL-baseline,Q2:yield-next-spontaneity-preamble-variant-controlled) |Q-secondary:#3(query-coherence+self-reference+convergence-all-data-logged-M3-analysis-M4) |metrics:essential=#8(all-zero-cost-schema-fields)+luxury=#6(all-deferred-reversible) |milestone-seq:M0(kill-switch)→M1a→M1b(parallel-clusters)→M1c(kill-switch)→M2→M3 |SQ-PS:#3 |PM-PS:#5(Q1-null,Project3-mismatch,async-tar-pit,noise-bimodal,stability) |VIABILITY[H11]:conditional-go(M0-bridge-prototype+Ollama-native-API) |key-flags:M1-effort-at-optimistic-end(§2b-gap-flagged-for-DA),H5-60-70%-unverified(prompt-claim),Q1-framing-revised-to-chatroom-delta-vs-BFCL(§2g-outcome-1) |XVERIFY-SKIP(non-security,advisory,neutral) |→ ready-for-build-track-challenge+DA-challenge+round-2-compare-on-lead-signal
product-strategist: ◌ round-2-compare complete |DIV:#6(defend:#3,concede:#2,compromise:#1) |BR-PS:#3(research-question-first:concede-fully,preamble-study-variable:concede-strengthen,M1-60-70%:partial-concede-upgraded-to-plausible) |key-shifts:M1c-naming-error-corrected+proposed-canonical-M0→M1a→M1b→M1c→M1d→M2→M3,essential-metrics-expanded(TTFT+stop_reason+yield-next-override),preamble-three-variant-adopted,H5-60-70%-upgraded-from-unverified-to-plausible-80th-percentile |OQ[1]-resolution:canonical-naming-proposed-in-DIV[3] |OQ[2]-resolution:§2b-gap-remains-DA-scrutiny-warranted-but-Brad-directionally-corroborated |flag-for-user:Q1-vs-candidate-a-pinning-is-user-priority-call |→ ready-for-challenge-round
product-strategist: ✓ responses-r1 |DA:#3 |BC:#2 |concede:#4 defend:#1 compromise:#0 |milestone-naming-final:CONFIRMED(M0(4-criteria)→M1a→M1b→M1c→M1d→M2→M3) |CAL[M1]-final:6d |CAL[total-v1]-final:11d-point/16d-80th |SQ[17]-scope:3-provider(not-13) |OQ[4]:does-not-block-plan-lock |ADR[9]-fallback:headless-JSONL-confirmed |→ ready-for-r2-re-evaluation

DA[#1 HIGH]: CONCEDE+CONFIRM |M0-expanded-4-criteria:(1)async-bridge (2)fragment-race (3)render@80-turns (4)Ollama-native-tool_call-shape |M0=3-4h gate not 2h throwaway |per-criterion-fallback:(1-fail)→headless-JSONL-v1 (3-fail-only)→partial-rerender-M2-scope (4-fail-only)→Ollama-text-only-v1-Q1-still-answerable (all-fail)→branch-d-headless-JSONL |plan-locks-P=0.65-named-uncertainty |P-resolves-0.85-after-M0-empirical-pass |canonical-naming-absorbs-expanded-M0 |source:[cross-agent]

DA[#4 MED]: CONCEDE-scope-reduce |SQ[17]-revised:3-provider-ProviderSpec-config(Anthropic+1-cloud+1-Ollama-local)+env-key-discovery-3-vars |full-13-provider-roster→M4 |ProviderSpec.tool_use_reliability=unknown-default-ensures-safe-extension |constraint-preserved:≥1-cloud-reliable-tool-use-model-per-session(PM-PS[1]) |source:[build-directives §4c+scope-boundary]

DA[#10 LOW]: CONCEDE-6d-accepted |CAL[M1-revised]:point=6d|80%=[5d,9d]|90%=[4d,12d] |CAL[M2-revised]:point=2d|80%=[1.5d,3.5d] |CAL[M3-revised]:point=2d|80%=[1.5d,3d] |CAL[total-v1-revised]:point=11d|80%=[9d,16d]|90%=[7d,20d] |M1-fraction:6/11=55%-point,60%-80th-upper—within-Brad-range |§2b-gap-resolved |source:[cross-agent—BC-impl]

BC[impl#11]: CONCEDE—addressed-in-DA[#10] |6d-accepted|CAL[]-locked|total-v1=11d-point/16d-80th

BC[impl#12]: CONCEDE—accept-correction |SQ[11]-ChatOrchestrator-sequential-after-SQ[7,8] |B-parallel=[SQ[8,9,10]]+SQ[7]→SQ[11]-sequential-merge |wall-clock-absorbed-in-CAL[M1-revised]=6d |structural-dep:IC[7]-constructor-takes-TurnEngine+ConversationHistory |source:[cross-agent—BC-impl+tech-architect-IC[]]

CROSS-TRACK: M0-4-criteria-CONFIRMED |ADR[9]-branch-d-CONFIRMED(headless-JSONL-answers-Q1/Q2) |OQ[4]-DOES-NOT-BLOCK(instrument-collects-both-datasets-at-zero-cost,user-decides-priority-at-session)

### devils-advocate

devils-advocate: ◌ plan-r1 challenge complete |DA:#10 challenges |severity:{HIGH:#3,MED:#5,LOW:#2} |exit-gate:FAIL |full-findings: ~/.claude/teams/sigma-review/shared/builds/2026-04-16-multi-model-chatroom/da-r1-challenge.md

summary: prompt-audit H-confirm-ratio=10/0(unanimous-confirmation-pattern,HIGH prompt-laundering-risk), echo-count=3/11(H1/H2/H3 near-verbatim), methodology=MIXED-investigative-leaning |engagement: tech-architect=B+ product-designer=A- product-strategist=B+ implementation-engineer=A- code-quality-analyst=A- |build-track BC:#12 triangulates with DA on BC[6]-pairing-invariant(↔DA[#7]), BC[9]-fragment-race(↔DA[#1]), BC[11]-CAL-6d(↔DA[#10] 3-way w/Brad), BC[12]-SQ[11]-sequencing(↔DA[#3])

challenges (target+severity+headline):
- DA[#1]-HIGH: VIABILITY P=0.65-vs-0.87 unresolved (DIV[5] amplification per task §rule) — expand SQ[1] M0 to (a)+(b)+(c)+(d=BC[4]) OR lock with P=0.65
- DA[#2]-HIGH: ADR[9] M0-fallback decision-tree missing (lead-flagged step-17) — lock 4-branch tree, replace "user decides" punt
- DA[#3]-MED: IC[7] ChatOrchestrator premature abstraction (§4c) — justify-with-v1-responsibilities OR collapse to cli.py coordinator; BC[12] sequencing confirms
- DA[#4]-MED: SQ[17] 13-provider YAML at v1 = gold-plating (§4c) — ship only empirically-tested providers
- DA[#5]-MED: ADR[6] falsifiability-reversal-condition-unreachable-for-natural-failure-mode (CQoT-6) — add ollama-python changelog re-evaluate trigger
- DA[#6]-MED: DS[2] WCAG-4.5:1-contrast-math UNGATED T3 (§2d+) — run contrast checker pre-lock (10min) OR revise palette
- DA[#7]-HIGH: SQ[12] M1 integration test underspecified (§4d) — explicit fixtures: ADR[4] merge-gate 3-turn-mid-tool-call, Ollama-declined null-case, session_state, BC[6] pairing, BC[5] multi-tool; add SQ[12b] 4-SDK adapter round-trip before M1d
- DA[#8]-LOW: ADR[5] concurrent-streaming steelman weak vs Poe precedent (CQoT-7) — add note "sequential is Streamlit-constrained, not carrying over to fallbacks"
- DA[#9]-MED: IC[2]↔IC[3]↔IC[7] cross-SDK turn chain untested (§4b) — expand SQ[12b] with Gemini-tool-call-on-N Anthropic-reads-on-N+1 fixture
- DA[#10]-LOW: CAL[M1] 5d→6d (§2b 3-way corroborated: Brad+BC[11]+DA) — accept BC[11]; communicate ship as 14-18d ¬10-11d

exit-gate-verdict: FAIL |fails(2,3,5,6,7): DIV[5]-unresolved+M0-fallback-missing | R2-consensus-from-draft-absorbed-without-adversarial-stress | H-confirm-ratio-10/0 | ADR[6]-reversal-unreachable-for-natural-failure | ADR[5]-Poe-steelman-absent

conditions-for-PASS (5, per T[exit-gate-condition-setting-as-leverage]):
1. DIV[5] resolved: SQ[1] M0 expanded to (a)+(b)+(c)+(d) OR plan locks with P=0.65 + named uncertainty
2. ADR[9] M0-fallback 4-branch tree locked
3. SQ[12] fixtures explicitly named (consolidates DA[#7]+DA[#9]+BC[5]+BC[6])
4. DS[2] contrast math validated pre-lock OR palette revised
5. IC[7] justified-concretely OR collapsed-to-coordinator

not-blocking-for-PASS: DA[#4], DA[#5], DA[#8], DA[#10] (recommended but acceptable if defended)

both-right-is-fine (task §rule amplification): product-designer P=0.65 maintenance IS stronger analysis than tech-architect P=0.87 |two answer DIFFERENT questions (narrow plumbing vs full UI at 80+ turns) |designer named it + proposed specific falsifiable test-expansion + did not collapse |A-grade DA-aligned behavior |plan-lock must preserve distinct P values with named conditions ¬average

BELIEF[plan-r1 devils-advocate]:
- ADR[6] Ollama-native: P=0.90 |ADR[5] sequential: P=0.80 |ADR[4] OpenAI-canonical: P=0.80
- IC[7] abstraction-at-v1: P=0.45 (premature)
- VIABILITY[H11] UI-complete: P=0.65 ← LOAD-BEARING; VIABILITY async-bridge-only: P=0.85
- CAL[M1]=5d-point-hits: P=0.30 (3-way argues 6d) |CAL[M1]=6d-more-accurate: P=0.80
- SQ[12] catches-integration-risks: P=0.30
→ P(plan-ready) ≈ 0.55-0.65

recommendation: ANOTHER ROUND (¬Toulmin-needed; conditions mechanical) — IF all 5 conditions addressed in R2 → likely PASS → lock-plan

DA ¬terminate-post-r1 |WAIT for lead next-round-signal OR lock-plan-signal |AGENT-DEF: DA controls exit timing, 3-round-min 5-round-max

## belief-tracking

BELIEF[plan-r1] — code-quality-analyst test-coverage component:

test-coverage: 0.52 (WEAK — significant gaps in assertion spec, failure-case coverage, mock boundary) |
reasoning:
- SQ[12] behavior-vs-runs: LOW confidence (0.40) — description specifies what RUNS not what is ASSERTED; no failure cases; mock could bypass TurnEngine loop
- SQ[16] assertion-scope: MEDIUM (0.55) — preamble_variant assertion missing; 10-turn stability unspecified; sigma-mem subprocess isolation unclear
- Q1 ToolCallRecord-3-states: LOW (0.40) — no test exercises all three states; malformed_json detection logic untested; risk: always=False in CI
- Q2 yield-next: MEDIUM (0.60) — unit test for parser absent; pure function, trivially testable, just not specified
- Adapter round-trip: MEDIUM (0.65) — fixture strategy incomplete for streaming delta reconstruction (OpenAI+Ollama scoped gap)
- M0 pass-criteria: LOW-MEDIUM (0.50) — 1-criterion vs 3-criterion divergence between tech-architect and product-designer unresolved; blocks clean kill-switch
- mock-risk: HIGH — Provider mock shape unspecified; cooperative CompleteResult mock would bypass TurnEngine exec-loop in SQ[12]

assumption-conflicts: NONE between test strategy and ICs; IC[1] Protocol signature (stream()→AsyncIterator[ChatEvent]) is consistent with correct mock requirement

overall: plan test strategy covers structural verification but not behavioral verification; Q1/Q2 measurement validity untested at plan stage

BELIEF[plan-r1] — implementation-engineer builder-feasibility component:

builder-feasibility: 0.68 (CONDITIONAL) |

reasoning:
- SQ[2] types: HIGH confidence (0.90) — straightforward Python dataclasses, well-scoped
- SQ[3] AnthropicProvider: MEDIUM (0.75) — content-block reassembly is non-trivial but SDK is well-documented (T1)
- SQ[4] OpenAIProvider: MEDIUM-HIGH (0.80) — delta reconstruction is documented; parallel tool_call policy gap reduces confidence
- SQ[5] GeminiProvider: LOWER-MEDIUM (0.60) — asymmetric adapter, SDK instability history, estimate likely underestimated
- SQ[6] OllamaProvider: MEDIUM (0.70) — native API confirmed but streaming tool_call chunk shape empirically unverified
- SQ[7] TurnEngine: MEDIUM-HIGH (0.78) — well-understood pattern; multi-tool_call policy gap must be resolved
- SQ[8] ConversationHistory: MEDIUM (0.72) — pairing invariant is a real constraint not in current spec; adds complexity
- SQ[9] ToolRegistry+MCP: MEDIUM-HIGH (0.78) — subprocess lifecycle needs specification; otherwise buildable
- SQ[10] SessionWriter: HIGH (0.85) — JSONL append-only with schema_version is well-understood
- SQ[11] ChatOrchestrator: MEDIUM-HIGH (0.78) — sequential dependency on SQ[7,8] limits parallelism; otherwise buildable
- Integration tests: MEDIUM (0.70) — mock-only tests are false confidence; live-API fixtures required (project memory pattern)

highest-risk dependency chain: SQ[5] Gemini adapter failure → SQ[12] integration test failure → M1 milestone miss
second-risk: SQ[6] Ollama streaming tool_call chunk shape empirically wrong → OllamaProvider redesign required

P(BUILDABLE in 5d): 0.45 (tight — GeminiProvider and pairing invariant work likely push to 6d)
P(BUILDABLE in 6d): 0.70
P(BUILDABLE in 8d, 80% bound): 0.88 (consistent with CAL[M1-engine] 80% upper)

recommendation: CONDITIONAL ACCEPT — address BC[6] (pairing invariant), BC[5] (multi-tool_call policy), BC[4] (Ollama chunk shape verification in SQ[1]) before plan lock. Revise CAL[M1] point estimate to 6d.

BELIEF[plan-r1] — ui-ux-engineer builder-feasibility component:

builder-feasibility: 0.65 (CONDITIONAL — pre-M0-prototype) |

reasoning:
- DS[1] TranscriptFragment: CONDITIONAL (0.60) — fragment-isolation architecture correct; BLOCKER-A (fragment-race T2-not-T1) + BLOCKER-B (render@80-turns borderline) must resolve in expanded M0 before committing transcript.py
- DS[2] speaker-identity: MEDIUM (0.65) — avatar mechanism requires SVG-generator utility (not in spec, add to SQ[F5]); palette WCAG claim INCORRECT for warm hues (hue 28°-110° fail at S=75% L=45% — per-hue L adjustment OR text-color logic required before SQ[D1])
- DS[3] preamble-picker: HIGH (0.92) — all patterns T1-documented standard Streamlit; H9 observability signals implementable; no blockers
- DS[4] tool-call-badges: MEDIUM→HIGH (0.78 with mechanism revision) — st.status replaces st.expander (T1-documented, ¬T3-novel); BLOCKER-C (st.status-in-bridge-context) must resolve in expanded M0; 3-state spec concept sound
- DS[5] metrics-panel: MEDIUM (0.72) — event-driven flag race manageable with ordering guarantee; CPU cost of fragment rerun acceptable; metrics dataframe bounded at v1 scale; F6 benchmark needed
- DS[6] sidebar-controls: HIGH (0.88) — standard patterns; per-option-tooltip workaround required (st.caption approach); otherwise buildable
- DS[7] session-management: HIGH (0.90) — st.dataframe on_select pattern T1-documented; JSONL read at v1 scale no performance concern

highest-risk dependency chain: M0 prototype BLOCKER-B (render cost) → if >1000ms at 80 turns → windowed render required in v1 → SQ[F1] transcript.py must implement windowed render before M2 build
second-risk: DS[2] palette warm-hue WCAG failure → if not corrected before SQ[D1] → accessibility non-compliance ships with v1

P(UI BUILDABLE per current spec): 0.50 (current spec has palette error + avatar mechanism gap + M0 scope insufficient)
P(UI BUILDABLE post-conditions-met): 0.85 (if DS[2] palette revised + DS[4] mechanism→st.status + expanded M0 passes all 4 criteria)

builder-feasibility-score: 0.65 (pre-M0, averaging CONDITIONAL DS items) → expected 0.85+ (post-M0-pass + DS[2] revision)
H11-P-contribution: WITH-DESIGNER P=0.65. Architect P=0.87 answers narrower question (async bridge plumbing only). My P=0.65 answers full UI system integration at 80+ turns. P divergence is load-bearing — expanded M0 is resolution mechanism.

## gate-log

step-32 BLOCKED 26.4.16: exit-gate preconditions not met |reason: BELIEF[]=empty, DA not spawned, build-track=empty, product-designer+product-strategist pending |flagged to lead ¬silently overridden |option-A selected: complete plan challenge first |status: standing by for product-strategist R1 + challenge signals

H8-raw-event pre-challenge note (tech-architect 26.4.16): ADR[7] has capture_raw=True per-session flag. Product-designer PM[D2] signals UI-precondition. Pre-challenge position: will concede to always-on default (capture_raw=True default in SessionWriter, opt-out allowed). Rationale: "reliable" models can still emit malformed tool_call JSON under specific prompt conditions — forensic record must exist regardless of reliability tier. Storage trivial at v1 scale (3-model sessions).

step-14 pre-accept-verify 26.4.16 (lead): ALL PLAN-TRACK OUTPUTS MEET ROLE REQUIREMENTS
- tech-architect ✓ ADR:8 + IC:7 + SQ:17 + PM:5 + §2a/§2b/§2g + XVERIFY-SKIP(reasoned) + prompt-understanding mapping present
- product-designer ✓ DS:7 + IX:6 + CT:6-modules + PM:5 + VIABILITY[H11] dedicated + accessibility + hygiene checklist + source tags present
- product-strategist ✓ Q-pinned:2 + Q-secondary:3 + metrics-matrix(essential#8+luxury#6) + milestone-seq-with-kill-switches + PM:5 + §2g DB[] on both Q + §2a/§2b/§2c
- all three declared ✓ in convergence with ΣComm summary
- memory persistence: pending until promotion round (per AGENT-DEF flow)

step-15 XVERIFY-coverage 26.4.16 (lead): SKIP PERMITTED — no security-critical ADRs
- this build contains no security-critical decisions (local research tool, sigma-mem read-only, no MCP untrusted, no injection surface)
- §2h: ΣVerify available + non-security ADR → advisory not mandatory
- tech-architect XVERIFY-SKIP on ADR[6] with reasoned §2h outcome 2 (empirical viability experiment > cross-model opinion) — ACCEPTED
- product-strategist XVERIFY-SKIP (non-security advisory, neutral) — ACCEPTED
- product-designer: no XVERIFY but DS[2] 4.5:1-contrast T3-validate flagged — DA will assess as load-bearing or not
- gate status: PASS (advisory, neutral, no penalty)

step-17 cross-agent-coherence 26.4.16 (lead): COHERENT with 3 MISALIGNMENTS FLAGGED
coherence confirmed:
- IC[1-7] ↔ DS[1-7]: ChatOrchestrator → AsyncIterator[ChatEvent] feeds @st.fragment transcript; ChatEvent discriminated union (TokenEvent/ToolCallEvent/ToolResultEvent) maps cleanly to DS[4] 3-state badge (invoked/succeeded/errored)
- data model: CanonicalMessage + ProviderSpec + ToolCallRecord schema fields match metrics-panel data requirements (DS[5]) and strategist's essential metrics #8
- dependency ordering: M0 viability gate → M1a types first → parallel clusters A/B against types → M1c (bridge OR clone) → M2 → M3 — ordering aligns across all 3 plans
- H11 VIABILITY: all three converge on conditional-go with compatible (not identical) preconditions
  - tech-architect: Ollama native /api/chat + M0 2h experiment
  - product-designer: @st.fragment-isolation + sequential-turn-model + mixed-type-gen
  - product-strategist: M0 bridge prototype + Ollama native API + M1c Streamlit bridge prototype as SECONDARY kill-switch
misalignments flagged for challenge phase:
→ M1c-scope-conflict: tech-architect M1c = "clone to remaining SDK families"; product-strategist M1c = "Streamlit async bridge prototype (~1.5h)"; SAME LABEL, DIFFERENT SCOPE. DA + build-track to arbitrate.
→ M0-kill-switch-ownership: what happens if M0 fails? strategist says "user decides instrument shape" + "headless JSONL fallback answers Q1/Q2". tech-architect says viability experiment gates M1 but does not specify fallback. Plan should declare fallback explicitly in locked ADR.
→ M1-effort-estimate: CAL[M1] at 4d is at OPTIMISTIC END of reference class per §2b (tech-architect) + repeated by strategist as [prompt-claim] unverified (H5: 60-70%). Brad critique explicitly pushes this. DA must scrutinize.
→ DS[4] tool-badge T3-novel-pattern + DS[2] contrast-math T3-validate → flagged for DA as design-by-T3-source risk per §2d+

step-20 zero-dissent-circuit-breaker 26.4.16 (lead): NOT-FIRED
- DA r1: 10 challenges (3 HIGH, 5 MED, 2 LOW) — exit-gate FAIL
- BC-impl: 12 findings, CONDITIONAL, builder-feasibility 0.68, P(5d)=0.45, P(6d)=0.70
- BC-quality: 11 findings, test-coverage 0.52 WEAK, mock-risk HIGH
- BC-ui: 9 findings, CONDITIONAL, H11-P converges with designer's 0.65 (not architect's 0.87)
- Designer P=0.65 MAINTAINED over architect's P=0.87 with specific test proposal → anti-sycophancy signal AMPLIFIED per DA grading rule
- 4 cross-agent independent triangulations (BC[6]↔DA[#7], BC[9]↔DA[#1], BC[11]↔DA[#10], BC[12]↔DA[#3]) — indicates real issues, not anchoring
→ circuit-breaker NOT-FIRED: 42+ findings across 4 reviewers with MAINTAINED divergence is the opposite of zero-dissent; no CB[] entries required
→ divergence is organic and logged, not suppressed

step-21 validate-circuit-breaker 26.4.16 (lead): PASS — divergence documented in ## convergence (designer P=0.65 maintained) and build-track-feasibility sections

step-22 route-challenges-to-plan-track 26.4.16 (lead): in-progress — batched message to each plan-track agent with their targeted challenges + coordination asks for M0 scope + ADR[9] M0-fallback + CAL[M1] revision

## open-questions

(plain English, user-facing — surface only if critical)

OQ[1]: M1c scope conflict between agents. tech-architect's M1c = "clone to remaining SDK families (GPT, Gemini, remaining Ollamas)." product-strategist's M1c = "Streamlit async bridge prototype (~1.5h)." Same label, different scope. Will be resolved by build-track/DA challenge; surfaced here for visibility.

OQ[2]: M1 effort estimate is at the optimistic end of the industry reference class (4 days vs. 4-9 day range). The external reviewer (Brad) claim "M1 is 60-70% of whole project" is currently unverified. DA will scrutinize; user may need to accept the optimism risk or explicitly re-estimate.

OQ[3]: H8 raw-event capture. tech-architect pre-conceded to capture_raw=True as SessionWriter default (opt-out), triggered by product-designer PM[D2] flagging it as UI-precondition. This resolves constructively before DA challenge. No user decision needed unless storage concern emerges.

OQ[4] (surfaced by product-strategist R2): The instrument collects identical data whether primary research question is (d) chatroom-context tool-use vs. BFCL — currently pinned as Q1 — OR (a) memory-invocation coherence, which was Brad's first suggestion. The difference is M4 analysis focus and which metric the M3 panel foregrounds; data collection is the same either way. USER DECISION potentially needed before M3 ships. Not blocking for plan lock — plan should preserve both options by logging raw query text + invocation records.

OQ[5] resolution of OQ[1]: canonical naming proposed by product-strategist R2 compromise: M0 (2h viability prototype) → M1a (types+ProviderProtocol) → M1b (two-provider streaming, no tools) → M1c (tool-use + exec loop on seed pair) → M1d (remaining SDK families) → M2 (Streamlit MVP) → M3 (sigma-mem + metrics + v1 ship). Absorbs tech-architect's "clone-to-remaining-SDKs" as M1d and uses M1c for narrower "tool-use on seed pair" scope. Pending tech-architect + build-track concurrence in challenge round.

## promotion

(empty — candidates for sigma-mem promotion at outcome delivery)
