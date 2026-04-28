# AI Agent Governance Committee Design
Last updated: 26.4.28 | Reviews: R-2026-04-22-ai-agent-rollout-playbook-vet (26.4.28)

## Summary
The AI Risk Committee — Chair (Legal/Security/Risk), Playbook Owner, independent reviewer, and members from Engineering, Legal, and Security — is the standard governance committee structure across both financial-services and B2B SaaS playbooks. The structure is sound for mid-to-large firms but is under-specified as a decision-forcing function in four documented ways, each mapping to a known group-decision failure mode. The committee has an undocumented firm-size floor below which the structure is unexecutable. Tier-promotion gates at principle-level rather than specification-level reintroduce groupthink risk that the multi-role committee was supposed to defend against. Reviewer calibration at 3-5 part-time reviewers covers <1% of production query volume, insufficient for criteria-drift detection without structured stratified sampling. Five tier-promotion cognitive biases are unaddressed by structural intervention.

## Committee Structure — Standard Form
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Both financial-services and B2B SaaS playbooks specify an AI Risk Committee with: Chair (Legal/Security/Risk function), Playbook Owner, independent reviewer, and committee members from Engineering, Legal, and Security. The structure is correct as a starting point. Four design gaps below convert it from "named structure" to "decision-forcing function."

## Design Gap 1 — No Pre-Commitment Mechanism
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Tier promotion criteria are typically not locked before the build team has observed the agent. This creates anchoring bias: criteria drift toward whatever the agent's actual performance happens to be. Intervention: pre-commit tier promotion criteria signed and dated before Phase 2 begins. The pre-commitment is the criterion's only protection from anchoring.

## Design Gap 2 — No Structural Independent Challenger
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Multi-agent review systems have a Devils-Advocate role because consensus is unreliable without adversarial challenge. The AI Risk Committee has no equivalent — the "independent reviewer" role is structurally part of the committee, not adversarial to it. Intervention: name a challenger who is not on the build team and who writes a dissent memo at every tier-promotion meeting. The dissent memo is mandatory regardless of whether the challenger personally agrees with promotion.

## Design Gap 3 — No Written Pre-Mortem Requirement
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] "What would have to be true for this Tier 1 promotion to fail within 6 months?" is rarely asked structurally. Intervention: required pre-mortem at each tier promotion, written before deliberation begins. The pre-mortem captures the failure modes the committee must explicitly address before promotion.

## Design Gap 4 — Chair-Decides Concentrates Authority on Optimism Bias
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] B2B SaaS doc's "Chair decides on disagreement" concentrates authority in the person with the highest optimism bias about launch — typically the role most invested in the launch timeline. Intervention: explicit recusal protocol when members have personal stakes in launch timing. Anonymous pre-vote before deliberation begins captures the unsoftened initial position.

## Tier Gates — Specification-Level, Not Principle-Level
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Severity HIGH gap: the B2B SaaS doc has 13 binary Phase 0 exit gates — falsifiable and executable. Financial-services tier-advancement criteria are observation-based ("observability maturity, not eval pass rate") — correct in principle, not falsifiable in practice. A ship-it coalition can satisfy "observability maturity" by pointing to any functional OTel deployment. Specification-level thresholds are needed for each tier transition:
- Minimum eval set size: 500+ items for initial; 200+ items per query class for ongoing
- Minimum shadow-mode duration: 6 weeks for advisory; 10 weeks for action-capable
- Minimum judge-to-SME agreement: 85%+ initial, with recomputation trigger at every vendor model update and every significant prompt change
- Minimum red-team coverage: full OWASP LLM Top 10 plus domain-specific attack cases

The thresholds themselves are not the point — the point is that they exist and cannot be talked past.

## Tier-Promotion Cognitive Biases
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Severity HIGH: tier promotion decisions are high-stakes, infrequent, committee-made under social pressure — exactly the conditions most vulnerable to systematic bias. Five unaddressed biases:
1. Optimism bias — build teams systematically overestimate readiness
2. Sunk-cost — Phase 0-2 investment creates pressure to promote
3. Social proof — "other firms are at Tier 1"
4. Authority bias — external consultancy declaring readiness carries disproportionate weight
5. Framing effect — "95% pass" versus "5% fail" produce different decisions on identical evidence

Pre-emption interventions:
- Outside-view reference class at every tier promotion (what is the historical promotion-success base rate at firms with similar evidence?)
- Pre-mortem requirement (Design Gap 3 above)
- Anonymous pre-vote before deliberation begins (defends against social proof and authority bias)
- "What would it take to delay?" asked before "Should we promote?" (defends against framing effect)

## Reviewer Calibration at Production Scale
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] At 3-5 part-time reviewers working 2-4 hours per week, the pool covers roughly 80 outputs per week at 15 minutes per review. At 5,000+ daily queries in Tier 1 production, this is 0.1-1% sampling — insufficient for criteria-drift detection without structured stratified sampling. Severity MEDIUM-HIGH. "Monthly calibration sessions" specify a schedule, not a feedback loop. Required specification:
- Who attends (reviewers, Playbook Owner, independent challenger)
- What input they review (sampled outputs by query class with risk weighting)
- What output the calibration produces (criteria revisions versus reviewer disagreement)
- Who has authority to update criteria mid-cycle (governance committee, not Playbook Owner alone)
- How the revision decision is made (anonymous pre-vote, then discussion, then signed-and-dated criterion update)

## Criteria Drift — Revision Process Not Just Cadence
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Both playbooks cite Shankar 2024 UIST correctly on criteria drift. Operationalizations are partial:
- Financial doc: "revisited on every pipeline change" — that is a trigger, not a process
- B2B SaaS doc: "monthly calibration sessions" — that is a schedule, not a feedback loop

Specification: what constitutes a criteria change, who approves it, how the eval set is updated, and how the change is documented for audit. Recomputation trigger should fire on every vendor model update (not just every prompt change). Measuring agreement without specifying what triggers changes is monitoring without a feedback loop. Severity MEDIUM.

## Over-Reliance — Behavioral Detection Methodology
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Both playbooks name over-reliance as a risk; neither specifies a detection methodology. The literature identifies three validated behavioral markers:
- Reduced verification behavior (decreased time spent reviewing agent output before acceptance)
- Automation bias (accepting incorrect confident outputs)
- Skill decay (degradation of unaided human performance over time)

Detection requires behavioral instrumentation rather than self-report:
- Edit-distance between agent output and final human output
- Time-to-accept as a verification-effort proxy
- Disagreement-rate trend as a decay signal

Severity MEDIUM, but legally material by January 1, 2027 for CCPA ADMT "meaningful human involvement" compliance — rubber-stamp detection requires this behavioral layer to demonstrate non-superficial human involvement.

## Firm-Size Floor — Unexecutable Below ~$500M Assets / ~30-Person Tech Org
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] The committee structure as specified is unexecutable below approximately $500M in assets or a 30-person technology organization. Below this floor, the same person who would be Chair is also the independent reviewer is also the Playbook Owner — the multi-role structure collapses. A "named-accountability single-owner" variant with documented pre-commitment criteria is needed for community banks, regional insurers, credit unions, and similar firms. This variant is not designed by the source review; it is flagged as an open design problem.

## Statutory Linkage to Article 9 EU AI Act
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] The committee's first substantive act is use-case classification (EU AI Act Article 6: high-risk or not). Article 9 risk management system design follows. Governance-first and use-case-selection-first are not in conflict — they are sequenced under Article 6 → Article 9 statutory ordering. For trust companies, loan-agency firms, and similar organizations where the lethal trifecta applies to almost every customer-proximate workflow, use-case selection and governance design are co-equal Phase 0 outputs rather than sequential steps.

## Open Questions
- The single-owner variant for sub-$500M firms — what pre-commitment criteria substitute for the multi-role committee's structural challenge function? Not designed. [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]
- Whether anonymous pre-vote actually changes outcomes or only documents resistance — empirical question, no published base rate. [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]
- Whether continuous per-query-class monitoring (capabilities gated per query class in a continuous loop) is a viable alternative to discrete tier-promotion ceremonies — not stress-tested. The tier structure remains the defensible default. [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]

## Sources
- R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28 — sigma-review Tier 3 ANALYZE on dual-track financial-services capability-maturity roadmap and B2B SaaS phased workbook
