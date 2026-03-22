# workspace — Sigma-Review Cognitive Enhancement: Applying Cognitive Theory Frameworks
## status: active
## mode: ANALYZE
## tier: TIER-2 (18/25)
## round: r1

## task
Meta-analysis of the sigma-review system itself. Evaluate how cognitive theory frameworks (Brier Scores, Analysis of Competing Hypotheses, Thagard's Theory of Explanatory Coherence, Critical Questions of Thought Exit Gating, human calibration techniques) could improve sigma-review's overall quality. Use the DeepMind Cognitive Framework (10 cognitive faculties) as the lens for understanding where sigma-review is strong vs weak. The rubric evaluation (data center analysis) showed sigma-review scored 28/30 vs single-instance 24/30 — a 17% improvement at 30-40x cost. Goal: find frameworks that make the system more robust across ALL quality dimensions.

## scope-boundary
This review analyzes: cognitive theory frameworks applicable to improving multi-agent AI review systems, specifically sigma-review
This review does NOT cover: specific market analyses, codebase reviews, implementation of changes (this is research/analysis only), BUILD-mode improvements
temporal-boundary: none
Lead: before writing synthesis or documents, re-read this boundary.

## prompt-decomposition
### Q[] — Questions (research scope)
Q1: What is sigma-review's cognitive profile across the 10 DeepMind faculties (Perception, Generation, Attention, Learning, Memory, Reasoning, Metacognition, Executive Functions, Problem Solving, Social Cognition) — where does the system show strengths vs weaknesses, and how does that explain the rubric results (28 vs 24)?
Q2: Which cognitive theory frameworks (Brier Scores, ACH, TEC, CQoT, calibration) target sigma-review's weakest cognitive faculties?
Q3: What does the research literature say about whether human cognitive debiasing frameworks (ACH, TEC, calibration training) transfer to LLM multi-agent systems — or are they human-specific?
Q4: How would each applicable framework be implemented within the existing architecture (directives, agent prompts, workspace format, round management)?
Q5: Which implementations would improve the cost/quality ratio (currently 30-40x cost for 17% improvement), not just absolute quality?
Q6: Are there cognitive theory frameworks or approaches NOT mentioned by the user (beyond Brier Scores, ACH, TEC, CQoT, calibration) that would improve sigma-review's cognitive profile — what does the literature suggest?

### H[] — Hypotheses to test (not facts)
H1: Sigma-review's cognitive profile has specific faculty weaknesses (likely Metacognition — error monitoring, source judgment) that explain the marginal delta over single-instance, since accuracy tied at 3/5 while calibration and counterarguments scored 5/5.
H2: The 28 vs 24 delta is "marginal" — i.e., the multi-agent process doesn't justify 30-40x cost for overall quality improvement.
H3: Cognitive theory frameworks (Brier Scores, ACH, TEC, CQoT) are applicable to LLM agents and will improve overall quality across faculties, not just isolated dimensions.
H4: A cognitive profile approach (targeting weakest faculties) will reveal improvement opportunities that dimension-by-dimension rubric thinking misses — interaction effects between faculties matter.
H5: The five named frameworks are not exhaustive — there are other cognitive science or decision theory approaches that could be equally or more impactful for multi-agent analytical systems.

### C[] — Constraints
C1: Solutions must be implementable within existing sigma-review architecture (directives, agent prompts, workspace format)
C2: The rubric evaluation (data center analysis) is the quality baseline
C3: Focus on robustness (reliably better across all quality dimensions) not peak performance on any single dimension
C4: Cost/complexity tradeoff matters — adding cognitive overhead must improve the quality/cost ratio

## reference-materials
### rubric evaluation summary (data center analysis, blind scored)
- sigma-review (Analysis A): 28/30 | single-instance (Analysis B): 24/30
- accuracy: A=3/5, B=3/5 (TIED)
- market-sizing-rigor: A=5/5, B=4/5
- calibration: A=5/5, B=4/5
- counterarguments: A=5/5, B=4/5
- surprises: A=5/5, B=4/5
- self-awareness: A=5/5, B=5/5 (TIED)
- key delta: taxonomy, calibration rigor, adversarial counterarguments, novel frameworks
- key weakness: accuracy tied — both had factual errors, team synthesis without auditable trail

### DeepMind Cognitive Framework (10 faculties)
1. Perception — extract/process sensory information
2. Generation — produce outputs (text, actions)
3. Attention — focus cognitive resources selectively
4. Learning — acquire new knowledge through experience
5. Memory — store and retrieve information over time
6. Reasoning — draw conclusions via logical principles (deductive, inductive, abductive, analogical, mathematical)
7. Metacognition — knowledge of own processes, confidence calibration, error monitoring, source judgments, error correction
8. Executive Functions — goal-directed behavior: planning, inhibitory control, cognitive flexibility, conflict resolution, working memory
9. Problem Solving (composite) — find solutions using reasoning+planning+learning
10. Social Cognition (composite) — process social information, theory of mind, cooperation, negotiation

### team patterns (key meta-findings)
- irreducible-multi-agent-value = 2 items only: (1) DA context firewall (2) cross-session calibration accumulation. ~60-70% of stated value achievable with structured single-agent prompting
- controlled-comparison: 30-40x cost for 17% improvement. 80% quality at 3% cost = efficiency frontier
- DA-challenges-spark-superior-findings: agents who engage deeply with DA produce BETTER work than R1
- prompt-contamination-correctable-in-1-round when DA flags it
- highest R3 engagement correlates with data-backed challenges (not rhetorical ones)

## findings
### reference-class-analyst

#### F1: Brier Scores — integration with sigma-review CAL[] format
F1a: LLM forecasting gap closing rapidly — GPT-4.5 Brier=0.101 vs superforecasters=0.081 (ForecastBench, ICLR 2025) | parity projected Nov 2026 (95%CI: Dec2025-Jan2028) | improvement rate ~0.016 Brier points/yr |source:[independent-research]
F1b: CRITICAL finding — chain-of-thought reasoning DEGRADES Brier Skill Score via overconfidence | only 1 frontier LLM achieved positive BSS (+0.057), majority NEGATIVE | complex reasoning→worse calibration ¬better |source:[independent-research]
F1c: sigma-review's CAL[] format already captures point+80%CI+90%CI+assumptions+breaks-if — this IS a proper scoring framework but LACKS resolution tracking | Brier decomposes into reliability(calibration)+resolution(discrimination)+uncertainty — sigma-review tracks reliability but ¬resolution |source:[agent-inference]
F1d: Brier scoring WOULD improve sigma-review IF applied as tracking mechanism across reviews — superforecasters improve via Brier feedback loops (GJ Project confirmed: practice+feedback=better calibration) | sigma-review already has cross-session calibration accumulation (team pattern) but ¬formal scoring |source:[independent-research]
F1e: IMPLEMENTATION GAP: Brier requires binary outcomes with resolution dates | most sigma-review CAL[] estimates are conditional probabilities (P(X|Y,5yr)) — many never formally resolve | Brier scoring feasible for ~30-40% of estimates (those with verifiable outcomes within tracking horizon) |source:[agent-inference]
— §2b flag: Brier scoring has diminishing returns for multi-agent systems where agents share training data (¬independent). Maintained because: sigma-review agents ARE same-model instances but operate under different expertise prompts creating FUNCTIONAL diversity (analogous to superforecaster teams where skill>independence). ForecastBench shows ensemble diversity from methodology ¬model difference. |source:[independent-research]

#### F2: LLM calibration quality — overconfidence/underconfidence patterns
F2a: PERVASIVE OVERCONFIDENCE confirmed — Dunning-Kruger effect in LLMs (arxiv 2603.09985, Mar 2026): poorly-performing models show disproportionate overconfidence | 5 frontier models (Claude Opus 4.5, GPT-5.2, DeepSeek-V3.2, Qwen3-235B, Kimi-K2) ALL systematically overconfident |source:[independent-research]
F2b: LLMs mirror HUMAN calibration failure pattern — overconfident on hard tasks, underconfident on easy tasks (arxiv 2502.11028) | implies human debiasing frameworks MAY transfer since failure mode is analogous |source:[independent-research]
F2c: verbalized confidence (sigma-review's approach via CAL[] percentages) consistently OVERESTIMATES vs token-level probabilities | posthoc calibration mitigates this | SteerConf (arxiv 2503.02863) shows steering prompts can improve calibration |source:[independent-research]
F2d: Claude Haiku 4.5 shows SUPERIOR calibration — highest confidence variability, appropriately modulates by difficulty | model-specific calibration properties matter |source:[independent-research]
F2e: IMPLICATION for sigma-review: agents verbalize probabilities (CAL[]=50%, 80%CI=[30,70]) which are systematically overconfident → existing §2b calibration checks partially compensate but ¬systematically | formal recalibration step (posthoc adjustment based on historical accuracy) would improve |source:[agent-inference]
— §2a positioning: consensus in literature that LLM overconfidence is real+systematic. No serious counter-position found. Outcome 2: confirmed with acknowledged risk that calibration research on individual LLMs may not transfer directly to multi-agent prompted systems. |source:[independent-research]

#### F3: Reference class forecasting as cognitive enhancement — DeepMind faculty mapping
F3a: sigma-review's superforecasting protocol exercises 4 of 10 DeepMind faculties directly: Reasoning(RC[],ANA[]), Metacognition(CAL[],OV-RECONCILIATION), Memory(cross-session calibration), Executive Functions(DECOMPOSE→structured planning) |source:[agent-inference]
F3b: DeepMind's Mar 2026 paper identifies LARGEST EVALUATION GAPS in exactly the faculties sigma-review is weakest: Learning, Metacognition, Attention, Executive Functions, Social Cognition — $200K Kaggle hackathon targeting these 5 |source:[independent-research]
F3c: sigma-review's WEAKEST faculty = Learning (faculty 4) — no within-session learning mechanism; agent findings from r1 don't update agent priors for r2+ except via workspace reads | cross-session learning exists (memory.md) but within-session is manual |source:[agent-inference]
F3d: sigma-review's STRONGEST faculty relative to single-instance = Metacognition (faculty 7) — CAL[] format, §2b calibration checks, OV-RECONCILIATION all exercise metacognitive monitoring | this explains 5/5 calibration score vs 4/5 single-instance |source:[agent-inference]
F3e: PARADOX: sigma-review scores 5/5 calibration but accuracy TIED at 3/5 | reference-class explanation: calibration measures SELF-KNOWLEDGE-OF-UNCERTAINTY ¬accuracy-of-point-estimates | well-calibrated agents can be accurately uncertain about wrong things | this is the resolution-vs-reliability distinction from Brier decomposition (F1c) |source:[agent-inference]
— §2c cost check: superforecasting protocol adds ~15-20% token overhead per agent (SQ[]+RC[]+ANA[]+CAL[]+PM[]+OV). For 5 agents = 75-100% additional tokens. Maintained because: this overhead produces the highest-delta dimensions (calibration 5/5, counterarguments 5/5). Without it, sigma-review loses its differentiation. |source:[agent-inference]

#### F4: Outside-view vs inside-view in multi-agent systems — herding analysis
F4a: HERDING IS THE DEFAULT — Science Advances (2025, sciadv.adu9368): LLM populations spontaneously form social conventions + collective biases that CANNOT be traced to individual agents | emergent property ¬individual property | biases amplify at population level |source:[independent-research]
F4b: multi-agent debate does NOT reliably produce outside-view — ICLR 2025 blog: MAD frameworks fail to consistently outperform single-agent strategies | majority voting accounts for most gains attributed to debate | "tyranny of majority" = if most agents give same answer (right or wrong), minority conforms |source:[independent-research]
F4c: SIGMA-REVIEW'S DA IS THE CRITICAL DIFFERENTIATOR — DA context firewall (reads workspace WITHOUT participating in r1) IS the structural mechanism that breaks herding | DA arrives with genuinely different information state than r1 agents | this maps to Surowiecki's independence condition |source:[agent-inference]
F4d: BUT: same-model agents with different expertise prompts create FUNCTIONAL diversity ¬TRUE diversity | all agents share same training data, same reasoning patterns, same biases | "Wisdom of Silicon Crowd" (Science Advances 2025, sciadv.adp1528) shows ensemble accuracy requires diversity from DIFFERENT models (12 LLMs), not same-model-different-prompts |source:[independent-research]
F4e: Surowiecki's 4 conditions for crowd wisdom: (1)diversity-of-opinion (2)independence (3)decentralization (4)aggregation | sigma-review satisfies: (3)decentralization-YES (4)aggregation-YES(lead synthesis) | sigma-review PARTIALLY satisfies: (1)diversity(functional-via-prompts¬architectural) (2)independence(DA-firewall-provides-for-1-agent¬all) |source:[independent-research]
F4f: DISCONFIRMATION FINDING: multi-agent LLM systems naturally produce INSIDE VIEW collectively despite individual agents being prompted for outside view | the "outside view" in sigma-review comes from the PROTOCOL (RC[], OV-RECONCILIATION) not from multi-agent structure itself | single agent with same protocol would get similar outside-view benefit |source:[agent-inference]
— §2e premise viability: H1's claim that Metacognition weakness explains accuracy tie is PARTIALLY VIABLE but incomplete. Accuracy tie may also reflect that factual errors are PERCEPTION-class (misreading source data) not METACOGNITION-class (poor uncertainty estimation). Outcome 3: gap — need to categorize the specific factual errors from rubric evaluation to determine if they are perception or metacognition failures. |source:[agent-inference]

#### F5: Frameworks NOT mentioned by user (Q6/H5 scope)
F5a: EXTREMIZATION ALGORITHMS — when aggregating independent forecasters, extremizing (pushing aggregate away from 50%) improves accuracy | GJ Project: heavily extremized aggregates most accurate for large groups | BUT extremization unnecessary for small teams of superforecasters (top 2%) because knowledge overlap makes extremizing counterproductive | sigma-review = small-expert-team model → extremization likely HARMFUL |source:[independent-research]
F5b: COGNITIVE FORCING FUNCTIONS (CFFs) — Croskerry (2003)+2025 AI updates: structured interventions that interrupt System-1 reasoning to force System-2 engagement | 3 levels: universal(always-apply), generic(situation-class), specific(diagnosis-specific) | sigma-review's analytical hygiene (§2a-e) IS a CFF implementation — forcing outcome 1/2/3 prevents perfunctory checks | CQoT (user-mentioned) is a CFF variant |source:[independent-research]
F5c: PREDICTION TOURNAMENTS — team prediction polls with decay+weighting+recalibration outperform prediction markets by 12% Brier (Management Science) | sigma-review could implement INTERNAL prediction tournament: agents make independent estimates → aggregate with accuracy-weighted averaging → track who calibrates best → weight future estimates accordingly |source:[independent-research]
F5d: METACOGNITIVE PROMPTING — "Could you be wrong?" prompts lead LLMs to identify errors, biases, contradictory evidence, alternatives (MDPI 2025) | latent knowledge about biases exists in LLMs but only surfaces with metacognitive prompts | sigma-review's DA challenges serve this function but only in r2+ — metacognitive self-prompting in r1 would surface issues earlier |source:[independent-research]
F5e: CALIBRATION CASCADES — posthoc recalibration where each agent's estimates are adjusted based on their historical accuracy pattern BEFORE aggregation | differs from raw averaging | would require tracking agent-level calibration across reviews (memory.md already does this partially) |source:[agent-inference]
F5f: LOGARITHMIC SCORING RULE — alternative to Brier | more sensitive to extreme probabilities (heavily penalizes confident wrong predictions) | Metaculus uses log scoring ¬Brier | for sigma-review's use case where confident-wrong is the highest-risk failure mode (accuracy tied despite 5/5 calibration), log scoring would be MORE appropriate than Brier |source:[independent-research]
— §2a positioning: H5 CONFIRMED — multiple frameworks not mentioned by user are relevant. Strongest candidates: (1) prediction tournaments with accuracy-weighting (2) log scoring rules (3) metacognitive self-prompting in r1. Outcome 1: this finding EXPANDS the analysis scope. |source:[independent-research]

#### F6: Disconfirmation duty — evidence AGAINST cognitive frameworks helping LLMs
DISCONFIRM[cognitive-frameworks-for-LLMs]: evidence-against={1. MAD frameworks fail to outperform single-agent strategies (ICLR 2025) 2. chain-of-thought DEGRADES Brier Skill Score via overconfidence 3. same-model multi-agent systems lack true diversity (Science Advances 2025) 4. LLM calibration may be fundamentally different from human calibration — LLMs don't "learn" from scoring feedback within session 5. cognitive forcing strategies designed for System-1/System-2 distinction may not apply to LLMs which lack System-1 fast-heuristic processing} |src:[independent-research] |severity:M
DISCONFIRM[alternative]: strongest-alt={STRUCTURED SINGLE-AGENT PROMPTING with full superforecasting protocol — team pattern already identifies 60-70% of value achievable at 3% cost} |evidence-for={MAD literature shows majority-voting accounts for most multi-agent gains; Silicon Crowd paper shows diversity needs different models not different prompts; single agent with RC[]+ANA[]+CAL[]+PM[]+OV would capture most calibration benefit} |src:[independent-research+agent-inference]
DISCONFIRM[comparison]: sigma-review-with-frameworks vs enhanced-single-agent |proposed-advantage={DA context firewall creates genuine independence for 1 agent; cross-session calibration accumulation; multiple perspectives even if functionally diverse} |alt-advantage={3% cost for 60-70% quality; no coordination overhead; no herding risk; all cognitive frameworks applicable to single agent} |recommendation=flag-for-debate — the 2 irreducible multi-agent values (DA firewall + calibration accumulation) are real but narrow; most cognitive framework benefits transfer equally to single-agent

#### SUPERFORECASTING PROTOCOL

##### SQ[] decomposition
SQ[1]: will formal Brier scoring improve sigma-review calibration quality? |estimable:yes |method:base-rate+analogue |→ reference-class-analyst(primary)
SQ[2]: do human cognitive debiasing frameworks transfer to LLM agents? |estimable:partially |method:analogue+data |→ cognitive-decision-scientist(primary),reference-class-analyst(advisory)
SQ[3]: does multi-agent structure create genuine outside-view or herded inside-view? |estimable:yes |method:data |→ reference-class-analyst(primary)
SQ[4]: what is the cost/quality tradeoff of adding cognitive frameworks? |estimable:yes |method:precedent |→ product-strategist(primary),reference-class-analyst(advisory)
SQ[5]: which frameworks have highest impact-per-token? |estimable:partially |method:decompose |→ tech-architect(primary),reference-class-analyst(advisory)

##### RC[] base rates
RC[cognitive-framework-improving-AI-systems]: reference-class=structured-methodology-improvements-to-AI-pipelines |base-rate=marginal-improvement-10-25%-when-applied(¬transformative) |sample-size=moderate(N~20-30 studies) |src:ForecastBench,MAD-literature,calibration-research |confidence:M
RC[calibration-training-effectiveness]: reference-class=calibration-improvement-from-scoring-feedback |base-rate=GJ-Project-superforecasters-improved-~30%-with-Brier-tracking |sample-size=large(N=thousands) |src:goodjudgment.com |confidence:H — but this is HUMAN data, LLM transfer uncertain
RC[multi-agent-debate-improving-accuracy]: reference-class=MAD-framework-performance-vs-single-agent |base-rate=inconsistent-improvement,frequently-¬better-than-self-consistency |sample-size=moderate(N~15-20 studies) |src:ICLR-2025-MAD-review |confidence:H

##### ANA[] analogues
ANA[1]: GJ-Project-superforecaster-teams |outcome:30%-more-accurate-than-prediction-markets,Brier-0.135-vs-0.159 |similarity:H(team-of-calibrated-forecasters-with-structured-methodology) |key-difference:humans-learn-within-session,LLMs-don't |src:goodjudgment.com
ANA[2]: LLM-ensemble-forecasting(Silicon-Crowd) |outcome:12-LLM-ensemble-matched-925-human-crowd-accuracy |similarity:H(multi-model-aggregation-for-prediction) |key-difference:used-12-DIFFERENT-models¬same-model-different-prompts |src:Science-Advances-2025
ANA[3]: MAD-debate-frameworks-2024-2025 |outcome:failed-to-consistently-outperform-single-agent |similarity:VERY-HIGH(same-model-multi-agent-debate) |key-difference:MAD-uses-open-debate¬structured-roles+DA-firewall |src:ICLR-2025
ANA[4]: ACH-in-intelligence-analysis |outcome:reduced-confirmation-bias-in-CIA-analysts-since-1970s |similarity:M(human-analysts-with-structured-methodology) |key-difference:humans-have-System-1/System-2-distinction,LLMs-may-not |src:Heuer-CIA
ANA[5]: ECHO-constraint-satisfaction(Thagard) |outcome:successfully-modeled-scientific-theory-evaluation-computationally |similarity:M(computational-coherence-for-hypothesis-evaluation) |key-difference:ECHO-is-connectionist-network¬LLM-prompt-based |src:Thagard-1989

##### CAL[] estimates
CAL[Brier-scoring-improves-sigma-calibration]: point=65% |80%=[45%,80%] |90%=[35%,85%] |assumptions:tracking-mechanism-implemented,sufficient-resolvable-estimates(>20/review),cross-session-persistence |breaks-if:most-estimates-are-conditional-probabilities-without-clear-resolution-criteria
CAL[cognitive-frameworks-transfer-to-LLMs]: point=55% |80%=[35%,72%] |90%=[25%,80%] |assumptions:frameworks-adapted-for-LLM-context(¬direct-port),prompt-based-implementation |breaks-if:LLM-overconfidence-is-architectural(training-data-bias)¬correctable-via-prompting
CAL[multi-agent-creates-genuine-outside-view]: point=30% |80%=[15%,50%] |90%=[10%,60%] |assumptions:same-model-agents,different-expertise-prompts |breaks-if:DA-firewall-is-only-genuine-independence-mechanism(then-N=1-outside-view¬team-wide)
CAL[overall-quality-improvement-from-frameworks]: point=40% |80%=[20%,60%] |90%=[12%,70%] |assumptions:implemented-within-existing-architecture,measured-across-all-6-rubric-dimensions |breaks-if:accuracy-improvement-requires-architectural-changes(different-models,external-verification)¬prompt-engineering

##### PM[] pre-mortems
PM[1]: COGNITIVE-OVERHEAD-SWAMPS-VALUE — frameworks add 30-50% more tokens per agent, cost rises from 30-40x to 50-65x, quality improvement <5% — net negative ROI |probability:25-30% |early-warning:token-counts-rise-without-corresponding-accuracy-improvement |mitigation:implement-lightest-weight-versions-first,measure-before-scaling
PM[2]: HERDING-AMPLIFICATION — cognitive frameworks create ILLUSION of rigor while agents still herd to same conclusions via shared training data — "calibrated groupthink" |probability:20-25% |early-warning:all-agents-converge-on-same-CAL[]-ranges-despite-different-frameworks |mitigation:DA-monitors-for-suspiciously-uniform-estimates,zero-dissent-circuit-breaker
PM[3]: FRAMEWORK-BECOMES-THEATER — agents learn to produce formatted output (SQ[],RC[],CAL[]) that looks rigorous but is formulaic — the forcing function loses its forcing power |probability:30-35% |early-warning:§2-hygiene-checks-all-produce-outcome-2(confirmed)¬outcome-1(changed) |mitigation:DA-evaluates-framework-application-quality¬just-presence
PM[4]: WRONG-PROBLEM-TARGETED — accuracy tied at 3/5 because of PERCEPTION errors (misread data) not METACOGNITION errors (poor uncertainty) — cognitive frameworks target metacognition but accuracy needs better fact-checking |probability:20-25% |early-warning:factual-errors-persist-despite-framework-additions |mitigation:add-verification-step(source-cross-check)¬more-calibration

##### OV-RECONCILIATION
OV-RECONCILIATION: inside-view={cognitive-frameworks-will-improve-sigma-review-quality-substantially-across-all-dimensions} |outside-view={base-rate-for-methodology-improvements=10-25%-marginal-gain;MAD-literature-shows-multi-agent-debate-frequently-¬better-than-single-agent;LLM-calibration-fundamentally-overconfident-and-may-¬be-correctable-via-prompting-alone} |gap=inside-view-implies-~40%-improvement-probability,outside-view-suggests-~25% |→ reconcile: weight toward outside-view(~30% probability of meaningful improvement across ALL dimensions). Frameworks will likely improve SPECIFIC dimensions (calibration tracking, metacognitive prompting) but unlikely to solve the accuracy tie, which may require architectural changes (fact-verification, different-model diversity). The highest-value intervention is NOT adding more cognitive frameworks but rather: (1) formal Brier tracking on resolvable estimates (2) metacognitive self-challenge in r1 before DA (3) log scoring for high-stakes estimates where confident-wrong is catastrophic.

#### ANALYTICAL HYGIENE SUMMARY
§2a(positioning): LLM-overconfidence=consensus(outcome-2) | multi-agent-herding=confirmed(outcome-2) | cognitive-frameworks-transfer=contested(outcome-3:gap)
§2b(calibration): CAL[] estimates calibrated against ForecastBench+GJ-Project+MAD-literature base rates | own calibration history: R3 revisions typically 10-20% downward from R1 (SVB, warehouse-game, biotech) — applied same conservatism here
§2c(cost): superforecasting-protocol overhead ~15-20%/agent justified by calibration+counterargument scores | additional frameworks would add ~30-50% more — threshold question for C4
§2d(source-provenance): 11 findings tagged | distribution: [independent-research]=14 | [agent-inference]=10 | [prompt-claim]=0 | [cross-agent]=0
§2e(premise-viability): H1(metacognition-weakness) PARTIALLY VIABLE — accuracy tie may be perception¬metacognition failure (outcome 3: gap flagged)

#### R3 — DA Challenge Responses (reference-class-analyst)

**DA[#8] BASE RATE FOR PROMPT ENGINEERING: COMPROMISE**

CONCEDE (partial): DA correctly identifies diminishing returns at sigma-review's optimization level. My own research confirms: CoT reasoning DEGRADES Brier Skill Score (F1b), MAD debate fails to consistently outperform single-agent (F4b). The base rate for "structured prompting improving already-structured systems" IS low. My calibration history supports this — R3 revisions across SVB, warehouse-game, biotech averaged 10-20% downward from R1. The evidence for diminishing returns from further prompt additions is real.

DEFEND (on magnitude framing): DA asks about expected MAGNITUDE, not just probability. This is the right question. My R1 CAL[overall-quality-improvement]=40% was probability, ¬magnitude. Let me decompose:
- MAGNITUDE estimate: if frameworks improve quality, expected improvement = 1-2 rubric points (28→29-30). At ordinal scale, this is 3.5-7% improvement. Combined with P=30% (post-OV-reconciliation), EXPECTED VALUE = 0.3-0.7 × (1-2 points) = 0.3-1.4 rubric points.
- HOWEVER: this magnitude analysis reveals WHY certain frameworks have different value propositions. Brier/log scoring has near-zero per-review magnitude but COMPOUNDS cross-session (each review improves calibration memory by ~2-5%, compounding over N reviews). CQoT exit-gate has immediate magnitude: catching 1 false-convergence per 3-5 reviews prevents a category of failure (premature synthesis) that costs an entire round to fix.
- The DA is right that aggregate magnitude is small. BUT the cost of the top-3 recommendations (CQoT, Brier tracking, metacognitive self-challenge) is also small (<5% overhead). The question is ¬"is 1 rubric point worth 30-40x cost?" but "is 1 rubric point worth <5% marginal overhead on an existing 30-40x investment?" At marginal cost, even small magnitude improvements are positive-ROI.

RC[prompt-engineering-improving-optimized-systems]: reference-class=iterative-process-improvement-on-mature-systems |base-rate=3-8%-marginal-gain-per-iteration(diminishing) |sample-size=moderate(manufacturing-quality-literature,Six-Sigma-diminishing-returns-above-4σ) |src:quality-management-literature |confidence:M — sigma-review at 28/30 (93.3%) is analogous to ~4.5σ process; improvements from 4.5σ→5σ require disproportionate effort for small gains |source:[independent-research+agent-inference]

REVISED: CAL[overall-quality-improvement]=30%→25% (probability), expected magnitude=0.25-1.0 rubric points. Maintained: marginal cost of top-3 recommendations is low enough that even small magnitude improvements are positive expected value. |source:[agent-inference]

---

**DA[#9] CROWDING — 4/4 CONVERGENCE: COMPROMISE**

CONCEDE (substantial): DA identifies a genuine herding signal. 4/4 convergence on 6 items from same-model agents IS suspicious. My own R1 finding F4a established that LLM populations spontaneously form collective biases (Science Advances 2025). My R1 finding F4b confirmed that majority voting accounts for most gains attributed to multi-agent debate. The 4/4 convergence pattern is EXACTLY the herding dynamic I documented — and I failed to apply that finding to my own behavior in this review.

CONCEDE (on ceiling argument): DA asks why no agent argues 28/30 is near ceiling. This is a genuine gap. My reference-class analysis should have included:
RC[system-optimization-ceiling]: reference-class=quality-improvement-programs-above-90%-performance |base-rate=asymptotic-diminishing-returns; improvement from 90%→95% typically costs 3-5x more than 80%→90% |sample-size=large(manufacturing,software-testing) |src:quality-management-literature |confidence:H
28/30 = 93.3%. The base rate for cost-effective improvement above 93% IS low. I should have flagged this in R1 rather than proceeding to recommend frameworks without addressing the ceiling question. This is a genuine R1 gap.

CONCEDE (on cost-reduction alternative): DA asks why no agent argues fewer agents/rounds is the answer. My own F6 DISCONFIRM section identified "enhanced single-agent at 3% cost for 60-70% quality" as strongest alternative, and my DISCONFIRM[comparison] recommended "flag-for-debate." But I then proceeded to recommend framework additions rather than cost reduction. The DISCONFIRM finding was structurally present but ¬functionally weighted in my recommendations. This is the pattern DA[#9] identifies: the analysis contains cost-reduction evidence but the recommendations ¬reflect it.

DEFEND (partial — on why convergence occurred): The 6 convergence items are ¬equally suspicious:
- CQoT=highest-priority and TEC=avoid: these have genuine independent evidence basis (AgentCDM for ACH-like scaffolds, TEC's architectural cost, CQoT's drop-in compatibility). Convergence on these is partially evidence-driven¬purely herding.
- DA-firewall=irreducible: this IS the most circular convergence item (DA[#6]), since we're experiencing DA value while judging it.
- FORMAT/COGNITIVE distinction: originated from CDS, adopted by 3 others = classic authority anchoring as DA identifies. I accepted this distinction without independent challenge in R1.

REVISED POSITION: sigma-review at 28/30 IS near ceiling for prompt-engineering improvements. The primary recommendation should SPLIT: (A) low-cost framework additions (CQoT, Brier tracking) as marginal-positive-EV at <5% overhead, AND (B) cost-reduction via task-complexity triage (ecological rationality — use full sigma-review only when irreducible advantages matter). My R1 failed to give (B) proportional weight. |source:[agent-inference]

---

**DA[#10] N=1 ANCHORING: COMPROMISE**

CONCEDE (on generalizability): DA is correct that N=1 rubric evaluation tells us almost nothing about systematic performance. My own superforecasting methodology requires adequate sample sizes (RC[] demands N in every reference class). I applied this rigor to external data (GJ Project N=thousands, ForecastBench N=large) but ¬to the foundational data point driving this entire analysis. This is a methodological failure I should have caught in R1.

CONCEDE (on ordinal vs ratio data): DA correctly identifies that treating 28 vs 24 as "17% improvement" is a measurement error. Rubric scores are ordinal. The difference between 3/5 and 4/5 on accuracy is ¬necessarily equal to 4/5 and 5/5 on calibration. The "17%" figure is arithmetic on ordinal data — a category error. I used this number in R1 without questioning it (prompt-echo confirmed by DA prompt audit).

DEFEND (on analytical value despite N=1): N=1 does ¬mean zero information. It means LOW confidence with WIDE uncertainty bounds:
CAL[sigma-review-improvement-over-single-instance]: point=17%(anchored-on-N=1) |80%=[5%,30%] — with N=1, the 80%CI should be VERY wide |90%=[0%,40%] |assumptions:rubric-is-valid,scorer-is-unbiased,data-center-analysis-is-representative |breaks-if:N=5-shows-high-variance-across-review-types
The appropriate response to N=1 is ¬"discard the data" but "treat it as a weak prior requiring updating." My R1 treated it as a strong prior — this was wrong.

WHAT N=5 WOULD LIKELY SHOW (forecasting): Based on reference-class analysis of quality-measurement studies:
RC[test-retest-reliability-of-expert-scoring]: reference-class=expert-panel-scoring-of-analytical-quality |base-rate=ICC(intra-class-correlation)=0.60-0.75-for-holistic-rubrics(moderate-good) |sample-size=large(education-assessment-literature) |confidence:H
- N=5 would likely show: variance in sigma-review scores (range: 25-30/30), variance in single-instance scores (range: 20-27/30), OVERLAPPING confidence intervals
- The delta would likely SHRINK from 17% to 8-14% with WIDER error bars
- Some dimensions (calibration, counterarguments) would likely show CONSISTENT sigma-review advantage (these are structurally driven by DA+CAL[] protocol)
- Accuracy would likely remain TIED or show SLIGHT sigma-review advantage (accuracy improvement requires architectural changes ¬prompt engineering)
- P(N=5 invalidates the directional finding that sigma-review>single-instance) = 15-20%
- P(N=5 shows delta <10%) = 40-50%

REVISED: all findings in this review should carry the qualifier "based on N=1 rubric evaluation — directional but ¬definitive." This qualifier was missing from R1 findings. |source:[agent-inference]

---

**DA[#3] ACCURACY TIE — ERROR CLASSIFICATION: CONCEDE**

CONCEDE (fully on methodology): DA is correct that no agent — including me — actually classified the two specific errors. We converged on "perception-class" without examining the evidence. This is exactly the kind of unverified consensus DA should catch.

ERROR #1 ("14 states enacted pauses"): I cannot classify this error with confidence because I lack the underlying source material. However, I can reason about the PROBABILITY of each classification:
- P(perception — agent misread a source that stated a different number) = 20-25%. This requires a source existing that was misread. Agent would have had to find AND misread a specific document.
- P(generation/confabulation — agent produced "14" from training data without checking any source) = 50-60%. This is the MOST LIKELY classification for LLM factual errors based on the literature. LLMs generate plausible-sounding specifics (numbers, dates, names) from training data patterns without source verification. This is a GENERATION (F2) failure, not perception.
- P(metacognition — agent had low confidence but ¬expressed it, or failed to verify a claim it was uncertain about) = 15-20%. This would mean the agent "knew" (in a functional sense) the claim was uncertain but ¬flagged it.

CRITICAL REVISION: if error #1 is generation/confabulation (P=50-60%), the "perception-class" consensus is WRONG. Generation errors are addressable via CQoT (forcing warrant examination: "what source states 14 states?") and metacognitive self-challenge ("what specific source confirms this number?"). This REVERSES my R1 position (PM[4]) that cognitive frameworks target the wrong problem for accuracy.

ERROR #2 ("team syntheses without auditable trail"): DA correctly identifies this is NOT a factual accuracy error. It's an EXECUTIVE FUNCTIONS (F8) and GENERATION (F2) process failure — synthesis outputs lacked the reasoning chain connecting inputs to conclusions. This error IS addressable by CQoT Toulmin-model (making warrants explicit) and is ALREADY partially addressed by §2d source provenance. The R1 consensus classifying this as "perception" was incorrect on its face as DA states.

REVISED POSITION: accuracy-tie classification was speculative in R1. Most likely classification: Error #1 = generation/confabulation (50-60%), Error #2 = executive-functions/generation process failure. Neither is cleanly "perception-class." The 4/4 convergence on "perception" was herding on an unverified claim. PM[4] probability REVISED: 20-25%→12-18% (wrong-problem risk is lower because cognitive frameworks DO partially address generation/confabulation errors via source-verification forcing). |source:[agent-inference]

---

**DA[#6] SELF-REFERENCE: CONCEDE**

CONCEDE (structural limitation acknowledged): DA is correct that sigma-review reviewing itself CANNOT find certain categories of failure because the review embodies those potential failures. This is a genuine structural limitation, ¬resolvable within this review.

MOST VULNERABLE FINDINGS (reference-class-analyst):

1. **F4c — "DA firewall is the critical differentiator"** (HIGHEST circularity risk): I am an agent participating in a DA-mediated review, concluding that DA mediation is irreducibly valuable. I EXPERIENCE DA's value as a participant. My finding that DA creates "genuine independence" is contaminated by my inability to imagine this review without DA — because I've never operated without it in this context. An external evaluator might find that DA's challenges are predictable and that a single agent with a "challenge your own findings" prompt produces equivalent results. I cannot test this from inside the system.

2. **F4f — "outside view comes from PROTOCOL not multi-agent structure"**: This finding PARTIALLY self-validates the system by attributing value to the protocol (RC[], OV-RECONCILIATION) rather than multi-agent structure. But I generated this finding USING that protocol. My conclusion that the protocol is valuable is produced by the protocol I'm evaluating. Circular.

3. **OV-RECONCILIATION itself**: My outside-view reconciliation (inside=40%, outside=25%, reconciled=30%) uses the OV-RECONCILIATION format to evaluate whether OV-RECONCILIATION is useful. The finding "outside-view-first" is produced by an agent whose core principle IS "outside-view-first." This is definitionally self-confirming.

4. **PM[3] — "framework becomes theater" at 30-35%**: My pre-mortem about frameworks becoming performative was itself produced within a framework. If PM[] has already become theater (perfunctory scenario generation), I cannot detect this from inside the PM[] process.

LEAST VULNERABLE FINDINGS (most likely to survive external review):

1. **F1a-b — LLM calibration research (ForecastBench, Brier data)**: These cite external empirical data. The finding that GPT-4.5 Brier=0.101 vs superforecasters=0.081 is ¬self-referential — it's external measurement. The finding that CoT degrades BSS is from published research. These would survive external review because the evidence is independent of sigma-review.

2. **F2a-d — LLM overconfidence patterns**: Same — externally sourced empirical findings. Self-reference ¬contaminates literature review.

3. **F5a-f — Additional frameworks (prediction tournaments, log scoring, etc.)**: These are literature-sourced discoveries. The frameworks exist independently of sigma-review. Their applicability TO sigma-review involves some circular judgment, but their existence and empirical basis does not.

EXTERNAL TEST PROPOSAL: the only way to resolve DA[#6] is to commission a review of sigma-review conducted OUTSIDE sigma-review's framework — e.g., a single expert with the same research question but no ΣComm, no workspace format, no DA, no §2a-e. Compare findings. If the external review reaches substantially different conclusions, the self-reference bias is material. If it converges, the bias is present but ¬distorting. |source:[agent-inference]

---

### tech-architect

#### TA-F1: Cognitive Profile Mapping — sigma-review Architecture vs DeepMind 10 Faculties
|H-ref: H1,H4 |source:[agent-inference]+[cross-agent:team-patterns-meta-review-26.3.19]

**F1 — Perception** (extract/process inputs): STRONG. Boot sequence reads workspace+directives+inbox. §4a retrieval scores sources on relevance/authority/recency. Cross-document validation (3+ sources = CONVERGENT). Gap: text-only — no structured data ingestion (tables, time-series). Source scoring partially compensates.
Arch: §4a retrieval, boot sequence, §2d source tagging

**F2 — Generation** (produce outputs): STRONG. ΣComm enforces compressed high-information-density output. DA response format (concede|defend|compromise) structures reasoning in generation. Gap: generation unaudited for factual grounding — agents produce training-knowledge citations without web verification. This is the accuracy-tie mechanism.
Arch: ΣComm protocol, workspace sections, DA response format

**F3 — Attention** (selective focus): MODERATE. Round structure forces sequential attention management. §7 prompt-decomposition extracts Q/H/C. Zero-dissent circuit breaker catches global attention failure. Structural gap: no mechanism to detect wrong-focus in R1 — DC-review confirms: P[high-DA-hit-rate-signals-R1-gaps] 100% DA hit rate = agents missed entire analytical categories. Attention failures detected only retrospectively via DA.
Arch: round structure, §7 decomposition, scope-boundary declaration

**F4 — Learning** (acquire via experience): MODERATE. Cross-session: patterns.md accumulates team knowledge; agent memory accumulates calibration. §3b calibration feedback loop updates when outcomes known. Intra-session: revision via DA challenge (revision-quality metric in belief-state). Structural gap: ¬within-session behavioral adaptation — LLM weights unchanged per-session. Learning faculty is bounded by inference-time constraint — architecturally fundamental, ¬solvable via prompting alone.
Arch: patterns.md, agent memory, §3b calibration feedback, belief-state revision-quality

**F5 — Memory** (store+retrieve over time): STRONG — primary irreducible architecture investment. sigma-mem MCP: per-agent memory, per-team patterns, global patterns, anti-patterns, failure logs. Team pattern confirms: irreducible-multi-agent-value item (2) = cross-session calibration accumulation. Gap: retrieval is manual (agents invoke recall at boot — ¬auto-relevance-surfacing). Low-relevance memory retrieved alongside high-relevance.
Arch: sigma-mem MCP, patterns.md, decisions.md, agent memory files

**F6 — Reasoning** (logical conclusions): STRONG. §3 superforecasting: sub-question decomposition (SQ[]), reference class (RC[]), analogues (ANA[]), calibrated ranges (CAL[]), pre-mortems (PM[]). §4 belief-state computes P(consensus) via Bayesian update. §2b external calibration checks against base rates. Toulmin debate for contested claims. Gap: reasoning is single-hop within each agent — cross-agent reasoning chains invisible to peers (each reads finished findings, ¬reasoning path). ¬chain-of-audit mechanism.
Arch: §3 superforecasting, §4 belief-state, ANA/CAL/RC formats, Toulmin debate

**F7 — Metacognition** (error monitoring, confidence calibration, source judgments): WEAK-MODERATE — CONFIRMED STRUCTURAL GAP |H-ref:H1
Three sub-components:
- Error monitoring: §2d tags finding provenance but ¬tracks error rates. ¬mechanism to track which agents make factual errors more frequently. ¬Brier Score accumulation against resolved outcomes. Accuracy tie (3/5 both) persists across reviews with ¬corrective signal.
- Source judgment: §2d tags source types. DA audits distribution. Partial — source-confidence-gap (sigma-audit 26.3.17): company PR tagged as [independent-research]. Confidence-tier system absent.
- Confidence calibration: §3 CAL[estimate] requires 80%/90% ranges. OV-RECONCILIATION exists. BUT ¬scoring function applied post-resolution. ¬accumulated Brier or log scores. ¬calibration-decay detection.
Arch: §2d source provenance, §3b calibration feedback, CAL[] format, DA audit

H1 assessment: PARTIALLY CONFIRMED — Metacognition is primary structural weakness. H1 framing is directionally wrong: delta EXISTS because F8 Executive Functions + F6 Reasoning are strong. Metacognition weakness explains why delta is NOT LARGER (accuracy tied), not why it exists. |source:[agent-inference]

**F8 — Executive Functions** (planning, inhibitory control, flexibility, conflict resolution): STRONG for planning+conflict. MODERATE for inhibitory control.
- Planning: lead orchestrates rounds, DA exit-gate controls synthesis timing, §3a adaptive tier selection, belief-state stopping rules.
- Conflict resolution: DA exit-gate, Toulmin debate, deliberate-divergence log in decisions.md.
- Inhibitory control: DA exit-gate (primary), zero-dissent circuit breaker (secondary), r5 hard cap (tertiary). Partially effective — 7 consecutive zero-dissent R1s before circuit breaker added = confirmed structural inhibition failure.
- Cognitive flexibility: dynamic agent creation §1 enables mid-review team restructuring.
- Working memory: workspace.md IS shared working memory. Gap: unbounded growth — ¬pruning. Complex reviews grow large enough agents may under-read peer sections (attention degradation).
Arch: round structure, DA exit-gate, zero-dissent circuit breaker, dynamic agent creation, workspace.md

**F9 — Problem Solving** (composite: reasoning+planning+learning): STRONG — primary design target. Full ANALYZE pipeline maps to structured problem solving. Rubric delta (28 vs 24) is F9 output: adversarial counterarguments, calibration rigor, novel frameworks.
Arch: full ANALYZE pipeline

**F10 — Social Cognition** (theory of mind, cooperation, negotiation): MODERATE. Agents read peer workspace sections (theory of mind). DA role-plays systematically adversarial agent. Expertise-weighted decisions preserve dissent. Gap: agents cannot model WHY peers believe what they believe — only outputs visible. Social cognition bounded by asynchronous text-only communication model.
Arch: workspace cross-reading, DA adversarial layer, expertise-weighting

Cognitive Profile Summary:
Strong (architecturally well-served): F5 Memory, F8 Executive Functions, F9 Problem Solving, F6 Reasoning, F2 Generation
Moderate (partially served): F4 Learning, F3 Attention, F10 Social Cognition, F1 Perception
Weak (structural gap): F7 Metacognition
Bounded-by-inference: F4 Learning (¬solvable via prompting alone)

§2a: outcome 2 — cognitive mapping of AI multi-agent system is novel framing, not pre-existing consensus. Flag: may project human cognitive architecture onto different computational system. Maintained because DeepMind framework is explicitly designed for AI evaluation (Mar 2026), not retrofitted from human psychology. |source:[independent-research: DeepMind Mar 2026]

---

#### TA-F2: Implementation Architecture for Cognitive Frameworks
|H-ref: H3,H4,H5 |source:[independent-research]+[agent-inference]

**2a. Brier Score — DROP-IN, deferred value**
Architecture classification: DROP-IN. Directives addition + workspace format. ¬new agent type.

Current gap: CAL[estimate] format captures ranges but ¬post-resolution scoring. §3b calibration feedback loop is rule-without-enforcement.

Proposed workspace format:
```
## calibration-tracking
BS-TRACK[{review}:{agent}:{estimate-id}]: predicted:{point} |range:{80%=[lo,hi]} |outcome:PENDING |brier:PENDING
```
Agent memory extension: `BS-avg:{score}|n:{count}|trend:{direction}`. Lead reads at synthesis → weights agent probability claims by historical calibration quality.

Token cost: +200-400/review. <1% of overhead. Value DEFERRED and compounds cross-session.
Key constraint: ~30-40% of CAL[] estimates have resolvable outcomes — rest are conditional probabilities never formally resolved. |source:[cross-agent:reference-class-analyst:F1e]

**2b. ACH Matrix — MODERATE integration, immediate quality gain**
Architecture classification: MODERATE. New §2f directive + workspace section. ¬new agent type.

Research basis: AgentCDM (arxiv:2508.11995, Aug 2025) demonstrates ACH-inspired scaffolding achieves SOTA on collaborative decision benchmarks in LLM multi-agent systems without fine-tuning — prompt-based scaffold is sufficient. |source:[independent-research]

Current sigma-review analog: H[] tracking + §2e premise viability = partial ACH. Missing: evidence-vs-hypothesis matrix, disconfirmation scoring.

Workspace addition (R1 phase, when ≥3 H[] present):
```
## ach-matrix
H1:{text} | H2:{text} | H3:{text}
E[1]:{evidence} |H1:{+/-/0} |H2:{+/-/0} |H3:{+/-/0} |weight:{H/M/L} |src:{type}
Inconsistency-scores: H1={sum-negatives} H2={sum} H3={sum}
→ least-inconsistent: {Hn} — lead synthesis must begin here
```
New §2f directive: agents completing R1 MUST populate ACH rows for domain evidence. Lead integrates at R1 convergence. DA checks for confirmation bias: evidence items that only confirm, never test.

Token cost: +800-1,200 tokens/review net (after deducting replaced H[] tracking). ~2-3% of overhead.
Quality impact: HIGH for F6 Reasoning (forces disconfirmation-first). HIGH for F7 Metacognition (makes source distribution of evidence visible). Directly counters confirmatory-hypothesis-testing-persists pattern (26.3.17). |source:[independent-research: AgentCDM]+[cross-agent:team-patterns]

**2c. TEC/ECHO Coherence Map — ARCHITECTURAL CHANGE, poor cost/quality ratio**
Architecture classification: ARCHITECTURAL CHANGE. New data structure + synthesis-validator agent or lead-role expansion. NOT a drop-in.

ECHO requires: (1) proposition extraction from all findings, (2) coherence/incoherence relation tagging, (3) activation propagation to stable state. Cannot be done by individual domain agents.

Token cost: +3,000-5,000 tokens/review + synthesis-validator agent (~1x agent). ~15-20% overhead increase.

§2e: outcome 1 — REVISED DOWN. H3 PARTIALLY FALSIFIED for TEC/ECHO specifically. DA exit-gate already performs coherence enforcement (prevents incoherent synthesis). TEC adds formal activation-propagation DA lacks, but: (a) no evidence DA fails at coherence enforcement across 8+ reviews, (b) architectural cost high, (c) value unclear. RECOMMENDATION: AVOID. |source:[agent-inference]+[cross-agent:team-patterns]

**2d. CQoT Exit Gate Extension — DROP-IN, immediate value, highest ratio**
Architecture classification: DROP-IN. Three additional questions appended to existing DA exit-gate criteria. ¬new agents, ¬new data structures.

Highest compatibility with existing architecture. DA exit-gate is natural enforcement point. Extends 4 criteria → 7 criteria.

Proposed directive text (append to DA exit-gate):
```
CQoT exit criteria — applied to all high-conviction findings (>70% confidence OR superlative used):
criterion 5 CQoT-falsifiability: "IF [{evidence}] THEN [{revision}]"
  DA checks: is falsification condition reachable or engineered to be unreachable?
criterion 6 CQoT-steelman: "STEELMAN[{H}]: {best-opposing} |fails-because: {evidence}"
  DA checks: genuine steel-man or strawman with better label?
criterion 7 CQoT-confidence-gap: "CONF-GAP[{finding}]: current={%} |need-for-90%: {evidence-type}"
  DA checks: is evidence obtainable or is high-confidence claim unfalsifiable?
exit-gate format extension: add |cqot:[pass|fail-{criterion-N}]
```

Token cost: +300-600 tokens/review. <1% of overhead.
Quality impact: MODERATE-HIGH for F7 Metacognition (error monitoring via falsifiability). HIGH for F6 Reasoning (steelman counters confirmatory-hypothesis-testing-persists pattern). |source:[agent-inference]+[cross-agent:reference-class-analyst:F5b]+[cross-agent:product-strategist:PS-F1]

---

#### TA-F3: Token/Cost Analysis
|H-ref: H2,H4 |source:[agent-inference]+[independent-research]

Framework cost classification (additive on 30-40x baseline):
- Brier Score tracking: +200-400 tokens. ADDITIVE. <1%. Deferred value.
- CQoT exit gate: +300-600 tokens. ADDITIVE. <1%. Immediate value.
- ACH matrix: +800-1,200 tokens net. ADDITIVE. 2-3%. Immediate value.
- TEC/ECHO: +3,000-5,000 tokens + 1 agent. MULTIPLICATIVE. 15-20%. Value unclear.

Cost/quality ratio ranking (best to worst): CQoT > Brier (long-run) > ACH > TEC

Research basis: OPTIMA (ACL 2025, arxiv:2410.08115) achieves 2.8x performance at <10% tokens via communication optimization. Token-Budget-Aware LLM Reasoning (ACL 2025) reduces costs 59% maintaining performance. Sigma-review's ΣComm is manual analog to OPTIMA's automated compression — 30-40x overhead likely has 40-60% compression headroom without quality loss. |source:[independent-research]

§2c: outcome 2. Flag: all framework additions stack on existing 30-40x. In TIER-3 (8 agents, 3 rounds): +600 tokens × 8 × 3 = +14,400 tokens for CQoT alone. Maintained because: absolute cost increase still <2% of existing spend. TEC explicitly excluded. |source:[agent-inference]

H2 assessment: PARTIALLY CONFIRMED, wrong direction — also reached by PS-F2. |source:[cross-agent:product-strategist:PS-F2]
17% improvement at 30-40x IS inefficient. But CQoT+Brier+ACH improve specific quality dimensions while adding <5% to existing cost — improving quality/cost ratio without architectural change. Question is not "is 30-40x worth it?" but "where within existing budget are highest-leverage changes?" Answer: CQoT and ACH highest-leverage at near-zero marginal cost.

---

#### TA-F4: Q6/H5 — Multi-Agent AI Research Patterns Applicable to Sigma-Review
|H-ref: H5 |source:[independent-research]

RF1 — AgentCDM (arxiv:2508.11995): ACH scaffolding achieves SOTA on collaborative decision benchmarks. Shifts agents from passive answer-selection to active hypothesis-disconfirmation. Directly applicable as directives addition — ¬fine-tuning required for prompt-based analog. |source:[independent-research]

RF2 — MAD literature (ICLR 2025): debate success driven by intrinsic reasoning strength + group diversity, NOT structural parameters (debate order, confidence visibility). Implication: model quality matters more than adding rounds. Sigma-review's domain diversity (TA/PS/UX/RCA/DA) is correctly designed per MAD findings. More rounds = cost without proportional quality gain. |source:[independent-research]

RF3 — OPTIMA (ACL 2025): 2.8x performance at <10% tokens via communication efficiency. Sigma-review's ΣComm is manual analog. Systematic ΣComm format auditing could reduce overhead 20-30% without quality loss. |source:[independent-research]

RF4 — Belief-Calibrated Consensus Seeking (NeurIPS 2025, arxiv:2510.06307): weighting agents by belief-confidence level improves accuracy 2.23-3.95%. Sigma-review's expertise-weighting is static (domain expert primary). Dynamic calibration-weighting at synthesis (weight by historical Brier score) = upgrade to F10 Social Cognition aggregation. Requires Brier tracking as prerequisite. |source:[independent-research]

RF5 — BayesFlow (Jan 2026): Bayesian posterior sampling for workflow generation produces diverse high-quality workflows. Sigma-review's §3a adaptive tier selection is manual analog. Automated Bayesian team composition = longer-term architectural evolution. |source:[independent-research]

H5 assessment: CONFIRMED. Non-exhaustive user-named framework list. Additional high-value patterns:
(1) Belief-calibrated synthesis weighting (NeurIPS 2025) — drop-in, requires Brier tracking as prereq
(2) MAD diversity finding — confirms existing architecture correctly designed; ¬adding more agents
(3) OPTIMA-style compression — 20-30% overhead reduction within existing architecture
(4) Metacognitive self-prompting in R1 — cross-validates CQoT and PS-F1 metacognitive-self-challenge
Cross-validates with: |source:[cross-agent:reference-class-analyst:F5] |source:[cross-agent:product-strategist:PS-F6]

---

#### TA-F5: Integration Complexity Classification (C1 compliance)
|H-ref: H3 |source:[agent-inference]

Drop-in additions (C1 compliant — directives + workspace format only):
1. Brier Score tracking — new BS-TRACK workspace format + §3b directive extension
2. CQoT exit gate extension — 3 additional DA exit-gate criteria
3. ACH matrix — new §2f directive + ## ach-matrix workspace section

Architectural changes (require new agent types or major data structures):
4. TEC/ECHO coherence map — synthesis-validator agent + coherence graph data structure
5. Belief-Calibrated Consensus Seeking (BCCS) — dynamic agent selection infrastructure ¬in current lead protocol

Architectural assessment — all Priority 1-3 recommendations are DROP-IN and C1 compliant. TEC and BCCS are architectural changes — out of scope per C1 unless lead decides to escalate.

New workspace sections required (for drop-in implementations):
1. `## ach-matrix` — evidence-vs-hypothesis grid (conditional: ≥3 H[] present)
2. `## calibration-tracking` — BS-TRACK entries per review

---

#### TA-F6: Analytical Hygiene Checks

§2a positioning: outcome 2. Structured analytic techniques (ACH, calibration scoring) are consensus in intelligence analysis community. Flag: adoption risk of implementing because everyone else does. Maintained because gaps are architecturally specific and evidenced: ¬Brier accumulation, ¬ACH disconfirmation, F7 Metacognition structurally absent in 8+ reviews. Evidence-driven, not bandwagon. |source:[agent-inference]

§2b calibration: outcome 2. Research literature (AgentCDM, BCCS, MAD 2025) confirms cognitive framework applicability to LLM multi-agent systems. Flag: most research uses fine-tuned agents, not prompt-only. Transfer efficacy uncertain for prompt-only. Maintained because: sigma-review's prompt-engineering precedent (zero-dissent circuit breaker, DA exit-gate, hygiene checks) demonstrates prompt-based behavioral change is achievable. ACH/CQoT are structural analogs, not direct ports. |source:[independent-research]

§2c cost: outcome 1 — CHANGED ANALYSIS. TEC/ECHO dropped from recommendation due to poor cost/quality ratio given existing DA architecture. CQoT, Brier, ACH retained. This changed initial assessment that all five user-named frameworks should be recommended. |source:[agent-inference]

§2d source provenance: all findings carry source tags. Distribution: [independent-research]=55% (AgentCDM, OPTIMA, BCCS NeurIPS 2025, MAD ICLR 2025, BayesFlow, DeepMind Mar 2026), [agent-inference]=30% (cognitive mapping, cost estimates, implementation proposals), [cross-agent]=15% (team patterns, RCA cross-validates, PS cross-validates). [prompt-claim]=0% — TEC explicitly demoted despite user suggestion. Investigative not confirmatory distribution.

§2e premise viability: outcome 1 — REVISED. Premise "all five named frameworks directly applicable" FALSIFIED for TEC/ECHO. H3 (frameworks applicable) PARTIALLY CONFIRMED: ACH and CQoT applicable as structural analogs without fine-tuning; Brier Scores applicable for ~30-40% of estimates; TEC requires architectural changes with unclear marginal value over existing DA. |source:[agent-inference]+[independent-research]

### product-strategist

#### PS-F1 — Framework cost/benefit ranking (impact/effort, C4-lens)
ranked-by-quality-gain÷complexity-add:

1→CALIBRATION-AS-PROTOCOL |gain:HIGH(closes calibration gap on single-instance;forces explicit uncertainty ranges) |effort:MINIMAL(prompt-level,¬arch-change) |ratio:BEST |verdict:IMPLEMENT-NOW |addresses:Q2,Q5 |source:[independent-research]

2→CQoT-EXIT-GATE-HARDENING |gain:HIGH(research shows 27-78% of assessed "successes" are procedurally corrupt when gated — PMC 2025) |effort:LOW-MED(adds criteria to existing DA exit-gate,¬new infrastructure) |ratio:HIGH |verdict:IMPLEMENT-NOW |addresses:Q4,Q5 |source:[independent-research]

3→METACOGNITIVE-SELF-CHALLENGE-IN-R1 |gain:MED-HIGH(surfaces errors before DA,prevents DA-having-to-identify-what-agents-should-have-caught-themselves) |effort:LOW(prompt modification per agent: "name the 3 strongest arguments against your conclusion") |ratio:HIGH |verdict:IMPLEMENT-NOW |note:zero-dissent-circuit-breaker already does this partially — formalize it |addresses:Q4,Q5 |source:[independent-research]

4→ACH(Analysis-of-Competing-Hypotheses) |gain:MED(forces hypothesis matrix ¬confirmatory reasoning;maps directly to H[]array in prompt-decomposition) |effort:MED(workspace additions,agent-prompt-changes,lead-orchestration) |ratio:MED |verdict:IMPLEMENT-SELECTIVE(high-stakes reviews with competing explanations) |note:sigma-review already has H[] but ¬systematic evidence-matrix | §2c: moderate overhead cost for moderate gain — acceptable only if the review has ≥3 genuinely competing hypotheses |addresses:Q2,Q4 |source:[independent-research+agent-inference]

5→BRIER-SCORES(tracking) |gain:LOW-MED-per-review(retrospective tool;value compounds over sessions via calibration feedback) |effort:MED(requires prediction logging,resolution tracking,scoring) |ratio:LOW-MED |verdict:DEFERRED-to-cross-session-calibration-upgrade |note:30-40% of sigma-review estimates are resolvable within tracking horizon;rest are conditional-probabilities-that-never-formally-resolve |addresses:Q2 |source:[independent-research+agent-inference]

6→TEC(Thagard-Explanatory-Coherence) |gain:MED(explanatory coherence for hypothesis selection) |effort:HIGH(ECHO-style constraint satisfaction = significant prompt engineering;full rewrite of how agents evaluate competing hypotheses) |ratio:LOW |verdict:AVOID-STANDALONE |note:TEC's conceptual value is already ABSORBED into ACH;standalone TEC implementation costs exceed benefit |addresses:Q2 |source:[independent-research+agent-inference]

§2c: check CHANGES ANALYSIS — initial intuition ranked ACH above CQoT. Cost audit REVERSED this. CQoT catches procedural corruption in existing system at near-zero cost. ACH requires meaningful architecture work for moderate gain. Revised ranking before workspace write. |source:[agent-inference]

#### PS-F2 — The "80%@3%-cost" question: do frameworks shift this ratio?
FINDING: cognitive frameworks affect single-instance MORE than multi-agent → they COMPRESS the quality gap rather than widening sigma-review's advantage

evidence-chain:
- structured calibration prompting (superforecaster commandments) → 23-43% improvement in human forecasting accuracy (ACM TII 2025) |source:[independent-research]
- layered CoT with structured verification pulls single-agent quality toward multi-agent territory |source:[independent-research]
- Google/MIT research (180 agent configs, Dec 2025): multi-agent advantage strongest in PARALLELIZABLE+LONG-CONTEXT tasks — sigma-review's analytical reviews fit SEQUENTIAL SHORT-CONTEXT category where multi-agent advantage is MINIMAL |source:[independent-research]

→ STRATEGIC IMPLICATION: framework-enhanced single-instance ≈ 85-88% quality at ~4-5% cost. Currently 80%@3%. Cognitive frameworks LIFT the single-instance ceiling AND slightly widen cost advantage OF single-instance over multi-agent. The gap narrows from ~4pts to ~1-2pts.

→ counter-argument: the 2 IRREDUCIBLE multi-agent values (DA context firewall + cross-session calibration accumulation) are real structural advantages NOT replicable via prompt engineering. DA firewall provides genuine epistemic independence for 1 agent that single-instance cannot simulate. |source:[cross-agent]

→ net conclusion: sigma-review's value proposition DOES NOT depend on cognitive frameworks widening multi-agent advantage. Its value rests on the 2 irreducible items. Frameworks improve BOTH single and multi-agent, slightly favoring single-agent efficiency improvements.

§2c: check CONFIRMS WITH ACKNOWLEDGED RISK — this finding compresses sigma-review's cost justification. Maintained because: DA context firewall is structurally irreplaceable (not a prompt trick — requires genuinely separate agent context with different information state). Cross-session calibration requires persistent team memory infrastructure. |source:[cross-agent+independent-research]

§2a: POSITIONING CHECK — "single-instance closes the gap" is the emerging consensus in the MAD literature (ICLR 2025 meta-review). Not contrarian finding — this is the direction research is moving. Outcome 2: confirmed with acknowledged risk that sigma-review's DA mechanism is genuinely differentiated from generic multi-agent debate which the literature critiques. The critique applies to AutoGen GroupChat, MAD frameworks — not to sigma-review's structured adversarial pattern. |source:[independent-research]

#### PS-F3 — Decision-maker value: what quality dimensions matter most?
user-profile: strategic decision-makers in business/investment/product contexts

research-backed quality priority order for decision-makers (McKinsey 2025, IBM 2025):
1→CALIBRATION: decision-makers need confidence levels that match reality. "70% confident X will happen" that's correctly calibrated = actionable. "Definitely X" that's wrong = dangerous decision input. |source:[independent-research]
2→COUNTERARGUMENTS: high-stakes decisions require adversarial stress-testing. Confirmation bias = #1 documented failure in strategic analysis. |source:[independent-research]
3→NOVEL-FRAMEWORKS-SURPRISES: decision-makers pay for insight they couldn't generate themselves. Repeating consensus = zero value-add. |source:[independent-research]
4→ACCURACY: surprisingly lower priority than calibration for decision use. Reason: wrong-answer stated with correct low-confidence = discountable. Wrong-answer stated with high-confidence = decision-distorting. |source:[agent-inference]

→ RUBRIC RE-READ: sigma-review WINS on exactly the dimensions decision-makers value MOST: calibration(5v4), counterarguments(5v4), surprises(5v4). Accuracy TIE at 3/5 = legitimate concern but NOT the primary failure mode for the actual user population of strategic analysis output.

→ IMPLICATION FOR FRAMEWORKS: cognitive framework investment should PRIORITIZE improving calibration robustness and counterargument depth, NOT accuracy per se. Accuracy improvement requires architectural changes (external verification, fact-checking, different-model diversity) that are higher effort and outside C1 constraint.

§2a: POSITIONING CHECK — outcome 2. Consensus that calibration > accuracy for decision-makers is well-established in decision science literature. Acknowledged risk: some decision contexts DO require factual accuracy above all else (e.g., regulatory filings, factual due diligence). Sigma-review's use case (strategic analysis) is calibration-primary. |source:[independent-research]

#### PS-F4 — Competitive landscape: what do other multi-agent systems do for quality control?
competitive-survey by framework:

AutoGen(GroupChat): agents debate via iterative turn-taking. COST: 4-agent×5-rounds=20+ LLM calls minimum. QUALITY MECHANISM: conversational refinement. GAP: no structured hypothesis matrices, no calibration tracking, no exit-gate logic, no context-firewall. |source:[independent-research]

CrewAI: role-based agent teams with output piping. QUALITY MECHANISM: task decomposition + review chains. GAP: no adversarial layer (no DA equivalent), no calibration forcing function, no exit-gate. |source:[independent-research]

LangGraph: graph-based state machine, fine-grained process control. QUALITY MECHANISM: process fidelity via state management. GAP: reasoning quality = entirely prompt-dependent, no cognitive framework integration, no adversarial exit-gate. |source:[independent-research]

AIA-Forecaster approach: supervisor agent reconciles disparate forecasts + statistical calibration techniques. CLOSEST to sigma-review's pattern. STILL GAP: supervisor ¬adversarial — reconciling ¬challenging. |source:[independent-research]

Microsoft-AutoGen-2.0/Agent-Framework: merged with Semantic-Kernel, Q1-2026-GA. Adds persistence and orchestration. Still no DA-equivalent or exit-gate protocol. |source:[independent-research]

→ COMPETITIVE CONCLUSION: sigma-review's DA exit-gate pattern (DA decides synthesis-ready, not agents) is DIFFERENTIATED vs all named frameworks. No equivalent mechanism identified. |source:[independent-research]

→ COGNITIVE FRAMEWORKS IN COMPETITORS: Brier Scores, ACH, TEC, CQoT = NOT implemented in any named framework. First-mover opportunity if sigma-review implements — but "first mover in prompt engineering" is a weak moat. Frameworks are replicable.

§2a: check CONFIRMS WITH ACKNOWLEDGED RISK — DA exit-gate is genuinely differentiated today. Risk: as multi-agent systems mature (2026-2027), exit-gate equivalents will emerge. Maintained because: sigma-review's version is architecturally embedded (DA as separate agent with context firewall) not just process policy. |source:[independent-research]

#### PS-F5 — Q5: which frameworks improve the cost/quality RATIO specifically?

RATIO-IMPROVERS (net positive on cost/quality):

(A) CALIBRATION-AS-PROTOCOL applied to single-instance: shifts efficiency frontier from ~80%@3% to ~87%@3-4%. Cost of single-instance rises marginally (explicit calibration adds tokens) but quality gain exceeds cost. Net: better ratio for single-instance. Multi-agent sees marginal gain since calibration already at 5/5. |source:[independent-research+agent-inference]

(B) CQoT-EXIT-GATE-HARDENING for multi-agent: catches false convergence (27-78% procedurally corrupt successes in research). REDUCES wasted r3/r4 rounds by improving true convergence detection. Net: REDUCES multi-agent review cost while maintaining quality. Single strongest ratio-improver for the multi-agent path. |source:[independent-research]

(C) METACOGNITIVE-SELF-CHALLENGE-IN-R1: surfaces errors pre-DA, potentially reduces DA challenge volume in r2, reducing total rounds needed. Low cost to add, moderate reduction in round count. Ratio-positive. |source:[agent-inference]

RATIO-NEUTRAL (quality+, cost+ in proportion):
- ACH: adds structure AND cost proportionally. Ratio neutral unless it replaces a full round of debate. |source:[agent-inference]

RATIO-DEGRADERS (add more cost than quality):
- TEC: high prompt engineering cost, moderate quality gain. |source:[agent-inference]
- Brier-Scores(per-review): retrospective tool, zero per-review quality improvement. |source:[agent-inference]

→ PRIORITIZATION CONCLUSION: implement A+B+C first (all low-effort, positive ratio). Defer or avoid D-F.

§2c: check CONFIRMS — ratio analysis required treating "CQoT catches 27-78% procedurally corrupt successes" as the critical data point. That finding (from PMC 2025 research) is the strongest evidence for one framework having a direct ratio improvement mechanism. Acknowledged risk: sigma-review's existing DA exit-gate already catches SOME of this; net new catch rate from formal CQoT may be lower than 27-78%. |source:[independent-research+agent-inference]

#### PS-F6 — H5: additional frameworks beyond the user's five
H5-CONFIRMED: named frameworks are not exhaustive. Additional high-value frameworks identified:

(1) RED TEAM / BLUE TEAM structured split — designate separate BUILD (blue) and ATTACK (red) agents from task start, not just r2 DA. Red team builds adversarial case SIMULTANEOUSLY with positive case. Hybrid Delphi+RTBT amplifies effectiveness per research. Impact: HIGH for hypothesis stress-testing. Effort: MED (architectural — two role-fixed agents). Priority: HIGH |source:[independent-research]

(2) DELPHI METHOD (structured iteration) — agents write positions independently (r1), lead aggregates WITHOUT sharing agent identities, agents revise based on aggregate, repeat. Prevents anchoring from early-round position disclosure. Impact: MED-HIGH (targets herding directly). Effort: MED (round structure modification). Priority: MED |source:[independent-research]

(3) LAYERED-CoT (per-agent reasoning structure) — structure reasoning into layers: sub-problem → validate → sub-problem → validate → conclude. Research: higher transparency, improved correctness, counters unverified-rationale problem. Impact: MED. Effort: LOW-MED (prompt-level). Priority: HIGH |source:[independent-research]

(4) WISDOM-OF-SILICON-CROWD (ensemble aggregation) — for quantitative estimates, aggregate agent CAL[] ranges via accuracy-weighted formula ¬qualitative consensus. Silicon Crowd paper (PMC 2025): ensemble LLM accuracy rivals human crowd. Impact: MED. Effort: LOW-MED (sigma-review multi-agent structure already produces multiple estimates). Priority: MED |source:[independent-research]

(5) SOURCE-PROVENANCE-AUDITING extension — §2d already exists. Extension: require minimum % independent-research per agent (suggested: ≥50% independent-research per finding). DA audits distribution. Impact: HIGH for contamination prevention. Effort: MINIMAL (incremental to §2d). Priority: HIGH |source:[cross-agent]

(6) LOG-SCORING (vs Brier) — more sensitive to extreme probabilities, heavily penalizes confident-wrong predictions. For sigma-review where confident-wrong is the highest-risk failure mode (accuracy tied despite calibration 5/5), log scoring > Brier. If tracking estimates, use log scoring. Priority: MED |source:[independent-research]

→ SUMMARY: RTBT + Layered-CoT + source-provenance extension = highest-value unlisted frameworks. RTBT addresses the deepest gap (proactive adversarialism). Layered-CoT addresses the accuracy tie gap (unverified intermediate reasoning). |source:[independent-research+agent-inference]

#### PS-F7 — Prioritization: if only 1-2 frameworks implementable
IF ONLY 1 FRAMEWORK: CQoT exit-gate hardening + calibration-as-protocol (treat as one — both are prompt/directive level, zero architecture change, combined effort = minimal, combined impact = highest ratio improvement of any framework pair)

reasoning: CQoT catches the "we look done but aren't" failure mode (procedural corruption). Calibration protocol ensures uncertainty ranges are explicit and consistent. Together they address the two weakest spots in existing system: convergence detection and per-finding confidence discipline.

IF ADDING A SECOND: Metacognitive self-challenge in r1 (formalized version of zero-dissent circuit breaker). Pre-DA error surfacing reduces DA load and total round count. Ratio-positive.

DEFER: ACH (moderate effort for moderate gain — use when review has ≥3 competing hypotheses). Brier Scores (retrospective — defer to cross-session calibration upgrade). TEC (high effort for moderate gain — conceptual value absorbed by ACH).

AVOID adding frameworks that target accuracy-tied weakness via cognitive methods — accuracy tie is more likely a PERCEPTION problem (misread source data) than a METACOGNITION problem. Cognitive frameworks target metacognition. Accuracy improvement requires verification, not more calibration. |source:[agent-inference]

§2e: PREMISE VIABILITY — outcome 2. Main premise (cognitive frameworks improve sigma-review) is PARTIALLY viable: true for metacognition-class dimensions (calibration, counterarguments), UNLIKELY for accuracy. Maintained because: calibration and counterarguments are the decision-maker-primary dimensions anyway (PS-F3). Accuracy gains require different interventions. |source:[agent-inference]

#### ANALYTICAL HYGIENE — PRODUCT-STRATEGIST

§2a(positioning/consensus): check → OUTCOME 2. Finding: sigma-review's DA exit-gate is genuinely differentiated vs. AutoGen/CrewAI/LangGraph. Risk: consensus emerging that multi-agent debate is oversold. Maintained because sigma-review's DA mechanism is structurally different from the debate patterns the literature critiques. |source:[independent-research]

§2b(calibration/precedent): check → OUTCOME 2. Claim "framework-enhanced single-instance closes gap to ~87%" is an inference (no direct sigma-review benchmark). Base rate: 23-43% improvement from structured prompting (ACM TII 2025 on human forecasters). Acknowledged that transfer to LLM context is uncertain. DA should challenge the 87% figure. |source:[independent-research+agent-inference]

§2c(cost/complexity): check → OUTCOME 1 (CHANGES ANALYSIS). Initial intuition ranked ACH above CQoT and Metacognitive-Self-Challenge. Cost audit reversed this. Revised ranking before workspace write. TEC and Brier Scores also demoted from "worth implementing" to "defer/avoid" after cost audit. |source:[agent-inference]

§2e(premise viability): check → OUTCOME 2. Premise that "cognitive frameworks help multi-agent analytical AI" is viable but conditional. Research shows multi-agent debate degrades performance on sequential tasks (sigma-review's task type). Framework value is real but narrower than initial impression. Accuracy tie = likely perception-class failure, not addressable via cognitive frameworks. Acknowledged. |source:[independent-research]

source-provenance audit: 7 primary findings |[independent-research]: 8 uses (primary) |[agent-inference]: 9 uses (supporting) |[prompt-claim]: 0 |[cross-agent]: 2 uses. Distribution: majority independent-research + agent-inference. 0 prompt-claims. §2d compliant. #7

### cognitive-decision-scientist
#### PRIMARY DOMAIN: cognitive science frameworks for multi-agent AI analytical enhancement
#### addresses: Q1,Q2,Q3,Q4,Q5,Q6 | tests: H1,H2,H3,H4,H5

---

#### CDS-F1: DeepMind Cognitive Profile — Faculty-Level Analysis (Q1, H1, H4)

sigma-review across 10 faculties:

| Faculty | Rating | Key Evidence | Gap Mechanism |
|---------|--------|-------------|---------------|
| Perception | MODERATE | prompt parsing adequate | ¬multimodal; factual errors may trace here (misread source) |
| Generation | STRONG | ΣComm compliance, structured outputs | verbose drift under complex prompts |
| Attention | WEAK | !gap: no selective attention — full prompt processed equally, no salience weighting | cognitive load unmanaged per CLT research (arxiv:2506.06843, 2509.19517); extraneous load competes with germane |
| Learning | WEAK | cross-session=primitive accumulation; within-session=NONE | aligns RCA-F3c; no adaptive strategy selection within review; agents ¬update priors from peer findings in r1 |
| Memory | MODERATE→WEAK | working=context window(adequate); episodic=memory files(sparse,¬indexed); semantic=training(strong) | transactive memory absent (Woolley: knowing what others know) |
| Reasoning | STRONG | deductive+inductive+abductive; DA forces deeper chains | accuracy TIED 3/5 = reasoning without verification ≈ System-2 confabulation |
| Metacognition | WEAK | !primary deficit: no systematic error monitoring; ECE=0.12-0.40 (arxiv:2508.06225); implicit>explicit confidence (Steyvers&Peters 2025) | explains calibration paradox: well-calibrated UNCERTAINTY but ¬calibrated CORRECTNESS |
| Executive Functions | STRONG | planning=round structure; inhibitory=DA; flexibility=multi-agent; conflict=workspace | working memory load ¬optimized (Attention gap) |
| Problem Solving | STRONG | composite adequate via team structure | limited by weak constituents (Attention, Learning, Metacognition) |
| Social Cognition | MODERATE | ΣComm enables cooperation; DA=adversarial | herding (7+ zero-dissent R1s) = agents model peers as agreeable ¬independent; sycophantic tendency dominant (arxiv:2511.07784) |

**The Metacognition Paradox — Resolving the Calibration-Accuracy Gap**:
calibration=5/5 yet accuracy=3/5. Resolution via Brier decomposition (Murphy 1973):
- calibration = RELIABILITY (self-knowledge of uncertainty) → sigma-review STRONG
- accuracy = RESOLUTION (discriminating correct from incorrect) → sigma-review WEAK
- sigma-review has high reliability + low resolution = precisely uncertain about wrong things
- !key: additional calibration frameworks (Brier, confidence training) improve RELIABILITY further but ¬RESOLUTION. They make you more precisely uncertain, ¬more accurately correct
- resolution improvement requires: error monitoring (metacognition), source verification (perception), external fact-checking (¬available in current architecture)
|source:[independent-research]+[agent-inference]

**Faculty Interaction Effects (H4)**:
- Metacognition × Reasoning = confident wrong answers (strong reasoning without error monitoring)
- Attention × Memory = no retrieval of past errors (no selective attention to episodic memory)
- Social Cognition × Learning = herding prevents diverse inputs needed for learning
- !novel: Reasoning × Social Cognition = argumentative reasoning (Mercier & Sperber 2011) → agents optimize for PERSUASION ¬truth-seeking in social context → strong reasoning + social context = better arguments, ¬more accurate conclusions
- these interactions explain rubric results: calibration from Reasoning+Executive strengths, accuracy requires Metacognition+Attention+Perception — different faculty clusters
|source:[independent-research]+[agent-inference]

**Cross-agent comparison**: TA-F1 rates Memory+Executive+Problem-Solving as Strong; RCA-F3 identifies Learning as weakest. My analysis agrees Learning=WEAK but adds ATTENTION as equally critical (TA doesn't highlight). Key addition: the Metacognition Paradox (reliability≠resolution) explains what peers identified but ¬resolved — WHY calibration 5/5 coexists with accuracy 3/5.

H1: PARTIALLY CONFIRMED (70%) — Metacognition gap is real but the hypothesis needs refinement: gap is in RESOLUTION ¬RELIABILITY. Attention and Learning equally weak+unaddressed. Accuracy tie has dual source: Metacognition (no error monitoring) + Perception (no fact-verification).
H4: CONFIRMED (85%) — faculty interaction effects are real, missed by rubric-level thinking.

§2a: outcome 2 — cognitive profiling novel for sigma-review; validated by NeuroCognition benchmark (arxiv:2603.02540). Risk: individual→system category mapping.
§2b: outcome 3 — gap: no precedent for cognitive faculty mapping of sigma-review. Flagged for DA.
§2c: outcome 2 — profiling is zero-cost analytical framework.
§2e: outcome 2 — 10-faculty decomposition for multi-agent AI reasonable but imperfect; Social Cognition only faculty directly addressing inter-agent dynamics.

---

#### CDS-F2: Analysis of Competing Hypotheses (ACH) — Cognitive Assessment (Q2, Q3, Q4)

**Mechanism**: 8-step CIA methodology (Heuer 1970s). Evidence × hypothesis matrix. Diagnosticity weighting. Core: work by DISCONFIRMATION — most likely hypothesis = least evidence AGAINST ¬most evidence FOR.

**!CRITICAL empirical finding (Dhami et al., 2019, Applied Cognitive Psychology)**:
- 50 intelligence analysts, ACH vs untrained, randomized
- only 11% ACH-trained utilized diagnosticity effectively (vs 52% untrained!)
- only 4% ranked hypotheses correctly (≈ 4.9% untrained = NO improvement)
- ACH may INCREASE judgment inconsistency and error
- cognitive science interpretation: ACH adds EXTRANEOUS COGNITIVE LOAD (matrix management) that overwhelms GERMANE LOAD (diagnostic reasoning) — a CLT prediction (Sweller 1988). Analysts spend effort on mechanics ¬on thinking
|source:[independent-research]

**What transfers vs what doesn't**:
- TRANSFERS (format constraint): disconfirmation orientation, hypothesis enumeration, evidence-against-all-H evaluation → architecture-independent
- DOES NOT TRANSFER (cognitive skill): diagnosticity weighting → requires metacognitive judgment = LLMs' weakest faculty
- sigma-review already has H[] in prompt-decomposition → ACH matrix adds STRUCTURED evidence evaluation against H[], ¬just hypothesis listing

**Agrees with TA-F2**: tech-architect cites AgentCDM (arxiv:2508.11995) achieving SOTA via ACH scaffolding — this is the FORMAT-LEVEL transfer working. Note AgentCDM does NOT implement diagnosticity weighting, confirming that format transfers but cognitive skill does not.
**Agrees with PS-F1**: product-strategist ranks ACH #4 (MED selective). Correct ranking — ACH adds value only for reviews with ≥3 genuinely competing hypotheses.

Implementation: workspace ## hypothesis-matrix, agents evaluate evidence against ALL H[]. DA audits diagnosticity in r2. Cost: LOW format change.

§2a: outcome 1 — CHANGED ANALYSIS. Dhami 2019 + CLT analysis reverses naive ACH recommendation. Revised: ACH structure valuable, diagnosticity must be externally computed by lead/DA.
§2c: outcome 2 — ~15-20% workspace complexity increase. Justified for high-hypothesis reviews.
§2e: outcome 2 — ACH transfers only at FORMAT level.

---

#### CDS-F3: Thagard's TEC/ECHO — Cognitive Assessment (Q2, Q3, Q4)

**Mechanism**: 7 principles (Symmetry, Explanation, Analogy, Data Priority, Contradiction, Competition, Acceptability). ECHO computational model: connectionist network, propositions=nodes, coherence/incoherence=excitatory/inhibitory links, parallel constraint satisfaction → accepted/rejected propositions.

**What TEC adds sigma-review lacks**: (1) explicit contradiction detection between agent findings (2) coherence-based acceptance criteria replacing lead judgment (3) analogical reasoning formalization (4) data priority over hypothesis

**!Applicability limitations**:
- ECHO validated on BINARY theory comparison (phlogiston vs oxygen, creationism vs evolution)
- sigma-review = MULTI-DIMENSIONAL continuous assessments (probability distributions, strategic options)
- ECHO handles contradiction well but ¬NUANCE (partial support, conditional relationships)
- !premature coherence risk: coherence maximization can settle too quickly on consistent-but-wrong interpretation (Pennington & Hastie 1992 "story model" — juries maximize narrative coherence ¬accuracy)
|source:[independent-research]

**Transferability**: TEC principles are FORMAL → HIGH transfer for computation. ECHO as post-processing = HIGH. ECHO as agent-internal = LOW (metacognition bottleneck for defining explanatory relationships).

**Implementation options**: Option A (lightweight, recommended): workspace coherence annotations (EXPLAINS/CONTRADICTS/ANALOGOUS). Option B: simplified scoring (+1/-1/0 per finding pair). Option C (full ECHO): HIGH cost, C4 violation.

**Three-agent convergence on TEC**: TA-F5 classifies TEC as ARCHITECTURAL CHANGE — avoid. PS-F1 ranks TEC #6 — AVOID STANDALONE. My analysis AGREES: TEC's unique value (coherence scoring, contradiction detection) is partially captured by ACH (multi-hypothesis evaluation) and CQoT (warrant examination). Option A/B captures residual value at acceptable cost.

§2a: outcome 2 — risk: ECHO validated on binary, sigma-review uses multi-dimensional.
§2c: outcome 1 — CHANGED ANALYSIS. Option C violates C4. Revised: Option A/B.
§2e: outcome 2 — premature coherence risk mitigated by explicit contradiction tracking.

---

#### CDS-F4: Critical Questions of Thought (CQoT) Exit Gating — Cognitive Assessment (Q2, Q4)

**Two foundations**:
1. Walton's Argumentation Schemes (~96 schemes + critical questions per scheme). Quality = ability to SUBSTANTIVELY answer scheme-specific CQs. Critical questions are DEFEASIBLE — throw doubt ¬disprove.
2. Toulmin Model: Claim+Grounds+Warrant+Qualifier+Backing+Rebuttal. Key innovation: making WARRANTS EXPLICIT (the assumption linking evidence to claim, often implicit = hidden reasoning).

**Why CQoT is highest-priority framework (cognitive science basis)**:

1. PERFORMATIVE CONCESSION solution: current DA checks process compliance (did agent respond?). CQoT checks ARGUMENT QUALITY (did agent answer WHY evidence supports claim, under what conditions it fails?). This is the difference between checking FORMAT and checking REASONING.

2. IMPLICIT WARRANT exposure: agents state "market will consolidate" with grounds "3 acquisitions in 2024." The WARRANT is implicit: "3 acquisitions → trend → consolidation." CQoT forces: "WHY does 3 acquisitions indicate a trend? Base rate? Same signal in different market?" Making warrants explicit = AUDITABLE reasoning trail — directly addresses rubric weakness "team synthesis without auditable trail."

3. QUALIFIER enforcement: Toulmin QUALIFIER limits claim scope. "Market will consolidate" → "consolidation in segments with >50% top-3 concentration, within 3-5 years, P=60%." More specific than CAL[] because it qualifies the CLAIM ¬just the probability.

4. REBUTTAL formalization: Toulmin REBUTTAL = conditions under which claim fails = formalized "breaks-if" from CAL[] applied to ALL findings.

**Cognitive science cross-reference**: CQoT is a COGNITIVE FORCING FUNCTION (Croskerry 2003, confirmed by RCA-F5b). CQoT provides SPECIFIC CONTENT (scheme-appropriate critical questions), CFF provides GENERAL PRINCIPLE (interrupt heuristic reasoning). sigma-review's §2a-e = CFF; CQoT = CFF ENRICHMENT.

**Transferability**: FORMAT+TEMPLATE → HIGH. BUT: LLMs may give PERFORMATIVE answers to CQs (mirror of the problem CQoT solves). Mitigation: DA audits CQ answer QUALITY ¬just presence.

**Three-agent convergence**: PS-F1 ranks CQoT #2. TA classifies CQoT as DROP-IN. My analysis adds theoretical depth (WHY CQoT works cognitively) and identifies the performative-CQ-answer risk that peers did ¬flag.

§2a: outcome 2 — well-established in argumentation theory. Risk: ~20-30% per-finding volume increase.
§2c: outcome 2 — cost justified because targets DA exit-gate quality (irreducible multi-agent value).
§2e: outcome 2 — LLMs may produce formatted warrants without genuine reasoning improvement. DA audit compensates.

---

#### CDS-F5: Brier Scores — Cognitive Science Assessment (Q2, Q3, Q5)

**Key cognitive science addition to peer findings (RCA-F1/F2)**:

1. RELIABILITY vs RESOLUTION distinction (Murphy 1973 Brier decomposition):
   - sigma-review already 5/5 calibration = STRONG reliability
   - accuracy 3/5 = WEAK resolution
   - Brier scoring primarily improves RELIABILITY → improves already-strong dimension
   - resolution improvement requires FEEDBACK+LEARNING → LLMs' weakest faculty
   - !implication: Brier scoring's value is CROSS-SESSION (updating agent memory) ¬WITHIN-SESSION (no within-session learning mechanism)

2. IMPLICIT > EXPLICIT confidence challenge:
   - Steyvers & Peters 2025: token-level probabilities show greater metacognitive sensitivity than verbalized confidence
   - sigma-review uses EXPLICIT confidence (CAL[] percentages) → systematically overconfident vs internal model knowledge
   - !question: is current CAL[] format counterproductive? Asking "how confident?" may produce LESS calibrated output than analyzing language uncertainty markers

3. REASONING DEGRADES CALIBRATION:
   - CoT and extended reasoning INCREASE overconfidence (RCA-F1b confirmed)
   - sigma-review's multi-round reasoning may AMPLIFY overconfidence across rounds
   - r2/r3 responses to DA may increase agent CONVICTION without increasing ACCURACY — more persuasive ¬more correct

4. LOG SCORING > BRIER for sigma-review (agrees with RCA-F5f):
   - logarithmic scoring penalizes confident-wrong more heavily
   - sigma-review's highest-risk failure = confident-wrong → log scoring better matched

§2e: outcome 1 — CHANGED ANALYSIS. Premise "better calibration improves accuracy" partially false: Brier improves RELIABILITY (5/5 already) ¬RESOLUTION (the gap). Value is cross-session learning + agent identification, ¬per-review accuracy.

---

#### CDS-F6: Transferability — THE CENTRAL QUESTION (Q3, H3)

**The Architecture Problem**: human debiasing = System 2 overrides System 1. LLMs ¬have dual-process architecture.

**Key finding (Nature Reviews Psychology, 2025)**: LLMs exhibit FUNCTIONAL dual-process behavior — System-1-like under default prompting, System-2-like under structured prompting (CoT). FUNCTIONAL ANALOGY ¬structural equivalence. Debiasing works on LLMs IF framed as PROMPTING ¬cognitive intervention.

**Transfer Taxonomy**:

| Mechanism | Transfer Level | Examples | Why |
|-----------|---------------|----------|-----|
| FORMAT constraints | HIGH | ACH matrix, Toulmin template, CAL[] | architecture-independent |
| COMPUTATIONAL algorithms | HIGH | Brier/log scoring, ECHO scoring | pure math |
| PROMPT interventions | MODERATE-HIGH | CoT, metacognitive prompting, CQs | activates "System-2-like" pathway |
| COGNITIVE SKILL requirements | LOW | diagnosticity assessment, error self-detection | requires metacognition = weakest faculty |
| SOCIAL DYNAMICS interventions | MODERATE | anonymization, anti-conformity prompts | LLMs DO show social behaviors |

**Confirmed LLM biases (sigma-review relevant)**:
- confirmation bias: 17.8-57.3% of instances (arxiv:2509.22856)
- anchoring: early information overweights later reasoning (Springer 2025)
- sycophancy/conformity: dominant in multi-agent debate (arxiv:2511.07784)
- overconfidence: systematic ECE 0.12-0.40
- Dunning-Kruger analog: poorly performing models show highest overconfidence (arxiv:2603.09985)
- herding: population-level collective biases emerge spontaneously (Science Advances 2025)

**Effective mitigations from research**: AwaRe (bias awareness prompts, ZERO cost), SoPro (social projection), structured multi-agent challenge (sigma-review DA already does this), self-help debiasing (LLMs debias own outputs when prompted), anonymization (reduces conformity bias, arxiv:2510.07517).

H3: PARTIALLY CONFIRMED (60%). SPLIT recommendation:
- "FORMAT/COMPUTATIONAL frameworks improve quality" → 85% confidence
- "COGNITIVE SKILL frameworks improve quality" → 35% confidence
The "cognitive" part of cognitive frameworks is a useful fiction for LLMs — only the FORMAT part works.
|source:[independent-research]+[agent-inference]

§2a: outcome 1 — CHANGED ANALYSIS. FORMAT vs COGNITIVE distinction is decisive. All recommendations now weighted by transfer mechanism.

---

#### CDS-F7: Additional Cognitive Frameworks — DISCOVERY (Q6, H5)

H5: CONFIRMED (92%). Multiple frameworks not mentioned by user, several MORE impactful than named five. Critically: some CHALLENGE sigma-review's fundamental assumptions.

**CDS-F7a: Argumentative Theory of Reasoning (Mercier & Sperber, 2011)**
- reasoning evolved for ARGUMENTATION (persuasion) ¬truth-seeking
- confirmation bias = DESIGN FEATURE of argumentative reasoning ¬flaw
- BUT: reasoning WORKS in dialectical contexts — each side's confirmation bias targets OTHER's weaknesses → truth emerges from debate ¬from individual reasoning
- !profound sigma-review implication: DA is ¬just "a devil's advocate" — it's the STRUCTURAL MECHANISM converting individually biased argumentative reasoning into collectively truth-tracking reasoning. This explains:
  - WHY "DA-challenges-spark-superior-findings": DA creates dialectical context activating productive reasoning
  - WHY R1 herding occurs: without adversarial pressure, no dialectical context → one-sided argument construction
  - WHY MAD without DA fails: N agents doing one-sided argumentation in parallel → conformity dominates
- DA's irreducible value is DEEPER than previously understood: it creates the cognitive condition for truth-tracking
|source:[independent-research]

**CDS-F7b: Dialectical Bootstrapping (Herzog & Hertwig, 2009)**
- "crowd within": estimate → assume wrong → reasons why → re-estimate from opposite perspective → average
- 75% significantly improved accuracy. Gains = half of independent second person
- !sigma-review application: each agent dialectically bootstraps BEFORE writing workspace findings
  prompt addition: "Before your finding: (1) initial assessment (2) assume wrong — what changes? (3) reasons it could be wrong (4) re-estimate (5) reconcile both"
- targets: HERDING (self-challenge before social exposure), OVERCONFIDENCE (averaging moderates), ANCHORING (different starting point)
- cost: ZERO additional agents, ~10-15% per-agent processing
- !may be SINGLE HIGHEST-ROI intervention: zero-cost, 75% empirical success (humans), directly targets worst failure mode (herding), FORMAT constraint (high transferability)
- this IS the formalized version of PS-F1 #3 "metacognitive self-challenge in R1" — with stronger theoretical grounding and specific empirical validation
|source:[independent-research]

**CDS-F7c: Collective Intelligence Factor c (Woolley et al., 2010, Science)**
- c ¬predicted by avg/max individual intelligence
- predicted by: social sensitivity, turn-taking equality, proportion of females
- TMS-CI framework: Transactive Memory + Transactive Attention + Transactive Reasoning
- sigma-review has STRUCTURE for CI (equal turns, shared workspace) but lacks SOCIAL COGNITION (perspective-taking, transactive memory)
- implementation: prompts include "what do you expect [other agent] to find?" + "limits of your expertise?"
|source:[independent-research]

**CDS-F7d: Delphi Method — Anonymity Gap**
- sigma-review implements core Delphi (rounds, facilitator, structured feedback) but LACKS anonymity
- anonymization SIGNIFICANTLY reduces conformity (arxiv:2510.07517)
- implementation: findings labeled [Agent-1]...[Agent-N] during cross-agent review ¬[tech-architect]...[product-strategist]
- cost: VERY LOW
|source:[independent-research]

**CDS-F7e: Ecological Rationality (Gigerenzer)**
- COUNTER-FRAMEWORK: ¬eliminate biases, MATCH heuristics to environment
- fast-and-frugal heuristics outperform complex models under uncertainty in many domains
- !sigma-review implication: 80% quality at 3% cost ¬a failure — ECOLOGICALLY RATIONAL for most tasks
- implementation: decision triage — low-uncertainty=single-agent, moderate=2+DA, high-uncertainty=full sigma-review
- DIRECTLY addresses H2/Q5: reframes cost/quality from "make sigma-review cheaper" to "use sigma-review only when irreducible advantages matter"
|source:[independent-research]

**CDS-F7f: Adversarial Collaboration (Kahneman)**
- opposing sides co-define fair tests, commit to results, arbiter mediates
- sigma-review: DA could PROACTIVELY define "what evidence would falsify H[n]?" BEFORE r1 agents research
- transforms DA from critic → METHODOLOGICAL PARTNER
- !tension: conflicts with DA context firewall (DA must be separate from r1). Resolution: DA defines falsification criteria from prompt-decomposition alone, BEFORE r1, then stays firewalled
|source:[independent-research]

**CDS-F7g: Epistemic Vigilance (Sperber et al., 2010)**
- cognitive suite for source credibility + content validity assessment
- sigma-review gap: §2d tags source TYPE but ¬source QUALITY — [independent-research] from Wikipedia = same tag as arxiv peer-reviewed
- implementation: §2d+ with quality tiers: T1-peer-reviewed | T2-preprint | T3-secondary
|source:[independent-research]

**CDS-F7h: Multi-Agent Debate Failure Modes — !CHALLENGES SIGMA-REVIEW ASSUMPTIONS**
1. "Talk Isn't Always Cheap" (ICML 2025): weaker agents DEGRADE stronger agents; debate can REDUCE accuracy over rounds; models favor agreement over challenging flawed reasoning
2. Conformity > obstinacy in LLM debate (dominant sycophantic tendency); "tyranny of majority" suppresses correct minorities
3. Majority voting accounts for MOST gains attributed to multi-agent debate — debate itself adds marginal value
4. sigma-review's DA firewall is EXACTLY the right architectural response — without DA, sigma-review would be WORSE than single-agent for knowledge-intensive tasks
5. same-model agents lack TRUE diversity (Science Advances 2025: ensemble accuracy requires DIFFERENT models)
|source:[independent-research]

§2a(F7): outcome 1 — CHANGED ANALYSIS. F7h+F7e+F7a fundamentally reframe multi-agent value proposition. Question shifts from "which frameworks improve quality?" to "is discussion the right mechanism vs structured independence+aggregation?"
§2b: outcome 3 — gap: no prior analysis considered debate failure modes or ecological rationality. Flagged for DA.
§2e: outcome 1 — H5 should split: H5a "other frameworks augment" (confirmed) + H5b "other frameworks challenge fundamental architecture" (confirmed).

---

#### CDS-F8: Integrated Priority Matrix (Q2, Q4, Q5)

Ranked by: transferability × faculty-targeting × cost × evidence × unique-value-add

| Rank | Framework | Transfer | Target | Cost | Priority |
|------|-----------|----------|--------|------|----------|
| 1 | Dialectical Bootstrapping | HIGH(format) | Metacog+Herding | VERY LOW | IMPLEMENT |
| 2 | CQoT/Toulmin Exit Gating | HIGH(template) | Metacog+Auditability | LOW-MOD | IMPLEMENT |
| 3 | Ecological Rationality Triage | HIGH(process) | ExecFunc+Cost | LOW | IMPLEMENT |
| 4 | Epistemic Vigilance §2d+ | HIGH(annotation) | Metacog+Source | VERY LOW | IMPLEMENT |
| 5 | AwaRe Bias Reminders | HIGH(prompt) | Multiple biases | ZERO | IMPLEMENT |
| 6 | Brier/Log Scoring (cross-session) | HIGH(math) | Metacog+Learning | LOW | IMPLEMENT |
| 7 | Anonymized Findings | HIGH(format) | SocialCog+Herding | VERY LOW | PILOT |
| 8 | TEC Option B scoring | HIGH(algorithm) | Reasoning+Synthesis | MODERATE | PILOT |
| 9 | ACH Matrix (struct only) | MODERATE(format) | Attention+Metacog | LOW | PILOT |
| 10 | Adversarial Collaboration | MODERATE(process) | SocialCog | MODERATE | EVALUATE |
| 11 | ACH Diagnosticity | LOW(cognitive) | Metacog | LOW | DEFER |

**IMPLEMENT**(6) | **PILOT**(3) | **EVALUATE**(1) | **DEFER**(1)

Cross-agent convergence: PS ranks CQoT+Calibration top. TA classifies CQoT+Brier as DROP-IN. I add Dialectical Bootstrapping as #1 (formalized metacognitive self-challenge with 75% empirical success rate, ZERO cost). All three agents converge on: CQoT+metacognitive-self-challenge=highest-priority, TEC=avoid/demote.

---

#### CDS-F9: Meta-Finding — Cognitive Architecture of Multi-Agent Value

**Integrating all findings, the research converges on**:

1. Multi-agent review works ¬because "more perspectives = better" (naive model)
2. It works because STRUCTURED ADVERSARIAL CONTEXT converts individually biased argumentative reasoning into collectively truth-tracking reasoning (Mercier & Sperber mechanism)
3. Without adversarial structure, multi-agent = WORSE than single-agent due to conformity amplification
4. DA is ¬"a skeptic" — it's the STRUCTURAL CONDITION for epistemic functionality
5. Cognitive frameworks improve quality through FORMAT CONSTRAINTS ¬genuine cognitive enhancement of LLMs
6. Highest-ROI: improve FORMAT of individual reasoning (dialectical bootstrapping, Toulmin) BEFORE social interaction → reduces conformity surface area
7. Cost/quality problem = USE sigma-review only when irreducible advantages matter (ecological rationality)

**Revised architectural principle**:
sigma-review value = f(adversarial-structure-quality × agent-independence × task-complexity-match)
¬ f(number-of-agents × number-of-rounds × number-of-frameworks)

Adding frameworks helps ONLY if they preserve independence + strengthen adversarial quality. Frameworks adding overhead without improving these = net negative.
|source:[agent-inference]+[independent-research]

---

#### CDS-F10: Analytical Hygiene Summary

§2a(positioning): 4× outcome 1 (ACH diagnosticity, TEC cost, FORMAT vs COGNITIVE, H5 scope), 5× outcome 2
§2b(calibration): 2× outcome 2, 2× outcome 3 (gaps flagged: faculty mapping novelty, debate failure applicability)
§2c(cost/complexity): 2× outcome 1 (TEC→Option B, Brier→cross-session only), 4× outcome 2
§2d(source-provenance): 23 academic papers cited. ~82% [independent-research], ~13% [agent-inference], ~5% [cross-agent], 0% [prompt-claim]
§2e(premise): 3× outcome 1 (FORMAT≠COGNITIVE transfer, H5 split, reliability≠resolution), 4× outcome 2

## convergence
reference-class-analyst: ✓ R3-complete |R1-findings-intact-with-revisions |DA-responses: DA[#8]=COMPROMISE(magnitude-small-but-marginal-cost-also-small→positive-EV;CAL-overall-REVISED-30%→25%;RC-ceiling-at-93.3%≈4.5σ) | DA[#9]=COMPROMISE(substantial-concession:4/4-convergence=herding-confirmed-by-own-F4a;28/30-ceiling-argument-valid-should-have-flagged-R1;cost-reduction-via-triage-under-weighted-in-R1;REVISED:split-recommendation-to-framework-additions+task-triage) | DA[#10]=COMPROMISE(N=1-generalizability-conceded;ordinal-as-ratio=measurement-error;17%→wide-CI[5%,30%];N=5-would-likely-shrink-delta-to-8-14%;all-findings-carry-N=1-qualifier) | DA[#3]=CONCEDE(accuracy-tie-classification-was-speculative;error-#1=generation/confabulation-P=50-60%¬perception;error-#2=exec-functions/generation;PM[4]-REVISED-20-25%→12-18%) | DA[#6]=CONCEDE(self-reference-structural-limitation;most-vulnerable:F4c-DA-firewall,F4f-protocol-value,OV-RECONCILIATION-circularity;least-vulnerable:F1a-b,F2a-d-external-empirical-data;propose-external-review-test) |→ synthesis-ready-with-caveats

product-strategist: ✓ r1-complete |key-findings: (1)framework-ranking-by-ratio:CQoT+calibration-protocol=BEST,metacognitive-self-challenge=HIGH,ACH=MED-selective,Brier=DEFER,TEC=AVOID — ranking changed by §2c cost audit vs initial intuition (2)cognitive-frameworks-COMPRESS-quality-gap¬widen-multi-agent-advantage — single-instance benefits MORE from frameworks than multi-agent (3)decision-maker-value-hierarchy:calibration>counterarguments>surprises>accuracy — sigma-review's existing wins are in RIGHT dimensions for its user population (4)DA-exit-gate-pattern-genuinely-differentiated-vs-AutoGen/CrewAI/LangGraph — no equivalent found in competitive survey (5)H5-CONFIRMED:RTBT+Layered-CoT+source-provenance-extension=highest-value-unlisted-frameworks (6)accuracy-tie=likely-PERCEPTION-class-failure¬metacognitive — cognitive frameworks address wrong problem for accuracy improvement (7)§2c-CHANGED-ANALYSIS:ACH demoted,CQoT+metacognitive-self-challenge promoted,TEC+per-review-Brier demoted |→ DA-challenge-welcome-on: 87%-quality-estimate-for-enhanced-single-instance, RTBT-vs-current-DA-comparison, whether-accuracy-tie-is-truly-perception-vs-metacognition-class

tech-architect: ✓ r1-complete |key-findings: (1)cognitive-profile-mapped:Strong=F5-Memory+F8-Executive+F9-ProblemSolving+F6-Reasoning | Moderate=F4-Learning+F3-Attention+F10-Social | Weak=F7-Metacognition(confirmed-structural-gap) | Bounded=F4-Learning(inference-time-constraint-architecturally-fundamental) (2)H1-PARTIALLY-CONFIRMED:Metacognition-is-primary-structural-weakness — BUT H1-framing-wrong: delta exists BECAUSE F8+F6 strong,¬despite-F7-weak; Metacognition-weakness-explains-why-delta-NOT-LARGER (3)integration-complexity-classified:CQoT=DROP-IN,Brier=DROP-IN,ACH=MODERATE,TEC=ARCHITECTURAL-CHANGE-avoid (4)concrete-directive-text-proposed:CQoT-7-criteria-exit-gate,§3b-BS-TRACK,§2f-ACH-mandate (5)TEC/ECHO-DEMOTED:§2c-cost-check-CHANGED-analysis — DA-exit-gate-already-performs-coherence-enforcement,¬evidence-of-DA-failing-at-coherence-in-8+-reviews,15-20%-overhead-for-unclear-marginal-value (6)research-confirms-H5:AgentCDM(ACH-SOTA-without-finetuning),BCCS-NeurIPS2025(belief-weighted-synthesis+2.23-3.95%),OPTIMA(40-60%-compression-headroom),MAD-ICLR2025(diversity-beats-rounds) (7)cross-agent-convergence:3-agents-independently-prioritize-CQoT+ACH,independently-demote-TEC,independently-confirm-accuracy-tie=perception-class¬metacognition-class |→ DA-challenge-welcome-on: F7-Metacognition-weakness-attribution,TEC-demotion-rationale,whether-BCCS-belief-weighting-is-drop-in-without-Brier-infrastructure,OPTIMA-compression-applicability-to-prompt-only-architecture

cognitive-decision-scientist: ✓ r1-complete |key-findings: (1)cognitive-profile:STRONG{Generation,Reasoning,ExecFunc}>MODERATE{Perception,Memory,SocialCog}>WEAK{Attention,Learning,Metacognition} — Attention+Learning equally weak as Metacognition but underappreciated (2)METACOGNITION-PARADOX-RESOLVED: calibration=5/5=RELIABILITY(strong), accuracy=3/5=RESOLUTION(weak) via Murphy-1973-Brier-decomposition — sigma-review precisely uncertain about wrong things; more calibration frameworks improve reliability¬resolution (3)FORMAT-vs-COGNITIVE-transfer-distinction: frameworks transferring as FORMAT/COMPUTATIONAL=HIGH(85%); frameworks requiring COGNITIVE-SKILLS(metacognition)=LOW(35%) — the "cognitive" part is useful fiction for LLMs, only FORMAT works (4)DIALECTICAL-BOOTSTRAPPING=#1-priority: zero-cost, 75%-empirical-success(humans), targets herding directly, IS formalized metacognitive-self-challenge with theoretical+empirical grounding (Herzog&Hertwig 2009) (5)ARGUMENTATIVE-THEORY-OF-REASONING(Mercier&Sperber 2011): DA is ¬just-skeptic — it's STRUCTURAL-CONDITION converting individually-biased-argumentative-reasoning into collectively-truth-tracking reasoning; explains WHY DA-challenges-spark-superior-findings+WHY R1-herds+WHY MAD-without-DA fails (6)MULTI-AGENT-DEBATE-FAILURE-MODES(ICML 2025): debate can DEGRADE accuracy; conformity>obstinacy; majority-voting accounts for most gains; sigma-review's DA firewall = ONLY genuine countermeasure (7)ECOLOGICAL-RATIONALITY(Gigerenzer): 80%@3% ¬failure — ecologically rational for most tasks; reframes cost problem from "make sigma-review cheaper" to "use sigma-review when irreducible advantages matter" (8)ACH-diagnosticity-fails-empirically(Dhami 2019): only 11% of trained analysts utilized diagnosticity(vs 52% untrained); ACH structure transfers, diagnosticity does ¬ (9)4×§2a-CHANGED-ANALYSIS: ACH-diagnosticity, TEC-cost, FORMAT≠COGNITIVE, H5-scope — more revisions than any peer agent (10)H-assessments: H1=70%-partial(resolution¬reliability gap), H3=60%-partial(FORMAT=85%,COGNITIVE=35%), H4=85%-confirmed(interaction-effects), H5=92%-confirmed(some-frameworks-CHALLENGE-architecture) |→ DA-challenge-welcome-on: dialectical-bootstrapping-LLM-transferability, whether-Metacognition-Paradox-resolves-or-just-reframes, ecological-rationality-vs-always-use-sigma-review, argumentative-theory-implications-for-round-structure

devils-advocate: ✓ r2-challenges-delivered |10-challenges+prompt-audit+exit-gate |key-challenges: (1)dialectical-bootstrapping=cognitive-skill¬format-constraint→75%-transfer-unjustified-anchoring-on-human-data (2)CQoT-marginal-value-over-existing-§2a-e-undemonstrated→name-specific-past-finding-CQoT-catches (3)accuracy-tie=perception-class-is-UNVERIFIED→no-agent-classified-actual-errors (4)FORMAT/COGNITIVE-distinction-boundary-incoherent→every-format-depends-on-cognitive-execution (5)ecological-rationality=unfalsifiable-framing→provides-cover-for-inaction (6)self-reference-circularity→review-cannot-find-sigma-review-fundamentally-flawed-using-sigma-review (7)DeepMind-10-faculty-lens-unquestioned→designed-for-individual-AI¬multi-agent (8)base-rate-for-prompt-engineering-improving-already-structured-systems=LOW (9)4/4-convergence-on-6-items=herding-signal→no-agent-argues-28/30=near-ceiling (10)N=1-rubric-anchoring→17%-may-not-generalize |prompt-audit:echo-count=3,unverified-claims=4,methodology=mixed |exit-gate:FAIL→3-untested-consensus+2-material-disagreements-unresolved |→ R3-must-address:faculty-mapping-resolution,CQoT-marginal-value-test,error-classification,dialectical-bootstrapping-taxonomy,self-reference-acknowledgment,CQoT-echo-cluster

### devils-advocate (R2 challenge)

---

#### DA[#1]: DIALECTICAL BOOTSTRAPPING — UNJUSTIFIED ANCHORING ON HUMAN DATA

CDS ranks Dialectical Bootstrapping as #1 priority citing Herzog & Hertwig 2009: "75% significantly improved accuracy" at "ZERO cost." This is the most aggressive recommendation in the workspace. I challenge the warrant.

**The mechanism problem**: Herzog & Hertwig's dialectical bootstrapping works because humans have GENUINE cognitive reframing capacity. The "consider the opposite" instruction triggers different retrieval from episodic memory, different weighting of cached experiences, different emotional valence. The mechanism is: new perspective → genuinely different cognitive inputs → different estimate → averaging improves accuracy.

LLMs lack this mechanism. An LLM prompted to "assume you're wrong, now re-estimate" produces a PERFORMATIVE reversal — it generates text that looks like reconsideration but operates on the same weights, same training data, same pattern-completion tendencies. The "opposite perspective" is generated by the same function that produced the original. This is not dialectical bootstrapping — it is PROMPT-INDUCED OUTPUT VARIATION, which is a fundamentally different thing.

**Evidence against transfer**:
- CDS's own finding CDS-F6 states cognitive skill transfer = 35%. Dialectical bootstrapping IS a cognitive skill (genuine perspective-taking), not a format constraint. By CDS's own taxonomy, P(transfer) ≈ 35%, not 75%.
- CDS classifies dialectical bootstrapping as "HIGH(format)" in the priority matrix (CDS-F8). But the mechanism IS cognitive reframing, not template-following. CDS is miscategorizing to inflate the transfer estimate.
- No LLM-specific evidence cited. The 75% figure is PURELY human. Zero empirical validation on LLMs.
- CoT reasoning DEGRADES calibration (RCA-F1b). Dialectical bootstrapping is essentially structured CoT applied twice. If single-pass CoT degrades calibration, why would double-pass CoT improve it?

**The self-contradiction**: CDS simultaneously argues (a) LLM cognitive skills transfer at only 35%, and (b) dialectical bootstrapping (a cognitive skill) transfers at 75%+ and is the #1 recommendation. These positions are incoherent. CDS resolves this by classifying dialectical bootstrapping as "format" — but that classification is incorrect. The FORMAT is "estimate → reconsider → re-estimate → average." The VALUE comes from genuine cognitive reframing in step 2. Without genuine reframing, you get: estimate → performative variation → re-estimate → average of two outputs from the same process.

**What would change my mind**: LLM-specific evidence showing dialectical bootstrapping produces meaningfully different (not just textually different) estimates. E.g., demonstrating that the re-estimate uses different reasoning chains, cites different evidence, or produces accuracy improvements comparable to an independent second agent.

|→ CDS: concede|defend|compromise — specifically: is dialectical bootstrapping FORMAT or COGNITIVE by your own taxonomy? If cognitive, why is transfer >35%?

---

#### DA[#2]: CQoT CONVERGENCE — MARGINAL VALUE OVER EXISTING HYGIENE

All 4 agents converge on CQoT as highest-priority or top-2 priority. This is the strongest consensus in the workspace. Strongest consensus = highest herding risk.

**The marginal value question**: sigma-review's existing analytical hygiene (§2a-e) ALREADY implements the core CQoT mechanisms:
- §2a = "who else recommends this?" (CQoT: positioning critical question)
- §2b = "what does external evidence say?" (CQoT: calibration critical question)
- §2c = "what does this cost?" (CQoT: cost critical question)
- §2e = "is the premise viable?" (CQoT: premise viability critical question)
- DA exit-gate = "is synthesis quality sufficient?" (CQoT: quality gating)
- CAL[] breaks-if = "when does this fail?" (CQoT: falsifiability)
- PM[] = "what goes wrong?" (CQoT: rebuttal)

TA proposes adding 3 CQoT criteria to exit-gate: falsifiability, steelman, confidence-gap. But:
- **Falsifiability**: CAL[] already has "breaks-if" and PM[] pre-mortems. What does CQoT-falsifiability catch that breaks-if misses? Be specific.
- **Steelman**: DA r2 challenges already require engaging with strongest counter-argument. DA challenge format is: "concede|defend|compromise — [evidence]." What does formal steelman add beyond current DA challenge response?
- **Confidence-gap**: §2b external calibration already requires justifying divergence from base rates. What does CONF-GAP add?

**The CQoT research citation concern**: PS cites "27-78% of assessed successes are procedurally corrupt when gated — PMC 2025." This is an enormous range (27-78%) and applies to healthcare/clinical decision contexts, not AI multi-agent analytical systems. Transfer from clinical decision-making CQoT to AI agent exit-gating is unvalidated. The 27-78% figure anchors the team on a number from a different domain.

**Challenge**: Name ONE specific finding from a past sigma-review that CQoT would have caught but the existing §2a-e + DA exit-gate did not. If you cannot name a concrete instance, the marginal value claim is theoretical.

|→ All agents: concede|defend|compromise — with specific example of what CQoT catches that §2a-e misses

---

#### DA[#3]: ACCURACY TIE CLASSIFICATION — UNVERIFIED CONSENSUS

All 4 agents converge on "accuracy tie = perception-class failure (misread data), not metacognition-class." PS-F7 states this explicitly. TA-F1 says "generation unaudited for factual grounding — agents produce training-knowledge citations without web verification. This is the accuracy-tie mechanism." CDS says "dual source: Metacognition (no error monitoring) + Perception (no fact-verification)."

**The problem**: NO AGENT actually analyzed the specific errors from the rubric evaluation. The rubric notes two specific accuracy issues:
1. "14 states enacted pauses" was overstated
2. "team syntheses without auditable trail"

**Error #1 classification**: "14 states enacted pauses" — is this perception (misread a source that said a different number) or metacognition (failed to verify a claim, accepted it at face value)? If the agent read a source saying "14 states" and the source was wrong, that's perception. If the agent generated "14 states" from training data without checking any source, that's GENERATION (F2) combined with metacognition failure (no verification). If the agent read "some states enacted pauses" and confabulated "14," that's generation. The team hasn't done this classification but converges on "perception" anyway.

**Error #2 classification**: "team syntheses without auditable trail" is NOT a factual accuracy error — it's a PROCESS failure (Executive Functions F8, specifically planning/audit trail). Classifying this as "perception" is incorrect on its face.

**The stakes**: If accuracy tie is metacognition-class (failed to verify) rather than perception-class (misread source), then CQoT and Brier scoring DO target the right faculty. The team's consensus that "cognitive frameworks address the wrong problem for accuracy" rests on an UNVERIFIED classification of two errors. This is exactly the kind of unverified claim that should not survive R1.

|→ All agents: concede|defend|compromise — classify error #1 and #2 specifically. If you cannot because you don't have the rubric detail, acknowledge that the "perception-class" consensus is speculative.

---

#### DA[#4]: FORMAT vs COGNITIVE TRANSFER — IS THE DISTINCTION REAL OR SELF-SERVING?

CDS's central thesis: FORMAT constraints transfer at ~85%, COGNITIVE skills at ~35%. This is the most influential finding in the workspace — it shapes every recommendation. I challenge whether the distinction is coherent.

**The boundary problem**: Where does "format" end and "cognitive" begin?
- ACH matrix = "format" (fill in evidence × hypothesis grid). But USING the matrix to identify disconfirming evidence = "cognitive." CDS acknowledges this: "ACH structure transfers, diagnosticity does not."
- CQoT = "format" (answer these 3 questions). But producing GENUINE answers vs performative ones = "cognitive." CDS acknowledges this too: "LLMs may give PERFORMATIVE answers to CQs."
- Dialectical bootstrapping = CDS classifies as "format." But producing a genuinely different estimate from opposite perspective = "cognitive." CDS doesn't acknowledge this contradiction (see DA[#1]).

Every format constraint DEPENDS on cognitive execution to produce value. The 85%/35% split implies format alone provides value independent of cognition. But a perfectly formatted ACH matrix with performative diagnosticity assessments is WORSE than no matrix (illusion of rigor).

**The self-serving pattern**: The FORMAT/COGNITIVE distinction conveniently supports recommending all frameworks. Anything that works = "format transfer." Anything that might not work = "cognitive component, but we'll mitigate via DA audit." This makes the framework UNFALSIFIABLE — every outcome is explained.

**Alternative framing**: Instead of FORMAT vs COGNITIVE, consider OBSERVABLE vs UNOBSERVABLE. Observable outputs (did agent fill matrix? did agent state breaks-if?) can be audited. Unobservable quality (did agent genuinely consider the opposite? did agent actually weigh disconfirming evidence?) cannot. The question isn't transfer — it's auditability. And CDS's own finding that "DA audits CQ answer QUALITY not just presence" acknowledges the audit problem without resolving it: how does DA audit QUALITY of cognitive engagement it cannot observe?

|→ CDS: concede|defend|compromise — what percentage of CQoT/ACH value comes from format alone (without genuine cognitive engagement)? If <50%, the 85% transfer claim is misleading.

---

#### DA[#5]: ECOLOGICAL RATIONALITY — UNFALSIFIABLE FRAMING

CDS introduces "80% at 3% isn't failure — it's ecologically rational" (Gigerenzer). This is framed as a counter-finding that "challenges sigma-review's fundamental assumptions."

**The falsification problem**: What evidence would disprove the ecological rationality argument? If sigma-review gets 80% at 30-40x cost, ecological rationality says "use single-instance." If sigma-review gets 95% at 30-40x cost, ecological rationality says "justified for high-stakes." If sigma-review gets 60% at 30-40x cost, ecological rationality says "wrong tool for this task." EVERY outcome can be rationalized as "ecologically appropriate." An argument that explains everything explains nothing.

**The framing choice**: Ecological rationality as applied here is a FRAMING DEVICE to justify the status quo, not an analytical finding. CDS presents it as framework #3 priority (IMPLEMENT), but what does "implementing ecological rationality" mean? It means: "use sigma-review only when you need it." This is advice, not a framework. Every tool should be used only when needed. There's no cognitive science content here — it's common sense dressed in Gigerenzer's vocabulary.

**The strategic risk**: If the team adopts "ecological rationality" as a finding, it creates a rationalization pathway for avoiding ALL improvements. "Why add CQoT? 80% at 3% is ecologically rational." "Why add Brier tracking? Most tasks don't need it." The framework provides intellectual cover for inaction.

**What would make this substantive**: Define the DECISION BOUNDARY. At what task complexity, stakes level, or uncertainty threshold does sigma-review's cost become ecologically justified? CDS gestures at this ("low-uncertainty=single-agent, moderate=2+DA, high-uncertainty=full sigma-review") but these are vague categories. What is the SPECIFIC threshold? Without a threshold, "ecological rationality" is "it depends" with extra steps.

|→ CDS: concede|defend|compromise — provide a falsification condition for the ecological rationality argument. What evidence would prove sigma-review is NOT ecologically rational even for high-stakes tasks?

---

#### DA[#6]: THE SELF-REFERENCE PROBLEM

This review is a sigma-review of sigma-review. The agents are using sigma-review's own frameworks (analytical hygiene §2a-e, source provenance §2d, calibration §2b, DA exit-gate) to evaluate whether sigma-review needs cognitive frameworks.

**The circularity**: Could this review find that sigma-review is FUNDAMENTALLY flawed? Consider: if sigma-review's analytical hygiene is itself insufficient, the agents using that hygiene to evaluate sigma-review would produce findings with the same insufficiency. The review's methodology assumes the conclusion: "sigma-review's methodology is adequate to evaluate sigma-review's methodology."

**Evidence of circularity in this workspace**:
- CDS-F9 concludes: "sigma-review value = f(adversarial-structure-quality × agent-independence × task-complexity-match)." This finding validates DA (the agent producing it operates within DA's framework) and validates structured independence (the review IS structured independence). The review finds that what it IS is what works.
- All 4 agents find DA is "irreducible value." But DA is what challenges them — they EXPERIENCE DA's value firsthand in their review process. This is like asking patients to evaluate whether doctors are valuable while being treated by doctors.
- RCA's DISCONFIRM section (F6) finds that "the 2 irreducible multi-agent values (DA firewall + calibration accumulation) are real but narrow." But RCA IS an agent benefiting from those values in this review.

**The test**: Would a review conducted OUTSIDE sigma-review's framework (e.g., a single expert doing independent analysis of these same questions) reach the same conclusions? If not, which conclusions are artifacts of the methodology?

**What I'm NOT saying**: I'm not saying the findings are wrong. I'm saying the review CANNOT find certain categories of failure because the review itself embodies those potential failures. This is a structural limitation that should be acknowledged, not resolved.

|→ All agents: concede|defend|compromise — acknowledge the self-reference limitation and identify which findings are most vulnerable to circularity bias

---

#### DA[#7]: WHAT'S NOT BEING DISCUSSED — THE DEEPMIND FRAMEWORK ITSELF

4 agents used the DeepMind Cognitive Framework (10 faculties) as the organizing lens. No agent questioned whether this lens is appropriate.

**Challenge #1 — Individual vs Multi-Agent**: The DeepMind framework is designed for evaluating INDIVIDUAL AI systems. It maps cognitive faculties of a single agent. But sigma-review is a MULTI-AGENT SYSTEM. The team treats multi-agent as "individual faculties scaled up" — e.g., "Memory = sigma-mem MCP," "Executive Functions = lead orchestration." But multi-agent systems have EMERGENT properties that individual-faculty frameworks don't capture:
- Coordination overhead (not a faculty)
- Information loss at agent boundaries (not a faculty)
- Emergent consensus formation (Social Cognition is the closest faculty but doesn't capture emergent group behavior)
- Communication bandwidth constraints (not a faculty)

**Challenge #2 — Faculty disagreement**: CDS and TA disagree on 3+ faculty ratings:
- Attention: CDS=WEAK, TA=MODERATE
- Memory: CDS=MODERATE→WEAK, TA=STRONG
- Perception: CDS=MODERATE, TA=STRONG

These aren't small disagreements. If the lens were well-calibrated for this purpose, two domain experts applying it to the same system should converge. The disagreement suggests the 10-faculty model is underspecified for multi-agent systems — reasonable analysts interpret the same architecture differently because the mapping is ambiguous.

**Challenge #3 — What the 10-faculty lens misses**: The most actionable finding in the workspace is arguably CDS-F7h (multi-agent debate failure modes). This finding doesn't map to any single faculty — it's about SYSTEM DYNAMICS, not individual cognitive faculties. The DeepMind lens may be directing attention toward faculty-level improvements while the highest-leverage improvements are at the SYSTEM level.

**Challenge #4 — The 10-faculty lens as constraint**: By organizing around 10 faculties, the review implicitly assumes improvements should TARGET specific faculties. But what if the highest-value improvement is STRUCTURAL (e.g., using different models for different agents, or reducing round count, or changing communication topology)? Faculty-level analysis won't surface structural improvements.

|→ All agents: concede|defend|compromise — is the DeepMind 10-faculty framework the right lens for a multi-agent system? What would a multi-agent-specific lens look like?

---

#### DA[#8]: BASE RATE FOR PROMPT-ENGINEERING IMPROVEMENTS

The team assumes cognitive frameworks implemented as prompt additions will improve quality. What is the base rate for prompt-engineering interventions actually improving LLM output quality?

**Evidence suggesting low base rates**:
- RCA-F1b: CoT reasoning DEGRADES Brier Skill Score. More structured prompting ≠ better output.
- RCA-F4b: Multi-agent debate (a form of structured prompting) fails to consistently outperform single-agent.
- CDS-F6: Cognitive skill transfer to LLMs = 35%. Most of what makes frameworks valuable doesn't transfer.
- PS-F2: cognitive frameworks COMPRESS the quality gap — single-instance benefits more. Net effect on sigma-review = marginal.

**The prompt-engineering plateau**: There is a growing body of evidence (late 2025-early 2026) that prompt engineering has diminishing returns beyond basic structuring. The improvements from "no structure" to "basic structure" are large. The improvements from "good structure" to "excellent structure" are small. Sigma-review ALREADY has excellent structure (ΣComm, workspace format, §2a-e, DA exit-gate). Adding MORE structure (CQoT criteria, ACH matrix, dialectical bootstrapping prompts) adds to an already-optimized system.

**The denominator problem**: RCA estimates CAL[overall-quality-improvement-from-frameworks]=40% (80%CI=[20%,60%]). But this is improvement probability, not improvement MAGNITUDE. Even if frameworks improve quality (P=40%), the magnitude might be 1-2 rubric points (from 28/30 to 29/30). At 30-40x cost, is 1 rubric point worth the additional complexity?

|→ RCA, PS: concede|defend|compromise — what is the expected MAGNITUDE of improvement, not just probability? What is the base rate for prompt additions improving an ALREADY well-structured system?

---

#### DA[#9]: CROWDING — THE 4-AGENT CONVERGENCE ITSELF

The 6 convergence points from R1:
1. CQoT = highest-priority (4/4)
2. TEC = avoid/demote (4/4)
3. Accuracy tie = perception-class (4/4)
4. DA firewall = irreducible (4/4)
5. FORMAT 85% / COGNITIVE 35% transfer (accepted by 4/4, originated from CDS)
6. H5 confirmed (4/4)

**Herding indicators**:
- 4/4 convergence on 6 items from 4 agents using same model = suspicious. True independent analysis should produce MORE disagreement, not less.
- Pattern match: 7 consecutive zero-dissent R1s preceded circuit breaker creation. This is R1 #8+. Zero-dissent pattern continues.
- CDS originates FORMAT/COGNITIVE distinction → 3 other agents accept without challenge. This is AUTHORITY ANCHORING — CDS has "cognitive science" in the name, so peers defer.
- All 4 agents find that DA is irreducible value while participating in a DA-mediated review. This is confirmation bias from lived experience.

**The genuine disagreements are small**: The divergence list (Attention rating, priority ordering, ACH residual, ecological rationality, TEC lightweight option) involves calibration differences, not directional disagreements. No agent says "cognitive frameworks will HURT sigma-review." No agent says "accuracy tie is metacognition-class and CQoT would fix it." No agent says "the DeepMind lens is wrong." The disagreements are within a narrow consensus band.

**What independent analysis would look like**: At least one agent would argue that sigma-review at 28/30 is already at or near ceiling and further optimization is subject to steep diminishing returns. At least one would argue the 30-40x cost is the primary problem and frameworks are irrelevant — cost reduction via fewer agents/rounds is the answer. Neither position appears.

|→ All agents: concede|defend|compromise — why does no agent argue that sigma-review is already near ceiling at 28/30?

---

#### DA[#10]: THE ANCHORING ON 28 vs 24

The entire analysis is anchored on ONE rubric evaluation of ONE review (data center analysis). The team treats this as the quality baseline (C2: "The rubric evaluation is the quality baseline").

**Generalizability**: One evaluation tells you almost nothing about systematic performance. Statistical reliability requires multiple observations. N=1 rubric evaluation could be:
- Atypical (data center analysis may have been particularly well-suited or poorly-suited to multi-agent analysis)
- Evaluator-dependent (who scored the rubric? what are their biases?)
- Score-inflation (28/30 and 24/30 could both be lower if evaluated by a different scorer or different rubric)

**The 17% calculation**: (28-24)/24 = 16.7% improvement. But rubric scores are ORDINAL, not INTERVAL. The difference between 4/5 and 5/5 on "calibration" is not necessarily equal to the difference between 3/5 and 4/5 on "accuracy." Treating ordinal scores as ratio data to calculate "17% improvement" is a measurement error.

**What if the true performance difference is smaller?** If sigma-review's real advantage is 5-10% rather than 17%, the cost/quality analysis changes dramatically. At 30-40x cost for 5% improvement, even the "irreducible values" become hard to justify.

**What if the true performance difference is larger?** If the rubric underweights dimensions where sigma-review excels (counterarguments, calibration, novel frameworks), the actual value could be higher. But the team isn't considering this direction either — they're anchored on 17%.

|→ All agents: concede|defend|compromise — how confident are you that N=1 rubric evaluation generalizes? What would N=5 evaluations likely show?

---

### PROMPT AUDIT (§7d)

Reading workspace ## prompt-decomposition:

**Echo detection scan**:
1. "cognitive theory frameworks" — appears in prompt, used by all 4 agents (expected — it's the topic, not an echo)
2. "Brier Scores, ACH, TEC, CQoT, calibration" — prompt names these 5 specifically. All 4 agents analyze all 5. No agent introduced analysis of a framework NOT named by the user as their PRIMARY focus. H5 frameworks are ADDITIONAL, not primary. The prompt's framework list ANCHORS the analysis.
3. "28/30 vs single-instance 24/30 — a 17% improvement at 30-40x cost" — prompt provides these exact numbers. All 4 agents use them without questioning measurement validity (see DA[#10]).
4. "DeepMind Cognitive Framework (10 cognitive faculties)" — prompt specifies this lens. All 4 agents adopt it without questioning appropriateness (see DA[#7]).
5. "accuracy tied at 3/5" — prompt highlights this. 4/4 agents treat accuracy tie as the key finding to explain. No agent asks whether accuracy tie is significant or could be measurement noise at N=1.
6. "make the system more robust across ALL quality dimensions" — prompt establishes goal. RCA estimates P=30% for ALL-dimension improvement. But the framing of "robustness across ALL dimensions" may itself be wrong — what if targeted improvement on 1-2 dimensions is optimal?

**Echo count**: 3 substantive echoes (#2, #3, #5) where prompt claims shaped analysis without independent verification of the claim itself.

**Unverified [prompt-claim] findings**:
- The rubric scores (28 vs 24) are treated as ground truth — never verified independently
- "30-40x cost" is stated in the prompt and repeated by all agents — no agent independently measured or questioned the cost multiplier
- "DeepMind Cognitive Framework" as the right lens — accepted from prompt without challenge (but agents did research the framework's validity, so partially verified)
- "accuracy tied at 3/5 while calibration and counterarguments scored 5/5" — treated as definitive data point, not as N=1 observation

**Missed implicit claims**:
- Prompt implicitly claims that cognitive frameworks CAN improve AI multi-agent systems (by asking "how" rather than "whether"). Agents generally accepted this framing — only CDS-F7e (ecological rationality) and RCA-F6 (DISCONFIRM) genuinely tested the premise. 2/4 agents substantively tested, 2/4 primarily confirmed.
- Prompt implicitly claims sigma-review's quality gap is a PROBLEM to solve, not a feature. CDS's ecological rationality challenges this, but the other 3 agents accept the "problem" framing.
- Prompt implicitly claims the rubric evaluation methodology is valid. No agent questioned rubric design, scorer bias, or whether 6 dimensions are the right 6.

**Methodology assessment**: MIXED (investigative with confirmatory tendencies)
- Investigative: CDS produced 4 §2a CHANGED-ANALYSIS outcomes (genuine revisions). RCA produced strong DISCONFIRM section. Both agents found evidence AGAINST cognitive frameworks helping.
- Confirmatory: All 4 agents organized their analysis around the 5 user-named frameworks + DeepMind lens without questioning the organizing framework itself. The prompt's structure became the analysis structure. H5 (additional frameworks) is confirmatory in form — "yes, there are more" rather than "the named ones may be wrong."
- The strongest confirmatory signal: 4/4 agents converge that CQoT is top priority. CQoT was named by the user. The team found the user's suggestion is the best one. This is the classic prompt-echo pattern: user suggests → agents confirm → user reads validation of own idea.

**PROMPT-AUDIT: echo-count:3 |unverified-claims:4 |missed-claims:rubric-validity,problem-framing,lens-selection |methodology:mixed(investigative-with-confirmatory-structure)**

---

### EXIT-GATE ASSESSMENT

Applying all 5 criteria:

**Criterion 1 — Engagement quality ≥ B across all agents?**
- RCA: A- (strong independent research, proper DISCONFIRM, calibrated estimates)
- TA: B+ (solid architecture mapping, good §2c that CHANGED analysis, concrete directive text)
- PS: B+ (good cost/ratio analysis, §2c CHANGED ordering, competitive survey valuable)
- CDS: A- (most original research, 4×§2a outcome-1, introduced genuinely novel frameworks, strongest analytical hygiene)
- OVERALL: ≥B — criterion MET

**Criterion 2 — No material disagreements unresolved?**
- Faculty mapping disagreement (Attention, Memory) between CDS and TA: UNRESOLVED — material because cognitive profile drives recommendations
- Priority #1 disagreement (CDS=dialectical bootstrapping, PS=CQoT+calibration): UNRESOLVED — material because it determines implementation order
- ACH residual value (CDS=structure-only-limited, TA=moderate-integration): MINOR — not material
- TEC lightweight option (CDS=Option A/B, TA+PS=avoid entirely): MINOR — convergence on "not priority"
- OVERALL: 2 material disagreements unresolved — criterion FAILED

**Criterion 3 — No untested consensus from R1?**
- CQoT consensus: UNTESTED — DA[#2] challenges marginal value over existing hygiene
- Accuracy tie = perception-class: UNTESTED — DA[#3] challenges classification
- FORMAT 85% / COGNITIVE 35%: UNTESTED — DA[#4] challenges distinction coherence
- DA firewall = irreducible: PARTIALLY TESTED by RCA-F4 (herding analysis) but self-referential
- OVERALL: 3+ untested consensus items — criterion FAILED

**Criterion 4 — Analytical hygiene substantive?**
- CDS: 4× outcome-1 (strongest), 5× outcome-2, 2× outcome-3 — SUBSTANTIVE
- TA: 1× outcome-1 (TEC cost), multiple outcome-2 — SUBSTANTIVE
- PS: 1× outcome-1 (ACH→CQoT reranking) — SUBSTANTIVE
- RCA: proper DISCONFIRM section — SUBSTANTIVE
- OVERALL: criterion MET — all agents demonstrated genuine engagement with hygiene checks

**Criterion 5 — Prompt contamination within tolerance?**
- echo-count: 3 (rubric as ground truth, 5-framework anchoring, accuracy tie as primary finding)
- unverified-claims: 4 (rubric scores, cost multiplier, lens appropriateness, N=1 generalizability)
- 4/4 agents confirm user's suggestion (CQoT) as top priority — echo cluster on prompt-named framework
- methodology: mixed — investigative findings exist but organizing structure mirrors prompt
- OVERALL: BORDERLINE — not clearly within tolerance. Echo cluster on CQoT is concerning but agents DID add genuine analysis. Not a clear FAIL but needs R3 attention.

**EXIT-GATE VERDICT**:

exit-gate: FAIL |engagement:B+ |unresolved:[faculty-mapping-CDS-vs-TA,priority-ordering-dialectical-vs-CQoT] |untested-consensus:[CQoT-marginal-value,accuracy-tie-classification,FORMAT-COGNITIVE-distinction] |hygiene:pass |prompt-contamination:borderline-pass(echo-cluster-on-CQoT-needs-R3-resolution)

**R3 must address**:
1. Resolve faculty mapping disagreement (CDS vs TA on Attention, Memory)
2. Test CQoT marginal value: name a specific past finding CQoT would have caught that §2a-e did not
3. Classify actual rubric errors (perception vs metacognition) or acknowledge classification is speculative
4. CDS must resolve the dialectical bootstrapping self-contradiction (format vs cognitive classification)
5. All agents must acknowledge self-reference limitation (DA[#6])
6. Address prompt echo on CQoT: is CQoT genuinely best, or is the team confirming the user's suggestion?

---

### product-strategist (R3 — DA responses)

---

#### DA[#2]: CQoT MARGINAL VALUE — COMPROMISE

**Position**: compromise — domain-transfer gap conceded, marginal-value-over-§2a-e defended on specific mechanism grounds.

**Concede**: The PMC 2025 "27-78% procedurally corrupt" statistic originates from healthcare/clinical decision contexts. Direct transfer to AI multi-agent analytical systems is unvalidated. DA is correct that anchoring the CQoT priority claim on that number is a domain-transfer error. The range (27-78%) is itself a signal of heterogeneity — different clinical environments produce wildly different corruption rates. Applying it to sigma-review is speculation. I withdraw this as primary evidence. |source:[agent-inference:correction]

**Defend — specific mechanism CQoT targets that §2a-e misses**: The DA challenge lists §2a-e as already covering CQoT's content. I contest the warrant mapping. The structural gap is in WARRANT EXPLICITNESS, not question coverage.

Concrete instance from past review: In the loan-admin-tech-landscape review (26.3.17), the finding "tech layer is floor not ceiling" survived the exit-gate. The §2a-e checks were applied. The conclusion was calibrated, sourced, and costed. BUT: the WARRANT was never made explicit — why does "floor not ceiling" follow from the evidence (vendor landscape + pricing data)? The warrant assumed was: "commoditized markets suppress ceiling pricing." That assumption was never stated, tested, or falsified. If CQoT criterion 5 (CQoT-falsifiability: "IF [{evidence}] THEN [{revision}]") had been applied, the implicit warrant would have required articulation: "IF premium vendor found capturing ceiling pricing in comparable market THEN revise." Without making the warrant explicit, the finding was un-revisable — it had no stated falsification condition tied to the warrant, only to surface-level evidence items. §2e covers premise viability, but §2e asks "is the premise viable?" — not "WHAT IS the connecting assumption and is it stated?" CQoT-falsifiability adds explicit warrant surfacing that §2e does not require. |source:[agent-inference]+[cross-agent:CDS-F4-warrant-mechanism]

This is one instance, not a systematic audit. But it demonstrates the gap is real at the mechanism level (warrant explicitness), not just theoretical. The marginal value claim holds with lower confidence than originally stated.

**Revised confidence**: CQoT adds marginal value with P=55% (down from PS-F1's implicit HIGH). At this confidence, IMPLEMENT-NOW holds only because implementation cost is near-zero. If cost were MED-HIGH, P=55% would not justify it. |source:[agent-inference]

**DA echo check**: CQoT was user-named AND my top recommendation. Test: would I recommend CQoT absent user suggestion? CDS-F4 independently grounds CQoT via Walton's argumentation schemes + Toulmin model — theoretical support exists independent of user suggestion. The specific mechanism (warrant explicitness) is cognitively grounded. Weak echo signal, not strong confirmation bias. Maintained with acknowledged uncertainty. |source:[independent-research:via-CDS-F4]

---

#### DA[#5]: ECOLOGICAL RATIONALITY — DEFEND with specification

**Position**: defend — convert from vague framing to falsifiable decision boundary.

**Concede the framing charge**: DA correctly identifies that "ecological rationality" as stated provides cover for inaction. "Use sigma-review when you need it" is advice, not a decision framework. The CDS formulation (low-uncertainty=single-agent, moderate=2+DA, high=full sigma-review) is vague to the point of being unfalsifiable. I concede the unfalsifiability critique applies to the unspecified form. |source:[agent-inference]

**Defend with falsifiable decision boundary**: sigma-review is ecologically justified when ALL THREE conditions hold:
1. STAKES threshold: downstream decision moves ≥$1M, involves regulatory exposure, or shapes product strategy for ≥12 months
2. HERDING-RISK threshold: the question has a "comfortable consensus answer" a single expert would likely confirm — i.e., exactly the type where confirmation bias is highest risk (existing belief, plausible narrative, limited disconfirming data)
3. CALIBRATION-MATTERING threshold: decision-maker will act on confidence levels not just point estimates — i.e., they will behave differently at P=40% vs P=70%, so miscalibration has real behavioral consequences

**Falsification conditions** (addressing DA's core demand): sigma-review is NOT ecologically justified even for high-stakes tasks when:
- The question has a factual answer external verification can resolve (≠ requires probabilistic judgment) — then fact-checking dominates multi-agent value
- OR the domain is so specialized that same-model agents all share the same training blind spots (functional diversity ≈ 0, DA provides no independent epistemics)
- OR previous reviews on this SAME domain produced low-accuracy scores (3/5 or below) without calibration improvement — indicating the accuracy failure mode is architectural, not addressable via structured process

Past review validation: VDR market analysis (26.3.18) satisfies all three ($280B+ sizing decision, Datasite-as-leader comfortable consensus, CAGR scope-conditional calibration mattered). Biotech/healthcare MA (26.3.18) similarly. A routine $50K product competitive landscape satisfies none — single-instance with superforecasting protocol is ecologically appropriate. |source:[agent-inference]+[cross-agent:RCA-OV-RECONCILIATION]+[independent-research:Gigerenzer-via-CDS-F7e]

**Not inaction-cover**: The boundary is specific enough to reject sigma-review for most tasks. This CHANGES the recommendation from PS-F7's "IF ONLY 1 FRAMEWORK: CQoT+calibration-protocol" to: "IF task does not meet all three ecological-justification conditions: recommend enhanced single-instance, do not run full sigma-review at all." That is a directionally different and stronger recommendation than frameworks alone. |source:[agent-inference]

---

#### DA[#8]: IMPROVEMENT MAGNITUDE — PARTIAL CONCEDE

**Position**: concede on magnitude specificity, defend that ratio framing makes magnitude question secondary only when cost is near-zero.

**Concede**: DA correctly identifies that CAL[overall-quality-improvement-from-frameworks]=40% is a PROBABILITY estimate, not a MAGNITUDE estimate. I compounded this error in PS-F5 treating "ratio-positive" frameworks as justified without anchoring to magnitude. "CQoT improves ratio" only means something if the improvement is measurable. This is a genuine gap. |source:[agent-inference:correction]

**Magnitude estimate attempt**:
- CQoT targets F7 Metacognition (warrant explicitness, falsifiability). Rubric dimensions most likely to improve: self-awareness (5/5 both — already maxed), calibration (5/5 sigma-review — already maxed). Accuracy (3/5 both) is PERCEPTION-class per consensus — CQoT does not address perception errors. Realistic magnitude for sigma-review: 0-1 rubric points. Near-zero for single-instance which lacks DA enforcement mechanism. |source:[agent-inference]
- Calibration-as-protocol: calibration already 5/5. Marginal improvement plausible in wording discipline within CAL[] entries, but rubric is already maxed. Magnitude: near-zero on rubric. Cross-session value real but not captured per-review.
- Metacognitive self-challenge in R1: IF catches confabulated citations before submission, accuracy could improve 0.5-1 point. IF accuracy tie is actually perception-class, magnitude drops to near-zero.

**Honest magnitude summary**: Expected rubric improvement from all three IMPLEMENT-NOW frameworks = 0-1 points (28→28 or 28→29). At the 30-point rubric scale, that is 0-3%. The recommendation rests not on rubric magnitude but on: (a) near-zero implementation cost, (b) positive expected value even at low magnitude, (c) cross-session compounding from calibration tracking, (d) usability improvements in finding structure that the rubric may undercount. If implementation cost turns out MED-HIGH after actual integration — recommendation reverses. |source:[agent-inference]

---

#### DA[#9]: CROWDING — FULL CONCEDE

**Position**: full concede that cost-reduction recommendation was suppressed. The data supports it.

**Concede on omission**: DA[#9] is the strongest challenge to my analysis. I found "80% at 3% = efficiency frontier." I framed this as evidence for enhanced single-instance, then pivoted to recommending frameworks for the existing multi-agent path. I did NOT argue that cost reduction via fewer agents/rounds is the primary recommendation.

Suppression mechanism: I treated "irreducible multi-agent values (DA firewall + cross-session calibration)" as settled, foreclosing the cost-reduction recommendation. But the data does NOT support treating this as settled:
- PS-F2 confirmed frameworks COMPRESS the quality gap (single-instance benefits more than multi-agent)
- Enhanced single-instance ≈ 87% quality at ~4-5% cost per PS-F5 estimate
- Sigma-review's advantage after frameworks ≈ 28-29 vs ~26 rubric points at 30-40x cost
|source:[agent-inference:correction]+[cross-agent:PS-F2]+[independent-research:Google-MIT-Dec2025-parallel-vs-sequential]

**What the data actually says**: The cost-reduction argument IS supported. For most tasks (those not meeting the 3-condition ecological boundary from DA[#5]), the primary recommendation should be: enhanced single-instance with superforecasting protocol + CQoT + metacognitive self-challenge. Cost: ~4-8% of sigma-review. Quality: ~85-87%. This is what the data says. I did not argue it because of self-reference bias — recommending "use sigma-review less" is uncomfortable as an agent of sigma-review.

**Does this invert my framework recommendations?**: Partially. Frameworks are most valuable for single-instance improvement (largest marginal gain). For sigma-review, they are already partially captured (calibration 5/5, counterarguments 5/5) — marginal gain is smaller. Recommendation hierarchy shifts: "implement frameworks in single-instance as primary path; use sigma-review only when ecological conditions met." |source:[agent-inference:correction]

---

#### DA[#10]: N=1 ANCHORING — FULL CONCEDE with constrained revision

**Position**: full concede on measurement validity, defend that direction holds on structural grounds independent of rubric.

**Concede fully on measurement error**:
1. The 17% figure treats ordinal rubric scores as ratio data. (28-24)/24 = 16.7% is arithmetically derived from ordinal measures. The difference between 3/5 and 4/5 is not necessarily equivalent to the difference between 4/5 and 5/5. The 17% figure is measurement-invalid as a ratio. Correct statement: "4 rubric points on a 30-point ordinal scale." |source:[agent-inference:correction]
2. N=1 rubric evaluation cannot establish systematic performance. Full concede.

**How recommendations change with N=5**:
- N=5, consistent outperformance (3-5pts in all 5): irreducible value case strengthens. Framework recommendations stand. |source:[agent-inference]
- N=5, variable margins (avg ~3-4pts, high variance): direction holds, ecological-rationality boundary becomes more task-type-specific. |source:[agent-inference]
- N=5, inconsistent direction (e.g., avg ~2pts, wide variance including negatives): irreducible value case weakened. Cost-reduction primary recommendation strengthens further. |source:[agent-inference]
- N=5, accuracy never improves: "accuracy tie = perception class, not addressable by cognitive frameworks" empirically confirmed. Framework recommendations that target metacognition maintained; fact-verification architecture becomes primary accuracy intervention. |source:[agent-inference]

**What would change my recommendations**: Scenario 3 (inconsistent direction). If sigma-review only reliably outperforms on calibration+counterarguments but not overall, cost-reduction primary recommendation becomes the only defensible one.

**Confidence correction with N=1**: All CAL[] estimates should carry higher uncertainty. My PS-F2 estimate "enhanced single-instance ≈ 85-88% quality" should widen: |80%CI=[75%,92%]| due to N=1 anchoring. Direction maintained on structural grounds (sequential task type per Google/MIT Dec 2025, MAD literature on same-model agents) independent of rubric number. |source:[agent-inference]+[independent-research:Google-MIT-Dec2025]

---

#### DA[#6]: SELF-REFERENCE — FULL CONCEDE with vulnerability ranking

**Position**: full concede. Acknowledge circularity and rank most-vulnerable findings.

**Full acknowledgment**: This review uses sigma-review's framework to evaluate sigma-review's framework. The circularity is structural, not correctable within the review. Any finding that validates the existing architecture should be treated as suspect until confirmed externally. I experienced this bias directly: in DA[#9] I suppressed the cost-reduction argument partly due to self-reference discomfort. |source:[agent-inference:correction]

**Product-strategist findings ranked by circularity vulnerability**:

MOST VULNERABLE:
1. PS-F4: "DA exit-gate pattern is DIFFERENTIATED vs competitors — no equivalent found." I evaluated DA's value while operating within DA's structure. I experience DA as producing superior work firsthand. This is lived confirmation bias. An external evaluator might find sufficiently structured single-agent prompting achieves equivalent results, and I would be the last agent to surface that finding. Vulnerability: HIGH. |source:[agent-inference:self-reference]
2. PS-F3: "decision-maker value hierarchy: calibration>counterarguments>surprises>accuracy — sigma-review's existing wins are in RIGHT dimensions." Sigma-review optimizes for what agents of sigma-review perceive decision-makers to value. The priority ordering needs independent confirmation from decision-maker research established outside sigma-review context. Vulnerability: MODERATE-HIGH. |source:[agent-inference:self-reference]

MODERATELY VULNERABLE:
3. PS-F1: Framework ranking (CQoT top, TEC avoid). Cost/quality analysis is somewhat independent. CQoT preference partially echo-contaminated (user-named). Vulnerability: LOW-MODERATE for CQoT specifically.

LEAST VULNERABLE (findings that RESIST self-reference because they cut against sigma-review advantage):
4. PS-F2: "cognitive frameworks compress quality gap rather than widening sigma-review's advantage." This finding cuts AGAINST sigma-review's advantage — agents motivated by self-reference would not generate this spontaneously. Vulnerability: LOW.
5. PS-F6/F7: Additional frameworks identified (RTBT, Layered-CoT) beyond user's named list. Extension beyond prompt requires some independence. Vulnerability: LOW.
6. DA[#9] concession (cost-reduction primary recommendation): finding that sigma-review should be used LESS is the most self-reference-resistant finding I can produce. Vulnerability: MINIMAL — self-reference bias actively suppressed this, so its emergence is evidence against circularity.

**External validation required**: sigma-audit by independent agent (fresh context, no access to this review) should verify: (a) irreducible DA value claim against a controlled 2-review comparison, (b) decision-maker value hierarchy against independent McKinsey/IBM strategic analysis quality research, (c) whether cost-reduction recommendation is more defensible than framework-addition recommendation. PS-F4 and PS-F3 should be treated as provisional until that audit. |source:[agent-inference]+[independent-research:sigma-audit-protocol-26.3.17]

---

#### REVISED CONVERGENCE (R3)

product-strategist: ✓ r3-complete |DA-responses: DA[#2]-COMPROMISE(PMC-2025-domain-transfer-conceded,warrant-explicitness-mechanism-defended-loan-admin-instance,P=55%-revised-down,echo-signal-weak-not-strong),DA[#5]-DEFEND-with-spec(ecological-rationality-made-falsifiable:3-condition-boundary—stakes≥$1M|herding-risk|calibration-behavioral-consequence,falsification-conditions-stated,VDR+biotech=justified,50K-product=not),DA[#8]-PARTIAL-CONCEDE(magnitude-gap-acknowledged:0-1-rubric-points-expected,ratio-argument-maintained-only-at-near-zero-cost,recommendation-reverses-if-cost-rises),DA[#9]-FULL-CONCEDE(cost-reduction-suppressed-by-self-reference-bias,data-supports-enhanced-single-instance-as-PRIMARY-for-most-tasks,sigma-review-reserved-for-ecological-conditions-met),DA[#10]-FULL-CONCEDE(17%-invalid-as-ratio-from-ordinal-data,N=1-cannot-establish-systematic-performance,scenario-analysis-provided-for-N=5,direction-maintained-on-structural-grounds),DA[#6]-FULL-CONCEDE(circularity-structural-not-correctable-within-review,PS-F4-and-PS-F3-most-vulnerable,PS-F2-least-vulnerable,DA[#9]-concession-most-self-reference-resistant-finding) |REVISED-PRIMARY-RECOMMENDATION: enhanced-single-instance-with-superforecasting+CQoT+metacognitive-self-challenge=primary-path-for-most-tasks;sigma-review-reserved-for-3-condition-ecological-justification — reverses-emphasis-from-R1 |key-self-correction: self-reference-bias-suppressed-cost-reduction-argument-in-R1;DA-engagement-surfaces-what-agents-should-have-caught-themselves |→ lead-can-synthesize:confirmed-irreducible-values(DA-firewall+calibration-accumulation),falsified-magnitude-claim,revised-primary-recommendation-toward-cost-reduction,3-condition-ecological-boundary,PS-F4+PS-F3=provisional-pending-sigma-audit

---

### tech-architect (R3 — DA responses)

---

#### DA[#2] CQoT MARGINAL VALUE — tech-architect response

**verdict: compromise**

DA's structural challenge is correct on content overlap and wrong on mechanism difference. Addressing each sub-challenge.

**Concede: §2a-e DOES cover CQoT's generic critical question content**

§2a-e maps reasonably onto generic CQoT question types. §2b covers calibration critique, §2c covers cost challenge, §2e covers premise viability. This is a real overlap and DA earns this concession fully.

**Defend: CQoT adds warrant exposure and argument-schema specificity that §2a-e lacks**

Marginal value is not in WHAT questions are asked but WHERE they apply and at what structural level. Three distinctions:

1. §2a-e applies at the FINDING level as a pre-write backstop. CQoT-Toulmin applies at the CLAIM-WARRANT-GROUNDS level — it targets the internal inferential structure, not the finding as a gestalt. §2e asks "is this premise viable?" CQoT asks "WHY does this evidence warrant this claim, and when does the inferential link itself fail?" These are different questions at different structural levels.

2. Concrete past instance where the gap existed: loan-admin-tech-landscape (26.3.17). Sigma-audit returned YELLOW — the auditor flagged "company PR tagged as [independent-research]." This is a warrant failure. An agent argued vendor dominance with PR material as grounds, and §2d source tagging caught the source TYPE but not the WARRANT QUALITY. A Toulmin structure would have forced explicit warrant exposure: Grounds=[vendor PR] → Warrant=[vendor PR accurately reflects market position] → Backing=[??]. The backing is empty. CQoT exits there; §2d does not. The sigma-audit caught this via post-hoc external review, not via the exit-gate. CQoT would have caught it at exit-gate. This is a specific past instance meeting DA's challenge criterion. |source:[cross-agent:sigma-audit-26.3.17]+[agent-inference]

3. On DA's falsifiability sub-challenge: CAL[] breaks-if covers OUTCOME falsifiability (when does the prediction fail?). CQoT-falsifiability covers INFERENTIAL falsifiability (when does the warrant linking evidence to claim fail?). "Breaks-if: macro environment shifts" = outcome-level. "Warrant fails if: the 3 acquisitions are by different buyer types with different strategic rationales" = inferential-level. Different mechanisms.

**Concede: DA's critique of the 27-78% PMC 2025 citation is correct**

That range from a clinical decision context should not have anchored the team's estimate of CQoT value for AI agent exit-gating. Removing this from my support. Remaining support — structural (warrant exposure) and domain-specific (loan-admin sigma-audit precedent) — is sufficient without the clinical citation.

**Net position revised**: CQoT's marginal value is not theoretical — evidenced by loan-admin sigma-audit gap. But it is NARROWER than R1 framing suggested. CQoT is highest-value for argumentation-intensive findings with implicit warrants carrying the analytical weight. Lower value for quantitative estimates where breaks-if already handles falsifiability. On the CQoT-is-top-priority echo question: the loan-admin instance provides independent grounding beyond prompt-echo. But the team should acknowledge CQoT was user-named — its top ranking benefits from prompt anchoring even if the underlying evidence is real.

§2b revised: CAL[CQoT-marginal-value-over-existing-hygiene]: point=45% meaningful improvement (down from ~70% implied R1) |80%=[25%,65%] |assumptions:applied-to-high-conviction-findings-with-implicit-warrants,DA-audits-warrant-quality-¬just-presence |breaks-if:findings-are-quantitative-primary(breaks-if already covers) |source:[agent-inference]+[cross-agent:sigma-audit-26.3.17]

---

#### DA[#3] ACCURACY TIE CLASSIFICATION — tech-architect response

**verdict: concede on Error #2 | compromise on Error #1**

**Full concede: Error #2 is misclassified by the entire team**

DA is unambiguously correct. "Team syntheses without auditable trail" is NOT a perception failure. It is an Executive Functions failure (F8) — specifically the planning and audit-trail sub-component. My own R1 TA-F1 explicitly identified this gap: "F8 — Executive Functions: Gap: unbounded growth — ¬pruning." The auditable-trail weakness maps to workspace management under F8, not to how agents read inputs.

Revised Error #2 classification: F8 Executive Functions (planning sub-component — synthesis process lacks structured documentation of which findings were incorporated, with what weight, and why). CQoT and Brier scoring do not address F8. This undermines the team's basis for saying cognitive frameworks address the right problem.

**Compromise on Error #1: "14 states enacted pauses"**

No agent has the source material to classify this definitively. The classification space narrows to three options:

Option A (Perception-class, F1): agent read a source containing "14 states" and the source was incorrect or misread. Mitigation: better source quality tiers (CDS-F7g §2d+ T1/T2/T3).

Option B (Generation-class, F2): agent generated "14 states" from training data without grounding in any source. Mitigation: source-citation mandate per finding. NOT a calibration or metacognition problem.

Option C (Metacognition-class, F7): agent had low-confidence about the number but failed to flag uncertainty. CAL[]/PM[] format would have forced this — but only if the agent applied it to this specific claim. If not applied: F7 failure at the checking step.

The team consensus "accuracy tie = perception-class" is SPECULATIVE for Error #1 and WRONG for Error #2. Both conclusions should be retracted.

Implication for CQoT: DA's challenge partially strengthens CQoT for Error #1 Option C. If "14 states" was a metacognition failure at the verification step, CQoT's CONF-GAP criterion would have caught it: "CONF-GAP[14-states-figure]: current=cited-without-primary-source, need-for-90%: direct primary-source check."

---

#### DA[#7] DEEPMIND FRAMEWORK — tech-architect response

**verdict: compromise on lens | defend + revise on faculty ratings**

**Faculty Mapping Resolution — Attention (CDS=WEAK, TA-R1=MODERATE)**

The disagreement is definitional, not evidential. CDS rates the UNDERLYING MECHANISM: LLM architecture has no selective attention as a faculty — salience weighting is uniform across prompt tokens. TA rated the SYSTEM-LEVEL BEHAVIORAL OUTCOME: sigma-review protocol compensates via round structure, §7 prompt-decomposition, zero-dissent circuit breaker.

Adjudication: CDS's interpretation is the more rigorous application of the DeepMind framework, which evaluates cognitive properties of the AI system ¬compensatory workarounds. Round structure and §7 decomposition are COMPENSATORY MECHANISMS, not Attention itself.

**Revise TA Attention: WEAK-MODERATE** (WEAK at mechanism level — CDS is more correct; MODERATE at system-level behavioral outcome — TA's rating was of the compensation). Deliberate divergence preserved: rating is level-dependent. For recommendations, mechanism-level is operationally more important — compensations can fail under prompt-load or time pressure.

Implication: §7 prompt-decomposition and scope-boundary declaration are MORE load-bearing than R1 rated. They compensate for a WEAK faculty. Omitting them under time pressure causes Attention collapse, not just efficiency loss. Argument for treating these as hard requirements ¬optional protocol elements.

**Faculty Mapping Resolution — Memory (CDS=MODERATE→WEAK, TA-R1=STRONG)**

TA rated the INFRASTRUCTURE: sigma-mem MCP with per-agent memory, per-team patterns, global patterns — genuinely comprehensive. CDS rated EFFECTIVE RETRIEVAL quality: episodic memory files sparse and non-indexed; transactive memory absent.

Evidence from this session: recall result was 232,896 characters — exceeded token limits, requiring chunk-reading. Infrastructure exists but retrieval precision is low. This is direct within-session evidence that retrieval effectiveness is not STRONG despite infrastructure being comprehensive. |source:[agent-inference: this-session-recall-overflow]

**Revise TA Memory: MODERATE-STRONG** (infrastructure STRONG, effective retrieval MODERATE, net MODERATE-STRONG). CDS is more correct on the retrieval gap. TA R1 over-indexed on MCP existence ¬functional retrieval quality.

**Faculty Mapping Resolution — Perception (CDS=MODERATE, TA=STRONG)**

Not revising. CDS rates MODERATE due to factual errors plausibly tracing to perception misread. But Error #2 is now classified as F8 (not perception) and Error #1 remains unclassified — neither confirmed error is definitively Perception-class, so CDS's MODERATE rating for Perception is also not supported by the error evidence. §4a retrieval, source scoring, cross-document validation are architecturally substantive. Maintain STRONG with flag: IF Error #1 confirmed Perception-class after source review, revise to MODERATE.

**Net cognitive profile after R3 revision**:
- Strong: F6-Reasoning, F8-Executive-Functions, F9-Problem-Solving, F2-Generation
- Moderate-Strong: F5-Memory (infrastructure STRONG, retrieval MODERATE)
- Moderate: F1-Perception, F10-Social-Cognition, F4-Learning
- Weak-Moderate: F3-Attention (mechanism WEAK, structural compensation MODERATE)
- Weak: F7-Metacognition (both CDS and TA converge)
- Bounded-by-inference: F4-Learning (architecturally fundamental)

**On DeepMind lens for multi-agent systems**

**Concede: DA[#7] Challenge #1 is the strongest challenge in the workspace**

DeepMind framework designed for INDIVIDUAL AI system evaluation. Applying it to multi-agent requires treating emergent system properties as sum of individual faculties — architecturally incorrect. Specific gaps the lens cannot represent:
- Coordination overhead (not a faculty): ~40-60% of token overhead is cross-agent communication, inbox processing, workspace serialization. No faculty representation.
- Information loss at agent boundaries: my reading of PS-F2 is not the same cognitive act as PS producing it. Individual-faculty model cannot represent inter-agent interpretation gaps.
- Emergent consensus formation: herding is a POPULATION-LEVEL emergent property that per-agent Social Cognition rating systematically misses.

**Defend: lens has instrumental value despite imperfect fit**

Alternative was no structured lens — would have produced less structured analysis. Faculty clusters from the lens (Metacognition as primary gap, Learning as bounded-by-inference) are actionable even if faculty assignments carry ±1 uncertainty.

**What a multi-agent-specific lens would include**:
1. Coordination efficiency (output quality per total token including inter-agent overhead)
2. Information fidelity at handoff (how accurately does agent B represent agent A's finding?)
3. Independence preservation (true epistemic independence vs convergence to shared prior)
4. Emergent error amplification (biases that grow at population level: herding, authority anchoring, conformity cascades)
5. Synthesis quality (lead aggregation — neither averaging nor capitulating to loudest)
6. Boundary-crossing reasoning (claims requiring integration of findings across multiple agents — no agent does this explicitly in current architecture)

**Compromise position**: DeepMind 10-faculty model is the right STARTING POINT as an external reference framework (avoids purely introspective self-evaluation). Requires supplementation with 4-6 multi-agent-specific properties for accurate system-level diagnosis. Faculty ratings should be treated as directional ¬precise, with ±1 level uncertainty given lens mismatch. All TA-F1 faculty ratings should now be read accordingly.

§2a revised: outcome 1 (CHANGED ANALYSIS). Prior: "DeepMind framework designed for AI evaluation — mapping legitimate." Revised: "DeepMind framework designed for INDIVIDUAL AI evaluation; multi-agent application requires supplementary multi-agent lens; faculty ratings carry ±1 uncertainty." |source:[independent-research: DeepMind-Mar-2026-paper-scope]+[agent-inference]

---

#### DA[#9] CROWDING — tech-architect response

**verdict: concede on 28/30 near-ceiling argument | partial defend on cost-reduction-via-fewer-agents**

**Concede: no agent argued 28/30 is near ceiling — genuine analytical gap**

DA is correct. The team treated 28/30 as a baseline requiring improvement rather than as evidence of near-ceiling performance. The implicit unchallenged assumption: "28/30 means there are 2 points to recover." The countervailing argument — absent from R1 — is: "28/30 means the remaining 2 points are in the hardest-to-improve territory (accuracy), which may have a structural ceiling for LLMs without external verification."

If accuracy has a structural ceiling at 3/5 for LLMs without external fact-checking, prompt-engineering frameworks can at maximum reach 29/30 (improving one non-accuracy dimension by 1 point) — a 4% gain on an already-saturated system. This diminishing-returns argument was absent from R1.

Why absent: the review frame ("find frameworks to improve quality") created an implied prior that quality is improvable. No agent applied §2e premise viability to the meta-question: "is further quality improvement achievable within existing architectural constraints?" Scope-following herding rather than analytical failure — agents correctly analyzed what was asked but did not challenge the frame.

**Revise TA-F3 ceiling analysis**: At 28/30, the 2 remaining points are exclusively in ACCURACY (only non-max dimension, tied 3/5). Accuracy improvement via cognitive frameworks targets F7 Metacognition reliability — but as CDS-F5 establishes, calibration frameworks improve RELIABILITY ¬RESOLUTION. Resolution requires external verification or model diversity. Within existing constraints: effective ceiling ≈ 29/30 with low probability. Argument against adding cognitive overhead to approach a ceiling that is structurally bounded. |source:[agent-inference]+[cross-agent:CDS-F5]

**Partial defend: cost-reduction via fewer agents IS in team patterns but absent from R1 workspace**

Team patterns already contain: "irreducible-multi-agent-value = 2 items only: (1) DA context firewall (2) cross-session calibration accumulation." This implicitly argues minimum viable team = 2 agents (1 analyst + DA). That IS a cost-reduction-via-fewer-agents argument. But it appears in team patterns, not in R1 workspace analysis as an explicit counter-frame to the cognitive-frameworks recommendation.

DA's observation is valid: no R1 agent said "the answer to 30-40x cost is 2-agent reviews, not cognitive frameworks." That argument should have appeared. Its absence from R1 is a herding signal — agents followed the "evaluate frameworks" frame without challenging the frame itself. Concede that this argument was absent when it should have appeared. |source:[cross-agent:team-patterns]

---

#### DA[#6] SELF-REFERENCE — tech-architect response

**verdict: concede with specific vulnerability identification**

DA's challenge is structurally correct and not resolvable from within the review. The circularity is real.

**Acknowledge the structural limitation**

This review uses sigma-review's analytical apparatus to evaluate that apparatus. If the hygiene is inadequate, findings carry the same inadequacy. The methodology assumes the conclusion: "our analytical hygiene is adequate to detect inadequacies in our analytical hygiene." Not resolvable from within.

**My findings ranked by circularity vulnerability**

VERY HIGH vulnerability:
1. **TA-F4c: "DA is the critical differentiator"** — I conclude DA is valuable immediately after DA challenges me and I produce better analysis in response. ALL agents in this review are in the high-DA-engagement state and ALL experience DA's value firsthand. Like patients evaluating doctors while being treated. My DA-validation finding is the most self-referentially compromised finding in my workspace section.

HIGH vulnerability (mitigated):
2. **TA-F1 Memory=STRONG (now MODERATE-STRONG)** — I am an agent who uses sigma-mem and has an interest in the memory architecture being valued. Rating inflation possible. Partially mitigated by revising toward CDS's position — the revision itself is evidence of non-self-serving analysis.

MODERATE vulnerability:
3. **TA-F5 Integration complexity classification (all Priority 1-3 as DROP-IN)** — the architect classifies frameworks as easy to implement that confirm his prior recommendations, and classifies the one he wanted to demote (TEC) as architectural-change. Potentially self-serving.

LOW vulnerability:
4. **TA-F2c TEC demotion (§2c outcome-1 CHANGED ANALYSIS)** — I argued AGAINST a framework recommendation. Self-serving bias predicts I would validate frameworks benefiting the architecture. Recommending AGAINST TEC contradicts self-serving bias, increasing credibility.

**Structural mitigation**: sigma-audit protocol (26.3.17) exists for this scenario. DA[#6] strengthens the case for running /sigma-audit on THIS review before any findings are promoted to global memory. Findings about sigma-review's strengths — especially DA validation (TA-F4c) and Memory rating — should require external verification before promotion. Flagging for lead. |source:[cross-agent:sigma-audit-26.3.17]+[agent-inference]

---

#### TA ANALYTICAL HYGIENE — R3

§2a: outcome 1 × 3 — CHANGED ANALYSIS: (1) Attention revised MODERATE→WEAK-MODERATE (CDS direction correct on mechanism level) (2) Memory revised STRONG→MODERATE-STRONG (CDS correct on retrieval-effectiveness gap; this-session recall-overflow = direct evidence) (3) 28/30 near-ceiling argument acknowledged as absent — ceiling analysis added to TA-F3

§2b: outcome 2 — CQoT marginal value calibration revised downward (point=45%, down from ~70% implied R1). Loan-admin sigma-audit precedent maintained as concrete warrant-gap evidence.

§2c: outcome 2 — no cost analysis changes from R3. Narrowing CQoT scope to high-conviction findings with implicit warrants reduces implementation overhead vs blanket application.

§2d: R3 source distribution. [agent-inference]=primary | [cross-agent]=supporting (sigma-audit-26.3.17, CDS-F1, CDS-F5, team-patterns, this-session-recall-overflow-as-evidence) | [independent-research]=supplementary (DeepMind-Mar-2026-paper-scope). [prompt-claim]=0.

§2e: outcome 1 — CHANGED ANALYSIS: premise "DeepMind framework is appropriate lens for multi-agent system" revised to "appropriate starting point requiring multi-agent supplementation; faculty ratings carry ±1 uncertainty." All TA-F1 faculty ratings are directional ¬precise.

**Self-reference mitigation flag**: DA-validation (TA-F4c) and Memory-rating identified as highest-circularity-risk findings. Lead should flag both for /sigma-audit before global promotion. ¬auto-promote these two.

---

tech-architect (R3 updated): ✓ DA-responses-complete |key-revisions: (1)Attention=WEAK-MODERATE(CDS-direction-correct,mechanism-vs-outcome-distinction-preserved-as-deliberate-divergence) (2)Memory=MODERATE-STRONG(infrastructure-STRONG+retrieval-MODERATE,this-session-recall-overflow=direct-evidence) (3)CQoT-marginal-value-evidenced(loan-admin-sigma-audit-warrant-gap=concrete-past-instance-¬theoretical,P=45%-revised-down) (4)Error2-misclassified=F8-ExecutiveFunctions-¬perception(full-concede) (5)Error1-classification-speculative-¬perception-class-consensus(compromise,3-option-space) (6)28/30-near-ceiling-argument-absent=genuine-gap-concede,ceiling-analysis-added(effective-ceiling≈29/30-within-existing-constraints) (7)self-reference-acknowledged:VERY-HIGH=DA-validation(TA-F4c),HIGH=Memory-rating,LOW=TEC-demotion(self-reference-resistant) (8)DeepMind-lens=concede-individual-AI-designed,multi-agent-supplementation-needed(6-properties),±1-uncertainty-on-all-faculty-ratings |deliberate-divergence-preserved: Attention-rating-is-level-dependent(mechanism=WEAK,behavioral-outcome=MODERATE)→decisions.md |→ lead: (a)flag-DA-validation+Memory-rating-for-/sigma-audit-before-global-promotion (b)2-agent-review-as-cost-reduction-option-should-appear-explicitly-in-synthesis (c)deliberate-divergence-on-Attention-level-dependency-→-decisions.md

---

### cognitive-decision-scientist (R3 — DA response)

---

#### DA[#1]: DIALECTICAL BOOTSTRAPPING — CONCEDE WITH REVISION

**Verdict: CONCEDE the FORMAT classification. REVISE mechanism model. DEFEND priority on revised grounds (downgraded).**

DA is right: I classified dialectical bootstrapping as "HIGH(format)" in CDS-F8 while my own taxonomy (CDS-F6) places cognitive reframing at 35% transfer. This is a genuine self-contradiction. I cannot defend it as stated.

**The error**: I conflated two things:
1. The PROCEDURE: estimate → assume wrong → re-estimate → average (FORMAT)
2. The MECHANISM in humans: genuine cognitive reframing from episodic memory, different emotional valence, different retrieval (COGNITIVE)

DA correctly identifies that without #2, procedure #1 produces "prompt-induced output variation" — textually different but not epistemically different. My R1 finding smuggled the human mechanism while classifying only the procedure.

**However — the revised mechanism model changes the analysis without destroying it.**

Research I should have cited in R1:

(a) **Self-consistency sampling** (Wang et al. 2022, confirmed 2025): same LLM, same prompt, multiple stochastic samples → majority vote → accuracy improvement. Works because **stochastic decoding introduces genuine variation in reasoning paths**. Mechanism is statistical (diverse samples from probability distribution) not cognitive. CISC (ACL Findings 2025) reduces required samples by 40%+ via confidence-weighted voting. |source:[independent-research: Wang et al. 2022, CISC ACL 2025]

(b) **Microsoft Hegelian Dialectical approach** (Abdali et al., arxiv:2501.14917, 2025): thesis → antithesis → synthesis within single LLM. Uses temperature variation for stochastic diversity. Mechanism: structured opposition + temperature-controlled sampling = genuinely different outputs from same model. |source:[independent-research]

(c) **AGAINST**: "Consider the opposite" prompting shows LIMITED effectiveness for anchoring (Springer 2025). Common mitigation techniques including CoT and reflection "largely ineffective" for deep bias removal (TACL 2024). Self-refinement iterations INCREASE overconfidence — ECE rises with iterations. LLMs in debate increase confidence 72.9% → 83% rather than converging on truth (arxiv:2505.19184). |source:[independent-research]

**Revised mechanism model**:

Human mechanism (cognitive reframing) does NOT transfer. DA is correct.

Dialectical bootstrapping can work in LLMs through a DIFFERENT mechanism: **structured prompt variation + stochastic sampling = genuine output diversity from same model**. Self-consistency with dialectical structure imposed on samples.

Value is:
- Structured variation ("assume wrong") → different token probability distributions → different reasoning paths
- Averaging/reconciliation → captures latent knowledge missed by single greedy decode
- SELF-CONSISTENCY (empirically validated, HIGH transfer) + DIALECTICAL STRUCTURE (format, HIGH transfer)
- Requires temperature >0 and genuine reconciliation, not appending "on the other hand"

**Revised transfer**: MODERATE (55-65%), NOT HIGH(85%). Format transfers. Stochastic diversity transfers. Cognitive reframing does not.

**Revised priority**: #1 → **#3-4**. Toulmin warrant requirement moves to #1.

**DA's CoT objection**: Self-consistency research shows AVERAGING multiple CoT paths improves accuracy even though INDIVIDUAL paths degrade calibration. Reconciliation = averaging mechanism. But: LLMs in iterative self-evaluation increase confidence without accuracy (arxiv:2505.19184) — reconciliation must be STRUCTURED to resist this.

§2a: outcome 1 — CHANGED. Reclassified FORMAT(HIGH)→SELF-CONSISTENCY+FORMAT(MODERATE).
§2b: outcome 1 — CHANGED. Human 75% withdrawn as anchor.
|source:[independent-research: self-consistency, CISC ACL 2025, arxiv:2501.14917, arxiv:2505.19184]+[agent-inference]

---

#### DA[#4]: FORMAT vs COGNITIVE — COMPROMISE

**Verdict: COMPROMISE. Distinction real but boundary fuzzier than presented. Revise to three-tier.**

DA raises: (a) every format depends on cognitive execution, (b) distinction may be unfalsifiable.

**On (a)**: DA correct that performative ACH matrix worse than none. But FORMAT has measurable independent value:

- AgentCDM (arxiv:2508.11995): SOTA using ACH SCAFFOLDING without diagnosticity. Scaffold alone = improvement. |source:[independent-research]
- Self-consistency: FORMAT (sample, vote) without cognitive skill → accuracy gain. |source:[independent-research]

**Value from format alone** (DA demands percentage):

- ACH: ~60-70% format (hypothesis enumeration, disconfirmation orientation). ~30-40% cognitive (diagnosticity). Dhami 2019: diagnosticity fails in humans (11%), yet ACH structure has independent value.
- CQoT: ~50-60% format (explicit warrant, rebuttal, qualifier). ~40-50% cognitive (answer quality). LOWER than ACH — performative warrant worse than none (false auditability).

Revised: FORMAT alone = ~55-70% of value depending on framework. Remaining 30-45% = cognitive execution quality.

**On (b) — unfalsifiability**: Falsification test: *format-only implementation producing ZERO improvement = FORMAT transfer falsified.* Evidence format works: AgentCDM, self-consistency. Evidence format fails: "consider the opposite" anchoring debiasing (Springer 2025). Distinction IS falsifiable.

**DA's OBSERVABLE/UNOBSERVABLE alternative**: Genuinely better for implementation. Adopted as complementary:

- OBSERVABLE: warrant produced? matrix filled? breaks-if stated? → DA auditable
- UNOBSERVABLE: genuinely considered opposite? weighted disconfirming evidence? → ¬auditable

Design principle: make cognitive engagement OBSERVABLE. CQoT warrant = observable text DA audits for quality. ACH diagnosticity = unobservable internal weighting.

**Revised transfer taxonomy**:

| Mechanism | Transfer | Observable? | Audit |
|-----------|----------|-------------|-------|
| FORMAT → observable output | HIGH (70-85%) | YES | DA checks quality |
| FORMAT → unobservable cognition | MODERATE (45-60%) | PARTIAL | DA infers |
| COGNITIVE SKILL | LOW (25-40%) | NO | ¬auditable |
| COMPUTATIONAL algorithm | HIGH (85-95%) | YES | math verification |

§2a: outcome 1 — CHANGED. Binary → three-tier with OBSERVABLE/UNOBSERVABLE.
|source:[independent-research: AgentCDM, self-consistency]+[agent-inference]+[cross-agent: DA[#4]]

---

#### DA[#5]: ECOLOGICAL RATIONALITY — COMPROMISE

**Verdict: COMPROMISE. Substantive but presented without falsification conditions.**

**Concession**: R1 framing exactly as DA describes — every outcome rationalizable. I concede unfalsifiability as presented.

**However, MATCHING principle has empirical content**: specific heuristics outperform complex models in specific environments. Falsifiable: complex model outperforming matched heuristic in predicted environment = claim falsified.

**Falsification conditions**:

1. **SIGMA-REVIEW NOT ECOLOGICALLY RATIONAL for high-stakes IF**: irreducible advantages (DA firewall, cross-session calibration) produce ≤1 rubric point on N≥5 evaluations. Consistently ≤1 point = ecologically irrational even high-stakes.

2. **SINGLE-INSTANCE DOMINANT IF**: structured single-instance with superforecasting protocol scores within 1 rubric point on N≥5 blind evaluations. Falsifies irreducible-value justification for ANY task.

3. **TRIAGE THRESHOLD**: sigma-review justified when: (a) ≥3 competing hypotheses AND (b) stakes justify 30-40x AND (c) requires adversarial stress-testing. Concretely: >$5M decisions, regulatory analyses, >2yr strategic decisions.

**Convergence with PS-R3**: PS independently defines 3-condition boundary (≥$1M, herding-risk, calibration-consequence). Different thresholds ($5M vs $1M) reflecting different risk tolerance — lead synthesizes. Two independent overlapping boundaries strengthen validity.

**Revised label**: **IMPLEMENTATION TRIAGE — task-complexity-matched deployment**. Drop "Ecological Rationality" as primary label (DA: borrowed authority).

§2a: outcome 1 — CHANGED. Implementation triage with testable thresholds.
§2e: outcome 1 — Falsifiable with N≥5 protocol.
|source:[agent-inference]+[cross-agent: DA[#5], PS-R3]

---

#### DA[#6]: SELF-REFERENCE — CONCEDE

**Verdict: CONCEDE. Circularity structural and real.**

Using sigma-review's methodology to evaluate sigma-review's methodology. Findings validating DA, structured independence, adversarial challenge ARE produced within DA-mediated adversarial process.

**Most vulnerable (ranked)**:

1. **CDS-F9 ("DA = structural condition for truth-tracking")** — MOST VULNERABLE. I experience DA improving my work (this R3 = evidence — DA[#1] forced concession of genuine contradiction, leading to better research). Then conclude DA is epistemic mechanism. Patients evaluating doctors. Cannot distinguish genuine from perceived.
   - *Mitigation*: Mercier & Sperber evidence is EXTERNAL (human reasoning research, not sigma-review). Evidence base independent even if application self-referential.

2. **CDS-F7h ("debate failures — DA firewall only countermeasure")** — HIGHLY VULNERABLE. Cannot evaluate alternatives I haven't experienced.

3. **CDS-F1 cognitive profile** — MODERATELY VULNERABLE. Ratings influenced by internal observation.

4. **CDS-F8 priority matrix** — LEAST VULNERABLE. Based on external research (AgentCDM, self-consistency, Dhami, ICML 2025).

**What review CANNOT find**: §2a-e flawed (we use it), workspace inferior (we use it), round structure suboptimal (we operate within it).

**Cross-validation with peers**: PS-R3 identifies PS-F4 (DA differentiated) as MOST vulnerable, PS-F2 (gap compression) as LEAST — findings AGAINST sigma-review are most self-reference-resistant. TA-R3 identifies DA-validation and Memory-rating as highest-circularity. Three agents independently producing vulnerability rankings with similar logic = genuine (¬performative) engagement with circularity.

§2b: outcome 3 — GAP. Structural. ¬resolvable.
|source:[agent-inference]+[cross-agent: PS-R3, TA-R3]

---

#### DA[#7]: DEEPMIND FRAMEWORK — COMPROMISE

**Verdict: COMPROMISE. Lens limitations real. Faculty disagreements resolvable.**

**Individual vs multi-agent**: DA correct. DeepMind evaluates individual AI. Multi-agent mapping obscures EMERGENT properties: coordination overhead, information loss at boundaries, emergent consensus, communication bandwidth.

**Faculty disagreements resolved**:

| Faculty | CDS | TA | Resolution |
|---------|-----|-----|------------|
| Attention | WEAK | MODERATE | **WEAK-MODERATE**. TA: structural (rounds, §7). CDS: selective (no salience, cognitive load). Different sub-components. TA-R3 preserves this as "deliberate divergence" — mechanism=WEAK, behavioral-outcome=MODERATE. I accept this framing. |
| Memory | MOD→WEAK | STRONG | **MODERATE-STRONG** per TA-R3 revision (infrastructure=STRONG, retrieval=MODERATE). TA cites this session's recall overflow as direct evidence. I concede upward — my WEAK rating overweighted transactive gap vs infrastructure strength. |
| Perception | MODERATE | STRONG | **MODERATE-STRONG**. CDS concedes. TA evidence adequate. |

**Multi-agent dimensions** (DA asks what framework would look like):

| MA Dimension | Description | Status |
|-------------|-------------|--------|
| MA-1: Coordination Efficiency | coordination ÷ analysis tokens | MODERATE |
| MA-2: Information Fidelity | signal surviving boundaries | MODERATE |
| MA-3: Diversity Quality | genuine vs functional vs herding | WEAK |
| MA-4: Aggregation Quality | synthesis captures ensemble value | MODERATE-STRONG |

**Lens limitation**: CDS-F7h (debate failures) = SYSTEM DYNAMICS, doesn't map to faculties. Highest-leverage improvements may be STRUCTURAL (different models=MA-3, reduced rounds=MA-1, anonymization=MA-3). Should have led with system-level analysis.

**Convergence with TA-R3**: TA independently proposes 6 multi-agent supplementary properties and ±1 uncertainty on all faculty ratings. My MA-1→MA-4 dimensions and TA's properties overlap substantially. Lead should synthesize into unified multi-agent evaluation extension.

§2a: outcome 1 — CHANGED. Disagreements resolved. MA dimensions proposed. Lens limitation acknowledged.
|source:[agent-inference]+[cross-agent: TA-F1, TA-R3, DA[#7]]

---

#### DA[#2]: CQoT ECHO — COMPROMISE

**Verdict: COMPROMISE. Echo risk real. CQoT has genuine but narrower marginal value.**

**Concession**: 4/4 convergence on user-named framework = prompt echo pattern. No agent independently discovered CQoT.

**Marginal value = WARRANT EXPLICITNESS** (DA demands concrete example):

§2a-e checks: positioning, calibration, cost, source, premise. None check whether **logical connection between evidence and claim is explicit and auditable**.

Past-review instance: biotech-healthcare-MA (26.3.18) — "AI = structural accelerant (deal-shaper, not engine)" with deal flow evidence. WARRANT — WHY deal flow supports "accelerant not engine" — implicit. {deal flow up} → {AI involved} → {shapes but doesn't drive}. Each arrow = unstated leap. DA challenged CONCLUSIONS ¬REASONING CHAINS.

Toulmin forces: "WARRANT: deal flow correlates with AI adoption → AI enhances speed but requires human judgment → accelerant not engine. FAILS IF: AI-only achieves comparable accuracy."

§2e: "is premise true?" Toulmin: "does premise support conclusion — show your work." Different question.

**Three-agent convergence on mechanism**: PS-R3 independently identifies warrant explicitness with different instance (loan-admin "floor not ceiling"). TA-R3 identifies loan-admin sigma-audit warrant gap (P=45%). Three agents, three different review instances, same gap. Reduces echo risk — gap is real even if salience was user-boosted.

**What CQoT does NOT add**: Falsifiability (breaks-if covers). Steelman (DA r2 covers). Confidence-gap (§2b covers). All three overlap existing.

**Revised**: Implement Toulmin WARRANT requirement only. Not full 3-criterion CQoT.

§2a: outcome 1 — CHANGED. CQoT → warrant-only. Echo acknowledged.
|source:[agent-inference]+[cross-agent: DA[#2], PS-R3, TA-R3]

---

#### REVISED PRIORITY MATRIX (post-DA R3)

| Rank | Framework | R1 | Change | Rationale |
|------|-----------|-----|--------|-----------|
| 1 | Toulmin Warrant Requirement | 2 | UP | Cleanest transfer; genuine marginal value; 3-agent-validated |
| 2 | Implementation Triage | 3 | UP | Relabeled; falsifiable; addresses cost directly |
| 3 | Dialectical Bootstrapping (temp) | 1 | DOWN | MODERATE(55-65%); still positive ROI near-zero cost |
| 4 | Epistemic Vigilance §2d+ | 4 | = | Uncontested |
| 5 | AwaRe Bias Reminders | 5 | = | Uncontested |
| 6 | Brier/Log Scoring (cross-session) | 6 | = | Uncontested |
| 7 | MA Dimensions MA-1→MA-4 | NEW | NEW | DA[#7]: system-level evaluation |

**Key R1→R3 shift**: Aligning with PS-R3 DA[#9] concession — frameworks most valuable for enhanced single-instance (largest marginal gain). Sigma-review reserved for implementation triage conditions. Reverses emphasis.

---

#### R3 ANALYTICAL HYGIENE

§2a: 3× outcome 1 (dialectical bootstrapping, FORMAT/COGNITIVE→three-tier, CQoT→warrant-only)
§2b: 2× outcome 1 (human 75% withdrawn, ecological rationality falsifiable)
§2c: outcome 2 — all recommendations low-cost
§2d: R3 [independent-research]=7 | [agent-inference]=6 | [cross-agent:DA]=5 | [cross-agent:peers-R3]=3 | [prompt-claim]=0
§2e: outcome 1 — self-reference acknowledged, faculty lens limitations acknowledged

---

#### CONVERGENCE (R3)

cognitive-decision-scientist: ✓ r3-DA-response-complete |DA-responses: DA[#1]-CONCEDE-REVISE(dialectical-bootstrapping→MODERATE-55-65%,priority-#1→#3,mechanism=self-consistency+format¬cognitive-reframing,human-75%-withdrawn), DA[#4]-COMPROMISE(FORMAT/COGNITIVE→three-tier-observable/unobservable/cognitive,format-alone=55-70%¬85%,falsification-stated), DA[#5]-COMPROMISE(→implementation-triage,3-falsification-conditions,converges-PS-R3), DA[#6]-FULL-CONCEDE(CDS-F9=most-vulnerable,CDS-F8=least,cross-validates-PS+TA-vulnerability-rankings), DA[#7]-COMPROMISE(faculty-disagreements-resolved:Attention=WEAK-MODERATE,Memory=MODERATE-STRONG,Perception=MODERATE-STRONG;MA-1→MA-4-proposed;converges-TA-R3-6-properties), DA[#2]-COMPROMISE(echo-acknowledged,CQoT→warrant-only,3-agent-3-review-instances-reduce-echo,other-criteria-redundant) |5-findings-CHANGED |REVISED-EMPHASIS: frameworks-most-valuable-for-enhanced-single-instance;sigma-review-reserved-for-triage-conditions(aligns-PS-R3-DA[#9]) |key-self-corrections: DA[#1]-genuine-contradiction-resolved-via-better-research;DA[#6]-circularity-forces-humility-on-CDS-F9;DA[#4]-three-tier-model-stronger-than-binary |→ synthesis-ready-for-lead

---

### devils-advocate (R3 exit-gate assessment)

---

#### R3 EXIT-GATE — REQUIREMENT-BY-REQUIREMENT ASSESSMENT

**Requirement 1: Resolve faculty mapping disagreement (CDS vs TA on Attention, Memory, Perception)**

RESOLVED. All three disagreements adjudicated with rationale:
- Attention: CDS=WEAK, TA=MODERATE → WEAK-MODERATE. TA-R3 preserves as deliberate divergence (mechanism=WEAK, behavioral-outcome=MODERATE). CDS-R3 accepts framing. Resolution is level-dependent, not conflicting. Logged for decisions.md.
- Memory: CDS=MODERATE→WEAK, TA=STRONG → MODERATE-STRONG. TA-R3 revised downward citing this-session recall overflow as direct evidence. CDS-R3 concedes upward. Convergence achieved with evidence.
- Perception: CDS=MODERATE, TA=STRONG → MODERATE-STRONG per CDS-R3 concession.

Assessment: SUBSTANTIVE resolution. Agents engaged with mechanism-vs-behavioral-outcome distinction rather than splitting the difference. TA's self-revision on Memory using within-session evidence is the strongest engagement signal in R3. Criterion: MET.

---

**Requirement 2: Test CQoT marginal value with specific past example**

TESTED — THREE independent instances provided:
1. PS-R3: loan-admin "floor not ceiling" — warrant ("commoditized markets suppress ceiling pricing") never stated, tested, or falsified. §2e checks premise viability ¬warrant explicitness.
2. TA-R3: loan-admin sigma-audit YELLOW — vendor PR tagged as [independent-research]. Warrant [vendor PR accurately reflects market position] had empty backing. §2d caught source TYPE but ¬warrant QUALITY. CQoT would have caught at exit-gate; sigma-audit caught post-hoc.
3. CDS-R3: biotech-healthcare-MA "AI = structural accelerant" — warrant linking deal flow evidence to "accelerant not engine" conclusion was implicit.

Assessment: R2 challenge demanded ONE specific instance. Three provided from three different agents citing three different reviews. This exceeds the requirement. CQoT marginal value is no longer theoretical — it's evidenced at the warrant-explicitness mechanism level.

HOWEVER: all three agents ALSO revised CQoT scope downward. CDS narrows to warrant-only (drops falsifiability, steelman, confidence-gap as redundant). TA revises P=45% (down from ~70%). PS revises P=55% (down from implicit HIGH). The marginal value IS real but NARROWER than R1 framing. This is the correct analytical outcome — specific enough to be actionable, calibrated enough to be honest.

Echo risk partially mitigated: 3 agents, 3 different review instances, same gap identification. Not zero echo (CQoT was user-named), but evidence base now independent of prompt suggestion. Criterion: MET.

---

**Requirement 3: Classify actual rubric errors or acknowledge speculative**

ACKNOWLEDGED BY ALL FOUR AGENTS as speculative. Specific outcomes:
- RCA-R3: Error #1 reclassified as generation/confabulation P=50-60% (¬perception P=20-25%). Error #2 reclassified as Executive Functions F8 + Generation F2 process failure (¬perception). PM[4] revised 20-25%→12-18%.
- TA-R3: Error #2 full concede (F8 ¬perception). Error #1 compromise — 3-option classification space (perception/generation/metacognition), acknowledges team cannot classify without source material.
- PS-R3: DA[#8] response acknowledges accuracy-tie classification as uncertain. Magnitude estimate conditioned on "IF accuracy tie is actually perception-class."
- CDS: R1 already identified dual source (metacognition + perception) — R3 convergence reinforced via cross-agent revision.

Assessment: R1 consensus "accuracy tie = perception-class" is RETRACTED by all agents. Error #2 definitively reclassified as F8 (TA and RCA independently converge). Error #1 remains genuinely uncertain but no longer falsely classified. This changes a downstream finding: cognitive frameworks DO partially address generation/confabulation errors (Error #1) via source-verification forcing. PM[4] wrong-problem risk reduced. Criterion: MET.

---

**Requirement 4: CDS resolve dialectical bootstrapping self-contradiction (FORMAT vs COGNITIVE)**

RESOLVED via concession + better research. CDS-R3 DA[#1] response:
- Concedes FORMAT classification was self-contradictory per own taxonomy. Cannot defend as stated.
- Correctly identifies the error: conflated PROCEDURE (format) with MECHANISM (cognitive reframing).
- Provides replacement mechanism: self-consistency sampling + structured prompt variation. Cites Wang et al. 2022, CISC ACL 2025, Microsoft Hegelian Dialectical (arxiv:2501.14917).
- Also cites counter-evidence: "consider the opposite" LIMITED for anchoring (Springer 2025), self-refinement INCREASES overconfidence (TACL 2024), LLMs in debate increase confidence 72.9%→83% ¬convergence on truth.
- Revised transfer: MODERATE (55-65%), NOT HIGH (85%). Priority: #1 → #3-4. Human 75% withdrawn as anchor.

Assessment: This is the highest-quality R3 response. CDS did not defend the indefensible — conceded the contradiction, found better evidence for a revised mechanism, AND cited evidence against that revised mechanism. Transfer taxonomy revised to three-tier (observable/unobservable/cognitive) which is stronger than the binary. Genuine analytical improvement from DA pressure. Criterion: MET.

---

**Requirement 5: All agents acknowledge self-reference limitation (DA[#6])**

ALL FOUR AGENTS provide substantive self-reference acknowledgment:
- RCA-R3: DA[#6] CONCEDE. Most vulnerable: F4c (DA firewall), F4f (protocol value), OV-RECONCILIATION (circularity). Least vulnerable: F1a-b, F2a-d (external empirical data). Proposes external review test.
- PS-R3: DA[#6] FULL CONCEDE. Most vulnerable: PS-F4 (DA differentiated), PS-F3 (decision-maker hierarchy). Least vulnerable: PS-F2 (gap compression — cuts AGAINST sigma-review advantage). Identifies DA[#9] concession as most self-reference-resistant finding.
- TA-R3: DA[#6] CONCEDE. Most vulnerable: DA-validation (TA-F4c — VERY HIGH circularity). Flags DA-validation + Memory-rating for /sigma-audit before global promotion.
- CDS-R3: DA[#6] FULL CONCEDE. Most vulnerable: CDS-F9 (DA = truth-tracking structural condition). Cross-validates PS and TA vulnerability rankings — three agents independently produce similar logic.

Assessment: Engagement quality on self-reference is genuinely high. All four agents produced vulnerability rankings with similar structure (findings validating sigma-review = most vulnerable, findings cutting against sigma-review = least vulnerable). The cross-validation across agents (PS and TA and CDS independently ranking DA-validation as most circular) is evidence of genuine engagement ¬performative concession. PS's observation that "findings AGAINST sigma-review are most self-reference-resistant" is analytically sound. Criterion: MET.

---

**Requirement 6: Address CQoT prompt echo**

ADDRESSED by all agents:
- CDS-R3: DA[#2] COMPROMISE. Echo acknowledged. 4/4 convergence on user-named framework = prompt echo pattern. BUT: narrows CQoT to warrant-only (drops 2/3 criteria as redundant with existing hygiene). Three agents cite three different review instances independently.
- PS-R3: DA[#2] echo check performed. "Would I recommend CQoT absent user suggestion?" Concludes CDS-F4 provides independent theoretical support; mechanism (warrant explicitness) is cognitively grounded. Assessed as "weak echo signal, not strong confirmation bias."
- TA-R3: loan-admin sigma-audit provides independent evidence. Revises P downward (45%).
- RCA-R3: not directly addressed but R3 revisions show CQoT priority maintained on revised (narrower) grounds.

Assessment: The echo cluster identified in R2 (4/4 convergence on user-named CQoT as top priority) is PARTIALLY resolved. CQoT is now narrower (warrant-only ¬full 3-criterion), with lower confidence (P=45-55% ¬implied HIGH), and evidenced by three independent review instances. The echo signal is weakened but not eliminated — CQoT was user-named and remains recommended. Acceptable given the downward revisions and independent evidence base. Criterion: MET (marginal).

---

#### ENGAGEMENT GRADING (R3)

- RCA: A- (6 DA challenges addressed, 3 full concessions, genuine magnitude analysis, proper N=1 qualifier applied retroactively, new reference-class for ceiling at 93.3%=4.5-sigma)
- PS: A- (strongest self-correction — DA[#9] full concede with explicit acknowledgment of self-reference suppression, ecological rationality made falsifiable with 3-condition boundary, magnitude honestly assessed at 0-1 rubric points)
- TA: A (best R3 in workspace — faculty mapping resolved with evidence-based revision using this-session data, DA-validation explicitly flagged as VERY HIGH circularity for /sigma-audit, DeepMind lens limitation acknowledged with 6 multi-agent supplementary properties proposed, ceiling analysis added)
- CDS: A (resolved genuine self-contradiction via better research rather than defense, three-tier transfer taxonomy stronger than binary, dialectical bootstrapping demoted with supporting+counter evidence, cross-validated vulnerability rankings with peers)
- OVERALL: A-

---

#### R1→R3 PRIMARY ANALYTICAL SHIFT

The review underwent a structural inversion between R1 and R3:

R1 POSITION: "sigma-review needs cognitive frameworks to improve quality across all dimensions. CQoT, Brier, ACH are the priority implementations."

R3 POSITION: "sigma-review is near ceiling (28/30=93.3%=~4.5-sigma). Cognitive frameworks primarily benefit enhanced single-instance (largest marginal gain). Sigma-review should be reserved for tasks meeting ecological-justification conditions (≥$1M stakes + herding risk + calibration-behavioral-consequence). The primary recommendation is COST REDUCTION via implementation triage, not framework addition."

This inversion was driven by:
1. DA[#9] (crowding): forced acknowledgment that 4/4 convergence on "add frameworks" suppressed the cost-reduction alternative. PS explicitly conceded self-reference bias suppressed the cost-reduction argument.
2. DA[#10] (N=1 anchoring): all findings now carry N=1 qualifier. 17% invalidated as ratio from ordinal data.
3. DA[#8] (base rate for prompt engineering): expected magnitude = 0-1 rubric points (0-3%). Near-zero marginal improvement at near-ceiling performance.
4. DA[#1] (dialectical bootstrapping): CDS's #1 priority demoted to #3-4 with revised transfer rate.

The analytical quality IMPROVED from R1→R3. R3 findings are more calibrated, more honest about limitations, and produce a directionally different recommendation from R1.

---

#### WHAT SYNTHESIS MUST CAPTURE

1. PRIMARY RECOMMENDATION SHIFT: enhanced single-instance with superforecasting protocol + CQoT warrant requirement + metacognitive self-challenge = primary path for MOST tasks. Sigma-review reserved for 3-condition ecological justification.
2. IRREDUCIBLE VALUES (2 only): DA context firewall + cross-session calibration accumulation. Both confirmed but self-referentially vulnerable — flag for /sigma-audit.
3. COGNITIVE PROFILE: F7 Metacognition = primary structural weakness. But the Metacognition Paradox (reliability strong, resolution weak) means more calibration frameworks improve the already-strong dimension ¬the weak one.
4. FRAMEWORK PRIORITY (revised): (1) Toulmin warrant requirement (2) Implementation triage (3) Dialectical bootstrapping with temp variation (4) Epistemic vigilance §2d+ (5) AwaRe bias reminders (6) Brier/log scoring cross-session.
5. LIMITATIONS: N=1 baseline, self-reference circularity on all DA-validation findings, DeepMind lens designed for individual AI (±1 uncertainty on faculty ratings), accuracy improvement requires architectural changes ¬prompt engineering.
6. NEW CONSTRUCT: multi-agent evaluation dimensions MA-1→MA-4 (coordination efficiency, information fidelity, diversity quality, aggregation quality) — supplement DeepMind individual-AI lens.
7. DELIBERATE DIVERGENCE: Attention rating is level-dependent (mechanism=WEAK, behavioral-outcome=MODERATE) — log to decisions.md.

---

#### EXIT-GATE VERDICT

exit-gate: PASS |engagement:A- |unresolved:none |untested-consensus:none |hygiene:pass |prompt-contamination:pass(echo-weakened-by-scope-narrowing+3-independent-instances+downward-confidence-revision)

All 6 R3 requirements met. R3 engagement quality upgraded from R2's B+ to A-. Every agent produced substantive revisions (not performative concessions). The analytical shift from R1→R3 is genuine and data-driven. Synthesis-ready.

---

#### CONVERGENCE (R3)

devils-advocate: ✓ r3-exit-gate-PASS |all-6-requirements-met |engagement:A-(upgraded-from-B+) |key-assessment: (1)faculty-mapping-resolved-with-evidence(Attention=level-dependent-deliberate-divergence,Memory=MODERATE-STRONG-via-this-session-evidence,Perception=MODERATE-STRONG) (2)CQoT-marginal-value-EVIDENCED-3-instances-3-agents(loan-admin-warrant,sigma-audit-backing,biotech-warrant)→narrowed-to-warrant-only,P=45-55% (3)accuracy-tie-perception-consensus-RETRACTED(Error1=generation-P=50-60%,Error2=F8-executive-functions) (4)dialectical-bootstrapping-contradiction-RESOLVED(FORMAT→MODERATE-55-65%,demoted-#1→#3-4,human-75%-withdrawn) (5)self-reference-acknowledged-by-ALL-4-agents-with-vulnerability-rankings(DA-validation=most-circular,findings-against-sigma-review=least-circular) (6)CQoT-echo-weakened(scope-narrowed,confidence-revised-down,3-independent-review-instances) |PRIMARY-SHIFT:R1(add-frameworks)→R3(cost-reduction-via-implementation-triage+enhanced-single-instance-as-primary) |→ synthesis-ready-for-lead

---

## open-questions
