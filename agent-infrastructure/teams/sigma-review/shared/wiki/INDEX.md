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

- [sigma-predict Architecture](sigma-predict-architecture.md) — LLMRouter client cache fix, PROVIDERS registry integration, deliberation hardcode fix, open defects (BUILD-R1/R3/R4/R5), known tech debt [B7, 26.4.13]
- [sigma-predict Prediction Methodology](sigma-predict-prediction-methodology.md) — parse_failed contamination, reference class instance count, falsification anchors, source clustering, hedging correction conditioning, multiplicative guard, BELIEF scores [B7, 26.4.13]
- [sigma-predict Validation Gates](sigma-predict-validation-gates.md) — PipelineValidator 5-gate architecture, non-blocking default, strict mode, gate descriptions [B7, 26.4.13]
- [Audit Logging Pattern](audit-logging-pattern.md) — JSON-L per-call log, hash-of-params, cross-system comparison (ollama-mcp-bridge fsync vs sigma-predict buffered), BUILD-R4 wiring gap [B6+B7, 26.4.13]

- [Enterprise AI Rollout — Financial Services](enterprise-ai-rollout-finserv.md) — four conditions model, SR 11-7 compliance architecture, compliance x adoption heuristic, ROI calibration (P=0.35 18mo), survivorship bias, cognitive biases in vendor selection, timeline base rates, pre-mortem taxonomy, measurement debiasing [R18, 26.4.16]

- [Sigma-Build Infrastructure Architecture](sigma-build-infrastructure-architecture.md) — chain-evaluator A12 grace + A20/A22/A23 WARN+CAL-EMIT + A24 sigma-verify pre-flight + A3 layered authority; phase-gate BLOCK 4 sed-i + shlex; multi-layer contract drift pattern (4 instances) [B-r19-remediation, 26.4.25]
- [β+ Calibration Pattern](beta-plus-calibration-pattern.md) — WARN-first gate-promotion, CAL-EMIT schema, 3-reviews/20%-FP/5-DA-verdicted thresholds, producer/consumer schema-decoupling failure mode, regression-lock pre-flight pattern [B-r19-remediation, 26.4.25]
- [workspace_write Contract](workspace-write-contract.md) — IC[6] signature, anchor-presence + no-op double-guard against PM[4], section-isolation convention, 67 production writes / 0 anchor failures, recursive-self-reference anti-pattern [B-r19-remediation, 26.4.25]
- [Premise-Audit Step 7a](premise-audit-step-7a.md) — pre-dispatch anti-anchoring, PA[1-4] template, sequence constraint at c1-plan.md:62, chain-eval BLOCK day-one, BUILD/ANALYZE split, self-application bootstrap exception [B-r19-remediation, 26.4.25]

## Convention
- One page per entity, domain, or topic that appears across reviews or warrants standalone reference
- Page filenames: lowercase, hyphenated (e.g., `loan-admin-tech-landscape.md`, `alter-domus.md`)
- Granularity is emergent — start broad, split pages when they get unwieldy
