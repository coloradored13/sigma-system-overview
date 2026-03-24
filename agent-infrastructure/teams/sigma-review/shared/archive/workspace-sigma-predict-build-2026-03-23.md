# workspace — BUILD: sigma-predict Streamlit prediction hub + pipeline improvements
## status: active
## mode: BUILD
## round: r3
## belief-r1: P=0.82 |→ proceed-to-r2
## belief-r2: P=0.92 |interface-agree=0.95 |conflicts=0 |test-strategy=defined |effort-cal=yes |DA=PASS(B+) |→ proceed-to-r3-build
## DA-challenges: 13 issued, 13 resolved (10 concede, 2 compromise, 1 defend-confirmed)

## task
Build sigma-predict Streamlit prediction hub and pipeline improvements. Follows completed sigma-review (5+DA, exit-gate PASS, archived workspace-sigma-predict-review-2026-03-23.md). All architecture decisions are review-settled — implement, don't re-debate.

Codebase: ~/Projects/Zoltar/sigma-predict
Key files: src/models.py, src/pipeline/orchestrator.py, src/config.py, src/registry/{store,query}.py, src/pipeline/{decomposer,base_rate,forecaster,search,aggregator,calibration,verification,deliberation}.py, src/review/human_review.py, scripts/{predict,resolve,dashboard}.py

## prompt-decomposition
### Q[] — What to build
Q1: P0 bug fixes — 7 items (hardcoded provider, thread-unsafe mutation, pipeline_warnings, parse_failed, extract utils x2, import cleanup)
Q2: Orchestrator split — predict_until_review() + submit_after_review() with Queue-based threading + st.fragment polling
Q3: Streamlit hub — 5 views (Dashboard, Predict, Review, Scoreboard, Registry) + RegistryCache + session state + plotly charts
Q4: Data model enhancements — close_date, tags, provider, falsification_anchors, actor_analysis_consulted, Literal types, generic PlatformSignals
Q5: Learning loop — ErrorClass enum, auto-classification in resolve.py, Brier decomposition (reliability+resolution+uncertainty), 5 Scoreboard surfaces
Q6: Search-augmented base rates — contamination controls (query restriction, temporal firewall, separate model call, labeled output)
Q7: Pre-mortem fix — strip probability+reasoning, keep question+criteria+sub-questions+actors; add falsification_anchors prompt+field
Q8: 3-phase calibration — flat hedging (N<20) -> isotonic regression on logit (N=20-50) -> Platt (N>=50); extremization gate (N>=2 providers only)
Q9: Multi-model forecasting (conditional) — Gemini as primary on >=1 run, A/B validation at N>=10, challenge aggregate/median (not last run), deliberation triggers

### H[] — Implementation hypotheses
H1: The 7 P0 fixes can be made without breaking existing tests or pipeline behavior
H2: The orchestrator can be cleanly split at the review boundary without refactoring internal pipeline stages
H3: Streamlit 5-view app integrates with the split orchestrator + RegistryCache without additional pipeline changes
H4: 3-phase calibration is backward-compatible with existing calibration data and resolved records
H5: Phase 3 multi-model conditioning (N>=10, delta>0.005) is implementable with current registry data

### C[] — Constraints (review-settled + user-specified)
C1: Personal tool — no auth, no multi-user, no deployment
C2: Streamlit framework
C3: dict-based RegistryCache, NOT pandas, NOT SQLite
C4: JSONL registry remains source of truth
C5: sigma-verify integration for cross-model verification
C6: Queue + st.fragment for threading (review-settled)
C7: 5 views defended against merge to 3 (review-settled)
C8: Existing tests must continue passing
C9: Behavioral contract tests for pipeline; NO implementation unit tests for restructured modules
C10: All architecture decisions are review-settled — implement, don't re-debate

## scope-boundary
This build implements: P0 bug fixes, orchestrator split, Streamlit 5-view app, data model enhancements, learning loop, search-augmented base rates, pre-mortem fix, 3-phase calibration, multi-model forecasting (conditional)
This build does NOT implement: multi-user auth, deployment infrastructure, new platform integrations beyond existing stubs, mobile UI, historical context injection stage (identified in review but not in build spec), platform signal feedback loop, auto-weight disagreement into CI

## complexity-assessment
BUILD TIER-3 |scores: module-count(5),interface-changes(5),test-complexity(3),dependency-risk(3),team-familiarity(3) |total:19 |team-size:5

## infrastructure
SVerify: openai (gpt-5.1), google (gemini-3.1) available

## plans
### tech-architect

#### a) Scope — files+changes
- orchestrator.py: split predict() → predict_until_review() + submit_after_review() | move SearchModule+StageVerification imports to top-level | fix challenge_forecast call to use aggregate/median run ¬last-run
- llm_router.py:127-152: replace model mutation pattern with pass-model-as-param to AnthropicClient.call / openai / gemini | affects all 3 provider branches in LLMRouter.call()
- base_rate.py: add search_augmented_base_rate() helper | mandatory contamination controls (restricted query, temporal firewall, separate model call, labeled output) | called AFTER base LLM estimate, result is statistical anchor ¬replacement
- forecaster.py:210-218: strip probability+reasoning_chain from pre_mortem_user | keep question.title+resolution_criteria+sub_questions+actor_analysis | inject "This prediction FAILED. What went wrong?" | add falsification_anchors LLM call | populate RunResult.falsification_anchors (new field — coordinate CQA)
- deliberation.py: implement deliberate() — trigger on cross-model disagreement OR high-vulnerability challenge OR pre_mortem |delta|>0.1, NOT within-model stdev | fix should_deliberate() to reflect new trigger conditions
- verification.py: fix challenge_forecast() — accept aggregate/median RunResult ¬raw run; orchestrator passes computed representative run
- aggregator.py: add get_aggregate_run() helper — construct synthetic RunResult representing aggregate (probability=raw_aggregate, model="aggregate", reasoning summarized from all runs) — used by challenge_forecast fix

#### b) Assumptions — from other agents
- CQA: RunResult.falsification_anchors: list[str] field added (default_factory=list) — TA will populate, CQA owns schema
- CQA: RunResult.provider: str field added (default="") — Q9 multi-model tracking needs this
- CQA: PredictionRecord unchanged structurally for orchestrator split; PredictionRecord returned by predict_until_review() must be serializable (no threading state)
- RCA: calibrate() signature unchanged — TA calls it in submit_after_review() same as current predict()
- UX: UX imports predict_until_review()+submit_after_review() from orchestrator | UX owns Queue+st.fragment+session_state wiring | TA delivers clean sync functions, UX wraps in threading
- UX: Queue is passed in by UX caller — predict_until_review() accepts optional progress_queue: queue.Queue | None param; puts progress strings to it if provided

#### c) Interfaces — public function signatures

```python
# orchestrator.py

def predict_until_review(
    self,
    question: PlatformQuestion,
    platform_client: PlatformClient,
    num_runs: int = 1,
    personas: list[SearchPersona] | None = None,
    progress_queue: queue.Queue | None = None,
) -> PredictionRecord:
    """Run pipeline through calibration, stopping before human review.
    Puts progress strings to progress_queue if provided.
    Returns PredictionRecord with human_review=HumanReview(reviewed=False).
    Does NOT save to registry.
    """

def submit_after_review(
    self,
    record: PredictionRecord,
    human_review: HumanReview,
    platform_client: PlatformClient,
) -> PredictionRecord:
    """Apply human review, submit to platform, save to registry.
    Returns updated PredictionRecord with submission+registry write.
    """

# aggregator.py — new helper
def get_aggregate_run(runs: list[RunResult], aggregation: Aggregation) -> RunResult:
    """Construct synthetic RunResult representing aggregate for challenge_forecast."""

# base_rate.py — new helper (contamination-controlled)
def search_augmented_base_rate(
    base_rate: float,
    reference_class: str,
    search_module: SearchModule,
    router: LLMRouter,
    config: Config,
) -> tuple[float, str]:
    """Augment base rate with statistical-only web search.
    Returns (augmented_rate, citation_note).
    Contamination controls: restricted query, temporal firewall >=6mo, separate model call.
    """

# deliberation.py — revised trigger + implementation
def should_deliberate(
    aggregation: Aggregation,
    config: Config,
    challenge_entry: ChallengeEntry | None = None,
    pre_mortem_delta: float = 0.0,
) -> bool:
    """Trigger on cross-model disagreement (stdev>threshold) OR
    challenge vulnerability=="high" OR |pre_mortem_delta|>0.1."""
```

#### d) SQ[] sub-task decomposition
SQ[1]: LLMRouter thread-safety fix (llm_router.py:127-152) |estimable: yes |method: precedent (existing call pattern) |→ tech-architect
SQ[2]: Import cleanup — move SearchModule+StageVerification to top-level orchestrator imports |estimable: yes |method: trivial |→ tech-architect
SQ[3]: Add get_aggregate_run() to aggregator.py |estimable: yes |method: precedent (RunResult constructor) |→ tech-architect
SQ[4]: Fix challenge_forecast call in orchestrator.py (pass aggregate run) |estimable: yes |method: analogue (existing call pattern) |→ tech-architect
SQ[5]: Orchestrator split — extract predict_until_review() |estimable: yes |method: decompose (steps 1-5 of current predict()) |→ tech-architect
SQ[6]: Orchestrator split — extract submit_after_review() |estimable: yes |method: decompose (steps 6-end of current predict()) |→ tech-architect
SQ[7]: Pre-mortem fix — strip inputs, inject failure framing (forecaster.py:210-218) |estimable: yes |method: precedent (prompt construction) |→ tech-architect
SQ[8]: Falsification anchors — add LLM call in forecaster.py, populate field |estimable: yes |method: analogue (existing pre-mortem call) |→ tech-architect (requires CQA field)
SQ[9]: Search-augmented base rates — search_augmented_base_rate() with contamination controls |estimable: yes |method: analogue (existing search usage) |→ tech-architect
SQ[10]: Deliberation.py — revise should_deliberate() triggers, implement deliberate() skeleton with correct trigger logic |estimable: yes |method: decompose |→ tech-architect
SQ[11]: Q9 multi-model — add Gemini as primary on >=1 run (orchestrator run loop) |estimable: yes |method: analogue (existing run_forecast provider param) |→ tech-architect (conditional on A/B gate)
SQ[12]: Q9 A/B gate — validate delta>0.005 at N>=10 resolved before enabling multi-model |estimable: yes |method: decompose |→ tech-architect (reads registry query)

#### e) CAL[] effort estimates
CAL[SQ1]: point=0.5h |80%=[0.5,1h] |90%=[0.5,1.5h] |breaks-if: AnthropicClient.call() doesn't accept model kwarg (it doesn't currently — needs param added)
CAL[SQ2]: point=0.25h |80%=[0.25,0.5h] |90%=[0.25,0.5h] |breaks-if: circular import (unlikely, same module)
CAL[SQ3]: point=0.5h |80%=[0.5,1h] |90%=[0.5,1.5h] |breaks-if: RunResult fields missing (coordinate CQA)
CAL[SQ4]: point=0.25h |80%=[0.25,0.5h] |90%=[0.25,0.5h] |breaks-if: SQ3 not done
CAL[SQ5]: point=1.5h |80%=[1.5,3h] |90%=[1.5,4h] |breaks-if: hidden state in predict() not exposed cleanly (cost tracking, timing)
CAL[SQ6]: point=1h |80%=[1,2h] |90%=[1,3h] |breaks-if: HumanReview field changes (CQA scope)
CAL[SQ7]: point=0.5h |80%=[0.5,1h] |90%=[0.5,1.5h] |breaks-if: pre_mortem prompt format incompatible (LLM context change)
CAL[SQ8]: point=1h |80%=[1,2h] |90%=[1,3h] |breaks-if: CQA falsification_anchors field not added before TA runs
CAL[SQ9]: point=2h |80%=[2,4h] |90%=[2,6h] |breaks-if: Tavily temporal_filter API unavailable or mis-documented
CAL[SQ10]: point=1h |80%=[1,2h] |90%=[1,3h] |breaks-if: ChallengeEntry.vulnerability field type inconsistent (currently str, need "high"|"medium"|"low")
CAL[SQ11]: point=1h |80%=[1,2h] |90%=[1,3h] |breaks-if: Gemini router path not threadsafe (feeds from SQ1)
CAL[SQ12]: point=1.5h |80%=[1.5,3h] |90%=[1.5,4h] |breaks-if: registry query count_resolved() has no field filter for multi-model entries
total-estimate: point=10.5h |80%=[10.5,21h] |90%=[10.5,30h]

#### f) PM[] pre-mortems
PM[1]: orchestrator split fails — hidden side-effects in predict() prevent clean boundary |probability:25% |early-warning: cost_tracking accumulated across both halves; timing (pipeline_start) spans the split |mitigation: pipeline_start+total_cost init in predict_until_review(); pass accumulated cost in PredictionRecord.cost so submit_after_review() reads ¬recomputes
PM[2]: LLMRouter thread-safety fix breaks AnthropicClient.call() signature |probability:20% |early-warning: AnthropicClient.call() currently takes no model param — must add it |mitigation: add optional model param to AnthropicClient.call(); default to self.model for backward compatibility; existing direct callers unaffected
PM[3]: search_augmented_base_rate contamination controls insufficient — Tavily doesn't support reliable temporal filtering |probability:35% |early-warning: Tavily docs show include_published_date param but not a reliable cutoff filter |mitigation: apply temporal filter in post-processing (check result publication date strings client-side, exclude if <6mo old); if date unavailable, flag result as unverified ¬exclude (conservative)
PM[4]: Deliberation implementation triggers on wrong signal — stdev condition preserved from stub conflicts with new trigger spec |probability:30% |early-warning: should_deliberate() currently uses stdev only; new spec adds vulnerability+pre_mortem triggers |mitigation: rewrite should_deliberate() to accept challenge_entry+pre_mortem_delta params; remove stdev-only path; orchestrator must pass both
PM[5]: Multi-model Gemini run adds latency spike — no timeout enforcement per run |probability:40% |early-warning: current run_forecast has no timeout; Gemini calls through sigma-verify can be slow |mitigation: wrap Gemini run_forecast call in concurrent.futures.ThreadPoolExecutor with timeout; on timeout, skip Gemini run and log warning

#### g) Analytical hygiene checks
§2a (default approach / simpler alternative?):
- LLMRouter fix: try/finally model restoration is current pattern → outcome 2 (confirms) BUT actually preserves a mutable-state design that's thread-unsafe by construction. Simpler: pass model directly to client.call() eliminating state mutation entirely. → outcome 1: changes plan (confirmed in scope as the fix)
- Orchestrator split at step 6: is there a simpler 80% alternative? Could pass auto_submit=True and skip review in same function. → outcome 2: no — Q2 explicitly requires split for Queue-based threading. Split is justified.
- Search augmentation in base_rate: could just improve prompt instead of adding search. → outcome 2: review-settled (Q6 spec), no re-debate

§2b (precedent from project / industry norm?):
- Queue-based threading + st.fragment: Streamlit docs recommend this pattern for long-running tasks. → outcome 2 (confirms)
- AnthropicClient.call() adding model param: precedent from sigma-verify OpenAI/Gemini clients which DO pass model directly. → outcome 2 (confirms, consistent pattern)
- Temporal firewall implementation: no existing precedent in this codebase; industry norm is client-side date filtering on search results. → outcome 3 (gap — implementation detail TBD in build)

§2c (maintenance cost justified?):
- search_augmented_base_rate: adds a full search + separate LLM call per prediction (~$0.002-0.005 extra). Adds complexity. Justified only if contamination controls hold. → outcome 3 (gap — contamination control reliability is a build risk; should gate on config flag)
- Deliberation implementation: currently a stub; implementing with new triggers adds complexity. Justified by Q9 scope. → outcome 2 (confirms)

§2e (assumptions — verified or speculative?):
- VERIFIED: PredictionRecord is a Pydantic model — safe to pass between thread contexts (immutable after construction, JSON-serializable)
- VERIFIED: RunResult.falsification_anchors MISSING from models.py (line 90-106) — CQA must add this field before SQ8 can build
- VERIFIED: LLMRouter.call() mutates self._anthropic.model (line 128) — thread-unsafe confirmed; fix is clear
- VERIFIED: challenge_forecast takes RunResult (last run) at orchestrator.py:207 — wrong; spec says challenge aggregate/median
- VERIFIED: deliberation.py:21 — should_deliberate() currently only checks stdev; new spec requires cross-model+vulnerability+pre_mortem triggers
- SPECULATIVE: Tavily supports temporal filtering via published_date metadata — needs verification in build (PM[3])
- SPECULATIVE: Q9 A/B validation will show delta>0.005 — not verifiable until N>=10 resolved predictions exist (may be long wait)

#### h) Risks and dependencies
RISK[1]: CQA falsification_anchors field not added before TA SQ8 — blocks pre-mortem falsification build |mitigation: TA completes SQ1-7 first; SQ8 conditional on CQA delivery
RISK[2]: UX Queue integration contract unclear — if UX passes queue differently than TA's progress_queue param, wiring breaks |mitigation: interface declared in §c above; UX must confirm acceptance
RISK[3]: Q9 conditional — A/B gate may never trigger during this build (need N>=10 resolved predictions). SQ11-12 may be deferred-complete (implemented but never activated) |mitigation: implement gate correctly; do not skip implementation
RISK[4]: Deliberation full implementation is a stub becoming real — needs supervisor agent prompt which doesn't exist yet |mitigation: implement trigger logic + routing; deliberate() can call run_forecast with "supervisor" persona as minimal implementation; full supervisor agent prompt = stretch goal

#### i) Interface contracts with other agents
FROM CQA (TA needs):
- RunResult.falsification_anchors: list[str] = Field(default_factory=list)
- RunResult.provider: str = "" (for Q9 multi-model tracking, to distinguish runs)
- No breaking changes to PredictionRecord, Aggregation, CalibrationData

FROM RCA (TA needs):
- calibrate() signature unchanged: (probability, config, platt_params, n_resolved) → (float, dict)
- load_platt_params() unchanged

TO UX (UX needs from TA):
- predict_until_review(question, platform_client, num_runs, personas, progress_queue) → PredictionRecord
- submit_after_review(record, human_review, platform_client) → PredictionRecord
- progress_queue receives str messages (e.g., "Step 1/7: Decomposing question...")
- PredictionRecord is safe to store in session_state (Pydantic, JSON-serializable)

TO CQA (CQA needs from TA):
- No new fields added to PredictionRecord by TA (only RunResult.falsification_anchors which CQA owns)
- deliberation.py should_deliberate() new signature (challenge_entry, pre_mortem_delta params) — CQA may need to adjust any test mocks

H2 EVIDENCE — split feasibility:
FOR: predict() has a clear natural boundary at step 6 (human review) — everything before is pipeline computation, everything after is write+submit. No shared mutable state across boundary except PredictionRecord object. Cost tracking (total_cost) and timing (pipeline_start) are straightforward to split — set latency in predict_until_review().
AGAINST: cost_tracking is accumulated across the full predict() including submission overhead. Splitting means submit_after_review() cannot accurately track submission latency. Mitigation: CostTracking is additive; submit_after_review() creates its own tracking for submission step only.
VERDICT: H2 CONFIRMED — clean split is achievable. No internal pipeline stages need refactoring. Single boundary point at step 6.

#### j) DA responses — r2

DA[#2]: CONCEDE — calibrate() isotonic_data wiring missing from SQ5
Evidence: RegistryQuery.get_calibration_pairs() exists at query.py:46 — returns list[tuple[float,float]]. RCA adding isotonic_data param to calibrate(). Wiring belongs in SQ5.
Action: SQ5 updated. §b: calibrate() will include isotonic_data param (RCA delivers).

DA[#4]: CONCEDE — warnings_out wiring missing from SQ5
Evidence: CQA plan (above) confirms pipeline_warnings on PredictionRecord + warnings_out param on decompose_question()+estimate_base_rate(). Both called in predict_until_review(). 2-line wiring per call site.
Action: SQ5 updated to include warnings_out=record.pipeline_warnings at both call sites.

DA[#5]: CONCEDE — n_distinct_providers not wired to aggregate_runs()
Evidence: RCA adding n_distinct_providers param for extremization gate. Computation: len(set(r.provider for r in record.runs)) after run loop. Requires CQA RunResult.provider field.
Action: Merged into SQ5. Dependency: CQA.provider → SQ5.

DA[#6]: CONCEDE — deliberation trigger wiring underspecified
Evidence: challenge_entry lives at challenge_sv.challenges[0] (orchestrator.py:212-220). Pre-mortem delta: max(abs(r.pre_mortem_delta) for r in record.runs) — worst case across all runs, default=0.0.
Action: SQ10 updated with exact extraction logic.

DA[#11]: COMPROMISE — extend pre-mortem JSON schema, NOT a separate LLM call
DA challenge is correct: separate call is gold-plating. pm_data is already parsed JSON. Add falsification_anchors key to pre-mortem output schema — zero extra latency, zero extra cost.
Action: SQ8 revised → extend pre-mortem prompt + extract pm_data.get("falsification_anchors", []). CAL[SQ8]: point=0.5h (was 1h).

DA[#13]: CONCEDE (partial) — sigma-verify call() is immutable; Option A (per-thread Orchestrator) is the fix
Evidence VERIFIED: sigma_verify/clients.py OpenAIClient.call() + GeminiClient.call() are (system, user_content, temperature, max_tokens) — no model param. Cannot change external library.
Analysis: LLMRouter.call() try/finally mutation for OpenAI/Gemini is inherently thread-unsafe. Fix: UX creates new Orchestrator(config) per threading.Thread — each thread owns its own LLMRouter+client instances, so self.model mutation is thread-local. No LLMRouter code change needed for these paths.
Action: SQ1 scope NARROWED → fix AnthropicClient only (add model param, remove mutation). Add code comment on OpenAI/Gemini paths. Interface TO UX updated: "MUST create new Orchestrator per thread." RISK[5] added.

#### k) Updated SQ[] (post-DA)
SQ[5] UPDATED: predict_until_review() | SCOPE adds: (a) isotonic_data=self.query.get_calibration_pairs()→calibrate(); (b) warnings_out=record.pipeline_warnings at decompose_question()+estimate_base_rate(); (c) n_providers=len(set(r.provider for r in record.runs))→aggregate_runs(); (d) extract challenge_entry from challenge_sv.challenges[0] + pm_delta=max(abs(r.pre_mortem_delta) for r in record.runs, default=0.0) → should_deliberate()
SQ[8] UPDATED: extend pre-mortem prompt JSON schema to output falsification_anchors: list[str]; extract pm_data.get("falsification_anchors",[]); assign to run_result.falsification_anchors. NO separate LLM call.
SQ[10] UPDATED: should_deliberate(aggregation, config, challenge_entry: ChallengeEntry|None, pre_mortem_delta: float) — triggers: challenge.vulnerability=="high" OR |pre_mortem_delta|>0.1 OR cross-model stdev>threshold. Remove stdev-only path.

#### l) Updated §b assumptions (post-DA)
- CQA: PredictionRecord.pipeline_warnings: list[str] = Field(default_factory=list) [DA[#4]]
- CQA: decompose_question()+estimate_base_rate() accept warnings_out param [DA[#4]]
- RCA: calibrate() adds isotonic_data: list[tuple[float,float]] param [DA[#2]]
- RCA: aggregate_runs() adds n_distinct_providers: int param [DA[#5]]
- UX: MUST create new Orchestrator(config) per threading.Thread — NOT shared instance [DA[#13]]

#### m) RISK[5] (post-DA)
RISK[5]: UX shares single Orchestrator across threads — OpenAI/Gemini self.model mutation in LLMRouter.call() is thread-unsafe, unfixable without modifying sigma-verify. Mitigation: per-thread Orchestrator (interface contract). Lead to notify UX.

### code-quality-analyst

#### a) Scope: exact files + line ranges

**P0-1 — Hardcoded provider replacement**
- decomposer.py:64 → `"anthropic"` → `config.primary_model.provider`
- base_rate.py:78 → `"anthropic"` → `config.primary_model.provider`
- forecaster.py: already correct (prov = provider or config.primary_model.provider at line 137) — no change needed

**P0-3 — pipeline_warnings on parse failure**
- models.py: add `pipeline_warnings: list[str] = Field(default_factory=list)` to PredictionRecord (after line 225)
- decomposer.py:76-81: add `warnings_out: list[str] | None = None` optional param to `decompose_question`; on JSONDecodeError, append `"decomposition_parse_failure"` to warnings_out if provided, then return Decomposition()
- base_rate.py:103-106: same pattern — `estimate_base_rate` gets `warnings_out: list[str] | None = None`; append `"base_rate_parse_failure"` on parse failure
- TA coordination: predict_until_review() must pass `warnings_out=record.pipeline_warnings` at both call sites

**P0-4 — parse_failed on RunResult**
- models.py: add `parse_failed: bool = False` to RunResult (after line 106)
- forecaster.py:200-203: set local `_parse_failed = True` on JSONDecodeError; pass `parse_failed=_parse_failed` to RunResult constructor at line 243

**P0-5 — Extract _extract_json() and _load_prompt() to utils.py**
- Create: `src/pipeline/utils.py`
- Extract `_extract_json(text)`: decomposer.py:151-171 + base_rate.py:27-44 + forecaster.py:34-51 (char-for-char identical)
- Extract `_load_prompt(config, filename)`: decomposer.py:24-27 + forecaster.py:28-31 (char-for-char identical)
- CRITICAL: base_rate.py:21-24 has DIFFERENT signature `_load_prompt(config)` with hardcoded filename. Unify: update base_rate.py call at line 63 to `_load_prompt(config, "base_rate.md")`
- Remove local defs from decomposer.py, base_rate.py, forecaster.py; add `from src.pipeline.utils import _extract_json, _load_prompt`

**P0-6 — Extract scoring functions to src/scoring.py**
- Create: `src/scoring.py`
- Extract `brier_score(predicted, actual)`: resolve.py:23-25 + dashboard.py:23-24 (identical)
- Extract `log_score(predicted, actual)`: resolve.py:28-34 (dashboard does not use — brier only)
- resolve.py: remove lines 23-34; add `from src.scoring import brier_score, log_score`
- dashboard.py: remove lines 23-24; add `from src.scoring import brier_score`

**Q4 — Data model enhancements (src/models.py)**
- Add `from typing import Literal` (line 3 area)
- PredictionRecord: add `close_date: str = ""`, `tags: list[str] = Field(default_factory=list)`, `pipeline_warnings: list[str] = Field(default_factory=list)`
- RunResult: add `parse_failed: bool = False`, `provider: str = ""`, `falsification_anchors: list[str] = Field(default_factory=list)`; add `provider=prov` to RunResult constructor at forecaster.py:243
- HumanReview: add `actor_analysis_consulted: bool = False`
- Actor.influence_estimate (line 58): `str` → `Literal["low","medium","high"]`
- VerificationEntry.assessment (line 164): `str` → `Literal["agree","disagree","partial","uncertain"]`
- VerificationEntry.confidence (line 165): `str` → `Literal["high","medium","low"]`
- ChallengeEntry.vulnerability (line 178): `str` → `Literal["high","medium","low"]`
- PlatformSignals (line 126-132): `default_factory=lambda: {hardcoded-keys}` → `Field(default_factory=dict)`. RISK: orchestrator.py:363 key-check becomes False for new empty-dict records; fallback at 365 handles correctly.

**Behavioral contract tests — tests/test_pipeline_contract.py (NEW)**

#### b) Assumptions

- TA: predict_until_review() must pass `warnings_out=record.pipeline_warnings` at decompose_question + estimate_base_rate call sites (optional param — no crash if missed, but warnings stay empty silently)
- TA: RunResult.provider field added by CQA; forecaster.py already has `prov` local var at line 137 — CQA adds `provider=prov` to RunResult constructor. TA does not duplicate.
- RCA: `src/scoring.py` available for import. No further coordination.
- UX: no direct CQA dependency.

#### c) Interfaces: new/changed signatures

```python
# src/pipeline/utils.py (NEW)
def _extract_json(text: str) -> str: ...
def _load_prompt(config: Config, filename: str) -> str: ...

# src/scoring.py (NEW)
def brier_score(predicted: float, actual: float) -> float: ...
def log_score(predicted: float, actual: float) -> float: ...

# decomposer.decompose_question (CHANGED — optional param added)
def decompose_question(
    question: PlatformQuestion, config: Config,
    router=None, warnings_out: list[str] | None = None
) -> Decomposition: ...

# base_rate.estimate_base_rate (CHANGED — optional param added)
def estimate_base_rate(
    question_text: str, sub_questions: list[str], reference_class: str,
    config: Config, router=None, warnings_out: list[str] | None = None
) -> tuple[float, str, str]: ...

# models new fields (abbreviated):
# PredictionRecord: pipeline_warnings, close_date, tags
# RunResult: parse_failed, provider, falsification_anchors
# HumanReview: actor_analysis_consulted
# Actor.influence_estimate → Literal["low","medium","high"]
# VerificationEntry.assessment → Literal["agree","disagree","partial","uncertain"]
# VerificationEntry.confidence → Literal["high","medium","low"]
# ChallengeEntry.vulnerability → Literal["high","medium","low"]
# PlatformSignals.prices_at_prediction_time → dict[str, float | None] = Field(default_factory=dict)
```

#### d) SQ[] sub-task decomposition

SQ1: Create `src/pipeline/utils.py` — `_extract_json` + unified `_load_prompt`
SQ2: Update decomposer.py — import utils, remove local defs, fix provider (P0-1), add warnings_out (P0-3)
SQ3: Update base_rate.py — import utils, remove local defs, fix provider (P0-1), add warnings_out (P0-3)
SQ4: Update forecaster.py — import utils, remove local defs, add parse_failed (P0-4), add provider to RunResult constructor
SQ5: Update models.py — Literal import + all field additions + Literal type changes
SQ6: Create `src/scoring.py` — `brier_score` + `log_score`
SQ7: Update scripts/resolve.py — import from scoring, remove local defs
SQ8: Update scripts/dashboard.py — import from scoring, remove local def
SQ9: Write `tests/test_pipeline_contract.py` — behavioral contract tests
SQ10: Run existing pytest suite — verify no regressions

#### e) CAL[] effort estimates

CAL[SQ1]: point=0.25h (pure extraction)
CAL[SQ2]: point=0.5h (3 distinct changes)
CAL[SQ3]: point=0.5h (signature unification risk)
CAL[SQ4]: point=0.25h (2 targeted changes)
CAL[SQ5]: point=1h (Literal validation risk)
CAL[SQ6]: point=0.25h (pure extraction)
CAL[SQ7,SQ8]: point=0.25h each
CAL[SQ9]: point=1.5h (mocking strategy is hardest part)
CAL[SQ10]: point=0.25h
total: point=5h |80%=[5,8h]

#### f) PM[] pre-mortem

PM1: **Literal types break on existing registry data** — If data/predictions/registry.jsonl has Actor/VerificationEntry/ChallengeEntry records with `""` or non-Literal strings, Pydantic raises ValidationError on load. Mitigation: inspect registry.jsonl before switching types; if records exist with invalid values, add validator to coerce → safe defaults rather than hard fail.
PM2: **PlatformSignals generic dict changes key semantics** — orchestrator.py:363 key-check becomes False for all new records. Fallback at 365 handles correctly. Behavioral change: new records use platform name as key ¬`platform_community`. Old records retain old keys. Flag in convergence.
PM3: **warnings_out TA coordination gap** — If TA omits `warnings_out=record.pipeline_warnings` passthrough, pipeline_warnings stays empty silently. Not a crash. Flag in convergence note.
PM4: **base_rate._load_prompt unification** — One internal call site at line 63. After unifying, update to `_load_prompt(config, "base_rate.md")`. Grep confirms no external imports. Low risk.
PM5: **Contract tests over-mock** — Full Orchestrator mock stack tests Python wiring only, not behavior. Mitigation: test at model field level directly; for orchestrator-level tests use shallow mocks (`router.call` returns minimal valid JSON, `auto_submit=True`).

#### g) Analytical hygiene — §2a/§2b/§2c/§2e

§2a (H1 — P0 fixes break nothing):
- OUTCOME 2 (confirms): Existing tests do NOT import decomposer/base_rate/forecaster. Optional params + new fields are backward-compatible. H1 holds via code analysis. |source:[independent-research]
- RESIDUAL: structural verification only — no existing tests exercise modified modules. SQ9 fills this.

§2b (coverage gap):
- OUTCOME 3 (gap): ZERO existing tests for orchestrator.py, decomposer.py, base_rate.py, forecaster.py. SQ9 is required.

§2c (dependency ordering):
- OUTCOME 1 (change needed): SQ1 before SQ2/3/4; SQ6 before SQ7/8; SQ5 before SQ9.

§2e (verified facts):
- VERIFIED: `_extract_json` in decomposer.py:151-171, base_rate.py:27-44, forecaster.py:34-51 — char-for-char identical
- VERIFIED: `_load_prompt(config, filename)` in decomposer.py:24-27 and forecaster.py:28-31 — char-for-char identical
- VERIFIED: `brier_score` in resolve.py:23-25 and dashboard.py:23-24 — identical
- VERIFIED: forecaster.py already has `prov` local var — P0-1 fix NOT needed in forecaster
- VERIFIED: Pydantic v2 Field(default_factory=...) pattern throughout models.py

#### h) Test plan — behavioral contract tests

**What to test:**
- PredictionRecord field defaults: `pipeline_warnings==[]`, `close_date==""`, `tags==[]`
- RunResult field defaults: `parse_failed==False`, `provider==""`, `falsification_anchors==[]`
- HumanReview field default: `actor_analysis_consulted==False`
- JSONL roundtrip: PredictionRecord with new fields → save via RegistryStore → load → all new fields preserved
- `parse_failed` flag: mock `router.call` to return `"not json"` → `RunResult.parse_failed == True`
- Provider propagation: `RunResult.provider == config.primary_model.provider`
- DA[#4] ADDED: `pipeline_warnings` end-to-end wiring — patch `decomposer.LLMRouter` to return unparseable JSON → call `decompose_question` with a `warnings_out=[]` list → assert list contains `"decomposition_parse_failure"`. Confirms param wiring works; TA test variant: call through `predict_until_review` mock → assert `record.pipeline_warnings` non-empty. Test fails if TA omits passthrough — makes dep enforceable.
- DA[#8] ADDED: Literal type migration safety — `ChallengeEntry(vulnerability="")` and `ChallengeEntry(vulnerability="HIGH")` → assert both raise `ValidationError`. If either passes (Pydantic accepts it), add `@field_validator("vulnerability", mode="before")` coercion to models.py. Test outcome drives models.py decision.

**What NOT to test (per C9):**
- `_extract_json()` logic, `_load_prompt()` — implementation tests for restructured modules
- Aggregation math — covered by test_aggregator.py
- Calibration math — covered by test_calibration.py
- Platform mapping — covered by test_platform_clients.py
- Real API calls

#### i) Dependency ordering (implementation sequence)

1. SQ1 + SQ6 (parallel): utils.py + scoring.py (no deps)
2. SQ2, SQ3, SQ4 (parallel): decomposer/base_rate/forecaster (require SQ1)
3. SQ5: models.py — run DA[#8] Literal safety test FIRST; add coercion validator if needed; then apply all field changes
4. SQ7, SQ8 (parallel): resolve.py/dashboard.py (require SQ6)
5. SQ9: contract tests (require SQ5; includes DA[#4] wiring test + DA[#8] Literal test)
6. SQ10: pytest run (must be last)

#### j) DA responses (r2)

DA[#4] — warnings_out wiring: CONCEDE — PM3 left this as a prose note. DA correctly elevates to testable contract. Adding to SQ9: patch decomposer LLM → return unparseable JSON → assert `pipeline_warnings` non-empty. Makes TA dependency enforceable rather than advisory.

DA[#8] — Literal type migration risk undertested: CONCEDE — PM1 deferred to manual inspection. Contract test is machine-verifiable and drive-models.py decisions. Adding: `ChallengeEntry(vulnerability="")` → assert `ValidationError`; `ChallengeEntry(vulnerability="HIGH")` → assert `ValidationError`. Test outcome determines whether `@field_validator` coercion needed. Run BEFORE finalizing models.py. SQ5 ordering updated.

DA[#12] — provider field population ownership: CONCEDE — confirming explicitly: CQA owns BOTH `RunResult.provider: str = ""` field (models.py) AND `provider=prov` at forecaster.py:243. TA does NOT touch forecaster.py:243. No plan change — ownership now unambiguous.

### ux-researcher

#### a) Scope — files + component inventory

Files created:
```

Files created:
```
app.py                          # st.navigation entry point, Config init, cache_resource setup
pages/1_Dashboard.py            # 4-metric strip + active predictions table + cross-nav
pages/2_Predict.py              # 35/65 split: question discovery + run config + pipeline thread + inline review
pages/3_Review.py               # selectbox + 4 tabs: Summary/Runs/Verification/Resolution
pages/4_Scoreboard.py           # calibration analytics + 5 learning loop surfaces
pages/5_Registry.py             # filter bar + full history table + CSV download
components/cache.py             # RegistryCache (dict-based, dirty-flag invalidation)
components/state.py             # session_state key string constants + init_state() helper
components/charts.py            # plotly builders: calibration_curve, brier_timeline, domain_brier, cost_stacked_bar, error_class_freq, adjustment_scatter, probability_waterfall
```

Component inventory per page:
- Dashboard: st.metric x4, st.dataframe (ProgressColumn, countdown col), st.button (manual refresh), st.fragment (conditional auto-rerun on pipeline_state=="running" only)
- Predict: st.columns([35,65]), st.selectbox (platform), st.radio (search/ID/URL), st.dataframe (results, on_select), st.number_input (runs), st.multiselect (personas), st.toggle (verification), @st.fragment pipeline progress poller (st.status inside), st.radio+st.slider+st.text_area+st.button (inline review — visible only when pipeline_state=="awaiting_review")
- Review: st.selectbox (prediction), st.tabs x4 (Summary/Runs/Verification/Resolution), st.expander (decomposition), st.expander (actor analysis, collapsed by default — H3 unvalidated), st.warning (per flag), st.dataframe (runs comparison), st.expander per run (waterfall chart), st.expander per stage (agreement badge), st.form (add lesson)
- Scoreboard: st.date_input, st.multiselect (domain), plotly calibration_curve (primary), plotly brier_timeline, plotly domain_brier, plotly cost_stacked_bar, plotly error_class_freq, st.dataframe (lessons feed), st.metric (pre-mortem effectiveness %), plotly adjustment_scatter
- Registry: st.multiselect x3 (platform, domain, status) + st.date_input + st.text_input (filters), st.dataframe (ProgressColumn), st.download_button (CSV)

#### b) Assumptions — interfaces from other agents

TA (orchestrator split — Q2):
- `orchestrator.predict_until_review(question, platform_client, num_runs, personas, progress_queue) -> PredictionRecord` — runs steps 1-5, writes progress strings to Queue, returns record with human_review.reviewed=False, does NOT save to registry
- `orchestrator.submit_after_review(record, human_review, platform_client) -> PredictionRecord` — applies review, submits, saves to registry, returns updated record
- `progress_queue` is `queue.Queue[str | None]` — None sentinel signals pipeline complete
- TA confirmed: PredictionRecord is safe to store in session_state (Pydantic, JSON-serializable)
- TA interface is instance methods on Orchestrator class (¬module-level functions based on TA plan §c)

CQA (data model enhancements — Q4):
- `PredictionRecord.close_date: str = ""` — used in Dashboard countdown
- `PredictionRecord.tags: list[str] = []` — used in Registry filter (if present)
- `PredictionRecord.provider: str = ""` — visible in Registry display
- `resolution.error_class_auto: list[str]` — already in models.py (confirmed) — drives Scoreboard error bar
- `actor_analysis_consulted: bool` — flag for actor analysis display in Review

RCA (scoring/calibration — Q5):
- Brier decomposition: importable function (module TBD) with signature `brier_decompose(pairs: list[tuple[float,float]]) -> dict` returning dict with keys "reliability", "resolution", "uncertainty" (DA[#3]: dict ¬typed object — bracket notation throughout Scoreboard)
- `auto_classify_error(record: PredictionRecord) -> list[str]` callable for Scoreboard error frequency bar
- If RCA functions not yet available: Scoreboard learning loop surfaces show `st.info("Learning loop available after N>=10 resolved predictions")` placeholder

!ASSUMPTION: All new-field accesses use `getattr(record, 'field', default)` for graceful degradation if CQA fields not yet merged.

#### c) Interfaces — imports + session_state keys

Session state keys (components/state.py string constants):
```python
KEY_SELECTED_PREDICTION_ID = "selected_prediction_id"   # str | None — Dashboard/Registry → Review cross-nav
KEY_PIPELINE_STATE = "pipeline_state"                   # "idle" | "running" | "awaiting_review"
KEY_PIPELINE_RECORD = "pipeline_record"                 # PredictionRecord | None — set when thread done
KEY_PIPELINE_QUESTION = "pipeline_question"             # PlatformQuestion | None — retained for submit_after_review
KEY_PIPELINE_CLIENT = "pipeline_client"                 # PlatformClient | None — retained for submit_after_review
KEY_SEARCH_RESULTS = "search_results"                   # list[PlatformQuestion] — question discovery results
KEY_SELECTED_PLATFORM = "selected_platform"             # str — platform selectbox value
KEY_REGISTRY_FILTERS = "registry_filters"               # dict — active Registry filters
KEY_SCOREBOARD_DATE_RANGE = "scoreboard_date_range"     # tuple[date, date]
KEY_SCOREBOARD_DOMAINS = "scoreboard_domains"           # list[str]
```

cache_resource (thread-safe, app-lifetime, survives page navigation):
```python
@st.cache_resource
def get_registry_cache(registry_path: str) -> RegistryCache: ...

@st.cache_resource
def get_pipeline_queue() -> queue.Queue: ...
```

init_state() helper (called at top of every page):
```python
def init_state():
    defaults = {KEY_SELECTED_PREDICTION_ID: None, KEY_PIPELINE_STATE: "idle",
                KEY_PIPELINE_RECORD: None, KEY_PIPELINE_QUESTION: None,
                KEY_PIPELINE_CLIENT: None, KEY_SEARCH_RESULTS: [],
                KEY_SELECTED_PLATFORM: "metaculus", KEY_REGISTRY_FILTERS: {},
                KEY_SCOREBOARD_DATE_RANGE: None, KEY_SCOREBOARD_DOMAINS: []}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
```

Imports from src (by file):
- cache.py: `from src.registry.store import RegistryStore; from src.models import PredictionRecord`
- charts.py: `import plotly.graph_objects as go; from src.models import PredictionRecord` (takes plain data, not cache)
- Dashboard: `from components.cache import RegistryCache; from components.state import *; from components.charts import brier_timeline_chart`
- Predict: `from src.pipeline.orchestrator import Orchestrator; from src.models import SearchPersona, Platform, HumanReview; from src.config import Config; import queue, threading`
- Review: `from components.cache import RegistryCache; from components.state import *; from components.charts import probability_waterfall_chart`
- Scoreboard: `from components.cache import RegistryCache; from components.charts import *`
- Registry: `from components.cache import RegistryCache; from components.state import *`
- app.py: `import streamlit as st; from src.config import Config; from src.registry.store import RegistryStore; from components.cache import RegistryCache`

#### d) SQ[] sub-task decomposition

SQ1: components/state.py — key constants + init_state() helper |no deps
SQ2: components/cache.py — RegistryCache exactly as spec |deps: SQ1
SQ3: components/charts.py — 7 plotly/visual builders |no src deps
SQ4: app.py — st.navigation wiring, Config+RegistryStore init, cache_resource declarations |deps: SQ1, SQ2
SQ5: pages/1_Dashboard.py — 4-metric strip, active predictions df, countdown column, conditional fragment, cross-nav |deps: SQ1, SQ2, SQ3
SQ6: pages/5_Registry.py — filter bar, full table, row-click nav, CSV download |deps: SQ1, SQ2
SQ7: pages/3_Review.py — selectbox, 4 tabs, all display sections, resolution form |deps: SQ1, SQ2, SQ3
SQ8: pages/4_Scoreboard.py — filters, calibration curve primary, 5 learning loop surfaces |deps: SQ2, SQ3
SQ9: pages/2_Predict.py — question discovery, run config, pipeline thread, fragment poller, inline review, submit_after_review |deps: SQ1, SQ2, TA-interface

Build order: SQ1→SQ2→SQ3→SQ4→SQ5→SQ6→SQ7→SQ8→SQ9 (Predict last — most complex, hard TA dependency)

#### e) CAL[] effort estimates

SQ1 state.py: 0.5h (trivial constants)
SQ2 cache.py: 0.75h (exact spec given)
SQ3 charts.py: 2h (7 plotly builders, data shaping)
SQ4 app.py: 0.5h (navigation wiring)
SQ5 Dashboard: 1.5h (ProgressColumn, countdown, conditional fragment)
SQ6 Registry: 1h (filters + table straightforward)
SQ7 Review: 2h (4 tabs, nested expanders, all display paths)
SQ8 Scoreboard: 2h (5 learning loop surfaces, filter logic)
SQ9 Predict: 3h (threading, fragment polling, two-phase pipeline, most state complexity)
Total: ~13h

#### f) PM[] pre-mortems — Streamlit-specific risks

PM1: RERUN LOOP — fragment polling may trigger full page reruns if not isolated. Risk: pipeline state lost, thread orphaned. Mitigation: poll ONLY inside @st.fragment(run_every=1); gate on pipeline_state=="running" at fragment entry (early return otherwise); use cache_resource for queue (survives rerun); never read queue outside fragment.

PM2: STATE LOSS ON NAVIGATION — page switch may not clear session_state but Streamlit multi-page apps (st.navigation) DO persist session_state across pages — however, new pages may not re-init missing keys. Mitigation: init_state() called at top of every page to fill any missing keys with defaults. pipeline_queue in cache_resource is navigation-safe by design.

PM3: THREAD ORPHAN — if user navigates away mid-pipeline, thread continues writing to queue but nobody polls. Risk: stale record in slot. Mitigation: completed_slot (cache_resource list, max 1 item) holds the record. Slot is NOT checked on Dashboard load (DA[#9]: gold-plating dropped). Stale slot entry is harmless — overwritten by next pipeline run via completed_slot.clear(). Unpolled sentinel in queue drains on next fragment activation. Acceptable for single-user tool.

PM4: REGISTRYCACHE STALE AFTER WRITE — invalidate() called in Predict after submit_after_review, but Dashboard loaded in same session reads stale. Acceptable: single-user tool, eventual consistency within session. cache.load() on each page load re-reads if dirty flag set. Mitigation: always call cache.invalidate() immediately after any write path in UX.

PM5: CQA FIELD MISSING — close_date not on PredictionRecord (confirmed gap: only on PlatformQuestion in current models.py). Dashboard countdown will degrade to showing horizon_days as proxy. Mitigation: all new-field reads use getattr() with sensible defaults; no hard AttributeError paths.

PM6: TA INTERFACE TIMING — Predict page built last (SQ9) but depends on predict_until_review/submit_after_review. If TA delivers late: implement SQ9 with a stub shim calling orchestrator.predict(auto_submit=True) to unblock UI scaffolding; replace shim with real interface when TA ready.

#### g) Analytical hygiene §2a/§2b/§2c/§2e

§2a FINDINGS (each must be outcome 1/2/3):
- Finding: RegistryStore.load_all() performs full JSONL file read every call — no internal caching |outcome 2: confirms RegistryCache dict wrap is the correct pattern, prevents N page-renders × M JSONL reads per session |source:[independent-research]
- Finding: close_date exists on PlatformQuestion (models.py:240) but NOT on PredictionRecord (models.py:203-225) |outcome 1: CHANGES plan — Dashboard countdown cannot use record.close_date; must use getattr fallback or horizon_days; CQA's Q4 enhancement adds this field → plan notes graceful degradation until CQA merges |source:[independent-research]
- Finding: resolution.error_class_auto already exists as list[str] on Resolution model (models.py:156) — no new field needed for Scoreboard error bar |outcome 2: confirms Scoreboard can display error class frequency without waiting for CQA to add the field; only auto-population (from RCA) is pending |source:[independent-research]

§2b SCOPE (each outcome 1/2/3):
- Finding: No existing Streamlit code in repo — zero migration risk but zero reusable patterns |outcome 3: GAP — all Streamlit wiring is greenfield; no internal analogs to reference for tricky Streamlit behaviors (ProgressColumn, fragment isolation) |source:[independent-research]
- Finding: human_review.flags_raised populated by _generate_flags() in human_review.py (line 302-379) — existing flag logic is comprehensive |outcome 2: confirms Review page can display flags directly from record.human_review.flags_raised without recalculation |source:[independent-research]
- Finding: orchestrator.predict() is monolithic through submission (lines 65-319) — predict_until_review() split is TA scope |outcome 2: confirms UX scope is cleanly bounded; UX only wraps TA's interface in threading, does not touch orchestrator internals |source:[independent-research]

§2c RISKS (each outcome 1/2/3):
- Risk: Fragment + thread pattern for pipeline progress display is underdocumented in Streamlit; queue.get_nowait() in fragment with run_every=1 may behave unexpectedly when thread finishes before fragment polls |outcome 1: CHANGES plan — add explicit sentinel check + st.rerun() call inside fragment when None received from queue; also gate on pipeline_state before queue access to avoid empty-queue exceptions |source:[independent-research]
- Risk: st.dataframe on_select behavior requires Streamlit 1.35+ (selection_mode parameter) |outcome 3: GAP — need to verify Streamlit version in repo requirements. Fallback: st.dataframe with row index + st.selectbox for navigation if on_select not available |source:[agent-inference]
- Risk: Actor analysis expander collapsed by default (H3 unvalidated) — if actor_analysis_consulted field not on model, cannot gate display |outcome 2: confirms collapsed=True by default is correct; H3 unvalidated means we show it collapsed, not hidden; display condition: `if record.decomposition.actor_analysis.actors_involved` |source:[independent-research]

§2e ASSUMPTIONS (verified vs speculative):
- VERIFIED: PredictionRecord is Pydantic BaseModel — safe for session_state storage (JSON-serializable, thread-copyable) |source:[independent-research]
- VERIFIED: RegistryStore.update() rewrites entire file (lines 73-94) — RegistryCache.invalidate() after every write is correct pattern |source:[independent-research]
- VERIFIED: HumanReview model (models.py:138-143) has reviewed, human_adjustment, human_reasoning, flags_raised — all fields needed for inline review UI exist |source:[independent-research]
- SPECULATIVE: st.navigation (Streamlit 1.29+) is available in project environment — needs requirements.txt check in build
- SPECULATIVE: Scoreboard RCA brier_decompose() function exists with expected signature — interface contract only, not yet implemented

#### h) Component dependency order

```
SQ1 (state.py)      ← no deps
SQ2 (cache.py)      ← SQ1
SQ3 (charts.py)     ← no deps
SQ4 (app.py)        ← SQ1, SQ2
SQ5 (Dashboard)     ← SQ1, SQ2, SQ3
SQ6 (Registry)      ← SQ1, SQ2
SQ7 (Review)        ← SQ1, SQ2, SQ3
SQ8 (Scoreboard)    ← SQ2, SQ3
SQ9 (Predict)       ← SQ1, SQ2, TA-interface [hard external dependency]
```

SQ6-SQ8 are independently buildable once SQ1-SQ4 done. SQ9 is the only hard external block.

#### i) State management plan

| Key | Type | Set by | Read by | Notes |
|---|---|---|---|---|
| selected_prediction_id | str\|None | Dashboard on_select, Registry on_select | Review selectbox default | Cross-page nav pivot |
| pipeline_state | "idle"\|"running"\|"awaiting_review" | Predict (launch/fragment/submit) | Dashboard fragment gate, Predict inline review visibility | Controls rerun behavior |
| pipeline_record | PredictionRecord\|None | Predict fragment on thread completion | Predict inline review, cache invalidation | Cleared after submit |
| pipeline_question | PlatformQuestion\|None | Predict before thread launch | Predict submit_after_review call | Retained across fragment reruns |
| pipeline_client | PlatformClient\|None | Predict before thread launch | Predict submit_after_review call | Platform client instance |
| search_results | list[PlatformQuestion] | Predict question discovery | Predict left column df | Cleared on new search |
| selected_platform | str | Predict selectbox | Predict client instantiation | Persists within session |
| registry_filters | dict | Registry filter bar | Registry df render | Persists within session |
| scoreboard_date_range | tuple\|None | Scoreboard date_input | Scoreboard chart renders | None = all time |
| scoreboard_domains | list[str] | Scoreboard multiselect | Scoreboard chart renders | [] = all domains |

cache_resource (app-lifetime, thread-safe, nav-safe):
- get_registry_cache(path) → RegistryCache singleton
- get_pipeline_queue() → queue.Queue singleton
- get_completed_record() → list[PredictionRecord] (slot for thread-orphan recovery, max 1 item)

#### j) Interface contracts — exact signatures needed from TA

```python
# From TA — confirmed via TA plan §c (instance methods on Orchestrator)

orchestrator.predict_until_review(
    question: PlatformQuestion,
    platform_client: PlatformClient,
    num_runs: int = 1,
    personas: list[SearchPersona] | None = None,
    progress_queue: queue.Queue | None = None,
) -> PredictionRecord
# Writes "Step N/7: ..." strings to progress_queue if provided
# Writes None sentinel on completion
# Does NOT save to registry
# Returns record with human_review.reviewed=False

orchestrator.submit_after_review(
    record: PredictionRecord,
    human_review: HumanReview,
    platform_client: PlatformClient,
) -> PredictionRecord
# Applies human review, submits to platform, saves to registry
# Returns updated record with .submitted populated
```

UX threading pattern — DA[#1] + TA-DA[#13] corrected (pages/2_Predict.py):
```python
# Per-thread Orchestrator instance — required for OpenAI/Gemini client thread-safety (TA DA[#13])
# Thread writes ONLY to cache_resource slot and queue — never session_state
def _run_pipeline(config, question, client, num_runs, personas, q, completed_slot):
    orchestrator = Orchestrator(config)  # new instance per thread — ¬share from session_state
    record = orchestrator.predict_until_review(question, client, num_runs, personas, q)
    completed_slot.clear()
    completed_slot.append(record)   # cache_resource list — thread-safe write
    q.put(None)                     # sentinel — signals fragment to promote to session_state

# Fragment runs on main script-runner thread — safe to write session_state
@st.fragment(run_every=1)
def pipeline_progress_fragment():
    if st.session_state.get(KEY_PIPELINE_STATE) != "running":
        return
    q = get_pipeline_queue()
    completed_slot = get_completed_record()
    msgs = []
    sentinel_received = False
    while True:
        try:
            msg = q.get_nowait()
            if msg is None:
                sentinel_received = True
                break
            msgs.append(msg)
        except queue.Empty:
            break
    if msgs:
        with st.status("Running pipeline..."):
            for m in msgs:
                st.write(m)
    if sentinel_received and completed_slot:
        # Promote from cache_resource to session_state on main thread (safe)
        st.session_state[KEY_PIPELINE_RECORD] = completed_slot[0]
        st.session_state[KEY_PIPELINE_STATE] = "awaiting_review"
        st.rerun()
```

#### k) DA responses — r2

DA[#1] CONCEDE — session_state writes from background thread:
Thread writes ONLY to cache_resource completed_slot (list) and progress_queue. Fragment detects None sentinel, reads completed_slot[0], performs all session_state writes (KEY_PIPELINE_RECORD, KEY_PIPELINE_STATE) from main script-runner thread, then st.rerun(). Corrected pattern documented in §j above. Removes the original thread→session_state writes entirely.

DA[#3] CONCEDE — dict vs object for Brier decomposition:
Scoreboard code uses bracket notation `decomp["reliability"]`, `decomp["resolution"]`, `decomp["uncertainty"]`. Assumption in §b updated: RCA returns dict, not typed object.

DA[#7] CONCEDE — Queue sentinel race documentation:
Corrected _run_pipeline sequence (§j): (1) thread: record = predict_until_review(...) → completed_slot.clear(); completed_slot.append(record) → q.put(None) | (2) fragment: drain msgs → detect None → read completed_slot[0] → set session_state from main thread → st.rerun(). Sentinel arrives AFTER record in slot — no race: slot is written before q.put(None).

DA[#9] CONCEDE — orphan recovery is gold-plating:
Dropped Dashboard-load orphan check. completed_slot is the primary completion mechanism per DA[#1] corrected pattern. Fragment is the sole consumer. Stale slot entry from prior run is harmless — gets overwritten on next _run_pipeline launch (completed_slot.clear() before append). PM3 updated below.

### reference-class-analyst

#### a) Scope — files+changes
Files: src/pipeline/calibration.py (rewrite), scripts/resolve.py (auto-classification), src/registry/query.py (Brier decomposition analytics), tests/test_calibration.py (update)
src/pipeline/aggregator.py: minimal add of n_distinct_providers param to aggregate_runs()
src/config.py: add min_resolved_for_isotonic=20 to CalibrationConfig
¬ src/models.py (CQA owns ErrorClass enum)
¬ dashboard.py (UX owns Scoreboard rendering — RCA provides data functions only)

Code-analysis — exact codebase state:
- calibration.py L36-71: single gate N>=50. Phase 0+1 both = flat hedging. No isotonic phase.
- apply_hedging_correction() L74-85: flat shift=0.04 regardless of distance from 0.5.
- platt_transform() L88-95: P_cal = 1/(1+exp(-(a*logit(p)+b))). Correct. Unchanged in Phase 2.
- fit_platt() L98-148: MLE Nelder-Mead. N<10 returns identity (a=1.0,b=0.0).
- CalibrationConfig (config.py L38-42): min_resolved_for_platt=50, prior_hedging_shift=0.04. Missing min_resolved_for_isotonic=20.
- aggregator.py L68-77: _extremize() always applied when method="extremized_trimmed_mean". No provider-count gate anywhere.
- RunResult L90-106: has model field (L93). NO provider field yet — depends on Q4/CQA.
- Resolution L151-158: error_class_auto is list[str] at L156. Already exists — no schema migration.
- resolve.py L41-96: no error classification. Hook point at L78-80 (after outcome computed, before save).

#### b) Assumptions — from other agents
DEP-CQA-1: ErrorClass enum in models.py with exactly: CONFABULATION, PROCESS, ACTOR_MISCLASSIFICATION, SEARCH_BLINDSPOT, CALIBRATION_FAILURE
DEP-CQA-2: RunResult.provider: str field added (for extremization gate). Fallback: infer from model string (claude→anthropic, gpt→openai, gemini→google).
DEP-CQA-3: Resolution.error_class_auto stays list[str] — no breaking change (already exists at L156).
DEP-UX-1: Scoreboard view calls RCA's analytics functions. UX plan §b confirms interface expectation: brier_decompose(pairs) with .reliability/.resolution/.uncertainty attributes.
NOTE: UX plan uses BrierDecomposition as return type — RCA will return dict instead (simpler, no new class). UX will access dict keys. Coordinate with UX.

#### c) Interfaces — new function signatures

```python
# calibration.py: 3-phase calibrate() — backward-compatible signature
def calibrate(
    probability: float,
    config: Config,
    platt_params: PlattParams | None = None,
    n_resolved: int = 0,
    isotonic_data: list[tuple[float, float]] | None = None,  # NEW: (pred,outcome) pairs
) -> tuple[float, dict | None]:
    # Phase 0 N<20: apply_hedging_correction_scaled()
    # Phase 1 N=20-49: isotonic_transform() if isotonic_data provided else scaled hedging
    # Phase 2 N>=50: platt_transform() (unchanged)
    # Returns same tuple type — backward-compatible

def apply_hedging_correction_scaled(probability: float, base_shift: float) -> float:
    # effective_shift = base_shift * 2 * |p - 0.5|

def fit_isotonic_logit(
    predictions: list[float], outcomes: list[float]
) -> list[tuple[float, float]]:
    # Returns sorted (logit_x, prob_y) breakpoints

def isotonic_transform(
    probability: float, isotonic_data: list[tuple[float, float]]
) -> float:
    # Linear interpolation on logit scale, clamp [0.01, 0.99]

# src/registry/query.py: Murphy 1973 Brier decomposition (module-level functions)
def compute_brier_decomposition(
    pairs: list[tuple[float, float]],
    n_bins: int = 10,
) -> dict | None:
    # keys: reliability, resolution, uncertainty, brier_check
    # Returns None if N<5 or <2 populated bins

def get_brier_decomposition_by_domain(
    records: list[PredictionRecord],
) -> dict[str, dict | None]: ...

def get_brier_decomposition_by_horizon(
    records: list[PredictionRecord],
) -> dict[str, dict | None]:
    # bucket keys: '<30d', '30-180d', '>180d'

# scripts/resolve.py: auto-classification
def classify_error(record: PredictionRecord, outcome: float) -> list[str]:
    # Returns list of ErrorClass.value strings

# src/pipeline/aggregator.py: minimal gate addition
def aggregate_runs(
    runs: list[RunResult],
    method: str = "extremized_trimmed_mean",
    trim_fraction: float = 0.1,
    extremization_factor: float = 1.5,
    n_distinct_providers: int = 1,  # NEW: gate extremization when >=2
) -> Aggregation: ...
```

#### d) SQ[] sub-task decomposition
SQ[1]: Keep apply_hedging_correction() unchanged + add apply_hedging_correction_scaled() |estimable: yes |method: analogue(shift-formula) |→ reference-class-analyst
SQ[2]: Add fit_isotonic_logit() + isotonic_transform() to calibration.py |estimable: yes |method: precedent(sklearn-isotonic-pattern) |→ reference-class-analyst
SQ[3]: Add min_resolved_for_isotonic=20 to CalibrationConfig in config.py |estimable: yes |method: direct |→ reference-class-analyst
SQ[4]: Rewrite calibrate() — 3-phase gate with isotonic_data param |estimable: yes |method: analogue(existing-platt-gate) |→ reference-class-analyst
SQ[5]: Add n_distinct_providers gate to aggregate_runs() in aggregator.py |estimable: yes |method: direct |→ reference-class-analyst
SQ[6]: Implement classify_error() in resolve.py (5-class rule engine) |estimable: yes |method: analogue(existing-scoring-hook) |→ reference-class-analyst
SQ[7]: Wire classify_error() into resolve.py main loop at L78-80 |estimable: yes |method: direct |→ reference-class-analyst
SQ[8]: Implement compute_brier_decomposition() — Murphy 1973 formulas in query.py |estimable: yes |method: precedent(sklearn-calibration_curve) |→ reference-class-analyst
SQ[9]: Implement domain + horizon stratified decompositions in query.py |estimable: yes |method: decompose(filter+apply-SQ8) |→ reference-class-analyst
SQ[10]: Update tests — test_calibration.py for scaled Phase 0 + new isotonic + Phase 1 gate; test_aggregator.py for provider gate |estimable: yes |method: analogue(existing-test-patterns) |→ reference-class-analyst

#### e) RC[] reference class
RC[calibration-rewrite]: reference-class={isotonic phase additions to existing Platt pipelines} |base-rate={3-8h} |sample-size={N≈15 open-source PRs} |src:[agent-inference] |confidence:M
RC[error-classification]: reference-class={rule-based 5-class engines in scoring pipelines} |base-rate={1-3h} |sample-size={N≈8} |src:[agent-inference] |confidence:M
RC[brier-decomposition]: reference-class={Murphy decomp in Python forecasting tools} |base-rate={2-4h with stratification+edge-cases} |sample-size={N≈6} |src:[agent-inference] |confidence:M
RC[test-update]: reference-class={test suite updates for calibration rewrites} |base-rate={1-2h} |sample-size={N≈10} |src:[agent-inference] |confidence:H

#### f) CAL[] calibrated effort
CAL[SQ1-scaled-hedging]: point=0.5h |80%=[0.25,1h] |90%=[0.2,1.5h] |breaks-if:{no-breaks}
CAL[SQ2-isotonic-infra]: point=1.5h |80%=[1,2.5h] |90%=[0.75,3h] |breaks-if:{scipy-isotonic-API-mismatch→sklearn-fallback}
CAL[SQ3-config]: point=0.25h |80%=[0.1,0.5h] |90%=[0.1,0.75h] |breaks-if:{no-breaks}
CAL[SQ4-phase-gate]: point=1h |80%=[0.5,1.5h] |90%=[0.5,2h] |breaks-if:{SQ3-not-done-first}
CAL[SQ5-provider-gate]: point=0.5h |80%=[0.25,0.75h] |90%=[0.2,1h] |breaks-if:{Q4-provider-absent→use-model-string-fallback}
CAL[SQ6-classify-error]: point=1.5h |80%=[1,2.5h] |90%=[0.75,3h] |breaks-if:{ErrorClass-enum-not-from-CQA}
CAL[SQ7-wire-resolve]: point=0.5h |80%=[0.25,0.75h] |90%=[0.2,1h] |breaks-if:{SQ6-not-done-first}
CAL[SQ8-brier-decomp]: point=2h |80%=[1.5,3h] |90%=[1,4h] |breaks-if:{edge-cases-empty-bins,single-outcome-class}
CAL[SQ9-stratified]: point=1h |80%=[0.5,1.5h] |90%=[0.4,2h] |breaks-if:{horizon_days-null-in-most-records}
CAL[SQ10-tests]: point=1h |80%=[0.5,1.5h] |90%=[0.4,2h] |breaks-if:{isotonic-non-deterministic-small-N}
CAL[TOTAL]: point=9.75h |80%=[6.5,15h] |90%=[5.5,19h] |breaks-if:{CQA-ErrorClass-delay,Q4-provider-field-gap}

#### g) PM[] pre-mortems
PM[1]: Isotonic regression overfits on N=20-49 — 20 examples + 10 breakpoints perfectly interpolates training, poor out-of-sample |probability:30% |early-warning:{calibration plot oscillates near breakpoints} |mitigation:{cap breakpoints at max(3,N//5); min N>=5 unique predictions; fallback to scaled hedging if N-unique<5}
PM[2]: classify_error() over-fires — most records get 3+ classes, diluting signal |probability:30% |early-warning:{test on synthetic data, avg error count >2 per record} |mitigation:{tighten thresholds: CALIBRATION_FAILURE needs brier>0.25 AND |delta|>0.4; SEARCH_BLINDSPOT needs score<2; CONFABULATION requires base-rate mismatch AND low search quality}
PM[3]: TestCalibrate existing tests break — analysis: test_uses_prior_correction(L82-87) asserts prob>0.6 for input=0.6,n_resolved=10. Scaled: distance=0.1, effective_shift=0.04*2*0.1=0.008, result=0.608>0.6. PASSES. apply_hedging_correction kept unchanged → test_pushes_high_higher passes. |probability:20% |early-warning:{pytest run} |mitigation:{keep apply_hedging_correction() unchanged; add apply_hedging_correction_scaled() separately}
PM[4]: Brier decomp empty-bin edge — N<30 resolved + 10 bins = most bins empty |probability:50% |early-warning:{compute with N<10 synthetic data, check NaN} |mitigation:{adaptive n_bins=min(10,N//3); return None if N<5 or <2-populated-bins}
PM[5]: RunResult.provider absent (Q4/CQA delay) blocks extremization gate |probability:35% |early-warning:{check CQA convergence before SQ5} |mitigation:{fallback: count distinct providers by matching model string (claude/gpt/gemini patterns)}

#### h) Analytical hygiene §2a-e
§2a ANALYZE:
- Outcome 1(changes): calibration.py Phase 0 flat shift sub-optimal at p near 0.5. aggregator.py has no provider gate — must add.
- Outcome 2(confirms): Platt transform L88-95 correct, unchanged in Phase 2. Resolution.error_class_auto list[str] L156 — no migration needed.
- Outcome 3(gap): scipy.optimize.isotonic_regression availability depends on scipy>=1.13. Must check pyproject.toml — sklearn.isotonic.IsotonicRegression as fallback.

§2b PLAN:
- Outcome 1(changes): CalibrationConfig needs min_resolved_for_isotonic=20. calibrate() needs isotonic_data param.
- Outcome 2(confirms): Murphy 1973 decomposition formulas match review spec exactly.
- Outcome 3(gap): Isotonic data persistence unspecified. Recommend: recompute from registry pairs each call at N<50 (cheap, avoids new file format). Confirm with lead.

§2c IMPLEMENT:
- Outcome 1(changes): test_calibration.py needs new isotonic Phase 1 tests. Existing tests pass per PM[3] analysis.
- Outcome 2(confirms): test_aggregator.py existing tests pass — default n_distinct_providers=1 means trimmed_mean only; existing extremize tests unaffected.
- Outcome 3(gap): No existing tests for Brier decomposition or classify_error() — must write from scratch.

§2e DISCONFIRM — evidence against 3-phase:
STRONGEST CASE AGAINST: Niculescu-Mizil & Caruana (2005) found isotonic regression consistently overfits at N<50. At N=20-49 isotonic may underperform flat hedging in practice. Simplest valid alternative: skip Phase 1, use flat-hedging → Platt at N=30.
VERDICT: Review-settled (C10 — no re-debate). Counter recorded. Mitigate via breakpoint cap in PM[1].

#### i) Backward-compatibility analysis — H4
- Resolved records: brier_score/log_score stored at resolution time from submitted probability. Decomp reads stored values. COMPATIBLE.
- CalibrationData: stores calibrated_probability + platt_params_used. New isotonic phase writes platt_params_used=None (same as Phase 0). COMPATIBLE.
- PlattParams persistence (platt_*.json): Phase 2 unchanged. Existing saved params load correctly. COMPATIBLE.
- calibrate() return signature: tuple[float, dict|None] unchanged. All callers unaffected. COMPATIBLE.
H4 verdict: CONFIRMED. Existing tests pass. New N=20-49 phase adds new behavior, no existing behavior removed.

#### j) Calibration math — exact formulas

Phase 0 (N<20) scaled hedging:
```
distance = |p - 0.5|
effective_shift = base_shift * 2 * distance
p_cal = min(0.99, p + effective_shift) if p > 0.5
p_cal = max(0.01, p - effective_shift) if p < 0.5
p_cal = p if p == 0.5
```

Phase 1 (N=20-49) isotonic on logit:
```
# Training: logit_preds = [log(p/(1-p))] for each p
# Fit non-decreasing step fn on (logit_pred, outcome) pairs
# Store sorted (logit_x, prob_y) breakpoints — cap at max(3, N//5)

# Inference: logit_p = log(p/(1-p))
# Linear interpolation between breakpoints → clamp [0.01, 0.99]
```

Phase 2 (N>=50) Platt — unchanged:
```P_cal = 1/(1+exp(-(a*logit(p)+b)))```

Murphy 1973 Brier decomposition:
```
bar_o = mean(outcomes)                                               # overall base rate
for each bin k (n_bins adaptive = min(10, N//3)):
    bar_p_k = mean(predictions in bin k)
    bar_o_k = mean(outcomes in bin k)

reliability = (1/N) * sum_k(n_k * (bar_p_k - bar_o_k)^2)  # lower = better
resolution  = (1/N) * sum_k(n_k * (bar_o_k - bar_o)^2)    # higher = better
uncertainty = bar_o * (1 - bar_o)                           # dataset constant
check: brier ≈ reliability - resolution + uncertainty
```

Extremization gate:
```
if n_distinct_providers >= 2 and method == "extremized_trimmed_mean":
    raw_aggregate = _extremize(trimmed_mean, extremization_factor)
else:
    raw_aggregate = trimmed_mean  # no extremization for single-provider
```

#### DA responses — reference-class-analyst

DA[#2]: defend — isotonic_data wiring is TA's responsibility, confirmed format is correct
Evidence:
- get_calibration_pairs() returns list[tuple[float, float]] as (predicted, actual) per query.py L46-63.
- fit_isotonic_logit(predictions, outcomes) takes those same two parallel lists.
- The orchestrator call at L245-250 must be updated by TA to add: `pairs = self.query.get_calibration_pairs()` then pass `isotonic_data=pairs` to calibrate(). This is precisely what DA[#2] identifies and is already in TA's coordination scope (DA[#5] also flags this wiring).
- Format confirmed COMPATIBLE: get_calibration_pairs() gives (pred, actual) tuples → unzip to (predictions, outcomes) → exactly what fit_isotonic_logit() expects.
- Action: Update plan §b to make DEP explicit: "TA must pass isotonic_data=self.query.get_calibration_pairs() to calibrate() call in predict_until_review(). No format conversion needed — get_calibration_pairs() already returns list[tuple[float,float]] in correct order."
- RCA plan clarification: calibrate() will unzip internally: `predictions, outcomes = zip(*isotonic_data)` if isotonic_data is not None.

DA[#3]: concede — confirm dict + bracket notation, close the coordination gap
Evidence: DA correctly identifies that "coordinate with UX" is deferred work not a resolution.
- RCA confirms: return type is dict with keys "reliability", "resolution", "uncertainty", "brier_check"
- UX must use bracket notation: decomp["reliability"], decomp["resolution"], decomp["uncertainty"]
- RCA will NOT return an object or dataclass — dict is simpler and avoids a new class dependency
- Action: Update plan §c return type annotation. Confirm to UX: bracket notation required. UX plan §b expectation of BrierDecomposition object is superseded by this dict contract.

DA[#10]: compromise — cite verified implementations, widen CAL ranges, keep M confidence for decomp only
Evidence from verification:
1. sklearn.calibration.CalibratedClassifierCV with method='isotonic' — standard reference for isotonic calibration on N~50 samples. Adds isotonic phase to classifiers. This is the primary open-source anchor for RC[calibration-rewrite]. Time to implement: sklearn PRs add isotonic method in ~200 LOC including tests — maps to 2-4h for isolated function.
2. scipy.optimize.isotonic_regression (verified available: scipy 1.17.1 in venv, confirmed working via live test). API: isotonic_regression(y, increasing=True) returns OptimizeResult with .x (fitted values). DIRECT dependency — no sklearn needed. Simpler than assumed.
3. netcal library (PyPI: netcal~=1.3) — temperature scaling + isotonic calibration utilities for neural nets. Isotonic implementation uses scipy under the hood, 50-100 LOC for fit+transform. Effort: ~2h for equivalent module.

RC[] updates:
RC[calibration-rewrite]: reference-class={sklearn.CalibratedClassifierCV isotonic method~200LOC,netcal isotonic~100LOC,scipy.optimize.isotonic_regression direct API} |base-rate={2-5h for isolated isotonic fit+transform with tests} |sample-size={N=3-verified} |src:[independent-research] |confidence:M (narrowed from 3-8h to 2-5h — scipy direct API is simpler than assumed)
RC[error-classification]: reference-class={rule-based classification hooks in scoring pipelines} |base-rate={1-3h} |sample-size={N≈8} |src:[agent-inference] |confidence:L (downgrade — no verified implementations cited, only analogical)
RC[brier-decomposition]: reference-class={sklearn.calibration.calibration_curve implementation,Murphy-1973 standard formula,forg library brier decomp} |base-rate={2-4h} |sample-size={N=2-verified+1-formula} |src:[independent-research] |confidence:M
RC[test-update]: reference-class={test suite updates for calibration rewrites} |base-rate={1-2h} |sample-size={N≈10} |src:[agent-inference] |confidence:L (downgrade — no verified implementations)

CAL[] revisions (widened for L-confidence items):
CAL[SQ2-isotonic-infra]: point=1.5h |80%=[1,2.5h] |90%=[0.75,3h] → REVISED: point=1h |80%=[0.75,2h] |90%=[0.5,2.5h] |breaks-if:{none — scipy.optimize.isotonic_regression confirmed in venv at 1.17.1, API verified working}
CAL[SQ6-classify-error]: point=1.5h |80%=[1,2.5h] |90%=[0.75,3h] → REVISED: point=1.5h |80%=[1,3h] |90%=[0.75,4h] (widened — L confidence, rule-engine threshold tuning adds variance)
CAL[SQ10-tests]: point=1h |80%=[0.5,1.5h] |90%=[0.4,2h] → REVISED: point=1h |80%=[0.75,2h] |90%=[0.5,2.5h] (widened — L confidence)
CAL[TOTAL]: point=9.25h |80%=[6,15h] |90%=[5,19.5h] (SQ2 narrowed, SQ6+SQ10 widened, net slightly wider)


reference-class-analyst: ✓ r2-DA-responses |DA[#2]-defend(format-confirmed-compatible,TA-wires-get_calibration_pairs()→isotonic_data,calibrate()-unzips-internally) |DA[#3]-concede(dict-confirmed,bracket-notation,UX-BrierDecomposition-object-superseded) |DA[#10]-compromise(3-verified-implementations-cited,SQ2-CAL-narrowed-to-1h,L-confidence-items-widened,scipy-direct-API-confirmed-in-venv) |→ r3-ready

## build-status

## findings
### tech-architect

### code-quality-analyst

### ux-researcher

### reference-class-analyst

### devils-advocate

DA[#1] integration-risk: UX+TA — session_state write from background thread is unsafe
  evidence: UX plan §j threading pattern (lines 618-619) sets `st.session_state[KEY_PIPELINE_RECORD] = record` and `st.session_state[KEY_PIPELINE_STATE] = "awaiting_review"` from inside `_run_pipeline()`, which runs in a `threading.Thread`. Streamlit's session_state is NOT thread-safe — it is tied to the script runner's thread context. Writing from a background thread may silently fail, raise RuntimeError, or corrupt state depending on Streamlit version.
  risk: Pipeline completes but UI never transitions to "awaiting_review" — user sees perpetual spinner. The `completed_slot.append(record)` cache_resource fallback (line 617) partially mitigates but the state transition itself (`pipeline_state`) has no fallback path.
  |→ UX: remove session_state writes from _run_pipeline thread. Instead, thread writes ONLY to cache_resource slot (thread-safe list). Fragment poller reads from cache_resource slot, detects completion (record present), and performs session_state writes from the main script-runner thread. This is the documented Streamlit pattern for thread→UI communication. |source:[independent-research]

DA[#2] integration-risk: TA+RCA — calibrate() isotonic_data parameter never wired
  evidence: TA plan §c shows calibrate() called with existing signature: `calibrate(probability, config, platt_params, n_resolved)`. RCA plan §c adds `isotonic_data: list[tuple[float, float]] | None = None` as new param. TA plan §i says "calibrate() signature unchanged" and makes no mention of passing isotonic_data. Orchestrator.predict() at line 245-250 calls calibrate() with 4 positional args — the new isotonic_data param will never be populated.
  risk: Phase 1 isotonic calibration (N=20-49) is dead code. calibrate() receives isotonic_data=None, falls back to scaled hedging. The entire isotonic implementation (RCA SQ2, SQ4) has zero effect at runtime.
  |→ TA: add isotonic_data retrieval to predict_until_review() between n_resolved and calibrate() calls. Query calibration pairs from registry: `pairs = self.query.get_calibration_pairs()` (already exists at query.py:46). Pass `isotonic_data=pairs` to calibrate(). RCA: confirm this is sufficient or specify different data format. |source:[independent-research]

DA[#3] integration-risk: RCA+UX — BrierDecomposition dict vs object expectation
  evidence: UX plan §b (line 432) expects `brier_decompose(pairs) -> BrierDecomposition` with `.reliability`, `.resolution`, `.uncertainty` **attributes** (dot access). RCA plan §b (line 668) explicitly states "RCA will return dict instead (simpler, no new class). UX will access dict keys." RCA plan §c (line 700-705) confirms return type is `dict | None` with keys: reliability, resolution, uncertainty, brier_check.
  risk: UX writes `decomp.reliability` (attribute access) → AttributeError at runtime. Both agents acknowledge the mismatch in their plans but neither commits to the resolution. "Coordinate with UX" is not a resolution — it's deferred work.
  |→ RESOLVE NOW: RCA returns dict. UX accesses dict keys: `decomp["reliability"]`, `decomp["resolution"]`, `decomp["uncertainty"]`. UX must update Scoreboard code to use bracket notation. Both agents confirm in convergence. |source:[independent-research]

DA[#4] integration-risk: CQA+TA — warnings_out silent failure path
  evidence: CQA plan §b (line 270) flags: "If TA omits `warnings_out=record.pipeline_warnings` passthrough, pipeline_warnings stays empty silently. Not a crash." CQA PM3 repeats same concern. TA plan §a mentions "predict_until_review() must pass warnings_out" but does NOT include it in SQ[] decomposition or CAL[] estimates. The actual wiring is not assigned to any sub-task.
  risk: CQA builds the warnings_out infrastructure (decomposer.py, base_rate.py changes). TA builds predict_until_review(). Neither agent's sub-task list includes the single line that connects them: `warnings_out=record.pipeline_warnings` at the two call sites. Integration falls through the crack.
  |→ TA: add explicit sub-task or append to SQ5 scope: "pass warnings_out=record.pipeline_warnings to decompose_question() and estimate_base_rate() calls within predict_until_review()". CQA: add integration verification to contract test SQ9. |source:[independent-research]

DA[#5] assumption-conflict: TA+RCA — aggregate_runs() signature change uncoordinated
  evidence: RCA plan §c (line 721-727) adds `n_distinct_providers: int = 1` param to aggregate_runs(). TA plan §a mentions fixing challenge_forecast to use aggregate/median and adds get_aggregate_run(). But TA's orchestrator.py line 224-229 calls aggregate_runs() without n_distinct_providers. TA does not mention this new parameter anywhere in plan. RCA plan assumes TA (or someone) will count distinct providers from runs and pass the count.
  risk: Extremization gate never activates. aggregate_runs() always receives default n_distinct_providers=1, so even with multi-model runs (Q9), extremization is applied unconditionally — the exact opposite of the review-settled design ("extremize only when N>=2 providers").
  |→ TA: in predict_until_review(), after collecting all runs, compute `n_providers = len(set(r.provider for r in record.runs))` and pass to aggregate_runs(). Requires CQA's RunResult.provider field. Add to SQ5 scope and dependency chain. |source:[independent-research]

DA[#6] spec-drift: TA — deliberation trigger rewrite incomplete
  evidence: TA plan §c (line 121-128) shows should_deliberate() accepting challenge_entry and pre_mortem_delta params. But orchestrator.py line 232-233 currently calls `should_deliberate(aggregation, self.config)` AFTER step 4 (aggregate) and BEFORE step 5 (calibrate). The new triggers require challenge_entry (from step 3c) and pre_mortem_delta (from individual runs). TA SQ10 says "revise should_deliberate() triggers" but does not specify how the orchestrator wiring changes — which step provides challenge_entry and pre_mortem_delta to the call.
  risk: TA rewrites should_deliberate() to accept new params but doesn't update the orchestrator call site to pass them. Or passes them incorrectly (e.g., pre_mortem_delta from last run only, not aggregate delta). Deliberation triggers remain stdev-only in practice.
  |→ TA: specify exact orchestrator wiring in SQ10: (1) challenge_entry comes from step 3c — already stored in challenge_sv.challenges[0] if it exists; pass it. (2) pre_mortem_delta: define which delta — mean of all runs' pre_mortem_delta? Max? Last run? Spec says "pre_mortem |delta|>0.1" but doesn't clarify aggregation. RESOLVE: use max(abs(r.pre_mortem_delta) for r in runs). Document in plan. |source:[independent-research]

DA[#7] interface-gap: TA+UX — Queue sentinel race condition
  evidence: UX plan §j (line 620) has `q.put(None)` AFTER `st.session_state` writes (see DA[#1]). Fragment poller (line 631) checks `if msg is None: st.rerun()`. But if DA[#1] fix is applied (session_state writes move to fragment), the sentinel must arrive AFTER the record is in the cache_resource slot. Current code: thread writes to completed_slot (line 617), then sets session_state (618-619), then puts sentinel (620). With DA[#1] fix, the sequence would be: thread writes to completed_slot → puts sentinel → fragment reads sentinel → fragment reads completed_slot → fragment sets session_state. This works IF completed_slot.append() is visible before q.put(None) — which it is because both are in the same thread (sequential memory ordering).
  risk: Low after DA[#1] fix. But the CURRENT plan has the race condition described in DA[#1]. Document the corrected sequence explicitly.
  |→ UX: after DA[#1] fix, document the corrected _run_pipeline: (1) record = predict_until_review(...) (2) completed_slot.append(record) (3) q.put(None). Fragment: (1) read None from queue (2) read record from completed_slot (3) set session_state (4) st.rerun(). |source:[agent-inference]

DA[#8] test-gap: CQA — Literal type migration risk undertested
  evidence: CQA plan §f PM1 identifies that existing registry.jsonl records with "" or non-Literal strings will raise Pydantic ValidationError. CQA plan says "inspect registry.jsonl before switching types; if records exist with invalid values, add validator to coerce." But CQA SQ9 contract tests (§h) do NOT include a test for Literal coercion/validation on load. The test plan tests field defaults and JSONL roundtrip but not the failure path: loading old records with `vulnerability: ""` after type changes to `Literal["high","medium","low"]`.
  risk: CQA switches types, existing tests pass (they construct fresh objects), but loading existing registry data fails at runtime. The pre-flight check is manual ("inspect registry.jsonl") with no automated gate.
  |→ CQA: add contract test: construct ChallengeEntry with vulnerability="" → expect Pydantic to either coerce or raise. If raises, test proves validator is needed. Test both "" and unexpected strings (e.g. "HIGH"). This catches the migration risk BEFORE it hits production data. |source:[independent-research]

DA[#9] over-engineering: UX — thread orphan recovery mechanism
  evidence: UX plan §f PM3 describes `get_completed_record() → list[PredictionRecord]` cache_resource slot for thread-orphan recovery. Dashboard and Predict both check this slot on load. This is a personal tool (C1). Pipeline runs take 30-60 seconds. If user navigates away mid-pipeline, the thread completes, record sits in slot, and is recovered on next page load.
  risk: Low — but the implementation adds complexity (checking slot on every page load, clearing slot after recovery, coordinating between Dashboard and Predict). For a personal tool where the user can simply re-run, this is gold-plating.
  |→ UX: SIMPLIFY. Keep completed_slot as the PRIMARY mechanism for thread→UI communication (per DA[#1] fix). Drop the separate "orphan recovery" logic that checks on Dashboard load. Fragment poller handles normal completion; if user navigates away, stale record in slot is harmless and gets overwritten on next run. §4c gold-plating: design doc does not require orphan recovery. |source:[agent-inference]

DA[#10] process-violation: RCA — RC[] reference classes use [agent-inference] only
  evidence: RCA plan §e (lines 743-746) lists 4 RC[] reference classes. All carry `|src:[agent-inference] |confidence:M` or `|confidence:H`. No T1/T2 source for any base-rate estimate. "N≈15 open-source PRs" and "N≈8" and "N≈6" are asserted without citation. §2d+ requires architecture/effort claims backed by T3-or-better with DA challenge for T3-only on load-bearing decisions.
  risk: Effort estimates (CAL[TOTAL] 9.75h) rest entirely on unsourced reference classes. Not blocking but violates §2d+ source-quality-tiers — effort estimates should at minimum cite the specific PRs/examples counted.
  |→ RCA: either cite 2-3 specific open-source isotonic calibration implementations (GitHub URLs) that anchor the base-rate estimates, or downgrade confidence to L and widen CAL ranges. |source:[independent-research]

DA[#11] spec-drift: TA — pre-mortem fix scope unclear on falsification_anchors LLM call
  evidence: TA plan §a SQ8 says "add LLM call in forecaster.py, populate RunResult.falsification_anchors." But the design spec (Q7) says "strip probability+reasoning, keep question+criteria+sub-questions+actors; add falsification_anchors prompt+field." TA SQ7 handles the stripping. SQ8 adds a SECOND LLM call specifically for falsification anchors. The spec does not clearly mandate a separate LLM call — it could mean "add a falsification_anchors field to the existing pre-mortem prompt response" (i.e., ask the pre-mortem to also output anchors).
  risk: TA implements a separate $0.002-0.005 LLM call per run for falsification anchors when the pre-mortem prompt could simply be extended to output them. Extra cost, extra latency, minimal benefit.
  |→ TA: clarify — is falsification_anchors a SEPARATE LLM call or an extension of the pre-mortem prompt? If separate: justify the added cost/latency for a personal tool. If extension: SQ8 collapses into SQ7 (modify pre-mortem prompt to also output falsification anchors array). The simpler approach is almost certainly correct here. §4c gold-plating check. |source:[agent-inference]

DA[#12] integration-risk: CQA+TA — provider field population timing
  evidence: CQA plan §b (line 271) says "forecaster.py already has `prov` local var at line 137 — CQA adds `provider=prov` to RunResult constructor." TA plan §a says "RunResult.provider: str field added (default='') — Q9 multi-model tracking needs this." Both agents claim ownership of populating the field. CQA says they'll add `provider=prov` to RunResult constructor at forecaster.py:243. TA says CQA owns the schema but TA needs the field for Q9.
  risk: Either both agents modify forecaster.py:243 (merge conflict) or each assumes the other will do it (neither does). The field exists but is never populated → all runs show provider="" → RCA's extremization gate (counting distinct providers) always sees 1 provider → gate never activates.
  |→ RESOLVE: CQA owns the field addition AND the population at forecaster.py:243. TA does NOT touch that line. Confirm in convergence. CQA adds `provider=prov` to RunResult constructor; TA reads it downstream. |source:[independent-research]

DA[#13] assumption-conflict: TA — AnthropicClient.call() model param inconsistency
  evidence: TA plan §a says "replace model mutation pattern with pass-model-as-param to AnthropicClient.call()." TA plan §g §2a says "pass model directly to client.call() eliminating state mutation entirely → outcome 1: changes plan." But examining AnthropicClient.call() (llm_router.py:34-56), it uses `self.model` at line 46 (`model=self.model`). Adding a model param to call() means changing the signature of call() across all 3 client classes (Anthropic, OpenAI, Gemini). OpenAI and Gemini clients are from sigma-verify — TA cannot modify their call() signatures.
  risk: TA adds model param to AnthropicClient.call() but cannot add it to sigma-verify's OpenAIClient.call() and GeminiClient.call(). The try/finally mutation pattern persists for OpenAI and Gemini branches. Half-fix: Anthropic is thread-safe, others remain thread-unsafe. The thread-safety fix is incomplete for multi-model runs.
  |→ TA: acknowledge that sigma-verify clients cannot be modified in this build. For OpenAI/Gemini, the try/finally pattern remains. Thread-safety for multi-model runs requires either: (a) separate LLMRouter instances per thread, or (b) a lock around the OpenAI/Gemini call paths. Option (a) is simpler — create router per run in the multi-model path. Document the limitation. |source:[independent-research]

### Prompt audit
PROMPT-AUDIT: echo-count:2 |unverified-claims:1 |missed-claims:none |methodology:investigative

Echo instances:
1. Q6 "contamination controls" — all 4 agents echo the prompt's contamination control spec (restricted query, temporal firewall, separate model call, labeled output) as requirements without independently validating that these controls are sufficient or correctly ordered. TA PM[3] partially challenges (Tavily temporal filter speculative) — best practice observed.
2. C6 "Queue + st.fragment" — labeled review-settled, accepted without independent Streamlit threading research. UX discovers issues in §2c (fragment rerun risk, sentinel handling) — good investigative behavior post-echo.

Unverified claims:
1. TA CAL[SQ1] "breaks-if: AnthropicClient.call() doesn't accept model kwarg (it doesn't currently)" — TA correctly identifies the gap but does not address the sigma-verify client limitation (see DA[#13]).

Missed claims: none — prompt decomposition captured all Q/H/C accurately.

Methodology assessment: INVESTIGATIVE. All 4 agents read code, verified line numbers, identified gaps independently. CQA's char-for-char duplicate verification is exemplary. RCA's §2e disconfirmation (Niculescu-Mizil 2005) is strong independent research. UX's §2c Streamlit-specific risk identification shows genuine investigation. TA's PM analysis is thorough. The plans demonstrate genuine codebase engagement, not prompt echo.

### Exit-gate verdict
exit-gate: PASS |engagement:B+ |unresolved:[DA#1-thread-safety-critical,DA#2-isotonic-wiring-critical,DA#3-dict-vs-object,DA#5-provider-gate-wiring] |untested-consensus:[DA#4-warnings_out-no-subtask] |hygiene:pass |prompt-contamination:pass(echo-count-low,investigative-methodology) |cqot:pass(TA-§2e-falsifiability-present,RCA-§2e-disconfirm-exemplary,UX-PM-series-addresses-reversal) |xverify:not-applicable-r2

Notes: PASS with 4 unresolved challenges that MUST be addressed before r3. DA[#1] is the highest-priority integration risk — Streamlit session_state from background thread is a correctness bug, not a style concern. DA[#2] would render the entire isotonic calibration feature dead code. DA[#3] and DA[#5] are straightforward coordination gaps that need explicit resolution. DA[#13] is important but may be acceptable as a known limitation if documented.

## convergence
tech-architect: ✓ r2-DA-responses |DA[#2]CONCEDE(isotonic_data wiring→SQ5) |DA[#4]CONCEDE(warnings_out wiring→SQ5) |DA[#5]CONCEDE(n_distinct_providers→SQ5) |DA[#6]CONCEDE(deliberation exact extraction: challenge_sv.challenges[0]+max-pm_delta→SQ10) |DA[#11]COMPROMISE(falsification_anchors: extend pre-mortem schema ¬separate-call→SQ8-simplified) |DA[#13]CONCEDE-PARTIAL(sigma-verify-immutable→AnthropicClient-fixed+OpenAI/Gemini-safe-via-per-thread-Orchestrator→RISK[5]+UX-constraint) |plan-updated(§j-m) |→ r2-complete
ux-researcher: ✓ r2-DA-responses+TA-DA[#13]-accepted |DA[#1]CONCEDE(thread-¬write-session_state→fragment-promotes-from-cache_resource-slot-on-main-thread) |DA[#3]CONCEDE(RCA-returns-dict→bracket-notation-throughout-Scoreboard) |DA[#7]CONCEDE(sentinel-race-documented:slot-written-before-q.put(None),fragment-reads-slot-after-None) |DA[#9]CONCEDE(orphan-recovery-dropped→stale-slot-harmless,overwritten-on-next-run) |TA-DA[#13]CONCEDE(per-thread-Orchestrator:config-passed-to-thread,Orchestrator(config)-created-inside-_run_pipeline,¬shared-from-session_state) |plan-updated(§j-threading-pattern,§b-RCA-assumption,PM3) |→ r2-complete
code-quality-analyst: ✓ r2-DA-responses |DA[#4]CONCEDE(SQ9-wiring-test-added:patch-decomposer-LLM→assert-pipeline_warnings-non-empty,makes-TA-dep-enforceable) |DA[#8]CONCEDE(Literal-safety-test-added:ChallengeEntry(vulnerability="")+ChallengeEntry(vulnerability="HIGH")→assert-ValidationError;test-outcome-drives-@field_validator-decision;SQ5-ordering-updated) |DA[#12]CONCEDE(CQA-owns-BOTH-RunResult.provider-field+forecaster.py:243-population;TA-¬touch-that-line;unambiguous) |plan-updated(§h+§i+§j) |→ r2-complete
devils-advocate: ✓ r2-challenge |13-challenges |4-critical(DA#1,DA#2,DA#5,DA#13) |→ agents-must-address: UX(DA#1,DA#3,DA#7,DA#9), TA(DA#2,DA#4,DA#5,DA#6,DA#11,DA#13), CQA(DA#4,DA#8,DA#12), RCA(DA#2,DA#3,DA#10) before r3

## build-status

CHECKPOINT[tech-architect]: files-modified: llm_router.py,orchestrator.py,aggregator.py,deliberation.py |functions-done: SQ1(AnthropicClient.call+model-param,LLMRouter.call-thread-safe),SQ2(SearchModule+StageVerification-top-level),SQ3(get_aggregate_run-at-EOF),SQ4(challenge_forecast-uses-aggregate-run,step-reordered-step4-before-3c),SQ5(predict_until_review-with-progress_queue,warnings_list,n_distinct_providers,isotonic_data,challenge_entry+pm_delta-→-should_deliberate),SQ6(submit_after_review),SQ10(should_deliberate-3-conditions,deliberate-supervisor-LLM-call) |drift: step-4-aggregation-moved-BEFORE-step-3c-challenge(correct-requires-aggregate-before-challenging-it;no-behavior-change-for-single-path) |surprises: RCA-already-modified-aggregator.py-added-n_distinct_providers-to-aggregate_runs()-before-TA-ran(linter-notification-confirmed,integrated-correctly);calibrate()-still-lacks-isotonic_data-param(RCA-dependency-pending);RunResult.provider-field-not-yet-added-by-CQA(n_distinct_providers-defaults-to-1-via-getattr-guard);warnings_out-param-not-yet-on-decompose_question/estimate_base_rate(CQA-dep-pending,wired-locally-as-list,will-activate-when-CQA-delivers) |next: SQ7(forecaster.py-pre-mortem-fix),SQ9(base_rate.py-search-augmented)

## open-questions
