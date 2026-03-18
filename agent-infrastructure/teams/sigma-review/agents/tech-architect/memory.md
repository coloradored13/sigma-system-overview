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
multiple-instance-convergence: when I reviewed as 3 separate instances, all found path-traversal independently → high-confidence signal
hateoas-agent-framework: handles action advertisement automatically — don't flag handler-level navigation as missing HATEOAS
team-memory-as-files: simple file-based persistence scales to ~5 agents, shared files need coordination beyond that
sigma-mem-team-gap: RESOLVED review-7 — bridge implemented (issue-14), _build_agent_boot provides one-call boot package with 8 data fields, team search/write actions wired through MCP
_state-magic-key: implicit conventions are harder to maintain than explicit types for published APIs
optional-deps-for-providers: framework should work without any specific LLM provider installed
protocol-incomplete: RESOLVED review-7 — HasHateoas Protocol now includes filter_actions, get_transition_metadata, validate (confirmed in registry.py:18-43)
delta-review-severity-decay: review-4(9)→review-5(3)→review-6(3-minor)→review-7(1-medium+5-trivial/advisory) — 7 rounds confirms diminishing-returns convergence, only cross-repo/doc issues remain
mcp-vs-runner-consistency: RESOLVED review-6 — MCP server now sanitizes error messages (mcp_server.py:115-119)
concurrent-workspace-writes: review-7 workspace.md had 5+ agents writing simultaneously — atomic Write needed over incremental Edit for shared files under contention

¬[over-engineering concerns — sigma-mem is 1,382 LOC but all functional, no dead code]
¬[security regressions in review-7 — path traversal, arrow injection, MCP error sanitization all solid]
¬[arch regressions in review-7 — HATEOAS contract, state machine wiring, bridge implementation all clean]

## team decisions
arch:weighted-state-detection, arch:path-validation-via-resolve (both for sigma-mem)
product:alpha-quality-reached for sigma-mem, blocker: hateoas-agent must publish first

## team patterns
review-rounds-converge: round-1=correctness, round-2=polish, round-3+=diminishing returns (confirmed through review-7: 7 rounds, only trivial/advisory findings remain, all substantive issues resolved)
agent-overlap-valuable: tech+ux catch different aspects of same issue
delta-review-format-effective: checking previous findings systematically works well, prevents re-flagging resolved issues
cross-agent-confirmation: review-7 had 5 agents, confirmed Resource.required bug found by code-quality-analyst + URL mismatch by product-strategist + doc issues by technical-writer — peer-validation strengthens findings
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
R[cloud-arch-wms:Manhattan 250 microservices K8s REST|refreshed:2026-03-14]
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

### cross-agent
PS:strong|tension(integration-cost-overestimate,MVP-timeline-reducible)
TIA:strong|WES-squeeze=addressed(adjacent-positioning)

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

→ actions:
→ r3+ → synthesis
→ next research → VDA5050-v2.2, Open-RMF-adoption, Python-FastAPI-warehouse
