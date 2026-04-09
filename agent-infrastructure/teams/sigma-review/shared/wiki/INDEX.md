# Sigma-Review Knowledge Wiki

Persistent, compiled domain knowledge from sigma-review analyses. Each page is updated incrementally across reviews — the wiki compounds, individual reviews don't.

## How This Works
- After each review's synthesis, a compilation agent reads findings and integrates them here
- Every claim is attributed to its source review: `[R{number}, {date}]`
- Contradictions between reviews are preserved, not silently resolved
- Process observations go in `patterns.md`, not here — this wiki is domain knowledge only

## Pages

- [ollama-mcp-bridge Security Architecture](ollama-mcp-bridge-security-architecture.md) — SecurityGateway chokepoint, SafePath/SafeURL/SafeRecipient adapters, policy-surface vs enforcement-surface, ToolState lifecycle, field-name gate, dormant field pattern, known limitations [B6, 26.4.9]
- [SIGMA-COMM-WIRE Protocol](sigma-comm-wire-protocol.md) — v0.1.0 spec: envelope schema, 9 message types, epistemic_type enum, belief_state_form, convergence_state, error taxonomy, schema evolution rules [R16, 26.4.9]
- [Cross-Model Protocol Calibration](cross-model-protocol-calibration.md) — bootstrap reliability by interface mode, format choice rationale, adoption risk pre-mortem, empirical gaps, hypothesis dispositions [R16, 26.4.9]

## Convention
- One page per entity, domain, or topic that appears across reviews or warrants standalone reference
- Page filenames: lowercase, hyphenated (e.g., `loan-admin-tech-landscape.md`, `alter-domus.md`)
- Granularity is emergent — start broad, split pages when they get unwieldy
