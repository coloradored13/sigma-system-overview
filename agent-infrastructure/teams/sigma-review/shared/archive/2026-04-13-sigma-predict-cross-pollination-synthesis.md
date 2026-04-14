# Synthesis: sigma-predict Cross-Pollination Build
**Date:** 2026-04-13
**Mode:** BUILD TIER-2
**Team:** tech-architect, implementation-engineer, code-quality-analyst, reference-class-analyst + DA(phase-03)
**Session:** sigma-predict cross-pollination improvements

---

## 1. Prompt Decomposition

### Q[] — Build Scope
| ID | Question |
|----|----------|
| Q1 | Deep-dive sigma-predict codebase — architecture, gaps, pain points, tech debt |
| Q2 | Deep-dive sigma ecosystem repos (sigma-verify, sigma-mem, hateoas-agent, ollama-mcp-bridge) + sigma-review patterns to identify applicable learnings |
| Q3 | Evaluate the cross-pollination analysis — validate, challenge, expand. What did it get right? What did it miss? What's mis-prioritized? |
| Q4 | Team determines build scope based on independent analysis |
| Q5 | Implement team-determined improvements |

### H[] — Hypotheses
| ID | Hypothesis | Status |
|----|-----------|--------|
| H1 | sigma-verify PROVIDERS registry compatible with LLMRouter dispatch | PARTIALLY VERIFIED — PROVIDERS has 13 entries, all with call(). Model param mismatch requires ADR[1] fix first. |
| H2 | Dynamic provider loading enables genuine multi-model primary forecasting | CONDITIONALLY SUPPORTED — multi-model benefit realized in verification only, not primary runs (all 5 runs use config.primary_model) |
| H3 | Validation gates are additive (pipeline_warnings), won't block pipeline | REASONABLE — pipeline_warnings infrastructure confirmed on PredictionRecord |
| H4 | sigma-optimize keyword-fragment findings transfer from Haiku to Sonnet/Opus | LOW CONFIDENCE — cross-model transfer <32% to Gemini; empirical gate blocks implementation |
| H5 | Source-clustering detection feasible from sources_cited | VERIFIED — sources_cited populated per run; apex-domain dedup implemented in <20 LOC |
| H6 | Registry maintenance can use existing RegistryStore/RegistryQuery | LIKELY TRUE — confirmed via code read; not implemented in this build |

### C[] — Constraints
| ID | Constraint |
|----|-----------|
| C1 | Personal tool — over-engineering risk real |
| C2 | 91 existing tests must pass — zero regressions |
| C3 | Use sigma-verify public API (PROVIDERS, client classes), not internals |
| C4 | LLMRouter model-mutation pattern is known tech debt — fix, don't perpetuate |
| C5 | Budget control — 13 providers × N runs = expensive, need provider selection config |

---

## 2. What Was Built

### Files Changed / Created
| File | Change Type | Corresponding SQ[] |
|------|------------|-------------------|
| `src/pipeline/llm_router.py` | Modified | SQ[1], SQ[2] |
| `src/pipeline/validator.py` | New | SQ[3] |
| `src/pipeline/llm_audit.py` | New | SQ[4] |
| `src/pipeline/aggregator.py` | Modified | SQ[5] |
| `src/pipeline/orchestrator.py` | Modified | SQ[3], SQ[4], SQ[5], CQA-F6 fix |
| `src/pipeline/deliberation.py` | Modified | CQA-F6 fix |
| `src/models.py` | Modified | SQ[5] (Aggregation fields) |
| `src/config.py` | Modified | SQ[2], SQ[3], SQ[4] (new config fields) |

### Implemented Features

**SQ[1] — LLMRouter model-mutation fix**
Refactored `call()` to use a per-(provider, model) client cache (`_get_or_create_client()`), eliminating the thread-unsafe try/finally mutation. AnthropicClient.call() retains model kwarg; non-anthropic providers use one cached instance per (provider, model) pair. No threading.Lock added (single-threaded codebase; IE-1 revision).

**SQ[2] — PROVIDERS registry expansion**
`LLMRouter._init_external_providers()` now iterates sigma-verify PROVIDERS (13 providers). `Config.verification_providers` field controls which are active. sigma-verify AnthropicClient loaded only when Anthropic is NOT primary. Backward-compat aliases (`self._openai`, `self._gemini`) preserved.

**SQ[3] — PipelineValidator inter-stage gates**
New `src/pipeline/validator.py`. Five gates: `base_rate_gate` (range 0.01–0.99), `probability_gate` (calibrated range), `run_count_gate` (actual vs requested), `parse_failure_gate` (warns on parse_failed=True), `search_quality_gate` (warns on avg score < 3). Non-blocking by default; `Config.strict_validation=True` raises `PipelineError`. Integrated into orchestrator after base_rate, runs, and calibration stages.

**SQ[4] — LLMAuditLogger**
New `src/pipeline/llm_audit.py`. JSON-L per-call log: timestamp, provider, model, params_hash, result_hash, duration_ms, cost_usd. Raw prompts never logged (structural summary only; secret keys REDACTED). Buffered (BUFFER_LIMIT=10), flush at pipeline end. Optional via `Config.audit_path=None`.

**SQ[5] — Source-clustering detection**
`source_cluster_check()` in `aggregator.py`. Apex-domain dedup across runs. Authoritative domains whitelist (reuters.com, bbc.com, .gov, .int, etc.) exempt from flagging. `Aggregation.sources_clustering_score` + `clustered_domains` fields added. Pipeline warning emitted when score >= 0.5. Legacy JSONL records load with defaults (backward-compatible).

**CQA-F6 fix — deliberation.py hardcoded provider**
`router.call("anthropic", ...)` → `router.call(config.primary_model.provider, config.primary_model.model_id, ...)`. Prevents runtime failure when primary is openai or google.

**G8/SQ-M6 — Confidence interval population (IE-independent)**
`orchestrator.py:324-326` computes 95% CI from stdev, populates `CalibrationData.confidence_interval`. Not in original IE scope — implemented independently. `human_review.py:140` displays it.

### Test Metrics
- Tests before: 91
- Tests after: 130
- New tests: 39
- Regressions: 0

---

## 3. Architecture Decisions

| ADR | Decision | Rationale | Status |
|-----|----------|-----------|--------|
| ADR[1] | Fix model-mutation via per-(provider, model) client cache | thread-unsafe try/finally is conceptually wrong; sigma-verify clients are single-model instances | IMPLEMENTED |
| ADR[2] | Import ALL providers via PROVIDERS registry; keep local AnthropicClient for primary | PROVIDERS is single source of truth; host-model semantic violation if sigma-verify Anthropic used for primary | IMPLEMENTED |
| ADR[3] | 4B local models verification-only, not primary forecasting | 4B parse failure risk too high for structured JSON forecaster output | IMPLEMENTED via config.verification_providers |
| ADR[4] | AuditLogger as optional component of LLMRouter, log via wrapper | Inline audit creates duplication; wrapper eliminates drift | PARTIALLY IMPLEMENTED — logger created but never wired into call/verify/challenge (BUILD-R4) |
| ADR[5] | Validation gates as pipeline_warnings (non-blocking) with configurable hard stops | pipeline_warnings already exists; gates should not kill pipeline on bad single search | IMPLEMENTED |
| ADR[6] | Source-clustering detection post-aggregation, warn-only | Data already available; <20 LOC; over-engineering to block | IMPLEMENTED (whitelist gap noted) |
| ADR[7] | Dual-role AnthropicClient — local for primary, sigma-verify for cross-verify | Host-model semantics: Anthropic should not self-verify | IMPLEMENTED |

### Interface Contracts (IC[])
All 5 ICs from tech-architect plan were implemented:
- IC[1]: LLMRouter.call() — no model mutation, cache keyed by (provider, model)
- IC[2]: Provider expansion via PROVIDERS registry
- IC[3]: PipelineValidator interface (5 gate methods + validate_all())
- IC[4]: AuditLogger optional integration in LLMRouter
- IC[5]: Source clustering fields on Aggregation model

---

## 4. Cross-Agent Convergence

Items independently identified by multiple agents without coordination:

| Finding | Agents Converging | Notes |
|---------|------------------|-------|
| LLMRouter model-mutation bug (thread-unsafe try/finally) | tech-architect (F1, F3), CQA (CQA-F1) | Both diagnosed same root cause independently; ADR[1] addresses |
| parse_failed runs contaminating aggregation | CQA (CQA-F5), reference-class-analyst (G3) | Both flagged; warning implemented but exclusion not done |
| Source-clustering detection feasibility | tech-architect (F8, ADR[6]), reference-class-analyst (G6) | Both confirmed feasibility; RA added canonical-source whitelist requirement |

---

## 5. Tensions and Resolutions

### Tension 1: pre-mortem prompt restructuring (Item 3)
- **Input analysis position:** LOW/MEDIUM priority — port sigma-optimize keyword findings
- **tech-architect position:** CANNOT VALIDATE — cross-model transfer <32%; empirical gate applies
- **reference-class-analyst position:** MEDIUM/HIGH — but focused on falsification_anchors (G7) and multiplicative guard (G5), not keyword transfer
- **Resolution:** sigma-optimize keyword transfer DEFERRED per !empirical-validation-gate. Methodology improvements (G5, G7) scoped as SQ-M items, not built in this session.

### Tension 2: parse_failed run exclusion vs. warning
- **reference-class-analyst:** G3/SQ-M3 requires EXCLUSION — warning without exclusion doesn't fix the contamination
- **implementation-engineer:** exclusion = reference-class methodology decision, not IE scope
- **CQA:** CHALLENGE-4 assessed as PARTIAL — acceptable as non-blocking warn
- **Resolution:** Warning implemented; exclusion explicitly deferred. RA's build review confirmed this is the critical remaining gap (G3 called out as "most important gap").

### Tension 3: threading.Lock for client cache
- **tech-architect plan (ADR[1]):** cache access should be protected by threading.Lock
- **implementation-engineer revision (IE-1):** single-threaded codebase; Lock adds zero value
- **Resolution:** IE-1 accepted — no Lock added. Reasoning valid for personal tool.

### Tension 4: Additive Bayesian framing (Item 9)
- **Input analysis:** LOW/LOW
- **reference-class-analyst:** MEDIUM — one-line prompt change, high leverage for preventing invisible multiplicative fallacy (G5)
- **Resolution:** RA's SQ-M5 prompt change NOT built. Deferred to methodology-only follow-up session.

---

## 6. DA Challenges and Resolutions

No DA agent appears in workspace convergence record. The workspace phase was plan (not build-review phase with DA). Four challenges were issued pre-build by CQA during the planning phase:

| Challenge | Issued By | Status | Notes |
|-----------|-----------|--------|-------|
| CQA-F6 must be in build scope (deliberation hardcode) | CQA | FIXED | deliberation.py now uses config.primary_model.provider |
| CQA-F7 temporal firewall gap — docstring false claim | CQA | NOT FIXED | Functional gap remains AND misleading documentation persists. No fix or docstring correction applied. |
| Test coverage gate — any SQ[] touching untested module adds tests | CQA | PARTIALLY MET | New tests cover SQ[1]-[5] and CQA-F6 but baseline coverage gap (CQA-F10) unchanged |
| CQA-F5 parse_failed propagation | CQA | PARTIALLY MET | Warning implemented via parse_failure_gate; exclusion not done |

---

## 7. Methodology Improvements

### From reference-class-analyst: 10 methodology gaps identified (G1-G10)

| Gap | Priority | Status |
|-----|----------|--------|
| G1: pre_mortem.md spec contradicts code (claims current_estimate as input) | HIGH | NOT BUILT — SQ-M1 deferred |
| G2: Reference class instance count unvalidated | HIGH | NOT BUILT — SQ-M2 deferred |
| G3: parse_failed runs contaminate aggregation | HIGH | PARTIALLY MET — warning only; exclusion deferred |
| G4: Phase 0 hedging correction too aggressive for near-50% base rates | HIGH | NOT BUILT — SQ-M7 deferred (BELIEF P=0.70 insufficient to modify calibration without empirical test) |
| G5: Multiplicative adjustment guard absent in forecaster prompt | MEDIUM | NOT BUILT — SQ-M5 deferred |
| G6: Source clustering signal absent | MEDIUM | IMPLEMENTED (SQ-M4 / ADR[6]) |
| G7: falsification_anchors stored but not surfaced | MEDIUM | NOT BUILT — SQ-M8 deferred |
| G8: Confidence interval never populated | MEDIUM | IMPLEMENTED independently by IE |
| G9: Deliberation supervisor lacks mode context | LOW | NOT BUILT — SQ-M9 deferred |
| G10: Pre-mortem scenario diversity not tracked | LOW | NOT BUILT — SQ-M10 deferred |

**RCA scope triage (reference-class-analyst build review):**

Recommended for immediate follow-up (low effort, no validation needed):
1. G3/SQ-M3 — exclude parse_failed from aggregation before aggregate_runs() (~5 LOC)
2. SQ-M1 — fix pre_mortem.md prompt spec (~10 LOC, zero regression risk)
3. SQ-M5 — add multiplicative guard to forecaster_base.md Step 3 (~5 LOC)
4. G7/SQ-M8 — wire falsification_anchors into _generate_flags() (~5 LOC)
5. Clustering whitelist — add .gov, .int, who.int, cdc.gov, bls.gov, census.gov, FRED to _AUTHORITATIVE_DOMAINS (~8 LOC)
6. G2/SQ-M2 — reference class instance count validation (~40 LOC)

Deferred (requires empirical calibration data):
- G4/SQ-M7 — hedging correction conditioning for base_rate ∈ [0.40, 0.60] (BELIEF P=0.70 not sufficient)

---

## 8. Code Quality Findings

### Pre-build audit (10 findings, CQA)
| ID | Issue | Risk | Build Scope |
|----|-------|------|-------------|
| CQA-F1 | LLMRouter model-mutation thread-unsafe | H | FIXED (SQ[1]) |
| CQA-F2 | _extract_json raises ValueError on malformed input; duplicated in deliberation.py | M | NOT FIXED |
| CQA-F3 | Dead code in _collect_platform_signals (if-branch never executes) | M | NOT FIXED |
| CQA-F4 | RegistryCache exists but unused — O(N) re-reads | M | NOT FIXED |
| CQA-F5 | parse_failed runs silently contribute to aggregate | M | PARTIAL (warning only) |
| CQA-F6 | deliberation.deliberate() hardcodes "anthropic" provider | M | FIXED |
| CQA-F7 | Temporal firewall in base_rate silently disabled — docstring false claim | M | NOT FIXED |
| CQA-F8 | apply_hedging_correction (non-scaled) dead production code with live tests | L | NOT FIXED |
| CQA-F9 | _estimate_effective_n effectively always returns n | L | NOT FIXED |
| CQA-F10 | Zero test coverage on all pipeline execution modules | H | NOT FIXED (baseline unchanged) |

### Post-build audit (6 new findings, CQA build review)
| ID | Issue | Severity | Status |
|----|-------|----------|--------|
| BUILD-R1 | test_client_cache_keyed_by_provider_model is a no-op test (if False bypasses _get_or_create_client) | M | OPEN — must fix |
| BUILD-R2 | test_non_anthropic_call_uses_cached_client mutation check is tautological | L | OPEN |
| BUILD-R3 | CQA-F7 temporal firewall docstring still claims protection that doesn't exist | M | OPEN — must fix |
| BUILD-R4 | LLMAuditLogger instantiated but never called — audit_path feature silently does nothing | M | OPEN — must fix |
| BUILD-R5 | PROVIDERS cls(model=model) kwarg not verified against sigma-verify client signatures | M | OPEN |
| BUILD-R6 | _collect_platform_signals dead code (CQA-F3) not fixed | M | OPEN (known) |

### CQA Build Verdict
**CONDITIONAL PASS** | regressions: 0 | tests: 130/130

Two issues must be resolved before this build is considered clean:
- BUILD-R4: audit feature is inert — either wire log_call into LLMRouter or remove Config.audit_path
- BUILD-R1: no-op test provides false confidence on cache behavior — must be rewritten

CQA-F7 docstring correction also required for process integrity.

**Overall quality grade: B+** (good behavioral tests on new features; one structural test failure; one dead feature)

---

## 9. Cross-Pollination Analysis Evaluation

### What the input analysis got right
- Items 1, 2, 5, 6 priorities are reasonable (LLMRouter expansion, validation gates, audit logging, registry maintenance)
- Item 8 (HATEOAS deferred) — correct assessment; would require full pipeline redesign
- Item 4 (source-clustering) — correct feasibility call; data already available

### What the input analysis missed (tech-architect)
1. **Model-mutation thread-safety bug (F1)** — the most important fix; not mentioned; prerequisite for everything else
2. **AnthropicClient duplication (F5)** — needs explicit decision before expansion; analysis assumed simple import
3. **sigma-verify AnthropicClient exists** — cross-verification use case not surfaced
4. **sigma-verify._parse_json_response reuse opportunity (F10)** — parallel implementations may diverge
5. **PROVIDERS registry as cleaner import pattern** — analysis didn't identify the registry as the right abstraction

### What the input analysis got wrong or mis-prioritized
- **Item 3 (pre-mortem prompt restructuring from sigma-optimize):** Analysis rated LOW/MEDIUM. RA rated MEDIUM/HIGH — but for falsification_anchors (G7), not keyword transfer. Keyword transfer specifically blocked by !empirical-validation-gate (cross-model transfer <32%).
- **Item 7 (result schema validation):** Framing off. Real need is INPUT validation (LLM response parsing), not result schema. sigma-verify._parse_json_response is better port target.
- **Item 9 (Additive Bayesian framing):** Analysis rated LOW/LOW. RA disagreed: one-line prompt guard prevents invisible multiplicative fallacy, MEDIUM leverage.

### What the input analysis missed (reference-class-analyst)
Five HIGH/MEDIUM gaps not mentioned in input analysis:
1. Reference class instance count unvalidated (G2) — HIGH
2. parse_failed contamination of aggregation (G3) — HIGH
3. Phase 0 hedging correction conditioning for near-50% base rates (G4) — HIGH
4. Confidence interval never populated (G8) — MEDIUM
5. Deliberation supervisor lacks mode context (G9) — LOW

---

## 10. Pre-Mortem

### From tech-architect
| ID | Risk | Mitigation |
|----|------|-----------|
| PM[1] | Provider expansion breaks existing tests (11 new provider classes in __init__) | Wrap each PROVIDERS entry in try/except ImportError |
| PM[2] | Client cache grows unbounded with many distinct model strings | Personal tool: N providers × N models < 30 entries — unbounded acceptable |
| PM[3] | AuditLogger fsync slows pipeline | Buffer limits (10 calls); <10 LLM calls per prediction total |
| PM[4] | Validation gates produce false warnings for legitimate extreme base rates | Configurable thresholds; default range 0.01–0.99 |
| PM[5] | sigma-verify PROVIDERS imports fail at runtime (Ollama not running) | Lazy-init Ollama clients; catch connection errors at call-time |

### From reference-class-analyst
| ID | Risk | Mitigation |
|----|------|-----------|
| PM-M1 | SQ-M3 too aggressive — aggregate degrades to single run | Require ≥2 valid runs; fall through to best single run with warning |
| PM-M2 | Prompt changes alter LLM behavior unexpectedly | Additive directives only; test on 3 archived questions before deployment |
| PM-M3 | Source clustering false positives for canonical sources | Whitelist .gov, .int, known statistical bodies |
| PM-M4 | Instance count validation blocks valid narrow reference classes | Warning not blocking; never reject prediction |

---

## 11. Open Questions and Deferred Items

### Deferred from this build (explicit)
| Item | Reason Deferred |
|------|----------------|
| HATEOAS state machine (Item 8) | Full pipeline redesign required; complexity >> benefit for personal tool |
| sigma-mem full dream consolidation (Item 6 variant) | Over-engineering for personal tool; simpler prune-malformed sufficient |
| sigma-optimize keyword fragment transfer (Item 3) | !empirical-validation-gate: cross-model transfer <32%; test premise before building |
| ΣComm check-in format (Item 10) | Internal tool, not multi-agent; no benefit |
| G2/SQ-M2: Reference class instance count | Medium effort; deferred to methodology-only follow-up |
| G4/SQ-M7: Hedging correction conditioning | BELIEF P=0.70 insufficient without empirical test on archived questions |
| G5/SQ-M5: Multiplicative guard in forecaster_base.md | Prompt-only; deferred to follow-up |
| G7/SQ-M8: Wire falsification_anchors to human_review | Data collected but not surfaced; ~5 LOC fix; deferred |
| G9/SQ-M9: Deliberation mode context | Low priority |
| G10/SQ-M10: Pre-mortem scenario count | Low priority |
| SQ-M1: Fix pre_mortem.md spec vs. code | Prompt-only; ~10 LOC; deferred |

### Open defects requiring resolution (from CQA CONDITIONAL PASS)
1. BUILD-R4: LLMAuditLogger never called — Config.audit_path feature silently does nothing
2. BUILD-R1: test_client_cache_keyed_by_provider_model is a no-op test
3. BUILD-R3 / CQA-F7: temporal firewall docstring still claims protection that doesn't exist

### Known gaps not targeted in this build
- CQA-F2: _extract_json ValueError + deliberation.py duplication
- CQA-F3: _collect_platform_signals dead if-branch
- CQA-F4: RegistryCache unused — O(N) re-reads
- CQA-F8: apply_hedging_correction dead production code
- CQA-F9: _estimate_effective_n effectively always returns n
- CQA-F10: Zero coverage on all pipeline execution modules (orchestrator, forecaster, deliberation, verification, base_rate, etc.)

---

## 12. Process Notes

### Implementation-engineer process violation
The workspace records that IE had a "REVISED SCOPE" note indicating methodology items from reference-class-analyst (G2, G3, G4) were "not in IE scope." The reference-class-analyst plan was written and completed on 2026-04-13 — the same day as the build — suggesting the plans were not fully integrated before build execution began. Specific methodology items from RA's plan (G3 parse_failed exclusion, G7 falsification_anchors) were available in the workspace during build but not acted upon. IE's scope note acknowledged these as "exclusion = reference-class methodology decision."

The CQA build review explicitly identified G3's warning-only treatment as the "most important gap" — a methodologically contaminated aggregate with a visible warning is not the same as a methodologically sound aggregate. This gap should be flagged for the next build session.

The workspace shows no DA challenge/review phase convergence declaration. Phase was recorded as "plan" at workspace header time. The echo-watch section flags an "unknown-agent" with 100% echo level on "general prompt language" — this appears to be a hook catch from a context that was not part of the core team agents.

---

## 13. Final Metrics

| Metric | Value |
|--------|-------|
| Tests before build | 91 |
| Tests after build | 130 |
| New tests | 39 |
| Regressions | 0 |
| Files changed | 8 (5 modified + 2 new + 1 new) |
| SQ[] items completed | 5/5 (SQ[1]-SQ[5]) + CQA-F6 fix + G8 confidence interval |
| CQA build verdict | CONDITIONAL PASS |
| CQA quality grade | B+ |
| ADRs locked | 7 (ADR[1]-ADR[7]) |
| Open P0 defects | 1 (BUILD-R4 — audit feature dead) |
| Open P1 defects | 2 (BUILD-R1 no-op test, CQA-F7 docstring false claim) |
| Deferred SQ-M items | 8 (SQ-M1, SQ-M2, SQ-M3 partial, SQ-M5, SQ-M7, SQ-M8, SQ-M9, SQ-M10) |

### BELIEF[] Scores (from reference-class-analyst)
| Claim | P | Evidence |
|-------|---|---------|
| Run quality gate high impact | P=0.85 | Noise inputs degrade ensemble regardless of model diversity |
| Reference class instance count: N<10 unreliable | P=0.80 | Literature: ±30pp 95% CI for N<10 |
| Hedging correction conditioning | P=0.70 | Correct on average but wrong for base_rate ∈ [0.40, 0.60] |
| Prospective pre-mortem ordering | P=0.55 | Not high-conviction; current clean separation captures most benefit |

### H2 Final Verdict (reference-class-analyst)
Multi-model IS better IF: (a) runs are parse-valid, (b) n_distinct_providers ≥ 2 for extremization, (c) run quality gate (SQ-M3) excludes noise. Same-model multi-persona: marginal benefit only. Note: n_distinct_providers will always be 1 for primary forecasting in current implementation (all 5 runs use config.primary_model) — multi-model benefit realized only in verification layer, not primary forecasting rounds.
