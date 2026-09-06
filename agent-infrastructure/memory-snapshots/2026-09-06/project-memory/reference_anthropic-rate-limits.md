---
name: Anthropic API rate limits
description: User's Anthropic API rate limits — applies to all Claude models, use for experiment pacing and concurrency planning
type: reference
---

All Claude models (Haiku, Sonnet, Opus):
- 1,000 requests per minute
- 450,000 input tokens per minute
- 90,000 output tokens per minute

**How to apply:** Use concurrent execution (asyncio) for experiment harnesses. 10 workers ≈ 100 RPM is safe. 20 workers hit the 90K output token/min limit (the actual binding constraint at ~350 tokens/response × 200 RPM = 70K tokens/min, close to limit). Serial execution at 1.3s delay = 46 RPM = 4.6% utilization (massive waste).

**Binding constraint is output tokens, not RPM.** With ~350 output tokens per Haiku response, the 90K/min limit caps effective throughput at ~257 calls/min. RPM limit (1K) is rarely reached. Exceeding the output token limit triggered a hard block that required API key reset to recover (see reference_api-budget-recovery.md).

Verified 26.4.2-26.4.3 during sigma-optimize Exp 2.
