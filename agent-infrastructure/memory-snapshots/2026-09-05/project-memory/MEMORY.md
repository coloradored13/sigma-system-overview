# sigma-system-overview — project-scoped memory
# project state lives in global ^projects.md — don't duplicate here

- [Fortna Agentic CI](project_fortna-agentic-ci.md) — sigma-review complete 26.8.31, chain 24/24: CI brief + 2 wiki pages + 14 approved patterns; OPEN: apply 6 protocol changes to directive files, fix sigma-verify provider budget/registry, lead-runs-init-before-spawn, A9 regex fix

- [Personas Audit](project_persona-audit.md) — loan-agency persona package v1.2, 13 personas, 26.5.12 — detail in file
- [K-shape Ultra Report](project_k-shape-ultra-report.md) — 13,995-word opportunity scan 26.5.17, ~/Documents/k-shape-ultra-report-2026-05-17.{md,docx} — detail in file
- [Prompt Coach](prompt-coach-project.md) — local webapp, scaffolded 26.3.6, paused → evolved into Spec Workshop
- [Spec Workshop](project_spec-workshop.md) — Streamlit spec-writing tool with Claude API, v1 spec drafted 26.3.29
- [AI PD Tracker](project_ai-pd-tracker.md) — ~/Projects/ai-pd-tracker/ FastAPI+SQLite curriculum tracker + Field Guide workbench; remote restructured 26.8.4 (Track P, Phase 3, 41 lessons, 106 tests); audit triage 26.9.5 → plan there-are-two-documents-hazy-peach.md; Wave 0 merged (PR #5); Wave 1 coach assessor PR #6 READY (4-way 13/13: assessor ×3, GPT-5.6, cold Gemini; must_hold 7/13); learner not started; next = merge #6 → currency run → Wave 2 — full detail in file
- [Cutebot MCP](project_cutebot-mcp.md) — ~/Projects/cutebot-mcp/ MCP server, v0.2.3 live 26.5.23: 22 actions verified, radio-wedge debunked (retries 1→3 fix), BLE not needed; 2 files dirty pending commit — full detail in file
- [Loan Admin KB](project_loan-admin-kb.md) — 6-doc review, complete 26.3.13
- [Rosetta](rosetta.md) — ΣComm notation decoder (canonical version now in sigma-mem/docs/notation-reference.md)
- [Dream Consolidation](project_dream-consolidation.md) — BUILT 26.3.29: dream.py 846 LOC, 76 tests, MCP registered, end-to-end verified

## sigma-ui
- [sigma-ui](project_sigma-ui.md) — Phase B3 COMPLETE (26.3.31): 16 modules, 280 tests, E2E integration, pushed. Repo: ~/Projects/sigma-ui/

## sigma-ralph
- [sigma-ralph](project_sigma-ralph.md) — ~/Projects/sigma-ralph/, Apache-2.0 Ralph Loop primitive via SDK-direct (sidesteps chain-evaluator). Phase 1 shipped 26.5.7 commit 0559289 (16/16 tests, 1305 hook-pass regression). Phase 2 (engineer-ralph) Gate-contingent on c2-baseline.md (sigma-system-overview commit c5d3f43). Plan: glowing-hugging-wilkinson.md.

## sigma-optimize
- [sigma-optimize](project_sigma-optimize.md) — Exp 1-2 COMPLETE, A2-follow + A3 COMPLETE, Exp 3 DESIGNED (convergence probe)
- [Exp 3 convergence probe](project_exp3-convergence.md) — cross-model/architecture convergence, ready to scope (Exp 2 dependency resolved)
- [sigma-verify providers](project_sigma-verify-providers.md) — 13 providers: 4 local + 6 Ollama cloud Pro + 2 per-token + 1 optional, expanded 26.4.5

## gate infrastructure
- [Gate infrastructure](project_gate-infrastructure.md) — atomic checklist model: chain-evaluator (A1-A19 + B1-B4) + phase-gate (2 hard blocks + 1 warn), replaces orchestrator + 841-line enforcer (26.4.16)
- [Orchestrator BUILD mode](project_orchestrator-build-mode.md) — SUPERSEDED 26.4.16: orchestrator deleted, BUILD uses 3-conversation phase files (c1-plan, c2-build, c3-review)
- [Sigma-Review Infrastructure Issues (R19 post-mortem)](project_sigma-review-infrastructure-issues.md) — 25 prioritized issues from R19 26.4.22; several since remediated (premise-audit, sed-i block, precision gate live), #3 ΣVerify agent-context root-caused 26.8.31 + #8 phase-gate header rigidity re-confirmed 26.8.31 — full list in file

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
kaggle-measuring-agi (deadline 26.4.16, PAST) — state in ^projects.md + ~/Projects/kaggle-measuring-agi/COMPETITION-BRIEFING.md

## skills + hooks
- [Skills integration v3](project_skills-integration-v3.md) — 42 skills installed, native Claude Code routing, opt-in skill access for agents during Work phase (26.4.15)
- [Hook enforcement](project_hook-enforcement.md) — chain-evaluator.py (Stop, non-looping) + phase-gate.py (5 BLOCKs + 2 WARNs: ctx-firewall + ΣComm Tier-2). LIVE 26.4.24; ΣComm three-tier WARN added 26.5.7 commit 437096c (1281 pass / 14 skip). Tier-1 BLOCK pending Phase C calibration (≤5% FP, ≥20 writes); plan: ~/.claude/plans/let-s-come-up-with-fancy-wilkinson.md
- [Skills architecture expansion](project_skills-architecture.md) — dual-use skills (single-instance + team), marketplace port planned, routing at ~15+ skills (26.4.8)
- !source-validation 26.4.29: sigma-single Stage 3.5 Source Bias Probe integrated (commit 08f8241); ¬percolated to sigma-review
- [Sigma-single triangulation gap](project_sigma-single-triangulation-gap.md) — aggregator-tier sources not down-weighted in sigma-single ranking math; fix = ≥2 source categories for load-bearing magnitudes — detail in file

## repos
coloradored13/{hateoas-agent(public),sigma-mem(public),ollama-mcp-bridge(public),sigma-verify,sigma-system-overview,sigma-predict(private)}
!licensing: all repos Apache 2.0 since 26.4.4-7 (except Updraft+Project 1, no remote); hateoas-agent+sigma-mem public-released with security audit + docs 26.4.4-5

## corrections
- [Check reviewed version before triage](feedback_check-reviewed-version-before-triage.md) — fetch + compare local vs remote before disposing of any external review's findings; local was 15 commits behind on 26.9.5
- [Asymmetric eval acceptance](feedback_asymmetric-eval-acceptance.md) — gating judges need aggregate agreement AND zero false-PASS on must_hold cases; false-HOLD reported not gating (26.9.5)
- [Transfer test not cold if committed](feedback_transfer-test-not-cold-if-committed.md) — commit rubric + authoring spec only; author instance just-in-time, gitignored, no-echo (26.9.5)
- [Persona assumed ≠ unprobed](feedback_persona-assumed-not-unprobed.md) — 'assumed at working level' = don't reteach by default, still probe on exposed gaps or domain shift (26.9.5)
- [Verify loss before cutting](feedback_verify-loss-before-cutting.md) — map each probe of a to-be-cut module to its covering home; move uncovered pieces first (26.9.5)
- [Shareable report style](feedback_shareable-report-style.md) — for docx/brief/report deliverables: strip methodology, cold-readable non-AI voice, inline cites + comprehensive Sources section (26.5.17)
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
- [Lead routing contamination](feedback_lead-content-routing-contamination.md) — SESSION-KILLER 26.4.16: lead must never batch/route analytical challenges per-agent — detail in file
- [Plan-mode workflow](feedback_plan-mode-workflow.md) — plans stay in plan-mode as handoff to sigma-build, not immediate ExitPlanMode approval; deferred memory writes noted in Session Handoff section (26.4.16)
- [Schema drift check](feedback_schema-drift-check.md) — when shipping features, either wire or delete every schema field; don't advertise functionality the app doesn't deliver (26.4.20)
- [Accountable rigor over permissiveness](feedback_accountable-rigor-over-permissiveness.md) — when a rule over-fires, require the system to defend each invocation rather than adding exceptions; rigor stays default, edges self-correct (26.4.20)
- [XVERIFY excludes Anthropic](feedback_xverify-anthropic-excluded.md) — sigma-verify cross-model checks must exclude anthropic provider; Claude verifying Claude is not cross-model; enforce in spawn prompts until sigma-verify default-excludes (26.4.23)
- [Avoid parallel sessions](feedback_avoid-parallel-sessions.md) — don't run concurrent Claude sessions writing to sigma-system-overview shared infra; check git log + mtimes before starting work that touches it (26.4.28)
- [Recovery over apology](feedback_recovery-over-apology.md) — don't apologize for tech hiccups (API errors, MCP flapping, dropped spawns); name state + recover; keeping to the plan after a hiccup IS the success (26.4.28)
- [User-approval gate non-bypassable](feedback_user-approval-gate-non-bypassable.md) — transport failure never authorizes skipping the auto-vs-user-approve gate (26.4.28)
- [Pivot direction logic](feedback_pivot-direction-logic.md) — active wheel arcs in SAME direction as heading change; verify before claiming wiring inversion (26.5.3)
- [Ralph plugin avoidance](feedback_ralph-loop-plugin-avoid.md) — never install ralph-loop plugin where chain-evaluator is active (Stop-hook collision) (26.5.7)
- [Phase Gate measurement pattern](feedback_phase-gate-measurement.md) — build Phase 1, gate Phase 2 on measured trigger; null result is a deliverable (26.5.7)
- [Other-model feedback pattern](feedback_other-model-feedback-pattern.md) — route non-trivial plans through cross-model review pre-approval (26.5.7)
- [TaskCreate before TeamCreate leak](feedback_taskcreate-before-teamcreate-leak.md) — pre-team TaskCreate strands tasks + bleeds into agent inboxes; skip task tracking for teams (26.5.8)
- [Avoid profile anchoring](feedback_avoid-profile-anchoring.md) — landscape/opportunity analysis stays evidence-neutral, never narrowed to user's profile/domain (26.5.17) — default opportunity types in file
- [Sigma-review restart hygiene](feedback_sigma-review-restart-hygiene.md) — unfinished WS at /sigma-review start: fully wipe before investigating prior framing; never surface prior hypotheses as resume options (26.5.21)
- [XVERIFY is cross-check not proof](feedback_xverify-is-cross-check-not-proof.md) — primary verification = web/source research; XVERIFY supplemental only; T1 needs primary external source (26.5.27)

## references
- [Enterprise AI Case exemplar](reference_enterprise-ai-case-exemplar.md) — six-part cold-case template in Downloads; warm domain for this learner, use as P.1 answer key + authoring template (26.9.5)
- [Sigma-review benchmark 26.5.17](reference_sigma-review-benchmark-2026-05-17.md) — sigma-review (24/24) beat Desktop Claude DR (22), sigma-single (20), ChatGPT DR (16), Gemini Pro DR (11) on K-shape opportunity-scan with 24-point rubric. Validates multi-agent architecture vs commercial DR products on conviction-required tasks.
- [ChatGPT DR hedging](reference_chatgpt-dr-hedging.md) — ChatGPT deep research natively produces smooth, low-conviction, "consider these lanes" deliverables on opportunity-scan tasks. Not editorial smoothing. Poor tool choice when deliverable value is conviction; appropriate when value is coverage.
- [Anthropic rate limits](reference_anthropic-rate-limits.md) — 1K RPM, 90K output tok/min (binding constraint), all Claude models (26.4.2)
- [API budget recovery](reference_api-budget-recovery.md) — 3 steps: add credits + increase limit + reset API key (26.4.2)
- [Gemini daily quota](reference_gemini-daily-quota.md) — 250 req/day per model even on paid tier (26.4.3)
- [Experiment execution pattern](reference_experiment-execution-pattern.md) — concurrent eval, checkpointing, budget pause, nohup (26.4.3)
- [Subscription vs per-token cost model](reference_subscription-vs-pertoken.md) — agents+lead are subscription, only XVERIFY paid providers (openai+google) bill per-token; full sigma-build ~$1-5 not $10-15 (26.4.23)
- [Split-pane agent teams](reference_split-pane-agent-teams.md) — native Claude Code UX for user-in-multi-agent chat: tmux + CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 (26.4.30)

## user profile
- [Learning goal: product thinking in AI](user_learning-goal-product-thinking-in-ai.md) — between novice and senior-PM framing; apply PM craft to AI contexts (26.9.5)
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
!agent-research STALE: last full refresh 26.3.22 (11 agents; Iran/Hormuz-crisis era assumptions) — refresh before relying on any market-domain agent memory
