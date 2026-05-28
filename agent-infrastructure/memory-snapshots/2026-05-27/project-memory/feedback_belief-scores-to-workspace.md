---
name: BELIEF scores must be written to workspace
description: Lead must write BELIEF[plan-rN] and BELIEF[build-rN] scores to workspace, not just report in conversation — confirmed systematic gap (2/2 audits)
type: feedback
---

BELIEF[] computation scores must be written to workspace ## gate-log section, not just reported in conversation.

**Why:** Two consecutive audits (5yr-PM-strategy 26.3.28, sigma-ui-build 26.3.29) found BELIEF[] scores absent from workspace despite being computed and reported to user. Workspace is the auditable record — conversation is ephemeral. Auditor cannot verify belief computation without workspace evidence.

**How to apply:** After every P(plan-ready) or P(build-quality) computation, lead writes to workspace ## gate-log:
```
BELIEF[{phase}-r{N}]: P={score} |components: {breakdown} |→ {lock|another-round|escalate}
```
This is a lead task, not an agent task. Enforce at every phase transition.
