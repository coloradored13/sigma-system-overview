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
- [Loan Admin Tech Landscape](loan-admin-tech-landscape.md) — incumbent platforms (SyndTrak/Intralinks/Debt Domain), AmendX/DataXchange launches, CME SOFR waiver expired April 1 2026, payment waterfall completeness [R17, 26.4.9]
- [Trust Charter Regulatory Path](trust-charter-regulatory-path.md) — OCC "most favorable decade" (P=65-75% 4-6mo), CRD6 93-day grandfathering window (cutoff July 11 2026), Basel III capital-reducing (tailwind), HMRC April 5 deadline passed [R17, 26.4.9]
- [Private Credit Market](private-credit-market.md) — AUM $3-3.5T broad / ~$2T narrow, BDC bear-as-base (BELIEF=0.88), mandate mix shift, calibrated breakeven 36-48mo, capital $30-55M realistic [R17, 26.4.9]
- [Key Competitors — Loan Administration](key-competitors-loan-admin.md) — Alter Domus (Cinven-backed, corrected from Bain), GLAS reference class, Kroll APAC, Hypercore (no charter), competitive window 12-18mo XVERIFY confirmed, 3 entry paths [R17, 26.4.9]

## Convention
- One page per entity, domain, or topic that appears across reviews or warrants standalone reference
- Page filenames: lowercase, hyphenated (e.g., `loan-admin-tech-landscape.md`, `alter-domus.md`)
- Granularity is emergent — start broad, split pages when they get unwieldy
