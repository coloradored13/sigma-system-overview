# C1-R3 scratch — BUILD: sigma-chatroom-m1ab
## status: archived-r3
## archived-date: 2026-04-21
## mode: BUILD-R3-revision
## trigger: sigma-evaluate grade C (2.5/4.0) — revise 3 high-leverage findings before C2

## meta
- spawned: 2026-04-21
- round: R3 (revision targeting eval findings)
- previous-rounds: R1 (challenge) + R2 (response) → PASS A- locked 2026-04-21
- eval-target: ~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.eval.md
- audit-target: ~/.claude/teams/sigma-review/shared/archive/2026-04-20-sigma-chatroom-m1ab-audit.md
- plan-file (current authoritative): ~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.plan.md
- archived-R1+R2-scratch: ~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab/c1-scratch.md (status: archived-c1)
- r3-directive: NO XVERIFY CALLS (hard stop — prior sessions hit cross_verify/verify_finding hangs 3x, plus this is a calibration+risk-matrix revision, not a new-claim verification)

## r3 scope — 3 high-leverage + secondary fixes

### High-leverage (must-resolve)
- **FIX[1]** ADR[2]/PM[5] Ollama /v1 streaming+tool_calls reframe from "exploratory risk PM[5] L=0.45" to "known-broken-unless-SQ6c-passes" with pre-computed FAIL branch estimate. ADR[2] BELIEF 0.95 → 0.70-0.75 conditional. Evaluator finding #1 (the killer).
- **FIX[2]** PM[3] expand with 3 missing risk categories: (a) tool-exec injection + argument smuggling security, (b) operational cost envelope (live-test default cap), (c) async-streaming DX (breakpoint debuggability, structured logging or replay harness escape hatch).
- **FIX[3]** UD#3 circular dependency cleanup: either decide rendering NOW (given UD#5 memory-invocation-coherence implies option-b inline) or restructure STEP-1 explicitly as a decision-point with empirical inputs listed (not a deferral).

### Secondary (address where tractable)
- **SEC[1]** Replace false-precision point estimates with ranges: ~41h → ~36-49h with coordination overhead explicit; 2-decimal BELIEF → ranges (0.80-0.85); collapse PM[5] 0.45 vs 0.40 false distinction.
- **SEC[2]** Carry-forward flag specificity: #1 cost-cap default ($5/session recommended), #2 session_id entropy source named (uuid4 or uuid7), #4 T1/T2/T3 missing-tag findings enumerated.
- **SEC[3]** Drop or primary-source the autogen/crewai "N>1 location-separation" precedent. If primary docs can't be produced in 5 min of research, drop as compensating evidence and accept the XVERIFY gap on weaker footing (4-agent consensus + DB re-run only).

### Meta-calibration
- **META[1]** Add directive: any ADR with BELIEF ≥0.85 must NOT have an SQ-level smoke test in the decomposition that could falsify it. Promote as new chain-evaluator check (post-C1, separate session).

## r3 section assignments (parallelizable — distinct file sections, no write conflicts)

### tech-architect-r4 (primary-owner of most fixes)
- FIX[1] ADR[2] BELIEF revision + PM[5] reframe + SQ6c-as-ADR-dependency
- FIX[2] PM[3] expand with 3 new categories (architecture-owned risks)
- FIX[3] UD#3 resolution (either pin or restructure STEP-1)
- SEC[1] BELIEF ranges on all load-bearing ADRs
- SEC[3] autogen/crewai precedent drop-or-source
- Write to: scratch ## plans → ### tech-architect-R3 section

### implementation-engineer-r4
- FIX[1] SQ6c-FAIL pre-computed branch — if Ollama /v1 + streaming + tool_calls broken, fallback SQ14b plan (ollama pypi AsyncClient +0.5h OR M1b Anthropic-only scope contraction). Recalc M1b estimate under each branch.
- SEC[1] SQ estimate ranges
- SEC[2] session_id entropy — name source (recommend uuid4 per standard practice or uuid7 for sortability)
- Write to: scratch ## plans → ### implementation-engineer-R3 section

### code-quality-analyst-r4
- FIX[2] PM[3] test impact — what tests address security/cost/DX risks? SQ additions or SQ revisions.
- SEC[2] cost-cap default for live tests — recommend value for `CHATROOM_MAX_SESSION_COST_USD` env var
- SEC[2] T1/T2/T3 missing-tag enumeration from prior-round findings
- Write to: scratch ## plans → ### code-quality-analyst-R3 section

### ui-ux-engineer-r4
- FIX[3] rendering-option recommendation given UD#5 memory-invocation-coherence and UD#4 TUI-vs-Streamlit pending
- Update forward-plan STEP-0-3b if rendering is pinned now (shrinks STEP-1 to confirmation, not decision)
- Write to: scratch ## plans → ### ui-ux-engineer-R3 section

### devils-advocate-r3 (R3 exit-gate — spawned AFTER plan-track R3 completes)
- R3 exit-gate verdict: did R3 actually fix the 3 high-leverage findings, or cosmetic?
- Anti-sycophancy self-audit — BELIEF changes should reflect real revision not lip service
- NO XVERIFY (hard stop)
- Verify META[1] directive (ADR BELIEF ≥0.85 no-smoke-test-dependency) is captured for post-C1
- Write to: scratch ## plans → ### devils-advocate-R3 section + ## r3 exit-gate verdict

## plans

### tech-architect-R3

#### FIX[1] — ADR[2] BELIEF revision + PM[5] reframe + SQ6c-as-ADR-dependency

**ADR[2] revised (replaces plan lines 119-125):**

> **ADR[2] — Native per-SDK tool-use; no text-convention, no ollama-mcp-bridge**
> - **Alternatives:** ALT1 text-convention regex, ALT2 ollama-mcp-bridge, ALT3 hybrid native+text-fallback
> - **Rationale:** Anthropic SDK emits `content_block_start/delta type="tool_use"` (structured, first-class). Ollama `/v1` OpenAI-compat emits `tool_calls` when instruction-tuned AND streaming-tool-calls works on the `/v1` path. Text-convention strictly worse WHERE native structure is actually delivered; where native structure is silently dropped, text-convention becomes a fallback rather than strictly inferior.
> - **Gap (LOAD-BEARING):** Ollama `/v1` streaming + tool_calls is documented-to-fail per Ollama docs + GitHub #12557 (issue scope was `/api/chat`, but the documentation pattern applies to the `/v1` OpenAI-compat layer). SQ6c smoke test is a VERIFICATION ATTEMPT, not exploratory discovery. The plan must pre-compute SQ6c-FAIL branch rather than trusting 0.95 confidence on unverified behavior.
> - **BELIEF:** **0.70-0.75** (**CONDITIONAL on SQ6c PASS**; drops to **0.55** on SQ6c FAIL with fallback to `ollama` pypi AsyncClient on `/api/chat` per impl-eng-R3 F1, OR M1b Anthropic-only scope contraction per F2)
> - **BELIEF dependency (explicit, in-ADR not separate-section):** this ADR's confidence is gated by SQ6c outcome, not ADR reasoning-strength alone. Downgrade recorded in the ADR itself.
> - **Prompted-by:** H2, C4
> - **Source:** `[source-plan C4]`, `[independent-research Anthropic content-block streaming — verified]`, `[primary-source-contradiction Ollama docs + GitHub #12557 on /v1+streaming+tool_calls — see PM[5]]`, `[code-read ollama-mcp-bridge warning]`

**PM[5] reframed (replaces plan lines 373-378):**

> **PM[5] — Ollama /v1 streaming + tool_calls documented-to-fail; blocks M1b Ollama tool-use unless SQ6c verification overrides docs**
> - **Likelihood:** **H (0.60-0.75)** — documentation pattern applies but devstral-specific `/v1` behavior in recent Ollama releases could surprise in either direction. Range honest about verification-attempt uncertainty rather than the earlier false ~0.45 "exploratory" framing.
> - **Reasoning:** Ollama documentation + GitHub #12557 indicate `tool_calls` silently dropped when streaming is enabled on the OpenAI-compat layer. **Documented-to-fail, NOT exploratory.** SQ6c is a verification attempt — if it passes, we accept that devstral-specific `/v1` behavior streams tool_calls despite documented pattern; if it fails, documented behavior confirmed.
> - **Detection:** SQ6c 15-min smoke test BEFORE SQ14b commits. Run against BOTH devstral-2:123b AND deepseek-v3.2:cloud.
> - **Mitigation (pre-computed FAIL branches; estimate deltas per impl-eng-R3 scratch):**
>   - **Primary (SQ6c PASS either model on /v1):** proceed with `openai` SDK AsyncStream + tool_calls; ADR[2] BELIEF 0.70-0.75; M1b ~23.5h baseline
>   - **Secondary (SQ6c FAIL all /v1 paths; pivot to F1 — `ollama` pypi `AsyncClient` on `/api/chat`):** SQ14b +0.5-1.5h rework; M1b **~24-25h**; ADR[2] BELIEF 0.55 under conditional, arguably *stronger* at 0.80-0.85 under F1 (two-path confirmation); scope preserved
>   - **Tertiary (F1 also fails — F2 emergency contraction):** M1b tool-use contracts to Anthropic-only; Ollama tool-use becomes M1c deliverable; M1b **~21-22h** (−1.5-2h net); ADR[2] BELIEF 0.55 (scope-contracted, core thesis unverified until M1c)
> - **Escalation trigger:** SQ6c results posted to plan file before SQ14b line-of-code; branch selection explicit in C2 build log.

**Net effect:** ADR[2] + PM[5] coherent — documented-to-fail reframing replaces exploratory-risk framing; SQ6c is verification-attempt not discovery; FAIL branches pre-computed with estimate deltas (aligned to impl-eng-R3 F1/F2). Addresses eval finding #1.

#### FIX[2] — PM[3] expansion (PM[6], PM[7], PM[8])

PM[3] itself stays as-is (it correctly covers async/state-machine). Three NEW risks close eval Weakness #3 (systematic gaps):

**PM[6] — Tool-exec injection / argument smuggling attack surface**
- **Likelihood:** **L-M (0.20-0.35)** for M1a/b research-instrument scope; **H (0.55+)** if ever routed to untrusted input at M4+ (when `web_search`, `calculator`, `code_exec` tools materialize)
- **Reasoning:** Tool-exec loop accepts `tool_name` (string) and `arguments` (dict) from SDK-parsed model output. Attack vectors:
  - (a) Malformed tool names — path traversal (`../../etc/passwd`), shell metacharacters, null bytes — exploitable if any future tool hands these to filesystem/subprocess without sanitization
  - (b) Malformed JSON arguments — nested-depth bombs, unicode homoglyphs, duplicate keys with parser-dependent behavior
  - (c) Oversized arguments — 10MB string in an `echo` tool exhausts memory/log storage
  - (d) Nested-object serialization exploits — pydantic model-loading edge cases
  - (e) Arguments that pass schema but exploit tool-specific semantics — deferred to tool-by-tool review; out of PM[6] scope
- **Detection:** SQ24 adds `T_INJ1-T_INJ5` new tests (handoff to code-quality-analyst-R3). Include: path-traversal tool name, 10MB argument string, deeply-nested dict (>100 levels), unicode-normalization collision in tool_name, schema-violating types in arguments.
- **Mitigation:**
  - IC[5] already defines `tool_arg_validator: Callable[[ToolSchema, dict], dict] | None` seam. **LOAD-BEARING — must default to a real validator in M1b, not `None`.**
  - **REVISION to carry-forward flag #3:** M1b ships with DEFAULT validator = `jsonschema.validate(arguments, schema=tool.parameters)` + `len(tool_name) <= 64` + `tool_name.isidentifier()` pre-check + `len(json.dumps(arguments)) <= 65536` size cap. Seam still accepts caller override for M3 sigma-mem-aware validator. Add `jsonschema ~= 4.0` to pyproject.
  - Tool name whitelist: registered tools only; no dynamic dispatch from model-provided name without registry lookup.
- **Escalation trigger:** any SQ24 T_INJ test fails → pause M1b, fix validator default, re-run suite before integration tests.

**PM[7] — Operational cost envelope for live tests**
- **Likelihood:** **M (0.30-0.45)** — moderate for budget incidents during C2/C3 build; rises with M1b tool-exec loops that can spiral on unbounded generation
- **Reasoning:** `tests/live/test_live_smoke_*.py` call Anthropic + Ollama cloud APIs. Without a session cap, an unbounded tool-exec loop (fencepost bug in max=5, max_tokens=2048 generation spiral, or flaky-test rerun cycle) could run up API cost silently. Opus-4 at 2048 output tokens ≈ $0.15/call; 100 calls during a debugging session = $15 silent burn.
- **Detection:** real-time cost tracking per live-test run. MetricsCollector already captures `tokens_in/out` — derive `cost_usd` from `ProviderSpec.price_per_mtok_{in,out}` aggregated per-session.
- **Mitigation:**
  - **`CHATROOM_MAX_SESSION_COST_USD` env var** with DEFAULT `5.0` (covers M1a 5-turn dual-model smoke × 3 reruns; cheap enough that a fencepost spiral trips before damage). Pins carry-forward flag #1.
  - `CHATROOM_LIVE_TESTS=1` gates live-test execution (M3-locked); cost cap enforces even when live tests approved.
  - `type="cost_summary"` JSONL record flushed on session close for post-hoc analysis.
- **Escalation trigger:** cap hit → abort session with structured `SessionCostExceeded` exception + cost-summary record flushed immediately (not only on orderly shutdown).
- **REVISION to carry-forward flag #1:** default value `$5.00` (was vague); implementation lands in M1a turn_engine via MetricsCollector hook, not deferred to M3.

**PM[8] — Async-streaming developer-experience (debuggability)**
- **Likelihood:** **M (0.30-0.45)** — moderate impact on build velocity, not correctness
- **Reasoning:** Async generators + tool-exec loop break standard breakpoint debugging:
  - (a) pdb breakpoints inside async-iterator body require `asyncio.run_until_complete` which many IDE integrations don't wire correctly
  - (b) Exceptions inside async generators lose stack frames when re-raised through `StreamEvent(kind="error")` convention
  - (c) Replay-a-failing-test hindered by async non-determinism unless raw-event capture is complete
  - (d) print-debugging interleaves with stdout token streaming, destroying signal
- **Detection:** dev feedback during C2 implementation; signal = >2h spent on a bug that would be 15min in sync code.
- **Mitigation (three complementary escape-hatches):**
  - **Structured logging on every StreamEvent emission** — `logger.debug` activated via `CHATROOM_TRACE_EVENTS=1`. Fields: `event.kind, event.stop_reason, tool_call_id, turn_id, speaker, elapsed_ms`. Textual event trace when breakpoints break. ~1h SQ add.
  - **Replay harness** — `scripts/replay_session.py <session.jsonl>` re-emits captured StreamEvents against a mock TurnEngine so you can pdb-walk policy/tool-exec logic without re-running live SDK calls. Builds on raw-capture sidecar already in ADR[6]. ~2h SQ add.
  - **Sync fallback** — `CHATROOM_DEBUG_SYNC=1` makes `Provider.stream()` collect events into a list and return synchronously for unit-test debugging. Test-fixture only, NOT production. ~0.5h SQ add.
- **Escalation trigger:** C2 build-track engineer reports >1 async-debugging blocker → escalate to lead for replay-harness priority bump (currently M1b tail; would move to M1b mid).
- **Scope note:** total ~3.5h SQ additions not in current M1b estimate. Feeds SEC[1] range expansion (~41h → ~40-50h).

**Net effect (FIX[2]):** three previously-unpriced risk categories (security, cost, DX) explicitly enumerated with quantified likelihoods, concrete mitigations, numeric defaults. Addresses eval Weakness #3.

#### FIX[3] — UD#3 circular dependency cleanup (Option A: pin rendering now)

**Decision: Option A — pin rendering option (b) inline-at-position_in_turn NOW.** Aligned with ui-ux-engineer-R3 who pinned option-b from UX perspective; this section covers architectural integrity of the pin.

**Architectural rationale (complementary to ui-ux's UX rationale):**

1. **ToolCallRecord schema (IC[3]) already sufficient for option-b** — `position_in_turn` (0-indexed) + `preceding_text` (50 chars) + `ts_started/completed` + `latency_ms` give inline rendering everything it needs. Field set was designed with inline-rendering as implicit assumption.
2. **ADR[4] escape-hatches preserve option-b across providers** — `Message.preceding_text_per_tool_call: list[str] | None` preserves Anthropic content-block ordering option-b depends on. Locked in ADR[4] R2. No new Message-shape changes needed.
3. **ADR[6] raw-event capture gives option-b a replay path** — inline rendering derived from raw events fully reproducible from JSONL sidecar when `tool_use_reliability != "reliable"`. Observability story holds.
4. **ui-ux flagged preceding_text 50-char collision risk** — acknowledged. Non-blocking for pin; if STEP-1 verification shows >5% collision rate, extend ToolCallRecord with `char_offset_in_turn: int` (1-line schema change, replay-back-compat trivial). Tracked as STEP-1 contingent revision.

**UD#3 revised (replaces plan line 412):**
> 3. **Rendering option (UI-1):** **PINNED to option (b) inline-at-position_in_turn** (R3 resolution). Rationale: UD#5 research question (memory-invocation coherence) requires position fidelity only option (b) preserves; framework-agnostic across Streamlit/TUI; ToolCallRecord schema already sufficient; ADR[4] escape-hatches preserve cross-provider ordering. Forward-plan STEP-1 reduces from "decide rendering" to "verify option (b) fidelity against empirical M1b JSONL data."

**Forward plan STEP-1 revision (replaces plan line 440):**
> - STEP-1: verify option (b) inline-at-position_in_turn renders 5-turn 2-model M1b JSONL fixture with position-fidelity ≥95% AND preceding_text reconstruction ≥95%. Reopen rendering decision ONLY if empirical data shows option (b) cannot deliver memory-invocation-coherence observability (e.g., tool calls cluster at position_in_turn=0 only, making inline≡appended, OR preceding_text systematically fails reconstruction). Otherwise proceed to STEP-2 with option (b) confirmed.

STEP-2/STEP-3/STEP-3b per ui-ux-engineer-R3 scratch section (aligned).

**Net effect (FIX[3]):** UD#3 no longer circular. STEP-1 is a confirmation checkpoint, not a decision-deferral. Forward plan self-consistent with UD#5. Addresses eval Scope Integrity circular-dependency finding.

#### SEC[1] — BELIEF ranges on load-bearing ADRs

2-decimal BELIEFs imply measurement precision ≤0.005 which is impossible for subjective probability elicitation. Ranges surface uncertainty honestly and address eval Calibration finding.

| ADR | OLD | NEW | Rationale |
|---|---|---|---|
| ADR[1] | 0.92 | **0.85-0.95** | purpose-built providers/, high-confidence; range reflects <20 LOC reuse estimate + sigma-verify evolution coupling |
| ADR[2] | 0.95 | **0.70-0.75 (conditional; 0.55 on SQ6c FAIL)** | per FIX[1] — dependency on SQ6c verification replaces overclaimed 0.95 |
| ADR[3] | 0.84 | **0.75-0.85** | XVERIFY gap compensated only by (4-agent consensus + DB re-run with LangChain counter); autogen/crewai DROPPED per SEC[3] narrows compensating-factors |
| ADR[4] | 0.70 | **0.60-0.75** | OpenAI-shaped canonical with escape-hatches; Gemini M1c+ fidelity uncertainty; wider range honest |
| ADR[5] | 0.85 | **0.75-0.90** | context-budget 60% + len//4; per-model drift unknown until M3 calibration |
| ADR[6] | 0.90 | **0.85-0.95** | raw-capture default-on; low-stakes config choice |
| ADR[7] | 0.95 | **0.90-0.98** | schema_version per-record + replay invariants; OpenTelemetry/Jaeger pattern well-validated |
| ADR[8] | 0.92 | **0.85-0.95** | streaming from day 1; TTFT + INV4/5 state-management solid |

**plan-belief P=0.87 → P=0.80-0.85** (range-aggregation; ADR[2] conditional is dominant downward drag; ADR[3] compensating-factors narrowing secondary). Still plan-ready (>0.75); range honestly calibrated.

**PM likelihood deduplication:** PM[5] 0.45 vs PM[2] 0.40 false-precision distinction resolved. PM[5] now 0.60-0.75 (reframed per FIX[1]); PM[2] stays M (0.40) point-estimate since it's different empirical risk (tool_calls formatting quality given schema-validity, not existence-of-tool_calls-at-all). Distinction is now real + range-separated.

#### SEC[3] — autogen/crewai precedent: DROPPED

**Decision: DROP autogen/crewai "N>1 location-separation" precedent from ADR[3] compensating factors.**

**Reasoning:**
- R3 directive prohibits XVERIFY (infra hang × 3 this session)
- 5-min web search budget insufficient to reliably primary-source the claim across autogen + crewai docs/GitHub without risk of citation-burning
- Evaluator already flagged as not-found in their search — independent validation of the problem
- Keeping a contested claim as "compensating evidence" for an XVERIFY gap compounds the evidence-quality problem rather than resolving it (anti-sycophancy calls for narrowing, not defending)
- Honest posture: drop claim; ADR[3] XVERIFY gap now rests on **(4-agent cross-agent consensus + DB re-run with real LangChain AgentExecutor counter)** — still defensible, narrower compensating-factors set

**ADR[3] rationale revision (replaces final sentence of plan line 129):**
> R2 DB re-run: LangChain AgentExecutor counter (Provider-owned loop industry mode for N=1 SDK) acknowledged; ADR defended on N>3 chatroom use-case + observability grounds. Single-SDK case would flip decision. **[R3: autogen/crewai N>1 location-separation precedent DROPPED — could not primary-source within search budget; rather than cite unverified precedent, honest posture accepts narrower compensating-factors set: 4-agent cross-agent consensus + DB re-run with LangChain AgentExecutor counter only.]**

**ADR[3] Source line revision (replaces plan line 133):**
> **Source:** `[source-plan H3]`, `[agent-inference]`, `[industry-pattern LangChain AgentExecutor — acknowledged counter, ADR defended on N>3 grounds]`

**Plan challenge summary revision (plan line 484 compensating factors):**
> Documented as §2h infra-gap with compensating factors: (a) 4-agent cross-agent consensus on ADR[3]; (b) DB re-run with real counter (LangChain AgentExecutor acknowledged as Provider-owned N=1 mode industry precedent). **[R3: (c) autogen/crewai precedent DROPPED; compensating-factors set narrowed to (a)+(b) only.]**

**BELIEF impact:** ADR[3] BELIEF narrowed in SEC[1] to 0.75-0.85 (was 0.84) reflects the narrowed compensating-factors set. Honest downward recalibration, not cosmetic.

#### Cross-references for lead distillation

Ordered application when lead distills R3 into plan file:
1. Replace plan lines 119-125 with revised ADR[2] (FIX[1])
2. Replace plan lines 373-378 with revised PM[5] (FIX[1])
3. Append PM[6], PM[7], PM[8] after plan line 379 (FIX[2])
4. Replace plan line 412 UD#3 with pinned rendering (FIX[3])
5. Replace plan line 440 STEP-1 with confirmation framing (FIX[3])
6. Update ADR BELIEFs with ranges in plan lines 116, 131, 144, 151, 157, 168, 175 (SEC[1]; ADR[2] already covered in step 1)
7. Update plan-belief P=0.87 → P=0.80-0.85 at plan line 13 (SEC[1])
8. Revise autogen/crewai clause in plan line 129 ADR[3] rationale (SEC[3])
9. Revise plan line 133 ADR[3] Source line (SEC[3])
10. Revise plan line 484 compensating factors (SEC[3])
11. Update carry-forward flag #1 plan line 491 with `$5.00` default (PM[7])
12. Update carry-forward flag #3 plan line 493 with jsonschema default validator + deps note (PM[6])

#### BELIEF[P(plan-ready)] post-R3

- OLD (R2 lock): **0.87** (point estimate)
- NEW (R3): **0.80-0.85** (range)
- Rationale: ADR[2] honest drop (conditional on SQ6c verification) + ADR[3] compensating-factors narrowed (autogen/crewai drop) + PM[3] expansion reveals previously-unpriced attack surface (security, cost, DX) + UD#3 decision pinned (positive, narrows forward-plan uncertainty). Net downward ~0.02-0.07. Still plan-ready (>0.75); range rather than point reflects SEC[1] calibration discipline.

#### Convergence

tech-architect-r4: ✓ R3-revisions-complete |FIX[1]:✓ (ADR[2] 0.70-0.75 conditional, PM[5] reframed H 0.60-0.75, pre-computed FAIL branches aligned w/ impl-eng F1/F2) |FIX[2]:✓ (PM[6] injection + PM[7] cost + PM[8] async-DX added) |FIX[3]:A (option-b pinned, aligned w/ ui-ux-engineer-R3) |SEC[1]:✓ (all 8 ADR BELIEFs now ranges; plan-belief 0.80-0.85) |SEC[3]:dropped (autogen/crewai; compensating-factors narrowed to (a)+(b)) |BELIEF[P(plan-ready)]:0.80-0.85 |→ ready-for-DA-R3

### implementation-engineer-R3

#### FIX[1] — SQ6c-FAIL pre-computed branch (canonical: F1)

**Reframe summary:** PM[5] reclassified from exploratory-risk (L=0.45, "we'll see") to gate-conditional with pre-computed branches. SQ6c is no longer a probabilistic hazard; it is a binary switch selecting one of two locked SQ14b plans. Plan commits to BOTH branches up-front; whichever SQ6c selects, M1b proceeds without re-planning.

**SQ6c-PASS branch (current plan estimates hold):**
- SQ14b (Ollama tool-use via `openai` SDK AsyncStream against Ollama /v1): ~2.0h
- M1b total: ~23.5h
- M1 grand (parallelized): ~40h (midpoint)
- Verification: both Anthropic + Ollama echo round-trip in live smoke
- `tool_use_reliability` for devstral: candidate for `"nominal"` or `"reliable"` depending on PM[2] escalation outcome
- ADR[2] BELIEF: 0.70-0.75 (conditional-on-SQ6c-PASS per R3 reframe; was unconditional 0.95)

**SQ6c-FAIL branch (canonical: F1 — pivot SQ14b to `ollama` pypi AsyncClient):**
- SQ14b (Ollama tool-use via `ollama.AsyncClient` instead of `openai.AsyncOpenAI`): ~2.5-3.5h (delta +0.5-1.5h vs PASS)
- Delta breakdown:
  - Add `ollama>=0.X` (or `uuid_utils` if bundled) to `pyproject.toml` deps (~0.1h)
  - Swap SQ6b (`ollama_client.py`) internal call from `openai.AsyncOpenAI(base_url=".../v1", api_key=...)` to `ollama.AsyncClient(host=..., headers={"Authorization": f"Bearer {key}"})` with `chat(stream=True, tools=[...])`; iterate async chunks; map chunk.message.tool_calls to canonical `StreamEvent(kind="tool_call")` (~0.5-1.0h)
  - Adjust SQ7 `message_mapping.py` Ollama path — native `/api/chat` wire shape is NOT OpenAI-identity; canonical→ollama adapter gains real work (no longer identity). This is the biggest delta: ~0.5-1.5h for the outbound+inbound mapping pair + fixture updates.
  - Re-run SQ6c smoke against native `/api/chat` streaming tool_calls to confirm pivot works (~0.1h)
  - SQ15 3-tier MERGE GATE fixtures for ollama-native branch: one additional tier-1/tier-2 hand-golden pair (~0.3h)
- M1b total under F1: **~24-25h** (+0.5-1.5h vs PASS)
- M1 grand under F1 (parallelized): **~40-42h**
- Verification: unchanged (both Anthropic + Ollama echo round-trip); wire protocol differs, canonical Message shape identical — IC[1-5] contracts unaffected
- ADR[2] BELIEF under F1: 0.80-0.85 (pivot absorbs the wire-protocol failure; core "native per-SDK tool-use" thesis intact — arguably *stronger* evidence, since we've exercised TWO Ollama paths)

**F2 (alternative, NOT canonical) — scope-contract M1b to Anthropic-only tool-use:**
- SQ14b removed from M1b entirely (defer to M1c); SQ6c still runs as diagnostic but does not block
- SQ22 (per-SDK tool-use tests): Ollama tests dropped; Anthropic-only
- SQ15 3-tier MERGE GATE: Anthropic-only
- M1b verification criterion weakens to: "≥1 echo round-trip for Anthropic; Ollama tool-use documented as M1c scope"
- M1b total under F2: ~21-22h (-1.5-2h vs PASS)
- M1 grand under F2 (parallelized): ~38-39h
- **Research-instrument value lost under F2:** M1b's whole point is proving the per-SDK tool-use adapter layer (plural SDKs, divergent wire shapes). Anthropic-only collapses this to single-SDK and leaves ADR[2] core thesis (native per-SDK across 2+ SDKs) unverified until M1c. F2 defers that discovery by ~1-2 weeks and silently promotes M1c from "clone to other SDKs" into the de-facto cross-SDK integration milestone.

**Canonical decision: F1.**

**Rationale:**
- (a) **Ollama pypi AsyncClient maturity.** The `ollama` Python package supports `AsyncClient.chat(stream=True, tools=[...])` with streaming tool_calls as a first-class capability — this is the vendor-canonical path, not an /v1 shim on top of an OpenAI-compat layer. Ollama's own streaming-tool-calls blog post, the ollama-python GitHub README, and the deepwiki function-calling + streaming-responses pages all document `AsyncClient` + `tools=` + `stream=True` compose cleanly. Maturity risk for F1 is LOW (web-search 2026-04-20 research-window, NO XVERIFY per R3 directive).
- (b) **Research-instrument value preserved.** F2 erases the primary reason M1b exists as a milestone separate from M1c. It converts M1b into "Anthropic tool-use + a waiting room" and pushes the actual per-SDK convergence test to M1c, making M1c the load-bearing integration milestone. The +0.5-1.5h cost of F1 is ~3-5% of M1b and directly preserves the milestone's analytical purpose.
- (c) **Failure-mode containment.** F1 limits blast radius of SQ6c failure to `providers/ollama_client.py` internals + `message_mapping.py` Ollama path. IC[1-5] contracts unchanged (Provider Protocol is SDK-agnostic by design). F2 changes the M1b verification criterion, rippling into Q3 forward plan (M1c scope expands, M2 pre-gate assumptions shift).
- (d) **Escalation retained.** If F1 also fails (Ollama `/api/chat` streaming tool_calls broken on BOTH devstral + deepseek), THEN F2 becomes the emergency fallback. Decision tree: SQ6c /v1 PASS → current plan; SQ6c /v1 FAIL → F1 pivot → re-run smoke on `/api/chat` → if pass, proceed under F1; if fail, F2 emergency contraction.

**ADR[2] BELIEF revision (load-bearing for FIX[1]):**
- Unconditional (pre-R3): 0.95 (treated SQ6c-PASS as near-certain — this was the killer)
- Conditional-on-PASS: 0.70-0.75 (honest acknowledgement that plan is conditional on a test not yet run)
- Conditional-on-F1-pivot: 0.80-0.85 (lower ceiling because a second smoke result is needed; but core thesis preserved — arguably reinforced by surviving wire-protocol divergence)
- Conditional-on-F2-emergency: 0.45-0.55 (M1b research-instrument value substantially reduced)
- **Recommend:** plan documents all three conditional BELIEFs; primary plan operates under PASS BELIEF 0.70-0.75 until SQ6c runs in C2.

**Carry-forward to C2:**
- C2 must run SQ6c as first live-test action after SQ1-5 land. Before SQ14b commits a line of Ollama tool-use code, smoke result determines branch.
- If F1 selected: `ollama>=0.X` dep added to `pyproject.toml` before SQ14b; `providers/ollama_client.py` either (a) refactored to accept `client: "openai" | "ollama"` internal switch OR (b) split keeping IC[1] surface identical. Recommend (a) — single file with an internal `_StreamAdapter` subtype — lower LOC churn and preserves the roster.py seam.

---

#### SEC[1] — SQ estimate ranges (replace false-precision point values)

**Current plan (point estimates, R2):**
- M1a: ~17.5h parallelized
- M1b: ~23.5h parallelized
- Grand: ~41h parallelized

**R3 revision (ranges with explicit coordination overhead + PASS/FAIL branching):**

| Scope | Coordinated (two impl-engs, shared inbox, tight handoffs) | Stop-start (single impl-eng OR degraded coordination) |
|---|---|---|
| **M1a** | 16-20h | 20-26h |
| **M1b SQ6c-PASS** | 22-26h | 26-32h |
| **M1b SQ6c-FAIL (F1)** | 23-28h | 27-34h |
| **M1b SQ6c-FAIL (F2)** | 20-24h | 24-30h |
| **Grand M1a+M1b PASS** | 38-46h | 46-58h |
| **Grand M1a+M1b FAIL-F1** | 39-48h | 47-60h |
| **Grand M1a+M1b FAIL-F2** | 36-44h | 44-56h |

**Range derivation:**
- **Lower bound** = current R2 point estimate (assumes no rework, clean parallelization, no idle waits on SQ6a/SQ6b integration, no 3-tier MERGE GATE failures requiring re-fix)
- **Upper bound (coordinated)** = +15-20% over lower, absorbing: one SQ6c smoke re-run, one 3-tier MERGE GATE fixture re-cut (PM[1] trigger but no escalation), one async-state bug caught in SQ24 (PM[3] single-instance, no re-scope)
- **Upper bound (stop-start)** = +30-50% over lower, absorbing: single-impl-eng serialization of SQ6a+SQ6b (loses parallelization gain), one PM[2]/PM[3] escalation requiring re-scope, sigma-verify XVERIFY retry costs (PM[4])
- **Coordination overhead (explicit)**: ~2-3h for impl-eng ↔ impl-eng shared-fixture handoffs (SQ6a/SQ6b test_mock_providers cross-fixture naming + SQ14a/SQ14b schema-adapter contract-test alignment). This overhead IS spent under coordinated mode. It is NOT saved under stop-start — instead, stop-start loses the parallelization gain entirely, which is a larger cost.

**Collapse PM[5] 0.45 vs 0.40 false distinction:**
- R3 reframe makes PM[5] no longer a pre-mortem likelihood (a probability-of-something-bad) — it is a pre-computed branch selector (a plan variant). The likelihood of SQ6c-FAIL is *still* ~0.40-0.50 empirically, but plan behavior does not depend on where in that range the true value lies.
- **Recommend:** move PM[5] out of the likelihood-weighted pre-mortem table and into a new "Conditional Plan Branches" section. Leaves PM[] table reserved for real risks (PM[1-4] + PM[3]-expansion-from-FIX[2]).

---

#### SEC[2] — session_id entropy source (recommend uuid7)

**Current plan (carry-forward flag #2):** "session_id collision handling — currently defaults to timestamp; may collide under rapid session creation."

**R3 revision:** name the entropy source and its collision properties.

**Option A — uuid4 (baseline, safest):**
- 122 bits random (RFC 4122 v4)
- Collision probability after 1 billion ids: ~10⁻¹⁹ (cryptographic-grade safety)
- No coordination, no ordering
- Python: `uuid.uuid4().hex` or `str(uuid.uuid4())`
- Cost: zero — stdlib, synchronous, no deps
- Trade-off: session list in filesystem (`sessions/<uuid>.jsonl`) sorts lexicographically by random hash, NOT by creation time. Requires reading file mtime OR parsing session_header `ts` field for chronological listing.

**Option B — uuid7 (recommended):**
- 48-bit Unix-ms timestamp prefix + 74 bits random (RFC 9562, finalized 2024)
- Collision safety equivalent to uuid4 at practical scales (74 random bits → birthday collision at ~2³⁷ ≈ 137 billion ids)
- Lexicographically sortable by creation time — `ls sessions/` gives chronological order natively
- Python: `uuid_utils` package (pure-Rust impl, ~50KB) OR Python 3.14+ stdlib `uuid.uuid7()`
- Cost: +1 dep (or Python 3.14 requirement) — minor
- Trade-off: extra dep OR min-Python bump

**Option C — timestamp + 4-char nonce (weaker, NOT recommended):**
- e.g., `20260420T143022_a7f3` (ISO-8601 compact + 4 hex chars)
- Collision probability under rapid creation: birthday collision at ~256 ids/second (4 hex chars = 16 bits random)
- Cheap + human-readable BUT the existing problem (timestamp collision under rapid creation) is barely improved
- Use only if human-readability of filenames is a hard requirement — it is not, per current plan

**Recommendation: uuid7**

**Rationale:**
- (a) **M2 session-list UI needs chronological ordering.** Plan line 446 explicitly scopes "session list + resume" in M2c. uuid7 gives this natively via filesystem sort; uuid4 requires an extra mtime/header-parse step per session during list rendering (more M2 code + latent performance trap at scale).
- (b) **M3 metrics benefit from time-ordering.** Plan M3 ("3-model autonomous session with real sigma_mem_recall" + metrics panel around memory-invocation coherence) benefits from sessions being naturally time-ordered for cross-session analytics queries.
- (c) **Collision safety equivalent to uuid4** at any practical M1-M4 scale (single-user research instrument; <10K sessions ever).
- (d) **Dep cost small** — single package (`uuid_utils` preferred) added to pyproject; or bump min-Python to 3.14 (available since 2024-10) to use stdlib.

**Fallback:** if user prefers zero-dep + Python-version-agnostic, fallback to uuid4 and accept the M2 list-ordering cost. Reasonable alternative; uuid7 is the stronger forward-looking choice given M2+ plan.

**C2 implementation:**
```python
# uuid7 via uuid_utils (recommended):
from uuid_utils import uuid7
session_id = str(uuid7())  # e.g., "018f3a5e-d3c4-7abc-9d0e-1234567890ab"

# uuid7 via stdlib (Python 3.14+):
from uuid import uuid7
session_id = str(uuid7())

# fallback uuid4:
from uuid import uuid4
session_id = str(uuid4())
```

File path construction unchanged: `sessions/{session_id}.jsonl`. Update carry-forward flag #2 text to reference chosen entropy source + cite RFC.

---

#### R3 convergence

`implementation-engineer-r4: ✓ R3-delta-complete |FIX[1]:branch-F1-chosen |SEC[1]:range-estimates-done |SEC[2]:entropy-uuid7-recommended |M1a-range:16-20h(coord)/20-26h(stop-start) |M1b-PASS:22-26h(coord) |M1b-FAIL-F1:23-28h(coord) |M1b-FAIL-F2:20-24h(coord) |Grand-PASS:38-46h(coord)/46-58h(stop-start) |ADR[2]-BELIEF:0.70-0.75(cond-PASS)/0.80-0.85(F1)/0.45-0.55(F2) |→ ready-for-DA-R3`

### code-quality-analyst-R3

!scope: R3-narrow test-strategy-expansion for FIX[2] PM[3] new categories (security/cost/DX) + SEC[2] cost-cap default + SEC[2] T1/T2/T3 enumeration. NO XVERIFY. R1+R2 test strategy locked.

---

#### FIX[2] PM[3] test impact — new SQs + invariant additions

!context: tech-architect-r4 adds 3 new PM categories (ref workspace §tech-architect-R3: PM[6] injection, PM[7] cost, PM[8] async-DX). Each needs test coverage. All new SQs target M1b test cluster G (tool-use test cluster), gate with MERGE-GATE rigor (not SHOULD).

---

**SQ29 — test_tool_exec_injection.py — security (PM[6]) (~1-1.5h)**
coverage:**L (absent in R1+R2)** |load-bearing:YES
owner: code-quality-analyst
deps: SQ16 (tool-exec loop) + IC[5] tool_arg_validator seam
gate: MERGE-GATE (MUST before M1b ships first tool with real args — NOT echo)

test matrix (MUST all; converges with tech-architect T_INJ1-T_INJ5 R3 handoff line 108):
  I1→ **tool_name path-traversal.** Model emits `{"name": "../../../etc/passwd", ...}`. Assert: tool-name rejection via schema-whitelist (tool_name ∈ registered ToolSchema.name set) → StreamEvent(kind="error") + ToolCallRecord.error="unknown_tool". ¬fallthrough to os.path lookups.
  I2→ **tool_name shell-metachars + null-byte.** `{"name": "echo; rm -rf /", ...}` + `{"name": "echo\x00cat", ...}`. Must hit whitelist rejection, never reach exec. (T_INJ1 path-traversal + unicode-normalization collision per T_INJ4 covered here + I6.)
  I3→ **oversized arguments (T_INJ2).** `{"name": "echo", "arguments": {"msg": "A" * 10_000_000}}`. Must reject via `tool_arg_validator` size-cap (recommend 64KB per-arg, 256KB total per-call). Assert: ToolCallRecord.error="args_too_large" + StreamEvent(kind="error"). 10MB arg ¬appended to canonical Message (memory-bomb prevention).
  I4→ **deeply-nested JSON arguments (T_INJ3, >100 levels).** `{"a": {"b": {"c": ... 1000 deep ...}}}`. Must reject via max-depth validator (recommend 32 levels). CPython default recursion limit ~1000; below that, but JSON-schema validators can stack-overflow on cycles.
  I5→ **circular references / self-referencing dicts.** Since JSON cannot natively represent cycles, this is a post-parse mutation risk. If tool impl mutates input dict to create a cycle and returns reference → JSONL serialization fails. Assert: `json.dumps(record)` ¬raises `ValueError: Circular reference detected`; if tool mutates, either deep-copy before execution or reject.
  I6→ **unicode-normalization collision in tool_name (T_INJ4).** Lone-surrogate `"\udcff"` + NFC/NFD variants of `"echo"` (e.g. `e + ◌̀ vs è`). Must normalize-then-match via NFC before whitelist lookup OR reject non-NFC names. ¬silent bypass of whitelist via visual-homoglyph.
  I7→ **schema-violating types in arguments (T_INJ5).** Tool declares `{"type": "object", "properties": {"msg": {"type": "string"}}}`; model emits `{"msg": {"type": "evil_payload"}}` (dict instead of string). `tool_arg_validator` must reject BEFORE dispatch. Test: jsonschema.validate raises → ToolCallRecord.error="schema_violation".
  I8→ **rejection reason ROUND-TRIPPED through ToolCallRecord.** Every rejection case above → assert ToolCallRecord.error ∈ {unknown_tool, args_too_large, depth_exceeded, non_utf8, schema_violation} (enumerated set, not free-text). Closed-set error taxonomy enables M3+ metrics aggregation.

invariant additions to IC[3] ToolCallRecord:
  INV-TCR-1 (R3-NEW): `error` field uses closed-set taxonomy for rejection cases: `{unknown_tool, args_too_large, depth_exceeded, non_utf8, schema_violation, exec_exception, timeout}`. Free-text fallback allowed ONLY for unanticipated categories (prefix "uncategorized:").
  INV-TCR-2 (R3-NEW): `arguments` field in rejected ToolCallRecord contains the RAW (invalid) args as received, capped at 4KB for post-hoc analysis. Oversized args replaced with `{"__truncated__": true, "__original_size__": N}`.

invariant addition to IC[5] TurnEngine:
  INV-TE-5 (R3-NEW): `tool_arg_validator` callable MUST be invoked before tool-dispatch for every tool_call when tools list is non-empty. If `None`, TurnEngine uses default-noop (M1b contract; M3 retrofits strict validator). Null validator ≠ absent validation — position_in_turn records reason_validated="noop-default". Aligns with impl-eng-R3 recommendation (jsonschema default validator per carry-forward #3).

estimate: **1.5h** (8 cases × 10min + invariant integration + fixture-file + docstring). Top end given schema-validation integration.
→ revise |source:[tech-architect-R3 PM[6] + T_INJ1-T_INJ5 handoff L108 + IC[5] tool_arg_validator seam R1] + [agent-inference] + [pattern: OWASP ASVS V5 input validation] + [independent-research JSON-schema library behavior]

---

**SQ30 — test_cost_cap.py — cost envelope (PM[7]) (~0.5h)**
coverage:**L (absent)** |load-bearing:YES
owner: code-quality-analyst
deps: SQ20 (MetricsCollector) + cost-cap abort path in TurnEngine
gate: integrate with existing live-test dual-flag gate (CHATROOM_LIVE_TESTS=1 + env keys). M1b-mandatory.

test matrix:
  CC1→ **Mock tool-exec runs up estimated cost above cap.** Mock provider yields 3 tool_calls with large mock-args; mock tool returns large mock-result. MetricsCollector.record_tool_call sums estimated tokens × per-model rate. Assert: when cumulative estimated cost >= CHATROOM_MAX_SESSION_COST_USD, TurnEngine emits StreamEvent(kind="error", error=CostCapExceededError), final stop_reason="cost_cap_exceeded" (new taxonomy member), session JSONL closed cleanly.
  CC2→ **Env-var override.** `CHATROOM_MAX_SESSION_COST_USD=0.10` → cap fires earlier. `CHATROOM_MAX_SESSION_COST_USD=0` → disables cap (research-instrument escape hatch). Assert parsing: invalid values (negative, non-numeric) → raise at session-start, not mid-session.
  CC3→ **Structured abort path carries partial transcript.** When cap fires mid-turn, JSONL contains ALL prior turns + partial turn record with stop_reason="cost_cap_exceeded" + cost_at_abort + tokens_at_abort fields. Replay must reconstruct exactly what was written. IC[7] record-type addition needed.
  CC4→ **Cost estimator accuracy proxy.** Since M1a/b uses `len(text)//4` (ADR[5]), assert cost estimate is WITHIN ±20% of sum-of-reported-input-tokens × per-model-rate when reported tokens available. Calibrated by ADR[5] drift envelope.

invariant additions:
  INV-stop-reason (R3-NEW): stop_reason taxonomy gains `cost_cap_exceeded`. IC[2] INV2 updated to 7-member enum.
  INV-MC-1 (R3-NEW): MetricsCollector.record_tool_call MUST emit running-cost estimate on every call. TurnEngine subscribes to running-cost event, aborts when threshold crossed (push-based, not poll-based — prevents race where 10 parallel tool_calls each individually below cap but cumulatively far over).

estimate: **0.5h** (4 cases, mock-based, no live API).
→ revise |source:[tech-architect-R3 PM[7] + SEC[2] carry-forward #1] + [agent-inference] + [pattern: OWASP ASVS V11.1.3 resource limits]

---

**SQ31 — test_stream_logging.py — async-streaming DX (PM[8]) (~0.5h)**
coverage:**L (absent)** |load-bearing:PARTIAL
owner: code-quality-analyst
deps: SQ16 + ADR[6] raw-capture
gate: MUST for M1b; log-schema lock prevents v1→v2 breaking change in M3 metrics panel.

test matrix:
  L1→ **Every StreamEvent emission logs structured record.** Hook Python logging at DEBUG via `chatroom.stream` logger. For a fixture session, assert N log records with fields `{session_id, turn_id, speaker, kind, ts_iso, seq_in_turn}`. N ≥ tokens_emitted + tool_calls + tool_results + stops.
  L2→ **Log schema stability.** Assert logged-record keys == locked set (CI-comparable). Adding a new field later requires bumping log_schema_version. Prevents M3 panel breaking.
  L3→ **Log level gating.** DEBUG emits every token; INFO emits only kind∈{tool_call, tool_result, stop, error}; WARNING emits only error. Verifies operator tuning for production vs research.
  L4→ **No PII leak in default log.** Assert no text content logged at INFO (only metadata). DEBUG MAY include text. Feedback-memory context-firewall-career-leak 26.4.8 precedent.

estimate: **0.5h** (4 cases, in-memory log capture via `caplog` fixture).
→ revise |source:[tech-architect-R3 PM[8] + feedback-memory context-firewall 26.4.8] + [agent-inference] + [pattern: structlog / Python logging best practice]

---

**SQ32 — test_replay_harness.py — async-streaming DX (PM[8]) (~1h)**
coverage:**L (absent)** |load-bearing:YES (DX escape hatch + M2+ enabler)
owner: code-quality-analyst
deps: SQ10 (persistence) + ADR[7] replay invariants + SQ16

issue: ADR[6] captures raw events default-on for unreliable providers; ADR[7] defines replay invariants; but no test asserts REPLAY produces events structurally identical to LIVE. Without this test, raw-capture is a write-only feature — ¬debuggable. Addresses PM[8] breakpoint-debuggability risk directly.

test matrix:
  R1→ **Record-replay identity for text-only session.** Record 3-turn M1a session (mock providers) to JSONL. Replay JSONL via new `replay_events(jsonl_path)` AsyncIterator. Assert: stream of replayed StreamEvents structurally identical to recorded (token kinds + text + stop_reasons + sequencing). Byte-for-byte equality on event fields except timestamps (normalized).
  R2→ **Replay with tool-exec.** Record M1b session with ≥1 tool_call round-trip. Replay produces identical StreamEvent sequence INCLUDING synthetic kind="tool_result" events that TurnEngine (not Provider) emitted. Raw-sidecar events correlated by tool_call_id.
  R3→ **Replay tolerates partial-flush.** Truncate last 20 bytes of JSONL. Assert: replay consumes up to last valid record + emits final kind="error" event (¬raise across boundary, per IC[2] INV1). ADR[7] INV-replay-1 wired.
  R4→ **Replay rejects schema_version mismatch.** Hand-craft JSONL with schema_version="2". Assert: replay raises `SchemaVersionMismatch` with actionable message on FIRST non-matching record (¬silently downgrades). ADR[7] INV-replay-4 wired.
  R5→ **Replay harness CLI.** New `python -m sigma_chatroom.replay <session_id>` dumps text events to stdout matching CLI format. DX: operator can `diff <(replay sess1) <(replay sess2)` for behavioral comparison across runs. Minimal — no fancy UI, just text dump.

invariant additions:
  INV-replay-5 (R3-NEW): `replay_events()` MUST be an AsyncIterator matching Provider.stream() interface shape (StreamEvent yield). Enables M2 UI to consume live OR replayed identically.
  INV-replay-6 (R3-NEW): session_header ts_written and ts_replayed distinguished; replayed events carry both in their raw dict. Prevents metric-collector double-counting when replaying historical sessions during M3 analysis.

estimate: **1h** (5 cases, primarily fixture-driven).
→ revise |source:[tech-architect-R3 PM[8] + ADR[6] + ADR[7]] + [agent-inference] + [pattern: event-sourcing replay harness — Kafka + Jaeger]

---

**FIX[2] SQ total impact:** SQ29 (1.5h) + SQ30 (0.5h) + SQ31 (0.5h) + SQ32 (1h) = **+3.5h to M1b test cluster G**. With impl-eng-R3 ranges (Grand-PASS 38-46h coord), R3-expanded total: **~41.5-49.5h coord (PASS branch)**. Delta justified by PM[6/7/8] expansion + empirical-gate rigor from F1-build-patterns memory (26.4.8).

**Coverage matrix PM[6/7/8] → tests:**
- PM[6] injection → SQ29 (I1-I8 + IC[3] invariants + IC[5] INV-TE-5)
- PM[7] cost → SQ30 (CC1-CC4 + IC[2] stop_reason expand + MetricsCollector invariant)
- PM[8] async-DX → SQ31 (L1-L4 structured logging) + SQ32 (R1-R5 replay harness)

---

#### SEC[2] — cost-cap default value recommendation

**Recommendation: `CHATROOM_MAX_SESSION_COST_USD=5.00` as default.**

Calculation:
- Anthropic claude-opus-4-7: input ~$15/Mtok, output ~$75/Mtok
- Ollama cloud devstral-2:123b-cloud: ~$0.50-1.50/Mtok blended (best estimate; no published rate card — T3-prompt-claim, flag for verification in M1b live-smoke)
- Nominal M1a/b 5-turn session × 2 models × ~2000 tokens/turn:
  - Claude: 5 × 2000 × ($15 input + $75 output)/2 × 1e-6 ≈ $0.45 per test
  - Ollama: 5 × 2000 × $1.00/2 × 1e-6 ≈ $0.01 per test
  - **Total ≈ $0.50 per nominal 5-turn live-smoke run**
- $5 cap = 10× nominal → catches runaway tool-loops (tool-exec-loop bug re-invoking provider repeatedly) well before budget impact
- $5 cap = ~10 nominal runs worth — session would have to go catastrophically wrong to hit

**Floor / override guidance (documented in C2 README):**
- `CHATROOM_MAX_SESSION_COST_USD=0.50` (tight): CI smoke tests, nominal-only
- `CHATROOM_MAX_SESSION_COST_USD=5.00` (default): dev runs, research sessions
- `CHATROOM_MAX_SESSION_COST_USD=25.00` (loose): M3+ multi-hour sessions with sigma-mem recall loops
- `CHATROOM_MAX_SESSION_COST_USD=0` (disabled): research-instrument escape hatch; user assumes cost responsibility

**Carry-forward to C2:** env-var validation at session-start (SQ30 CC2 asserts this). Invalid values raise before first API call — fail-closed, not fail-open. Aligns with tech-architect-R3 carry-forward #1 plan-file L491 update.

→ revise |source:[tech-architect-R3 carry-forward update #1 + SEC[2] carry-forward #1 + Anthropic public rate card] + [T3-prompt-claim Ollama cloud rates pending M1b empirical] + [agent-inference nominal session size]

---

#### SEC[2] — T1/T2/T3 missing-tag enumeration (bounded top-8 load-bearing cqa findings)

!scope: top 8 cqa R1+R2 findings by load-bearing weight (coverage=L + load-bearing:YES). Enumeration format: finding-ref | current-tag | proposed-tier. Per R1 DA (L2328) + R2 DA (L2409+L2433) minor gap.

**Tier definitions (per ΣComm rosetta + sigma-review analytical-hygiene §2d):**
- **T1** = primary external source (SDK docs, RFC, W3C spec, vendor API reference, peer-reviewed literature, source code of the verified lib)
- **T2** = cross-agent convergence / agent-inference on SDK behavior / industry pattern citation
- **T3** = prompt-claim (user-provided context, plan-file assertion, unverified training-data recall)

| finding-ref | current-tag(s) | proposed-tier | rationale |
|---|---|---|---|
| BC-cqa-1 F1-F8 (message_mapping fixtures) | [code-read plan-track ADR[4]+PM[1]] + [agent-inference] + [independent-research Anthropic SDK tool_use content-blocks] + [cross-agent impl-eng BC#14] | **T1 for F2+F4 (Anthropic content-block behavior verifiable in SDK docs); T2 for F1+F3+F5+F6+F7+F8** | F2/F4 grounded in Anthropic SDK ref (primary); F6 malformed-JSON is empirical-only (T2 pending M1b); F8 cache_control is forward-compat (T2 agent-inference) |
| BC-cqa-2 G1+G2 (mock fidelity) | [code-read IC[2]+IC[5]] + [agent-inference] + [independent-research Anthropic+OpenAI SDK streaming] | **T1 for G1 (Anthropic SSE event sequence is published API ref); T2 for G2 (Ollama /v1 OpenAI-compat chunk accumulation inferred from OpenAI stream docs applied to Ollama — cross-inference not primary)** | G2 is exactly the SQ6c smoke-test question; tier honesty matters here — don't claim T1 |
| BC-cqa-3 T1-T9 (TurnEngine state-machine) | [code-read IC[5]+PM[3]+ToolCallRecord INV1/INV2] + [agent-inference] + [pattern: pytest-asyncio async-gen cleanup] | **T2** (all cases; IC[5]/PM[3] are plan-internal, not external primary) | Load-bearing but tier is honestly T2 — no external spec mandates these cases; they're agent-inferred from plan contracts |
| BC-cqa-4 J1-J5 (JSONL persistence) | [code-read ADR[7]+IC[3]+IC[7]] + [agent-inference] + [cross-agent impl-eng BC#10] | **T2** (all cases) | Replay-invariant contracts are internal; no external spec; T2 correct |
| BC-cqa-6 live-smoke (SQ12i/SQ28) | [code-read source-plan verification] + [cross-agent feedback 26.4.5 + impl-eng SQ6c complementary] | **T2 with T3-origin** | Justification traces to feedback-memory 26.4.5 (T3-prompt-claim per sigma-review hygiene: memory-sourced ≠ T1 external) + cross-agent T2 |
| BC-cqa-7 IC[1] INV3 contradiction | [cross-inference on plan-file text] | **T3** (plan-internal contradiction — no external authority) | Tier is T3 BUT the finding is TRIVIALLY verifiable (read plan-file); tier ≠ weight. Accepted despite T3 per DA[#8] response |
| BC-cqa-9 style gates (Q1-Q5) | [pattern: Python-ecosystem convention] + [agent-inference] | **T1 for Q1+Q4+Q5 (pyright/ruff/black are published tools with docs); T2 for Q2+Q3 (pydocstyle scope + naming conventions are project-policy choices)** | Tooling-cite gets T1; policy-choice remains T2 |
| BC-cqa-11 EG1-EG5 event-grammar suite | [cross-agent DA[7] + ui-ux IC-flag[5] + impl-eng BC#3] + [own-R1 BC#2/3] | **T2** (4-agent convergence, strongest internal signal, but no external spec) | Convergence ≠ external validation — honest T2. Load-bearing + 4-agent = high BELIEF but NOT T1. |

**Summary:** 8 findings enumerated. Current tags mostly [agent-inference]/[code-read]/[cross-agent] — structurally T2-equivalent but not labeled. Proposed: explicit tier on each finding for consistency with sigma-review hygiene §2d.

**T1-eligible (upgrade): 2 findings** (BC-cqa-1 F2+F4 partial; BC-cqa-9 Q1+Q4+Q5 partial).
**T2 (most common): 5 findings** (BC-cqa-2 G2, BC-cqa-3, BC-cqa-4, BC-cqa-6, BC-cqa-11) + partial upgrades.
**T3 (trivially verifiable but non-external): 1 finding** (BC-cqa-7 plan contradiction) + 1 origin-flag (BC-cqa-6 memory-sourced).

**Recommendation:** tier-tag every BC-cqa-N finding in the lead's plan-file distillation. The label itself is low-cost and future-audits can grep `T[123]\b`. Accept the honest T2 majority rather than inflating to T1. Anti-sycophancy note: resist reframing T2 findings as T1 to look more rigorous — the convergence IS the evidence, not a substitute for external primary sources.

→ revise |source:[DA R1 L2328 + DA R2 L2409 + SEC[2] carry-forward #4] + [agent-inference tier assignment] + [pattern: sigma-review analytical-hygiene §2d]

---

#### Convergence declaration

`code-quality-analyst-r4: ✓ R3-test-expansion |FIX[2]:SQ29+SQ30+SQ31+SQ32 proposed (+3.5h, M1b cluster G; PM[6/7/8] fully covered, T_INJ1-T_INJ5 handoff absorbed in SQ29) |SEC[2]:cost-cap-default=$5/session w/ 0.50/5/25/0 tier rec |SEC[2]:T1/T2/T3-enum #8 findings (T1-eligible 2 partial, T2 majority 5, T3 honest 1) |IC-deltas: IC[2] stop_reason taxonomy +cost_cap_exceeded; IC[3] ToolCallRecord +INV-TCR-1/2 closed-set error taxonomy; IC[5] +INV-TE-5 validator-mandatory; ADR[7] +INV-replay-5/6 replay-as-AsyncIterator |→ ready-for-DA-R3`

### ui-ux-engineer-R3

#### FIX[3] — UD#3 rendering-decision cleanup

**Decision: Option A — pin rendering option-b (inline-at-position_in_turn) NOW.**

##### Rationale

1. **UD#5 research-question (memory-invocation coherence) requires position fidelity.**
   Memory-invocation coherence = cross-model convergence on *when* and *how* memory queries occur within a turn. Measuring this requires preserving `position_in_turn` in the rendered transcript — which tool_call came before/after which tokens, which preceded which. Options (a) end-of-turn-appended and (c) separate-panel DESTROY or DIVORCE position information respectively. Only option (b) inline-at-position_in_turn preserves the temporal signal UD#5 needs.

2. **UD#4 Streamlit-vs-TUI is orthogonal to rendering-option choice.**
   Option-b (inline) is framework-agnostic:
   - Streamlit path: inline `st.markdown(preceding_text)` + `ToolCallBadge` component + `st.markdown(post_text)` in sequence within a turn container (DS[4] badge applies)
   - Textual-TUI path: inline `Static(preceding_text)` + `ToolCallWidget` + `Static(post_text)` within a turn `Container` (DS[4] badge translates to rich-symbol pill per DS[6])
   Both paths render inline at position_in_turn fine. TUI-specific reason to defer rendering decision = none. Rejecting the paternalistic "wait for UD#4" reading.

3. **Deferring rendering was circular.**
   Evaluator was right: "STEP-1: pin rendering option (a/b/c) with user per UD#3" is a circular dependency when UD#3 says "deferred to pre-M2 STEP-1." Converting the deferral into verification-of-pinned-choice resolves this.

##### Side-check: position_in_turn + preceding_text fidelity (ToolCallRecord IC[3])

Per plan IC[3]:
```
position_in_turn: int              # 0-indexed within this Turn
preceding_text: str                # last 50 chars of text preceding this tool_call
```

**Verdict: adequate for option-b inline rendering. ✓**

- `position_in_turn` (0-indexed) gives ordering → deterministic inline placement across tool_calls in same turn
- `preceding_text` (last 50 chars) gives fuzzy-match anchor for replay-determinism checking against full turn text
- Combined: renderer splits turn text at each tool_call's position (using preceding_text as verification anchor) and inserts badge inline

**Caveat (flag to tech-architect-r4, non-blocking):** 50 chars of preceding_text is tight for fuzzy-match in long turns with duplicate substrings. If empirical M1a/b data shows collision rate >0 in test fixtures, tech-architect may want to expand preceding_text to 100 chars OR add `char_offset_in_turn: int` to ToolCallRecord. Non-blocking for option-b pin — falls into STEP-1 verification scope.

**Caveat-2 (M1b cross-provider):** Anthropic content_blocks can interleave text and tool_use; `preceding_text_per_tool_call` list on Message (IC[4]) is the escape-hatch for exact ordering. Option-b rendering MUST consume `preceding_text_per_tool_call` when present, falling back to `ToolCallRecord.preceding_text` otherwise. Flag: ensure message_mapping.py round-trip preserves `preceding_text_per_tool_call` list when Anthropic → canonical translation occurs (already in plan ADR[4] escape-hatch lock — verified consistent).

##### Forward-plan updates (Pre-M2 hard gate, ~1-1.5 day)

Revised:
- **STEP-0:** verify tech-architect IC[2] `kind="tool_result"` + `final_message` acceptance (done — locked in IC[2]). *Carry: also gate IC-flag[5] tool_arg_validator seam present-but-unused check from carry-forward flag #3.*
- **STEP-1 (was: decide rendering a/b/c) → NOW: verify option-b (inline-at-position_in_turn) fidelity against 5-turn 2-model M1b JSONL fixture.**
  - Inputs to verify: position_in_turn ordering deterministic; preceding_text 50-char anchor reconstructs turn-text reliably; Anthropic preceding_text_per_tool_call preserved round-trip.
  - Exit: 5-turn fixture renders with each tool_call inline at correct position, preceding_text matches turn-text at that offset ≥95%, no position conflicts.
  - Fallback: if collision rate >0 OR Anthropic round-trip drops preceding_text_per_tool_call, flag to tech-architect for ToolCallRecord field expansion (char_offset_in_turn) BEFORE M2 shell code.
- **STEP-2 (was: prototype chosen rendering option) → NOW: prototype option-b in BOTH candidate frameworks (Streamlit + Textual TUI) against 5-turn fixture.** Duplicated work, but small (2 × ~2h) and directly feeds STEP-3b decision with concrete renderability evidence.
- **STEP-3:** prototype pre-M2 Streamlit concurrency shim (2h, unchanged).
- **STEP-3b (UD#4):** 2h Textual TUI comparison sketch (unchanged). Now informed by STEP-2 option-b renderability result in each framework.
- **Exit (revised):** option-b renders 5-turn fixture with ≥1 echo-tool round-trip per provider in BOTH framework prototypes; position fidelity ≥95%; user declares "feels right" + picks framework.

##### STEP-1 decision-point framing (belt-and-suspenders)

Even pinned to option-b, STEP-1 retains empirical inputs for BELIEF calibration — not for re-deciding option:
- M1a TTFT p95 informs streaming-inline UX (if p95 >3s, caret+pulse DS[5] becomes load-bearing, not decorative)
- M1b position_in_turn distribution across seed-pair validates option-b assumption empirically (not a deferred decision, but a confidence update on the pinned choice)
- SQ6c pass/fail affects tool_calls coverage in fixture (ADR[2] BELIEF conditional already tracked)

If STEP-1 verification SURPRISES (e.g., position_in_turn collisions >5%, or preceding_text fails to reconstruct >10% of cases), escalate to tech-architect for ToolCallRecord schema extension BEFORE STEP-2 prototypes. Otherwise proceed to STEP-2 with option-b confirmed.

##### BELIEF

- UD#3 resolution (pin option-b): **BELIEF 0.85** (high — UD#5 drives it; fidelity side-check passes; framework-agnostic)
- position_in_turn + preceding_text adequacy: **BELIEF 0.80** (with flagged caveats; verification in STEP-1 will move this to 0.90 or trigger schema expansion)

##### Convergence

ui-ux-engineer-r4: ✓ R3-UD#3-resolution |chose:A |forward-plan-updated:✓ |position_in_turn-fidelity-OK:y |preceding_text-caveat-flagged-to-tech-architect |→ ready-for-DA-R3

### devils-advocate-R3
{to be written}

## r3 belief-tracking
{updates to belief scores post-revision}

## r3 exit-gate verdict
{DA-r3 verdict after plan-track R3 complete}

## r3 delivery
{lead distills approved R3 revisions into plan file after DA PASS}
