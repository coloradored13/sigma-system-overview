# Cross-Model Protocol Design — Calibration and Empirical Findings
Last updated: 26.5.2 | Reviews: R16, R-2026-04-28-shared-process-hardening

## Summary

Calibration and confidence estimates for SIGMA-COMM-WIRE and cross-model protocol design generally. Covers bootstrap reliability, format choice rationale, adoption risk, and pre-mortem failure modes. Produced by reference-class-analyst with DA challenge. These findings inform confidence levels for the protocol specification — they are not the spec itself.

[R-2026-04-28-shared-process-hardening, 26.5.2] also adds operational findings on XVERIFY behavior in practice: single-provider fallback when `cross_verify` hangs, and the Anthropic exclusion rule for cross-model verification.

---

## Bootstrap Reliability — Conditional on Interface Mode

No production system demonstrates genuine model-to-model cold-start bootstrapping. All production multi-agent systems (A2A, MCP, AutoGen, OpenAI SDK) use infrastructure/framework pre-configuration. Bootstrap reliability is therefore primarily an infrastructure problem, not a protocol problem. [R16, 2026-04-09]

| Mode | P(success) | 80% CI | Evidence basis |
|---|---|---|---|
| Infrastructure-assisted (framework pre-configures, constrained decoding, JSON mode) | 85% | [72%, 93%] | Every production system uses this path |
| JSON mode available, no infrastructure assistance | 70–80% | — | Conditioned on constrained decoding |
| Instruction-following only, no infrastructure | 40–55% | [35%, 70%] | Empirically untested for protocol cold-start |
| Messages alone, zero prior knowledge | 35% | [20%, 52%] | Zero empirical precedent; plausible from JSON benchmarks |

**Prominent caveat:** The PROTOCOL_HANDSHAKE message type is valuable in both modes — in infra-assisted mode it documents the contract; in messages-alone mode it attempts self-description. Its value is not negated by infrastructure dominance. [R16, 2026-04-09]

---

## Format Choice — JSON

P(JSON optimal cross-model format) = 72% | 80% CI [58%, 84%]

**Training-data circularity caveat:** JSON's dominance is partially circular — models produce JSON well because trained on JSON. This is evidence of reliability, not theoretical optimality. The review compared JSON against formats known to be worse (YAML, XML), not against potentially better M2M formats (S-expressions, binary+text hybrids). DA flagged this as a confirmation bias pattern. Practically irrelevant given the C1/C2 design constraints (human-decodable, cross-architecture), but the caveat stands for future protocol research. [R16, 2026-04-09]

**Why not YAML:** Indentation fragility and type coercion traps under model generation pressure.
**Why not XML:** Verbosity and nesting depth push into format error territory.

---

## Single Protocol for Three Use Cases

P(single protocol covering messages, workspace, memory) = 20% | 80% CI [12%, 32%]

Base rate is low. Email required 3 protocols; HTTP required WebSocket for streaming. The type-discriminated-union approach (one envelope, type-discriminated payloads) is the best-available bet via the HTTP content-type analogy, but workspace (concurrent writes, consistency) and memory (persistence, retrieval, staleness) may eventually demand protocol extensions. [R16, 2026-04-09]

---

## Epistemic-Type Field — Adoption Friction Caveat

FIPA ACL's 22 performative types were individually defensible but collectively lethal to adoption. A single categorical field with 9 values and a sensible default (`inferred`) has roughly 1/50th the adoption friction of FIPA's full semantic machinery. CDS-F3's epistemic_type has strong cognitive science grounding on the benefit side; FIPA provides the outside-view risk on the adoption side. Net assessment: low-friction contribution; the field likely persists even if the rest of the spec is trimmed. [R16, 2026-04-09]

---

## Pre-Mortem Risks

Joint P(at least one materializes within 2yr) = 65–75% [R16, 2026-04-09]

| Risk | P | Description | Mitigation |
|---|---|---|---|
| Existing standard preemption | 35–40% | A2A achieves critical mass, rendering novel protocols redundant | Design as expressible A2A profile |
| NL good enough | 20–25% | Next-gen models parse NL at 99.9%. Format drift was transient. | Protocol value shifts to auditability |
| Protocol proliferation | 15–20% | 5+ approaches, none wins. XKCD 927. | Keep spec minimal enough to layer on existing |
| Infrastructure solves at different layer | 10–15% | Constrained decoding + middleware make format irrelevant | Protocol provides schema that tooling enforces |
| Problem misspecified | 5–10% | Communication format was never the bottleneck | Acknowledge scope: transmission fidelity, not orchestration quality |

---

## Known Empirical Gaps

**GAP 1 (SQ[5]): Cold-start empirical data.** No production test of model-to-model protocol bootstrapping exists. Priority empirical test: give N diverse models a Tier-1 handshake message and measure field-level compliance rates. [R16, 2026-04-09]

**GAP 2: Token cost quantification.** Per-message overhead estimated at 150–300 tokens but ungrounded empirically. No reference class for self-describing vs. implicit-convention overhead. [R16, 2026-04-09]

**GAP 3: Concurrent write semantics under pressure.** Can LLMs reliably produce sequence numbers under generation pressure? Can they produce vector clocks? Untested. [R16, 2026-04-09]

**GAP 4: Multi-session persistence.** Protocol defines format but not retrieval, indexing, or staleness handling for cross-session memory use. [R16, 2026-04-09]

---

## Hypothesis Dispositions

| Hypothesis | Disposition | Confidence | Notes |
|---|---|---|---|
| H1: Structured > NL for coordination | CONDITIONALLY CONFIRMED | P=72% [58%, 84%] | JSON for coordination, NL for content |
| H2: Self-describing solves cold-start | CONFIRMED with caveats | P=35–85% conditional on infrastructure | Requires redundant encoding |
| H3: Architectures differ meaningfully | PARTIALLY CONFIRMED | P=55% [38%, 72%] | TRUE at output framing level; FALSE at parse level. May be false within 12–18 months. |
| H4: NL most robust | FALSE as stated | P=38% [22%, 55%] | NL = most fault-tolerant but least precise. Correct for content fields, wrong for coordination. |
| H5: Optimal protocol looks alien | FALSE | P=18% [8%, 32%] | Models exploit shared training signal. Alien formats require in-context learning from scratch. |

[R16, 2026-04-09]

---

## Contradictions

None within this review. H5 represents the clearest falsification — pre-review prior might have placed alien-format P higher given theoretical arguments; the independent convergence evidence refutes it. [R16, 2026-04-09]

---

## XVERIFY Operational Findings

[R-2026-04-28-shared-process-hardening, 26.5.2] Two operational rules for XVERIFY usage emerged in practice during this build's C3 close-out:

**Single-provider fallback when `cross_verify` hangs.** Per `build-directives.md §2h`, when the multi-provider `cross_verify` MCP call hangs (a known infra issue), agents and lead are authorized to fall back to a single-provider `verify_finding` call against one non-Anthropic provider. In this build, `openai gpt-5.4` was used as the fallback verifier on ADR[6]/IC[6] BLOCK 5 compliance and returned medium-confidence agreement. Result is recorded as **partial / medium-confidence** in the synthesis — a single-provider verify is NOT the same evidence weight as a multi-provider cross-verify, and synthesis must label it as such rather than presenting partial verification as full cross-verify.

**Anthropic exclusion rule for cross-model verification.** Per `feedback_xverify-anthropic-excluded.md` (26.4.23) and reaffirmed in this build: sigma-verify cross-model checks must exclude the `anthropic` provider, because Claude verifying Claude is not cross-model. This is enforced in spawn prompts as a temporary measure until sigma-verify default-excludes anthropic from `cross_verify`. The rule applies to both the multi-provider and single-provider fallback forms — when falling back to a single provider per §2h, choose a non-Anthropic provider (`openai`, `google`, etc.). The rule is not a quality concern about Claude as a verifier; it is a logical-independence concern (a self-consistent verifier of itself does not provide cross-model convergence evidence).

**Pattern**: cross-model protocol design must accommodate the operational reality that multi-provider verification can hang, fall back gracefully, and label the fallback honestly. Building this distinction (full cross-verify vs single-provider fallback verify) into the verification record format is a candidate addition to the SIGMA-COMM-WIRE error taxonomy and result-confidence enum.

---

## Sources

- `archive/2026-04-09-cross-model-protocol-synthesis.md` — R16 synthesis, Appendix: Calibration and Confidence Notes (reference-class-analyst, with DA challenge)
- R-2026-04-28-shared-process-hardening synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-synthesis.md`
