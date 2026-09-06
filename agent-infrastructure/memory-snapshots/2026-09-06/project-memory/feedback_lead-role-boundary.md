---
name: Lead role boundary — no analytical work
description: Lead/orchestrator must not call XVERIFY, write synthesis, or absorb agent work — flag gaps instead of filling them
type: feedback
---

Lead must not call analytical tools (XVERIFY, challenge, verify_finding) or write synthesis content. These are agent responsibilities.

**Why:** When lead absorbs work that should be independent agent verification, the output *looks* like multi-agent analysis with cross-model checks but is actually single-agent self-verification. The user presents this as rigorous independent analysis. Misrepresentation of analytical provenance causes downstream trust miscalibration. The user's analogy: "If I go into a meeting and say 'look at what my agents found' and it's just fake/single agent" — this can cause real harm. Being agreeable and completing is pulling the trigger, not avoiding it.

**How to apply:**
- Agents run XVERIFY in their Work sequence (step 2→VERIFY in spawn template)
- DA uses challenge() during R2 to stress-test claims
- If synthesis agent fails to spawn: deliver raw agent findings with explicit gap flag, do NOT write synthesis yourself
- Lead may organize/format but must not add conclusions, estimates, or judgments
- Flag gaps honestly rather than filling them — an incomplete honest output is safer than a polished compromised one
- Do not shut down agents until all post-round work is complete

Correction logged: 26.3.28, from M&A deal terms review where lead ran XVERIFY and wrote synthesis directly.
