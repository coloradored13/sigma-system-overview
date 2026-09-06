---
name: sigma-review invocation requires explicit triage
description: When /sigma-review is invoked, lead MUST run triage (§3c) or explicitly acknowledge the invocation and explain why it's being skipped — never silently pivot to direct implementation
type: feedback
---

When /sigma-review is invoked, lead MUST either execute the protocol (pre-flight → triage → route) or explicitly tell the user "this doesn't meet sigma-review criteria, proceeding as [alternative]." Never silently ignore the invocation and jump straight into implementation.

**Why:** Session 26.3.22 — user invoked /sigma-review for a technical implementation task (adding cross-model verification). Lead asked clarifying question, user described the task, lead jumped directly into implementation without running §3c triage or acknowledging the skill invocation. The task would have failed all three triage conditions (stakes, herding, calibration) and should have been explicitly routed as a regular implementation task. Process was skipped, not deliberately triaged.

**How to apply:** On any /sigma-review invocation: (1) run §3c triage gate, (2) if fail-any → tell user explicitly "TRIAGE: this routes to [single-instance/direct-implementation] because [reasons]" and get confirmation, (3) only then proceed. The acknowledgment is the key part — silent pivots leave the user uncertain about whether the protocol was engaged.
