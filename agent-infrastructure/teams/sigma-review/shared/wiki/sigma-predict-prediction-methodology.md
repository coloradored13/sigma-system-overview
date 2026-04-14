# sigma-predict: Prediction Methodology
Last updated: 26.4.13 | Reviews: B7

## Summary

sigma-predict's prediction methodology has 10 documented gaps identified by reference-class-analyst in B7, ranging from HIGH severity contamination issues (parse_failed runs silently contributing to aggregates) to MEDIUM gaps (confidence interval unpopulated, falsification anchors not surfaced). Three were fully or partially addressed in B7; seven remain deferred.

---

## Aggregation: parse_failed Contamination

Runs where the LLM fails to produce valid JSON (`parse_failed=True`) are silently included in aggregation. Their probability estimates propagate into the ensemble average alongside valid structured outputs. This is the highest-priority methodology gap identified in B7.

Reference-class-analyst position: exclusion is required, not optional. Warning without exclusion does not fix the contamination — a visible warning on a contaminated aggregate is worse than no warning (false confidence). [B7, 26.4.13]

B7 status: A `parse_failure_gate` warning was added to PipelineValidator, but exclusion from `aggregate_runs()` was not implemented. CQA called this the "most important gap" in the build review.

Recommended fix (RA): ~5 LOC — filter parse_failed=True runs before `aggregate_runs()`. Pre-mortem consideration: if all runs are parse_failed, fall through to best single run with warning rather than failing the pipeline entirely (PM-M1). [B7, 26.4.13]

Multi-agent convergence: both CQA (CQA-F5) and reference-class-analyst (G3) independently flagged this without coordination. [B7, 26.4.13]

---

## Reference Class: Instance Count Validation

The pipeline does not validate the number of instances in the selected reference class. Reference classes with N < 10 yield ±30 percentage points at 95% CI — rendering the probability estimate unreliable as a standalone signal. BELIEF: P=0.80 based on forecasting literature. [B7, 26.4.13]

B7 status: Not implemented. Deferred as SQ-M2 (medium effort, ~40 LOC).

Recommended approach: warning not blocking — never reject a prediction solely for small reference class, but surface the unreliability prominently. [B7, 26.4.13]

---

## Confidence Interval: Population Gap

Pre-B7, `CalibrationData.confidence_interval` was never populated despite the field existing on the model. This means any downstream consumer or display of CIs would receive null/empty values. [B7, 26.4.13]

B7 status: IMPLEMENTED — implementation-engineer independently added 95% CI computation from stdev at orchestrator.py:324-326, outside original build scope. `human_review.py:140` now displays it. This was classified as G8 by reference-class-analyst; IE-implemented as part of G8/SQ-M6. [B7, 26.4.13]

---

## Falsification Anchors: Collected But Not Surfaced

The pipeline collects `falsification_anchors` per run — conditions or evidence that would falsify the forecast — but does not surface them in the human review output. The data is available; the display wiring is absent. [B7, 26.4.13]

B7 status: Not built. Deferred as SQ-M8. Recommended fix: ~5 LOC to wire falsification_anchors into `_generate_flags()`. [B7, 26.4.13]

---

## Source Clustering Detection

Runs may draw from the same underlying sources across multiple LLM calls, reducing effective independence. Pre-B7, no detection of this existed.

B7 status: IMPLEMENTED — `source_cluster_check()` in `aggregator.py` performs apex-domain dedup across runs. Known authoritative domains (reuters.com, bbc.com, .gov, .int, etc.) are whitelisted and exempt from flagging. `Aggregation.sources_clustering_score` and `clustered_domains` fields added. Pipeline warning emitted when score >= 0.5. [B7, 26.4.13]

Multi-agent convergence: tech-architect (F8, ADR[6]) and reference-class-analyst (G6) independently confirmed feasibility. RA added the canonical-source whitelist requirement. [B7, 26.4.13]

Open gap: the whitelist needs expansion. Recommended additions: .gov, .int, who.int, cdc.gov, bls.gov, census.gov, FRED (Federal Reserve Economic Data). ~8 LOC. [B7, 26.4.13]

---

## Hedging Correction: Conditioning Gap

The `apply_hedging_correction` function corrects for anchoring bias by shifting predictions toward more extreme values. However, this correction is too aggressive when the base rate is near 50% (the ∈ [0.40, 0.60] range). The correction assumes the prediction is anchored away from the base rate, but for near-50% base rates the correction introduces error rather than removing it. [B7, 26.4.13]

B7 status: Not built. Deferred as SQ-M7. BELIEF: P=0.70 — not sufficient to modify calibration without empirical test on archived questions. Must test on 3+ archived predictions before deploying. [B7, 26.4.13]

Note: `apply_hedging_correction` (non-scaled variant) is also dead production code with live tests (CQA-F8) — the dead code concern is separate from the conditioning gap. [B7, 26.4.13]

---

## Multiplicative Adjustment Guard

The forecaster_base.md prompt has no guard against invisible multiplicative compounding. When multiple adjustment factors are applied sequentially, they can compound multiplicatively in ways that are not visible to the LLM, pushing final estimates to extremes even when each individual adjustment appears reasonable. [B7, 26.4.13]

B7 status: Not built. Deferred as SQ-M5. Recommended: additive directive in forecaster_base.md Step 3 (~5 LOC prompt change). [B7, 26.4.13]

Reference-class-analyst BELIEF: one-line prompt guard prevents invisible multiplicative fallacy — MEDIUM leverage despite input analysis rating of LOW/LOW. Additive Bayesian framing explicitly superior to multiplicative compounding for this class of problem. [B7, 26.4.13]

---

## pre_mortem.md Spec vs. Code Mismatch

The pre_mortem.md prompt spec claims `current_estimate` as an input parameter, but the actual code does not pass this value. This is a documentation/spec inconsistency that could mislead future developers modifying the pre-mortem stage. [B7, 26.4.13]

B7 status: Not fixed. Deferred as SQ-M1 (prompt-only, ~10 LOC, zero regression risk). Classified as HIGH priority by reference-class-analyst. [B7, 26.4.13]

---

## Deferred Methodology Items: Priority Summary

From reference-class-analyst triage, ordered by recommended priority:

1. **G3/SQ-M3** — exclude parse_failed from aggregation before aggregate_runs() (~5 LOC) — HIGH
2. **SQ-M1** — fix pre_mortem.md prompt spec (~10 LOC, zero regression risk) — HIGH
3. **SQ-M5** — add multiplicative guard to forecaster_base.md Step 3 (~5 LOC) — MEDIUM
4. **G7/SQ-M8** — wire falsification_anchors into _generate_flags() (~5 LOC) — MEDIUM
5. **Clustering whitelist** — add .gov, .int, statistical bodies to _AUTHORITATIVE_DOMAINS (~8 LOC) — MEDIUM
6. **G2/SQ-M2** — reference class instance count validation (~40 LOC) — MEDIUM
7. **G4/SQ-M7** — hedging correction conditioning for base_rate ∈ [0.40, 0.60] — HIGH but blocked on empirical test

Items 1-6 are ready to implement. Item 7 requires 3+ archived question empirical tests before deployment. [B7, 26.4.13]

---

## BELIEF Scores (from reference-class-analyst, B7)

| Claim | P | Evidence Basis |
|-------|---|---------------|
| Run quality gate high impact | P=0.85 | Noise inputs degrade ensemble regardless of model diversity |
| Reference class instance count N<10 unreliable | P=0.80 | Literature: ±30pp 95% CI for N<10 |
| Hedging correction conditioning | P=0.70 | Correct on average but wrong for base_rate ∈ [0.40, 0.60] |
| Prospective pre-mortem ordering | P=0.55 | Not high-conviction; current clean separation captures most benefit |

---

## Open Questions

- What is the actual parse_failed rate in production runs? This determines urgency of SQ-M3.
- How many archived questions are available for testing G4/SQ-M7 hedging conditioning?
- Does the 4B Ollama local model verification add signal, or is parse failure rate too high to be useful even as verifiers?

---

## Sources

- B7 synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-13-sigma-predict-cross-pollination-synthesis.md`
