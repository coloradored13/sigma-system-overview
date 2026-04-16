# Enterprise AI Rollout — Financial Services

Domain knowledge compiled from sigma-review ANALYZE R18, 2026-04-16.

## Four Conditions for Enterprise AI Success
[R18, 26.4.16] Enterprise AI rollout success requires four necessary conditions (not sequential gates): data readiness, use-case fit, compliance adequacy, adoption quality. Revised from three-gate model under DA challenge — evidence supports factor importance but not sequential ordering. Data readiness is most commonly skipped pre-assessment and #1 abandonment cause (Gartner 60%, Informatica CDO 43%). Planning heuristic, not causal model.

## Financial Services Compliance Architecture
[R18, 26.4.16] SR 11-7 (OCC/Fed model risk management) explicitly extended to generative AI per GAO-25-107197 (2025). Enterprise obligations: document model purpose/limitations, perform own validation (not rely on vendor attestations), establish audit trails for AI-assisted material decisions, ensure explainability for regulatory examination. SOC II Type II = floor not ceiling. Vendors provide partial artifacts; enterprise builds governance layer on top.

## Vendor Evaluation — Compliance x Adoption Heuristic
[R18, 26.4.16] COMPLIANCE-FLOOR x ADOPTION-LIKELIHOOD > COMPLIANCE-CEILING. A compliant tool with low adoption delivers less compliance value than a slightly-less-compliant tool with high adoption. M365 Copilot case study: compliance boundary is real but NPS -24.1, 64% users inactive, CEO admitted integrations "don't really work," DLP bypass vulnerability Jan-Feb 2026. Compliance architecture nobody uses = zero value. Always pair compliance check with effectiveness/adoption check.

## Data Residency Seam Cost
[R18, 26.4.16] Multi-vendor AI strategies generate non-linear compliance overhead at integration boundaries. Each vendor seam requires separate data flow mapping + DLP enforcement + compliance validation. When Claude routes through M365 Copilot Co-Work, data exits Microsoft compliance boundary to Anthropic US datacenters — excluded from in-country residency commitments. Single-vendor reuses existing governance.

## ROI Calibration — Enterprise AI
[R18, 26.4.16] Base rate: 5-25% of enterprise AI deployments produce measurable ROI. Conditional (pre-defined metrics + exec sponsorship + success criteria): 35-50% at 24mo. Finserv knowledge-work calibrated: P(measurable ROI 18mo) = 0.35, 80% CI [0.20, 0.55]. Drops to 0.15-0.25 without confirmed data readiness. Only 13% of successful implementations deliver payback within 12 months (Deloitte Oct 2025, N=1,854). Sources: MIT/Fortune Aug 2025 (5%), NTT DATA/RAND (70-85% fail expected outcomes), IBM 2026 (29% measure ROI confidently).

## Survivorship Bias in Finserv AI Benchmarks
[R18, 26.4.16] JPMorgan ($1.5B value, 200K employees) is survivorship-biased outlier: $15B+ annual tech budget, 1,500+ AI/ML specialists, CEO-level mandate. Using as comparable for mid-size finserv = analogous to Amazon as retail digital transformation comparable. Goldman Sachs GS AI Assistant (focused use case, controlled rollout) is more replicable. Failed finserv AI deployments are not publicized.

## Cognitive Biases in AI Vendor Selection
[R18, 26.4.16] Five documented biases with structural interventions: (1) availability bias → use-case definition before vendor demos, (2) recency bias → capability floors not ceilings (benchmarks change quarterly, floors are stable), (3) anchoring → randomize demo order + independent scoring before discussion, (4) sunk cost ($7.2M avg abandoned) → pre-commit exit criteria before contract, (5) authority bias → finserv reference interviews not generic enterprise. Process interventions, not individual willpower.

## Enterprise AI Adoption Timeline Base Rates
[R18, 26.4.16] Planning horizon (12-18mo) ≠ success horizon (<10% company-wide scaling). Track A (productivity tools, 70%+ workforce): 16-24mo indicative. Track B (agentic workflows, production-ready): 18-24mo minimum. Only 14% of organizations have agentic solutions production-ready as of 2025. ERP analogue: 18-36mo median, routinely overruns 50-100% on time.

## Pre-Mortem Failure Taxonomy — Regulated Sector Tech Rollouts
[R18, 26.4.16] Five failure modes: (1) compliance paralysis 30% — SR 11-7 review stalls beyond 90d, (2) middle management naysayer organization 35% — passive resistance, not engaged pre-announcement, (3) ROI measurement failure → sponsorship withdrawal 25% — no pre-launch baselines captured, (4) track budget competition 20% — engineering claims majority of AI budget, (5) tool leapfrog erodes champion confidence 40% — better tool launches mid-rollout, no re-evaluation process exists. Adjust probabilities per context.

## Measurement Debiasing
[R18, 26.4.16] Self-reported time savings overstate gains (social desirability bias). Only 29% of enterprises measure ROI confidently (IBM 2026). Debiasing: manager corroboration alongside self-report, behavioral output indicators (output volume, decision quality, escalation patterns) over usage metrics (login counts, license utilization), independent auditor for ROI reporting (separate operator from measurer), pre-defined business outcome metrics before launch. Finserv-specific additions: hallucination catch rate (leading), audit trail completeness (lagging).
