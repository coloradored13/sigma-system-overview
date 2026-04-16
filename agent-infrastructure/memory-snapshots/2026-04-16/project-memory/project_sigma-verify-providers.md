---
name: sigma-verify provider architecture
description: sigma-verify 13 providers — 4 local Ollama + 6 Ollama cloud Pro + 2 per-token (OpenAI + Gemini) + 1 optional (Anthropic). Expanded 26.4.5.
type: project
---

**Status:** COMPLETE. 13 providers active, verified via `sigma-verify init` (26.4.5). Pushed to coloradored13/sigma-verify (26.4.4 base, providers expanded since).

**Why:** Cross-model verification needs diverse architectures and lineages. Ollama Pro ($20/mo flat) provides 6 cloud providers at zero per-call cost. Local models provide free, unlimited verification. 7 distinct model lineages for Exp 3 convergence testing.

**How to apply:** `sigma-verify init` auto-detects all available providers. Ollama pre-flight auto-starts the server if needed. All Ollama providers (local + cloud) are always available when Ollama is running.

**Providers (13):**
| Provider | Model | Backend | Cost |
|----------|-------|---------|------|
| `openai` | GPT-5.4 | OpenAI API (per-token) | ~$0.002-0.01/call |
| `google` | Gemini 3.1 Pro Preview | Google API (per-token) | ~$0.001-0.003/call |
| `llama` | llama3.1:8b | Ollama local | free |
| `gemma` | gemma4:e4b | Ollama local | free |
| `nemotron-nano` | nemotron-3-nano:4b | Ollama local | free |
| `qwen-local` | qwen3.5:4b | Ollama local | free |
| `nemotron` | nemotron-3-super:cloud | Ollama cloud | included in Pro |
| `deepseek` | deepseek-v3.2:cloud | Ollama cloud | included in Pro |
| `qwen` | qwen3.5:cloud | Ollama cloud | included in Pro |
| `devstral` | devstral-2:123b-cloud | Ollama cloud (Mistral AI) | included in Pro |
| `glm` | glm-5:cloud | Ollama cloud (Zhipu AI) | included in Pro |
| `kimi` | kimi-k2.5:cloud | Ollama cloud (Moonshot AI) | included in Pro |
| `anthropic` | claude-opus-4-6 | Anthropic API (optional) | ~$0.001-0.005/call |

**Reasoning tiers available:** openai (gpt-5.4-pro), google (gemini thinking mode), anthropic (extended thinking). All others standard only.

**Infrastructure:** Ollama 0.20.2 Pro subscription ($20/mo). Pre-flight auto-start + health check on init/cross_verify.

**Expansion history:**
- 26.4.4: Base 8 providers (openai, google, llama, gemma, nemotron, deepseek, qwen, anthropic). Removed OpenRouter, Fireworks, NVIDIA NIM.
- 26.4.5: +5 providers (devstral, glm, kimi, nemotron-nano, qwen-local). Total: 13.

**MCP config:** OPENAI_API_KEY, GOOGLE_AI_API_KEY in `~/.claude.json` under mcpServers.sigma-verify.env. Ollama providers need no API keys.
