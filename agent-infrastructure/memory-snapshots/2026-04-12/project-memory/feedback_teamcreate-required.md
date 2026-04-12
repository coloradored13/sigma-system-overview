---
name: TeamCreate required for sigma-review
description: sigma-review agents MUST be spawned via TeamCreate, never isolated Agent calls — inter-agent communication is the core value
type: feedback
---

sigma-review agents MUST be spawned via TeamCreate, never as isolated Agent tool calls.

**Why:** The whole point of sigma-review is that agents are NOT in isolated contexts. They need to SendMessage to each other, read peer workspace sections in real-time, and interact. Isolated Agent spawns break inter-agent communication which is the core value of the multi-agent review. User corrected this on 26.3.28 — first time this error occurred.

**How to apply:** When orchestrating sigma-review (or sigma-build), always use TeamCreate to establish the team, then spawn agents into that team context. Never use bare Agent tool calls for team members.
