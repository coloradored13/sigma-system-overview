# reference-class-analyst — personal memory

## identity
role: reference class forecasting and calibration specialist
domain: base-rate-analysis,superforecasting,reference-class-forecasting,Bayesian-reasoning,calibration,decomposition,historical-analogues,pre-mortem,prediction-markets,outside-view
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)
## SVB risk analysis r1 findings (2026-03-17)
task: SVB risk profile as of 2023-01-31 | temporal-boundary enforced
SQ[1-5] decomposition: 5 sub-questions | 3×outcome-1(changed) | 2×outcome-2(confirmed) | 1×outcome-3(gap)
RC[1-4]: unconditional 0.14%/yr | high-uninsured 100% distress (N=1) | S&L 32% | tech-concentrated=GAP
ANA[1-5]: WaMu(failure) | IndyMac(failure) | Continental Illinois(bailout,most relevant) | Schwab(survival) | S&L industry(systemic)
CAL: P(adverse,12mo)=45-55% | P(failure,12mo)=15-25% | P(run>20%/30d)=20-30%/Q | P(stock>50%down)=30-40%
PM[1-4]: capital raise spiral(25-30%) | slow bleed(20-25%) | info cascade run(15-20%) | rate rescue(10-15%)
OV-RECONCILIATION: market implied <2-3% failure | reference-class 15-25% | 5-10x divergence
key-insight: all risk info was PUBLIC pre-cutoff — market failure = normalcy bias + accounting mask + correlated-withdrawal underestimation
cross-agent: aligns w/ macro-rates F3 (HTM losses), portfolio-analyst F4 (capital adequacy), product-strategist F3-F4 (deposits+correlation)
DA challenges flagged: multiplicative adjustment methodology | survivorship bias | S&L analogy validity | RC[2] N=1
## SVB R3 response (2026-03-17)
DA[#3] P(failure): REVISED 15-25%→5-12% (point ~8%) | methodology: multiplicative→additive Bayesian | conceded: multiplicative unsound, short interest ¬existential, no examples >10% CET1+IG failing w/o sudden trigger | disputed: well-capitalized framing (FDIC Hoenig: 98% failed banks were well-capitalized pre-GFC) + trigger-as-exogenous framing
DA[#4] Continental: DEMOTED "most relevant"→"partially informative" | conceded 4/5 structural differences | RC[2] abandoned as quantitative anchor | Schwab elevated as survival comparator
DA[#5] S&L: CONCEDED all 4 structural differences | 32% rate abandoned as quantitative input | retained qualitative pattern only
hindsight self-assessment: ~2x overestimate in R1 | multiplicative method outcome-anchored | "KEY INSIGHT" was most contaminated sentence
calibration lesson: P[additive-Bayesian-updating superior to multiplicative-adjustment for base-rate forecasting|src:SVB-review-R3|class:calibration]
P[well-capitalized-regulatory-status is weak predictor of survival (FDIC Hoenig: 501/510=98% of GFC failures were well-capitalized)|src:SVB-review-R3|class:pattern]
P[deposit-concentration (uninsured%) is stronger failure predictor than capital ratios in liquidity crises|src:SVB-review-R3|class:pattern]
## research
R[superforecasting-methodology:{1}GJ superforecasters 30% more accurate than prediction markets avg 2024-2025(FT)|{2}core methods: Fermi decomposition, reference-class outside-view, extremizing aggregation, accuracy-weighted teaming|{3}superforecasters beat Fed futures in 2023+2024+2025|{4}Brier 0.135 vs Polymarket 0.159 across 1756 daily forecasts (18% better)|{5}key traits: cautious, humble, actively open-minded, high need-for-cognition|{6}World Ahead 2026 contributions (Starship, US midterms, tariffs, Russia-Ukraine)|{7}longer-horizon (12mo+) structured expert panels outperform markets; markets better for short-term event-driven|src:goodjudgment.com,goodjudgment.substack.com,futuratty.com,edge.org|refreshed:2026-03-17|next:2026-06-17]

R[reference-class-forecasting:{1}2025 systematic lit review (Tandfonline) covers 2001-2025, 74% of articles since 2015—adoption expanding but validity/applicability questions remain|{2}Oxford Global Projects database: 16K→20K megaproject entries from 136 countries (world's largest)|{3}base rates: 91.5% of megaprojects over budget/schedule, only 8.5% meet cost+schedule targets, mean cost overrun 62%|{4}fat-tail sectors: IT, nuclear storage, defense, Olympics, nuclear power, dams (overruns up to 600%)|{5}low-risk sectors: solar, wind, thermal power, electricity transmission, highways|{6}RCF adopted by UK, Denmark, US, China, Australia governments|{7}gap: limited off-the-shelf RCF tools for non-infrastructure domains (finance, tech, startups)|{8}ScienceDirect 2024 paper addresses RCF when adequate project data unavailable|src:tandfonline.com/doi/10.1080/09537287.2025.2578708,oxfordglobalprojects.com,sbs.ox.ac.uk,arxiv.org/pdf/1409.0003|refreshed:2026-03-17|next:2026-06-17]

R[prediction-markets:{1}CFTC Feb 2026: withdrew proposed ban on political+sports event contracts, signaled new rulemaking for "clear standards"|{2}Kalshi: federally compliant DCM, operates in 42+ US states, won federal court rulings in DC/NJ/TN on preemption|{3}Polymarket: acquired QCEX for $112M (late 2025) to re-enter US, still invite-only waitlist, state-level battles continue|{4}state vs federal conflict: MA state court ruled against Kalshi (Jan 2026), NV gaming board sued Polymarket (Jan 2026), likely headed to Supreme Court|{5}Metaculus launched FutureEval (Feb 2026)—continuously updated AI vs human forecasting benchmark|{6}cumulative trading volume $27.9B Jan-Oct 2025|{7}Metaculus projections: AI surpass community by Apr 2026, Pro Forecasters by mid-2027|{8}markets outperformed polls in 74% of US election forecasts (2024)|src:hklaw.com,sidley.com,goodjudgment.com,metaculus.com,predictionmarket.tools,forecastbench.org|refreshed:2026-03-17|next:2026-06-17]

R[bayesian-reasoning-tools:{1}BayesiaLab: commercial platform for Bayesian network modeling (market research, healthcare, policy)|{2}Python ecosystem: agrum (graphical models), bnlearn (structure learning+inference), PyMC, Stan, NumPyro|{3}Squiggle: open-source probabilistic programming language by QURI for intuitive estimation—readable syntax, JS-embeddable, no Bayesian inference support|{4}Squiggle Hub: platform for sharing probabilistic models, Squiggle AI generates models via LLM|{5}probabilistic programming frontier: PyMC, Stan, NumPyro for full Bayesian inference; Squiggle for rapid prototyping|{6}industrial applications expanding: FMEA integration, causal modeling, risk assessment in large-scale datasets|{7}future directions: probabilistic programming, likelihood-free inference, Bayesian neural networks|{8}gap for team-review context: no turnkey Bayesian tool for structured analytical forecasting teams—requires custom integration|src:bayesia.com,squiggle-language.com,squigglehub.org,arxiv.org/pdf/2503.17025,projecteuclid.org/doi/10.1214/23-STS907|refreshed:2026-03-17|next:2026-06-17]

R[calibration-research:{1}expert overconfidence persistent: 16,559 economic forecasts showed 53% self-reported confidence but only 23% accuracy|{2}effective debiasing: accuracy incentives, probability scale training, practice+feedback (frequent, timely, unambiguous)|{3}2026 SMJ paper distinguishes overestimation vs overprecision as separate biases with different firm performance impacts|{4}RCF (outside view) remains primary debiasing tool—forces comparison to base rates vs inside-view optimism|{5}briefings on policy/economic/social factors produce wider (better-calibrated) forecast intervals|{6}GJ Project finding: calibration improves with practice—superforecasters self-correct via Brier score tracking|{7}ICLR 2026 workshop: Uncertainty-Gated Generative Modeling (UGGM) for internal uncertainty control in AI systems|{8}SVB-review calibration lesson confirmed: multiplicative adjustment inflates estimates vs additive Bayesian updating|src:sms.onlinelibrary.wiley.com/doi/10.1002/smj.70007,arxiv.org/pdf/2603.07753,learnmoore.org/CAC/CAC.pdf,dl.acm.org/doi/10.1287/mnsc.2016.2525|refreshed:2026-03-17|next:2026-06-17]

R[base-rate-databases:{1}FDIC BankFind Suite: searchable database of all US bank failures since 1933 (banks.data.fdic.gov)|{2}FDIC historical: median 7 failures/yr since 1933; 570 failures 2001-2025; ~400 in 2009-2011 alone; 5 in 2023 (incl SVB, Signature); 2 in 2024; 2 in 2025; 1 so far in 2026|{3}FRED (St. Louis Fed): time series data on bank failures (BKFTTLA641N)|{4}startup failure rates (2026 data): 90% lifetime failure; 1yr survival ~80%; 5yr survival ~48-55%; 10yr survival ~33-37%|{5}industry-specific: tech 63% failure, blockchain 95%, e-commerce 80%, fintech 75%|{6}founder experience: first-time 18% success, prior-failure 20%, prior-success 30%|{7}Oxford Global Projects: 20K megaproject entries, 136 countries (infrastructure focus)|{8}gap: no single consolidated cross-domain base-rate repository—data fragmented across FDIC, BLS, Crunchbase, Oxford GP, industry reports|{9}AI funding context: $211B in 2025 (85% YoY increase), half of all global VC into AI|src:banks.data.fdic.gov,fdic.gov,fred.stlouisfed.org,growthlist.co,failory.com,demandsage.com,oxfordglobalprojects.com|refreshed:2026-03-17|next:2026-06-17]

R[pre-mortem-methodology:{1}Gary Klein's method: assume plan has already failed → independently generate failure reasons → no arguing/objecting during generation phase|{2}effectiveness: 30% improvement in risk identification accuracy (prospective hindsight research)|{3}benefits beyond risk-ID: reduces overconfidence, promotes discoveries, deepens team appreciation, builds candor culture|{4}best practices: 20-30min session post-briefing, independent generation before group discussion, exclude top executives (domination effect), include newcomers+failure-experienced people|{5}2025 Brookings: pre-mortems applied to AI deployment risks (ethical+operational failure anticipation)|{6}integration with strategic planning: runs after plan briefing but before commitment—captures dissent that normal critique sessions suppress|{7}key mechanism: "prospective hindsight" (mentally transporting to future) activates different cognitive pathways than present-tense critique|{8}relevance to sigma-review: PM methodology maps directly to DA adversarial function—DA essentially runs continuous pre-mortem on team analysis|src:gary-klein.com/premortem,hbr.org/2007/09/performing-a-project-premortem,psychologytoday.com,theuncertaintyproject.org,cognitivebiaslab.com|refreshed:2026-03-17|next:2026-06-17]

R[ai-assisted-forecasting:{1}ForecastBench: GPT-4.5 achieves Brier 0.101 vs superforecasters 0.081 (Oct 2025)—gap modest and closing|{2}projected LLM-superforecaster parity: Nov 2026 (95% CI: Dec 2025–Jan 2028)|{3}LLM-augmented human forecasting: 24-28% accuracy improvement over control; superforecasting assistant +41%, noisy assistant +29%|{4}Brier Index improvement: +2.4 percentage points in one year (Claude 3.5 Sonnet Oct 2024 → Grok 4.20 Preview Oct 2025)|{5}Metaculus FutureEval (launched Feb 2026): continuous AI vs human benchmark across science, tech, health, geopolitics, AI domains|{6}Pro Forecasters still lead AI systems on FutureEval; AI projected to surpass community Apr 2026, Pro Forecasters mid-2027|{7}caveat: linear extrapolation may break down near frontier—last mile may be hardest|{8}implication for sigma-review: LLM-assisted forecasting (current approach) is empirically validated as accuracy-enhancing; team should track own calibration vs pure-LLM and pure-human baselines|src:forecastbench.org,forecastingresearch.substack.com,arxiv.org/abs/2402.07862,metaculus.com/futureeval,goodjudgment.com|refreshed:2026-03-17|next:2026-06-17]
## Loan Admin Agent Technology Landscape — r1 findings (2026-03-17)
task: superforecasting analysis of loan admin agent technology competition | corporate lending (BSL + private credit)
SQ[1-5]: 5 sub-questions | 3×outcome-1(changed) | 2×outcome-2(confirmed)
RC[1-4]: transformation-success 20-30% | share-shifts take 10-20yr | platform-dominance 15-25yr | unexpected-entrant <10% in 5yr
ANA[1-5]: fund-admin(HIGH:consolidation-via-M&A) | transfer-agency(HIGH:incumbent-survives) | custody(MODERATE:top-3-stable-40yr) | Broadridge(HIGH:M&A-to-dominance-15yr) | FIS-Worldpay(MODERATE:FAILED-big-bang-$43B→$17.5B)
CAL[1-6]: P(tech-primary-diff,3yr)=20% | P(dominant-via-tech,5yr)=15% | P(unexpected>10%share,5yr)=8% | P(DLT-disrupts,5yr)=12% | P(private-credit-forces-adoption)=62% | P(consolidation<5-players,10yr)=48%
PM[1a-d,2a-d]: 8 scenarios | top-failure:FIS-syndrome(25-30%) | top-disruption:infrastructure-becomes-service(20-25%)
OV-RECONCILIATION: "tech wins" narrative PARTIALLY CORRECT but OVERSTATED in timeframe(3-5yr→10-20yr) and mechanism(organic→M&A) | tech=necessary-to-survive ¬sufficient-to-win | consolidation is highest-confidence pattern
cross-agent: validates tech-architect F1(assembled=debt)+F4(S&P-DataXchange)+F10(tech-debt)+F11(unexpected-plays)
market-data: loan-agency-TAM $1.45B(2024)→$2.19B(2032) | private-credit $3T→$5T(2029) | BSL $1.3T | tech-spend-ceiling ~$115-220M/yr
key-players-verified: Alter Domus, Kroll, GLAS, SRS Acquiom, Ankura Trust, Wilmington Trust + infrastructure: Versana, Finastra, AccessFintech, S&P Global(DataXchange/AmendX Mar 2026)
## VDR Competitive Market Analysis — r1 findings (2026-03-18)
task: superforecasting analysis of VDR technology market | competitive landscape + forecasting
SQ[1-5]: 5 sub-questions | 2×outcome-1(changed) | 2×outcome-2(confirmed) | 1×outcome-3(gap)
RC[1-5]: SaaS-consolidation(top-5:36%→51%in5yr) | ERP-duopoly(15yr) | CRM-Salesforce(21%after20yr) | PE-rollups(4-6x,#1fail=integration) | vertical-SaaS(23.9%CAGR)
ANA[1-5]: ERP(HIGH:M&A→duopoly-15yr) | CRM(MODERATE:organic+M&A-20yr) | LegalTech(MODERATE:AI+315%-adoption) | IDP(HIGH:extract→understand+act) | PE-rollup(VERY-HIGH:Datasite/CapVest-8+acq-$500M)
CAL[1-6]: CAGR=12-16%realized(¬18-22%forecast) | P(top-3>60%,5yr)=30% | P(AI-disruption,3yr)=50% | P(leaders-stable,5yr)=65% | P(new-entrant>10%,3yr)=5% | P(M&A-consolidation,3yr)=75%
PM[1-5]: M&A-downturn(15-20%) | AI-commoditizes(20-25%) | Datasite-integration-fail(20-30%) | regulatory-fragmentation(10-15%) | market-overestimation(35-45%)
OV-RECONCILIATION: CONSOLIDATION-THROUGH-ACQUISITION(ERP pattern)¬DISRUPTION-BY-INNOVATION(Salesforce pattern) | inside-view overestimates growth 20-30% | Datasite/CapVest executing PE-rollup explicitly
key-market-data: VDR $2.4-3.4B(2024-2025) | Datasite 8+ acq since 2020 | SS&C Intralinks $420M rev | DFIN Venue $142M FY2025 | Ansarada acquired by Datasite Aug2024(AUD$212-263M) | iDeals fastest organic growth(2M+ users) | VDR AI adoption only 8% vs 77% VDR use
divergences: CAGR lower than PS(18-22%) aligned w/ EA(13-18%) | concentration timeline more conservative than EA(65-70% by 2028) | AI-commoditization risk weighted higher than PS+TA
cross-agent: aligns w/ PS(consolidation+Ansarada), TA(AI-table-stakes+Datasite-flywheel), EA(CAGR-calibration+demand-floor)
H1:partially-falsified | H2:partially-confirmed | H3:confirmed(via M&A ¬organic)

## Warehouse Game Design R3 responses (2026-03-18)
task: R3 DA challenge responses | reference-class-analyst
DA#1(crowding): CONCEDE(partial) | game NOT independently recommended; anchoring via C1 prompt constraint real; RC6 amended: game=validated choice given constraints, not independent first choice; counterfactual-reasoning gap IS genuine independent case
DA#2(Pymetrics): COMPROMISE(major) | Pymetrics "supports"→"tangential proof of concept" | behavioral signals (routing patterns, avoidance) may classify as personality/behavioral (consistently fails) not cognitive (sometimes works) — category UNRESOLVED | closest analogue=GEMS COW (ANA1)
DA#3(incremental-R²): CONCEDE(with boundary) | quantified: ~2-5% incremental R² above WMS logs for performance prediction = insufficient for cost justification | defense: if Thesis-C (counterfactual reasoning), incremental R² is wrong benchmark — but game advantage over qualitative methods also unestablished | CAL-H2: 45%→30% | 80%CI[18%,45%] | 90%CI[12%,52%]
DA#6(joint-probability): CONCEDE | modeled explicitly: joint P(all 15 conditions) = 0.1%-1% | lowest-P conditions (validation study P=0.35, third-party admin P=0.40, discretion audit P=0.50) are most load-bearing AND most likely cut first under project pressure | realistic deployment: 7-10 conditions | CAL-H4: 50%→35%
UPDATED CAL[]:
  CAL-H1: 60%→50% | 80%CI[32%,68%] | 90%CI[24%,75%]
  CAL-H2: 45%→30% | 80%CI[18%,45%] | 90%CI[12%,52%] (largest revision)
  CAL-H3: unchanged 55%/30%
  CAL-H4: 50%→35% | 80%CI[22%,50%] | 90%CI[15%,58%]
  CAL-H5: unchanged 65%
R3 verdict: "Premise launderable for Thesis-C (counterfactual reasoning elicitation) under partial-compliance producing partial value. Inside-view comprehensive-insight claim requires joint P<1%. Build only if: Thesis-C accepted, pre-deployment gate completed, expected value calibrated to 7-10 condition reality."
calibration-lesson: P[joint-probability of multi-condition viability must be explicitly modeled; enumerating conditions independently systematically overstates viability|src:warehouse-game-R3|class:calibration]
calibration-lesson: P[behavioral signals in game assessments (routing patterns, avoidance tendencies) may classify as personality/behavioral not cognitive — resolve category before applying validity literature|src:warehouse-game-R3|class:calibration]
## AI Biotech Healthcare M&A — r1 findings (2026-03-18)
task: superforecasting analysis of AI impact on biotech/healthcare M&A 2026-2031
SQ[1-5]: 5 sub-questions | 2×outcome-1(changed) | 2×outcome-2(confirmed) | 1×outcome-3(gap)
RC[1-5]: tech-M&A-lag(7-15yr,AI~12yr=EARLY-WAVE) | exit-outcomes(60-65%M&A,15-20%IPO) | macro-STRONGLY-favorable(cliff+rates=structural) | transform-5yr(20-30%base-rate) | 25%-techs-never-trigger-wave
ANA[1-5]: genomics(HIGH:partnership→acquisition-15yr) | mRNA(HIGH:crisis-compressed) | CRISPR(HIGH:licensing→partnership→acq) | comp-chem(MODERATE:embedded-tool-¬wave) | Watson(VERY-HIGH:$5B→$1B-FAILURE)
CAL[H1-H4]: P(AI-accelerates-M&A,2031)=72% | P(>$5B-AI-acq-by-2028)=55% | P(medtech>$10B)=82%broad/45%native | P(M&A>2023)=88% | P(AI-net-catalyst)=62%
PM[1-5]: clinical-fail(20-25%) | Watson-2.0(15-20%) | regulatory-geopolitical(15-20%) | recession(10-15%) | embedded-tool(15-20%) | joint-P(≥1)=55-65%
OV-RECONCILIATION: inside-OVERSTATES-AI-causal-role | M&A-volume=HIGH-CONF(88%)-driven-by-NON-AI(cliff,rates,firepower) | AI-SPECIFIC=MOD-CONF(72%) | AI=15-25%-of-total-M&A-by-2031(vs~8-10%-now)
key-insight: patent-cliff($236-400B)+macro=primary-M&A-driver|AI=additive-new-target-category ¬ primary-cause|inside-view-narrative-conflates-AI-contribution-with-structural-macro-forces
cross-agent: aligns PS(non-AI-triple),PA(cliff-primary,premium-bifurcated),RA(regulatory-bifurcated),EA(CAGR-calibration,Eroom's)|diverges PS(AI-as-primary-vs-additive)
H1:partially-confirmed | H2:partially-confirmed | H3:confirmed+caveat(peak-may-extend-2033-35) | H4:split(62/38)
calibration-lesson: P[M&A-driven-by-EXPECTED(narrative)-value-independent-of-REALIZED(evidence)-value — hype-itself-drives-deals-before-clinical-validation|src:AI-biotech-review-R1|class:calibration]
calibration-lesson: P[patent-cliff-is-stronger-M&A-predictor-than-technology-narrative — $236-400B-at-risk-creates-structural-buying-urgency-regardless-of-AI|src:AI-biotech-review-R1|class:pattern]
## AI Biotech Healthcare M&A — R3 DA responses (2026-03-18)
task: R3 DA challenge responses | DA[#1]+DA[#3]+DA[#5]+DA[#8]
DA[#1] H1-reconciliation: proposed 3-category framework (AI-irrelevant 55-65%|AI-additive 20-30%|AI-primary 8-15%→20-25% by 2031) | PS-RCA CONVERGENCE achieved — PS R3 adopted "deal-shaper ¬deal-engine" = aligned
DA[#5] 173-decomposition: ~40 Phase1|~26-31 Phase2|2-3 Phase3|0 NDA | M&A-relevant(P2+)=28-34=16-20% of 173 | expected 4-8 FDA AI drugs by 2031(optimistic) / 2-5(base rate) | base rates: P1→P2=47%, P2→P3=28%, P3→NDA=55%, overall LOA=6.7% | AI P1 claimed 80-90% but vendor-forward → blended 63%
DA[#3] Eroom's: ~50% compositional(oncology/rare-disease accelerated approval lower bar: 85% AA drugs=oncology, 57% failed confirmatory, Phase III required 26% AA vs 75% regular) + ~50% real(ROI 1.2→5.9%, biomarker stratification) | reversal UNDEMONSTRATED | STRENGTHENS R1 position | AI R&D productivity claims ~50% overstated
DA[#8] failure-catalogue: Watson+Olive($4B)+Babylon($4.2B)+Pear($6.1M auction)+BenevolentAI(delisted Mar 2025)+Recursion(REC-994)+Cano+Mindstrong+HealthIQ = N≥5, $14B+ destroyed | systematic pattern ¬ outlier | ANA[5] ELEVATED | PM[2] revised 15-20%→20-25%
CAL revisions: H1=72→68% | H1a=55→50% | H4=62→60% | PM[2]=15-20→20-25% | H2,H3 unchanged
net: DA challenges STRENGTHENED RCA position on 3/4 items | modest-downward revision
calibration-lesson: P[173-as-anchor-requires-phase-decomposition;M&A-relevant-pipeline=16-20%-of-headline;headline-pipeline-numbers-systematically-inflate-perceived-near-term-opportunity|src:AI-biotech-R3|class:calibration]
calibration-lesson: P[Eroom's-deceleration-~50%-compositional-from-oncology/rare-disease-accelerated-approval-with-lower-evidence-bar;market-pricing-AI-as-reversing-Eroom's-when-evidence-shows-partial-deceleration-partially-artifactual|src:AI-biotech-R3|class:pattern]
calibration-lesson: P[AI-healthcare-systematic-failure-N≥5-$14B+-is-reference-class-¬-anecdote;Watson-was-not-N=1-outlier-but-representative-of-pattern(marketing>capability,ambitious-scope,data-quality,adoption-assumed)|src:AI-biotech-R3|class:pattern]
## US Data Center Infrastructure Constraints — R3 DA responses (2026-03-19)
task: R3 DA challenge responses | US data center market infrastructure constraints
DA-grade: A(r1) | DA challenges directed: #1,#2,#4,#5,#7,#8,#10a,#10b

### DA responses summary
DA[#1] CAPACITY REALIZATION: COMPROMISE | base-rate REVISED 20-60%→15-45% | political-opposition=NEW constraint(not in fiber/nuclear/EV/shale analogs) | construction-fell-5.7%(Bloomberg Feb 2026) | 25-cancellations-2025(21-in-H2) | $64B-blocked | distribution-bimodal(hyperscaler-BTM=35-45%/grid-connected-colo=15-25%) |source:independent-research
DA[#2] LABOR: CONCEDE(material-omission) | 439K-worker-shortage(ITIF) | 349K-NET-NEW-needed-2026(CNBC) | electricians=45-70%-DC-construction-cost | crew-sizes-750→4000-5000 | labor-MULTIPLIER-on-delay(¬standalone) | BTM-¬bypasses-labor | timeline-extension-6-18mo-across-2026-2029 | PM3-revised-25-30%→30-35% |source:independent-research
DA[#4] CAPEX SUSTAINABILITY: CONCEDE | $660-690B-at-90%-OCF | $100B-bonds-+record-CDS-protection | $25B-revenue-vs-$450B-AI-capex(5.6%-ratio) | MIT-95%-no-meaningful-revenue-increase | fiber-analog-STRENGTHENING | REVISED-P=55%→42% | arms-race-lock-in=real-floor(prevents-<25%) | P-NOT-uniform-across-5(MSFT-Azure-more-durable) |source:independent-research
DA[#5] CHIP SUPPLY: DEFEND+STRENGTHEN | HBM-sold-out-through-2026(Micron) | AI-firms-locked-supply-into-2027 | 1GB-HBM=4x-fab-capacity-standard-DRAM(multiplicative-shortage) | 20%-of-global-DRAM-wafer-capacity-to-AI-2026(TrendForce) | UPGRADED: harder-ceiling-than-power | power=geographic+solvable-via-BTM | chips=global+NO-WORKAROUND | LEI-finding-validated |source:independent-research
DA[#7] H4 NUCLEAR: ACCEPT-DA-framework | bifurcation-correct | MY-P=5%-conflated-restart+new-build(imprecise) | CAL[restart-4GW-2030]=P=70%(80%CI=[50%,85%]) | TMI-80%-staffed/500+-on-site/2027-target-ahead-of-schedule/DOE-$1B-loan-Q1-2026 | CAL[SMR-5GW-2035]=P=10%(maintained,minor-upper-nudge) | resolves-EMA-RCA-divergence | EMA-right-on-restarts/RCA-right-on-new-build |source:independent-research
DA[#8] DEEPSEEK: RESOLVE | Fork-A(efficiency-dominant)=P=20-25%→implied-230-310TWh | Fork-B(Jevons-dominant)=P=55-60%→implied-420-580TWh | Fork-C(balanced)=P=15-25%→implied-340-420TWh | Jevons-modal | temporal-fork:Jevons-dominates-2026-2028/Fork-A/C-may-emerge-2029-2030 | pop-weighted-expected-value≈423TWh(close-to-IEA/GS-base) | 360TWh-estimate-sits-below-consensus-for-defensible-reasons |source:independent-research
DA[#10a] DEMAND CYCLICALITY: COMPROMISE | PM1-REVISED-P=20-25%→25-30% | MIT-95%-no-revenue-increase | $25B-vs-$450B-ratio | cascade-risk(one-cuts=reduces-competitive-pressure-for-others-to-maintain) |source:independent-research
DA[#10b] STRANDED ASSETS: RESOLVE(new) | retrofit-cost=$1-5M/MW | $20-100B-unrecognized-liability(20GW-pre-2022-vintage×$1-5M) | KKR-CyrusOne($15B-2022)+Blackstone-QTS($10B-2021)=most-acute | PM6(NEW)=P=15-20% | PM1+PM3+PM6-positively-correlated |source:independent-research

### updated CAL estimates
CAL[US-DC-power-2030]: R1=380TWh→R3=360TWh | 80%CI=[240,510] | 90%CI=[195,640]
CAL[US-DC-capacity-2030]: R1=45GW→R3=38GW | 80%CI=[25,55] | 90%CI=[18,70]
CAL[hyperscaler-capex-sustained-2028]: R1=55%→R3=42% | 80%CI=[25%,62%]
CAL[nuclear-restart-4GW-2030]: NEW=70% | 80%CI=[50%,85%]
CAL[nuclear-SMR-5GW-2035]: MAINTAINED=10% | 80%CI=[3%,22%]

### hygiene check
§2b-OUTCOME-2: 360TWh(15-18%-below-IEA/GS-426TWh-base) | maintained-because: Bloomberg-construction-decline(revealed-preference>forward-projection) + Sightline-31%-realization + HBM-chip-ceiling + historic-base-rate-no-boom->60% | upside-preserved-in-upper-CI

### OV-reconciliation
inside-view=360-420TWh/38-45GW | outside-view-range=240-430TWh/20-50GW | gap=team-at-lower-optimistic-end-of-base-rate-range | 30-35%-probability-2030-outcomes-below-revised-estimates | fiber-analog=assets-survive-but-on-7-12yr-lag | key-question=whether-3-5yr-useful-life-generates-returns-before-next-generation-makes-vintage-obsolete

### key calibration lessons
P[multi-constraint-joint-probability: 4 simultaneous constraints(political-opposition/chip-supply/labor/capital) partially sequential; resolving 3-of-4 produces MUCH-less than 75% of potential capacity; joint-favorable-resolution-probability-LOW|src:US-DC-R3|class:calibration]
P[chip-supply-creates-HARDER-ceiling-than-power: power=geographic+solvable-via-BTM; chips=global+NO-WORKAROUND; BYOP-gas-cannot-fill-GPU-starved-DC|src:US-DC-R3|class:pattern]
P[political-community-opposition-is-NEW-additive-infrastructure-constraint-not-in-fiber/nuclear/EV/shale-analogs: construction-can-DECLINE-while-announcements-GROW(Bloomberg-2026)|src:US-DC-R3|class:pattern]
P[H4-nuclear-requires-bifurcation: restarts(P=70%-credible/signed/financing-secured) vs new-build-SMR(P=10%/zero-operating/reference-class-devastating) are TWO different claims; conflating them produces wrong verdict|src:US-DC-R3|class:calibration]
P[Jevons-paradox-fork: efficiency-dominant-P=20-25% is meaningful tail not dismissible; Jevons-dominant-P=55-60% is modal; temporal-bifurcation(Jevons-early-elasticity-phase/efficiency-dominates-as-saturation-approaches)|src:US-DC-R3|class:pattern]
P[stranded-asset-cascade: $20-100B-unrecognized-retrofit-liability on 2021-2022-PE-acquisitions; 6yr-depreciation-schedules vs 24mo-economic-obsolescence; PM1+PM3+PM6-positively-correlated-cascade-risk|src:US-DC-R3|class:risk]
