---
name: F1 audit remediation
description: YELLOW audit on F1 build — 4 gaps (BELIEF tracking, build-track source tags, contamination check, XVERIFY skip). Remediation pattern for future builds.
type: feedback
---

F1 build (26.4.8) audit returned YELLOW with 4 targeted gaps. Build quality was strong (DA A-, 810 tests) but process documentation had holes.

**Why:** BELIEF[] is the most consistently missed protocol element across builds. Build-track agents produce strong evidence in prose but skip formal |source:{type} tags. XVERIFY available but not used. §6 contamination check skipped.

**How to apply:**
1. BELIEF[]: Must be written to workspace gate-log at EVERY phase transition. Not optional. Consider a simplified BUILD template: `BELIEF[{phase}-r{N}]: P={X} |{components} |DA={grade} |→ {action}`
2. Build-track source tags: DA §2d audit must cover ALL agents, not just plan-track. Add to DA spawn prompt: "audit source tags on build-track findings too"
3. CONTAMINATION-CHECK: Add to Phase 05 exit checklist as explicit step. BUILD mode has lower contamination risk but check is still required per §6.
4. XVERIFY: For security-critical ADRs (IP normalization, profile enforcement), run at least 1 cross-model verification. 13 providers were available and unused.
5. BUILD-specific §2d: [code-read] dominates BUILD source distribution (93%+). Focus audit on tagging compliance rather than distribution balance.
