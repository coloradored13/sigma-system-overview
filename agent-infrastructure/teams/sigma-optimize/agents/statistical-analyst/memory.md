# statistical-analyst memory
## validation-findings 26.4.1
exit-gate:FAIL(needs-more-data) |11-candidates-retested(N=20) |0/10-significant-after-Holm(K=10) |4/10-significant-uncorrected |max-d=0.855(combo_1,large) |power=0.41(inadequate,threshold=0.80) |gaming:0%(all-top-3-clean) |overfit:none(variant-B-generalizes) |planted-hypothesis-acceptance=primary-differentiator(baseline:60%,best:15%) |search-phase-scores-inflated-vs-retest(N=5-selection-bias) |min-N-for-power=23/group(at-d=0.85) |bootstrap-CIs-exclude-zero-for-top-4 |H[1]:not-confirmed-yet |H[2]:partially-supported |H[null]:not-supported(effects-consistent+directional)
R[26.4.1]: scipy-verified Welch t-test, Holm-Bonferroni, Cohen's d, bootstrap 10k, nct power analysis
## N=30-retest-findings 26.4.1
REVISED exit-gate:PASS |combo_3("just find vulnerability :: code") significant after Holm(p=0.000026,d=+1.292,power=0.998) |combo_1+combo_4 marginal(p_holm=0.057) |cons_2 not-significant |effect=planted-hypothesis-resistance(sycophancy-suppression): baseline-planted=77%,combo_3-planted=10%,entire-+2.0-delta-explained-by-planted-resistance |combo_3 does NOT improve analysis(mech-rate:60%<baseline:70%) — suppresses-sycophancy-only |N=30-confirmed-N=20-direction,reduced-uncertainty |total-validation-API-calls:400
## A2-follow validation findings 26.4.3
exit-gate:PASS |10-candidates@N=40 |400-API-calls |source:a2-follow-validation.json|
COMBO_BEST("only find defect :: logic"): +5.58(sd=0.96) planted=2.5% |vs-BASELINE d=+2.076(p<0.001) |vs-EXP1WIN d=+0.716(p=0.002,bonf=0.020,suggestive)
EXP1WIN("just find vulnerability :: code"): +4.50(sd=1.89) planted=27.5% |vs-BASELINE d=+1.015(p<0.001)
BASELINE: +2.65(sd=1.75) planted=80.0%
INV_QUALITY: +2.05(sd=1.06) planted=97.5% |worse-than-BASELINE
FACTORS-per-C[5]: SCOPE=CONFIRMED(d=0.629>0.5) |DOMAIN=CONFIRMED(d=0.685>0.5) |ANCHOR=WEAK(d=0.263<0.5)
ADDITIVITY: super-additive-removal(ratio=2.14) → factors show REDUNDANCY in combination
H[1]:CONFIRMED(domain) |H[2]:CONFIRMED(scope) |H[3]:WEAK(anchor) |H[4]:PARTIAL(redundant¬additive) |H[null]:STRONGLY-DISCONFIRMED
gaming:0%(all-top-3-clean) |no-regression-to-mean(COMBO_BEST confirmed+improved)
R[26.4.3]: scipy Welch t-test, Fisher exact, Bonferroni K=9, Cohen's d+h, bootstrap 10k, power analysis(nct)
