---
name: Hook enforcement architecture
description: Minimal hook enforcement — chain-evaluator (Stop) + phase-gate (2 BLOCKs + 1 WARN), 154 tests collected / 143 passing / 11 pre-existing failures (verified 26.4.24 R19-C2 CQA), non-looping
type: project
originSessionId: 76c5468f-a7a0-451e-b3c3-63637a10d184
---
Hook enforcement simplified from 8 scripts/8 BLOCKs to 2 scripts/2 BLOCKs (26.4.16).

**Why:** The 841-line phase-compliance-enforcer caused infinite loops when it fired in regular (non-sigma) conversations. It returned actionable "CHAIN INCOMPLETE: fix these items" messages that Claude tried to address, triggering the Stop hook again. The new model is: minimal hard blocks for irreversible actions, flat checklist evaluation for everything else.

**How to apply:** phase-gate.py fires on PreToolUse/PostToolUse. chain-evaluator.py fires on Stop. Both are scoped to active sigma sessions (workspace has ## task or ## mode). Regular conversations are unaffected.

## 2 hard BLOCKs (PreToolUse exit code 2)
1. **Code write authorization** — Write/Edit to code files blocked during BUILD sessions unless workspace contains plan-lock evidence (ADR[] + IC[]). Infrastructure paths always writable.
2. **Git commit gate** — git commit/push blocked during active sigma sessions unless chain-evaluator reports complete. Scoped via `_is_sigma_session()` — does NOT fire outside sigma sessions.

## 1 soft WARN (PostToolUse systemMessage)
3. **Context firewall** — warns when personal context keywords detected in workspace writes.

## Chain evaluator (Stop hook)
- Non-looping: returns informational `[chain-eval] N/M passed` message, never actionable demands
- Idempotent: skips re-evaluation if workspace hash unchanged since last eval
- Session-scoped: returns {} when workspace has no ## task/## mode markers

## Infrastructure
- hooks/ symlinked: ~/.claude/hooks → sigma-system-overview/agent-infrastructure/hooks
- settings.json: PreToolUse(Write|Edit|Bash → phase-gate), PostToolUse(Write|Edit → phase-gate), Stop(sigma-retrospective + chain-evaluator)
- LIVE TEST COUNT (verified 26.4.24 during R19 remediation C2 CQA PF[1] reconciliation): 154 collected, 143 passing, 11 pre-existing failures
  - test_chain_evaluator.py + test_phase_gate.py + test_gate_checks.py: 3-file canonical set, all present at hooks/tests/ + shared/
  - 11 failures all in test_gate_checks.py — trace to MINIMAL_WORKSPACE fixture using agent-alpha/agent-beta not in roster.md (broken since roster.md was added 26.4.11); fix = SQ[0] in R19-C2 build
  - test_hooks.py (~/.claude/hooks/): 24 tests, all passing
- CORRECTION 26.4.24: earlier claim "test_chain_evaluator.py + test_phase_gate.py lost in refactor" was FALSIFIED. Consolidation commits ea5ae97+d9d21ad MOVED these files, did not delete them. Earlier "92 tests" count was a measurement error (scoped to test_gate_checks.py alone and miscounted).
