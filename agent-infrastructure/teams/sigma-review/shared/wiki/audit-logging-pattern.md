# Audit Logging Pattern (sigma ecosystem)
Last updated: 26.4.13 | Reviews: B6, B7

## Summary

The audit logging pattern originates in ollama-mcp-bridge (B6) and was ported to sigma-predict (B7). The core design: a buffered JSON-L writer that captures per-call metadata without logging raw inputs, with configurable output path and optional-by-default behavior. The pattern is consistent across both systems with one key difference: ollama-mcp-bridge's logger is wired; sigma-predict's is not yet wired (BUILD-R4 open defect).

---

## Core Design

Audit logs are written as JSON Lines (one JSON object per line), with each entry capturing:
- Timestamp
- Provider and model
- Params hash (structural fingerprint, not raw params)
- Result hash (structural fingerprint, not raw result)
- Duration (ms)
- Cost (USD)

Raw prompts are never logged. This is a deliberate design choice in both systems: logging raw LLM prompts creates a risk surface (prompt injection artifacts in logs, inadvertent credential capture in prompt text). Structural summaries and hashes provide forensic utility without the exposure. [B6, 26.4.9] [B7, 26.4.13]

---

## sigma-predict: LLMAuditLogger

Implemented in `src/pipeline/llm_audit.py`. Buffered at BUFFER_LIMIT=10; flush at pipeline end. Optional via `Config.audit_path=None` (disabled by default). Secret keys are REDACTED from any logged metadata. [B7, 26.4.13]

**Open defect (P0 — BUILD-R4):** The logger is instantiated but never called. `Config.audit_path` configuration has no effect on pipeline behavior. The feature is architecturally sound but requires wiring `log_call()` into `LLMRouter.call()` (or removing the config field entirely). [B7, 26.4.13]

ADR[4] (sigma-predict): AuditLogger as optional component of LLMRouter, log via wrapper. Inline audit creates duplication; wrapper eliminates drift. Status: PARTIALLY IMPLEMENTED — logger created, not wired. [B7, 26.4.13]

---

## ollama-mcp-bridge: fsync-on-write

ollama-mcp-bridge's audit logger uses fsync after every write. This was a design decision reached with full multi-agent convergence: DA, CQA, and tech-architect all independently reached the same conclusion (always-fsync superior to two-path design). The rationale: audit integrity requires that logged events be durable even on process crash; buffering trades durability for throughput in a context where throughput is not the constraint. [B6, 26.4.9]

sigma-predict's LLMAuditLogger uses buffering (BUFFER_LIMIT=10) rather than fsync-per-call. Rationale: sigma-predict makes <10 LLM calls per prediction total, so the buffer will flush completely at pipeline end. The risk of losing audit data on crash is lower in a short single-pipeline run than in a long-running bridge service. [B7, 26.4.13]

This is a deliberate design divergence, not an inconsistency — the threat models differ.

---

## When to Use This Pattern

The audit logger pattern is appropriate when:
1. Multiple LLM calls are made in a pipeline and cost/performance tracking is useful
2. The operators do not want raw prompts in logs (privacy, security, or compliance)
3. The component is intended to be optional — operators who don't need audit trails should not pay the I/O cost
4. Forensic attribution of specific outputs to specific model calls is needed

Not appropriate when: single-call tools where the call itself is the full record; or when the full prompt must be captured for regulatory reasons (use a different logger that accepts that risk explicitly).

---

## Cross-System Convergence

Both systems independently converged on:
- JSON Lines format (appendable, parseable, no schema migration)
- Hash-of-params rather than raw params
- Optional-by-default (controlled by config path)

The parallel implementation is noted in B7 as a reuse opportunity (sigma-verify._parse_json_response reuse; ADR[4] sigma-predict). If the two audit loggers diverge in behavior over time, the sigma-verify logger should be treated as the reference implementation given it is the more mature and tested system. [B7, 26.4.13]

---

## Sources

- B6 synthesis (ollama-mcp-bridge audit remediation)
- B7 synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-13-sigma-predict-cross-pollination-synthesis.md`
