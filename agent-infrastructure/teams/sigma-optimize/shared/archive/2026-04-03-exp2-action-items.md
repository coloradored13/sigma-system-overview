# Experiment 2 Action Items — 2026-04-03

## Priority 1: Do before Exp 3

### A1. Make concurrent eval the default harness mode
- experiment_multi.py already has evaluate_batch with asyncio
- Set MAX_WORKERS=10 as default (safe under 90K output token/min limit)
- Remove serial evaluate() from the main loop — keep only as fallback import for other scripts
- **Why**: root cause of all agent execution failures

### A2. Add per-provider incremental saves to cross_model_multi.py
- Save results JSON after each provider completes (not only at end)
- On crash/kill, partial data is preserved
- **Why**: lost 120 complete OpenAI calls when Gemini hung

### A3. Test budget pause/resume end-to-end
- The asyncio.Event + RESUME file mechanism was built but never triggered cleanly
- Write a test that simulates budget error mid-batch and verifies workers pause + resume
- **Why**: built in panic, never validated

### A4. Add asyncio.wait_for timeout to external provider calls
- Current signal.alarm doesn't work with async
- Replace with `asyncio.wait_for(call(), timeout=90)` pattern
- **Why**: Gemini hung indefinitely, killed the process

### A5. Build provider quota pre-check
- Before cross-model experiments, query each provider's remaining quota
- Gemini: check daily request count vs 250 limit
- Anthropic: estimate cost from call count × avg tokens, compare to remaining budget
- **Why**: hit Gemini 250/day and Anthropic budget mid-experiment without warning

### A6. Tier-matched model selection for cross-model
- Add a MODEL_TIERS config to the harness
- Search tier: Haiku (cheap, high volume)
- Validation tier: Sonnet (peer to GPT-5.4/Gemini Pro)
- Cross-model tier: matched across providers (Sonnet ↔ GPT-5.4 ↔ Gemini Pro)
- **Why**: comparing Haiku to GPT-5.4 is apples to expensive apples

## Priority 2: Framework improvements

### B1. Update SKILL.md §5 to account for Bash timeout
- Add note: each gen must complete within 10 min (Bash tool limit)
- Require concurrent eval for multi-task experiments
- Agent instructions should use `--gen-limit 1 --resume` pattern
- **Why**: framework assumed agents could run multi-hour processes

### B2. Add model-agnostic scoring option
- LLM-judged evaluation as alternative to regex scoring
- Or: behavioral metrics only (planted-hypothesis acceptance rate) for cross-model
- Regex rubrics are fine for single-model search, but cross-model needs agnostic scoring
- **Why**: Gemini scored 0 on correct analyses because vocabulary didn't match regex

### B3. Reduce §1 lead contamination surface
- The current rules assume agents execute everything. When lead must execute (API constraints), define what's acceptable:
  - Lead CAN: run scripts, launch nohup processes, poll logs for completion status
  - Lead CANNOT: read result JSONs, interpret score patterns, comment on preliminary findings
- Add explicit "lead-as-execution-layer" exception with boundaries
- **Why**: §1 was written for a world where agents handle execution; reality required lead involvement

### B4. Add regression-to-mean warning to search output
- Print warning when search-phase best exceeds baseline by <1.0 points
- "Search-phase advantage of +X.XX is within typical regression-to-mean range (0.3-0.5 points). Validate at N≥20 before drawing conclusions."
- **Why**: search consistently overestimates by 0.4+ points

### B5. Fix seed contamination in conservative search
- Remove ΣComm operators from conservative seed population (Tier 3 seeds)
- Or: explicitly label conservative search as "natural-language + structural operators" (honest framing)
- **Why**: ΣComm operators leaked in via seeds, making conservative-vs-aggressive comparison unclean

## Priority 3: Nice to have

### C1. Add cost estimator to harness
- Before launching: print estimated API cost based on (candidates × runs × tasks × avg_tokens × price)
- Warn if estimated cost > $10
- **Why**: would have caught the $15 garbage combinatorial run

### C2. Agent interaction for analysis phases
- Evaluate whether combinatorial + statistical-analyst would benefit from interaction
- Currently pure serial handoff — combinatorial writes, analyst reads
- Possible: analyst challenges combinatorial's combination matrix before running
- **Why**: agents never communicated despite framework supporting it

### C3. Workspace-driven orchestrator (not manual)
- Orchestrator should read workspace ## convergence for ✓ declarations
- Auto-advance when all required agents have converged
- Remove manual `advance --context` calls
- **Why**: orchestrator state diverged from reality when phases were manually managed

### C4. Add output-token-aware throttling
- Track cumulative output tokens per minute
- Slow down or pause workers when approaching 90K/min limit
- Currently only RPM-aware (via semaphore count), not token-aware
- **Why**: 20 workers exceeded output token limit and triggered hard block
