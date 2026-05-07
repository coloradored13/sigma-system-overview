---
name: Gemini daily request quota
description: Gemini 3.1 Pro has 250 requests/day cap even on paid tier — plan cross-model experiments accordingly
type: reference
---

Google AI (Gemini) enforces a **250 requests per day per model** quota for gemini-3.1-pro, even on the paid tier. This is separate from per-minute rate limits.

At 120 calls per cross-model run (3 candidates × 4 tasks × 10 runs), a single cross-model validation nearly exhausts the daily quota. Two runs in one day will fail.

**How to apply:**
- Check Gemini quota before designing cross-model experiments: 250/day ÷ (candidates × tasks × runs)
- For experiments needing >250 Gemini calls, split across multiple days or use Gemini Flash (different model, separate quota)
- Retry-after header says ~11-15 hours — the quota resets daily, not on a rolling window
- Error type: 429 RESOURCE_EXHAUSTED (not 400 like Anthropic budget errors)

Discovered 26.4.3 during sigma-optimize Exp 2 cross-model validation. Gemini completed ~110/120 calls before hitting the cap.
