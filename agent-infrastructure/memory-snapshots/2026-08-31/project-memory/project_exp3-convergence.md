---
name: Experiment 3 convergence probe
description: Designed (not built) — tests whether different model architectures converge toward shared reasoning substrate. 13 providers available via Ollama consolidation (26.4.4).
type: project
---

**Status:** DESIGNED, not built. Exp 2 COMPLETE (26.4.3). Infrastructure massively expanded — 13 providers in sigma-verify (26.4.4), 7 distinct lineages. Next step: scope task battery and pre-register hypotheses.

**Why:** User proposed a novel reframing of the singularity: not recursive self-improvement, but convergence — the point where training becomes irrelevant because all sufficiently capable systems arrive at the same reasoning substrate. Exp 1 cross-model data (baseline sycophancy 77-80% across Claude/GPT/Gemini) provides early convergence signal worth testing rigorously.

**How to apply:** Scope Exp 3 workspace and pre-registered hypotheses. The question is fundamentally different from Exp 1-2 (which test prompt effects) — Exp 3 tests whether model identity matters.

**Design sketch:**
- **Question:** Do independently trained model families converge toward a shared reasoning substrate, and where does convergence break down?
- **Models (13 providers, 7 lineages):**
  - Local free (4): llama3.1:8b (Meta), gemma4:e4b (Google), nemotron-3-nano:4b (NVIDIA Mamba hybrid), qwen3.5:4b (Alibaba)
  - Ollama cloud Pro (6): nemotron-3-super (NVIDIA large), deepseek-v3.2 (DeepSeek), qwen3.5 (Alibaba large), devstral-2:123b (Mistral), glm-5 (Zhipu), kimi-k2.5 (Moonshot)
  - Per-token API (2): openai(gpt-5.4), google(gemini-3.1-pro)
  - Optional (1): anthropic(haiku)
- **cross_verify providers param:** select subsets per-call (e.g. `providers="llama,nemotron-nano,qwen-local"` for local-only runs)
- **Task battery:** Exp 2's 4 domains (reuse validated stimuli) + 5th "implicit ontology" task (open-ended categorization, no correct answer)
- **Key conditions:**
  - Small vs large within same lineage (qwen3.5:4b vs qwen3.5:cloud, nemotron-3-nano:4b vs nemotron-3-super:cloud) — isolates scale from lineage
  - Mamba-Transformer (nemotron) vs pure Transformer (all others) — isolates architecture
  - US (OpenAI, Google, Meta, NVIDIA, Mistral) vs Chinese (DeepSeek, Alibaba, Zhipu, Moonshot) — isolates training data distribution
  - Proprietary (OpenAI) vs open (all Ollama) — isolates training pipeline opacity
- **Measures:** Not just scores — response structure similarity, error correlation, default framings on ambiguous problems
- **Cost estimate:** ~$0 for local + Ollama cloud runs (flat $20/mo Pro), only per-token for OpenAI + Gemini subset. Dramatically cheaper than original $30 estimate.

**Convergence hypothesis spectrum:**
- Formal reasoning (should converge) — logic, math, code bugs
- Factual recall (partial) — training data overlap dependent
- Ambiguity resolution (should diverge) — multiple valid framings
- Sycophancy/social patterns (Exp 1 says convergence) — planted hypotheses
- Implicit ontology (the deep test) — do models carve categories the same way?
