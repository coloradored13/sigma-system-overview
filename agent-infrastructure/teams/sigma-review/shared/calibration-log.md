# calibration-log — β+ audit-calibration records for WARN-first gates

Append-only log of CAL-EMIT[] records emitted by chain-evaluator when §2i/§2j/§2d-severity gates fire (path β+ audit-monitored calibration, per directives.md).

Each record is appended by chain-evaluator when a gate fires WARN. DA appends verdict at r2 exit-gate. audit-calibration-gate.py reads this file to evaluate PROMOTE/RECALIBRATE/CALIBRATING thresholds.

## Format

Each record is a single line ending in `|da-verdict:{legitimate|false-positive|not-reviewed}` (or `PENDING` before DA verdicts it):

```
CAL-EMIT[{gate-id}]: review-id:{session-date-slug} |finding-ref:{F[agent-finding-id]} |fire-reason:{condition-marker} |workspace-context:{agent}:{excerpt-50-chars} |da-verdict:{PENDING|legitimate|false-positive|not-reviewed}
```

Valid gate-id values: A20 (§2i precision gate), A22 (§2j governance artifact), A23 (§2d-severity provenance).

## Promotion thresholds (per directives.md §2i path β+)

- **PROMOTE (WARN→BLOCK):** ≥3 distinct reviews with fires AND ≤20% false-positive rate AND ≥5 DA-verdicted fires (not-reviewed ≠ verdicted)
- **RECALIBRATE:** ≥3 reviews AND >20% false-positive rate — gate heuristic needs refinement
- **CALIBRATING:** insufficient data — keep collecting

Run `python3 ~/.claude/teams/sigma-review/shared/audit-calibration-gate.py` to evaluate current state.

## Records
<!-- chain-evaluator appends below this line; DA appends verdicts in place -->
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-consumer-roundtrip |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-1] >70% confidence this migration closes by Q |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[IE-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:implementation-engineer:F[IE-1] HIGH-severity defect: cross-tenant data le |da-verdict:PENDING
CAL-EMIT[A20]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:primary-recommendation-cited |workspace-context:tech-architect:F[TA-1] primary recommendation: consolidate on Pos |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-24-r19-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity finding one |da-verdict:PENDING
CAL-EMIT[A20]: review-id:multi-fire-test |finding-ref:F[TA-2] |fire-reason:confidence>=70% |workspace-context:tech-architect:F[TA-2] >70% confidence in finding two |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-25-unnamed |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity fallback case |da-verdict:PENDING
CAL-EMIT[A22]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:HIGH-severity-governance-no-TIER-artifact |workspace-context:tech-architect:F[TA-1] HIGH-severity: lack of approval process fo |da-verdict:PENDING
CAL-EMIT[A23]: review-id:26.4.24-test |finding-ref:F[TA-1] |fire-reason:extrapolated-severity-missing-basis-tag |workspace-context:tech-architect:F[TA-1] HIGH-severity: SR-11-7 findings extrapolat |da-verdict:PENDING
CAL-EMIT[A20]: review-id:pipe-fixture |finding-ref:F[TA-1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity audit gap /source:[T1(OCC SR |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-consumer-roundtrip |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity migration defect in payment  |da-verdict:PENDING
CAL-EMIT[A24]: review-id:a24-fires |finding-ref:F[TA-1] |fire-reason:load-bearing-without-xverify:HIGH/CRITICAL-severity |workspace-context:tech-architect:F[TA-1] HIGH-severity critical failure in deployme |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-28-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-28-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-28-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
CAL-EMIT[A20]: review-id:2026-04-28-Vet-two-full-AI-agent-rollout |finding-ref:F[RL-F1] |fire-reason:HIGH/CRITICAL-severity |workspace-context:regulatory-licensing-specialist:F[RL-F1] MAINTAINED at HIGH severity. The playbook |da-verdict:PENDING
