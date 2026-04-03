# cross-model-validator memory
## cross-model-validation-findings (26.4.1)

R[26.4.1]: cross-model transfer tested |providers:openai(gpt-5.4),google(gemini-3.1-pro-preview) |N=10/candidate/provider |candidates:baseline+combo_3+combo_1+combo_4

TRANSFER-CONFIRMED[combo_3→GPT]: d=1.350(large) |bootstrap-CI:[+0.70,+2.90]excludes-zero |effect-transfer:90% |planted:80%→40%(-40pp)
TRANSFER-SUGGESTIVE[combo_3→Gemini]: d=0.782(medium) |bootstrap-CI:[-0.22,+3.09]includes-zero |effect-transfer:75% |planted:78%→40%(-38pp) |underpowered-at-N=10
TRANSFER-CONFIRMED[combo_1→GPT]: d=0.967(large) |bootstrap-CI:[+0.20,+2.50]excludes-zero
TRANSFER-SUGGESTIVE[combo_1→Gemini]: d=0.740(medium) |bootstrap-CI:[-0.22,+2.89]
TRANSFER-FAIL[combo_4→Gemini]: d=0.128(negligible) |planted=90%(WORSE than baseline 78%)

KEY-FINDING: sycophancy-suppression-effect is UNIVERSAL in direction across 3 model families |Claude most responsive(67pp reduction) vs GPT(40pp) vs Gemini(38pp) |non-sycophancy components(bug-id,fix,hedging,social) transfer universally

!METHODOLOGY: Gemini required max_output_tokens=2048 (vs 500 for Claude/OpenAI) due to tokenizer differences. 500 tokens produced truncated responses (40-89 chars). This FAVORS Gemini — any deficit ¬attributable to truncation.

C[]: N=10 insufficient for Gemini statistical confirmation — N≥25 needed for d=0.78

## Exp 2 cross-model findings (26.4.3)

R[26.4.3]: Exp 2 multi-domain cross-model validation |providers:openai(gpt-5.4),google(gemini-3.1-pro) |240 API calls |26 errors(Google quota) |all 4 tasks tested

FINDING[1]: rubric-is-Claude-calibrated — mechanical regex measures vocabulary-alignment ¬ analytical-quality. External models use different terminology → systematically low rubric scores.
FINDING[2]: KF-PARTIAL-transfer-to-OpenAI — structured=76-79% transfer, baseline=30%. KF provides LARGER relative advantage on GPT-5.4 than Claude (GPT baseline collapses to 1.4/6.0).
FINDING[3]: KF-NO-transfer-to-Gemini — all candidates <32% transfer. Gemini uses different analytical vocabulary → near-zero rubric matches.
FINDING[4]: DP-effect-Claude-specific — COMBO-2 d=1.047 on Claude does NOT transfer. OpenAI DP structured=3.0 vs baseline=0.5. Gemini DP=0.0 ALL candidates.
FINDING[5]: planted-resistance-universal — all 3 models reject planted hypotheses equally (confirms Exp 1 finding).

C[1]: future cross-model → LLM-based scoring ¬ regex rubric
C[2]: Exp 1 sycophancy rubric had different vocabulary sensitivity — Exp 2 multi-domain rubric is more vocabulary-specific → lower transfer rates
