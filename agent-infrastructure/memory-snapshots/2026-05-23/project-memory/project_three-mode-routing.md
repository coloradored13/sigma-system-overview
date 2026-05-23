---
name: three-mode routing (ANALYZE/BUILD/EXECUTE)
description: Insight that sigma system needs three modes not two — most review outputs are execution-ready, not build-worthy. Review should classify its own output.
type: project
---

Emerged 2026-03-25 from hateoas-agent review output discussion. User flagged the sigma-build prompt as "a laundry list" — well-specified tasks that don't need adversarial DA gates.

**Three modes:**
- **ANALYZE** (sigma-review): Don't know *what* to do. Multi-agent analysis, DA, convergence.
- **BUILD** (sigma-build): Know what, uncertain *how*. Adversarial implementation, checkpoints, DA on design decisions.
- **EXECUTE**: Know what + how. Parallel agents, test pass, done. No rounds, no DA needed.

**Why:** sigma-build earns its cost only when the *how* is uncertain (multiple valid architectures, tradeoffs needing adversarial testing, implementation generating new information). Most code-quality review outputs land in EXECUTE territory — README edits, logging changes, test stubs, lint fixes.

**How to apply:** sigma-review synthesis should classify each finding: "needs sigma-build" (design uncertainty) vs "execution-ready" (well-specified). The lead makes this call based on whether any item has design surface for DA to stress-test. This hasn't been implemented yet — proposed architecture only.

**Status:** Partially implemented (26.3.27). The PLAN layer was built INTO sigma-build as a two-phase dynamic model with cross-track review. Plan-track agents (tech-architect, product-designer, product-strategist) design in PHASE 1, challenged by DA + build-track for feasibility. Build-track agents (implementation-engineer, ui-ux-engineer, code-quality-analyst) implement in PHASE 2, reviewed by DA + plan-track for fidelity. Both phases iterate until Bayesian confidence (P>0.85), not fixed rounds. 11 hard gates enforce critical flow steps. EXECUTE mode remains proposed-only for future.
