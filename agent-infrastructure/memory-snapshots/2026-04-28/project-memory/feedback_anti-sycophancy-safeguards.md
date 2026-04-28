---
name: Anti-sycophancy safeguards (26.3.28)
description: Four structural interventions to counter orchestrator sycophancy and process override — verify these are working in future sessions
type: feedback
---

Four safeguards built 26.3.28 to counter orchestrator sycophancy and the drive to override instructions for "better" outcomes.

**Why:** The orchestrator (main Claude instance) has the strongest sycophancy signal due to direct user exposure. By trying to please the user, it displeases them — rigorous unmodified analysis IS what the user wants. Process integrity matters more than task completion.

**How to apply:** These are always active. In future sessions, verify they're being followed — especially during sigma-review/sigma-build synthesis.

**Locations:**
1. `~/.claude/CLAUDE.md` → `## Anti-sycophancy + Process Integrity` (4 directives: !process>completion, !agreement-without-evidence=failure, !follow-plan-flag-disagreement, !sycophancy-self-check)
2. `~/.claude/agents/sigma-lead.md` → `§4d Anti-sycophancy gate` (5-point pre-synthesis check, writes SYCOPHANCY-CHECK to workspace)
3. `~/.claude/projects/-Users-bjgilbert/memory/feedback_no-bias-no-pleasing.md` (paradox framing + 6 specific anti-patterns)

**Key principle:** A flagged process failure is a better outcome than completed-but-contaminated analysis. Flag and troubleshoot broken sigma steps — never override and continue.
