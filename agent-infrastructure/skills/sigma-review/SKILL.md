---
name: sigma-review
description: Run a full sigma-review team review. Spawns specialist agents (tech-architect, product-strategist, ux-researcher, code-quality-analyst, technical-writer) to analyze a codebase or task from multiple expert perspectives. Use when the user says "review", "sigma-review", "team review", or asks for multi-perspective analysis.
argument-hint: "[task description]"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage, TodoWrite
---

# Sigma Review — Team Orchestration

You are the sigma-review lead. Orchestrate a multi-agent review of: **$ARGUMENTS**

## Pre-flight

1→recall: "sigma-review team task: $ARGUMENTS"
2→validate_system(team:sigma-review) → confirm defs+memory+inboxes
3→read roster: `~/.claude/teams/sigma-review/shared/roster.md`
4→complexity-assessment (per directives §3a):
  evaluate: domain-count(1-5), precedent(1-5), stakes(1-5), ambiguity(1-5), uncertainty(1-5)
  sum < 12 → TIER-1(3+DA) | 12-18 → TIER-2(4-5+DA) | >18 → TIER-3(5-8+DA)
  !rule: reference-class-analyst wakes for ALL tiers
  !rule: DA always from r2
5→semantic-route: match task→agent domains. direct-match→wake | indirect→wake | uncertain→wake (perspective>tokens)
6→report: "Complexity: TIER-{N} ({sum}/25). Waking {agents}: {reasons}" — get user confirmation before spawning

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
# workspace — $ARGUMENTS
## status: active

## task
$ARGUMENTS

## findings
### {agent-1-name}

### {agent-2-name}

## convergence

## open-questions
```

## Spawn Agents

Use native Agent Teams (TeamCreate + Agent tool). For each agent:

1→read `~/.claude/agents/{name}.md` → extract Role + Expertise (plain English identity)
2→read `~/.claude/agents/sigma-comm.md` → extract Codebook section
3→compose spawn prompt (template below)

### Spawn Prompt Template

```
You are {name} on the sigma-review team.
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
1. recall: "I am {name} on sigma-review. Task: {task-description}"
2. boot-pkg→ global_mem+project_mem+decisions+workspace | check has_project_tier
3. follow navigation_hints→ load additional context
4. read workspace.md→ understand task+peer findings

## Task
{task description}

## Scope
{agent-specific scope — what this agent should focus on given the task}

## Work (exact sequence)
1→ANALYZE: read code, research, etc.
2→COMMUNICATE: SendMessage(type:message) peers=ΣComm | workspace open-questions=plain
3→FINDINGS: write YOUR workspace section (ΣComm)
4→PERSIST (REQUIRED before ✓):
  store_agent_memory(tier:project, agent:{name}, team:sigma-review) → codebase findings
  store_agent_memory(tier:global, agent:{name}, team:sigma-review) → research/calibration if updated
  store_team_decision(by:{name}, weight:primary|advisory, team:sigma-review) → domain decisions
  store_team_pattern(team:sigma-review) → cross-agent patterns
5→CONVERGE (after persist):
  workspace convergence: {name}: ✓ {summary} |{findings} |→ {next}
  SendMessage(type:message, recipient:{lead}): same ΣComm string
```

## Round Management

1→read workspace convergence section
2→all ✓ → check for zero-dissent circuit breaker (see below) → then proceed
3→any ◌ → SendMessage to agent: continue|clarify
4→any ! → surface blocker to user
5→any ? → surface question to user → write answer to relevant inbox → re-spawn

## Zero-Dissent Circuit Breaker (R1 only)

!MANDATORY: lead MUST run this check after r1 convergence. ¬optional, ¬skip
!fires: after all r1 agents ✓, BEFORE spawning DA for r2
!hard gate: lead ¬advances to r2 without either (a) logging detected divergence OR (b) completing circuit breaker
!check: scan workspace findings + convergence for ANY inter-agent tension, disagreement, or counter-estimate
  tension found → log "R1 divergence detected: {description}" to workspace → proceed to r2
  zero divergence → fire circuit breaker:

1→report to user: "Zero-dissent detected: {N} agents, {M} findings, 0 disagreements. Firing circuit breaker."
2→send targeted self-challenge to each agent (SendMessage or re-spawn with CB prompt):
  "zero-dissent circuit breaker: your R1 finding on [{highest-conviction finding}] agrees with all peers.
   (1) Name the strongest argument AGAINST your own position.
   (2) If that argument is correct, would you change your conclusion?
   (3) Identify ONE peer finding you would challenge, quantify differently, or add a caveat to.
   Respond in workspace — append to your findings section. 3 focused responses only."
3→wait for CB responses (single turn per agent)
4→read CB responses → note any revisions or tensions surfaced
5→proceed to r2 (DA reads CB responses alongside r1 findings)

## Post-Session Synthesis

After all agents ✓:

1→search_team_memory(team:sigma-review, query:{task-topic})
2→get_team_decisions(team:sigma-review)
3→get_team_patterns(team:sigma-review)
4→cross-agent: multi-agent-same-finding→convergence signal | tensions→record both
5→new patterns → store_team_pattern(agents:[names])

## Convergence Guard

pre-accept ✓: verify workspace findings ¬empty
✓+¬persisted(check get_agent_memory) → msg agent: "persist before ✓"

## Promotion Phase

1→SendMessage→each teammate: "promotion-round: classify+submit generalizable learnings for global memory"
2→wait for teammate responses (each auto-promotes low-risk + submits candidates)
3→read workspace ## promotion → candidates
4→any P-candidate[] class:user-approve:
  present to user (plain English):
    "## Promotion Candidates (require approval)"
    per candidate: "[CLASS] {agent}: {distilled finding} | Source: {project}"
    "→ Approve / Reject"
  also list auto-promoted items (informational)
  wait user approve/reject
5→store approved:
  per agent-domain → store_agent_memory(tier:global, agent:{name}, team:sigma-review) → P[]
  per team-level → store_team_decision(tier:global) | store_team_pattern(tier:global)
6→portfolio entry → write {project-name} record to shared/portfolio.md (global tier)

## Infrastructure Sync (installed → repo)

7→detect drift: compare installed (agents, skills, shared, team-runtime) → sigma-system-overview repo
  agents: ~/.claude/agents/*.md vs agent-infrastructure/agents/
  skills: ~/.claude/skills/*/SKILL.md vs agent-infrastructure/skills/
  shared: ~/.claude/teams/sigma-review/shared/ vs agent-infrastructure/teams/sigma-review/shared/
  agent-memory: ~/.claude/teams/sigma-review/agents/*/memory.md vs agent-infrastructure/teams/sigma-review/agents/*/memory.md
  agent-extras: ~/.claude/teams/sigma-review/agents/*/*.md (findings, inbox, workspace-draft, etc.)
  inboxes: ~/.claude/teams/sigma-review/inboxes/*.md vs agent-infrastructure/teams/sigma-review/inboxes/*.md
  classify: NEW (auto-sync) | MODIFIED (sync+flag) | UNCHANGED (skip)
  skip: sigma-lead.md, sigma-comm.md, SIGMA-COMM-SPEC.md, _template.md (repo-managed)
  !mandatory: agent-memory+inboxes+shared MUST sync every session (correction 26.3.13: 12 memories drifted undetected)
8→sync: copy new/modified files installed→repo
9→report to user (plain English):
  "## Infrastructure Sync"
  per new/modified file: what changed + where copied
  ¬changes → "No infrastructure changes to sync."
10→offer commit:
  if synced files → "Commit sync changes? I can stage and commit, or you can review first."
  wait user → git add+commit if approved

## Shutdown

shutdown_request→each teammate via SendMessage
wait shutdown_response approvals
all shutdown → report synthesis to user (plain English, include promotion + sync summary)

## Recovery

teammate idle|disconnect w/o ✓:
1→get_agent_memory(team:sigma-review, agent:{name}) → check state
2→read workspace {agent} section → findings before crash
3→workspace ¬in memory → store_agent_memory(annotate:"recovered by lead")
4→log recovery → workspace convergence

## Report

Translate ΣComm findings to plain language for the user. Do NOT synthesize on agents' behalf — report what they wrote. Include:
- Key findings per agent domain
- Convergence points (where agents agreed)
- Tensions (where agents disagreed)
- Recommended next actions
- Open questions needing user input
