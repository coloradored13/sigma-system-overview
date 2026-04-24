---
name: Skills architecture expansion
description: Plan to port Claude Chat marketplace skills to Claude Code; routing layer needed when count exceeds ~15; dual-use pattern (single-instance + team agents)
type: project
---

User plans to export/build skills from Claude Chat marketplace in bulk. Current state: 13 sigma-* skills, 0 general-purpose skills.

**Why:** Skills should work in two modes — single-instance (user + Claude) and team mode (sigma-review/sigma-build agents referencing skill knowledge). MCP builder skill is the template: SKILL.md = orchestration workflow, reference/ = domain knowledge anyone can read.

**How to apply:** Phase A installs phase-based sigma-review + DA lobotomy + MCP builder as first general skill. Phase B adds routing layer (ROUTER.md + domain INDEX files) once skill count warrants it (~15+). Install skills at ~/.claude/skills/{name}/ — flat structure works now, routing overlays later without moving files. When building sigma-review/sigma-build agent prompts, agents can read skill reference/ dirs directly for domain knowledge.
