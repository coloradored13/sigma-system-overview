---
name: xverify-is-cross-check-not-proof
description: "sigma-verify (LLM-checking-LLM) is a cross-check / sanity check, NOT primary verification. Agents and DA must do primary research; XVERIFY supplements but doesn't replace it."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 305e4969-de1b-47c1-aa27-243897d424a1
---

LLM cross-model verification (sigma-verify, XVERIFY) is an ouroboros — one inference engine confirming another inference engine confirms nothing independent. Treat it as a SANITY CHECK that catches model-specific hallucination or confident-wrong outputs, not as PROOF that a claim is correct.

**Why:** User flagged during /sigma-review la-org-proposal session 26.5.27: "An LLM just checking with another LLM is a bit of an ouroboros. Sanity checks are fine, considering the other models as proof isn't." The session surfaced this because DA initially treated sigma-verify XVERIFY as their primary counter-evidence mechanism, only doing WebSearch + WebFetch after explicit prompting. The same gap exists in the agent-def template: r2 "research NOW" was interpretable as XVERIFY-only.

**How to apply:**

1. **Agent R1 protocol:** Primary verification path is web research + primary-source citation (vendor sites, press releases, regulatory filings, peer-reviewed work, named industry analysts with attribution). XVERIFY is a supplemental check applied AFTER primary research is done — it catches "did I hallucinate this" not "is this true."

2. **DA r2 protocol:** Counter-evidence MUST be primary (web research first, sigma-verify second). When briefing DA, explicitly authorize WebSearch + WebFetch alongside sigma-verify; the agent-def's "research NOW" language is ambiguous and reads as XVERIFY-only by default.

3. **Quality-tier assignment:** T1-verified should require ≥1 primary external source (web citation, regulatory filing, primary doc). XVERIFY agreement alone is NOT sufficient to tier a finding T1. Pattern: T1 = primary-source + (optional) XVERIFY-confirm; T2 = primary-source-thin OR XVERIFY-only on agent-generated claim; T3 = neither.

4. **Exit-gate criteria revision (for future agent-def update):** §2h cross-model verification integrity check should distinguish (a) XVERIFY-attempted-and-failed-due-to-infrastructure (acceptable if primary sources compensate) from (b) XVERIFY-as-primary-evidence-for-load-bearing-claim (process violation — primary research missing).

5. **DA spawn prompt fix:** Explicitly say "research = WebSearch + WebFetch + sigma-verify, in that priority order. sigma-verify is a cross-check on primary findings, not a substitute for them."

6. **Lead behavior:** When agents return XVERIFY-FAIL due to API/registry issues, distinguish "no primary research either" (process violation, route back) from "primary research is solid, XVERIFY couldn't supplement" (acceptable per §2h outcome 2, with T2 tier flag).

Related: [[feedback_mock-tests-false-confidence]] (similar pattern — synthetic verification ≠ real verification), [[reference_subscription-vs-pertoken]] (XVERIFY costs apply at per-token; primary research is "free" within subscription).

**Concrete forward-fix list:**
- Update `~/.claude/agents/devils-advocate.md` r2 protocol to say "research = primary (web/source) first, sigma-verify as cross-check on primary findings, not substitute"
- Update agent-def templates' R1 sequence step 6 (XVERIFY) to require step 1 (primary research) to be complete first
- Update spawn-prompt templates to include explicit primary-vs-XVERIFY hierarchy
- Update §2d+ quality-tier rules to make T1 contingent on primary-source presence
- Update directives.md §2h XVERIFY integrity check to reflect the new hierarchy
