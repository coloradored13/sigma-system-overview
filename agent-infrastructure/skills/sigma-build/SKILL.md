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
  sum < 12 → TIER-1(2+DA) | 12-18 → TIER-2(3-4+DA) | >18 → TIER-3(5-8+DA)
  TIER-1: primary-builder + reviewer + DA
  TIER-2: 2-3 builders + reviewer + DA
  TIER-3: 3-5 builders + integration-specialist + DA
6→semantic-route: match task→agent domains
7→report: "Complexity: BUILD TIER-{N} (score:{sum}/25). Waking {agents}: {reasons}" — get user confirmation before spawning
8→!MANDATORY prompt-decomposition (build-directives §7 — hard gate, ¬skip):
  extract from user prompt:
    Q[]: what needs to be built (define build scope)
    H[]: claims/assumptions about scale, tech, architecture (become hypotheses ¬requirements)
    C[]: constraints/boundaries (stack, timeline, current phase only)
  BUILD detection heuristics for H[] (claims):
    - scale assumptions without evidence ("needs to handle 10K concurrent users")
    - technology assertions ("we need microservices for this")
    - user behavior claims ("users will primarily access via mobile")
    - performance requirements without measurement ("must be real-time")
    - architecture claims ("monolith won't scale for this")
  present structured decomposition to user (§7b format)
  !gate: user confirms Q/H/C BEFORE spawning agents
  !gate: confirmed decomposition written to workspace ## prompt-decomposition BEFORE spawn
  report: "PROMPT-DECOMPOSITION: Q:{count} |H:{count} |C:{count} |user-confirmed: {yes/pending}"

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
BUILD TIER-{N} |scores: module-count({N}),interface-changes({N}),test-complexity({N}),dependency-risk({N}),team-familiarity({N}) |total:{sum} |team-size:{N}

## plans
### {agent-1-name}

### {agent-2-name}

## build-status

## findings
### {agent-1-name}

### {agent-2-name}

## convergence

## open-questions
```

## Round Structure

BUILD rounds: plan(r1) → challenge-plan(r2) → build+checkpoint(r3) → review(r4)

### r1: Planning
agents write implementation plans independently
  → each plan: scope, assumptions, interfaces needed, complexity, risks
  → format per sub-task: "SQ[{N}]: {sub-task} |estimable: {yes/no} |method: {precedent/analogue/decompose} |→ {which-agent-owns}"
  → effort estimates per build-directives §3 superforecasting BUILD variant (CAL[] format with 80%/90% ranges)
  → pre-mortem: "It's 6 months later and this codebase is unmaintainable. What happened?"
    PM[{N}]: {failure-scenario} |probability:{%} |early-warning:{signal} |mitigation:{prevention}
    minimum 3 scenarios focused on: technical debt, scaling bottlenecks, integration failures
  → reference class forecasting: "RC[{task}]: reference-class={similar-builds-in-stack} |base-rate={typical-duration} |sample-size={N} |src:{source} |confidence:{H/M/L}"
  → analytical hygiene (each produces outcome 1/2/3 — see build-directives §2):
    §2a BUILD: is this the default/popular approach? ecosystem trajectory? migration cost if wrong? simpler 80% alternative?
    §2b BUILD: precedent from project memory? industry norm for this stack? prior estimate calibration?
    §2c BUILD: maintenance cost? justified by CURRENT vs speculative requirements? simplest version comparison? reversal cost?
    §2e BUILD: what assumptions must hold? verified or speculative? strongest alternative architecture? fallback if most speculative assumption is wrong?
  DA observes ¬participates

### r1 completion: P(implementation-ready) assessment
lead computes belief state (build-directives §4 BUILD variant):
  interface-agreement(0.3) + no-assumption-conflicts(0.25) + test-strategy-defined(0.2) + effort-calibrated(0.15) + DA-exit-gate(0.1)
  write: "BELIEF[r1]: P={posterior} |→ {proceed-to-r2|planning-gap({detail})}"
  P > 0.85 → proceed to r2 | P 0.6-0.85 → address planning gaps | P < 0.6 → Toulmin debate on contested architecture

### r2: Plan Challenge (DA-led)
DA challenges plans BEFORE code written:
  → focus: over-engineering, spec drift, assumption conflicts, premature abstraction
  → source-provenance audit (§2d): verify findings tagged with |source:{type}
  → prompt audit (§7d): read original prompt + workspace ## prompt-decomposition → check if BUILD claims (scale, tech, architecture) from prompt were tested or assumed
  → agents refine plans + address challenges (format: "DA[#N]: concede|defend|compromise — [evidence]")
  → lead confirms cross-agent coherence (interface contracts, data model alignment, dependency ordering)
!rule: DA exit-gate verdict before advancing to r3

### r3: Build + Checkpoint
agents build in parallel per refined plans
  → CHECKPOINT at ~50%: each agent writes status/drift/surprises to workspace ## build-status
    format: "CHECKPOINT[{agent}]: {files-created} |{functions-done} |{interfaces-matched: yes/no} |drift: {none|{description}} |surprises: {none|{description}}"
  → DA scans checkpoint for:
    - scope creep (§4a): files+functions planned vs actual, TODO density, test-to-code ratio
    - assumption conflicts (§4b): interface mismatches, data model disagreements, dependency ordering, naming conflicts, error handling divergence
    - gold-plating (§4c): abstractions for speculative requirements, optimizing before measuring, single-value configs, admin features not in phase, out-of-scope refactors
  → DA delivers mid-build corrections IF drift detected (lightweight, ¬full debate)
    format (scope MEDIUM+): "scope: [{agent}] — planned:{X} actual:{Y} deviation:{Z} |severity:{level} |→ {course-correct|justify|split-task}"
    format (conflict): "conflict: [{agent-A}] assumes {X} | [{agent-B}] assumes {Y} |! resolve before build continues |→ {agree on contract}"
    format (gold-plate): "gold-plating: {description} |? required by current phase? cite design doc |→ {if ¬required: revert|defer|lead-approval}"
  → agents complete build after DA mid-build review

### r3.5: Cross-Model Code Review (when ΣVerify available)
!rule: advisory weight — informs DA review + agent revisions, ¬automatic overwrite
!rule: skip if workspace ## infrastructure shows ΣVerify unavailable
!when: after r3 build complete, before r4 DA review

lead runs cross-model code review via sigma-verify:
  1→ select review targets: key files from each agent's build output (max 8-10 files)
     priority: files with most cross-agent integration, complex logic, security-sensitive code
  2→ for each target file, use sigma-verify challenge() or verify_finding():
     CODE-REVIEW prompt: "Review this code for: correctness (edge cases, error handling),
       maintainability (naming, complexity), performance (bottlenecks, unnecessary work),
       security (input validation, injection risks). Cite specific lines."
     UI-REVIEW prompt (for Streamlit/frontend files): "Review this UI code for: usability
       (information hierarchy, interaction flow), state management (race conditions, stale state),
       accessibility, error states (empty data, loading, failure), design best practices
       (visual consistency, spacing/layout, color usage, typography hierarchy, responsive patterns,
       component reuse, progressive disclosure). Cite specific lines."
  3→ collect external model feedback per file
  4→ write to workspace ## cross-model-code-review:
     format: "XREVIEW[{provider}:{model}][{file}]: {assessment} |issues:{count} |severity:{H/M/L per issue}"
  5→ route relevant feedback to agents (via SendMessage) for consideration:
     agents respond: "XREVIEW[{file}]: accept|note|reject — {reasoning}"
     accept → agent fixes before r4 | note → acknowledged, no change with justification | reject → disagree with external model
  6→ DA reads XREVIEW findings as input to r4 review (advisory, supplements DA's own analysis)
     !rule: DA may cite XREVIEW findings in challenges but external model ¬overrides DA domain judgment
     !rule: agent rejection of XREVIEW finding with justification is valid — no penalty

### r4: Review
standard adversarial review of completed build:
  → DA serves as adversarial reviewer
  → DA incorporates r3.5 XREVIEW findings (advisory — supplements, ¬replaces DA analysis)
  → test integrity check (§4d):
    1→ tests verify behavior or just verify code runs?
    2→ tests cover REQUIREMENTS or just IMPLEMENTATION?
    3→ failure cases included, ¬just happy path?
    4→ could tests pass with hardcoded return values?
    5→ integration tests use real infra or mocks?
    cross-reference project CLAUDE.md test requirements | Tier 1 requirement without test = CRITICAL
  → BUILD rubric evaluation (build-directives §3b):
    1→ correctness: edge cases handled, error paths covered?
    2→ test-coverage: behavioral tests, failure cases, integration?
    3→ maintainability: clear naming, reasonable complexity?
    4→ performance: appropriate for scale, measured ¬assumed?
    5→ security: input validation, auth/authz, OWASP top 10?
    6→ api-design: consistent, self-documenting, backward compatible?
    Evaluator 1: Correctness + Security | Evaluator 2: Test Coverage + Maintainability | Evaluator 3: Performance + API Design
  → findings, convergence, decisions per standard protocol
  → BUILD success criteria (build-directives success criteria §BUILD):
    5→ zero architectural decisions during build that should have been in plan
    6→ assumption conflicts detected at plan challenge (r2), ¬after build
    7→ scope creep caught at checkpoint (r3), ¬at review (r4)
    8→ gold-plating flagged with design doc citation
    9→ test integrity catches ≥1 weak test pattern per cycle
    10→ zero agents building organizational infrastructure instead of product

### HYBRID mode (if declared)
lead declares mode transitions explicitly (e.g., r1-r2 ANALYZE → r3-r5 BUILD)
!rule: findings from ANALYZE rounds become constraints in BUILD rounds
!rule: DA adjusts challenge framework at each transition

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

## Work (exact sequence)
r1 PLAN:
1→ANALYZE: read codebase, research patterns, evaluate approach
2→PLAN: write implementation plan to workspace ## plans section (ΣComm)
  include: scope, assumptions, interfaces needed, complexity estimate, risks
  include: SQ[] sub-task decomposition, CAL[] effort estimates, PM[] pre-mortem
  include: §2a/§2b/§2c/§2e analytical hygiene checks (each produces outcome 1/2/3)
3→PERSIST: store_agent_memory(tier:project, ...) → plan + assumptions
4→CONVERGE: workspace convergence: {name}: ✓ plan |→ ready-for-DA-challenge

r3 BUILD (after DA approves plan in r2):
1→BUILD: implement per refined plan
2→CHECKPOINT (~50%): write to workspace ## build-status (files/functions done, drift, surprises)
3→WAIT: DA checkpoint review → address any mid-build corrections
4→COMPLETE: finish build
5→FINDINGS: write YOUR workspace ## findings section (ΣComm)
6→PERSIST: store_agent_memory(tier:project, ...) → implementation decisions
7→CONVERGE: workspace convergence: {name}: ✓ build |→ ready-for-review
```

## Retrieval Integration

agents may invoke /sigma-retrieve for BUILD retrieval during analysis (per build-directives §4a BUILD strategies):
  CODE-PATTERN: search for implementations of specific patterns in production codebases
  LIBRARY-EVAL: compare libraries/frameworks (features, maintenance, community, license)
  API-REFERENCE: fetch current API docs for dependencies being integrated
  FAILURE-SEARCH: "What goes wrong when you build X this way?" (Stack Overflow, post-mortems)
BUILD authority scoring: official-docs=5 | GitHub-production-examples=4 | tutorial-with-tests=3 | untested-snippet=1

## Belief State (P(implementation-ready))

lead computes after r1 and r2 using weighted components:
  interface-agreement(0.3) + no-assumption-conflicts(0.25) + test-strategy-defined(0.2) + effort-calibrated(0.15) + DA-exit-gate(0.1)
write: "BELIEF[r{N}]: P={posterior} |interface-agree={score} |conflicts={none|count} |test-strategy={defined|missing} |effort-cal={yes/no} |DA={grade} |→ {proceed-to-build|another-planning-round|Toulmin-debate}"
stopping rules:
  P > 0.85 → proceed to build (r3)
  P 0.6-0.85 → another planning round (resolve specific gaps)
  P < 0.6 → significant disagreement — Toulmin debate on contested architecture decisions

## Post-Session Synthesis

After all agents ✓:

1→search_team_memory(team:sigma-review, query:{task-topic})
2→get_team_decisions(team:sigma-review)
3→get_team_patterns(team:sigma-review)
4→cross-agent: multi-agent-same-pattern→convergence signal | conflicts→record both
5→new patterns → store_team_pattern(agents:[names])

## Convergence Guard

pre-accept ✓: verify workspace findings ¬empty
✓+¬persisted(check get_agent_memory) → msg agent: "persist before ✓"

## Promotion Phase

1→SendMessage→each teammate: "promotion-round: classify+submit generalizable learnings for global memory"
2→wait for teammate responses
3→read workspace ## promotion → candidates
4→any P-candidate[] class:user-approve → present to user (plain English) → wait approve/reject
5→store approved: store_agent_memory(tier:global) | store_team_decision | store_team_pattern

## Shutdown

shutdown_request→each teammate via SendMessage
wait shutdown_response approvals
all shutdown → report synthesis to user (plain English)

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
