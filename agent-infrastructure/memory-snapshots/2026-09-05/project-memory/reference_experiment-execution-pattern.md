---
name: Experiment execution pattern
description: Proven pattern for running long API experiments — concurrent eval, checkpointing, budget pause, nohup. Learned from sigma-optimize Exp 2 failures.
type: reference
---

Correct pattern for running API-intensive experiments (1000+ calls):

**Harness requirements:**
1. **Concurrent evaluation** (asyncio + semaphore) — 10 workers ≈ 100 RPM, 25x faster than serial. Worker count tuned to output token limit (90K/min), not RPM limit.
2. **Per-generation checkpointing** (`--resume --gen-limit N`) — saves state after each generation. Process can crash/timeout without losing work. Agent runs one gen at a time within Bash 10-min timeout.
3. **Budget pause/resume** — asyncio.Event gate + `touch results/RESUME` file. Workers pause on budget error, resume when file appears. No -5 error scores, no wasted money.
4. **Budget error detection** — catch "usage limit" / "you have reached your specified" in error messages. Propagate as BudgetExhaustedError or clear the pause gate.
5. **Per-provider incremental saves** — write results after each provider completes, not only at the end. Prevents losing completed provider data when a later provider hangs.
6. **Connection timeouts** — 60s on Anthropic SDK, 90s signal.alarm on external providers (Gemini/OpenAI). Prevent indefinite hangs.
7. **Client reuse** — module-level singleton clients, not per-call instantiation.

**Execution pattern:**
- `nohup python3 -u experiment.py --resume > results/log.txt 2>&1 &`
- Poll `tail -5 results/log.txt` for progress
- Check `results/checkpoint-*.json` for generation completion
- If budget pauses: user tops up, then `touch results/RESUME`

**Agent compatibility:**
- With concurrent eval (~3 min/gen), TeamCreate agents CAN run experiments via `Bash(python3 experiment.py --gen-limit 1 --resume)` within the 10-min timeout
- Without concurrent eval (serial, ~67 min/gen), agents CANNOT hold the process — use nohup from lead instead
- Always run search agents SEQUENTIALLY when sharing an API key — parallel agents cause thundering herd at rate limits

**Cross-model specifics:**
- Tier-match models: search on Haiku (cheap), validate on Sonnet, cross-model against peer-tier (GPT-5.4, Gemini Pro, not Haiku vs frontier)
- Gemini: 250 req/day quota per model (see reference_gemini-daily-quota.md)
- Gemini: needs max_output_tokens ≥ 1000 (tokenizer produces shorter text at same token count)
- Rubrics are model-specific: mechanical regex measures vocabulary alignment with the model it was calibrated on. Cross-model needs model-agnostic scoring (LLM-judged or behavioral metrics)

Established 26.4.2-26.4.3 from sigma-optimize Exp 2 operational failures.
