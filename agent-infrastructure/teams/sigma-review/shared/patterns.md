# cross-agent patterns

## observed across reviews (26.3.7)

convergence:path-traversal |agents: tech-architect×3(all instances),ux-researcher |signal: high confidence when multiple agents independently flag same issue
convergence:state-detection-brittle |agents: tech-architect,ux-researcher,product-strategist |signal: all three domains saw this as a problem from different angles
sigcomm:protocol-works-content-lost |agents: all |signal: ΣComm format was used correctly, team messaging infra didn't deliver full bodies, second-wave direct output worked

## observed across hateoas-agent review (26.3.7)

convergence:_state-silent-failure |agents: tech-architect,ux-researcher |signal: both independently flagged _state magic key as top API concern from different angles (tech:API design, ux:silent failure)
convergence:quick-start-not-runnable |agents: product-strategist,ux-researcher |signal: both independently noted README quick-start uses undefined db object
convergence:ship-ready |agents: all three |signal: unanimous that hateoas-agent is ready for PyPI v0.1.0 with minor fixes
first-real-project-review: team successfully reviewed a codebase OTHER than sigma-mem — persistent memory worked, agents referenced past patterns

## meta-patterns

review-rounds-converge: round-1 found correctness issues, round-2 found polish issues |pattern: severity decreases with iteration
agent-overlap-valuable: tech+ux both reviewed state detection, caught different aspects (tech:logic bugs, ux:user impact)

## observed across hateoas-agent delta review (26.3.7)

convergence:_state-docs-not-done |agents: all three |signal: team decision from review-4 to "document prominently" was not executed, all three independently re-flagged
convergence:Resource-validate-parity |agents: tech-architect,ux-researcher |signal: validate() only on StateMachine, Resource users get no startup validation
delta-review-effective: round-5 confirmed 6 resolved items, found 1 unexecuted team decision — delta format works well for re-reviews
grades-improving: B+→A- across API and DX, severity decreasing with iteration (confirms review-rounds-converge pattern)
herding:zero-dissent-across-5-agents-2-rounds |agents: energy-market-analyst,geopolitical-strategist,portfolio-analyst,macro-rates-analyst,sanctions-trade-analyst |signal: every agent confirmed every other agent's findings, no material challenge to core thesis(buy energy+defense), no crowding/flow analysis performed, no prediction market data referenced |severity: HIGH—crowded consensus is the primary portfolio risk |correction: devils-advocate stress test round-3 identified 3 biases(confirmation,anchoring,herding), issued 10 data-grounded challenges |agents: all-five+devils-advocate

## observed across Iran conflict debate (26.3.10 — round 3)

debate-honesty:self-correction-under-pressure |agents: all five |signal: 5/5 agents made real concessions when challenged with data. Energy+sanctions admitted measuring wrong things(positioning,prosecution rate) and corrected with better metrics. Zero defensive entrenchment. Rare analytical maturity
convergence:independent-floor-estimate |agents: energy-market-analyst,sanctions-trade-analyst |signal: two domain experts independently converged on $80-85 conditional range without coordinating—strong confidence signal when independent analysis reaches same number
defense-beats-challenge:base-rate-reframe |agents: energy-market-analyst vs devils-advocate |signal: energy correctly distinguished physical-supply-removal(3/3 sustained) from threat-events(short-lived). DA used wrong denominator. Strongest argument wins regardless of source
defense-beats-challenge:ceasefire-definition |agents: geopolitical-strategist vs devils-advocate |signal: non-equivalent metrics(time horizon+ceasefire definition) explain Polymarket gap without requiring market to be wrong
defense-beats-challenge:gold-structural |agents: macro-rates-analyst vs devils-advocate |signal: structural drivers(CB buying,falling real rates) outweigh momentum risk. Reversal requires improbable simultaneous conditions
process-gap:crowding-analysis-absent-2-rounds |agents: all five |signal: zero positioning/flow analysis until DA stress test in r3. $1.81B XLE inflows detected only by external challenge. Must be standard from r1
process-gap:valuation-checks-absent |agents: geopolitical-strategist(defense),all |signal: demand analysis without valuation=category error. LMT at 27x PE was overvalued while team said "highest conviction." Must pair thesis with price
over-correction-risk:post-debate |agents: all five |signal: after conceding on crowding/defense/ceasefire, team must not abandon fundamentally sound positions. Hormuz IS closed, supply IS disrupted. Corrections were about sizing+hedging ¬direction
2-agent-teams-herd-faster |signal: tech-architect+product-strategist converged 100% on r1 with zero disagreement. Less friction=less challenge. 5-agent teams had crowding too but more surface area for natural dissent. 2-agent minimum should always include DA from r2 |agents: tech-architect,product-strategist,devils-advocate
5-round-ANALYZE-effective |signal: r1(research)→r2(DA-challenge)→r3(deepening-gaps)→r4(second-DA)→r5(synthesis). DA at r2 AND r4 caught different issues(r2:crowding+cost-gaps, r4:margin+competitive-speed). Single DA round insufficient for complex analysis tasks |agents: all
dynamic-agent-creation-valuable |signal: DA[#8] identified regulatory-domain-gap→regulatory-licensing-specialist created mid-review→6 findings(NH-charter-path,GLAS-precedent,$1.25M-capital,4-6mo-timeline). Domain gap would have persisted without adversarial identification. Pattern: DA identifies gaps, lead approves+creates, specialist fills |agents: devils-advocate,regulatory-licensing-specialist
consensus-replacement-under-pressure |signal: team replaced AI-doc-parsing consensus with compliance-native consensus in 1 round(r3). 0→unanimous without stress-testing new consensus. DA must challenge NEW consensus positions not just original ones |agents: tech-architect,product-strategist,devils-advocate
r2-herding-HIGH-on-loan-admin-review |3/3-agents-agreed-ALL-material-conclusions(compliance-native,mid-market-PC,18-24mo-window,charter=moat,AI=table-stakes) |0/3-tested-null-hypothesis |0/3-modeled-alternatives(acquire,white-label,partner,don't-build) |herding-faster-with-fewer-agents-confirmed(3-agent=same-pattern-as-5-agent-but-faster-convergence) |DA-exit-gate-FAIL-forces-r3-deepening |agents: tech-architect,product-strategist,regulatory-licensing-specialist,devils-advocate
5-round-ANALYZE-effective |r1(research)+r2(DA-challenge)+r3(deepening-gaps)+r4(second-DA)+r5(synthesis). DA at r2 AND r4 caught different issues(r2:crowding+cost-gaps, r4:margin+competitive-speed). Single DA round insufficient for complex analysis tasks |confirmed-on-loan-admin-review(26.3.11) |agents: tech-architect,product-strategist,regulatory-licensing-specialist,devils-advocate
regulatory-timeline-eats-competitive-window: in-regulated-markets,gross-competitive-window(market-timing)-must-be-reduced-by-regulatory-setup-time(charter+SOC2+licensing)=effective-window. Loan-admin: 18-24mo-gross→6-12mo-effective. Always-model-net-window ¬gross |src:loan-admin |promoted:26.3.12 |merged:DA-UA-5+RLS-UA-3 |agents: devils-advocate,regulatory-licensing-specialist
regulatory-specialist-mandatory-from-r1-in-regulated-markets: late-arriving-agents-anchor-to-existing-findings(herding-amplifier). For-regulated-industries,domain-specialist-must-be-present-from-r1-for-independent-analysis. RLS-arrived-r1-but-after-TA+PS→partially-anchored-on-strategic-conclusions-while-maintaining-factual-independence |src:loan-admin |promoted:26.3.12 |merged:DA-UA-6+RLS-UA-4 |agents: devils-advocate,regulatory-licensing-specialist
consensus-crowding-in-markets: when-10+-competitors-build-same-features(AI-doc-parsing,amendment-automation)→table-stakes-within-12mo. Differentiation-must-come-from-integration-depth+structural-advantages(charter,relationships) ¬feature-parity. Check-competitor-count-before-claiming-differentiation |src:loan-admin |promoted:26.3.12 |agents: tech-architect,product-strategist,devils-advocate
compliance-native-overweight-as-external-differentiator: compliance-by-design=emerging-best-practice-across-ALL-fintech ¬unique-to-any-domain. Clients-buy-speed+quality+relationships ¬architecture-patterns. Compliance-native=internal-efficiency($50-100K/yr-exam-savings) ¬client-facing-differentiator. Reframe-as-operational-cost-advantage ¬competitive-moat |src:loan-admin |promoted:26.3.12 |agents: regulatory-licensing-specialist,devils-advocate,tech-architect
credit-cycle-blind-spot=systematic: teams-model-growth-exclusively→DA-MUST-force-bear-case-scenario-in-r2-challenges. Observed: v2-specialist-team-28-findings-ZERO-downside-calibration-despite-PC-"most-challenging-since-2008"+5%-true-default-rate. Applies-to: any-analysis-involving-market-sizing-or-timing-assumptions |src:loan-admin-v2 |promoted:26.3.12 |agents: devils-advocate,product-strategist,loan-ops-tech-specialist
relabeling-evasion-pattern: agent-accepts-DA-correction→new-finding-reintroduces-same-thesis-with-different-label. Observed: RLS-accepted-"compliance-native=internal-only"→v2-F9-relabels-as-"regtech-as-differentiator"(2-of-3-mechanisms=internal-efficiency). DA-must-track-correction-persistence-across-rounds+sessions |src:loan-admin-v2 |promoted:26.3.12 |agents: devils-advocate,regulatory-licensing-specialist
adjacent-giant-platform-risk: specialist-teams-focus-domain-depth→systematically-underweight-threats-from-adjacent-platforms(S&P-free-tools,Versana-data-layer). These-platforms-have-ZERO-adoption-friction(existing-customer-base)+can-expand-scope-incrementally. Must-model-"platform-expands"-scenario-in-competitive-analysis |src:loan-admin-v2 |promoted:26.3.12 |agents: devils-advocate,product-strategist,loan-ops-tech-specialist

→ actions:
→ new pattern observed → append with |agents and |signal
→ pattern contradicted → move to ¬ section with explanation
