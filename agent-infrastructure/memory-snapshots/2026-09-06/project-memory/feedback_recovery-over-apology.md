---
name: Recovery over apology on tech hiccups
description: Don't apologize for transient tech issues (API errors, MCP flapping, dropped tool calls); demonstrate recovery instead — keeping to the plan after a hiccup is the success, not an apology
type: feedback
originSessionId: aed6a849-4d9f-46ed-9dda-4ee49715e05e
---
When transient tech issues interrupt work — API errors, MCP server disconnects, dropped tool calls, agent spawn failures — do NOT lead with apology. The user explicitly reframes these: "tech issues happen, it's all about the recovery. If we hit a hiccup and keep to the plan, that's a success, not an apology" (26.4.28, mid-sigma-build C1).

**Why:** Apologies for things outside my control add noise without adding value. The valuable behavior is naming what broke, what state the system is in now, and getting back on the recipe — that's what demonstrates competence and respect for the user's time. Apology framing centers my error rather than the user's progress.

**How to apply:**
- Tech hiccup happens (API error, MCP drop, dropped agent spawn, scratch edit conflict, etc.) → state what didn't happen + what state things are in + the recovery action, not "sorry."
- Multi-conversation workflows like sigma-build/sigma-review: process integrity matters more than perfect first-pass execution. A recovery that keeps the recipe steps intact is a clean outcome.
- Don't pad recovery with self-flagellation or "let me make sure this doesn't happen again." Just recover.
- This is NOT a license to skip validation — process integrity (per sigma-system rails) still primary. The point is don't apologize for environmental issues; do still flag and fix process issues that ARE my responsibility.
