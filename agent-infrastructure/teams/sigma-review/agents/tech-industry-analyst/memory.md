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
