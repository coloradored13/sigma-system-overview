---
name: other-model-feedback-review-pattern
description: For non-trivial plans, the user routes drafts through "other model feedback" before approval. Match that cadence — accept honest critique, push back where the fix doesn't belong in the proposed layer.
type: feedback
originSessionId: 23e5861d-b4e3-43a6-99f1-f69f9b372243
---
When a plan involves new infrastructure with multiple integration points or hook interactions, the user runs the draft through cross-model review before approval. Match this cadence: deliver the draft, welcome the critique, integrate it rapidly with explicit accept/push-back framing.

**Why:** During the sigma-ralph plan (26.5.7), the user routed both draft rounds through "other model feedback" before ExitPlanMode approval. Each round caught material issues my self-review missed. Round 1 found: the verify_completion CLI flag would get used (footgun → replace with env var + .unverified-completion marker), missing max_cost_usd cap (cost was bounded by iter count not dollars), the test-strength gap in TDD-ralph (engineer writes both tests AND impl; weak-test/min-viable-impl can pass without solving problem), the engineer-judgment exploitable out-clause, and the strategic sequencing issue (build standalone first, gate engineer-ralph on measurement). Round 2 caught: single-incident gate sensitivity (one bad day shouldn't trigger infra changes), peer-verifier pencil-whipping risk (test-strength check becomes clicked-through), eyeballed-vs-mechanical analysis, the green-by-coincidence test edge case, and the missing decision-artifact requirement. None of these were caught by my own self-review.

**How to apply:** For planning sessions on non-trivial infra (multi-file builds, hook interactions, agent definitions, anything involving 3+ files or new exit conditions), proactively suggest routing the plan through cross-model review before ExitPlanMode. The user already does this — match cadence: deliver the draft plan, then welcome and rapidly integrate cross-model critique with explicit accept/push-back delineation.

**Anti-sycophancy boundary:** Push back honestly when the fix doesn't belong in the proposed layer. Examples from sigma-ralph:
- Reviewer suggested test-strength validation in ralph layer — push back: belongs in peer-verifier with IC-traceability, ralph stays simple
- Reviewer suggested resumption in v1 — push back: adds state-reconciliation complexity, defer to v2
- Both push-backs were structural, not tone-based, and the user accepted both

Accept-everything is sycophantic toward the reviewer; the goal is structurally correct, not maximum-agreement.
