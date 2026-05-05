# Premise-Audit Step 7a (Pre-Dispatch Anti-Anchoring)
Last updated: 26.5.2 | Reviews: B-r19-remediation, R-2026-04-28-shared-process-hardening

## Summary

Premise-audit is a pre-dispatch step in `c1-plan.md` (Step 7a) that runs before agent spawn during sigma-build/sigma-review C1 plan phase. It surfaces frame-assumptions in the user's prompt before they get baked into agent hypotheses, mitigating analytical anchoring on flawed premises. The structure is a four-field template (PA[1-4]) and is enforced by chain-evaluator BLOCK day-one (not WARN). Step 7a is sequence-load-bearing — it must run before Step 8 hypothesis drafting. [B-r19-remediation, 26.4.25]

Confirmed [R-2026-04-28-shared-process-hardening, 26.5.2]: the BUILD-side Step 7a HARD GATE was extended to the ANALYZE side (`sigma-lead.md` and `SKILL.md`) so the same anti-anchoring discipline applies before sigma-review dispatch, not only before sigma-build. The "Step 7a" label was deliberately dropped on the ANALYZE side (kept on BUILD side at `c1-plan.md:62/137/138/174` and `build-directives.md:144/151`) to avoid a renumber-cascade in the sigma-review numbering. The four-field PA[1-4] structure, sequence constraint, premise-audit-results section, decision line, CHALLENGED/GAP rules, and DA r2 cross-check survived; only the label was dropped. This partially falsifies H7 ("verbatim reuse") — structure transfers, label does not.

---

## What Premise-Audit Is

Premise-audit fits as workflow Step 7a pre-spawn, not as a new agent role. TA + CDS independently converged on this placement during R19 ADR resolution. The motivation: hypotheses (Step 8) inherit frame-assumptions from the prompt unless those assumptions are explicitly surfaced and challenged first. [B-r19-remediation, 26.4.25]

The CDS rationale: frame-assumptions are categorically different from hypotheses. Hypotheses are claims about the world the build will test; frame-assumptions are claims about what kind of problem the build is trying to solve. If the frame is wrong, no amount of hypothesis testing will surface the error.

---

## PA[1-4] Template

Located in `c1-plan.md` Step 7a + `premise-audit-results` template + preflight checklist (3-file propagation per CAL[?]):

- **PA[1]** — what does the prompt assume about the problem class?
- **PA[2]** — what does the prompt assume about the desired outcome?
- **PA[3]** — what does the prompt assume about constraints / non-goals?
- **PA[4]** — what would change if any of PA[1-3] is wrong?

[B-r19-remediation, 26.4.25]

The PA[4] field is the most load-bearing: it forces the lead to articulate decision-relevance for each frame-assumption, preventing the audit from being a hand-wave checkbox.

---

## Sequence Constraint (Step 7a Position)

Step 7a sits between Step 7 (prompt understanding Q[]) and Step 8 (hypothesis drafting H[]). The sequence is load-bearing at `c1-plan.md:62`:

1. Step 7: Q[] decomposition (what does the prompt ask?)
2. **Step 7a: Premise-audit (what does the prompt assume?)**
3. Step 8: H[] hypotheses (what claims will the build test?)

If 7a runs after 8, hypotheses are already framed and the premise-audit becomes retrospective justification rather than prospective challenge. [B-r19-remediation, 26.4.25]

---

## BLOCK Enforcement (Day-One)

Chain-evaluator presence-check enforces 7a as a BLOCK at `c1-plan.md:88`, not a WARN. Day-one BLOCK status was a deliberate choice — premise-audit is the kind of step that gets skipped under delivery pressure, and the WARN→BLOCK promotion path (β+ calibration) doesn't apply here because the gate is structural rather than analytical. [B-r19-remediation, 26.4.25]

The BLOCK fires if Step 7a is missing or if PA[1-4] fields are unpopulated. It does not assess the quality of the audit — that's DA's role at C3 review.

---

## BUILD vs ANALYZE Split

CDS split the premise-audit definition for BUILD vs ANALYZE modes:
- **BUILD mode**: PA[1-4] focuses on shipped-code assumptions (what does the prompt assume the codebase looks like?).
- **ANALYZE mode**: PA[1-4] focuses on domain assumptions (what does the prompt assume about the subject matter?).

Both modes share the four-field structure and the Step 7a sequence position. [B-r19-remediation, 26.4.25]

[R-2026-04-28-shared-process-hardening, 26.5.2] **ANALYZE-side placement details**: In the shared-process-hardening build, the premise-audit pre-dispatch sub-step landed in `sigma-lead.md` Step 1 (lines ~38-72) and in `SKILL.md` Step 1 Prepare extension. The structure mirrors `c1-plan.md:62` Step 7a HARD GATE: PA[1-4] tier-necessity / firm-size-floor / data-readiness / adoption-baseline; sequence-constraint (PA before H-space re-read); PREMISE-AUDIT[pre-dispatch] workspace template; decision line REQUIRED (chain-evaluator §2p presence-check); CHALLENGED/GAP rules; DA r2 cross-check at Step 5 (ANALYZE numbering). The four PA[] domain-tier examples (tier-necessity, firm-size-floor, data-readiness, adoption-baseline) come from the AI-agent-rollout review and are illustrative — actual content is prompt-specific.

**Bounded grep-audit pattern (PM[8] mitigation)**: workflow-step renumbering breaks cross-refs. The shared-process-hardening build ran a pre+post grep-audit confirming "Step 7a" appears only in BUILD contexts (sigma-build/phases/c1-plan.md:62/137/138/174, build-directives.md:144/151) plus the deliberately bounded DC[3] cross-ref in directives.md. This is the canonical pattern: when a step-label is intentionally bounded to one mode, grep-audit pre-edit and post-edit, name the bounded set in the cross-ref, and treat any new occurrences outside the bounded set as drift to be resolved before merge.

---

## Self-Application Bootstrap Exception

A legitimate edge case surfaced in C1 of the R19 build: the plan that *introduced* premise-audit didn't itself run premise-audit (it can't — Step 7a doesn't exist yet at plan-introduction time). C1 audit YELLOW flagged this self-application gap; lead retroactively added the section.

DA[#10] challenged this as potential structural hypocrisy. Lead defended: this is a legitimate bootstrap exception, self-detected by C1 audit YELLOW (not silently overlooked), and closed before ship. The pattern is documented to prevent ambiguity in future builds: **for any new always-required step, document the bootstrap-build exception explicitly rather than retroactively closing without a record.** [B-r19-remediation, 26.4.25]

---

## Open Questions

- **Step 7a evidence quality bar** (synthesis-defer): chain-evaluator BLOCK enforces presence, not quality. DA assesses quality at C3 review. Question: is C3 too late to catch a shallow premise-audit that already framed C2 work? Possible mitigation: lead self-review at Step 7a exit before proceeding to Step 8. Deferred. [B-r19-remediation, 26.4.25]

## Contradictions

None.

## Sources

- B-r19-remediation synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md`
- R-2026-04-28-shared-process-hardening synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-synthesis.md`
