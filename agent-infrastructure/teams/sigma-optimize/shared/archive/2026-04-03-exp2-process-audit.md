# Experiment 2 Process Audit — 2026-04-03

## Process Failures (framework violated its own rules)

### 1. Lead ran experiments directly (§1 violation)
§1: "lead MUST NOT execute experiment.py, ablation.py, or any scoring code directly." Lead ran both search experiments and combinatorial via nohup. User authorized override due to agent execution failures. Contamination risk mitigated (lead didn't analyze raw results), but provenance chain broken.

### 2. Agents failed to execute long-running experiments
Framework assumes agents can run multi-hour processes. They can't — the Bash TOOL within agents has a hard 10-min max timeout (600,000ms). At serial speed (~67 min/gen), a single generation exceeded this limit. The agents themselves (spawned via TeamCreate) had no time constraint, but their tool calls did.

### 3. Search agents spawned and killed multiple times
Conservative agent: spawned → failed → respawned → sent corrective messages → shut down → respawned. Same for aggressive. The "clean spawn with context firewall" model broke down. Agents saw partial state from prior attempts.

### 4. Conservative search ran with wrong parameters
Due to execution failures, lead ran conservative at N=3/task as a compromise. The agent later ran its own N=10 version (mostly API errors). Final clean N=10 run happened much later after concurrent harness was built. Three different conservative datasets existed at various points.

### 5. Lead interpreted patterns mid-experiment (§0 violation)
User asked about findings; lead commented on token duplication patterns, competing prompt architectures, etc. User caught this and flagged it. Per §0, lead should have refused to interpret. Risk: interpretations could leak into agent instructions for later phases.

### 6. Combinatorial burned $15 on garbage data
Combinatorial agent ran 160 candidates but 84% scored -5 (budget exhaustion errors). No budget guard existed yet. The harness had no mechanism to detect or stop on budget errors. All 6,400 calls were wasted.

### 7. Cross-agent independence never tested
§2 requires search-conservative and search-aggressive to write findings independently before reading each other. Since lead ran both experiments, there was no independence to enforce. Agents that wrote workspace findings read lead-generated result JSONs, not each other's sections.

### 8. Promotion round incomplete
sigma-mem store tools (store_agent_memory, store_team_decision, store_team_pattern) weren't available to several agents. Promotion candidates written to workspace but not persisted to team memory.

### 9. Orchestrator state diverged from reality
Orchestrator thought we were in "parallel_search" while lead was manually running experiments via nohup. Phase transitions manually forced with advance commands rather than triggered by agent convergence declarations.

### 10. §4b agent spawn template not followed
Skill defines a specific spawn template (§4b) with context firewall, ΣComm protocol, boot sequence. Later agents (statistical-analyst, cross-model-validator, synthesis-writer) got custom prompts. Context firewall concept was preserved but standardized format wasn't.

---

## New Findings (operational improvements for future experiments)

### Execution Infrastructure

1. **Concurrent evaluation is essential.** Serial API calls = 4.6% utilization. 10 async workers = ~100 RPM, 25× speedup (67 min/gen → 3 min/gen). Should be the default harness mode, not an upgrade.

2. **Per-generation checkpointing.** `--resume --gen-limit` prevents losing work on crashes/timeouts. Each gen saves population state, generation history, RNG state. Worked well once built.

3. **Budget pause/resume > hard crash.** asyncio.Event gate + RESUME file lets workers pause on budget exhaustion instead of recording -5 scores. Built but never cleanly triggered in production — needs testing.

4. **Budget error detection.** `_is_budget_error()` catches the specific Anthropic error message ("you have reached your specified API usage limits"). Without this, budget errors fell through to generic exception handling and silently produced -5 scores across hundreds of calls.

5. **Per-provider incremental saves.** Cross-model script writes results only at completion. When Gemini hung, all OpenAI data (120 complete calls) was lost. Should save after each provider completes.

6. **External provider timeouts.** Gemini API calls hung indefinitely without a timeout. Added 90s signal.alarm, but this doesn't work with async. Needs proper asyncio.wait_for.

7. **Client reuse.** Cross-model script created a new OpenAI/Gemini client per API call. Should use module-level singletons.

8. **nohup + poll is the reliable pattern.** For any process exceeding 10-min Bash timeout, nohup with log file polling is the only reliable execution method from within Claude Code.

### API/Provider Management

9. **API key reset required for recovery.** Three steps to recover from Anthropic budget exhaustion: (1) add credits, (2) increase spend limit, (3) reset the specific API key in the console. Steps 1-2 alone don't work.

10. **Output token limit is the binding constraint.** 90K output tokens/min, not the 1K RPM limit. At ~350 tokens/response, effective cap is ~257 calls/min. 20 workers exceeded this and triggered a hard block requiring key reset.

11. **Gemini daily quota: 250 req/day.** Even on paid tier, gemini-3.1-pro has a 250 requests/day cap per model. Must check provider quotas before designing cross-model experiments.

12. **Sequential execution for shared rate limits.** Two agents sharing one API key = thundering herd at rate limits. Always run search agents sequentially when sharing credentials.

### Experimental Design

13. **Tier-matched cross-model testing.** Haiku (small) vs GPT-5.4 (top) vs Gemini Pro (top) is unfair. Search on Haiku (cheap), validate on Sonnet, cross-model against peer-tier models.

14. **Rubric calibration is model-specific.** Mechanical regex rubrics measure vocabulary alignment with the model they were developed on. Cross-model testing needs model-agnostic scoring (LLM-judged or behavioral metrics like planted-hypothesis acceptance).

15. **Search-phase score inflation.** Structured candidates regressed -0.414 from search to validation. Baselines regressed -0.046. Search-phase scores systematically overestimate true performance. N=10 is better than N=5 but still inflates.

### Agent Execution Model

16. **TeamCreate agents work if harness fits Bash constraints.** The agents themselves have no time limit — the Bash tool calls do (10 min max). With concurrent eval (~3 min/gen), agents can run `--gen-limit 1 --resume` repeatedly and complete full experiments. The fix (concurrent eval + checkpointing) makes TeamCreate viable.

17. **Agents never interacted with each other.** The workspace acted as a serial handoff document, not a collaboration space. No inbox communication, no dialectical rounds, no peer challenges. For sigma-optimize's sequential phase structure, this may be correct — but it's worth evaluating whether combinatorial + statistical-analyst could benefit from interaction.

---

## Root Cause Analysis

The cascade of failures traces to one root cause: **the experiment harness was designed for human execution speed, not agent execution constraints.** Each API call takes ~5s (Haiku generating 350 tokens against long stimuli). At serial speed, one generation = 800 calls × 5s = 67 minutes — far exceeding the 10-min Bash timeout that agents operate within.

Everything else followed: agents failed → lead took over (§1 violation) → no agent independence → no workspace-mediated communication → orchestrator diverged → manual phase transitions.

The concurrent harness fix (asyncio, 10 workers, ~3 min/gen) resolves the root cause. With this in place from the start, agents could have run the full experiment within Bash timeout constraints, preserving the contamination firewall and agent independence.

---

## Session Cost

| Phase | API Calls | Est. Cost | Notes |
|-------|-----------|-----------|-------|
| Conservative (multiple runs) | ~10,000 | ~$16 | Includes failed N=3 run, agent N=10 run (mostly errors), final clean N=10 run |
| Aggressive | ~6,560 | ~$10 | 6 serial gens + 4 concurrent gens |
| Combinatorial (failed) | ~6,400 | ~$10 | 84% errors, $15 wasted |
| Combinatorial (clean) | ~6,400 | ~$10 | Full 160 candidates |
| Validation (N=20 + N=40) | ~920 | ~$1.5 | Clean |
| Cross-model (OpenAI+Gemini) | ~480 | ~$3 | Includes redundant re-run |
| Smoke tests/debugging | ~200 | ~$0.3 | |
| **Total** | **~31,000** | **~$51** | ~$25 wasted on failed runs |

Roughly half the budget was wasted on failed attempts. With the concurrent harness from the start, total would have been ~$25.
