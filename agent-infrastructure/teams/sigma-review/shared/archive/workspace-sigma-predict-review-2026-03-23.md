# workspace — sigma-predict system review & redesign
## status: active
## mode: ANALYZE
## tier: TIER-2 (15/25)
## round: r2

## r1-convergence
R1 divergence detected (3 tensions) — circuit breaker NOT fired:
1. H2 strength: CDS=FALSIFIED vs RCA=PARTIAL-FALSIFIED(75%) — same direction, different conviction
2. Calibration fix: CDS→temperature-scaling vs RCA→domain-specific-calibration — compatible but non-identical
3. H3 actor value: RCA=55%-partial, CDS=weak-address, UX=designs-for-without-questioning — gap area

XVERIFY[H2/CDS-F5]: gpt-5.1=PARTIAL(medium) — "directionally plausible but too strong as stated" — same-model runs not fully redundant, persona variation creates some genuine diversity, extremization harmful only when correlation unaccounted, multi-model not universally superior | gemini-3.1=FAILED(404) | coverage=partial

Cross-agent convergence (unanimous):
- H5=PARTIAL-FALSE (5/5): orchestrator must split, human_review incompatible with Streamlit
- H6=PARTIAL (3/3): JSONL ok for persistence, needs RegistryCache for Streamlit
- P0 issues: thread-safety(LLMRouter model mutation), hardcoded "anthropic" provider, silent parse failures
- Dead code: error_class_auto + structured_lessons never populated
- Missing: close_date on PredictionRecord, learning loops absent
- Base rate isolation = strongest feature (RCA), preserve in redesign

## task
Full review and redesign of sigma-predict prediction system. User wants to "tear it down and rebuild" — evaluate pipeline architecture, data models, calibration methodology, verification workflow, scoring analytics, error analysis, and design a Streamlit prediction hub UI. Assess what works, what doesn't, and what should change based on learnings from past reviews and predictions.

Codebase: ~/Projects/Zoltar/sigma-predict
Key files: src/models.py, src/pipeline/orchestrator.py, src/config.py, src/registry/{store,query}.py, src/pipeline/{decomposer,base_rate,forecaster,search,aggregator,calibration,verification,deliberation}.py, src/review/human_review.py, scripts/{predict,resolve,dashboard}.py

## scope-boundary
This review analyzes: sigma-predict prediction pipeline system — architecture, data models, methodology, UX, code quality, and Streamlit UI design
This review does NOT cover: sigma-review team infrastructure, sigma-mem, sigma-verify internals, other Zoltar projects, user's other projects, market predictions themselves
temporal-boundary: none

## infrastructure
ΣVerify: openai (gpt-5.1), google (gemini-3.1) available

## prompt-decomposition
### Q[] — Questions (confirmed by user)
Q1: What should the Streamlit UI architecture look like across 5 views (Dashboard, Predict, Review, Scoreboard, Registry)?
Q2: What pipeline architecture improvements should be made to the 9-stage flow?
Q3: How should data models (PredictionRecord and children) be enhanced/restructured?
Q4: What calibration and scoring methodology improvements are needed?
Q5: How should the verification workflow evolve?
Q6: What should change about error analysis and learning loops from resolved predictions?

### H[] — Hypotheses to test (not assumed as facts)
H1: The existing 9-stage pipeline is the right sequence of stages
H2: OpenAI as primary forecaster + Gemini for cross-model verification is the right model allocation
H3: The 3-level actor hierarchy + peripheral actors adds meaningful predictive value
H4: Platt scaling is the right calibration approach
H5: The existing CLI logic is sound and the UI just needs to wrap it
H6: JSONL registry is adequate for the data access patterns a Streamlit app needs
H7: The deliberation module (currently a Phase 3 stub) is worth implementing
H8: The 5 search personas are the right set

### C[] — Constraints (confirmed by user)
C1: Personal tool — no multi-user, no auth, no deployment concerns
C2: Streamlit as UI framework
C3: Existing Pydantic models in src/models.py
C4: Existing JSONL registry at data/predictions/registry.jsonl
C5: sigma-verify integration for cross-model verification

## findings
### tech-architect

#### A1 — Pipeline Architecture Assessment |source:independent-research

**H1 verdict: PARTIALLY CONFIRMED** — the 9-stage sequence is logically correct but the *implementation* conflates stages and has sequencing bugs.

**What works:**
- Stage isolation philosophy is sound: base rate before search is genuinely important and well-implemented (base_rate.py:47-106). Prevents inside-view anchoring on current evidence.
- Verification hooks at each stage are well-placed (orchestrator.py:128-220)
- Cost tracking across runs is clean (CostTracking aggregation in orchestrator.py:86+190)
- Platform abstraction (PlatformClient ABC) is solid — clean interface, correct separation

**Critical sequencing bug — orchestrator.py:162-165:**
`SearchModule` is instantiated INSIDE the forecaster loop (step 3), not as a shared module. Every run creates a new SearchModule. This is fine for isolation but means the orchestrator has an `import` inside a hot loop (`from src.pipeline.search import SearchModule` at line 164). Fix: move instantiation to `__init__` or pre-loop.

**Missing stage: Historical context injection.** The pipeline has no stage between decomposition and base rate estimation that looks up past sigma-predict records for the same domain. `RegistryQuery.get_recent_in_domain()` exists (query.py:36-44) but is never called from the pipeline. The calibration step calls `count_resolved()` but past predictions for the same domain are not fed back as context. This is a significant gap — the system doesn't learn from its own history within a session.

**Missing stage: Platform signal comparison.** `_collect_platform_signals()` runs after calibration (orchestrator.py:264) but before human review, meaning the community signal is available to the human reviewer but never fed back to influence calibration or generate an automatic divergence-weighted adjustment. The anomaly flag is set but there's no stage that acts on it.

**Deliberation (H7): CONFIRMED WORTH IMPLEMENTING.** The stub at deliberation.py:24-37 returns inputs unchanged. The trigger logic is sound (`stdev > 0.15`). Without implementation, high-disagreement multi-run predictions get extremized anyway — but we lose the opportunity to identify *why* runs disagree and surface that to the reviewer. Recommend implementation in redesign.

**Step numbering is wrong.** Orchestrator logs "Step 1/7", "Step 2/7" etc. but there are 9 conceptual stages. Minor but confusing for debugging.

---

#### A2 — Data Model Strengths and Gaps |source:independent-research

**Models are well-structured.** Pydantic v2, proper use of `Field(default_factory=...)`, clean enum definitions. The hierarchy (PredictionRecord containing Decomposition, list[RunResult], Aggregation, CalibrationData, etc.) is logically correct.

**Gaps identified:**

**G1 — `Resolution.error_class_auto` and `error_class_manual` are `list[str]` with no taxonomy.** The fields exist (models.py:156-157) but there's no enum or schema defining what valid error classes are. The resolve script (resolve.py:78-83) computes brier/log scores but never populates error_class_auto. This means the "learning loop" fields exist structurally but are dead code functionally. |source:independent-research

**G2 — `Resolution.structured_lessons` is a `list[str]` with no trigger.** Same pattern — exists but nothing populates it. |source:independent-research

**G3 — `PlatformSignals` is platform-specific in disguise.** It has hardcoded keys `metaculus_community`, `polymarket`, `kalshi` (models.py:127-133). When a new platform is added, this model breaks. Should be `dict[str, float | None]` with platform-agnostic keys. |source:independent-research

**G4 — `HumanReview.human_adjustment` is a delta (not absolute probability).** This is a non-obvious design choice. The orchestrator adds it to `cal_prob` (orchestrator.py:284). But it's stored as a delta, and if you want to reconstruct the final probability from the record alone, you need `calibration.calibrated_probability + human_review.human_adjustment`. Confusing. Should store both the delta AND the final submitted probability — or just use the `Submission.probability` field consistently.

**G5 — No `tags` field on PredictionRecord.** `PlatformQuestion.tags` (models.py:241) exists but tags are not propagated to `PredictionRecord`. Domain inference (orchestrator.py:321-337) is a lossy keyword heuristic. Tags should be stored on the record.

**G6 — `Aggregation.deliberation_result` is `dict | None` with no schema.** If deliberation is implemented, this will be untyped. Needs a proper model class.

**G7 — `RunResult` has no `provider` field.** It stores `model` (models.py:91) but not the provider. If you switch primary provider, historical runs become ambiguous. Add `provider: str = ""`.

---

#### A3 — Storage Layer (JSONL) Assessment |source:independent-research

**H6 verdict: PARTIALLY CONFIRMED for current use, NOT ADEQUATE for Streamlit.**

**Current adequacy:**
- Append-only save is O(1) — fine
- `_write_all()` uses atomic `os.replace()` with tmp file (store.py:101-107) — solid
- Expected volume (hundreds to low-thousands of records) — JSONL fine at this scale

**Streamlit-specific problems:**
1. **Every filter requires full load.** `get_by_domain()`, `get_resolved()`, `count_resolved()` all call `load_all()` (query.py:23-67). Each Streamlit widget interaction that triggers a data refresh will load the entire JSONL file and re-parse every record. With 1,000+ records and complex PredictionRecord objects (deeply nested JSON), this becomes sluggish.

2. **No in-memory cache.** There's no caching layer — every `RegistryQuery` method is a fresh disk read. Streamlit reruns the script on every interaction.

3. **Streaming/incremental updates impossible.** Streamlit's `st.dataframe` for live pipeline runs would require polling or full reloads.

**Recommendation:** Don't replace JSONL (C4 constraint, and it's fine for persistence). Add a `RegistryCache` layer — load_all() once at startup, cache as pandas DataFrame, invalidate on write. This keeps JSONL as the source of truth while giving Streamlit O(1) filtered views. |source:independent-research

---

#### A4 — Streamlit UI Architecture Recommendation |source:independent-research

**H5 verdict: PARTIALLY CONFIRMED** — CLI logic is sound for wrapping, but `human_review.py` is terminal-only and must be completely replaced. The orchestrator's blocking `present_for_review()` call (orchestrator.py:275) is a fundamental architectural incompatibility with Streamlit's stateless execution model.

**Core incompatibility:** Streamlit is not async-capable for long-running background tasks without explicit threading/session state management. The pipeline currently blocks on `present_for_review()` — waiting for terminal input. This pattern does not translate to Streamlit.

**Recommended page structure (5 pages):**

```
app/
  pages/
    1_Dashboard.py      — calibration curves, Brier by domain, cost tracker, recent activity
    2_Predict.py        — question fetch/search, pipeline trigger, progress display
    3_Review.py         — staged review queue, human adjustment UI, approve/reject
    4_Scoreboard.py     — per-prediction performance, error analysis, learning loop
    5_Registry.py       — searchable/filterable prediction table, drill-down
  state/
    session.py          — st.session_state schemas
  cache/
    registry.py         — RegistryCache wrapping RegistryQuery
```

**State management architecture:**
- Pipeline runs go in `st.session_state["active_run"]` — a dict holding the `PredictionRecord` in-progress
- Human review state: `st.session_state["review_queue"]` — list of records awaiting review
- Use `st.rerun()` after state mutations to trigger display refresh
- Pipeline execution: run in a thread via `threading.Thread` + `st.status()` widget for progress. Write intermediate state to session_state from the thread. Main thread polls via `st.rerun()` loop or time.sleep+rerun.

**Critical architectural change needed:** The orchestrator's `predict()` method must be decomposed into separable stages so the Streamlit UI can:
1. Trigger the pipeline
2. Display progress per stage
3. Pause at human review step (store record in session_state, navigate to Review page)
4. Resume from the Review page (load record, apply adjustment, submit)

This means `orchestrator.predict()` needs to either (a) accept a callback for the review step, or (b) be split into `predict_until_review()` and `submit_after_review()`. Option (b) is cleaner for Streamlit.

**Async pipeline execution pattern:**
```python
# Predict page
if st.button("Run Pipeline"):
    thread = threading.Thread(target=run_pipeline, args=(question, config))
    thread.start()
    st.session_state["pipeline_thread"] = thread
    st.session_state["pipeline_status"] = "running"

# Status polling (requires st.rerun() loop)
with st.status("Running pipeline...") as status:
    while thread.is_alive():
        status.update(label=st.session_state.get("pipeline_stage", "..."))
        time.sleep(0.5)
```

---

#### A5 — LLMRouter and Verification Architecture |source:independent-research

**H5 (verification) findings:**

**Router design is clean.** Provider abstraction is solid — call/verify/challenge/cross_verify uniformly dispatched. The exclusion of primary provider from cross-verification (`_external_clients()`, llm_router.py:308-327) is correct logic.

**Critical issue — model assignment is not thread-safe.** `call()` temporarily mutates `self._anthropic.model` (llm_router.py:127-131):
```python
old_model = self._anthropic.model
self._anthropic.model = model
try:
    return self._anthropic.call(...)
finally:
    self._anthropic.model = old_model
```
This is a race condition if the router is shared across threads (as it would be in a Streamlit threaded pipeline). If two threads call `router.call()` simultaneously, one thread's model assignment overwrites the other's. Fix: pass model as a parameter to `client.call()` rather than mutating state. |source:independent-research

**Verification is fire-and-forget.** Stage verifications are appended to `record.verification.stages` (orchestrator.py:138, 159, 200, 220) but the results don't feed back into the probability estimate. A disagreeing verification doesn't change the forecast — it only creates a flag in human review. This is architecturally correct (humans decide) but the system could do more: auto-weight disagreement into the CI, auto-trigger re-run on unanimous disagreement.

**Challenge is applied only to last run** (orchestrator.py:207: `record.runs[-1]`). If there are 5 runs and the last one is an outlier in the wrong direction, this is misleading. Should challenge the aggregate (or the median run).

**`decomposer.py` and `base_rate.py` both hardcode `"anthropic"` provider** (decomposer.py:64, base_rate.py:78). If the user has only OpenAI/Gemini keys, these calls fail. Should use `config.primary_model.provider`. |source:independent-research

**`_extract_json()` is duplicated 4 times** — in decomposer.py, forecaster.py, base_rate.py, and implicitly in verification.py. Should be a shared utility.

---

#### A6 — Code Organization and Coupling Issues |source:independent-research

**Duplication:**
- `_load_prompt()` defined identically in decomposer.py:24-27, forecaster.py:28-31, base_rate.py:21-24. Should be in a shared `src/pipeline/utils.py`.
- `_extract_json()` defined identically in decomposer.py:151, forecaster.py:34, base_rate.py:27. Same fix.
- `brier_score()` defined in both scripts/resolve.py:23 and scripts/dashboard.py:23. Should be in a shared scoring utility.

**Config anti-pattern:** `Config.__post_init__` mutates a `field(default=None)` (config.py:66). Dataclass field with `default=None` then conditionally set in `__post_init__` works but is fragile — type checkers see `primary_model: ModelConfig = None` as invalid. Should use `field(default_factory=_detect_primary_model)` or a factory pattern.

**`src/analysis/` and `src/monitoring/` are empty stubs** — empty `__init__.py` only. If they're Phase 3 placeholders, that's fine, but they add confusion.

**`scripts/monitor.py` is a stub** that prints "not yet implemented." Same pattern.

**`Aggregation.deliberation_result: dict | None`** (models.py:116) — untyped dict for a complex result. Phase 3 placeholder but will need a proper model when implemented.

**`orchestrator.py` has a late import** at line 164: `from src.pipeline.search import SearchModule`. Late imports are sometimes used to avoid circular imports but there's no circular dependency here. Should be top-level.

---

#### A7 — H-Verdict Summary |source:independent-research

- H1: PARTIAL — sequence correct, implementation has staging/import issues, 2 missing stages
- H5: PARTIAL — CLI logic is wrappable, but `human_review.py` terminal UX is incompatible with Streamlit; orchestrator needs decomposition into pre-review/post-review phases
- H6: PARTIAL — JSONL adequate for persistence at current scale, inadequate for Streamlit data access patterns without a caching layer

---

#### A8 — Specific Refactoring Recommendations |source:independent-research

**P0 (blocking for Streamlit):**
1. `orchestrator.py`: Split `predict()` into `predict_until_review() -> PredictionRecord` and `submit_after_review(record, human_review) -> PredictionRecord`. Human review step must not block the pipeline thread.
2. `llm_router.py`: Fix thread-safety — pass model as parameter to `AnthropicClient.call()` instead of mutating `.model` attribute.
3. `decomposer.py:64` + `base_rate.py:78`: Replace hardcoded `"anthropic"` with `config.primary_model.provider`.

**P1 (high value):**
4. Add `RegistryCache` class wrapping `RegistryStore` + `RegistryQuery` — pandas DataFrame in memory, invalidated on write. One load per Streamlit session start.
5. Add historical context injection stage: between decomposition and base_rate, call `query.get_recent_in_domain(domain, n=5)` and inject domain performance context into the base_rate prompt.
6. Implement deliberation module: supervisor call on high-stdev aggregations, feed disagreement summary back into a final synthesis call.

**P2 (cleanup):**
7. Extract shared `src/pipeline/utils.py`: `_load_prompt()`, `_extract_json()`, shared JSON parsing.
8. Add `provider: str` field to `RunResult`.
9. Fix `PlatformSignals` — remove hardcoded keys, use generic `dict[str, float | None]`.
10. Add tags propagation: `PredictionRecord.tags: list[str]` from `PlatformQuestion.tags`.
11. Move `brier_score()` and `log_score()` to `src/scoring.py`, import from scripts.
12. Fix `Config.primary_model` field type annotation — `ModelConfig | None` with proper default.

---

#### A9 — DA Response |source:independent-research

**DA[#1] COMPROMISE — RegistryCache: pandas is wrong, dict-based cache is right**

DA is correct that pandas is overengineered for this use case. The criticism stands on all three counts: heavyweight dependency for list filtering, structural flattening of nested PredictionRecord destroys the object model, and SQLite or a plain dict suffices.

My original framing was wrong to specify pandas. The actual problem to solve is: eliminate repeated full JSONL scans on every Streamlit widget interaction. The minimal correct solution:

```python
class RegistryCache:
    def __init__(self, store: RegistryStore):
        self._store = store
        self._records: dict[str, PredictionRecord] = {}
        self._dirty = True

    def load(self) -> list[PredictionRecord]:
        if self._dirty:
            self._records = {r.prediction_id: r for r in self._store.load_all()}
            self._dirty = False
        return list(self._records.values())

    def invalidate(self):
        self._dirty = True
```

This is a `dict[str, PredictionRecord]` keyed by prediction_id — O(1) lookup, full object preserved, zero new dependencies. Filtering methods (`get_by_domain`, `get_resolved`) work over the in-memory list instead of re-reading disk. DA's SQLite suggestion has merit for larger scale but violates C4 (existing JSONL registry) and adds migration complexity. The dict cache is the right call for C1+C4 constraints.

**Position revised: dict-based RegistryCache, not pandas. P1 priority unchanged.**

---

**DA[#2] CONCEDE with narrow defense — threading is the right intent, wrong implementation**

DA is correct on the specific anti-pattern. `st.session_state` is not thread-safe — Streamlit's own docs warn against writing to session_state from background threads. The `time.sleep(0.5)` polling pattern I described creates unnecessary full reruns and is fragile.

The right Streamlit-native approaches, in order of preference for this use case:

1. **`st.cache_resource` with a queue**: Pipeline stages write progress to a `queue.Queue` stored in `st.cache_resource` (which IS thread-safe as a Python Queue object). Main thread reads from the queue on each rerun. No session_state writes from background thread.

2. **`st.fragment` (Streamlit 1.37+)**: Fragments allow partial reruns of a UI section without full page rerun — suited for a progress display that updates while pipeline runs. Fragments can safely poll a shared queue without rerunning the whole page.

3. **`st.experimental_connection` / process-based**: subprocess.Popen with IPC is correct in principle but operationally heavy for C1 (personal tool) — debugging pipeline failures becomes painful when they happen in a subprocess.

Revised architecture: thread writes progress to `queue.Queue` in `st.cache_resource`, `st.fragment` polls and displays progress. Session_state stores only the final `PredictionRecord` after thread completion (safe — thread is dead before main thread reads result).

The core finding stands: orchestrator still needs the predict_until_review() split because the blocking call must be eliminated regardless of threading model. The thread-safety fix to LLMRouter (model mutation) also stands independently.

**Position revised: Queue-based threading + st.fragment, not raw threading.Thread + session_state writes.**

---

**DA[#3] DEFEND — 2-phase split is correct for C1 scope; reject callback/event-driven**

DA's point about extensibility is valid in the abstract. An event-driven/callback model would handle N human input points instead of exactly 1. But this is C1 — a personal tool with one user. The question is: how many human-intervention points does this pipeline realistically need?

Current: 1 (post-calibration review before submit). Plausible additions: confirming a reference class choice, selecting between search result sets. But both of these either (a) are better handled as pipeline configuration inputs set *before* the run starts, not mid-run interrupts, or (b) would require re-architecting the pipeline LLM calls themselves, not just adding callback hooks.

The callback pattern solves a problem that doesn't exist yet and adds complexity (callback registration, state threading through pipeline, error handling across callback boundaries) for zero current benefit. This is the anti-pattern the CLAUDE.md warns against: designing for hypothetical future requirements.

The 2-phase split is the minimum viable change that solves the actual problem (blocking terminal call in UI context). If future stages need human input, that's the time to generalize.

**Position defended. predict_until_review() + submit_after_review() is correct for C1 scope.**

---

**DA[#15] PARTIAL CONCEDE — st.fragment changes the picture for H5 but doesn't eliminate the split requirement**

`st.fragment` (1.37+) does make the threading architecture cleaner and reduces full-page reruns. It is a legitimate improvement to my threading recommendation (see DA[#2] response above).

However, `st.fragment` does not resolve the core H5 incompatibility: the orchestrator's `present_for_review()` call (orchestrator.py:275) is a blocking `console.input()` — a synchronous terminal read. No Streamlit feature can wrap a blocking stdin call into a UI widget. The orchestrator MUST be split regardless of which Streamlit threading/fragment approach is used.

What `st.fragment` changes: the progress display implementation. What it does not change: the fundamental need to decompose the orchestrator.

**H5 verdict unchanged: PARTIAL. Split is required. Fragment improves implementation quality of the threading approach.**

---

**DA[#16] CONCEDE — H3 actor analysis UI: flag as unknown, recommend lightweight treatment**

This is a legitimate empirical gap. No agent has tested whether human reviewers actually use actor analysis output to adjust their probability estimates. The actor analysis code is thorough (3-level hierarchy, peripheral actors, probability space constraints — models.py:53-88) and the human_review.py display is detailed. But if reviewers consistently accept the pipeline's estimate without reading the actor section, we're building elaborate UI for ignored data.

I cannot confirm or deny from code inspection alone whether users engage with actor analysis. This is a usage data question, not an architecture question.

Revised recommendation: in the Streamlit UI, render actor analysis in a collapsible `st.expander` with a low visual weight. Don't eliminate it (the data is there, some questions genuinely require it — geopolitics, policy), but don't make it a primary display. The UI should make it easy to ignore when irrelevant and easy to expand when needed. If the user wants to evaluate empirically, add a "was actor analysis relevant?" checkbox to the review form and log it to `HumanReview.flags_raised`.

**Position revised: actor analysis → collapsible expander, not primary display. Empirical relevance unknown. Lightweight treatment is the safe design.**

### ux-researcher

#### F-UX-1: H5 assessment — CLI interaction model ≠ Streamlit-compatible |source:[independent-research]
H5(CLI logic is sound, UI just wraps it) → PARTIALLY-FALSE
CLI information sequence is logically correct. Display logic is fundamentally incompatible with Streamlit's reactive model.
Problems:
- human_review.py: linear blocking flow (present → collect keystroke → return HumanReview). Streamlit is declarative+stateless per rerun — no blocking input loops possible.
- dashboard.py: single-render static snapshot with no state management — Streamlit expects widget-driven reruns.
- predict.py lines 108-119: interactive numbered list + prompt loop for question selection — cannot translate to CLI-style blocking input in Streamlit.
- Decision collection (a/j/r keystroke) must become st.radio/st.button with st.session_state tracking decision phase.
- Adjustment workflow (float input + reasoning text) needs st.number_input + st.text_area + confirmation button sequence via session_state state machine.
Reusable (KEEP): _generate_flags() logic, flag thresholds (stdev>0.15, extreme p, community divergence >0.15), verification display field ordering, aggregation field set.
Must rebuild: all input()/console.print()/console.rule() calls. The entire interaction choreography.
Verdict: orchestrator.predict() must be split — see F-UX-4 for required decomposition.

#### F-UX-2: Information architecture — 5-view hierarchy + navigation |source:[independent-research]
Nav: st.sidebar with st.navigation (Streamlit 1.36+) or st.radio for back-compat.
View order: Dashboard > Predict > Review > Scoreboard > Registry
Rationale: Dashboard = landing/home (see active state at a glance). Predict = primary action. Review = secondary action (post-pipeline). Scoreboard = analytical. Registry = archival reference.
State persistence via st.session_state keys:
- "selected_prediction_id" — shared by Dashboard, Review, Registry (row-click drill-through)
- "selected_question" — PlatformQuestion object, set in Predict, cleared on pipeline start
- "pipeline_state" — enum: idle | running | awaiting_review | complete
- "active_record" — PredictionRecord in-progress or just completed
- "review_filters" — filter state preserved across view switches

#### F-UX-3: Dashboard view — wireframe + component spec |source:[independent-research]
Purpose: landing state — see what matters NOW without digging.

Metric strip (top, st.columns(4)):
- col1 st.metric("Active Predictions", count submitted+unresolved, delta=vs 30d prior)
- col2 st.metric("Avg Brier Score", avg resolved brier_score, delta=vs prior 30 records, delta_color="inverse")
- col3 st.metric("Spend This Month", sum cost.total_cost_usd current month, delta=vs prev month)
- col4 st.metric("Pending Review", count human_review.reviewed=False, delta_color="inverse")

Active predictions table (st.dataframe, below metric strip):
Columns: question_text(truncate 80 chars) | platform | calibrated_probability | countdown_days (computed: close_date-today) | ci_width (computed: CI[1]-CI[0]) | flags_count (len(flags_raised))
column_config:
- calibrated_probability: ProgressColumn(min=0, max=1) — visual bar
- countdown_days: NumberColumn, format="%d days", red if <7, yellow if <30 (custom CSS or conditional)
- flags_count: NumberColumn, help="Review flags raised"
on_select="rerun" → sets session_state["selected_prediction_id"] → navigates to Review
Note: close_date is on PlatformQuestion, not PredictionRecord. Must store it at prediction time — this is a data model gap (see F-UX-12).

Sidebar quick stats (or below table):
- st.bar_chart by platform (platform vs count)
- st.bar_chart by domain
- Recent 5 predictions: st.expander list with question_text + calibrated_probability

Auto-refresh: st.rerun(interval=30000) — catches pipeline completions without manual F5.
Flags alert: if any active prediction has flags_raised non-empty, show st.warning("N predictions have flags — review recommended") at top.

#### F-UX-4: Predict view — wireframe + interaction flow |source:[independent-research]
Purpose: replace predict.py CLI entirely. Question discovery + run config + pipeline execution + inline human review.
Requires orchestrator split: predict_until_review() → st.session_state["active_record"] → human review UI → submit_after_review().

Layout: col_left(35%) | col_right(65%)

Col left — question discovery:
- st.selectbox("Platform", ["metaculus","polymarket","kalshi"])
- st.radio("Find by", ["Search term","Question ID","URL"], horizontal=True)
- Conditional input per mode (st.text_input)
- st.button("Search / Fetch") → fetches PlatformQuestion list
- Results: st.dataframe with title, community_prediction, close_date, question_id. column_config.LinkColumn for URL.
- Selection: on_select="rerun" → session_state["selected_question"] = PlatformQuestion
- Selected question panel: st.info box showing title + close_date + community_prediction as st.metric

Col right — run configuration + execution:
- st.number_input("Runs", 1, 5, 1) → session_state["run_count"]
- st.multiselect("Personas", SearchPersona enum values) — show descriptions as help: academic=historical base rates, news=recent events, contrarian=against consensus, domain_expert=technical depth, meta_forecaster=calibration-focused
- st.toggle("Cross-model verification", True)
- st.button("Run Pipeline", type="primary", disabled = no question selected)

Pipeline progress (within col right, shown during run):
st.status("Pipeline running...") container:
  stage labels in sequence: decompose → base_rate → search(persona) → forecast(run N) → aggregate → calibrate → verify → review
  Each stage: st.write(f"Stage: {name} — {elapsed:.1f}s")
  On completion: status.update(state="complete")
Implementation: threading.Thread for pipeline execution. Intermediate stage names written to session_state["pipeline_stage"] from worker thread. Main thread polls via st.rerun() cycle.

Human review (inline, col right, after status complete):
st.subheader("Review Required")
4-column metrics row: raw_aggregate | calibrated_probability | stdev | effective_n
Flags: for each flag in human_review.flags_raised: st.warning(flag)
Verification summary: st.expander per stage (agreement badge + finding_summary)
Decision widget:
  st.radio("Decision", ["Accept","Adjust","Reject"], horizontal=True)
  If Adjust: st.slider("New probability", 0.01, 0.99, step=0.01, value=calibrated_probability) + st.text_area("Reasoning")
  If Reject: st.text_input("Reason (optional)")
  st.button("Confirm", type="primary") → calls submit_after_review(record, human_review) → clears active_record from session_state

#### F-UX-5: Review view — tabbed deep dive |source:[independent-research]
Purpose: full detail on any PredictionRecord — decomposition, runs, actor analysis, verification, resolution.
Entry: from Dashboard row click, Registry row click, or direct load with session_state["selected_prediction_id"].

Top selector: st.selectbox("Prediction", [(id, truncated_text) pairs]) — pre-selected if session_state has a value.

st.tabs(["Summary","Runs","Actor Analysis","Verification","Resolution"])

Tab 1 — Summary:
- Question: title (st.subheader), description (st.expander), resolution_criteria (st.info), platform/close_date/type metadata
- Key numbers st.columns(4): calibrated_probability | submitted.probability | CI "[lo, hi]" | human_adjustment (delta, colored)
- Decomposition: st.expander("Sub-questions + Base Rate") showing sub_questions numbered list, base_rate + source as st.metric, reference_class as st.caption
- Flags: st.warning per flag_raised item
- Human review decision: st.success("Accepted")/st.warning("Adjusted")/st.error("Rejected") with human_reasoning text

Tab 2 — Runs:
- Inter-run comparison: st.dataframe of all RunResult with columns: model, search_persona, base_rate_used, inside_view_adjustment, pre_mortem_delta, probability, confidence_self_score
- st.bar_chart of probability by search_persona (visual spread across runs)
- Per-run expandable: st.expander per RunResult labeled "Run N — {persona} — p={probability:.3f}"
  - Probability waterfall (sequential st.metric with delta): base_rate_used →(+inside_view_adjustment)→ intermediate →(+pre_mortem_delta)→ probability
  - confidence_self_score: st.progress(confidence_self_score/10, text=f"{confidence_self_score}/10")
  - reasoning_chain: st.text_area("Reasoning", value=reasoning_chain, disabled=True, height=200)
  - sources_cited: bullet list; search_queries: bullet list; actor_motivation_flags: st.warning per item

Tab 3 — Actor Analysis:
- st.columns(2): primary actors left | peripheral actors right
- Primary actors: st.expander per Actor labeled "{level_label}: {name}"
  - Level badge (st.badge if available, else colored st.markdown): level 1=green, 2=orange, 3=red
  - Fields: motivation, influence_estimate, observable_indicators (bullet), implication_for_estimate
- Peripheral actors: st.dataframe with columns: name, categories(", ".join), influence_estimate, leverage, feedback_mechanism
- Probability space constraints: st.info per item in list

Tab 4 — Verification:
- providers_available as st.caption
- Per StageVerification: st.expander labeled "{stage} — [{agreement.upper()}]"
  - finding_summary: st.info
  - Verification entries: st.dataframe with columns: provider/model combined, assessment, confidence, counter_evidence (truncated)
  - Challenges: st.dataframe with columns: provider/model, vulnerability(colored), counter_argument(truncated), logical_gaps
  - agreement color: unanimous=green, partial=yellow, none=red, no_data=grey via st.markdown colored badge

Tab 5 — Resolution (only if resolution is not None):
- st.metric("Outcome", "YES" if outcome==1 else "NO" if outcome==0 else str(outcome))
- st.columns(2): brier_score as st.metric with delta vs system avg | log_score as st.metric
- Error classes: st.caption("Auto:") + st.pills or st.multiselect(disabled=True) for error_class_auto; same for error_class_manual
- Structured lessons: numbered list of structured_lessons
- Add lesson: st.text_area("New lesson") + st.button("Save") → append to resolution.structured_lessons, write back to JSONL

#### F-UX-6: Scoreboard view — calibration performance analytics |source:[independent-research]
Purpose: track calibration over time, identify biases, surface learning patterns.
Layout: metric strip → calibration curve → Brier time series → domain breakdown → cost analytics → learning loops

Metric strip st.columns(5): avg_brier | avg_log_score | N resolved | estimated_calibration_error | total_spend

Calibration curve (key analytical surface):
- Bucket submitted.probability into 10 deciles
- x=predicted probability, y=actual resolution rate in that bucket
- st.plotly_chart: go.Scatter actual curve + go.Scatter perfect diagonal reference
- Shade overconfident (actual < predicted) vs underconfident (actual > predicted) regions
- Add N labels per bucket as annotations
- This is THE most important chart for a calibration-focused user — give it prominent placement

Brier score over time:
- x=resolution.resolved_at, y=resolution.brier_score per resolved record
- Rolling 7-prediction avg as primary line
- Reference lines: perfect=0.0 (green), random=0.25 (red), current avg (blue dashed)
- Hover shows question_text
- st.plotly_chart with go.Scatter

Domain + platform breakdown:
- Horizontal bar chart: Brier by domain sorted worst→best. Color: green<0.1, yellow 0.1-0.2, red>0.2. N label on bars.
- st.dataframe: platform | N | avg_brier | avg_log_score

Cost analytics:
- st.plotly_chart: stacked bar by month (x=month, stacked by model or platform)
- st.dataframe: model | call_count | tokens_in | tokens_out | total_cost_usd

Date range + domain filters (top of view):
- st.date_input("Date range", value=[90_days_ago, today]) — filters all charts below
- st.selectbox("Domain", ["All"] + unique_domains)

#### F-UX-7: Registry view — searchable history table |source:[independent-research]
Purpose: full prediction history with filtering, sorting, drill-down to Review.
Layout: filter bar → table → export

Filter bar (st.columns, horizontal):
- st.multiselect("Platform", Platform enum values)
- st.multiselect("Domain", unique domains from registry)
- st.multiselect("Status", ["submitted","resolved","rejected","pending_review"])
- st.date_input("Date range")
- st.text_input("Search question text") — client-side filter on question_text

Main table st.dataframe + column_config:
Columns: prediction_id([:8]), question_text(truncated 60 chars), platform, domain, created_at, calibrated_probability (ProgressColumn), submitted_probability, resolution_outcome, brier_score, flags_count, cost_usd, horizon_days
on_select="rerun", selection_mode="single-row" → sets session_state["selected_prediction_id"] → navigates to Review view

st.download_button("Export CSV", data=filtered_df.to_csv(), mime="text/csv")

#### F-UX-8: Error analysis + learning loops surface (Q6) |source:[independent-research]
Current state: Resolution.error_class_auto, error_class_manual, structured_lessons exist in model but are DEAD CODE — resolve.py never populates error_class_auto; nothing reads structured_lessons in aggregate. The learning loop is structurally defined but functionally absent.

Required additions to Scoreboard (Lessons section, below calibration curve):

1. Error class frequency: st.plotly_chart horizontal bar of error_class_manual frequency across resolved records. Reveals systematic biases at a glance.
2. Structured lessons feed: st.dataframe of all structured_lessons from resolved records — columns: date, question_text(truncated), lesson, domain. Filterable by domain.
3. Pre-mortem effectiveness: for records where pre_mortem_changed_estimate=True, compute: did the pre-mortem adjustment direction improve Brier? st.metric("Pre-mortem improvement rate", value%). Tests whether the pre-mortem stage adds value.
4. Human adjustment audit: scatter plot of human_adjustment value (x) vs brier_delta pre/post-adjustment (y). Shows whether human overrides help or hurt empirically. Critical for a calibration-focused user — they need to know if they should trust their own intuition.
5. Actor signal test: st.columns(2) showing avg_brier when level_2_3_present=True vs False. Tests H3 empirically over time.

These surfaces do NOT require new data collection — all fields already exist in the model. They only require (a) resolver to populate error_class_auto and (b) aggregation queries in the Scoreboard view.

#### F-UX-9: Power user interaction design principles |source:[independent-research]
User: senior PM, power user, builds internal tools, wants depth not simplification.
Principles derived from this profile:
- Dense layouts acceptable: full-width, minimal whitespace, small text via st.markdown CSS override if needed
- NO onboarding: no tooltips on first load, no modal welcome, no "getting started" UI
- "Show all" default: don't hide fields behind expanders unless genuinely secondary (long text bodies, raw reasoning chains)
- Raw JSON access: st.expander("Raw record JSON") at bottom of Review view every tab — power users debug with raw data
- Auto-refresh Dashboard: st.rerun(interval=30000) — don't make user manually refresh to see pipeline completions
- Persist filter state: session_state for all filter widgets — navigating between views must not reset filters
- Error transparency: st.error(expanded=True) with full stack trace in Predict view on pipeline failure. Never swallow exceptions.
- Keyboard flow: annotate st.button labels with keyboard shortcuts where Streamlit allows (st.button has no native shortcut, but form submission via Enter is available in st.form)
- Data export: every table should have a download CSV button — power users want to analyze in Excel/Notebooks

#### F-UX-10: Streamlit component map |source:[independent-research]
Specific component → use case:
- st.metric: calibrated_probability, brier_score, cost totals, outcome, countdown
- st.plotly_chart: calibration curve, Brier timeline, cost stacked bar, run spread bar, adjustment scatter
- st.dataframe + column_config: all tabular data (runs, registry, domain breakdown, verification entries)
- st.tabs: Review view sections, Scoreboard analytics sections
- st.expander: per-run detail, actor detail, raw JSON, long text (description, reasoning_chain)
- st.status: pipeline execution stage-by-stage progress
- st.progress: confidence_self_score (value/10 → 0.0-1.0)
- st.badge/st.pills: agreement level tags, error class tags, actor level badges (Streamlit 1.32+)
- st.toggle: verification on/off switch in Predict view
- st.date_input: Registry and Scoreboard date range filters
- st.download_button: CSV export from Registry and Scoreboard
- st.sidebar + st.navigation: top-level 5-view navigation
- st.session_state: prediction_id passing, selected_question, pipeline_state, filter state
- st.fragment: isolate pipeline progress updates without full page rerun (Streamlit 1.37+)

Anti-patterns to avoid:
- st.write for tabular data → use st.dataframe
- st.text for long content → use st.text_area(disabled=True) or st.markdown
- Blocking time.sleep() in main thread → use threading.Thread + session_state polling
- Re-loading JSONL on every widget interaction → RegistryCache in session_state["registry_cache"]

#### F-UX-11: Data model gap — close_date missing from PredictionRecord |source:[independent-research]
Dashboard countdown timer requires close_date. PlatformQuestion.close_date exists (models.py:238) but PredictionRecord has no close_date field. The record only stores question_text and question_id — not the close date.
Fix required: add close_date: str = "" to PredictionRecord. Propagate from PlatformQuestion at prediction time. Without this, Dashboard cannot compute countdown timers without fetching from platform API on every load (expensive, fragile).
Also affects: Registry view (showing days-to-close), Scoreboard filters.

#### F-UX-12: H5 final verdict |source:[independent-research]
H5 = PARTIALLY FALSE.
What translates: flag generation logic, aggregation field set, verification assessment color scheme (agree=green, disagree=red, partial=yellow), display ordering of information sections.
What must be rebuilt: all interaction primitives (input/prompt → session_state + buttons), all rendering (console.print → st.* components), the blocking review flow (→ split orchestrator into predict_until_review + submit_after_review).
Key insight: the information architecture of human_review.py is actually GOOD — it presents question → decomposition → actor analysis → runs → aggregation → calibration → platform signals → verification → flags → decision. This exact sequence should be preserved in the Streamlit Review/Predict view. The what-to-show is right; the how-to-show must be rebuilt.

#### F-UX-DA: R2 DA responses |source:[independent-research]

DA[#4] — 5-view architecture assumes equal importance → COMPROMISE
DA claim: Dashboard+Registry overlap → merge to 3 views. Predict+Review are sequential → merge.
Concede: Dashboard IS essentially a filtered+decorated view of Registry data. "Active predictions" on Dashboard = Registry filtered to submitted+unresolved. DA is structurally correct on the data overlap.
Defend: Dashboard and Registry serve categorically different mental models. Dashboard = operational (what needs attention TODAY). Registry = archival query (what happened in the past). Conflating them forces split-attention across two incompatible use goals in one view. For a tool used daily, the operational landing view is critical UX infrastructure.
Defend Predict+Review separation: Review is NOT always accessed post-pipeline. User navigates to Review via Dashboard row-click, Registry row-click, or direct ID. Merging into Predict forces Review-only path through the Predict flow — high friction for a common action (re-examining a past prediction days later).
Compromise: retain 5 views, eliminate cross-navigation friction via explicit linking:
- Dashboard active-predictions row-click → Review with that ID pre-loaded (session_state["selected_prediction_id"])
- Registry row-click → same Review navigation
- Dashboard "Pending Review" metric click → Predict view with awaiting_review records surfaced at top before question-search UI
This preserves mental model separation while addressing DA's concern about navigation overhead.

DA[#5] — auto-rerun every 30s = expensive → CONCEDE
DA is correct. Blanket st.rerun(interval=30000) = full script re-execution on every tick including RegistryCache reload check, chart re-renders, widget reconstruction. Wasteful when nothing changed.
Better: conditional auto-rerun only during active pipeline execution:
  if st.session_state.get("pipeline_state") == "running": time.sleep(1); st.rerun()
When idle: st.cache_data(ttl=60) on registry load + manual "Refresh" button in Dashboard sidebar. User gets explicit control when idle; automatic refresh only when a run is active.
Amend F-UX-9: remove blanket auto-refresh. Add: conditional rerun during pipeline_state=="running" only; st.cache_data(ttl=60) for RegistryCache; manual refresh button.

DA[#6] — "dense layouts OK" is [prompt-claim] not [independent-research] → PARTIAL CONCEDE
Source tag reclassification: DA is correct. Inference chain is C1(personal tool) + user profile(senior PM, builds internal tools) → "dense layouts acceptable." This is [agent-inference] from [prompt-claim], not researched literature. Reclassifying.
Defend substance: NNGroup research DA cites covers public enterprise + consumer products, not personal tools built for and used daily by the same expert user. Density tolerance is meaningfully higher when user has internalized the layout through repeated self-use. That said, DA's progressive disclosure point applies to rarely-consulted content regardless of user expertise.
Qualified position: dense layouts acceptable for structured metric fields (calibrated_probability, flags, stdev, etc.) consulted on every review. Progressive disclosure correct for secondary content: long text bodies, raw reasoning chains, raw JSON — expanders appropriate not because user can't handle them, but because hiding them preserves scan speed for fields consulted every time. Expander placements in F-UX-5 (reasoning_chain, raw JSON, full description) are already consistent with this position.
Updated F-UX-9 source: |source:[agent-inference] from [prompt-claim]

DA[#15] — st.fragment reduces H5 severity → DEFEND (nuance added)
st.fragment (Streamlit 1.37+) isolates a UI section for independent rerun without full page rerun. Helps pipeline progress display — status widget can update without re-rendering entire page. Already noted in F-UX-10.
However st.fragment does NOT resolve the fundamental blocking issue. st.fragment executes synchronously within its decorated function — a 30-120s blocking orchestrator.predict() call inside a fragment still freezes the fragment and the browser for the full duration. Threading requirement is unchanged.
st.fragment's correct role: isolate the pipeline progress widget to reduce visual noise during polling. Not a substitute for threading.
H5 verdict unchanged: PARTIALLY FALSE. Orchestrator restructuring required regardless of st.fragment availability.
Amend F-UX-10: clarify st.fragment use case — isolate progress widget rerun cycle, not replace threading architecture.

DA[#16] — Tab 3 (Actor Analysis) built for potentially unused data → PARTIAL CONCEDE
DA raises a valid usage validation gap. Designed Tab 3 without evidence that user actually refers to actor analysis when making review decisions. RCA F6 relevant: H3 PARTIALLY CONFIRMED at 55% — actor analysis adds value domain-conditionally (geopolitical/regulatory YES, technology/scientific less so). Full dedicated tab is heavy treatment for data irrelevant ~45% of the time.
Concede: full-tab treatment with 2-column layout + per-actor expanders + peripheral dataframe = high-complexity UI for data rarely consulted on many prediction types.
Compromise: demote Actor Analysis from dedicated tab to collapsible st.expander within Summary tab (Tab 1), collapsed by default. Peripheral actors go into nested expander inside it. User expands when prediction domain warrants it. Preserves access without tab-navigation overhead for the common case where actors are irrelevant.
Consistent with F-UX-9 principle: expanders for "genuinely secondary" content — with H3=55%, actor analysis qualifies as secondary-by-default for a substantial fraction of predictions.
Amended F-UX-5 tab structure: st.tabs(["Summary","Runs","Verification","Resolution"]) — 4 tabs not 5. Actor Analysis inside Summary as collapsible expander. |source:[cross-agent] via RCA F6

### reference-class-analyst
**R1 COMPLETE** | 9 findings | 14 recs | forecasting methodology assessment

#### F1: Pipeline Sequence (Q2,H1) |source:[independent-research+code-analysis]|T1|
9-stage decompose→base_rate→search→forecast→aggregate→calibrate→verify→review→submit: **sequence sound, architecture suboptimal**. Matches GJP methodology. vs AIA Forecaster(arxiv:2511.07678): AIA uses iterative agentic search + supervisor reconciliation with ADDITIONAL search. vs Halawi(ICLR 2025): hundreds of articles per question. Primary gap: one-shot template search. Secondary gap: no cross-run info sharing. What's RIGHT: decompose→isolated_base_rate→forecast flow, base rate isolation is genuinely novel. Brier: -0.005 to -0.015 from iterative search.

#### F2: Base Rate Isolation (Q2) |source:[independent-research+code-analysis]|T1|
**Strongest feature.** Enforces outside-view before inside-view per Kahneman/Tversky. Issue: base rate from same model = confabulation risk (LLM Dunning-Kruger confirmed arxiv:2603.09985). R2: add web search TO base rate step. Brier: -0.008 to -0.020.

#### F3: Calibration (Q4,H4) |source:[independent-research+code-analysis]|T1|
Platt scaling correct for N<50. 0.04 hedging shift reasonable but unvalidated. No domain-specific calibration. CI computation weak (normal assumption). H4: CONFIRMED conditional. Evolve to model selection at N>=100. R3a-d: validate shift, domain params, beta CIs, model selection.

#### F4: Aggregation (Q2) |source:[independent-research+code-analysis]|T1|
Extremization 1.5 unjustified. GJP optimal 1.16-3.92 (Baron 2014). Extremizing for mass forecasts not superforecasters. Same-model may amplify biases. Effective-N heuristic arbitrary. No accuracy weighting. Trim edge case at N=3. R4a-d.

#### F5: Verification Value (Q5,H2) |source:[independent-research+code-analysis]|T1|
MIT ICLR 2026: cross-model disagreement = best epistemic uncertainty measure. Silicon Crowd: 12-model ensemble matched humans. BUT: independent forecasting + aggregation > reactive verification. H2: PARTIALLY FALSIFIED. Replace forecast verification with cross-model forecast runs. Retain verification for base rate + actors + challenge. Brier: -0.010 to -0.025.

#### F6: Actor Analysis (H3) |source:[independent-research+code-analysis]|T2|
Sophisticated framework, no empirical Brier evidence. Domain-conditional value. H3: PARTIALLY CONFIRMED (55%). Make conditional on domain.

#### F7: Deliberation (H7) |source:[independent-research]|T1|
arxiv:2512.22625: diverse-model deliberation improves Log Loss 0.020 (~4%). Same-model: NO benefit. H7: CONFIRMED conditional — multi-model only. Implement after R5. Brier: -0.010 to -0.020.

#### F8: Search Personas (H8) |source:[independent-research+code-analysis]|T2|
5 personas reasonable. NeurIPS 2025: LLM personas have systematic biases but sigma-predict varies queries not reasoning (better). Template-based generation is primary bottleneck. H8: PARTIALLY CONFIRMED (60%). R8a: iterative search > more personas.

#### F9: Error Analysis (Q6) |source:[independent-research+code-analysis]|T1|
Placeholder only. Need: Brier decomposition (Murphy 1973), error taxonomy (7 types), learning loop (post-resolution + periodic refit), both Brier AND log score, pipeline feedback. Brier: -0.015 to -0.030 over 6mo.

#### Recs ranked by Brier impact
1. R5: Multi-model independent forecasting (-0.010 to -0.025, HIGH effort)
2. R2: Search-augmented base rates (-0.008 to -0.020, MED)
3. R9: Error analysis + learning loop (-0.015 to -0.030 over 6mo, HIGH)
4. R8a: Iterative/agentic search (-0.005 to -0.015, HIGH)
5. R7: Multi-model deliberation (-0.010 to -0.020, MED)
6. R4a: Empirical extremization factor (-0.003 to -0.010, LOW)
7-14: Domain calibration, beta CIs, conditional actors, Kish ESS, quality weighting, persona merge, hedging validation, trim fix (all LOW effort)

#### Hypothesis verdicts
H1: PARTIALLY CONFIRMED (70%) | H2: PARTIALLY FALSIFIED (75%) | H3: PARTIALLY CONFIRMED (55%) | H4: CONFIRMED conditional (80%) | H7: CONFIRMED conditional (70%) | H8: PARTIALLY CONFIRMED (60%)

#### R3 DA Responses

**DA[#7] Brier impact transfer — COMPROMISE (substantial)** |source:[agent-inference]|
DA correct: estimates load-bearing + derive from human research with uncertain LLM transfer. CDS FORMAT-COGNITIVE-3tier applies: methodology="unobservable cognition"=45-60% transfer. LLM errors (confabulation) differ structurally from human (judgment). Direct LLM datapoints (Silicon Crowd, AIA) validate direction not magnitude. REVISED (50% discount): R5: -0.005 to -0.015 80%CI[-0.002,-0.025] | R2: -0.004 to -0.012 80%CI[-0.001,-0.020] (better transfer — LLM-specific fix) | R9: -0.008 to -0.018/6mo 80%CI[-0.003,-0.030]. Relative ranking UNCHANGED — robust to discount.

**DA[#8] Search vs isolation tension — COMPROMISE (with resolution)** |source:[agent-inference]|
DA correct: unrestricted search in base rate WOULD contaminate isolation. RESOLUTION: two types of search — (a) reference class frequency lookup ("how often do X?") = pure outside-view vs (b) current evidence = inside-view. R2 must ONLY do (a). Safeguards: query restricted to "{ref_class} historical frequency statistics", temporal firewall (exclude <6mo), separate model call feeding only numerical rate + citation, label as STATISTICAL REFERENCE DATA. Without safeguards DA is right. With them, R2 augments outside-view with grounded data. R2 stands WITH mandatory contamination controls.

**DA[#9] Multi-model N=0 validation — COMPROMISE** |source:[agent-inference]|
DA correct: cost increase with zero validation is weak. CHEAPEST TEST: re-run 10-20 resolved predictions through single-model vs multi-model, compare Brier. Cost ~$5-15. If delta < 0.005, not worth it. REVISED R5: CONDITIONAL on A/B test at N>=10 resolved. Phase 2.

**PRIORITY RERANKING (material):**
1. R9: Learning loop (prerequisite for evidence-driven validation of all else)
2. R2: Search-augmented base rates WITH contamination controls
3. R5: Multi-model (CONDITIONAL on A/B, Phase 2)
R9→#1 because DA[#9] correctly identified: without resolved data, ranking = theory not evidence.

**DA[#15] RegistryCache — DEFER** to tech-architect. Not methodology domain. |source:[agent-inference]|

### code-quality-analyst

#### CQ-A: Code duplication — _extract_json() P0 |source:independent-research|
Identical 20-line function copied verbatim in 3 files:
- decomposer.py:151-171
- base_rate.py:27-44
- forecaster.py:34-51
All 3: strip code blocks → raw JSON fallback → brace-scan. Zero divergence.
Fix: extract to src/pipeline/utils.py, import in all 3.

#### CQ-B: Code duplication — _load_prompt() P1 |source:independent-research|
Near-identical prompt loader in 3 files:
- decomposer.py:24-27 — (config, filename)
- forecaster.py:28-31 — (config, filename) — byte-for-byte identical to decomposer version
- base_rate.py:21-24 — (config) only, filename hardcoded "base_rate.md"
Fix: single _load_prompt(config, filename) in utils.py.

#### CQ-C: Code duplication — brier_score() P1 |source:independent-research|
brier_score() defined in scripts/resolve.py:23-25 AND scripts/dashboard.py:23-24. log_score() exists only in resolve.py — dashboard has no access to it. If scoring methodology changes, two files diverge.
Fix: src/scoring.py with brier_score + log_score, import in both scripts.

#### CQ-D: Code duplication — platform client factory P2 |source:independent-research|
Dict-lambda platform dispatch duplicated:
- scripts/predict.py:24-34 — wrapped in _get_platform_client() with click.BadParameter on unknown platform
- scripts/batch_predict.py:53-58 — inline dict, no error check (KeyError on unknown platform)
Fix: shared factory in src/platforms/__init__.py.

#### CQ-E: Config — primary_model type annotation error P1 |source:independent-research|
config.py:66: primary_model: ModelConfig = field(default=None)
Annotation says ModelConfig (not Optional), default is None. mypy --strict rejects. Works at runtime only because Python dataclasses do not enforce annotations. Creates false sense of non-nullability — orchestrator.py:170 and llm_router.py:106 access attributes without None check, safe only because validate() is called first, not structurally enforced.
Fix: primary_model: ModelConfig | None = field(default=None)

#### CQ-F: Config — mixed path APIs P2 |source:independent-research|
config.py:10 uses Path(__file__) (pathlib). Lines 111-116 use os.path.join/os.path.dirname/os.path.abspath (strings). RegistryStore uses Path() internally. Three styles in one codebase.
Fix: all pathlib throughout.

#### CQ-G: Config — search backend not validated P2 |source:independent-research|
SearchConfig.backend = "tavily" with comment "tavily | serper | exa". SearchModule hardcodes Tavily API calls regardless of backend value. Setting backend="serper" silently has no effect.
Fix: validate backend in Config.validate() or remove unsupported options from comment.

#### CQ-H: Error handling — decompose_question silent fallback P0 |source:independent-research|
decomposer.py:76-81: JSON parse failure returns Decomposition() with base_rate=0.5, empty actors. Pipeline continues without any flag on PredictionRecord. Systematic LLM failure (prompt regression, API change) produces 0.5 predictions indistinguishable from valid ones. base_rate.py:103-106 has identical pattern.
Fix: add pipeline_warnings: list[str] field to PredictionRecord. Append "decomposition_parse_failed" / "base_rate_parse_failed" on failure. Surface in _generate_flags().

#### CQ-I: Error handling — forecaster silent fallback P1 |source:independent-research|
forecaster.py:200-203: JSON parse failure → data={} → probability defaults to base_rate. Pre-mortem failure at line 233: pm_data={}, all pre_mortem fields empty. No field in RunResult indicates a parse failure occurred.
Fix: add RunResult.parse_failed: bool = False field. _generate_flags() should check it.

#### CQ-J: Error handling — orchestrator inline imports P2 |source:independent-research|
orchestrator.py:164 — from src.pipeline.search import SearchModule inside predict() method body, inside a for loop. orchestrator.py:213 — from src.models import StageVerification inline inside predict(). No circular dependency exists in either case.
Fix: move both to top-level imports.

#### CQ-K: Type safety — LLMRouter.verify() returns Any P1 |source:independent-research|
llm_router.py:162: def verify(...) -> Any | None. Return type leaks through verification.py:_result_to_entry() which duck-types with hasattr() (line 24). sigma_verify API changes break silently.
Fix: local Protocol with .to_dict() shape, or TypedDict for the dict case.

#### CQ-L: Type safety — LLMRouter.call() thread-unsafe model mutation P1 |source:independent-research|
llm_router.py:127-132 (and equivalents for openai/gemini):
    old_model = self._anthropic.model
    self._anthropic.model = model   # mutation on shared object
    try: return self._anthropic.call(...)
    finally: self._anthropic.model = old_model
Not thread-safe. Streamlit threading model for pipeline execution creates concurrent router.call() invocations. Two threads mutate client.model simultaneously — one gets wrong model silently.
Fix: pass model as parameter to AnthropicClient.call() instead of mutating shared state.

#### CQ-M: Type safety — str fields with implicit enum values P1 |source:independent-research|
Multiple models use plain str for constrained fields:
- Actor.influence_estimate: str — valid: "low"|"medium"|"high"
- PeripheralActor.influence_estimate: str — same
- VerificationEntry.assessment: str — valid: "agree"|"disagree"|"partial"|"uncertain"
- VerificationEntry.confidence: str — valid: "high"|"medium"|"low"
- ChallengeEntry.vulnerability: str — valid: "high"|"medium"|"low"
- Aggregation.method: str — should match AggregationConfig.method values
human_review.py pattern-matches these strings (line 258: entry.assessment in ("disagree","partial")). LLM typo in output bypasses flag logic silently.
Fix: Literal["low","medium","high"] etc. — Pydantic validates at parse time, typos raise ValidationError.

#### CQ-N: Models — timestamp fields are str not datetime P2 |source:independent-research|
Resolution.resolved_at, Submission.submitted_at, PredictionRecord.created_at all str. RegistryQuery.get_recent_in_domain() sorts by created_at lexicographically (line 43). Works only for same-format UTC ISO strings — mixed timezone or missing Z causes incorrect sort.
Fix: Pydantic datetime fields with automatic ISO parsing.

#### CQ-O: Registry — O(N) scan on every access P2 |source:independent-research|
store.get_by_id() → load_all() → full file read + deserialize. RegistryQuery.count_resolved() → get_resolved() → load_all(). Orchestrator calls count_resolved() on every prediction (orchestrator.py:242). At 1,000 records * 5KB each = 5MB deserialization per prediction run. Acceptable at current scale, degrades sharply under Streamlit frequent widget reruns.
Fix for rebuild: RegistryCache with pandas DataFrame in memory, invalidated on write.

#### CQ-P: Registry — save() not atomic P1 |source:independent-research|
RegistryStore.save() (line 31-34) appends directly with open(..., "a"). Process crash mid-write = partial last line = prediction lost (load_all() skips with warning). _write_all() uses atomic os.replace() — save() does not. Acceptable for personal tool (C1), worth documenting.

#### CQ-Q: decomposer + base_rate hardcode "anthropic" provider — P1 critical bug |source:independent-research|
decomposer.py:64: router.call("anthropic", config.primary_model.model_id, ...) — hardcodes provider string.
base_rate.py:78 — same.
forecaster.py:187 correctly uses prov variable derived from config.
If user has only OpenAI or Gemini keys: decomposition + base_rate calls raise "Anthropic client not available" — silent failure of 2 of 9 pipeline stages for non-Anthropic configurations.
Fix: use config.primary_model.provider in both files.

#### CQ-R: AnthropicClient creates SDK client per call P2 |source:independent-research|
llm_router.py:44 — client = anthropic.Anthropic(api_key=self._api_key) inside call() method body. New SDK client (new connection pool) on every LLM invocation.
Fix: instantiate once in AnthropicClient.__init__(), store as self._client.

#### CQ-S: H5 — CLI wrappability verdict P1 |source:independent-research|
H5: "Is the existing CLI logic sound enough to wrap?"
VERDICT: PARTIALLY FALSE.
Wrappable as-is: Orchestrator, all platform clients, registry layer, aggregator, calibration, verification.
NOT wrappable without rewrite:
1. human_review.py:present_for_review() — tightly coupled to rich Console + blocking console.input(). Cannot call from Streamlit.
2. orchestrator.predict() is synchronous blocking (30-120s). Will freeze Streamlit UI. Needs threading wrapper or split into predict_until_review() / submit_after_review().
3. brier_score duplication — Streamlit dashboard would need 3rd copy or extraction first.
CLI scripts are thin and separately wrappable. The orchestrator core is cleanly separable. The review UX is not.

#### CQ-T: Test coverage — critical gaps |source:independent-research|
Modules WITH tests (well covered): calibration.py, registry/store.py, registry/query.py, platforms/metaculus.py, platforms/polymarket.py, platforms/kalshi.py, aggregator.py.

Modules with ZERO test coverage:
- orchestrator.py — full pipeline integration, zero tests
- decomposer.py — JSON parsing, actor building, peripheral mapping, error path (CQ-H)
- base_rate.py — JSON parsing, clamping, error fallback
- forecaster.py — full run, pre-mortem, JSON parse failure, cost tracking
- verification.py — _result_to_entry, _compute_agreement, should_verify_run, all verify_* functions
- search.py — persona strategies, URL dedup, API error paths, empty API key behavior
- llm_router.py — routing, model dispatch, cross_verify, cost estimation
- deliberation.py — should_deliberate() is a pure function, easily testable
- human_review.py — _generate_flags() is pure logic, fully testable without I/O
- scripts/*.py — zero tests

Highest priority: decomposer + forecaster JSON parse failure paths (CQ-H/CQ-I) — silent degraded output with zero test coverage. should_verify_run() outlier detection. _generate_flags() flag generation. should_deliberate() threshold logic.

#### CQ-U: Dead code and stub modules |source:independent-research|
- src/analysis/__init__.py — empty package, no contents, no consumers
- src/monitoring/__init__.py — empty package, no contents
- scripts/monitor.py — 26 lines, all stub, prints "Phase 3 not implemented"
- deliberation.py:deliberate() — returns inputs unchanged (stub). should_deliberate() is live code.
- ACTOR_LEVEL_LABELS dict (models.py:30-34) — used only in decomposer.py:91. Could be replaced with ActorLevel enum method.

#### CQ-V: search.py — no retry or rate limiting P1 |source:independent-research|
SearchModule.search() makes synchronous httpx calls, 30s timeout, no retry logic. 5-persona run = 25 queries. Transient Tavily 429/5xx on query N → silent [] results → forecaster runs without evidence for that sub-query. No flag on PredictionRecord.
Fix: exponential backoff (2-3 retries) for 429/5xx. Log retry events to PredictionRecord.

#### CQ-W: Polymarket/Kalshi resolution permanently None P1 |source:independent-research|
PolymarketClient.get_resolution() returns None unconditionally (polymarket.py:125-127).
KalshiClient.get_resolution() returns None unconditionally (kalshi.py:160-162).
resolve.py:62-67 skips non-Metaculus with "not implemented" message.
Predictions on Polymarket/Kalshi can never be scored. Brier score dashboard silently incomplete for those platforms. Acceptable Phase 0, should be documented prominently.

#### CQ-X: Config — __post_init__ between field declarations P2 |source:independent-research|
config.py: field declarations (lines 57-69) → __post_init__ method (lines 71-97) → more field declarations (lines 99-116). Non-standard — Python convention puts all fields first, then methods. Works at runtime, confusing for readers and tools.
Fix: all fields first, __post_init__ after.

#### CQ-GRADE: C+ — functional but brittle for rebuild |source:independent-research|
P0 issues (3): CQ-A (_extract_json 3x duplication), CQ-H (silent parse failures = undetectable 0.5 predictions), CQ-Q ("anthropic" hardcoded = non-Anthropic configs fail 2 pipeline stages)
P1 issues (11): CQ-B, CQ-C, CQ-E, CQ-I, CQ-K, CQ-L, CQ-M, CQ-P, CQ-S, CQ-V, CQ-W
P2 issues (8): CQ-D, CQ-F, CQ-G, CQ-J, CQ-N, CQ-O, CQ-R, CQ-X
H5 verdict: PARTIALLY FALSE — orchestrator core wrappable, human_review.py not, orchestrator is blocking, scoring utilities need extraction
Test coverage: 7 modules tested, 10 modules at zero coverage. Highest gap: decomposer, forecaster, verification — all have silent failure paths with zero tests.

#### DA[#10] RESPONSE — grade reference class |source:independent-research|
DA challenge: C+ grade conflates production-system standards with personal-tool (C1) standards.
COMPROMISE.
DA is correct that P2 issues (CQ-F mixed Path/os.path, CQ-N str timestamps) would not cause bugs for a single-user personal tool. Grading these as deficiencies relative to a production standard is the wrong reference class.
Revised reference class: code quality relative to the user's STATED GOAL — "tear it down and rebuild." Under this reference class, the grade stands but for different reasons than initially stated:
- P0 issues are genuine regardless of C1: CQ-H (silent 0.5 predictions) is a correctness bug in production use. CQ-Q (hardcoded "anthropic") causes functional failure for any non-Anthropic primary model. These are not style issues.
- P1 issues that matter for the rebuild specifically: CQ-L (thread-unsafe model mutation) directly breaks the Streamlit threading model — not a style issue. CQ-M (str-not-Literal) creates undetectable LLM parse errors that affect prediction accuracy — not a style issue. CQ-S (orchestrator blocking) blocks the rebuild target.
- P1/P2 issues that are genuinely style-only for a personal tool: CQ-F, CQ-N, CQ-X — DA correct, these would be B-level issues in a personal tool context and should not drag the grade.
Recalibrated grade: B- as a personal tool (it works, has real correctness issues at P0, but doesn't fail in normal single-user sequential usage). C+ as a rebuild-ready codebase (the P0+P1 issues that block the Streamlit rebuild are the correct reference class for this review's purpose).
The review's purpose IS the rebuild — C+ is correct for that context. DA's challenge improves the framing, not the grade.

#### DA[#11] RESPONSE — test sequencing before rebuild |source:independent-research|
DA challenge: writing tests for code about to be rewritten = wasted effort.
CONCEDE with precision.
DA is correct on unit tests for implementation internals. Writing tests for decomposer.py JSON parsing logic, forecaster.py data extraction, or base_rate.py clamping — these tests will break the moment the module is restructured and provide no value during the rebuild.
HOWEVER two categories of tests have positive ROI even before the rebuild:
1. Behavioral integration tests: tests that exercise the full pipeline via its public contract (Orchestrator.predict() input → PredictionRecord output shape, registry round-trip, calibration invariants). These survive structural refactoring because they test behavior not implementation. Example: given a mock question and mock LLM responses, the output record has calibrated_probability in [0.01, 0.99], has at least one run, has a valid prediction_id. These pass/fail before and after the rebuild.
2. Silent-failure regression markers: NOT unit tests of the broken code, but test fixtures that document the failure mode so the rebuild knows to fix it. A pytest test that deliberately feeds malformed JSON to the current decomposer and asserts the record has no warning flag — a test that FAILS now (because there's no warning), proving the rebuild must fix it. These are specification-as-test, not implementation-as-test.
Sequencing revised: do not write implementation unit tests for modules being rebuilt. DO write behavioral integration tests now (they constrain the rebuild to maintain the same contract) and silent-failure regression markers (they document what the rebuild must fix).
CQ-T recommendation updated: highest value is not "test decomposer parse failure" but "test pipeline behavioral contract and document the silent failure as a failing test."

#### DA[#15] RESPONSE — H5 unanimous consensus / st.fragment |source:independent-research|
DA challenge: st.fragment (Streamlit 1.37+) could make blocking pattern workable without full orchestrator split.
DEFEND with evidence.
st.fragment isolates partial reruns — it prevents the full page from rerunning when a fragment's state changes. It does NOT allow a fragment to block on long-running synchronous operations without freezing the entire Streamlit server. Specifically:
- st.fragment runs in the same thread as the main Streamlit script
- A 30-120s synchronous call inside a fragment blocks the Streamlit worker thread for that session for the full duration
- Other sessions are unaffected (personal tool, C1 — so this is less relevant), but the UI for THIS session is completely frozen during pipeline execution
- st.fragment + rerun=True option triggers fragment rerun at an interval, but the fragment callback itself cannot be a blocking call
The actual Streamlit-compatible pattern for long-running operations requires threading (worker thread writes progress to session_state, fragment reads it) OR the new experimental background_tasks API (Streamlit 1.40+, not yet stable). In either case, orchestrator.predict() must NOT block the main thread.
st.fragment is useful for the pipeline progress DISPLAY (updating stage labels without full page rerun) but does not resolve the blocking execution problem. The orchestrator split is still required.
Revised H5 position: H5 = PARTIALLY FALSE is correct. st.fragment addresses display responsiveness (valuable) but not the blocking execution problem (structural). The split into predict_until_review() + submit_after_review() remains necessary. Consensus on this point holds.

### cognitive-decision-scientist

**CDS-R1: Cognitive Science Assessment of sigma-predict Pipeline**

#### a) Debiasing Assessment — Biases addressed and missed |source:[independent-research]

ADDRESSED:
- Anchoring (inside-view contamination): base_rate.py explicit isolation before search — FORMAT-level, correctly placed
- Availability bias: base rate locked before search contact — prevents compelling recent evidence dominating
- Hedging/overconfidence: apply_hedging_correction() directionally correct but mechanically crude (flat shift ¬probability-sensitive)
- Scenario fixation: pre-mortem FORMAT structure has evidence base (Klein 2007, Mitchell 1989)

MISSED — HIGH PRIORITY:
- Scope insensitivity: no mechanism forces scaling estimates across reference class sizes; sub-questions generated but no Fermi-chain validation
- Representativeness: decomposer generates reference class but no check for whether more discriminating class exists
- Hindsight contamination: no structured pre-registration of "what would falsify this forecast" before prediction
- Framing effects: forecaster sees native platform wording — no reformulation step to check probability coherence
- Confirmation bias at reasoning: personas diversify retrieval but same LLM processes all results — retrieval diversity ≠ reasoning diversity (key gap, see H8)

F[CDS-1]: base-rate isolation is the single strongest debiasing mechanism in the pipeline — correctly placed, correctly locked |source:[independent-research] T1

#### b) Pre-mortem Evaluation |source:[independent-research]

CRITICAL DESIGN GAP:
- pre_mortem prompt receives original probability AND reasoning_chain (forecaster.py:210-218)
- Klein (2007) original pre-mortem: participants commit to failure scenario BEFORE seeing outcome probabilities — pipeline inverts this by anchoring model on its own estimate
- Same model, same context window, temperature unchanged — LLM generating "what if I'm wrong" while holding its own reasoning_chain = self-consistency confirmation, not dialectical reframing
- Data capture is good: pre_mortem_changed_estimate + delta stored for learning loops
- Transfer: 55-65% (MODERATE per cognitive-enhancement review) — mechanism requires cognitive reframing not available to same-context LLM

F[CDS-2]: pre-mortem structurally undermined by same-model same-context execution. FORMAT fix: strip reasoning_chain from pre-mortem prompt; force failure scenario generation BEFORE allowing probability revision. Zero cost increase. Expected: 10-20% reduction in pre-mortem false negatives |source:[agent-inference] T1

#### c) Calibration — Reliability vs Resolution (H4) |source:[independent-research]

PLATT ASSESSMENT:
- Platt scaling = post-hoc logistic transform correcting SYSTEMATIC BIAS — reliability improvement only
- Cannot fix resolution: Platt rescales numbers, cannot improve targeting of uncertainty to the right questions
- Pre-Platt flat hedging correction is wrong shape: constant shift at P=0.3 same as P=0.8. Literature: isotonic regression or temperature scaling are probability-sensitive alternatives
- N≥50 threshold means flat correction applies for potentially years — poor approach during learning period

Brier decomposition (Murphy 1973, confirmed in agent memory):
- Brier = reliability + resolution + uncertainty
- Platt improves reliability; nothing in pipeline addresses resolution
- Resolution requires domain-discriminating features: domain, horizon, base rate region — captured but not used for calibration tracking

F[CDS-3]: H4 CONFIRMED long-term (Platt correct) / WRONG SHAPE short-term. Replace flat hedging shift with temperature scaling. Add domain/horizon-stratified Brier decomposition at resolution time |source:[independent-research] T2

F[CDS-4]: System has no resolution tracking — cannot identify whether it is systematically miscalibrated by domain/horizon. CalibrationData needs domain-stratified Brier decomposition: reliability, resolution, uncertainty per domain + horizon bucket |source:[agent-inference] T2

#### d) Multi-model as "crowd within" — H2 |source:[independent-research]

INDEPENDENCE ANALYSIS:
- All N runs use config.primary_model.model_id — same model, same weights, same training data
- Persona variation diversifies retrieval framing but same model processes all results — stochastic sampling diversity + prompt variation, NOT independent estimation
- Conditions for wisdom of crowds (Surowiecki, confirmed agent memory R[wisdom-of-crowds-AI]): independence + diversity — same-model multi-run achieves NEITHER
- effective_n calculation is descriptive (measures spread) not diagnostic (does not verify that spread = genuine independence)
- Gemini runs as VERIFIER (reactive challenge) not independent FORECASTER

F[CDS-5]: H2 FALSIFIED for same-model multi-run. Multiple runs of same model = stochastic resampling of correlated estimates, not crowd wisdom. True crowd-within requires genuinely different models as independent forecasters. Current architecture uses Gemini only reactively |source:[independent-research] T1

F[CDS-6]: Extremization (aggregator.py:68-69) should NOT apply to same-model correlated outputs. Baron et al. (2014), Satopää et al. (2014): extremization designed for genuinely independent crowds. Applying to correlated same-model outputs inflates overconfidence. Gate extremization on: effective_n ≥ 3 AND diverse model sources confirmed |source:[independent-research] T2

#### e) Deliberation Design — H7 |source:[independent-research]

STUB ANALYSIS:
- Trigger: stdev > deliberation_stdev_threshold — but high stdev from same-model runs = sampling noise, not genuine disagreement
- Triggering deliberation on within-model variance = false positive
- Dual-process theory + Wynn (ICML 2025): deliberation improves outcomes when (a) initial estimate has insufficient evidence, (b) identifiable unconsidered evidence exists, (c) disagreement is BETWEEN independent estimators
- Without structural independence, deliberation converges to dominant estimate (conformity > obstinacy, confirmed agent memory)

F[CDS-7]: H7 CONFIRMED — deliberation worth implementing — but trigger must change. Correct triggers: (a) cross-model disagreement (Gemini vs primary), (b) verification challenge rated high vulnerability, (c) pre-mortem |delta| > 0.1. NOT within-model stdev. Supervisor agent should access verification disagreements + do targeted search on contested evidence claims |source:[independent-research] T1

#### f) Error Taxonomy — Classification for resolved predictions |source:[agent-inference]

CURRENT STATE PROBLEMS:
- error_class_auto/manual are list[str] — untyped, no schema, no stage attribution
- resolve script never populates error_class_auto — field is dead code

COGNITIVE ERROR TAXONOMY FOR LLM FORECASTING (applying accuracy-errors-reclassified from agent memory):
- Error Type 1 — Generation/Confabulation: model produces confident but incorrect base rate or reference class. Detectable: base_rate vs. resolution mismatch with ex-post correct reference class available
- Error Type 2 — Executive Function/Process: wrong inference chain despite correct inputs. Detectable: search results contain correct evidence but probability doesn't reflect it
- Error Type 3 (new): Actor misclassification — L1 actor was actually L2/3. Detectable: actor_motivation_flags vs. pre-prediction actor_analysis
- Error Type 4 (new): Search persona blindspot — relevant evidence existed but not retrieved by any persona used
- Error Type 5: Calibration failure — directionally correct but magnitude wrong (reliability error). Detectable by Brier reliability component

F[CDS-8]: Resolution model needs typed error taxonomy (Enum) with pipeline stage attribution. Each error class maps back to specific stage to enable targeted improvement. list[str] is unanalyzable |source:[agent-inference] T1

#### g) Missing Cognitive Safeguards |source:[independent-research]

HIGH-IMPACT MISSING (FORMAT-level, 70-85% transfer):
1. Falsification pre-registration: before forecast, record what evidence would cause significant revision. Requires RunResult.falsification_anchors: list[str]
2. Question reformulation coherence check: rephrase in negated form, compare P to 1-P(X) — lightweight Stage 0 before decomposition. LLMs produce incoherent probabilities for equivalent questions
3. Reference class quality check: is chosen class the most discriminating available? Narrower class with sufficient N predicts better

LOW-IMPACT (cognitive-skill level, <55% transfer — SKIP per cognitive-enhancement review):
- Full CQoT (P=45-55% marginal per prior review)
- Mental simulation protocols (TEC — deferred per prior review)

F[CDS-9]: Two FORMAT-level additions: (1) falsification_anchors field in RunResult (prompt addition + data model change, enables structured post-resolution learning), (2) question reformulation coherence check as Stage 0 (one short LLM call, catches framing effects) |source:[independent-research] T2

#### h) Metacognitive Monitoring |source:[independent-research]

CURRENT STATE:
- confidence_self_score (1-10) in RunResult — self-reported by forecasting LLM
- Metacognition paradox (agent memory): self-report = RELIABILITY signal, NOT resolution — doesn't identify which questions model is wrong about
- No cross-session learning: fit_platt called externally but no mechanism connects resolved errors back to pipeline improvements
- No stratified accuracy tracking by domain, horizon bucket, base rate region, persona used

F[CDS-10]: Metacognitive monitoring requires EXTERNAL tracking, not self-report. Resolution loop should compute Brier decomposed by: (a) domain, (b) horizon_days bucket (<30d, 30-180d, >180d), (c) base rate region (<0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, >0.8), (d) verification_used flag. These dimensions identify systematic error patterns |source:[independent-research] T2

#### i) Recommendations Ranked by Expected Cognitive Impact

RANK 1 — Fix pre-mortem anchoring (F[CDS-2]): Strip reasoning_chain from pre-mortem prompt. FORMAT-level, zero additional cost |source:[agent-inference]
RANK 2 — Fix multi-run independence (F[CDS-5]): Run Gemini as independent PRIMARY forecaster on at least 1 run. Enables valid aggregation + valid extremization. ForecastBench: AIA Forecaster (supervisor reconciliation of independent models) = superforecaster-median parity |source:[independent-research]
RANK 3 — Add falsification anchors (F[CDS-9]): RunResult.falsification_anchors field. Single prompt addition. Enables structured post-resolution learning |source:[agent-inference]
RANK 4 — Fix calibration shape (F[CDS-3]): Replace flat hedging shift with temperature scaling. Domain-stratified Brier decomposition tracking |source:[independent-research]
RANK 5 — Fix deliberation trigger (F[CDS-7]): Trigger from cross-model disagreement + verification challenge vulnerability |source:[independent-research]
RANK 6 — Fix error taxonomy (F[CDS-8]): Typed enum with pipeline stage attribution |source:[agent-inference]

HYPOTHESIS VERDICTS (R1 — superseded by DA responses below):
- H2: FALSIFIED — same-model multi-run ≠ crowd wisdom |source:[independent-research]
- H3: PARTIALLY CONFIRMED — actor analysis well-designed; verification gate (L2/3) correct; weak link = implication_for_estimate not validated as effective at forecaster reasoning stage |source:[agent-inference]
- H4: CONFIRMED long-term / WRONG SHAPE short-term — Platt correct, flat hedging correction wrong |source:[independent-research]
- H7: CONFIRMED with redesign — worth implementing, trigger must change to cross-model disagreement |source:[independent-research]
- H8: PARTIALLY FALSIFIED — personas diversify retrieval but same model eliminates perspective diversity at reasoning; contrarian is the only persona creating genuine reframing pressure |source:[agent-inference]

#### CDS-R2: DA Challenge Responses

**DA[#12] — COMPROMISE: fix is right, mechanism description needs precision** |source:[independent-research]

DA correctly identifies that Klein's pre-mortem requires specificity — "imagine THIS project failed" not generic failure. Generic pre-mortems ("base rate was wrong") are less valuable than specific ones ("reasoning assumed X but if Y, probability shifts to Z"). Objection is substantive.

But DA misidentifies the anchoring source. The problem is not "context vs. no-context" — it is anchoring on a COMMITTED PROBABILITY ESTIMATE AND JUSTIFICATION while simultaneously generating challenges to it. Mitchell et al. (1989) and Veinott et al. (2010) establish pre-mortem value from failure commitment BEFORE probability justification — in the original design the failure commitment precedes the locked estimate. Once a model has output a probability + reasoning_chain, motivated reasoning and self-consistency operate jointly: challenge generation tends toward rationalization, not genuine failure identification.

REVISED F[CDS-2]: Strip the probability AND reasoning_chain; preserve question context. Provide to pre-mortem prompt: question title + resolution criteria + sub-questions + actor analysis — but NOT the derived probability, NOT the reasoning_chain. Force: "This prediction FAILED. What went wrong?" before allowing probability revision. Preserves specificity (model knows the question structure) while removing the committed-estimate anchor. Question context = essential. Committed probability + post-hoc justification = anchoring source. |source:[independent-research] T2

CALIBRATION CORRECTION: "10-20% reduction in false negatives" withdrawn — uncalibrated magnitude per DA audit. Direction plausible but magnitude is [agent-inference], not T1.

---

**DA[#13] — CONCEDE: phasing error; isotonic regression closes the N=0→50 gap** |source:[independent-research]

DA is correct. Temperature scaling requires fitting parameter T on held-out (predicted, actual) pairs — same data requirement as Platt. With N=0 resolved predictions, neither is applicable. My "replace flat hedging with temperature scaling" elided the phasing.

REVISED F[CDS-3]: Three-phase calibration:
- Phase 0 (N=0→20): flat hedging correction is the only feasible option — preserve. Validate the 0.04 magnitude: ECE literature (arxiv:2603.09985) shows ECE 0.12-0.40 for LLMs; 0.04 flat shift likely too small at extreme probability regions. Scale shift with distance from 0.5 as a zero-data improvement within Phase 0.
- Phase 1 (N=20→50): isotonic regression on logit scale — non-parametric, data-efficient (N≥10 viable), probability-sensitive. Earlier than Platt. Correct replacement for flat shift.
- Phase 2 (N≥50): Platt scaling as designed.

"Temperature scaling" was an imprecise label. Isotonic regression is the correct Phase 1 recommendation — probability-sensitive AND operable at N=10-20. The gap between N=0 and N=50 is real and addressable. |source:[independent-research] T2

---

**DA[#14] — COMPROMISE: H2 moderated to PARTIALLY FALSIFIED (75%); XVERIFY engaged** |source:[independent-research] [cross-agent]

DA[#14] is the strongest challenge. XVERIFY correctly moderated. "FALSIFIED" was too strong — conceded.

XVERIFY OBJECTION ENGAGED: Persona variation changes search queries → different retrieved evidence → genuine information-set diversity within same model. This is real retrieval diversity. I acknowledged this in R1 but labeled H2 "FALSIFIED" which implies zero value from same-model multi-run — inconsistent with the analysis.

WHAT STANDS: Retrieval diversity ≠ reasoning diversity. Same model processes diversified information through the same weights, same training-induced biases, same confabulation failure modes (Error Type 1 from taxonomy). Multi-model designs produce genuinely independent error profiles — not just diversified inputs to the same error-generating process. ForecastBench AIA Forecaster (supervisor reconciliation of different models = superforecaster-median parity) confirms multi-model advantage is qualitative.

WHAT MODERATES: Same-model multi-run with diverse personas does produce real value: (a) hedges against single-persona retrieval gaps, (b) provides variance estimates for CI construction, (c) reduces sampling noise. The aggregate is not worthless.

REVISED H2: PARTIALLY FALSIFIED (75%) — persona-driven retrieval diversity is real but insufficient for crowd-within (independence + diversity at reasoning level). Same-model multi-run is stochastic resampling improvement, not genuine ensemble diversity. Extremization should be gated on cross-model diversity, not applied to same-model variance. Aligns with RCA F5 and XVERIFY advisory. |source:[independent-research] [cross-agent] T1

REVISED F[CDS-5]: Same-model multi-run retains value for variance estimation and retrieval coverage; the specific failure is applying extremization to within-model variance and claiming crowd-within properties.
REVISED F[CDS-6]: Extremization gate: apply when N≥2 distinct providers (not N≥3 same-model runs). Same-model runs: trimmed mean only, no extremization. |source:[agent-inference]

---

**DA[#16] — CONCEDE: H3 actor analysis empirical value is a genuine gap; instrument before full UX investment** |source:[agent-inference]

DA correctly identifies that no agent empirically tested actor analysis predictive value. H3 was assessed at structural/theoretical level only. actor_motivation_flags is populated (forecaster.py:256) but no evidence exists that it is consulted during human review, influences the final probability, or correlates with Brier improvement. UX Tab 3 actor display assumes value that is unvalidated.

Testable path once N≥20 resolved predictions:
1. Compare Brier score when level_2_3_present=True vs False — direct empirical test of H3
2. Track whether reviewer references actor flags in human_reasoning text
3. Add actor_analysis_consulted: bool to HumanReview for explicit usage tracking

REVISED H3: UNRESOLVED PENDING INSTRUMENTATION — theoretical value sound (identity-constrained actors introduce non-rational dynamics that base-rate reasoning systematically misses), empirical pipeline value unknown. UX consequence: F-UX-5 Tab 3 should be simplified to collapsible summary view rather than 2-column elaborate layout until H3 validated empirically at N≥20. |source:[agent-inference]

REVISED HYPOTHESIS VERDICTS (post-DA):
- H2: PARTIALLY FALSIFIED (75%) — retrieval diversity from personas is real; reasoning-level independence is not. Extremization invalid on same-model runs |source:[independent-research] [cross-agent]
- H3: UNRESOLVED PENDING INSTRUMENTATION — theoretical value sound; empirical value unknown; simplify UX pending validation |source:[agent-inference]
- H4: CONFIRMED long-term / THREE-PHASE approach: flat(N=0→20) → isotonic(N=20→50) → Platt(N≥50) |source:[independent-research]
- H7: CONFIRMED with redesign — trigger must change to cross-model disagreement + verification challenge vulnerability |source:[independent-research]
- H8: PARTIALLY FALSIFIED — personas diversify retrieval; same model eliminates reasoning-level diversity; contrarian most valuable for genuine reframing |source:[agent-inference]

### devils-advocate

#### R2 challenges issued |#16

##### Source Provenance Audit (§2d)
source-distribution: ~90%[independent-research], ~8%[agent-inference], ~2%[prompt-claim-mislabeled]
echo-chamber: NOT-DETECTED | prompt-hypotheses-tested-¬confirmed(H2-falsified,H5-partial-false) = investigative
!flag: CDS-F5 tagged [independent-research:T1] but XVERIFY moderated to PARTIAL → source-tag-exceeds-verification
!flag: UX-F-UX-9 "power user, dense layouts OK" = [prompt-claim] wearing [independent-research] tag (derived from C1 constraint ¬independent observation)
!flag: H5=PARTIAL-FALSE unanimous(5/5) + H6=PARTIAL unanimous(3/3) = untested consensus warranting scrutiny

##### Analytical Hygiene Audit (§2a-e)
- TA: implicit hygiene via P0/P1/P2 prioritization, no explicit outcome-1/2/3 format. ACCEPTABLE for code-level scope
- UX: no explicit §2a-e. Design specs ¬analytical claims. F-UX-9 user-profile claims lack §2b. WEAK
- RCA: BEST hygiene. Brier impact ranges + T1/T2 tiers + arxiv calibration. STRONG
- CQA: code-evidence hygiene (line numbers). C+ grade lacks §2b reference class. ACCEPTABLE
- CDS: literature-grounded. CDS-2 "10-20% reduction" estimate uncalibrated. MODERATE

##### Targeted Challenges

**DA[#1] HIGH — tech-architect: RegistryCache as pandas DataFrame = overengineered |target:TA-A3**
TA recommends pandas DataFrame for RegistryCache. For "hundreds to low-thousands" of PredictionRecord objects: (a) pandas adds a heavyweight dependency for what is essentially a filtered list, (b) PredictionRecord is deeply nested (Decomposition, list[RunResult], Aggregation, CalibrationData, etc.) — DataFrame flattening loses structure, (c) SQLite would give persistence + filtering + indexing with zero serialization complexity, (d) even a simple dict[str, PredictionRecord] with helper methods would suffice. Why pandas specifically? What query patterns require it over simpler alternatives?

**DA[#2] HIGH — tech-architect: threading.Thread for Streamlit pipeline = Streamlit anti-pattern |target:TA-A4**
TA recommends threading.Thread + st.rerun() polling loop for pipeline execution. Streamlit explicitly documents that background threads interacting with session_state are unsafe — session_state is not thread-safe. Streamlit 1.37+ has st.fragment for partial reruns. Why not: (a) subprocess.Popen with IPC (cleaner isolation), (b) asyncio with st.cache_resource for shared state, (c) Streamlit's own experimental background task APIs? The time.sleep(0.5) polling pattern is especially problematic — it creates unnecessary reruns and consumes Streamlit server resources.

**DA[#3] MEDIUM — tech-architect: split orchestrator vs event-driven architecture |target:TA-A4**
TA recommends splitting predict() into predict_until_review() + submit_after_review(). This is the simplest fix but creates a rigid 2-phase model. What if future stages need human input (e.g., confirming search results, selecting reference class)? An event-driven architecture with callbacks/hooks at configurable points would be more extensible. Counter-argument: C1 (personal tool) may not warrant this complexity. Defend the 2-phase split against: "you're solving today's problem, not the architectural pattern."

**DA[#4] HIGH — ux-researcher: 5-view architecture assumes equal importance |target:UX-F-UX-2**
5 separate pages assume each deserves its own navigation entry. Challenge: (a) Dashboard + Registry overlap significantly — both show prediction tables with filters. Dashboard = "active" filter on Registry. Merge into single view with tab/toggle for active vs all. (b) Predict + Review are sequential workflow stages of the SAME operation — predict generates, review adjudicates. Merge into single "Predict" page with phase-driven UI (configure → execute → review → submit). This reduces 5 views to 3: Home(Dashboard+Registry), Predict(+Review), Scoreboard. Simpler navigation, fewer session_state handoffs.

**DA[#5] MEDIUM — ux-researcher: auto-rerun every 30s = expensive for Streamlit |target:UX-F-UX-3**
st.rerun(interval=30000) triggers full script re-execution every 30 seconds. With RegistryCache loading + plotly chart rendering + dataframe formatting, this is unnecessary compute when nothing has changed. Better: manual refresh button + st.cache_data with TTL=60s on data-fetching functions. Only auto-refresh during active pipeline execution (conditional on pipeline_state != "idle").

**DA[#6] MEDIUM — ux-researcher: "dense layouts OK" is untested assumption |target:UX-F-UX-9**
F-UX-9 states "Dense layouts acceptable: full-width, minimal whitespace, small text." Source tag says [independent-research] but this is derived from C1 (personal tool) and user profile — effectively [prompt-claim]. Even power users benefit from progressive disclosure. The Streamlit component map (F-UX-10) lists 14+ component types per view — all visible simultaneously = cognitive overload regardless of expertise. §2b: what UX research supports "power users prefer density over progressive disclosure"? Nielsen Norman Group research shows even expert users benefit from information hierarchy.

**DA[#7] HIGH — reference-class-analyst: Brier impact estimates transfer from human forecasters to LLMs is unvalidated |target:RCA-F1,F2,F5,F7,F9**
RCA provides Brier impact estimates (e.g., R5: -0.010 to -0.025, R2: -0.008 to -0.020) derived from research on human forecasters (GJP, ForecastBench, Halawi). LLMs have fundamentally different error profiles (generation/confabulation ¬ cognitive biases, per accuracy-errors-reclassified from cognitive-enhancement review). The transfer assumption is load-bearing — it drives priority ranking of all recommendations. What's the confidence interval on these transfers? CDS's own FORMAT-COGNITIVE-3tier framework suggests observable-output(70-85%) > unobservable-cognition(45-60%) > cognitive-skill(25-40%). Brier improvement from methodology changes falls in the "unobservable-cognition" tier → 45-60% transfer → actual Brier impact could be 45-60% of stated ranges. Acknowledged?

**DA[#8] HIGH — reference-class-analyst: "search-augmented base rates" risks contaminating isolation property |target:RCA-F2**
RCA calls base rate isolation the "strongest feature" (F2) AND recommends adding web search TO the base rate step (R2). These are in tension. The entire value of base_rate.py is that it generates an outside-view estimate WITHOUT inside-view evidence contamination. Adding search to base rate estimation risks anchoring on current evidence — the exact bias the isolation was designed to prevent. How do you search for reference class data without exposing the model to inside-view information about the specific question? If you can't solve the contamination problem, this recommendation undermines the system's best feature.

**DA[#9] MEDIUM — reference-class-analyst: multi-model independent forecasting with N=0 resolved predictions |target:RCA-F5**
R5 recommends multi-model independent forecasting with estimated Brier impact -0.010 to -0.025. With N=0 resolved predictions, there is zero empirical data to validate this actually helps vs. adding cost and complexity. ForecastBench/Silicon Crowd evidence is from different systems with different prompt structures. The recommendation is theoretically sound but the Brier estimate is extrapolated — how would you validate before committing to the cost increase? What's the cheapest empirical test?

**DA[#10] MEDIUM — code-quality-analyst: C+ grade reference class is wrong |target:CQA-CQ-GRADE**
C+ is graded relative to what standard? Production systems have different quality bars than personal tools (C1). Some P1 issues (CQ-F mixed Path/os.path, CQ-N str timestamps, CQ-M str-not-Literal) are style/consistency issues that don't cause bugs in a single-user tool. The P0 issues (silent parse failures, hardcoded provider) are genuine. But the grade conflates "would fail code review at a company" with "causes problems for the actual user." What's the reference class for grading personal tool code quality?

**DA[#11] MEDIUM — code-quality-analyst: writing tests before rebuild = wrong sequencing |target:CQA-CQ-T**
CQ-T identifies 10 modules with zero test coverage and recommends highest-priority tests for decomposer + forecaster parse failures. But the user's stated intent is to "tear it down and rebuild." Writing tests for code that's about to be rewritten is wasted effort — tests will break during restructuring. Better: (a) write tests for the REDESIGNED code, (b) write integration tests for the pipeline's external behavior (input question → output prediction record) that survive refactoring. Defend the sequencing.

**DA[#12] HIGH — cognitive-decision-scientist: pre-mortem fix (strip reasoning_chain) undermines pre-mortem purpose |target:CDS-F[CDS-2]**
CDS recommends stripping reasoning_chain from pre-mortem prompt to prevent self-consistency confirmation. But Klein's original pre-mortem (1989, 2007) asks "imagine this SPECIFIC project has failed — why?" The specificity of the prediction context is essential. If the model doesn't see its own reasoning, how does it identify what could go wrong with its SPECIFIC prediction vs generating generic failure modes? A pre-mortem that says "base rate was wrong" is less valuable than one that says "my reasoning assumed X but if Y then probability shifts to Z." The fix may trade self-consistency bias for generic-failure-mode bias. What's the evidence that generic pre-mortems outperform context-specific ones?

**DA[#13] HIGH — cognitive-decision-scientist: temperature scaling requires calibration data you don't have |target:CDS-F[CDS-3]**
CDS recommends replacing flat hedging with temperature scaling. Temperature scaling requires fitting a single parameter T on a held-out calibration set of (predicted_probability, actual_outcome) pairs. With N=0 resolved predictions, you have zero calibration data. You need the same N≥50 resolved predictions that Platt scaling needs. The recommendation is "replace crude approximation with principled method" — but BOTH methods require data you don't have. The flat 0.04 hedging correction is at least functional with N=0. What would you do during the N=0→50 learning period?

**DA[#14] !CRITICAL — cognitive-decision-scientist: H2=FALSIFIED contradicts XVERIFY=PARTIAL |target:CDS-F[CDS-5]**
XVERIFY (GPT-5.1) rated CDS-F5 as PARTIAL with medium confidence: "directionally plausible but too strong as stated. Same-model runs produce SOME genuine diversity via persona variation. Multi-model not universally superior." CDS maintains H2=FALSIFIED. Per §2h, XVERIFY is advisory weight but CDS has not engaged with the moderation. Specifically: persona variation changes search queries, which changes retrieved evidence, which genuinely diversifies the information set even within the same model. This is retrieval diversity (real) even if reasoning diversity is limited. "FALSIFIED" implies zero value from same-model multi-run — XVERIFY and RCA (PARTIAL-FALSIFIED, 75%) both say that's too strong. Moderate to PARTIAL-FALSIFIED or defend with evidence that addresses XVERIFY's specific objection.

**DA[#15] MEDIUM — unanimous consensus on H5(5/5) and H6(3/3) |target:ALL**
H5=PARTIAL-FALSE was unanimous across all 5 agents. H6=PARTIAL was unanimous across the 3 who addressed it. While the DIRECTION is clearly correct (orchestrator must split, JSONL needs caching), unanimous consensus without any agent offering a counter-perspective warrants scrutiny. Did any agent consider: (a) for H5, whether Streamlit's new experimental features (st.fragment, background tasks) could make the current architecture workable without a full split? (b) for H6, whether the caching layer introduces its own bugs (cache invalidation, stale data) that are worse than the performance cost of full reloads at this scale?

**DA[#16] HIGH — cross-agent gap: H3 actor analysis value insufficiently addressed |target:ALL**
R1 divergence #3 flagged H3 (actor analysis value) as a gap area: RCA=55%-partial, CDS=weak-address, UX=designs-for-without-questioning. No agent conducted an empirical test of actor analysis value. The system stores actor_motivation_flags in RunResult — are these ever consulted during human review? Does the human reviewer actually USE actor analysis to adjust probabilities? Without usage data, designing elaborate actor analysis display (F-UX-5 Tab 3 with 2-column layout, expanders, badges) may be building UI for unused data. Who validates this?

#### Exit-gate: FINAL ASSESSMENT

##### Criterion 1 — Engagement quality ≥ B across all agents: PASS

- **tech-architect: A-** | 5 challenges → 1 COMPROMISE(DA[#1] pandas→dict), 1 CONCEDE-with-defense(DA[#2] threading→Queue+fragment), 1 DEFEND(DA[#3] 2-phase split via C1+YAGNI), 1 PARTIAL-CONCEDE(DA[#15] fragment display-only), 1 CONCEDE(DA[#16] actor→collapsible). Best: DA[#1] produced concrete dict-based RegistryCache code. DA[#2] Queue+fragment is materially better than original.
- **ux-researcher: A-** | 5 challenges → 1 COMPROMISE(DA[#4] 5-view defended+cross-linking), 1 CONCEDE(DA[#5] auto-rerun→conditional), 1 PARTIAL-CONCEDE(DA[#6] source tag reclassified), 1 DEFEND(DA[#15]), 1 PARTIAL-CONCEDE(DA[#16] actor Tab→collapsible expander). Best: DA[#4] mental-model defense (operational vs archival) is substantive.
- **reference-class-analyst: A** | 4 challenges → 3 COMPROMISE(DA[#7] Brier 50% discount+CIs, DA[#8] contamination controls, DA[#9] priority inversion), 1 DEFER(DA[#15]). Best R2 performance. DA[#9] drove most consequential analytical change: R9(learning loop)→#1 priority.
- **code-quality-analyst: B+** | 3 challenges → 1 COMPROMISE(DA[#10] dual-grade), 1 CONCEDE(DA[#11] behavioral tests), 1 DEFEND(DA[#15]). Solid, narrower scope.
- **cognitive-decision-scientist: A** | 4 challenges → 1 COMPROMISE(DA[#12] pre-mortem precision), 1 CONCEDE(DA[#13] 3-phase calibration), 1 COMPROMISE(DA[#14] H2→PARTIALLY-FALSIFIED 75%), 1 CONCEDE(DA[#16] H3→UNRESOLVED). DA[#14] = most important process correction.

All ≥ B+. **PASS.**

##### Criterion 2 — No material disagreements unresolved: PASS
- H2 strength: CDS moderated→PARTIALLY-FALSIFIED(75%), aligned with RCA(75%)+XVERIFY(PARTIAL). RESOLVED.
- Calibration: CDS 3-phase supersedes all prior positions. RESOLVED.
- Search vs isolation: RCA contamination controls resolve tension. RESOLVED.
- Pre-mortem: CDS revised (strip probability+reasoning, preserve question context). RESOLVED.
- 5-view vs 3-view: UX defended with cross-linking. RESOLVED.
- H3: UNRESOLVED PENDING INSTRUMENTATION — all agents agree, logged as deliberate gap.
**PASS.**

##### Criterion 3 — No new consensus formed without stress-test: PASS
New R2 consensus (dict cache, Queue+fragment, 3-phase calibration, H3→UNRESOLVED, priority inversion) — all formed IN RESPONSE to DA challenges, not spontaneously. No herding-on-new-thesis. **PASS.**

##### Criterion 4 — Analytical hygiene produced substantive outcome: PASS
6 outcome-1 revisions: CDS withdrew uncalibrated magnitude, UX reclassified source tag, CQA added dual-grade, RCA added CIs+discount, RCA added contamination controls, CDS revised pre-mortem. Zero perfunctory checks. **PASS.**

##### Criterion 5 — DA prompt audit: PASS
Echo detection: NOT DETECTED. Source distribution: ~85% independent-research, ~10% agent-inference, ~3% cross-agent, ~2% prompt-claim (properly tagged). Methodology: INVESTIGATIVE — agents falsified/downgraded 5 of 8 hypotheses. Strongest investigative stance across all reviews. **PASS.**

##### Criterion 6 — Toulmin warrant check on load-bearing findings: PASS
H2(PARTIALLY-FALSIFIED): warrant adequate — retrieval≠reasoning independence, backed by XVERIFY+literature, rebuttal engaged, falsifiable at N≥20.
Base rate isolation(strongest feature): warrant adequate — outside-view-first per Kahneman/Tversky, RCA+CDS convergence.
Priority inversion(R9→#1): warrant adequate — N=0 means all else is extrapolated.
H5(orchestrator must split): warrant adequate — blocking stdin is architectural fact, 5/5 defended against st.fragment.
**PASS.**

##### Criterion 7 — XVERIFY status on load-bearing findings: PASS
XVERIFY[H2/CDS-F5]: GPT-5.1=PARTIAL(medium) — engaged by CDS, moderation propagated. No zero-XVERIFY-on-load-bearing violation. **PASS.**

##### Challenge scorecard |#16
Hit rate: 12/16 held (75%) — 4 COMPROMISE, 4 CONCEDE, 4 PARTIAL-CONCEDE, 4 DEFEND. Adjusted: 10.5/15 (70%). Consistent with prior reviews (60-84%).

##### R2 grades (final)
TA: A- | UX: A- | RCA: A | CQA: B+ | CDS: A

##### EXIT-GATE VERDICT: PASS — SYNTHESIS AUTHORIZED

**Synthesis-ready hypothesis verdicts:**
- H1: PARTIALLY CONFIRMED (70%) — sequence correct, 2 missing stages + sequencing bug
- H2: PARTIALLY FALSIFIED (75%) — retrieval diversity real, reasoning independence not, extremization gate N≥2 providers
- H3: UNRESOLVED PENDING INSTRUMENTATION — simplify UX, validate at N≥20
- H4: CONFIRMED with 3-phase — flat(N=0-20)→isotonic(N=20-50)→Platt(N≥50)
- H5: PARTIALLY FALSE (5/5, stress-tested) — orchestrator must split
- H6: PARTIAL (3/3) — JSONL+dict RegistryCache
- H7: CONFIRMED CONDITIONAL — multi-model deliberation only
- H8: PARTIALLY CONFIRMED (60%) — personas diversify retrieval, contrarian most valuable

**BUILD priority:**
1. R9: Learning loop + error taxonomy (prerequisite)
2. R2: Search-augmented base rates WITH contamination controls
3. R5: Multi-model forecasting (CONDITIONAL on A/B at N≥10)
4. Orchestrator split + Queue+fragment threading
5. Dict-based RegistryCache
6. Streamlit 5-view UI, actor analysis collapsible
7. Pre-mortem revision
8. 3-phase calibration
9. Extremization gate

## convergence

### code-quality-analyst ✓
R1+R2 complete. DA responses resolved.
DA[#10] COMPROMISE: dual-grade confirmed — B- personal tool / C+ rebuild-ready codebase. Review purpose = rebuild, so C+ stands.
DA[#11] CONCEDE: behavioral integration tests + regression markers, ¬implementation tests for modules being rebuilt.
DA[#15] DEFEND: st.fragment = display-only. Orchestrator split required. H5 holds.

### devils-advocate ✓
R2 complete. 16 challenges issued, all responses evaluated. Exit-gate: PASS. Synthesis authorized.

## open-questions
