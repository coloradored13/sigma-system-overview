# Phase 01: Workspace Init + Agent Spawn

**Every step below is mandatory. Complete them in order.**

## Steps

### Step 1: Initialize Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py start --mode build --context '{"task": "$ARGUMENTS", "tier": N, "team_created": true}'
```
Record the returned state. Current phase should be `plan`.

### Step 2: Write Workspace
Write to shared workspace (project tier if exists, else global):

```markdown
# workspace — BUILD: $ARGUMENTS
## status: active
## mode: BUILD

## task
$ARGUMENTS

## infrastructure
ΣVerify: {status from preflight step 3}

## prompt-understanding
{Q/H/C from preflight step 8 — copy exactly as user confirmed}

## scope-boundary
This build implements: {phase description, specific features}
This build does NOT implement: {future phases, nice-to-haves, features not in spec}
Lead: before accepting agent output, verify it builds ONLY what's in scope.

## complexity-assessment
BUILD TIER-{N} |scores: module-count({N}),interface-changes({N}),test-complexity({N}),dependency-risk({N}),team-familiarity({N}) |total:{sum} |plan-track:{N} |build-track:{N}

## plans (plan-track agents)
### tech-architect
### product-designer
### product-strategist

## architecture-decisions (locked after DA approval)
{ADR[N]: decision |alternatives:{considered} |rationale:{why} |prompted-by:{Q[N]/H[N]/C[N]}}

## design-system (locked after DA approval)
{DS[]: design tokens, component hierarchy, interaction patterns, responsive strategy}

## interface-contracts (build-track implements against these)
{IC[]: typed contracts between components}

## build-status (checkpoints)

## cross-model-code-review

## findings
### {builder-1-name}
### {builder-2-name}

## convergence

## gate-log

## open-questions
```

### Step 3: Spawn Agents via TeamCreate
For each agent selected in preflight:

1. Read `~/.claude/agents/{name}.md` → extract Role + Expertise
2. Read `~/.claude/agents/sigma-comm.md` → extract Codebook section
3. Select model tier (per build-directives §5):
   - DA: model="opus" | domain agents: model="sonnet"
4. Compose spawn prompt using template (see below)
5. Spawn via TeamCreate

**Do NOT spawn DA in this phase.** DA joins in Phase 03 (plan challenge).

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
shared API: 1K RPM + 90K output tok/min across all agents. rate-limit-error→backoff 10s, max 3 retries/60s.

## Work
{select track based on agent role — lead includes ONLY the relevant section}

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
5→LOCK: when P(plan-ready) > 0.85, finalize to workspace
6→PERSIST + EXIT: plan-track exits. Re-spawned for build review.

PHASE 2 — BUILD REVIEW (re-spawned to evaluate build against your plan):
1→READ: your locked output from workspace
2→READ: build-track output (workspace ## findings, code)
3→REVIEW: evaluate build against your architectural/design intent
  format: "PLAN-REVIEW[{name}]: {component} |compliance:{full|partial|drift} |issue:{description} |→ {accept|fix:{specific-change}}"
4→ITERATE: build-track fixes agreed issues → you re-review
5→PERSIST + CONVERGE: when build passes review

### BUILD-TRACK (implementation-engineer, ui-ux-engineer, code-quality-analyst)
PHASE 1 — PLAN CHALLENGE (evaluate plan for feasibility):
1→READ: workspace ## plans, ## architecture-decisions, ## design-system, ## interface-contracts
2→CHALLENGE: evaluate plan for implementability
  format: "BUILD-CHALLENGE[{name}]: {plan-element} |feasibility:{H/M/L} |issue:{description} |→ {revise|clarify|accept}"
3→ITERATE: plan-track refines → you re-evaluate

PHASE 2 — BUILD (implement + fix until consensus):
1→READ: locked constraints from workspace (ADRs, design system, interface contracts)
  !rule: these are BUILD CONSTRAINTS. Implement against them, ¬redesign.
2→BUILD: implement per approved plan
3→CHECKPOINT (~50%): write to workspace ## build-status
4→RESPOND TO REVIEW: DA + plan-track will review your build
5→FIX + RE-SUBMIT: implement agreed changes
6→ITERATE: repeat until P(build-quality) > 0.85
7→PERSIST + CONVERGE: when build passes review
```

### Step 4: Verify Spawn
Confirm all agents spawned successfully. For any failed spawn: retry once, report to user if retry fails.

## Exit Checklist

- [ ] Orchestrator started (phase = plan)
- [ ] Workspace written with all required sections
- [ ] Prompt understanding in workspace matches user-confirmed version
- [ ] All selected agents spawned (excluding DA)
- [ ] Spawn failures handled

**All items checked → read `phases/02-plan.md`**
