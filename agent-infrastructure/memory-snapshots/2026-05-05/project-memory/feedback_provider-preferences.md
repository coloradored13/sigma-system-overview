---
name: provider preferences
description: Ollama Pro ($20/mo) is primary for 10 providers. OpenRouter ($10 credit) is paid fallback for Llama/Nemotron. OpenAI + Gemini per-token. ¬Together AI. ¬Fireworks.
type: feedback
---

Primary infrastructure is Ollama Pro ($20/mo flat) — covers 8 Ollama-backed providers (4 local + 6 cloud) at zero per-call cost. OpenAI and Gemini remain per-token APIs. Anthropic (Opus 4.6) is per-token optional.

**Why:** User consolidated from per-token OpenRouter/Fireworks to Ollama Pro for cost predictability. OpenRouter retained as fallback with $10 credit for Llama 4 Maverick and Nemotron-3-Super when Ollama is unavailable.

**How to apply:**
- Default: all providers via Ollama (local + cloud). No env vars needed.
- OpenRouter fallback: set `LLAMA_PROVIDER=openrouter` or `NEMOTRON_PROVIDER=openrouter`
- OPENROUTER_API_KEY in ~/.claude.json sigma-verify MCP env
- ¬Together AI (user rejected)
- ¬Fireworks (removed, limited free tier)
