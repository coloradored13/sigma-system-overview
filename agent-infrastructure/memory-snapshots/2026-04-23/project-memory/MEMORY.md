# sigma-system-overview — project-scoped memory
# project state lives in global ^projects.md — don't duplicate here

- [Prompt Coach](prompt-coach-project.md) — local webapp, scaffolded 26.3.6, paused → evolved into Spec Workshop
- [Spec Workshop](project_spec-workshop.md) — Streamlit spec-writing tool with Claude API, v1 spec drafted 26.3.29
- [AI PD Tracker](project_ai-pd-tracker.md) — ~/Projects/ai-pd-tracker/ FastAPI+SQLite curriculum tracker, ALL 10 STEPS SHIPPED 26.4.20, private repo coloradored13/ai-pd-tracker, coach validated (shares sigma-verify API key)
- [Loan Admin KB](project_loan-admin-kb.md) — 6-doc review, complete 26.3.13
- [Rosetta](rosetta.md) — ΣComm notation decoder (canonical version now in sigma-mem/docs/notation-reference.md)
- [Dream Consolidation](project_dream-consolidation.md) — BUILT 26.3.29: dream.py 846 LOC, 76 tests, MCP registered, end-to-end verified

## sigma-ui
- [sigma-ui](project_sigma-ui.md) — Phase B3 COMPLETE (26.3.31): 16 modules, 280 tests, E2E integration, pushed. Repo: ~/Projects/sigma-ui/

## sigma-optimize
- [sigma-optimize](project_sigma-optimize.md) — Exp 1-2 COMPLETE, A2-follow + A3 COMPLETE, Exp 3 DESIGNED (convergence probe)
- [Exp 3 convergence probe](project_exp3-convergence.md) — cross-model/architecture convergence, ready to scope (Exp 2 dependency resolved)
- [sigma-verify providers](project_sigma-verify-providers.md) — 13 providers: 4 local + 6 Ollama cloud Pro + 2 per-token + 1 optional, expanded 26.4.5

## gate infrastructure
- [Gate infrastructure](project_gate-infrastructure.md) — atomic checklist model: chain-evaluator (A1-A19 + B1-B4) + phase-gate (2 hard blocks + 1 warn), replaces orchestrator + 841-line enforcer (26.4.16)
- [Orchestrator BUILD mode](project_orchestrator-build-mode.md) — SUPERSEDED 26.4.16: orchestrator deleted, BUILD uses 3-conversation phase files (c1-plan, c2-build, c3-review)
- [Sigma-Review Infrastructure Issues (R19 post-mortem)](project_sigma-review-infrastructure-issues.md) — 25 issues from R19 session 26.4.22 (GREEN audit / B 3.14 eval). Top infrastructure: #3 ΣVerify agent-context, #1 sed -i ban, #4+#20 A12 parser+timing, #19 A3 DB-step parser. Top protocol (NEW from evaluator): #21 premise-audit-pre-dispatch, #22 precision-gate, #23 governance-min-artifact. Validated patterns: §8e recovery template, DA not-discussed probe, DA XVERIFY severity calibrator. 2 pending global promotions (RA UP-B/UP-C) + MITRE ATLAS citation fix in workspace archive.

## sigma-system-2
- [Clean-room rebuild](project_sigma-system-2.md) — A/B test, sequenced after sigma-predict build (26.3.23)
- [Three-mode routing](project_three-mode-routing.md) — ANALYZE/BUILD/EXECUTE distinction, review classifies own output (26.3.25)

## multi-model agents
- [Multi-model agent vision](project_multi-model-agents.md) — any model fills any agent role; ΣComm distribution > definition; spawn infra is bottleneck (26.4.8)

## chatroom + ollama-mcp-bridge
- [Multi-model chatroom + MCP bridge](project_chatroom.md) — Bridge B6 complete (816 tests). Chatroom PLANNED 26.4.16 (plan: look-for-the-plan-snazzy-giraffe.md), scoped sigma-build M1a+M1b recommended after prior C1 attempt failed.
- [ΣComm translator](project_sigmacomm-translator.md) — DESIGNED in F1, DEFERRED pending empirical validation (DA[1] challenge 26.4.8). ADR[2] locked in archive.
- [F1 build patterns](project_f1-build-patterns.md) — 6 patterns promoted: IP normalization, HARDENED enforcement, empirical gates, multi-agent convergence, parallel engineers (26.4.8)

## kaggle competition
kaggle-measuring-agi in ^projects.md | briefing: ~/Projects/kaggle-measuring-agi/COMPETITION-BRIEFING.md
DeepMind hackathon, $200K, cognitive benchmarks, deadline 26.4.16, status: review-complete→build-started

## skills + hooks
- [Skills integration v3](project_skills-integration-v3.md) — 42 skills installed, native Claude Code routing, opt-in skill access for agents during Work phase (26.4.15)
- [Hook enforcement](project_hook-enforcement.md) — chain-evaluator.py (Stop hook, non-looping) + phase-gate.py (2 BLOCKs: code-write-auth + git-commit-gate, 1 WARN: context-firewall), 154 tests (26.4.16)
- [Skills architecture expansion](project_skills-architecture.md) — dual-use skills (single-instance + team), marketplace port planned, routing at ~15+ skills (26.4.8)

## repos
coloradored13/{hateoas-agent(public),sigma-mem(public),ollama-mcp-bridge(public),sigma-verify,sigma-system-overview,sigma-predict(private)}
!public-release 26.4.4-5: hateoas-agent+sigma-mem → Apache 2.0, READMEs reconciled, ΣComm docs standalone, notation-reference added, security audit(7 fixes: path traversal, context injection, param filter), 2 independent code reviews addressed, core-concepts/gateway/orchestrator/MCP documentation added
!apache-2.0 expansion 26.4.7: LICENSE added to Daycare, recharge, sigma-system-overview, sigma-ui, sigma-verify, thriveapp (all repos now Apache 2.0 except Updraft+Project 1 which have no remote)

## corrections
- [Triage gate](feedback_sigma-review-triage.md) — /sigma-review must run triage or explicitly acknowledge skip (26.3.22)
- [Actionable over hype](feedback_actionable-over-hype.md) — synthesis leads with buildable detail, not strategy pitch (26.3.22)
- [Lead role boundary](feedback_lead-role-boundary.md) — lead must not call XVERIFY or write synthesis; flag gaps instead of absorbing work (26.3.28)
- [No bias, no pleasing](feedback_no-bias-no-pleasing.md) — raw analysis only, process integrity > task completion, specific anti-patterns listed (26.3.28)
- [Anti-sycophancy safeguards](feedback_anti-sycophancy-safeguards.md) — 4 structural interventions across CLAUDE.md, sigma-lead §4d, feedback memory (26.3.28)
- [Post-exit-gate enforcement](feedback_post-exit-gate-enforcement.md) — promotion/sync/archive are orchestrator phases not prose; synthesis=separate agent; agents WAIT after convergence (26.3.28)
- [TeamCreate required](feedback_teamcreate-required.md) — sigma-review agents MUST use TeamCreate, never isolated Agent calls (26.3.28)
- [Synthesis file gate](feedback_synthesis-file-gate.md) — lead must write synthesis to file before setting synthesis_delivered, not just relay in conversation (26.3.28)
- [BELIEF to workspace](feedback_belief-scores-to-workspace.md) — lead must write BELIEF[] scores to workspace gate-log, not just conversation (systematic: 2/2 audits, 26.3.29)
- [DA workspace delivery](feedback_da-workspace-delivery.md) — DA BUILD findings go to workspace not just memory; BUILD exit-gate template needed (26.3.29)
- [Research framing](feedback_research-framing.md) — any finding is a win including null results; don't optimize for impressive outcomes (26.4.1)
- [Provider preferences](feedback_provider-preferences.md) — OpenRouter preferred for Llama/Nemotron, Fireworks fallback; ¬Together AI (26.4.2)
- [API key location](feedback_api-key-location.md) — MCP keys in ~/.claude.json mcpServers env, NOT .env files; use claude mcp add or nano (26.4.2)
- [API budget pause](feedback_api-budget-pause.md) — stop and notify on API failures, don't push through; user tops up budget (26.4.2)
- [Exp 2 process audit](feedback_exp2-process-audit.md) — 10 process violations + 15 operational lessons from Exp 2 session (26.4.3)
- [Check repo location](feedback_check-repo-location.md) — always check project memory for file locations before editing; repos move (26.4.3)
- [Mock tests false confidence](feedback_mock-tests-false-confidence.md) — 132 mock tests ≠ production readiness; empirical testing (SQ[0]) is non-negotiable before declaring build complete (26.4.5)
- [Realistic test scenarios](feedback_realistic-tests.md) — tests must model real usage patterns, not flip flags to pass; every config = a real scenario (26.4.6)
- [Test execution pattern](feedback_test-execution-pattern.md) — run live/model tests by tier not monolith; pause and restructure on timeouts (26.4.6)
- [Use git ls-files](feedback_use-git-ls-files.md) — use git ls-files or Grep, not find, for repo file searches; avoids .venv clutter (26.4.7)
- [Context firewall career leak](feedback_context-firewall-career-leak.md) — personal context in prompt contaminates agents; strip before workspace write (26.4.8)
- [Parallel build engineers](feedback_parallel-build-engineers.md) — spawn N implementation-engineers with worktree isolation for independent SQ[] items (26.4.8)
- [F1 audit remediation](feedback_f1-audit-remediation.md) — YELLOW: BELIEF tracking, build-track source tags, contamination check, XVERIFY skip (26.4.8)
- [Process over momentum](feedback_process-over-momentum.md) — RECURRING: lead skips validate under agent pressure, optimizes for visible progress over process integrity. Only mechanical enforcement sticks. (26.4.8)
- [Process over speed](feedback_process-over-speed.md) — run every gate command, document failures not hand-wave; identifying unenforced gates = primary output (26.4.9)
- [WARNs must be BLOCKs](feedback_warns-must-be-blocks.md) — if hook WARN has no legitimate override, promote to BLOCK; WARNs have same failure mode as directives (26.4.11)
- [Never-advance loophole](feedback_never-advance-loophole.md) — gates guard transitions not actions; lead dispatches work without advancing phase → all hard blocks bypassed (26.4.13, B7 RED audit)
- [Synthesis is not deliverable](feedback_synthesis-not-deliverable.md) — completed chain = deliverable, not synthesis doc; visible output creates false "done" signal; pre-shutdown hook needed (26.4.16)
- [Lead routing contamination](feedback_lead-content-routing-contamination.md) — SESSION-KILLER 26.4.16: lead batched/routed challenges per-agent at Step 22, contaminating multi-agent architecture; user killed 3-hour C1 (multi-model-chatroom) rather than ship tainted output; only mechanical hooks can prevent recurrence
- [Plan-mode workflow](feedback_plan-mode-workflow.md) — plans stay in plan-mode as handoff to sigma-build, not immediate ExitPlanMode approval; deferred memory writes noted in Session Handoff section (26.4.16)
- [Schema drift check](feedback_schema-drift-check.md) — when shipping features, either wire or delete every schema field; don't advertise functionality the app doesn't deliver (26.4.20)
- [Accountable rigor over permissiveness](feedback_accountable-rigor-over-permissiveness.md) — when a rule over-fires, require the system to defend each invocation rather than adding exceptions; rigor stays default, edges self-correct (26.4.20)

## references
- [Anthropic rate limits](reference_anthropic-rate-limits.md) — 1K RPM, 90K output tok/min (binding constraint), all Claude models (26.4.2)
- [API budget recovery](reference_api-budget-recovery.md) — 3 steps: add credits + increase limit + reset API key (26.4.2)
- [Gemini daily quota](reference_gemini-daily-quota.md) — 250 req/day per model even on paid tier (26.4.3)
- [Experiment execution pattern](reference_experiment-execution-pattern.md) — concurrent eval, checkpointing, budget pause, nohup (26.4.3)

## user profile
- [LLM internals interest](user_llm-internals-interest.md) — embeddings, hidden states, superposition, AI philosophy, convergence theory (26.4.2)
- [User hardware](user_hardware.md) — MacBook Air M3 16GB, Ollama 0.20.2 Pro, four local models: llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, qwen3.5:4b (26.4.4)
- [User Loan Agency](user_loan-agency.md) — third-party loan agent firm context

## sigma-mem (global memory — patterns, decisions, builds, reviews)
All patterns, decisions, corrections, build/review history, and project state live in sigma-mem (~/.claude/memory/).
Call sigma-mem recall → follow navigation hints to topic files. Use search_memory for specific lookups.
Agent team protocol lives in agent definitions (~/.claude/agents/) and directives (~/.claude/teams/{team}/shared/).

## memory architecture
!two-layer: auto-dream→project-scoped(plain English) | sigma-mem dream()→global+team(ΣComm) | neither touches the other's files (26.3.25)
!/sigma-dream: skill+weekly-trigger(Mon 8am MDT, team-scope dry-run) | trig_01EtnbDfEPYr2QeqbhUFMnPK | 26.3.25
!sigma-mem: MCP memory server | 6 modules, ~2600 LOC, 293 tests | dream.py BUILT 26.3.29 | Apache 2.0, public-ready 26.4.4

## research refresh
!11-agents-refreshed 26.3.22: macro-rates,sanctions-trade,energy,geopolitical,portfolio,regulatory,tech-industry,economics,reg-licensing,reference-class,cognitive-decision-scientist | DA skipped(reactive) | core-5+loan-ops already current(26.3.7/26.3.12) | next-refresh: 26.4.22 (geopolitical: 26.3.25 for Iran ultimatum resolution)
!dominant-theme 26.3.22: Iran-war/Hormuz-crisis colors all market-domain research — Brent $112, Hormuz -70% traffic, 400M-bbl SPR release, stagflation signals, Great Rotation(energy+27%,tech-20%)
