---
name: Plan-mode workflow for sigma-build consumption
description: User writes plans in plan-mode to feed into sigma-build separately, not for immediate ExitPlanMode approval. Don't reflexively push ExitPlanMode after plan amendments.
type: feedback
originSessionId: 14b9f828-d8d9-4ee2-bdf6-f613944b3cfc
---
Rule: When user writes a plan in plan-mode and says "save as plan", "plan saved for further review", "going to run it through sigma-build", "close the session", or asks "how do I exit plan mode?" — the plan file IS the deliverable. Do not call ExitPlanMode unless user explicitly says "ready to build," "approve plan," or equivalent.

**Why:** User's workflow separates plan-writing (iterative, multi-reviewer, often across days) from plan-execution (sigma-build spawn, adversarial build, tight scope). ExitPlanMode signals "approved for immediate execution" — the wrong commitment at the wrong time. Plans often sit for days, get scoped to subsets (e.g., M1a+M1b only), or get reviewed externally before sigma-build invocation. Forcing approval early contaminates the iteration cycle.

**How to apply:**
- After substantive plan amendments: acknowledge, stop, don't drive toward ExitPlanMode.
- On "save as plan" / "close the session" / "run through sigma-build" signals — plan-mode state preserved is the goal. The plan file is authoritative.
- Memory writes are blocked in plan-mode. When updates are needed: note them in a Session Handoff section inside the plan file, defer actual writes until post-exit. If the user wants writes before closing, they exit plan-mode themselves (Shift+Tab) and signal readiness.
- "How do I exit plan mode?" = user wants the mode exited to wrap up — not a request for me to call ExitPlanMode (which requires their approval anyway).
- When a plan contains a deferred-memory-writes list, remember to fulfill those writes once plan mode exits.

Observed 4x in a single session on `/Users/bjgilbert/.claude/plans/look-for-the-plan-snazzy-giraffe.md` (26.4.16 planning session → resumed through 26.4.20 close). Each ExitPlanMode call was rejected with a variant of "save as plan" / "plan saved for further review" / "save this plan so we can pick it up in another session."
