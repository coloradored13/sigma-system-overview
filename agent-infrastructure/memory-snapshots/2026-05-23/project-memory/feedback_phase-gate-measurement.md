---
name: phase-gate-measurement-pattern
description: When extending working infrastructure with new mechanism, build Phase 1 first, then Gate Phase 2 on a measured baseline rather than building both at once.
type: feedback
originSessionId: 23e5861d-b4e3-43a6-99f1-f69f9b372243
---
For extensions to working infrastructure (not greenfield): split into Phase 1 (low-risk, doesn't modify existing system) + Phase 2 (modifies existing system), then gate Phase 2 build on a measurement window that produces evidence the change is needed.

**Why:** Building both phases simultaneously assumes the second phase solves a problem you've measured. Often it doesn't — the existing flow already works fine. Sigma-build engineer-ralph (Phase 2 of sigma-ralph plan) was almost built without measuring engineer single-pass success rate first; the cross-model reviewer correctly flagged "is this solving a problem you've measured?" as the strongest critique. The framework that emerged: trigger conditions (rate thresholds + qualitative judgment, not single-incident sensitivity), mechanical analysis (script not eyeballing — manual rates rationalize whatever you were already leaning toward), decision artifact (date/data/reasoning, repo-stored not memory-only because future-you and collaborators can find it), null-result acceptance (measurement is itself the deliverable per feedback_research-framing.md 26.4.1).

**How to apply:** When the user proposes extensions to existing working systems, ask whether the underlying problem has been measured. If not, propose a Phase 1 (low-coupling, ships now) + Phase 2 (coupled, contingent) split with a measurable gate trigger and a fixed-duration measurement window (the sigma-ralph plan used two weeks). Document the trigger conditions explicitly so the decision is mechanical, not eyeballed-into-confirmation. Acceptable triggers combine quantitative thresholds (rate <X% over N samples) AND qualitative judgment (recurring pattern), with explicit "single incident is noise" guard. Establish a decision artifact path BEFORE the measurement starts — naming where it goes makes it easier to write later.

**Where it doesn't apply:** truly greenfield work (no existing system to measure against), or work where the cost of building Phase 2 is trivially small (under a few hours and zero coupling). Don't add Gate ceremony to one-shot operations.
