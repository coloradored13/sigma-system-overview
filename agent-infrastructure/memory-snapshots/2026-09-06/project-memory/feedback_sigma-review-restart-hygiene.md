---
name: feedback-sigma-review-restart-hygiene
description: "On /sigma-review with active unfinished workspace, FULLY wipe state before any framing investigation — do not surface prior session's hypotheses, scope, or premise-audit back to user as resume options"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c01929bd-9422-4802-a88b-4070be2b8d39
---

When `/sigma-review` is invoked and the workspace already contains an active unfinished session, the lead must FULLY wipe state BEFORE doing detailed investigation of the prior content, and must NOT surface the prior session's framing (hypotheses, scope, decomposition, premise-audit) back to the user as resume options.

**Why:** Even reading the prior workspace and presenting it back to the user as a "resume vs. restart" question anchors both the lead AND the user on the prior framing. That contamination is the exact failure §2p premise-audit is designed to prevent — premise-audit must be answered from the user's RAW prompt alone, not from any prior session's hypotheses. The user made this explicit on 2026-05-21: "start a new session where you didn't see anything first." A "did the prior session find anything?" preview is itself an anchoring vector.

**How to apply:**
1. On `/sigma-review` invocation, check workspace + `.chain-status.json` for active unfinished state.
2. If unfinished state detected, ask user `resume / restart / abandon` using NEUTRAL labels only — do NOT show prior topic, hypotheses, agents-spawned, or findings preview.
3. On `restart` or `abandon`: perform full wipe BEFORE Step 1 — workspace → idle stub, `.chain-status.json` removed, `git checkout --` any uncommitted shared/agent-memory writes that were promoted before the chain reached A13.
4. After wipe, END the current session and instruct user to start a fresh Claude session — the lead's prompt context is itself contaminated by having seen the prior workspace contents. A new session's lead has zero prior-framing exposure.
5. Save the abort to an `ABORTED.md` archive only with explicit user approval — default-deny on archiving aborted state, because the BLOCK-5 compilation-complete gate exists for the same anti-contamination reason.

**Anti-pattern (what happened 2026-05-21):** Lead read aborted workspace, summarized its hypotheses and agent findings in the resume question, then attempted Step 1 premise-audit "from raw prompt only" — user correctly identified this as still contaminated and demanded full wipe + new session.

Related: [[feedback_avoid-parallel-sessions]] (don't run concurrent), [[feedback_process-over-momentum]] (process integrity > preserving work), [[feedback_lead-role-boundary]] (lead absorbs vs. coordinates).
