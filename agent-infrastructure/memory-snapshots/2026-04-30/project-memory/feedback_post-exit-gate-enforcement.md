---
name: Post-exit-gate mechanical enforcement
description: Orchestrator phases for promotion/sync/archive are mechanically enforced — synthesis must be separate agent, agents wait after convergence
type: feedback
---

Post-exit-gate phases (promotion, sync, archive) are now orchestrator-enforced phases, not prose directives.

**Why:** Lead skipped promotion round entirely during M&A deal terms review (26.3.28) because post-exit-gate steps were prose instructions that competed with task-completion pressure. Prose directives that rely on orchestrator discipline will always be vulnerable to being skipped. The failure wasn't ignorance — it was prioritization under pressure.

**How to apply:**
- orchestrator-config.py defines: synthesis → promotion → sync → archive → complete (terminal)
- is_terminal=true ONLY at "complete" — NOT at synthesis
- Lead calls `orchestrator advance` with completion flags after each phase
- Agents WAIT after convergence for promotion-round (5min timeout safety valve)
- Synthesis MUST be produced by a separate agent — lead writing synthesis = provenance contamination (lead has conversation context that agents were firewalled from)
- If synthesis agent fails: deliver RAW findings with explicit gap flag, do NOT silently write synthesis yourself
