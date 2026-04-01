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
2→read $D — internalize integrity directives (§1-§5)
3→read $R — load agent roster
4→verify harness: check $E/experiment.py exists, check $E/ablation.py exists
5→verify API: check ANTHROPIC_API_KEY is set (source from sigma-ui .env if needed)
6→sigma-verify pre-flight: attempt sigma-verify init → write availability to workspace ## infrastructure
7→read prior results: if $RESULTS/*.json exist, summarize what experiments have already been run (¬read raw data in detail, just filenames + experiment type)

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

## §5 — Phase 1: PARALLEL-SEARCH

1→spawn search-conservative + search-aggressive SIMULTANEOUSLY via TeamCreate
  - both agents get: workspace path, experiment config, their specific search parameters
  - !independence-instruction: "Write your findings to workspace BEFORE reading any peer agent's section. Do NOT read other search agents' findings until you have written your own."
  - !context-firewall: agents receive workspace but NOT raw result files from prior experiments

2→monitor workspace ## convergence for both agents to declare ✓
3→DO NOT read ## findings sections (§1 lead-cannot-see-raw-data)
4→log to ## experiment-log: "Phase 1 started: {timestamp} | agents: search-conservative, search-aggressive"

!phase-1-complete: BOTH agents show ✓ in workspace ## convergence
  log: "Phase 1 complete: {timestamp}"
  advance to Phase 2

## §6 — Phase 2: COMBINATORIAL

1→verify Phase 1 complete (both search agents converged)
2→spawn search-combinatorial via TeamCreate
  - agent reads peer findings from workspace to design combination matrix
  - agent runs systematic tests on all token combinations
3→monitor workspace ## convergence for search-combinatorial ✓
4→log to ## experiment-log

!phase-2-complete: search-combinatorial shows ✓
  advance to Phase 3

## §7 — Phase 3: VALIDATION (Exit Gate)

1→verify Phase 2 complete
2→spawn statistical-analyst via TeamCreate
  - agent has FULL workspace read access (all findings from all agents)
  - agent runs re-tests, computes statistics, checks for gaming
  - agent issues exit-gate verdict
3→monitor workspace ## validation → exit-gate

!exit-gate-PASS: advance to Phase 4
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

1→verify Phase 3 exit-gate PASS
2→spawn cross-model-validator via TeamCreate
  - agent reads validated candidates from workspace ## validation
  - agent runs them against GPT + Gemini via sigma-verify
  - agent reports transfer rates
3→monitor workspace ## cross-model for convergence

!phase-4-complete: cross-model-validator shows ✓
  advance to Phase 5

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

## §10 — Phase 6: Promotion + Archive

1→signal promotion-round to all agents
2→collect promotion candidates from workspace ## promotion
3→auto-promote: pattern-confirms-existing, calibration-self-update → agent memory
4→user-approve: present candidates to user, await approval
5→archive workspace to $T/shared/archive/{date}-{experiment-slug}.md
6→update sigma-mem with experiment outcomes (validated findings only, ¬speculative)

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
