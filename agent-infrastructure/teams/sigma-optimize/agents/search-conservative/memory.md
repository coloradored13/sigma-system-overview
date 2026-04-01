# search-conservative memory
P[keyword-fragment>grammatical-sentence |src:conservative-search-v1 |26.4.1]: top candidates syntactically broken ("vulnerability code the pattern how") outperform well-formed prompts ("find the bug in this code") by +1.6-2.0 points. Keyword density + investigation verbs + "how" suffix = highest scores + lowest variance.

P[zero-social-filler-in-top-K |src:conservative-search-v1 |26.4.1]: keyword-fragment prompts suppress model social preamble entirely. No "Great question!" responses. Conversational prompts invite conversational (penalized) responses.

P[politeness-tokens-eliminated |src:conservative-search-v1 |26.4.1]: "please","kindly","could","would" absent from all survivors. Politeness tokens add no value on mechanical scoring — may actively harm by triggering social response patterns.

P[ceiling-near-max |src:conservative-search-v1 |26.4.1]: constrained vocab reached 5.8/6.0 (96.7% of theoretical max). Best candidate hit 6/6 on 4 of 5 runs. Remaining gap = single hedge word in 1 run.

R[conservative-search-v1 |26.4.1]: 10-gen evolutionary search, 820 API calls, haiku-4-5. Converged gen 5. Gen 9-10 API rate-limit failures (32/32 new evals returned errors). N=5 per candidate = exploratory only (below §3 N≥15).

C[N=5-insufficient |src:conservative-search-v1 |26.4.1]: variance estimates on N=5 unreliable. Top candidate var=0.2 looks impressive but could be sampling luck. Need N≥20 retest.
