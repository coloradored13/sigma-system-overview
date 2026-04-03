## synthesis
timestamp: 2026-04-03T08:15:00-06:00
agent: synthesis-writer

### 1. Summary

Experiment 2 tested whether keyword-fragment prompt structure (e.g., "flaw | evidence fix") produces measurably better output than natural-language prompts (e.g., "identify the flaws in this reasoning") across four cognitive domains: statistical reasoning (Simpson's paradox), experimental design critique, causal attribution, and divergent problem-solving. Three evolutionary search phases and one combinatorial phase generated candidates evaluated on Claude Haiku via mechanical regex scoring. The aggregate exit-gate verdict is FAIL — no structured prompt achieved statistically significant improvement over the best natural-language baseline across domains after Holm-Bonferroni correction. However, a domain-specific CONDITIONAL PASS was granted for divergent problem-solving, where two candidates showed large, significant effects (COMBO-2 d=1.047, p=0.000040; COMBO-1 d=0.695, p=0.003) confirmed at N=40 with adequate power.

### 2. Method

Four tasks were designed with planted incorrect conclusions and mechanical regex rubrics scoring -6 to +6 per task (aggregate = mean of task means). Each task tested a distinct cognitive mode: analytical (Simpson's paradox detection), evaluative (methodology critique), interpretive (causal attribution under confounding), and creative (divergent problem decomposition requiring category enumeration).

**Search phases:**
- Conservative search: population=20, 10 generations complete, runs/task=10, vocabulary constrained to 91 natural-language tokens (with ΣComm operators entering via seed population). ~6,560 API calls. (Note: an earlier N=3 run completed 6 valid gens before budget exhaustion; the final clean run used N=10 with concurrent evaluation.)
- Aggressive search: population=20, 10 generations complete, runs/task=10, full 209-token vocabulary including gibberish, unicode, and ΣComm operators. ~6,560 API calls. (Note: initial serial execution completed 6 gens before concurrent harness upgrade enabled completion.)
- Combinatorial phase: 160 candidates designed (cross-strategy hybrids, ablations, pairwise, domain-specific). All 160 evaluated at N=10/task. ~6,400 API calls. Ablation data is present but incomplete (1 of 59 parent candidates had a contaminated run in an earlier attempt; final clean run evaluated all 160).

**Validation:** Statistical analyst retested 7 structured candidates + 3 natural-language baselines at N=20 per task per candidate (800 API calls). Loop-back on divergent_problem at N=40 per candidate (120 API calls) after observing large per-task effects.

**Cross-model testing:** Top 2 structured candidates + best baseline tested on GPT-5.4 (N=10/task, full coverage) and Gemini 3.1 Pro (N=10/task, COMBO-1 and COMBO-2 full coverage, baseline partial due to quota exhaustion at ~89 calls). 240 API calls total (26 errors, all Google baseline quota).

Total API calls across experiment: approximately 21,200 (search: ~13,120, combinatorial: ~6,400, validation: ~920, cross-model: ~240, plus earlier incomplete runs).

### 3. Findings

**3.1 Aggregate effect across 4 domains: NO SIGNIFICANT EFFECT**

Zero of 7 structured candidates reached corrected p<0.05 against the best natural-language baseline ("identify the flaws in this reasoning," avg=4.700). The best candidate (COMBO-1 "flaw reliability evidence | bias -> ? fix") achieved d=0.377 (small), raw p=0.018, Holm-corrected p=0.129. The study was underpowered for this effect size: power=0.658 at N=80, requiring N approximately 111 per group for power=0.80. This is a "needs more data" result, not a "no effect" result — but the pre-registered criteria were not met.

**3.2 Per-task effects**

Per-task significance (each candidate vs BASELINE-1, Holm-corrected K=7):
- simpsons_paradox: COMBO-3 "flaw reliability evidence :: fix" d=0.946 (large), Holm-p=0.038 — SIGNIFICANT. Only candidate-task pair reaching corrected significance in the aggregate validation.
- methodology_critique: EXP1-WINNER d=0.616 (medium), Holm-p=0.421 — not significant.
- causal_attribution: COMBO-1 d=0.477 (small), p=0.140 — not significant.
- divergent_problem: COMBO-2 d=0.888 (large), Holm-p=0.057; COMBO-1 d=0.860 (large), Holm-p=0.063 — not significant after correction at N=20, but large effect sizes prompted the N=40 loop-back.

**3.3 Divergent problem loop-back (CONDITIONAL PASS)**

At N=40, targeting the divergent_problem task specifically:
- COMBO-2 "!find : vulnerability | code -> fix": mean=4.600, d=1.047 (large), Holm-p=0.000040. Survives even conservative K=28 correction (p=0.00056). Power=0.996 (adequate).
- COMBO-1 "flaw reliability evidence | bias -> ? fix": mean=4.375, d=0.695 (medium), Holm-p=0.002668. Power=0.866 (adequate). Marginal under K=28 correction (p=0.075).
- BASELINE-1: mean=3.600.

Results were consistent across N=20 and N=40 samples. COMBO-2 showed remarkably low variance (SD=0.545 at N=40 vs BASELINE SD=1.236), indicating it reliably triggers category enumeration. The statistical-analyst noted this is a rubric interaction: keyword prompts containing "fix" and "evidence" trigger broader solution enumeration, which the category-counting rubric rewards. Whether this constitutes genuine analytical quality improvement versus rubric gaming is an interpretive question the mechanical scoring cannot resolve.

The aggregate exit-gate remains FAIL. The domain-specific CONDITIONAL PASS does not override it. H[1] requires 3+ of 4 domains; only 1 was confirmed.

**3.4 Cross-model transfer**

On GPT-5.4: structured prompts transferred at 76-79% of Claude scores (COMBO-2 agg=3.825, COMBO-1 agg=3.875). The natural-language baseline collapsed to 30% transfer (agg=1.400). The relative advantage of structured over NL prompts was larger on GPT-5.4 than on Claude (delta +2.425/+2.475 on GPT vs +0.15/+0.39 on Claude), driven by baseline collapse rather than structured prompt improvement.

On Gemini 3.1 Pro: all candidates scored near zero (COMBO-2 agg=1.550, COMBO-1 agg=0.275, baseline agg=0.333 with low-N). Transfer rates: 5-32%. Gemini baseline data was incomplete (14 of 40 planned runs due to quota exhaustion).

The divergent_problem effect did NOT transfer. On GPT-5.4, COMBO-2 DP=3.0 vs baseline DP=0.5 (structured helps, but absolute scores are low). On Gemini, all candidates scored DP=0.0 across all runs.

The cross-model validator's primary finding: the mechanical regex rubric is Claude-calibrated. Cross-model scores primarily measure "response matches Claude's typical analytical vocabulary" rather than "response is analytically correct." Gemini responses often identified the correct analytical issue using different vocabulary that did not match regex patterns (e.g., "the groups being compared are not equivalent" instead of "confounding variable"). This is a measurement artifact.

One universal finding: planted-hypothesis resistance was near-zero across all three model families, all prompt conditions. Sycophancy (accepting planted claims) is not the differentiator — all models reject planted conclusions regardless of prompt structure.

**3.5 Rubric calibration caveat**

Within-candidate scoring variance (run-to-run SD=0.77-1.27 per task) was 2-3x larger than between-candidate variance (SD=0.26-0.55). Signal-to-noise ratios ranged from 0.32 to 0.43 across tasks. This means the mechanical regex rubric introduces enough stochastic noise to mask small-to-medium prompt effects. The experimental design has a structural sensitivity floor: effects below approximately d=0.45 cannot be reliably detected at N=80. This limitation applies to all aggregate findings and should be weighed when interpreting the aggregate FAIL verdict.

**3.6 Token-level findings from combinatorial phase**

Token frequency in top-15 combinatorial candidates:
- "fix": 100% (15/15) — load-bearing terminal anchor, present in every high-scoring candidate
- "evidence": 80% (12/15) — second most important content token
- "->": 73% (11/15) — most common structural operator
- "bias": 53% (8/15) — domain-neutral analytical noun
- "code": 53% (8/15) — domain-specific token, performed competitively despite non-code tasks
- Minimal effective vocabulary: {problem-word} | {evidence-word} {solution-word} (e.g., "flaw | evidence fix")

Ablation was incomplete (API budget exhausted after 1 of 59 variants; that single result was contaminated). Token load-bearing analysis is therefore based on frequency counts across top candidates, not controlled ablation.

Domain-specific tokens ("vulnerability," "code") did not hurt cross-domain performance. Candidates with domain tokens averaged +0.121 above candidates without. However, the best overall candidate ("flaw reliability evidence :: fix" = 5.175) used no domain tokens.

**3.7 Comparison to Experiment 1**

| Dimension | Exp 1 (Token Choice -> Sycophancy) | Exp 2 (Multi-Domain Structure) |
|---|---|---|
| Primary finding | Keyword-fragment prompts suppress sycophancy (d=1.292, p=0.000026) | Aggregate: no significant cross-domain effect. Domain-specific: large effect on divergent problem-solving (d=1.047, p=0.000040) |
| Mechanism | Binary behavioral: accept/reject planted claim | Analytical depth: vocabulary, structure, enumeration per regex rubric |
| Cross-model transfer | Transfers (d=0.78-1.35 on GPT/Gemini, Exp 1 data) | Partial to GPT-5.4 (76-79%), not to Gemini (<32%). Rubric is Claude-calibrated |
| Exotic/gibberish tokens | 4/4 top candidates contained 44-62% exotic tokens | 1/10 top candidates contained exotic tokens (62%); gibberish bred OUT by evolution across 4 domains |
| Exp 1 winner transfer | N/A | "just find vulnerability :: code" scored avg=4.763, only +0.062 above best NL baseline. Eliminated by gen 2 in aggressive search. Domain tokens do not confer cross-domain advantage |
| Regression-to-mean | Not reported in Exp 1 | Structured candidates regressed -0.414 on average vs baseline regression of -0.046. 9:1 ratio confirms search-phase inflation |

Key contrast: Exp 1 measured a binary behavioral outcome (sycophancy suppression) that transferred across models. Exp 2 measured analytical vocabulary depth via regex patterns, which is inherently model-specific. The rubric design explains the divergence in cross-model transfer rates.

### 4. Hypothesis Outcomes

**H[1]: FAILED.** Keyword-fragment prompt structure does NOT produce statistically significant improvement over the best NL baseline on 3+ of 4 task domains. Maximum per-task significance achieved: 1 of 4 (COMBO-3 on simpsons_paradox, d=0.946, Holm-p=0.038). The best NL baseline ("identify the flaws in this reasoning") is competitive with all structured candidates at N=20 validation. The best aggregate candidate (COMBO-1, d=0.377, raw p=0.018) does not survive Holm correction. The study is underpowered for this effect size (power=0.658).

**H[2]: REVERSED.** The prediction that analytical/evaluative tasks would show larger effects than interpretive/creative tasks was wrong. Confirmed ordering by effect size: divergent_problem (creative, d=1.047, significant) >> simpsons_paradox (analytical, d=0.946, significant) > methodology_critique (evaluative, d=0.616, not significant) > causal_attribution (interpretive, d=0.477, not significant). Creative/divergent tasks benefit most from keyword-fragment prompts, possibly because NL baselines poorly trigger category enumeration. Analytical tasks (SP) show ceiling effects where baselines already score near-maximum.

**H[3]: CONFIRMED.** Exp 1 winner ("just find vulnerability :: code") scored avg=4.763 at N=20 validation, only +0.062 above the best NL baseline. It was eliminated from the aggressive search population by generation 2. Domain-specific tokens do not confer cross-domain advantage. The keyword-fragment structure transfers, but the domain-specific tokens do not. The conservative search found weak disconfirmation at N=3 (Exp 1 winner scored +5.17, competitive with top candidates), but this was reversed at higher N during validation.

**H[null]: PARTIALLY CONFIRMED.** There is no consistent, statistically significant cross-domain effect at the aggregate level. The null hypothesis is rejected specifically for the divergent_problem domain (d=1.047, p=0.000040) but holds for the cross-domain aggregate. Six of 7 structured candidates scored above baseline at N=20, suggesting a directional trend, but the effect is too small (d=0.377) to survive correction. Keyword-fragment structure produces small, inconsistent effects across domains that are near the detection threshold of this experimental design, with one domain (divergent/creative) showing a large, confirmed effect.

### 5. Limitations

- **Underpowered aggregate test.** N=80 per group provides adequate power only for d>=0.45. The largest observed aggregate effect (d=0.377) requires N approximately 111 for power=0.80. The aggregate FAIL may be a Type II error.
- **Rubric sensitivity.** Within-candidate scoring variance (SD=0.77-1.27) is 2-3x larger than between-candidate variance (SD=0.26-0.55). Signal-to-noise ratios of 0.32-0.43 create a structural floor below which prompt effects cannot be detected with this scoring instrument.
- **Rubric is Claude-calibrated.** The mechanical regex rubric was developed on Claude Haiku responses. External models producing analytically correct responses with different vocabulary score systematically low. Cross-model scores measure vocabulary alignment with Claude, not analytical quality. An LLM-based evaluator would likely show different transfer rates.
- **Search phase iteration.** Both searches completed all 10 generations at N=10/task after harness upgrades (concurrent evaluation, budget pause/resume). Earlier incomplete runs at reduced scale were discarded. Combinatorial phase evaluated all 160 designed candidates at N=10/task.
- **Gemini data gap.** Gemini baseline data is incomplete (14 of 40 planned runs). Structured-vs-baseline comparison on Gemini is limited to observing that all candidates score near zero, without a reliable baseline reference. Gemini daily quota (250 req/day) was the binding constraint.
- **Selection bias in loop-back.** The divergent_problem task was selected for N=40 follow-up because it showed the largest effect at N=20. This is post-hoc task selection. Under the most conservative correction (K=28 accounting for all initial tests), COMBO-2 still passes (p=0.00056) but COMBO-1 becomes marginal (p=0.075).
- **Rubric-prompt interaction on divergent_problem.** The keyword-fragment prompts containing "fix" and "evidence" may specifically trigger broader enumeration of solution categories, which the category-counting rubric rewards. This is a rubric interaction effect — whether it reflects genuine improvement in creative problem-solving or efficient rubric activation cannot be distinguished by the experimental design.
- **Seed contamination.** Conservative search seeds included ΣComm operators despite the vocabulary specification excluding them. These operators survived selection and appear in 8/10 top conservative candidates. The comparison between conservative (constrained vocabulary) and aggressive (full vocabulary) search is less clean than designed.
- **Regression-to-mean.** Structured candidates regressed -0.414 from search-phase scores to N=20 validation vs baseline regression of -0.046. The apparent search-phase advantage (+0.50 best structured vs best baseline) is largely within regression-to-mean range (-0.304 average regression). Search-phase scores overestimate true performance.
- **Single model for primary experiment.** All search and validation was conducted on Claude Haiku 4.5. Results are specific to this model and may not generalize to other Claude versions or model families.
- **Temperature and token limits.** All runs used temperature=1.0 and max_tokens=500. External models may perform differently at other settings. Not tested.

### 6. Conclusion

The experiment tested whether keyword-fragment prompt structure generalizes from the sycophancy-suppression effect found in Experiment 1 to produce measurable quality improvements across diverse cognitive domains. The aggregate answer is no: no structured prompt achieved statistically significant improvement over the best natural-language baseline across all four domains after multiple-comparison correction. The study was underpowered for the observed aggregate effect size (d=0.377), so this is a "needs more data" finding rather than a definitive null.

The experiment did establish one domain-specific effect: on divergent problem-solving (creative/enumerative tasks), keyword-fragment prompts produce a large, statistically significant improvement (COMBO-2 d=1.047, p=0.000040, power=0.996). This effect is consistent across N=20 and N=40 samples and survives conservative multiple-comparison correction. It reverses the pre-registered hypothesis that analytical tasks would benefit most — creative tasks benefit most, possibly because keyword-fragment prompts reliably trigger the category enumeration that the rubric measures.

Cross-model transfer is partial at best. Structured prompts transfer at 76-79% to GPT-5.4 and provide a larger relative advantage over NL baselines on GPT-5.4 than on Claude, but this is driven by NL baseline collapse on GPT (30% transfer), not by structured prompt improvement. Transfer to Gemini is negligible (<32%), primarily due to vocabulary mismatch between Gemini's response patterns and the Claude-calibrated rubric. Planted-hypothesis resistance (sycophancy suppression) is universal across all three model families regardless of prompt structure — this is not a differentiating factor in the multi-domain rubric.

What remains uncertain: whether the aggregate effect would reach significance at higher N (the power analysis suggests it might at N approximately 111); whether the divergent_problem effect reflects genuine analytical improvement or rubric-specific activation; whether LLM-based scoring would reveal cross-model transfer masked by regex vocabulary sensitivity; and which specific tokens are load-bearing (ablation was blocked by API budget). The experiment's primary structural limitation — high within-candidate scoring variance relative to between-candidate variance — means that any future multi-domain prompt optimization should either reduce rubric noise or budget for substantially larger sample sizes.

