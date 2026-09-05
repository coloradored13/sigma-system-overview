---
name: F1 build patterns
description: 6 patterns promoted from ollama-mcp-bridge F1 build (26.4.8) — IP normalization, HARDENED enforcement, empirical gates, multi-agent convergence, parallel engineers, model_copy
type: project
---

Patterns from F1 build (5 agents, TIER-2, DA PASS A-, 810 tests):

1. **normalize_and_validate_ip() pattern**: standalone function for IP bypass defense covering 6 encoding forms (decimal, hex, octal, percent-encoded, IPv4-mapped IPv6, non-URL host+port). Post-urlparse, returns typed IPv4/IPv6 or None. Reusable across any Python URL policy enforcement.

2. **Named profile enforcement gap**: HARDENED profile checked 2 booleans while implying full policy coverage. Pattern: named security profiles MUST mechanically enforce their promises — profile-name > enforcement-scope mismatch is a silent security gap.

3. **Empirical validation gate**: DA[1] deferred highest-complexity feature by asking "has anyone tested the premise?" Building 300-400 LOC of new attack surface for an unvalidated assumption = wrong. Test BEFORE build for keystone features.

4. **Multi-agent code-read convergence**: 4 agents independently found same 6+ IP bypass vectors reading same code path. Independent confirmation > single-agent review for security findings. Multi-agent code-read is highest-confidence security pattern.

5. **Parallel implementation engineers**: SQ[] independence → worktree isolation → merge step. User-identified during F1 build. Naming: implementation-engineer-1, -2, -N. Code-quality-analyst owns merge integration. Saves build time on TIER-2+.

6. **model_copy(update=) for frozen Pydantic**: Idiomatic Pydantic v2 pattern for overwriting fields on frozen models in exception handlers. Used for MaxTurnsError → RECOVERY_REQUIRED signal on last ToolCallRecord.
