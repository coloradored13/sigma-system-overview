---
name: Subscription vs per-token cost model
description: What's covered by Claude Code subscription vs what hits per-token APIs in sigma sessions — to avoid mis-framing budget conversations
type: reference
originSessionId: 6b9f49a0-c5ab-4066-aa61-f641e5a32a77
---
In sigma-review and sigma-build sessions, cost is NOT proportional to token volume across all components. The split:

**Subscription-covered (no per-call cost):**
- Lead orchestration (Claude Code session, any model)
- All spawned agents via TeamCreate (Sonnet, Opus, Haiku — the agent layer)
- Background work (memory recall, file reads, hook execution)

**Per-token (actual API spend):**
- XVERIFY calls to per-token providers: `openai` (gpt-5.4) and `google` (gemini-3.1-pro). These are the only paid XVERIFY providers when cross-model verification fires.
- XVERIFY anthropic provider would also be per-token API (sigma-verify routes through MCP, not subscription) — but excluded by the cross-model integrity rule (see feedback_xverify-anthropic-excluded.md).

**Subscription-covered XVERIFY providers:**
- 4 local Ollama models (llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, qwen3.5:4b) — runs on user hardware
- 6 Ollama Cloud Pro models (nemotron, deepseek, qwen, devstral, glm, kimi) — covered by Ollama Pro subscription

**Implication for budget conversations:**
- Adding agents to a sigma-build roster has near-zero marginal cost — agents run on subscription.
- "Approve C1 only first" is a *quality* checkpoint, not a *cost* lever.
- The only real cost knob is XVERIFY provider mix: paid frontier (openai + google) vs free (Ollama local + cloud pro).
- A full TIER-3 sigma-build typically costs $1-5 per-token, not the $10-15 estimated when modeling all token use as API spend.

**Mistake to avoid:** Estimating sigma-build cost by modeling all agent + lead tokens as Claude API per-token billing. That's the wrong cost model and makes sigma-builds look ~10x more expensive than they actually are.

Established 2026-04-23 after user correction during R19 remediation C1 preflight.
