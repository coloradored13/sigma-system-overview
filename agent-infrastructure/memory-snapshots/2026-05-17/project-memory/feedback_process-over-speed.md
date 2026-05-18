---
name: Process over speed — gate audit mandate
description: User explicitly requires full process adherence over speed; failed gates must be documented not hand-waved; identifying unenforced gates is as important as review findings
type: feedback
originSessionId: 2dc0cf3e-be23-40dd-99e3-a6eb59a22de8
---
When orchestrator gates fail (bugs, regex mismatches, broken commands), do NOT skip past them. Run every gate command, log the exact result, document whether the failure is substance or tooling, and maintain a running gate enforcement audit table.

**Why:** User values process integrity as the primary output. A review that identifies broken gates is more valuable than a polished review that silently bypassed them. The gate infrastructure exists to prevent specific past failures — unenforced gates mean those failures can recur undetected.

**How to apply:**
- Attempt every orchestrator command specified in phase files, even if you expect it to fail
- A failed validation is a failed validation — don't reclassify as "format issue" to proceed
- Maintain a gate enforcement audit table through the entire review
- Document: gate name, expected behavior, actual behavior, root cause, severity
- Process over speed is the explicit user preference — never optimize for completion time at the expense of step execution
