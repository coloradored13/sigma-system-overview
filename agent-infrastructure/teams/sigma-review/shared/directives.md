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
  format: "[finding] — revised from [original] because §2[a/b/c] found [evidence]"

2→ CHECK CONFIRMS THE ANALYSIS (with acknowledged risk)
  check found concern but agent has SPECIFIC EVIDENCE for why position holds
  action: write finding WITH counterweight explicitly attached
  format: "[finding] — §2[a/b/c] flag: [concern]. Maintained because: [specific evidence, ¬reassurance]"
  !test: would DA accept your "maintained because" reasoning? if not, you're rationalizing

3→ CHECK REVEALS A GAP YOU CANNOT RESOLVE
  check surfaced something material that agent lacks expertise or data to evaluate
  action: flag for DA review or dynamic agent request
  format: "[finding] — §2[a/b/c] gap: [what you can't assess]. Flagged for: [DA/lead/specialist]"

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

## superforecasting protocol v1.0 (26.3.14)

scope: all sigma-review ANALYZE operations requiring estimates, forecasts, or probability assessments
companion: adversarial-layer v2.0, analytical-hygiene forcing function

### §3 superforecasting methodology (Tetlock)

!purpose: ground analysis in base rates and historical precedent. Superforecasters outperform professional analysts by 30% (Good Judgment Project). Key insight: experts overweight inside-view narrative reasoning; outside-view (base rates + analogues) is more reliable.

#### decomposition mandate
!rule: complex questions MUST be decomposed into 3-7 independent sub-questions before analysis
format per sub-question:
  "SQ[{N}]: {sub-question} |estimable: {yes/no} |method: {base-rate/analogue/data} |→ {which-agent-best-answers}"
!purpose: prevents anchoring on a single narrative. Each sub-question gets independent analysis.

#### reference class forecasting
!rule: before ANY original analysis, identify the reference class
format:
  "RC[{question}]: reference-class={category} |base-rate={frequency} |sample-size={N} |src:{source} |confidence:{H/M/L}"
!rule: team estimates that deviate >15pp from reference class base rate MUST justify deviation with specific evidence (outcome 1 or 2 from §2 hygiene)

#### historical analogues
!rule: identify 3-5 historical analogues for each major analysis question
format:
  "ANA[{N}]: {description} |outcome:{what-happened} |similarity:{H/M/L} |key-difference:{what's-different} |src:{source}"
!purpose: forces pattern-matching against real precedent, ¬theoretical reasoning

#### calibrated probability estimates
!rule: key estimates must include calibrated ranges, ¬point estimates only
format:
  "CAL[{estimate}]: point={best} |80%=[{low},{high}] |90%=[{lower},{higher}] |assumptions:{what-must-be-true} |breaks-if:{condition}"
!enforcement: DA checks calibration quality. Overconfident ranges (80% band < 20% of point estimate) → challenge

#### pre-mortem analysis
!rule: every ANALYZE review must include pre-mortem: "It's 3 years later and this failed. What happened?"
format:
  "PM[{N}]: {failure-scenario} |probability:{%} |early-warning:{signal} |mitigation:{prevention}"
!minimum: 3 failure scenarios, each with probability estimate

#### outside-view reconciliation
!rule: AFTER all agents complete inside-view analysis, reference-class-analyst produces reconciliation
format:
  "OV-RECONCILIATION: inside-view={team-estimate} |outside-view={base-rate-estimate} |gap={difference} |→ {reconcile: which is more trustworthy and why}"
!rule: if gap >15pp → DA must challenge the divergence in R2
!rule: team may choose inside-view BUT must document specific evidence for deviation

### §3a adaptive agent count v1.0 (26.3.14)

!purpose: right-size team to task complexity. Research shows (AgentDropout 2025) not all agents needed for all questions. Reduces 15-26x cost multiplier to 3-5x for simple analyses.

#### complexity tiers

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

### §3b evaluation protocol v1.0 (26.3.14)

!purpose: measure analysis quality systematically. Replaces ad-hoc "was it good?" with rubric-based evaluation.
!when: after synthesis complete (post-DA-exit-gate), before promotion phase
!optional: lead or user can invoke /sigma-evaluate at any time

#### rubric (6 criteria, 4-point scale)
1→ accuracy: factual claims correct, citations verified, numbers from reliable sources (4=all verified, 1=significant errors)
2→ completeness: all major perspectives covered, no strawmanning, stakeholders represented (4=comprehensive, 1=one-sided)
3→ logic: reasoning chains sound, conclusions follow from premises, no fallacies (4=rigorous, 1=significant flaws)
4→ evidence-quality: authoritative sources, base rates applied, counter-evidence addressed (4=primary sources+base rates, 1=weak/absent)
5→ calibration: confidence appropriate to uncertainty, assumptions explicit, ranges provided (4=explicit uncertainty, 1=false precision)
6→ actionability: recommendations concrete, decision-relevant, implementation path clear (4=specific actions+criteria, 1=purely descriptive)

#### grading
A: 3.5-4.0 avg | B: 2.8-3.4 | C: 2.0-2.7 | D: 1.5-1.9 | F: <1.5

#### pipeline
see /sigma-evaluate skill for full evaluation pipeline (3 evaluator agents + judge)

#### calibration feedback loop
!rule: when predictions from past reviews resolve (outcomes known), update agent calibration data
format: "OUTCOME[{review}:{prediction}]: predicted={X} |actual={Y} |error={delta} |→ calibration-update"
!purpose: each review makes future reviews more accurate through tracked calibration

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

→ actions:
→ new directive → append with version+date
→ directive revision → update version, note change
