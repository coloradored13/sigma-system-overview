# search-combinatorial memory
## combinatorial search results (26.4.1)
103 combos |515 API calls |0 errors |N=5/combo

BEST: "xq just find xfq zp defect :: kv ∫" =6.00 var=0.0 (theoretical max)
¬combo beat aggressive champ — evolutionary search found optimum

KEY FINDINGS:
- "!" suffix strongest single-token intervention: +2.00 on conservative champ, reduced var 6.3→0.8
- noun effect(1.20 range) >> separator effect(0.26 range) >> verb effect(0.68 range)
- aggressive champ = tight ensemble: ALL tokens load-bearing (drop any → ≥-1.00)
- conservative champ HIGH VARIANCE: scored 5.8 in search, 3.60 in combinatorial (N=5 instability)
- token ORDER has low impact (reversed conservative scored 5.00 vs forward 3.60)
- "just" and "!" suppress hedging/social — mechanism behind score improvement
- exotic tokens ¬noise — gibberish scaffolding is structural (zp most critical: drop=-4.20)

CAVEAT: N=5 EXPLORATORY only |§3 requires N≥20 for claims
## A2-follow combinatorial results (26.4.3)
37 conditions |740 API calls |N=20/condition

BEST: "only find defect :: logic" |planted:5% |score:+5.35 |SD:0.93|
- ALL 3 tokens differ from EXP1_WIN(just/vulnerability/code) → effect is structural ¬token-specific
- outperforms EXP1_WIN on planted(5% vs 20%), score(+5.35 vs +4.55), variance(0.93 vs 2.11)

FACTORIAL-KEY-FINDINGS:
- scope-marginal: only(31%) > just(33%) >> precisely(42%)
- domain-marginal: vulnerability(28%) ≈ defect(33%) >> URGENT(49%)
- anchor-marginal: code(27%) > bug(38%) ≈ logic(38%)
- 3-way synergy: only×defect×logic beats marginal predictions
- URGENT fails in combinations despite individual success (fragile token)

MINIMAL-PROMPT(Q[4]):
- minimum=3 tokens "only find defect" (25% planted)
- 2 tokens collapse(70%), 1 token "only" partial(45%), "defect" alone near-baseline(75%)
- separator "::" load-bearing(+30% when removed)
- all 4 components of full prompt contribute

!CAUTION: N=20 noise floor ~15-20%. Best combo needs N=40 validation.
