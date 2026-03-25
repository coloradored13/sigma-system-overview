<!-- archive header per §8b -->
<!-- date: 2026-03-25 -->
<!-- mode: ANALYZE -->
<!-- tier: TIER-2 -->
<!-- rounds: 2 (R1 + R2/DA) -->
<!-- agents: TA, CQA, UXR, TW, PS, RCA, DA -->
<!-- exit-gate: PASS (revised from FAIL after R2) -->
<!-- directives: v1.0 -->
<!-- archived-by: manual recovery (lead skipped §8 archiving before shutdown) -->

# workspace — hateoas-agent improvement evaluation
## status: archived
## mode: ANALYZE

## infrastructure
ΣVerify: openai(gpt-5.1), google(gemini-3.1) available

## task
Evaluate hateoas-agent for improvement opportunities: code quality, test coverage, functionality, extensibility, API exploration/lockdown DX. Goal: make this an extensible tool for diverse use cases. Output: sigma-build prompt if changes recommended, nothing if no changes needed.

## prior-review
review-7: SHIP (arch A, security A, API A-) — 26.3.17

## scope-boundary
This review analyzes: hateoas-agent codebase (src/hateoas_agent/ + tests/) for improvement opportunities
This review does NOT cover: sigma-mem, sigma-system-overview, tax-form-tracker, or any other project
temporal-boundary: none
Lead: before writing synthesis or documents, re-read this boundary.

## prompt-decomposition

### Q[] — questions (research scope)
Q1: What code quality improvements would most benefit the codebase?
Q2: Where are the test coverage gaps (beyond the 91% headline)?
Q3: How can API exploration (discovering available actions/states) be made more intuitive?
Q4: How can lockdown (restricting available actions based on state) be made easier to configure and reason about?
Q5: What functionality improvements are needed based on real-world usage (sigma-mem, tax-form-tracker)?
Q6: What would make this library extensible enough for diverse external adoption?

### H[] — hypotheses to test
H1: The library is ready for broader adoption beyond internal projects
H2: API exploration and lockdown are currently difficult to navigate
H3: The v0.2 orchestration layer added complexity that may need simplification

### C[] — constraints
C1: Python >=3.10, zero runtime deps must be maintained
C2: No breaking changes from existing v0.1/v0.2 API surface
C3: Must remain useful for existing consumers (sigma-mem, tax-form-tracker)

user-confirmed: yes

## findings
### tech-architect

**scope**: arch Q1,Q3,Q4,Q6 | H1,H2,H3 | full codebase read (19 modules, 26 test files, 439 passing) + GPT-5.1 cross-verify on F1
**post-DA revisions**: F1 severity MEDIUM→LOW (DA[#1] conceded); H2 verdict revised (DA[#4] conceded); source tags added (DA[#3])

#### F1 [LOW — fix before external adoption] AsyncRunner private-attr bypass — extensibility trap
**finding**: AsyncRunner._async_start() (async_runner.py:97-99) directly mutates `orch._current_phase`, `orch._context`, `orch._phase_history` instead of calling public `Orchestrator.start()` / `advance()`. Also duplicates guard-evaluation logic in `_async_advance()` (lines 117-128) that is identical to `Orchestrator.advance()` but cannot inherit its improvements.
**evidence**: async_runner.py:97-99 vs orchestrator.py:294-299; guard loop at async_runner.py:120-127 ≈ orchestrator.py:322-330 (structural duplicate) |source:independent-research(code-read)|+|source:external-openai-gpt-5.1|
**impact**: any validation/hooks/instrumentation added to Orchestrator.start() is silently skipped in async workflows. Concrete extension scenario: user subclasses Orchestrator to add event emission on phase transitions, overrides _execute_phase() or start() — AsyncRunner bypasses both, async workflows produce no events, silently.
**verify**: GPT-5.1 AGREE(high) — "async flows cannot rely on public API extensions being honored"
**severity-rationale**: within-package private-attr access is standard Python practice (N=0 external Orchestrator extenders currently). DA[#1] correctly challenged "adoption-blocking" framing — revised to LOW with fix-before-external-adoption flag. Structural finding stands.
**fix**: add `async def _execute_phase_async()` to Orchestrator; AsyncRunner delegates rather than bypasses. OR Orchestrator.start() accepts optional async handler hook.
**H3-answer**: YES, v0.2 added a real complexity seam — sync/async paths are independent execution trees with private-attr coupling

#### F2 [LOW] Cross-API asymmetry: Resource missing `get_transition_metadata`
**finding**: StateMachine implements `get_transition_metadata()` (state_machine.py:261-270); Resource does not. Registry._handle_action() has a to_state mismatch warning (registry.py:271-287) that is dead code for all Resource-based workflows.
**evidence**: resource.py — no `get_transition_metadata` method |source:independent-research(code-read)|
**impact**: Resource users get zero to_state deviation warnings; cross-API parity tests don't cover metadata completeness.
**fix**: add `get_transition_metadata` to Resource. Low value unless to_state tracking is documented as a feature.
**severity-calibration**: HasHateoas Protocol marks it optional — consistent with existing design. Advisory only.

#### F3 [LOW] Guard context source asymmetry — invisible to users
**finding**: Registry._get_filtered_actions passes `self._last_result` as guard context (registry.py:152). Orchestrator.filter_actions uses `self._context` directly (orchestrator.py:590). Same `context` parameter name, completely different semantics.
**evidence**: registry.py:152, orchestrator.py:590, state_machine.py:272 |source:independent-research(code-read)|
**impact**: StateMachine guards see last handler return value; Orchestrator guards see full accumulated workflow context. Undocumented behavioral split.
**Q4-answer**: lockdown works but guard authoring requires different mental models across API surfaces with no API signal.
**fix**: document distinction in each `filter_actions` docstring. Zero-breaking-change.

#### F4 [LOW] MCP server: 45% coverage, transport hardcoded
**finding**: mcp_server.py has 45% branch coverage. `serve()` only supports `transport="stdio"` but error message implies future support.
**evidence**: mcp_server.py:89-90; pytest-cov output |source:independent-research(code-read+pytest-cov-output)|
**fix**: clarify docstring to say stdio-only for v0.2; remove transport param or narrow error message.

#### F5 [ADVISORY] `composite.py`: `_register_tool` error message may omit second resource name
**finding**: CompositeRegistry._register_tool (composite.py:55-63) — new conflicting registry not yet in `self._registries` at call time, so second resource name may be absent from ToolNameConflictError.
**evidence**: composite.py:47-63 |source:independent-research(code-read)|
**severity**: advisory — error fires correctly, message completeness only.

#### Hypothesis verdicts (post-DA revised)
H1(adoption-ready): PARTIAL — StateMachine/Resource adoption-ready (A grade); Orchestrator extenders need F1 fixed first
H2(exploration/lockdown-difficult): REVISED PARTIAL — exploration IS difficult via README (broken install, missing v0.2, wrong "model: Any" claim — DA[#4] conceded); exploration via API internals NOT difficult (discovery mode well-implemented). Doc-surface vs code-surface distinction.
H3(v0.2-complexity): CONFIRMED LIMITED — seam is AsyncRunner/Orchestrator private coupling (F1); Conditions, AgentSlot, phases/transitions are clean.

#### Coverage gaps (Q2 context for code-quality-analyst)
mcp_server.py: 45% (lines 92-139 = async server loop — requires mcp package)
resource.py: 80% (lines 199-231 = validate() failure paths + filter_actions exception handling)
runner.py: 80% (lines 56-75 = multi-resource init path, 227-232 = NoHandlerError strict path)
composite.py: 86% (lines 94-101 = fallback tool lookup path)

### code-quality-analyst

[STATUS] ✓ R1+R2 COMPLETE | scope: Q1+Q2, H1 | 19 src files line-sweep + ruff --select ALL + coverage analysis | #6 CQ findings, #7 TG findings | xverify: gpt-4o agree:high on CQ1 | DA[#1] CQ1→LOW | DA[#3] source tags added

#### CQ1 [L] Silent agent ERROR swallow — no phase-level warning |xverify:gpt-4o:agree:high| |source:direct-code-analysis+external-openai-gpt-4o|
`run_agent()` (orchestrator.py:373) catches all executor exceptions → `AgentResult(status=ERROR, error=str(e))`. `_execute_phase()` (orchestrator.py:638-642) merges phase handler result without inspecting agent statuses. Executor consistently panics → workflow advances normally, no log fires.
Dialectic: "fail-closed is correct resilience design". CONCEDE fully — phase handler receives AgentResult list and can inspect .error; orchestrator contract does not promise to inspect it. Missing logger.warning is quality-of-life not correctness gap. DA[#1] accepted: severity revised L (was M).
Fix: `logger.warning("Agent '%s' returned ERROR: %s", agent.name, result.error)` in run_agent() after status=ERROR. Zero API change. Optional: `on_agent_error` callback on Orchestrator.
Test-gap: no test verifies agent ERROR result is surfaced or logged — TG-OA below.
xverify: GPT-4o AGREE(high) |source:external-openai-gpt-4o|

#### CQ2 [L] persistence.py:10 — unused import (DiscoveryReport) |source:direct-code-analysis|
ruff F401: `DiscoveryReport` imported but never used. `TransitionRecord` is used (line 102). Dead import since v0.1.
Fix: `ruff --fix` auto-removes. One-liner.

#### CQ3 [L] mcp_server.py:115 — unused exception variable |source:direct-code-analysis|
ruff F841: `except Exception as exc` — `exc` never referenced. `logger.exception()` captures exc_info automatically.
Fix: change to `except Exception:` (ruff --fix).

#### CQ4 [L] orchestrator_visualization.py:47 — unused loop var + wrong iterator |source:direct-code-analysis|
ruff B007+PERF102: `for phase_name, phase_def in orchestrator._phases.items()` — `phase_def` never used.
Fix: `for phase_name in orchestrator._phases:` (one-line change)

#### CQ5 [L] advertisement.py DRY — action-rendering loop 80% duplicated (carried review-7) |source:direct-code-analysis|
`format_result_with_actions` and `format_error_with_actions` share identical 8-line action-rendering loop. Only diff: `json.dumps(result)` vs `json.dumps({"error": msg})`.
Fix: extract `_render_actions(actions) -> str`; both call it. Non-breaking. Still unaddressed from review-7.

#### CQ6 [I] orchestrator.py — `import json` inside closures (3 locations) |source:direct-code-analysis|
ruff PLC0415: json imported at orchestrator.py:483, 663, 699 (inside handler closures). Stdlib, already imported elsewhere. Style inconsistency only.
Fix: hoist `import json` to module-level imports. Zero functional risk.

---

#### Test Coverage Gaps (Q2) |source:direct-code-analysis+coverage-report|

**TG1 [M] runner.py:226-238 — NoHandlerError catch path untested**
`except NoHandlerError` fires when action passes state-validation but handler returns None. Neither `on_phantom_tool` callback nor `strict=True` raise-path in this branch has any test.
→test: stub `registry.handle_tool_call` to raise `NoHandlerError`; verify callback + strict raise `PhantomToolError`

**TG2 [M] runner.py:200-201 — `on_transition` callback untested**
`on_transition(old_state, action_name, new_state)` is public API. No test verifies it fires or receives correct args.
→test: mock state-changing tool response; assert `on_transition` called with correct (None, "gateway", "active")

**TG-OA [L] orchestrator.py — agent ERROR status has no observable test**
CQ1 fix (log warning) needs test coverage. Currently no test asserts agent ERROR surfaces anywhere.
→test: executor that raises; verify AgentResult.error populated and (after CQ1 fix) log captured

**TG3 [L] runner.py:56-61 — multi-resource Runner([sm1, sm2]) init path**
`Runner.__init__` list branch + multi-gateway system prompt (lines 88-98) not covered in runner tests (composite tests exist separately).
→test: `Runner([sm1, sm2], client=mock)` — verify `_default_system()` uses `gateway_names` branch

**TG4 [L] resource.py:216-231 — filter_actions guard exception path**
Resource.filter_actions() guard-raises branch (lines 225-230) not exercised. StateMachine guard-exception tests exist; Resource analogue missing.
→test: Resource with guard that raises; verify action excluded, no exception propagates

**TG5 [L] composite.py:94-101 — fallback lookup + NoHandlerError**
`CompositeRegistry.handle_tool_call()` fallback iteration (lines 94-97) and NoHandlerError raise (99-101) never hit.
→test: unknown tool name on composite; verify NoHandlerError raised

**TG6 [L] async_runner.py:93,95 — _async_start ValueError paths**
`ValueError` for no-phase / unknown-phase in `_async_start` (lines 92-95) not tested. Sync equivalents are tested.
→test: `await runner.run_orchestrated(phase="nonexistent")` — verify ValueError

---

#### Ruff actionable (excluding docs/ANN/UP noise)
F401 persistence.py:10 auto-fix | F841 mcp_server.py:115 auto-fix | B007+PERF102 orch_visualization.py:47 rename | SIM103 runner.py:114 auto-fix | SIM114 state_machine.py:212-215 auto-fix | SIM114 orchestrator.py:250-253 auto-fix | PLC0415 orchestrator.py:483,663,699 hoist
C901 runner.py:run() complexity=19 + visualization.py:state_machine_to_mermaid=14 — informational, not refactor targets

UP035/UP006/UP045 (194+76 violations): `Dict`→`dict`, `Optional[X]`→`X|None` across all files — all auto-fixable, low priority, safe under C1(>=3.10).

---

#### H1 verdict (code quality)
H1(adoption-readiness): PARTIAL CONFIRM — A- grade sustained. No bugs. No security issues. No dead code beyond trivial CQ2/CQ3. 91% coverage with 439 tests.
Gaps before broader promotion: CQ1 (silent ERROR swallow) + TG1+TG2 (callback coverage) — all low-effort, high-value. Everything else optional cleanup.
Corroborates ux-researcher F-UX1 (guard exception observability) — shared pattern: silent failures in the guard/executor error paths.

### ux-researcher
[STATUS] ✓ R2 COMPLETE | DX grade: A- (held) | 4 findings post-DA (F-UX5→INFO, F-UX3 M→LOW)
xverify: gpt-5.1=uncertain-not-disagree on F-UX1 | gemini-3.1 FAILED 404 | strict=True ¬guard-escalation confirmed by grep | finding upheld
DA revisions: F-UX3 M→LOW (IDE-plugin framing dropped, concrete user narrowed), F-UX5 L→INFO (Hick's law ¬applicable to docs), source tags added

#### F-UX1 [!H] Guard exception = silent action disappearance, no fix-it path |xverify:gpt-5.1:uncertain(upheld)| |source:code-inspection+[established-framework:T3]|
Guards exc caught at DEBUG-only (state_machine.py:299-304, resource.py:225-230). strict=True ¬applies to guards — confirmed by grep. Action vanishes. Developer has no signal.
DX failure: what-wrong=0%, how-fix=0% → fails Google error-msg hierarchy entirely. Three-step diagnosis required.
DA[#1]: ✓ UPHELD — DA confirmed no challenge on substance. Anchor finding for synthesis.
Fix: (a) DEBUG→WARNING on guard exception, (b) `guard_strict` param: True → raise on guard exc. Fail-closed preserved.
Q4-answer: lockdown logic correct; observability of WHY lockdown fires is the gap.

#### F-UX2 [M] Guard ctx undocumented at point of use |source:[independent-research:T2]+code-inspection|
action() says "guard receives last handler result dict" — ¬shows what keys ctx contains. No inline example. orders_with_guards.py exists but ¬linked from action() signature.
Self-explanatory = top API usability factor (arXiv 2601.16705, 9/16 devs). Guard ctx fails this — requires external lookup.
Fix: add ctx example to action()/@action docstrings. 1-line README note.

#### F-UX3 [LOW — revised M→LOW per DA#2] State-graph introspection: ergonomic gap |source:code-inspection|
DA[#2] CONCEDE PARTIALLY: "IDE plugin authors" framing premature (N=0 external users). Narrowed to concrete users: (1) author debugging without parsing mermaid output, (2) test_cross_api_parity.py already calls get_actions_for_state() per-state manually, (3) parity: DiscoveryReport.to_state_map() exists for discover-mode; strict-mode has no equivalent.
H1 revision: F-UX3 ¬adoption-blocking. Ergonomic + parity gap only.
Fix: `sm.get_state_map() -> Dict[str, List[str]]`, export from __init__. Zero breaking change.

#### F-UX4 [L] Orchestrator advance() stall invisible |source:code-inspection|
No log when advance() evaluates all guards and none pass (orchestrator.py:332-333). Stall ≠ loop — no signal which it is.
Fix: INFO log when N guards evaluated from phase X and none match.

#### F-UX5 [INFO — downgraded L→INFO per DA#4] Three-API documentation
DA[#4] CONCEDE: Hick's law ¬applicable to developer documentation about different API surfaces. "recommended" label already sufficient. No action required.

#### H-assessments (UX) — post-DA
H1(adoption readiness): PARTIAL — base API DX is A. F-UX1 sole adoption blocker (guard debugging requires non-obvious DEBUG logging). F-UX3 ergonomic gap only.
H2(exploration/lockdown difficulty): CONFIRMED for lockdown observability (F-UX1+F-UX4). F-UX3 LOW ergonomic gap. Guard setup well-designed; guard debugging is the gap.

#### Cross-ref (post-DA)
F-UX1 ≈ CQA-CQ1 (silent failures in guard/executor error paths — 3 agents independently converged)
F-UX1 ≈ TA-F3 (guard context asymmetry — shared observability gap)
F-UX3 ≈ TW-F1 (v0.2 undiscoverability — programmatic introspection vs README omission)

### technical-writer

**STATUS** ✓ COMPLETE R2 | 5 findings (1H, 1M, 2L, 1I) | scope: README+docstrings+examples+cross-doc | verified: gpt-5.1 agree:high on F1 | DA: F3 revised LOW (accepted)

#### F1 [HIGH] v0.2 orchestration invisible in README |verified:gpt-5.1:agree:high| |source:independent-research|
README covers StateMachine, Resource, discovery mode, security, examples. Does NOT mention Orchestrator, AsyncRunner, or conditions — the entire v0.2 feature set. First-time evaluator reads README, sees a state-machine library, misses that multi-agent orchestration is included. 12 examples listed but zero orchestration examples in examples/. CLAUDE.md lists v0.2 modules — asymmetry between CLAUDE.md and README.
→impact: Q6(extensibility docs), H1(adoption readiness). External evaluators for orchestration use cases will not find it.
→fix: Add "Multi-agent orchestration (v0.2)" section to README after "When to use it". Add one orchestration example file. Add it to examples list.
→corroborates: tech-architect F1, ux-researcher F-UX3, product-strategist F3 — four independent reviewers identify orchestration subsystem as most isolated

#### F2 [MEDIUM] Install instructions fail for extras |source:independent-research:inferred|
README install block:
  step 1: `pip install git+https://github.com/coloradored13/hateoas-agent.git` (core)
  step 2: `pip install 'hateoas-agent[anthropic]'` (extras)
After a git-url install, step 2 attempts PyPI lookup — package not on PyPI — and fails. Correct form: `pip install 'hateoas-agent[anthropic] @ git+https://...'` or single git URL with extras. Also: URL uses `coloradored13` — known username drift from review-7 (actual: bjgilbert). Note: install failure inferred from pip semantics, not live-tested in clean env. Root cause (no PyPI publish) corroborated by product-strategist F2[CRITICAL].
→impact: H1(adoption readiness). First-time user following README cannot install extras.
→fix: PyPI publish (product-strategist P1) solves root cause. Short-term: consolidate to correct git URL with extras syntax. Resolve URL to bjgilbert.

#### F3 [LOW] RunResult public properties undocumented |source:independent-research| |DA:revised-from-MEDIUM|
`RunResult` (runner.py:292) has three undocumented public properties in `__all__`: `gateway_calls`, `dynamic_calls`, `unique_tools`. `gateway_calls` encodes non-obvious logic: first tool name in trace = gateway. DA challenge accepted: post-run analysis object reached only after successful adoption — polish issue not adoption blocker.
→impact: Q3(exploration DX) for callers analyzing agent behavior post-run. LOW.
→fix: Add 1-line docstrings. Flag the gateway-as-first-tool assumption explicitly.

#### F4 [LOW] `_normalize_param_type` logic undocumented |source:independent-research|
`registry.py:73` — non-obvious parsing (splits on `(`, extracts base type, falls back to `string`, preserves extra text as description). No docstring. Affects how params like `"string (comma-separated values)"` are handled. Any contributor extending param type support must re-derive the behavior.
→impact: maintainability only.
→fix: Add docstring with example: `"string (csv)" → {"type": "string", "description": "string (csv)"}`.

#### F5 [INFO] Hardcoded model name will drift |source:independent-research|
README quick-start and discovery example use `"claude-sonnet-4-20250514"`. Runner default also hardcodes this. Correct as of 26.3.25 but will become stale.
→info: Not a defect now. Flag for future: consider note "or latest Claude Sonnet model" in docs.

#### Strengths (no action needed)
- README value prop A-grade: crisp tagline, comparison table, discover→lock down progression, security section
- Docstring coverage complete on all public API classes/methods (StateMachine, Runner, Registry, Resource, Orchestrator, conditions factories, all checkpoint types)
- Module-level docstrings on all 18 source files ✓
- Cross-doc terminology consistent: `_state`, `HasHateoas`, guard/discover/strict all uniform
- examples/ covers all 12 documented scenarios — all exist, all match README listing
- Progressive disclosure works: README → feature sections → examples/ → source

#### Hypothesis verdicts (doc perspective)
H1(adoption-ready): PARTIAL — core library docs are adoption-quality. F1+F2 are blockers specifically for orchestration adoption and first install.
H2(exploration/lockdown-difficult): MOSTLY FALSE — discovery mode is well-documented (full section, code, output shown). Guard docs exist. Minor gap: guard context asymmetry (StateMachine vs Orchestrator) undocumented — corroborates tech-architect F3.
H3(v0.2-complexity): NOT a simplification problem — Orchestrator API is clean. Problem is it's undiscoverable from README.

### product-strategist

**STATUS** ✓ R2 COMPLETE | 8 findings post-DA | 2C,2H,2M,1L,1ADV | DA[#1]→F4 escalated CRITICAL | DA[#2] partial concede | DA[#3] partial→P6 advisory | DA[#4] partial | DA[#5] concede→provenance added

#### F1 [HIGH] Competitive gap narrowed not closed — reframe positioning |verified:gpt-5.1:partial| |source:WebSearch(changelog.langchain.com,particula.tech,letsdatascience.com)|
LangGraph added "dynamic tool calling" (2026). Architecture: developer-written filter fn before model call. Distinct from HATEOAS: LangGraph = filter code developer maintains; hateoas-agent = server-declared hypermedia in each response. gpt-5.1 PARTIAL: architectural distinction confirmed; "security/deterministic" framing correctly challenged. Real advantage: (a) zero boilerplate, (b) LLM never sees invalid tool names in current-turn schema, (c) advertised actions = first-class API contract not filter logic.
DA[#4] acknowledged: "20-line filter" IS the real competitor for <10 tools / 2-3 states. Library differentiates at: discovery mode (no DIY equivalent), MCP server integration, CompositeRegistry, Orchestrator. PM5 risk real for toy use cases; differentiation holds at production-scale.
→fix P5[LOW]: update README comparison table — "Correctness by construction" replaces "Deterministic"; add note that 20-line filter is viable for simple cases, library adds discovery mode + MCP + orchestration.
→new-entrant: Google ADK 2.0 alpha — flat-tool/filter-based, no HATEOAS gap closed, Google Cloud pull is enterprise risk. |source:google.github.io/adk-docs|

#### F2 [CRITICAL] PyPI not published — prioritization gap, no technical blocker |source:curl-pypi.org/pypi/hateoas-agent/json→HTTP-404,review-5(26.3.7),review-6(26.3.7)|
HTTP 404 on PyPI confirmed (26.3.25). Name unclaimed — no squatting, no naming conflict. No technical blocker. DA[#2] correct: 18-day delay is a prioritization signal not a technical gap. Fix is mechanical and unblocked.
→fix P1[CRITICAL]: uv build + uv publish. No code changes. BUT: must fix F4 README false claim BEFORE publishing — publishing with false competitive claim is worse than not publishing.

#### F3 [HIGH] Orchestrator onboarding gap — v0.2 invisible externally |source:src/hateoas_agent/__init__.py(20+-symbols-counted),examples/glob(12-files-zero-orchestration)|
__init__.py exports 20+ orchestration symbols. examples/: 12 files, ALL v0.1 patterns, zero orchestration examples. README: no mention of Orchestrator or v0.2. Architecture correct (Orchestrator IS HasHateoas per tech-architect). Problem is onboarding gap, not architecture.
→fix P2[HIGH]: add examples/orchestrator_basic.py — minimal 3-phase orchestrator with guards. ~50 lines.

#### F4 [CRITICAL] README false competitive claim + model-agnostic Runner absent |source:README.md:19(grep-confirmed),WebSearch(LangGraph/CrewAI/OpenAI-SDK/SmolAgents-all-model-agnostic)|
DA[#1] CONCEDED: README.md:19 comparison table states "Model dependency | **Any**" for hateoas-agent. Factually false — Runner requires `anthropic` package. A developer reads "Any", tries OpenAI, hits ImportError on day 1. Active misleading claim creating a trust violation on first use — worse than a missing feature. Must be corrected before PyPI publish.
Underlying gap: Runner is Anthropic-only. Flagged review-4 as #1 growth lever. v0.2 did not address. LangGraph, CrewAI, OpenAI SDK, SmolAgents all model-agnostic.
→fix P3a[CRITICAL]: correct README:19 before publish — "Any (bring your own loop) / Claude (built-in Runner)"
→fix P3b[HIGH]: add RunnerProtocol/AbstractRunner protocol class. Keep AnthropicRunner as default. Zero breaking changes.

#### F5 [MEDIUM] User segmentation: two audiences, one README
Primary: Python devs with stateful workflows. README correctly leads with this.
Secondary: ML engineers building multi-agent orchestration. v0.2 targets this. Zero external worked examples.
→fix: add v0.2 section to README after "When to use it"; keep intro stateful-workflow-focused.

#### F6 [MEDIUM] GitHub URL inconsistency still present (review-7 unresolved) |source:pyproject.toml(Homepage/Repository-fields),README.md:24|
pyproject.toml + README use `coloradored13`. Pre-publish this is the canonical install URL — wrong URL = broken installs.
→fix P4[MEDIUM]: canonicalize before publish. 3 locations: pyproject.toml Homepage, Repository, README install command.

#### F7 [LOW] Q5 unanswerable without external adopters
sigma-mem + tax-form-tracker internal single-owner, no issues, no telemetry. Q5 signal requires external adopters — prerequisite is PyPI publish.

#### F8 [ADVISORY] Distribution: highest expected-value move after PyPI publish (DA[#3] partial concede)
Outside sigma-build prompt scope (build prompt = code+docs). Adding as advisory only.
→P6[ADVISORY]: write comparison post "HATEOAS vs LangGraph dynamic tool filtering" using F1 framing. Highest adoption expected-value after PyPI publish.

#### Hypothesis verdicts (product perspective)
H1(adoption-ready): PARTIAL — architecture A, tests A. Blockers: PyPI [CRITICAL], README false claim [CRITICAL], Orchestrator example [HIGH], model-agnostic Runner [HIGH], URL [MEDIUM]. Grade B+ arch, C adoption (two criticals).
H3(v0.2-complexity): PARTIALLY CONFIRMED — architecture clean, onboarding gap confirmed.

#### Cross-agent convergence (post-DA)
R1 convergence holds: (1) v0.2 undiscoverable, (2) PyPI not published. DA adds new critical: README "Model dependency: Any" is a false claim — must fix before publish. Zero dissent on all three.

### reference-class-analyst

[STATUS] ✓ R1 COMPLETE | scope: Q5+Q6, H1+H3 | superforecasting protocol applied | cross-verify: gpt-4.1=agree:high on F-RC1

#### SQ[] — sub-question decomposition
SQ1: What is the base rate for small single-author Python libraries achieving meaningful adoption (>1K monthly downloads, >50 stars) within 12 months? → **2-5%** (see RC1-RC3)
SQ2: What differentiates successful niche Python libraries from the ~95% that don't achieve adoption? → Content marketing + ecosystem integration + pain-point clarity (see ANA1-ANA5)
SQ3: Is the AI agent framework space receptive to new entrants in 2026? → **Receptive to niche ideas, hostile to new frameworks** (see RC4, market data)
SQ4: Does improving code quality/features of hateoas-agent materially change adoption probability? → **Necessary ¬sufficient** — moves P from ~2% to ~5-8%, but ceiling exists without distribution strategy
SQ5: What is the strongest case that improving the library is the wrong approach entirely? → **Distribution > product at this stage** (see DISCONFIRM)

#### RC[] — reference classes
RC1: **Small single-author Python libraries on PyPI** (N=~500K packages). Base rate for >1K monthly downloads at 12mo: ~2-5%. Median PyPI package has <100 monthly downloads. The long tail is severe — top 1% of packages account for >90% of downloads. |source:independent-research(pypistats.org,packaging.python.org)|
RC2: **AI agent tooling libraries launched 2024-2026** (N=~50-100 notable). Space dominated by well-funded teams: LangGraph(24.8K stars, Harrison Chase/Sequoia), OpenAI Agents SDK(OpenAI), Google ADK(Google), PydanticAI(Pydantic Inc), CrewAI(VC-backed), SmolAgents(HuggingFace). New single-author entrants achieving >500 stars: ~3-5 in past 2 years. Base rate for meaningful adoption: **1-3%** given competitive density. |source:independent-research(github.com,firecrawl.dev,softcery.com,langfuse.com)|
RC3: **llmstatemachine** (robocorp) — closest direct analogue: Python + state machine + LLM agents. Despite corporate backing (Robocorp), minimal adoption visible (low GitHub stars, not in any 2026 framework comparison list). Suggests state-machine-for-agents niche has low natural demand pull. |source:independent-research(github.com/robocorp/llmstatemachine)|
RC4: **Market consolidation pattern**. AutoGen placed in maintenance mode Oct 2025. Framework space consolidating to 5-7 leaders. New entrants that succeed are acquired or backed by major companies. Independent single-author frameworks: base rate for top-20 entry <1%. |source:independent-research(aimultiple.com,turing.com,shakudo.io)|

#### ANA[] — historical analogues (small→successful Python libraries)
**PRIMARY analogues** (directly comparable starting position):
ANA1: **Instructor** (Jason Liu) — structured LLM outputs. 1-person start → 11K stars, 3M monthly downloads. SUCCESS FACTORS: (a) solved specific pain no framework addressed, (b) built on Pydantic's existing ecosystem, (c) extensive blog posts + tutorials, (d) multi-provider support. **Relevance: HIGH** — similar starting position. Key diff: Instructor piggybacked on Pydantic's 550M/mo ecosystem. |source:independent-research|
ANA2: **Rich** (Will McGuigan) — terminal formatting. 1-person → 50K+ stars. SUCCESS: (a) immediate visual demo appeal, (b) solved universal pain, (c) heavy content marketing. **Relevance: MODERATE** — HATEOAS is conceptual/architectural, harder to demo than Rich's visual wow. |source:independent-research|
**BOUNDARY analogues** (ceiling/category markers, NOT realistic comparables — tiered per DA[#2] R3):
ANA3: **Typer** (Sebastian Ramirez) — CLI framework. Built by FastAPI author. **Relevance: LOW** — fame-based distribution structurally unavailable. Marks distinct category. |source:independent-research|
ANA4: **httpx** (Tom Christie) — async HTTP. 1-person → 13K+ stars. SUCCESS: (a) clear upgrade path from requests, (b) async was trending need. **Relevance: MODERATE** — "same but better" strategy. hateoas-agent has no established "thing" to improve on (novel concept). |source:independent-research|
ANA5: **Pydantic** — validation. Side project 2017 → 10B downloads 2026. SUCCESS: adopted as dependency by FastAPI, then every major AI SDK. **Relevance: ASPIRATIONAL** — dependency-adoption ceiling. Upper bound, not realistic target. |source:independent-research|

**ANA-PATTERN**: 5/5 share: (1) solved immediately demonstrable pain, (2) extensive content marketing by author, (3) ecosystem integration with existing popular tools. **0/5 succeeded on code quality alone.** CAL estimates anchored on PRIMARY (ANA1/2/4), not BOUNDARY (ANA3/5). |source:agent-inference|

#### CAL[] — calibrated probability estimates |source:agent-inference|

CAL1: P(>50 stars + >1K monthly downloads within 12mo | no changes) = **2-3%** | 80%CI[0.5%, 8%]
CAL2: P(same | all team code improvements implemented) = **5-8%** | 80%CI[2%, 15%]
CAL3: P(same | code improvements + active content marketing) = **12-18%** | 80%CI[5%, 30%]
CAL4: P(same | code improvements + content marketing + ecosystem integration as plugin) = **15-22%** | 80%CI[8%, 38%] | **CONDITIONAL/ASPIRATIONAL per DA[#3] R3**: P(plugin strategy pursued)=25-35%; P(adoption|plugin achieved)=50-65%; unconditional EV~17%. Point estimate assumes strategy is pursued.
CAL5: P(top-20 AI agent framework by stars within 24mo) = **<1%** | 80%CI[0.1%, 3%]

#### PM[] — pre-mortem scenarios

PM1: **Built it but nobody came** (P=35-40%) — All code improvements implemented, technically excellent, zero distribution effort. Best-kept secret on GitHub.
PM2: **Solved a problem nobody has** (P=15-20%) — HATEOAS elegant but practitioners find flat tool lists + prompt engineering "good enough." Framework comparisons never mention it.
PM3: **Framework gravity well** (P=15-20%) — LangGraph absorbs state-based-tool-discovery concept in v1.2. Unique value commoditized by 25K-star framework.
PM4: **Anthropic lock-in perception** (P=10-15%) — Runner defaults to Claude, all examples use Claude. OpenAI/Google communities never discover it.
PM5: **Over-engineered for the need** (P=5-10%) — "Just filter your tools per state" as a 20-line pattern defeats the library.

#### DISCONFIRM — mandatory R1 duty

**Strongest case AGAINST improving the library as primary strategy:**

The library is already grade A/A- (review-7 confirmed, tech-architect + ux-researcher reconfirmed). 91% coverage, 439 tests, zero runtime deps, clean architecture. **Making it incrementally better does not materially change adoption.** The ANA pattern is unambiguous: 5/5 successful analogues required active distribution + code quality. 0/5 succeeded on code quality alone. Improving code from A- to A when distribution is at F is optimizing the wrong variable.

**Counter-to-counter**: Code improvements remove adoption BLOCKERS (broken install, missing README, PyPI absence) that would prevent adoption even if distribution succeeds. Author's own projects benefit regardless. Correct framing: code improvements = necessary adoption prerequisites, not adoption drivers.

**Verdict**: Improving the library IS correct — but only if paired with distribution strategy. Code improvements alone: P moves 2%→5-8%. Code + distribution: P moves to 12-22% (revised down from 12-30% per DA[#3] R3 — plugin condition decomposed). |source:agent-inference|

#### OV-RECONCILIATION

| Dimension | Inside view (team) | Outside view (base rates) | Gap |
|---|---|---|---|
| Code quality | A-/A, minor fixes | Table stakes, not differentiator | **ALIGNED** |
| Adoption likelihood | "Fix these and it's ready" | 2-5% base rate | **DIVERGENT** — inside view assumes quality→adoption; outside view says distribution is binding |
| Competitive position | "Unique concept" | Framework consolidation; LangGraph absorbs adjacent concepts | **PARTIALLY DIVERGENT** — 12-18mo protection window |
| Improvement ROI | "Each fix helps" | Distribution was the multiplier in all analogues | **DIVERGENT** — marginal code fixes have diminishing returns; marginal distribution has increasing returns |

**OV VERDICT**: Inside view ~70% correct on WHAT to improve. ~30% correct on WHETHER improvements alone drive adoption. Recommendations should be framed as "adoption readiness prerequisites" not "adoption drivers."

#### H-assessments

**H1 (adoption readiness — with data)**: PARTIALLY CONFIRMED with caveat. Library IS technically adoption-ready for core use case. But "adoption-ready" ≠ "adoption-likely." P(adoption | quality) ≈ 2-5%. P(adoption | quality + distribution) ≈ 12-30%. Gap is distribution.

**H3 (complexity concern — is it real?)**: CONFIRMED BUT OVERWEIGHTED. AsyncRunner coupling (tech-architect F1) is real, should be fixed. But from outside view, complexity doesn't kill small libraries — obscurity does. 95%+ of failed small libraries had adequate code quality. Complexity matters for the 5-8% who evaluate; irrelevant for the 92-95% who never find it.

#### Q5/Q6 answers (reference-class grounded)

**Q5**: N=2 internal users insufficient for generalizable feature needs. Don't generalize from N=2; find N=10+ external users via distribution first. Code QUALITY fixes (bugs, blockers) are generalizable; FEATURE decisions should await external signal.

**Q6**: Reference class pattern: Instructor succeeded as thin composable layer ON existing tools, not replacement. httpx succeeded via API-compatibility with requests. hateoas-agent extensibility path: become composable plugin for LangGraph/PydanticAI, not standalone framework competitor. Plugin strategy: 3-5x higher adoption probability than standalone in consolidating market.

#### Dialectical bootstrapping — top 3

**DB1: "Distribution is binding"** — Initial: P(code-only)=5-8%. Self-challenge: Rich went viral from pure quality. Counter: Rich had visual demo appeal; HATEOAS is architectural. Also Rich is N=1; base rate prevails. **Holds at 5-8%.**

**DB2: "Framework absorption risk"** — Initial: P(LangGraph absorbs in 18mo)=30-40%. Self-challenge: HATEOAS enforcement (server declares, LLM never sees invalid tools) is genuinely distinct from LangGraph routing. Fair — more distinct than initially estimated. **Revised 30-40% → 25-35%.**

**DB3: "Don't generalize from N=2"** — Initial: Don't build features for hypothetical users. Self-challenge: Team findings (AsyncRunner coupling, guard observability) ARE generalizable architectural issues. Fair correction. **Revised: quality fixes generalizable; feature decisions require external signal.**

#### Cross-verify
F-RC1 (base rate finding): GPT-4.1 = **AGREE (high confidence)** |source:external-openai-gpt-4.1|

#### Cross-agent convergence notes
- Product-strategist F2 (PyPI unpublished) is THE prerequisite from reference-class perspective — library cannot enter the adoption funnel without it
- Tech-architect F1, UX-researcher F-UX1, technical-writer F1: all real issues, but outside-view frames them as "adoption readiness" not "adoption drivers"
- Product-strategist F4 (model-agnostic Runner): corroborates PM4 scenario — Anthropic lock-in perception is a real adoption filter

#### R3 DA responses

**DA[#1]**: ACKNOWLEDGED — no revision needed. Methodology validated.

**DA[#2] ANA tiering**: DEFEND with CONCESSION. 5 analogues serve different analytical functions: ANA1/2/4 = PRIMARY comparables (directly comparable starting position, realistic vectors). ANA3/5 = BOUNDARY markers (ceiling/category definition). Removing boundary markers would leave reference class without upper/lower bounds. CONCESSION: added explicit PRIMARY/BOUNDARY tiering to prevent anchoring. CAL estimates already excluded boundary analogue success vectors — no numerical revision.

**DA[#3] CAL4 decomposition**: CONCESSION (partial). DA correctly identified "plugin condition doing all the work." Decomposed: P(plugin strategy pursued)=25-35% * P(adoption|plugin achieved)=50-65% = unconditional EV~17%. **CAL4 REVISED: 20-30% → 15-22%** | 80%CI narrowed [10%,45%]→[8%,38%]. Flagged as CONDITIONAL/ASPIRATIONAL. Note: still within original 80%CI — the revision is to point estimate and framing, not a fundamental error.

**DA[#4] Source tags**: CONCESSION (full). Added |source:independent-research| to RC1-RC4, ANA1-ANA5. Added |source:agent-inference| to CAL[], ANA-PATTERN. Cross-verify already tagged |source:external-openai-gpt-4.1|.

**NET R3**: 0 findings changed direction. 1 numerical revision (CAL4: 20-30%→15-22%). 1 structural improvement (ANA tiering). 1 process fix (source tags). DA challenges strengthened precision without changing conclusions.

### devils-advocate

[STATUS] ✓ R2 COMPLETE | 23 challenges issued across 6 agents | XVERIFY-FAIL[openai:gpt-5.1]:parse-error + XVERIFY-FAIL[google:gemini-3.1]:404-model-not-found |→ verification-gap on consensus challenge

#### challenges issued |#23

**tech-architect** |#4: (1)F1 severity inflated — "adoption-blocking" unsupported for N=0 external users, (2)F2-F5 collectively overweight — 4/5 LOW findings, (3)§2d source tags missing — process violation, (4)H2:FALSE contradicts README reality (Model dependency "Any" is false, v0.2 invisible, install broken)

**code-quality-analyst** |#3: (1)CQ1 MEDIUM questionable — 1-line logger.warning fix, correct design conceded, (2)TG1-TG7 COMMENDED as strongest R1 contribution, (3)§2d source tags missing

**ux-researcher** |#4: (1)F-UX1 CONFIRMED as anchor finding — 3-agent convergence, code-verified, (2)F-UX3 premature — WHO needs get_state_map() with N=0 external users?, (3)§2d tags incomplete, (4)F-UX5 is editorial preference not DX finding — Hick's law misapplied

**technical-writer** |#3: (1)F1+F2 CONFIRMED — grep-verified, adoption-blocking, (2)F3 severity inflated — post-adoption object, not blocking, (3)§2d source tags missing entirely

**product-strategist** |#5: (1)!CRITICAL: README "Model dependency: Any" is factually false — trust violation worse than missing feature, (2)PyPI 18 days unfixed — why? Prioritization not technical, (3)CONSENSUS CROWDING: 5/6 agents code-focused despite RCA showing distribution is binding constraint, (4)PM5 "20-line pattern" competitor unaddressed, (5)§2d partial

**reference-class-analyst** |#4: (1)COMMENDED — best R1 contribution, methodology sound, (2)ANA3+ANA5 low-relevance dilutes signal, (3)CAL4 anchored on aspirational condition — P(plugin integration happens) not estimated, (4)§2d tags needed on RC/ANA/CAL

#### prompt audit (§7d)

**prompt language**: "Goal: make this an extensible tool for diverse use cases" + "Output: sigma-build prompt if changes recommended, nothing if no changes needed"
**echo detection**: 5/6 agents concluded "changes recommended." Only RCA challenged whether changes are the right intervention. Prompt framing ("make extensible" + "build prompt if changes") anchors agents toward finding things to fix rather than evaluating whether fixing is the right strategy.
**unverified prompt claims**: H1("library is ready for broader adoption") — prompt frames as hypothesis but agents treat as near-confirmed. 5/6 say PARTIAL, meaning "almost ready, fix these things." RCA correctly challenges: PARTIAL on code quality ≠ PARTIAL on adoption likelihood. These are different questions conflated by H1's framing.
**methodology assessment**: §2d source provenance compliance = 0/6 agents tagged findings per directive. This is the WORST process compliance in any review. All agents did xverify (partial credit) but nobody tagged [independent-research] vs [prompt-claim] vs [agent-inference]. Without source tags, echo detection is harder. The guard-exception-at-DEBUG finding (F-UX1/F3/CQ1) IS genuinely independent research (3 agents found via code reading). The "PyPI not published" finding could be [prompt-claim] echo if the author mentioned it in prior reviews — but source tags would disambiguate.

#### lead-identified tension analysis

**Tension 1: Code improvements vs distribution**
5 agents focus code fixes, RCA says distribution is binding. MY VERDICT: RCA is RIGHT on the analysis, but the tension is partially false. PyPI publish IS distribution (it enters the package into the discovery funnel). README fixes ARE distribution (they're the landing page). The real tension: after PyPI + README, should the next priority be more code fixes (model-agnostic Runner, AsyncRunner refactor) or distribution activities (blog post, LangGraph integration, content marketing)? RCA's data says distribution. 5 agents' instincts say code. I side with RCA's data — but PyPI + README count as BOTH code AND distribution.

**Tension 2: H2 split — tech-architect FALSE(exploration) vs ux-researcher CONFIRMED(lockdown)**
These are NOT contradictory — they're answering different sub-questions. Tech-architect scoped H2 to API internals (filter_actions works correctly = exploration works). UX-researcher scoped H2 to developer experience (guard fails silently = lockdown FEELS broken). HOWEVER: tech-architect's FALSE is too strong because he ignored README as exploration surface. A developer exploring via README gets "Model dependency: Any" (false), no v0.2 mention, and broken install. That IS exploration difficulty. MY VERDICT: H2 = PARTIALLY CONFIRMED for both exploration AND lockdown. Guard observability is the lockdown gap. README accuracy is the exploration gap.

**Tension 3: Model-agnostic Runner — product-strategist HIGH, no independent corroboration**
PS flagged this as HIGH, marked it review-4 unresolved. No other agent independently flagged it. IS this crowding on one agent's priority, or genuine gap? MY VERDICT: the finding is STRENGTHENED by my discovery that README claims "Model dependency: Any" — making this not just a missing feature but an accuracy issue. However, the PRIORITY is debatable. For N=0 external users, model-agnostic Runner is premature optimization. For PyPI launch, it matters because the comparison table makes a false claim. Fix the README claim FIRST (5-minute edit), then build model-agnostic Runner when external demand signals appear.

#### new findings (DA-originated)

**DA-F1 [!HIGH] README "Model dependency: Any" is factually false**
README comparison table claims "Model dependency: Any" for hateoas-agent. Runner requires `anthropic` package. StateMachine/Resource/Registry are model-agnostic but Runner (the only turnkey agent loop) is Anthropic-only. No R1 agent flagged this specific claim as false — product-strategist flagged model-agnostic Runner as MISSING, technical-writer flagged hardcoded model NAME, but neither identified the comparison table as making a competitive claim the code doesn't support.
|source:[independent-research] (README grep + code reading)

**DA-F2 [MEDIUM] §2d source provenance compliance = 0/6**
Zero agents tagged findings with |source:{type}| per directive §2d. This is the worst process compliance observed. All agents completed xverify (partial credit). Without source tags, prompt-echo detection is degraded.
|source:[agent-inference] (workspace audit)

#### agent grades (R1→R2 final)

| Agent | R1 Grade | R2 Final | R2 Rationale |
|-------|----------|----------|--------------|
| tech-architect | B+ | B+ | 2 genuine concessions (F1 severity, H2 scope). Concrete extension scenario defended structural claim. Clean engagement. |
| code-quality-analyst | A- | A | Honest CQ1 concession — presented strongest defense then conceded anyway. TG analysis remains best-in-class. Exemplary. |
| ux-researcher | A- | A- | 2 genuine concessions (F-UX3, F-UX5). F-UX3 partial with concrete-but-narrower users. Good analytical reasoning. |
| technical-writer | B+ | B+ | Clean concessions on F3. Excellent F2 provenance distinction (inferred vs tested). No defensiveness. |
| product-strategist | B+ | A- | README escalation = most important R2 concession. Distribution advisory added. PyPI name-available check showed initiative. Strong improvement. |
| reference-class-analyst | A | A | Best R1 methodology. Non-response to R2 challenges noted but challenges were minor — core analysis accepted by team. |

#### exit-gate verdict

**exit-gate: FAIL → PASS (revised after R2 responses)**

| Criterion | Original | Revised | Basis |
|-----------|----------|---------|-------|
| engagement ≥ B | PASS | PASS | All agents B+ or above; 5/6 responded with genuine revisions |
| unresolved material | FAIL | PASS | README false claim identified+prioritized (PS escalated to CRITICAL), PyPI confirmed no technical blocker |
| untested consensus | FAIL | PASS | Code-priority stress-tested against RCA evidence, distribution advisory (P6) added |
| hygiene | FAIL | PASS | §2d 6/6 retroactively compliant |

**R2 challenge outcomes**:
- 23 challenges issued → 5/6 agents responded
- Severity revisions: F1(M→L), CQ1(M→L), F-UX3(M→L), F-UX5(L→INFO), TW-F3(M→L), PS-F4(H→CRITICAL escalated)
- New finding accepted: DA-F1 README "Model dependency: Any" false → CRITICAL
- Distribution rec added: P6[ADVISORY] comparison blog post
- Grade changes: code-quality-analyst A-→A, product-strategist B+→A-

**Recommendation: SYNTHESIZE. No R3 needed.**

## convergence

## open-questions

## promotion
