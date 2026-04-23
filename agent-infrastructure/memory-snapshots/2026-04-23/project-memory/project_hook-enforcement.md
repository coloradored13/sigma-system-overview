---
name: Hook enforcement architecture
description: Minimal hook enforcement — chain-evaluator (Stop) + phase-gate (2 BLOCKs + 1 WARN), 92 tests live (was 154 claim — test files lost in refactor), 11 pre-existing failures, non-looping
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
- LIVE TEST COUNT (verified 26.4.23 during R19 remediation C1): 92 tests, 81 passing, 11 failing
  - test_gate_checks.py: 68 tests (57 passing, 11 failing — MINIMAL_WORKSPACE fixture uses agent-alpha/agent-beta not in roster.md, broken since roster.md was added)
  - test_hooks.py (~/.claude/hooks/): 24 tests, all passing
- WAS 154 (per 26.4.16 entry): test_chain_evaluator.py(41) + test_phase_gate.py(45) + test_gate_checks.py(68) — test_chain_evaluator.py and test_phase_gate.py NO LONGER EXIST. Lost in unknown refactor between 26.4.16 and 26.4.23. Investigate before claiming chain-evaluator/phase-gate are tested.
