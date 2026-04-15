---
name: ΣComm translator deferred
description: Q2 ΣComm bidirectional translator designed in F1 but deferred pending empirical validation — build gated on small-model test
type: project
---

ΣComm bidirectional translator (SigmaCommTranslator) fully designed in F1 build (26.4.8) but deferred by DA challenge DA[1]: no empirical evidence small models (llama3.1:8b, gemma4:e4b) produce usable output with expanded ΣComm notation.

**Why:** DA falsifiability challenge — building 300-400 LOC of new attack surface (injection via expansion) for an unvalidated premise. Tech-architect conceded deferral pending test.

**How to apply:**
- Validation test: send manually-expanded ΣComm spawn prompt to llama3.1:8b via existing Bridge, check tool coherence. Zero new code needed.
- Architecture locked in F1 workspace (ADR[2], IC[1-2], SR[3-4]): SigmaCommTranslator class, Layer 4 placement, post-sanitization/pre-model-context, SigmaCommConfig(enabled, expand_inbound, compress_outbound)
- If test passes → build from locked ADR[2]. If fails → redesign or drop.
- Archive: ~/.claude/teams/sigma-review/shared/archive/ (26.4.8 F1 build workspace)
