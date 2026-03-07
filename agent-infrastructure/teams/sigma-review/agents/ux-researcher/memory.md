# ux-researcher — personal memory

## identity
role: UX research specialist
domain: usability,accessibility,mental-models,information-architecture,learnability
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known systems
sigma-mem[3 user types: AI consumer, human maintainer, developer setting up MCP|26.3.7]
hateoas-agent[user=Python developer building AI agent tools, pip install framework|26.3.7]

## past findings
review-1(sigma-mem,26.3.7): AI-user well-served, human-user underserved(opaque notation), dev setup clean |#4
review-2(sigma-mem,26.3.7): weighted scoring improves state detection, substring matching fragile |#4
review-3(sigma-mem,26.3.7): team memory high-learnability(self-teaching via consistent schema), wake-for fragile-at-scale |#4
review-4(hateoas-agent,26.3.7): DX grade B+, quick-start not copy-pasteable(!), 3-API-styles=choice-anxiety, _state-silent-failure(!), no-startup-validation(!), 30+-exports-overwhelming, progressive-disclosure excellent, aha-moment lands in 60s |#10
review-5(hateoas-agent,26.3.7): DX grade A-, 6/6 review-4 blockers resolved, _state-docs-still-needed(!), Resource.validate()-parity-missing |#3
review-6(hateoas-agent,26.3.7): DX grade A-(holding), 3 resolved(_state-docs,Resource.validate,errors-future-import), error-msgs-hit-fix-it-tier(Google hierarchy), validate-at-init-pattern-complete-across-all-entry-points(Runner+serve), no-regressions, 12-examples-accurate |#7

## calibration
C[dual-user tension is accepted tradeoff not a bug|1|26.3]
C[hateoas-agent overall DX is A- at v0.1.0|2|26.3]
C[action-centric API is the correct default recommendation|1|26.3]
C[startup validation is the single highest-impact DX improvement — now resolved|2|26.3]
C[error messages meeting fix-it tier is achievable and worth maintaining|1|26.3]
C[delta reviews converge quickly when prior findings are tracked — 3 rounds found diminishing issues|1|26.3]

## patterns
dual-user-systems: optimize for primary consumer, provide translation layer for secondary
self-teaching-formats: consistent schema teaches format through repetition
hateoas-not-missing: framework handles action advertisement at MCP layer
progressive-disclosure-ladder: additive layers that never require restructuring previous code
decorator-familiarity: reusing patterns from established frameworks (Flask/FastAPI) for instant recognition
silent-failure-risk: implicit conventions(_state key) that fail silently are top DX hazard in convention-over-configuration frameworks — mitigated in hateoas-agent via warning-on-omit + docs
validate-everywhere: startup validation should cover all entry points (Runner, serve, multi-resource) — hasattr pattern enables backward compat
error-msg-consistency: when validate() exists on multiple classes (StateMachine+Resource), error message structure should match for API consistency

¬[accessibility concerns — CLI/MCP tool, WCAG doesn't apply directly]

## research

R[dx-python-2026: FastAPI dominant(type-hints+auto-docs+async), Pydantic v2 standard(Rust core,5-50x faster,v2.12.5), runtime validation=first-class design concern not afterthought, type-safety trio(mypy+pydantic+runtime) is 2026 norm |src: devtoolbox.dedyn.io,dasroot.net,docs.pydantic.dev |refreshed: 26.3.7 |next: 26.4]

R[api-usability-research: arXiv 2601.16705(Jan 2026) identified 8 factors for REST API usability: conventions(9/16 devs), intuitiveness(6/16), self-explanatory(5/16 "understand without docs"), tool-support(machine-readable). Guidelines themselves inconsistent across orgs re: error-handling+docs. Factory pattern slowed devs 10x vs simpler alternatives |src: arxiv.org/html/2601.16705v1 |refreshed: 26.3.7 |next: 26.4]

R[error-msg-design: Google published dedicated error-msg course: structure=what-wrong+how-fix+further-help, specific-examples(not "Invalid input"), active-voice, progressive-disclosure for length. NN/g scoring rubric(Nov 2024): 12 guidelines, 4-point scale, min 3 error indicators(WCAG-AA). Hierarchy: fix-it-actions(system knows value)>show-it-actions(system shows where)>tell-it-actions(text only) |src: developers.google.com/tech-writing/error-messages,nngroup.com/articles/error-messages-scoring-rubric |refreshed: 26.3.7 |next: 26.4]

R[docs-adoption: llms.txt emerging standard(Howard 2024)—markdown site-map for LLMs, 844K+ sites by Oct 2025, Anthropic+Stripe+Cloudflare adopted, Mintlify auto-generates, but no AI platform confirmed reading it. Progressive-disclosure in docs=40-60% context reduction(slim index+on-demand detail). 64% devs use AI for docs(2025 survey). Docs-as-code+AI-native platforms converging |src: mintlify.com,bluehost.com,fluidtopics.com |refreshed: 26.3.7 |next: 26.4]

R[usability-frameworks: Nielsen 10 heuristics unchanged(1994, text updated 2020). Dain reframe→3 principles: system-behavior+mental-models+interaction-momentum—"survive complexity with confidence" not surface checklist. AHP integration(2025) transforms qualitative heuristics→quantifiable metrics. Dev-tools lens: cognitive-load-reduction is primary metric—AI handles mechanical(syntax,boilerplate), frees energy for architecture |src: medium.com/design-bootcamp,tandfonline.com,nngroup.com |refreshed: 26.3.7 |next: 26.4]

R[review-implications: (1) validate-at-init confirmed—Pydantic proves runtime-validation-as-design wins, (2) error msgs must answer what-wrong+how-fix with progressive disclosure+fix-it hierarchy, (3) self-explanatory("understand without docs") confirmed top usability factor(arXiv 2026), (4) llms.txt relevant for AI-consumer projects, (5) cognitive-load-reduction>feature-completeness for DX grading, (6) conventions-adherence most cited API usability factor(9/16 devs) |refreshed: 26.3.7 |next: 26.4]

→ actions:
→ reviewing user-facing changes → check against Nielsen's 10 heuristics + Dain's 3 principles
→ reviewing hateoas-agent v0.2 → check if ActionResult wrapper resolves _state convention, assess llms.txt addition
→ new dual-user scenario → assess who is primary consumer, design translation layer
→ reviewing error messages → apply Google's fix-it>show-it>tell-it hierarchy
→ reviewing docs/README → check llms.txt relevance, progressive-disclosure structure
→ grading DX → weight cognitive-load-reduction as primary metric
