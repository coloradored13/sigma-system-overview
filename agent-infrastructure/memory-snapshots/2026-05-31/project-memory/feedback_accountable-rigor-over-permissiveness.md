---
name: Fix over-firing rules with accountability, not permissiveness
description: When a rigorous rule over-fires on edge cases, the fix is to require the system to defend each invocation — not to carve out exceptions. Rigor stays the default; edge cases self-correct.
type: feedback
originSessionId: c34a8540-25ae-4a1a-ad5f-a84fa133aa13
---
When a rigorous rule (e.g., "always demand X") generates false positives on edge cases, the instinct is to add an exception clause ("unless Y"). That reliably introduces false negatives — the system now under-fires on cases that actually needed the rule.

Better move: keep the rule rigorous, but require the system to *defend* each invocation. "Do X, AND be able to articulate specifically why this case calls for X."

**Why:** On ai-pd-tracker (26.4.20), the coach system prompt demanded project-grounded answers on every concept. User flagged: theoretical concepts (transformer math) have no work analog, so the coach would reject correct abstract answers. I proposed an exception clause ("skip grounding when the concept has no analog"). User rejected — that slope leads to pattern-matched answers slipping through on applied lessons where grounding IS needed, which was the original failure mode the whole check was supposed to catch. Their fix: keep the demand rigorous AND require the coach to be able to articulate *why* this specific concept has a real analog. If it can construct the justification, the demand stands. If it can't, the concept is theoretical and the coach pivots to other pushback. Same rigor, self-correcting on edges.

**How to apply:**

- When a rule seems too rigid, ask: "Could the edge case be resolved by requiring the rule to defend itself?" before adding an exception.
- Two failure modes to name explicitly in the rule: (a) reflexive unjustified invocation — blocks correct answers, (b) waving through — misses the thing the rule was there to catch. Framing both failure modes alongside the rule makes the standard legible and symmetric.
- Works best when the system can be challenged by the user (or another agent) to produce the justification on demand. The challengeability is what makes the rule self-correcting.
- General shape: "Do X. Before invoking X on a case, be able to articulate specifically why this case needs X. If you cannot construct that articulation, don't invoke X — pivot to Y instead. Do not soften X just because invocation is sometimes awkward."

Applies well beyond prompt engineering: code review rules, compliance checks, escalation policies, security gates — anywhere a blunt rule generates false positives and the instinct is to add exceptions.
