---
name: check-reviewed-version-before-triage
description: Before triaging an external review or audit of a repo, verify which version it reviewed — diff local clone vs remote first
metadata:
  type: feedback
---
Before disposing of findings from an external review, audit, or plan written about a repo, establish which version the reviewer saw. Compare local HEAD to the remote and to any dated references in the document before judging a single finding.

**Why:** On 2026-09-05 the ai-pd-tracker audit described Track P, Phase 3, and a currency mechanism that did not exist in the local clone. They existed on remote main, 15 commits ahead. Without the check, every "already exists" claim would have been mis-scored as hallucination and the triage would have been against the wrong codebase.

**How to apply:** `git fetch` + `git log HEAD..origin/main --oneline` (or `gh api compare`) as the first step of any review-triage task. Read the remote versions of files the review cites. Say explicitly which commit the triage is against. Related: [[avoid-parallel-sessions]], [[check-repo-location]].
