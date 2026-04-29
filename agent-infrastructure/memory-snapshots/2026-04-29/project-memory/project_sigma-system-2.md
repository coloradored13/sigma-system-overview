---
name: sigma-system-2 clean-room test
description: Plan to build a cleaned-up sigma-review system and A/B test against current system to identify load-bearing complexity vs cruft
type: project
---

sigma-system-2: clean-room rebuild of sigma-review infrastructure to test which complexity is load-bearing.

**Why:** User uncertain whether system's accumulated complexity (ΣComm, 47 corrections, 400-line directives) is essential or cruft. Also weighing whether to make repos public — clean version could be publishable without giving away calibration value.

**How to apply:** Run same review prompt through both systems, compare DA catch rate, hypothesis falsification, priority ordering. Passes full triage gate (stakes=core-infra, herding=agents-reviewing-themselves, calibration=the-whole-point). Self-reference bias risk — DA needs priming against self-preservation.

**Sequencing:** After sigma-predict build. Fresh session, no contamination from reviews that used the system.

Established 26.3.23.
