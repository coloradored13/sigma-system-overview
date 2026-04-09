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
