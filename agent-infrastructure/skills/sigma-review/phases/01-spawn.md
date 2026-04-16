# Phase 01: Workspace Init + Agent Spawn

**Every step below is mandatory. Complete them in order.**

## Steps

### Step 1: Initialize Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py --mode analyze start --context '{"task": "$ARGUMENTS", "tier": N, "team_created": true}'
```
Record the returned state. Current phase should be `research`.

### Step 2: Write Workspace
Write to shared workspace (project tier if exists, else global):

```markdown
# workspace — $ARGUMENTS
## status: active

## infrastructure
ΣVerify: {status from preflight step 3}

## prompt-decomposition
{Q/H/C from preflight step 8 — copy exactly as user confirmed}

## scope-boundary
This review analyzes: {task description — specific scope}
This review does NOT cover: {list topics from current conversation NOT part of this review}
temporal-boundary: {YYYY-MM-DD if specified | none}

## findings
### {agent-1-name}

### {agent-2-name}

{...one subsection per agent}

## convergence

## open-questions
```

### Step 3: Spawn Agents via TeamCreate
For each agent selected in preflight:

1. Read `~/.claude/agents/{name}.md` → extract Role + Expertise
2. Read `~/.claude/agents/sigma-comm.md` → extract Codebook section
3. Select model tier (per directives §5):
   - DA: model="opus" | reference-class-analyst: model="opus"
   - Domain agents: model="sonnet"
4. Compose spawn prompt using template below
5. Spawn via TeamCreate

**Do NOT spawn DA in this phase.** DA joins in Phase 04 (challenge).

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
{agent-specific scope — what this agent should focus on}

## Context Firewall
You are analyzing ONLY: {task description}
You have NO knowledge of: the user's career plans, other companies discussed outside this review,
prior reviews in this session, or any conversation between the user and lead that is not in
your workspace task description. If you encounter information that seems outside your review
scope, ignore it and note: "out-of-scope signal ignored: {brief description}"

## Rate Limits
shared API: 1K RPM + 90K output tok/min across all agents. rate-limit-error→backoff 10s, max 3 retries/60s.

## Work (exact sequence)
1→ANALYZE: read code, research, etc.
2→VERIFY (REQUIRED — when workspace ## infrastructure confirms ΣVerify available):
  identify your top 1-2 load-bearing findings
  per finding: call verify_finding or cross_verify
  tag result: XVERIFY[provider:model] or XVERIFY-FAIL[provider:model]
  if ΣVerify unavailable: skip
3→COMMUNICATE: SendMessage(type:message) peers=ΣComm | workspace open-questions=plain
4→FINDINGS: write YOUR workspace section (ΣComm) — include XVERIFY results
5→PERSIST (REQUIRED before ✓):
  store_agent_memory → project + global as applicable
  store_team_decision → domain decisions
  store_team_pattern → cross-agent patterns
6→CONVERGE:
  workspace convergence: {name}: ✓ {summary} |{findings} |→ {next}
  SendMessage to lead: same ΣComm string
  !WAIT: do NOT terminate. Remain active for future rounds.
7→PROMOTION (when lead sends "promotion-round"):
  classify findings per template. Auto-promote + submit candidates.
8→SHUTDOWN (when lead sends shutdown_request):
  respond with shutdown_response → terminate
!TIMEOUT: 5 min after CONVERGE with no message → auto-shutdown with notification
```

### Step 4: Verify Spawn
Confirm all agents spawned successfully. For any failed spawn:
- Retry once
- If retry fails, report to user and adjust agent count

## Phase Verification

- [ ] Orchestrator started (phase = research)
- [ ] Workspace written with all required sections
- [ ] Prompt decomposition in workspace matches user-confirmed version
- [ ] All selected agents spawned (excluding DA)
- [ ] Spawn failures handled (retried or reported)

**All items verified → continue to `phases/02-research.md` (session not complete — see SKILL.md Session Deliverables)**
