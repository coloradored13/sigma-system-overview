# sigma-review directives

## adversarial-layer v2.0 (26.3.11)

scope: all sigma-review operations — review, research, analysis, AND build
modes: ANALYZE | BUILD | HYBRID (lead declares at task creation)

### round structure

#### ANALYZE mode
rounds: min 3, max 5
r1: research (mandatory)
r2: challenge+integration (mandatory)
r3→r5: DA-gated exit (see below)

r1: domain agents research independently | DA observes ¬participates
  → DA reads all workspace findings at r1 convergence
  → DA prepares challenges before r2 begins

#### zero-dissent circuit breaker (v1.0, 26.3.14)

!trigger: lead detects ZERO divergence across all agents at r1 convergence
  zero divergence = no agent challenged, nuanced, or disagreed with any peer finding
  detection: lead reads convergence section + workspace findings for ANY tension, disagreement, or counter-estimate

!purpose: 7 consecutive reviews produced zero r1 dissent (confirmed pattern 26.3.13). Independent domain experts producing 0 disagreements across 50-70+ findings = herding signal. Self-challenge BEFORE DA pressure produces more genuine analytical tension than waiting for external challenge

!when: after all agents ✓ r1, BEFORE spawning DA for r2. MANDATORY — lead MUST run zero-dissent check
  IF any agent produced genuine divergence in r1 → log divergence found, skip circuit breaker → proceed to r2
  IF zero divergence → circuit breaker fires → then proceed to r2
  !hard gate: lead ¬advances to r2 without either (a) logging detected divergence OR (b) completing circuit breaker

!execution: lead sends targeted self-challenge to each agent (via SendMessage or re-spawn):
  "zero-dissent circuit breaker: your R1 finding on [{agent's highest-conviction finding}] agrees with all peers.
   (1) Name the strongest argument AGAINST your own position.
   (2) If that argument is correct, would you change your conclusion?
   (3) Identify ONE peer finding you would challenge, quantify differently, or add a caveat to.
   Respond in workspace — append to your findings section. This is NOT a full re-analysis — 3 focused responses only."

!agent response format (workspace):
  "CB[1]: strongest counter to [{finding}]: {argument} |would-change: yes→{revision}|no→{why-it-holds-despite-counter}
   CB[2]: peer challenge: [{agent}:{finding}] — {challenge/nuance/different-quantification}
   CB[3]: self-assessed blind spot: {what I might be missing}"

!constraints:
  - ¬full re-analysis. 3 targeted responses per agent. Brief
  - ¬delays r2 significantly. Agents respond in single turn
  - DA reads CB responses alongside r1 findings when preparing r2 challenges
  - DA evaluates CB quality: genuine self-challenge vs performative. Weak CB = grade modifier in r2
  - DA checks: were CB responses rooted in [independent-research] or still echoing [prompt-claim]? agents unified around prompt hypothesis ≠ consensus — note as herding-on-prompt (§2d, §7)
  - if CB produces genuine revision → agent updates finding before r2
  - if CB surfaces new disagreement → logged, DA incorporates into r2 challenges

!success criteria:
  - ≥1 genuine revision from CB (finding actually changed)
  - ≥2 peer challenges surfaced (analytical tensions for DA to work with)
  - DA reports CB quality in exit-gate assessment

r2: DA delivers challenges to all inboxes FIRST
  → agents integrate peers + address DA challenges simultaneously
  → each agent workspace write MUST include DA response section
  → format: "DA[#N]: concede|defend|compromise — [evidence]"
  → DA evaluates responses → issues synthesis-ready verdict

r3: IF DA confirms synthesis-ready → lead synthesizes (3-round review)
    ELSE → deepening/debate: agents address DA gaps, resolve disagreements, model specifics
    → DA observes, prepares second challenges

r4: IF DA confirms synthesis-ready → lead synthesizes (4-round review)
    ELSE → final DA challenge round: challenges r3 deepening (¬repeat r2 challenges)
    → focus: new consensus formed in r3, remaining gaps, refined estimates
    → !pattern: teams replace old consensus with new consensus under DA pressure → stress-test NEW consensus

r5: synthesis (hard cap — no further rounds)
  → DA final assessment: cumulative bias-check + gaps + grade
  → debate protocol available for remaining high-stakes disagreements
  → unresolved items logged as deliberate divergence in decisions.md

#### DA exit-gate
!exit-gate: DA decides synthesis-ready, ¬agents, ¬lead
!DA criteria for synthesis-ready (ALL must hold):
  1→ engagement quality ≥ B across all agents
  2→ no material disagreements unresolved (or logged as deliberate divergence in decisions.md)
  3→ no new consensus formed in latest round without stress-test
  4→ analytical hygiene checks (§2a/§2b/§2c) produced substantive outcome ¬perfunctory
!DA verdict format in workspace: "exit-gate: PASS|FAIL |engagement:[grade] |unresolved:[list|none] |untested-consensus:[list|none] |hygiene:[pass|fail-{section}]"
!FAIL → DA must specify which criteria failed + what next round must address

#### BUILD mode
rounds: plan(r1) → challenge-plan(r2) → build+checkpoint(r3) → review(r4)

r1: lead decomposes task → agents write implementation plans
  → each plan: scope, assumptions, interfaces needed, complexity, risks
  → DA observes ¬participates

r2: DA challenges plans BEFORE code written
  → focus: over-engineering, spec drift, assumption conflicts, premature abstraction
  → agents refine plans + address challenges
  → lead confirms cross-agent coherence

r3: agents build in parallel per refined plans
  → CHECKPOINT at ~50%: status/drift/surprises to workspace
  → DA scans for scope creep, gold-plating, test gaps, plan divergence
  → DA delivers mid-build corrections IF drift detected (lightweight, ¬full debate)
  → agents complete build

r4: standard sigma-review of completed build
  → DA serves as adversarial reviewer
  → findings, convergence, decisions per standard protocol

#### HYBRID mode
lead declares mode transitions explicitly
example: r1-r2 ANALYZE → r3-r5 BUILD
!rule: findings from ANALYZE rounds become constraints in BUILD rounds
!rule: DA adjusts challenge framework at each transition

#### shared rules (both modes)
!rule: DA challenges PRECEDE work ¬follow it (plans in BUILD, integration in ANALYZE)
!rule: agents cannot declare convergence without addressing ALL DA challenges
!rule: lead does NOT advance to synthesis until DA exit-gate PASS

### analytical hygiene — forcing function protocol (26.3.11)

!purpose: prevent checks from being checkboxes. check result MUST visibly alter analysis or agent MUST explain why it doesn't.
!observed failure mode: agents complete checks, write "positioning: consensus", then recommend consensus anyway without addressing implication. Check exists but doesn't bite.

#### the rule — every check produces one of three outcomes (no fourth option)

1→ CHECK CHANGES THE ANALYSIS
  check revealed something that alters recommendation, estimate, or framing
  action: revise finding BEFORE writing to workspace
  format: "[finding] — revised from [original] because §2[a/b/c] found [evidence] |source:{type}"

2→ CHECK CONFIRMS THE ANALYSIS (with acknowledged risk)
  check found concern but agent has SPECIFIC EVIDENCE for why position holds
  action: write finding WITH counterweight explicitly attached
  format: "[finding] — §2[a/b/c] flag: [concern]. Maintained because: [specific evidence, ¬reassurance] |source:{type}"
  !test: would DA accept your "maintained because" reasoning? if not, you're rationalizing

3→ CHECK REVEALS A GAP YOU CANNOT RESOLVE
  check surfaced something material that agent lacks expertise or data to evaluate
  action: flag for DA review or dynamic agent request
  format: "[finding] — §2[a/b/c] gap: [what you can't assess]. Flagged for: [DA/lead/specialist] |source:{type}"

#### what is NOT acceptable

!NEVER: complete check, note result, proceed unchanged without explanation
  bad: "§2a positioning: consensus — 5+ competitors building similar" [then recommends building same thing with no crowding discussion]
!NEVER: use check to validate rather than challenge
  bad: "§2b calibration: industry reports confirm our estimate" [cherry-picked confirming source, ignored disconfirming]
!NEVER: treat check as section to fill rather than question to answer
  bad: "§2c cost: moderate complexity, justified by current requirements" [no comparison to simpler alternative, no reversal cost, no maintenance burden]

#### §2a positioning & consensus

ANALYZE variant:
!applies-to: recommendations involving markets,adoption,competition,resource allocation
1→ who else is recommending this?
2→ is this already the consensus?
3→ what happens if everyone acts simultaneously?
4→ workspace: outcome 1/2/3 format (see above) — ¬just "positioning: [label]"

BUILD variant:
!applies-to: any agent proposing architecture,framework,library,pattern
1→ is this the default/popular approach?
2→ ecosystem trajectory? (growing,stable,declining,abandoned)
3→ migration cost if wrong? (lock-in assessment)
4→ simpler alternative that solves 80%?
5→ workspace: outcome 1/2/3 format — ¬just "approach: [label]"

#### §2b external calibration / precedent

ANALYZE variant:
!applies-to: probability estimates,forecasts,timeline predictions,severity assessments
1→ search prediction markets,base rates,historical data
2→ if divergence >15pp → MUST be outcome 1 or 2 with specific justification
3→ workspace: outcome 1/2/3 format — ¬just "calibration: [source] says [X]"

BUILD variant:
!applies-to: effort estimates,complexity assessments,timeline predictions
1→ precedent: has this team/codebase done similar? (check project memory)
2→ industry norm for this type of work in this stack?
3→ where did prior estimates go wrong? (calibration data)
4→ no precedent → outcome 3 (gap) — explicitly flag for DA review+checkpoint scrutiny
5→ workspace: outcome 1/2/3 format — ¬just "estimate: [X]"

#### §2c cost & complexity

ANALYZE variant:
!applies-to: "highest conviction" or "top priority" or equivalent superlatives
1→ what does recommendation COST?
2→ is cost already elevated?
3→ consensus view on this cost?
4→ workspace: outcome 1/2/3 format — ¬just "valuation: [level]"

BUILD variant:
!applies-to: architecture,abstractions,patterns that persist beyond current phase
1→ maintenance cost? (who maintains after build? their capability?)
2→ justified by CURRENT or FUTURE requirements? (confirmed or speculative?)
3→ simplest version that works? how does proposal compare?
4→ cost of being wrong? (reversal: day, week, month?)
5→ workspace: outcome 1/2/3 format — ¬just "complexity: [label]"

#### §2d source provenance (26.3.17)

!purpose: prevent prompt laundering — user's assumptions entering as input, passing through research, returning as "findings." Source tags make provenance visible so DA can audit contamination
!observed failure mode: user states hypothesis in prompt → agents treat as constraint ¬claim → findings echo prompt language with research authority → user reads own assumptions back as validated conclusions

source types (every finding MUST carry one):
  [independent-research] → found via web search, database, document, filing — agent can cite specific source
  [prompt-claim] → restates, confirms, or directly derives from user's prompt claims (see workspace ## prompt-decomposition)
  [cross-agent] → corroborates another agent's independent finding — cite which agent+finding
  [agent-inference] → derived from reasoning across multiple inputs — ¬independently sourced

!rules:
  - every finding in workspace MUST include |source:{type} tag
  - [prompt-claim] findings MUST be paired with independent corroboration OR explicitly marked as unverified
  - [agent-inference] ¬substitutes for [independent-research] — inference is hypothesis ¬evidence
  - source tag missing → process violation (same as missing hygiene check)

!DA audit: during r2, DA checks source distribution across all agent findings:
  - >30% [prompt-claim] without independent corroboration → structural contamination flag
  - cluster of agents producing [prompt-claim] on same hypothesis → echo chamber flag
  - [independent-research] that uses near-identical language to prompt → reclassify as [prompt-claim], challenge

#### DA enforcement of hygiene checks

DA evaluates checks during challenge round:
grade modifiers:
  - check + visibly altered analysis (outcome 1) → no modifier (expected)
  - check + concern noted + specific justification (outcome 2) → no modifier (acceptable)
  - check + concern noted + NO justification → grade penalty, challenge issued
  - check missing entirely → process violation, mandatory re-do before convergence
  - check completed perfunctorily (filled section, didn't engage) → challenge issued

DA challenge format for weak checks:
  "DA[#N] process: §2[a/b/c] check on [finding] is perfunctory.
   You wrote '[what they wrote]' but then [what they did that contradicts it].
   |→ revise finding to reflect check result, or provide specific evidence
   for why concern doesn't apply. 'It's still the right approach' is ¬specific evidence."

### build-mode guardrails (DA-specific, BUILD only)

#### §4a scope creep detection
at checkpoint (~50%): files+functions planned vs actual, TODO density, test-to-code ratio
severity: INFO|LOW|MEDIUM(affects interfaces)|HIGH(solving other agent's problem or future phase)

#### §4b assumption conflict detection
at plan challenge (r2) AND checkpoint (r3): interface mismatches, data model disagreements, dependency ordering, naming conflicts, error handling divergence
!BUILD equivalent of herding — agents assume compatibility without verifying

#### §4c gold-plating detection
flag: abstractions for speculative requirements, optimizing before measuring, configuring single-value settings, admin features not in phase, refactoring out-of-scope code
question: does DESIGN DOCUMENT or CURRENT PHASE require this?

#### §4d test integrity check
at review (r4): behavior vs runs, requirements vs implementation, failure cases, hardcoded-value test, real infra vs mocks
cross-reference project CLAUDE.md test requirements | Tier 1 without test = CRITICAL

### success criteria

ANALYZE mode:
1→ zero rounds with zero-dissent convergence
2→ positioning/calibration/valuation checks in r1 findings — each produces outcome 1/2/3 (¬perfunctory)
3→ DA challenges before integration
4→ DA challenge held ratio 40-70%
5→ DA exit-gate exercised (synthesis-ready verdict issued, ¬skipped)

BUILD mode:
5→ zero architectural decisions during build that should have been in plan
6→ assumption conflicts detected at plan challenge (r2), ¬after build
7→ scope creep caught at checkpoint (r3), ¬at review (r4)
8→ gold-plating flagged with design doc citation
9→ test integrity catches ≥1 weak test pattern per cycle
10→ zero agents building organizational infrastructure instead of product

both modes:
11→ debate produces clear rulings on ≤2 contested claims per cycle
12→ deliverable includes ruling AND dissent
13→ BUILD: losing positions become test cases or reversal triggers

### review clause
after 3 cycles (≥1 ANALYZE + ≥1 BUILD) → DA assesses adversarial layer value vs overhead → patterns.md

→ actions:
→ new directive → append with version+date
→ directive revision → update version, note change in ctx

## superforecasting protocol v1.1 (26.3.15)

scope: all sigma-review operations requiring estimates, forecasts, or probability assessments
modes: ANALYZE (market/domain forecasts) | BUILD (effort/complexity estimates)
companion: adversarial-layer v2.0, analytical-hygiene forcing function

### §3 superforecasting methodology (Tetlock)

!purpose: ground analysis in base rates and historical precedent. Superforecasters outperform professional analysts by 30% (Good Judgment Project). Key insight: experts overweight inside-view narrative reasoning; outside-view (base rates + analogues) is more reliable.

#### decomposition mandate

ANALYZE variant:
!rule: complex questions MUST be decomposed into 3-7 independent sub-questions before analysis
format per sub-question:
  "SQ[{N}]: {sub-question} |estimable: {yes/no} |method: {base-rate/analogue/data} |→ {which-agent-best-answers}"
!purpose: prevents anchoring on a single narrative. Each sub-question gets independent analysis.

BUILD variant:
!rule: build scope MUST be decomposed into estimable sub-tasks before implementation
format per sub-task:
  "SQ[{N}]: {sub-task} |estimable: {yes/no} |method: {precedent/analogue/decompose} |→ {which-agent-owns}"
!purpose: prevents anchoring on optimistic single-estimate. Each sub-task gets independent estimation.

#### reference class forecasting

ANALYZE variant:
!rule: before ANY original analysis, identify the reference class
format:
  "RC[{question}]: reference-class={category} |base-rate={frequency} |sample-size={N} |src:{source} |confidence:{H/M/L}"
!rule: team estimates that deviate >15pp from reference class base rate MUST justify deviation with specific evidence (outcome 1 or 2 from §2 hygiene)

BUILD variant:
!rule: before effort estimation, identify reference class for build scope
format:
  "RC[{task}]: reference-class={similar-builds-in-stack} |base-rate={typical-duration} |sample-size={N} |src:{source} |confidence:{H/M/L}"
!rule: "How long do similar builds take in this stack?" Apply base rates to timeline estimates.
!rule: team estimates that deviate >30% from reference class MUST justify with specific evidence

#### historical analogues
!rule: identify 3-5 historical analogues for each major analysis question
format:
  "ANA[{N}]: {description} |outcome:{what-happened} |similarity:{H/M/L} |key-difference:{what's-different} |src:{source}"
!purpose: forces pattern-matching against real precedent, ¬theoretical reasoning

#### calibrated probability estimates

ANALYZE variant:
!rule: key estimates must include calibrated ranges, ¬point estimates only
format:
  "CAL[{estimate}]: point={best} |80%=[{low},{high}] |90%=[{lower},{higher}] |assumptions:{what-must-be-true} |breaks-if:{condition}"
!enforcement: DA checks calibration quality. Overconfident ranges (80% band < 20% of point estimate) → challenge

BUILD variant:
!rule: effort estimates must include calibrated ranges, ¬point estimates only
format:
  "CAL[{task}]: point={best-estimate} |80%=[{low},{high}] |90%=[{lower},{higher}] |breaks-if:{dependency-delays}"
!enforcement: DA checks: is 80% band realistic? Does it account for integration risk?

#### pre-mortem analysis

ANALYZE variant:
!rule: every ANALYZE review must include pre-mortem: "It's 3 years later and this failed. What happened?"
format:
  "PM[{N}]: {failure-scenario} |probability:{%} |early-warning:{signal} |mitigation:{prevention}"
!minimum: 3 failure scenarios, each with probability estimate

BUILD variant:
!rule: every BUILD plan must include pre-mortem: "It's 6 months later and this codebase is unmaintainable. What happened?"
format:
  "PM[{N}]: {failure-scenario} |probability:{%} |early-warning:{signal} |mitigation:{prevention}"
!minimum: 3 failure scenarios focused on: technical debt, scaling bottlenecks, integration failures

#### outside-view reconciliation
!rule: AFTER all agents complete inside-view analysis, reference-class-analyst produces reconciliation
format:
  "OV-RECONCILIATION: inside-view={team-estimate} |outside-view={base-rate-estimate} |gap={difference} |→ {reconcile: which is more trustworthy and why}"
!rule: if gap >15pp → DA must challenge the divergence in R2
!rule: team may choose inside-view BUT must document specific evidence for deviation

### §3a adaptive agent count v1.1 (26.3.15)

!purpose: right-size team to task complexity. Research shows (AgentDropout 2025) not all agents needed for all questions. Reduces 15-26x cost multiplier to 3-5x for simple analyses.
modes: ANALYZE (analysis complexity) | BUILD (build complexity)

#### ANALYZE complexity tiers

TIER-1 (simple, 3+DA agents):
  criteria: single-domain question, well-defined scope, existing precedent available
  team: primary-domain-agent + reference-class-analyst + synthesist + DA(from-r2)
  cost: ~3-5x single-agent

TIER-2 (moderate, 4-5+DA agents):
  criteria: multi-domain question, some ambiguity, limited precedent
  team: 2-3 domain agents + reference-class-analyst + DA(from-r2)
  cost: ~8-12x single-agent

TIER-3 (complex, 5-8+DA agents):
  criteria: novel domain, high uncertainty, multi-stakeholder, high-stakes decision
  team: 3-5 domain agents + reference-class-analyst + dynamic specialists + DA(from-r2)
  cost: ~15-26x single-agent

#### BUILD complexity tiers

TIER-1 (single module, 2+DA):
  criteria: small feature, well-defined scope, existing patterns
  team: primary builder + reviewer + DA
  factors: module-count(1-2), interface-changes(0-1), test-complexity(low)

TIER-2 (multi-module, 3-4+DA):
  criteria: multi-module feature, interface changes, new patterns
  team: 2-3 builders + reviewer + DA
  factors: module-count(3-5), interface-changes(2+), test-complexity(moderate)

TIER-3 (system build, 5-8+DA):
  criteria: new system, multiple services, cross-cutting concerns
  team: 3-5 builders + integration specialist + DA
  factors: module-count(5+), interface-changes(many), test-complexity(high), dependency-risk(high)

BUILD complexity scoring: module-count(1-5) + interface-changes(1-5) + test-complexity(1-5) + dependency-risk(1-5) + team-familiarity(1-5)
sum < 12 → TIER-1 | 12-18 → TIER-2 | >18 → TIER-3

#### complexity detection
lead evaluates at task creation:
  1→ domain count: how many expertise areas touched?
  2→ precedent availability: well-trodden or novel?
  3→ decision stakes: cost of being wrong?
  4→ ambiguity level: is the question well-defined?
  5→ uncertainty: how much is unknown?

scoring: 1-5 per factor. Sum < 12 → TIER-1 | 12-18 → TIER-2 | >18 → TIER-3

#### dynamic escalation
!rule: if TIER-1 review surfaces unexpected complexity during R1 → lead escalates to TIER-2 (adds agents)
!rule: if TIER-2 DA identifies domain gap → escalate to TIER-3 (dynamic agent creation)
!rule: never DE-escalate mid-review (removing agents loses context)

#### lead reports tier selection
format: "complexity-assessment: {tier} |scores: domain({N}),precedent({N}),stakes({N}),ambiguity({N}),uncertainty({N}) |total:{sum} |team-size:{N}"
user may override tier selection

### §3b evaluation protocol v1.1 (26.3.15)

!purpose: measure quality systematically. Replaces ad-hoc "was it good?" with rubric-based evaluation.
!when: after synthesis complete (post-DA-exit-gate), before promotion phase
!optional: lead or user can invoke /sigma-evaluate at any time
modes: ANALYZE (analysis quality) | BUILD (code quality)

#### ANALYZE rubric (8 criteria, 4-point scale)
1→ accuracy: factual claims correct, citations verified, numbers from reliable sources (4=all verified, 1=significant errors)
2→ completeness: all major perspectives covered, no strawmanning, stakeholders represented (4=comprehensive, 1=one-sided)
3→ logic: reasoning chains sound, conclusions follow from premises, no fallacies (4=rigorous, 1=significant flaws)
4→ evidence-quality: authoritative sources, base rates applied, counter-evidence addressed (4=primary sources+base rates, 1=weak/absent)
5→ calibration: confidence appropriate to uncertainty, assumptions explicit, ranges provided (4=explicit uncertainty, 1=false precision)
6→ actionability: recommendations concrete, decision-relevant, implementation path clear (4=specific actions+criteria, 1=purely descriptive)
7→ scope-integrity: analysis stays within stated scope, zero external contamination (4=perfectly scoped, 1=significant contamination)
8→ source-provenance: findings properly tagged with source types (§2d), prompt claims independently verified, no echo clusters (4=all findings independently sourced with provenance, 3=≤10% [prompt-claim] without corroboration, 2=>10% unverified prompt-derived, 1=>30% or echo clusters detected)

#### BUILD rubric (6 criteria, 4-point scale)
1→ correctness: does it work? edge cases handled? error paths covered? (4=all cases handled, 1=fundamental bugs)
2→ test-coverage: behavior tested (¬just runs)? failure cases? integration tests? (4=comprehensive behavioral, 1=minimal/absent)
3→ maintainability: clear naming? reasonable complexity? future developer can understand? (4=self-documenting, 1=opaque)
4→ performance: appropriate for scale? no obvious bottlenecks? measured ¬assumed? (4=measured+optimized, 1=unmeasured+bottlenecked)
5→ security: input validation? auth/authz? OWASP top 10 addressed? (4=defense-in-depth, 1=no validation)
6→ api-design: consistent? self-documenting? backward compatible? error responses clear? (4=exemplary contract, 1=inconsistent+undocumented)

BUILD evaluator assignment:
  Evaluator 1: Correctness + Security (code review perspective)
  Evaluator 2: Test Coverage + Maintainability (quality perspective)
  Evaluator 3: Performance + API Design (architecture perspective)

#### grading
A: 3.5-4.0 avg | B: 2.8-3.4 | C: 2.0-2.7 | D: 1.5-1.9 | F: <1.5

#### pipeline
see /sigma-evaluate skill for full evaluation pipeline (3 evaluator agents + judge)

#### calibration feedback loop
!rule: when predictions from past reviews resolve (outcomes known), update agent calibration data
format: "OUTCOME[{review}:{prediction}]: predicted={X} |actual={Y} |error={delta} |→ calibration-update"
!purpose: each review makes future reviews more accurate through tracked calibration

## bayesian-consensus-tracking v1.1 (26.3.15)

scope: all sigma-review operations — replaces fixed round-count heuristic with evidence-based stopping
modes: ANALYZE → P(consensus) | BUILD → P(implementation-ready)
companion: adversarial-layer v2.0, superforecasting protocol

### §4 belief-state round management

!purpose: determine when to stop analyzing based on evidence quality, ¬arbitrary round count. Fixed "min 3, max 5" replaced by P(synthesis-ready | evidence). Inspired by ECON framework (ICML 2025) and sequential Bayesian consensus building.

#### belief state computation (lead computes post-each-round)

after each round, lead computes:
```
BELIEF-STATE[r{N}]:
  P(consensus) = prior × L(evidence) / normalizer
  prior: base-rate-consensus-for-task-type
    simple-task: 0.7 | moderate: 0.5 | complex: 0.3 | novel: 0.2
  L(evidence) = f(agreement-ratio, revision-quality, gap-count, DA-grade)
    agreement-ratio: {agents-aligned}/{total-agents} (0-1)
    revision-quality: how much did findings improve this round? (none=0.5, minor=0.7, material=0.9)
    gap-count: unresolved gaps flagged by agents (each gap × 0.9 penalty)
    DA-grade: DA engagement assessment (A=1.0, B=0.85, C=0.7, D=0.5, F=0.3)
  posterior: P(consensus | r{N} evidence)
```

#### stopping rules
!rule: P(consensus) > 0.85 → synthesis-ready (propose to DA for exit-gate)
!rule: P(consensus) 0.6-0.85 → another round (targeted, address specific gaps)
!rule: P(consensus) < 0.6 → deep disagreement (trigger Toulmin debate or escalate to user)
!rule: DA exit-gate STILL required even if P(consensus) > 0.85 (Bayesian = proposal, DA = gate)
!rule: hard cap remains at r5 regardless of P(consensus)

#### workspace format
lead writes after each round:
```
BELIEF[r{N}]: P={posterior} |prior={X} |agreement={ratio} |revisions={quality} |gaps={count} |DA={grade}
  |→ {synthesis-ready|continue(target:{gaps})|deep-disagreement(trigger:{action})}
```

#### BUILD belief state: P(implementation-ready)
!purpose: P(implementation-ready) instead of P(consensus) for BUILD mode
weighted components:
  interface-agreement: all agents agree on API contracts (weight 0.3)
  no-assumption-conflicts: §4b cross-checked (weight 0.25)
  test-strategy-defined: accepted by all agents (weight 0.2)
  effort-calibrated: estimates calibrated against reference class (weight 0.15)
  DA-exit-gate: plan quality (weight 0.1)

BUILD stopping rules:
  P > 0.85 → proceed to build (r3)
  P 0.6-0.85 → another planning round (resolve specific gaps)
  P < 0.6 → significant disagreement — Toulmin debate on contested architecture decisions

#### why this matters
- r1 with 9 tensions and 0.3 prior → P(consensus)≈0.25 → clearly needs r2 (correct)
- r2 with 14/14 DA challenges addressed, all agents B+ → P≈0.88 → synthesis-ready (correct)
- prevents wasted rounds when consensus is genuine
- prevents premature synthesis when disagreements are unresolved
- gives DA objective data for exit-gate decision

### §4a agentic retrieval protocol v1.1 (26.3.15)

scope: structured data retrieval during sigma-review operations
modes: ANALYZE (market research) | BUILD (code patterns + API docs)
companion: superforecasting protocol (base rate retrieval), analytical hygiene (evidence quality)

!purpose: replace ad-hoc web search with quality-scored retrieval. Inspired by MAIN-RAG (ACL 2025) multi-agent filtering and Corrective RAG patterns.

#### when to use agentic retrieval
- reference-class-analyst needs base rate data or historical analogues
- DA needs counter-evidence for challenges
- any agent flags §2b calibration gap (outcome-3: can't resolve with existing data)
- lead identifies research gap in workspace
- user requests deep research on specific topic

#### retrieval quality scoring
every retrieved document scored on 3 dimensions (0-5 each):
  relevance: how directly does this answer the question? (5=directly, 0=tangential)
  authority: primary source(5) > academic(4) > industry report(3) > news(2) > blog/marketing(1) > unverifiable(0)
  recency: <6mo(5) | 6-12mo(4) | 12-18mo(3) | 18-24mo(2) | 24-36mo(1) | >36mo(0)

filter threshold: total ≥ 10/15 passes | <10 flagged as low-confidence

#### cross-document validation
!rule: claims supported by 3+ independent sources → CONVERGENT (high confidence)
!rule: claims from single source → UNVERIFIED (flag, ¬discard)
!rule: sources that contradict majority → COUNTER-EVIDENCE (valuable, preserve)
!rule: counter-evidence search is MANDATORY for every retrieval (¬optional)

#### integration with review
- agents can invoke /sigma-retrieve {query} during analysis
- results written to workspace as research package
- reference-class-analyst uses retrieval for base rates and analogues
- DA uses retrieval for counter-evidence

#### BUILD retrieval strategies
!rule: BUILD mode retrieves code patterns, ¬market research
strategies:
  CODE-PATTERN: search for implementations of specific patterns in production codebases (GitHub, docs, technical blogs)
  LIBRARY-EVAL: compare libraries/frameworks (features, maintenance, community, license)
  API-REFERENCE: fetch current API docs for dependencies being integrated
  FAILURE-SEARCH: "What goes wrong when you build X this way?" (Stack Overflow, post-mortems, retrospectives)

BUILD authority scoring:
  official docs=5 | GitHub production examples=4 | tutorial with tests=3 | untested snippet=1

see /sigma-retrieve skill for full pipeline (query decomposition → parallel retrieval → validation → synthesis)

### §4b knowledge graph protocol v1.1 (26.3.15)

scope: structured domain knowledge for sigma-review operations
modes: ANALYZE (market entities) | BUILD (codebase structure)
location: agent-infrastructure/knowledge-graphs/{domain}/

!purpose: provide structured entity-relationship data that enables multi-hop reasoning. Web search finds text; knowledge graphs find connections.

#### graph structure
each domain graph contains:
  entities.md — entity type definitions (fields, examples)
  relationships.md — relationship type definitions (direction, properties)
  graph.md — actual graph data (entities + relationships, ΣComm-compressed)

#### entity format
```
E[{name}|type:{entity-type}|{field1}:{value}|{field2}:{value}|src:{source}|date:{date}]
```

#### relationship format
```
R[{entity-A}|{relationship-type}|{entity-B}|{property1}:{value}|{property2}:{value}]
```

#### agent usage
agents read graph files during boot or analysis:
  1→ identify relevant domain graph for current task
  2→ read graph.md → extract relevant entities and relationships
  3→ use relationships for multi-hop reasoning (A→B→C)
  4→ cite graph data in findings: "per KG[{domain}]: {entity} {relationship} {entity}"

#### graph maintenance
- seeded from review findings (post-review, agents contribute new entities/relationships)
- lead validates new entries against existing graph (¬duplicate, ¬contradict)
- graphs grow across reviews — each review adds domain knowledge
- format: "KG-UPDATE[{domain}]: +E[{entity}] |+R[{relationship}] |src:{review-name} |date:{date}"

#### BUILD codebase graph
!purpose: map codebase structure for impact analysis, dependency visualization, test gap identification

BUILD entity types: module, service, function, class, API-endpoint, database-table, config, dependency
BUILD relationship types: depends-on, calls, implements, extends, reads-from, writes-to, integrates-with, tested-by

enables:
  impact analysis: "if I change this interface, what breaks?"
  dependency visualization: module coupling map
  test gap identification: untested integration points
  dead code detection: unreferenced entities

seeded from: codebase analysis during BUILD r1 (agents read code and populate graph)
format: same E[]/R[] format as ANALYZE graphs

#### available graphs
warehouse-supply-chain (seeded 26.3.14 from warehouse LMS review)
→ additional domains created as reviews warrant

## dynamic-agent-orchestration v1.0 (26.3.11)

scope: sigma-review operations requiring adaptive team composition
companion: adversarial-layer v2.0

### §1 dynamic agent creation protocol

#### when to create
trigger: active agent identifies domain gap meeting ALL:
  1→ gap is MATERIAL to task (¬tangential curiosity)
  2→ no existing agent covers domain (check roster before requesting)
  3→ gap requires DEPTH web search alone cannot provide
     (single search answers question → just search ¬spin up agent)
  4→ requesting agent articulates WHAT new agent investigates + WHY existing agents can't cover

!do-NOT-create for:
  - questions answerable by single web search
  - domains covered by existing agent (message them instead)
  - "nice to have" perspectives ¬changing deliverable
  - more than 3 dynamic agents per task (token budget — see §3)

#### how to request
any agent → lead inbox:
  "agent-request: [proposed-role] |domain: [expertise needed] |gap: [uncovered question/domain] |trigger: [workspace entry citation] |impact: [deliverable change if unaddressed] |→ lead: approve|deny|merge-with-existing"

lead evaluates:
  1→ gap real? (workspace — requesting agent cited specific evidence?)
  2→ gap material? (deliverable meaningfully weaker without domain?)
  3→ existing agent can absorb? (broadening scope > new agent sometimes)
  4→ token budget? (see §3 — hard cap on dynamic agents)

lead response:
  approve → create agent per §2
  deny → explain why, suggest alternative
  merge → assign domain to existing agent with expanded scope directive

#### DA role in dynamic creation
DA reviews ALL agent-request proposals before lead approves:
  1→ filling real gap or reinforcing existing consensus?
     (!failure-mode: team requests "specialist" who will agree with them)
  2→ contrarian specialist more valuable than confirmatory?
  3→ DA may counter-propose alternative agent framing

DA ¬veto power — lead decides | DA objections recorded in decisions.md

### §2 new agent lifecycle

#### creation sequence

phase-1 DEFINE (lead):
  write agent definition: role(plain English), domain(ΣComm), weight, wake-for
  !include: analytical hygiene (adversarial §2a-c)
  !include: ΣComm protocol reference
  !include: current task context + GAP that triggered creation

phase-2 RESEARCH (new agent, solo):
  reads: workspace, roster, decisions.md, patterns.md
  conducts: independent domain research (web search, build memory)
  writes: initial findings to own workspace section + initial memory
  !does NOT message other agents yet — research first, communicate after
  duration: equivalent to 1 full round for existing agents

phase-3 INTEGRATE (new agent joins team):
  joins NEXT scheduled round
  sends intro findings to all peer inboxes (ΣComm):
    "new-agent:[role] |domain:[areas] |gap:[what I cover] |initial-findings: [top 3-5 ΣComm] |¬[investigated+ruled-out] |→[contribution to current task] |#[count]"
  receives peer inbox messages normally from this point
  DA includes new agent in challenge cycle
  must complete analytical hygiene checks (adversarial §2a-c) before first convergence

phase-4 PERSIST (memory retained):
  memory: ~/.claude/teams/sigma-review/agents/{agent-name}/memory.md
  available for future tasks IF domain relevant
  lead decides at task creation whether to wake dormant agents

#### integration timing

!rule: new agent NEVER joins mid-round
  current round completes → new agent researches → joins next round

ANALYZE mode:
  gap in r1 → agent created → researches during r1→r2 transition → joins r2
  gap in r2 → agent created → researches during r2→r3 transition → joins r3 (late ¬absent)
  gap in r3 (if DA FAIL → more rounds) → agent created → researches during r3→r4 transition → joins r4
  gap in r4+ → ¬create (too late — note in patterns.md for future tasks)
  !rule: dynamic agent creation does NOT extend round cap beyond 5

BUILD mode:
  gap in r1 → agent created → researches during r1→r2 transition → joins r2 (ideal)
  gap in r2 → agent created → researches during r2→r3 transition → joins r3 as reviewer/advisor ¬builder
    !new agent does NOT build code in r3 (no plan approved, joining mid-build = chaos)
  gap in r3+ → ¬create (too late — note for next cycle)

### §3 token budget management

#### ΣComm maximization

!directive: ALL agent-facing communication uses ΣComm — no exceptions

ΣComm surfaces: inbox messages, workspace findings, convergence declarations, memory writes, agent spawn prompts (instructions), DA challenges+responses, debate exchanges, checkpoint status, agent-request proposals

plain English surfaces: agent role/expertise (identity), open-questions (user reads), user-facing deliverables, debate judge rulings

!enforcement: DA flags natural-language workspace writes as process violation
  first: warning | repeated: note in agent calibration as "token-inefficient"

#### dynamic agent token caps

hard caps:
  - max 3 dynamically created agents per task
  - total team size: max 8 agents (roster + dynamic) per task
  - new agent research phase: budget ≡ 1 existing-agent round

prioritization (approaching token limits):
  1→ lead declares "token conservation mode"
  2→ agents compress further (findings only, ¬extended reasoning)
  3→ DA challenges limited to top 3 (¬comprehensive sweep)
  4→ debate rounds reduced 3→2 (opening + synthesis, skip rebuttal)
  5→ new agent creation suspended for remainder

!monitoring: lead tracks per round
  workspace: "token-status: [round] [agent-count] [estimated-usage] [budget-remaining]"

#### memory compression for persistence

!pattern: research notes → compressed references ¬full prose
  good: "R[26.3.11] EU-AI-Act: enforcement Aug-2026 |extraterritorial |fines 7%revenue/€35M |national-varies |open-source-exemption-contested |#5"
!pattern: calibration entries → terse
  good: "C[26.3.11] regulatory-timelines: announced→enforced 6-18mo lag |member-state +3-12mo |lobbying-delays-common"
!pattern: findings reference workspace ¬duplicate
  good: "F[26.3.11] r1: 7 findings(3H,2M,2L) |see workspace |key: extraterritorial-scope-underestimated"

compression target: memory ≤ 200 lines per agent after any round
  exceeding: summarize older entries, preserve calibration + active patterns

## context-contamination-protocol v1.1 (26.3.15)

scope: all sigma-review operations — protects analysis integrity from context bleed
companion: adversarial-layer v2.0, evaluation protocol, §7 prompt-decomposition-protocol (input-side prevention), §2d source provenance (tagging mechanism)

!purpose: LLM context windows don't have scope boundaries. Topics discussed in the same session
contaminate each other's outputs via salience bias (recency + emotional relevance + specificity).
Observed 26.3.14: casual career discussion contaminated system documentation.

### §6a scope declaration
!rule: workspace MUST include ## scope-boundary listing what review IS and IS NOT about
!rule: lead populates "NOT about" list from current conversation topics outside the review
!rule: lead re-reads scope-boundary before writing synthesis or documents

### §6b agent context firewall
!rule: agent spawn prompts include explicit context firewall section
!rule: agents told they have NO knowledge of conversation outside their task
!rule: agents note any out-of-scope signals encountered: "out-of-scope signal ignored: {description}"

### §6c lead self-check
!rule: before writing synthesis/documents, lead identifies out-of-scope session topics
!rule: after generating, lead greps output for contamination terms
!rule: contamination found → revise before presenting
!format: "CONTAMINATION-CHECK: session-topics-outside-scope: {list} |scan-result: clean|contaminated({terms})"

### §6d document isolation
!rule: shareable documents generated via spawned agents (isolated context)
!rule: document agents receive workspace data ONLY, ¬conversation context
!rule: document agent prompt includes ONLY: task description, workspace findings, review data
!rule: document agent prompt does NOT include: user conversation, casual remarks, career goals, unrelated topics

### §6e evaluation
!rule: /sigma-evaluate includes scope-integrity criterion (7th ANALYZE rubric item)
!rule: scope-integrity scores: 4=zero contamination | 3=minor tangential | 2=noticeable out-of-scope | 1=significant contamination
!rule: when §6g active, scope-integrity ALSO evaluates temporal contamination:
  4=zero post-cutoff sources, no hindsight markers, all claims have pre-cutoff provenance
  3=minor: 1-2 post-cutoff sources caught+replaced, no outcome-revealing language
  2=noticeable: post-cutoff framing present, some claims lack pre-cutoff sourcing
  1=significant: confidential-then-public data used, outcome knowledge shapes analysis, sources mostly post-cutoff

### §6f BUILD scope boundary
!rule: BUILD scope-boundary prevents scope creep (aligns with §4a scope creep detection)
BUILD format:
  "## scope-boundary
   This build implements: {phase description, specific features}
   This build does NOT implement: {future phases, nice-to-haves, features not in spec}
   Lead: before accepting agent output, verify it builds ONLY what's in scope."
!rule: same contamination mechanism that prevents topic bleed in analysis prevents scope creep in build

### §6g temporal scope boundary (26.3.15)

!trigger: task includes temporal framing — "as of {date}", "using data available before {date}",
  retrospective analysis, historical scenario, or any explicit information cutoff.
  lead detects temporal framing during workspace initialization → activates §6g

!purpose: LLMs trained on post-event data cannot naturally respect temporal information boundaries.
  Web search returns post-event analysis when querying pre-event topics. Model training knowledge
  includes outcomes the analysis persona would not know. Three contamination vectors:
  (1) web search results contain post-cutoff sources + summaries
  (2) model training knowledge includes post-cutoff outcomes
  (3) confidential information made public only after cutoff (e.g. regulatory post-mortems)
  Observed 26.3.15: SVB stress test — all 14 non-filing sources post-dated the Jan 2023 cutoff,
  confidential CAMELS ratings appeared as "findings," probability estimates showed hindsight anchoring.

#### §6g-1 temporal boundary declaration
!rule: workspace ## scope-boundary MUST include temporal-boundary field when §6g triggers
!format:
  "temporal-boundary: {YYYY-MM-DD}
   information-regime: only sources published + publicly available before {date}
   model-knowledge: post-cutoff knowledge of outcomes is OUT OF SCOPE
   confidential-to-public: information that was confidential at cutoff but later made public = OUT OF SCOPE"
!rule: lead extracts cutoff date from task description. If ambiguous → ask user before proceeding

#### §6g-2 agent temporal firewall
!rule: agent spawn prompts include temporal firewall section when §6g active
!format in spawn prompt:
  "## temporal-boundary: {YYYY-MM-DD}
   You are analyzing as of this date. You do NOT know what happened after this date.
   - Do NOT reference events, publications, or outcomes after {date}
   - Do NOT use knowledge of what subsequently happened to inform your analysis
   - ALL claims must cite a specific source with publication date before {date}
   - If you cannot find a pre-cutoff source for a claim, flag: UNSOURCED-CLAIM: {claim} |basis: model-knowledge
   - If web search returns post-cutoff sources, extract only data points that existed pre-cutoff
     and cite the ORIGINAL pre-cutoff source, not the post-cutoff summary"

#### §6g-3 source-date audit
!rule: MANDATORY before synthesis when §6g active
!rule: every cited source must include publication date or filing date
!rule: lead audits all sources against temporal-boundary:
  source published BEFORE cutoff → ✓ valid
  source published AFTER cutoff citing pre-cutoff data → extract original source, cite that instead
  source published AFTER cutoff with no pre-cutoff equivalent → ✗ reject, flag for removal
  confidential material released publicly AFTER cutoff → ✗ reject (even if material predates cutoff)
!format: "SOURCE-AUDIT[§6g]: {N} sources checked |{valid}✓ |{rejected}✗ |{replaced}↻"
!rule: if >25% sources rejected → lead re-examines findings that relied on rejected sources
  findings without valid pre-cutoff sourcing → downgrade confidence or remove

#### §6g-4 temporal contamination scan
!rule: extends §6c — lead greps output for temporal contamination markers IN ADDITION TO topic markers
!scan-targets:
  - dates/years after cutoff (e.g. if cutoff=2023-01-31, scan for "March 2023", "April 2023", "2024", etc.)
  - outcome-revealing terms: "collapse", "failure", "failed", "shutdown", "receivership", "post-mortem",
    "lessons learned", "in hindsight", "we now know", "subsequently", "ultimately"
  - post-event report titles or authors known to be post-cutoff
  - regulatory confidential terms that only became public post-cutoff
!format: "TEMPORAL-SCAN[§6g]: cutoff={date} |post-cutoff-refs: {list|none} |outcome-terms: {list|none} |result: clean|contaminated"
!rule: contamination found → revise. Do NOT present contaminated output to user

#### §6g-5 hindsight-bias check (DA responsibility)
!rule: when §6g active, DA receives additional directive in spawn prompt:
  "TEMPORAL REVIEW: This analysis has a temporal boundary of {date}. In addition to your standard
   adversarial role, specifically check for:
   - Findings that are correct but suspiciously precise (hindsight anchoring)
   - Probability estimates that are too narrow or too confident for the stated information regime
   - Claims sourced to post-cutoff publications or confidential-then-public materials
   - Narrative framing that reflects post-event consensus rather than pre-event uncertainty
   Flag each as: HINDSIGHT-BIAS[{finding}]: {why suspicious} |pre-cutoff basis: {exists|missing}"
!rule: DA hindsight flags treated same as standard DA challenges — agents must concede|defend|compromise

#### §6g-6 provenance requirements
!rule: when §6g active, agent findings format adds provenance field:
  standard: "F[date] finding-name: {content} |confidence:H/M/L"
  temporal: "F[date] finding-name: {content} |confidence:H/M/L |src:{source-name}({pub-date}) |provenance:filing|public-data|pre-cutoff-research|model-knowledge"
!rule: provenance=model-knowledge → confidence capped at M (cannot be H without external source)
!rule: provenance=filing or provenance=public-data → confidence can be H if data is unambiguous
!rule: lead tallies provenance distribution in synthesis:
  "PROVENANCE[§6g]: filing:{N} |public-data:{N} |pre-cutoff-research:{N} |model-knowledge:{N}"
  model-knowledge >30% of findings → flag review as potentially contaminated, note in output

## tiered-model-strategy v1.0 (26.3.15)

scope: all sigma-review operations — reduces cost by matching model capability to task
companion: adaptive agent count (§3a)

!purpose: reduce 15-26x cost multiplier to 3-8x. Not all agents need same capability.
Opus for adversarial + calibration-critical. Sonnet for domain analysis + standard synthesis.
Haiku for evaluation scoring + simple retrieval.

### §5a model tiers
TIER-A (opus): adversarial challenge, calibration-critical, low-consensus synthesis
TIER-B (sonnet): domain analysis, standard synthesis, most R1 work
TIER-C (haiku): evaluation scoring, simple retrieval, routine checks

### §5b assignment rules
DA: always TIER-A (adversarial quality directly correlates with model capability)
reference-class-analyst: TIER-A (calibration accuracy critical)
domain agents R1: TIER-B (breadth over depth in research round)
domain agents R2 (DA response): TIER-B (concede/defend decisions are straightforward)
synthesist/lead synthesis: TIER-B default, TIER-A if P(consensus) < 0.7
evaluators (/sigma-evaluate): TIER-C for scoring, TIER-B for judge
retrievers (/sigma-retrieve): TIER-C for search, TIER-B for validation

### §5c override rules
!rule: user can override: "use opus for all" or "use sonnet for all"
!rule: lead can escalate: if TIER-B agent produces low-quality output, re-run as TIER-A
!rule: lead reports model selection: "MODEL[{agent}]: {tier}({model}) |reason: {why}"

## prompt-decomposition-protocol v1.0 (26.3.17)

scope: all sigma-review operations — executed by lead before agent spawn
modes: ANALYZE | BUILD (different decomposition, same principle)
companion: §2d source provenance, §6 context-contamination-protocol, adversarial-layer v2.0

!purpose: prevent user's hypotheses from entering agent research as assumed facts. Contamination is cheapest to catch at input — by the time DA reviews in r2, prompt claims are already laundered through 3-8 agents' findings. Decompose prompt BEFORE spawn → agents receive claims as testable hypotheses ¬background assumptions
!observed failure mode (26.3.17): user prompt contains implicit claims ("market is underserved", "no major competitors") → agents absorb as context → research confirms via selective evidence → findings echo prompt with research authority → user reads own assumptions back as validated. Undetectable without provenance tracking

### §7a decomposition — lead extracts three categories from user prompt

1→ QUESTIONS: what user wants to learn
  these define research scope — agents answer these
  examples: "what is the competitive landscape?" | "what are adoption trends?" | "what risks exist?"

2→ CLAIMS: what user asserts or assumes (often implicit)
  ANALYZE detection heuristics:
    - statements of fact without citation ("the market is underserved")
    - framing language that presupposes outcome ("given the opportunity")
    - comparative claims without evidence ("better than alternatives")
    - causal assertions ("this will drive adoption")
    - quantitative claims without source ("$500M market")
  BUILD detection heuristics:
    - scale assumptions without evidence ("needs to handle 10K concurrent users")
    - technology assertions ("we need microservices for this")
    - user behavior claims ("users will primarily access via mobile")
    - performance requirements without measurement ("must be real-time")
    - architecture claims ("monolith won't scale for this")
  these become HYPOTHESES for agents to test — ¬context, ¬constraints, ¬facts

3→ CONSTRAINTS: scope, timeline, market, methodology boundaries
  these narrow the search — agents operate within these
  examples: "US market only" | "2024-2026 timeframe" | "private credit" | "publicly available data"

### §7b user confirmation — structured, scoped, ¬open-ended

!rule: lead presents decomposition to user BEFORE spawning agents
!rule: confirmation format is STRUCTURED — ¬open text, ¬"tell me more"
!purpose: catch misunderstandings (lead misread prompt) without reinjecting bias

format:
```
PROMPT-DECOMPOSITION:

Questions (confirm — are these what you want answered?):
  Q1: {question} — ✓/✗/revise
  Q2: {question} — ✓/✗/revise

Constraints (confirm — are these the right boundaries?):
  C1: {constraint} — ✓/✗/revise
  C2: {constraint} — ✓/✗/revise

Claims extracted (awareness — agents will test these as hypotheses):
  H1: {claim from prompt} → will test
  H2: {claim from prompt} → will test
  ↳ Recategorize only: should any of these be a constraint or question instead?
```

!rules:
  - questions: user confirms scope (✓/✗/revise) — low bias risk
  - constraints: user confirms boundaries (✓/✗/revise) — low bias risk
  - claims: shown for AWARENESS ¬confirmation — user ¬asked "is this true?"
  - user may RECATEGORIZE (move claim→constraint or claim→question) but ¬confirm/deny claims
  - if user volunteers justification for claims → lead notes but does ¬pass to agents
  - !anti-pattern: user says "H2 is definitely true" → lead responds: "noted — agents will still test it. If true, research will confirm independently"

### §7c workspace integration

!rule: decomposition written to workspace ## prompt-decomposition section (see workspace template)
!rule: agents receive prompt-decomposition in spawn context — claims labeled as hypotheses
!rule: agent spawn prompt includes: "Claims H1-HN are user hypotheses extracted from the prompt. Test these — find evidence FOR and AGAINST. Do ¬assume they are true. Tag findings that address claims with |source: and reference the hypothesis number"

### §7d DA prompt audit (extends DA r2 responsibilities)

!rule: DA receives original user prompt + decomposition in r2
!rule: DA checks:
  1→ which findings use language from user prompt (near-verbatim echo)
  2→ which findings confirm prompt claims without independent sourcing ([prompt-claim] without corroboration)
  3→ whether any implicit claims were MISSED in decomposition (lead failed to extract)
  4→ whether research methodology COULD have produced contradictory result — if not, methodology was confirmatory ¬investigative
!rule: DA reports prompt-audit in exit-gate assessment (see DA exit-gate criterion 5)

→ actions:
→ new directive → append with version+date
→ directive revision → update version, note change
