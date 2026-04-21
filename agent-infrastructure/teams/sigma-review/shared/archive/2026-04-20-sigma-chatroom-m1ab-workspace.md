# C1 scratch — BUILD: sigma-chatroom-m1ab
## status: archived-c1
## archived-date: 2026-04-21
## mode: BUILD
## archive-metadata: C1 PLAN phase complete. DA-r2 exit-gate PASS, P(plan-ready)=0.87, engagement A-, rounds 2/5. XVERIFY[ADR3] documented gap per §2h (sigma-verify cross_verify infra hang x3 this session). Agents: tech-architect-r3 (final R2 author — prior r1+r2 instances hung), ui-ux-engineer, implementation-engineer, code-quality-analyst, devils-advocate-r2 (prior r1 hung). Lead-proxy persistence applied (8 agent memories + 1 team decision + 1 team pattern stored via sigma-mem by lead due to agent tool-permission gap).

## task
Build C1 (PLAN phase) for sigma-chatroom M1a + M1b. Source plan: ~/.claude/plans/look-for-the-plan-snazzy-giraffe.md.
Repo ~/Projects/sigma-chatroom/ does not exist — to be created by C2 (build phase).

M1a: two-model streaming (Anthropic claude-opus-4-7 + Ollama cloud devstral-2:123b-cloud preferred) with RoundRobin, JSONL persistence, CLI to stdout, NO tools.
M1b: native tool-use + TurnEngine tool-exec loop (cap 5 calls/turn) on the same pair, YieldNext + Random policies, MetricsCollector baseline, ToolCallRecord observability (preceding_text + position_in_turn + latency_ms + result), echo-tool fixture.

Scope add (per user, 2026-04-20): Q3 = produce preliminary forward build-out plan for M1c → M2 → M3 → M4. Not code-scope for C2; planning deliverable that gets revised as M1a/b findings come in.

## infrastructure
ΣVerify: READY |providers: openai(gpt-5.4), google(gemini-3.1-pro-preview), anthropic(claude-opus-4-6), + 10 Ollama (local + cloud: nemotron-3-super, deepseek-v3.2, qwen3.5, devstral-2:123b, glm-5, kimi-k2.5, nemotron-3-nano:4b, qwen3.5:4b, llama3.1:8b, gemma4:e4b) | #13 providers
XVERIFY mandate: top 1 load-bearing finding per plan-track agent (tech-architect, ui-ux-engineer)
Security-critical: NONE for this build — research instrument, not security-critical per source plan (C1 constraint). XVERIFY remains advisory not mandate for this build.

## prompt-understanding

### Q[] — what to build
- Q1: M1a — two-model streaming (Anthropic + Ollama cloud), RoundRobin policy, JSONL persistence (schema_version: "1"), CLI streaming to stdout, NO tools. Success = one session, 2 models, 5 turns, round-robin, streamed live, persisted JSONL with stop_reason + ttft_ms populated, replayable from JSONL.
- Q2: M1b — native per-SDK tool-use (Anthropic content-blocks + Ollama OpenAI-compat tool_calls), TurnEngine tool-exec loop (cap 5 calls/turn → force stop_reason="max_tool_calls"), YieldNext + Random policies, tests/fixtures/echo_tool.py, MetricsCollector baseline, ToolCallRecord with preceding_text + position_in_turn + latency_ms + result, raw event capture default-on when tool_use_reliability != "reliable". Success = same 2 models, ≥1 successful echo-tool round-trip per provider, ToolCallRecord captured with full fields.
- Q3: preliminary forward build-out plan for M1c (clone to OpenAI + Google + Ollama local — 13 providers in roster) → M2 (Streamlit MVP + pre-M2 2h concurrency shim prototype) → M3 (sigma-mem wiring + metrics panel + per-model context calibration; v1 ship point) → M4 (more tools + embedding convergence + topic drift + speaker-influence graph). Revision hooks tied to M1a/b findings (e.g., if message_mapping proves harder than expected, M1c scope adjusts).

### H[] — architectural claims to STRESS-TEST, not accept
- H1: Purpose-built `providers/` module beats abstracting sigma-verify's `clients.py` for multi-turn streamed chat with tool-use. [source-plan ADR]
- H2: Native per-SDK tool-use (Anthropic content-blocks + Ollama OpenAI-compat tool_calls) beats text-convention or ollama-mcp-bridge. [source-plan ADR]
- H3: Tool-exec loop belongs in TurnEngine, not Provider. Provider.stream() = exactly one SDK call. TurnEngine orchestrates tool_call→execute→append tool_result→re-invoke stream. [source-plan ADR]
- H4: `message_mapping.py` is the elevated-risk adapter file (Anthropic content-blocks ↔ OpenAI siblings ↔ Gemini parts). Per-SDK round-trip tests in test_message_mapping.py as MERGE GATES. [source-plan ADR]
- H5: 60% of max_context_tokens is sufficient budget for M1 (down from 70% accounting for tokenizer drift across SDKs); `len//4` estimate adequate for M1. [source-plan tuning]
- H6: Raw event capture default-on when `tool_use_reliability != "reliable"` distinguishes declined / malformed / SDK-swallowed from silent failure. [source-plan observability]
- H7: Canonical `Message` shape = OpenAI-shaped by convention; adapters own all non-trivial translation (Anthropic content-blocks, Gemini parts). [source-plan design]

!rule: H[] are HYPOTHESES not requirements. Plan-track stress-tests each against independent evidence. Build-track evaluates implementability. DA probes alternatives. If evidence suggests a better approach, plan diverges from source — per user directive "plan is starting point, not blindly followed."

### C[] — constraints (hard boundaries)
- C1: TIER-2 BUILD, research instrument, NOT security-critical. XVERIFY on security-critical ADRs is advisory here.
- C2: New repo at ~/Projects/sigma-chatroom/ — does not exist. C2 creates it.
- C3: Study ~/Projects/sigma-verify/src/sigma_verify/clients.py for patterns. DO NOT IMPORT. [hard-stop]
- C4: Do NOT use ~/Projects/ollama-mcp-bridge. Use each SDK's native tool-use, including Ollama's OpenAI-compat tool_calls. [hard-stop]
- C5: Streaming from day 1 (M1a baseline), not M4.
- C6: M1 seed pair: Anthropic claude-opus-4-7 + Ollama cloud. Cloud model preference: devstral-2:123b-cloud, alternates: deepseek-v3.2:cloud, qwen3.5:cloud.
- C7: SDK deps for M1a/b: anthropic, openai (for Ollama OpenAI-compat), pydantic. Streamlit + mcp deferred to M2/M3. google-genai deferred to M1c.
- C8: schema_version: "1" on every JSONL record from day 1 (not retrofitted).
- C9: Out-of-scope hard-stops: M1c (cloning to other SDK families), M2 (Streamlit UI), M3 (sigma-mem wiring — M1b uses echo tool only), M4 (more tools + embedding metrics), ollama-mcp-bridge.
- C10: "memory" is NOT a valid Turn.speaker value (vestigial from early text-convention draft). ProviderSpec.key or "human" only.

### user-confirmed: YES (2026-04-20)

## scope-boundary
This build implements (C2 code scope):
- M1a: providers/base.py, providers/registry.py, providers/anthropic_client.py, providers/ollama_client.py, providers/message_mapping.py (streaming-only paths), conversation.py (Turn, ConversationState, PreambleVariant), turn_engine.py (RoundRobinPolicy + advance_stream), persistence.py (JSONL schema_version: "1"), cli.py (streaming to stdout). Tests: mock providers (streaming), RoundRobin policy unit, JSONL round-trip.
- M1b: ToolSchema, providers/tool_schema.py, providers/message_mapping.py tool-use paths, tool_call StreamEvent emission in both providers, TurnEngine tool-exec loop (cap 5/turn), YieldNextPolicy + RandomPolicy, tests/fixtures/echo_tool.py, MetricsCollector baseline, ToolCallRecord capture. Tests: per-SDK tool-use round-trip, message-mapping round-trip (merge gate), turn-engine tool-exec loop, echo-tool integration.

This build does NOT implement (code-scope hard-stops):
- M1c: OpenAI + Google + Ollama local clients, 13-provider roster.
- M2: Streamlit app, sidebar, transcript view, tool-call badges, autonomous/human-moderated modes.
- M3: MemoryHelper + MCP client, SIGMA_MEM_RECALL tool, metrics panel, per-model context calibration.
- M4: Additional tools (web search, calculator, code exec), embedding convergence, topic drift, speaker-influence graph.

This build produces (C1 planning scope, non-code):
- Locked ADRs/ICs/SQs/PMs for M1a + M1b (primary plan deliverable).
- Preliminary forward build-out plan for M1c → M2 → M3 → M4 with revision hooks tied to M1a/b findings (Q3 scope add per user).

Lead: before accepting agent output, verify it builds ONLY what's in code scope. Q3 forward plan = planning artifact only, not code scope.

## complexity-assessment
BUILD TIER-2 |scores: module-count(4), interface-changes(3), test-complexity(4), dependency-risk(2), team-familiarity(2) |total:15 |plan-track:2 (tech-architect + ui-ux-engineer) |build-track:2 (implementation-engineer + code-quality-analyst) |DA: joins Step 18

Composition rationale:
- tech-architect: primary plan-track owner — ADRs for providers/TurnEngine/message_mapping, ICs, technology selection, performance strategy for streaming + tool-exec loop.
- ui-ux-engineer: secondary plan-track — owns Q3 forward plan for M2 (Streamlit) + stress-tests pre-M2 concurrency shim feasibility claim (H from source plan risk table). No UI in M1a/b code, but M2 readiness is at risk of M1a/b interface contract leakage.
- implementation-engineer: build-track feasibility challenge — evaluates M1a/b implementability; will own C2 code.
- code-quality-analyst: build-track feasibility challenge — evaluates test strategy, merge-gate coverage for message_mapping round-trips, edge cases.
- devils-advocate: joins Step 18, probes H1-H7 alternatives, source-provenance audits all [source-plan] findings.

Product-designer NOT included — no UI in M1a/b code scope; ui-ux-engineer covers M2 forward design in Q3.

## plans (plan-track agents)
### tech-architect

#### Boot-read summary
- sigma-verify clients.py: synchronous `call()` only, no streaming/tool-use, dataclass results, Ollama base class wraps OpenAI SDK against `localhost:11434/v1`, `_extract_content` fallback handles reasoning-model content-vs-reasoning split. Pattern study confirms `clients.py` shape is fan-out-verification, ¬multi-turn-streamed-chat.
- Source plan: 7 H[] hypotheses extracted to workspace ## prompt-understanding. Independent stress-test follows.

---

#### ADR[1]: providers module shape — purpose-built vs sigma-verify abstraction
!stress-tests:H1 |load-bearing:YES

**Decision.** Purpose-built `providers/` module. ¬import/subclass sigma-verify `clients.py`. Study patterns only.

**Alternatives considered.**
  ALT1→ Subclass `_OllamaClientBase` from sigma-verify for all Ollama-backed providers (reuse env discovery, `_extract_content` fallback).
  ALT2→ Copy `_OllamaClientBase` verbatim into sigma-chatroom then extend.
  ALT3→ Purpose-built from scratch, borrow only specific functions (`_extract_content`, env-discovery pattern) via re-implementation.

**Rationale.** [code-read /Users/bjgilbert/Projects/sigma-verify/src/sigma_verify/clients.py:266-288] `_OllamaClientBase.call()` is sync, returns `tuple[str, int, int]`, ¬streaming, ¬tool-use. Adapting this to async+streaming+tool-use means replacing every method body — only `__init__` env-discovery + `_extract_content` survive. That's <20 LOC of real reuse against ~900 LOC of divergent surface area. ALT1/ALT2 buy coupling at cost ~equal to ALT3's re-implementation. Coupling risk: sigma-verify ships under Apache 2.0 and evolves independently; API breakage in clients.py breaks chatroom silently.

**Evidence FOR H1 (purpose-built beats abstraction).**
  E1→ [code-read clients.py:266] sync `call()` signature is wrong shape for async streaming — any subclass must override the entire public surface.
  E2→ [code-read clients.py:290,318] `verify()` + `challenge()` methods embed prompt-building + JSON parsing — none of which chatroom needs. Inheriting these as dead weight is anti-abstraction.
  E3→ [agent-inference] Chatroom's `Provider.stream()` returns `AsyncIterator[StreamEvent]` — fundamentally incompatible with `call() → tuple`.

**Evidence AGAINST H1 (would favor abstraction).**
  A1→ [code-read clients.py:247-264] `_extract_content` correctly handles Ollama reasoning-model content/reasoning split — ¬trivial to rediscover. Re-implementing risks missing the edge case.
  A2→ [code-read clients.py:221-236] Env-discovery pattern (`{PREFIX}_PROVIDER`, `{PREFIX}_MODEL`, `{PREFIX}_API_KEY`, `{PREFIX}_BASE_URL`) is a well-considered convention. Divergent env-var schemas across sigma-verify and chatroom increase user confusion.

**Reconciliation.** E1-E3 dominate: shape mismatch is load-bearing. A1-A2 mitigated by borrowing specific logic (`_extract_content` function, env-var naming convention) via copy-with-attribution, ¬inheritance.

**Tradeoffs.**
  + No coupling to sigma-verify lifecycle.
  + Clean async/streaming design unconstrained by sync parent class.
  − ~20 LOC duplication (extract_content logic, env-discovery helper).
  − Divergence risk: if sigma-verify fixes a bug in `_extract_content`, chatroom won't inherit it.

**Mitigation for duplication risk.** Copy-with-attribution: paste `_extract_content` into `providers/ollama_client.py` with comment `# borrowed from sigma-verify clients.py:247 — handles reasoning-mode models`. Name env vars identically (`{PREFIX}_API_KEY`, etc.) so user conventions carry over.

**Reversibility cost.** LOW. If we change our minds in M1c/M2, moving to sigma-verify-as-dep is a 1-2 day refactor (change imports, adapt async shim). ¬data-migration, ¬schema-change.

**Source tags.** [code-read clients.py:266-288,247-264,221-236] + [agent-inference] + [source-plan claim]

**§2a positioning.** CONSENSUS with source plan H1. Outcome 2: CONFIRMS WITH ACKNOWLEDGED RISK. Risk: duplication of `_extract_content` logic; mitigation specified.

**§2b calibration.** Precedent: sigma-mem repo chose same pattern — independent providers module, ¬sigma-verify dep. Calibration point: prior project made identical call.

**§2c cost/complexity.** Justified. ~800-1200 LOC providers module estimated for M1a/b; overhead vs abstraction is <5%.

**§2e premise viability.** Premise "sigma-verify's shape is wrong" is viable — verified by code-read.

---

#### ADR[2]: tool-use architecture — native per-SDK vs text-convention vs bridge
!stress-tests:H2 |load-bearing:YES

**Decision.** Native per-SDK tool-use. Anthropic: `messages.stream` with `tool_use` content blocks. Ollama: OpenAI-compat `tool_calls`. ¬text-convention. ¬ollama-mcp-bridge.

**Alternatives considered.**
  ALT1→ Text-convention: models emit `TOOL_CALL: <name>(<args>)` in plain text, chatroom parses regex.
  ALT2→ ollama-mcp-bridge: route all Ollama calls through the local MCP bridge which synthesizes tool_calls for models that don't natively support them.
  ALT3→ Hybrid: native for SDKs that support it, text-convention fallback for models with `tool_use_reliability="none"`.

**Evidence FOR H2 (native beats alternatives).**
  E1→ [independent-research] Anthropic Python SDK ≥0.40 emits `content_block_start` / `content_block_delta` events with `type: "tool_use"` in streaming — structured, parseable, first-class. Regex on text is strictly worse given SDK provides structure.
  E2→ [independent-research] Ollama OpenAI-compat endpoint (`/v1/chat/completions`) emits `tool_calls` array when model is instruction-tuned for it (e.g. `devstral-2:123b` trained on Mistral's function-calling format). Bridge would add indirection + a moving dep.
  E3→ [source-plan claim + code-read C4] User directive: "use each SDK's native tool-use". ollama-mcp-bridge is out-of-scope hard-stop (C4).
  E4→ [agent-inference] `tool_use_reliability` taxonomy is ONLY meaningful when comparing across native SDK behaviors — abstracting behind a bridge erases the research signal.

**Evidence AGAINST H2 (would favor alternatives).**
  C1→ [agent-inference] If devstral-2:123b emits malformed `tool_calls` under load, native path offers no recovery — bridge could sanitize. But: this is what raw-event capture + `tool_use_reliability="nominal"` is designed to surface, ¬paper-over.
  C2→ [source-plan risk-table] Small Ollamas may silently decline → "0 invocations ambiguity". Mitigation: raw sidecar. Native still correct, just needs observability.

**Reconciliation.** E1-E4 dominate. C1-C2 are addressed by raw event capture (ADR[6]), ¬architectural change. H2 holds. Consensus with source plan.

**Tradeoffs.**
  + Research signal preserved (per-SDK reliability observable).
  + No extra dependency.
  − Per-SDK divergence in message_mapping.py adapter (see ADR[4]).

**Reversibility cost.** MEDIUM. Adding a bridge later = M1c or M2 refactor. Removing native = expensive (rewrite message_mapping, lose tool_use_reliability signal).

**Source tags.** [source-plan claim C4] + [independent-research Anthropic SDK] + [independent-research Ollama OpenAI-compat] + [agent-inference]

**§2a positioning.** CONSENSUS with H2. Outcome 2.
**§2b calibration.** Precedent: Anthropic docs + Ollama docs both document native tool-use as preferred path.
**§2c cost/complexity.** Justified. Native is actually cheaper than bridge because it avoids bridge process mgmt.
**§2e premise viability.** Premise viable.

---

#### ADR[3]: tool-exec loop location — TurnEngine vs Provider
!stress-tests:H3 |load-bearing:YES (highest-stakes — XVERIFY candidate)

**Decision.** Tool-exec loop lives in `TurnEngine`. `Provider.stream()` = exactly one SDK call. TurnEngine orchestrates: tool_call event → execute tool → append tool_result Message → re-invoke `provider.stream()`.

**Alternatives considered.**
  ALT1→ Tool-exec inside `Provider.stream()` (Provider runs the loop internally, yields only final stop). Provider becomes "smart".
  ALT2→ Tool-exec as a separate `ToolExecutor` service that sits between Provider and TurnEngine.
  ALT3→ Hybrid: Provider handles tool-exec for its own SDK's "agentic" mode (e.g. if Anthropic exposes one in the future), TurnEngine handles cross-SDK.

**Evidence FOR H3 (TurnEngine location is correct).**
  E1→ [agent-inference] Separation of concerns: Provider knows ITS SDK's wire format; TurnEngine knows the chatroom's turn semantics (5-call cap, stop_reason override, ToolCallRecord emission). Mixing violates single-responsibility.
  E2→ [source-plan claim + code-read ToolCallRecord schema] ToolCallRecord captures `position_in_turn` + `preceding_text` — these require knowing the chatroom's conversation state, which Provider ¬has.
  E3→ [agent-inference] The 5-call cap is a chatroom policy, ¬SDK feature. Enforcing it inside Provider couples SDK wrapper to research-instrument policy. If policy changes (e.g. M3 raises to 10), only TurnEngine changes.
  E4→ [agent-inference] Re-invocation of `provider.stream()` after tool_result — if Provider loops internally, it must know how to append tool_result to its own message list AND how to re-enter streaming AND how to track turn-level state. Three responsibilities instead of one.

**Evidence AGAINST H3.**
  C1→ [agent-inference] ALT1 (Provider-owned loop) matches Anthropic's "agentic tool_use" SDK pattern (if Claude handles the loop internally, SDK offers agent mode). But: chatroom wants the tool_use loop observable (metrics, tool-use-reliability calibration), agent-mode hides intermediate steps.
  C2→ [agent-inference] ALT2 (ToolExecutor service) cleaner for testability. But: adds layer without clear benefit for M1a/b. Defer to M3 if complexity warrants.

**Reconciliation.** E1-E4 dominate. C1 erases research signal. C2 premature. H3 holds.

**Tradeoffs.**
  + Clear separation: Provider = wire, TurnEngine = policy.
  + Testable: mock Provider returning tool_call event, assert TurnEngine calls tool + re-invokes stream.
  − TurnEngine complexity: it owns both turn-dispatch (next_speaker) and tool-exec orchestration. Risk: TurnEngine becomes god-class.

**Mitigation for god-class risk.** TurnEngine delegates tool-exec to a private `_execute_tool_chain` coroutine; unit-test separately. Target: `turn_engine.py` ≤400 LOC for M1a/b.

**Reversibility cost.** MEDIUM-HIGH. Pushing the loop into Provider later requires re-wiring StreamEvent flow, ToolCallRecord emission, 5-call cap. ~1-2 weeks refactor.

**Source tags.** [source-plan claim H3] + [agent-inference] + [code-read source-plan ToolCallRecord schema]

**§2a positioning.** CONSENSUS with H3. Outcome 2.
**§2b calibration.** Precedent: langchain-agents, autogen, crewai all separate agent-loop from LLM-client. Consensus across industry.
**§2c cost/complexity.** Justified.
**§2e premise viability.** Premise viable.

**XVERIFY candidate.** This is top-1 load-bearing ADR. Recommend `verify_finding` on cross-model (openai+google+anthropic) for consensus check — see §XVERIFY below.

---

#### ADR[4]: message_mapping.py scope — canonical Message + adapter responsibility
!stress-tests:H4 + H7 |load-bearing:YES |elevated-risk:CONFIRMED

**Decision.** Canonical `Message` is OpenAI-shaped by convention. `message_mapping.py` owns ALL non-trivial translation to/from Anthropic content-blocks, Ollama OpenAI-compat, (future: Gemini parts). Per-SDK round-trip tests in `test_message_mapping.py` are MERGE GATES (CI blocks merge if any `to_sdk → from_sdk` round-trip loses fidelity).

**Alternatives considered.**
  ALT1→ Canonical Message = Anthropic-shaped (content-blocks primary). Adapters would simplify Anthropic path but complicate Ollama/Gemini.
  ALT2→ Per-provider Message subclasses; no canonical form.
  ALT3→ Canonical Message as a union type (OpenAI | Anthropic | Gemini shape) — zero translation, explicit per-SDK shape.

**Evidence FOR (OpenAI-shaped canonical).**
  E1→ [independent-research] Majority of providers in scope speak OpenAI-compat natively: Ollama (all local + cloud) + OpenAI (M1c) + most third-party SDKs (Fireworks, OpenRouter, Together). Choosing OpenAI shape minimizes adapter work for majority.
  E2→ [code-read sigma-verify clients.py] 8/13 providers in sigma-verify roster are OpenAI-compat via Ollama. Pattern precedent.
  E3→ [agent-inference] OpenAI's `tool_calls` + sibling `role="tool"` messages are flat list structure — easier to append/persist in JSONL than nested content-blocks.

**Evidence AGAINST.**
  C1→ [independent-research] Anthropic's `tool_use` + `tool_result` ARE content blocks within an assistant/user message. Converting to OpenAI's siblings means splitting one Anthropic message into multiple OpenAI messages AND reassembling on `from_sdk`. This IS the "elevated-risk" complexity H4 warns about.
  C2→ [independent-research] Gemini `function_call` + `function_response` are parts within `role="model"` / `role="user"` content — neither OpenAI sibling shape nor Anthropic content-blocks exactly. Gemini adapter will be hardest.

**Reconciliation.** C1-C2 confirm H4's elevated-risk claim. But choosing any canonical shape leaves two adapters as the hard part — OpenAI-shape minimizes count of adapters needed (Ollama = identity for M1a/b). H7 holds.

**Specific translation responsibilities (load-bearing detail).**
  M1a→ Streaming-only, no tool-use. Anthropic adapter: expand `content: str` to `[{"type": "text", "text": "..."}]` on `to_sdk`, concatenate text blocks on `from_sdk`. Ollama adapter: identity (OpenAI-compat = canonical shape).
  M1b→ Tool-use paths. Anthropic adapter: split assistant message with `tool_calls` into Anthropic assistant message with `tool_use` content blocks. On `from_sdk`, collapse `tool_use` blocks back into `tool_calls` field + text into `content`. Tool result: user message with `tool_result` content block → canonical `role="tool"` with `tool_call_id`. Ollama adapter: identity.
  M1c→ (Q3 forward-plan only) Gemini adapter: map `role="assistant"` ↔ `role="model"`, flatten `tool_calls` to `parts: [{function_call: ...}]`, `role="tool"` → `role="user"` + `parts: [{function_response: ...}]`.

**Round-trip test spec (MERGE GATE).**
  for each sdk in [anthropic, ollama]:
    for each canonical message in fixtures (text-only, tool-call, tool-result, mixed-content):
      assert from_sdk(to_sdk(msg)) == msg  # fidelity preservation
  fixtures: ≥8 per SDK covering: system/user/assistant/tool roles, single-turn, multi-turn, tool_call with args, tool_result with content, tool_result with error, mixed text+tool_call.

**Tradeoffs.**
  + Majority-provider (OpenAI-compat) gets trivial adapter.
  + Round-trip tests catch adapter drift.
  − Anthropic adapter is non-trivial (documented as elevated-risk).

**Reversibility cost.** HIGH. Changing canonical shape after M1a ships = rewrite every adapter + break JSONL replay (schema_version bump required).

**Source tags.** [source-plan H4+H7] + [independent-research Anthropic SDK] + [independent-research Gemini SDK] + [agent-inference] + [code-read clients.py]

**§2a positioning.** CONSENSUS with H4+H7. Outcome 2: CONFIRMS WITH ACKNOWLEDGED RISK — risk = Anthropic adapter complexity documented in PM[1].
**§2b calibration.** Precedent: langchain uses OpenAI-shaped canonical + per-SDK adapters. Consensus.
**§2c cost/complexity.** Justified. Alternative (per-provider subclasses) explodes test matrix.
**§2e premise viability.** Premise viable + elevated-risk confirmed.

**DB[ADR4]:** (1) initial: OpenAI-shaped canonical is clearly right. (2) assume-wrong: what if Anthropic-shape saves more complexity? (3) strongest-counter: if we go Anthropic-shape, Ollama/OpenAI adapters must split content-blocks into flat list — same splitting work, but now against majority-traffic. More total complexity. (4) re-estimate: OpenAI-shape still correct. (5) reconciled: keep OpenAI-shape; document Anthropic adapter as highest-test-priority file.

---

#### ADR[5]: context budget strategy — 60% + len//4 for M1
!stress-tests:H5

**Decision.** For M1a/b: budget = 60% of `ProviderSpec.max_context_tokens`. Estimator = `len(text) // 4`. Per-model calibration deferred to M3 per source plan.

**Alternatives considered.**
  ALT1→ 70% budget (source plan's original figure, revised down to 60%).
  ALT2→ Use SDK-provided tokenizers (`anthropic.tokenize`, `tiktoken` for OpenAI-compat) for accurate counts — kills the drift problem but adds import weight.
  ALT3→ 60% + per-SDK tokenizer call only at truncation-decision time (cheap, accurate).

**Evidence FOR H5 (60% + len//4 sufficient for M1).**
  E1→ [independent-research] `len//4` approximates ~4 chars/token for English — Anthropic docs cite ~3.5, OpenAI cites ~4. Drift is ≤15% across tokenizers for English text. With 60% budget, drift is absorbed.
  E2→ [source-plan risk-table] M3 explicitly handles per-model calibration using `reported input_tokens`. M1 is headless-engine milestone; calibration is not on critical path.
  E3→ [agent-inference] For M1 seed pair (claude-opus-4-7 + devstral-2:123b), both have large context windows (200K+, 128K+). 60% = 120K+ usable, ≥77K for devstral — far exceeds any plausible 5-turn M1 session.

**Evidence AGAINST.**
  C1→ [agent-inference] If user runs M1a/b with a small-context Ollama (e.g. llama3.1:8b with 8K ctx), 60% = 4.8K usable. A 5-turn session with verbose preamble could approach truncation. But: M1 seed pair is Anthropic + Ollama-cloud large models — small-context case is M1c.
  C2→ [agent-inference] `len//4` overcounts for code-heavy text (code is ~3 chars/token) and undercounts for CJK (~1-2 chars/token). Multi-lingual research scope could bias. M1 content is English research prompts → within tolerance.

**Reconciliation.** E1-E3 dominate for M1 scope. C1-C2 are M1c+ concerns. H5 holds.

**Calibration hook (critical).** ADR[5] includes a **revision hook for Q3 forward plan**: if M1a empirical run shows `reported_input_tokens` diverges from `len(concatenated_text)//4` by >15% for any M1 model, M3 calibration design must shift LEFT to M1c — because divergence invalidates the 60% buffer assumption for small-context providers added in M1c.

**Tradeoffs.**
  + Cheap, no extra deps.
  + Adequate for M1 scope.
  − Risks silent truncation on code-heavy prompts or CJK.

**Reversibility cost.** LOW. Swapping estimator is local change in `context.py` (not written in M1a — but scoped for M1b or as noted for M1c).

**Source tags.** [source-plan H5] + [independent-research tokenizer drift] + [agent-inference] + [source-plan M3 calibration]

**§2a positioning.** CONSENSUS with H5, with added revision hook.
**§2b calibration.** Industry standard crude estimator.
**§2c cost/complexity.** Justified.
**§2e premise viability.** Premise viable for M1 scope.

---

#### ADR[6]: raw event capture — default-on when tool_use_reliability != "reliable"
!stress-tests:H6

**Decision.** Raw SDK event capture default-on for any provider whose `ProviderSpec.tool_use_reliability != "reliable"`. Sidecar file: `sessions/raw/<session_id>.raw.jsonl`. Env override: `CHATROOM_CAPTURE_RAW=0` disables; `CHATROOM_CAPTURE_RAW=1` forces-on regardless of reliability tag.

**Alternatives considered.**
  ALT1→ Raw capture always-on for all providers.
  ALT2→ Raw capture opt-in only (env flag).
  ALT3→ Raw capture on for M1a (learning phase), off by default in M3+ (ship phase) except for `tool_use_reliability="none"|"nominal"|"unknown"`.

**Evidence FOR H6.**
  E1→ [source-plan risk-table] "0 invocations ambiguity" — w/o raw capture, we cannot distinguish: model declined / model tried + emitted malformed JSON SDK swallowed / model emitted tool_call but SDK parser failed. Three causes, same observation.
  E2→ [agent-inference] In M1 seed pair, devstral-2:123b has `tool_use_reliability="unknown"` (not yet empirically tested). Default-on captures the first run's evidence, updates tag.
  E3→ [agent-inference] Storage cost is bounded: raw events for a 5-turn session at ~4KB/event × ~50 events = ~200KB per session. Trivial.

**Evidence AGAINST.**
  C1→ [agent-inference] ALT1 (always-on) is simpler. But for `tool_use_reliability="reliable"` providers, raw capture is redundant — we have structured events. Storage + privacy (raw events may contain prompts verbatim) argue against always-on.

**Reconciliation.** E1-E3 dominate. ALT1 wastes disk and exposes more data than needed. H6 holds.

**Tradeoffs.**
  + Observability on the hard cases, silence on the reliable ones.
  + Storage bounded.
  − Two env toggles (implicit via tag, explicit via env) = slightly higher DX complexity.

**Reversibility cost.** LOW. Flag is local to `persistence.py`.

**Source tags.** [source-plan H6 + risk-table] + [agent-inference]

**§2a positioning.** CONSENSUS with H6.
**§2b calibration.** Default-selective-capture is standard pattern for debug tooling.
**§2c cost/complexity.** Justified.
**§2e premise viability.** Premise viable.

---

#### ADR[7]: schema_version + JSONL persistence format
!stress-tests:source-plan C8

**Decision.** Every JSONL record (Turn, ToolCallRecord, session-header) carries `"schema_version": "1"` field from day 1. `persistence.py` writes session header as first line, then turns+tool-records interleaved.

**Alternatives considered.**
  ALT1→ Top-level schema in session header only; records inherit implicitly.
  ALT2→ `schema_version` in sidecar metadata file, not per-record.
  ALT3→ Semantic version `"1.0.0"` vs simple `"1"`.

**Rationale.** Per-record schema_version means any line is self-describing → replay tools can version-check individual records. Critical for M3+ when schema v2 may be introduced (e.g. adding `preamble_variant` reference or per-turn model_version).

**Evidence FOR.**
  E1→ [source-plan C8] "schema_version: '1' on every JSONL record from day 1 (not retrofitted)" — retrofit is expensive.
  E2→ [agent-inference] Simple integer `"1"` beats semver for research instrument — we don't need patch-level compat.
  E3→ [industry-pattern] OpenTelemetry, Jaeger, most event-log formats version per-record.

**Evidence AGAINST.** [agent-inference] Slight storage overhead (~20 bytes/record). Trivial at research scale.

**Format spec (load-bearing detail).**
```jsonl
{"schema_version": "1", "type": "session_header", "session_id": "...", "mode": "autonomous", "roster": [...], "preamble_variant": "identity-aware", "ts": "..."}
{"schema_version": "1", "type": "turn", "speaker": "claude-opus-4-7", "provider": "anthropic", "content": "...", "tokens_in": 0, "tokens_out": 0, "stop_reason": "end_turn", "ttft_ms": 450, "total_ms": 2300, "ts": "...", "tool_calls": [...]}
{"schema_version": "1", "type": "tool_call", "turn_id": "...", "speaker": "...", "provider": "...", "tool_name": "echo", "arguments": {...}, "ts_started": "...", "ts_completed": "...", "latency_ms": 12, "result": "...", "result_chars": 24, "error": null, "position_in_turn": 0, "preceding_text": "..."}
```

**Source tags.** [source-plan C8] + [industry-pattern] + [agent-inference]

**§2a/2b/2c/2e:** all outcome 2, consensus.

---

#### ADR[8]: streaming from day 1 (M1a)
!stress-tests:source-plan C5

**Decision.** Streaming is M1a baseline. `Provider.stream()` is required; `Provider.complete()` can stub (raise `NotImplementedError` for M1a; implement thin wrapper over `stream()` in M1b if needed).

**Alternatives considered.**
  ALT1→ Defer streaming to M2 (UI phase). M1a uses `complete()` only, CLI prints once per turn.
  ALT2→ Streaming optional in M1a, gated by flag.

**Evidence FOR source-plan C5.**
  E1→ [source-plan design-decision #2 + C5] "Token-by-token rendering; TTFT and stop_reason are first-class signals." TTFT is a metric; can't be captured without streaming.
  E2→ [agent-inference] Streaming adds async plumbing to the providers module. If we defer, M2 Streamlit shim (already identified as risk) is forced to integrate async streaming + new interface simultaneously — worse not better.
  E3→ [agent-inference] For M1b, tool_call events are delivered via streaming (`content_block_start` in Anthropic, `delta.tool_calls` in OpenAI-compat). Non-streaming paths require different parsing code. Unifying on streaming reduces code paths.

**Evidence AGAINST.**
  C1→ [agent-inference] Streaming is harder to test — async generators need async test runners. Mock provider complexity rises.

**Reconciliation.** E1-E3 dominate. H holds.

**Tradeoffs.**
  + TTFT captured from day 1.
  + Single code path for tokens + tool_calls.
  − Test infra complexity (mitigated: `pytest-asyncio` + async mock provider fixture).

**Reversibility cost.** N/A — deferring streaming later is strictly a feature-removal.

**Source tags.** [source-plan C5 + design-decision #2] + [agent-inference]

**§2a/2b/2c/2e:** all outcome 2, consensus.

---

#### IC[1]: Provider protocol
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

    async def complete(
        self,
        messages: list[Message],
        system: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: list[ToolSchema] | None = None,
    ) -> CompleteResult: ...
    # M1a: stream() required; complete() MAY raise NotImplementedError.
    # M1b+: complete() wraps stream() + collects to CompleteResult.

    # ¬method: provider does NOT execute tools. That belongs in TurnEngine.
    # ¬method: provider does NOT manage conversation state. Stateless per-call.
```

**Invariants.**
  INV1→ `Provider.stream()` = exactly one SDK call; ¬tool-exec loop inside.
  INV2→ `Provider.stream()` emits exactly one `StreamEvent(kind="stop")` as final event (or `kind="error"` on failure).
  INV3→ `Provider.stream()` raises ¬swallows exceptions — errors emerge as `StreamEvent(kind="error", error=exc)` for clean handling OR propagated exception (choose one pattern — see IC[2]).

**Source tag.** [source-plan architecture + refined via stress-test].

---

#### IC[2]: StreamEvent taxonomy + error-handling convention
```python
@dataclass
class StreamEvent:
    kind: Literal["token", "tool_call", "stop", "error"]
    text: str = ""                     # populated when kind="token"
    tool: dict | None = None           # populated when kind="tool_call"; shape: {"id": str, "name": str, "arguments": dict}
    stop_reason: str | None = None     # populated when kind="stop"; values: "end_turn" | "max_tokens" | "tool_use" | "max_tool_calls" | "error" | "stop"
    error: Exception | None = None     # populated when kind="error"
    # M1b observability:
    raw_event: dict | None = None      # optional raw SDK event for sidecar capture; populated only when raw capture enabled
```

**Error convention (load-bearing).** Errors ALWAYS emerge as `StreamEvent(kind="error", error=exc)` — ¬raised exceptions across async iterator boundaries. Reason: allows TurnEngine to capture partial content before error, persist `stop_reason="error"`, continue autonomous loop.

**Stop-reason taxonomy.**
  end_turn→ model chose to stop naturally.
  max_tokens→ hit max_tokens limit.
  tool_use→ model emitted tool_calls, waiting for tool results.
  max_tool_calls→ TurnEngine-enforced cap (5/turn). ¬SDK concept — TurnEngine injects this stop_reason when cap hit.
  error→ stream failed; `error` field populated.
  stop→ generic stop (fallback when SDK-specific reason unknown).

**Source tag.** [source-plan StreamEvent dataclass + agent-inference on error convention].

---

#### IC[3]: ToolSchema + ToolCallRecord
```python
@dataclass
class ToolSchema:
    name: str
    description: str
    parameters: dict                   # JSON-schema; converted per-SDK by tool_schema.py

@dataclass
class ToolCallRecord:
    turn_id: str                       # references Turn this call occurred in
    speaker: str                       # ProviderSpec.key
    provider: str                      # ProviderSpec.provider_class.__name__ or similar stable id
    tool_name: str
    arguments: dict
    ts_started: str                    # ISO 8601 UTC
    ts_completed: str
    latency_ms: int
    result: str                        # tool result as text
    result_chars: int
    error: str | None = None
    position_in_turn: int = 0          # 0-based index of this tool call within its Turn
    preceding_text: str = ""           # text content emitted by model before tool_call in this turn
```

**Invariants.**
  INV1→ `position_in_turn` is monotonic within a Turn.
  INV2→ `preceding_text` is exactly the text content from the current turn before this tool_call (may be "").
  INV3→ ¬populated until TurnEngine has fully executed + assembled the record.

**Source tag.** [source-plan ToolCallRecord + typed for load-bearing observability].

---

#### IC[4]: Canonical Message shape
```python
@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str                       # text content; tool_calls sibling when role="assistant" with tool use
    speaker: str | None = None         # ProviderSpec.key or "human"; for assistant messages identifies WHICH model
    tool_call_id: str | None = None    # populated when role="tool" (result of tool call with this id)
    tool_calls: list[dict] | None = None  # populated when role="assistant" emits tool calls; each dict: {"id", "name", "arguments"}
```

**Invariants.**
  INV1→ `role="tool"` REQUIRES `tool_call_id`. Adapter must reject otherwise.
  INV2→ `role="assistant"` with `tool_calls` MAY have `content=""` (tool-only response).
  INV3→ `speaker` populated for `assistant` role (identifies provider in multi-model sessions).

**Adapter responsibilities (pointer to message_mapping.py spec, see ADR[4]).**

**Source tag.** [source-plan design-decision #11 + H7 + agent-inference].

---

#### IC[5]: TurnEngine.advance_stream signature
```python
class TurnEngine:
    def __init__(
        self,
        policy: TurnPolicy,
        memory: MemoryHelper | None = None,   # None in M1a/b when no real tool; echo tool passed via tools arg
        metrics: MetricsCollector | None = None,
        max_tool_calls_per_turn: int = 5,
    ): ...

    async def advance_stream(
        self,
        state: ConversationState,
        tools: list[ToolSchema] | None = None,
    ) -> AsyncIterator[StreamEvent | Turn]:
        """Yields StreamEvents as they arrive; yields final Turn once turn completes.

        Invariants:
          - Yields zero or more StreamEvent(kind="token"|"tool_call") during streaming.
          - Yields exactly one StreamEvent(kind="stop") before yielding the final Turn.
          - Yields exactly one Turn at the end, with all tool_calls captured.
          - If tool_call count exceeds max_tool_calls_per_turn, forces stop_reason="max_tool_calls".
          - On error, yields StreamEvent(kind="error") and Turn with stop_reason="error".
        """
```

**Tool-exec loop invariants.**
  INV1→ Each tool_call event from provider → execute tool → append tool_result Message to working messages list → re-invoke `provider.stream(messages=updated, ...)`.
  INV2→ Loop counter increments on each provider re-invocation; at count > max_tool_calls, inject synthetic `StreamEvent(kind="stop", stop_reason="max_tool_calls")`.
  INV3→ ToolCallRecord populated between `ts_started` (just before tool.execute) and `ts_completed` (just after).

**Source tag.** [source-plan TurnEngine + agent-inference on invariants].

---

#### IC[6]: TurnPolicy protocol + concrete policies
```python
class TurnPolicy(Protocol):
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...
    # Returns None → no eligible speaker → TurnEngine halts session.

class RoundRobinPolicy:
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None:
        if not state.roster: return None
        return state.roster[len(state.turns) % len(state.roster)]

class YieldNextPolicy:
    # M1b. Parses trailing "@next:<key>" from last assistant turn content.
    # Self-nomination → fall back to RoundRobin.
    # Unknown key → fall back to RoundRobin.
    # Logs override event to metrics (yield_next_override_rate).
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...

class RandomPolicy:
    # M1b. Uniform random from roster excluding last speaker.
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...
```

**Source tag.** [source-plan TurnPolicy + refinements].

---

#### IC[7]: Persistence JSONL record shapes
See ADR[7] format-spec block. Canonical form:
  session_header→ `{schema_version, type: "session_header", session_id, mode, roster: [...], preamble_variant, ts, system_preamble}`
  turn→ `{schema_version, type: "turn", speaker, provider, content, tokens_in, tokens_out, stop_reason, ttft_ms, total_ms, ts, tool_calls: [ToolCallRecord.to_dict(), ...]}`
  tool_call→ (written inline in turn.tool_calls AND optionally as separate record for querying ease) `{schema_version, type: "tool_call", turn_id, speaker, provider, tool_name, arguments, ts_started, ts_completed, latency_ms, result, result_chars, error, position_in_turn, preceding_text}`

**Replay contract.** `persistence.replay(path) → ConversationState` reconstructs state exactly (invariant for M1a success criterion).

**Source tag.** [source-plan persistence spec + ADR[7]].

---

#### SQ[] — sub-task decomposition for M1a + M1b

**M1a — cluster A (foundation, must complete before B)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ1 | pyproject.toml, repo init, pre-commit, .gitignore (incl. `sessions/`) | implementation-engineer | 0.5h | pyproject.toml, .gitignore, README stub | ¬ |
| SQ2 | base types: Message, StreamEvent, ToolSchema, CompleteResult, ToolCallRecord, Provider Protocol | implementation-engineer | 1h | providers/base.py, providers/__init__.py | SQ1 |
| SQ3 | ProviderSpec + roster.py (M1 entries only: claude-opus-4-7 + devstral-2:123b-cloud + alternates deepseek+qwen) | implementation-engineer | 0.5h | roster.py | SQ2 |
| SQ4 | registry.py with env-key discovery | implementation-engineer | 0.5h | providers/registry.py | SQ3 |
| SQ5 | errors.py classification taxonomy (port from sigma-verify pattern, re-implement) | implementation-engineer | 0.5h | providers/errors.py | SQ2 |

**M1a — cluster B (clients + mapping, PARALLELIZABLE across engineers)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ6a | anthropic_client.py streaming path (messages.stream, extract TTFT, stop_reason, usage) | implementation-engineer-1 | 2h | providers/anthropic_client.py | cluster A |
| SQ6b | ollama_client.py streaming path (OpenAI-compat, chat.completions.create stream=True with include_usage) | implementation-engineer-2 | 2h | providers/ollama_client.py | cluster A |
| SQ7 | message_mapping.py streaming-only paths (Anthropic content↔canonical, Ollama identity) | implementation-engineer | 1.5h | providers/message_mapping.py | SQ2, SQ6a, SQ6b |

*Parallelization note.* SQ6a and SQ6b are independent (different SDKs, different files) — spawn two implementation-engineers with worktree isolation per §parallel-build-engineers pattern. SQ7 integrates after both complete.

**M1a — cluster C (orchestration)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ8 | conversation.py: Turn, ConversationState, PreambleVariant | implementation-engineer | 1h | conversation.py | SQ2 |
| SQ9 | turn_engine.py: RoundRobinPolicy + advance_stream (no tool-exec loop yet) | implementation-engineer | 2h | turn_engine.py | SQ8 |
| SQ10 | persistence.py: write_session, write_turn, replay, schema_version="1" on every record | implementation-engineer | 1.5h | persistence.py | SQ8 |
| SQ11 | cli.py: argparse, streaming tokens to stdout, session file write | implementation-engineer | 1h | cli.py | SQ9, SQ10 |

**M1a — cluster D (tests)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ12a | mock_providers.py fixture (async mock Provider w/ streaming) | code-quality-analyst | 1h | tests/fixtures/mock_providers.py | SQ2 |
| SQ12b | test_providers_base.py — Provider Protocol conformance | code-quality-analyst | 0.5h | tests/test_providers_base.py | SQ2, SQ12a |
| SQ12c | test_providers_streaming.py — per-SDK stream+usage extraction (uses live when keys present, else skips) | code-quality-analyst | 2h | tests/test_providers_streaming.py | SQ6a, SQ6b |
| SQ12d | test_message_mapping.py — round-trip streaming paths (MERGE GATE) | code-quality-analyst | 1.5h | tests/test_message_mapping.py | SQ7 |
| SQ12e | test_turn_engine.py — RoundRobin + advance_stream with mock provider | code-quality-analyst | 1h | tests/test_turn_engine.py | SQ9, SQ12a |
| SQ12f | test_conversation.py | code-quality-analyst | 0.5h | tests/test_conversation.py | SQ8 |
| SQ12g | test_persistence.py — JSONL round-trip incl. schema_version | code-quality-analyst | 1h | tests/test_persistence.py | SQ10 |

**M1a total estimate.** ~18h sequential; ~14h with SQ6a/6b parallelization.
**M1a verification** (per source-plan): live CLI run — 2 models, 5 turns, round-robin, streamed, JSONL persisted, replay reproduces transcript.

---

**M1b — cluster E (tool-schema + providers tool-use)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ13 | tool_schema.py: ToolSchema → Anthropic tool format + Ollama OpenAI-compat function format | implementation-engineer | 1h | providers/tool_schema.py | M1a complete |
| SQ14a | anthropic_client.py tool-use streaming (tool_use content blocks emit as StreamEvent(kind="tool_call")) | implementation-engineer-1 | 2h | providers/anthropic_client.py | SQ13 |
| SQ14b | ollama_client.py tool-use streaming (tool_calls delta emit as StreamEvent(kind="tool_call")) | implementation-engineer-2 | 2h | providers/ollama_client.py | SQ13 |
| SQ15 | message_mapping.py tool-use paths (Anthropic tool_use/tool_result ↔ canonical tool_calls + role="tool"; Ollama identity) | implementation-engineer | 2.5h | providers/message_mapping.py | SQ14a, SQ14b |

*Parallelization.* SQ14a/14b independent; spawn parallel.

**M1b — cluster F (TurnEngine tool-exec + policies)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ16 | TurnEngine tool-exec loop (cap 5, max_tool_calls stop, ToolCallRecord population) | implementation-engineer | 2.5h | turn_engine.py | SQ15 |
| SQ17 | YieldNextPolicy (parses @next:, self-nom fallback, unknown-key fallback) | implementation-engineer | 1h | turn_engine.py | SQ9 |
| SQ18 | RandomPolicy | implementation-engineer | 0.5h | turn_engine.py | SQ9 |
| SQ19 | echo_tool fixture (name="echo", params={"text": str}, returns text verbatim) | implementation-engineer | 0.25h | tests/fixtures/echo_tool.py | ¬ |
| SQ20 | MetricsCollector baseline (record_turn, record_tool_call, snapshot) | implementation-engineer | 1.5h | metrics.py | SQ2 |
| SQ21 | Raw event capture (sessions/raw sidecar, conditional on tool_use_reliability != "reliable" or CHATROOM_CAPTURE_RAW=1) | implementation-engineer | 1h | persistence.py + anthropic_client.py + ollama_client.py | SQ10 |

**M1b — cluster G (tests)**
| SQ | Task | Owner | Est | Files | Deps |
|---|---|---|---|---|---|
| SQ22 | test_providers_tool_use.py — per-SDK tool-call emission round-trip | code-quality-analyst | 2h | tests/test_providers_tool_use.py | SQ14a, SQ14b |
| SQ23 | test_message_mapping.py tool-use paths (MERGE GATE expansion) | code-quality-analyst | 2h | tests/test_message_mapping.py | SQ15 |
| SQ24 | test_turn_engine_tools.py — tool-exec loop, cap enforcement, ToolCallRecord fields | code-quality-analyst | 2h | tests/test_turn_engine_tools.py | SQ16, SQ19 |
| SQ25 | test_metrics.py — MetricsCollector correctness | code-quality-analyst | 0.5h | tests/test_metrics.py | SQ20 |
| SQ26 | test_persistence.py raw-sidecar expansion | code-quality-analyst | 0.5h | tests/test_persistence.py | SQ21 |
| SQ27 | test_yield_next_policy.py + test_random_policy.py | code-quality-analyst | 1h | tests/... | SQ17, SQ18 |

**M1b total.** ~22h sequential; ~18h with SQ14a/14b parallelization.
**M1b verification** (per source-plan): same CLI run with `--tool echo`; ≥1 echo round-trip per provider; ToolCallRecord fields populated incl. preceding_text + position_in_turn; raw sidecar written for devstral.

**Grand total M1a+M1b.** ~32h with parallelization. Build-track to refine in challenge round.

---

#### PM[] — pre-mortem (failure modes)

**PM[1]: message_mapping.py Anthropic adapter explodes in scope**
  likelihood→ MEDIUM-HIGH. Source plan flags as "elevated-risk". Independent reasoning confirms (ADR[4] analysis).
  reasoning→ Anthropic `tool_use` inside assistant content blocks + `tool_result` inside user content blocks, with IDs linking them. Splitting into OpenAI sibling form requires:
    1. Assistant msg with [text, tool_use, text, tool_use] → OpenAI assistant msg with content="text1 text2" + tool_calls=[call1, call2] (lossy — ordering of text interleaving can't round-trip in OpenAI flat form without a convention).
    2. User msg with [tool_result, tool_result] → 2 separate OpenAI role="tool" msgs with matching tool_call_id each.
  detection→ test_message_mapping.py round-trip tests fail; OR production run produces malformed SDK payload → Anthropic SDK raises ValidationError.
  mitigation→ (a) Round-trip tests as MERGE GATES. (b) Canonical Message adds optional `content_blocks: list[dict] | None` field for Anthropic round-trip fidelity when needed (fallback for elevated-fidelity cases). (c) Document known-lossy cases explicitly in message_mapping.py docstring.
  trigger-for-escalation→ if ≥2 round-trip test fixtures fail at SQ15 boundary, escalate to architecture revision — consider Anthropic-native canonical form for assistant messages only (hybrid canonical).

**PM[2]: Ollama OpenAI-compat tool_calls reliability on devstral-2:123b**
  likelihood→ MEDIUM. `tool_use_reliability="unknown"` per roster; first empirical test in M1b.
  reasoning→ Mistral's function-calling training on Devstral lineage is documented but the Ollama cloud deployment layer adds a serialization round-trip. Historical pattern: Ollama OpenAI-compat on function_calling has intermittent malformed-JSON issues when model generates nested objects.
  detection→ M1b integration test: echo tool round-trip. Either succeeds (upgrade to "reliable" in roster) or malformed tool_calls JSON (stays "unknown"→downgrade to "nominal").
  mitigation→ Raw event capture (ADR[6]) default-on for this provider. Raw log surfaces WHICH of {declined | malformed | SDK-swallowed} is the failure mode.
  trigger-for-escalation→ if echo round-trip fails 3/3 attempts across 3 different prompt phrasings, flag `tool_use_reliability="none"` for devstral-2:123b and switch M1 seed pair's Ollama to `deepseek-v3.2:cloud` (alternate). Raw capture evidence attached to escalation.
  !M1b-scope question→ is mitigation sufficient? **ASSESSMENT: YES for M1b.** Raw capture is observability, not recovery. M1b success criterion is "≥1 round-trip per provider" — if devstral fails all attempts, we swap providers per escalation trigger. M1 is research milestone; documenting `tool_use_reliability="none"` on devstral IS a successful M1 outcome.

**PM[3]: Streaming + async + tool-exec state-machine bug**
  likelihood→ MEDIUM. Source plan defers Streamlit concurrency shim to pre-M2 2h prototype. But M1b's own TurnEngine tool-exec loop is an async state-machine with known sharp edges.
  reasoning→ Tool-exec loop interleaves: async-generator consumption → sync tool call → async-generator re-entry. Risks: (a) partial buffer from provider.stream() not flushed before re-invocation; (b) ToolCallRecord ts_started/ts_completed captured under wrong event-loop context; (c) exceptions during tool execution not surfaced back into StreamEvent(kind="error") correctly.
  detection→ test_turn_engine_tools.py SHOULD catch (a) + (b). (c) needs adversarial test: tool that raises mid-execution.
  mitigation→ (a) IC[5] INV1-INV3 explicit. (b) Use `monotonic_ns()` for latency, not wall clock. (c) Add `test_tool_exec_error_propagation` test (implementation-engineer's task in SQ16).
  trigger-for-escalation→ if >1 async-state-machine bug surfaces in SQ24 review, pause and re-scope: consider simplifying tool-exec to sync `await tool_coro()` inside the async generator (already the default but make it explicit policy).
  !agreement-with-source-plan→ source plan defers concurrency shim to M2 2h prototype. DO I AGREE deferral is safe for M1a/b? **ASSESSMENT: YES.** M1a/b tool-exec is async-in-async (provider.stream inside TurnEngine.advance_stream); Streamlit async-to-sync is a different problem (UI thread ↔ async backend). They are orthogonal. Deferring Streamlit shim does NOT weaken M1b's own state-machine correctness.

---

#### XVERIFY (advisory)

**Recommendation.** XVERIFY on ADR[3] (tool-exec loop location) — highest-stakes decision that constrains whole TurnEngine shape.

**Proposed call.**
```
mcp__sigma-verify__cross_verify(
  finding="Tool-exec loop belongs in TurnEngine (orchestration layer), not Provider (SDK wrapper). Provider.stream() is exactly one SDK call; TurnEngine orchestrates tool_call → execute → append tool_result Message → re-invoke stream, with 5-call cap per turn.",
  context="Building multi-model chatroom research instrument. Each Provider wraps one SDK (Anthropic messages.stream OR Ollama OpenAI-compat chat.completions.create stream=True). TurnEngine is the chatroom's orchestrator. ToolCallRecord captures position_in_turn + preceding_text + latency_ms which require conversation-level state."
)
```

**Expected verifiers.** openai gpt-5.4, google gemini-3.1-pro-preview, anthropic claude-opus-4-6. Ollama verifiers weaker — skip.

**Status.** DEFERRED to DA round — XVERIFY will be triggered if DA challenges ADR[3] with counter-evidence. Not triggered pre-challenge to conserve budget.

**XVERIFY-fallback.** If ΣVerify rate-limits or any provider fails, write `XVERIFY-FAIL[...]` to workspace; continue with [agent-inference] + [industry-pattern] as source tags.

---

#### DB[] — dialectical bootstrapping on top-3 highest-conviction findings

**DB[ADR1 — purpose-built providers].**
  (1) initial: purpose-built clearly correct given sync/async mismatch with sigma-verify.
  (2) assume-wrong: what if subclassing saves more than it costs?
  (3) strongest-counter: `_extract_content` is non-trivial + env-discovery pattern is valuable. Inheriting means bugs in sigma-verify propagate as fixes.
  (4) re-estimate: still purpose-built. Counter addressed by copy-with-attribution of specific functions.
  (5) reconciled: ADR[1] stands; explicitly specify "copy-with-attribution of `_extract_content` + env var naming convention" in implementation.

**DB[ADR3 — tool-exec loop in TurnEngine].**
  (1) initial: separation of concerns mandates TurnEngine location.
  (2) assume-wrong: what if Anthropic's agentic tool_use SDK mode is actually the right shape?
  (3) strongest-counter: Anthropic (and others eventually) offer first-party agent-mode SDKs that handle the loop. If we wrap them, we have two different code paths (agent-mode providers vs manual-loop providers).
  (4) re-estimate: still TurnEngine. Agent-mode SDKs hide tool_call events from observability — incompatible with ToolCallRecord research goal. We'd have to disable agent-mode even if available.
  (5) reconciled: ADR[3] stands; add explicit note "if SDK offers agent-mode, disable it; we want observability over convenience."

**DB[ADR4 — message_mapping OpenAI-shaped canonical].**
  (1) initial: OpenAI-shape is right (majority-provider argument).
  (2) assume-wrong: what if Anthropic-shape canonical saves more total adapter work?
  (3) strongest-counter: Anthropic's content-block model is more expressive (ordered mixed text+tool_use). Canonicalizing on it retains information that OpenAI-shape loses (interleaving).
  (4) re-estimate: OpenAI-shape still correct for M1 scope (only two adapters, M1 doesn't stress interleaving). BUT acknowledge fidelity limitation explicitly.
  (5) reconciled: ADR[4] stands; PM[1] documents interleaving loss as known constraint; optional `content_blocks` escape-hatch field on Message if needed in M2+.

---

#### Analytical hygiene summary

**§2a positioning/consensus.** All 8 ADRs CONSENSUS with source plan. No divergence in load-bearing calls — evidence confirms source plan's hypotheses. Independent stress-test adds specific invariants (IC[2] error convention, PM[1] interleaving-loss, ADR[5] revision hook, ADR[6] raw-capture env override).

**§2b calibration/precedent.** All 8 ADRs have industry precedent (langchain, autogen, Anthropic docs, OpenTelemetry, sigma-mem prior).

**§2c cost/complexity.** All 8 ADRs cost-justified for M1a/b scope. Highest-cost is ADR[4] (message_mapping merge-gate tests); cost justified by elevated-risk status.

**§2e premise viability.** All H[] premises viable. H5 (60% budget) adds revision hook for small-context providers in M1c.

**§2d source tags.** Every ADR carries source tags: [code-read] dominant (sigma-verify clients.py read in full), [agent-inference] supplementing, [source-plan] anchoring, [independent-research] where SDK behaviors are documented.

**Load-bearing findings identified.** ADR[1-4] are load-bearing (architectural constraints). ADR[5-8] are configuration (lower stakes but still explicit).

---

### tech-architect R2 responses

!scope:R2 delta post-DA + post-build-challenges. R1 ADRs/ICs/SQs stand except where explicitly revised below. 9 priority items (XVERIFY gap-doc replaces XVERIFY call per infra-block).

---

#### DA[#1]: defend-with-revision — DB re-runs on ADR[3] + ADR[4] with stronger counters

**DB[ADR3] RE-RUN with stronger counter "tool-exec in Provider matches LangChain AgentExecutor pattern":**
  (1) initial: tool-exec loop in TurnEngine per separation-of-concerns.
  (2) assume-wrong: LangChain AgentExecutor wraps LLM client + runs agent loop inside. autogen GroupChat similar. Most teams KEEP agent-loop bound to LLM client. Provider-owned-loop is the industry mode, not exception.
  (3) strongest-counter (revised per DA[#1]): if industry convention is Provider-owned agent loop, TurnEngine-location is the speculative divergence. Our IC[1] stateless-Provider invariant IS ALREADY the choice that forces TurnEngine-location — but DA[#1] reads that as self-justification circularity. Counter-weight: LangChain AgentExecutor COUPLES SDK choice with agent policy; every SDK bump ripples through agent code. Our 13-provider roster makes that coupling O(N) maintenance. Provider-owned-loop is industry mode when N=1 SDK; TurnEngine-location is correct when N>3 with observability mandate.
  (4) re-estimate: ADR[3] holds on multi-provider grounds, NOT on generic separation-of-concerns. Reconciled rationale is STRONGER after re-run, not weaker. LangChain counter is real but addresses N=1 case.
  (5) reconciled: ADR[3] stands. Reconciled rationale ADDS: "industry precedent (LangChain AgentExecutor) is Provider-owned for N=1 SDK; our N=13 + observability-mandate forces TurnEngine-location. If chatroom were single-SDK, ADR[3] flips." BELIEF updated below.

**DB[ADR4] RE-RUN with stronger counter "ALT3 union-type canonical loses zero fidelity":**
  (1) initial: OpenAI-shaped canonical per majority-provider argument.
  (2) assume-wrong: ALT3 from my own ALT-list — canonical as union type `Message = OpenAIMessage | AnthropicMessage | GeminiMessage` — preserves EVERY shape losslessly. Why rejected with so little analysis?
  (3) strongest-counter (revised per DA[#1]): union-type canonical means JSONL persistence serializes TYPE-TAGGED records (one of N shapes per message). Replay branches on type-tag. TurnEngine must handle N shapes. Multi-model conversation REQUIRES cross-SDK message interop (model A emits Anthropic-shape, model B receives — must convert). Union-type doesn't eliminate conversion, it just pushes it to consumption points. Same adapter surface, distributed instead of centralized.
  (4) re-estimate: ALT3 DOES preserve fidelity but at the cost of N^2 adapter pairs (A→B, A→Gemini, B→Gemini, etc.) vs OpenAI-shape's N (each SDK ↔ canonical). For 4 SDKs: 12 vs 4. Also defeats replay determinism (type-tag drift across schema versions). Fidelity is preserved; complexity is worse.
  (5) reconciled: ADR[4] holds BUT reconciled rationale now explicitly addresses ALT3. DA[#1] concern about weaker-counter-than-available is legitimate — R1 DB was pro-forma. This R2 DB is stronger; outcome unchanged but reasoning genuine.

**BELIEF updates from DB re-runs (written to ## belief-tracking below):**
  - BELIEF[ADR3] 0.88 → **0.84**. Counter-argument (LangChain pattern) is real industry mode; our case is defensible on N>3 grounds but not on generic SoC.
  - BELIEF[ADR4] 0.80 → **0.70** after DA[#2] math AND this re-run. See DA[#2] for composition reasoning.

|source:[DA[#1] L1683-1700 + own R1 ALT-lists L96-98/177-181/219-223 + agent-inference on industry-precedent weight]

---

#### DA[#2]: concede-with-revision — BELIEF[ADR4] math + escape-hatch lock

DA[#2] math is correct. BELIEF[ADR4]=0.80 with PM[1] L=0.55 for the load-bearing failure mode is Bayesian-inconsistent. Two paths to resolution:

(a) Lower BELIEF to reflect unmitigated PM[1] likelihood.
(b) Lock escape-hatches INTO ADR[4] proper (not PM[1] mitigation).

**Choosing (b) + partial (a):** lock BOTH escape-hatches into ADR[4] proper + drop BELIEF to reflect residual risk after locking.

**Locked into ADR[4] proper (was PM[1] mitigation):**
  - `Message.preceding_text_per_tool_call: list[str] | None = None` — NEW canonical field per impl-eng BC#5 (R1) + BC[R2-clarify-1] (R2). Populated by Provider when reconstructing final_message from interleaved Anthropic content-blocks. Enables round-trip fidelity for text-before-tool-use ordering.
  - `Message.content_blocks: list[dict] | None = None` — escape-hatch for cases `preceding_text_per_tool_call` doesn't cover (tool_result with image content M4+, cache_control markers, other Anthropic-only features). Default None for M1a/b.
  - Round-trip tests as MERGE GATES — **locked into ADR[4]**, not PM[1]. Per cqa BC[cqa-1] F1-F8 + impl-eng BC#14 direction-asymmetry + DA[#6] hand-golden-SDK-fixtures (see DA[#6] response below).

**Updated BELIEF[ADR4]:** 0.80 → **0.70**.
  Reasoning: with escape-hatches locked + hand-golden fixtures as merge gate, P(PM1-fires-and-escapes-mitigation) drops from ~0.55 to ~0.25. 1 - 0.25 = 0.75 upper bound; conservative 0.70 acknowledges Gemini adapter (M1c) is not yet validated.

|source:[DA[#2] L1704-1716 + impl-eng BC#5 R1 + BC[R2-clarify-1] R2 + cqa BC[cqa-1] F1-F8 + cqa R2-Δ-1 DA6 hand-goldens]

---

#### DA[#3]: XVERIFY — NOT-ATTEMPTED, infrastructure-blocked (documented gap)

```
XVERIFY[ADR3 tool-exec-loop-location]: NOT-ATTEMPTED — infrastructure-blocked
reason: sigma-verify cross_verify + verify_finding hang pattern observed 3x this session (DA-r1, TA-r1, TA-r2). Per feedback/failures memory: cross_verify multi-provider fanout appears to block on slowest provider with no per-provider timeout.
gap-status: documented, not silently ignored per §2h
compensating-factor: ADR[3] has cross-agent consensus (tech-architect ADR3, impl-eng R1+R2 did NOT challenge ADR3 location, cqa EG1-EG5 tests state machine at this layer, ui-ux IC-flag[5] compatible with this layer)
remediation: post-C1 troubleshoot session to fix mcp__sigma-verify cross_verify timeout + per-provider partial-result return
```

**Flag ALSO added to ## gate-log at end of R2 write.** Not silently skipped per §2h; escalated to user via convergence summary.

Additional compensating evidence for ADR[3] without XVERIFY:
  - 4-agent read of ADR[3] location: impl-eng did not challenge location (only parallel tool-call INV4 + final_message reconstruction on IC[2]), cqa built test-coverage ON TOP of location assumption (EG1-EG5 state machine tests tool-exec layer), ui-ux IC-flag[5] composed compatibly (new StreamEvent emitted BY TurnEngine post-exec — affirms TurnEngine-owns-loop).
  - DB[ADR3] re-run (DA[#1] response above) with LangChain-AgentExecutor counter — ADR stands on N>3 + observability grounds.
  - Industry multi-provider precedent: autogen GroupChat separates agent-orchestrator from LLM-client; crewai similar pattern. N>1 agent-orchestrators tend to location-separate.

|source:[failures memory cross_verify hang pattern this session x3 + cross-agent convergence none-challenge-location + DB[ADR3] re-run]

---

#### DA[#4]: gold-plating 3 items — responses

**GP[1] registry.py (concede).** SQ4 registry.py for 2 providers IS gold-plating for M1a/b scope. Simplify: replace SQ4 separate file with a **5-line dict** in roster.py + `available()` helper in same file. Delete `providers/registry.py` from M1a/b file list. Create registry.py when M1c adds ≥5 providers and the dict grows beyond readability.

**SQ4 revised:**
  SQ4→ "providers discovery: PROVIDERS dict + available() helper added to roster.py" | owner:implementation-engineer | est:0.25h (was 0.5h) | files:roster.py (¬providers/registry.py) | deps:SQ3

**File list updated:** `providers/registry.py` REMOVED from M1a/b file list. Recreate in M1c.

Savings: -0.25h code + -1 test file (no test_registry.py needed) ≈ -0.5h total.

**GP[2] Provider.complete() (concede).** cross-agent consensus (DA + cqa BC-cqa-8 D1 + impl-eng R2-Δ-3 confirm). complete() has ZERO M1a/b callers. Defer complete() method from IC[1] Protocol entirely until a caller materializes.

**IC[1] revised (see ## interface-contracts below):**
  - `complete()` REMOVED from Protocol signature for M1a/b.
  - `CompleteResult` dataclass REMAINS in base.py (might be used for future sync-paths) — type only, no wiring.
  - When M1c or caller needs it, add complete() method + CompleteResult population back to Protocol.

Savings: -0 LOC eliminated (it was a stub) but smaller mock-Provider surface (-0.25h SQ12a fidelity).

**GP[3] PreambleVariant (compromise per ui-ux R2 concede+compromise).** ui-ux already compromised: M1a/b ships **type + logged field + ONE rendering (identity-aware)**. Accept ui-ux compromise:
  - IC[4] Message.preamble_variant type remains as `Literal["neutral", "identity-aware", "research-framed"]` — type-level only.
  - IC[7] `preamble_variant` field persisted from day-1 per source-plan L207.
  - SQ8 renders identity-aware variant ONLY for M1a/b. No neutral or research-framed rendering code.
  - M2 picker activates remaining variants incrementally per ui-ux R2 IX[5] revised.

Savings: SQ8 -0.25h on variant rendering (ui-ux noted net impact already).

|source:[DA[#4] GP1-GP3 L1740-1750 + cqa BC-cqa-8 D1/D3/D4 + impl-eng R2-Δ-3 + ui-ux R2 DA4-GP3 concede]

---

#### DA[#5]: forward-plan H2 decompose (accept + apply to other hooks)

Accept DA[#5] decomposition principle: research-vs-code split at plan phase.

**H2 decomposed (M1c revision hook):**
  H2-code→ M1c SDK implementation scope unchanged (openai_client.py + google_client.py + message_mapping Gemini + tool_schema Gemini + roster expansion). Timeline: 1-2 weeks.
  H2-research→ Provider reliability sweep (10 Ollama + 3 cloud SDKs × 1 echo test each). **Own deliverable, own phase timeline.** Runs IN PARALLEL to H2-code. Produces: reliability matrix updated in roster.py empirically. Estimate: 0.5-1 day empirical work + 0.5 day analysis write-up = ~1 day. Can be parallelized AFTER M1c-code ships SDK support.

**Other forward-plan hooks — apply decomposition check:**
  H1 (context calibration): pure research trigger → pure code action. Well-formed. No decomposition needed. ✓
  H3 (Anthropic message_mapping fidelity loss → content_blocks escape-hatch): pure code (escape-hatch is ALREADY locked per DA[#2] response above — hook now fires as "confirm fidelity holds," not "add field post-hoc"). Simplified.
  H4 (Streamlit async→sync-gen feasibility): pure research in 2h prototype → pure scope decision. Well-formed. ¬code-track inside. ✓ (ui-ux owns)
  H5 (ToolCallRecord preceding_text expensive): measurement-first → deferred-population code. Well-formed. ✓
  H6 (MetricsCollector baseline insufficient): empirical → scope expansion. Well-formed. ✓
  H7 (user pins research question): user-decision → scope lock. UD#5 ALREADY RESOLVED (memory-invocation coherence). Hook fires retroactively; no future trigger. **Mark resolved.**
  H8 (M4 scope dep on M3 research-Q): depends on UD#5 outcome. Resolved: embeddings CORE per memory-invocation coherence framing. Update H8 status.

**Forward-plan updated (see ## forward-plan section below) with:**
  - Q3 cadence checkpoint per UD#1 (user-decision-1 acceptance) — scheduled BETWEEN M1a ships and M1c scope locks. Concrete marker: "CHECKPOINT-Q3-A" in forward-plan.
  - devstral→deepseek escalation policy per UD#2 accepted form (see DA[#9] item below for full policy spec).
  - H2 decomposed into H2-code + H2-research parallel tracks.
  - H7/H8 resolved by UD#5; marked.

|source:[DA[#5] L1764-1774 + UD#1 + UD#2 + UD#5 + impl-eng BC#15 R1 parallelization recommendation]

---

#### DA[#6]: merge-gate test strategy — accept 3-tier strategy + cqa hand-goldens

Accept impl-eng R2 3-tier strategy + cqa R2-Δ-1 hand-golden SDK fixtures. Compositional:

**Tier 1 (hand-golden outbound):** `tests/fixtures/anthropic_golden.py` + `openai_golden.py` with pre-computed SDK payloads. Assert `to_sdk(canonical) == SDK_golden_expected`. Catches: wrong field names, dropped content-blocks, mis-ordered interleaving. (cqa R2-Δ-1 G-F1 + G-F2)

**Tier 2 (hand-golden inbound):** `tests/fixtures/anthropic_responses_golden.py` + `openai_responses_golden.py` with pre-computed SDK response shapes. Assert `from_sdk(SDK_response_golden) == canonical_expected`. Catches: response parsing bugs, inbound field-loss. (cqa R2-Δ-1 G-F3 + impl-eng BC#14 direction-asymmetry)

**Tier 3 (round-trip):** `from_sdk(to_sdk(msg)) == msg` — DERIVATIVE baseline. Kept as smoke-level sanity check; not primary gate. (ADR[4] R1 baseline; demoted)

**Merge gate tests in SQ12d + SQ23 organized by tier:**
  SQ12d (streaming-only, M1a) — owns Tier 1 text-only fixtures + Tier 2 text-only + Tier 3 smoke. Est: 1.5h → **2.5h** per cqa R2-Δ-1.
  SQ23 (tool-use, M1b, MERGE GATE) — owns Tier 1 tool-use fixtures (anthropic content-block interleaving per cqa F1+F3+F4+F6) + Tier 2 tool-use responses + Tier 3 smoke. Est: 2h → **3.5h** per cqa R2-Δ-1.

**ADR[4] test spec revised:** "MERGE GATE has 3 tiers: hand-golden outbound (Tier 1), hand-golden inbound (Tier 2), round-trip smoke (Tier 3 DERIVATIVE). Tier 1+2 fixtures are HAND-COMPUTED, not machine-round-tripped. Adapter must pass Tier 1 AND Tier 2 AND Tier 3 to merge."

|source:[DA[#6] L1778-1788 + cqa R2-Δ-1 hand-goldens + cqa BC[cqa-1] F1-F8 + impl-eng BC#14 direction-asymmetry + impl-eng R2 accept-1]

---

#### DA[#7]: IC[2] dual additions — accept both (4-agent UNIFIED position)

Accept both additions to IC[2] per 4-agent cross-agent consensus (impl-eng BC#2+BC#3, cqa BC-cqa-11 EG1-EG5, ui-ux IC-flag[5]). **CONFLICT[1] resolved: both are compositional, separate tool-exec loop phases, not redundant.**

**IC[2] revised StreamEvent (see ## interface-contracts below):**

```python
@dataclass
class StreamEvent:
    kind: Literal["token", "tool_call", "stop", "tool_result", "error"]  # +tool_result
    text: str = ""                     # populated when kind="token"
    tool: dict | None = None           # populated when kind="tool_call"; shape: {"id": str, "name": str, "arguments": dict}
    stop_reason: str | None = None     # populated when kind="stop"
    final_message: Message | None = None  # NEW: populated when kind="stop" AND stop_reason="tool_use" — reconstructed canonical assistant Message (impl-eng BC#3 + R2-clarify-1)
    tool_call_record: ToolCallRecord | None = None  # NEW: populated when kind="tool_result" — FULL ToolCallRecord with latency_ms+result+position_in_turn+preceding_text (ui-ux IC-flag[5])
    error: Exception | None = None
    raw_event: dict | None = None
```

**IC[2] event grammar (new — for cqa EG1 conformance tests):**
```
token* → (tool_call+ → stop(stop_reason="tool_use", final_message=M) → tool_result+)* → token* → stop(stop_reason∈{end_turn,max_tokens,max_tool_calls,error})
```

**IC[2] new invariants:**
  - INV4→ Multiple `kind="tool_call"` events MAY be emitted within one Provider.stream() call when model requests parallel tools. Each event carries exactly one tool dict. TurnEngine accumulates into Turn.tool_calls. (impl-eng BC#2)
  - INV5→ When stop_reason="tool_use", Provider MUST populate `final_message` with the reconstructed canonical assistant Message (content = concatenated text blocks, tool_calls = list, preceding_text_per_tool_call = populated for Anthropic interleaved). (impl-eng BC#3)
  - INV6→ `kind="tool_result"` events are emitted ONLY BY TurnEngine (never by Provider). Emitted after each tool execution completes, before re-invoking Provider.stream(). `tool_call_record.tool_call_id` correlates with a prior `kind="tool_call"` event in the same turn. (ui-ux IC-flag[5] + cqa EG4)
  - INV7→ Orphan `kind="tool_result"` (no matching prior tool_call) is a contract violation; TurnEngine MUST raise. (cqa EG4)

**Phase-by-phase sequencing in TurnEngine.advance_stream:**
  1. Call provider.stream() → yield tokens, tool_calls, final stop(tool_use, final_message).
  2. Append final_message to state.messages (enables next provider call to see assistant-with-tool_use).
  3. For each tool_call accumulated: execute, build ToolCallRecord, yield StreamEvent(kind="tool_result", tool_call_record=...).
  4. Append tool_result Messages (one per tool_call) to state.messages.
  5. Re-invoke provider.stream() → loop back to (1). Or if tool-call count ≥ max_tool_calls, see DA-related IC[5] INV2 revision below.

**IC[5] INV2 revised (impl-eng BC#4):**
INV2 revised: "When tool-call count reaches max_tool_calls_per_turn (default 5), after executing the Nth tool and yielding its tool_result, TurnEngine re-invokes provider.stream(messages=updated, tools=None) ONE FINAL TIME to allow model to emit text explanation. Yields resulting tokens + final stop. Overrides final stop_reason to 'max_tool_calls' regardless of what model emits."

**Source tag on IC[2] revisions:** [cross-agent 4-agent-convergence: impl-eng BC#2+BC#3+R2-NEW-2 + cqa BC-cqa-11 EG1-EG5 + ui-ux IC-flag[5] + DA[#7] CONFLICT[1]] + [agent-inference on phase-by-phase sequencing]

|source:[DA[#7] L1823-1833 + impl-eng BC#2/BC#3 R1 + BC[R2-clarify-1] + cqa BC-cqa-11 + ui-ux IC-flag[5] + impl-eng BC#4 R1]

---

#### DA[#8]: provider statelessness INV4+INV5 (accept per impl-eng R2-NEW-2)

Accept impl-eng R2-NEW-2 resolution. SDK context-manager semantics confirmed: `anthropic.AsyncAnthropic.messages.stream()` returns `MessageStreamManager`, `openai.AsyncOpenAI.chat.completions.create(stream=True)` returns `AsyncStream` — both have WITHIN-CALL reconstruction state, flushed at context exit. **Provider IS stateless-per-call per IC[1] invariant; no violation.**

**IC[1] invariants revised (new INV4 + INV5 per impl-eng R2):**
```
INV1→ Provider.stream() = exactly one SDK call; ¬tool-exec loop inside.
INV2→ Provider.stream() emits exactly one StreamEvent(kind="stop") as final event (or kind="error" on failure).
INV3→ Provider.stream() error convention: ALWAYS emerge as StreamEvent(kind="error", error=exc) — ¬raised exceptions across async iterator boundaries. (LOCKED — resolves cqa BC-cqa-7 contradiction with prior "choose one" language; see DA-adjacent note below.)
INV4→ Provider.stream() reconstruction state is WITHIN-CALL only; across-call state forbidden. SDK context-manager semantics MUST be used for connection lifecycle. (impl-eng R2-NEW-2)
INV5→ Provider.stream() MUST support early-termination cleanup via async-generator close() propagation to underlying SDK context. (impl-eng R2-NEW-2 + cqa BC-cqa-3 T7)
```

**Resolves cqa BC-cqa-7 as DA[#8]-adjacent:** IC[1] INV3 locked to "ALWAYS emerge" per IC[2]. Deleted "choose one" language. Parallel engineers on SQ6a/SQ6b have unambiguous contract.

**SQ14a/SQ14b estimate impact (impl-eng R2 verified):**
  - SQ14a: no estimate change. 2.5h (revised R1) stands. `anthropic.MessageStreamManager.get_final_message()` built-in.
  - SQ14b: no change IF SQ6c passes. 2h → **+0.5h CONDITIONAL** only if SQ6c fails and we pivot to ollama pypi AsyncClient (which doesn't use context manager — caller owns cleanup).

|source:[DA[#8] CONFLICT[2] L1829-1831 + impl-eng BC[R2-NEW-2] L1262-1284 + cqa BC-cqa-7 L1441-1447 + cqa BC-cqa-3 T7]

---

#### DA[#9]: UD#1 + UD#2 baked into forward-plan

**UD#1 Q3 cadence checkpoint:** scheduled in forward-plan.
  **CHECKPOINT-Q3-A** (new): AFTER M1a ships empirical data + BEFORE M1c scope-lock. Revisit forward-plan H1-H8, reconcile any revision-hook firings against empirical M1a/b findings, user decision on Textual-TUI-vs-Streamlit (UD#4 pre-M2 STEP-3b output), confirm M1c scope (code + research per H2-decompose). Estimated interval: ~2 weeks post-M1a ship. Output: revised forward-plan locked for M1c execution.

**UD#2 devstral→deepseek escalation policy (accepted form: (c) manual-M1b-auto-M1c+ per impl-eng R2):**

```
ESCALATION POLICY (devstral-2:123b tool_use_reliability):

M1b — MANUAL escalation (human-gated)
  trigger-1: devstral echo round-trip fails 3/3 attempts × 3 prompt phrasings → reliability="none" → OPERATOR swaps to deepseek-v3.2:cloud via --models CLI flag. Raw capture evidence attached to roster.py update.
  trigger-2: devstral echo round-trip produces 1-2/3 malformed tool_calls → reliability="nominal" → KEEP devstral; annotate in roster.py.
  trigger-3: devstral echo round-trip 0/3 fail + 3/3 well-formed → reliability="reliable" → LOCK in roster.py.

  CODE IMPACT: none. ollama_client.py is model-agnostic; PROVIDERS dict in roster.py receives manual reliability update. persistence.py captures raw events per SQ21 (ADR[6]). Operator decides; system doesn't auto-swap.

M1c+ — AUTOMATIC escalation (code-gated, FUTURE)
  When: post-M1c, empirical reliability data across 10+ providers enables baseline comparison.
  What: new SQ (M1c or later) — `providers/escalation.py` detects N malformed tool_calls in session → flags for swap. Initially advisory (logs + UI warning); operator confirms swap. Full auto-swap deferred to M3+.

SQ21 raw capture works identically across Cases A + B; no mid-escalation code path change needed in M1b.
```

Written to forward-plan under M1c section + embedded in PM[2] trigger expansion (see below).

**PM[2] updated:** trigger-for-escalation expanded with quantitative thresholds per policy above.

|source:[DA[#9] + UD#1 L2108 + UD#2 L2110 + impl-eng BC[R2-clarify-2] UD#2 manual-vs-automatic + PM[2] R1]

---

### BC batch responses (impl-eng + cqa)

!scope: respond to all impl-eng R1 BC#1-15 + R2 delta (4 items) + cqa R1 BC-cqa-1 through -11 + EC1-5 + R2 delta (4 items). Many cross-reference DA responses above.

#### impl-eng BC#1-15 (R1) + R2 delta

**BC[#1-impl-eng] Ollama /v1 streaming+tool_calls unverified — SQ6c smoke test: ACCEPT.**
New SQ6c added: "Ollama cloud /v1 streaming+tool_calls smoke test — AsyncOpenAI(base_url=ollama-cloud-v1) stream=True + minimal tool def on devstral-2:123b-cloud; confirm tool_calls arrive in delta stream. If fail: pivot to ollama pypi AsyncClient OR constrain M1b tool-use to Anthropic-only. BLOCKS SQ14b." Est: 0.25h, owner:implementation-engineer, deps:cluster-A-complete. |source:[impl-eng BC#1 + DB top-1]

**BC[#2-impl-eng] IC[2] INV4 parallel tool_calls: ACCEPT.** Locked into IC[2] INV4 above (DA[#7] response). |source:[impl-eng BC#2 + DA[#7]]

**BC[#3-impl-eng] IC[5] assistant-message reconstruction via final_message on stop: ACCEPT.** Locked into IC[2] INV5 above (DA[#7] response). |source:[impl-eng BC#3 + DA[#7] + impl-eng R2-NEW-2]

**BC[#4-impl-eng] IC[5] INV2 max_tool_calls final-response: ACCEPT.** IC[5] INV2 revised above (DA[#7] response). +1 SDK call per max-hit turn; preserves final-text invariant. Test impact: cqa EG5 covers. |source:[impl-eng BC#4 + DA[#7]]

**BC[#5-impl-eng] ADR[4] interleaved-content lossiness + preceding_text_per_tool_call: ACCEPT as ADR[4] field.** Locked into ADR[4] proper via DA[#2] response (Message.preceding_text_per_tool_call is NEW canonical field). PM[1] mitigation list updated: (d) preceding_text_per_tool_call stored per-tool-call on canonical Message. |source:[impl-eng BC#5 + DA[#2]]

**BC[#6-impl-eng] SQ7/SQ15/SQ23 estimates: REVISE.** SQ7: 1.5h→2h. SQ15: 2.5h→4h. SQ23: 2h→3.5h (per DA[#6] + cqa hand-goldens, stricter than impl-eng's 3h). |source:[impl-eng BC#6 + cqa R2-Δ-1]

**BC[#7-impl-eng] SQ8 preamble rendering vs field: CLARIFY + split.** system_preamble is a COMPUTED function (not pre-rendered field). Split SQ8 into SQ8a (dataclasses, 0.5h) + SQ8b (preamble rendering, identity-aware only per DA[#4] GP3, 0.25h). Total 0.75h (was 1h). Savings from GP[3] reduction offsets. |source:[impl-eng BC#7 + DA[#4] GP[3] + cqa BC-cqa-8 D4]

**BC[#8-impl-eng] SQ9 turn_engine M1a estimate: REVISE.** SQ9: 2h→2.5h per impl-eng per-invariant accounting. |source:[impl-eng BC#8]

**BC[#9-impl-eng] SQ10 persistence replay contract ambiguity: CLARIFY + ADR[7] invariants.** Add to ADR[7]:
  - INV-replay-1: replay skips malformed trailing lines with warning log (partial-flush graceful).
  - INV-replay-2: partial turn records (stop_reason="error") ARE INCLUDED in replayed state.
  - INV-replay-3: session_header MUST be valid first line; if missing, replay raises CorruptedSessionError.
SQ10b added: "replay robustness tests — malformed trailing line, missing header, crash-mid-turn" (0.5h, owner:code-quality-analyst, deps:SQ10).
|source:[impl-eng BC#9 + cqa BC-cqa-4 J3+J5]

**BC[#10-impl-eng] SQ13 tool_schema.py: ACCEPT 1h.** JSON-schema drift between SDKs is light-validation testable in 1h. |source:[impl-eng BC#10]

**BC[#11-impl-eng] SQ14a anthropic_client tool-use streaming: REVISE.** 2h→2.5h per impl-eng per-event-type accounting. |source:[impl-eng BC#11]

**BC[#12-impl-eng] SQ14b ollama_client tool-use streaming: CONDITIONAL.** Block SQ14b on SQ6c outcome. Add ADR note: "Ollama provider transport (openai-SDK vs ollama-SDK) chosen empirically by SQ6c." Est stands 2h if /v1 path (default); +0.5h if ollama-SDK pivot. |source:[impl-eng BC#12]

**BC[#13-impl-eng] PM[2] escalation thresholds: REVISE.** PM[2] trigger-for-escalation updated per UD#2 policy (DA[#9] response above). Thresholds: 3/3 fail → reliability="none" → swap. 1-2/3 malformed → "nominal" → keep+flag. 0/3 fail → "reliable" → lock. Also: SQ6c TESTS BOTH devstral-2:123b AND deepseek-v3.2:cloud pre-SQ14b commit; pick better pair. |source:[impl-eng BC#13 + DA[#9]]

**BC[#14-impl-eng] message_mapping direction asymmetry: ACCEPT.** Combined with cqa R2-Δ-1 hand-goldens in 3-tier strategy (DA[#6] response). |source:[impl-eng BC#14 + DA[#6]]

**BC[#15-impl-eng] M1c H2 2-3x scope multiplier: ACCEPT + decompose.** H2 decomposed into H2-code + H2-research per DA[#5] response above. M1c-code 1-2w stands; M1c-research own deliverable parallel track. |source:[impl-eng BC#15 + DA[#5]]

**impl-eng R2 deltas (4 items):**
  - R2-clarify-1 (DA7 three-additions scope): ACCEPT. IC[2] revision has 3 schema surfaces ([A] StreamEvent.final_message on stop, [B] StreamEvent.tool_result kind, [C] Message.preceding_text_per_tool_call field). (A)+(B) in IC[2] per DA[#7]; (C) on Message per DA[#2] + BC#5. Clean compositional. Noted above.
  - R2-accept-1 (DA6 golden fixtures complement BC#14): ACCEPT. 3-tier test strategy locked per DA[#6].
  - R2-NEW-2 (DA8 CONFLICT[2] SDK context-manager): ACCEPT. IC[1] INV4+INV5 locked per DA[#8].
  - R2-clarify-2 (UD#2 C2 code impact manual-gated): ACCEPT. Policy reflected in DA[#9] response.

---

#### cqa BC-cqa-1 through -11 + EC1-5 + R2 delta

**BC[cqa-1] message_mapping fixture matrix F1-F8 + direction-asymmetry: ACCEPT.** Folded into 3-tier merge-gate strategy per DA[#6]. F1+F3+F6 MUST, F2+F4+F5+F7 SHOULD, F8 M1a-smoke. Direction-asymmetric via Tier 1 + Tier 2. SQ12d 1.5h→**2.5h**. SQ23 2h→**3.5h**. |source:[cqa BC-cqa-1 + DA[#6] + cqa R2-Δ-1]

**BC[cqa-2] mock_providers.py fidelity + streaming tests: REVISE.** SQ12a 1h→2h (Anthropic event-sequence fidelity G1 + Ollama tool_calls chunk-accumulation G2 load-bearing). SQ12c at 2h covers S1-S4 post-mock-fidelity. |source:[cqa BC-cqa-2]

**BC[cqa-3] TurnEngine tool-exec state-machine T1-T9: REVISE.** SQ24 2h→3h. MUST T1+T3+T4+T6+T8+T9 (PM/INV-mandated). SHOULD T2+T5+T7. T3 contract per revised IC[5] INV2 (max_tool_calls with final-text, DA[#7]). |source:[cqa BC-cqa-3 + impl-eng BC#4 + DA[#7]]

**BC[cqa-4] JSONL persistence J1-J5 + raw sidecar: REVISE + ADR[7] INV.** Per impl-eng BC#9 response above: INV-replay-1/2/3 added to ADR[7]. SQ10b added (0.5h). J4 raw-sidecar correlation covered by SQ26 expansion. |source:[cqa BC-cqa-4 + impl-eng BC#9]

**BC[cqa-5] CLI streaming to stdout — SQ12h: ACCEPT.** SQ12h added: "test_cli.py — stdout buffering + encoding + speaker attribution + Ctrl-C flush" (1.5h, owner:code-quality-analyst, deps:SQ11). M1a success criterion requires stdout streaming validation. |source:[cqa BC-cqa-5]

**BC[cqa-6] Live-smoke SQ12i/SQ28: ACCEPT.** SQ12i added (test_live_smoke_m1a.py, 1h, M1a code-path) + SQ28 (test_live_smoke_m1b.py, 1h, M1b echo round-trip). Gated by dual flag (CHATROOM_LIVE_TESTS=1 + env keys). Budget: M1a ~$0.01 Anthropic + free Ollama; M1b similar. Addresses mock-tests-false-confidence feedback memory 26.4.5. |source:[cqa BC-cqa-6]

**BC[cqa-7] IC[1] INV3 vs IC[2] contradiction: RESOLVED via DA[#8] response.** IC[1] INV3 locked to "ALWAYS emerge" per IC[2]. SQ12j added: "test_stream_error_convention.py — 0.5h" per cqa recommendation. |source:[cqa BC-cqa-7 + DA[#8]]

**BC[cqa-8] DEAD CODE scan D1-D5: PARTIAL ACCEPT.**
  D1 Provider.complete(): CONCEDE — removed per DA[#4] GP[2].
  D2 raw_event on StreamEvent: CLARIFY — `raw_event` flows THROUGH StreamEvent (couples Provider to observability but keeps single data path); documented in IC[2] revision. If observability need grows (raw_event >1MB/event), M1c can split to BESIDE callback. Stand pat for M1a/b.
  D3 registry.py: CONCEDE — removed per DA[#4] GP[1].
  D4 PreambleVariant: CONCEDE per DA[#4] GP[3] — M1a/b ships 1 rendering + type + logged field.
  D5 tools_enabled: ACCEPT.
|source:[cqa BC-cqa-8 + DA[#4]]

**BC[cqa-9] Style + docstring gates: ACCEPT.** Q1 pyright --strict + mypy backup. Q2 pydocstyle D100/D102 public API. Q3 naming accepted. Q4 ruff/isort. Q5 line-length 88. All in pyproject.toml (SQ1). |source:[cqa BC-cqa-9]

**BC[cqa-10] Test-execution strategy: ACCEPT.** X1 pytest-asyncio strict. X2 Python 3.11+3.12 CI matrix. X3 tests/ vs tests/live/ tier structure. X4 coverage target 85% on providers/+turn_engine.py. SQ6c smoke lives in `scripts/smoke_ollama_v1.py` per DA[#8] CONFLICT[3] resolution (not tests/live/ — it's a feasibility probe, not regression). |source:[cqa BC-cqa-10 + DA[#8] CONFLICT[3]]

**BC[cqa-11] IC[2]/IC[5] CLUSTER EG1-EG5: ACCEPT.** All 5 EG tests land. EG1+EG4+EG5 integrated-state-machine (TurnEngine side, SQ24 3h). EG2 INV4 parallel-tool-call independent. EG3 final_message reconstruction independent. SQ22 2h→3h (EG2+EG3 per-SDK × 2 SDKs on provider side). |source:[cqa BC-cqa-11 + DA[#7]]

**EC[1-5] edge cases:**
  EC[1] Ollama network hiccup mid-stream: ACCEPT zero retries for M1a/b research-instrument. Test via mock ConnectionError.
  EC[2] Anthropic 429 pre-stream vs mid-stream: ACCEPT tests injecting 429 at both points.
  EC[3] Context overflow mid-generation — M1a scope? **CONFIRM M1a scope.** budget check BEFORE advance_stream(); truncate-oldest per ADR[5]; emit `[truncated: N]` marker. Add SQ12k (context-truncation test, 1h) + code lives in turn_engine.py OR a new `context.py` helper (0.75h impl-eng). **Net +1.75h M1a.**
  EC[4] YieldNextPolicy parse edge cases: CLARIFY — case-sensitive exact match on ProviderSpec.key; trailing punctuation stripped; multiple `@next:` in same turn → use LAST (natural model revision pattern); unknown key → fallback RoundRobin. Add 0.5h to SQ27 (1h→1.5h total). Split SQ27 into SQ27a yield-next (1h) + SQ27b random (0.5h) per cqa.
  EC[5] RandomPolicy determinism: ACCEPT — RandomPolicy accepts `rng: random.Random | None = None`; default module random; tests pass seeded instance.

**cqa R2 deltas (4 items):**
  - R2-Δ-1 DA6 hand-goldens: ACCEPT (DA[#6] response above). SQ12d +0.5h (2h→2.5h). SQ23 +0.5h (3h→3.5h).
  - R2-Δ-2 DA7 EG separability: CLARIFY framing NOTED. BC[cqa-11] R1 structure adequate.
  - R2-Δ-3 DA4 GP2 Provider.complete() confirms BC-cqa-8 D1: ACCEPT confirmation (DA[#4] GP[2] response).
  - R2-Δ-4 DA5 H2 scope separation from SQ12i/SQ28: ACCEPT scope separation (DA[#5] response H2-decompose).

|source:[cqa BC-cqa-1 through -11 R1 + EC[1-5] + R2-Δ-1 through -4 + DA responses above]

---

### R2 architecture-decisions revisions summary

**ADR[3] tool-exec in TurnEngine:** stands. Rationale strengthened with N>3 + observability rationale from DB re-run. BELIEF 0.88 → **0.84** (DA[#1] DB re-run).

**ADR[4] OpenAI-shaped canonical + escape-hatches:** escape-hatches LOCKED into ADR[4] proper:
  - Message.preceding_text_per_tool_call: list[str] | None (impl-eng BC#5)
  - Message.content_blocks: list[dict] | None (existing escape-hatch locked)
  - 3-tier MERGE GATE (hand-golden outbound + hand-golden inbound + round-trip smoke)
  BELIEF 0.80 → **0.70** (DA[#2] math + escape-hatch locked). Residual risk = Gemini adapter M1c+.

**IC[1] Provider protocol:**
  - complete() REMOVED from Protocol for M1a/b (DA[#4] GP[2]).
  - INV3 LOCKED: "ALWAYS emerge as StreamEvent(kind='error')" — deleted "choose one" language (DA[#8] CONFLICT[2] + cqa BC-cqa-7).
  - INV4 ADDED: within-call reconstruction state only (impl-eng R2-NEW-2).
  - INV5 ADDED: early-termination cleanup via async-generator close() (impl-eng R2-NEW-2 + cqa BC-cqa-3 T7).

**IC[2] StreamEvent taxonomy:**
  - kind literal expanded: {token, tool_call, stop, **tool_result**, error} (ui-ux IC-flag[5]).
  - final_message: Message | None ADDED (populated when stop_reason="tool_use") (impl-eng BC#3).
  - tool_call_record: ToolCallRecord | None ADDED (populated when kind="tool_result") (ui-ux IC-flag[5]).
  - INV4 ADDED: multiple kind="tool_call" events per stream allowed (impl-eng BC#2).
  - INV5 ADDED: final_message required on stop(tool_use) (impl-eng BC#3).
  - INV6 ADDED: kind="tool_result" emitted ONLY by TurnEngine (ui-ux IC-flag[5] + cqa EG4).
  - INV7 ADDED: orphan tool_result raises (cqa EG4/EG7).
  - Event grammar: `token* → (tool_call+ → stop(tool_use, final_message) → tool_result+)* → token* → stop(end_turn|max_tokens|max_tool_calls|error)`.

**IC[4] Message canonical shape:**
  - preceding_text_per_tool_call: list[str] | None ADDED (impl-eng BC#5 + DA[#2]).
  - content_blocks: list[dict] | None ADDED (escape-hatch locked from PM[1]).
  - preamble_variant typed as Literal["neutral","identity-aware","research-framed"] (type only, 1 rendering M1a/b per DA[#4] GP[3]).

**IC[5] TurnEngine.advance_stream:**
  - INV2 revised: on max_tool_calls, execute final tool, THEN re-invoke provider.stream(tools=None) once for text response, override stop_reason="max_tool_calls" (impl-eng BC#4).
  - Phase-by-phase sequencing documented in DA[#7] response above.

**ADR[7] persistence replay:**
  - INV-replay-1/2/3 ADDED for malformed trailing line / partial turn / missing header (impl-eng BC#9 + cqa BC-cqa-4).

**PM[2] escalation:**
  - Thresholds specified (3/3 → "none" → swap; 1-2/3 → "nominal" → flag; 0/3 → "reliable" → lock).
  - SQ6c tests BOTH devstral AND deepseek (DA[#9] + BC#13).

**NEW SQs:** SQ6c (0.25h blocks SQ14b), SQ8a+SQ8b split (0.5h + 0.25h = was 1h), SQ10b replay robustness (0.5h), SQ12h test_cli (1.5h), SQ12i+SQ28 live-smoke (1h+1h=2h), SQ12j error-convention (0.5h), SQ12k context-truncation (1h).

**REMOVED SQs:** SQ4 registry.py (-0.25h) — merged into roster.py (DA[#4] GP[1]).

**REVISED SQs:** SQ7 1.5h→2h, SQ9 2h→2.5h, SQ12a 1h→2h, SQ12d 1.5h→2.5h, SQ14a 2h→2.5h, SQ15 2.5h→4h, SQ22 2h→3h, SQ23 2h→3.5h, SQ24 2h→3h, SQ27 1h→1.5h (split).

**M1a revised total:** ~14h (R1) → ~17.5h (R2 parallelized; +3.5h = 2 on SQ12a/d + 0.5 on SQ7+SQ9 + 1 SQ12h + 0.75 EC3 context code + 0.25 SQ12j + SQ12i + 1h SQ12k - 0.25 registry removed - 0.25 SQ8-GP3).
**M1b revised total:** ~18h (R1) → ~23.5h (R2 parallelized; +5.5h = 1.5 on SQ15 + 1.5 on SQ23 + 1 on SQ22+SQ24 + 0.5 SQ10b + 1 SQ28 + 0.25 SQ6c + 0.5 SQ27 + -0.25 GP3).
**Grand total R2:** ~41h parallelized (was 32h R1; ~+28%). Justified by merge-gate rigor + 4-agent IC[2] convergence + PM-mandated state-machine coverage + anti-mock-overconfidence live-smoke.

---

### R2 convergence declaration

tech-architect-r3: ✓ R2-complete
  |DA-resp:#9 (DA1 DB-rerun-both, DA2 BELIEF-math+escape-hatch-locked, DA3 XVERIFY-GAP-DOC, DA4 GP1+GP2 concede / GP3 compromise-per-ui-ux, DA5 H2-decompose+other-hooks-decomp-checked, DA6 3-tier-merge-gate, DA7 IC[2]-dual-additions-BOTH, DA8 INV4+INV5-per-impl-eng-R2, DA9 UD#1-checkpoint+UD#2-manual-M1b-auto-M1c+-policy)
  |BC-resp-impl-eng:#15 R1 + #4 R2 delta (accepted-with-folding to DA responses)
  |BC-resp-cqa:#11 R1 + #5 EC + #4 R2 delta (accepted-with-SQ-revisions per DA[#6])
  |ADR-revised:#5 (ADR3 rationale + BELIEF↓, ADR4 escape-hatches locked + BELIEF↓, ADR7 replay INVs, PM[2] thresholds, IC[2] expanded)
  |IC-revised:#5 (IC[1] INV3/4/5, IC[2] kinds+fields+INV4-7+grammar, IC[4] 2-new-fields + preamble-Literal, IC[5] INV2, IC[7] via ADR[7])
  |SQ-delta:+5.5h net (M1a+3.5, M1b+5.5, -0.25 GP1 removed, -0.25 GP3 reduced; partially offset by modularity)
  |BELIEF[P(plan-ready)]: 0.82 → **0.87** (post-R2, post-DA-responses, pre-lock-gate)
  |XVERIFY[ADR3]: FAIL[infra-gap-documented — sigma-verify cross_verify hang x3 this session; compensated by 4-agent cross-agent consensus + DB re-run + industry precedent audit]
  |gate-log §2a/b/c/d/e/g: updated
  |gate-log §2h: XVERIFY gap documented in ## gate-log; NOT silently skipped; escalated to user
  |→ ready-for-DA-exit-gate-re-eval

→ WAIT for lead signal (promotion-round or lock-ready).

### ui-ux-engineer

!scope: secondary plan-track |primary=FC[Streamlit shim] + M2 sub-phase forward plan + IC-flags for M2 viability |M1a/b has NO UI code — observations target M2 readiness
!frame: per user directive 26.4.20, source plan is STARTING POINT — if evidence suggests better alt (Textual TUI), written below.
!alignment: tech-architect defined IC[1-7] + SQ[1-27] + forward-plan(M1c→M4). ui-ux-engineer REFERENCES tech-architect's ICs + narrows forward-plan to M2 sub-phases. ¬duplicate M1c/M3/M4 overviews — tech-architect owns.

---

#### FC[feasibility-check] — pre-M2 Streamlit concurrency shim

**Claim under test (source-plan risk-table):** 2h pre-M2 shim prototype is sufficient; no M1a/b interface-contract accommodation needed.

**Evidence** (source tags per §2d):

E1[streamlit-docs]: `st.write_stream` (v1.41.1+, async-gen PR#8724 merged) accepts async generators, auto-converts to sync internally. |src:[external-verification T1-verified streamlit-docs]
E2[streamlit-docs]: typewriter effect applies to STRING chunks only. Non-string yields routed via `st.write` → SEPARATE output block, ¬inline with text. |src:[external-verification T1-verified]
E3[streamlit-docs]: `st.fragment` CANNOT write to externally-created containers; streaming/async support ¬documented. |src:[external-verification T1-verified]
E4[cross-agent tech-architect IC[5]]: `TurnEngine.advance_stream → AsyncIterator[StreamEvent | Turn]` where StreamEvent.kind ∈ {token, tool_call, stop, error}. |src:[cross-agent IC[5] L542]
E5[xverify openai:gpt-5.4]: assessment=PARTIAL — agrees non-string yields break inline rendering. Counter: lightweight adapter (map token→string, buffer tool_call for side-container) may obviate full prototype. Categorical-deferral-safe claim is less certain than load-bearing claim. |src:[external-verification XVERIFY[openai:gpt-5.4]]
E6[cross-agent tech-architect IC[2]+IC[5]]: StreamEvent emits `kind="tool_call"` at provider-emission-time (pre-exec; tool={id,name,arguments}). NO `kind="tool_result"` event after TurnEngine executes. ToolCallRecord (latency_ms+result+ts_completed+preceding_text fully populated) surfaces ONLY in final `Turn.tool_calls` list yielded at turn-end. |src:[cross-agent analysis IC[2] L444-455 + IC[3] L480-501 + IC[5] L540-552]

**Analytical implication.** Direct-pipe of `advance_stream` into `st.write_stream`:
- token events → typewriter. ✓
- tool_call events (pre-exec, dict) → stacked `st.write` blocks beneath text. ✗ breaks flow
- Turn event (at end) → `st.write`d as dict dump. ✗
- Consequence: tool-call badge cannot render inline at position_in_turn because (i) mixed-type yield breaks inline typewriter (E2), (ii) ToolCallRecord result+latency+preceding_text aren't known until POST-exec but no event signals that moment (E6).

**DB[FC] dialectical bootstrap (§2g — top-1 conviction):**
1. initial: shim required, feasible in 2h, deferral safe
2. assume-wrong: what if shim is 1 day not 2h? OR st.write_stream is wrong primitive entirely?
3. strongest-counter: per E5, adapter MAY be trivial (~20 LOC wrapper yielding only .text from token events + post-stream st.expander render pass for buffered tool_calls). BUT: "post-stream" loses inline positional affordance — tool badges appear at end, not at position_in_turn, undermining M1b's position_in_turn instrumentation purpose.
4. re-estimate: shim is MORE than 2h IF inline positioning is required. Source plan's 2h assumes adapter/post-stream approach. Rendering-option has NOT been pinned.
5. reconciled: FC splits into 3 cases by rendering-option choice (see verdict).

**FC verdict:**
◌ deferral of prototype to M2-start is SAFE for interface-contract stability — IC[5] advance_stream is black-box input regardless of rendering strategy. NO M1a/b contract churn from deferral itself.
! BUT: source plan's 2h estimate is CONTINGENT on which rendering-option is pinned pre-M2:
  - option-a (post-stream tool-badges, adapter-only): 2h realistic. `st.write_stream` + token-extraction wrapper. |effort:S |loses:position_in_turn affordance
  - option-b (inline tool-badges at position_in_turn during stream): 0.5-1 day. Manual render loop (`st.empty().markdown()` progressive + interleaved `st.expander` calls). |effort:M |preserves:full affordance
  - option-c (tool-calls in sidebar panel, NOT in transcript): 1h. |effort:S |loses:all positional observability
! MATERIAL GAP: E6 reveals IC[2] has NO `kind="tool_result"` event. UI cannot know WHEN ToolCallRecord is populated (for latency_ms+result badge-rendering) until Turn-end. See IC-flag[5] below — NOT resolved by any M2 shim; requires IC[2] addition. Priority HIGH for option-b, MEDIUM for option-a.
→ rendering-option pin is a PRE-M2 gate decision (OQ[ui-1]).
|source:[source-plan + cross-agent IC[2]+IC[5] + external-verification T1-streamlit-docs + XVERIFY[openai:gpt-5.4] + agent-inference]

---

#### DS[] — design-system tokens baseline for M2

DS[1]: spacing-scale | 4 / 8 / 12 / 16 / 24 / 32 / 48 px | 4px base matches Streamlit rhythm; 8px speaker-block gutter; 16px inter-turn margin |src:[agent-inference + spec-workshop-reference]
DS[2]: typography-hierarchy | speaker-name: 16px/600 bold > tool-badge: 12px/600 caption-semibold > message-body: 14px/400 body > metadata (TTFT/tokens): 11px/400 muted |rationale: multi-model transcript lacks single-author continuity — speaker-name must anchor visual scan |src:[agent-inference]
DS[3]: color-semantics — per-speaker palette via deterministic hash(provider_key) → one of 8 WCAG-AA hues (≥4.5:1 on bg). Reserved: red=error, amber=truncation/warning, green=tool-success, blue-grey=streaming-in-flight, neutral-grey=human/system. Cap=8; beyond → composite attribution (hue + letter-prefix). |rationale:deterministic → cross-session visual reproducibility (research-instrument value) |src:[agent-inference + WCAG-2.2 T1]
DS[4]: tool-call badge visual language — pill-shaped, baseline-inline, states: `[tool:name] ↻` pending → `[tool:name] ✓ 240ms` settled → `[tool:name] ✗ err:{class}` error. Click→expand `st.expander` revealing: full query, full result (truncate at 2000ch + "full-result" sub-action), latency_ms, preceding_text (last 50ch), position_in_turn. |src:[agent-inference + IC[3] ToolCallRecord fields]
DS[5]: streaming-in-flight — cursor caret (▍) on active streaming line, fades on stop_reason; subtle pulse on active speaker-chip. |src:[agent-inference]
DS[6]: status-icon set — Streamlit-native `:material/icon:` |streaming:`graphic_eq` |tool-pending:`sync` |tool-success:`check_circle` |tool-error:`error` |human-injection:`person` |truncation:`content_cut` |rationale:no custom CSS, honors Streamlit theme |src:[external-verification T1-streamlit-docs]
DS[7]: density — default medium (16px turn-gap); "dense" toggle (8px) for long-session viewing; metadata row collapsed by default.

§2a consensus [DS]: alt = default `st.chat_message`. DS[3] diverges (13-model attribution need). |outcome:2 confirms-with-counterweight
§2b precedent [DS]: ChatGPT letter-avatars, Anthropic console color-chips. |outcome:2
§2c cost [DS]: tokens 0-effort now. |outcome:2
§2e premise [DS]: Streamlit-is-right-primitive at risk per OQ[ui-2]; TUI would thin DS layer. |outcome:2

---

#### IX[] — interaction patterns for M2

IX[1]: streaming-render — strategy determined by FC-pinned rendering-option. Auto-scroll during stream; pause auto-scroll on user-scroll-up (chat convention). |depends-on:FC
IX[2]: tool-call badge interaction — collapsed default `[tool:name] ✓ {latency}ms`. Click→`st.expander` expansion per DS[4]. State-machine: pending → settled | error. |src:[IC[3]]
IX[3]: autonomous-mode state-machine — idle / running / paused / error / done.
  - idle→[Start]→running
  - running: [Pause] + live turn-counter + running token-cost + current-speaker chip
  - paused→[Resume]|[Stop-and-save]
  - error (provider-fail mid-stream): red banner, partial Turn saved w/ stop_reason="error" per IC[5]; [Retry-turn]|[Skip-speaker]|[Stop]
  - done (N-turns/max): [Export]|[New-session]
IX[4]: human-moderated-mode — `[Speaker: roster-dropdown] [Inject-message textarea] [Override-next-speaker: checkbox]`. Human turn: `provider="human"` in JSONL per source-plan L187.
IX[5]: preamble-picker — 3 radio options (neutral/identity-aware/research-framed) + live preview pane rendering system_preamble. LOGGED per session, immutable post-first-turn. Warning banner if historical session opened with different preamble_variant (cross-session comparison gate). |src:[source-plan L182]
IX[6]: yield-next visualization — YieldNextPolicy fires (IC[6]) → transcript shows `→ @next:name` at turn-end. Sidebar metric: "spontaneous yield-next attempts" per speaker (feeds M3).
IX[7]: session-list + resume — sidebar list (timestamp + roster + mode + preamble_variant). Click→`persistence.replay` (IC[7]) loads instant transcript; [Resume] button if ¬marked-done.

§2a consensus [IX]: default Streamlit chat tutorial is single-speaker. IX[2/4/5] diverge, justified by observability requirement (source-plan Outcome). |outcome:2
§2b precedent [IX]: Claude Artifacts, ChatGPT function-call UI, Cursor inline tool-use — badge-expansion is established. |outcome:2
§2c cost [IX]: IX[2] most expensive (expand-collapse with streaming). M2b scope. |outcome:2
§2e premise [IX]: IX[2]/IX[6] priority depends on research-question pin (source-plan open-decision #1). |flag:OQ[ui-3]

---

#### A11Y[] — accessibility plan (WCAG 2.2 AA)

A11Y[1]: keyboard nav — all interactives tabbable; advance/pause→Space; inject textarea focusable; session-list arrow-key; tool-badge expand→Enter. |risk:Streamlit widget keyboard coverage partial. |flag:OQ[ui-4]
A11Y[2]: screen-reader streaming — `aria-live="polite"` for new tokens; tool-badge `aria-label="Tool {name}, status {state}, latency {ms}ms, press Enter to expand"`. |risk:Streamlit native aria-live partial; may need custom component (+0.5-1 day). |flag:OQ[ui-4]
A11Y[3]: color + text attribution (NOT color-only per §1.4.1) — DS[3] color + speaker-name text + provider-prefix. |src:[WCAG-2.2 T1]
A11Y[4]: contrast — speaker-color-on-bg ≥4.5:1 (§1.4.3); tool-badge pill ≥3:1 (UI component §1.4.11). Verify via contrast tool pre-M2a-ship.
A11Y[5]: focus indicators — 2px outline ≥3:1 (§2.4.11 + §2.4.13).
A11Y[6]: reduced-motion — cursor + spinners respect `prefers-reduced-motion: reduce`. Cursor→static; spinner→text.

§2a/2b [A11Y]: WCAG 2.2 AA T1-consensus. |outcome:1
§2c [A11Y]: A11Y[2] aria-live highest-cost. |outcome:3 gap→tech-architect
§2e [A11Y]: AA correct for research-instrument; AAA not required. |outcome:1

---

#### PERF[] — rerun-cost strategy

PERF[1]: Streamlit rerun = O(n_turns × avg_tokens) render. Negligible at M1 5-turn; measurable at M3 30-50 turn. |src:[streamlit-community-pattern]
PERF[2]: mitigation hierarchy:
  - Level-1 (M2a, cheap): `st.container` per turn + `@st.cache_data` on `render_turn(turn)` — reruns only recompute streaming turn. Cost:0.25 day. |sufficient-for:≤30 turns
  - Level-2 (M2b, moderate): `st.fragment` scoping autonomous-advance button. CAVEAT E3: fragment ¬writes-to-external-containers — transcript must live INSIDE fragment; tool-expanders must also be inside. Cost:0.5 day. |sufficient-for:≤80 turns
  - Level-3 (M3/M4, heavy): transcript virtualization — last 20 turns + "load earlier" sentinel. Source plan defers to M4; MAY need shift-left to M3c if session-length empirically >40 turns. Cost:1-2 days.
PERF[3]: raw-event sidecar writes separate JSONL → ¬rerun impact.

§2a [PERF]: fragment isolation is consensus. |outcome:1
§2b [PERF]: community reports ~40-60-turn pain threshold in Streamlit chats. |outcome:2
§2c [PERF]: Level-3 M4-defer is GAMBLE — if M3 session-length exceeds 40 turns, UX degrades pre-ship. |flag:revision-hook UX-H1 added
§2e [PERF]: rerun-cost-tolerable premise holds for M2-shakedown, at-risk for M3. |outcome:2

---

#### ES[] — empty/loading/error state designs

ES[1]: no-session (first-load) — centered hero: "sigma-chatroom — multi-model conversation lab" + CTA `[Start new session]` + sidebar-hint `[or pick past session →]`. Muted Streamlit-native icon illustration.
ES[2]: streaming-in-flight — speaker-chip + cursor caret + live token-counter `▍ 47 tokens...`. NO modal spinner (blocks interaction). |rationale:inline-progress > modal
ES[3]: tool-invocation-in-progress — inside badge: `[tool:sigma_mem_recall] ↻` + latency timer `↻ 1.2s`. Badge click-inert during pending.
ES[4]: provider-failure — banner: `⚠ {provider} failed mid-stream ({error_class}). Partial turn saved.` + [Retry]|[Skip speaker]|[Stop session]. Transcript shows partial + `[...stream interrupted]` suffix. |src:[IC[5] error convention]
ES[5]: context-overflow — `[truncated: 8 earlier turns]` marker (source-plan L364). Click expands to show dropped turn-IDs.
ES[6]: empty-roster — sidebar-picker shows greyed providers + tooltip `env-key missing: set ANTHROPIC_API_KEY` per `registry.available()` (source-plan L372).
ES[7]: MCP-server-unavailable (M3 only) — badge `[tool:sigma_mem_recall] ✗ MCP unavailable`; ToolCallRecord.error populated per source-plan L368.
ES[8]: max-tool-calls-reached — inline `⚠ max 5 tool calls reached; stop_reason="max_tool_calls"` per IC[5] INV + source-plan L227. !NOTE: if tech-architect adopts impl-eng's ADR[3] max_tool_calls revision (BUILD-CHALLENGE[impl-eng R1] L785) emitting final text after 5th tool_result, ES[8] copy shifts to trailer-not-truncation.

§2a [ES]: standard loading/error/empty triad = consensus. |outcome:1

---

#### IC-flag[] — M1a/b interface-contract flags for tech-architect (M2-UX readiness)

!these are FLAGS — tech-architect owns IC[] ; ui-ux-engineer surfaces UX-driven accommodations.

IC-flag[1]: `StreamEvent.position_in_turn` — currently position_in_turn lives on ToolCallRecord only (IC[3]). For option-b inline-badge rendering, UI needs position available ON StreamEvent when kind="tool_call" emits, placing badge inline without post-hoc diff vs ToolCallRecord list. Recommend: add `position_in_turn: int = 0` to StreamEvent (TurnEngine pre-fills pre-yield). |priority:low if option-a, HIGH if option-b. |decide-after:OQ[ui-1]

IC-flag[2]: `StreamEvent.running_tokens_out` — ES[2] needs running token count. Options: (a) UI counts kind="token" events itself, (b) StreamEvent carries running_tokens_out. (a) is UI-owned — no IC change. |resolved:UI-owned

IC-flag[3]: ConversationState observation — IC[5] yields Turn appended to `state.turns`. UI polls len(state.turns) on rerun → sees new turn. Works in Streamlit poll-rerun model. |resolved:poll-based

IC-flag[4]: Preamble-variant immutability post-first-turn — IC[6]-adjacent. Recommend tech-architect lock ConversationState.preamble_variant as mutable-only-when-state.turns-is-empty; raise if mutated post-first-turn. Prevents UX corruption (user toggling preamble mid-session). |priority:medium

IC-flag[5]: **ToolCallRecord inline-surfacing during stream — MATERIAL GAP.** Per E6, IC[2] emits `kind="tool_call"` pre-exec (tool={id,name,arguments}). After TurnEngine executes, ToolCallRecord populated with result+latency_ms+ts_completed+preceding_text+position_in_turn — but NO StreamEvent signals this moment. ToolCallRecord surfaces ONLY in final Turn.tool_calls. Consequence: UI cannot render settled-state badge (`[tool:name] ✓ 240ms`) until Turn ends. During exec UI shows only pending; on Turn-yield all badges jump to settled simultaneously — visual disconnect from streaming flow.
**Recommend:** TurnEngine emits NEW `StreamEvent(kind="tool_result")` post-tool-exec carrying fully-populated ToolCallRecord (either as new StreamEvent kind OR by enriching existing `tool: dict` and emitting a second event with same tool id). Note: this composes cleanly with impl-eng's BUILD-CHALLENGE on IC[2] (parallel-tool-call INV4 — L781) and on IC[5] final-message reconstruction (L783). IC[2] is already under active revision for related concerns; adding tool_result is low marginal cost.
|priority:HIGH — biggest M2-UX risk if unaddressed |effort:~1h in TurnEngine (SQ16 addition) |flag:tech-architect, DA

IC-flag[6]: error_class taxonomy surfacing — ES[4] needs error_class ("rate_limit"|"auth"|"context_overflow"|"network"|"tool_exec_fail"|"unknown"). Tech-architect SQ5 creates providers/errors.py taxonomy. Recommend: StreamEvent(kind="error") carries `error_class: str` field OR `error` is a typed exception from errors.py enabling `type(event.error).__name__`. |priority:medium |flag:tech-architect

---

#### FORWARD-PLAN — M2 sub-phases (ui-ux-engineer scope)

!ui-ux-engineer narrows to M2 sub-decomposition + pre-M2 gate details. ¬duplicate tech-architect's M1c/M3/M4 phases above.

**pre-M2 spike (gate before M2 starts) — 1 day max**
- STEP-1 (30 min): pin rendering-option (a/b/c) with user per OQ[ui-1]
- STEP-2 (2-4h): prototype chosen option against 5-turn 2-model M1b JSONL fixture
  - option-a: 2h adapter (st.write_stream + token-extraction wrapper; tool_calls buffered to post-stream expander-list)
  - option-b: 0.5-1 day manual-loop (st.empty + progressive-markdown + interleaved st.expander at position_in_turn; REQUIRES IC-flag[5] resolved)
  - option-c: 1h sidebar-panel (tool-calls separate pane)
- STEP-3 (2h): Textual TUI comparison sketch — same 5-turn M1b JSONL fixture in TUI equivalent; user evaluates Streamlit-vs-TUI. |rationale:source-plan TUI-as-fallback becomes informed-choice, not emergency-fallback
- exit-criteria: chosen option renders 5-turn 2-model M1b JSONL fixture with ≥1 echo-tool round-trip per provider; user declares "feels right"

**M2a — shell + transcript + autonomous mode (3 days)**
- `streamlit_app.py` entry
- `ui/sidebar.py` — roster-picker + mode-toggle + preamble-picker
- `ui/transcript.py` — baseline streaming via chosen shim-option; DS[1-7] applied; ES[1-2]; IX[1]
- `ui/controls.py` — [Start]/[Pause]/[Resume]/[Stop] state-machine per IX[3]
- PERF[2] Level-1 caching
- exit-criteria: end-to-end 2-provider autonomous session (Anthropic + Ollama cloud M1 seed pair) runs in Streamlit startup→JSONL persist

**M2b — tool-call badges + preamble + error-handling (3-4 days)**
- DS[4] badge states + IX[2] expand/collapse
- IX[5] preamble-picker live-preview + immutability-post-first-turn (REQUIRES IC-flag[4])
- IX[6] yield-next annotation
- ES[3-4] error banners + retry/skip
- A11Y[1-4] (keyboard + aria-live + contrast)
- exit-criteria: echo-tool round-trip badge renders correctly; retry flow works on injected provider-fail

**M2c — human-moderated + session-list + polish (2-3 days)**
- IX[4] human-moderated mode
- IX[7] session-list + resume via `persistence.replay`
- ES[5-8] edge states
- A11Y[5-6] focus + reduced-motion
- PERF[2] Level-2 fragment isolation (IF session-length empirically >30 turns in M2b)
- exit-criteria: full human-moderated session with injected turns + resume works

**Revision hooks (UI-track additions to tech-architect's):**
UX-H1→ if M1a TTFT p95 > 2000ms → M2a adds "waiting for {provider}" pre-first-token indicator. +0.25 day.
UX-H2→ if M1b ToolCallRecord.result p95 > 4KB → M2b expander adds truncation + "view full result". +0.25 day.
UX-H3→ if M1b position_in_turn clusters at turn-endpoints (not distributed) → M2b badge simplifies to header-cluster + footer-cluster. +0 day (simplification).
UX-H4→ if M1b tool_use_reliability="none" on devstral-2 (PM[2]) → M2a roster-picker shows per-model reliability badge. +0.5 day.
UX-H5→ if IC-flag[5] rejected by tech-architect → option-b infeasible; force option-a. Reduces M2b by 0.5 day but lose observability.
UX-H6→ if pre-M2 TUI sketch reveals strong preference → Q3 plan pivots to Textual-TUI v1. Scope shifts completely; est:4-6w total v1.

**Grand M2 estimate.** 8-10 days (1.5-2 weeks) w/ option-a; 10-12 days w/ option-b. Aligns with tech-architect's 2-3w M2 estimate (tech-architect's scope includes broader integration).

---

#### DB[] — dialectical bootstrapping (§2g, top-2 conviction)

DB[FC] performed inline (top-1).

**DB[option-b feasibility]** (top-2):
1. initial: option-b achievable in 0.5-1 day with manual render-loop
2. assume-wrong: what if Streamlit render model fundamentally can't interleave streaming text update with fully-rendered st.expander in visual-flow order?
3. strongest-counter: E2+E3 suggest NOT a solved pattern in Streamlit docs. Community patterns likely exist (discourse.streamlit.io) but undocumented officially. Risk: 1-2 weeks on M2a-b ends discovering true-inline requires st.empty()-per-char hack that flickers at browser paint-rate. TUI gets inline natively via rich.
4. re-estimate: 70% P(Streamlit option-a ships clean in 8-10 days); 50% P(option-b ships clean in 10-12 days). TUI 90% P(option-b-equivalent ships similar window, inline default in rich/textual).
5. reconciled: **pre-M2 spike MUST include 2h TUI comparison sketch** (STEP-3). Makes Streamlit-vs-TUI informed-choice. +2h pre-M2. Reward: de-risks largest premise in Q3 plan.

---

#### OPEN-QUESTIONS (plain English, for user/lead)

OQ[ui-1]: **Rendering-option pin.** (a) post-stream badges, (b) inline-at-position_in_turn, (c) sidebar-panel. Pin before pre-M2 spike. Drives IC-flag[1]+IC-flag[5] priority. Recommendation: (b) if research question is memory-invocation coherence; (c) if yield-next spontaneity.

OQ[ui-2]: **Streamlit vs Textual TUI for v1.** Shareability/demo requirement (screenshots, showing to others)? If YES → Streamlit. If audience-of-1 acceptable → TUI viable (avoids rerun cost, native async streaming, inline-by-default, keyboard-native). Pre-M2 STEP-3 (2h sketch) gives empirical basis. Source plan lists TUI as "fallback only" — recommend promoting to "informed choice."

OQ[ui-3]: **Research-question pin** (source-plan open-decision #1). Affects M3 metrics priority (IX[6] vs IX[2]). Duplicates tech-architect OQ — consolidate.

OQ[ui-4]: **A11Y[2] custom component.** If Streamlit aria-live insufficient, is custom Streamlit component in-scope for M2b? (+0.5-1 day). Alt: document A11Y[2] as M2 gap, resolve M3+.

---

#### Analytical hygiene summary (ui-ux-engineer)

**§2a positioning.** DS[3] diverges from Streamlit default chat (multi-model attribution). IX[2/4/5] diverge from single-speaker tutorial (observability requirement). Others CONSENSUS.
**§2b calibration.** Precedents cited for DS (ChatGPT, Anthropic console), IX (Claude Artifacts, Cursor), PERF (Streamlit community), A11Y (WCAG 2.2 AA).
**§2c cost.** All items cost-justified against M2 8-12 day estimate. IC-flag[5] highest-leverage: 1h tech-architect fix → biggest M2b risk reduction.
**§2d source-provenance.** Every finding tagged.
**§2e premise.** Streamlit-right-primitive premise AT RISK per DB — TUI comparison warranted pre-M2.
**§2g dialectical.** DB on FC (top-1) + option-b feasibility (top-2).
**§2h XVERIFY.** FC verified via openai:gpt-5.4 → PARTIAL (counter incorporated in DB[FC]).

**Load-bearing findings.** FC + IC-flag[5] top load-bearing. Others are M2-design guidance, medium stakes.
**XVERIFY coverage.** 1/1 required (top-1 load-bearing). Adequate per C1 (XVERIFY advisory).

---

#### convergence-ready marker
!R2-update (post-DA + user-decisions)
FC:#1 |DS:#7 |IX:#7 |A11Y:#6 |PERF:#3 |ES:#8 |IC-flags:#6 |OQ:#4 |forward-plan:✓(pre-M2 STEP-0/1/2/3a/3b/4 + M2a/M2b/M2c + decomposed UX revision-hooks) |DB:#2 |XVERIFY:#1-openai-gpt5.4-partial
DA-resp:#4 (DA4-GP3 + DA5 + DA8 CONFLICT[1] + UD#3/4/5/6 acceptance)
P(plan-ready ui-ux-scope R2): 0.88

---

#### R2 DA-responses + user-decision acceptance (ui-ux-engineer, 26.4.20)

**DA[4] GP[3] — preamble-variant gold-plating (concede+compromise)**
concede: DA4-GP[3] + user-decision #5 (research-Q pinned = memory-invocation-coherence) make ONE primary preamble variant correct for M1a/b. Building 3 variants in M1a/b is speculative.
compromise (not full concede): M1a/b ships ONE variant rendering (identity-aware — matches memory-invocation-coherence research framing + retains `@next:` convention per source-plan L218). PreambleVariant Literal type + preamble_variant logged field REMAIN in IC[4]/IC[7] (type-level only + persisted field, no unused rendering code). This preserves:
  - IX[5] preamble-picker M2 deliverable (still 3-variant target, matches source-plan L182-184 cross-session comparison requirement)
  - source-plan L207 "preamble_variant logged per session" contract
  - logged sessions default to identity-aware; cross-session comparison works on matching variant (research-Q pin implies this)
  - M2 adds neutral + research-framed variants when preamble-picker UI materializes
rationale: GP[3] ≠ cut PreambleVariant from type system. GP[3] = cut unused RENDERING code. The type + persisted field are free; the variant rendering code is what's gold-plated.
action: IX[5] revised — M2a ships identity-aware-only picker. M2b activates neutral. M2c activates research-framed CONDITIONAL on user checkpoint. Net scope: M2a -0.25d; M2b +0.25d; M2c +0.5d conditional.
|source:[DA[4] GP[3] L1448-1449 + user-decision #5 L1814 + source-plan L182-184,L207]

**DA[5] forward-plan H2 decompose (accept + apply to UI-track)**
accept: DA5 decompose-code-from-research pattern correct at plan-phase. Apply to ui-ux UX-H1-H6:
  - UX-H1 (TTFT slow-indicator): pure code. ✓ no decomposition.
  - UX-H2 (result-size truncation): pure code. ✓
  - UX-H3 (position_in_turn distribution): **BUNDLED — decompose.** "If position clusters at endpoints" is AN EMPIRICAL M1b OBSERVATION, not a code change. Split: (a) M1b-research: observe distribution after 3 M1b runs (0.5h analysis); (b) M2b-code: CONDITIONAL on (a) — if clustered, simplify to header/footer-cluster (+0 day).
  - UX-H4 (reliability-badge): bundled — trigger (devstral="none") is empirical, action is code. Split: (a) M1b-research: 0h (captured in roster updates per tech-architect PM[2]+UD#2); (b) M2a-code: reliability-badge render in sidebar (+0.5d).
  - UX-H5 (IC-flag[5] rejected): pure scope change from tech-architect R2. ✓ no decomposition.
  - UX-H6 (TUI pivot): pure research→code decision from STEP-3b. Already well-formed. ✓
action: UX-H3 + UX-H4 decomposed below. Makes code/research boundary explicit.
|source:[DA[5] L1466-1474 + ui-ux UX-H1-H6]

**DA[8] CONFLICT[1] — dual IC[2] additions (defend ui-ux proposal, compose with impl-eng)**
DA8 CONFLICT[1] correctly identifies: impl-eng BC#3's `final_message` on kind="stop" (reconstructs PRE-tool-exec assistant message) + ui-ux IC-flag[5]'s `kind="tool_result"` (emits POST-tool-exec populated ToolCallRecord) are TWO DIFFERENT additions addressing DIFFERENT tool-exec phases.
defend: ui-ux IC-flag[5] NOT subsumed by impl-eng's final_message. Phase breakdown:
  - PROVIDER.stream() yields tool_call event → stop(reason=tool_use) + final_message (impl-eng BC#3 — reconstructed canonical assistant msg for conversation history)
  - TurnEngine executes tool → writes ToolCallRecord (latency_ms, result, position_in_turn, preceding_text)
  - **NO StreamEvent fires here currently** (ui-ux IC-flag[5] — UI blind to tool-settled moment)
  - TurnEngine appends tool_result Message + re-invokes provider.stream() OR caps at 5 → final stop
Without IC-flag[5]: UI receives nothing between stop(tool_use)+final_message and next token-stream start. Multi-tool: UI can't know which tool settled; visually frozen during exec; all badges jump-to-settled at turn-end. Option-b rendering impossible.
Without final_message: conversation history reconstruction impossible OR requires Provider statelessness violation (see DA8 CONFLICT[2] — tech-architect owns).
Both compositional. Recommend tech-architect R2 IC[2] revision adds BOTH:
  - `kind="stop"` carries `final_message: Message | None` (impl-eng BC#3)
  - `kind="tool_result"` new event w/ `tool_call_record: ToolCallRecord` (ui-ux — NB: FULL ToolCallRecord per IC[3], not `tool: dict`)
Emission sequence within TurnEngine.advance_stream: provider emits tool_call, provider emits stop+final_message, TurnEngine executes, TurnEngine emits tool_result (NEW), TurnEngine appends messages, re-invokes provider.stream() → next iteration.
|source:[DA[8] CONFLICT[1] L1529 + ui-ux IC-flag[5] + impl-eng BC#3 L1027 + cqa BC-cqa-11]

**user-decision #3 rendering-option (accept + verify agnosticism conditional)**
accept: M1a/b contracts ARE rendering-option-agnostic from ui-ux perspective IFF tech-architect R2 accepts dual IC[2] additions. Verification per option:
  - option-a (post-stream badges): needs position_in_turn + preceding_text in ToolCallRecord (already IC[3] L492-493). ✓ no M1 change.
  - option-b (inline at position_in_turn): needs position_in_turn available DURING stream. If IC-flag[5] accepted → StreamEvent(kind="tool_result").tool_call_record.position_in_turn. ✓ agnostic.
  - option-c (sidebar-panel): renders from Turn.tool_calls at Turn-yield. ✓ no M1 change.
Conclusion: agnosticism CONDITIONAL on IC-flag[5] acceptance. Without it, option-b blocked regardless of pre-M2 spike. UD#3 deferral safe only if IC-flag[5] resolved as expected in R2.
action: forward-plan pre-M2 STEP-0 added — "verify tech-architect R2 IC[2] revision accepted BEFORE offering option-b in STEP-1 pin." If rejected, STEP-1 presents 2 options (a+c) only.
|source:[user-decision #3 L1810 + ui-ux IC-flag[5] + IC[3] L492-493]

**user-decision #4 TUI comparison (accept, bake into pre-M2)**
accept: STEP-3b TUI sketch pre-committed +2h. pre-M2 structure revised:
  STEP-0: gate check on tech-architect R2 IC-flag[5]
  STEP-1: pin rendering-option (30 min user call)
  STEP-2: Streamlit prototype of chosen option (2h-1 day)
  STEP-3a: exit-criteria check (30 min)
  STEP-3b: Textual TUI comparison sketch (2h) — ALWAYS executed
  STEP-4: user Streamlit-vs-TUI decision (30 min)
Total pre-M2: 1-1.5 days (was 1 day).
|source:[user-decision #4 L1812 + ui-ux DB[FORWARD-PLAN]]

**user-decision #5 research-Q pin (accept + M3 re-prioritize)**
accept: memory-invocation-coherence pinned. Validates IX[2] tool-call-badge priority (memory queries ARE the research observable). IX[6] yield-next drops from priority-1 to priority-2 supplement.
M3b metrics-panel re-priority:
  1st-row: per-speaker memory-query count + query-text per call + latency distribution (research observable)
  2nd-row: per-query-topic frequency (research observable)
  3rd-row: cross-speaker query-similarity (embedding — defer to M4 per source-plan)
  deferred from M3 to M4: yield-next override rate (was in tech-architect M3 deliverables), speaker-influence graph (M4 anyway)
|source:[user-decision #5 L1814 + IX[2] + IX[6] + tech-architect M3 deliverables L1674-1686]

**user-decision #6 A11Y[2] = M2 documented gap (accept)**
accept: A11Y[2] aria-live for streaming tokens = M2 DOCUMENTED-GAP. Marked in DS/IX:
  - IX[1] streaming-render: note added "SR-a11y streaming tokens = known M2 gap; resolves M3+ if shareability becomes requirement; moots if TUI pivot."
  - A11Y[2] status: DOCUMENTED-GAP (not blocking).
If STEP-3b pushes toward TUI, A11Y[2] fully moots (terminals have native a11y).
|source:[user-decision #6 L1816]

**lead item #7 cqa EC[5] RandomPolicy seed (concede out-of-scope)**
concede: cqa EC[5] is test-determinism, not UI. IX[3] autonomous-mode state-machine orthogonal to policy internals. UI emits `policy=RandomPolicy` selection event; policy seed is TurnEngine-internal. IX[3] unaffected.
|source:[lead R2 item 7 + cqa EC[5]]

---

#### revised IX + DS annotations (post-R2)

IX[1] revised: "streaming-render strategy determined by FC-pinned rendering-option. SR-a11y streaming tokens = DOCUMENTED M2 GAP per user-decision #6."
IX[5] revised (post-DA4 GP3 concede): **M2a ships identity-aware-only picker + greyed future-options. M2b activates neutral. M2c activates research-framed CONDITIONAL on user checkpoint.** PreambleVariant Literal type remains in IC[4] (type+logged field only, no unused rendering code in M1a/b). `preamble_variant` field persisted per IC[7] from day-1.
IX[6] reprioritized (post-UD#5): yield-next visualization → priority-2 supplement (not primary observable). Still renders in transcript; removed from M3 priority-1 metrics-panel.

---

#### revised FORWARD-PLAN (post-R2)

**pre-M2 spike — 1-1.5 days**
STEP-0 (gate): verify tech-architect R2 IC-flag[5] acceptance. If accepted → STEP-1 offers options a/b/c. If rejected → STEP-1 offers options a/c only.
STEP-1 (30 min): pin rendering-option per OQ[ui-1]. UD#5 memory-invocation-coherence → recommend option (b) inline for positional observability IF STEP-0 accepted; else option (a) post-stream.
STEP-2 (2h-1 day): Streamlit prototype of chosen option.
STEP-3a (30 min): exit-criteria check.
STEP-3b (2h): Textual TUI comparison sketch — ALWAYS executed per UD#4.
STEP-4 (30 min): user Streamlit-vs-TUI v1 decision.

**M2a — shell + transcript + autonomous mode (3 days, -0.25d DA4 IX[5] concede)**
- Streamlit path: streamlit_app.py + ui/sidebar.py (roster + mode + preamble-picker[1-variant]) + ui/transcript.py + ui/controls.py (IX[3])
- DS[1-7] applied; ES[1-2]; IX[1] w/ A11Y[2] gap noted
- PERF[2] Level-1 caching
- TUI alt-path (if UD#4 landed TUI): textual app.py + sidebar widget + streaming pane + controls — same scope, different framework. A11Y[2] moots.
- exit: 2-provider autonomous session runs startup→JSONL

**M2b — tool-call badges + preamble-v2 + error-handling (3.5 days, +0.25d IX[5] concede)**
- DS[4] badge states + IX[2] expand/collapse
- IX[5] activates neutral preamble (second of three) — +0.25d
- IX[5] preamble-variant immutability post-first-turn (CONDITIONAL on IC-flag[4] R2 accept)
- IX[6] yield-next annotation (priority-2 supplement per UD#5)
- ES[3-4] error banners + retry/skip
- A11Y[1], A11Y[3], A11Y[4] (keyboard + color+text + contrast; A11Y[2]=DOCUMENTED-GAP per UD#6)
- exit: echo-tool badge correct; retry flow works

**M2c — human-moderated + session-list + conditional variant-3 (2.5-3 days)**
- IX[4] human-moderated mode
- IX[7] session-list + resume
- ES[5-8] edge states
- A11Y[5-6] focus + reduced-motion
- PERF[2] Level-2 fragment isolation (if session-length >30 turns empirically)
- IX[5] research-framed variant activation — CONDITIONAL on user checkpoint (DA4 concede): +0.5d if approved, +0d if dropped
- exit: full human-moderated session with injected turns + resume

**Decomposed revision hooks (DA5 research-vs-code split):**
UX-H1 (TTFT slow-indicator) — pure code, trigger: M1a TTFT p95>2000ms. +0.25d M2a.
UX-H2 (result-size truncation) — pure code, trigger: M1b ToolCallRecord.result p95>4KB. +0.25d M2b.
UX-H3 **decomposed:**
  UX-H3-research: observe position_in_turn distribution after 3 M1b runs. 0.5h M1b-analysis (¬M2 scope).
  UX-H3-code: CONDITIONAL on research — if clustered at endpoints, M2b badge simplifies to header/footer-cluster. +0d.
UX-H4 **decomposed:**
  UX-H4-research: tool_use_reliability logged per M1b run. 0h (captured in roster per tech-architect PM[2]+UD#2).
  UX-H4-code: roster-picker shows reliability badge per-model. +0.5d M2a.
UX-H5 — moved from runtime hook to pre-M2 STEP-0 gate. If IC-flag[5] rejected, option-b removed from STEP-1 menu; M2b -0.5d.
UX-H6 — already well-formed (research → scope). M2 framework pivots, ~same effort.

**Grand M2 estimate (Streamlit path):** 8.5-10 days (was 8-10) — net +0.25d from R2 revisions.
**Grand M2 estimate (TUI path):** ~7-9 days (A11Y[2] moots, st.write_stream moots, inline-native).
**pre-M2 spike:** 1-1.5 days.

---

#### R2 convergence declaration

ui-ux-engineer R2: ✓ R2-complete |DA-resp:#4 (DA4-GP3 concede+compromise, DA5 accept+apply, DA8 CONFLICT[1] defend-both, IC-flag[5] reaffirmed) |user-decisions-applied:#5 (UD#3 agnosticism-verified-conditional, UD#4 STEP-3b baked, UD#5 M3 re-prioritized, UD#6 A11Y[2] DOCUMENTED-GAP, UD#2/7/8 out-of-ui-scope acknowledged) |IX-revisions:IX[1] a11y-gap-note + IX[5] 1-variant-first + IX[6] priority-2 |forward-plan-revised:pre-M2 +STEP-0+STEP-3b / M2a -0.25d / M2b +0.25d / M2c conditional-variant-3 / 6 hooks decomposed |net-scope-delta:+0.25d M2-streamlit / M2-TUI shorter / pre-M2 +2h
lead-item-7 (cqa EC[5] RandomPolicy): concede out-of-ui-scope.
P(plan-ready ui-ux-scope R2): 0.88 (was 0.83)
→ pending-on: tech-architect R2 dual-IC[2]-addition acceptance (both final_message AND kind="tool_result"). If rejected → pre-M2 STEP-0 constrains STEP-1 menu; net M2b -0.5d.
→ ready-for-lock-post-tech-architect-R2

!wait for lead promotion-round signal.

### implementation-engineer challenges (build-track, R1 — post-tech-architect)
!scope: challenge C2-code-implementability of tech-architect ADRs + ICs + SQs. ¬plan re-litigation; flag hidden complexity that bites at build time. Aligned with source-plan H1-H7 + user directive "plan is starting point, stress-test and tweak."

---

BUILD-CHALLENGE[impl-eng, R1]: ADR[2] + IC[1] — Ollama cloud OpenAI-compat streaming+tool_calls is UNVERIFIED at SDK version level |feasibility:L→M(conditional) |issue: ADR[2] E2 asserts "Ollama OpenAI-compat endpoint emits tool_calls array when model is instruction-tuned for it" citing [independent-research] — but ollama-mcp-bridge project (~/Projects/ollama-mcp-bridge/src/ollama_mcp_bridge/ollama_client.py:11-14) has inline warning: "DO NOT switch to /v1/chat/completions — that endpoint silently drops tool_calls when streaming (confirmed Ollama bug, github.com/ollama/ollama/issues/12557). The native /api/chat endpoint handles streaming + tool calls correctly." Verified against issue #12557: it was actually about /api/chat non-piecewise streaming and closed as ¬bug by maintainer ParthSareen. The /v1 behavior remains OPEN QUESTION. XVERIFY[openai:gpt-5.4]: uncertain(low) — "cannot conclude streamed tool_calls reliably preserved on /v1 without end-to-end test against ollama.com/v1 stream=True + tools." |→ revise-SQ |action-required: ADD new pre-M1b SQ: "SQ6c — Ollama cloud /v1 streaming+tool_calls smoke test (15min): AsyncOpenAI(base_url=ollama-cloud-v1) with stream=True + minimal tool def on devstral-2:123b-cloud; confirm tool_calls arrive in delta stream. If fail: pivot to (a) add ollama pypi dep + use native AsyncClient for Ollama provider in M1b, (b) constrain M1b tool-use to Anthropic-only with Ollama-tool-use deferred to M1c gate. BEFORE SQ14b commits 2h on ollama_client tool-use path." Estimate: 0.25h. Blocks: SQ14b. |source:[code-read Projects/ollama-mcp-bridge/src/ollama_mcp_bridge/ollama_client.py:11-14, gh-CLI Projects/ollama/ollama#12557, external-verification XVERIFY[openai:gpt-5.4]]

BUILD-CHALLENGE[impl-eng, R1]: IC[2] StreamEvent — `tool: dict | None` loses parallel tool_calls mid-stream |feasibility:M |issue: IC[2] defines `tool: dict | None` for kind="tool_call" events. Anthropic models (incl. opus-4-7) can emit MULTIPLE tool_use content-blocks within a single assistant turn. OpenAI models emit parallel tool_calls as an array. If IC[2] emits kind="tool_call" once per tool_use block (atomic at content_block_stop), that's fine — each event carries one tool. But `tool: dict | None` with SINGULAR dict implies "one tool_call per turn" semantics that may mis-suggest API shape. Source-plan Message dataclass line 103 has `tool_calls: list[dict] | None` (plural) for canonical Message — consistent. IC[2] is consistent IF documented that multiple kind="tool_call" events can fire within one Provider.stream() call. Currently NOT documented in IC[2] invariants. |→ clarify |action-required: tech-architect add invariant to IC[2]: "INV4→ Multiple StreamEvent(kind='tool_call') events MAY be emitted within one Provider.stream() call when model requests parallel tools. Each event carries exactly one tool dict. TurnEngine accumulates these into Turn.tool_calls list." |source:[code-read IC[2] lines 444-455, agent-inference on parallel-tool-call SDK behavior]

BUILD-CHALLENGE[impl-eng, R1]: IC[5] TurnEngine + IC[1] Provider — assistant-message reconstruction responsibility gap |feasibility:M |issue: When model emits tool_use and SDK stream ends with stop_reason="tool_use", TurnEngine must construct an assistant Message to append BEFORE the tool_result user message. For Anthropic: this is `{role:"assistant", content:[{type:text,...}, {type:tool_use, id, name, input}, ...]}` — content-block list. For OpenAI: `{role:"assistant", content:"text...", tool_calls:[{id, function:{name, arguments}}, ...]}` — sibling fields. Who builds this message? IC[5] INV1 says "append tool_result Message to working messages list" but doesn't specify how the preceding assistant message is materialized. Three options: (a) TurnEngine builds canonical from accumulated StreamEvents — requires TurnEngine to know canonical Message shape (already does via Message dataclass, OK), (b) Provider exposes `get_final_message() → Message` after stream ends — adds contract surface but cleaner, (c) StreamEvent(kind="stop") carries `final_message: Message` field — preserves stateless-Provider contract. |→ clarify |action-required: tech-architect ADR[3]/IC[5] specify: option (c) — StreamEvent(kind="stop") on tool_use stop_reason MUST carry the reconstructed canonical assistant Message in a new field `final_message: Message | None`. TurnEngine appends final_message + tool_result messages before re-invoking stream. Provider owns reconstruction (it has the SDK context); TurnEngine owns orchestration. Matches stateless-Provider invariant. |source:[code-read IC[5] lines 527-559, IC[1] lines 403-441, agent-inference on SDK reconstruction patterns]

BUILD-CHALLENGE[impl-eng, R1]: ADR[3] + IC[5] INV2 — max_tool_calls stop-reason injection vs final-model-response |feasibility:M |issue: IC[5] INV2 says "at count > max_tool_calls, inject synthetic StreamEvent(kind='stop', stop_reason='max_tool_calls')." This TRUNCATES the turn after 5 tool executions with NO opportunity for model to emit final text response. User gets a Turn with 5 tool_calls and empty text content. Alternative behavior: on 5th tool_result, re-invoke Provider.stream(tools=None) forcing a text-only final response. Source-plan line 226 is ambiguous ("force stop_reason='max_tool_calls'"). UX impact: under current IC[5], autonomous loop with a stuck-in-tool-call-loop model produces no explanatory turns — violates M1b success criterion's implicit UX. |→ clarify |action-required: tech-architect ADR[3] or new ADR specify max_tool_calls behavior. Recommendation: INV2 revised to "at count == max_tool_calls, execute final tool_result as normal, then re-invoke Provider.stream(tools=None) ONE MORE TIME for final text response. Set stop_reason='max_tool_calls' on resulting Turn. This adds +1 SDK call per max-hit turn but preserves final-text invariant." |source:[code-read IC[5] INV2 line 557, agent-inference on UX implication]

BUILD-CHALLENGE[impl-eng, R1]: ADR[4] + PM[1] — Anthropic interleaved-content round-trip lossiness is LARGER than PM[1] acknowledges |feasibility:M |issue: PM[1] mitigation (c) says "document known-lossy cases explicitly in message_mapping.py docstring." Known-lossy cases include: (1) Anthropic assistant with [text, tool_use, text, tool_use, text] pattern — OpenAI flat form has text as single content string + tool_calls sibling list; ordering of text-before vs text-between vs text-after is UNRECOVERABLE. (2) Anthropic tool_result content can be [{type:text}, {type:image}] — OpenAI role="tool" content must be string; images are lost. (3) Anthropic `cache_control: ephemeral` markers on specific content blocks — no OpenAI equivalent. Lossiness (1) matters for REPLAY — if JSONL stores canonical OpenAI-shape, `replay(jsonl) → ConversationState → re-materialize Anthropic messages` loses text-interleaving. (2) matters for multi-modal (M4 scope, OK to defer). (3) matters for cost optimization (defer). |→ revise |action-required: tech-architect ADR[4] specify CANONICAL storage rule: "If assistant message has interleaved text+tool_use blocks, canonical stores `content` as the concatenation of text blocks joined with '\\n' separator (OpenAI-compat), AND an optional `preceding_text_per_tool_call: list[str]` field on Message for fidelity. `preceding_text_per_tool_call[i]` = text preceding tool_calls[i]." This is the SAME information source as ToolCallRecord.preceding_text — consolidate. PM[1] mitigation list gets a new (d): "preceding_text stored per-tool-call on canonical Message enables reconstruction of Anthropic content-block order on to_sdk." |source:[code-read ADR[4] lines 230-244, PM[1] lines 685-692, cross-reference ToolCallRecord.preceding_text IC[3] line 493]

BUILD-CHALLENGE[impl-eng, R1]: SQ7 estimate 1.5h for streaming-only message_mapping.py |feasibility:M(too-tight) |issue: SQ7 at 1.5h for M1a streaming-only paths: Anthropic expand content:str→[{type:text,...}] + collapse back on from_sdk, plus Ollama identity. Plus fixtures (text-only × 4 roles = system/user/assistant/tool canonical cases). Plus SQ12d test_message_mapping round-trip merge gate tests (separate 1.5h SQ). 1.5h for the mapping CODE is arguably OK but docstring + edge-case thinking (empty content, empty list, None roles) pushes it to 2h. For SQ15 (M1b tool-use paths) at 2.5h: per my earlier challenge to edge cases (6-case matrix: text-only/tool-call-only/text-then-tool/tool-then-text/parallel-tools/malformed-args), actual implementation + fixture construction + debugging iteration is 3.5-4h. |→ revise |action-required: Adjust estimates. SQ7: 1.5h→2h. SQ15: 2.5h→4h. SQ23 (test_message_mapping tool-use expansion): 2h→3h. Adjusted M1a total: 14h→14.5h. Adjusted M1b total: 18h→20.5h. Grand total: 32h→35h with parallelization. Still reasonable. |source:[agent-inference on test fixture construction overhead + per-direction edge-case matrix, code-read SQ table lines 617-636,666-674]

BUILD-CHALLENGE[impl-eng, R1]: SQ8 conversation.py 1h for Turn + ConversationState + PreambleVariant |feasibility:L(OK) |issue: 1h is reasonable for dataclasses. BUT: ConversationState.system_preamble is "rendered from variant + roster" per source-plan line 206 — this is a RENDERING FUNCTION not a field. Needs template logic: for each PreambleVariant, format string with participant names. For identity-aware variant, include per-model display_names. This rendering logic is ~30min beyond dataclass definition. Propose splitting SQ8 → SQ8a (dataclasses, 0.5h), SQ8b (preamble rendering, 0.5h). |→ clarify |action-required: tech-architect specify whether system_preamble is a pre-rendered str field OR a computed @property. If computed, add explicit SQ8b. |source:[code-read SQ8 line 625, source-plan line 206]

BUILD-CHALLENGE[impl-eng, R1]: SQ9 turn_engine.py 2h for M1a RoundRobin+advance_stream |feasibility:M |issue: M1a scope excludes tool-exec loop (in SQ16). But advance_stream even without tool-exec must: (a) consume provider.stream async-iterator, (b) buffer StreamEvents + yield passthrough to caller, (c) accumulate content into Turn object, (d) extract TTFT from first token event, (e) extract usage/stop_reason from terminal event, (f) populate Turn.tokens_in/tokens_out/stop_reason/ttft_ms/total_ms/ts, (g) yield final Turn. Plus RoundRobin impl (trivial, 5min). Plus error-path handling: StreamEvent(kind="error") must produce Turn with stop_reason="error" + partial content. 2h is borderline — 2.5h realistic. |→ revise |action-required: SQ9 estimate 2h→2.5h. No plan change; just est refinement. |source:[code-read IC[5] invariants lines 545-552, SQ9 line 626]

BUILD-CHALLENGE[impl-eng, R1]: SQ10 persistence.py replay contract — ambiguity on partial-turn records |feasibility:M |issue: IC[7] says "persistence.replay(path) → ConversationState reconstructs state exactly." But what about partial turns? If session crashes mid-turn, last JSONL line may be turn WITH stop_reason="error" + partial content. Replay must handle this AND gracefully reject malformed trailing lines (e.g. JSON parse error on last line due to crash-during-write). Plan doesn't specify. |→ clarify |action-required: tech-architect ADR[7] or IC[7] add replay invariants: "INV1→ replay skips malformed trailing lines with warning log. INV2→ partial turn records (stop_reason='error') are INCLUDED in replayed state. INV3→ session_header must be valid first line; if missing, replay fails." Add SQ10b: "replay robustness tests — malformed trailing line, missing header, crash-mid-turn" (0.5h). |source:[code-read IC[7] line 596, agent-inference on persistence edge cases]

BUILD-CHALLENGE[impl-eng, R1]: SQ13 tool_schema.py 1h for 2-SDK schema conversion |feasibility:L(OK)-M |issue: Anthropic tool format: `{"name": str, "description": str, "input_schema": {...}}` where input_schema is JSON-schema. Ollama OpenAI-compat: `{"type": "function", "function": {"name": str, "description": str, "parameters": {...}}}` where parameters is JSON-schema. Conversion is mechanical. BUT: JSON-schema validation across SDKs has subtle differences (Anthropic accepts `additionalProperties: false`; OpenAI strict mode requires it). 1h includes light validation testing. OK. |→ accept |source:[code-read SQ13 line 649, agent-inference on JSON-schema drift]

BUILD-CHALLENGE[impl-eng, R1]: SQ14a anthropic_client.py tool-use streaming 2h |feasibility:M |issue: Anthropic messages.stream emits in order: message_start → content_block_start (type: text or tool_use) → content_block_delta (text_delta or input_json_delta) → content_block_stop → [repeat for next block] → message_delta (stop_reason + usage) → message_stop. Implementation must: (a) buffer input_json_delta accumulator PER tool_use block (id-keyed), (b) emit StreamEvent(kind="tool_call") atomically at content_block_stop for type=tool_use, (c) emit StreamEvent(kind="token") per text_delta for type=text, (d) emit StreamEvent(kind="stop", stop_reason=..., final_message=...) at message_stop with reconstructed canonical Message. 2h for (a)+(b)+(c)+(d) plus error-path is tight. 2.5-3h realistic. |→ revise |action-required: SQ14a 2h→2.5h. Adjusted M1b cluster E total impact: +0.5h. |source:[independent-research Anthropic SSE event taxonomy, agent-inference on accumulator implementation]

BUILD-CHALLENGE[impl-eng, R1]: SQ14b ollama_client.py tool-use streaming 2h — conditional on SQ6c smoke test |feasibility:L-H(conditional) |issue: If SQ6c (new: Ollama /v1 streaming+tool_calls smoke test, see first challenge above) PASSES: SQ14b implementation uses openai SDK's AsyncStream with chunk.choices[0].delta.tool_calls accumulator (OpenAI streams arguments as partial-JSON deltas). 2h estimate reasonable, similar to SQ14a. If SQ6c FAILS: SQ14b must add `ollama` pypi dep + use ollama.AsyncClient.chat(stream=True, tools=[]) instead, adapt chat response chunks to StreamEvent (per ollama-mcp-bridge pattern). Different code path; 2-2.5h. Either way estimate holds but the IMPLEMENTATION MIGHT DIVERGE — plan MUST NOT commit SQ14b approach until SQ6c lands. |→ conditional |action-required: Block SQ14b on SQ6c outcome. Update SQ graph: SQ6c blocks SQ14b. Add ADR note: "Ollama provider transport (openai-SDK vs ollama-SDK) is chosen empirically by SQ6c." |source:[own-earlier-challenge, code-read SQ14b line 651]

BUILD-CHALLENGE[impl-eng, R1]: PM[2] tool_use reliability on devstral-2:123b — 3/3 escalation threshold |feasibility:M |issue: PM[2] trigger-for-escalation is "fails 3/3 attempts across 3 different prompt phrasings." That's a REASONABLE decision rule but it blocks SQ24 (test_turn_engine_tools) progression with live-test noise. More concerning: if devstral works but produces malformed args 1/3 times (intermittent), PM[2] trigger as stated fails to fire — we stay with devstral AND inherit instability. Consider: ≥1 malformed tool_call in M1b verification run should downgrade reliability tag to "nominal" (plan already says this at line 697-698), AND the OVERALL M1b pair selection should be re-evaluated — maybe the ORDER is wrong and we should test alternate (deepseek) first. |→ clarify |action-required: PM[2] mitigation should specify: (a) test devstral-2:123b AND deepseek-v3.2:cloud in SQ6c smoke test (both Ollama cloud alternates) BEFORE committing to devstral; pick whichever has more reliable tool_use on echo round-trip for M1b. (b) Escalation thresholds: 3/3 fail → reliability="none" → swap seed pair. 1-2/3 malformed → reliability="nominal" → keep but flag in roster. 0/3 fail → reliability="reliable" → lock in. |source:[code-read PM[2] lines 695-700, agent-inference on stability testing]

BUILD-CHALLENGE[impl-eng, R1]: Test coverage of message_mapping MERGE GATE is under-specified on DIRECTION |feasibility:M |issue: ADR[4] round-trip test spec (lines 240-244) says "assert from_sdk(to_sdk(msg)) == msg." This tests canonical→SDK→canonical fidelity. But the ACTUAL round-trip in production is: canonical (from JSONL) → to_sdk → SDK sends to model → model response (SDK-native) → from_sdk → canonical (appended to state + written to JSONL). The PRODUCTION round-trip is canonical→SDK-outbound AND SDK-inbound→canonical, NOT to_sdk→from_sdk paired on the same message. Some lossiness only surfaces when inbound messages arrive in shapes we didn't round-trip-test (e.g. Anthropic response with cache_control markers, or OpenAI response with content=null + tool_calls). |→ revise |action-required: test_message_mapping.py MERGE GATE must test BOTH directions as independent properties: (i) outbound fidelity: canonical→SDK preserves all fields needed for model input (tested via fixture: known-canonical → known-SDK-shape equality). (ii) inbound fidelity: SDK-response→canonical preserves all fields needed for persistence + replay (tested via fixture: known-SDK-response-shape → known-canonical equality). Round-trip test from_sdk(to_sdk(msg))==msg is DERIVATIVE and weaker than testing both directions directly. Add SQ12d.2 and SQ23.2 inbound-direction test matrices. |source:[code-read ADR[4] lines 240-244, agent-inference on production data flow]

BUILD-CHALLENGE[impl-eng, R1]: Forward-plan M1c revision hook H2 — scope expansion is LOAD-BEARING for timeline |feasibility:M |issue: Forward-plan M1c revision hook H2 says "if M1b finds devstral-2:123b reliability='none', M1c scope expands to test ALL Ollama cloud + local models for tool_use reliability systematically." This is a POTENTIALLY 2-3x M1c scope multiplier. 10 Ollama providers × ~1h empirical tool-use test each = 10h additional M1c work, plus reliability calibration write-up. Plan allots "1-2 weeks after M1b ships" for M1c — that window might not hold with expansion. |→ clarify |action-required: forward-plan add explicit timeline-contingency line: "If revision hook H2 fires at M1b boundary, M1c baseline timeline 1-2w → 2-3w. Decompose empirical tool-use testing as parallel SQ matrix (10 providers × 1 test fixture) to keep wall-clock close to 1.5-2w." |source:[code-read forward-plan M1c revision hooks lines 800-803, agent-inference on empirical test scaling]

DB[impl-eng-top-1, H2-ollama-streaming-tool-use]: (1) initial: plan's Ollama tool-use path is unverified + potentially broken. (2) assume-wrong: what if ollama-mcp-bridge's warning is stale/wrong about /v1 specifically? Issue #12557 IS about /api/chat, not /v1 — the bridge may have misread. If so, /v1 streaming+tool_calls works fine and the plan is OK. (3) strongest-counter: XVERIFY gpt-5.4 said "uncertain(low)" — NOT a confirmed bug, just unverified. Ollama cloud has been iterating; 2026-04 behavior may differ from ollama-mcp-bridge's earlier observation. (4) re-estimate: risk is NOT that the plan is broken; risk is that we're betting M1b on unverified SDK behavior. The REMEDIATION is cheap: 15-minute smoke test (SQ6c) BEFORE committing 2h on SQ14b. (5) reconciled: this is a FEASIBILITY GAP not a plan-break. Add SQ6c; plan otherwise stands. If SQ6c fails we pivot; if passes we proceed with confidence.

DB[impl-eng-top-2, ADR4-message-mapping-direction-asymmetry]: (1) initial: round-trip test from_sdk(to_sdk(msg))==msg is weaker than specified-direction tests. (2) assume-wrong: what if round-trip IS sufficient because fidelity failures symmetrize (if outbound loses a field, inbound can't restore it, so the asymmetry collapses)? (3) strongest-counter: actually that argument supports my challenge — if fidelity failures symmetrize, then to_sdk(msg)→SDK→model→response→from_sdk loses DIFFERENT fields than from_sdk(to_sdk(msg)) round-trip. They're not the same test. (4) re-estimate: direction-asymmetric testing is strictly better, not redundant. (5) reconciled: finding stands; add inbound-direction fixtures to SQ12d and SQ23.

---

### implementation-engineer challenge summary
BC[R1, impl-eng]: 15 findings |feasibility:{L:2, M:11, H:1, conditional:1, L-H:1} |categories:{sdk-contract:3, ic-gap:3, sq-estimate:5, test-coverage:2, risk-calibration:2} |→ revise:5, clarify:8, accept:1, conditional:1 |load-bearing:{ollama-v1-streaming-tool_use(H-conditional), interleaved-content-lossiness(M), assistant-msg-reconstruction(M)} |source-provenance:{code-read:9, agent-inference:15, independent-research:2, external-verification:1 (XVERIFY openai:gpt-5.4 uncertain-low), cross-agent:0} |DB:#2 (H2-ollama + ADR4-direction-asymmetry) |XVERIFY-result:1 (openai:gpt-5.4 uncertain-low on H2) |→ ready-for-plan-track-R2-response-or-DA-round

---

### implementation-engineer R2 delta (post-DA round)
!scope: narrow response to 4 lead-directed items (DA7 CONFLICT1, DA6 golden fixtures, DA8 CONFLICT2, UD#2 escalation policy). R1 findings UNCHANGED; R2 appends clarifications + 1 new BC triggered by DA8 CONFLICT[2].

---

BC[impl-eng, R2-clarify-1]: DA7 CONFLICT[1] IC[2] dual-additions scope — three distinct schema surfaces, not two |response-to:DA[8] CONFLICT[1] + lead-R2-item-1

DA is correct that my BC #2/#3 and ui-ux E6/IC-flag[5] are distinct proposals. Four-agent convergence on IC[2] touches THREE schema surfaces:

(A) **StreamEvent.final_message on kind="stop"** (impl-eng BC #3, cqa EG3 assumes) — reconstructed canonical ASSISTANT Message when stop_reason="tool_use". Phase: END of Provider.stream() call, BEFORE tool execution. Purpose: give TurnEngine a valid prior-assistant Message to append before tool_result messages.

(B) **StreamEvent(kind="tool_result") emission** (ui-ux E6 / IC-flag[5]) — new event kind emitted by TurnEngine AFTER tool execution. Phase: BETWEEN Provider.stream() calls. Purpose: UI observability + metrics latency + ToolCallRecord timing.

(C) **Message.preceding_text_per_tool_call: list[str] | None** (impl-eng ADR[4] R1 challenge) — field on CANONICAL Message for interleaved-content fidelity across to_sdk/from_sdk. Phase: storage/persistence. Purpose: round-trip fidelity for Anthropic content-block interleaving.

**Scope verification:** (C) does NOT overlap (A) or (B). (C) = PERSISTENCE field. (A) = EVENT-LAYER field (StreamEvent transport). (B) = EVENT-LAYER new enum. They compose cleanly.

**However:** (A)'s implementation may depend on (C). If Provider populates `StreamEvent(kind="stop", final_message=Message(...))` from Anthropic content-blocks with interleaved [text, tool_use, text, tool_use], the Message MUST preserve block ordering — either via `preceding_text_per_tool_call` (C) or by flattening (loses ordering, breaks round-trip). Therefore: if (A) adopted AND fidelity-preserves content-blocks, (C) is REQUIRED as carrier field.

**Net schema additions:** 2 distinct if (A) uses (C) internally; 3 distinct if (A) flattens and (C) added only at persistence boundary.

**Recommendation:** tech-architect specifies `Message.preceding_text_per_tool_call: list[str] | None` as CANONICAL Message field, populated by Provider-reconstruction when building final_message (A). One field on Message dataclass; used in two contexts (event + persistence). DA8 CONFLICT[1] resolved: "two StreamEvent additions compose — (A)+(B); (C) is Message-schema field (A) uses internally."

|source:[cross-agent: DA[8] CONFLICT[1] + cqa BC-cqa-11 + ui-ux IC-flag[5]] + [own-R1: BC #2, BC #3, ADR[4]] + [agent-inference on schema-layer separation]

---

BC[impl-eng, R2-accept-1]: DA6 golden SDK fixtures — accept cqa's addition, complements my BC #14 direction-asymmetry |response-to:DA[6] + cqa BC-cqa-1 + lead-R2-item-2

cqa's BC-cqa-1 argues merge-gate needs hand-computed known-SDK-shape fixtures, not just round-trip identity. My R1 BC #14 argued from_sdk(to_sdk(msg))==msg is weaker than direction-specific tests. COMPLEMENTARY, not duplicative:

- **cqa's addition:** hand-computed golden fixtures for SDK shapes → canonical equality. Catches adapter bugs where from_sdk/to_sdk are symmetrically WRONG.
- **my BC #14:** test BOTH directions independently. Catches asymmetric lossiness.

Accepting DA6/cqa addition. BC #14 stands as separate concern. Combined test strategy for test_message_mapping.py:
  Tier 1: hand-golden canonical → SDK outbound (cqa BC-cqa-1)
  Tier 2: hand-golden SDK response → canonical inbound (impl-eng BC #14)
  Tier 3: round-trip from_sdk(to_sdk(msg))==msg (plan baseline, DERIVATIVE not primary)

→ no new estimate delta; already scoped in cqa SQ23 revision (2h→3h). I defer to cqa's EG1-EG5 coverage for IC[2] event-grammar testing per lead item 2.

|source:[cross-agent: cqa BC-cqa-1 + own BC #14 + DA[6]] + [agent-inference on test-strategy compositionality]

---

BC[impl-eng, R2-NEW-2]: DA8 CONFLICT[2] Provider statelessness vs reconstruction-state — RESOLVED via SDK context-manager semantics |response-to:DA[8] CONFLICT[2] + lead-R2-item-3

**DA caught a gap I missed in R1.** DA cold-read surfaced the stateless-contract question my R1 BC #3 left implicit: if Provider owns final_message reconstruction, does it need SDK session state across tool-exec boundary?

**Investigation (independent-research on SDK internals 2026-04):**
- **anthropic.AsyncAnthropic.messages.stream()** returns a `MessageStreamManager` context manager. Each `async with client.messages.stream(...) as stream` creates FRESH SSE connection + FRESH reconstruction buffer. `stream.get_final_message()` available AFTER iterator exhausts — WITHIN-CALL state, flushed at context exit. No session state between stream() calls.
- **openai.AsyncOpenAI.chat.completions.create(stream=True)** — same semantics: per-call stream, accumulator dies at close.

**Therefore:** Provider IS stateless-per-call per IC[1]. Reconstruction buffer is WITHIN-CALL scope. Between tool-exec iterations, TurnEngine re-invokes `provider.stream(messages=updated, ...)` → FRESH SDK call, FRESH accumulator. **No state leak, no contract violation.**

**Subtle related concern (cqa T7 flagged):** async-generator not-closed on early termination → SDK context manager may leak connection. CODE HYGIENE, not stateless-contract violation.

**SQ14a/14b estimate impact:**
- SQ14a: **NO estimate change.** 2.5h holds. Context-manager pattern handles cleanup; `stream.get_final_message()` built-in.
- SQ14b: **NO change IF SQ6c passes.** 2h holds. openai SDK uses same `async with`. **BUT +0.5h conditional** — if SQ6c fails and we switch to ollama pypi AsyncClient, that package's async iteration doesn't use context manager; close handling is caller's responsibility.

**Recommendation to tech-architect R2:** add IC[1] invariants:
  INV4→ "Provider.stream() reconstruction state is WITHIN-CALL only; across-call state forbidden. SDK context-manager semantics MUST be used for connection lifecycle."
  INV5→ "Provider.stream() MUST support early-termination cleanup via async-generator close() propagation to underlying SDK context."

Resolves DA[8] CONFLICT[2] without IC[1] architectural change. Explicitly permits within-call reconstruction state while preserving stateless-per-call invariant.

|source:[DA[8] CONFLICT[2]] + [independent-research anthropic MessageStreamManager + openai AsyncStream context manager] + [agent-inference on stateless-contract interpretation] + [cross-agent: cqa T7]

---

BC[impl-eng, R2-clarify-2]: UD#2 devstral→deepseek escalation — C2 code impact NONE for M1b if manual-gated |response-to:lead-R2-item-4

**Question:** does tech-architect R2's escalation policy (devstral tool_use_reliability="none" → swap to deepseek) affect C2 code structure (raw event capture consumer)?

**Answer — two cases:**

**Case A — MANUAL escalation (human-gated, RECOMMENDED for M1b):** lead/operator observes raw capture → changes `--models` CLI flag → re-runs. **NO C2 code impact.** ollama_client.py is generic (any Ollama cloud model via env/arg). Raw capture consumer in persistence.py writes sidecar regardless. Roster.py reliability tag updated manually post-observation. Behavior already implied by PM[2] spec.

**Case B — AUTOMATIC escalation (code-gated, DEFER to M1c+):** ollama_client.py or TurnEngine detects N malformed tool_calls → auto-swaps. Requires: malformed-args detection in Provider, runtime roster mutation, session-mid swap handling. **NOT in M1b scope.**

**Recommendation:** tech-architect keeps escalation MANUAL for M1b. PM[2] trigger is human-decision. SQ21 raw capture provides the observability. No consumer-side logic change needed. Automated escalation = NEW SQ for M1c if desired.

**SQ21 raw capture handles post-swap correctly:** when user swaps devstral→deepseek mid-experiment, deepseek's reliability tag is also "unknown" initially → sidecar continues. Same code path.

|source:[lead-R2 UD#2] + [own-R1: PM[2] challenge, SQ21 spec] + [agent-inference on manual-vs-automatic decomposition]

---

### R2 delta summary
BC[R2, impl-eng]: 4 deltas |clarify:2 (DA7 three-additions scope, UD#2 manual-escalation), accept:1 (DA6 golden fixtures complement), NEW:1 (DA8 CONFLICT[2] resolution — IC[1] INV4+INV5 proposed) |estimate-delta:{SQ14a:no-change, SQ14b:no-change-if-SQ6c-passes +0.5h-conditional-if-ollama-native} |cross-agent-alignment:high (DA caught 1 gap I missed; R2 closes via SDK context-manager semantics) |gap-acknowledged:1 (R1 BC #3 didn't explicitly address stateless-contract — R2 NEW-2 resolves) |DB:not-required-narrow-scope |XVERIFY:not-triggered-R2-budget-conservation
→ ready-for-tech-architect-R2-integration + subsequent DA R2 or lock-preparation

---

### code-quality-analyst challenges (build-track, R1 — post-tech-architect + impl-eng)

!scope: test-strategy + quality-gates ONLY. ¬architecture, ¬UX, ¬SDK-contract (impl-eng owns). |ΣVerify:available(advisory) |XVERIFY:deferred-to-DA-per-tech-architect (impl-eng consumed 1 on H2-ollama)

#### Boot-read summary
- Read plan-track tech-architect output (ADR[1-8] + IC[1-7] + SQ[1-27] + PM[1-3] + DB[ADR1/3/4]). Ui-ux-engineer wrote Q3 forward plan (4 phases, 8 revision hooks) — out-of-scope for my test-strategy challenge; no M1a/b UI code.
- Read impl-eng R1 challenges (15 BC). Overlap-check: impl-eng BC #14 ("test_message_mapping direction asymmetry") converges with my BC[cqa-1] on direction-asymmetric fixtures — independent arrival strengthens confidence. Impl-eng BC #10 (replay partial-turn contract) converges with my BC[cqa-4]. Impl-eng owns SDK-contract risk; I own test-coverage adequacy.
- Read sigma-verify tests/ for pattern study. [code-read test_clients_anthropic.py:83-177] [code-read test_clients_ollama_base.py:140-227] [code-read test_clients.py:13-51]
- Read sigma-verify src/clients.py:1-120 for error-classification taxonomy. [code-read clients.py:12-48]
- !gap-noted: sigma-verify has ¬streaming tests (call() sync). Chatroom breaks new ground on per-SDK streaming event-shape fidelity — pattern-reuse budget is LOWER than plan-track's SQ plan assumes.

#### Challenge coverage-matrix — plan-track claims vs required test strategy

Format: `BUILD-CHALLENGE[cqa, R1]: {plan-element} |coverage:{H/M/L} |issue:{description} |→ {revise|clarify|accept} |source:{type}`

---

**BC[cqa-1]: test_message_mapping.py MERGE GATE — SQ12d (M1a, 1.5h) + SQ23 (M1b, 2h) FIXTURE MATRIX**
coverage:**L** |load-bearing:YES (elevated-risk by ADR[4] + PM[1])
!cross-agent-convergence: impl-eng BC #14 independently flagged direction asymmetry. This extends with fixture specificity.

issue: Plan-track's ADR[4] round-trip spec says "≥8 per SDK covering: system/user/assistant/tool roles, single-turn, multi-turn, tool_call with args, tool_result with content, tool_result with error, mixed text+tool_call." **Grossly insufficient** for MERGE GATE given PM[1] acknowledges interleaving-loss is KNOWN LOSSY in OpenAI-shape canonical.

Missing fixtures that actually matter:
  F1→ **tool_use_id preservation round-trip.** Anthropic tool_use block has `id` field; Ollama tool_calls has `id`; canonical must preserve across to_sdk → from_sdk. ¬in spec. Subtle ID-rewrite bug → malformed tool_result threading → models silently reject.
  F2→ **role attribution fidelity: role="tool" vs content-block role.** Anthropic tool_result lives inside user message content-blocks (role="user"!). Canonical: role="tool". Must verify Anthropic adapter ¬misroutes tool_result as literal "tool" role (Anthropic rejects). ¬in spec.
  F3→ **multi-tool-call-per-turn ordering.** Model emits 3 tool_calls in one assistant turn. Order must preserve both directions. "Multi-turn" in plan-track = multiple Turns, ¬multiple tool_calls in one Turn. Different axis, same risk.
  F4→ **interleaved content: [text, tool_use, text, tool_use, text].** PM[1] explicitly calls LOSSY. ADR[4] lists only "mixed text+tool_call" (one of each). Round-trip fidelity for 5+ interleaved blocks must be tested; lossy behavior must be EXPLICITLY asserted. Prose-only contract, ¬enforced, without this test. Note: impl-eng BC #5 proposes `preceding_text_per_tool_call: list[str]` on Message for reconstruction — if accepted, F4 asserts reconstruction fidelity.
  F5→ **empty/null argument variants.** tool_use with `input={}` vs omitted vs None. Anthropic SDK emits `input={}`; canonical round-trips as `arguments={}`. If canonical maps empty-dict to None, round-trip fails silently.
  F6→ **malformed JSON arguments from model.** Devstral-2 edge case (PM[2]): model emits truncated JSON string. Canonical must have explicit fallback (arguments=None + error flag) AND round-trip must exercise it. ¬in spec.
  F7→ **tool_result content variants: string | error-string | empty-string.** Anthropic tool_result content can be [text]+[image]. M1a/b scope: text only — test must ASSERT non-text content raises or is rejected (¬silently dropped).
  F8→ **cache_control marker round-trip (forward-compat).** Anthropic prompt caching may arrive M2+. Canonical schema must NOT silently drop unknown fields. Fixture: canonical Message with `extra={"cache_control":{"type":"ephemeral"}}` through adapter → either survives OR adapter REJECTS unknown fields. Either contract OK; NO contract is the failure mode.

!direction-asymmetry (confirms impl-eng BC #14): round-trip from_sdk(to_sdk(msg))==msg is DERIVATIVE. MERGE GATE must test both directions as independent properties — outbound (canonical→SDK) AND inbound (SDK-response→canonical) with separate fixture sets.

Proposed revision: F1-F7 MUST for M1b merge gate (SQ23). F8 SHOULD for M1a (SQ12d). Plus direction-asymmetric fixtures per impl-eng BC #14.

estimate-revision: SQ12d **2h** (from 1.5h); SQ23 **3h** (from 2h). Aligns with impl-eng's independently-derived 2h→3h recommendation.
→ revise |source:[code-read plan-track ADR[4]+PM[1]] + [agent-inference] + [independent-research Anthropic SDK tool_use content-blocks] + [cross-agent: impl-eng BC #14]

---

**BC[cqa-2]: Streaming event-shape fidelity — SQ12a mock_providers.py (1h) + SQ12c test_providers_streaming.py (2h)**
coverage:**M** |load-bearing:YES

issue: SQ12a = 1h for mock_providers.py; SQ12c = 2h per-SDK streaming. Gaps:
  G1→ **Mock fidelity to real Anthropic event sequence.** Mock must simulate `message_start → content_block_start → content_block_delta(text_delta) → content_block_delta(input_json_delta for tool_use) → content_block_stop → [repeat] → message_delta(usage+stop_reason) → message_stop`. **2-3h MINIMUM**, not 1h. Mock diverges from real SDK order → tests pass while prod breaks. [independent-research Anthropic Messages streaming SSE events]
  G2→ **Ollama OpenAI-compat streaming mock.** Ollama returns chunks with `tool_calls` args ACCUMULATED ACROSS CHUNKS (partial JSON over multiple deltas). Mock must chunk args character-by-character; client MUST accumulate. Without test, ollama_client works on toy cases, breaks on tools with args >50 chars. [independent-research OpenAI chat.completions streaming tool_calls delta]

Missing test cases:
  S1→ TTFT captured — first yield of kind="token" → ttft_ms populated. Time-travel fixture (freeze monotonic_ns).
  S2→ stop_reason taxonomy test — 6 stop_reasons (end_turn, max_tokens, tool_use, max_tool_calls, error, stop) each produced under right condition.
  S3→ Usage extraction positive AND negative — missing fallback-to-0 per source-plan risk-table.
  S4→ Stream interrupted mid-message — network drop must emit StreamEvent(kind="error") per IC[2], not raise.

estimate-revision: SQ12a **2h** (from 1h). SQ12c at 2h covers S1-S4 adequately post-mock-fidelity.
→ revise |source:[code-read IC[2]+IC[5]] + [agent-inference] + [independent-research Anthropic+OpenAI SDK streaming]

---

**BC[cqa-3]: TurnEngine tool-exec loop state-machine — SQ24 (test_turn_engine_tools.py, 2h)**
coverage:**L** |load-bearing:YES (PM[3] flags "known sharp edges")

issue: 2h for "tool-exec loop, cap enforcement, ToolCallRecord fields". PM[3] enumerates 3 specific async-state-machine risks. Test spec does not map to risks.

Required cases mapped to failure modes:
  T1→ Single tool_call happy path. (Baseline.)
  T2→ Multi-tool-call sequence (3 in one Turn). position_in_turn monotonic 0,1,2; preceding_text per call. ToolCallRecord INV1+INV2. ¬in plan-track.
  T3→ max_tool_calls=5 boundary. 4 succeed, 5th → synthetic stop. Turn.stop_reason="max_tool_calls". IC[5] INV2. (Note: impl-eng BC #4 proposes revising INV2 to allow final text response after 5th tool — T3 test contract depends on that resolution.)
  T4→ Tool execution error propagation (PM[3] risk C). Tool raises → ToolCallRecord.error populated, StreamEvent(kind="error") emitted, Turn.stop_reason="error". Contract choice — MUST test either way.
  T5→ Tool returns malformed (non-serializable) result. Must coerce to str or raise-caught. ¬in spec.
  T6→ **Stream error AFTER tool_call emitted but BEFORE tool_result appended.** Provider emits tool_call, then stream raises. TurnEngine must: (a) NOT execute the tool, (b) emit error, (c) Turn.tool_calls=[] (no partial record). PM[3] risk (a)+(c). ¬in spec.
  T7→ Provider state cleanup after error — consecutive advance_stream calls → no memory leak. Async-generator not-closed regression. ¬in spec.
  T8→ ts_started/ts_completed use monotonic clock. PM[3] (b). Mock monotonic_ns, verify latency_ms = (completed-started)//1_000_000, NOT wall-clock.
  T9→ Re-entry after tool_result — canonical Message list updated correctly. Mock provider inspects messages on SECOND stream call, asserts tool message appears. IC[5] INV1. ¬tested.

estimate-revision: SQ24 **3h** (from 2h). Minimum T1+T3+T4+T6+T8+T9 (INV/PM-mandated); T2+T5+T7 SHOULD if time.
→ revise |source:[code-read IC[5]+PM[3]+ToolCallRecord INV1/INV2] + [agent-inference] + [pattern: pytest-asyncio async-gen cleanup]

---

**BC[cqa-4]: JSONL persistence — SQ12g (1h) + SQ26 raw-sidecar (0.5h)**
coverage:**M**
!cross-agent: impl-eng BC #10 flagged replay contract ambiguity on partial turns. Mine complements with schema-version + determinism.

issue:
  J1→ **schema_version forward-compat behavior unspecified.** v2 reader encounters `schema_version: "1"` record — what happens? ADR[7] doesn't specify reader policy. Must assert v2 raises `SchemaVersionMismatch` with actionable message (or migration layer passes through). Without test, v2 introduction = silent break.
  J2→ **Round-trip determinism with int fields.** `ttft_ms`, `total_ms` — JSON serializes whole numbers ambiguously. Must assert int-typed post-load.
  J3→ **Partial flush during process kill.** JSONL, write 3 lines, SIGKILL. Replay must tolerate last-line-truncation. Contract: replay() either (a) silently drops with warning, or (b) raises `CorruptedSessionError` with recovery hint. Converges with impl-eng BC #10; I add fixture spec.
  J4→ **Raw sidecar correlation with main JSONL.** Every tool_call in main must have corresponding raw_event; timestamps align within 10ms; session_id in filename matches. ¬in spec.
  J5→ **ToolCallRecord when model emits tool_call but NEVER receives tool_result** (crash after emit, before exec). Record should have ts_started populated, ts_completed=null + error="uncompleted". IC[3] ts_completed typed `str` (non-optional) → partial records get dropped or lie. Contract must be tested.

→ revise |source:[code-read ADR[7]+IC[3]+IC[7]] + [agent-inference] + [cross-agent: impl-eng BC #10]

---

**BC[cqa-5]: CLI streaming to stdout — SQ11 (1h) + ZERO test allocation**
coverage:**L**

issue: SQ11 = 1h for cli.py. Plan-track allocates **ZERO hours for test_cli.py**. M1a success criterion IS "streamed to stdout + persisted to JSONL + replayable". Stdout streaming untested.

Required:
  C1→ Output buffering. print(..., flush=True) each token; test piped stdout shows tokens-not-chunks.
  C2→ Character encoding. UTF-8 explicit; test with non-ASCII fixture (en-dashes, curly quotes).
  C3→ Speaker attribution. Two models round-robin — CLI prefixes with speaker name. Contract+test missing.
  C4→ Graceful Ctrl-C. KeyboardInterrupt mid-stream flushes pending JSONL writes.

Add: **SQ12h — test_cli.py — 1.5h, owner:code-quality-analyst, deps:SQ11**.
→ revise |source:[code-read source-plan M1a success criterion] + [agent-inference] + [pattern: stdout buffering]

---

**BC[cqa-6]: Live-smoke test (CHATROOM_LIVE_TESTS=1) — NOT in SQ plan**
coverage:**L (absent)** |!cross-agent: feedback-memory 26.4.5 mock-tests-false-confidence

issue: SQ[1-27] ¬include live-smoke for M1a/b. Source plan line 88 specs test_live_smoke.py and line 345 the CHATROOM_LIVE_TESTS=1 invocation — but explicitly in **M3 verification**, ¬M1a/b.

Clarification: if plan intends live-smoke at M3, plan-track is correct. BUT: mock-only strategy for M1a/b = merge gate proves fidelity only against MOCK SDK shapes. Real SDK emits events mock doesn't replicate → merge gate passes, real run fails. Same failure mode as feedback-memory correction 26.4.5.

Note on overlap: impl-eng BC #1 proposes SQ6c (Ollama /v1 smoke test, 15min) — different scope (SDK contract verification pre-SQ14b, single API call). Mine proposes SQ12i/SQ28 as end-to-end pipeline tests (stream → tool-exec → JSONL). Complementary, not duplicative.

Proposed: **SQ12i — test_live_smoke_m1a.py — 1h, live-only, SKIP by default** (one Anthropic turn + one Ollama-cloud turn, streamed, JSONL written, no tools). **SQ28 — test_live_smoke_m1b.py — 1h** (one echo round-trip per provider).
gating: dual flag (CHATROOM_LIVE_TESTS=1 AND env keys present). cost: ~$0.01 Anthropic + free Ollama. Skip for local pytest default.
→ revise |source:[code-read source-plan verification] + [cross-agent: feedback 26.4.5 + impl-eng SQ6c complementary]

---

**BC[cqa-7]: StreamEvent error-convention — IC[1] INV3 vs IC[2] CONTRADICTION**
coverage:**L (¬tested, ¬contract-locked)**

issue: IC[1] INV3: "Provider.stream() raises ¬swallows exceptions — errors emerge as StreamEvent(kind='error', error=exc) for clean handling **OR propagated exception (choose one pattern — see IC[2])**." IC[2]: "Errors **ALWAYS emerge** as StreamEvent(kind='error', error=exc) — ¬raised exceptions across async iterator boundaries."

"Choose one" vs "ALWAYS emerge". **Contract contradiction.** Parallel engineers (SQ6a, SQ6b) flip coins → divergent error handling.

Resolution BEFORE SQ6a/SQ6b/SQ14a/SQ14b. Recommend: lock on IC[2]'s ALWAYS-emerge (stronger). Delete IC[1]'s "choose one" language. Add test: **SQ12j — test_stream_error_convention.py — 0.5h** — Provider raises in real path → assert StreamEvent(kind="error") emitted, no exception propagated.
→ clarify+revise |source:[code-read IC[1] INV3 vs IC[2]] + [agent-inference]

---

**BC[cqa-8]: DEAD CODE risk — forward-compat scaffolding**
coverage:**M**

issue: Scan of IC[1-7] + SQ[1-27]:
  D1→ `Provider.complete()` in IC[1]. ADR[8] says "stub for M1a; thin wrapper for M1b if needed". If M1b doesn't need it, dead signature. **Challenge: defer complete() to M1c. Remove from Protocol in M1a+M1b.**
  D2→ `raw_event: dict | None` in StreamEvent (IC[2]). If raw-capture path hooks SDK directly (not through StreamEvent), this field is unused. **Clarify: flows THROUGH StreamEvent (couples Provider to observability) or BESIDE (separate SDK callback)?**
  D3→ `registry.py` SQ4 — full registry module for 2 providers is over-engineered. **Challenge: simplest form (dict literal + available() helper, <30 LOC).** Extract if M1c expands.
  D4→ `PreambleVariant` in conversation.py (SQ8) — 3 variants but M1a/b use ONE. **Clarify test-burden: all 3 renderings in M1a, or only identity-aware default?** (Note: impl-eng BC #7 flagged preamble as rendering-function-not-field.)
  D5→ `ConversationState.tools_enabled: bool` — dead in M1a, activates M1b. **Accept**.

→ clarify+revise |source:[code-read IC[1]+IC[2]+SQ4+SQ8+SQ21] + [agent-inference] + [cross-agent: impl-eng BC #7]

---

**BC[cqa-9]: Style + docstring quality gates — UNSPECIFIED in plan-track**
coverage:**L (absent)**

issue:
  Q1→ pyright/mypy strictness level. Proposal: `pyright --strict` at CI gate, mypy backup. In pyproject.toml SQ1.
  Q2→ Docstrings on public API surface (Provider, Message, StreamEvent, CompleteResult, ToolCallRecord, TurnPolicy, TurnEngine.advance_stream, persistence.write_session/replay). Proposal: ruff pydocstyle D100/D102 pass threshold; exempt tests.
  Q3→ Style consistency: naming. **Accept** existing source-plan filenames.
  Q4→ Import ordering / dead imports. Ruff/isort standard.
  Q5→ Line length. Default ruff 88; lock in pyproject.

→ revise |source:[code-read source-plan file list + IC[1-7]] + [agent-inference]

---

**BC[cqa-10]: Test-execution strategy + CI**
coverage:**L (absent)**

issue:
  X1→ pytest-asyncio = strict (catches missing markers).
  X2→ CI matrix Python 3.11 + 3.12 minimum.
  X3→ Test tier structure per feedback-memory test-execution-pattern 26.4.6: `tests/` (unit+async, <1min), `tests/live/` (API-gated, opt-in, minutes).
  X4→ Coverage target 85% on providers/ + turn_engine.py (load-bearing); exempt cli.py main-guard.

→ revise |source:[cross-agent: feedback memory 26.4.6] + [agent-inference]

---

#### Edge-case challenge — beyond plan-track PM[1-3]

**EC[1]: Ollama cloud network hiccup mid-stream.** Does ollama_client.stream() retry on network blip or emit error immediately? **Recommend:** zero retries for M1a/b (research-instrument: fail fast + observable), explicit doc. Test via mock ConnectionError mid-stream.

**EC[2]: Anthropic rate-limit 429 mid-stream.** Per-provider Semaphore(1) protects against concurrent 429. Does 429 happen BEFORE stream start (clean raise) or MID-stream (partial content + error)? Test inject 429 at both points.

**EC[3]: Context overflow mid-generation.** Model exceeds 60% budget after N turns. TurnEngine must: (a) check budget BEFORE advance_stream(), (b) truncate-oldest per ADR[5], (c) emit `[truncated: N]` marker. No SQ owns this. **Question:** M1a scope or deferred? Source-plan Risks table suggests M1 scope. **Add SQ12k:** context truncation test 1h (paired with implementation SQ if tech-architect confirms M1a scope).

**EC[4]: YieldNextPolicy parse edge cases.** Spec: trailing `@next:<key>`. Cases:
  - `@next: claude-opus-4-7` (space after colon)
  - `@next:claude-opus-4-7.` (trailing period — common)
  - `@next:Claude-Opus-4-7` (case mismatch)
  - Multiple @next: in same turn (first? last? error?)
  SQ27 at 1h combined covers basic happy only. **Recommend split: 1h yield-next + 0.5h random.**

**EC[5]: RandomPolicy determinism for tests.** Tests MUST seed RNG. If RandomPolicy uses module-level random.choice without injectable seed, tests flaky. **Challenge:** RandomPolicy accepts optional `rng: random.Random = None`; default module random; tests pass seeded instance.

#### Source-provenance ledger
All BC[cqa-1..10] + EC[1-5] source-tagged per §2d.
  - [code-read plan-track ADR/IC/SQ/PM] — grounded in tech-architect output
  - [code-read impl-eng R1 challenges] — cross-agent reference
  - [agent-inference] — where plan-track silent
  - [independent-research Anthropic/Ollama/OpenAI SDK] — event-shape claims
  - [cross-agent: feedback-memory 26.4.5 mock-tests-false-confidence, 26.4.6 test-execution-pattern]

No T3 sources. No [prompt-claim] findings requiring corroboration.

#### Analytical hygiene (§2a/§2b/§2c/§2e)

**§2a positioning.** My challenges CONTRADICT plan-track in BC[cqa-1..3] severity (plan-track treats test strategy as thin-coverage adequate; I assess ~50% underestimated). Outcome **1** — CHECK CHANGES ANALYSIS. Revised: SQ12d 1.5h→2h, SQ23 2h→3h, SQ24 2h→3h, SQ12a 1h→2h. **Converges with impl-eng BC #14 (direction asymmetry) + BC #10 (replay) + BC #8 (SQ estimates) — independent-arrival pattern strengthens confidence.**

**§2b calibration.** Precedent for under-specified test strategy on elevated-risk adapter: feedback memories mock-tests-false-confidence (26.4.5), realistic-tests (26.4.6), test-execution-pattern (26.4.6). Pattern: every prior audit where test estimate was halved, real tests surfaced bugs mock-only missed. Calibration: SQ23 at 2h below-threshold. Outcome 2 → confirms with flagged risk.

**§2c cost/complexity.** Revised adds ~6-8h to M1a+M1b (14h parallelized → 20-22h, plus impl-eng's +3h stacking = ~38-40h total). ~+20-25% on 32h build. Justified for merge-gate tests (PM[1] concedes elevated risk). Live-smoke (+2h) directly addresses feedback-memory correction.

**§2e premise viability.** Core premise: "plan-track's test estimates are calibrated below what load-bearing merge gates demand." Viable — supported by 3 prior-correction patterns + line-by-line SQ comparison + cross-agent convergence with impl-eng.

#### DB[] — dialectical bootstrapping on top-2 highest-conviction challenges

**DB[BC-cqa-1 — message_mapping merge gate fixture expansion].**
  (1) initial: SQ12d (1.5h) + SQ23 (2h) grossly insufficient given PM[1] known-lossy. Expand to 2.5h + 4h.
  (2) assume-wrong: what if 8 fixtures IS adequate and I'm over-engineering?
  (3) strongest-counter: For research instrument (¬security-critical), F1+F3+F6 are the three that block end-to-end correctness; F2+F4+F5+F7 are defensive. Maybe +1.5h total.
  (4) re-estimate: F1+F3+F6 non-negotiable (merge gate demands them). F2+F4+F5+F7 strong defensive — skipping creates silent-failure surface. Hybrid: F1+F3+F6 MUST, F2+F4+F5+F7 SHOULD. Impl-eng BC #14 direction-asymmetry independently arrived at both-direction coverage need.
  (5) reconciled: **SQ12d → 2h (+F5+F7+F8). SQ23 → 3h (+F1+F3+F6 minimum; F2/F4 time-permitting; direction-asymmetric per impl-eng).** ~50% over plan-track; convergent with impl-eng.

**DB[BC-cqa-3 — TurnEngine tool-exec state-machine test coverage].**
  (1) initial: SQ24 at 2h is half what PM[3] demands. Expand to 4h.
  (2) assume-wrong: T1+T3+T4 cover minimum; T2+T5+T6+T7+T8+T9 over-engineered for M1a/b?
  (3) strongest-counter: T9 IS IC[5] INV1 (non-negotiable). T8 IS PM[3] (b) (non-negotiable). T6 IS PM[3] (a)+(c) (non-negotiable). Minimum T1+T3+T4+T6+T8+T9 = 6 cases.
  (4) re-estimate: 6 cases × ~30min = 3h. Less than initial 4h but 50% over plan-track's 2h. Impl-eng BC #4 flags max_tool_calls behavior needs revision — T3 contract depends on that.
  (5) reconciled: **SQ24 → 3h (MUST T1+T3+T4+T6+T8+T9; T2+T5+T7 SHOULD; T3 contract depends on impl-eng BC #4 resolution).**

#### Summary of reconciled positions for plan-track ITERATE round

**MUST revise (merge-gate adequacy):**
  1. SQ12d (message_mapping streaming): 1.5h → 2h. +F5, F7, F8; direction-asymmetric split.
  2. SQ23 (message_mapping tool-use MERGE GATE): 2h → 3h. +F1, F3, F6 (non-negotiable); F2/F4 time-permitting; direction-asymmetric.
  3. SQ24 (turn_engine tool-exec): 2h → 3h. +T6, T8, T9 (INV/PM-mandated).
  4. SQ12a (mock_providers.py fidelity): 1h → 2h. Anthropic event-sequence accuracy load-bearing.

**SHOULD add (gaps):**
  5. SQ12h test_cli.py — 1.5h. (BC-cqa-5)
  6. SQ12i + SQ28 live-smoke tests — 2h total. (BC-cqa-6)
  7. SQ12j test_stream_error_convention — 0.5h. (BC-cqa-7, after IC[1]/IC[2] reconciliation)
  8. SQ12k context-truncation test — 1h. (EC[3], pending tech-architect M1a-scope decision)

**MUST clarify (contract contradictions + dead code):**
  9. IC[1] INV3 vs IC[2] error-convention — lock on IC[2] ALWAYS-emerge. (BC-cqa-7)
  10. raw_event on StreamEvent — field vs separate hook? (BC-cqa-8 D2)
  11. PreambleVariant test coverage M1a — all 3 or default? (BC-cqa-8 D4)
  12. YieldNextPolicy parse edge cases — error vs fallback. (EC[4])

**SHOULD accept + lock (style + infrastructure):**
  13. pyright --strict + pydocstyle + ruff in pyproject.toml. (BC-cqa-9)
  14. pytest-asyncio = strict. (BC-cqa-10 X1)
  15. Test tier structure: tests/ vs tests/live/. (BC-cqa-10 X3)
  16. Coverage target 85% on providers/ + turn_engine.py. (BC-cqa-10 X4)

!deferred-for-DA: BC-cqa-1 fixture expansion fidelity depends on SDK documentation — DA could XVERIFY that F1-F8 coverage IS what merge-gate rigor demands. Plan-track's claim is self-assessment; cross-model verification recommended. (Budget-aware: impl-eng already consumed 1 XVERIFY on H2-ollama; leave rest for DA.)

---

**BC[cqa-11]: IC[2]/IC[5] CLUSTER test-strategy — addresses lead-highlighted triple convergence**
coverage:**L** |load-bearing:YES
!cross-agent-convergence: triple — impl-eng BC #2 (IC[2] parallel tool_calls INV4 missing) + impl-eng BC #3 (IC[5] assistant-message reconstruction via `final_message` on stop event) + ui-ux-engineer E6/IC-flag[5] (missing `kind="tool_result"` StreamEvent post-exec). All three propose expanding IC[2] event taxonomy. Lead flagged this cluster as elevated-risk for test strategy.

issue: IC[2] as currently specified has 4 `kind` values: token, tool_call, stop, error. After incoming revisions propose 2 additions:
  (a) INV4 addition — multiple `kind="tool_call"` events per Provider.stream() call allowed (impl-eng BC #2)
  (b) `final_message: Message | None` field on kind="stop" when stop_reason="tool_use" (impl-eng BC #3)
  (c) new `kind="tool_result"` event emitted by TurnEngine post-exec (ui-ux E6)

If all three land, IC[2] state machine becomes: `token* → (tool_call+ → stop(tool_use, final_message) → tool_result+)* → token* → stop(end_turn|max_tokens|max_tool_calls|error)`. This is a materially richer event grammar than plan-track's current spec. **Test strategy implication: SQ22 (test_providers_tool_use, 2h) + SQ24 (test_turn_engine_tools, 2h→3h per my BC-cqa-3) do NOT currently cover this event-grammar state machine.**

Required test additions if IC[2] cluster-revision accepted:
  EG1→ **Event grammar conformance test** (property-based, pytest hypothesis-style OR table-driven). Given a sequence of StreamEvents, assert it conforms to the grammar above. Catches: tool_result emitted without preceding tool_call (orphan); stop emitted with final_message=None after tool_use (contract violation); token emitted after final stop (post-stream leak).
  EG2→ **Parallel tool_call accumulation test** (INV4). Provider.stream() yields 3 kind="tool_call" events sequentially. Test: TurnEngine accumulates into Turn.tool_calls ordered by emission; each has distinct tool_use_id; TurnEngine executes all 3 before re-invoking stream with tool_results.
  EG3→ **final_message reconstruction fidelity.** StreamEvent(kind="stop", stop_reason="tool_use", final_message=Message(...)) — reconstructed assistant Message must match what Anthropic emitted content-block-by-content-block. Round-trip test: mock Anthropic response with [text, tool_use, text, tool_use] → stream → collect → final_message equals canonical expected shape. This is MESSAGE-MAPPING round-trip BUT triggered by stream-reconstruction path, not by adapter.to_sdk() directly. Gap: currently SQ23 (message_mapping tool-use merge gate) tests adapter-called-from-test; EG3 tests adapter-called-from-stream-reconstruction. Different code paths, same adapter.
  EG4→ **tool_result event correlation.** Every kind="tool_result" carries tool_call_id matching a prior kind="tool_call" within the same turn. Orphan tool_result = test failure. Mock that emits orphan → assert TurnEngine rejects or logs-and-drops per contract.
  EG5→ **max_tool_calls with final-text-response** (if impl-eng BC #4 accepted, T3 changes). After 5th tool_result, TurnEngine re-invokes stream(tools=None). Test: assert 6th Provider.stream call has tools=None, yields text-only, terminates with stop_reason="max_tool_calls" (not "end_turn" despite clean termination).

!test-file-impact: SQ22 (test_providers_tool_use.py) + SQ24 (test_turn_engine_tools.py) BOTH expand. SQ22 (provider-side) owns EG2+EG3 (per-SDK parallel emission + final_message reconstruction). SQ24 (engine-side) owns EG1+EG4+EG5 (event grammar, correlation, max_tool_calls behavior).

estimate-revision (conditional on IC[2] cluster-revision acceptance):
  SQ22: 2h → **3h** (+EG2, EG3 per-SDK × 2 SDKs)
  SQ24: 2h → **3h already proposed in BC-cqa-3**; EG1+EG4+EG5 fit within that 3h (same state-machine focus, reinforces T6/T9 coverage)

If tech-architect R2 REJECTS the IC[2] cluster-revision (stays with 4-kind taxonomy), BC[cqa-11] is moot — but the rejection itself becomes a critical test surface (no tool_result observability = metrics panel in M3 can't render latency; UI in M2 can't show "tool executing" state). Either acceptance or rejection, the test strategy must be explicit about the event grammar.

→ **revise conditional on tech-architect R2** |source:[cross-agent: impl-eng BC #2+#3 + ui-ux E6/IC-flag[5]] + [code-read IC[2] lines 444-455 + IC[5] INV1-INV3] + [agent-inference on event-grammar completeness]

---

#### R2 delta — response to DA cross-refs (lead wake 2026-04-20)

!scope: 4 narrow DA-triggered items. R2 = delta on R1, ¬re-litigation.

**R2-Δ-1: DA6 golden SDK fixtures — REAL GAP, adds to BC[cqa-1]**
DA challenge: round-trip `from_sdk(to_sdk(msg))==msg` passes **symmetric field-loss** bugs — if adapter loses field X in both directions, round-trip is lossless but the SDK payload is wrong. My F1-F8 + direction-asymmetric approach (BC[cqa-1]) still ultimately tests canonical → canonical equality. ¬same as asserting the EXACT SDK wire shape.

Remediation (complementary to F1-F8 + direction-asymmetry, ¬replacement):
  G-F1→ **hand-computed Anthropic golden fixture** — file `tests/fixtures/anthropic_golden.py` with 4-6 pre-computed SDK payloads (content-block dicts exactly as Anthropic SDK would emit). Assert: `to_sdk(canonical_fixture) == anthropic_golden_expected[i]` for each — NOT round-tripped. Catches: adapter emits wrong SDK field names, drops content-blocks, mis-orders tool_use/text interleaving, etc.
  G-F2→ **hand-computed OpenAI/Ollama golden fixture** — file `tests/fixtures/openai_golden.py` with pre-computed chat-completion message dicts. Assert `to_sdk(canonical) == openai_golden_expected[i]`.
  G-F3→ **hand-computed inbound goldens** — file `tests/fixtures/anthropic_responses_golden.py` + `openai_responses_golden.py` with pre-computed SDK *response* shapes. Assert `from_sdk(sdk_golden_response) == canonical_expected[i]`. Inbound fidelity independent of outbound fidelity.

estimate-revision: SQ12d **2h → 2.5h** (from R1 2h; +G-F1+G-F3 anthropic goldens for streaming scope). SQ23 **3h → 3.5h** (from R1 3h; +G-F1+G-F2+G-F3 for tool-use scope, both SDKs both directions).
→ revise |source:[cross-agent: DA6] + [agent-inference on symmetric-field-loss semantics] + extends BC[cqa-1]

**R2-Δ-2: DA7 CONFLICT1 separability — clarifies BC[cqa-11] EG3+EG4**
DA challenge: IC[2]/IC[5] is TWO ADDITIONS (impl-eng BC #2 parallel tool_calls INV4 + impl-eng BC #3 final_message reconstruction) — EG coverage should test BOTH independently, ¬only the integrated state machine.

Verifying my R1 EG coverage maps separably:
  EG1 event grammar conformance — integrated (tests full state machine)
  EG2 parallel tool_call accumulation — **addresses INV4 independently** ✓
  EG3 final_message reconstruction fidelity — **addresses final_message independently** ✓
  EG4 tool_result correlation — integrated (requires both additions present)
  EG5 max_tool_calls final-text — integrated (requires BC #4 accept + tool_result)

Coverage IS separable: EG2 and EG3 can pass/fail independently. DA concern already addressed in R1 but framing wasn't explicit. Add framing note to BC[cqa-11]: "EG2+EG3 are independent-addition tests; EG1+EG4+EG5 are integrated-state-machine tests. If tech-architect R2 accepts only ONE of INV4 / final_message, EG2 or EG3 alone remains required — grammar EG1/EG4/EG5 become partial-state tests covering the one-addition case."

→ clarify (no SQ delta) |source:[cross-agent: DA7 CONFLICT1] + confirms BC[cqa-11] R1 structure adequate

**R2-Δ-3: DA4 GP2 gold-plating (Provider.complete) — CONFIRMS BC[cqa-8] D1**
DA independently flagged `Provider.complete()` as gold-plated with no M1a/b callers. This matches my BC[cqa-8] D1 exactly — I already recommended defer to M1c. If tech-architect accepts DA4, my SQ plan shed: no `test_providers_complete.py` needed, Provider protocol shrinks. Net ~0.25h test savings on tests not in my R1 SQ addition list (SQ12h-SQ12k + SQ22/SQ23/SQ24 revisions don't touch complete()). **Neutral-to-positive.**

→ accept DA confirmation |no SQ delta |source:[cross-agent: DA4 GP2] + BC[cqa-8] D1

**R2-Δ-4: DA5 forward-plan H2 decompose scope — CONFIRM SQ12i/SQ28 stay in-scope**
DA challenge: forward-plan M1c revision hook H2 (if devstral fails, sweep all 10 Ollama providers) may split code-work vs empirical-sweep; may affect M1a/b live-smoke scope if I straddled.

Verifying my SQ12i/SQ28 scope:
  SQ12i test_live_smoke_m1a.py — **1 Anthropic turn + 1 Ollama-cloud turn, streamed, JSONL written, NO TOOLS**. Code-path only. ¬reliability sweep.
  SQ28 test_live_smoke_m1b.py — **1 echo round-trip per provider on the M1 seed pair (Anthropic + ONE Ollama cloud)**. Code-path only. ¬reliability sweep.

Neither test straddles H2's 10-provider sweep. Both are strictly M1a/b code-path smoke. **H2's reliability sweep belongs in M1c per forward-plan; my SQ is M1a/b.** Confirmed scope separation.

→ accept + confirm scope separation |no SQ delta |source:[cross-agent: DA5] + BC[cqa-6] live-smoke spec

**R2 summary.**
R2 deltas: 2 real (R2-Δ-1 DA6 golden fixtures adds +1h total across SQ12d+SQ23; R2-Δ-2 DA7 clarifies BC[cqa-11] framing). 2 confirmations (R2-Δ-3 + R2-Δ-4, no SQ delta). Updated total-SQ-impact: +8-10h cqa alone (was +7-9h R1), ~39-41h stacked with impl-eng.

→ **R2-complete** |BC-additions:0 (R1 BC count stable at #11) |SQ-delta:+1h (SQ12d 2h→2.5h + SQ23 3h→3.5h) |clarifications:1 (BC[cqa-11] EG separability framing) |confirmations:2 (BC[cqa-8] D1 + BC[cqa-6] scope)

---

### code-quality-analyst challenge summary
BC[R1+R2, cqa]: 11 findings + 5 EC + 4 R2-deltas (2 real Δ1+Δ2, 2 confirmations Δ3+Δ4) |coverage-scores:{L:7, M:3, absent:3} |load-bearing:{message_mapping-fixture-matrix(L)+golden-fixtures(R2), streaming-mock-fidelity(M), tool-exec-state-machine(L), IC[2]/IC[5] event-grammar-cluster(L, separable EG2/EG3)} |source-provenance:{code-read:13, agent-inference:17, independent-research:3, cross-agent:9 (impl-eng BC #2/#3/#4/#7/#8/#10/#14 + ui-ux E6/IC-flag[5] + feedback-memory 26.4.5/26.4.6 + DA R2 rounds)} |DB:#2 (BC-cqa-1 + BC-cqa-3) |XVERIFY:not-triggered-budget-aware |cross-agent-convergence:4+DA-rounds (impl-eng/ui-ux originals + DA6 golden-fixture + DA7 separability-clarification + DA4 GP2 + DA5 H2 scope) |→ revise:11, clarify:4, accept:3-style-lockin, add-SQ:5 (SQ12h+SQ12i+SQ12j+SQ12k+SQ28), revise-SQ:{SQ12d 1.5h→2.5h, SQ23 2h→3.5h, SQ24 2h→3h, SQ12a 1h→2h, SQ22 2h→3h conditional} |merge-gate-coverage-score:L→M-with-revisions-and-golden-fixtures |edge-case-gaps:#5 |→ R2-complete →  ready-for-C2-dispatch

### code-quality-analyst ↔ tech-architect ITERATION

**Open questions for tech-architect to resolve BEFORE C1 convergence:**
Q1→ IC[1] INV3 vs IC[2] contradiction — lock one. (BC-cqa-7)
Q2→ ADR[4] fixture expansion F1-F7 + direction-asymmetry (converges with impl-eng BC #14) — accept? (BC-cqa-1)
Q3→ raw_event on StreamEvent coupling — field vs separate hook? (BC-cqa-8 D2)
Q4→ context-truncation M1a scope — in or deferred? (EC[3])
Q5→ Provider.complete() — keep as M1b stub or defer to M1c entirely? (BC-cqa-8 D1)
Q6→ PreambleVariant test coverage M1a — all 3 or default only? (BC-cqa-8 D4)

**Proposed revised SQ total impact (mine + impl-eng BC #8 stacked):** M1a+M1b parallelized: **~38-40h** (was 32h; +~20-25%). Justified by merge-gate rigor + PM-mapped state-machine coverage + anti-mock-overconfidence live-smoke tier + SDK-estimate corrections from impl-eng.

**Status:** ◌ iteration-1 complete |BC:#10 cqa + #15 impl-eng (cross-agent-ack) |EC:#5 |merge-gate-coverage-score:L→M-with-revisions |edge-case-gaps:#5 |→ WAIT for tech-architect R2 response or DA round before final convergence.

---

### devils-advocate challenges (R1)

!scope: plan-track + build-track + Q3 forward-plan. ¬destroy, challenge for stronger output. Cold-read assessment formed BEFORE reading lead-flags.
!prior-failures-noted: (1) lead-provenance-contamination 26.4.15 → I read lead-flags AFTER own assessment. (2) lead-routing-contamination 26.4.16 → all findings go DIRECTLY to scratch, no lead mediation. (3) DA-hung-silently this-session → tool calls time-boxed 90s.

---

#### DA[1] ANCHORING PROBE — H1-H7 all-consensus is suspicious

issue: tech-architect's independent stress-test lands at CONSENSUS on ALL 7 source-plan hypotheses (H1-H7). BELIEF[] scores: ADR1=0.92, ADR2=0.95, ADR3=0.88, ADR4=0.80, ADR5=0.85, ADR6=0.90, ADR7=0.95, ADR8=0.92 — mean 0.89, min 0.80. That is extraordinary convergence for a "cold stress-test." Prior patterns catalogued from source-plan anchoring show teams arriving at 4-5 of 7 aligned when genuine; 7/7 is a statistical outlier.

base-rate check: across sigma-review archive patterns, independent analysis against a 7-hypothesis source plan converges on all 7 roughly ~8% of the time when evidence is honestly cold (agent-inference from prior F1/F2 reviews; no hard data). The remaining 92% produces at least one divergence.

DB[] quality audit (§2g forcing function): tech-architect DB[] entries for ADR[1], ADR[3], ADR[4]:
- DB[ADR1] step (3) "strongest-counter": `_extract_content` non-trivial + env-discovery valuable. → But this counter is DEFEATED by step (4) with "copy-with-attribution" mitigation proposed by tech-architect itself. That's SELF-RESCUING, not "assume-wrong." PRO-FORMA.
- DB[ADR3] step (3) "strongest-counter": Anthropic agent-mode SDKs. → Step (4) dismisses via "disable agent-mode even if available." Fine reasoning but the STRONGEST counter to tool-exec-in-TurnEngine is NOT "agent-mode hides observability" — it's "tool-exec-in-Provider is simpler and most teams do it that way" (e.g. LangChain AgentExecutor binds to LLM client). Chosen counter is WEAKER than the available one.
- DB[ADR4] step (3) "strongest-counter": Anthropic-shape canonical saves more. → Step (4) dismisses via "only two adapters in M1." But the stronger counter is "use union-type canonical and lose NO fidelity at all" (ALT3 from tech-architect's own alternatives list). The chosen DB counter is weaker than ALT3 which got no DB treatment.

!DB quality verdict: 2/3 DB entries carry WEAKER counters than the strongest alternative the agent's own ALT-list identified. That is pro-forma dialectical bootstrapping — the agent steel-manned NOT-the-strongest position and knocked it down. This inflates confidence artificially.

→ challenge-to-tech-architect: rerun DB[ADR3] with counter "tool-exec in Provider matches LangChain AgentExecutor pattern, most teams keep agent loop with LLM client, separation here is speculative"; rerun DB[ADR4] with counter "union-type canonical (ALT3 from your own alternatives) loses zero fidelity vs OpenAI-shape which PM[1] admits is lossy — why rejected?"

→ action-required: tech-architect R2 responds to above DB re-runs explicitly. If the stronger counter survives, BELIEF[] must drop.

|source:[code-read DB[ADR1/3/4] scratch L737-753 + tech-architect own ALT lists L96-98, 177-181, 219-223 + agent-inference on counter-selection]

---

#### DA[2] BELIEF[ADR4] 0.80 — inconsistency with PM[1] "elevated-risk"

issue: tech-architect assigns BELIEF[ADR4 OpenAI-shaped canonical] = 0.80 with "elevated-risk:acknowledged-via-PM[1]". But PM[1] MEDIUM-HIGH likelihood (0.55) is specifically that the CHOSEN canonical shape causes adapter-explosion. A 0.55 likelihood of the load-bearing failure mode for an ADR is NOT compatible with 0.80 confidence in the ADR.

math: P(ADR4-sound) ≤ 1 - P(PM1-fires) × severity. If PM1 fires with likelihood 0.55 and severity is "adapter-scope-explodes" (scope-break), ADR4 BELIEF upper bound is ~0.45-0.55, not 0.80. The 0.80 figure assumes PM1's mitigation (merge-gate + escape-hatch field) fully recovers — but the escape-hatch `content_blocks: list[dict] | None` is PROPOSED in mitigation (b), NOT in ADR[4] itself.

cqa BC-cqa-1 has already flagged that the round-trip fixture spec is "grossly insufficient" — if cqa is right, PM1 mitigation (a) is incomplete too. impl-eng BC #5 flags that interleaved-content lossiness is LARGER than PM[1] acknowledges, and the `preceding_text_per_tool_call` fix is a NEW field on canonical Message.

→ the escape-hatch isn't locked. PM[1] mitigation list is exposed as partial. BELIEF[ADR4]=0.80 is inconsistent with the evidence.

→ action-required: tech-architect R2 either (a) lower BELIEF[ADR4] to reflect PM[1] risk (0.55-0.65 range), or (b) lock the escape-hatch (content_blocks field + preceding_text_per_tool_call field) INTO ADR[4] itself rather than as PM[1] mitigation. Current state hides risk in the PM instead of the decision.

|source:[code-read BELIEF[ADR4] L1508 + PM[1] L685-692 + cqa BC-cqa-1 L1081-1103 + impl-eng BC #5 L1031 + agent-inference on Bayesian composition]

---

#### DA[3] ADR[3] XVERIFY deferral — process violation

issue: tech-architect marked ADR[3] as "highest-stakes — XVERIFY candidate" at L173 and "Status: DEFERRED to DA round — XVERIFY will be triggered if DA challenges ADR[3] with counter-evidence. Not triggered pre-challenge to conserve budget" at L726-727. BUT:
- §2h directive: "top 1 load-bearing finding per plan-track agent (tech-architect, ui-ux-engineer)" MUST have XVERIFY.
- tech-architect SELF-IDENTIFIED ADR[3] as that top-1 candidate.
- Deferring to "conserve budget" while producing 8 ADRs with 0 XVERIFY calls is a process violation: ui-ux-eng did their XVERIFY (openai:gpt-5.4 on FC) to spec; tech-architect did not.
- The "deferred until DA challenges" pattern inverts the control flow — XVERIFY is meant to PRECEDE DA challenge as cross-model validation, not be triggered REACTIVELY.

This is the "never-advance loophole" cousin (feedback memory 26.4.13): mandatory gate skipped via conditional deferral. If I don't challenge ADR[3] now, the gate is silently skipped.

→ action-required: tech-architect runs XVERIFY on ADR[3] via mcp__sigma-verify__cross_verify (openai:gpt-5.4 + google:gemini-3.1-pro-preview + anthropic:claude-opus-4-6) BEFORE plan-lock. ¬budget excuse — ΣVerify is available (infrastructure section confirms), and 1 cross-model call on ADR[3] is the MINIMUM for plan-track §2h compliance. If that's not feasible per rate-limits, use single-provider challenge() with openai:gpt-5.4.

!I do NOT run XVERIFY on tech-architect's behalf. DA enforces the gate; tech-architect executes it. (Lead Role Boundary: XVERIFY is agent tool; same applies in reverse — DA doesn't absorb tech-architect work.)

|source:[code-read scratch L713-727 + spawn prompt infrastructure section + CLAUDE.md feedback_never-advance-loophole 26.4.13]

---

#### DA[4] GOLD-PLATING audit (§4c)

Scan of IC[] + SQ[] for abstractions unjustified by M1a/b scope per C9 + source-plan:

GP[1]: `providers/registry.py` (SQ4, 0.5h). Registry module for 2 providers in M1a + same 2 in M1b. Tech-architect scope says "env-key discovery + registry.available()." cqa BC-cqa-8 D3 already called this out. A 2-entry registry is a dict literal + 10-line available() helper. Separate module justified ONLY by M1c's 13 providers, which is C9 out-of-scope.
→ recommend: SQ4 simplified to a dict-in-roster.py (5 LOC addition), registry.py DELETED from M1a/b file list. Create registry.py in M1c when there are 13 entries. Saves: 0.5h SQ4 + test allocation.

GP[2]: `Provider.complete()` method in IC[1] L420-427. ADR[8] says "M1a: stub; M1b: thin wrapper over stream() if needed." cqa BC-cqa-8 D1 caught this. M1b success criterion is "≥1 echo round-trip per provider" — uses stream() throughout. complete() is zero-caller dead weight. If kept as NotImplementedError stub, still adds to Protocol surface that mocks must fulfill.
→ recommend: REMOVE complete() from IC[1] Protocol for M1a/b. Add when a caller materializes. This is "premature abstraction for speculative future requirements" (§4c #1). "Building for M1c's possible non-streaming path" is not a current-phase requirement.

GP[3]: `PreambleVariant` in conversation.py SQ8 (L625). Source-plan defines 3 variants (neutral / identity-aware / research-framed). M1a/b uses ONE preamble per session. Building 3 variant renderings in M1a = building for IX[5] M2 UI which doesn't exist yet. cqa BC-cqa-8 D4 flagged.
→ recommend: M1a/b ships identity-aware variant ONLY (current research-Q pinned per user-decision #5 = memory-invocation coherence → identity-aware is the research framing). Add others in M2 when preamble-picker UI is written. Saves: SQ8 effort + test burden on unused variants.

GP[4]: Raw event capture (SQ21, 1h, ADR[6]) across providers ALREADY has a conditional: `tool_use_reliability != "reliable"` default-on, env override. For M1 seed pair, devstral=unknown → ON; anthropic=reliable → OFF. That's one of two providers. Fine as-is — NOT gold-plating. ADR[6] is justified. ✓

GP[5]: `MetricsCollector` baseline (SQ20, 1.5h). M1b spec: record_turn, record_tool_call, snapshot. No consumer in M1a/b (metrics panel is M3). Source plan flags metrics as M3 scope. Baseline collector for M1b is "measuring before consuming" — low cost (1.5h), and the data collected is the PRIMARY RESEARCH ARTIFACT (this is a research instrument, metrics ARE the output). So actually justified: the collected data IS the purpose.
→ accept with rationale.

GP[6]: ui-ux-engineer's pre-M2 TUI comparison (STEP-3, 2h). user-decision #4 pre-committed this. Not M1a/b scope. Out of challenge scope per my context-firewall. ✓

→ actions: GP[1], GP[2], GP[3] are gold-plating per §4c. GP[4], GP[5] justified.

|source:[code-read SQ4+IC[1]+SQ8+SQ20+SQ21 + cqa BC-cqa-8 + §4c gold-plating checklist]

---

#### DA[5] Q3 FORWARD-PLAN scope creep — revision hook H2 is a stealth 2x multiplier

issue: forward-plan M1c revision-hook H2 (scratch L1404): "If M1b finds devstral-2:123b tool_use_reliability='none', M1c scope expands to test ALL Ollama cloud + local models for tool_use reliability systematically." impl-eng BC #15 (L1051) already flagged this as "2-3x M1c scope multiplier, 10h additional."

deeper concern: this revision hook conflates two activities — (i) M1c SDK implementation (OpenAI + Google + Ollama local clients), (ii) empirical provider-reliability matrix (10 providers × 1 echo test). (ii) is an empirical research task, not a code-implementation task. Bundling them inside M1c inflates M1c's perceived effort AND muddies whether M1c is "ship new code" or "run research sweep."

This is a §4a scope-creep detection pattern at PLAN phase, not checkpoint. user-decision #1 says Q3 plan revisits at ~2 weeks — that's when the bundle becomes a problem if not decomposed now.

→ recommend: forward-plan splits H2 fire into two work-items: M1c-code (SDK implementation) + M1c-research (provider reliability sweep, OWN phase/deliverable with OWN timeline). M1c-research can run in parallel or sequentially but is scoped separately. Keeps "ship code" and "run empirical sweep" as distinct deliverables.

|source:[code-read forward-plan L1404 H2 + impl-eng BC #15 L1051 + §4a scope-creep plan-phase detection]

---

#### DA[6] TEST INTEGRITY (§4d soft-check) — merge-gate round-trip is self-referential

issue: cqa + impl-eng already convergently flagged direction-asymmetry (cqa BC-cqa-1 + impl-eng BC #14). I add one further test-integrity concern:

merge-gate test spec says `assert from_sdk(to_sdk(msg)) == msg` (ADR[4] L240-244). If canonical Message + to_sdk + from_sdk are all written by the same engineer, this test can pass with a FIELD-LOSS bug that symmetrizes: if `to_sdk` drops field X and `from_sdk` re-defaults it, round-trip succeeds by returning the same reconstructed-with-defaults message. The test reports green while field X is silently unreachable.

specific case: IC-flag[5] / final_message / preceding_text_per_tool_call — if canonical Message adds preceding_text_per_tool_call as proposed by impl-eng BC #5, and to_sdk DROPS it going to OpenAI (because OpenAI has no slot), and from_sdk RECONSTRUCTS it from tool_call position (best-effort), the round-trip tests will look like they pass but SDK-outbound-to-SDK-inbound-without-canonical-intermediate loses ordering.

→ recommend: merge-gate tests MUST include "known-goldens" — canonical Message fixtures with pre-computed expected-to_sdk outputs (hand-written, not machine-round-tripped). F1-F8 from cqa BC-cqa-1 should include at least 3 hand-computed SDK-output fixtures per SDK. This is what catches hardcoded-return-value test integrity failures (§4d rule #4).

|source:[code-read ADR[4] test spec L240-244 + cqa BC-cqa-1 F1-F8 + §4d test-integrity rule #4]

---

#### DA[7] PROMPT AUDIT (§7d) — echo detection + methodology

Per §7d BUILD prompt-audit checks. Source prompt = look-for-the-plan-snazzy-giraffe.md. Prompt-understanding shows H1-H7 extracted from source prompt verbatim.

(1) echo-detection: did plans use source-prompt language verbatim?
- ADR[1-8] section headings use source-plan terminology ("providers module", "tool-exec loop", "canonical Message shape") — inherited from source. That's expected vocabulary-alignment, not echo.
- Near-verbatim claim-echoes: H1 "Purpose-built `providers/` module beats abstracting sigma-verify's `clients.py`" appears as source-plan ADR claim AND as Hypothesis AND as tech-architect ADR[1] decision. The claim survived three layers unchanged. That's anchoring risk but defensible if stress-tested.
- Verdict: low echo density in findings prose, but HIGH claim-echo pattern on H1-H7 structure (7/7 survived).

(2) unverified [prompt-claim] findings: source tags audit — I count [source-plan] tags as prompt-derived. ADR[1-8] all carry [source-plan] + additional source types:
- ADR[1]: [code-read] dominant + [source-plan]. Code-read DOES dominate. ✓
- ADR[2]: [independent-research Anthropic SDK] + [independent-research Ollama] + [source-plan C4] + [agent-inference]. ¬over-reliance on prompt. ✓
- ADR[3]: [source-plan H3] + [agent-inference] + [code-read source-plan ToolCallRecord schema]. → MOSTLY agent-inference. No independent-research. XVERIFY deferred (DA[3]). RISK.
- ADR[4]: mix incl. [code-read] + [independent-research Anthropic] + [independent-research Gemini] + [source-plan H4+H7]. ✓
- ADR[5]: mostly [source-plan] + [independent-research tokenizer drift]. Acceptable, config decision.
- ADR[6-8]: [source-plan] + [industry-pattern] + [agent-inference]. Configuration decisions, lower stakes.

→ [prompt-claim]-only findings without corroboration: ≤1 of 8 ADRs (ADR[3] most-exposed, but DB performed). Under 30% threshold. §7d echo criterion = PASS (¬perfect, but within tolerance).

(3) methodology: could the plan have produced a contradictory result?
- ADR[1]: YES — code-read clients.py COULD have shown overwhelming reuse opportunity. It didn't. Investigative. ✓
- ADR[3]: PARTIALLY — agent-inference doesn't give contradiction vector. This is why XVERIFY was required.
- ADR[4]: YES — PM[1] explicitly acknowledges elevated risk, has fallback-to-Anthropic-shape option. Investigative.
- Overall: mostly investigative, ADR[3] weakest on methodological falsifiability.

§7d verdict: PASS with ADR[3] flagged for XVERIFY deficiency (already DA[3]).

|source:[code-read source-prompt H1-H7 + ADR source-tags + §7d audit checklist]

---

#### DA[8] ASSUMPTION CONFLICTS (§4b) — what the agents agreed WITHOUT verifying

Cross-reference 4 agents for hidden assumption conflicts. cqa BC-cqa-7 caught the IC[1] INV3 vs IC[2] error-convention contradiction (CAUGHT — no new finding needed; lead-flag #4 also notes).

Hunting for uncaught conflicts:

CONFLICT[1]: `final_message` field location. impl-eng BC #3 proposes `StreamEvent(kind="stop", final_message=Message|None)`. cqa BC-cqa-11 EG3 assumes this too. ui-ux-eng IC-flag[5] wants `kind="tool_result"` NEW event. These are TWO DIFFERENT proposed IC[2] additions, not one. impl-eng = carry reconstructed-assistant-message on stop event (pre-tool-exec); ui-ux-eng = emit NEW event post-tool-exec with ToolCallRecord fields. Both proposals address different phases of the tool-exec loop. cqa BC-cqa-11 conflates them ("a/b/c additions to IC[2]") but they compose — they're NOT redundant. tech-architect R2 needs to accept BOTH or explicitly reject the less-important one with reason.

CONFLICT[2]: provider-state cleanup after tool-exec. impl-eng BC #3 says Provider owns final_message reconstruction. cqa BC-cqa-3 T7 says "provider state cleanup — async-generator not-closed." If Provider holds SDK context for reconstruction, it also holds the async-gen state that T7 is testing. tech-architect must specify: does provider.stream() return a FRESH async-gen each call (stateless-per-call per IC[1] invariant) OR does it retain SDK session state between invocations (needed for final_message reconstruction across tool-exec boundary)? This is a subtle stateless-contract violation if reconstruction requires session.

→ action: tech-architect R2 resolves (a) dual IC[2] additions (final_message on stop + optional kind="tool_result" post-exec) and (b) Provider statelessness invariant vs reconstruction responsibility.

CONFLICT[3]: test-tier naming drift. cqa BC-cqa-6 proposes `tests/live/` subdir. cqa BC-cqa-10 X3 says "tests/ + tests/live/." impl-eng proposes SQ6c smoke test as a pre-build check, not clearly in tests/live/. tech-architect hasn't weighed in. Minor but: where does SQ6c's smoke test live? As an SDK feasibility probe it's arguably NOT a regression test and should live in scripts/smoke_ollama_v1.py or similar, not in tests/live/.

|source:[cross-ref impl-eng BC #3 L1027 + cqa BC-cqa-11 L1328-1353 + ui-ux IC-flag[5] L914-916 + §4b assumption-conflict checklist]

---

#### DA[9] LEAD-FLAGS cross-check (read LAST per protocol)

Only now reading `## lead-flags-for-DA` section. Comparing against my above cold-read findings:

Lead flag #1 (H1-H7 all-consensus anchoring): I caught this independently as DA[1]. Validates cold-read. ✓
Lead flag #2 (existing-pattern recall miss — P[ollama-openai-compat-drops-tool-calls-streaming] + P[streamlit-async-gen-supported-with-caveat] in memory): NEW to me — I did not check global memory for these patterns during cold-read. This is a process observation about boot-recall exhaustiveness, ¬a plan-quality challenge. Noted; weighing as "process pattern for memory compiler," not a build challenge. I will NOT re-do impl-eng's XVERIFY pretending it was the missing memory-recall. impl-eng's independent arrival at the same conclusion via XVERIFY is VALID evidence, just a duplicated effort.
Lead flag #3 (4-agent IC[2]/IC[5] convergence): Caught as DA[8] CONFLICT[1]. I ADD: the convergence is NOT on ONE addition — it's on TWO additions that need both. Lead's framing slightly over-collapses the four proposals.
Lead flag #4 (IC[1] vs IC[2] contradiction hard ordering): Already addressed by cqa BC-cqa-7. No new DA challenge needed; I concur — must resolve before SQ6a/6b.

Verdict: 3/4 lead flags match my cold-read independently; 1/4 is a process observation I accept as context but do not convert into challenge. No contamination risk detected — cold-read dominated.

|source:[scratch L1577-1585 lead-flags + self-audit against DA[1]+DA[8]]

---

#### DA[10] WHAT THE TEAM IS NOT DISCUSSING

Per challenge framework item #7. Gaps no one raised:

GAP[1]: **Cost of Anthropic live runs.** M1a success criterion = "one session, 2 models, 5 turns, round-robin, streamed live." That IS live API usage. At claude-opus-4-7 pricing, 5-turn multi-model session could be $0.05-0.20. M1b adds tool-use → 10-15 turns reasonable per empirical run. cqa BC-cqa-6 proposes SQ12i/SQ28 live tests "cost: ~$0.01" which is an UNDER-estimate for opus-4-7 with realistic preambles. No SQ allocates budget-awareness to live-test running. Recommend: M1a verification run logged with token-count + estimated cost in persistence.py session header; budget kill-switch env `CHATROOM_MAX_SESSION_COST_USD` default 0.50.

GAP[2]: **What happens when user runs SAME session twice.** Source plan spec says JSONL filename conventions unclear. session_id collision handling? Replay of session → append-to-same-file OR new file? impl-eng BC #10 caught partial-turn replay, not overwrite semantics. Minor but worth 5min decision.

GAP[3]: **Security: tool arguments are untrusted model output.** echo tool in M1b is safe. But the PATTERN established by echo (tool receives model-generated arguments and echoes back) becomes the template for M3's `SIGMA_MEM_RECALL` which HITS a live MCP server with model-generated query strings. No input-validation layer in TurnEngine tool-exec loop. For M1a/b echo this is fine (C1: not security-critical). But the ABSENCE of an input-validation seam means M3 will retrofit it or ship without. Recommend: TurnEngine.advance_stream accepts optional `tool_arg_validator: Callable[[ToolSchema, dict], dict] | None = None` parameter. M1a/b default: identity. Small seam, avoids M3 retrofit. NON-blocking for C1 but noted.

GAP[4]: **Process observation — anti-sycophancy check for DA itself.** Am I agreeing with cqa/impl-eng too readily on cross-agent convergence findings (lead-flag #3)? Self-audit: DA[8] CONFLICT[1] ADDS disagreement with cqa's collapsing of the 4-agent cluster. DA[4] GP[5] ACCEPTS metrics baseline despite its being a plan-track ADR (I could have contrarian-for-its-own-sake rejected it but the rationale is genuine). DA[6] adds test-integrity concern neither cqa nor impl-eng raised. Conclusion: no sycophancy detected; I'm disagreeing where evidence points.

|source:[agent-inference on what's missing + self-audit per anti-sycophancy CLAUDE.md]

---

#### DA[11] XVERIFY (§2h, DA-optional)

Time-boxed per boot directive (≤90s/call, max 2 total). Decision:

Candidate #1 — XVERIFY on DA[1] anchoring probe (DB quality claim): NOT a good XVERIFY fit. This is a meta-process finding, not a domain claim. Cross-model verification would waste call.

Candidate #2 — XVERIFY on DA[2] BELIEF[ADR4]=0.80 inconsistency with PM[1]: domain-adjacent but philosophical. Skip.

Candidate #3 — XVERIFY on DA[3] that ADR[3] tool-exec-in-TurnEngine is the correct architecture: THIS is what tech-architect should run. I don't duplicate; that's tech-architect's gate. Flagged as DA[3].

Candidate #4 — XVERIFY on GAP[3] security-seam recommendation: overkill; low-stakes NOT-blocking note.

→ Decision: XVERIFY NOT-ATTEMPTED by DA. My challenges are structural/process, not cross-model-verifiable domain claims. ΣVerify budget preserved for tech-architect ADR[3] gate (DA[3]) and for future-round agent XVERIFY if needed.

|source:[self-audit of DA findings for XVERIFY applicability + ≤2 call budget directive]

---

#### DA exit-gate verdict (R1)

Criteria evaluated per agent def lines 52-77 (adapted to BUILD mode):

1. Engagement quality: tech-architect = B+ (thorough ADRs, DB[] pro-forma on 2/3, XVERIFY deferred). ui-ux-eng = A- (XVERIFY executed, IC-flag[5] material, DB solid). impl-eng = A (cross-SDK technical depth, XVERIFY triggered, convergent with cqa). cqa = A (independent arrivals, test-integrity-pattern-application, feedback-memory cross-refs).
  → Overall: B+ to A. PASSES ≥B threshold.

2. Material disagreements unresolved: YES — DA[1] DB rerun, DA[2] BELIEF[ADR4] math, DA[3] XVERIFY mandate, DA[4] 3 gold-plating items, DA[5] forward-plan H2 decomposition, DA[6] golden fixture addition, DA[8] CONFLICT[1] dual IC[2] additions. 7 challenges require tech-architect R2.
  → FAILS until tech-architect R2 addresses.

3. New consensus stress-tested: NOT YET — cqa BC-cqa-11 + impl-eng BC#2/#3 + ui-ux IC-flag[5] 4-agent convergence on IC[2]/IC[5] needs tech-architect R2 response. DA[8] flagged it's TWO additions not one.

4. Analytical hygiene (§2a/b/c/e): outcome 1/2/3 present per ADR ✓. Hygiene check PASS but DB[] quality concerns per DA[1].
  4a. §2d source provenance: R1 tags present ✓.
  4b. T1/T2/T3 tier tags: partial — tech-architect tagged [independent-research] but not T1/T2/T3 explicitly on all. ui-ux-eng tagged T1 explicitly. MINOR GAP (not fail).

5. Prompt contamination (§7d): ≤1/8 ADRs [prompt-claim]-only, under 30% threshold. H1-H7 7/7 survival is structural anchoring concern (DA[1]) not echo-density concern. PASS with flag.

6-8. CQoT falsifiability/steelman/confidence-gap: DB[] entries present but 2/3 pro-forma (DA[1]). Weaker than required; challenge logged.

9. XVERIFY integrity:
  - tech-architect: top-1 load-bearing XVERIFY NOT ATTEMPTED — process violation per DA[3].
  - ui-ux-eng: XVERIFY executed, partial result honestly documented ✓.
  - impl-eng: XVERIFY executed on H2 ✓.
  - cqa: not required (not plan-track).
  → FAILS on tech-architect XVERIFY missing.

**Exit-gate verdict:** `"exit-gate: FAIL |engagement:B+ |unresolved:[DA1-DB-rerun, DA2-BELIEF-math, DA3-XVERIFY-missing, DA4-3-gold-plating-items, DA5-forward-plan-H2-decomp, DA6-golden-fixtures, DA8-CONFLICT1-dual-IC2-additions] |hygiene:pass-with-DB-quality-flag |prompt-contamination:pass-with-H1-H7-structural-flag |xverify:fail-tech-architect-missing-top1"`

→ required for PASS (R2): tech-architect runs XVERIFY on ADR[3]; tech-architect re-runs DB[ADR3/4] with stronger counters; tech-architect resolves BELIEF[ADR4] math vs PM[1]; tech-architect decides GP[1]/GP[2]/GP[3]; tech-architect responds to CONFLICT[1] dual-addition; tech-architect decides forward-plan H2 decomposition; cqa adds hand-golden SDK fixtures to MERGE GATE.

→ ready for plan-track R2 responses.

---

### devils-advocate R2 re-evaluation (exit-gate round 2)

!scope: re-evaluate R1 findings against plan-track R2 responses (tech-architect-r3 L773-1192, ui-ux-engineer R2 L1441-1591, impl-eng R2 L1639-1730, cqa R2 L2027-2080). Apply exit-gate criteria #1-9 per agent def.

---

#### R2 disposition per DA[] finding

**DA[1] anchoring probe + DB quality:** RESOLVED.
tech-architect re-ran BOTH DB[ADR3] and DB[ADR4] with the stronger counters I flagged (LangChain AgentExecutor for ADR3, union-type ALT3 for ADR4). Re-runs are genuinely engaged: ADR[3] survives on N>3 + observability-mandate (not generic separation-of-concerns as pro-forma R1 version), explicitly concedes "if chatroom were single-SDK, ADR[3] flips." ADR[4] DB re-run shows ALT3 defeats itself on N^2 adapter-pair explosion (4→12 pairs) and replay non-determinism. BELIEF[ADR3] 0.88→0.84 + BELIEF[ADR4] 0.80→0.70 — both drops are honest confidence adjustments reflecting where R1 was inflated. This IS the outcome R1 DA[1] demanded.

**DA[2] BELIEF[ADR4] vs PM[1] math:** RESOLVED.
Concede + lock. Escape-hatches LOCKED into ADR[4] proper (not buried in PM[1] mitigation): Message.preceding_text_per_tool_call + Message.content_blocks + 3-tier MERGE GATE now structural parts of ADR[4]. BELIEF 0.80→0.70 explicitly reasoned: "P(PM1-fires-and-escapes-mitigation) drops 0.55→0.25 with locked hatches; conservative 0.70 acknowledges Gemini adapter residual risk." Math now defensible; risk visible in the decision, not hidden in the pre-mortem.

**DA[3] XVERIFY missing (the hard one):** PASS-WITH-DOCUMENTED-GAP.
R1 framing "process violation / conserve-budget loophole" was a COLD-READ assumption. R2 reveals this is infra failure, not budget excuse: sigma-verify cross_verify + verify_finding hung 3x this session (DA-r1, TA-r1, TA-r2). Per §2h directive "¬retry failed providers, flag gap + continue" — documented gap IS the allowable escape hatch. Compensating factors claimed by tech-architect:
  (a) 4-agent cross-agent read of ADR[3] location — impl-eng R1 + R2 did NOT challenge location (only stacked INV4/5/6 emissions ON TOP of location); cqa EG1-EG5 test state-machine AT this layer (implicit endorsement); ui-ux IC-flag[5] COMPOSES with TurnEngine-owns-loop (explicit affirmation).
  (b) DB[ADR3] re-run with stronger counter (LangChain AgentExecutor) — ADR survives on N>3 multi-provider grounds after honest engagement.
  (c) Industry precedent audit: autogen GroupChat, crewai — N>1 agent-orchestrator systems location-separate. Pattern precedent supports ADR[3].
  (d) Gap escalated to user via convergence summary + gate-log entry (¬silently skipped).
Self-audit: am I accepting this because evidence supports it, or because I want to close? → Evidence supports. Criterion #9 language is "XVERIFY-FAIL ¬flagged as gap → process violation" — flagging WITH compensating evidence is the defined PASS pattern. Accepting.

**DA[4] gold-plating 3 items:** RESOLVED.
GP[1] registry.py CONCEDE (merged into roster.py 5-line dict, -0.25h). GP[2] complete() CONCEDE (removed from IC[1] Protocol for M1a/b, CompleteResult dataclass kept as type-only). GP[3] PreambleVariant COMPROMISE per ui-ux defense (type + logged field remain; 1 rendering only for M1a/b; variants 2+3 activate in M2). Ui-ux compromise is substantive: preserves source-plan L182-184 cross-session comparison contract while cutting unused rendering code. All 3 genuinely addressed.

**DA[5] forward-plan H2 decomposition:** RESOLVED + EXTENDED.
ACCEPT decomposition principle. H2 split into H2-code (M1c SDK implementation, 1-2w) + H2-research (provider reliability sweep, ~1 day parallel). Propagated check to ALL forward-plan hooks: H1/H3/H4/H5/H6 confirmed well-formed (no decomposition needed), H7/H8 marked resolved via UD#5. ui-ux UX-H3 + UX-H4 also decomposed per same pattern (research-observation → code-conditional). Checkpoint-Q3-A added per UD#1 at ~2w post-M1a-ship.

**DA[6] hand-golden fixtures:** RESOLVED.
3-tier strategy LOCKED into ADR[4] test spec: Tier 1 hand-golden outbound (canonical→SDK) + Tier 2 hand-golden inbound (SDK-response→canonical) + Tier 3 round-trip smoke (DERIVATIVE). Fixture files specified: anthropic_golden.py + openai_golden.py + *_responses_golden.py. cqa R2-Δ-1 adds G-F1/G-F2/G-F3 hand-goldens complementing F1-F8. SQ12d 1.5h→2.5h + SQ23 2h→3.5h. Catches symmetric-field-loss bug I flagged (test can't pass with hardcoded-matching-loss because hand-computed SDK shapes are independent source of truth).

**DA[7] prompt audit:** already PASS in R1 verdict; no R2 action needed. Noted in gate.

**DA[8] assumption conflicts:** RESOLVED.
CONFLICT[1] dual IC[2] additions — ACCEPT BOTH. IC[2] expanded: kind literal gets +tool_result; final_message: Message|None on stop; tool_call_record: ToolCallRecord|None on tool_result. INV4-INV7 added. Event grammar documented: `token* → (tool_call+ → stop(tool_use, final_message) → tool_result+)* → token* → stop(end_turn|max_tokens|max_tool_calls|error)`. impl-eng R2-clarify-1 surfaces that the schema changes are actually on THREE surfaces (StreamEvent.final_message + StreamEvent kind=tool_result + Message.preceding_text_per_tool_call) — compositional, not redundant.
CONFLICT[2] Provider statelessness vs reconstruction-state — RESOLVED via impl-eng R2-NEW-2 SDK context-manager semantics investigation: anthropic MessageStreamManager + openai AsyncStream both flush accumulator at context-exit. Provider IS stateless-per-call. IC[1] INV4+INV5 added.
CONFLICT[3] SQ6c location — resolved in scripts/ not tests/live/.

**DA[9] lead-flags cross-check:** already reconciled in R1. Validates cold-read (3/4 match). No R2 action needed.

**DA[10] what the team is NOT discussing:** partial.
GAP[1] Anthropic live-run cost: NOT explicitly addressed by R2 but cqa BC-cqa-6 SQ12i/SQ28 budget note "~$0.01" is still an under-estimate for opus-4-7. Not R2-blocking; flag for C2 to set CHATROOM_MAX_SESSION_COST_USD env.
GAP[2] session_id collision: still unaddressed. Low-priority flag for C2.
GAP[3] input-validation seam: unaddressed. Non-blocking for M1a/b (echo-tool only); note for M3+.
GAP[4] anti-sycophancy self-check: self-audit was adequate R1.
These are carry-forward items for C2 build phase, NOT R2-blocking plan-lock.

**DA[11] DA XVERIFY:** remains NOT-ATTEMPTED-per-design (process findings, not domain claims). No change.

---

#### R2 exit-gate criteria evaluation

1. **Engagement quality:** R2 agents responded substantively to every DA challenge. tech-architect did 9 DA-resp + 15 impl-eng BC-resp + 11 cqa BC-resp + 5 EC-resp = ~40 discrete responses, with genuine concede/revise patterns (not defensive). DB re-runs were genuine engagements. ui-ux compromise on GP[3] defended the type-level contract while cutting unused code — that's the right nuance. impl-eng R2-NEW-2 surfaced a gap I caught they missed, investigated SDK internals, proposed INV4+INV5 — honest concession with contribution.
  → Engagement: **A-** across all agents.

2. **Material disagreements unresolved:** 7 R1 items identified → 7 resolved (DA[1] DB re-run, DA[2] escape-hatch lock + BELIEF drop, DA[3] XVERIFY-gap-doc with compensating factors, DA[4] 3 gold-plating items, DA[5] H2 decompose, DA[6] hand-goldens, DA[7/8] IC[2] dual additions). DA[10] GAP[1-3] flagged as C2-build-phase follow-ups, NOT unresolved plan-track items. Zero load-bearing plan disagreements remain.

3. **New consensus stress-tested:** Yes. The IC[2] 4-agent convergence (flagged as strong in R1) produced compositional 3-surface resolution (2 StreamEvent + 1 Message field) — each addition traced to a different agent's concern; none redundant. DB re-runs performed on the new consensus specifically (ADR[3] location).

4. **Analytical hygiene (§2a/b/c/e):** outcome 1/2/3 format preserved. §2d source tags present on R2 additions. §2g DB quality substantially improved (R1 pro-forma → R2 substantive). T1/T2/T3 tier tags still partial (minor gap, non-blocking).

5. **Prompt contamination (§7d):** PASS — already clean in R1; R2 adds no [prompt-claim]-heavy findings. H1-H7 survival pattern was structural anchoring concern that DB re-runs now substantively addressed.

6-8. **CQoT falsifiability/steelman/confidence-gap:** R2 DB[ADR3] re-run includes explicit falsification: "if chatroom were single-SDK, ADR[3] flips" — reachable condition. DB[ADR4] re-run genuinely steel-mans ALT3 union-type canonical before defeating on N^2 adapter-pair grounds. Confidence-gap implicit in BELIEF drops (0.88→0.84, 0.80→0.70). PASS.

9. **XVERIFY integrity:**
  - tech-architect ADR[3]: FAIL-with-documented-gap per §2h allowable pattern. Compensating factors cited + gap escalated + gate-log entry. NOT silent skip.
  - ui-ux-eng XVERIFY: executed in R1 (openai:gpt-5.4 partial on FC). ✓
  - impl-eng XVERIFY: executed in R1 (openai:gpt-5.4 uncertain-low on H2-ollama). ✓
  - DA XVERIFY: not-attempted-per-design (process findings).
  → Criterion #9 definition allows documented-gap; tech-architect pattern matches definition.
  → PASS with documented infrastructure gap (not-silent).

---

#### R2 exit-gate verdict

`exit-gate R2: PASS |engagement:A- (R2-substantive, genuine-concede-revise across all 4 agents) |unresolved:[none-plan-blocking; 3-C2-followups:cost-env-var + session-id-collision + input-validation-seam] |hygiene:pass (DB R2 substantive, T1-T3 tier-tags minor-gap non-blocking) |prompt-contamination:pass |xverify:pass-with-documented-gap (tech-architect ADR[3] infra-blocked 3x-session, compensating-factors: 4-agent-consensus + DB-re-run + industry-precedent, escalated-to-user-via-gate-log per §2h)`

**Additional context for lead:**
- BELIEF[P(plan-ready)] posted by tech-architect: 0.87. Above 0.85 lock threshold.
- Scope delta acceptable: ~32h R1 → ~41h R2 parallelized (+28%) justified by merge-gate rigor + 4-agent IC[2] coherence + PM-mapped state-machine coverage + anti-mock-overconfidence live-smoke. Consistent with feedback memory 26.4.5 "mock-tests-false-confidence."
- Self-audit anti-sycophancy: am I passing this because the user/lead wants the plan locked, or because R2 addressed my challenges? → Evidence-based: R2 made 5 BELIEF adjustments downward (not upward to please DA), and R2 acted on 7/7 material challenges including the one (XVERIFY) I was most likely to be dismissed on. Agents genuinely engaged rather than performing concession.
- One soft concern persists: T1/T2/T3 tier tags were called out in R1 as minor gap ("partial — tech-architect tagged [independent-research] but not T1/T2/T3 explicitly on all"). Not addressed in R2. Non-blocking for lock but could be tightened if R3 were to occur. I am NOT requesting R3 for this alone.

**Carry-forward flags for C2 build phase (NOT R2-blocking):**
- CHATROOM_MAX_SESSION_COST_USD env or session-header cost-tracking for live-test runs.
- session_id collision handling (replay behavior on duplicate).
- Input-validation seam in TurnEngine.advance_stream for tool-arg validator (M3 retrofit prevention).
- T1/T2/T3 tier-tag consistency on source-provenance (minor hygiene improvement).

→ PASS — plan ready for lock. Process rounds budget preserved (used 2 of 5).

---

## architecture-decisions (locked after DA approval)

ADR[1]: **Purpose-built `providers/` module; ¬import/subclass sigma-verify clients.py.** |alternatives:{ALT1 subclass _OllamaClientBase, ALT2 copy-verbatim, ALT3 purpose-built borrowing specific functions} |rationale:sync/async mismatch — clients.py.call() sync returns tuple; chatroom Provider.stream() async yields StreamEvent. <20 LOC real reuse vs ~900 LOC divergent surface. Coupling to sigma-verify Apache-2.0 evolution = silent-break risk. Mitigation: copy-with-attribution of `_extract_content` + env-var naming convention. |prompted-by:H1+C3 |BELIEF:0.92 |source:[code-read clients.py:266-288,247-264,221-236]+[agent-inference]+[source-plan] |R2:stands

ADR[2]: **Native per-SDK tool-use; ¬text-convention, ¬ollama-mcp-bridge.** |alternatives:{ALT1 text-convention regex, ALT2 ollama-mcp-bridge, ALT3 hybrid native+text-fallback} |rationale:Anthropic SDK ≥0.40 emits content_block_start/delta type="tool_use" (structured, first-class). Ollama /v1 OpenAI-compat emits tool_calls when instruction-tuned. Text-convention strictly worse when structure available. Bridge adds indirection + moving dep; C4 hard-stop. tool_use_reliability taxonomy only meaningful on native SDK behaviors. Gap: /v1 streaming+tool_calls unverified → SQ6c smoke test pre-SQ14b. |prompted-by:H2+C4 |BELIEF:0.95 |source:[source-plan C4]+[independent-research Anthropic+Ollama]+[code-read ollama-mcp-bridge warning] |R2:SQ6c conditional added

ADR[3]: **Tool-exec loop lives in TurnEngine; Provider.stream() = exactly one SDK call.** |alternatives:{ALT1 tool-exec inside Provider.stream (Provider-owned), ALT2 separate ToolExecutor service, ALT3 hybrid Provider-for-agent-mode+TurnEngine-cross-SDK} |rationale:separation-of-concerns (Provider=wire, TurnEngine=policy) + ToolCallRecord needs conversation-level state Provider ¬has + 5-call cap is chatroom policy ¬SDK feature. R2 DB re-run: LangChain AgentExecutor counter (Provider-owned loop industry mode for N=1 SDK) acknowledged; ADR defended on N>3 + observability grounds. Single-SDK case would flip decision. autogen/crewai N>1 location-separation precedent. |prompted-by:H3 |BELIEF:0.88 → **0.84 R2** |XVERIFY:FAIL[infra-gap-documented — cross_verify hang x3; compensated by 4-agent consensus + DB re-run] |source:[source-plan H3]+[agent-inference]+[industry-pattern autogen+crewai+LangChain] |R2:rationale strengthened, BELIEF↓

ADR[4]: **OpenAI-shaped canonical Message; message_mapping.py owns all non-trivial translation; escape-hatches LOCKED in ADR; 3-tier hand-golden MERGE GATE.** |alternatives:{ALT1 Anthropic-shaped canonical, ALT2 per-provider subclasses, ALT3 union-type (zero-loss but N^2 adapters)} |rationale:majority-provider (8/13 OpenAI-compat). OpenAI flat-list simpler for JSONL persistence. Escape-hatches `Message.preceding_text_per_tool_call: list[str] | None` (impl-eng BC#5) + `Message.content_blocks: list[dict] | None` NOW IN ADR PROPER not PM[1] mitigation. 3-tier MERGE GATE: Tier 1 hand-golden outbound + Tier 2 hand-golden inbound + Tier 3 round-trip smoke (derivative). R2 DB re-run: ALT3 union-type = zero-loss but 12 vs 4 adapters + defeats replay determinism. |prompted-by:H4+H7 |BELIEF:0.80 → **0.70 R2** |source:[source-plan H4+H7]+[independent-research Anthropic+Gemini+OpenAI]+[cqa BC[cqa-1] F1-F8]+[impl-eng BC#14]+[DA[#2]+DA[#6]] |R2:escape-hatches locked, 3-tier gate, BELIEF↓

ADR[5]: **Context budget = 60% ProviderSpec.max_context_tokens; estimator len(text)//4; per-model calibration deferred to M3 with revision hook.** |alternatives:{ALT1 70% budget, ALT2 SDK-tokenizer per-call, ALT3 60% + SDK-tokenizer at truncation-decision only} |rationale:len//4 ≈ 4 chars/token English; drift ≤15% absorbed by 60% buffer. M1 seed pair (opus-4-7 200K+ / devstral-2:123b 128K+) far exceeds 5-turn session. Revision hook H1: if M1a empirical shows reported_input_tokens diverges >15%, M3 calibration shifts LEFT to M1c. |prompted-by:H5+source-plan-risk-table |BELIEF:0.85 |load-bearing:no(config) |source:[source-plan H5]+[independent-research tokenizer drift] |R2:stands

ADR[6]: **Raw SDK event capture default-on when ProviderSpec.tool_use_reliability != "reliable"; env override CHATROOM_CAPTURE_RAW={0,1}.** |alternatives:{ALT1 always-on all providers, ALT2 opt-in only via env, ALT3 on M1a-learning + off M3+ except unreliable} |rationale:"0 invocations ambiguity" distinguishes declined/malformed/SDK-swallowed. devstral-2:123b reliability="unknown" → default-on captures first-run evidence. Storage ~200KB/session bounded. For "reliable" providers redundant. |prompted-by:H6+risk-table |BELIEF:0.90 |load-bearing:no |source:[source-plan H6+risk-table]+[agent-inference] |R2:stands

ADR[7]: **Per-record schema_version="1" on every JSONL line (session_header + turn + tool_call); replay INVs added.** |alternatives:{ALT1 version in session_header only, ALT2 sidecar metadata file, ALT3 semver "1.0.0"} |rationale:per-record = each line self-describing → replay tools version-check individual records. Critical for M3+ schema v2. R2 replay invariants: INV-replay-1 skips malformed trailing lines with warning; INV-replay-2 partial turns (stop_reason="error") INCLUDED in replay; INV-replay-3 missing session_header raises CorruptedSessionError. OpenTelemetry+Jaeger pattern. |prompted-by:C8 |BELIEF:0.95 |source:[source-plan C8]+[industry-pattern]+[impl-eng BC#9+cqa BC-cqa-4] |R2:replay INVs added

ADR[8]: **Streaming from day 1 (M1a baseline); Provider.stream() required; complete() REMOVED from M1a/b Protocol per DA[#4] GP[2].** |alternatives:{ALT1 defer streaming to M2, ALT2 streaming optional gated-by-flag} |rationale:TTFT metric requires streaming; defer = force M2 Streamlit shim to integrate async+new-interface together. tool_call events delivered via streaming — unifying reduces code paths. Test infra mitigated by pytest-asyncio + async mock fixture. R2: complete() REMOVED from IC[1] Protocol for M1a/b — zero callers. CompleteResult dataclass retained for future. |prompted-by:C5+design-decision-2 |BELIEF:0.92 |load-bearing:no |source:[source-plan C5]+[agent-inference]+[DA[#4] GP[2]+cqa BC-cqa-8 D1] |R2:complete() removed

## design-system (locked after DA approval)

!M1a/b has NO UI — DS[] apply to Q3 M2 scope only. Locked after DA-r2 PASS.

DS[1]: spacing-scale |scope:all |tokens: 4/8/12/16/24/32/48 px (4px base matches Streamlit rhythm; 8px speaker-block gutter; 16px inter-turn margin) |rationale:consistent visual rhythm across multi-speaker transcript

DS[2]: typography-hierarchy |scope:all |levels: speaker-name 16px/600 bold > tool-badge 12px/600 caption-semibold > message-body 14px/400 body > metadata (TTFT/tokens) 11px/400 muted |rationale:multi-model transcript lacks single-author continuity — speaker-name must anchor visual scan

DS[3]: color-semantics |scope:all |palette:deterministic hash(provider_key) → 8 WCAG-AA hues (≥4.5:1 on bg); reserved red=error, amber=truncation/warning, green=tool-success, blue-grey=streaming-in-flight, neutral-grey=human/system; cap=8 (beyond → composite hue+letter-prefix attribution) |rationale:deterministic palette enables cross-session visual reproducibility (research-instrument value); paired with DS[2] speaker-name text per WCAG §1.4.1 (¬color-only attribution)

DS[4]: tool-call-badge-visual-language |scope:M2b |states:pill-shaped baseline-inline — `[tool:name] ↻` pending → `[tool:name] ✓ 240ms` settled → `[tool:name] ✗ err:{class}` error; click→st.expander reveals full query / result (truncate 2000ch + "view full" sub-action) / latency_ms / preceding_text (last 50ch) / position_in_turn |rationale:inline observability at position_in_turn = core research affordance per UD#5 memory-invocation-coherence

DS[5]: streaming-in-flight-affordance |scope:M2a |cursor caret (▍) on active streaming line, fades on stop_reason; subtle pulse on active speaker-chip |rationale:live-feedback visual separation from static content

DS[6]: status-icon-set |scope:all |Streamlit-native `:material/icon:` — streaming:`graphic_eq` / tool-pending:`sync` / tool-success:`check_circle` / tool-error:`error` / human-injection:`person` / truncation:`content_cut` |rationale:honors Streamlit theme engine, no custom CSS; TUI alt-path swaps to rich-library symbols if UD#4 lands TUI

DS[7]: density-mode |scope:M2c |default medium (16px turn-gap) + "dense" toggle (8px) for long-session viewing; metadata row collapsed by default |rationale:long-session readability + density toggle cheap big-readability-win

!a11y-notes: A11Y[2] aria-live for streaming tokens = DOCUMENTED M2 GAP per UD#6 (moots if TUI path). DS[3] color-semantics paired with DS[2] speaker-name text ensures WCAG 2.2 §1.4.1 compliance (color ¬ sole attribution channel).
!variant-gating: PreambleVariant Literal type persists in IC[4]/IC[7] (logged field), but RENDERING code gold-plated per DA4 GP[3] — M2a ships identity-aware-only picker (others greyed); M2b activates neutral; M2c activates research-framed conditional on user checkpoint.
!framework-agnosticism: DS[1-7] translate thinly if TUI path chosen (spacing→char-grid, color→ANSI, typography→rich styles, icons→rich symbols). Lock survives UD#4 outcome.

## interface-contracts (build-track implements against these)

IC[1]: **Provider Protocol.**
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

    # R2: complete() REMOVED per DA[#4] GP[2] — zero callers in M1a/b.
    # Add back when M1c caller materializes.
    # ¬method: Provider does NOT execute tools (TurnEngine owns).
    # ¬method: Provider does NOT manage conversation state (stateless per-call).
```
**Invariants (R2-revised).**
  INV1→ Provider.stream() = exactly one SDK call; ¬tool-exec loop inside.
  INV2→ Provider.stream() emits exactly one StreamEvent(kind="stop") as final event (or kind="error").
  INV3→ **LOCKED R2** — errors ALWAYS emerge as StreamEvent(kind="error", error=exc); ¬raised exceptions across async iterator boundaries (resolves cqa BC-cqa-7).
  INV4→ **NEW R2 (impl-eng R2-NEW-2)** — Provider.stream() reconstruction state is WITHIN-CALL only; across-call state forbidden. SDK context-manager semantics MUST be used for connection lifecycle.
  INV5→ **NEW R2 (impl-eng R2-NEW-2 + cqa BC-cqa-3 T7)** — Provider.stream() MUST support early-termination cleanup via async-generator close() propagation to underlying SDK context.

IC[2]: **StreamEvent taxonomy + error convention (R2-EXPANDED, 5-kind).**
```python
@dataclass
class StreamEvent:
    kind: Literal["token", "tool_call", "stop", "tool_result", "error"]  # R2: +tool_result
    text: str = ""                     # kind="token"
    tool: dict | None = None           # kind="tool_call"; {"id", "name", "arguments"}
    stop_reason: str | None = None     # kind="stop"
    final_message: Message | None = None  # NEW R2: kind="stop" AND stop_reason="tool_use" — reconstructed canonical assistant Message (impl-eng BC#3)
    tool_call_record: ToolCallRecord | None = None  # NEW R2: kind="tool_result" — FULL ToolCallRecord (ui-ux IC-flag[5])
    error: Exception | None = None
    raw_event: dict | None = None      # optional raw SDK event for sidecar capture
```
**Event grammar (R2-NEW).**
`token* → (tool_call+ → stop(stop_reason="tool_use", final_message=M) → tool_result+)* → token* → stop(stop_reason∈{end_turn,max_tokens,max_tool_calls,error})`
**Invariants (R2-revised).**
  INV1→ Errors ALWAYS emerge as StreamEvent(kind="error", error=exc) — allows TurnEngine to capture partial content, persist stop_reason="error", continue loop.
  INV2→ stop_reason taxonomy: end_turn | max_tokens | tool_use | max_tool_calls | error | stop.
  INV3→ **NEW R2** — Multiple kind="tool_call" events MAY be emitted within one Provider.stream() call when model requests parallel tools (impl-eng BC#2). Each event carries exactly one tool dict. TurnEngine accumulates into Turn.tool_calls.
  INV4→ **NEW R2** — When stop_reason="tool_use", Provider MUST populate final_message with reconstructed canonical assistant Message (content = concatenated text blocks, tool_calls = list, preceding_text_per_tool_call = populated for Anthropic interleaved). (impl-eng BC#3)
  INV5→ **NEW R2** — kind="tool_result" events emitted ONLY BY TurnEngine (never by Provider). Emitted after each tool execution, before re-invoking Provider.stream(). tool_call_record.tool_call_id correlates with prior kind="tool_call" event in same turn. (ui-ux IC-flag[5] + cqa EG4)
  INV6→ **NEW R2** — Orphan kind="tool_result" (no matching prior tool_call) is contract violation; TurnEngine MUST raise. (cqa EG4/EG7)

IC[3]: **ToolSchema + ToolCallRecord.**
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
    ts_started: str                    # ISO-8601 timestamp
    ts_completed: str | None           # None if crashed pre-completion (replay-compat)
    latency_ms: int                    # monotonic_ns-derived
    result: str                        # string-coerced tool return
    result_chars: int
    error: str | None                  # error-class name if tool raised
    position_in_turn: int              # 0-indexed within this Turn
    preceding_text: str                # last 50 chars of text preceding this tool_call
```

IC[4]: **Canonical Message shape (R2-EXPANDED).**
```python
@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str                       # text content
    speaker: str | None = None         # ProviderSpec.key or "human"
    tool_call_id: str | None = None    # role="tool": result-of-tool-call-with-this-id
    tool_calls: list[dict] | None = None  # role="assistant" with tool use
    preamble_variant: Literal["neutral","identity-aware","research-framed"] | None = None  # logged field
    preceding_text_per_tool_call: list[str] | None = None  # NEW R2 (impl-eng BC#5): ith-element = text preceding tool_calls[i]; enables Anthropic content-block order reconstruction
    content_blocks: list[dict] | None = None  # NEW R2 (escape-hatch locked per DA[#2]): Anthropic-only fidelity for edge cases (cache_control, tool_result with image, etc.)
```
**Invariants.**
  INV1→ role="tool" REQUIRES tool_call_id. Adapter must reject otherwise.
  INV2→ role="assistant" with tool_calls MAY have content="" (tool-only response).
  INV3→ speaker populated for assistant role (identifies provider in multi-model sessions).
  INV4→ **NEW R2** — preceding_text_per_tool_call length equals tool_calls length when both populated.

IC[5]: **TurnEngine.advance_stream.**
```python
class TurnEngine:
    def __init__(
        self,
        policy: TurnPolicy,
        memory: MemoryHelper | None = None,
        metrics: MetricsCollector | None = None,
        max_tool_calls_per_turn: int = 5,
        tool_arg_validator: Callable[[ToolSchema, dict], dict] | None = None,  # DA[#10] GAP[3] seam
    ): ...

    async def advance_stream(
        self,
        state: ConversationState,
        tools: list[ToolSchema] | None = None,
    ) -> AsyncIterator[StreamEvent | Turn]: ...
```
**Tool-exec loop invariants (R2-revised).**
  INV1→ Each tool_call event from provider → execute tool → append tool_result Message → re-invoke provider.stream(messages=updated).
  INV2→ **REVISED R2 (impl-eng BC#4)** — On tool-call count == max_tool_calls, after executing Nth tool and yielding its tool_result, TurnEngine re-invokes provider.stream(messages=updated, tools=None) ONE FINAL TIME for text explanation. Yields resulting tokens + final stop. Overrides final stop_reason="max_tool_calls".
  INV3→ ToolCallRecord populated between ts_started (pre-exec) and ts_completed (post-exec). Uses monotonic_ns() for latency_ms.
  INV4→ **NEW R2** — Phase sequencing: (1) provider.stream yields tokens+tool_calls+stop(tool_use,final_message); (2) append final_message to state.messages; (3) for each tool_call: execute, build ToolCallRecord, yield StreamEvent(kind="tool_result"); (4) append tool_result Messages; (5) loop to (1) or hit max_tool_calls INV2.

IC[6]: **TurnPolicy protocol + concrete policies.**
```python
class TurnPolicy(Protocol):
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...
    # None → no eligible speaker → TurnEngine halts session.

class RoundRobinPolicy:
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None:
        if not state.roster: return None
        return state.roster[len(state.turns) % len(state.roster)]

class YieldNextPolicy:  # M1b
    # Parses trailing "@next:<key>" from last assistant turn content.
    # Case-sensitive exact match on ProviderSpec.key; trailing punctuation stripped.
    # Multiple @next: in same turn → use LAST (natural model revision pattern).
    # Self-nomination or unknown key → fallback RoundRobin.
    # Logs override to metrics.yield_next_override_rate.
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...

class RandomPolicy:  # M1b
    # Uniform random from roster excluding last speaker.
    # Accepts optional rng: random.Random | None = None (cqa EC[5] determinism).
    def next_speaker(self, state: ConversationState) -> ProviderSpec | None: ...
```

IC[7]: **Persistence JSONL record shapes + replay contract.**
Canonical form:
```jsonl
{"schema_version":"1","type":"session_header","session_id":"...","mode":"autonomous","roster":[...],"preamble_variant":"identity-aware","ts":"...","system_preamble":"..."}
{"schema_version":"1","type":"turn","speaker":"claude-opus-4-7","provider":"anthropic","content":"...","tokens_in":0,"tokens_out":0,"stop_reason":"end_turn","ttft_ms":450,"total_ms":2300,"ts":"...","tool_calls":[ToolCallRecord.to_dict(),...]}
{"schema_version":"1","type":"tool_call","turn_id":"...","speaker":"...","provider":"...","tool_name":"echo","arguments":{...},"ts_started":"...","ts_completed":"...","latency_ms":12,"result":"...","result_chars":24,"error":null,"position_in_turn":0,"preceding_text":"..."}
```
**Replay contract (R2-INVs added).**
  INV-replay-1→ replay skips malformed trailing lines with warning log (partial-flush graceful).
  INV-replay-2→ partial turn records (stop_reason="error") ARE INCLUDED in replayed state.
  INV-replay-3→ session_header MUST be valid first line; if missing, replay raises CorruptedSessionError.
  INV-replay-4→ schema_version forward-compat: v2 reader encountering "1" raises SchemaVersionMismatch with actionable message unless explicit migration layer provided.

## sub-task-decomposition

**M1a cluster A (foundation, must complete before B):**
SQ1: pyproject.toml + repo init + pre-commit + .gitignore (incl. sessions/) + pyright-strict + ruff-88 + pydocstyle + pytest-asyncio-strict |owner:implementation-engineer |est:0.5h |files:pyproject.toml,.gitignore,README.md-stub |deps:¬
SQ2: base types — Message (incl. preceding_text_per_tool_call + content_blocks + preamble_variant), StreamEvent (5-kind + final_message + tool_call_record), ToolSchema, CompleteResult, ToolCallRecord, Provider Protocol (¬complete() per GP[2]) |owner:implementation-engineer |est:1h |files:providers/base.py,providers/__init__.py |deps:SQ1
SQ3: ProviderSpec + roster.py (M1 entries + PROVIDERS dict + available() helper merged per DA[#4] GP[1]) |owner:implementation-engineer |est:0.5h |files:roster.py |deps:SQ2
SQ4: **REMOVED R2** (merged into SQ3 per DA[#4] GP[1] — no separate registry.py for M1a/b)
SQ5: errors.py classification taxonomy (port sigma-verify pattern, re-implement; error_class on StreamEvent(kind="error")) |owner:implementation-engineer |est:0.5h |files:providers/errors.py |deps:SQ2

**M1a cluster B (clients + mapping, PARALLELIZABLE):**
SQ6a: anthropic_client.py streaming (messages.stream context-manager; extract TTFT, stop_reason, usage; INV4+INV5 compliance) |owner:implementation-engineer-1 |est:2h |files:providers/anthropic_client.py |deps:cluster-A
SQ6b: ollama_client.py streaming (OpenAI-compat, chat.completions.create stream=True with include_usage; INV4+INV5 compliance) |owner:implementation-engineer-2 |est:2h |files:providers/ollama_client.py |deps:cluster-A
SQ6c: **NEW R2 (impl-eng BC#1)** — Ollama cloud /v1 streaming+tool_calls smoke test. AsyncOpenAI(base_url=ollama-cloud-v1) stream=True + minimal tool def on devstral-2:123b-cloud AND deepseek-v3.2:cloud; confirm tool_calls arrive in delta stream. Lives in scripts/smoke_ollama_v1.py (¬tests/live/). BLOCKS SQ14b. |owner:implementation-engineer |est:0.25h |files:scripts/smoke_ollama_v1.py |deps:cluster-A
SQ7: message_mapping.py streaming-only paths (Anthropic content↔canonical expand/collapse, Ollama identity) |owner:implementation-engineer |est:2h (R2 +0.5h) |files:providers/message_mapping.py |deps:SQ2+SQ6a+SQ6b

**M1a cluster C (orchestration):**
SQ8a: **NEW R2 split** — conversation.py dataclasses (Turn, ConversationState, PreambleVariant Literal type) |owner:implementation-engineer |est:0.5h |files:conversation.py |deps:SQ2
SQ8b: **NEW R2 split** — identity-aware preamble rendering (1 variant per DA[#4] GP[3]) |owner:implementation-engineer |est:0.25h |files:conversation.py |deps:SQ8a
SQ9: turn_engine.py — RoundRobinPolicy + advance_stream (¬tool-exec loop yet for M1a) |owner:implementation-engineer |est:2.5h (R2 +0.5h) |files:turn_engine.py |deps:SQ8a
SQ10: persistence.py — write_session, write_turn, replay, schema_version="1" on every record, INV-replay-1/2/3 |owner:implementation-engineer |est:1.5h |files:persistence.py |deps:SQ8a
SQ10b: **NEW R2 (impl-eng BC#9 + cqa BC-cqa-4)** — replay robustness tests (malformed trailing line, missing header, crash-mid-turn) |owner:code-quality-analyst |est:0.5h |files:tests/test_persistence_replay.py |deps:SQ10
SQ11: cli.py — argparse, streaming tokens to stdout with flush, speaker attribution, Ctrl-C flush, JSONL writes |owner:implementation-engineer |est:1h |files:cli.py |deps:SQ9+SQ10
SQ11b: **NEW R2 (EC[3])** — context truncation helper: budget check before advance_stream, truncate-oldest per ADR[5], emit `[truncated: N]` marker |owner:implementation-engineer |est:0.75h |files:turn_engine.py or context.py |deps:SQ9

**M1a cluster D (tests):**
SQ12a: mock_providers.py fixture — async mock Provider with Anthropic-event-sequence fidelity (G1) + Ollama tool_calls chunk-accumulation (G2) |owner:code-quality-analyst |est:2h (R2 +1h per cqa BC-cqa-2) |files:tests/fixtures/mock_providers.py |deps:SQ2
SQ12b: test_providers_base.py — Provider Protocol conformance |owner:code-quality-analyst |est:0.5h |files:tests/test_providers_base.py |deps:SQ2+SQ12a
SQ12c: test_providers_streaming.py — per-SDK stream+usage extraction, S1-S4 (TTFT, stop_reason taxonomy, usage fallback, mid-stream error) |owner:code-quality-analyst |est:2h |files:tests/test_providers_streaming.py |deps:SQ6a+SQ6b
SQ12d: test_message_mapping.py — round-trip streaming paths (MERGE GATE 3-tier: Tier 1 hand-golden outbound + Tier 2 hand-golden inbound + Tier 3 round-trip smoke) |owner:code-quality-analyst |est:2.5h (R2 +1h per DA[#6]) |files:tests/test_message_mapping.py,tests/fixtures/anthropic_golden.py,tests/fixtures/openai_golden.py |deps:SQ7
SQ12e: test_turn_engine.py — RoundRobin + advance_stream with mock provider |owner:code-quality-analyst |est:1h |files:tests/test_turn_engine.py |deps:SQ9+SQ12a
SQ12f: test_conversation.py |owner:code-quality-analyst |est:0.5h |files:tests/test_conversation.py |deps:SQ8a
SQ12g: test_persistence.py — JSONL round-trip incl. schema_version |owner:code-quality-analyst |est:1h |files:tests/test_persistence.py |deps:SQ10
SQ12h: **NEW R2 (cqa BC-cqa-5)** — test_cli.py: stdout buffering, UTF-8 encoding, speaker attribution, Ctrl-C flush |owner:code-quality-analyst |est:1.5h |files:tests/test_cli.py |deps:SQ11
SQ12i: **NEW R2 (cqa BC-cqa-6)** — test_live_smoke_m1a.py: 1 Anthropic turn + 1 Ollama-cloud turn, streamed, JSONL written, NO tools; SKIP by default |owner:code-quality-analyst |est:1h |files:tests/live/test_live_smoke_m1a.py |deps:SQ11
SQ12j: **NEW R2 (cqa BC-cqa-7)** — test_stream_error_convention.py: Provider raises → assert StreamEvent(kind="error") emitted, no exception propagated |owner:code-quality-analyst |est:0.5h |files:tests/test_stream_error_convention.py |deps:SQ6a+SQ6b
SQ12k: **NEW R2 (EC[3])** — test_context_truncation.py: budget check + truncate-oldest + [truncated: N] marker |owner:code-quality-analyst |est:1h |files:tests/test_context_truncation.py |deps:SQ11b

**M1b cluster E (tool-schema + providers tool-use):**
SQ13: tool_schema.py — ToolSchema → Anthropic tool format + Ollama OpenAI-compat function format |owner:implementation-engineer |est:1h |files:providers/tool_schema.py |deps:M1a-complete
SQ14a: anthropic_client.py tool-use streaming (tool_use content blocks → kind="tool_call"; stop_reason="tool_use" w/ final_message reconstruction) |owner:implementation-engineer-1 |est:2.5h (R2 +0.5h per impl-eng BC#11) |files:providers/anthropic_client.py |deps:SQ13
SQ14b: ollama_client.py tool-use streaming (tool_calls delta → kind="tool_call"; final_message reconstruction) |owner:implementation-engineer-2 |est:2h (+0.5h conditional if SQ6c fails + ollama-SDK pivot) |files:providers/ollama_client.py |deps:SQ13+SQ6c
SQ15: message_mapping.py tool-use paths (Anthropic tool_use/tool_result ↔ canonical w/ preceding_text_per_tool_call; Ollama identity) |owner:implementation-engineer |est:4h (R2 +1.5h per impl-eng BC#6) |files:providers/message_mapping.py |deps:SQ14a+SQ14b

**M1b cluster F (TurnEngine tool-exec + policies):**
SQ16: TurnEngine tool-exec loop (cap 5, INV2-revised final-text-response, INV4 phase sequencing, INV6 kind="tool_result" emission) |owner:implementation-engineer |est:2.5h |files:turn_engine.py |deps:SQ15
SQ17: YieldNextPolicy (case-sensitive match, trailing punctuation stripped, multiple @next: uses LAST, self-nom/unknown fallback RoundRobin) |owner:implementation-engineer |est:1h |files:turn_engine.py |deps:SQ9
SQ18: RandomPolicy (excludes last speaker, accepts optional rng: random.Random per EC[5]) |owner:implementation-engineer |est:0.5h |files:turn_engine.py |deps:SQ9
SQ19: echo_tool fixture (name="echo", params={"text": str}, returns text verbatim) |owner:implementation-engineer |est:0.25h |files:tests/fixtures/echo_tool.py |deps:¬
SQ20: MetricsCollector baseline (record_turn, record_tool_call, snapshot) |owner:implementation-engineer |est:1.5h |files:metrics.py |deps:SQ2
SQ21: Raw event capture sidecar (conditional on tool_use_reliability != "reliable" OR CHATROOM_CAPTURE_RAW=1) |owner:implementation-engineer |est:1h |files:persistence.py,providers/anthropic_client.py,providers/ollama_client.py |deps:SQ10

**M1b cluster G (tests):**
SQ22: test_providers_tool_use.py — per-SDK tool-call emission + EG2 parallel tool_call accumulation + EG3 final_message reconstruction fidelity |owner:code-quality-analyst |est:3h (R2 +1h per cqa BC-cqa-11) |files:tests/test_providers_tool_use.py |deps:SQ14a+SQ14b
SQ23: test_message_mapping.py tool-use paths (MERGE GATE 3-tier expansion; F1 tool_use_id preservation + F3 multi-tool ordering + F6 malformed JSON fallback MUST; F2/F4/F5/F7 SHOULD; hand-golden outbound+inbound both SDKs) |owner:code-quality-analyst |est:3.5h (R2 +1.5h per DA[#6]+cqa BC-cqa-1 R2-Δ-1) |files:tests/test_message_mapping.py,tests/fixtures/anthropic_responses_golden.py,tests/fixtures/openai_responses_golden.py |deps:SQ15
SQ24: test_turn_engine_tools.py — T1+T3+T4+T6+T8+T9 MUST (PM/INV-mandated); T2+T5+T7 SHOULD; EG1 event-grammar conformance + EG4 tool_result correlation + EG5 max_tool_calls final-text |owner:code-quality-analyst |est:3h (R2 +1h per cqa BC-cqa-3) |files:tests/test_turn_engine_tools.py |deps:SQ16+SQ19
SQ25: test_metrics.py — MetricsCollector correctness |owner:code-quality-analyst |est:0.5h |files:tests/test_metrics.py |deps:SQ20
SQ26: test_persistence.py raw-sidecar expansion (J4 raw-sidecar correlation: every tool_call in main has corresponding raw_event, timestamps align ≤10ms) |owner:code-quality-analyst |est:0.5h |files:tests/test_persistence.py |deps:SQ21
SQ27a: **SPLIT R2 (cqa EC[4])** — test_yield_next_policy.py (case-sensitive, punctuation strip, multiple @next:, self-nom/unknown fallback) |owner:code-quality-analyst |est:1h |files:tests/test_yield_next_policy.py |deps:SQ17
SQ27b: **SPLIT R2** — test_random_policy.py (exclude-last, seeded rng determinism per EC[5]) |owner:code-quality-analyst |est:0.5h |files:tests/test_random_policy.py |deps:SQ18
SQ28: **NEW R2 (cqa BC-cqa-6)** — test_live_smoke_m1b.py: 1 echo round-trip per provider (M1 seed pair). Gated dual flag. |owner:code-quality-analyst |est:1h |files:tests/live/test_live_smoke_m1b.py |deps:SQ16+SQ19

**Estimate totals (R2 parallelized).**
M1a: ~17.5h (R1 14h + 3.5h = SQ12a+SQ12d +2h / SQ7+SQ9 +1h / SQ11b+SQ12k +1.75h / SQ12h+SQ12i+SQ12j +3h / -0.25 SQ4 removed / -0.25 SQ8-GP3).
M1b: ~23.5h (R1 18h + 5.5h = SQ15 +1.5 / SQ23 +1.5 / SQ22+SQ24 +2 / SQ10b +0.5 / SQ28 +1 / SQ6c +0.25 / SQ27 +0.5 / -0.25 GP3).
Grand total R2: ~41h parallelized (R1 32h; +28%). Justified by merge-gate rigor + 4-agent IC[2] convergence + PM-mandated coverage + anti-mock-overconfidence live-smoke.

## forward-plan (Q3 scope — preliminary, revised after M1a/b)

### Scope-note
!planning-artifact, ¬C2-code-scope. Phases below revised as M1a/b empirical findings arrive.

### M1c — clone to remaining SDK families (est: 1-2 weeks after M1b ships)
**Deliverables.**
  - `providers/openai_client.py` (OpenAI SDK native + Ollama local as subclass per sigma-verify pattern)
  - `providers/google_client.py` (google-genai SDK, Gemini function_declarations)
  - `providers/message_mapping.py` Gemini parts adapter (new, hardest adapter — see PM[1] rationale)
  - `providers/tool_schema.py` Gemini + OpenAI schema adapters
  - `roster.py` expanded to 13 ProviderSpec entries (sigma-verify providers list as source of truth)
  - Tests green across all 4 SDK families; test_message_mapping.py merge gate expanded.

**Revision hooks tied to M1a/b findings.**
  H1→ If M1a finds `reported_input_tokens` diverges from `len(text)//4` by >15% for any M1 model, M1c MUST ship per-model calibration (shifted LEFT from M3). Reason: small-context providers (llama3.1:8b @ 8K) are now in scope; 60% buffer assumption invalidated.
  H2→ If M1b finds devstral-2:123b `tool_use_reliability="none"`, M1c scope expands to test ALL Ollama cloud + local models for tool_use reliability systematically (escalate to M3 empirical task). Roster entries updated empirically.
  H3→ If M1b surfaces Anthropic message_mapping fidelity loss (PM[1] triggers), M1c adds `content_blocks` escape-hatch to Message dataclass BEFORE Gemini adapter is written (Gemini parts model is even more structured than Anthropic's).

### M2 — Streamlit MVP (est: 2-3 weeks after M1c)
**Pre-M2 task (hard gate).** 2-hour async→sync-generator shim prototype. Must prove:
  - `st.write_stream()` can consume an async iterator of non-string events (via sync-wrapper generator).
  - Tool-call badges render inline with streaming tokens without flicker.
  - One turn per Streamlit rerun; autonomous-loop toggle mechanics sound.
  If prototype fails → fall back to Textual TUI for v1 per source-plan risk-table. Do NOT commit M2 scope until prototype green.

**Deliverables.**
  - `streamlit_app.py` entry
  - `ui/sidebar.py` — roster picker, mode toggle, preamble picker
  - `ui/transcript.py` — streamed transcript + tool-call badges
  - `ui/controls.py` — advance/pause/inject/stop buttons
  - Session list + resume from JSONL.

**Revision hooks tied to M1a/b findings.**
  H4→ If M1a's Provider.stream AsyncIterator turns out to be hard to convert to sync-generator in the 2h prototype, reconsider streaming architecture — possibly fall back to non-streaming for UI layer, keep streaming for CLI layer (dual path).
  H5→ If M1b's ToolCallRecord has fields that are expensive to compute live (e.g. preceding_text requires full turn buffer), M2 badge render uses deferred population.

### M3 — sigma-mem wiring + metrics + v1 ship (est: 2-3 weeks after M2)
**Deliverables.**
  - `memory.py` — MemoryHelper + MCP client for sigma-mem
  - `SIGMA_MEM_RECALL` tool schema registered when tools_enabled=True
  - `metrics.py` expansion — per-speaker + per-session aggregates, live panel updates
  - `ui/metrics_panel.py`
  - Per-model context calibration using `reported_input_tokens` → update `ProviderSpec.context_correction_factor`
  - `test_live_smoke.py` gated by CHATROOM_LIVE_TESTS=1 → 3-model autonomous session with sigma_mem_recall

**Revision hooks.**
  H6→ If M1b's MetricsCollector baseline proves insufficient for research-question pinning (see source-plan open decisions), M3 metrics scope expands to answer the pinned question.
  H7→ User must pin research question (open-decision #1 in source plan) BEFORE M3 scope locks. Without a pinned question, metrics panel risks scope creep.

**v1 ship criterion.** 3-model autonomous session with real sigma_mem_recall works end-to-end; metrics panel live-updates; JSONL replay reproduces sessions.

### M4 — more tools + richer metrics (est: 2-3 weeks, post-v1)
**Deliverables.**
  - Additional tools: web_search, calculator, code_exec (each a ToolSchema + executor)
  - Embedding-based metrics: convergence/divergence, topic drift, speaker-influence graph (requires embedding model choice — defer pending user decision)
  - Transcript summarization for long sessions
  - Per-model temperature customization in sidebar

**Revision hooks.**
  H8→ M4 scope strongly depends on M3 research-question pinning outcome. If pinned question is (a) memory-invocation coherence, embeddings are core; if (c) yield-next spontaneity, embeddings are not needed.

### Forward-plan summary
Q3 planning scope surfaces 8 revision hooks. C2 build-track may flag additional hooks after stress-testing M1a/b scope. This is a living plan; user/lead should revisit after M1a ships empirical data.

## pre-mortem

PM[1]: **message_mapping.py Anthropic adapter explodes in scope.** |likelihood:M (0.55 R1 → **0.25 R2** post-escape-hatch-lock) |reasoning:Anthropic tool_use inside assistant content-blocks + tool_result inside user content-blocks with ID-linked pairs. Splitting into OpenAI sibling form requires: (1) assistant [text, tool_use, text, tool_use] → content="text1 text2" + tool_calls=[...] (lossy — ordering unrecoverable WITHOUT preceding_text_per_tool_call field); (2) user [tool_result, tool_result] → 2 separate role="tool" msgs with matching tool_call_id. |detection:test_message_mapping.py 3-tier MERGE GATE fails OR production ValidationError |mitigation-R2-LOCKED-IN-ADR[4]: (a) `Message.preceding_text_per_tool_call` field populated for Anthropic interleaved content preserves ordering; (b) `Message.content_blocks` escape-hatch for edge cases (cache_control, image tool_result); (c) 3-tier hand-golden MERGE GATE (Tier 1 outbound + Tier 2 inbound + Tier 3 round-trip smoke); (d) known-lossy cases documented in message_mapping.py docstring |trigger-for-escalation:if ≥2 round-trip test fixtures fail at SQ15 boundary → consider Anthropic-native canonical for assistant messages (hybrid canonical)

PM[2]: **Ollama OpenAI-compat tool_calls reliability on devstral-2:123b unreliable.** |likelihood:M (0.40) |reasoning:Mistral function-calling training on Devstral lineage documented but Ollama cloud /v1 layer adds serialization round-trip. Historical pattern: Ollama OpenAI-compat function_calling has intermittent malformed-JSON on nested objects. tool_use_reliability="unknown" per roster until M1b empirical test. |detection:SQ6c smoke (pre-SQ14b) + M1b integration echo round-trip (post-SQ16) |mitigation-R2:(a) SQ6c tests BOTH devstral-2:123b AND deepseek-v3.2:cloud pre-SQ14b; pick better pair per empirical; (b) Raw event capture (ADR[6]) default-on for devstral (reliability="unknown"); (c) MANUAL escalation policy per UD#2 — operator observes raw capture + updates roster.py |trigger-for-escalation-R2-QUANTIFIED:(i) 3/3 fail × 3 prompt phrasings → reliability="none" → swap seed pair's Ollama to deepseek-v3.2:cloud via --models CLI flag; raw capture attached; (ii) 1-2/3 malformed → reliability="nominal" → keep devstral + annotate roster.py; (iii) 0/3 fail + 3/3 well-formed → reliability="reliable" → lock in roster.py. AUTO-escalation deferred to M1c+ per impl-eng R2-clarify-2.

PM[3]: **Streaming + async + tool-exec state-machine bug.** |likelihood:M (0.35) |reasoning:Tool-exec loop interleaves async-generator consumption → sync tool call → async-generator re-entry. Risks: (a) partial buffer from provider.stream() not flushed before re-invocation; (b) ToolCallRecord ts_started/ts_completed captured under wrong event-loop context; (c) exceptions during tool execution not surfaced back into StreamEvent(kind="error") correctly; (d) NEW R2 — reconstructed final_message on stop(tool_use) mis-populated across parallel tool_calls. |detection:test_turn_engine_tools.py SQ24 T1-T9 covers; adversarial test for (c); EG1 event-grammar conformance catches (d) |mitigation-R2:(a) IC[5] INV1-INV4 explicit phase sequencing; (b) monotonic_ns() for latency_ms not wall-clock; (c) test_tool_exec_error_propagation in SQ24 T4; (d) IC[1] INV4 (within-call reconstruction state only) + INV5 (early-termination cleanup) prevent state leak; EG2 parallel tool_call accumulation test + EG3 final_message reconstruction fidelity in SQ22 |trigger-for-escalation:if >1 async-state-machine bug in SQ24 review → pause + re-scope: simplify tool-exec to sync await tool_coro() inside async generator (already default; make explicit policy)

PM[4]: **XVERIFY infrastructure hang blocks §2h gate.** |likelihood:H (1.0 — observed this session 3x: DA-r1, TA-r1, TA-r2) |reasoning:sigma-verify cross_verify + verify_finding appear to fan out multi-provider calls without per-provider timeout; one slow provider blocks entire call. Pattern surfaced via TA-r2 time-box abort. |detection:tool call exceeds 90s → abort per boot directive |mitigation-R2:(a) XVERIFY[ADR3] marked NOT-ATTEMPTED with infra-gap documentation in gate-log (¬silently skipped per §2h); (b) compensating evidence via 4-agent cross-agent consensus (none challenged ADR3 location) + DB re-run (DA[#1] response) + industry-pattern audit (autogen+crewai+LangChain); (c) BELIEF[ADR3] dropped 0.88→0.84 to reflect XVERIFY miss honestly |trigger-for-escalation:post-C1 troubleshoot session — fix mcp__sigma-verify cross_verify timeout + per-provider partial-result return; retry XVERIFY[ADR3] before M1b commits first line of tool-exec code

PM[5]: **Ollama /v1 streaming+tool_calls broken — blocks M1b.** |likelihood:M (~0.45) |reasoning:ollama-mcp-bridge inline warning on /v1 (DO-NOT-switch) + issue #12557 actual-content about /api/chat non-piecewise streaming (closed ¬bug) + XVERIFY[openai:gpt-5.4] uncertain(low) — plan bets M1b on unverified SDK behavior. |detection:SQ6c 15-min smoke test BEFORE SQ14b commits 2h |mitigation-R2:(a) SQ6c runs pre-SQ14b; if passes, proceed with openai SDK AsyncStream; if fails, pivot to ollama pypi AsyncClient (+0.5h SQ14b) OR constrain M1b tool-use to Anthropic-only with Ollama-tool-use deferred to M1c gate; (b) Raw capture (ADR[6]) surfaces WHICH failure mode |trigger-for-escalation:if SQ6c fails for BOTH devstral-2:123b AND deepseek-v3.2:cloud, M1b tool-use scope contracts to Anthropic-only; Ollama-tool-use becomes M1c deliverable; revised M1b verification criterion: "≥1 echo round-trip for Anthropic; Ollama tool-use documented as M1c scope."

## files
| File | Action | Description |
| ---- | ------ | ----------- |
| ~/Projects/sigma-chatroom/pyproject.toml | new | deps: anthropic, openai, pydantic, pytest, pytest-asyncio |
| ~/Projects/sigma-chatroom/.gitignore | new | incl. sessions/, .venv/, __pycache__ |
| ~/Projects/sigma-chatroom/README.md | new | stub; M1 scope; live-test env instructions |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/__init__.py | new | package marker |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/__init__.py | new | re-exports base types |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/base.py | new | Message, StreamEvent, ToolSchema, CompleteResult, ToolCallRecord, Provider Protocol (IC[1-4]) |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/registry.py | new | PROVIDERS dict, env-key discovery, registry.available() |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/anthropic_client.py | new | M1a: streaming; M1b: +tool_use |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/ollama_client.py | new | OpenAI-compat; M1a: streaming; M1b: +tool_calls |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/message_mapping.py | new | canonical↔SDK; merge-gate file |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/tool_schema.py | new | M1b: ToolSchema→per-SDK format |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/providers/errors.py | new | error classification taxonomy |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/roster.py | new | ProviderSpec catalog (M1 entries only for M1a/b) |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/conversation.py | new | Turn, ConversationState, PreambleVariant |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/turn_engine.py | new | M1a: RoundRobin+advance_stream; M1b: +tool-exec loop, +YieldNext/Random (IC[5-6]) |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/persistence.py | new | JSONL write+replay, schema_version="1", raw sidecar (M1b) |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/metrics.py | new | M1b: MetricsCollector baseline |
| ~/Projects/sigma-chatroom/src/sigma_chatroom/cli.py | new | headless streaming runner |
| ~/Projects/sigma-chatroom/tests/fixtures/mock_providers.py | new | async mock Provider |
| ~/Projects/sigma-chatroom/tests/fixtures/echo_tool.py | new | M1b: echo tool |
| ~/Projects/sigma-chatroom/tests/test_providers_base.py | new | Protocol conformance |
| ~/Projects/sigma-chatroom/tests/test_providers_streaming.py | new | per-SDK streaming |
| ~/Projects/sigma-chatroom/tests/test_providers_tool_use.py | new | M1b: per-SDK tool-use round-trip |
| ~/Projects/sigma-chatroom/tests/test_message_mapping.py | new | MERGE GATE round-trip tests |
| ~/Projects/sigma-chatroom/tests/test_turn_engine.py | new | RoundRobin + advance_stream |
| ~/Projects/sigma-chatroom/tests/test_turn_engine_tools.py | new | M1b: tool-exec loop |
| ~/Projects/sigma-chatroom/tests/test_conversation.py | new | Turn/ConversationState |
| ~/Projects/sigma-chatroom/tests/test_persistence.py | new | JSONL round-trip + raw sidecar |
| ~/Projects/sigma-chatroom/tests/test_metrics.py | new | M1b: MetricsCollector |
| ~/Projects/sigma-chatroom/tests/test_yield_next_policy.py | new | M1b: YieldNext parse + fallback |
| ~/Projects/sigma-chatroom/tests/test_random_policy.py | new | M1b: RandomPolicy exclude-last |
| ~/Projects/sigma-verify/src/sigma_verify/clients.py | read-only | pattern reference; ¬import (C3 hard-stop) |

## convergence

tech-architect: ✓ plan-complete |ADR:#8 |IC:#7 |SQ:#27 (M1a:12, M1b:15) |PM:#3 |forward-plan:✓ (4 phases M1c-M4, 8 revision-hooks) |DB:#3 (ADR[1]+[3]+[4]) |XVERIFY:deferred-to-DA-round (ADR[3] candidate) |DA-resp:#0 (pre-challenge) |§2a/b/c/e:✓ |source-tags:✓ |P(plan-ready):0.82 → ready-for-challenge-round-not-lock-yet

ui-ux-engineer: ✓ plan-complete (secondary-plan-track) |FC:#1(deferral-safe-conditional) |DS:#7 |IX:#7 |A11Y:#6 |PERF:#3 |ES:#8 |IC-flags:#6 (IC-flag[5] MATERIAL GAP → tech-architect, HIGH priority) |M2-subphase-forward-plan:✓ (pre-M2/M2a/M2b/M2c + 6 UX-revision-hooks) |DB:#2 (FC top-1 + option-b-feasibility top-2) |XVERIFY:#1 openai:gpt-5.4 partial on FC (counter incorporated in DB) |OQ:#4 (rendering-option, TUI-vs-Streamlit, research-Q-pin, custom-aria-component) |source-tags:[source-plan, cross-agent:IC[1-7], external-verification:streamlit-docs-T1, external-verification:XVERIFY-openai-gpt5.4, agent-inference, WCAG-2.2-T1] |§2a/b/c/d/e/g/h:✓ |→ ready-for-DA-challenge |P(plan-ready ui-ux-scope):0.83

ui-ux-engineer R2: ✓ R2-complete |DA-resp:#4 (DA4-GP3 concede+compromise on preamble-variants, DA5 accept+apply decomposition to UX-H3+UX-H4, DA8 CONFLICT[1] defend-both-IC[2]-additions, IC-flag[5] reaffirmed as distinct-from-impl-eng-BC#3) |user-decisions-applied:#5 (UD#3 agnosticism-verified-conditional-on-IC-flag[5], UD#4 STEP-3b TUI-sketch baked into pre-M2, UD#5 M3 metrics re-prioritized around memory-invocation-coherence, UD#6 A11Y[2] DOCUMENTED-GAP marked, UD#2/7/8 out-of-ui-scope concede) |IX-revisions:IX[1] a11y-gap-note + IX[5] 1-variant-first-M2a / 2nd-M2b / 3rd-M2c-conditional + IX[6] priority-2-supplement |forward-plan-revised:pre-M2 +STEP-0 (tech-architect R2 IC-flag[5] gate) +STEP-3b (UD#4 TUI sketch) / M2a -0.25d / M2b +0.25d / M2c conditional-variant-3 / 6 hooks decomposed code-vs-research |lead-item-7 cqa EC[5] RandomPolicy: concede out-of-ui-scope |net-scope-delta: +0.25d M2-streamlit, M2-TUI shorter, pre-M2 +2h |P(plan-ready ui-ux-scope R2):0.88 |→ pending tech-architect R2 dual-IC[2]-addition acceptance (final_message + kind="tool_result") |→ ready-for-lock-post-tech-architect-R2

implementation-engineer: ✓ feasibility-check-R1-complete |BC:#15 (sdk-contract:3, ic-gap:3, sq-estimate:5, test-coverage:2, risk-calibration:2) |concerns-resolved:#1 (ADR[1] purpose-built confirmed via code-read) |concerns-open:#14 (11 revise/clarify targeting tech-architect ADR/IC/SQ; 1 conditional blocking SQ14b; 1 accept-with-rationale) |load-bearing:{H2-ollama-v1-streaming-tool_use-feasibility-GAP, ADR[4]-interleaved-content-lossiness, IC[5]-max_tool_calls-truncation-vs-final-response, IC[2]-parallel-tool_calls-invariant-missing, IC[5]-assistant-msg-reconstruction-gap} |DB:#2 (H2-ollama + ADR4-direction-asymmetry) |XVERIFY:#1 openai:gpt-5.4 uncertain(low) on H2-ollama-streaming-tool_use |new-SQ-proposed:SQ6c (0.25h Ollama /v1 streaming+tool_calls smoke test, blocks SQ14b) |source-tags:[code-read:9, agent-inference:15, independent-research:2, external-verification:1, gh-CLI:1] |§2a/b/c/e/d:✓ |→ ready-for-C2 conditional-on-tech-architect-R2-responses-to-11-clarify/revise-items + DA-round-resolution |recommend-XVERIFY-trigger:YES on H2 (Ollama streaming tool_calls) — highest-feasibility-risk pre-SQ14b

code-quality-analyst: ✓ R2-complete (test-strategy-challenge R1+R2) |BC:#11 + EC:#5 + R2-Δ:#4 (2 real+2 confirmations) |merge-gate-coverage-score:L→M-with-revisions-and-golden-fixtures |edge-case-gaps:#5 |load-bearing:{BC-cqa-1 message_mapping fixture-matrix (F1+F3+F6 MUST + F2+F4+F5+F7 SHOULD + R2-Δ-1 G-F1+G-F2+G-F3 hand-computed SDK goldens for symmetric-field-loss), BC-cqa-3 TurnEngine tool-exec T6+T8+T9 PM-mandated-absent, BC-cqa-2 mock-fidelity Anthropic-event-sequence 1h→2h, BC-cqa-11 IC[2]/IC[5] event-grammar-cluster separable EG2/EG3 (DA7 clarified)} |cross-agent-convergence:4-originals+DA-rounds (impl-eng BC #14 direction-asymmetry + BC #10 replay-partial-turn + BC #7 preamble-rendering + TRIPLE on IC[2]/IC[5] with impl-eng BC #2/#3 + ui-ux E6/IC-flag[5] + R2 DA6 golden-fixtures + DA7 separability + DA4 complete()-dead-code confirms BC-cqa-8-D1 + DA5 H2-sweep-scope confirms BC-cqa-6) |SQ-revisions:{SQ12d 1.5h→2.5h (R2 +G-F1+G-F3 goldens), SQ23 2h→3.5h (R2 +G-F1+G-F2+G-F3 goldens), SQ24 2h→3h, SQ12a 1h→2h, SQ22 2h→3h conditional-on-IC[2]-cluster-accept} |SQ-additions:{SQ12h test_cli 1.5h, SQ12i+SQ28 live-smoke 2h (M1a/b code-path, ¬H2-reliability-sweep), SQ12j error-convention 0.5h, SQ12k context-truncation 1h} |contract-contradiction-flagged:IC[1]-INV3 vs IC[2] error-convention → lock IC[2] ALWAYS-emerge |event-grammar-test-additions:EG1-EG5 separable (EG2 INV4-independent, EG3 final_message-independent, EG1/EG4/EG5 integrated) |DB:#2 (BC-cqa-1 fixture-expansion + BC-cqa-3 state-machine-coverage) |XVERIFY:not-triggered (budget-aware) |source-tags:[code-read plan-track ADR/IC/SQ/PM:13, code-read sigma-verify tests:3, agent-inference:17, independent-research Anthropic+OpenAI+Ollama SDK:3, cross-agent impl-eng+ui-ux+feedback-memory+DA-rounds:9] |§2a/b/c/d/e:✓ |§2g DB on top-2:✓ |total-SQ-impact:+8-10h cqa alone, ~39-41h stacked with impl-eng |→ ready-for-C2-dispatch

## belief-tracking

BELIEF[ADR1 purpose-built providers]: 0.92 |source:code-read+industry-pattern |load-bearing:yes |DB-reconciled
BELIEF[ADR2 native tool-use]: 0.95 |source:source-plan+SDK-docs |load-bearing:yes |C4-hard-stop
BELIEF[ADR3 tool-exec in TurnEngine]: 0.88 |source:agent-inference+industry-pattern |load-bearing:yes |DB-reconciled |XVERIFY-candidate
BELIEF[ADR4 OpenAI-shaped canonical]: 0.80 |source:independent-research+agent-inference |load-bearing:yes |DB-reconciled |elevated-risk:acknowledged-via-PM[1]

[tech-architect R2 BELIEF updates (26.4.20)]
BELIEF[ADR3 tool-exec in TurnEngine] R2: 0.88 → **0.84** |source:DB-rerun-per-DA[#1] |reasoning:LangChain-AgentExecutor counter (Provider-owned loop is industry mode for N=1 SDK) is real; our N>3 + observability mandate defends ADR, but weaker than generic-SoC framing. |XVERIFY-gap-documented per DA[#3]
BELIEF[ADR4 OpenAI-shaped canonical] R2: 0.80 → **0.70** |source:DA[#2] math + escape-hatch-locked-into-ADR + DB-rerun-per-DA[#1] |reasoning:escape-hatches (preceding_text_per_tool_call + content_blocks) now IN ADR[4] proper not PM[1] mitigation; 3-tier hand-golden merge-gate locked; P(PM1-fires-and-escapes-mitigation) ~0.25; conservative 0.70 acknowledges Gemini M1c+ uncertainty.
BELIEF[IC[2] 4-agent dual-additions accepted] R2: 0.90 |source:4-agent-cross-agent-convergence + impl-eng R2-NEW-2 SDK-context-manager-resolves-stateless-concern |load-bearing:yes |INV4+INV5+INV6+INV7 locked
BELIEF[IC[1] INV3 always-emit-error locked] R2: 0.95 |source:cqa BC-cqa-7 + DA[#8] + impl-eng R2-NEW-2 |prior-contradiction resolved
BELIEF[IC[5] INV2 max_tool_calls + final-text] R2: 0.80 |source:impl-eng BC#4 + DA[#7] |+1 SDK call per max-hit turn; preserves UX invariant
BELIEF[UD#2 manual-M1b-auto-M1c+ escalation] R2: 0.85 |source:impl-eng BC[R2-clarify-2] + PM[2] thresholds specified |matches user UD#2 intent
BELIEF[H2 decompose H2-code+H2-research] R2: 0.85 |source:DA[#5] + impl-eng BC#15 + UD#1 checkpoint |forward-plan timeline preserved
BELIEF[3-tier merge-gate hand-golden] R2: 0.88 |source:DA[#6] + cqa R2-Δ-1 + impl-eng BC#14 |catches symmetric-field-loss bugs round-trip misses
BELIEF[SQ-estimates-revised-R2] R2: 0.82 |source:cross-agent-convergence impl-eng+cqa |M1a ~17.5h, M1b ~23.5h, grand ~41h parallelized; +28% vs R1; justified

BELIEF[P(plan-ready)] R2: **0.87** |pre-exit-gate re-eval |XVERIFY[ADR3] gap documented (not-silently-skipped); compensated by 4-agent consensus + DB re-run; all other DA/BC items addressed
BELIEF[ADR5 60%+len//4]: 0.85 |source:source-plan+tokenizer-research |load-bearing:no (config) |revision-hook-added
BELIEF[ADR6 raw-capture default-on]: 0.90 |source:source-plan+observability-pattern |load-bearing:no
BELIEF[ADR7 schema_version per-record]: 0.95 |source:C8+industry-pattern |load-bearing:no
BELIEF[ADR8 streaming day-1]: 0.92 |source:C5+agent-inference |load-bearing:no

BELIEF[PM1 message_mapping Anthropic adapter explodes]: L=MH (0.55) |detection:test_message_mapping round-trip |mitigation:merge-gate-tests+content_blocks-escape-hatch
BELIEF[PM2 devstral-2 tool_use unreliable]: L=M (0.40) |detection:M1b echo round-trip |mitigation:raw-capture+escalation-to-deepseek alternate
BELIEF[PM3 async-state-machine bug in tool-exec loop]: L=M (0.35) |detection:test_turn_engine_tools |mitigation:IC[5] invariants explicit

BELIEF[P(plan-ready)]: 0.82 |pre-challenge-round |post-DA+build-challenge expected >0.85 for lock

[impl-eng R1 beliefs — feasibility gaps surfaced]
BELIEF[H2-ollama-v1-streaming-tool_use-works]: 0.55 |source:code-read(ollama-mcp-bridge ollama_client.py:11-14 contradicts)+gh-CLI(issue#12557 closed-not-bug-about-/api/chat)+XVERIFY[openai:gpt-5.4 uncertain-low]+independent-research |load-bearing:YES for M1b |action:SQ6c smoke test resolves pre-SQ14b
BELIEF[ADR4-Anthropic-interleaved-content-loss-PM1-sufficient]: 0.60 |source:agent-inference on production-round-trip shape |concern:PM[1] mitigation list doesn't include preceding_text-per-tool_call reconstruction vector |action:ADR[4] revision recommended
BELIEF[IC5-max_tool_calls-truncation-UX-acceptable]: 0.40 |source:agent-inference |concern:synthetic stop_reason with no final text breaks autonomous-loop UX |action:recommend INV2 revision to force tools=None final call
BELIEF[IC2-parallel-tool_calls-invariant-obvious]: 0.50 |source:agent-inference |concern:IC[2] invariants don't document that multiple kind="tool_call" events per stream are valid |action:add INV4
BELIEF[IC5-assistant-msg-reconstruction-who-owns]: 0.55 |source:agent-inference on Provider-stateless invariant |concern:reconstruction responsibility unassigned between Provider + TurnEngine |action:recommend StreamEvent(kind="stop") carries final_message field
BELIEF[SQ-estimates-adjusted]: 0.75 |source:agent-inference on test-matrix + adapter complexity |concern:SQ7/SQ14a/SQ15/SQ23 under-estimated by 0.5-1.5h each |action:revise ests, +3h M1b total
BELIEF[test-direction-asymmetry-matters]: 0.80 |source:agent-inference on production data flow |concern:from_sdk(to_sdk)==msg weaker than direction-specific tests |action:SQ12d + SQ23 add inbound-direction fixtures

BELIEF[P(build-track-ready-post-R1)]: 0.70 |15 findings delivered to scratch, 11 require tech-architect R2 response |post-R2 + DA expected >0.85 for lock

## gate-log

[tech-architect 26.4.20]
  - §2a positioning: ALL 8 ADRs consensus with source plan; outcome 2 (acknowledged risks documented)
  - §2b calibration: precedents cited per ADR
  - §2c cost/complexity: justified per ADR for M1a/b scope
  - §2d source-provenance: [code-read clients.py] + [source-plan] + [agent-inference] + [independent-research] tags on all findings
  - §2e premise viability: H1-H7 viable, H5 adds revision hook for small-context providers
  - §2g dialectical-bootstrapping: DB[] on top-3 highest-conviction (ADR[1]+[3]+[4])
  - §2h XVERIFY: deferred to DA round — ADR[3] top-1 candidate; will trigger if DA challenges

[tech-architect R2 26.4.20]
  - §2a positioning R2: ADR[3] rationale re-anchored (N>3+observability not generic-SoC); ADR[4] escape-hatches locked in ADR proper; IC[2] expanded to 5-kind taxonomy per 4-agent convergence.
  - §2b calibration R2: LangChain AgentExecutor precedent acknowledged in DB re-run; autogen/crewai N>1 location-separation cited as compensating precedent.
  - §2c cost/complexity R2: +5.5h net SQ impact (M1a 14h→17.5h, M1b 18h→23.5h); justified per merge-gate rigor + 4-agent IC[2] convergence + PM-mandated coverage.
  - §2d source-provenance R2: every R2 response carries source tags; cross-agent references to impl-eng BC, cqa BC, ui-ux IC-flag, DA responses.
  - §2e premise viability R2: ADR[3] premise re-examined with stronger counter, holds on N>3 grounds. ADR[4] premise revised; escape-hatches lock fidelity.
  - §2g DB re-runs on ADR[3] + ADR[4] with stronger counters per DA[#1]; outcomes unchanged but reasoning genuine; BELIEF reduced to reflect honest residual uncertainty.
  - §2h XVERIFY[ADR3]: NOT-ATTEMPTED — infrastructure-blocked.
    ```
    XVERIFY[ADR3 tool-exec-loop-location]: NOT-ATTEMPTED — infrastructure-blocked
    reason: sigma-verify cross_verify + verify_finding hang pattern observed 3x this session (DA-r1, TA-r1, TA-r2). Per feedback/failures memory: cross_verify multi-provider fanout appears to block on slowest provider with no per-provider timeout.
    gap-status: documented, not silently ignored per §2h
    compensating-factor: ADR[3] has cross-agent consensus (tech-architect ADR3, impl-eng R1+R2 did NOT challenge ADR3 location, cqa EG1-EG5 tests state machine at this layer, ui-ux IC-flag[5] compatible with this layer); DB re-run with LangChain-AgentExecutor counter affirms ADR on N>3 grounds.
    remediation: post-C1 troubleshoot session to fix mcp__sigma-verify cross_verify timeout + per-provider partial-result return.
    ```
  - BC-responses delivered: impl-eng #15 R1 + #4 R2 delta; cqa #11 R1 + #5 EC + #4 R2 delta. All addressed; many folded into DA response structure above.
  - Convergence R2: P(plan-ready) 0.82 → 0.87 with XVERIFY gap documented.

[implementation-engineer 26.4.20]
  - §2a positioning: 1 CONSENSUS (ADR[1] purpose-built confirmed), 14 acknowledged-risk or clarify/revise against tech-architect findings. Outcome 2 for load-bearing challenges, outcome 3 (gap) for H2 Ollama-streaming-tool_use.
  - §2b calibration: ollama-mcp-bridge project precedent (code-read ollama_client.py:11-14 inline warning) + gh CLI issue #12557 actual-content vs claimed-content reconciliation + sigma-verify clients.py reference read in full.
  - §2c cost/complexity: 15 findings produce ~+3h M1b estimate revision + 1 new 0.25h SQ (SQ6c) + test matrix expansion (SQ12d+SQ23 inbound direction). Justified by hidden-complexity prevention.
  - §2d source-provenance: every BUILD-CHALLENGE finding tagged with source type and line references. External-verification used once (XVERIFY[openai:gpt-5.4] on H2-ollama).
  - §2e premise viability: H2 premise (Ollama /v1 streaming+tool_calls reliable) flagged as gap — unverified, requires empirical smoke test.
  - §2g dialectical-bootstrapping: DB[] on top-2 (H2-ollama + ADR4-direction-asymmetry). Both surface refinements, not rejections.
  - §2h XVERIFY: 1 call executed (openai:gpt-5.4 on H2), returned uncertain(low) — written as finding with XVERIFY tag per INV[§2h]. Recommendation: tech-architect ADR[3] XVERIFY triggered in DA round OR after SQ6c resolves (whichever is earlier).
  - BC[R1, impl-eng]: 15 findings |→ revise:5, clarify:8, accept:1, conditional:1 |ready for plan-track R2 response + DA round

## open-questions

(Original 8 OQs from tech-architect + ui-ux-engineer resolved 2026-04-20. Authoritative answers in ## user-decisions below.)

## user-decisions (locked 2026-04-20 by user — accepted all lead recommendations)

**#1 Q3 forward plan revision cadence (TA-2):** ~2 weeks. Revisit after M1a ships + before M1c scope locks. tech-architect R2 writes this as a scheduled checkpoint in Q3 forward plan.

**#2 devstral→deepseek escalation authority (TA-4):** (c)→(a). tech-architect R2 writes explicit escalation policy NOW (thresholds based on raw event capture from PM[2]); C2 impl-eng executes per policy without halting. User retains visibility via gate log.

**#3 Rendering option pin (UI-1):** DEFER to pre-M2 STEP-1 per ui-ux-engineer forward plan. M1a/b is rendering-option-agnostic (position_in_turn + preceding_text captured regardless). Note: #5 implies option (b) inline, which requires IC-flag[5] resolved in tech-architect R2 — already strongest 4-agent cross-agent convergence point, so likely accepted in R2.

**#4 Streamlit vs Textual TUI for v1 (UI-2):** 2h pre-M2 comparison sketch. TUI upgraded from source-plan "fallback only" to informed-choice via empirical evaluation. +2h pre-M2 scope. Decision is NOT pre-committed.

**#5 Research question pin (UI-3):** (a) **memory-invocation coherence**. Pins M3 metrics priority around query clustering + cross-model similarity + per-model tool-invocation rate on memory-specific queries. Narrows preamble-variant design + per-turn position capture fidelity in M1a/b.

**#6 A11Y[2] custom component scope (UI-4):** M2 gap, document. Revisit M3+ if shareability becomes a requirement. If #4 lands on TUI, this question moots (terminal-native A11Y).

**#7 Plan-track anchoring pre-check (process):** (a) trust DA. DA spawn prompt includes explicit H1-H7 all-consensus anchoring probe. No forced plan-track self-challenge before DA.

**#8 sigma-mem agent-scoped write-tool gap (infrastructure):** (A)+(C). Lead-proxy persistence at Step 33 — lead invokes `store_agent_memory` on behalf of each agent from scratch content with source attribution. Audit of impl-eng + ui-ux-eng patterns.md writes = NO CONTAMINATION (both wrote well-formed generalizable process patterns with project case studies as src — correct destination). Root-cause fix (permission exposure to agents) deferred to post-C1 update-config session.

## re-anchor (2026-04-20)

User directive: "The completed recipe is the goal. If we get a plan with a bunch of steps missed/side-stepped/etc before or after, we get pasta, not bolognese." Process integrity spans full lifecycle — pre-plan, plan-challenge, AND post-plan (promotion/archive/synthesis). Lead check at every phase boundary: "which step am I tempted to skip right now?" — that's the one that matters most. Persisted to sigma-mem patterns.md as !recipe-over-deliverable-pasta-metaphor 26.4.20.

## lead-flags-for-DA (Step 18 spawn)

1. **H1-H7 all-consensus anchoring probe.** tech-architect's independent analysis landed at 100% agreement with source plan's 7 hypotheses. Step 20 Circuit Breaker doesn't catch this (CB evaluates *challenger* silence, not plan-track source-alignment). DA must probe whether H1-H7 consensus is genuine post-stress-test convergence or subtle source-plan anchoring via §2a positioning check.

2. **Existing-pattern recall miss.** Two highly-relevant 26.4.16 patterns already in global memory: `P[ollama-openai-compat-drops-tool-calls-streaming]` + `P[streamlit-async-gen-supported-with-caveat]`. impl-eng landed on Ollama issue (#12557) independently via XVERIFY — agent would've saved time if direct recall surfaced existing pattern at boot. ui-ux-eng may have also had recall miss on Streamlit pattern. Not fatal but worth DA noting — may indicate recall-at-boot is not fully exercising existing memory.

3. **Cross-agent IC[2]/IC[5] convergence (4-agent).** impl-eng BC #2 + BC #3 + ui-ux-eng IC-flag[5] + cqa BC-cqa-11 EG1-EG5 — all 4 agents independently flagged overlapping gaps on event-grammar. Strongest convergence signal in build. DA should weight this heavily and probe whether tech-architect R2 can reject (answer: probably no without explicit test-coverage accommodation per cqa's ask).

4. **Contract contradiction (cqa).** IC[1] INV3 vs IC[2] error-convention — must lock IC[2] ALWAYS-emerge BEFORE parallel SQ6a/6b engineers in C2. Hard ordering constraint for tech-architect R2.

## promotion

**Lead-proxy persistence applied 2026-04-21** per user-decision #8 (sigma-mem agent-scoped write-tool gap). Agents could not call `store_agent_memory` / `store_team_pattern` / `store_team_decision` directly — lead invoked on their behalf with source attribution.

### auto-promote (executed by lead-proxy)

- **tech-architect** → auto-promote #2 to `~/.claude/teams/sigma-review/agents/tech-architect/memory.md`:
  - P[pro-forma-DB-bootstrap-detection|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:self-correction] — detection via DA §2a positioning audit; remediation via ALT-list counter rerun; validated in this build (ADR3 0.88→0.84, ADR4 0.80→0.70 honest drops)
  - P[XVERIFY-infra-gap-documentation|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:process] — template for §2h-compliant XVERIFY-FAIL documentation with compensating factors

- **ui-ux-engineer** → auto-promote #1 to `~/.claude/teams/sigma-review/agents/ui-ux-engineer/memory.md`:
  - P[gold-plating-code-vs-type-system-split|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:pattern] — when DA flags gold-plating on feature variants, distinguish code gold-plating from type-system scaffolding

- **implementation-engineer** → auto-promote #2 to `~/.claude/teams/sigma-review/agents/implementation-engineer/memory.md`:
  - P[3-tier-merge-gate-test-strategy|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:pattern] — hand-golden outbound + hand-golden inbound + round-trip derivative (catches symmetric-field-loss round-trip misses)
  - P[provider-statelessness-SDK-context-manager|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:pattern] — anthropic.MessageStreamManager + openai.AsyncStream within-call scope pattern

- **code-quality-analyst** → auto-promote #1 to `~/.claude/teams/sigma-review/agents/code-quality-analyst/memory.md`:
  - P[event-grammar-conformance-tests-EG|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:pattern] — EG1-EG5 test categories for streaming event APIs with tool-exec loops

- **devils-advocate** → auto-promote #2 to `~/.claude/teams/sigma-review/agents/devils-advocate/memory.md`:
  - P[DA-anti-sycophancy-exit-gate-self-audit|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:technique] — pre-PASS self-audit verification signals (BELIEF direction, resolution depth, infra-gap vs silent-skip, flag classification)
  - T[DA-cold-read-ordering-discipline|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:technique] — chunks a-e (findings) before chunk f (lead-flags) + chunked reads + time-box + mandatory boot-complete ping

### team-decision (executed by lead-proxy)

- `store_team_decision` → `~/.claude/teams/sigma-review/shared/decisions.md`:
  - Decision: sigma-chatroom M1a+M1b BUILD architectural commitments (purpose-built providers, native tool-use, TurnEngine tool-exec, IC[2] dual additions, 3-tier merge-gate, 60% context, raw capture default-on-when-unreliable, research-question=memory-invocation-coherence, rendering-deferred-pre-M2, Streamlit-vs-TUI-at-pre-M2-STEP-3b, manual-M1b-auto-M1c+-escalation)
  - Weight: primary
  - By: tech-architect + ui-ux-engineer + lead-user-decisions
  - Context: sigma-chatroom-m1ab C1 2026-04-20 to 2026-04-21; DA-r2 PASS A- rounds 2/5; XVERIFY documented gap; P=0.87

### team-pattern (executed by lead-proxy)

- `store_team_pattern` → `~/.claude/teams/sigma-review/shared/patterns.md`:
  - P[cross-agent-4-independent-convergence-validates-IC-revision|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:team-pattern] — when 4 agents independently flag overlapping gaps from different scoping perspectives, cross-agent convergence is itself strongest signal for IC revision. Validated against anchoring risk by DA-r2 matching 3/4 lead-flags + finding 1 new conflict.

### user-approve (none this build)

No new-principle / contradicts-global / behavior-change items surfaced. All promoted entries are auto-promote class (calibration/pattern/technique/process — cross-project applicable).

### infrastructure gap note

Root-cause fix (expose agent-scoped sigma-mem write tools to agent tool permissions) deferred to post-C1 session with update-config skill. Current lead-proxy path preserves outcome chain integrity but is not sustainable; next build should have agent self-persistence restored.

## archive-notes

Scratch archived 2026-04-21 to `~/.claude/teams/sigma-review/shared/archive/2026-04-20-sigma-chatroom-m1ab-workspace.md` (298KB). INDEX.md updated (build row appended). Plan file written LAST to `~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.plan.md` (37KB) — outcome chain complete: promotion → archive → plan file in that order.
