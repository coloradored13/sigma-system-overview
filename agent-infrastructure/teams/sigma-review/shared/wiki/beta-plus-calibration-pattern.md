# β+ Calibration Pattern (WARN-First Promotion Mechanics)
Last updated: 26.4.25 | Reviews: B-r19-remediation

## Summary

β+ calibration is a WARN-first gate-promotion mechanism: a new analytical-tier check fires as a WARN, emits a CAL-EMIT telemetry record, and accumulates evidence in `calibration-log.md`. Once threshold conditions are met (≥3 reviews, ≤20% false-positive rate, ≥5 DA-verdicted records), `audit-calibration-gate.py` recommends PROMOTE → BLOCK. The pattern was operationalized for A20/A22/A23/A24 in the R19-remediation build. The dominant failure mode is producer/consumer schema decoupling — the producer (chain-evaluator) and consumer (audit-calibration-gate) must agree on record format, allowlists, and escape rules. Four schema-decoupling defects surfaced in C3 alone. [B-r19-remediation, 26.4.25]

---

## Why WARN-First

A new gate cannot start as a hard BLOCK because:
- False-positive rate is unknown until the gate has fired against real findings.
- The codebase contains pre-existing content that may match the rule but was not authored under it.
- Lead has no calibration data to defend invocations under C5 (when a gate over-fires, defend each invocation rather than add exceptions).

WARN-first lets the gate accumulate evidence, lets DA verdict each fire, and lets `audit-calibration-gate.py` decide promotion deterministically rather than by lead intuition. [B-r19-remediation, 26.4.25]

---

## CAL-EMIT Schema

When a path-β+ gate fires, chain-evaluator emits a single-line record to `calibration-log.md`:

```
gate-id | review-id | finding-ref | fire-reason | workspace-context:{agent}:{50-char-excerpt} | da-verdict:PENDING
```

**Field semantics**:
- `gate-id`: A20, A22, A23, or A24 (must be in `audit-calibration-gate.VALID_GATES`).
- `review-id`: build-id or review-id of the firing context.
- `finding-ref`: anchor or line-id pointing to the source finding.
- `fire-reason`: human-readable trigger (e.g., "missing |source: tag", "no XVERIFY in 500-char window").
- `workspace-context`: `{agent-name}:{50-char-excerpt}` of the offending content.
- `da-verdict`: starts as `PENDING`; updated to `TRUE-POSITIVE` / `FALSE-POSITIVE` / `NOT-REVIEWED` by DA.

**Producer** (chain-evaluator.py:613): formats the record. **Consumer** (audit-calibration-gate.py:34-41): parses with `[^|]+?` capture per field. Producer-side sanitization is required because real findings routinely contain pipe-delimited inline tags per §2d source-tag notation. [B-r19-remediation, 26.4.25]

### Pipe-Escape Defect (resolved)
C3 round-1 surfaced: producer formatted `clean_excerpt = excerpt.replace("\n", " ").strip()[:50]` WITHOUT pipe-escape; consumer regex `[^|]+?` excluded pipes. Failure mode: production records with HIGH-severity + |source:[T1(...)]| tags landed in malformed bucket; audit-calibration-gate under-reported, biasing PROMOTE/RECALIBRATE thresholds. Fix: producer-side sanitization at chain-evaluator.py:613-616 (pipes replaced inline before record emission). XVERIFY: openai high-agree + google high-agree (cross-family confirmed). [B-r19-remediation, 26.4.25]

---

## Threshold Constants

Defined identically in `directives.md` and `audit-calibration-gate.py` (CDS r1 verified character-for-character match):

- **≥ 3 reviews**: gate must have fired across at least 3 distinct review-ids before promotion eligibility.
- **≤ 20% false-positive rate**: of DA-verdicted records, no more than 1 in 5 may be FALSE-POSITIVE.
- **≥ 5 DA-verdicted records**: at least 5 records must have a non-PENDING verdict (sample size for FP-rate calculation).

Decision ordering is exhaustive without overlap: HOLD if not enough DA verdicts; RECALIBRATE if FP-rate >20%; PROMOTE if all three conditions met. [B-r19-remediation, 26.4.25]

The 20% FP threshold is C5-compatible: it forces defense-of-invocation rather than exception-addition. PM[CDS-4] flags this threshold as "revise after 2 promotions" — too strict could indefinitely delay useful promotion. [B-r19-remediation, 26.4.25]

---

## Producer/Consumer Schema-Decoupling Failure Mode

This is the **dominant failure class** observed in C3 — four instances of the same architectural defect:

1. **Pipe-escape (r1)**: producer didn't sanitize pipe in 50-char excerpt; consumer regex assumed pipe-free. Fix: producer-side replace.
2. **A24 VALID_GATES (r2)**: producer emitted A24 records; consumer allowlist still `{"A20", "A22", "A23"}`. Fix: VALID_GATES += A24 + auto-syncing argparse choices from sorted(VALID_GATES).
3. **BLOCK 3→4 doc drift (r1)**: phase-gate code shipped BLOCK 4; 27 documentation files said BLOCK 3. Fix: TW OPTION 2 phrasing sweep (drops numeric identifier).
4. **§-enumeration (r3)**: directives.md enumerates 3 §-tiers; producer (chain-evaluator) added 4th gate (A24) without updating the directive. Deferred to future build.

**General mitigation pattern (preferred when possible)**: derive the consumer's allowlist from the producer's source-of-truth at runtime. Example: `argparse choices = sorted(VALID_GATES)` makes the CLI choices automatically follow the allowlist. The producer cannot drift from a runtime-derived consumer.

**Operational mitigation pattern (when single-source isn't possible)**: explicit re-sync from canonical source whenever the producer changes. TW R3-2 canonical-block-hash-identity invariant is the operational version of this pattern (29 files resynced from `_template.md:140-152` to byte-identical hash). [B-r19-remediation, 26.4.25]

**Detection pattern (DA r3 spot-check predicted-and-found)**: after seeing 3 instances, search for the 4th proactively. Look for hardcoded enumerations in human-facing context (directives, agent files, skill phase docs) that should be tracking machine-enforced source-of-truth. [B-r19-remediation, 26.4.25]

---

## Empirical-XVERIFY-via-local-python-c (Pattern Promotion)

CDS surfaced this technique in C3 round 1 to verify the pipe-escape defect: rather than running synthetic-fixture unit tests against a stubbed parser, run a small `python -c` exercise against the real producer + real consumer + real calibration-log content. This caught a material latent defect that synthetic-fixture tests missed (the producer was being called correctly in tests but pipes never appeared in fixture data). Promotion-worthy. [B-r19-remediation, 26.4.25]

CQA generalized this in r3 as the **regression-lock pre-flight assertion pattern**: tests halt non-silently if a contract is reverted (`assert "A24" in acg.VALID_GATES`). Three-layer robustness: pre-flight assertion + end-to-end exercise + three independent assertions on produced record. DA noted this as "better than any test pattern DA had seen this build." [B-r19-remediation, 26.4.25]

---

## Open Questions

- **PM[CDS-1] (40% probability)**: §2i CAL-EMIT calibration data never reaches 3 reviews → WARN-only indefinitely. Mitigation: sigma-audit auto-invokes audit-calibration-gate. Ongoing. [B-r19-remediation, 26.4.25]
- **PM[CDS-4] (30%)**: WARN→BLOCK promotion delayed beyond useful window because 20% FP threshold is too strict. Mitigation: revise after 2 promotions. Ongoing. [B-r19-remediation, 26.4.25]
- **A24 no-Condition-1-suppression**: A24 intentionally has no Condition-1-style suppression heuristic — A20 catches false-precision via qualifiers; A24 catches missing-XVERIFY which qualifiers don't resolve. Synthesis-defer: 1-line note in audit-calibration-gate.py docstring header to prevent future readers from assuming behavioral parity. [B-r19-remediation, 26.4.25]
- **calibration-log integrity vs DA-verdict audit-trail scope** (SS r1): calibration-log.md is a SIBLING log to workspace gate-log; agents/lead may conflate. SS classified calibration-log integrity contract as separate from ADR[SS-3]'s DA-verdict trail scope (consistent with ADR[CDS-2..3] design intent). [B-r19-remediation, 26.4.25]

## Contradictions

None unresolved. SS r1 carried CDS's prior OSError silent-skip concern forward correctly with consistent classification.

## Sources

- B-r19-remediation synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md`
