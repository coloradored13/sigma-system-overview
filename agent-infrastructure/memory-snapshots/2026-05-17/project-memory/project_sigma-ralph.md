---
name: sigma-ralph
description: Local Apache-2.0 Python primitive implementing Ralph Loop pattern via SDK-direct (sidesteps chain-evaluator Stop hook). Phase 1 of two-phase plan; Phase 2 (engineer-ralph) Gate-contingent.
type: project
originSessionId: 23e5861d-b4e3-43a6-99f1-f69f9b372243
---
~/Projects/sigma-ralph/ — created 2026-05-07. Single-file Python module + Click CLI wrapping a fresh-context iteration loop with multi-provider sigma-verify completion check.

**Architecture:** Calls anthropic SDK directly per iteration; never enters Claude Code session. chain-evaluator and phase-gate hooks do not fire during a sigma-ralph run. This is the deliberate sidestep of the official `claude-plugins-official/plugins/ralph-loop` plugin's Stop-hook collision with chain-evaluator.py.

**Bounded exits (terminated_by):**
- `sentinel_verified` — sentinel emitted + sigma-verify cross-model agreement
- `sentinel_unverified` — sentinel + env opt-out via SIGMA_RALPH_SKIP_VERIFY=1, writes `.unverified-completion` marker
- `max_iter`, `max_cost_usd`, `no_progress` (Jaccard >0.95 over 3 iters), `error`

**Observability:** workspace/.ralph.jsonl with prompt_hash, response, sentinel_seen, test_exit, cost_usd, files_changed_jaccard_vs_prev, context_tokens_in/out per iteration.

**Phase 2 gate:** ~/.claude/teams/sigma-review/shared/c2-baseline.md (committed in sigma-system-overview) tracks engineer single-pass success rate across c2-builds. Trigger conditions: clean rate <70% over 5+ builds, OR test-gap ≥30% of fix-causes, OR ≥2 incidents (or 1+pattern). Mechanical analysis: scripts/analyze_c2_baseline.py. Gate decision artifact: phase-2-gate-decision.md (write at end of two-week window).

**Plan:** ~/.claude/plans/glowing-hugging-wilkinson.md (approved 26.5.7, 4 review rounds: original draft + 2 cross-model critiques + final).

**Status 26.5.7:**
- v0.1.0 committed locally (0559289), 16/16 tests pass, pip install -e in venv works
- Hook-regression confirmed (1305 pass / 14 skip in agent-infrastructure/hooks)
- Local-only, no remote (per plan: "not pushed initially — local only until validated")
- End-to-end real-API test deferred to user invocation
- Two-week measurement window for Phase 2 Gate begins on first c2-build session

**Files:**
- `ralph.py` (~250 LOC): ralph() function + Click CLI; bounded exits, JSONL log, sigma-verify integration with anthropic-exclusion default
- `test_ralph.py` (16 tests): every terminated_by exit path covered with mocked clients
- `scripts/analyze_c2_baseline.py` (~80 LOC): parses BUILD[] lines, prints rates + GATE: TRIPPED|NOT TRIPPED
- `README.md`: Pomodoro worked example + Anthropic-exclusion note + chain-evaluator caveat
