# SIGMA-COMM-WIRE Protocol
Last updated: 2026-04-09 | Reviews: R16

## Summary

SIGMA-COMM-WIRE v0.1.0 is a structured JSON protocol for model-to-model communication across heterogeneous LLM architectures. It operates at the cognitive layer — how models structure and interpret messages — not at the transport or routing layer. It unifies three use cases (ephemeral messages, shared workspace, persistent memory) under a single envelope schema discriminated by message type.

The protocol independently converges on the same JSON-envelope + natural-language-content hybrid architecture as A2A (Google, 2025), NLIP (Ecma TC-56, December 2025), and MCP (Anthropic/Linux Foundation). It extends those standards with epistemic-type primitives, drift-mitigation fields, System 1/2 structural separation, belief state categorization, convergence state for multi-party coordination, and a three-category error taxonomy. [R16, 2026-04-09]

---

## Core Design Principles

Eight principles govern the protocol. [R16, 2026-04-09]

**P1: Envelope-first.** Routing fields appear before content fields in every message. Receiving model processes coordination metadata (System 1) before semantic content (System 2). This is cognitively load-reducing and protects against format drift truncating coordination fields.

**P2: Additive-only evolution.** Schema versions add fields; they never remove or rename fields. Receivers MUST ignore unknown fields; they MUST NOT error on unknown fields.

**P3: JSON mode preferred.** All senders SHOULD use JSON mode / constrained decoding when available. Receivers MUST implement extraction fallback (find first `{`, extract to matching `}`) for instruction-following mode.

**P4: Verbose over compressed.** `message_id` not `mid`. `sender` not `snd`. Single-token keys reduce perplexity across diverse tokenizers and improve production reliability. Parsability > token efficiency.

**P5: One protocol, three use cases.** Message type discriminates use case. Envelope schema is identical across all types. Follows the HTTP content-type pattern.

**P6: Self-describing once.** PROTOCOL_HANDSHAKE bootstraps all subsequent communication. Per-message schema repetition is prohibited.

**P7: Epistemic_type over numeric confidence.** Categorical source-provenance tags are mandatory. Numeric confidence is advisory and optional. Categorical provenance types transfer reliably across model architectures (~70-85%); numeric confidence is systematically poorly calibrated in verbalized form (ECE 0.12–0.40).

**P8: Maximum nesting depth = 3.** Nested JSON >4 levels produces statistically higher format error rates across model families under generation pressure.

---

## Base Envelope Schema

Every message — regardless of type — MUST contain all required envelope fields, and they MUST appear before payload fields in the serialized JSON object. [R16, 2026-04-09]

Required fields: `schema_version`, `message_id` (UUID v4), `session_id` (UUID v4), `message_type` (enum), `sender` (format: `role/model_family`), `recipient` (agent ID or `"*"` for broadcast), `timestamp` (ISO 8601 UTC), `payload` (object).

Optional envelope fields: `reply_to` (UUID of replied-to message), `sequence_number` (required for WORKSPACE_WRITE), `epistemic_type` (required in most payloads), `belief_state_form`.

Field constraints:
- `schema_version` MUST match a version from the session's PROTOCOL_HANDSHAKE. Unknown versions → ERROR(VERSION_MISMATCH).
- `message_id` MUST be globally unique. Duplicate → ERROR(DUPLICATE_MESSAGE), discard.
- `sender` / `recipient` MUST NOT use programming-language reserved words or be empty strings.
- All field names: snake_case. No abbreviations. No reserved words.

---

## Message Types (9)

### PROTOCOL_HANDSHAKE
First message of every session. Bootstraps a receiver with zero prior protocol knowledge. Mid-session handshake is a spec violation → ERROR(HANDSHAKE_REJECTED).

Three tiers based on receiver context capacity:
- **T0 (~300 tokens):** For sub-8K context models. Minimal required fields and enum lists only.
- **T1 (~600 tokens):** Default. Adds `field_semantics`, `version_negotiation`, and `ack_format`.
- **T2 (~1000 tokens):** For high-stakes or first-time cross-architecture sessions. Adds worked examples per message type, one anti-example with violation annotations, and an explicit injection-risk warning.

All tiers require acknowledgment: receiver replies MESSAGE with `reply_to` = handshake message_id, `body: "ACK"`, `version_selected: "0.1.0"`.

[R16, 2026-04-09]

### MESSAGE
Core agent-to-agent communication: findings, analysis, status, requests.

Required payload fields: `subject` (≤120 chars), `body` (natural language — not executable), `epistemic_type`.

Optional: `belief_score` (float [0,1], advisory), `reasoning`, `evidence` (array), `tags`, `belief_state_basis`, `xverify_provider`, `xverify_result`, `stance_target`, `convergence_state`, `open_questions`.

`stance_target` (message_id of claim being assessed) is REQUIRED when `epistemic_type` is `agree_independent`, `agree_unverified`, `disagree`, or `abstain`.

### WORKSPACE_WRITE
Writes state to shared workspace. Supports concurrent writes from N agents.

Required payload fields: `section` (hierarchical path, e.g. `findings/tech-architect`), `key`, `value`, `merge_strategy` (overwrite | append | merge_object), `epistemic_type`.

Optional: `supersedes` (UUID of prior write this replaces), `ttl_seconds`.

Concurrent write rules:
- Writes applied in `sequence_number` order, not arrival order.
- Same section+key, different sequence_numbers: higher wins.
- Same section+key+sequence_number (collision): BOTH preserved with CONFLICT suffix. Session lead resolves.

### MEMORY_STORE
Writes to persistent memory that survives session termination.

Required payload fields: `memory_key` (format: `category/identifier`), `category` (finding | decision | calibration | pattern | correction | reference), `content`, `tags` (min 1), `epistemic_type`, `source_session`.

Optional: `belief_score`, `expires_at`, `supersedes_key`.

### ERROR
Signals a processing failure. Three categories with different recovery logic.

| Error category | Recovery | Error codes |
|---|---|---|
| structural | Retry with repair hint. Max 2 retries → HANDSHAKE_REFRESH → human escalation | MISSING_REQUIRED_FIELD, WRONG_FIELD_TYPE, INVALID_FIELD_VALUE, HANDSHAKE_REJECTED, VERSION_MISMATCH, DUPLICATE_MESSAGE |
| semantic | Flag and continue. Blind retry produces same error. Sender sends AMENDED. Persists → DISPUTED. | CONTRADICTORY_FIELDS, UNRESOLVABLE_REFERENCE |
| pragmatic | Not enough info. Receiver sends REQUEST_CLARIFICATION. Sender responds with ELABORATION. | INSUFFICIENT_CONTEXT, EPISTEMIC_TYPE_IMPLAUSIBLE |

Required payload fields: `error_category`, `error_code`, `source_message_id`, `recovery_action`, `retry_permitted` (true for structural, false for semantic/pragmatic).

### REQUEST_CLARIFICATION
Receiver needs more information. NOT an error — a continuation protocol.

Required: `source_message_id`, `missing_context`. Optional: `specific_fields`, `urgency` (blocking | non-blocking).

### ELABORATION
Sender responds to REQUEST_CLARIFICATION.

Required: `clarifies_message_id`, `clarification_request_id`, `additional_context`, `epistemic_type`.

### AMENDED
Sender corrects a prior message after receiving a SEMANTIC error.

Required: `amends_message_id`, `correction_summary`, `subject`, `body`, `epistemic_type`.

### DISPUTED
Marks a message as contested when semantic error cannot be resolved by retry.

Required: `disputed_message_id`, `dispute_reason`, `human_review` (boolean), `epistemic_type`.

[R16, 2026-04-09]

---

## Epistemic Type (9-value enum)

Encodes HOW the sender arrived at content — the generative process, not a quality rating. Placed in System 1 (envelope layer): processed before payload, governs content trust model before body is read.

Graceful fallback rule: absent or unrecognized value → treat as `inferred`. No structural error. [R16, 2026-04-09]

| Value | Meaning | Implied failure mode | Receiver action |
|---|---|---|---|
| `inferred` | Concluded by reasoning. No single traceable procedure. **DEFAULT.** | Reasoning error, hallucination | Standard skepticism. Seek corroboration for load-bearing claims. |
| `directly_observed` | Present in sender's current input context. Not recalled, not reasoned. | Observation error (rare) | Low skepticism. Ground truth unless input is suspect. |
| `retrieved_verbatim` | From context, document, or memory with minimal transformation. | Source error or retrieval error | Verify the source, not the reasoning. |
| `computed` | Derived by explicit logical or algorithmic operation sender can trace. | Procedure error or input error | Verify the procedure and inputs. |
| `cross_verified` | Verified against at least one independent source or model. | Verification quality depends on verifier | Higher trust. Request xverify_provider + xverify_result if load-bearing. |
| `model_generated` | Delegated to sub-process (tool, another model). Sender is relaying. | Propagated error from sub-process | Treat as sub-process's provenance. Minimum `inferred` trust. |
| `agree_independent` | Multi-party: sender independently verified before agreeing. Own evidence chain. | Independent review quality | Full evidential weight. Independent confirmation. |
| `agree_unverified` | Multi-party: sender agrees with majority but has NOT independently verified. | Conformity masquerading as confirmation | **Zero additional evidential weight.** Social signal only. |
| `disagree` | Multi-party: sender holds incompatible position. MUST pair with `reasoning` field. | — | Blocking signal. Convergence cannot advance until resolved. |
| `abstain` | Multi-party: sender has insufficient basis for any position. | — | Neutral. Neither confirms nor blocks convergence. |

Additional fallback rules:
- `cross_verified` without `xverify_provider` → treat as `inferred`.
- `disagree` without `reasoning` → treat as `abstain`.
- `agree_*` without `stance_target` → treat as `inferred`.

**Gaming caveat:** `epistemic_type` is self-reported and not cryptographically enforced. Cannot be solved at the protocol layer. Mitigations: DA roles audit epistemic_type distribution (uniform high-credibility tagging = process violation signal); `cross_verified` claims checked against known providers via `xverify_provider`; receiving agents assess plausibility against content. [R16, 2026-04-09]

---

## Belief State Form (5-value enum)

Captures uncertainty TYPE rather than uncertainty MAGNITUDE. Different from `epistemic_type` (provenance) — this classifies the structural pattern of the sender's epistemic state. Default: `provisional`. [R16, 2026-04-09]

| Value | Meaning | Receiver action |
|---|---|---|
| `high_confidence` | Strong consistent evidence. Sender has cross-checked. | Load-bearing. Challenge only if contradictory evidence present. |
| `provisional` | Sender's best current position. Expected to update. **DEFAULT.** | Working hypothesis. Flag as provisional in downstream reasoning. |
| `evidence_conflict` | Evidence points in multiple directions. | Actively contested. Seek additional signal before further inference. |
| `knowledge_gap` | At edge of sender's reliable knowledge. | High skepticism. Verify before acting. Do not propagate as established. |
| `delegated` | Relaying from sub-process; sender cannot assess independently. | Treat as minimum `provisional`. Verify sub-process if load-bearing. |

When both `belief_state_form` and `belief_score` are present: `belief_state_form` takes precedence for processing decisions. `belief_score` is OPTIONAL, advisory, and retained for numeric use cases only.

**Tension noted:** Classifying one's uncertainty type is a System 2 operation for the sender but a System 1 input for the receiver. Placement in envelope may impose higher sender-side cognitive cost than other envelope fields. Open design question. [R16, 2026-04-09]

---

## Convergence State (multi-party coordination)

In N>2 communication, unanimous agreement may be 4 independent confirmations or 1 confirmation + 3 conformity signals. `convergence_state` is an optional field in MESSAGE payloads that surfaces the distribution. [R16, 2026-04-09]

```
convergence_state:
  claim_id        — message_id of original claim
  participant_count
  positions:
    agree_independent / agree_unverified / disagree / abstain / pending
  status          — one of: insufficient | provisional | strong | contested | deadlock
```

Status computation:
- `insufficient`: 0 `agree_independent`. Do not use as basis for inference.
- `provisional`: ≥1 `agree_independent`, 0 `disagree`.
- `strong`: ≥2 `agree_independent`, 0 `disagree`. Load-bearing within session.
- `contested`: ≥1 `disagree`. Do not advance until resolved.
- `deadlock`: `agree_independent` = `disagree`, ≥1 each. Cannot resolve by counting. Escalate via DISPUTED + `human_review: true`.

**Critical:** Unanimous `agree_unverified` = `insufficient`. Herding cascade cannot produce `strong` convergence.

---

## System 1 / System 2 Field Classification

Rule: if a field's value changes how the receiver processes OTHER fields → System 1 (envelope, processed first). If it carries content to reason about → System 2 (payload). [R16, 2026-04-09]

System 1 fields: `schema_version`, `message_id`, `session_id`, `message_type`, `sender`, `recipient`, `timestamp`, `reply_to`, `sequence_number`, `epistemic_type`, `belief_state_form`.

System 2 fields: `subject`, `body`, `reasoning`, `evidence`, `belief_state_basis`, `xverify_provider`, `xverify_result`, `open_questions`, `convergence_state`, `belief_score`, `stance_target`.

---

## Schema Evolution Rules

**E1: Additive-only.** Never remove or rename fields across versions.
**E2: Unknown fields MUST be silently ignored.**
**E3: Version negotiation.** PROTOCOL_HANDSHAKE lists `supported_versions`. Receiver responds with `version_selected`. No common version → ERROR(VERSION_MISMATCH).
**E4: Semantic versioning.**
  - Patch (0.1.x → 0.1.y): Non-normative only. Wire format identical.
  - Minor (0.1.x → 0.2.x): Additive. New optional fields, new enum values. Backward compatible.
  - Major (0.x → 1.x): Breaking change (new required fields or changed field semantics). Requires version negotiation.
**E5: Field deprecation.** Fields deprecated in handshake `deprecated_fields` array. Remain valid to send. Removed only at next major version.

[R16, 2026-04-09]

---

## Failure Modes

| Failure | Condition | Resolution |
|---|---|---|
| Handshake rejection | Mid-session PROTOCOL_HANDSHAKE | ERROR(HANDSHAKE_REJECTED). Start new session. |
| Version deadlock | No overlap in supported_versions | (a) sender downgrades; (b) out-of-band coordination; (c) DISPUTED + human_review=true |
| Token budget exhaustion | Receiver ≤8K context, handshake too large | Sender sends T0 if context limit known; receiver replies with `context_exceeded: true` |
| Format extraction failure | Instruction-following mode wraps JSON in framing text | Find first `{`, extract to matching `}`. If fails → ERROR. |
| Epistemic-type gaming | Agent marks all findings as `cross_verified` or `directly_observed` | Protocol cannot enforce. DA audits distribution. Mitigation at receiving-agent layer. |
| Concurrent write collision | Two agents write same section+key with same sequence_number | Both preserved with CONFLICT suffix. Session lead resolves. |

[R16, 2026-04-09]

---

## Interface Mode Recommendations

| Interface Mode | Recommended | Bootstrap P |
|---|---|---|
| JSON mode / constrained decoding | Strongly preferred | 70–80% |
| Function calling / tool use | Preferred | — |
| Instruction-following (no JSON mode) | Supported but degraded | 40–55% |
| Raw completion | Not recommended | ~35% |

[R16, 2026-04-09]

---

## Relationship to External Standards

| Standard | Date | Convergent primitives |
|---|---|---|
| A2A (Google, 150+ orgs) | Apr 2025 | JSON envelope, capability discovery, structured metadata + NL content |
| NLIP (Ecma TC-56, ECMA-430-434) | Dec 2025 | NL as first-class content type, multimodal envelope |
| MCP (Anthropic, Linux Foundation) | 2024 | JSON-RPC 2.0, capability handshake, version negotiation, typed primitives |

SIGMA-COMM-WIRE extends these with: epistemic-type primitives, drift-mitigation fields (version + schema_ref in every message), System 1/2 structural separation, belief_state_form, convergence_state, and a three-category error taxonomy with recovery protocols. Independent convergence across A2A/NLIP/MCP on the same envelope architecture is T1 corroboration that the design choices are sound. [R16, 2026-04-09]

---

## Open Questions

**Q1 — Stance as epistemic_type vs separate field:** Current spec uses one enum for both provenance and social stance. Alternative: separate `stance` field. Trade-off: cleaner semantics vs higher field count. [R16, 2026-04-09]

**Q2 — belief_state_form envelope placement:** Classifying uncertainty type is System 2 for sender but System 1 input for receiver. Tension is real. Placement may impose higher sender-side cognitive cost than other envelope fields. [R16, 2026-04-09]

**Q3 — disagree requiring reasoning:** Current rule: absent reasoning = treated as abstain. Alternative: allow disagree without reasoning but reduce its convergence-blocking weight. [R16, 2026-04-09]

**Q4 — Concurrent write semantics:** LLMs can reliably produce sequence numbers; unclear if they can produce vector clocks under generation pressure. Simpler (last-writer-wins + sequence) may be more reliable even if less correct. [R16, 2026-04-09]

**Q5 — Multi-session persistence:** Protocol defines FORMAT but not retrieval/indexing/staleness for cross-session memory. [R16, 2026-04-09]

---

## Contradictions

None within this review. Hypothesis H5 ("optimal protocol looks alien") was FALSE by agent consensus — models exploit shared training signal; alien formats require in-context learning from scratch. No minority dissent recorded. [R16, 2026-04-09]

---

## Sources

- `archive/2026-04-09-cross-model-protocol-synthesis.md` — R16 synthesis (tech-architect, cognitive-decision-scientist, technical-writer, reference-class-analyst, devils-advocate; exit-gate PASS, A-, 3-provider XVERIFY)
