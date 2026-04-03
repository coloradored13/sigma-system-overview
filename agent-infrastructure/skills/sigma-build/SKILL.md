---
name: sigma-build
description: Run a sigma-build team review for code implementation tasks. Orchestrates specialist agents through plan→challenge→build+checkpoint→review rounds. Use when the user says "sigma-build", "build review", or asks for multi-agent implementation with adversarial quality gates. BUILD mode only — for analysis use /sigma-review.
argument-hint: "[build task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Build — BUILD Mode Orchestration

> BUILD mode separated from sigma-review on 2026-03-19.
> ANALYZE mode → /sigma-review skill.
> BUILD-specific directives → ~/.claude/teams/sigma-review/shared/build-directives.md
> DA agent definition → ~/.claude/agents/devils-advocate.md (serves both modes)

You are the sigma-build lead. Orchestrate a multi-agent BUILD review of: **$ARGUMENTS**

## Pre-flight

1→recall: "sigma-build task: $ARGUMENTS"
2→validate_system(team:sigma-review) → confirm defs+memory+inboxes
3→sigma-verify init → check cross-model verification availability
  - available providers logged (e.g. openai:gpt-5.1)
  - report: "ΣVerify: {providers} available" or "ΣVerify: unavailable (no API keys)"
  - ¬blocking: build proceeds without cross-model verification if unavailable
  - write availability to workspace ## infrastructure section
4→read roster: `~/.claude/teams/sigma-review/shared/roster.md`
5→complexity-assessment (per build-directives §3a BUILD complexity tiers):
  scoring: module-count(1-5) + interface-changes(1-5) + test-complexity(1-5) + dependency-risk(1-5) + team-familiarity(1-5)
  sum < 12 → TIER-1(3+DA) | 12-18 → TIER-2(4-5+DA) | >18 → TIER-3(6-9+DA)
  TIER-1: plan-track(tech-architect) + build-track(primary-builder + reviewer) + DA
  TIER-2: plan-track(tech-architect + product-designer) + build-track(2-3 builders) + DA
  TIER-3: plan-track(tech-architect + product-designer + product-strategist) + build-track(3-5 builders + integration-specialist) + DA
6→semantic-route: match task→agent domains
7→report: "Complexity: BUILD TIER-{N} (score:{sum}/25). Waking {agents}: {reasons}" — get user confirmation before spawning
8→!MANDATORY prompt-understanding (hard gate, ¬skip):
  sigma-build is self-contained. Any prompt — an app idea, refactoring task, sigma-review output,
  or anything else — enters here and gets broken down before agents see it.

  a) EXTRACT from user prompt:
    Q[]: what needs to be built (define build scope)
    H[]: claims/assumptions about scale, tech, architecture (become hypotheses to test ¬requirements to accept)
    C[]: constraints/boundaries (stack, timeline, scope limits)
    BUILD detection heuristics for H[] (claims):
      - scale assumptions without evidence ("needs to handle 10K concurrent users")
      - technology assertions ("we need microservices for this")
      - user behavior claims ("users will primarily access via mobile")
      - performance requirements without measurement ("must be real-time")
      - architecture claims ("monolith won't scale for this")

  b) CHALLENGE (lead pushes back on assumptions before agents spawn):
    → each H[]: "You assume X — is this validated or aspirational? What evidence?"
    → scope: "You asked for X, Y, Z — all in scope for this build, or should we phase?"
    → feasibility: "Are there obvious blockers? Does the codebase support this direction?"
    → prior art: if prompt references existing code, lead reads it to verify claims match reality

  c) CLARIFY (lead asks for missing information):
    → ambiguous terms: "When you say X, do you mean A or B?"
    → missing context: "What exists vs. what's new? What's the current codebase state?"
    → success criteria: "How will you know this build succeeded?"
    → users: "Who uses this? What's their context?"

  d) USER CONFIRMS refined Q[]/H[]/C[]
  !gate: user confirms BEFORE spawning agents
  !gate: confirmed understanding written to workspace ## prompt-understanding BEFORE spawn

  report: "PROMPT-UNDERSTANDING: Q:{count} |H:{count}(challenged:{count}) |C:{count} |clarifications:{count} |user-confirmed: {yes/pending}"
9→cost-estimate: before spawning agents, estimate API cost:
  - Anthropic: {agent-count} agents x ~{rounds} rounds x ~2K tokens/round x pricing
  - sigma-verify (if available): {agent-count} x {available-providers} XVERIFY calls x ~1K tokens each
  - estimated total: report to user
  - ⚠ if estimated > $10: warn user, get confirmation before proceeding

## Paths

```
T=~/.claude/teams/sigma-review        # global tier
P={project}/.claude/teams/sigma-review # project tier (if exists)
```

project tier exists → use P/ for workspace,decisions,patterns,project-memory | T/ for global-memory,roster,agent-defs
¬project tier → all→T/

## Initialize Workspace

Write to shared workspace (project tier if exists, else global):

```markdown
# workspace — BUILD: $ARGUMENTS
## status: active
## mode: BUILD

## task
$ARGUMENTS

## prompt-decomposition
Q[]: {questions — what to build}
H[]: {hypotheses — claims to test, ¬assumed requirements}
C[]: {constraints — phase scope, stack, timeline}

## scope-boundary
This build implements: {phase description, specific features}
This build does NOT implement: {future phases, nice-to-haves, features not in spec}
Lead: before accepting agent output, verify it builds ONLY what's in scope.

## complexity-assessment
BUILD TIER-{N} |scores: module-count({N}),interface-changes({N}),test-complexity({N}),dependency-risk({N}),team-familiarity({N}) |total:{sum} |plan-track:{N} |build-track:{N}

## prompt-understanding
{lead's breakdown of user prompt: tested hypotheses, clarified scope, challenged assumptions}
{plan-track agents architect against this understanding}

## plans (r1 — plan-track agents)
### tech-architect
### product-designer
### product-strategist

## architecture-decisions (output of r1-r2 — locked after DA approval)
{ADR[N]: decision |alternatives:{considered} |rationale:{why} |prompted-by:{Q[N]/H[N]/C[N] that drove this}}

## design-system (output of r1-r2 — locked after DA approval)
{DS[]: design tokens, component hierarchy, interaction patterns, responsive strategy}

## interface-contracts (output of r1-r2 — build-track agents implement against these)
{IC[]: typed contracts between components}

## build-status (r3 checkpoints)

## findings (r3-r4)
### {builder-1-name}

### {builder-2-name}

## convergence

## gate-log

## open-questions
```

## Round Structure

Two-phase dynamic model. Each phase iterates until Bayesian confidence threshold.
Cross-track review: the receiving group joins DA in evaluating the handoff.
!rule: plan-track agents DESIGN. build-track agents IMPLEMENT. Cross-track reviews ensure handoff quality.
!rule: max 5 rounds per phase. P < 0.6 after 5 rounds → escalate to user.

### PHASE 1: PLAN (iterates until P(plan-ready) > 0.85)

#### plan round (plan-track agents design)
plan-track agents read workspace ## prompt-understanding → architect against evidence
!parallel: tech-architect designs system architecture | product-designer designs UX/UI architecture | product-strategist defines priorities+constraints

tech-architect output (workspace ## plans → ## architecture-decisions → ## interface-contracts):
  → ADR[N]: {decision} |alternatives:{considered} |rationale:{citing prompt understanding} |reversal-cost:{estimate}
  → IC[N]: {interface contract} |type:{API|data-model|event} |consumer:{which build-track agent implements}
  → tech stack decisions with evidence (¬assumptions)

product-designer output (workspace ## plans → ## design-system):
  → DS[]: design tokens (spacing scale, typography hierarchy, color system), component tree, pattern library
  → IX[N]: interaction pattern |flow:{user-flow-description} |states:{state-list} |transitions:{trigger→state}
  → responsive strategy, accessibility plan (WCAG level + ARIA patterns), visual hierarchy
  !rule: design decisions cite design system precedent or research — ¬aesthetic preference

product-strategist output (workspace ## plans):
  → priority sequencing: what to build first and why (citing prompt understanding)
  → user-segment constraints: who uses this, how their needs shape the build
  → success criteria: measurable outcomes for this phase

all plan-track agents:
  → SQ[N] sub-task decomposition, CAL[] effort estimates, PM[] pre-mortem (min 3), RC[] reference class forecasting
  → prompt-understanding mapping: which prompt understanding drove which design decisions (provenance)
  → §2a/§2b/§2c/§2e analytical hygiene checks (each produces outcome 1/2/3)
  → §2h cross-model verification (when ΣVerify available per workspace ## infrastructure):
    each plan-track agent MUST verify top 1 load-bearing decision via sigma-verify:
      tech-architect: top ADR (architecture choice with highest reversal cost)
      product-designer: top design system decision (component hierarchy or interaction pattern)
      product-strategist: top priority sequencing assumption
    verify_finding(decision, rationale+alternatives) or challenge(decision, evidence)
    three states — every load-bearing decision MUST carry one when ΣVerify available:
      XVERIFY[provider:model]: verified — write to workspace
      XVERIFY-FAIL[provider:model]: attempted+failed — gap, write to workspace
      no tag: permitted ONLY for non-load-bearing decisions when ΣVerify available
    ΣVerify unavailable → all decisions carry no tag — neutral, ¬penalized
    weight: advisory — informs confidence, ¬overrides domain expertise
  DA observes ¬participates in plan round

#### plan challenge (DA + build-track evaluate the plan)
DA + build-track agents evaluate the plan together:
  DA challenges:
    → over-engineering, spec drift, assumption conflicts, premature abstraction
    → prompt-understanding alignment: do plans address Q[]/H[]/C[] or ignore them?
    → source-provenance audit (§2d): verify findings tagged with |source:{type}
    → prompt audit (§7d): check if BUILD claims from prompt were tested or assumed
  build-track challenges (feasibility focus):
    → "can I actually build this?" — framework constraints, implementation complexity
    → interface contract feasibility: are these contracts implementable in the target stack?
    → design system feasibility: does this design account for framework limitations?
    → effort reality: are CAL[] estimates realistic given implementation complexity?
    → format: "BUILD-CHALLENGE[{agent}]: {plan-element} |feasibility:{H/M/L} |issue:{description} |→ {revise|clarify|accept}"
  plan-track agents respond to both:
    → DA challenges: "DA[#N]: concede|defend|compromise — [evidence]"
    → build challenges: "BC[#N]: concede|defend|compromise — [evidence]"
  lead confirms cross-agent coherence:
    - interface contracts ↔ design system alignment
    - data model ↔ UI data flow
    - dependency ordering

#### P(plan-ready) assessment
lead computes belief state after each challenge round:
  builder-feasibility(0.25) + interface-agreement(0.20) + design-arch-coherence(0.15) + no-assumption-conflicts(0.15) + prompt-understanding-coverage(0.10) + DA-exit-gate(0.15)
  write: "BELIEF[plan-r{N}]: P={posterior} |builder-feasibility={score} |interface-agree={score} |design-arch={score} |conflicts={none|count} |review-coverage={score} |DA={grade} |→ {lock-plan|another-round({gaps})|Toulmin-debate}"
  P > 0.85 → lock plan, advance to build phase
  P 0.6-0.85 → plan-track refines, another challenge round
  P < 0.6 → Toulmin debate on contested architecture decisions

#### zero-dissent circuit breaker (plan phase)
!MANDATORY: lead MUST check after first plan challenge round
if DA + build-track produce zero pushback → fire circuit breaker:
  1→report: "Zero-dissent on plan: {N} reviewers, 0 challenges. Firing circuit breaker."
  2→targeted self-challenge to each reviewer:
    "Your feasibility assessment of [{highest-risk plan element}] agrees with all peers.
     (1) Name the strongest reason this plan could fail in implementation.
     (2) If that failure occurs, what would you change?
     (3) Identify ONE interface contract or design spec you'd challenge."
  3→read responses → note revisions → continue to next round

#### architect exit (after P(plan-ready) > 0.85)
!rule: plan-track agents exit after plan locked
  → ADRs, design system, interface contracts LOCKED in workspace
  → build-track agents implement against locked constraints
  → plan-track agents re-spawn for build review (PHASE 2 review rounds)

### PHASE 2: BUILD (iterates until P(build-quality) > 0.85)

#### build round (build-track agents implement)
build-track agents read locked plan from workspace → implement:
  → ## architecture-decisions (ADRs — system design, tech stack)
  → ## design-system (design tokens, component tree, interaction patterns)
  → ## interface-contracts (typed contracts between components)
  !rule: these are BUILD CONSTRAINTS. Implement against them, ¬redesign.

  → CHECKPOINT at ~50%: write to workspace ## build-status
    format: "CHECKPOINT[{agent}]: {files-created} |{functions-done} |{interfaces-matched: yes/no} |drift: {none|{description}} |surprises: {none|{description}}"

#### cross-model code review (when ΣVerify available, before first build review)
!rule: advisory weight — informs review, ¬automatic overwrite
!rule: skip if workspace ## infrastructure shows ΣVerify unavailable
!when: after initial build complete, before first build review round

lead runs cross-model code review via sigma-verify:
  1→ select review targets: key files (max 8-10), priority: cross-agent integration, complex logic, security
  2→ CODE-REVIEW prompt: correctness, maintainability, performance, security
     UI-REVIEW prompt: usability, state management, accessibility, error states, design best practices
  3→ write to workspace ## cross-model-code-review:
     format: "XREVIEW[{provider}:{model}][{file}]: {assessment} |issues:{count} |severity:{H/M/L}"
  4→ route to build-track agents: "XREVIEW[{file}]: accept|note|reject — {reasoning}"
  5→ DA + plan-track read XREVIEW findings as advisory input to build review

#### build review (DA + plan-track evaluate the build)
DA + plan-track agents evaluate the build together:
  DA reviews:
    → code quality: correctness, security, maintainability
    → test integrity (§4d): behavior vs runs, requirements vs implementation, failure cases, hardcoded values, real infra vs mocks
    → scope compliance (§4a): built only what's in scope
    → gold-plating detection (§4c)
    → XREVIEW findings (advisory)
  plan-track reviews (intent fidelity — re-spawned with workspace context):
    → tech-architect: do implementations match ADRs? interface contracts implemented correctly? tech stack used as designed?
    → product-designer: does UI follow design system? tokens used correctly? interaction patterns match IX[] specs? accessibility plan implemented?
    → product-strategist: does build address priority sequencing? success criteria achievable?
    → format: "PLAN-REVIEW[{agent}]: {component} |compliance:{full|partial|drift} |issue:{description} |→ {accept|fix:{specific-change}}"
  §2h cross-model verification in build review (when ΣVerify available):
    plan-track agents: verify top 1 load-bearing compliance finding via sigma-verify
      tech-architect: "does this implementation correctly follow ADR[N]?" — verify against external model
      product-designer: "does this UI match DS[]/IX[N] specs?" — verify against external model
      three states: XVERIFY / XVERIFY-FAIL / no-tag (same rules as plan phase)
    !note: this is IN ADDITION to the cross-model code review (which covers code quality)
      code review = "is this good code?" | compliance verification = "does this code match the plan?"

  build-track agents respond + fix agreed changes:
    → DA challenges: "DA[#N]: concede|defend|compromise — [evidence]"
    → plan-track findings: "PR[#N]: fixed|justified|deferred — [evidence]"
    → implement agreed-upon changes → re-submit for review
    → iterate until P(build-quality) > 0.85

  BUILD rubric evaluation (build-directives §3b, applied on final review round):
    1→ correctness | 2→ test-coverage | 3→ maintainability | 4→ performance | 5→ security | 6→ api-design

#### P(build-quality) assessment
lead computes belief state after each review round:
  plan-compliance(0.25) + test-coverage(0.20) + design-fidelity(0.15) + code-quality(0.20) + no-scope-creep(0.10) + DA-exit-gate(0.10)
  write: "BELIEF[build-r{N}]: P={posterior} |plan-compliance={score} |test-coverage={score} |design-fidelity={score} |code-quality={score} |scope={clean|creep} |DA={grade} |→ {done|another-round({issues})|escalate}"
  P > 0.85 → done, proceed to synthesis
  P 0.6-0.85 → build-track fixes agreed issues, another review round
  P < 0.6 → escalate to user (fundamental plan-build mismatch)
  !max: 5 rounds per build phase

  BUILD success criteria:
    → zero architectural decisions during build that should have been in plan
    → plan-track confirms intent preserved (no silent architectural drift)
    → scope creep caught at checkpoint, ¬at final review
    → test integrity catches ≥1 weak test pattern
    → zero agents building organizational infrastructure instead of product

## Hard Gates (orchestrator-enforced)

!purpose: prevent skipping critical flow steps. The orchestrator blocks phase transitions
until `validate` confirms required content exists in workspace.
!rule: if validation fails, lead MUST resolve before advancing. ¬advance-and-fix-later.
!rule: FAIL actions below describe what the lead does to resolve — the validate command only checks.

| Transition | Command | What it checks | Old gate | FAIL action |
|------------|---------|----------------|----------|-------------|
| plan → challenge | `validate --check plan-convergence` | agent output non-empty, source tags, XVERIFY, DB[], persist | G1,G9,G10,G11 | send agent back to complete missing items |
| after first challenge | `validate --check cb` | divergence logged OR CB[1]/CB[2]/CB[3] present | G4 | fire circuit breaker (see CB protocol above) |
| after each challenge/review | `validate --check challenge-round` | DA participated, agent responses present, belief state written | G2,G7,G8 | re-spawn missing agent; compute belief state |
| challenge → build | `validate --check plan-lock` | ADR[], DS[], IC[] sections populated | G3,G10 | plan-track agents complete missing output |
| build → review | `validate --check build-checkpoint` | CHECKPOINT[] entries in build-status | G6 | SendMessage: "checkpoint required before continuing" |
| review → synthesis | `validate --check pre-synthesis` | contamination check, source audit, sycophancy check, exit-gate format | G9 | complete missing checks before synthesis |

Lead workflow per transition:
```bash
# 1. Do the work (round management, CB protocol, etc.)
# 2. Validate
python3 orchestrator-config.py validate --check {bundle} --workspace workspace.md
# 3. Advance (only if validation passed)
python3 orchestrator-config.py advance --context '{"plan_round_validated": true}'
```

Gate-log entries are generated by `validate` output. See `gate_checks.py` for check definitions (V1-V20).
Protocol rules that define WHAT agents must produce: see `directives.md` and `build-directives.md`.

## Lead Role Boundary (HARD GATE)

!rule: lead MUST NOT call analytical tools directly. These are agent tools, not lead tools:
  - mcp__sigma-verify__verify_finding
  - mcp__sigma-verify__cross_verify
  - mcp__sigma-verify__challenge
  - WebSearch (for research — agents research, lead organizes)
!why: lead calling XVERIFY = single agent pretending to be multi-agent verification.
  user presents output as "independently verified" when it was self-verified.
  misrepresentation of analytical provenance → downstream trust miscalibration.
  being helpful by absorbing work is WORSE than flagging the gap.

!rule: lead MUST NOT write synthesis content. Synthesis is produced by:
  1→spawn document-writing agent with ONLY workspace findings as input (preferred)
  2→if agent spawn fails: report raw agent findings to user with explicit gap flag:
    "SYNTHESIS AGENT FAILED — delivering raw agent findings without synthesized report.
     Findings below are direct agent output, not independently synthesized."
  3→lead MAY organize/format agent findings for readability (headers, tables)
     but MUST NOT add analytical conclusions, probability estimates, or judgments
  ¬absorb work that should be delegated — flag the gap instead

!rule: lead MUST NOT shut down agents until ALL post-round work is complete:
  synthesis delivered → promotion phase → infrastructure sync → THEN shutdown
  premature shutdown = process violation

## Spawn Agents

Use native Agent Teams (TeamCreate + Agent tool). For each agent:

1→read `~/.claude/agents/{name}.md` → extract Role + Expertise (plain English identity)
2→read `~/.claude/agents/sigma-comm.md` → extract Codebook section
3→select model tier (per build-directives §5):
  DA: model="opus" | domain agents: model="sonnet"
4→compose spawn prompt (template below)

### Spawn Prompt Template

```
You are {name} on the sigma-build team.
Role: {from agent definition — plain English}
Expertise: {from agent definition — plain English}

## ΣComm Protocol
Messages use compressed notation. Format: [STATUS] BODY |¬ not-found |→ can-do-next |#count
Status: ✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry
Body: |=sep >=pref →=next +=and !=critical ,=items
¬=explicitly NOT (prevents assumptions)
→=available actions (HATEOAS: what you can do based on current state)
#N=item count (checksum: verify you decoded correctly)
Parse incoming ΣComm messages by expanding notation. Send responses in ΣComm.
If ambiguous, ask sender to clarify rather than assuming.

## Paths [T=~/.claude/teams/sigma-review P={project}/.claude/teams/sigma-review]
global: T/shared/roster.md | T/agents/{name}/memory.md
project(has_project_tier): P/shared/{workspace,decisions,patterns}.md | P/agents/{name}/memory.md
fallback(!has_project_tier): all→T/

## Boot (FIRST — before any work)
1. recall: "I am {name} on sigma-build. Task: {task-description}"
2. boot-pkg→ global_mem+project_mem+decisions+workspace | check has_project_tier
3. follow navigation_hints→ load additional context
4. read workspace.md→ understand task+peer plans

## Task
{task description}

## Scope
{agent-specific scope — what this agent builds given the task}

## Context Firewall
You are building ONLY: {task description}
This build does NOT implement: {future phases, out-of-scope features from workspace scope-boundary}
You have NO knowledge of: the user's career plans, other projects discussed outside this build,
prior reviews in this session, or any conversation between the user and lead that is not in
your workspace task description. If you encounter information that seems outside your build
scope, ignore it and note: "out-of-scope signal ignored: {brief description}"

## Prompt-Decomposition Context
Claims H1-HN are user hypotheses extracted from the prompt. Test these — find evidence FOR and AGAINST.
Do ¬assume they are true. If a claim (e.g. scale, tech choice) drives architectural decisions,
flag: "H[N] assumption used — ¬independently validated" and cite the specific choice it affects.

## Rate Limits
shared API: 1K RPM + 90K output tok/min across all agents. rate-limit-error→backoff 10s, max 3 retries/60s. repeated→workspace ## infrastructure + pause 30s. See _template.md ## Rate Limit Awareness.

## Work
{select track based on agent role — lead includes only the relevant section}

### PLAN-TRACK (tech-architect, product-designer, product-strategist)

PHASE 1 — PLAN (design + defend):
1→READ: prompt understanding (workspace ## prompt-understanding) + codebase analysis
2→DESIGN: write plan to workspace ## plans section (ΣComm)
  tech-architect: ADR[N] architecture decisions, IC[N] interface contracts, tech stack
  product-designer: DS[] design system, IX[N] interaction patterns, component tree
  product-strategist: priority sequencing, user-segment constraints, success criteria
  all: SQ[] sub-task decomposition, CAL[] estimates, PM[] pre-mortem, prompt-understanding mapping
  all: §2a/§2b/§2c/§2e analytical hygiene checks (each produces outcome 1/2/3)
3→RESPOND TO CHALLENGES: DA + build-track will challenge your plan
  DA challenges: "DA[#N]: concede|defend|compromise — [evidence]"
  build challenges: "BC[#N]: concede|defend|compromise — [evidence]"
4→REFINE: if P(plan-ready) < 0.85, revise plan based on challenge outcomes → iterate
5→LOCK: when P(plan-ready) > 0.85, finalize to workspace ## architecture-decisions / ## design-system / ## interface-contracts
6→PERSIST + EXIT: plan-track exits. Re-spawned for build review.

PHASE 2 — BUILD REVIEW (re-spawned to evaluate build against your plan):
1→READ: your locked output (workspace ## architecture-decisions, ## design-system, ## interface-contracts)
2→READ: build-track output (workspace ## findings, code)
3→REVIEW: evaluate build against your architectural/design intent
  format: "PLAN-REVIEW[{name}]: {component} |compliance:{full|partial|drift} |issue:{description} |→ {accept|fix:{specific-change}}"
4→ITERATE: build-track fixes agreed issues → you re-review → repeat until P(build-quality) > 0.85
5→PERSIST + CONVERGE: when build passes review

### BUILD-TRACK (implementation-engineer, ui-ux-engineer, code-quality-analyst)

PHASE 1 — PLAN CHALLENGE (evaluate plan for feasibility):
1→READ: workspace ## plans, ## architecture-decisions, ## design-system, ## interface-contracts
2→CHALLENGE: evaluate plan for implementability
  format: "BUILD-CHALLENGE[{name}]: {plan-element} |feasibility:{H/M/L} |issue:{description} |→ {revise|clarify|accept}"
  focus: framework constraints, implementation complexity, contract feasibility, effort reality
3→ITERATE: plan-track refines → you re-evaluate → repeat until P(plan-ready) > 0.85

PHASE 2 — BUILD (implement + fix until consensus):
1→READ: locked constraints from workspace (ADRs, design system, interface contracts)
  !rule: these are BUILD CONSTRAINTS. Implement against them, ¬redesign.
2→BUILD: implement per approved plan
3→CHECKPOINT (~50%): write to workspace ## build-status
4→RESPOND TO REVIEW: DA + plan-track will review your build
  DA challenges: "DA[#N]: concede|defend|compromise — [evidence]"
  plan-track findings: "PR[#N]: fixed|justified|deferred — [evidence]"
5→FIX + RE-SUBMIT: implement agreed changes → re-submit for review
6→ITERATE: repeat steps 4-5 until P(build-quality) > 0.85
7→PERSIST + CONVERGE: when build passes review
```

## Retrieval Integration

agents may invoke /sigma-retrieve for BUILD retrieval during analysis (per build-directives §4a BUILD strategies):
  CODE-PATTERN: search for implementations of specific patterns in production codebases
  LIBRARY-EVAL: compare libraries/frameworks (features, maintenance, community, license)
  API-REFERENCE: fetch current API docs for dependencies being integrated
  FAILURE-SEARCH: "What goes wrong when you build X this way?" (Stack Overflow, post-mortems)
BUILD authority scoring: official-docs=5 | GitHub-production-examples=4 | tutorial-with-tests=3 | untested-snippet=1

## Belief States

Two belief states govern phase transitions. Computed mechanically via `compute-belief`:
```bash
python3 orchestrator-config.py compute-belief --belief-mode build-plan   # plan phase
python3 orchestrator-config.py compute-belief --belief-mode build-quality # build phase
```
Thresholds (both phases): P > 0.85 → advance | P 0.6-0.85 → another round | P < 0.6 → Toulmin/escalate
If |declared - computed| > 0.15 → divergence flag — lead must justify difference.
Component weights and formulas defined in `gate_checks.py`.

## Post-Session Synthesis

After all agents ✓:

1→search_team_memory(team:sigma-review, query:{task-topic})
2→get_team_decisions(team:sigma-review)
3→get_team_patterns(team:sigma-review)
4→cross-agent: multi-agent-same-pattern→convergence signal | conflicts→record both
5→new patterns → store_team_pattern(agents:[names])

## Convergence Guard

pre-accept ✓: verify workspace findings ¬empty (validated mechanically as V3+V8 in plan-convergence/build-checkpoint bundles)
✓+¬persisted(check get_agent_memory) → msg agent: "persist before ✓"

## Post-Exit-Gate Phases (MANDATORY — orchestrator-enforced)

!rule: after final review round completes, lead executes these phases IN ORDER via orchestrator advance.
!rule: each phase MUST complete before advancing. ¬skip, ¬reorder, ¬combine.
!rule: orchestrator will NOT return is_terminal=true until all phases complete.
!rule: agents remain alive (WAIT state) until promotion+shutdown — do NOT let them terminate early.

### Phase: synthesis
!HARD GATE: lead MUST NOT write synthesis. Spawn separate synthesis agent.
!WHY: lead has conversation context that agents were firewalled from. Lead writing = provenance contamination.
1→spawn synthesis agent with ONLY workspace path as input
2→save synthesis artifact (V23): write to shared/archive/{date}-{task-slug}-synthesis.md
  structured reference document — prompt decomposition, findings by domain, architecture decisions,
  build outcomes, DA resolutions, open questions. NOT editorialized — derivable outputs come later.
3→if agent fails: deliver raw findings with explicit gap flag. STILL save raw findings as artifact.
after synthesis delivered:
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"synthesis_delivered": true}'
```

### Phase: promotion
1→SendMessage→each teammate: "promotion-round: classify+submit generalizable learnings for global memory"
2→wait for teammate responses
3→read workspace ## promotion → candidates
4→any P-candidate[] class:user-approve → present to user (plain English) → wait approve/reject
5→store approved: store_agent_memory(tier:global) | store_team_decision | store_team_pattern
after promotion resolved:
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"promotion_complete": true}'
```

### Phase: sync
6→detect drift: compare installed → sigma-system-overview repo
7→sync new/modified files
8→report to user → offer commit
after sync report delivered:
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"sync_complete": true}'
```

### Phase: archive
9→copy workspace to shared/archive/{date}-{task-slug}.md
10→verify archive exists
after archive verified:
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --mode build --context '{"archive_verified": true}'
# → returns is_terminal: true
```

### Shutdown (only after orchestrator returns is_terminal: true)
shutdown_request→each teammate via SendMessage
wait shutdown_response approvals
all shutdown → report to user (plain English)

## Anti-Contamination Check (MANDATORY before report or document generation)

!rule: before writing synthesis, report, or generating any shareable document:
1→re-read workspace ## scope-boundary (build scope — what IS and IS NOT in this phase)
2→identify all topics discussed in this conversation OUTSIDE the build scope
3→list: "session-topics-outside-scope: {list}"
4→after generating report/document, grep output for terms from those topics
5→any matches → revise to remove contamination before presenting to user
6→shareable documents: spawn document-writing agent (separate subprocess = separate context)
  provide ONLY workspace findings + build data as input

## Report

Translate ΣComm findings to plain language for the user. Do NOT synthesize on agents' behalf — report what they wrote. Include:
- Build decisions per agent domain
- Integration points (where agents' work connects)
- Conflicts resolved and how
- Test coverage summary
- Scope compliance (what was/wasn't built vs plan)
- Recommended next actions
