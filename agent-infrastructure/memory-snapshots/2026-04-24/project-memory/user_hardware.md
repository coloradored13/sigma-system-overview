---
name: user hardware
description: MacBook Air M3 16GB — runs 4B-12B local models via Ollama. Four models: llama3.1:8b, gemma4:e4b, nemotron-3-nano:4b, qwen3.5:4b.
type: user
---

User's development machine: MacBook Air, Apple M3 chip, 16GB RAM.

**Local models installed (Ollama 0.20.2 Pro, verified 26.4.4):**
- `llama3.1:8b` — Meta Llama 3.1 8B (pulled 26.4.2)
- `gemma4:e4b` — Google Gemma 4 E4B (pulled 26.4.4)
- `nemotron-3-nano:4b` — NVIDIA Nemotron-3-Nano 4B, Mamba-Transformer hybrid (pulled 26.4.4)
- `qwen3.5:4b` — Alibaba Qwen 3.5 4B, multilingual (pulled 26.4.4)

**How to apply:**
- Local LLM inference limited to ~8-12B parameter models. 70B models need ~40GB RAM, won't fit.
- Ollama API available at `http://localhost:11434` (OpenAI-compatible at `/v1`)
- Both models usable as sigma-verify local providers (zero cost, no rate limits, no API key)
- For frontier-scale experiments (70B+), use API providers (OpenRouter preferred, Fireworks as fallback)
- Q5_K_M quantization recommended over Q4 for 16GB — retains more quality at acceptable speed
- Expect 15-28 tok/s on 8B models
- Gemma 4 E4B generally benchmarks stronger than Llama 3.1 8B at similar size class
