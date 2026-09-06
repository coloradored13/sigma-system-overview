---
name: fortna-agentic-ci
description: "Fortna competitive-intelligence + agentic-tech sigma-review, completed 26.8.31 — brief, wiki pages, 14 approved patterns, and the open infra items it surfaced"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3cb9f637-c1e8-4669-bee2-f56706c75c90
  modified: 2026-08-31T23:58:22.895Z
---

Sigma-review R-fortna-agentic-ci-2026-08-31 (TIER-2 ANALYZE, 4 rounds, exit-gate PASS, chain 24/24). Deliverable: standalone CI brief at `~/.claude/teams/sigma-review/shared/archive/2026-08-31-fortna-agentic-ci-synthesis.md` (5,886 words); wiki pages `fortna-competitive-position.md` + `warehouse-automation-agentic-ai-landscape.md`; full workspace archived alongside. Repo commits 8fbe958 + 5f92383, pushed.

Headline findings: Fortna's 2026-08-20 debt-for-equity recapitalization (Ares-led lender group, agreed-not-closed at review date) was missed by all 5 R1 agents and caught by the DA; warehouse-automation agentic adoption is at parity with general enterprise (~10%), no vertical tailwind; Fortna is at-par with Dematic and behind only Manhattan on shipped agentic; recommendation = clear the floor on agentic / differentiate on the provable (imitable, time-limited, not a moat), invest-don't-market internal work (sales/RFP first by payback speed), instrument bid debriefs now as an observation trigger. Open data gap: Fortna software-revenue share (two agents, unfindable).

**Open items this review left** (all approved or logged, none executed):
- Apply 6 user-approved protocol changes to files: directives.md §2 (entity-recency R1 sweep, concession-propagation, stale-read hygiene, anti-leniency protocol), devils-advocate.md (overcorrection-check standing duty), agent-defs §2h (sigma-verify venv workaround). Recorded in sigma-mem decisions.md `D[fortna-promotion-batch-protocol-changes]`.
- sigma-verify provider health: openai credits exhausted, google quota 0, deepseek-v3.2 retired in registry, nemotron/qwen cloud IDs 404 — venv workaround restores access ¬coverage; [[reference_api-budget-recovery]] applies.
- sigma-verify registration root cause CONFIRMED: spawn-time tool snapshot — lead must run init BEFORE spawning agents (failures.md).
- chain-evaluator A9 regex false-positive (prompt.claim.*%) — fix queued in failures.md.

Related: [[feedback_xverify-is-cross-check-not-proof]], [[feedback_api-budget-pause]], [[reference_sigma-review-benchmark-2026-05-17]]
