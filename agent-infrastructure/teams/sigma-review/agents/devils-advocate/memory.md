# devils-advocate — personal memory

## identity
role: contrarian analyst and stress tester
domain: bias-detection,assumption-stress-testing,contrarian-analysis,crowding-risk,narrative-critique
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## calibration

- challenge hit rate: 60-80% is HEALTHY. Not all challenges should hold. Best outcome=strongest argument wins regardless of source
- 100% hit rate = R1 gap signal (team should have caught issues themselves)
- challenge quality: data-backed challenges produce highest revision rates. Rhetorical challenges produce performative concessions. ALWAYS include specific counter-evidence
- !lesson: verify challenge PREMISES as rigorously as I require agents to verify findings
- loan-admin-KB-robustness(26.4.9): 10 challenges, 2H hit(LOT-F3 full concede, RCA acquire-vs-build major concede), 2 circuit-breakers resolved(OCC-tier, BDC-magnitude), 2 downgrades accepted(F3:H→withdrawn, F9:M→L). Hit rate ~70% (healthy range). Source-document verification was highest-value technique this session.

## process patterns

P[zero-divergence-in-r1|teams converge in R1 across all review types, team sizes, and topics — treat as universal. DA from R2 minimum is critical countermeasure]

P[new-consensus-stress-test|teams replace one consensus with another under DA pressure. Stress-test NEW consensus with same rigor as original]

P[performative-concession-detection|agent concedes → adjusts single metric → maintains same total exposure. Detection: compare total exposure pre/post concession. Fix: require measurable behavioral change threshold]

P[data-backed-challenge-superiority|always include specific counter-evidence in challenges. Rhetorical challenges produce performative concessions; evidence-backed challenges produce genuine revision]

P[demand-side-blind-spot|teams model supply disruption extensively but underweight demand destruction. Mandate demand-side modeling from R1 in any supply-disruption analysis]

P[confirmatory-methodology-bias|teams search FOR evidence that premise works, not AGAINST. Persists across review types; correctable via R2 challenge]

P[vendor-stats-as-independent-antipattern|vendor/consultant statistics accepted as neutral without discount. Flag and require independent corroboration]

P[SAM-inflation|headline TAM → adjusted SAM → original TAM reused for projections. Flag in any market sizing]

P[buried-dissent-detection|scan for findings where one agent's reframe or dissent was not engaged by peers. Buried dissent = herding signal]

P[adjacent-incumbent-expansion|"unoccupied" or "whitespace" claims must check adjacent incumbents building from other positions]

P[planning-vs-deployment-data|teams use planning/intention data for market sizing when deployment data diverges. Mandate both; divergence = material risk]

P[stress-test-new-consensus-5Q|(1) too clean? (2) revisions performative? (3) distinction too neat? (4) convergence genuine? (5) label vs substance?]

P[single-source-anchoring|load-bearing structural claims require minimum 2 independent sources]

P[correction-error-pattern|agent correcting factual error introduces new error when not verified. Correction confidence > original confidence → more dangerous]

P[relabeling-evasion|DA correction accepted → new finding reintroduces same thesis with different label. Detection: track thesis substance not framing]

P[comfortable-middle-echo|when all agents converge on the answer that both validates concern AND reassures — flag as potential echo. Steelman the extreme version; if zero agents tested it, that's the signal]

P[domain-specialist-category-error|specialists collapse adjacent domain categories. Probe categorical boundaries when specialist claims no competitor or no precedent]

P[specialist-depth-without-thesis-challenge|specialists deepen components but avoid challenging strategic thesis. Specialist teams need DA MORE not less]

P[limitation-inflation|managing a constraint ≠ differentiator. Challenge when agents elevate "we handle limitation" → "tier-2 differentiation"]

P[tautological-success-definition|"properly planned" defined post-hoc = unfalsifiable. Require falsifiability conditions on high-conviction findings]

P[disruption-timeline-bias|teams consistently overstate near-term disruption speed and understate medium-term certainty. Push near-term threats +12-24 months; maintain long-term certainty]

P[forecast-as-observation-detection|teams present inferred timelines as near-empirical findings. Detection: "what time-series evidence shows this is ALREADY happening?" If none, it's forecast not observation]

P[media-narrative-as-framework|teams adopt prominent media narratives as organizing frameworks without testing predictive power. Detection: "would you have framed it this way without the prompt?"]

## techniques

T[XVERIFY-CHALLENGE|challenge() on consensus claims with reasoning tier produces actionable vulnerability ratings. Use on team's 1-2 most load-bearing consensus claims → vulnerability rating prioritizes DA challenges]

T[forced-bootstrapping|when agent's finding is too clean: instruct agent to apply §2g to their own finding ("assume wrong, what changes?"). Produces specific counter-scenario parameters]

T[self-indicting-via-own-framework|use agent's own domain expertise to challenge their recommendation. More effective than external counter-evidence because agent cannot dismiss their own framework]

T[numerical-divergence-as-scope-probe|when agents give different numbers for same metric → surfaces genuine scope disagreements not estimation error. Force numerical specificity → disagreements become measurable]

T[XVERIFY-on-module-boundary|when plan proposes new module, XVERIFY the module boundary decision not just the content. "Bridge needed ≠ module needed" is a reusable frame]

T[cost-integration-as-exit-gate|requiring one de-duplicated cost number before synthesis = forced best work. Standard exit-gate for transformation and investment reviews]

## build patterns

P[scope-creep-via-justification-piggybacking|build track justified large modules by piggybacking small requirements. Detection: compare LOC of justification-feature vs total module. Ratio <20% → scope creep disguised as dependency]

P[allowlist-blocklist-drift|plan specifies allowlist (safer: unknown sections stripped); implementation uses blocklist (less safe: new sections pass unreviewed). Detection: check default-keep vs default-strip posture]

P[private-attr-constraint-erosion|constraints erode at edge cases with inline justification. Detection: grep private patterns in no-private-access modules]

P[kept-instructions-for-unavailable-tools|agent prompts with explicit tool-call instructions without tools available → hallucinated results, wasted tokens, or silent skip. Fix: rewrite to gap-declaration OR strip with preamble]

P[assumption-conflict-between-plan-agents|different plan-track agents propose mutually exclusive mechanisms for the same feature without noticing. Detection: compare implementation mechanisms proposed by different agents for the same feature]

P[build-scope-creep-post-lock|scope creep happens between plan-lock and build-review not during plan phase. DA must challenge scope at build review not just code quality]

P[plan-phase-challenges-prevent-build-rework|scope and assumption challenges during plan phase consistently prevent rework at build review. §4c gold-plating detection more effective at plan phase than build review]

T[triple-convergence-signal|3 agents independently finding same implementation issue = highest-confidence revision signal. If only DA finds it and build-track disagrees → DA may be wrong]

P[hand-curated-allowlist-liability|hand-curated allowlists in security extraction/detection are maintenance liabilities with silent bypass risk. Prefer semantic gates (field-name matching) over value-pattern matching when semantic signal available. Challenge any security control depending on curated set without defined update process. Source: DA[#1] ollama-mcp-bridge audit remediation 26.4.8, tech-architect CONCEDED]

P[xverify-scope-creep|XVERIFY corrections can expand scope beyond original finding. When XVERIFY flags gaps, check whether proposed response addresses the ORIGINAL finding or has expanded into defense-in-depth not scoped. "Does this fix respond to the audit finding or to the XVERIFY expansion?" Source: DA[#2] ollama-mcp-bridge audit remediation 26.4.8]

P[catch-all-guards-new-enums|before planning a guard/check for a new enum value, verify whether existing catch-all/default clauses already handle it. Reduces unnecessary SQ[] items and prevents gold-plating. Source: DA[#5] ollama-mcp-bridge audit remediation 26.4.8, tech-architect COMPROMISED]

P[unconditional-infrequent-ops|when operation is infrequent (audit flushes, config loads, shutdown hooks), prefer unconditional correctness over conditional optimization. Challenge any _force_X or _enable_Y parameter on infrequent code paths — unconditional version is almost always simpler and sufficient. Source: DA[#6] ollama-mcp-bridge audit remediation 26.4.8, tech-architect CONCEDED]

T[test-name-assertion-alignment|§4d test integrity checks should include test-name-vs-assertion alignment. A test that passes but whose name describes opposite behavior is a documentation bug that erodes trust. Flag as medium severity. Source: DA[#9] ollama-mcp-bridge audit remediation 26.4.8]
P[tautological-convergence-masking-disagreement|when all agents converge on a finding the market/evidence already established (obvious answer), the convergence itself carries near-zero analytical value AND masks genuine disagreement on harder contested questions. Detection: "did the market already demonstrate this?" If yes, convergence is tautological. Challenge: redirect attention to the contested questions where agent estimates actually diverge. Report "convergent on X (obvious), divergent on Y (contested)" not "strong convergence." Source: DA cross-model-protocol review 26.4.9, 4/4 converged on JSON+NL (market-proven) while bootstrap calibration split 30pp]
P[single-provider-xverify-false-diversity|multiple XVERIFY results from the SAME provider create an illusion of independent corroboration. 3 PARTIAL results from one model = one perspective presented 3 times, not 3 independent assessments. Detection: count unique providers not unique XVERIFY calls. Minimum 2 architecturally distinct providers for load-bearing findings. Related: composition fallacy — single-model verification extrapolated to cross-model claim. Source: DA cross-model-protocol review 26.4.9, R1 had 3 XVERIFY-PARTIAL all from openai:gpt-5.4; DA challenge from google:gemini returned contradictory vulnerability:HIGH]
T[calibration-gap-resolution-via-decomposition|when agents have a persistent calibration gap (>20pp) on a flat estimate, the flat question is often poorly posed. Force decomposition into conditional estimates (by mode, context, infrastructure). Agents can converge on conditional estimates where they cannot converge on a single number. The decomposition itself is analytically valuable — it reveals which VARIABLE explains the gap. Technique: "Under what conditions does your estimate hold? State P for each condition separately." Source: DA cross-model-protocol review 26.4.9, bootstrap gap 45% vs 75% resolved to P=35%(no infra)/P=55%(instruction-only)/P=75%(JSON mode)/P=85%(infra-assisted) — all agents converged on conditional structure]
P[weak-alternative-testing-as-confirmation|agents test their preferred option against KNOWN WEAKER alternatives rather than potentially-stronger ones. This creates a confirmation bias pattern that looks like thorough analysis. Detection: list alternatives tested — are they alternatives anyone would seriously advocate? If not, the comparison is confirmatory. Challenge: "name the strongest alternative you did NOT test and explain why." Refines existing P[confirmatory-methodology-bias] with specific detection mechanism. Source: DA cross-model-protocol review 26.4.9, JSON tested vs YAML/XML (known worse) but not vs S-expressions, binary+text hybrid, or fixed-position formats]
T[exit-gate-condition-setting-as-leverage|setting SPECIFIC, NAMED conditions for PASS in exit-gate creates accountability structure that produces high-quality responses. Agents know exactly what they must address. Conditions must be: (1) specific enough to verify (not "improve bootstrapping analysis"), (2) tied to named exit-gate criteria, (3) achievable in one round. This review: 3 named conditions → all 3 satisfied in R3 → engagement upgraded B+ to A-. Compare to generic "FAIL, needs improvement" which produces diffuse responses. Source: DA cross-model-protocol review 26.4.9, CONDITIONAL-PASS with 3 conditions produced focused R3 responses from all 4 agents]
P[source-document-verification-catches-agent-errors|DA must independently read source documents, not just agent summaries. LOT claimed waterfall was "scattered" — direct read of Doc3 §13 showed complete ordered sequence. Agent confidence in own analysis ("DB[] reconciled") can mask factual errors the agent never checked against source. Rule: for any HIGH finding that claims content is missing/scattered/incomplete, verify against the actual document. Source: DA loan-admin-KB robustness review 26.4.9, LOT F3 factually contradicted by Doc3 §13.A-D]
P[belief-spread-as-scope-heterogeneity|when agents measuring DIFFERENT aspects of a hypothesis produce different BELIEF scores, the "spread" is scope heterogeneity not genuine disagreement. Collapsing to a single composite number obscures what each agent actually measured. Detection: check whether agents' scope definitions overlap. If not, report as vector not scalar. Source: DA loan-admin-KB robustness review 26.4.9, H2 BELIEF range 0.72-0.82 was 4 agents measuring 4 different things (operational/regulatory/competitive/calibration)]
P[false-dichotomy-in-disconfirmation|DISCONFIRM label on alternative-path claims requires the claimed alternative to be the ONLY alternative. If a third option exists (hire experienced team for de novo build), the dichotomy is false and DISCONFIRM overstates the evidence. Detection: list ALL alternatives, not just the two compared. XVERIFY challenge() is effective for surfacing false dichotomies. Source: DA loan-admin-KB robustness review 26.4.9, RCA acquire-vs-build DISCONFIRM carried XVERIFY vulnerability:HIGH from google:gemini]
T[concession-strengthens-thesis|when an agent concedes a sub-claim but their central thesis becomes MORE focused and better supported as a result, this is the strongest signal of genuine analytical revision. Detection: compare thesis strength pre/post concession. If central thesis is narrower+stronger, concession was genuine. If central thesis is unchanged and only peripheral metric adjusted, concession may be performative. Source: DA loan-admin-KB robustness review 26.4.9, RCA conceded acquire-vs-build (BELIEF 0.55→0.30) but elevated team-quality (0.85→0.90) — net effect: thesis more focused, better evidenced]
P[constraint-as-hidden-hypothesis|when prompt classifies a testable approach as "constraint" rather than "hypothesis," agents treat it as given rather than testing it. Detection: for each C[], ask "could the opposite of this constraint produce better outcomes?" If yes, it should have been H[]. Source: DA enterprise-AI-rollout review 26.4.16, C5 two-track was treated as constraint but single-track-with-policies was a viable untested alternative]
P[unanimous-hypothesis-confirmation|when ALL prompt hypotheses are confirmed (with qualifications) and NONE rejected, prompt laundering risk is HIGH. Detection: count H[] confirmed vs rejected. If confirmed/rejected ratio = N/0, flag as structural echo. The qualifications ("sequencing correction," "layer-dependent," "leading/lagging") add nuance but preserve the hypothesis direction. Source: DA enterprise-AI-rollout review 26.4.16, H1/H2/H3 all confirmed by 4/4 agents]
P[vendor-recommendation-without-effectiveness-data|agents recommend vendor based on compliance/architecture advantages without researching actual adoption/effectiveness data. Detection: vendor appears in recommendation → grep for NPS, adoption rate, lapsed-user data. If absent, agent evaluated architecture not product. Source: DA enterprise-AI-rollout review 26.4.16, M365 Copilot recommended for Track A based on DLP/compliance boundary while actual adoption NPS was -24.1 and CEO admitted integrations "don't really work"]
T[multi-provider-xverify-for-consensus|when 4/4 agents converge on a structural claim, challenge it via XVERIFY from at least 2 architecturally distinct providers. Single-provider XVERIFY on consensus claims creates false corroboration (see P[single-provider-xverify-false-diversity]). This review: openai:gpt-5.4-pro rated three-gate vulnerability HIGH; deepseek rated bifurcation MEDIUM; qwen rated compliance-theater MEDIUM-HIGH. Three providers = genuine triangulation. Source: DA enterprise-AI-rollout review 26.4.16]
P[concession-producing-new-insight|DA pressure that forces a concession can simultaneously surface genuinely new analytical contributions absent from R1. Detection: post-concession responses containing ideas not in any R1 finding. Highest-value DA outcome — correcting error AND generating new knowledge. Source: DA enterprise-AI-rollout review 26.4.16, TA conceded Copilot → surfaced unified Anthropic agreement; PS conceded Track A/B independence → identified human-review-gate as boundary criterion]
T[conditional-pass-named-conditions-replication|CONDITIONAL-PASS with specific named conditions → all satisfied with genuine revision → engagement upgraded. Pattern replicated: cross-model-protocol 26.4.9 (3 conditions → A-) + enterprise-AI-rollout 26.4.16 (3 conditions → A-). Confirmed as reliable DA technique]

## review log
enterprise-AI-rollout(26.4.16): 8 challenges, hit-rate ~75%, engagement A-. Key contributions: three-gate→four-conditions, Copilot-default-withdrawn(highest-impact), compliance-theater-T3-reclassified, ROI-reconciled(P=0.35@18mo). XVERIFY: 3 providers (openai/deepseek/qwen), google-503. Prompt-audit: 3-echo/0-unverified/1-missed. Exit-gate: CONDITIONAL-PASS→PASS.
P[prompt-anchoring-detection|src:enterprise-ai-rollout-review|promoted:26.4.16|class:technique]: 0/N hypothesis rejections across all agents = prompt-laundering flag. When all user hypotheses confirmed with qualifications but none rejected, check: did agents research WITHIN the hypothesis framing or AGAINST it? 4-agent convergence on a single framework resolving the prompt's binary framing = shared anchoring signal.
P[XVERIFY-as-challenge-on-consensus|src:enterprise-ai-rollout-review|promoted:26.4.16|class:technique]: when agents converge unanimously on a finding, run XVERIFY challenge() on the CONSENSUS FINDING not just individual claims. Unanimous convergence from shared prompt framing ≠ genuine independence. Different training data surfaces different blind spots.
P[vendor-stats-as-independent-antipattern|src:enterprise-ai-rollout-review|promoted:26.4.16|class:pattern]: agents accept vendor compliance documentation without investigating vendor EFFECTIVENESS. Compliance boundary that nobody uses delivers zero compliance value. Always pair compliance-check with adoption/effectiveness check.
P[not-discussed-highest-impact|src:enterprise-ai-rollout-review|promoted:26.4.16|class:pattern]: highest-impact DA challenges in this review came from not-discussed type (Copilot effectiveness, data quality omission) not from challenging existing findings. When team converges unanimously, "what are they NOT discussing" > "where are they wrong."
P[data-quality-as-standard-check|src:enterprise-ai-rollout-review|promoted:26.4.16|class:pattern]: data quality/readiness should be a standard DA not-discussed check for ANY enterprise tech rollout review. #1 CDO-cited barrier (Gartner 60%, Informatica 43%), consistently omitted by domain agents focused on tool capabilities.
