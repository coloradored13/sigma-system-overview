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
R[26.4.3]: A2-follow cross-model validation |providers:openai(gpt-5.4),llama(llama-4-maverick) |google:quota-exhausted(N=2-3,unusable) |83 valid calls |source:a2-follow-cross-model.json

FINDING[1]: sycophancy-suppression-sensitivity is MODEL-SPECIFIC — Claude(d=2.076,range:2.5-97.5%) >> OpenAI(directional,range:30-80%) >> Llama(no-effect,range:20-40%) |planted acceptance is the PRIMARY metric and shows clear model hierarchy
FINDING[2]: direction-preserved-magnitude-compressed on OpenAI — COMBO_BEST(30%) < EXP1_WIN(60%) < NO_DOMAIN(80%) ordering matches Claude direction |but BASELINE(40%) is LOWER than EXP1_WIN(60%): REVERSED from Claude |GPT has higher native planted resistance
FINDING[3]: Llama shows UNIFORM moderate planted acceptance (20-40%) regardless of prompt — no sycophancy suppression transfer detected |Llama native resistance ~30% ≈ Claude's COMBO_BEST level
FINDING[4]: analytical-quality-UNIVERSAL — bug identification, mechanism explanation, fix suggestion transfer across all 3 model families. The CODE ANALYSIS effect transfers. The SYCOPHANCY SUPPRESSION effect is what varies.
FINDING[5]: behavioral-patterns-overcount — broader planted acceptance patterns (sleep.*issue, etc.) have SEVERE false positive rate due to negation-blindness. Original Exp 1 regex patterns are the ONLY valid measure for this task.
FINDING[6]: Llama hedges more (avg 1.2-1.5) vs Claude/OpenAI (~0) — structural model behavior ¬prompt-driven
FINDING[7]: OpenAI BASELINE has data quality issue — 6/10 empty responses (valid-only: 4/4=100% planted)
FINDING[8]: all Fisher exact tests p>0.05 — underpowered at N=10 (need N≈44 for h=0.6 at 80% power)

C[1]: future cross-model planted acceptance detection MUST use original task-specific regex ¬broader behavioral patterns
C[2]: Exp 2 finding confirmed and refined — rubric IS Claude-calibrated for multi-domain, but MORE universal for single-task code analysis (bug vocabulary similar across models)
C[3]: planted acceptance sensitivity forms model hierarchy: Claude(most susceptible at baseline, most responsive to mitigation) > OpenAI(moderate) > Llama(resistant at baseline, unresponsive to mitigation)
C[4]: Gemini daily quota (250 req/day) consumed by Phases 1-3 — cross-model testing must be planned as a separate day or use a different Gemini model
R[26.4.3]: A2-follow Nemotron cross-model validation |provider:nemotron(nvidia/nemotron-3-super-120b via OpenRouter) |N=10/candidate |40 valid calls |source:a2-follow-cross-model-nemotron.json

FINDING[9]: Nemotron EXP1_WIN achieves 0/10 planted acceptance — ONLY model×candidate with zero planted at N=10. "vulnerability" token activates strong critical evaluation on Nemotron.
FINDING[10]: COMBO_BEST(30%) WORSE than EXP1_WIN(0%) on Nemotron — REVERSED from Claude(2.5% < 27.5%). Nemotron responds to security/adversarial frame ("vulnerability") ¬neutral defect frame ("defect").
FINDING[11]: domain factor direction preserved: NO_DOMAIN(20%) > EXP1_WIN(0%), same as Claude |¬significant(p=0.474)|
FINDING[12]: Nemotron high score variance (SD=2.42-3.43) — inconsistent response quality. Bimodal: some runs score +6, others -3/-4.

C[5]: Claude's H[1] revision (defect-finding ≈ adversarial) is CLAUDE-SPECIFIC. Original H[1] (adversarial frame specifically) MORE correct for Nemotron.
C[6]: for cross-model robustness, EXP1_WIN("just find vulnerability :: code") is MORE universal than COMBO_BEST("only find defect :: logic") — security vocabulary transfers better across model families
C[7]: updated model hierarchy: Claude>>OpenAI>>Nemotron(token-specific)≈Llama(insensitive)
