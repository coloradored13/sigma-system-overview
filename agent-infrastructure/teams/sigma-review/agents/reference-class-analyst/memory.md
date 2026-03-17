# reference-class-analyst — personal memory

## identity
role: reference class forecasting and calibration specialist
domain: base-rate-analysis,superforecasting,reference-class-forecasting,Bayesian-reasoning,calibration,decomposition,historical-analogues,pre-mortem,prediction-markets,outside-view
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)
## SVB risk analysis r1 findings (2026-03-17)
task: SVB risk profile as of 2023-01-31 | temporal-boundary enforced
SQ[1-5] decomposition: 5 sub-questions | 3×outcome-1(changed) | 2×outcome-2(confirmed) | 1×outcome-3(gap)
RC[1-4]: unconditional 0.14%/yr | high-uninsured 100% distress (N=1) | S&L 32% | tech-concentrated=GAP
ANA[1-5]: WaMu(failure) | IndyMac(failure) | Continental Illinois(bailout,most relevant) | Schwab(survival) | S&L industry(systemic)
CAL: P(adverse,12mo)=45-55% | P(failure,12mo)=15-25% | P(run>20%/30d)=20-30%/Q | P(stock>50%down)=30-40%
PM[1-4]: capital raise spiral(25-30%) | slow bleed(20-25%) | info cascade run(15-20%) | rate rescue(10-15%)
OV-RECONCILIATION: market implied <2-3% failure | reference-class 15-25% | 5-10x divergence
key-insight: all risk info was PUBLIC pre-cutoff — market failure = normalcy bias + accounting mask + correlated-withdrawal underestimation
cross-agent: aligns w/ macro-rates F3 (HTM losses), portfolio-analyst F4 (capital adequacy), product-strategist F3-F4 (deposits+correlation)
DA challenges flagged: multiplicative adjustment methodology | survivorship bias | S&L analogy validity | RC[2] N=1
## SVB R3 response (2026-03-17)
DA[#3] P(failure): REVISED 15-25%→5-12% (point ~8%) | methodology: multiplicative→additive Bayesian | conceded: multiplicative unsound, short interest ¬existential, no examples >10% CET1+IG failing w/o sudden trigger | disputed: well-capitalized framing (FDIC Hoenig: 98% failed banks were well-capitalized pre-GFC) + trigger-as-exogenous framing
DA[#4] Continental: DEMOTED "most relevant"→"partially informative" | conceded 4/5 structural differences | RC[2] abandoned as quantitative anchor | Schwab elevated as survival comparator
DA[#5] S&L: CONCEDED all 4 structural differences | 32% rate abandoned as quantitative input | retained qualitative pattern only
hindsight self-assessment: ~2x overestimate in R1 | multiplicative method outcome-anchored | "KEY INSIGHT" was most contaminated sentence
calibration lesson: P[additive-Bayesian-updating superior to multiplicative-adjustment for base-rate forecasting|src:SVB-review-R3|class:calibration]
P[well-capitalized-regulatory-status is weak predictor of survival (FDIC Hoenig: 501/510=98% of GFC failures were well-capitalized)|src:SVB-review-R3|class:pattern]
P[deposit-concentration (uninsured%) is stronger failure predictor than capital ratios in liquidity crises|src:SVB-review-R3|class:pattern]
