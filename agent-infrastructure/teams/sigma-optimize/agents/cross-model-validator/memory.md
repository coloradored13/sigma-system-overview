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
