---
name: asymmetric-eval-acceptance
description: When an assessor gates a competence or quality claim, require zero false-PASS on designated must_hold cases, not just aggregate agreement
metadata:
  type: feedback
---
Acceptance for any LLM assessor or judge that gates a claim ("competence demonstrated", "safe to ship") must be asymmetric: an aggregate agreement threshold AND zero false-PASS on a designated set of `must_hold` cases (shallow-but-fluent, dangerous misconception, upstream-system-wrongly-approved). False-HOLD rate is reported, not gating.

**Why:** User amendment 2026-09-05 on the ai-pd-tracker coach assessor: "a false HOLD is annoying; a false PASS corrupts the tracker's claim that competence was demonstrated." Aggregate-only acceptance is the same "94% accurate" anti-pattern the curriculum itself teaches against.

**How to apply:** Every gold set for a gating judge carries a `must_hold` flag on critical cases; the runner prints agreement, false-PASS-on-must_hold, and false-HOLD rate as three separate numbers; green requires the second to be zero. Related: [[xverify-is-cross-check-not-proof]], [[realistic-tests]].
