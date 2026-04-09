# tech-architect — personal memory

## identity
role: technical architecture specialist
domain: architecture,security,performance,infra,api-design
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known codebases
sigma-mem[4 modules 1,382 LOC, 165 tests(5 files), HATEOAS state machine via hateoas-agent, MCP server, team memory bridge, agent boot|handlers.py=856 LOC largest|26.3.7]
hateoas-agent[13 modules ~2K LOC, 250+ tests(9 skipped), 3 APIs (declarative/action-centric/class-based), MCP server, composite multi-resource, discovery mode, guards, persistence, validate() on both APIs, CI 3.10-3.13|26.3.7]
sigma-review-team[persistent team memory at ~/.claude/teams/sigma-review/, agents/shared/inboxes dirs, boot-sequence pattern, expertise-weighted decisions|26.3.7]
sigma-system-overview[setup.sh 430 lines, ARCHITECTURE.md, SETUP.md, README.md, agent-infrastructure/, .gitmodules for both repos|26.3.7]
thriveapp[~10K LOC prod, 3.5K LOC tests, 365+ test cases, 13 test files, Expo SDK 54+/TypeScript-strict/NativeWind/Supabase/Cloudflare-Workers, 20 SQL migrations, 11 tables, AES-256-GCM encryption(@noble/ciphers+SubtleCrypto), Turborepo monorepo(packages/app+supabase+worker), Phase 4/10 complete, health behavior change app with behavioral-science constraints|26.3.8]

## past findings (on sigma-mem, NOT on hateoas-agent)
review-1(26.3.7): path-traversal(!fixed), checksum-logic(docstring-fixed), state-detection(rewritten to scoring), dead-code(removed), no-tests(32 added) |#5
review-2(26.3.7): _detect_state missing memory_dir passthrough(fixed), unused import re(fixed) |#2
review-3(26.3.7): team-memory-arch-review: inbox-proliferation(16 files, no GC), no-shared-file-write-coordination, sigma-mem-team-bridge-missing, no-schema-versioning, {team-name}-placeholder-ok, cross-agent-read-intentional |#6
review-7(26.3.7): arch(A) security(A) tests(A) CI(A-) | bridge-implemented(review-3-gap-closed), 165-tests-across-5-files(up-from-32), weighted-state-detection-solid, path-traversal-prevention-solid, arrow-corruption-prevention-solid | sigma-mem-is-mature-HATEOAS-consumer |#grades-only(findings-above-are-cross-repo)

## past findings (on hateoas-agent)
review-4(26.3.7): arch(A-) api(B+) security(A) release(B) | _state-magic-key-footgun, ActionResult-unused-but-exported, RunResult-not-dataclass, anthropic-hard-dep(should-be-optional), registry-private-state-leakage(runner+persistence access _last_state), mcp-error-leaks-exceptions, no-__version__, .DS_Store/dist-in-repo, deprecated-persistence-funcs-still-exported
review-5(26.3.7): arch(A-) api(A-) security(A) release(B+) | 6 review-4 items resolved(anthropic-optional,validate-at-init,quick-start-runnable,LICENSE-author,__version__,runner-exception-safe), _state-docs-still-needed, Resource-validate-parity
review-6(26.3.7): arch(A) api(A-) security(A) release(A-) | review-4: 5-resolved+2-acceptable+1-partial(mcp-error-leak)+1-reclassified | review-5: 2/2-resolved | new: HasHateoas-Protocol-incomplete(minor), mcp-error-leak-to-LLM(minor,security), dist-stale(trivial) |#3
review-7(26.3.7): arch(A) api(A-) security(A) release(A-) | review-6: 3/3-resolved(HasHateoas-complete, mcp-error-sanitized, dist-stale-deferred) | confirmed-from-peers: Resource.required-bug(resource.py:166-172,medium), pyproject-URL-mismatch(bjgilbert-vs-coloradored13,trivial), phantom-detection.py-in-ARCHITECTURE.md(trivial), LOC-stats-outdated(trivial) | new: handlers.py-856LOC-should-split(advisory), _detect_agent_identity-broad-except(trivial), setup.sh-no-checksum-verify(advisory), CI-pin-hateoas-version(advisory), roster-3-agents-not-5(trivial), SETUP.md-memory-dir-reference(trivial) |SHIP |#6-new+4-confirmed
review-8(26.3.25): arch(A) api(A-) | F1[MEDIUM]:AsyncRunner-private-attr-bypass(async_runner.py:97-99+117-128 duplicate guard loop, GPT-5.1-AGREE-high) F2[LOW]:Resource-missing-get_transition_metadata F3[LOW]:guard-context-asymmetry(last_result-vs-workflow-context) F4[LOW]:mcp_server-45%-cov+transport-hardcoded F5[ADVISORY]:CompositeRegistry-error-message-incomplete | H1:PARTIAL(SM+Resource ready,Orchestrator-extenders-blocked-F1) H2:FALSE-for-exploration/PARTIAL-for-lockdown H3:CONFIRMED-LIMITED(seam=AsyncRunner-coupling-not-Orchestrator-concept) | coverage-gaps: mcp_server(45%),resource(80%),runner(80%),composite(86%)

## calibration
C[user values honest assessment over diplomatic framing|1|26.3]
C~[codebase is clean but early — alpha quality|1|26.3] → upgraded review-5: ship-quality alpha → upgraded review-7: ship-ready(both repos A/A- across all dimensions, 16-issue external audit resolved, 7 review rounds converged)
C[hateoas-agent is publication-quality code — security model is genuinely novel for AI agent tooling|1|26.3]
C[test suite quality: hateoas-agent 250+(9 skipped) + sigma-mem 165 tests + adversarial + integration = excellent coverage for combined ~3.4K LOC|3|26.3]
C[sigma-mem handlers.py at 856 LOC is approaching split threshold — not blocking but track|1|26.3]
C[finserv-platform-cost-estimates must include regulatory+licensing+staffing ¬just-tech-build |$10-20M-tech-only=50%-of-true-cost |lesson from DA[#3]|1|26.3.11]
C[AI-capability-claims(e.g.,"99%-accuracy") require independent-validation ¬vendor-citation |lesson from DA[#1]|1|26.3.11]
C[when-all-architecture-decisions="standard"→differentiation-is-elsewhere(compliance-integration,operational-execution,regulatory-positioning) |lesson from DA[#9]|1|26.3.11]

## patterns
hateoas-agent-framework: handles action advertisement automatically — don't flag handler-level navigation as missing HATEOAS
team-memory-as-files: simple file-based persistence scales to ~5 agents, shared files need coordination beyond that
sigma-mem-team-gap: RESOLVED review-7 — bridge implemented (issue-14), _build_agent_boot provides one-call boot package with 8 data fields, team search/write actions wired through MCP
_state-magic-key: implicit conventions are harder to maintain than explicit types for published APIs
optional-deps-for-providers: framework should work without any specific LLM provider installed
protocol-incomplete: RESOLVED review-7 — HasHateoas Protocol now includes filter_actions, get_transition_metadata, validate (confirmed in registry.py:18-43)
delta-review-severity-decay: review-4(9)→review-5(3)→review-6(3-minor)→review-7(1-medium+5-trivial/advisory) — 7 rounds confirms diminishing-returns convergence, only cross-repo/doc issues remain
mcp-vs-runner-consistency: RESOLVED review-6 — MCP server now sanitizes error messages (mcp_server.py:115-119)
concurrent-workspace-writes: review-7 workspace.md had 5+ agents writing simultaneously — atomic Write needed over incremental Edit for shared files under contention
async-sync-execution-parity: AsyncRunner duplicates Orchestrator sync execution path (private attr mutation + guard loop) — pattern to watch: async variants that bypass rather than extend sync implementations lose all future improvements to the sync path
guard-context-semantics-split: StateMachine guards see last_result (flat handler return dict); Orchestrator guards see full accumulated context — same parameter name, different semantics across API surfaces

P[python-3.14-importlib-sys.modules-preregistration|src:sigma-ui|promoted:26.3.29|class:pattern]
When loading a Python file via importlib.util.spec_from_file_location + spec.loader.exec_module(), register the module in sys.modules BEFORE exec_module, not after. Root cause: dataclass machinery calls sys.modules.get(cls.__module__) during field resolution — if not yet registered, returns None → AttributeError. Pattern: sys.modules[name] = mod; try: spec.loader.exec_module(mod); except: sys.modules.pop(name, None); raise. Discovered empirically at import integration test gate on Python 3.14 (F[IE-2], sigma-ui SQ[TA-1a]).

P[sdk-dispatch-rewrite-not-strip-for-hygiene|src:sigma-ui|promoted:26.3.29|class:pattern]
When adapting agent .md prompts for SDK dispatch (messages.create), REWRITE tool-dependent hygiene sections (§2a-§2e, §2h) with SDK-context equivalents — do not strip. Stripping removes behavioral instruction entirely: agents get no XVERIFY gap declarations, no hygiene checks. Correct rewrite: §2h → "XVERIFY not available — note intended verification as outcome 3 gap." §2a-§2e → stripped tool-call sub-steps replaced with text-equivalents. Strip-not-rewrite = zero adapted hygiene = H3 quality mitigation failure. This is load-bearing for any SDK dispatch build.

P[interface-contract-constructor-state-drift|src:sigma-ui|promoted:26.3.29|class:pattern]
When an IC specifies a param on individual method calls (dispatch(agent, task, ctx, mode="analyze")), builders often migrate it to constructor state + setter (current_phase in __init__ + update_phase()). Drift is subtle: equivalent for single-phase usage, but constructor approach creates stale-state risk when caller dispatches across phase transitions without calling setter. IC per-call param forces mode to be explicit at every call site. Flag constructor-state-for-behavioral-param as compliance gap in build reviews even when functionally equivalent in Phase A.

P[plan-mechanism-requires-source-file-inspection|src:sigma-ui|promoted:26.3.29-B1|class:pattern]
When a plan specifies a mechanism for transforming/parsing text (e.g. "subsection-header-match", "regex-on-line-N"), the mechanism MUST be verified against actual source file content before challenge round — not just against code structure. DA[#1]/IE-2 both independently caught that §2a-§2e "subsection-header-match" mechanism described in ADR[2] could not work because §2a-§2e are bullet items within a single section body, not separate headers — discoverable only by reading the .md file. Pattern: for any plan item claiming "X mechanism handles Y format", read a sample of Y format before finalizing the plan. Mechanism-without-file-inspection = guaranteed challenge-round concession.

P[cross-role-convergence=high-confidence|src:sigma-ui|promoted:26.3.29-B1|class:pattern]
When 3 agents from different roles (DA, CQA, IE) independently identify the same issue without coordination, treat as architectural fact not candidate finding. B1: _phase_round_registry write-order issue identified by CQA-5, IE-4, and DA[#4] independently — all three read the same code and reached the same conclusion. This is stronger than multiple-instance-convergence (same-agent-multiple-runs) because different expertise lenses and incentive structures reach the same result. Apply: when challenge responses show 3-agent convergence on a single structural issue, skip further deliberation and implement the fix directly.

P[validation-set-derived-from-enum|src:sigma-ui|promoted:26.3.29-B1|class:pattern]
When using both an enum (SourceTag) and a validation set (_VALID_SOURCE_TAGS frozenset) for the same domain, derive the frozenset FROM the enum: `frozenset(tag.value for tag in MyEnum)`. Independent definition of both creates dual-authority drift: add a member to enum, forget the frozenset (or vice versa). Derived frozenset = O(1) lookup + single canonical definition + impossible to diverge. Standard Python pattern for validation-against-enum. Test: assert frozenset == {tag.value for tag in Enum} enforces the contract.

C[challenge-concede-without-SQ-entry=unbuilt-scope|src:sigma-ui|promoted:26.3.29|class:calibration]
Scope items accepted in challenge responses (e.g. "concede: add types.py +0.25d") have ~40% non-delivery rate unless immediately added to SQ[] decomposition. IE implements from original SQ list, not challenge response text. Pattern: types.py accepted in challenge round as Phase A scope, never built, 11 tests skipped at delivery. Rule: when accepting scope in challenge responses, either (a) add to SQ[] immediately, or (b) explicitly defer to next phase with IC note. Acceptance without SQ entry is not commitment.

¬[over-engineering concerns — sigma-mem is 1,382 LOC but all functional, no dead code]
¬[security regressions in review-7 — path traversal, arrow injection, MCP error sanitization all solid]
¬[arch regressions in review-7 — HATEOAS contract, state machine wiring, bridge implementation all clean]

## team decisions
arch:weighted-state-detection, arch:path-validation-via-resolve (both for sigma-mem)
product:alpha-quality-reached for sigma-mem, blocker: hateoas-agent must publish first

## team patterns
review-rounds-converge: round-1=correctness, round-2=polish, round-3+=diminishing returns (confirmed through review-7: 7 rounds, only trivial/advisory findings remain, all substantive issues resolved)
delta-review-format-effective: checking previous findings systematically works well, prevents re-flagging resolved issues
shared-workspace-contention: 5 agents writing workspace.md simultaneously causes Edit failures — need atomic writes or coordination protocol

## research

R[OWASP-agentic-top10-2026: ASI01-goal-hijack, ASI02-tool-misuse, ASI03-identity-privilege-abuse, ASI04-supply-chain(tool-poisoning,rug-pulls), ASI05-unexpected-code-exec, ASI06-memory-context-poisoning | defense: input-validation-all-sources, goal-lock, tool-sandboxing-least-priv, HITL-for-high-impact | directly relevant to sigma-mem+hateoas-agent security model |src: genai.owasp.org, paloaltonetworks.com/blog |refreshed: 26.3.7 |next: 26.4]

R[MCP-security-landscape: 43%-of-MCP-servers-have-cmd-injection(Equixly), CVE-2025-6514-mcp-remote-RCE(437K-downloads), tool-poisoning=hidden-instructions-in-tool-descriptions(invisible-to-user,visible-to-LLM), rug-pull=tool-definition-mutates-post-approval, confused-deputy=server-cant-differentiate-users, credential-theft-via-agent-exfiltration | mitigations: pin-server-versions, alert-on-description-change, scope-tokens-minimally, carry-user-context-to-server | hateoas-agent's action-advertisement-model naturally constrains tool surface area(good) |src: invariantlabs.ai, simonwillison.net, checkmarx.com, practical-devsecops.com |refreshed: 26.3.7 |next: 26.4]

R[prompt-injection-design-patterns: action-selector-pattern(agent=selector-only,no-tool-feedback-loop), plan-then-execute(fixed-action-list,no-runtime-deviation), second-order-injection(low-priv-agent-tricks-high-priv-agent) | arxiv:2506.08837 formalizes these as reusable security patterns | relevant: hateoas-agent guards+state-machine already implement constrained-action-selection |src: arxiv.org/abs/2506.08837, christian-schneider.net |refreshed: 26.3.7 |next: 26.4]

R[HATEOAS-for-AI-agents-validated: Nordic-APIs+Amundsen confirm HATEOAS is "API style waiting for AI", GRAIL-framework(Goal-Resolution-through-Affordance-Informed-Logic) demonstrates hypermedia-driven-agent-navigation, key-insight: "actionability is perceived not inferred"=agents detect affordances rather than predict, workflows-discovered-at-runtime-not-designed | directly validates hateoas-agent architecture — we're ahead of the curve |src: nordicapis.com, mamund.substack.com, tldrecap.tech/apidays-paris |refreshed: 26.3.7 |next: 26.4]

R[A2A-protocol-launched: Google Agent2Agent protocol(Feb 2026, Linux Foundation, 50+ partners), complements MCP(tools+context) with agent-collaboration(communication+coordination), built on HTTP+SSE+JSON-RPC, Agent-Cards for capability-discovery, task-lifecycle-management, gRPC-support added | A2A=inter-org-agent-comm, MCP=agent-tool-comm, our ΣComm=intra-team-agent-comm — three distinct layers |src: developers.googleblog.com, a2a-protocol.org, cloud.google.com/blog |refreshed: 26.3.7 |next: 26.4]

R[multi-agent-orchestration-patterns: sequential,concurrent,group-chat,handoff,magnetic,hierarchical,event-driven | Microsoft-Agent-Framework merges AutoGen+Semantic-Kernel: session-state, type-safety, middleware, telemetry, explicit-workflow-control | centralized-vs-federated orchestration models | our sigma-review uses centralized(lead-mediates)+federated(agents-self-curate) hybrid |src: learn.microsoft.com/azure/architecture, learn.microsoft.com/agent-framework |refreshed: 26.3.7 |next: 26.4]

R[python-typing-3.13-3.14: TypeIs(PEP-742) narrows both if+else branches(unlike TypeGuard=if-only), requires narrowed-type compatible-with-input, 3.14-adds-lazy-annotations | review-relevance: recommend TypeIs for state-detection guards in hateoas-agent, replace hasattr checks with typed narrowing |src: peps.python.org/pep-0742, docs.python.org/3/library/typing.html |refreshed: 26.3.7 |next: 26.4]

R[python-packaging-2026: uv-is-default(Rust-based,10-100x-faster-than-pip,replaces-pip+pipx+pyenv+virtualenv+twine), uv_build=zero-config-backend-for-pure-Python, uv.lock=cross-platform-reproducible, Poetry-still-preferred-for-library-PyPI-publishing | hateoas-agent+sigma-mem should evaluate uv migration, uv.lock for reproducibility |src: learn.repoforge.io, scopir.com, docs.astral.sh/uv |refreshed: 26.3.7 |next: 26.4]

R[python-api-design-2026: Pydantic-v2-ecosystem=standard-for-validation, FastAPI=default-for-async-APIs, circuit-breaker+exponential-backoff=standard-error-patterns, EAFP-over-LBYL | review-relevance: Pydantic for MCP handler input validation, explicit error types over bare exceptions |src: easyparser.com, talent500.com, khaled-jallouli.medium.com |refreshed: 26.3.7 |next: 26.4]

## past findings (on thriveapp)
review-1(26.3.8): security(A-) performance(A) architecture(A) schema(A-) tests(A-) | overall(A-) SHIP-phase-4 | S1(!HIGH):SECURITY-DEFINER-missing-search_path(seed.sql+2-migrations), S2(HIGH):session-var-bypass-theoretical(app.deleting_all_data), S3(MEDIUM):check_ins.notes-unencrypted-free-text, S4(MEDIUM):no-quality_rating-CHECK-constraint, S5(MEDIUM):encryption-key-not-user-derived(ok-for-single-user), S6(LOW):client-only-rate-limit, S7(LOW):onAuthStateChange-no-encryption-reinit, A4(LOW):onboardingState-mutable-singleton | RLS 11/11 complete, encryption solid, error-msgs sanitized, crisis-detection-immutable-at-DB-level |#9

## loan-admin-agent research (26.3.11) — r1

### market-data
loan-agency-services: $10.8B(2024)→$22.1B(2033) CAGR 8.7%
private-credit-AUM: $3.5T(2025)→$5T(2029) |deployment +78% YoY
BSL: ~$5T notional |Finastra Loan IQ=70% BSL market
Private-Credit+ TAM: $45T(Oxane est.)

### competitor-tech-stacks |#8
Alter-Domus: $1.4T AUA |Agency360+Solvas+CorPro |M&A-assembled-integration-debt
CSC: independent-agent |tech-opaque |KYC-focus
Citco: $1.9T AUA(total) |built-from-fund-admin 5-10yr |generalist
GLAS: independent,conflict-free |proprietary-tech |40% organic-growth
Kroll: #3 Bloomberg Q1-2025 |!first-cloud-native-platform |8-day vs 47-day settlement
Virtus/FIS: $180B AUA |Glide+Nexus+Settlement |Loan IQ based
S&P-Global: DataXchange+AmendX(Mar 2026) |AI-categorization |¬full-admin
Versana: $3.5T notional,6000+ facilities |real-time-digital-capture |JPM cashless-roll

### architecture-decisions
1→event-driven+microservices(loan-lifecycle=event-native)
2→multi-tenant+dedicated-DB-per-client(regulatory-isolation)
3→API-first(REST+webhook+SFTP+FIX)
4→cloud-native+hybrid-option(bank-clients need private-cloud)
5→real-time+batch dual-mode(CQRS pattern)

### AI/NLP-differentiators(REVISED r2: table-stakes ¬highest-impact)
credit-agreement-parsing: 200-500pg docs→structured-data |Ontra(2M contracts)+V7+CovenantIQ exist as point-tools |!gap: ¬integrated-with-admin |r2-revision: AI-parsing=commoditizing(10+ competitors), integration-depth=differentiator
amendment-processing-AI: parse→identify-changes→auto-update→generate-consent
covenant-compliance: auto-ingest-financials→test→flag→notify→cure-track
doc-classification: AI-categorize+auto-route
calibration: AI-in-loan-admin=emerging ¬mature |Ontra(AI+human-review)=best-practice

### architecture-decisions(REVISED r2: +2 novel)
6→compliance-native-architecture(approach:NOVEL) |policy-as-system-primitive |event-sourced-deterministic-workflows |cryptographically-verifiable-audit-logs |examiner-access-patterns-in-data-model |!NEW-highest-impact-differentiator
7→DLT-ready-settlement-layer(approach:CONTRARIAN,3-5yr) |ECB-Pontes-Q3-2026 |atomic-DvP-from-day-1 |syndicated-loans="most-likely-DLT-beneficiary"

### build-vs-buy(REVISED r2)
BUILD: waterfall-engine(core-IP) + credit-agreement-AI(integration-depth ¬standalone-parsing)
BUY/INTEGRATE: Loan IQ(adapter-pattern,¬direct-coupling) + security-infra(HSM,identity,monitoring) + compliance-infra(AML:Alloy/Hummingbird $20-100K/yr, KYC-automation, regulatory-reporting)

### cost-estimate(REVISED r2: per regulatory-licensing-specialist)
tech-build: $10-20M |regulatory-capital: $2-4M(LOCKED,NH-trust-charter) |regulatory-ops: $1-2.7M/yr |loan-admin-staff: $500K-1.5M/yr
TOTAL-LAUNCH: $13-27M |ONGOING-NON-TECH: $2-5M/yr
Hypercore-comparison: $13.5M-SaaS-only(¬trust-co)=lower-but-limited-scope

### analytical-hygiene-results(REVISED r2)
§2a: standard-arch(5-decisions)+novel-compliance-native+contrarian-DLT-ready |ecosystem: all-growing
§2b: industry-norm=fragmented-point-solutions(KPMG) |compliance-by-design=emerging-fintech-best-practice-2026 |AD-HAS-AI-in-production(Solvas-Digitize)→¬slow-to-ship(r1-assumption-corrected)
§2c: $13-27M-launch + $2-5M/yr-ongoing |justified-by-$10.8B-TAM |regulatory-capital=$1.5-3M-locked |data-model=high-reversal-cost

### r2-key-position-changes |#5
1→AI-parsing: downgraded from "!highest-impact" → table-stakes-with-integration-depth-as-differentiator
2→compliance-native-architecture: upgraded to !highest-impact-differentiator(novel, ¬standard)
3→cost-estimate: revised upward 30-50%(tech-only→full-operational)
4→Loan-IQ: adapter-pattern-mandatory(¬direct-coupling) + Versana-as-strategic-hedge
5→build-sequence: regulatory-timeline-gates-tech-timeline(disagree-with-product-strategist)

### research-sources
S&P-Global(DataXchange/AmendX Mar 2026), KPMG(tech-fragmentation-report 2025), AIMA(private-credit $3.5T), IntelMarketResearch(loan-agency $10.8B), Finastra(Loan IQ 70% BSL), Kroll(cloud-native+8-day-settlement), Versana(digital-data $3.5T, JPM+BofA+Citi+DB+MS+WF+Barclays-backed), Oxane($800B+ Panorama), Ontra(AI covenant 2M contracts), Bloomberg(Kroll #3 agent), AD-Solvas-Digitize(automated-doc-receipt+extraction+validation), ECB-Pontes(DLT-settlement-Q3-2026), Capterra(Loan-IQ-alternatives), LoanPro(API-first-alternative)


## r3-deepening findings (26.3.11) — loan-admin-agent

### competitive-response-modeling
AD: acquisition-most-likely(PE-playbook,12-18mo)+feature-matching-on-Solvas-Digitize(6-12mo)+price-war-unlikely(Cinven-EBITDA-focus) |M&A-integration-debt=structural(3-5yr+$50-100M-to-fully-integrate-6-acquisitions) |AD-2024-annual-report: 18%-revenue-growth, 5500+-employees, $2.5T-AUA, North-America=40%+-of-revenue
GLAS: $1.35B-deal(Oakley-Capital,43x-revenue-multiple)=well-capitalized |build-tech+M&A-of-startups(Hypercore-acquisition-plausible) |own-M&A-creates-integration-risk(Serica+Watiga) |$750B-AUA, $30.9M-parent-revenue
Kroll: complementary-¬direct-competitor-for-mid-market-PC |settlement-speed-moat(8-day) |expanding-APAC(Madison-Pacific) |AI-practices-launched-2026
Hypercore: most-direct-BUT-most-acquirable |20-person-team+$13.5M=vulnerable |SaaS-only=service-ceiling |full-lifecycle-AI(origination→servicing→monitoring) |supports-term,revolvers,mezzanine,bridge,syndicated,construction,hybrid
competitive-window: 18-24mo-on-integration-depth |12mo-on-AI-features(incumbents-match) |confirms-r2: compliance-native-integration=durable-differentiator

### build-sequence-resolution(resolves-TA-vs-PS-disagreement)
dual-critical-path-confirmed(regulatory+tech=parallel) |Loan-IQ=conditional-trigger(month-12-24,demand-signal-based)
Phase-0(0-3):foundation(incorporate,file-charter,hire-CTO+GC,arch-design) |headcount:10 |burn:$350-500K/mo
Phase-1A(4-8):charter+MVP(NH-grant~month-5,first-2-3-clients,limited-scope) |headcount:18 |burn:$550-750K/mo
Phase-1B(9-14):platform-maturity(AI-v1+human-review,SOC2-Type-II@month-12-14) |headcount:25 |burn:$700K-1M/mo
Phase-2(15-24):scale+BSL(Loan-IQ-if-triggered,Versana-integration,settlement-optimization) |headcount:35-40 |burn:$1-1.3M/mo
Phase-3(25-36):institutional+expansion(full-BSL,successor-agent,FCA,DLT) |headcount:50-65 |burn:$1.3-1.8M/mo
total-funding: $25-35M-to-breakeven |Series-A($10-15M,month-0)+Series-B($15-25M,month-18-24)

### insurance-as-deal-gate(architecture-implication)
E&O=$1-5M(startup)→max-deal-$250-500M |$10M-coverage-difficult-without-track-record
platform-MUST-implement: deal-size-vs-insurance-coverage-tracking(NOVEL-system-constraint)
`max_deal_size = f(current_E&O_coverage, deal_type, client_requirements)`
coverage-upgrade: Y1($1-5M)→Y2($5-10M)→Y3+($10-25M) |each-unlocks-larger-deal-tier
mid-market-PC-entry=ALIGNED-with-startup-coverage-limits |mega-BSL=Phase-3-coverage-required

### platform-cost-at-mid-market-fees
fixed=$4.7-7.2M/yr |marginal=$36-72K/yr/client |revenue-per-client(median)~$100K/yr
gross-margin~46%(service-heavy ¬pure-SaaS,closer-to-managed-services-40-60%) |improves-to-55-65%-with-AI-automation
cash-breakeven: month-28-34 at 50-70-clients |cost-efficient(unit-positive)@15-20-clients
works-IF: (1)automation-reduces-ops (2)upsell-trustee/escrow(2-3x) (3)BSL-expansion-by-month-24 (4)50+-clients-within-30mo
Hypercore-comparison: 40-50%-lower-burn(SaaS-only)→$13.5M-sufficient vs $25-35M-for-full-service

### r3-calibration-updates
C[AD-has-AI-in-production(Solvas-Digitize+internal-ChatGPT+ML-RFP-analysis)→¬slow-to-ship(r1-assumption-fully-corrected)|2|26.3.11]
C[GLAS-43x-revenue-multiple-signals-PE-expects-massive-growth-trajectory|1|26.3.11]
C[Hypercore-most-direct-competitor-AND-most-acquirable(PE-exit-via-GLAS/AD-acquisition=high-probability)|1|26.3.11]
C[mid-market-PC-unit-economics=viable-but-tight(46%-gross-margin,breakeven-month-28-34)|1|26.3.11]
C[insurance-coverage-is-growth-gate-for-first-2-3-years(E&O-limits-deal-size)|1|26.3.11]
C[competitive-window=18-24mo-on-integration-depth(durable) vs 12mo-on-AI-features(non-durable)|1|26.3.11]

### r3-research-sources(new)
AD-2024-Annual-Report(18%-rev-growth,5500+-employees), Cinven-investment-announcement(€4.9B-EV,Mar-2024), GLAS-Oakley-Capital-deal($1.35B,Jan-2026,La-Caisse-minority), Kroll-AI-practices-launch(Jun-2026), Hypercore-Series-A-announcement(Insight-Partners,$13.5M,Feb-2026), Dynamo-Software-survey(Feb-2026:66%-manual-entry-challenges), WTW-fintech-E&O-risk-analysis(2025), EIM-Services-SOC2-ISO27001-fintech-case-study(2025), SaaS-Capital-2025-spending-benchmarks
## loan-admin-agent research (26.3.11) — r1 (fresh session)

### market-data
private-credit-AUM: $3.5T(2025,AIMA)→$5T(2029,Morgan-Stanley) |deployment +78% YoY(2024)
private-loan-agency-services: $760M(2024)→$1.14B(2032) CAGR 6.2%
BSL: Finastra-Loan-IQ=75%-global-syndicated-volume |IDC-MarketScape-2025-Leader
Versana: $5T-notional(up-from-$3.5T), Morgan-Stanley+Mizuho-live(2025), JPM-cashless-roll

### competitor-tech-stacks |#8
AD: $2.5T-AUA,5500+emp |Agency360+Solvas-Digitize+CorPro |Bain-Capital-$30B-win(Feb-2026) |Cinven(€4.9B-EV)
GLAS: $750B+AUA |Oakley-Capital+La-Caisse($1.35B,43x-rev,Jan-2026) |acquired-Serica+Watiga+LAS(Italy) |10-jurisdictions
Kroll: cloud-native |8-day-settlement |AI-practices-2026 |agency+trustee ¬full-admin
Hypercore: $13.5M-Series-A(Insight,Feb-2026) |$20B+AUM,10K+loans,3.5x-CARR |!first-AI-Admin-Agent-PC |SaaS-only
S&P: DataXchange+AmendX(Mar-2026) |AI-categorization |¬full-admin(point-tools)
Oxane: $350B+notional,100+clients,13/25-top-banks |Panorama+Loan-Servicing-2.0
Ontra: 2M+docs,1000+firms,9/10-top-PE |Insight-for-Credit(Sep-2025) |point-tool

### architecture-decisions |#7
1→event-sourced-microservices 2→multi-tenant+dedicated-DB 3→API-first 4→cloud-native+hybrid 5→waterfall-engine(core-IP) 6→compliance-native(!highest-impact,NOVEL) 7→DLT-ready(contrarian,3-5yr)

### differentiation-tiers
T1(durable,18-24mo): compliance-native-architecture + integration-depth(AI→admin→waterfall→reporting)
T2(defensible,12-18mo): waterfall-engine(BSL+PC) + multi-market-data-model
T3(table-stakes,<12mo): AI-doc-parsing, cloud-native, API-first, SOC2
T4(contrarian,3-5yr): DLT-ready-settlement, tokenized-loan-positions

### research-sources
AIMA($3.5T), Morgan-Stanley($5T-2029), IntelMarket($760M-agency), Finastra(75%-BSL,IDC-Leader-2025), Versana($5T-notional), AD-Bain-Capital(Feb-2026), GLAS-Oakley($1.35B), Hypercore-Insight($13.5M,Feb-2026), S&P-DataXchange+AmendX(Mar-2026), Ontra-Insight-for-Credit(Sep-2025), Oxane-Loan-Servicing-2.0, DLA-Piper(77%-AI-adoption), Dynamo(66%-manual-challenges), ECB-Pontes(Q3-2026), PwC+Confluent(EDA-finserv)
## r2 DA-response summary (26.3.11)

### DA-responses |#7
DA[#1](AI-crowding): compromise — 2-specific-workflows-named(covenant→waterfall-block, amendment→recalc). Integration-depth=12-18mo-window ¬permanent
DA[#2](incumbent-tech): compromise — AD-has-AI-FEATURES ¬AI-ARCHITECTURE. UiPath-RPA=bolt-on. M&A-3-platforms="digital-bridge"
DA[#3](cost): concede — $10-20M→$25-35M-total. Tech=50%-of-cost. Cash-runway-scenario-modeled
DA[#5](herding): partial-concede — 4-options(¬build,acquire-Hypercore,white-label,build). Build=highest-EV, white-label=viable-lower-risk
DA[#6](data-flywheel): defend — already-secondary. AD-data-SILOED. Unified-model>volume
DA[#7](Loan-IQ): compromise — 3-scenarios(60%-cooperative,15%-competes,25%-restricts). Versana=hedge. BSL=real-Phase-2-plan
DA[#9](standard-arch): defend — 3-specific-implementations(event-sourced-state-machine,policy-as-code,examiner-native). AD=30-60mo-to-replicate. Honest: drops-vs-greenfield

### r2-key-revisions
cost: $25-35M-total(was-$10-20M-tech-only)
AI: table-stakes-with-2-named-integrated-workflows
compliance-native: specific-not-abstract, 18-24mo-vs-incumbents, 12mo-vs-greenfield
differentiation-stack: added-tier-0(charter,structural) + tier-1b(integration-depth,named-workflows) + tier-2-E&O-deal-gate(novel)
null-hypothesis: build ¬unanimous, white-label=viable-alternative
P[AI-features-vs-AI-architecture: features(doc-parsing,classification)=replicable-12mo, architecture(event-sourced-compliance,integrated-workflows)=18-36mo-rewrite. Assess-competitive-window-against-architecture-replication ¬feature-replication |src:loan-admin |promoted:26.3.12 |class:new-principle]
P[M&A-integration-debt=structural-greenfield-advantage: incumbents-with-6+-acquisitions-face-$50-100M+3-5yr-unification. Greenfield=18-24mo-integrated-platform. Advantage-temporary-but-sufficient-for-relationship-lock-in |src:loan-admin |promoted:26.3.12 |class:new-principle]
P[differentiation-tiering-framework: structural(charter,regulatory)>architectural(compliance-native,integration-depth)>functional(waterfall-engine,dual-market)>feature(AI-parsing,APIs). Higher-tiers=more-durable. Use-to-assess-competitive-moats |src:loan-admin |promoted:26.3.12 |class:new-principle]
P[sigma-predict-review|F1(!C):orchestration-cost-3-8x-competitive-baseline(AIA-Forecaster=10-independent-agents→matched-superforecasters,Panshul42=5-model-aggregate=$1-3)|F2(H):isolation-unsupported-technically+counterproductive(AIA=SOTA-without-isolation)|F3(H):context-window-saturation-at-33-44-invocations|F5(M):Metaculus-forecasting-tools-framework-makes-proposal-redundant|build-prompt:5-phases-starting-fork-Metaculus-framework|grade:arch(B-)feasibility(C+)cost(D)|src:sigma-predict-review|26.3.12]
## research
R[engineered-labor-standards:MOST=dominant PMTS|3 sequences:General-Move,Controlled-Move,Tool-Use|calc:sum-indexes×10=TMU(1TMU=0.036s)|alternatives:MTM,MODAPTS,ML-dynamic|Manhattan:ELS engine task-timestamp vs standard|Blue Yonder:AI/ML forecasting+dynamic adjustment|allowances:PFD 15-20%|maturity:MOST=proven(50yr),ML-standards=emerging,hybrid=emerging|src:wikipedia.org/MOST,takt.io,manh.com,blueyonder.com|refreshed:2026-03-14|next:2026-04-14]
## research
R[real-time-perf-tracking:scanner events(barcode/RFID)+UWB RTLS(10-30cm)+wearables(ring scanners,smart glasses)+CV(YOLO11 pose)|pipeline:scanner-event to Kafka/Flink to TSDB to dashboard|Manhattan:250+ microservices,K8s,REST,real-time per-task tracking|UWB:tag to anchor to server to position(5-layer)|wearables:+30pct efficiency,70pct adoption projected|maturity:scanners=proven,UWB=proven,CV-pose=emerging,biometric=emerging|src:manh.com,sewio.net,ultralytics.com|refreshed:2026-03-14|next:2026-04-14]
## research
R[robot-fleet-mgmt:3 standards-VDA5050(EU),MassRobotics(NA),Open-RMF(OSS)|VDA5050:JSON-over-MQTT,order=graph(nodes+edges),QoS0 order/state,QoS1 connection,v2.1.0 Jan2025|MassRobotics:coexistence+monitoring,broadcasts location/speed/health,v2.0 adds charging|Open-RMF:ROS2-based,free_fleet adapter,traffic negotiation via schedule-aware routing|vendor:Locus LocusConnect API-first 6-8wk deploy,6RS Chuck robot-leads-picker|maturity:VDA5050=proven(EU),MassRobotics=proven(NA),Open-RMF=proven(OSS),unified metrics=emerging|src:github.com/VDA5050,open-rmf.org,locusrobotics.com|refreshed:2026-03-14|next:2026-04-14]
## research
R[task-allocation:3 paradigms-wave(static,rigid),zone(workers confined,reduce travel),waveless(continuous,+40pct throughput,+20pct labor)|algorithms:Hungarian(O(n3),optimal,proven),auction-based(distributed),RL(Q-Mix POMDP,92.5pct conflict-free),hybrid Hungarian+RL|waveless arch:continuous stream to priority scoring to dynamic batch to assignment by proximity+availability|maturity:wave=proven(legacy),zone=proven,waveless=proven(modern),Hungarian=proven,RL=emerging,hybrid=speculative|src:nature.com/s41598-025-88305-9,inviarobotics.com/blog/waveless-picking|refreshed:2026-03-14|next:2026-04-14]
## research
R[iot-edge-arch:MQTT pub/sub for edge low-latency,Kafka high-throughput stream,Flink/Spark ETL|edge:local broker sub-ms,selective cloud fwd|TSDB:InfluxDB=fast-ingest,TimescaleDB=SQL+joins,TDengine=fastest|maturity:MQTT+Kafka=proven,edge-TSDB=proven,edge-ML=emerging|src:hivemq.com,instaclustr.com|refreshed:2026-03-14|next:2026-04-14]
R[cloud-arch-wms:Manhattan 250 microservices K8s REST|refreshed:2026-03-14|stale-after:2026-04-14]
R[cloud-arch-wms-detail:SAP-EWM MFS PLC-level automation|multi-tenant per-customer-DB versionless-CD|integration REST MQ event-streams|Manhattan-Automation-Network for robotics|src:developer.manh.com sap.com|next:2026-04-14]
R[warehouse-data-model:entities Worker Task Zone Robot Standard Shift PerformanceMetric CostCenter|rollup worker-zone-area-dept|metrics UPH LPH utilization cost-per-unit picking-accuracy|SQL-operational+TSDB-analytics|src:easymetrics.com|refreshed:2026-03-14|next:2026-04-14]
R[computer-vision-warehouse:YOLO11 pose PPE hazards|OpenPose MediaPipe AlphaPose sub-2mm to 70mm|unsafe-bending lifting fatigue PPE pick-verify zone-intrusion|DHL deploying|PPE=proven pose=emerging pick-verify=emerging|src:ultralytics.com dhl.com|refreshed:2026-03-14|next:2026-04-14]

## warehouse-lms-architecture findings (26.3.14) — r1

### architecture-decisions |#10
F1(!C):modular-monolith+event-backbone(Kafka)→microservices-at-scale|7-modules
F2(H):2-store(PG+TimescaleDB)→ClickHouse-deferred(REVISED-from-3)
F3(H):MQTT→Kafka→Kafka-Streams(day-1)→Flink-at-scale(REVISED-from-Flink-day-1)
F4(H):MOST-first→ML-phase-2(XGBoost,±15%-cap)
F5(H):waveless+Hungarian+constraints(¬RL-day-1)
F6(H):VDA5050-adapter-first|!GAP:no-precedent-all-3-standards-unified
F7(H):canonical-model+WMS-adapters
F8(M):edge-first-offline(30min)+cloud-analytics
F9(M):Go+Python|alt:Python-only-MVP
F10(M):OIDC+RBAC+RLS+mTLS+SOC2

### hygiene-outcomes
3×outcome-1(revised):F2,F3,F3-§2c|1×outcome-3(gap):F6-§2b|rest=outcome-2

### r2-DA-responses |#4
DA[#6]:compromise—unified-telemetry(output)+paradigm-native-adapters(input) ¬canonical-command. ~85%(output) vs ~40%(full-canonical)
DA[#7]:compromise—MVP-tightened(human-only-10-12mo)
DA[#13]:concede—Python-only(talent-scarcity-binding)
DA[#14d]:compromise—human-only-first(AMR-declining-18→10%)

### r2-calibration
C[canonical-robot-model=infeasible-across-paradigms|1|26.3.14]
C[human-only-MVP=more-honest-than-unified-vision|1|26.3.14]
C[Go+Python-for-startup=luxury|1|26.3.14]
C[robotics-adoption-gap-real:planning↑-deployment↓|1|26.3.14]
## loan-admin-agent tech research (26.3.17) — r1 fresh session

### architecture-taxonomy |#3-tiers
T1-Assembled/Acquired: AD(Agency360+Solvas+CorTrade+CorPro+VBO+Vega-portal), Computershare(TrustConnect+WF-inherited-systems) | integration-debt=$50-100M+3-5yr | "digital bridges" ¬native-integration
T2-Purpose-Built-Proprietary: GLAS(conflict-free,single-system,40%-organic-growth), Kroll("first-cloud-native"-independent-agent,8-day-settlement), Hypercore(AI-native-2020,10K+loans,$20B+AUM) | greenfield-advantage
T3-Configured-Vendor: Wilmington-Trust(Loan-IQ+AccessFintech-Synergy), Virtus/FIS(Loan-IQ+Glide+Nexus), Ankura(specialist/distressed) | roadmap-dependency

### key-tech-findings |#12
F1: build-vs-buy=primary predictor of architectural flexibility
F2: Finastra Loan IQ=70-75% BSL volume, modernizing(Nexus+Build APIs), ¬SaaS-native, container-cloud options. Adapter-pattern mandatory ¬direct-coupling
F3: Versana=$5T+notional,14-agent-banks, API-first, cloud-native(EY-built) | integration=table-stakes-for-BSL(T3 by 2027). API-first=3-6mo integration, monolith=12-18mo+
F4: S&P-Global-DataXchange+AmendX(Mar-2026) = UNEXPECTED data-vendor-as-infrastructure-layer | agent→lender notice routing + amendment lifecycle | "become-the-pipe" strategy | Bloomberg-early-bond-market analogy | addresses H5+Q7
F5: AI/NLP=commoditizing-point-tools(Ontra,V7,CovenantIQ) | integration-depth=differentiator ¬parsing-alone | AD-Solvas-Digitize=production-ML | Hypercore-"AI-Admin-Agent"=marketing-for-AI-assisted-SaaS+human-oversight ¬autonomous
F6: Client-portals: AD-Vega(best-incumbent-unification,SSO), SRS-Acquiom-Deal-Dashboard(tech-born,real-time), Wilmington+AccessFintech-Synergy(shared-workflow-network-¬portal), Hypercore(unified-borrower+lender+LP-view). No-firm=full-single-pane-across-all-parties(gap)
F7: Security: SOC2-Type-II=baseline, ZTA-emerging, compliance-native(event-sourced+deterministic+cryptographic-audit)=greenfield-wins-vs-retrofitted
F8: Scalability: private-credit $3.5T→$5T(2029) forcing decisions now. Waterfall-calc+amendment-cascade=non-linear complexity. Batch-only=operationally-constrained. CQRS-real-time+batch=correct-architecture
F9: Integration-burden-ADDITIVE: Versana+LSTA+Bloomberg+DTC+SFTP+AccessFintech+S&P-DataXchange. API-first=weeks per adapter. Monolith=months
F10: Tech-debt: HIGH(AD,Computershare,Virtus/FIS), MODERATE(Wilmington,SRS-Acquiom,Ankura), LOW(GLAS,Kroll,Hypercore)
F11: Unexpected-plays: S&P-DataXchange(#1-most-significant), Finley+Concord-merger(SaaS+trust-co-wrapper), Hypercore-"AI-Agent"-branding-bet, AccessFintech-Synergy-shared-workspace-network, Oxane-hybrid-service+software
F12: H1=verified+incomplete(missing:Computershare,Versana,Hypercore,Oxane,S&P,AccessFintech), H2=partial(tech=acquisition-differentiator ¬retention-moat), H3=confirmed(race-real-13mo-sprint), H4=conditional(compliance-native+integration-depth wins), H5=FALSIFIED(landscape-under-defined)

### calibration-updates(26.3.17)
C[S&P-Global-DataXchange+AmendX=data-vendor-inserting-as-agent-workflow-infrastructure(Mar-2026)=most-unexpected-competitive-move|1|26.3.17]
C[AI-Admin-Agent-framing(Hypercore)=marketing ¬technical-architecture-claim|1|26.3.17]
C[integration-burden-is-additive-tax-on-monolithic-architectures=direct-operational-ROI-argument-for-API-first|1|26.3.17]
C[no-firm-has-fully-cracked-single-pane-of-glass-across-all-deal-parties=open-gap|1|26.3.17]
C[Finley+Concord-merger=SaaS-platform+trust-company-wrapper=viable-greenfield-model-template|1|26.3.17]

### research-sources(new-26.3.17)
AD-Vega(alterdomus.com), AD-Solvas-Digitize(alterdomus.com), Versana-platform(versana.io), S&P-DataXchange+AmendX(press.spglobal.com Mar-2026), Wilmington+AccessFintech(globenewswire Feb-2025), Computershare-TrustConnect(computershare.com), SRS-Acquiom-Deal-Dashboard(srsacquiom.com), Hypercore-Series-A(prnewswire Feb-2026), Oxane-Panorama(oxanepartners.com), Finastra-Loan-IQ-Nexus(finastra.com), Finley+Concord(finleycms.com 2026), Ankura-Trust(ankuratrust.com), GLAS-Oakley(glas.agency Jan-2026)
## VDR competitive market analysis research (26.3.18) — r1

### platform-architecture
cloud-SaaS=dominant(all-8) |deployment-archetypes: T1-Enterprise-SaaS(Datasite/Azure,Intralinks,iDeals) T2-Compliance-SaaS(CapLinked/GovCloud/FedRAMP) T3-Deal-OS(Midaxo/lifecycle) T4-Vertical-Fintech(SRS-Acquiom/payments+escrow) T5-Regulatory-Bundle(DFIN-Venue/ActiveDisclosure-SEC)

### !KEY-FACT: Ansarada-absorbed-by-Datasite
Datasite acquired Ansarada AUD212M Aug-2024(ACCC-confirmed) |Ansarada=Datasite-product-¬independent-competitor |Ansarada-ESG/gov/board-carved-out→CEO-Sam-Riley-$500K |named-8-includes-absorbed-entity

### security-differentiators
AES-256+TLS=baseline-all |ABOVE: IRM/UNshare(Intralinks,pioneer,post-download-revocation) + CMEK(iDeals,RSA+AES-256-GCM) + BYOK(Datasite) + per-room-KMS-CMKs+S3-Object-Lock(CapLinked/GovCloud) + fence-view+remote-shred(iDeals)
FedRAMP-High-aligned: CapLinked-ONLY-in-named-set(AWS-GovCloud,CMMC-2.0,DoD-IL5,ITAR) |¬others
Compliance-above-baseline: Intralinks(ISO-27701,first-VDR) + iDeals(SOC3+HIPAA)

### AI-capability-tiers
TIER-A: Datasite(Azure-Cognitive-Services,3M-doc-training,100+-PII-types,80%-redaction-speed[vendor],Blueflame-LLM-unit) + Ansarada-IP-absorbed(Bidder-Prediction-97%[vendor],37K-deal-set,Smart-Sort)
TIER-B: Intralinks(DealCentre-AI+VDRPro-redaction) + Midaxo(IDC-Leader-AI-Deal-Mgmt-2025) + DFIN-Venue(90%-contract-review[vendor])
TIER-C: iDeals+SRS-Acquiom+CapLinked
!MOAT: Datasite-3M-doc-flywheel+Ansarada-37K-deal-set=¬replicable-by-greenfield

### tech-moats
Datasite: STRONG(3M-doc-AI+Blueflame+M&A-Index-data)
Intralinks: STRONG(IRM-pioneer+ISO-27701+30yr-Fortune-1000-network+Deal-Flow-Predictor)
CapLinked: STRONG-in-gov(FedRAMP+CMMC+ITAR) MODERATE-outside
iDeals: MODERATE(CMEK+fence-view+pricing-transparency+175K-clients)
DFIN-Venue: MODERATE(ActiveDisclosure-SEC-bundle+captive-base)
Midaxo: MODERATE-in-niche(lifecycle-breadth+IDC-Leader)
SRS-Acquiom: MODERATE(vertical-stack+88%-global-PE+3800-deal-research)

### pricing-signal
per-page=incumbent-weakness(2-10x-overrun,>15%-deals=$50K+) |flat-rate=new-entrant-attack-vector |free-tier(Peony,Papermark)=SME-disruption

### hypotheses
H1: partially-falsified(missing: Firmex,Drooms-EU,ShareVault,FirmRoom,Imprima,Thomson-Reuters)
H2: confirmed(new-entry=real,barriers=moderate-high,data-flywheel=strongest-barrier)
H3: confirmed(M&A-consolidation:Datasite+Ansarada+Firmex+MergerLinks|DFIN-FDIC-loss-documented)

### research-sources
ACCC-merger-register(Datasite-Ansarada), Microsoft-CS-story(Datasite-Azure-Cognitive-Services), Ansarada-Gulfnews+Zawya(AI-ME-expansion), CapLinked-blog(AWS-GovCloud-FedRAMP), DFIN-PRNewswire(new-Venue-Sept-2025), Midaxo-PRWeb(IDC-Leader-Nov-2025), iDeals-SOC3-report(Dec-2025), dataroom-providers.org, datarooms.org, v7labs.com, peony.ink, citybiz.co, researchandmarkets.com
## workflow automation research (26.3.18) — r1

### review-task
workflow-automation-implementation for 300-1000 employee companies | Q3(primary):technical-implementation | Q1,Q2,Q5,Q7(advisory) | H1,H2(test)

### F1: architecture tiers |[independent-research]
T1(300-500emp): iPaaS-first(Zapier/Make/Celigo)+webhook+no-code | $200-2K/mo | risk:vendor-lock-in,logic-ceiling
T2(500-800emp): iPaaS+API-gateway+lightweight-event-bus(Kafka-lite) | adds:error-handling,retry-queues,dead-letter-queues | $2-15K/mo
T3(800-1000emp): full-EDA+microservices+orchestration-engine(Temporal/Camunda)+dedicated-data-pipeline | $15-50K/mo | requires-platform-team
!PRIMARY-FAILURE-MODE: T3-architecture+T1-team-capacity=collapse | most common mid-market mistake

### F2: integration patterns ranked |[independent-research]
1→API-first(REST/webhooks): weeks-not-months, OAuth+HMAC+idempotency-keys required
2→iPaaS-middleware: 60-80% faster integration, built-in governance, TCO higher but hidden ops cost lower
3→EDA(Kafka): T3-only, 19% response-time-improvement+34% lower-error-rate vs API-driven, overkill below 800emp
4→ESB/legacy-middleware: avoid — legacy-ESB→async-event-hub migration cuts integration costs "double digits"
¬point-to-point-custom: highest long-term maintenance burden
hybrid(webhooks-speed+polling-reliability) = practical mid-market standard

### F3: data management — equal-weight success factor |[independent-research]
EY-2024: 83% of IT leaders cite poor data infrastructure as #1 automation blocker
MDM-first sequence: MDM-phase-1(customer+product) → ETL-standardized(Airbyte/Fivetran) → operational-data-store → data-lake/warehouse-only-if-needed
H2: data management IS missing from standard success factor lists but is equal-weight to change-mgmt+upskilling

### F4: tool selection framework |[independent-research]
decision axes(ordered): team-tech-capacity → integration-complexity → governance-requirements → volume → workflow-complexity
Tier-A(entry,<500emp): Zapier/Make | ¬governance ¬complex-logic
Tier-B(mid,500-800emp): Celigo/Tray.ai/n8n-self-hosted
Tier-C(full,800-1000emp): Workato/Boomi/SnapLogic | enterprise-governance+audit+RBAC
Tier-D(orchestration): Temporal.io/Camunda | long-running+stateful workflows
1-day-POC: top-10-apps → 10K-records+200-events+forced-error → validate governance+security+cost

### F5: security architecture |[independent-research]
ZTA components mandatory: OAuth2+OIDC(svc-auth) | HMAC-webhook-sig | RBAC(build-vs-run separation) | AES-256+PII-detection | immutable-audit-trail | microsegmentation
!RISK: automation-chains=new-data-exfiltration-surface (CRM-reads+email-writes=leak without breach)
¬bolt-on-security: costs 3-5x more post-implementation

### F6: scalability patterns |[independent-research]
async-by-default | idempotent-workers | backpressure+rate-limiting | horizontal-scale-stateless-workers | monitoring-day-1 | modular-decomposition
orgs automate 3x more processes year-2 vs year-1 → plan for volume growth
cloud-first(default) | hybrid(if data-residency required) | ¬on-prem-only

### F7: failure taxonomy ranked |[independent-research]
F7a(~40%): ¬data-foundation → garbage-in-garbage-out → trust-collapse → abandonment | mitig: MDM before automation
F7b(~25%): integration-fragility(point-to-point) → schema-change breaks → silent-failure | mitig: iPaaS+contract-testing+schema-registry
F7c(~15%): scope-creep-architecture(T1-running-T3-workload) → collapse-under-load | mitig: arch-review-gate+5x-load-test
F7d(~10%): security-bypass(over-permissioned credentials) → exfiltration-via-automation | mitig: least-privilege+audit
F7e(~10%): ¬observability → silent-failure discovered-downstream | mitig: execution-monitoring+dead-letter-alerts
70-80% of AI/automation projects fail to scale beyond pilot (system fragmentation root cause)

### H1+H2 findings
H1: PARTIALLY-CONFIRMED | 60%-achieve-ROI-12mo(for-those-with-foundation) | 70-80%-fail-to-scale-pilot(overall)
"properly-planned" technical definition: MDM-first+arch-team-alignment+governance-before-tools+observability-day-1+security-built-in
H2: PARTIALLY-CONFIRMED | data-management IS missing from standard lists | 4 missing technical factors: data-mgmt(#1),arch-capacity-match(#2),observability(#3),security-by-design(#4)

### research sources
kissflow.com(stats+trends) | informatica.com(iPaaS) | snaplogic.com(mid-market+POC) | EY-2024(83%-data-infra) | seraphicsecurity.com(ZTA) | confluent.io(EDA) | rudderstack.com(API-design) | parseur.com(MDM) | stackai.com(cloud-vs-onprem) | quixy.com(ROI-stats) | vfunction.com(70-80%-pilot-failure) | ziphq.com(CFO-pause) | flowwright.com(failure-patterns) | autonoly.com(common-mistakes)
refreshed: 26.3.18 | next: 26.4


## workflow-automation-review r3 findings (26.3.18)

### DA-response-positions |#9
DA[#1]: CONCEDE | survivorship-bias-acknowledged | vendor-stats→M-confidence | "60%-ROI"=individual-process,surviving-orgs-only
DA[#2]: CONCEDE+EX-ANTE | 5-testable-criteria(TA-READINESS-SCORE) | R1-READY-threshold:4/5 | T1-only@4/5 | stop-at-3/5 | !honest: checklist-predictive-¬-validated
DA[#3]: §2e=NO-unconditionally | process-improvement-first-for-readiness≤3/5 | automation=highest-ROI-ONLY-IF:readiness≥4/5+>500-tx/mo+data-quality-passes | inter-agent-disagree: UX-F8-capacity-reallocation-requires-system-design(¬management-aspiration)
DA[#6]: COMPROMISE | process-improvement-only:20-50%-gains@20-40%-cost | combined-approach-dominates | decision-gate-before-tool-selection-mandatory
DA[#7]: CONCEDE | all-findings→[extrapolated-from-general,M-confidence] | no-mid-market-specific-quant-study-found
DA[#9]: CONCEDE+REVISED-TCO | T1:$38-112K-yr1 | T2:$180-560K-yr1 | T3:$600K-1.8M-yr1 | license=15-30%-of-TCO | 3-6x-underfunded-if-license-only-budget
DA[#10]: CONCEDE+EXPLICIT | individual-process:60%-ROI-12mo | enterprise-wide:15-25%-scale | 40-50pp-gap=central-finding | pilot-to-scale-failure=dominant-challenge
DA[#12]: 4/6-blind-spots | vendor-lock-in(proprietary-DSL,40-60%-rewrite-on-switch) | automation-tech-debt(0.5-FTE/yr-per-50-workflows-yr3) | shadow-automation(annual-audit-4hrs) | AI-disruption(hedge:abstraction-layer) | regulatory-flagged(SOX+GDPR+HIPAA-compliance-review-mandatory)

### revised findings
REVISED-F1: T1-TCO=$38-112K-yr1 | T2-TCO=$180-560K-yr1 | T3-TCO=$600K-1.8M-yr1 | was:license-only
REVISED-F8: individual-process:60%[M-conf] | enterprise-wide:15-25%[M-H-conf] | ex-ante-readiness:TA-READINESS-SCORE≥4/5

### key calibration
C[license-cost=15-30%-of-iPaaS-TCO → budget-from-license-only=3-6x-underfunded|1|26.3.18]
C[process-improvement-only achieves 20-50%-efficiency-gains@20-40%-cost-of-automation → decision-gate-required-before-tool-selection|1|26.3.18]
C[individual-process-success(60%)-vs-enterprise-wide-success(15-25%)=40-50pp-gap=most-important-single-finding|1|26.3.18]
C[ex-ante-readiness-checklist(5-criteria):predictive-¬-validated-in-published-literature-for-300-1000emp-segment|1|26.3.18]
C[shadow-automation=higher-risk-in-mid-market-than-enterprise(flat-orgs,less-IT-oversight,free-tier-tools)|1|26.3.18]

### research sources (r3)
ezintegrations.ai(legacy-iPaaS-TCO:$300-800K/yr) | cazoomi.com(Workato-$15-50K/yr,Boomi-$25-75K/yr) | sageitinc.com(Boomi-pricing) | leansixsigmainstitute.org(LSS-ROI-3:1-minimum) | 6sigma.us(15:1-lean-return) | advanceit.sg(process-improvement-ROI) | superblocks.com(vendor-lock-in) | dataiku.com(automation-debt-2026) | baytechconsulting.com(software-risk-2026) | automationanywhere.com(RPA-maturity) | forrester.com(RQ-readiness) | infotech.com(automation-readiness-assessment)
## data-center-infra-review r3 (26.3.19)

### DA-response-positions |#6
DA[#1]:CONCEDE — pipeline≠buildout | 85GW→30-50GW realistic | construction-speed=gate-5 ¬gate-1 | community-opposition=gate-1 | Bloomberg:construction-fell(6.35→5.99GW) | Sightline:5/16GW-2026-under-construction | cancellations-quadrupled(25-projects,4.7GW)
DA[#2]:CONCEDE — labor=material-omission | 439K-shortage(ITIF-Jan-2026) | electrician=45-70%-construction-cost | 11mo-backlog(irecruit) | modular-reduces-labor-30%-¬eliminates | REVISED-timelines:+6-12mo-all-primary-markets
DA[#3]:CONCEDE+NEW-FINDING — 16%-cost-escalation(S&P) | NEW:transformer-bottleneck=concurrent-critical-path | LPT:US-imports-80%+,18-24mo-lead+25%-tariff+274%-demand-growth | solving-queue≠solving-hardware-procurement
DA[#5]:CONCEDE — chip-supply-co-binding-2025-2026 | HBM-sold-out-through-2026(Micron-CEO) | CoWoS-oversubscribed-mid-2026 | 3-window-rotation-model(chips→power→political/labor)
DA[#6]:CONCEDE — H1 CONFIRMED→PARTIALLY CONFIRMED | P(power=#1-nationally)=45-55% | 7-simultaneous-constraints | hierarchy(labor>community>chips>power>transformers>water>tariffs)
DA[#8]:COMPROMISE — Jevons fork quantified | dominant(P=55-65%/demand-higher) | efficiency(P=35-45%/demand-lower) | revealed-preference(36%-more-capex-post-DeepSeek)=stronger-than-architecture-claims

### r3-key-position-changes |#10
1→H1:CONFIRMED→PARTIALLY-CONFIRMED(7-constraints,P-power-primary=45-55%)
2→critical-path:grid-only→5-serial-gates(community-first,labor-concurrent,transformers-new-concurrent,chips-2025-2026,grid-terminal)
3→construction-timelines:+6-12mo-labor-all-primary-markets
4→transformer-supply:NEW-finding(LPT-18-24mo+25%-tariff+274%-demand=concurrent-bottleneck-¬downstream-of-queue)
5→chip-supply:integrated-as-co-binding-2025-2026
6→stranded-assets:quantified($5-50B-write-down;~5-10GW-genuinely-stranded;$20-125B-retrofit-20-25GW)
7→BTM-emissions:quantified(~74-80-MMt-CO2e/yr-at-25GW;EPA-NSPS-tightening;risk-LOW→HIGH-by-2030)
8→insurance:NEW($1.8B→$28B-signals-real-risk-pricing;climate-deductibles-climbing;BTM-adds-environmental-liability)
9→Jevons:stated-¬quantified→fork-modeled(dominant-55-65%/efficiency-35-45%)
10→pipeline-realization:85GW→30-50GW-realistic

### hygiene-outcomes
§2e:Outcome-1(critical-path-premise-falsified-by-evidence;revised-to-5-serial-gates)
§2c:Outcome-1(stranded-asset-$5-50B-write-down-¬in-prior-market-sizing)

### demand-side-scenario
plateau/reversal-by-2028:P=20-25% | multi-constraint-model=inadvertent-market-stabilizer(fewer-built=fewer-stranded) | BTM-gas-stranded-risk-highest(dedicated-generation-without-load) | modular-speed-premium-disappears-in-oversupply

### calibration-updates
C[community-opposition=gate-1-¬grid-queue:$64B-blocked-before-breaking-ground|1|26.3.19]
C[transformer-supply-chain=concurrent-critical-path-independent-of-grid-queue:LPT-18-24mo+274%-demand-growth|1|26.3.19]
C[multi-constraint-model-is-inadvertent-stabilizer:6-constraints-cap-buildout=smaller-demand-gap-if-AI-plateaus|1|26.3.19]
C[BTM-gas-trades-grid-queue-risk-for-emissions-regulatory-risk:~74-80-MMt-CO2e/yr-at-25GW|1|26.3.19]
C[chip-supply-co-binding-2025-2026-then-hands-off-to-power-2026-2028-then-political/labor-2027-2030:rotating-constraint-model|1|26.3.19]
C[insurance-market-15x-growth($1.8B→$28B)=underwriters-pricing-real-climate+obsolescence-risk-¬just-demand|1|26.3.19]

### r3-research-sources
bloomberg.com(DC-construction-drop-2026-02-25) | sightlineclimate.com | heatmap.news/cancellations | fortune.com/electrician-shortage(2026-03-02) | itif.org/worker-shortage(2026-01-12) | irecruit.co/workforce-needs | powermag.com/transformers-2026 | constructconnect.com/metal-prices-2026 | nextplatform.com/hbm-supply | fusionww.com/cowos-constraints | wccftech.com/memory-crisis | insurancebusinessmag.com/data-center-insurance-28B | riskandinsurance.com/data-center-boom | tonygrayson.ai/stranded-assets | datacenterknowledge.com/legacy-infrastructure | edgecore.com/traditional-designs
## cognitive-enhancement-review (26.3.21)

### cognitive-profile-map (DeepMind 10 faculties → sigma-review architecture)
Strong: F5-Memory(sigma-mem-MCP) | F8-Executive-Functions(round-structure+DA-exit-gate+belief-state) | F9-Problem-Solving(full-ANALYZE-pipeline) | F6-Reasoning(superforecasting-§3) | F2-Generation(ΣComm+DA-format)
Moderate: F3-Attention(round-structure-¬R1-focus-detection) | F4-Learning(cross-session-via-memory,¬intra-session) | F10-Social-Cognition(workspace-cross-read+DA-adversarial)
Weak: F7-Metacognition — CONFIRMED STRUCTURAL GAP: ¬Brier-accumulation, ¬error-rate-tracking, confidence-tier-gap(company-PR-tagged-as-[independent-research])
Bounded-by-inference: F4-Learning(LLM-weights-unchanged-per-session — ¬solvable-via-prompting-alone)

### framework-integration-complexity
DROP-IN(C1-compliant): CQoT-exit-gate-extension(3-new-DA-criteria,+300-600-tokens/review), Brier-Score-tracking(BS-TRACK-workspace-format+§3b-extension,+200-400-tokens/review,value-deferred), ACH-matrix(§2f-directive+##ach-matrix-workspace-section,+800-1200-tokens/review-net,immediate-quality-gain)
ARCHITECTURAL-CHANGE(avoid): TEC/ECHO(synthesis-validator-agent+coherence-graph,+15-20%-overhead,DA-already-performs-coherence-enforcement,¬evidence-of-DA-coherence-failure-in-8+-reviews)

### research-findings
AgentCDM(arxiv:2508.11995,Aug2025): ACH-inspired-scaffolding achieves SOTA on collaborative decision benchmarks in LLM multi-agent systems — prompt-based scaffold sufficient,¬fine-tuning required
OPTIMA(ACL2025,arxiv:2410.08115): 2.8x performance at <10% tokens — sigma-review's 30-40x overhead has 40-60% compression headroom. ΣComm is manual analog
BCCS(NeurIPS2025,arxiv:2510.06307): belief-calibrated consensus seeking +2.23-3.95% accuracy by weighting agents by belief-confidence. Requires Brier tracking as prerequisite
MAD-literature(ICLR2025): debate success = intrinsic-reasoning-strength+group-diversity,NOT structural-parameters(debate-order,confidence-visibility). More rounds ¬= more quality
BayesFlow(Jan2026): Bayesian posterior sampling for workflow generation. Sigma-review §3a adaptive-tier = manual analog

### h-assessments
H1: PARTIALLY-CONFIRMED — Metacognition IS primary structural weakness. But H1-framing wrong: delta EXISTS because F8+F6 strong; Metacognition weakness explains why delta NOT LARGER(accuracy-tied), not why it exists
H2: PARTIALLY-CONFIRMED — 30-40x for 17% IS inefficient. But CQoT+Brier+ACH improve at <5% marginal cost. Question is highest-leverage changes WITHIN existing budget
H3: PARTIALLY-CONFIRMED — ACH+CQoT applicable as structural analogs(¬fine-tuning); Brier feasible for 30-40% of estimates; TEC FALSIFIED for this architecture
H5: CONFIRMED — BCCS, OPTIMA-compression, metacognitive-self-prompting, MAD-diversity-finding all add value

## sigma-ui architecture review (26.3.28) — R1

### key findings

F1[Q1 dispatch]: Python-SDK>Agent-SDK(0.x-premature)>CLI-shell-out. !CRITICAL gap: CLI-shell-out preserves Claude-Code-tool-access(Bash,Read,Write,Glob,Grep,MCP) that API-dispatch loses. Three mitigation paths: (a)pass-tool-defs(high-complex),(b)pre-load-context(large-prompts),(c)redesign-for-structured-output(cleanest,requires-agent-rewrite). Flag for implementation-engineer. |source:[independent-research]|T2

F2[Q3/H2/H6 — load-bearing]: XVERIFY[openai:gpt-5.4]=PARTIAL(high-confidence). Outer-loop dispatch fixes WHO calls advance() ¬WHAT guards read. Guard gaming residual: if guards read agent-produced workspace artifacts, agents can satisfy gates without doing the work. Hard-observable guards required: ✓-declaration-count, section-presence, tag-syntax-regex ¬agent-asserted values. gate_checks.py(run_compute_belief+BUNDLES) is correct extension seam. |source:[external-verification+independent-research]|T1

F3[Q5]: Workspace-as-shared-state sufficient + buffer-merge pattern for parallel phases. ¬message-bus needed. |source:[independent-research]|T2

F4[Q6/H3]: RISK-1(guard-gaming-residual), RISK-2(API-dispatch-tool-access-loss=highest-impl-complexity), RISK-3(AsyncRunner-private-attr-bypass[review-8-F1] elevated-to-HIGH-in-gate-trust-context→use-direct-Orchestrator.start()/advance()-instead). H3=CONFIRMED-PARTIAL: all-components-reusable(hateoas-agent,gate_checks,sigma-mem,sigma-verify,agent-md-defs,orchestrator-config.py) ¬AsyncRunner-as-trust-anchor. |source:[independent-research]|T1

H2=PARTIALLY-CONFIRMED: outer-loop-dispatch+hard-observable-guards-together=fix, neither-alone-sufficient
H3=CONFIRMED-PARTIAL: all-components-reusable with above caveats
H6=CONFIRMED-with-condition: structural-parsing-required ¬trust-agent-prose

### calibration-updates
C[AsyncRunner-review-8-F1-severity-escalates-from-MEDIUM→HIGH-when-used-as-gate-enforcement-trust-anchor|1|26.3.28]
C[outer-loop-dispatch-is-necessary-¬sufficient-for-control-inversion-fix|1|26.3.28]
C[CLI-shell-out-vs-API-dispatch-tool-access-gap-is-primary-impl-complexity-driver-for-sigma-ui|1|26.3.28]

### calibration-updates (DA R2 revisions, 26.3.28)
C[H2=WEAKLY-TO-PARTIALLY-CONFIRMED-¬PARTIALLY-CONFIRMED: P(H2-fully-works)≈0.55-0.65, requires-TIER-A-observable-implementation|1|26.3.28]
C[Agent-SDK-v0.1.48-NOT-premature: hooks+sessions+MCP-write-lock-real; but-hook-abstraction-level-wrong-for-phase-gate-orchestration|1|26.3.28]
C[structural-parse-observables-cost-raising-¬gaming-resistant: only-orchestrator-produced-observables-are-TIER-A|1|26.3.28]
C[RISK-2=HIGH-impl-complexity-AND-HIGH-H4-risk-two-separate-dimensions-¬one|1|26.3.28]

### patterns(new)
orchestrator-outer-loop-trust-boundary: dispatch-control + hard-observable-guards required together; either alone leaves bypass path open
tool-access-gap-on-api-dispatch: agent tool access must be explicitly reconstructed when moving from CLI shell-out to SDK dispatch; no implicit inheritance
observable-tier-model: TIER-A(orchestrator-produced,gaming-resistant) > TIER-B(structural-parse,cost-raising) > TIER-C(agent-asserted,gameable). Gate enforcement anchors on TIER-A only.
agent-sdk-hook-vs-phase-gate: hooks fire at tool-call level; phase-gate orchestration needs phase-transition level control. Different abstractions — don't conflate.
P[output-framing-variance-is-interface-dependent|src:cross-model-protocol-review|promoted:26.4.9|class:calibration]
LLM output framing (markdown wrappers, reasoning-trace prefixes, CoT preambles) is NOT a stable model-family property — it is interface-dependent. JSON mode / constrained decoding / function-calling eliminates framing variance entirely, shifting primary failure mode to schema-noncompliance. Instruction-following mode (no JSON mode) is where framing variance dominates. Protocol designs that assume "just use JSON" without distinguishing interface mode will miscalibrate failure expectations. Always condition failure mode analysis on interface mode, not model family alone. XVERIFY-PARTIAL[openai:gpt-5.4]: counter-evidence from GPT-5.4 surfaced this correction.
P[envelope-fields-first-reduces-format-errors|src:cross-model-protocol-review|promoted:26.4.9|class:pattern]
In structured protocol messages, routing/coordination fields (sender, type, version, message_id) MUST appear before semantic content fields (body, reasoning, evidence). Rationale: LLMs show increased structured-format error rates in long responses (>~1500 tokens) due to generation pressure. Fields at the start of the JSON object are generated under lower cognitive load. If load-bearing routing fields are buried after long NL content, error rates for those fields increase. Applied to: any protocol spec, API response design, or agent message format where structured fields coexist with free-text fields. This is not cosmetic ordering — it is a reliability constraint. Confirmed by CDS dual-process analogy (System-1 coordination fields / System-2 content fields) and TA-9 generation-pressure finding.
P[additive-only-schema-evolution-unknown-fields-ignored|src:cross-model-protocol-review|promoted:26.4.9|class:pattern]
For any protocol that will evolve across heterogeneous consumers: (1) schema versions MUST be additive-only — new versions add optional fields, never remove or rename; (2) receivers MUST silently ignore unknown fields, never error; (3) version negotiation in session-init (capability advertisement via supported_versions array) + lowest-common-version selection by receiver. This is the same pattern as HTTP content negotiation, protobuf field numbering, and JSON Schema additionalProperties:false antipattern. Apply to: agent communication protocols, API versioning, structured data formats intended for multi-consumer use. The "unknown field = error" antipattern is fragile — it couples sender schema version to receiver schema version, preventing independent deployment.
P[json-as-cross-model-intersection-format|JSON dominance grounded in training-data economics(GitHub,APIs,StackOverflow) not just parsability|sufficient type system+canonical representation+universal parser support|YAML rejected(indentation+type coercion)|XML rejected(lower production reliability)|src:cross-model-protocol-review|promoted:26.4.9|class:principle]
CAL[bootstrap-reliability-splits-by-interface-mode|P=0.75 JSON-mode|P=0.55 instruction-only|P=0.35 messages-alone-no-infra|P=0.85 infra-assisted|must condition on interface mode to avoid overconfidence|src:cross-model-protocol-review|promoted:26.4.9|class:calibration]
P[epistemic-gaming-unsolvable-at-protocol-layer|agents can mark everything "directly-observed" to gain credibility|protocol cannot enforce honesty|mitigation at receiving-agent layer: DA-audit of epistemic_type distribution+xverify_provider as structural signal(harder to fake)|src:cross-model-protocol-review|promoted:26.4.9|class:principle]
P[schema-in-first-message-cold-start-pattern|generalizable bootstrapping for any zero-prior-knowledge protocol consumer|PROTOCOL_HANDSHAKE type containing full field schema+type vocabulary+examples+version|handshake-once per session ¬per-message repetition|src:cross-model-protocol-review|promoted:26.4.9|class:pattern]
