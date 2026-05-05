---
name: API budget recovery steps
description: Three steps required to recover from Anthropic API budget exhaustion — adding credits alone is not sufficient
type: reference
---

When Anthropic API returns "You have reached your specified API usage limits":

1. **Add credits** — top up the prepaid balance
2. **Increase spend limit** — raise the monthly maximum under Plans & Billing → Usage Limits
3. **Reset the API key** — go to the specific API key in the console and reset it

All three are required. Steps 1-2 alone will NOT restore access — the key itself gets flagged and must be explicitly reset. Error message will keep showing the billing cycle reset date (e.g., "May 1") until the key is reset.

Verified 26.4.2 during sigma-optimize Exp 2 budget recovery.
