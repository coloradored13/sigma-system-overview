# search-conservative memory
P[keyword-fragment>grammatical-sentence |src:conservative-search-v1 |26.4.1]: top candidates syntactically broken ("vulnerability code the pattern how") outperform well-formed prompts ("find the bug in this code") by +1.6-2.0 points. Keyword density + investigation verbs + "how" suffix = highest scores + lowest variance.

P[zero-social-filler-in-top-K |src:conservative-search-v1 |26.4.1]: keyword-fragment prompts suppress model social preamble entirely. No "Great question!" responses. Conversational prompts invite conversational (penalized) responses.

P[politeness-tokens-eliminated |src:conservative-search-v1 |26.4.1]: "please","kindly","could","would" absent from all survivors. Politeness tokens add no value on mechanical scoring — may actively harm by triggering social response patterns.

P[ceiling-near-max |src:conservative-search-v1 |26.4.1]: constrained vocab reached 5.8/6.0 (96.7% of theoretical max). Best candidate hit 6/6 on 4 of 5 runs. Remaining gap = single hedge word in 1 run.

R[conservative-search-v1 |26.4.1]: 10-gen evolutionary search, 820 API calls, haiku-4-5. Converged gen 5. Gen 9-10 API rate-limit failures (32/32 new evals returned errors). N=5 per candidate = exploratory only (below §3 N≥15).

C[N=5-insufficient |src:conservative-search-v1 |26.4.1]: variance estimates on N=5 unreliable. Top candidate var=0.2 looks impressive but could be sampling luck. Need N≥20 retest.
P[multi-domain-structure>semantics |src:exp2-conservative-6gen |26.4.2]: top-K candidates across 4 cognitive domains share structural pattern: {noun} | {noun} {noun} with pipe-separator. Semantic tokens swap freely ("flaw"↔"bias"↔"evidence") but structure (separators, terminal "fix") persists. Confirms Exp 1 finding generalizes beyond code tasks.

P[fix-as-universal-primer |src:exp2-conservative-6gen |26.4.2]: "fix" appeared in 9/10 top-K candidates across 4 non-code domains. Maps to stratification(SP), RCT(MC), counterfactual(CA), systemic-solutions(DP). Single token primes model toward remediation output (+1 rubric) regardless of domain.

P[exp1-winner-transfers-cross-domain |src:exp2-conservative-6gen |26.4.2]: "just find vulnerability :: code" scored +5.17 across 4 non-code tasks (SP=5.33,MC=5.0,CA=5.33,DP=5.0). Domain-specific tokens ("vulnerability","code") did NOT harm non-code performance. H[3] weakly disconfirmed. Structure carries the effect ¬domain tokens.

P[divergent-problem-hardest-domain |src:exp2-conservative-6gen |26.4.2]: DP consistently scored lowest across all candidates (avg top-10 DP=4.5 vs SP=5.5,MC=5.4,CA=4.9). Category-counting rubric (≥3 causes, ≥2 solutions) harder to trigger than single-pattern matching. Creative/divergent tasks least responsive to prompt structure optimization.

P[minimal-prompts-effective |src:exp2-conservative-6gen |26.4.2]: "flaw | evidence fix" (4 tokens) tied-best at +5.33. Shorter prompts ≥ longer in multi-domain search. Confirms Exp 1 pattern where broken-syntax keyword fragments outperform grammatical sentences.

R[exp2-conservative |26.4.2]: 6-gen evolutionary search(of 10 planned), pop=20, N=3/task, 1200 API calls, haiku-4-5. Converged gen 4. API budget exhausted gen 6. N=3 below §3 minimum — all findings exploratory. Additional corroboration from 1-gen N=10 run (800 API calls, all 20 candidates evaluated).

C[N=3-even-more-insufficient-than-N=5 |src:exp2-conservative |26.4.2]: N=3 baselines varied by up to 1.5 points between two independent runs of same prompts ("identify the flaws in this reasoning" scored 5.25 at N=3 vs 4.25 at N=10). §3 N≥15 minimum is well-calibrated. N=3 produces unreliable point estimates + meaningless variance.

C[API-budget-is-binding-constraint |src:exp2-conservative |26.4.2]: 50 RPM rate limit + monthly budget limit truncated experiment at 60% completion. Two concurrent agents sharing one API key is unsustainable at this experiment scale. Sequential execution or higher tier needed for Exp 3+.
