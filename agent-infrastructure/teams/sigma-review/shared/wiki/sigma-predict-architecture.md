# sigma-predict: Pipeline Architecture
Last updated: 26.4.13 | Reviews: B7

## Summary

sigma-predict is a personal prediction pipeline that orchestrates LLM calls for structured probabilistic forecasting. The pipeline moves through base rate estimation, multi-run forecasting, optional deliberation, calibration, and aggregation. Key architectural debt identified in B7: the LLMRouter had a thread-unsafe model-mutation pattern and the PROVIDERS registry integration was missing, limiting verification diversity.

---

## LLMRouter: Model-Mutation Bug and Fix

The pre-B7 LLMRouter used a try/finally pattern to temporarily mutate the client's model attribute before each call, then restore it. This is thread-unsafe (shared state mutation), conceptually wrong (clients are single-model instances in sigma-verify), and was independently identified by tech-architect (F1, F3) and CQA (CQA-F1) without coordination. [B7, 26.4.13]

The fix introduces a per-(provider, model) client cache (`_get_or_create_client()`). AnthropicClient.call() retains its model kwarg; all other providers use one cached client instance per (provider, model) pair. No threading.Lock was added — the codebase is single-threaded and the lock would add zero value for a personal tool. [B7, 26.4.13]

Interface contract (IC[1]): `LLMRouter.call()` — no model mutation; cache keyed by (provider, model).

---

## PROVIDERS Registry Integration

sigma-verify exposes a `PROVIDERS` registry of 13 provider entries, each with a `call()` interface. Pre-B7, LLMRouter did not use this registry for verification calls. [B7, 26.4.13]

`LLMRouter._init_external_providers()` now iterates PROVIDERS and loads all entries. `Config.verification_providers` controls which providers are active. The sigma-verify AnthropicClient is loaded only when Anthropic is NOT the primary model — this enforces the dual-role separation: local AnthropicClient for primary forecasting, sigma-verify AnthropicClient for cross-verification (host-model self-verification is semantically wrong per ADR[7]). [B7, 26.4.13]

Backward-compat aliases (`self._openai`, `self._gemini`) are preserved.

ADR[3] establishes that 4B local models (Ollama) are verification-only, not primary forecasting — parse failure risk too high for structured JSON forecaster output. [B7, 26.4.13]

### Multi-Model Forecasting Scope Limit

An important constraint surfaced in B7: multi-model diversity is realized **only in the verification layer**, not primary forecasting. All 5 primary forecasting runs use `config.primary_model`. BELIEF score from reference-class-analyst: multi-model IS better IF (a) runs are parse-valid, (b) n_distinct_providers ≥ 2 for extremization, (c) run quality gate excludes noise — but condition (b) is not met for primary runs in current architecture. Same-model multi-persona delivers marginal benefit only. [B7, 26.4.13]

---

## Deliberation: Provider Hardcode Fix

Pre-B7, `deliberation.py:deliberate()` hardcoded `router.call("anthropic", ...)`. This would cause a runtime failure when `config.primary_model.provider` was openai or google. Fixed to `router.call(config.primary_model.provider, config.primary_model.model_id, ...)`. This was independently raised by CQA (CQA-F6) and treated as a must-fix before build. [B7, 26.4.13]

---

## Known Tech Debt (Pre-B7, Unresolved)

| ID | Issue | Risk |
|----|-------|------|
| CQA-F2 | `_extract_json` raises ValueError on malformed input; duplicated in deliberation.py | Medium |
| CQA-F3 | Dead code in `_collect_platform_signals` — if-branch never executes | Medium |
| CQA-F4 | RegistryCache exists but unused — O(N) re-reads on every registry access | Medium |
| CQA-F7 | Temporal firewall in base_rate silently disabled; docstring falsely claims protection | Medium |
| CQA-F8 | `apply_hedging_correction` (non-scaled variant) is dead production code with live tests | Low |
| CQA-F9 | `_estimate_effective_n` effectively always returns n | Low |
| CQA-F10 | Zero test coverage on all pipeline execution modules (orchestrator, forecaster, deliberation, verification, base_rate) | High |

CQA-F7 is additionally flagged as a process integrity issue: the docstring makes a false security claim. This is documented in open defects from B7 (BUILD-R3) as a must-fix. [B7, 26.4.13]

---

## Open Defects (from CQA CONDITIONAL PASS, B7)

1. **BUILD-R4 (P0):** LLMAuditLogger is instantiated but never called — `Config.audit_path` feature silently does nothing. Must wire `log_call()` into LLMRouter or remove the config field.
2. **BUILD-R1 (P1):** `test_client_cache_keyed_by_provider_model` is a no-op test — `if False` branch bypasses `_get_or_create_client`. Must rewrite.
3. **BUILD-R3 (P1):** CQA-F7 temporal firewall docstring still claims protection that doesn't exist.
4. **BUILD-R5 (P1):** `PROVIDERS cls(model=model)` kwarg not verified against sigma-verify client signatures — may fail at runtime for non-Anthropic providers.

---

## Sources

- B7 synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-13-sigma-predict-cross-pollination-synthesis.md`
