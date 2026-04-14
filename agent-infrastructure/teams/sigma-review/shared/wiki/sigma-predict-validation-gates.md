# sigma-predict: Pipeline Validation Gates
Last updated: 26.4.13 | Reviews: B7

## Summary

B7 introduced `PipelineValidator` — a new inter-stage validation layer at `src/pipeline/validator.py`. Five gates check pipeline health at defined checkpoints. Non-blocking by default; configurable hard-stop mode. This is a direct port of the gate philosophy established in sigma-review orchestrator (validate command), applied to the prediction pipeline context.

---

## Architecture

`PipelineValidator` is instantiated in the orchestrator and called after base_rate, runs, and calibration stages. It exposes five gate methods plus a `validate_all()` convenience call.

Integration: `Config.strict_validation=True` converts all gate failures from pipeline warnings to `PipelineError` (hard stop). Default is non-blocking — gates populate `PredictionRecord.pipeline_warnings` and the pipeline continues. [B7, 26.4.13]

Design rationale (ADR[5]): pipeline_warnings infrastructure already existed on PredictionRecord. Gates should not kill the pipeline on bad single search results — the intent is observability and operator awareness, not blocking. [B7, 26.4.13]

---

## The Five Gates

### base_rate_gate
Checks that the estimated base rate is within the valid probability range [0.01, 0.99]. Values at the extremes (0 or 1) indicate a degenerate base rate estimate. Configurable threshold. [B7, 26.4.13]

Pre-mortem consideration: false positives possible for legitimate extreme base rates (e.g., historical near-certainties). Default range 0.01–0.99 is intentionally permissive. [B7, 26.4.13]

### probability_gate
Checks that the calibrated probability estimate is within a calibrated range — tighter than raw [0,1], reflecting that extreme probability outputs from LLMs typically indicate failure modes rather than genuine extreme probabilities. [B7, 26.4.13]

### run_count_gate
Checks that the actual number of completed runs matches the requested run count. A mismatch indicates provider failures, timeouts, or parse failures that reduced the ensemble size below target. [B7, 26.4.13]

### parse_failure_gate
Warns when any run has `parse_failed=True`. This gate surfaces the parse_failed contamination issue (see sigma-predict-prediction-methodology.md ## Aggregation: parse_failed Contamination) — the warning is visible but exclusion is not yet implemented. [B7, 26.4.13]

### search_quality_gate
Warns when average search score across runs falls below 3. Low search quality indicates the pipeline is operating on low-signal source material. [B7, 26.4.13]

---

## Non-Blocking Philosophy

The non-blocking default reflects the personal-tool context (C1 constraint): the operator running the pipeline is the same person viewing the results. Hard stops on every validation warning would interrupt legitimate edge-case predictions. The operator can review warnings and make their own call.

`Config.strict_validation=True` provides the hard-stop mode for contexts where the operator wants pipeline integrity enforcement (e.g., batch runs, automated evaluation). [B7, 26.4.13]

---

## Relationship to sigma-review Gate Infrastructure

The V1-V28 mechanical gates in sigma-review orchestrator enforce process compliance (BELIEF[], DA exit-gate, phase skip, etc.). The PipelineValidator in sigma-predict enforces prediction data quality. Different domains, same philosophy: make violations visible and configurable, not silent. The sigma-review gate infrastructure was a reference point during design. [B7, 26.4.13]

---

## Open Questions

- Should `parse_failure_gate` be promoted to default-blocking once the parse_failed exclusion (SQ-M3) is implemented? A warning about a contaminated input is lower value once the pipeline can exclude it automatically.
- What threshold for `search_quality_gate` separates signal from noise in practice? The default of 3 was set without empirical calibration.

---

## Sources

- B7 synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-13-sigma-predict-cross-pollination-synthesis.md`
