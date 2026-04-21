---
name: Orchestrator BUILD mode — SUPERSEDED
description: orchestrator-config.py deleted 26.4.16 — BUILD uses 3-conversation phase files (c1-plan, c2-build, c3-review) with chain-evaluator enforcement
type: project
originSessionId: 76c5468f-a7a0-451e-b3c3-63637a10d184
---
SUPERSEDED 26.4.16: Orchestrator deleted in atomic checklist migration. BUILD workflow now operates via 3 conversation-scoped phase files, not orchestrator state machine.

**Current architecture:**
- C1 (c1-plan.md): planning, DA challenge, plan lock → produces plan file
- C2 (c2-build.md): pure execution against locked plan, checkpoints, tests
- C3 (c3-review.md): review, synthesis, promotion, archive

Enforcement via chain-evaluator.py (B1-B4 checks) + phase-gate.py (code write auth requires plan lock).

**History:** Original gap (26.4.12) was that BUILD mode never existed in orchestrator. Implemented 26.4.13 as 3 sub-workflows. Entire orchestrator deleted 26.4.16 when system moved to atomic checklist model.
