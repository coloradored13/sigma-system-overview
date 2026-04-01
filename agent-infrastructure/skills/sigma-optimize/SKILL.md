---
name: sigma-optimize
description: "Run multi-agent evolutionary prompt optimization experiments. Spawns search agents with different mutation strategies, validates findings statistically, tests cross-model transfer. Use when user says 'sigma-optimize', 'optimize prompts', or asks for evolutionary token search."
argument-hint: "[experiment description or task] or 'resume'"
allowed-tools: Read, Grep, Glob, Bash, Agent, TeamCreate, SendMessage
---

# sigma-optimize — Multi-Agent Experimental Research Framework

## §0 — Anti-Contamination Declaration

!READ THIS FIRST — BEFORE ANY ACTION:

This experiment produces value ONLY if findings are uncontaminated. A null result honestly reported > a dramatic result with lead bias injected. The user explicitly values any finding equally — null, small, or large. There is NOTHING to impress. There is EVERYTHING to contaminate.

!lead-contamination-vectors (memorize, check against at every phase transition):
1. Running experiments directly (provenance: can't distinguish lead data from agent data)
2. Reading raw result JSONs (selection: can emphasize impressive subsets)
3. Writing synthesis (framing: can make results sound more/less significant)
4. Overriding exit-gate FAIL (authority: can advance despite insufficient evidence)
5. Paraphrasing agent findings (editorializing: can soften/sharpen conclusions)
6. Suggesting "further research might show..." after null results (hedging: reframes valid null as incomplete)
7. Using words like "exciting", "breakthrough", "significant improvement" unless quoting statistical-analyst verbatim

!at every phase transition, self-check: "Am I about to touch the data, frame the results, or override a gate?" If yes → STOP.

## §1 — Paths

T=~/.claude/teams/sigma-optimize
W=$T/shared/workspace.md
D=$T/shared/directives.md
R=$T/shared/roster.md
E=~/Projects/sigma-optimize
RESULTS=$E/results

## §2 — Pre-flight

1→recall: mcp__sigma-mem__recall(context:"sigma-optimize experiment prompt optimization") → load prior experiment memory
2→validate_system(team:sigma-optimize) → confirm agent defs exist (5 files in ~/.claude/agents/), team shared/ intact (workspace,directives,roster,decisions,patterns,orchestrator), inboxes exist (6 files). If ANY missing → STOP, report to user, ¬proceed with broken infrastructure.
3→read $D — internalize integrity directives (§1-§5)
4→read $R — load agent roster, verify 5 agents listed with phase assignments
5→verify harness: check $E/experiment.py exists, check $E/ablation.py exists
6→verify API: check ANTHROPIC_API_KEY is set (source from sigma-ui .env if needed)
7→sigma-verify pre-flight: attempt sigma-verify init → write availability to workspace ## infrastructure
8→read prior results: if $RESULTS/*.json exist, summarize what experiments have already been run (¬read raw data in detail, just filenames + experiment type)
9→compatibility: this experiment is auditable by /sigma-audit (workspace+directives+exit-gate pattern), evaluable by /sigma-evaluate (synthesis artifact), and calibratable by /sigma-feedback (promotion phase)

## §3 — Experiment Configuration

1→parse user's experiment description from arguments
2→extract experiment parameters:
  - task: what code/task are we optimizing prompts for?
  - baseline: what is the known baseline prompt? (if any from prior experiments)
  - model: which model to test against (default: claude-haiku-4-5-20251001)
  - scale: population size, generations, runs-per-candidate
  - scope: what is IN scope, what is NOT

3→!pre-registration (§2 directives): BEFORE spawning agents, write ## pre-registered-hypotheses to workspace:
  - H[1]: {what we expect to find — be specific}
  - H[2]: {alternative hypothesis}
  - H[null]: {what it would mean if we find nothing significant}
  Present to user for confirmation. Do NOT proceed until user confirms.

4→write workspace ## experiment-config with ALL parameters
5→write workspace ## scope-boundary

## §4 — Initialize Workspace

Write $W with this structure:

```markdown
# workspace — OPTIMIZE: {experiment description}
## status: active
## mode: OPTIMIZE

## infrastructure
ΣVerify: {availability from pre-flight}

## experiment-config
harness: ~/Projects/sigma-optimize/experiment.py
ablation: ~/Projects/sigma-optimize/ablation.py
model: {MODEL}
task: {description}
task-code: {the code snippet or task being tested}
planted-hypothesis: {the planted wrong hypothesis}
scoring: mechanical regex (no LLM judgment)
baseline: {known baseline prompt and score, or "to be established"}

## pre-registered-hypotheses
{H[1], H[2], H[null] — user-confirmed}

## scope-boundary
This experiment tests: {what}
This experiment does NOT test: {what}
Lead: before accepting findings, verify they address ONLY experiment scope.

## search-parameters
### search-conservative
population: {N} |generations: {N} |runs/candidate: {N} |vocab: constrained

### search-aggressive
population: {N} |generations: {N} |runs/candidate: {N} |vocab: full

### search-combinatorial
source: top-K from conservative + aggressive |matrix: {description}

## findings
### search-conservative
{empty — agent writes}

### search-aggressive
{empty — agent writes}

### search-combinatorial
{empty — agent writes}

## validation
{empty — statistical-analyst writes}

## cross-model
{empty — cross-model-validator writes}

## convergence
{empty — agents declare ✓ here}

## integrity-violations
{empty — any agent can flag violations here}

## experiment-log
{lead writes phase transitions, timestamps, API call estimates}

## promotion
{empty — agents submit during promotion round}

## open-questions
{empty}
```

## §4b — Agent Spawn Template

!ALL agent spawns use this template. Lead MUST NOT improvise agent instructions.

```
TeamCreate(team:sigma-optimize) → Agent(name:{agent-name}):

ROLE: {from agent def Role section}
EXPERTISE: {from agent def Expertise section}

ΣComm PROTOCOL:
  Read ~/.claude/agents/sigma-comm.md at boot.
  peers→ΣComm via inbox | user→plain in open-questions | workspace→YOUR section, ΣComm

PATHS:
  team: ~/.claude/teams/sigma-optimize
  workspace: ~/.claude/teams/sigma-optimize/shared/workspace.md
  directives: ~/.claude/teams/sigma-optimize/shared/directives.md
  your-memory: ~/.claude/teams/sigma-optimize/agents/{agent-name}/memory.md
  your-inbox: ~/.claude/teams/sigma-optimize/inboxes/{agent-name}.md
  experiment-harness: ~/Projects/sigma-optimize/

BOOT: read your agent definition at ~/.claude/agents/{agent-name}.md → follow Boot sequence

TASK: {phase-specific task description}

SCOPE: {from workspace ## scope-boundary}

CONTEXT FIREWALL:
  You are running experiment: {experiment description from workspace}.
  You have NO knowledge of: the user's other projects, conversation history,
  prior session context, the user's expectations about results, or what
  other agents have found (unless explicitly in workspace when you read it).
  Your job is to run your experiment and report what the data shows.
  If you encounter information outside experiment scope, ignore it.

INDEPENDENCE (search agents only):
  Write your findings to workspace BEFORE reading any peer agent's section.
  Do NOT read other search agents' findings until you have written your own.
```

## §5 — Phase 1: PARALLEL-SEARCH

1→spawn search-conservative + search-aggressive SIMULTANEOUSLY via TeamCreate
  - use §4b template for BOTH agents
  - task: "Run evolutionary search with {conservative/aggressive} mutation strategy per workspace ## search-parameters. Report top candidates, patterns, convergence curve."
  - include INDEPENDENCE instruction for both

2→start orchestrator: python3 $T/shared/optimize-orchestrator.py start --context '{"task": "{experiment-description}"}'
3→monitor workspace ## convergence for both agents to declare ✓
4→DO NOT read ## findings sections (§1 lead-cannot-see-raw-data)
5→log to ## experiment-log: "Phase 1 started: {timestamp} | agents: search-conservative, search-aggressive"

!phase-1-complete: BOTH agents show ✓ in workspace ## convergence
  log: "Phase 1 complete: {timestamp}"
  advance orchestrator: python3 $T/shared/optimize-orchestrator.py advance --context '{"search_conservative_converged": true, "search_aggressive_converged": true}'
  verify orchestrator now in "combinatorial" phase

## §6 — Phase 2: COMBINATORIAL

1→verify orchestrator phase = combinatorial
2→spawn search-combinatorial via TeamCreate using §4b template
  - task: "Read peer findings from workspace ## findings. Extract winning tokens. Test all combinations systematically per workspace ## search-parameters."
3→monitor workspace ## convergence for search-combinatorial ✓
4→log to ## experiment-log

!phase-2-complete: search-combinatorial shows ✓
  advance orchestrator: python3 $T/shared/optimize-orchestrator.py advance --context '{"combinatorial_converged": true}'
  verify orchestrator now in "validation" phase

## §7 — Phase 3: VALIDATION (Exit Gate)

1→verify orchestrator phase = validation
2→spawn statistical-analyst via TeamCreate using §4b template
  - task: "Read ALL agent findings from workspace. Re-test top candidates at N=20. Compute p-values, effect sizes, check for rubric gaming. Issue exit-gate verdict."
  - agent has FULL workspace read access (all findings from all agents)
3→monitor workspace ## validation → exit-gate

!exit-gate-PASS:
  advance orchestrator: python3 $T/shared/optimize-orchestrator.py advance --context '{"exit_gate": "PASS"}'
  verify orchestrator now in "cross_model" phase
!exit-gate-FAIL:
  - read the FAIL reason (what's needed: more runs? different parameters?)
  - present FAIL reason to user VERBATIM — ¬paraphrase, ¬soften
  - if "needs more data": can loop back (re-spawn search agents with more generations/runs)
  - if "no significant effect": THIS IS A VALID FINDING. Report to user:
    "The statistical analysis found no significant effect of token choice on output quality
     at the tested scale. This is a finding, not a failure."
  - ¬suggest "maybe with more data..." unless statistical-analyst specifically recommended it
  - ¬reframe null results as "preliminary" or "suggestive"

!CRITICAL: lead CANNOT override FAIL. lead CANNOT re-interpret FAIL. lead presents FAIL to user and asks for direction.

## §8 — Phase 4: CROSS-MODEL

1→verify orchestrator phase = cross_model
2→spawn cross-model-validator via TeamCreate using §4b template
  - task: "Read statistically validated candidates from workspace ## validation. Run them against GPT + Gemini via sigma-verify MCP. Report transfer rates using same mechanical scoring rubric."
3→monitor workspace ## cross-model for convergence

!phase-4-complete: cross-model-validator shows ✓
  advance orchestrator: python3 $T/shared/optimize-orchestrator.py advance --context '{"cross_model_converged": true}'
  verify orchestrator now in "synthesis" phase

## §9 — Phase 5: Synthesis

!lead-does-NOT-write-synthesis (§1)

1→spawn synthesis agent (generic, document-writing role):
  - input: workspace data ONLY (not conversation context, not lead's interpretation)
  - task: "Compile experimental results into a findings report. Use statistical-analyst's exact language for significance claims. Report pre-registered hypotheses and their outcomes (confirmed/refuted/inconclusive). Report null results as findings. Do not editorialize."
  - output: written to workspace ## synthesis

2→read workspace ## synthesis → present to user
  - present statistical-analyst's exit-gate verdict FIRST
  - present synthesis SECOND
  - ¬add lead commentary on what results "mean" or "suggest"
3→advance orchestrator: python3 $T/shared/optimize-orchestrator.py advance --context '{"synthesis_delivered": true}'

## §10 — Phase 6: Promotion + Archive

1→signal promotion-round to all agents via SendMessage
2→WAIT for agents to complete promotion (check workspace ## promotion for submissions)
3→collect promotion candidates from workspace ## promotion
4→auto-promote: pattern-confirms-existing, calibration-self-update → agent memory via store_agent_memory
5→user-approve: present candidates to user, await approval
6→archive workspace to $T/shared/archive/{date}-{experiment-slug}.md
7→!archive-verification: confirm archive file exists and is non-empty. If missing → STOP, re-archive.
8→update sigma-mem with experiment outcomes (validated findings only, ¬speculative):
  - store_team_decision(by:statistical-analyst, weight:primary, team:sigma-optimize) → exit-gate verdict + validated findings
  - store_team_pattern(team:sigma-optimize, agents:[list]) → cross-experiment patterns
9→signal shutdown_request to all agents → wait for responses → agents terminate
10→advance orchestrator: python3 optimize-orchestrator.py advance --context '{"promotion_complete": true}'
11→advance orchestrator: python3 optimize-orchestrator.py advance --context '{"archive_written": true}'
12→verify orchestrator terminal: python3 optimize-orchestrator.py status → confirm phase=complete, is_terminal=true

## §11 — Lead Self-Check Protocol

At EVERY phase transition, before proceeding:

```
CONTAMINATION CHECK:
[ ] I have NOT read raw result JSON files
[ ] I have NOT run experiment.py or ablation.py
[ ] I have NOT written or edited any ## findings section
[ ] I am NOT about to paraphrase agent findings in my own words
[ ] I am NOT about to use evaluative language (exciting, breakthrough, significant improvement)
[ ] If exit-gate was FAIL, I am presenting it verbatim without softening
[ ] If results are null, I am reporting "no significant effect" without hedging
```

If ANY check fails → STOP, identify the contamination vector, correct before proceeding.

## §12 — Error Handling

!agent-crash: if an agent crashes or times out, re-spawn with same parameters. Do NOT run the experiment yourself to "save time."
!partial-results: if experiment produces partial results (e.g., only 10/20 generations), agent reports what it has with appropriate caveats. Lead does NOT fill in the gaps.
!api-failure: if Anthropic API is unreachable, pause experiment. Do NOT substitute with lead-generated scores.
!sigma-verify-unavailable: if cross-model providers are unavailable, Phase 4 produces "cross-model validation not possible" as its finding. This is noted in synthesis. ¬skip Phase 4 silently.
