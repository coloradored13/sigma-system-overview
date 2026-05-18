---
name: Exp 2 process audit
description: Process failures and operational lessons from sigma-optimize Exp 2 (26.4.2-26.4.3) — 10 process violations, 15 new findings
type: feedback
---

## Process failures (framework violated its own rules)

1. **Lead ran experiments (§1 violation)** — agents couldn't hold long processes, lead executed via nohup. User authorized override. Mitigated (didn't analyze raw data) but provenance chain broken.
2. **Agents failed on long-running experiments** — Bash 10-min timeout, rate limit collisions, agent context overhead. Root cause of §1 override.
3. **Search agents spawned/killed multiple times** — "clean spawn with context firewall" model broke down. Agents saw partial state from prior attempts.
4. **Wrong parameters (N=3 instead of N=10)** — conservative ran at reduced scale as compromise. Three different conservative datasets existed at various points.
5. **Lead interpreted patterns mid-experiment** — user caught it. Risk: interpretations leaking into agent instructions.
6. **$15 burned on garbage data** — combinatorial ran without budget guard, 84% of scores were -5 errors.
7. **Cross-agent independence untested** — lead ran both searches, independence enforcement didn't apply.
8. **Promotion round incomplete** — sigma-mem store tools unavailable to agents.
9. **Orchestrator state diverged** — phase transitions manually forced, not triggered by convergence.
10. **§4b spawn template not followed** — later agents got custom prompts instead of standardized template.

**Why:** The harness wasn't designed for agent execution constraints (Bash timeout, shared rate limits, budget exhaustion). Concurrent eval + checkpointing (built mid-session) would have prevented most failures.

**How to apply:** Before running any sigma-optimize experiment, verify: (1) concurrent eval is in harness, (2) checkpointing works, (3) budget guard is active, (4) per-provider saves enabled. See reference_experiment-execution-pattern.md for the proven pattern. With these in place, TeamCreate agents should work — each gen fits in ~3 min, well within Bash timeout.
