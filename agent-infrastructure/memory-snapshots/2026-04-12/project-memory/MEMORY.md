# sigma-system-overview — project-scoped memory
# project state lives in global ^projects.md — don't duplicate here

- [Prompt Coach](prompt-coach-project.md) — local webapp, scaffolded 26.3.6, paused → evolved into Spec Workshop
- [Spec Workshop](project_spec-workshop.md) — Streamlit spec-writing tool with Claude API, v1 spec drafted 26.3.29
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
- [Gate infrastructure](project_gate-infrastructure.md) — 28 mechanical gates (V1-V28) via orchestrator validate/compute-belief + hook enforcement layer, post-exit-gate phases now auto-validated (26.4.11)

## sigma-system-2
- [Clean-room rebuild](project_sigma-system-2.md) — A/B test, sequenced after sigma-predict build (26.3.23)
- [Three-mode routing](project_three-mode-routing.md) — ANALYZE/BUILD/EXECUTE distinction, review classifies own output (26.3.25)

## multi-model agents
- [Multi-model agent vision](project_multi-model-agents.md) — any model fills any agent role; ΣComm distribution > definition; spawn infra is bottleneck (26.4.8)

## chatroom + ollama-mcp-bridge
- [Multi-model chatroom + MCP bridge](project_chatroom.md) — Bridge B6 audit remediation COMPLETE (816 tests, DA A-). Chatroom NOT STARTED.
- [ΣComm translator](project_sigmacomm-translator.md) — DESIGNED in F1, DEFERRED pending empirical validation (DA[1] challenge 26.4.8). ADR[2] locked in archive.
- [F1 build patterns](project_f1-build-patterns.md) — 6 patterns promoted: IP normalization, HARDENED enforcement, empirical gates, multi-agent convergence, parallel engineers (26.4.8)

## kaggle competition
kaggle-measuring-agi in ^projects.md | briefing: ~/Projects/kaggle-measuring-agi/COMPETITION-BRIEFING.md
DeepMind hackathon, $200K, cognitive benchmarks, deadline 26.4.16, status: review-complete→build-started

## skills + hooks
- [Skills integration v3](project_skills-integration-v3.md) — 29 claude.ai skills installed, agent boot step 2a, progressive disclosure, socratic-grill handoff (26.4.11)
- [Hook enforcement](project_hook-enforcement.md) — 8 hooks, 5 hard BLOCKs (phase skip, DA exit-gate, BELIEF, CB, lead synthesis), MCP monitor, 1242 tests (26.4.11)
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

## references
- [Anthropic rate limits](reference_anthropic-rate-limits.md) — 1K RPM, 90K output tok/min (binding constraint), all Claude models (26.4.2)
- [API budget recovery](reference_api-budget-recovery.md) — 3 steps: add credits + increase limit + reset API key (26.4.2)
- [Gemini daily quota](reference_gemini-daily-quota.md) — 250 req/day per model even on paid tier (26.4.3)
- [Experiment execution pattern](reference_experiment-execution-pattern.md) — concurrent eval, checkpointing, budget pause, nohup (26.4.3)

## user profile
- [LLM internals interest](user_llm-internals-interest.md) — embeddings, hidden states, superposition, AI philosophy, convergence theory (26.4.2)
- [User hardware](user_hardware.md) — MacBook Air M3 16GB, Ollama 0.20.2 Pro, four local models: llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, qwen3.5:4b (26.4.4)
- [User Loan Agency](user_loan-agency.md) — third-party loan agent firm context

## agent teams
!self-sufficient: agents read own files at boot |¬ inject memory into prompts
boot→ ~/.claude/agents/sigma-lead.md |→ follow protocol
defs: sigma-lead,sigma-comm,tech-architect,implementation-engineer,product-strategist,product-designer,ux-researcher,ui-ux-engineer,code-quality-analyst,technical-writer,devils-advocate @~/.claude/agents/
team "sigma-review": 8 core + DA + 5 market-domain + 3 regulatory-domain + 3 dynamic = 20 agents on roster (product-designer added 26.3.27 for BUILD plan-track)
team "sigma-optimize": 5 agents (search-conservative,search-aggressive,search-combinatorial,statistical-analyst,cross-model-validator) | experimental research mode | statistical exit-gate ¬dialectical | hateoas-agent orchestrator | anti-contamination directives §1-§5 | 26.4.1
!ANALYZE→BUILD-separation: ux-researcher→product-designer→ui-ux-engineer(frontend) | tech-architect→implementation-engineer(backend) | analyst-defines-WHAT,designer-architects-HOW,builder-implements | builder-flags-impractical-specs-with-evidence (26.3.24, extended 26.3.27)
!plan-track/build-track(26.3.27): plan-track(tech-architect,product-designer,product-strategist) | build-track(implementation-engineer,ui-ux-engineer,code-quality-analyst) | DA spans both
!cross-track-review(26.3.27): build-track joins DA to challenge plan feasibility | plan-track joins DA to review build fidelity | receiving group = best critic
!dynamic-BUILD-rounds(26.3.27): ¬fixed 4 rounds → two-phase Bayesian: P(plan-ready)>0.85→lock→P(build-quality)>0.85→done | max 5 rounds/phase | builders fix until architects+DA satisfied
!sigma-build-self-contained(26.3.27): ¬depends on sigma-review | any prompt enters → UNDERSTAND(extract Q[]/H[]/C[], challenge, clarify) → PLAN → BUILD | workspace ## prompt-understanding replaces ## review-findings | gates now orchestrator-enforced via validate command (26.3.28)
!sigma-build-phase-based(26.4.8): SKILL.md 577→88 lines + 13 phase files in phases/ | lead reads ONE phase at a time | every step mandatory | skipping=failure | phases: 00-preflight→01-spawn→02-plan→03-plan-challenge→04-build→05-build-review→05b-debate→06-synthesis→06b-compilation→07-promotion→08-sync→09-archive→10-shutdown
!adversarial-layer v2.1: DA from r2 minimum | ANALYZE(min 3, max 5, DA exit-gate controls) | BUILD(dynamic rounds, cross-track review, Bayesian exit 26.3.27)
!dynamic-agent-orchestration v1.0: DA identifies gaps → lead creates specialist mid-review (see directives.md)
!hard gate: step 0 research check before spawning — never skip (correction logged 26.3.7)
workspace: ~/.claude/teams/{team}/shared/workspace.md (source of truth)
directives: ~/.claude/teams/{team}/shared/directives.md (adversarial+dynamic protocols)
inboxes: ΣComm via markdown, summarize-and-clear pattern
convergence: agents declare ✓ in workspace, lead reads to detect completion
research: check agent memory ## research freshness before reviews

## patterns
self-sufficient boot(read own files) | ΣComm agent↔agent, plain lang agent↔user
expertise-weighted decisions(domain expert primary, dissent preserved)
selective wake(wake_check matches task↔roster wake-for)
agents self-curate(findings,calibration,patterns,research)
2-agent teams herd faster → always include DA from r2
teams replace consensus under DA pressure → DA must stress-test NEW consensus too
dual DA rounds (r2+r4) catch different issues → single DA round insufficient for complex analysis
!analytical-hygiene-forcing-function: every check→outcome 1(changes)/2(confirms+evidence)/3(gap)→no checkboxes (see directives.md §2)
!source-provenance §2d: every finding carries |source:{type} tag — [independent-research]|[prompt-claim]|[cross-agent]|[agent-inference]|[external-verification] — DA audits distribution (26.3.17, extended 26.3.22)
!cross-model-verification §2h: sigma-verify MCP wraps 13 providers (4 local + 6 Ollama cloud + 2 per-token + 1 optional) | mandatory-when-available(top-1-load-bearing-finding) | 3 states: XVERIFY/XVERIFY-FAIL/no-tag | DA exit-gate criterion 9 | advisory weight ¬override domain expertise (26.3.22, expanded 26.4.5)
!prompt-decomposition §7: lead extracts Q/H/C from user prompt before spawn — claims become testable hypotheses ¬assumed facts — both ANALYZE+BUILD (26.3.17)
!DA-prompt-audit: exit-gate criterion 5 — echo detection, source distribution, methodology assessment (investigative vs confirmatory) (26.3.17)
!ANALYZE rubric now 8 criteria (added source-provenance) | all agents now have hygiene sections (26.3.17)
!§8 workspace-archiving: lead archives workspace to shared/archive/ at shutdown — preserves review state for /sigma-audit (26.3.17)
!/sigma-audit: independent process quality check — fresh opus agent verifies protocol compliance (GREEN/YELLOW/RED verdict) — calibration stored to team patterns (26.3.17)
!/sigma-feedback §9: post-review calibration loop — datum(pushback-once→accept) | concept(DA-tested-mini-review) | cascade-check | pattern-detection(systemic≥3) | corrections→agent-memory-C[]+workspace-addendum (26.3.23)
!team-size-calibration: 8-agent review (WU 26.3.13) produced depth but high volume → consider 3+DA model for future (PS+econ+tech-industry covered 80% of ground) → compare results
!DA-should-not-research-in-refresh: DA is reactive (challenges from r2), doesn't need independent domain research pre-review
!source-quality-tiers-mandatory §2d+: load-bearing findings(>70% or superlative) MUST carry T1/T2/T3 tier tag | missing=process-violation | T3-only¬sufficient for high-conviction | DA audits tier distribution (enforced 26.3.22)
!agent-template-enforcement: dynamic agents MUST use ~/.claude/agents/_template.md as base | template provides: boot,comms,persistence,promotion,hygiene(§2a-e),source-provenance(§2d/§2d+),cross-model(§2h),dialectical(§2g) | lead fills: Role,Expertise,Review,Weight (enforced 26.3.22)
!sigma-verify-pre-flight: sigma-review+sigma-build step 3 runs sigma-verify init → writes availability to workspace ## infrastructure | ¬blocking (26.3.22)
!research-date-format: R[] blocks use YY.M.D format(26.3.22) for freshness validator | sigma-mem also accepts YYYY-MM-DD as fallback (26.3.22)
!implementation-triage: 3-condition gate for sigma-review use — stakes≥$1M/regulatory/12mo-strategy AND herding-risk AND calibration-matters | fail-any→enhanced-single-instance | established 26.3.22 (cognitive-enhancement review)
!Toulmin-warrant-exit-gate: DA criteria 5-7 — falsifiability+steelman+confidence-gap | narrowed from full CQoT to warrant-only | §2a-e covers rest | P=45-55% marginal value | 26.3.22
!cognitive-findings: FORMAT-3tier+metacognition-paradox+accuracy-reclassification+dialectical-bootstrapping → see ^cognitive-enhancement-meta review (26.3.22)
!§7-prompt-decomposition-user-confirmation-gate: extract Q/H/C → present to user → get confirmation → THEN spawn | unconfirmed decomposition = contaminated → restart (correction 26.3.17)
!prompt-wash-scenario: downstream analysis uses locked findings as input, separate agent context, no conversation leakage (established 26.3.17)
!doc-generation-heredoc: Bash(python3:*) heredoc ¬Write tool | RECURRING: background agents hit permission walls (3 failures 26.3.22) | workaround: lead generates docx in main context
!lead-role-boundary(26.3.28→26.4.11): lead MUST NOT call XVERIFY/verify/challenge — agent tools only | lead MUST NOT write synthesis — now HARD BLOCKED by hook (PreToolUse blocks Write to synthesis/report files without synthesis-agent evidence) | lead MUST NOT shutdown before synthesis+promotion+sync complete | absorbing work = provenance misrepresentation
!empirical-validation-gate(26.4.8): DA can defer keystone features by asking "has anyone tested the premise?" | building attack surface for unvalidated assumption=wrong | test BEFORE build | source:F1-build DA[1]
!multi-agent-code-read-convergence(26.4.8): 4 agents independently found same 6+ IP bypass vectors reading same code path | independent confirmation>single-agent review for security findings
!BELIEF-most-missed(26.4.8→26.4.11): BELIEF[] was most consistently missed protocol element | now HARD BLOCKED by phase-compliance-enforcer hook — cannot advance from challenge/review without BELIEF[] in workspace
!XVERIFY-mandatory-security-critical(26.4.8): ΣVerify available + security-critical ADR → XVERIFY MANDATORY on top-1 | non-security → advisory | unavailable → neutral | hard-gated in phase 02

## builds (6 completed)
sigma-ui-phase-a: 5+DA, BUILD TIER-2 | 7 modules, 132 tests, P(build-quality)=0.87 | H1=CONFIRMED, H3=ACCEPTED(P=50-60%), DA cond-PASS | 26.3.29
sigma-ui-phase-b1: types extraction, dispatcher fixes, review_state enhancements | 176 tests | 26.3.29
sigma-ui-phase-b2: 5+DA, BUILD TIER-2 | 15 modules, 250 tests, P(build-quality)=0.91 | Streamlit UI, gate lifecycle, preflight | DA PASS | 26.3.29
sigma-ui-phase-b3: 5+DA, BUILD TIER-2 | 16 modules, 280 tests, E2E integration, 7 str Enums, G1/G2 dismissibility, quality metric | DA EXIT-GATE PASS | 26.3.31
ollama-mcp-bridge-F1: 5+DA, BUILD TIER-2 | 5 gaps(provenance,signal-codes,IP-hardening,HARDENED-enforcement,typed-dispatch) | 810 tests, 0 regressions | Q2 ΣComm DEFERRED(DA[1] empirical gate) | DA plan:B+ build:A- rubric:A(3.75/4) | audit:YELLOW→remediated+5-green-path-tweaks | 26.4.8
ollama-mcp-bridge-B6: 5+DA, BUILD TIER-2 | 6 audit findings(bare-filename-P0,dormant-fields-P1,BLOCKED_PROFILE-P1,secret-scoping-P2,email-domain-P2,fsync-P2) | 816 tests, 0 regressions | DA plan:B+ build:B+ rubric:A-(3.75/4) | 26.4.9

## reviews (10 completed, all exit-gate PASS, archives in shared/archive/)
cross-model-protocol-R16: 5+DA, 2r | 3-layer protocol(envelope+payload+contract), H1=COND-CONFIRMED(P=72%), H4=FALSE, H5=FALSE, 3-provider XVERIFY, engagement A- | gate enforcement ~50%→7 bugs found→fixed | 26.4.9
loan-admin-tech-landscape: 5+DA, 2r | tech=floor¬ceiling, P(consolidation)=48%, H5-falsified | audit:YELLOW→remediated | 26.3.17
vdr-market-analysis: 5+DA, 3r | $2.8-3.4B market, CAGR=8-16%(scope-conditional), Datasite-leader+30%-rollup-risk | 26.3.18
biotech-healthcare-MA: 6+DA, 3r | AI=accelerant¬engine, patent-cliff=$300B+primary-driver, CAGR=18-22%(¬38-44%) | 26.3.18
cognitive-enhancement-meta: 4+DA, 3r | R1→R3-INVERSION, enhanced-single-instance>sigma-review, 3-condition-triage | 26.3.22
kaggle-agi-benchmark: 5+DA, 2r | "Monitoring Without Knowing" JOL+calibration+error-monitoring, P(prize)=22-24% | 26.3.23
sigma-predict-review: 5+DA, 2r | DA-priority-inversion(learning-loop→#1), 3-phase-calibration, strongest-methodology | 26.3.23
hateoas-agent-improvement: 6+DA, 2r | 2C+2H findings, P(adoption-12mo)=2-22%, 5-phase-build-prompt | audit:YELLOW→remediated(§2d+tier-tags) | 26.3.25
5yr-PM-strategy: 6+DA, 2r | build-to-learn>earn-premium, adaptation-theater=#1-failure(40-45%), execution-gap>info-gap, P(PM-viable)=72%, tutorial-test-heuristic | 26.3.28
5yr-PM-strategy-AUDIT: YELLOW | CB skipped(RED), §2f absent, §2g absent, format gaps | triggered gate infrastructure build (V1-V23) | 26.3.28
sigma-ui-architecture: 5+DA, 2r | P(full-arch)=35%, Streamlit+SDK-v1-recommended, framework=UI¬orchestration, TIER-A/B/C-observables, H2=WEAKLY-PARTIAL, H4=52%-coin-flip, 7-patterns-promoted | 26.3.28

## memory architecture
!two-layer: auto-dream→project-scoped(plain English) | sigma-mem dream()→global+team(ΣComm) | neither touches the other's files (26.3.25)
!/sigma-dream: skill+weekly-trigger(Mon 8am MDT, team-scope dry-run) | trig_01EtnbDfEPYr2QeqbhUFMnPK | 26.3.25
!sigma-mem: MCP memory server | 6 modules, ~2600 LOC, 293 tests | dream.py BUILT 26.3.29 | Apache 2.0, public-ready 26.4.4

## research refresh
!11-agents-refreshed 26.3.22: macro-rates,sanctions-trade,energy,geopolitical,portfolio,regulatory,tech-industry,economics,reg-licensing,reference-class,cognitive-decision-scientist | DA skipped(reactive) | core-5+loan-ops already current(26.3.7/26.3.12) | next-refresh: 26.4.22 (geopolitical: 26.3.25 for Iran ultimatum resolution)
!dominant-theme 26.3.22: Iran-war/Hormuz-crisis colors all market-domain research — Brent $112, Hormuz -70% traffic, 400M-bbl SPR release, stagflation signals, Great Rotation(energy+27%,tech-20%)
