---
name: Hook enforcement architecture
description: Claude Code hooks as mechanical enforcement layer for sigma-review/build protocol compliance — 8 scripts, 5 hard BLOCKs, 1242 tests
type: project
originSessionId: d7eadd85-5bd2-4be5-8e47-6169aa3c139b
---
Hook-based enforcement layer for sigma-review and sigma-build. 8 scripts in ~/.claude/hooks/ (symlinked to sigma-system-overview repo). 1,242 tests.

**Why:** Lead agent has documented, recurring pattern of skipping protocol gates under task pressure. Prose directives and phase file "mandatory" language fail because the lead can choose to ignore them. Hooks fire automatically on tool calls — the lead cannot opt out.

**How to apply:** Hooks are the involuntary enforcement layer. Directives document intent. Orchestrator manages state. Gate checks validate workspace content. Each layer catches what the others miss.

## 5 hard BLOCKs (PreToolUse exit code 2)
1. Phase skip — can't read phase files ahead of orchestrator checkpoint
2. DA exit-gate — can't advance from challenge/review without `exit-gate: PASS` in workspace
3. BELIEF on advance — can't advance from challenge/review/challenge_plan without BELIEF[] in workspace
4. CB evidence — can't advance from circuit_breaker without CB[]/divergence evidence
5. Lead synthesis write — can't write synthesis/report files during synthesis without synthesis-agent evidence

## Soft WARNs (PostToolUse/Stop systemMessage)
- BELIEF format (must be `BELIEF[P(x)=N.NN]`)
- Context firewall (personal context keywords in workspace)
- DA workspace delivery (via MCP monitor — DA storing to memory instead of workspace)
- sigma-verify unused (available but no verify_finding calls)
- MCP error recovery (2+ consecutive failures → pause suggestion)

## MCP compliance monitor
mcp-compliance-monitor.py fires on sigma-mem and sigma-verify MCP tool calls. Tracks DA workspace delivery, ΣComm format, sigma-verify availability/results, error patterns.

## Design principle
If a WARN can be ignored the same way a directive can be ignored, and the rule has no legitimate override, it must be a BLOCK. WARNs reserved for heuristic/edge-case-prone checks.

## Infrastructure
hooks/ symlinked: ~/.claude/hooks → sigma-system-overview/agent-infrastructure/hooks (26.4.11)
settings.json: PreToolUse(Read|Bash|Write|Edit), PostToolUse(Write|Edit|Bash, SendMessage, Read, MCP tools), Stop
state files: .phase-compliance-state.json, .mcp-compliance-state.json (gitignored)
checkpoint: /tmp/sigma-review-orchestrator.json (read by hooks to detect active session + current phase)

## Gate checks expanded
V27: promotion content, V28: sync evidence
PHASE_REQUIRED_VALIDATIONS now includes post-exit-gate phases (compilation, promotion, sync, archive)
