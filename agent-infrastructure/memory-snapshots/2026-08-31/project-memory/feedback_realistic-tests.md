---
name: Realistic test scenarios
description: Tests must model real usage patterns, not flip flags to pass — every config choice should represent a real use case
type: feedback
---

Tests should model real scenarios, not force flag flips just to make them pass. Passing tests shouldn't just be for passing sake — they should pass because they cover real situations.

**Why:** User corrected a proposal to add `require_first_run_approval=False` to existing test configs just to avoid dealing with the new default. That would make tests pass without actually testing realistic behavior.

**How to apply:** When a behavior change breaks existing tests, fix them by modeling the real scenario they represent:
- "Returning user with known tools" → pre-populate the approval registry with hashes
- "New user, interactive first run" → set an approval callback
- "New user, convenience mode" → use `auto_approve_first_seen=True`
- "New user, no callback" → test the fail-safe pending state

Every config value in a test should answer "what real user scenario does this represent?" If the answer is "none, it just makes the test pass," the test is wrong.
