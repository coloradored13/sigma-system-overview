---
name: transfer-test-not-cold-if-committed
description: A cold-context or transfer test whose content is committed to a repo the learner owns is not cold — commit only rubric and authoring spec, author the instance just-in-time from a session the learner does not read
metadata:
  type: feedback
---
Sealed assessments (cold cases, gauntlet artifacts) must not be committed to a repository the assessed person owns, diffs, or reviews — hiding the text in a prompt field is not sealing. Commit the slot, rubric, and an authoring spec; generate the instance shortly before use into a gitignored path from a separate session; instruct that session to write the file and not echo or summarize the content in its visible response.

**Why:** User amendment 2026-09-05: "the learner owns and reviews the repo and may see it in source or diffs"; and the follow-up: "the seal can be defeated by the agent helpfully printing the assessment after generating it." Transfer testing was the one genuinely new measurement surface in the plan, so its integrity mattered more than convenience.

**How to apply:** Verification has three parts: committed source contains no instance; runtime includes the instance only when the local file exists; the authoring transcript contains path and difficulty anchor but no body. Related: [[asymmetric-eval-acceptance]].
