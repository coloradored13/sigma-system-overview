---
name: XVERIFY excludes Anthropic providers
description: Cross-model verification (XVERIFY / sigma-verify) must exclude Anthropic-family models — Claude verifying Claude isn't a cross-model check
type: feedback
originSessionId: 6b9f49a0-c5ab-4066-aa61-f641e5a32a77
---
XVERIFY (sigma-verify) provider selection MUST exclude `anthropic` provider entries (claude-opus-4-6, etc.). The point of cross-model verification is architectural diversity — Claude verifying Claude provides no independent check.

**Why:** XVERIFY exists to surface dissent that single-architecture reasoning misses. Same-family verification is a no-op signal. Including it pollutes the dissent count and gives false-positive convergence ("3-of-3 agree" when 1 of those 3 is structurally identical to the source).

**How to apply:**
- Plan-track agents calling `verify_finding` or `cross_verify`: must specify `providers` parameter excluding `anthropic`. Default to mix of frontier paid (openai, google) + Ollama-architecture-distinct (deepseek, glm, kimi, nemotron, qwen).
- DA agents calling XVERIFY for severity calibration: same rule.
- When the durable fix lands (sigma-verify MCP default-excludes anthropic), this guidance can lift — until then, enforce in spawn prompts and review.
- This rule applies even when budget would allow anthropic — cheapness doesn't justify a useless data point.

Established 2026-04-23 during R19 remediation sigma-build C1 preflight.
