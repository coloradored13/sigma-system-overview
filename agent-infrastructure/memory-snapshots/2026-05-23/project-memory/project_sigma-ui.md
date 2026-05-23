---
name: sigma-ui
description: Phase B3 COMPLETE (26.3.31) — 16 modules, 280 tests, E2E integration + enum canonicalization + gate dismissibility. Repo ~/Projects/sigma-ui/
type: project
---

Local tool for running sigma-review/sigma-build with proper orchestration UI instead of chat interface.

**Why:** Current chat-based sigma-review has control inversion problem — agent calls orchestrator (can skip/game) instead of orchestrator calling agent (enforced). User must scroll hundreds of messages to track status. Belief state is self-reported. No mandatory user gates.

**How to apply:** This is the next evolution of the sigma system. Build on existing components (hateoas-agent, sigma-mem, sigma-verify, agent definitions, review protocol). Local-only, repo-clonable.

**Architecture (locked from 26.3.28 review):**
- Orchestrator: import orchestrator-config.py as library (85% verbatim); Orchestrator.start()/advance() cycle; NOT AsyncRunner
- Agent dispatch: anthropic.AsyncAnthropic().messages.create() with agent .md as system= parameter
- MCP integration: P1 orchestrator-mediated (context injection pre-spawn + persistence post-response); P2 tool-forwarding deferred
- Belief computation: TIER-A observables (gaming-resistant, orchestrator-produced) > TIER-B > TIER-C
- UI (Phase B): Streamlit with fragment-per-agent-card; graduation to FastAPI if needed
- Persistence: sigma-mem (as-is, handlers imported directly)
- Cross-model: sigma-verify (as-is, wrapped in async adapter)

**Key design principles:**
- Orchestrator is outer loop (dispatches agents, computes belief, enforces gates)
- Agents are workers (receive tasks, write to workspace, no phase control)
- User gates at: post-R1, post-exit-gate, post-synthesis minimum
- Belief computed from observables (convergence markers, XVERIFY coverage, source provenance)
- Immutable audit log (externally written, not agent-reported)
- Local-only, clone-and-run, API keys in env

**Status:** Phase B3 COMPLETE (26.3.31). 16 modules, 280 tests passing (3 skipped w/ documented reasons). Committed `39ebdc1`, pushed to origin.

**Phase B2 build results (26.3.29 — 5+DA, BUILD TIER-2, P(build-quality)=0.91):**
- Streamlit app entry point (app.py) with session state machine per IC[B2-1]
- 5 UI components: PhaseStrip, AgentGrid, FindingsFeed, TensionPanel, UserGate (data-prep/render separation per ADR[B2-6])
- IC5 gate lifecycle: set_active_gate(), resolve_gate(), fire_gate(), GateConflictError
- Preflight health check module, setup.sh, .env.example
- CQA-R4 dispatcher mode behavioral tests (dispatch_parallel mode= reaches system prompt)
- ADR[B2-3] gate lifecycle, ADR[B2-4] PhaseStateDict type fix, ADR[B2-5] active_gate hardcode fix
- H[1] FALSIFIED: st.fragment has no key= param → closure factory workaround
- H[2] CONFIRMED: OrchestratorWrapper survives Streamlit reruns via session_state
- H[3] PARTIALLY FALSE: snapshot insufficient for findings/tensions → separate calls needed
- DA exit-gate: PASS (0.88 r1, 0.90 r2), 8/8 challenges addressed
- Archive: shared/archive/26.3.29-sigma-ui-phase-b2-workspace.md
- Session crashed post-build pre-promotion; workspace archived and memory updated in recovery session

**Phase A build results (26.3.29 — 5+DA, BUILD TIER-2, P(build-quality)=0.87):**
- 7 modules: orchestrator_wrapper, dispatcher, context_builder, review_state, tier_a_observables, async_adapter + tests
- H1 CONFIRMED: orchestrator-config.py imports as library (A.0 gate PASS, importlib approach)
- H3 ACCEPTED WITH MITIGATIONS (P=50-60%): REWRITE approach for agent .md (not KEEP_SECTIONS), 7-item context injection, MEMORY ENTRY extraction, SDK unavailability preamble
- H4 PARTIALLY CONFIRMED: agent .md as system= with section rewriting + mode filtering
- H5 CONFIRMED: asyncio.to_thread() wraps sigma-verify clients
- H6 CONFIRMED: dual stagger (dispatch + write-path Semaphore)
- Key DA impact: KEEP_SECTIONS→REWRITE (3-agent convergence), A.0 smoke gate, dual stagger, 7-item injection
- ReviewState scoped INTO Phase A (justified: SC2 stagger home)
- types.py deferred (string constants work for Phase A)
- Archive: shared/archive/26.3.29-sigma-ui-phase-a-build.md + synthesis

**Phase B3 build results (26.3.31 — 5+DA, BUILD TIER-2, DA EXIT-GATE PASS):**
- E2E integration wiring: execution_loop.py bridges OrchestratorWrapper → AgentDispatcher → ReviewState
- 8 seams identified and fixed (SEAM[1]-[8]): executor wiring, bridge module, poll loop, GateTier format, dismissibility, ContextBuilder instantiation, belief state updates, DispatchMode conflict
- 7 str Enums canonicalized in types.py (AgentStatus, GateStatus, GateTier, DispatchMode, XVerifyStatus, SourceTier, ObservableTier) per ADR[B3-1]
- G1/G2 dismissibility: field-based (NotRequired[bool] in GateRequestDict) + string-match fallback per IC[B3-3]
- G2 buttons: Advance/Extend/Cancel 3-column layout, on_dismiss='rerun'
- Quality metric: score_response() with 3-check approach per ADR[B3-2] REVISED
- response_utils.py: justified deviation from plan (Streamlit import side-effects forced extraction)
- 280 tests passing, 3 skipped (GateActionRole deferred B4, 2x async_adapter)
- DA: 0 blocking issues, 1 justified deviation, 2 INFO notes
- 3 auto-promoted patterns (str-enum-zero-migration, streamlit-on_dismiss-default, sdk-dispatch-degradation)
- 3 user-approved promotions (decorator-param-definition-time, asyncio-primitives-bound-to-loop, framework-entrypoint-not-importable)
- Archive: shared/archive/26.3.31-sigma-ui-phase-b3-workspace.md
- Session froze during promotion; workspace archived and promotions completed in recovery session

**Architecture review (26.3.28 — 5+DA, 2r, exit-gate PASS, DA grade A-):**
- P(core goals full architecture)=35% — below-average bet
- RECOMMENDED: Streamlit + Anthropic Python SDK as v1, graduation to FastAPI if v1 succeeds
- Key reframing (DA-driven): "Streamlit+SDK vs FastAPI+SDK" — both need dispatch layer, framework choice is UI not orchestration
- H2 weakened to WEAKLY-TO-PARTIALLY (P=55-65%) — outer loop alone insufficient, needs TIER-A observables
- H4 (quality preservation) at 52% — coin flip, weakest hypothesis
- Scope creep = #1 risk (P=35-42%), tool-access regression = #2 (P=20-25%)
- 7 patterns promoted to global memory
- Archive: shared/archive/26.3.28-sigma-ui-architecture.md + synthesis
