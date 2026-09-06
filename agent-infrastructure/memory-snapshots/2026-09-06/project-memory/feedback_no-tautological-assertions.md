---
name: no-tautological-assertions
description: Never ship a test assertion that cannot fail (e.g. `... or True`); if the expected value is uncertain, compute it from the same rule the code uses or assert a weaker real property
metadata:
  type: feedback
---
Do not write assertions that are permanently green — `assert x == y or True`, `assert True`, bare `assert result` on an always-truthy dict — as a way of hedging an expected value you have not worked out. Either derive the expected value from the same rule the code applies (and assert both sides of a cycle), or assert a weaker property that can actually fail.

**Why:** User correction 2026-09-05 on ai-pd-tracker: a spaced-review test I wrote ended an assertion with `or True` because I had not pinned down which objective the review cycle would serve. "A permanently-green assertion undermines the evidence quality the tracker is now designed to enforce." The fix took five lines: read the served objective from the queue, assert the mock received that lesson, that objective, and the submitted text, and assert the next cycle's objective too.

**How to apply:** Before committing tests, grep for `or True`, `assert True`, and `assert <name>` on non-boolean values. When a value depends on a modulus or seed, compute it in the test with the same formula and assert equality. Related: [[realistic-tests]], [[mock-tests-false-confidence]].
