---
name: DA must deliver BUILD findings to workspace not just memory
description: DA §4a-§4d findings go to workspace sections, not agent memory — BUILD exit-gate template needed in build-directives.md
type: feedback
---

DA exercised §4a (scope compliance) and §4d (test integrity) during sigma-ui build review but delivered findings to agent memory rather than workspace. Workspace has no record of DA's BUILD guardrail assessments.

**Why:** No BUILD-specific exit-gate template exists in build-directives.md. ANALYZE mode has a clear exit-gate format (directives.md). DA defaulted to memory because workspace had no designated section for BUILD exit-gate. Audit cannot verify DA engagement without workspace evidence.

**How to apply:**
1. Add BUILD exit-gate template to build-directives.md specifying workspace format for DA verdict + §4a-§4d assessments
2. Lead must verify DA writes exit-gate to workspace (not just messages it to lead) before advancing past build review
3. §2f (hypothesis matrix) and §2g (dialectical bootstrapping) need BUILD-specific guidance — §2f designed for competing hypotheses may not apply to viability questions; §2g should specify minimum DB[] count per agent
