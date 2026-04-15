---
name: Hook enforcement architecture
description: Claude Code hooks as mechanical enforcement layer — 8 scripts, 8 hard BLOCKs (including default-deny code writes), 120 tests in phase-compliance-enforcer alone
type: project
originSessionId: 18c56ad6-98f6-42d1-8c53-4a32cc06daa6
---
Hook-based enforcement layer for sigma-review and sigma-build. 8 scripts in ~/.claude/hooks/ (symlinked to sigma-system-overview repo).

**Why:** Lead agent has documented, recurring pattern of skipping protocol gates under task pressure. Prose directives and phase file "mandatory" language fail because the lead can choose to ignore them. Hooks fire automatically on tool calls — the lead cannot opt out.

**How to apply:** Hooks are the involuntary enforcement layer. Directives document intent. Orchestrator manages state. Gate checks validate workspace content. Each layer catches what the others miss.

## 8 hard BLOCKs (PreToolUse exit code 2)
1. Phase skip — can't read phase files ahead of orchestrator checkpoint
2. DA exit-gate — can't advance from challenge/review without `exit-gate: PASS` in workspace
3. BELIEF on advance — can't advance from challenge/review/challenge_plan without BELIEF[] in workspace
4. CB evidence — can't advance from circuit_breaker without CB[]/divergence evidence
5. Lead synthesis write — can't write synthesis/report files during synthesis without synthesis-agent evidence
6. **Code write authorization (L1)** — default-deny: Write/Edit to code files blocked unless phase=build|fixes. Primary gate, not bypassable. (26.4.13)
7. Git commit gate (1b) — can't git commit/push before synthesis+promotion complete. (26.4.13)
8. SendMessage gate (1c) — soft: pattern-match on implementation dispatch during non-build phases. Early warning, not load-bearing. (26.4.13)

## Enforcement model (26.4.13)
Default-deny on code writes (L1) is the primary gate. Pattern-matching gates (1c) are soft defense-in-depth. This inverts the original model from "block bad actions" to "require positive authorization." Nothing happens until the orchestrator unlocks the phase's action set.

## Soft WARNs (PostToolUse/Stop systemMessage)
- BELIEF format (must be `BELIEF[P(x)=N.NN]`)
- Context firewall (personal context keywords in workspace)
- DA workspace delivery (via MCP monitor — DA storing to memory instead of workspace)
- sigma-verify unused (available but no verify_finding calls)
- MCP error recovery (2+ consecutive failures → pause suggestion)

## Infrastructure
hooks/ symlinked: ~/.claude/hooks → sigma-system-overview/agent-infrastructure/hooks (26.4.11)
settings.json: PreToolUse(Read|Bash|Write|Edit|SendMessage), PostToolUse(Write|Edit|Bash, SendMessage, Read, MCP tools), Stop
phase-compliance-enforcer.py: 120 tests (26.4.13)
checkpoint: /tmp/sigma-review-orchestrator.json (read by hooks to detect active session + current phase)
