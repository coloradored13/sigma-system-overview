# tech-industry-analyst — agent memory

## methodology patterns

P[26.3.13] DA-learning: volume-conflation-bias|large aggregate numbers (stablecoin $33T, Solana $650B) obscure segment-specific relevance|always decompose by use-case before threat-sizing
P[26.3.13] DA-learning: testnet≠production|enterprise blockchain adoption shows consistent 2-3x timeline slippage+75% PoC failure|discount pre-production announcements for mgmt advisory
P[26.3.13] DA-learning: infrastructure-launch≠consumer-adoption|SWIFT retail, FedNow, blockchain rails all follow adoption curves measured in years ¬months|UK FP=best precedent
P[26.3.14] volume-conflation-confirmed: cross-domain pattern(WU stablecoin vol + LMS robot adoption)|aggregate numbers obscure segment dynamics
P[26.3.14] PINCER-detection: check BOTH ends—needy customers have incumbents?+reachable customers need it yet?|if yes+no=pincer
P[26.3.14] orchestration≠economics: orchestration gaps close fast(cloud-native)|economics=deeper domain modeling=longer window
P[26.3.14] legacy-assumption-trap: enterprise company≠legacy product|verify specific product arch before assuming constraint
P[26.3.14] planning-deployment-gap: "plan to adopt" overstates 2-3x|decompose breadth vs depth|can move opposite

## methodology calibration

P[26.3.18-r3] cyclical-vs-structural: M&A-correlated revenue dip ≠ competitive position loss|requires direct account defection evidence OR declining win rates OR deteriorating renewals to classify structural|Q4 recovery = cyclical confirmed
P[26.3.18-r3] single-event-classification-error: never classify trajectory from one event without checking subsequent earnings data|single loss alone = incomplete picture; loss + subsequent earnings together = correct picture
P[26.3.18-r3] AI-table-stakes-must-specify-tier: basic(commodity API) vs advanced(data-flywheel-trained) vs architectural AI have different commoditization timelines|single undifferentiated "table stakes by X" claim is analytically under-specified
P[26.3.18-r3] AI-premium-phased-model: EA premium(now=Phase 1) + table-stakes claim(future=Phase 2) are consistent when phased|logical tension = spec error not analytical contradiction

## cross-review methodology patterns

C[26.3.28] benchmark-contamination-vigilance: SWE-bench Verified inflates apparent progress vs SWE-bench Pro (81% vs 46% same model) | always check for benchmark contamination when citing AI capability claims

P[26.3.28] benchmark-contamination-detection: when AI capability claims cite benchmark scores, always check for decontaminated variant | capability benchmarks with public training data overlap systematically overstate progress | apply to any future AI capability review
P[26.3.28] two-speed-S-curve: technology adoption runs two simultaneous S-curves at different speeds | TOOL curve: individual adoption in weeks/months | ORG curve: org-wide transformation in 10-12yr (internet/cloud reference class) | conflating these produces both false urgency (ORG) and false complacency (TOOL) | apply whenever analyzing technology disruption impact on knowledge workers
P[26.3.28] bessen-paradox-conditions: task automation + elastic demand = augmentation + headcount growth (spreadsheets, ATMs) | task automation + inelastic demand = role bifurcation (senior augmented, junior compressed) | do not assume compression by default; first test demand elasticity for the specific role/sector | apply to any labor market disruption analysis
P[26.3.28] benchmark-category-error: coding/structured-task benchmarks (METR, SWE-bench) do not predict capability gains in ambiguity-heavy, relationship-dependent, success-criteria-absent work | always check whether benchmark domain matches the work domain before extrapolating
P[26.3.28] xverify-note: Gemini 3.1 has training-cutoff artifact on specific frontier model version names — flagging as XVERIFY-FAIL on specific benchmark claims ¬underlying trend; GPT-5.4 more reliable for this domain
R[26.4.22] AI-agent-rollout-playbook-vet (R1):
TOP-FINDINGS:
F[TIA-3] guardrails-data-sovereignty: Lakera/Azure/Bedrock = vendor API sub-processors; LLM Guard = self-hosted zero-exfil | BOTH docs collapse this distinction | H4 PARTIALLY FAILS
F[TIA-4] H8-framework-maturity: Claude Agent SDK 12-mo stability guarantee (Nov 2025); LangGraph v0.3 stable; pushback#5 mechanism WRONG (it's governance elapsed-time, not framework immaturity) | H8 PARTIALLY CONFIRMED
F[TIA-7] MCP-server-build-cost: 3-6wk/server × 3-8 servers = 10-50wks unbudgeted in both cost models | H4 PARTIALLY FAILS | H2 UNDERSTATED
F[TIA-8] gateway-EU-residency: Bedrock/Azure Foundry US-default; self-hosted LiteLLM EU-VPC = only clean path for EU customer data | H4 PARTIALLY FAILS
F[TIA-2] Statsig: acquired by OpenAI → dual-vendor concentration risk; conflict-of-interest in feature-flag + model-provider
F[TIA-6] time-to-hire: 14-18wk median for Senior AI Platform Engineer → Phase0→1 transition risk

HYPOTHESIS-DISPOSITIONS: H4=PARTIALLY-FAILS(5-negatives) | H5=FALSIFIED(confirmed by TA) | H8=PARTIALLY-CONFIRMED | H3=headcount-OK-comp-low | H2=cost+timeline UNDERSTATED

METHODOLOGY-PATTERNS:
P[26.4.22] guardrails-as-sub-processors: always categorize guardrails vendors by data-handling class (API-exfil vs self-hosted) before recommending | cross-domain pattern: applies to eval platforms, observability backends, any tool that processes prompts
P[26.4.22] framework-maturity-vs-governance-elapsed-time: distinguish these constraints when evaluating compression-pressure pushbacks; framework maturity accelerates build; governance constraints are elapsed-time not engineering-time
P[26.4.22] vendor-acquisition-TPRM: mid-contract vendor acquisitions are material TPRM events; docs should specify how to handle (re-evaluate, update sub-processor disclosures, update NYDFS Part 500 vendor inventory)

XVERIFY: FAIL[both providers] tool-not-found despite init=ready | pattern: sigma-verify sub-tools not registering as callable tools in this session
R[26.4.22] AI-agent-rollout-playbook-vet — POST-DA promotion entries:

## methodology patterns (generalizable)

P[26.4.22] guardrails-data-sovereignty-split: when reviewing AI infrastructure vendor lists, always split by data-handling class BEFORE by function — API-exfiltrating (Lakera/Azure AI Content Safety/Bedrock Guardrails) vs self-hosted zero-exfil (LLM Guard) are categorically different compliance decisions for NYDFS/GDPR/HIPAA firms | cross-domain: applies to eval platforms (Langfuse self-hosted vs Braintrust cloud), observability backends, any tool that processes prompt content

P[26.4.22] framework-maturity-vs-governance-elapsed-time: distinguish these two distinct timeline constraints when evaluating AI platform build timelines — framework maturity is an engineering-build variable (6-8 weeks, compressible with mature SDKs); governance elapsed time (SME eval construction, vendor agreement negotiation, shadow mode stabilization) is non-compressible regardless of framework choice | apply whenever reviewing timeline-compression pushback claims

P[26.4.22] vendor-acquisition-TPRM: mid-contract vendor acquisitions by strategic competitors (e.g. Statsig by OpenAI) are material TPRM events that create dual-vendor concentration risk and potential conflict-of-interest in feature-flag data | neither doc reviewed addressed this pattern; add to vendor-risk section of any future AI infra review

P[26.4.22] MCP-build-cost-hidden: firms following production-grade MCP posture (no community servers; internal servers require SAST/SCA + version-pinning + allowlist proxy) must budget 3-6 weeks/server × 3-8 servers = $75-400K unbudgeted in standard AI infra cost models; flag in any cost-model review

P[26.4.22] consultancy-COI-governance: AI infrastructure consultancies that build systems then validate them carry authority-bias risk at committee tier-promotion meetings — equivalent of auditor independence problem; neither reviewed playbook identifies this; add to governance-design checklist

P[26.4.22] pushback-doc-split: when a claim is about "both docs," always verify per-doc with source line numbers before asserting — DA[#3] revealed SaaS Pushback #9 already endorsed the exact frameworks my finding claimed were absent; financial addendum Pushback #5 did not; conflating both = overstatement

## calibration updates

C[26.4.22] eval-platform-segmentation: Langfuse (Apache 2.0 self-hosted, data-sovereignty), Braintrust (enterprise-managed, best judge UX), LangSmith (LangGraph lock-in risk), Inspect AI (peer-reviewed adversarial eval, regulatory red team docs) — not interchangeable; select by data-handling requirement FIRST

C[26.4.22] gateway-EU-residency: Bedrock and Azure AI Foundry route to US by default for Anthropic models; self-hosted LiteLLM in EU VPC is currently the only clean path for GDPR Art.44 compliance on model API calls; "data residency is binding" principle in both reviewed docs was not applied to the gateway layer itself

C[26.4.22] talent-market-2026: Senior AI Platform Engineer US major markets = $280-380K total comp; Senior AI Application Engineer = $220-300K total comp; time-to-hire 14-18 weeks median; Phase 0 Week-6 hire assumption in standard playbooks is optimistic by 8-12 weeks at median

## DA engagement pattern

P[26.4.22] source-tag-on-DA-revision: when DA challenge produces a finding revision, update source tag to include [prompt-claim:re-read-with-DA-evidence] to preserve provenance chain — this distinguishes DA-driven revisions from original independent-research findings; DA-2 acknowledged this as correct practice
R[k-shape-opportunities-2026-05-17] AI-shovel-layer-map R1:
TOP-FINDINGS:
F[TIA-1] physical-layer-captured: NVIDIA 80-92% AI accelerator share→75% by 2026; HBM sold out through 2026 (SK Hynix 53-62% share); hyperscaler AI capex $600-700B 2026 up 60-63% YoY; foundation model layer closed (open-weight commoditizes base capability); inference infra $50M-$1B+ capital floor. H4 CONFIRMED on physical layer. |source:[independent-research:T2] BELIEF=0.90
F[TIA-2] power-grid-second-order: SMR offtake agreements for AI data centers 25→45 GW (2024-2026 new phenomenon); IEA confirms data center demand surge; PPA structuring/site selection/SMR advisory = solo-accessible niches requiring pre-existing domain expertise. |BELIEF=0.60
F[TIA-3] service-layer-open: agent/workflow frameworks saturated at generic level (LangChain 100K+ stars, Claude SDK stable); vertical-specific agent products OPEN at ~$0 capital floor; EU AI Act compliance consulting EARLY cycle (Aug 2026 full application deadline); eval/observability consolidating (Braintrust $800M, Arize $70M Series C, Langfuse→ClickHouse). |BELIEF=0.85
F[TIA-4] ai-consulting-rates: $150-500/hr; vertical specialist 30-50% premium; BCG $3.6B AI consulting 2025; 26.2% CAGR market; YC warning: generic positioning fails; mid-market B2B more solo-accessible than regulated verticals (compliance structure requirements gate solo entry to healthcare/legal). |BELIEF=0.72
F[TIA-5] disconfirming-ROI: MIT 2025 95% of pilots deliver zero P&L impact; IBM 25% of initiatives delivered ROI; 74% struggle pilot→production; S&P Global 42% abandoned AI projects in 2025. Enterprise ROI crisis = BOTH risk (budget pullback 2027-2028) AND opportunity (need deployment help). Wells Fargo May 2026 calls AI capex "euphoric bubble" — contradicted by operational hyperscaler guidance.

HYPOTHESIS-DISPOSITIONS: H4=CONFIRMED (physical layer captured, service layer open). H6=CONFIRMED (services/products not infrastructure for solo operators). Generic AI consulting=saturating; vertical-specialist=EARLY-MID cycle.

DB-REVISIONS: DB[TIA-4] revised recommendation from "regulated verticals" to "mid-market B2B with domain specificity" — regulated verticals have compliance structure requirements (HIPAA org structure, FINRA registration) that gate solo entry beyond mere knowledge.

METHODOLOGY-PATTERNS:
P[26.05.17] physical-infra-layer-closed-both-directions: solo operator in AI physical compute layer faces double risk — "not enough supply" (can't get NVDA allocation priority vs hyperscalers) AND "too much supply" (inference efficiency gains could collapse GPU spot prices). Physical layer avoidance is correct from both supply scarcity AND efficiency gain scenarios.
P[26.05.17] credential-structure-vs-knowledge-moat: regulated industry verticals (healthcare, legal, finance) have TWO distinct entry barriers — domain knowledge (learnable) AND organizational compliance structure (requires entity formation, licensing, registration). Solo consultants often have the knowledge but lack the structure; target mid-market B2B to avoid structural barrier.
P[26.05.17] generic-vs-vertical-saturation-distinction: "AI consulting" is saturating; "AI automation for property managers" is not. Always decompose service-layer market by vertical specificity before assessing saturation — generic positioning saturates; vertical-specific positioning has much longer runway.

XVERIFY: UNAVAILABLE (sigma-verify sub-tools not loadable in agent context) | sigma-retrieve cross-source convergence substituted per §2h
PEER-VERIFY: economics-analyst PASS (F[EC-1] source tier appropriate; F[EC-2] §2a hygiene substantive; F[EC-3] asset-wealth-as-primary-driver = load-bearing [agent-inference] — flagged for DA)
P[26.05.17-r2] label-saturation-cascade-speed: service-layer opportunity labels (e.g. "AI consulting" → "vertical AI consulting" → "mid-market B2B AI consulting") saturate as consensus in <18 months | the defensible position is NOT the label but PRIOR CUSTOMER NETWORK + SPECIFIC IMPLEMENTATION DEPTH at sub-vertical level | "Yardi-API workflow agents for 50-200 unit operators" ≠ "mid-market B2B AI consulting" even though the latter label describes the former | apply: when analyzing service-layer opportunities, always decompose to whether defensibility comes from label OR from pre-existing relationships + depth-of-implementation knowledge | DA[#6] confirmed via k-shape-opportunities-2026-05-17 |src:R-2026-05-17-k-shape-opportunities|promoted:2026-05-17|class:pattern
C[26.05.17-r2] secondary-market-GPU-arbitrage-conditional: AI physical compute layer ("Solo entry: NONE" in 2026 primary market) has a conditional 2027-2028 secondary-market window | trigger: ≥2 hyperscalers publicly cut AI capex guidance >20% | if triggered: distressed GPU fire-sale opens entry at $200K-$1M capital floor | monitoring signal: capex GUIDANCE cuts (not GPU spot prices — prices lag guidance by 6-9 months) | distinguish from efficiency-gain scenario (DeepSeek-style): efficiency gains → gradual spot-price softening over 2+ years; ROI-failure scenario → abrupt fire-sale in 6-12 months | BELIEF[window-opens-if-trigger]=0.35 | apply: any AI infrastructure opportunity analysis where primary market is capital-locked — always check for distressed-secondary-market scenario as conditional carve-out |src:R-2026-05-17-k-shape-opportunities|promoted:2026-05-17|class:calibration
P[26.05.17-r2] demand-profitability-belief-split: when evaluating a niche opportunity, demand-timing and profitability/margin are distinct claims requiring separate BELIEF scores and separate evidence | common failure mode: asserting single high-conviction BELIEF where demand signal is strong (regulatory mandate, compliance deadline, verifiable external driver) but price/margin signal is absent | §2i precision gate violation: treating demand-certainty as sufficient to assert "highest-conviction niche" when margin is unverified | correct form: BELIEF[demand-timing]=X based on [evidence]; BELIEF[margin-potential]=Y based on [separate evidence or GAP] | applies to: any opportunity with mandate-driven demand (regulatory compliance, insurance requirements, legal requirements) where the demand driver does not reveal willingness-to-pay | DA[#13] identified this error in EU AI Act compliance consulting analysis |src:R-2026-05-17-k-shape-opportunities|promoted:2026-05-17|class:pattern
R[sustainable-ai-power-2026-05-22] AI-compute-power-sourcing R1:
TOP-FINDINGS:
F[TIA-1] demand-supply-gap: IEA global DC demand 485 TWh/2025→945 TWh/2030 | US 325-580 TWh by 2028 (LBL) | inference=75-80% of AI energy share by 2030; training=concentrated <50 sites | gap=operational-demand-NOW vs contracted-clean-supply-2027-2030+ | CAL[US-2028]: point=450 TWh |80%=[325,580] | overestimation risk: historical DC forecasts overshot 30-50%; maintained because LLM-era training compute ~4x/yr outpaces efficiency ~2x/yr |source:[independent-research:T1]
F[TIA-2] nuclear-PPA-announced-vs-operating: >10 GW nuclear PPAs signed 2024-2025 | ONLY TMI (835 MW) CONTRACTED with near-term delivery (2027 ahead of schedule) | all SMR deals (Google/Kairos 500 MW, AWS/X-energy ~300-500 MW) = announced/pre-contracted, first delivery 2030+ | zero commercial SMRs operating US | Vogtle Units 3&4 precedent: conventional LWR 7yr late $17B over; SMR risk = higher not lower | 10 GW announced ≠ 1-2 GW realistically operating 2030 | BELIEF[10GW-by-2030]=0.10; BELIEF[1-2GW-by-2030]=0.65 |source:[independent-research:T1-T2]
F[TIA-3] hydrogen-null-finding: green-H2 appropriately deprioritized NOT overlooked | costs $4-8/kg vs $1.5-3/kg parity target | LCOE $80-150/MWh vs gas $50-80/MWh | Amazon explicitly tried+abandoned Bloom Energy fuel cell deployments | MS hydrogen = 48hr proof-of-concept not production | $7.65B "fuel cell deals" Oct-Jan 2026 = primarily gray/blue H2 SOFC, not green-H2 | 45V IRA credit ($3/kg) required for any near-term economics | BELIEF[green-H2-viable-data-center-before-2030]=0.15 | C3 null finding per instructions |source:[independent-research:T2]|source-bias:[framing-capture] on vendor claims
F[TIA-4] FERC-queue-dominant-barrier: PJM interconnection wait risen from <2yr (2008) to 8+yr (2025) | ~2300 GW generation seeking US grid connection | Northern Virginia utilities pausing new grid connections | dominant reason for all new-generation non-pursuit; also explains BTM/co-location race |source:[independent-research:T1]
F[TIA-5] training-inference-asymmetry: training at <50 sites = monopsony PPA power for BTM nuclear/geothermal co-location | inference edge = grid-dependent retail buyers | under-pursued opportunity: advanced geothermal (Fervo EGS) in Basin-and-Range geology for training campus operators | geography-limited but highly suitable for always-on baseload |source:[independent-research:T2]

HYPOTHESIS-DISPOSITIONS: H1=CONFIRMED-WITH-CAVEAT (gap real; upper bound overestimated). H2=NULL-FINDING (green-H2 appropriately deprioritized). H3=PARTIAL (geothermal for training sites = genuine under-pursuit; nuclear consensus bet). H4=CONFIRMED (FERC queue=#1 overall; economics=#1 for H2 specifically).

XVERIFY: XVERIFY-FAIL[openai]: verify_finding tool not separately loadable in this session (sigma-verify sub-tools schema not available as deferred tools) | same pattern as prior reviews | gap on F[TIA-2] announced-vs-operating taxonomy

METHODOLOGY-PATTERNS (R3 additions):
P[26.05.22-r3] water-axis-flips-nuclear-vs-EGS: multi-axis sustainability analysis (water + carbon) produces DIFFERENT technology ranking than carbon-only analysis | nuclear SMR cooling-tower ~600-800 gal/MWh; EGS closed-loop ~0.1-0.3 gal/MWh | for water-stressed siting (TX/AZ/NV, Colorado-River-basin), EGS closed-loop is superior on BOTH carbon AND water axes | gas+CCS counterintuitive: low-carbon-aspiration but water-intensive (~230-500 gal/MWh amine scrubbing) | apply: any energy-infrastructure analysis in water-stressed geography must run carbon + water axes separately before ranking technologies |src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:calibration

P[26.05.22-r3] curtailment-absorption-training-co-location: AI training campuses co-sited with high-curtailment zones (ERCOT West TX, CAISO Mojave CA) can source 20-40% of annual training energy at near-$0 marginal cost | TX 2024 curtailment ~5.3 TWh; CA 2024 ~3.4 TWh (EIA) | curtailment-shift stack: ~$5-15/MWh vs $60-110/MWh standard firm-renewable stack | structural constraint: curtailment is geographically concentrated — remote campus CANNOT absorb without co-location or new transmission | checkpoint-restart overhead ~10-30% for interrupted training runs | policy lever: FERC interruptible-load classification for AI training = zero hyperscalers have structured this | apply: when evaluating training campus siting options, curtailment-proximity is an under-utilized LCOE lever |src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:pattern

C[26.05.22-r3] CFE-365-hourly-matching-explains-nuclear-PPA-race: Google+Microsoft CFE-365 (100% hourly carbon-free by 2030) is the structural driver of the nuclear/geothermal PPA race — NOT just baseload preference | annual REC-matching satisfies annual-average commitment; CFE-365 requires EVERY HOUR to be matched | 4h BESS + grid-forming inverters improve hourly score but cannot cover multi-day/seasonal gaps | only firm clean generation (nuclear, geothermal, hydro) covers those gaps | implication: hyperscalers with CFE-365 commitments are structurally differentiated buyers from annual-REC operators; pricing, contract terms, and technology choices differ materially | apply: distinguish CFE-365 buyers from annual-REC buyers before analyzing hyperscaler clean-energy procurement strategy |src:sustainable-ai-power-2026-05-22|promoted:2026-05-23|class:calibration

METHODOLOGY-PATTERNS:
P[26.05.22] announced-contracted-operating-taxonomy: when evaluating clean-energy supply for data centers, ALWAYS decompose: ANNOUNCED (LOI/term sheet/RFP) vs CONTRACTED (signed PPA with financial commitment) vs OPERATING (kWh actually delivered) | >10 GW nuclear announced in 2024-2025; only ~1-2 GW operating-by-2030 is defensible | failure to distinguish = supply-side gap wildly underestimated
P[26.05.22] null-finding-from-vendor-framing: hydrogen fuel cell "promise for data centers" is primarily a Plug Power/FCHEA advocacy narrative, not independent analysis | Amazon's reported abandonment of Bloom deployments is the correct signal over vendor claims | when a technology's "promise" narrative originates predominantly from companies who benefit from that narrative being believed, apply [creator-on-creation]+[framing-capture] bias probes before accepting
P[26.05.22] training-inference-power-asymmetry: training and inference face structurally different power-sourcing problems | training (<50 concentrated sites, 500+ MW each) = can negotiate BTM/co-location deals, has monopsony power | inference (distributed edge, grid-dependent) = price-takes local utility carbon mix | analysis of "AI power sustainability" that treats all AI workloads the same misses this bifurcation | bifurcation has policy implications: training operators can be regulated/incentivized differently
