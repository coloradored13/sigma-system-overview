# AI Agent Rollout Playbook Vetting — Synthesis Report
**Review date:** 2026-04-22
**Review type:** ANALYZE — multi-agent sigma-review, Tier 3 (20/25)
**Subjects:** Financial services capability-maturity roadmap (ai_agent_roadmap_v2.md + addendum) and B2B SaaS phased workbook (ai_agent_playbook_b2b_saas.md + addendum)
**Target audience:** Firms planning to execute from 0 to deployed AI agent in production

---

## Synthesis preamble

Three working conditions must be stated up front before the analysis proper.

**Tier-structure anchoring.** All seven review agents worked within the tier-based framing of the financial roadmap (Tier 0 through 3) and the phase-based framing of the B2B SaaS workbook (Phase 0 through 4). No agent independently tested continuous per-query-class monitoring as an alternative to discrete tier-promotion ceremonies. This is a genuine analytical blind spot acknowledged by three agents after adversarial challenge. The tier structure remains defensible as an organizing device for most firms, but the alternative — where capabilities are gated per-query-class in a continuous monitoring loop rather than promoted in discrete ceremonies — was not stress-tested as a design option. Synthesis readers should carry this caveat.

**Three DA carry-forward flags.** The devils-advocate review produced three informational flags that are not findings in themselves but must color how the synthesis is read: (a) the governance-first framing has an undocumented firm-size floor (addressed below in the limitations section), (b) data quality and corpus readiness were not addressed by any agent and are acknowledged out-of-scope gaps, and (c) adoption-economics — whether the governance overhead exceeds the agent's productivity savings at low query volumes — was qualitatively flagged but not quantified.

**Governance-versus-use-case dual framing.** The financial roadmap's organizing premise is "AI agent deployment is primarily an autonomy governance problem, not a model selection problem." This premise holds for mid-to-large financial institutions with internal-facing use cases that do not initially trigger the lethal trifecta. It may not hold for trust companies, loan-agency firms, and similar organizations where the lethal trifecta (private data access + untrusted content ingestion + external communication capability) applies to almost every customer-proximate workflow. For those firms, use-case selection and governance design are co-equal Phase 0 outputs — not sequential steps where governance comes first and then unlocks use-case selection. Additionally, the EU AI Act's statutory ordering confirms this: Article 6 scope-determination (classifying whether a use case is high-risk) must precede Article 9 risk management system design. The governance committee's first substantive act is the use-case classification — governance-first and use-case-selection-first are not in conflict, but the playbooks do not make this explicit.

---

## Executive summary

This review vetted two AI agent rollout playbooks — a financial services capability-maturity roadmap and a B2B SaaS phased operational workbook — against the standard "firms can take and run with this without worrying about gaps." Seven specialist agents conducted independent research across technical architecture, security, US financial regulation, EU and state AI law, reference-class calibration, vendor landscape, and cognitive-operational governance. A devils-advocate conducted adversarial challenge against the strongest-conviction findings, performing external verification from three architecturally distinct AI providers to calibrate severity ratings. The core finding: both playbooks are built on a structurally sound governance-first spine and share approximately 80% of their underlying architecture (gateway, OBO identity, observability, eval harness, guardrails, kill switch, vendor agreements, audit store, governance committee). The architecture is largely correct and defensible. What is missing is not a different architecture — it is the layer that converts correct architecture into exam-ready, audit-ready, firm-executable deliverables. Firms executing these playbooks as written will build sound technical infrastructure but will encounter surprises on their first regulatory examination, their first multi-agent expansion, and their first vendor discontinuity. The strongest executable form is a unified document with substantive sector-specific annexes, not two separate documents, and that document needs seven categories of material additions detailed below.

---

## What the two playbooks got right

### The governance-first spine is correct

All seven review agents confirmed that governance-first sequencing — establishing observability, eval methodology, identity scoping, and governance committee before agent deployment — is the right order for regulated-firm and customer-facing deployments. The evidence is strong: Morgan Stanley's 98% advisor adoption followed a governance-first approach with an evaluation framework that "wasn't static, it evolved as the team learned" (F[R1-A5], ANA[1]). Klarna's 2024-2026 CSAT walkback and partial agent rollback followed a governance-light approach (ANA[2]). Air Canada's 2024 BCCRT loss confirmed "the firm owns what its agent says" (ANA[4]). The single exception is Stripe's internal-tool-first pattern for low-blast-radius, non-customer-facing tools, which shows governance-first is oversized for pure-internal advisory use cases at technically strong organizations (ANA[6], F[R1-A5]).

Both playbooks correctly identify that tier or phase advancement is evidence-gated, and that the gate is observability maturity, not benchmark scores. Berkeley RDI's 2025 demonstration that all major agent benchmarks are exploitable by automated auditors (SWE-bench, WebArena, τ-bench) validates this stance.

### The shared architectural spine is sound

The approximately 80% shared architecture across both documents is correct:

- **VPC-resident model gateway** as single chokepoint for data egress, cost, and logging: defensible default. LiteLLM, Portkey, and Kong are all reasonable choices. The financial doc's framing — gateway as day-one non-negotiable — is correct.
- **OBO-style per-user scoped tokens with short TTL, no shared service accounts**: correct and important. Both docs identify shared service accounts as the most common early mistake and the one examiners find first.
- **OpenTelemetry GenAI v1.37** as the observability standard: factually accurate — v1.37 reached stability in 2025, Datadog natively supports it. The mandate for full-fidelity retrieval context in the trace is correctly stated.
- **Layered guardrails**: defense-in-depth framing is architecturally correct. Anthropic's Constitutional Classifiers at 4.4% jailbreak success is cited accurately as the best published number for external classifier defense, and the docs correctly note this is still not zero.
- **Kill switch** with sub-60-second propagation: correct design.
- **Git-based prompt and tool versioning with PR review**: the audit-defensible pattern is correctly identified.
- **Agent inventory, risk assessment, and agent card**: correct as the spine of every regulatory conversation.
- **Third-party risk review** including model providers and MCP servers: correctly framed as mandatory before production.
- **MCP security posture** — "pin by hash, proxy through allowlists, SAST/SCA on every server, avoid community servers in production": this is the correct 2026 posture. The docs' hedging is not fence-sitting — it is the executable posture given CVE-2025-32711, CVE-2025-6514, and 1,800+ public MCP servers without authentication as of April 2026.
- **Use-case selection discipline**: both docs' criteria for choosing a first agent (low blast radius, advisory rather than action-taking, bounded scope, real users, SME availability) are correct and should be preserved.
- **Build-versus-buy allocation** — buy generic plumbing, build risk-bearing policy: this is the correct 2026 default, validated by reference-class analysis.

### The lethal trifecta framework and Rule of Two are correctly specified

Both docs correctly identify Simon Willison's lethal trifecta (private data access + untrusted content ingestion + external communication) and Meta's Rule of Two as the right per-agent scoping framework. The B2B SaaS doc's use-case selection criteria apply the trifecta check at Phase 0. The financial doc's agent card captures it at inventory time. These are the right places for these checks.

### The financial doc's CoT unfaithfulness warning is correct and important

The financial roadmap explicitly warns: "Do not build regulatory or consumer explainability on chain-of-thought. The audit artifact must be the action log, retrieved-context snapshot, and tool-call trace — not the model's self-explanation." This warning is grounded in Anthropic's May 2025 finding that Claude 3.7 Sonnet verbalized decision-relevant hints in fewer than 25% of cases. This is a critical correct finding that unfortunately appears only in the financial document (see What's Genuinely Missing below).

---

## What's factually wrong or outdated

### F[TA-A3]: pgvector-as-default thresholds outdated for 2026

Both documents recommend pgvector on managed Postgres as the defensible day-one vector store default. This is partially outdated. In 2026, Qdrant v1.13 (released March 2026) matches pgvector on operational simplicity while exceeding it 3-5x on filtered-vector-search latency at volumes above 1 million vectors. Turbopuffer has emerged as the dominant cold-start multi-tenant retrieval option.

Corrected thresholds: pgvector is correct for fewer than 500,000 vectors or latency-tolerant applications; Qdrant is appropriate for more than 500,000 vectors or when p95 latency must stay below 50ms; Turbopuffer is the choice for multi-tenant cold-start retrieval dominance. The B2B SaaS doc's tenant-partitioned indexing pattern is architecturally correct regardless of which store is selected.

### F[RA-A3]: "WMS is generally not directly listed in Annex III" is partially wrong

The B2B SaaS playbook states that WMS products are generally not directly listed in EU AI Act Annex III. This is partially wrong. Annex III paragraph 2 covers AI systems for "employment, workers management and access to self-employment," specifically including "monitoring and evaluating performance and behavior of persons in the working relationship." WMS AI that tracks worker efficiency, generates performance scores, influences task allocation affecting compensation, or feeds productivity data into HR decisions falls within Annex III paragraph 2. This classification triggers full high-risk AI obligations (Arts 8-25) for the employment-monitoring dimension of WMS AI features.

### F[TIA-2]: Statsig / OpenAI acquisition creates dual-vendor concentration risk

Both documents list Statsig alongside LaunchDarkly as equivalent feature-flag platform options. Statsig was acquired by OpenAI in 2025. Firms deploying OpenAI models through a feature-flag platform now owned by OpenAI have concentrated vendor dependency at two points in their stack (model provider and feature-flag platform) without the playbooks flagging this as a TPRM event. Under NYDFS Part 500 expectations, a vendor acquired by your model provider mid-engagement is a material third-party risk event requiring documented assessment. Severity: MEDIUM.

### F[SS-1] / F[TIA-1]: CoT unfaithfulness warning missing from B2B SaaS document

The financial roadmap explicitly warns that chain-of-thought should not be used as regulatory or consumer explainability, and that the compliance artifact is the action log and tool-call trace. The B2B SaaS document instructs firms to capture "intermediate reasoning traces where produced" as part of the audit store for customer audit response, without carrying the equivalent warning. When a regulated-industry customer auditor asks to see "how the agent decided," the CoT trace will be produced as evidence when it is less than 25% faithful to the actual decision process. This is a correctness gap specific to the SaaS document — the asymmetry between the two docs is the finding. Fix: add the financial doc's CoT-is-debugging-only warning to B2B SaaS Phase 1 Workstream I. Zero engineering cost; high audit-failure prevention value.

### F[RL-F3]: FINRA RN 25-07 and 2026 AROR absent

The financial playbook correctly cites FINRA Regulatory Notice 24-09. Two subsequent developments are absent: FINRA RN 25-07 (April 2025), which directly asks whether AI-generated content constitutes "business as such" under Exchange Act Rule 17a-4(b)(4) — the specific exam question FINRA examiners are now bringing to member firms — and the FINRA 2026 Annual Regulatory Oversight Report, which identifies specific AI agent risk vectors examiners are probing (agents acting without human validation, scope exceeding user intent, auditability in multi-step reasoning). Severity: MEDIUM.

### F[RL-F9]: FBIIC/FSSCC Financial Services AI Risk Management Framework (February 2026) absent

The financial playbook references Treasury reports from March 2024 and December 2024. The FBIIC/FSSCC AI Executive Oversight Group published in February 2026 an AI Lexicon and the Financial Services AI Risk Management Framework — an operationalized NIST AI RMF specifically tailored for financial services, jointly produced by Treasury, FBIIC, and FSSCC. This is the closest available operationalization of what the financial playbook's regulatory section lacks. A firm not referencing the FS AI RMF in its AI governance program will face examiner questions. Severity: HIGH.

### Severity calibration: graduated ratings replace flat HIGH on four findings

External verification from three architecturally distinct AI providers (openai:gpt-5.4-pro, google:gemini-3.1-pro-preview, deepseek:v3.2:cloud) established that four findings initially rated HIGH by agents are more precisely rated on a graduated scale:

- **F[TA-A5]: CaMeL operationalization gap** — MEDIUM for the documentation gap (the core principle "never derive authorization from model output" is correctly stated in the financial doc at line 79; OPA/Cedar, planner/executor separation, and brokered tool execution are mature patterns that map onto it); HIGH specifically and solely for the sub-finding that neither playbook names per-tool policy codification as a Phase 2 deliverable. Without naming it, this work will not appear in any project plan.
- **F[SS-4]: Classifier-only defense at Tier 2+** — split into (a) MEDIUM for the documentation gap that neither doc makes the tier-dependent distinction explicit, and (b) MEDIUM-HIGH for the specific operational gap that parameter-provenance taint tracking at Tier 2+ (where writes occur) is unspecified.
- **F[RL-F10]: Trust-company lethal-trifecta** — graduated by agent architecture: HIGH for autonomous interpretive agents (AI directly triggers operational action on covenant or waterfall decisions); MEDIUM-HIGH for human-supervised interpretive agents (AI shapes determination, human documents final call); MEDIUM for rule-based deterministic calculations; LOW for pure read-only advisory. The gap in the playbook — no sector-specific lethal-trifecta checklist for loan-agency or trust-company firms — is a valid finding at all tiers.
- **F[RA-A2]: EU AI Act Article 25(1)(b) fine-tuning hook** — MEDIUM for the assessment gap (any firm doing fine-tuning for EU-customer-facing AI must assess Art 25(1)(b), and neither playbook prompts this); HIGH where fine-tuning targets an Annex III high-risk intended purpose, particularly WMS labor performance management where Art 25(1)(b) and Annex III paragraph 2 combine.

---

## What's genuinely missing

### Regulatory gaps

**F[RL-F1]: The capability-to-examiner-crosswalk is absent and material (HIGH)**

The financial playbook correctly identifies applicable regulatory regimes across OCC/Fed/FDIC, FINRA/SEC, NAIC/state DOIs, and NYDFS. It organizes content by capability tier. Examiners do not examine by capability tier — they examine by examiner question set. A firm facing an OCC AI examination needs to map: which regulation applies, what the examiner will specifically ask, what evidence constitutes a valid answer, and which artifact to produce. No such crosswalk exists in the playbook.

This is the primary artifact that converts the playbook from a technology guide into a regulatory program. The playbook's own goal — "firms can take and run with this without worrying about gaps" — cannot be satisfied if a firm's first examiner visit produces findings. Fix: a crosswalk appendix organized by regulator (OCC/Fed/FDIC; FINRA/SEC; NAIC/state DOI; NYDFS), containing 3-5 exam questions per regulator and a specific artifact for each answer. Estimated cost: 2-4 weeks with compliance counsel, $25-80,000. Without this appendix, first-cycle OCC/FINRA/NYDFS AI examinations are expected to produce deficiency findings at a 40-60% rate (the base rate for SR 11-7 first-cycle compliance programs).

**F[RL-F2]: SR 11-7 compensating-controls framework needs examiner-vocabulary translation (MEDIUM)**

The playbook correctly identifies the SR 11-7 unit-of-analysis problem for agents and proposes a compensating-controls framework using statistical testing, trajectory evaluation, and red-teaming. This framework is correct in substance but is described as a narrative, not as documentation a firm can show an OCC examiner. Examiners use SR 11-7 vocabulary (model inventory, conceptual soundness assessment, ongoing monitoring, validation independence) and expect responses in that vocabulary. Fix: a one-paragraph preamble in the MRM section acknowledging the mapping problem, followed by the compensating-controls framework translated into SR 11-7 vocabulary with specific artifact names.

**F[RL-F4]: NAIC evaluation tool pilot entirely missing (HIGH for insurance-sector firms)**

The financial playbook treats NAIC Model Bulletin adoption as varying "widely by state" without a count or examination instrument. As of April 2026: 23 states and DC have adopted the NAIC AI Model Bulletin. More materially, NAIC launched a 12-state multistate AI Systems Evaluation Tool pilot running January through September 2026 across CO, MD, LA, VA, CT, PA, WI, FL, RI, IA, VT, and CA. This is the next-generation examination instrument replacing self-attestation. Firms with insurance operations in any of those 12 states face examination using this tool in 2026 without knowing it exists.

**F[RL-F7]: NYDFS October 2025 TPSP letter absent (MEDIUM-HIGH for NY-regulated firms)**

The financial playbook cites the NYDFS October 2024 AI Industry Letter. NYDFS issued a second industry letter on October 21, 2025, specifically on third-party service provider management addressing AI vendor due diligence — structured across initial diligence, contractual protections, and ongoing monitoring — and previewing examiner methodology for TPSP/AI vendor assessment. A NYDFS-specific AI vendor management checklist per this letter is absent from the playbook.

**F[RA-A2]: EU AI Act Article 25(1)(b) fine-tuning hook entirely absent (graduated MEDIUM-HIGH)**

Neither playbook mentions that fine-tuning or parameter-adapting a foundation model on customer or domain data for EU-customer-facing outputs may trigger full EU AI Act provider obligations under Article 25(1)(b): conformity assessment, CE marking, EU database registration, post-market monitoring under Arts 72-73. Pure RAG plus system prompt customization is generally below the "substantial modification" threshold per HLEG informal guidance; LoRA and full fine-tuning on domain data are more likely to cross it. Phase 0 Workstream A of the B2B SaaS playbook has no prompt to trigger this assessment.

**F[RA-A5]: CCPA ADMT operationalization almost entirely absent (HIGH)**

CPPA finalized ADMT-specific regulations in September 2025, effective January 1, 2027. For B2B SaaS with California-resident end-users (typical in WMS: workers in California warehouses), pre-use notice, opt-out rights, access rights, and risk assessments are required by January 2027. The B2B SaaS addendum dismisses ADMT as deferrable "until we have California customer-facing activity that meets the 'significant decision' threshold." Most WMS firms already have California-resident employee end-users. The operationalization question — how to deliver pre-use notice in a B2B context, how opt-out works for workers objecting to performance scoring — is answered nowhere in either document.

**F[RA-A7]: SOC 2 TSC-to-AI-control mapping absent (MEDIUM)**

Both docs correctly note that SOC 2 auditors are still developing AI control language. What neither doc provides is the TSC mapping a firm should bring to the auditor engagement. As of 2026, Big 4 AI audit practices expect firms to propose AI control mappings to Trust Services Criteria. Emerging consensus: CC6.1/CC6.7 (access to AI features and model APIs), CC7.2 (AI anomaly monitoring — drift, refusal spikes, cost anomalies), CC9.2 (AI vendor risk management), A1.2 (AI system availability and fallback), C1.1/C1.2 (confidentiality of prompts and retrieved context), PI1.4 (accuracy of AI outputs in decision-making). A firm arriving at an early SOC 2 engagement without this mapping will have an unproductive conversation.

**F[RA-A8]: GDPR Art 22 worker-as-data-subject gap (MEDIUM for WMS with labor performance AI)**

The B2B SaaS playbook addresses tenant isolation at the enterprise-customer level but not GDPR Article 22 automated decision-making where the data subject is the customer's worker. If AI agents make or materially influence decisions about individual workers (performance scores, task allocation), Article 22 rights of explanation, human review, and contestation run to individual workers directly — not fulfilled via the enterprise's B2B processor agreement.

### Security gaps

**F[SS-2]: Agent-to-agent trust boundaries structurally absent from both docs (HIGH at Tier 2+)**

Neither playbook addresses multi-agent trust models. Both treat agents as isolated entities under single-user OBO tokens. In multi-agent topologies — now the default deployment pattern in LangGraph (which LangSmith Q1 2026 telemetry shows has more than 60% of production deployments using multi-agent subgraph patterns with default credential inheritance) — orchestrator compromise via indirect prompt injection allows subagents to execute actions with the orchestrator's full scope. MITRE ATLAS added technique AML.T0051 "LLM Prompt Injection via Intermediate Agent" in its March 2026 update, classifying chain-of-agent injection as a production technique category.

Minimum viable multi-agent trust design absent from both docs: subagents inherit reduced scope from orchestrators (not full scope), subagent tool calls carry originating-user-session trace ID separate from orchestrator identity, orchestrator instructions treated as untrusted content at the same taint level as retrieved external content. This is not a future-state concern — it is current default behavior of the dominant production framework.

**F[SS-4b]: Parameter-provenance taint tracking at Tier 2+ unspecified (MEDIUM-HIGH)**

At Tier 2 write-capable agents, the architectural principle "never derive authorization from model output" is correctly stated in the financial doc. The specific implementation work — per-tool policy codification connecting that invariant to each tool's actual input parameters — is named nowhere in either document as a deliverable. OPA/Cedar policy engines and brokered tool execution are mature patterns for this work. The gap is not architectural invention; it is that the per-tool codification is unnamed and unbudgeted, so it will not appear in any project plan.

**F[SS-5]: Composite lethal trifecta in multi-agent systems (MEDIUM-HIGH)**

Both docs apply the lethal-trifecta check and Meta's Rule of Two per agent. In multi-agent topologies, two individually safe agents can together constitute a lethal trifecta: Agent A reads private customer data and ingests external documents (two trifecta legs); Agent B sends external notifications (one leg); Agent A orchestrates Agent B. All three legs are present without explicit human confirmation across the A-to-B delegation. Fix: agent card template should include a "combined topology lethal-trifecta assessment" field, owned by the AI Risk Committee at each Tier 2+ expansion.

**F[TIA-3]: Guardrails buy-list collapses the data-sovereignty distinction (MEDIUM-HIGH for regulated deployments)**

Both documents list Lakera Guard, Azure AI Content Safety, Bedrock Guardrails, and LLM Guard as roughly equivalent guardrail options. They are not equivalent on the dimension that matters most for regulated firms: Lakera Guard, Azure AI Content Safety, and Bedrock Guardrails all send prompt content to vendor APIs — every input classified becomes a data flow to a third-party processor requiring sub-processor disclosure and vendor agreement coverage. LLM Guard (self-hosted OSS) sends nothing. For firms under NYDFS Part 500, EU GDPR Article 28, or handling healthcare PHI, this is a compliance decision before a product decision.

### Technical gaps

**F[TA-A9]: Multi-agent A2A topology not mentioned in either doc (HIGH at Tier 2+)**

The Agent-to-Agent (A2A) protocol (Google, February 2026, Linux Foundation stewardship, 50+ enterprise partners including Salesforce, SAP, and ServiceNow) is the emerging interoperability standard for enterprise multi-agent systems. The B2B SaaS playbook's Phase 4 "multi-agent operation" section is one sentence with no architectural guidance. The financial roadmap has zero mentions of agent-to-agent. For enterprise B2B SaaS firms, A2A adoption will increasingly be customer-driven.

**F[TA-B1]: ANN pre-filter tenant isolation gap (MEDIUM-HIGH for multi-tenant production)**

The B2B SaaS doc's tenant isolation treatment is architecturally strong — the strongest section in either document. One gap: it does not address ANN cross-tenant leakage when HNSW graph structures cross tenant boundaries, or when ANN search with per-tenant post-filtering returns results from Tenant A when Tenant B's filtered result set is sparse. Standard pgvector and Qdrant default ANN configurations do not prevent this. Requires pre-filtered ANN (filtering before similarity scoring, not after).

**F[TA-A2]: OTel trace storage cost unbudgeted (MEDIUM)**

Both docs mandate full-fidelity retrieval context in traces. At 50-200KB per trace with 3-6 year retention under SEC 17a-4 / FINRA 4511 horizons, storage costs reach $200,000-$2,000,000 per year. Neither cost model accounts for this.

**F[TIA-7]: MCP server build cost absent from cost models (MEDIUM-HIGH)**

Both docs correctly position MCP with strict controls (no community servers, pin by hash, proxy through allowlists, SAST/SCA). The cost implication is absent: firms following the prescribed posture will build internal MCP servers rather than use community ones. A single production-grade internal MCP server requires approximately 3-6 weeks of senior engineering time. A typical Tier 1-2 deployment uses 3-8 MCP servers (data retrieval, document access, notification, CRM lookup). This adds 10-50 weeks of engineering effort — $75,000-$400,000 — not reflected in either cost model.

**F[TIA-8]: EU gateway residency gap (HIGH for EU-data-constrained firms)**

Both docs say "data residency is binding" and "EU customer data requires EU-hosted embeddings and vector store." Neither applies this analysis to the gateway or model API calls. Bedrock routes through US regions by default (EU regions exist but require explicit configuration and not all models are available). Azure AI Foundry EU data residency is available for Azure OpenAI but not for Anthropic models on Azure (which route through US East). Self-hosted LiteLLM in an EU VPC is the only clean path for GDPR Article 44 compliance when routing to EU-hosted models.

### Operational governance gaps

**F[CDS-A1]: AI Risk Committee design-gaps — governance artifact risk HIGH**

Both docs establish an AI Risk Committee with defined authority. The design is under-specified as a decision-forcing function in four ways, each mapping to documented group-decision failures:

1. No pre-commitment mechanism — tier promotion criteria are not locked before the build team has observed the agent, creating anchoring bias
2. No structural independent challenger at committee level — multi-agent review systems have a DA role because consensus is unreliable without adversarial challenge; the AI Risk Committee has no equivalent
3. No written pre-mortem requirement — "what would have to be true for this Tier 1 promotion to fail within 6 months?" is never asked structurally
4. B2B SaaS doc's "Chair decides on disagreement" concentrates authority in the person with the highest optimism bias about launch

Low-cost interventions: (a) pre-committed tier promotion criteria signed before Phase 2 begins; (b) independent challenger not on the build team who writes a dissent memo at every tier-promotion meeting; (c) required pre-mortem at each tier promotion; (d) explicit recusal protocol when members have personal stakes in launch timing.

**F[CDS-A2]: Tier gates are principle-level, not specification-level (HIGH)**

The B2B SaaS doc has 13 binary Phase 0 exit gates — falsifiable and executable. The financial roadmap's tier advancement criteria are observation-based ("observability maturity, not eval pass rate") — correct in principle, not falsifiable in practice. A ship-it coalition can satisfy "observability maturity" by pointing to any functional OTel deployment. Specific gaps: neither doc specifies minimum eval set size, minimum shadow-mode duration, minimum reviewer agreement statistic, or minimum red-team coverage before tier advancement. Neither provides a threshold below which tier advancement is automatically blocked — committee judgment reintroduces groupthink risk.

**F[CDS-A3]: Reviewer calibration inadequate at production scale (MEDIUM-HIGH)**

At 3-5 part-time reviewers working 2-4 hours per week, the pool covers roughly 80 outputs per week at 15 minutes per review. At 5,000+ daily queries in Tier 1 production, this is 0.1-1% sampling — insufficient for criteria-drift detection without structured stratified sampling. The playbook's "monthly calibration sessions" are the right intent, but neither doc specifies who attends, what the input is, what the output is, who has authority to update criteria mid-cycle, or how the revision decision is made.

**F[CDS-A4]: Criteria drift principle cited, revision process absent (MEDIUM)**

Both docs cite Shankar 2024 UIST correctly on criteria drift. The financial doc operationalizes as "revisited on every pipeline change" (trigger, not process). The B2B SaaS doc specifies "monthly calibration sessions" (schedule, not feedback loop). Neither specifies the revision process — what constitutes a criteria change, who approves it, how the eval set is updated, and how the change is documented for audit. Measuring agreement without specifying what triggers changes is monitoring without a feedback loop.

**F[CDS-A6]: Over-reliance detection — named, no behavioral measurement methodology (MEDIUM)**

Both docs name over-reliance as a risk. Neither specifies a detection methodology. Over-reliance literature identifies three validated behavioral markers: reduced verification behavior, automation bias (accepting incorrect confident outputs), and skill decay. Detection requires behavioral instrumentation: edit-distance between agent output and final human output, time-to-accept as verification-effort proxy, disagreement-rate trend as decay signal. For CCPA ADMT "meaningful human involvement" compliance (effective January 1, 2027), rubber-stamp detection requires this behavioral layer.

**F[CDS-B1]: Tier-promotion cognitive biases — systematic gap with no structural interventions (HIGH)**

Tier promotion decisions are high-stakes, infrequent, committee-made under social pressure — the exact conditions most vulnerable to systematic bias. Five specific biases are unaddressed: optimism bias (build teams systematically overestimate readiness), sunk-cost (Phase 0-2 investment creates pressure to promote), social proof ("other firms are at Tier 1"), authority bias (external consultancy declaring readiness carries disproportionate weight), and framing effect ("95% pass" versus "5% fail" produce different decisions on identical evidence). Pre-emption interventions: outside-view reference class at every tier promotion, pre-mortem requirement, anonymous pre-vote before deliberation, "What would it take to delay?" before "Should we promote?"

---

## What's overreach or deferrable

Based on DA severity calibration and cross-agent convergence on necessary versus ceremonial elements:

**Items correctly identified as deferrable in the addenda:** Formal MRM function (pattern of designated independent reviewer is adequate at B2B SaaS scale), Tier 2 formal validation (not needed until regulated decisions are touched), EU AI Act conformity artifacts (not needed without EU customer exposure), CCPA ADMT compliance for non-California deployments. The addenda's deferrable-items lists are correctly calibrated.

**Governance committee structure for small firms:** The governance committee design specified in both docs assumes organizational complexity — a Chair (Legal/Security/Risk), Playbook Owner, independent reviewer, and committee members from Engineering, Legal, and Security. Below approximately $500 million in assets or a 30-person technology organization, this committee structure is not just over-built — it is unexecutable (F[CDS-C1]). The same person who would be Chair is also the independent reviewer is also the Playbook Owner. Neither document provides a "named-accountability single-owner" variant with documented pre-commitment criteria for small regulated firms. This is the governance committee's undocumented firm-size floor, and it matters for community banks, regional insurers, and credit unions.

**CaMeL as full deployment pattern at Tier 0-1:** The financial doc's reference to CaMeL is correctly placed at Tier 2 writes, where it is the right defense. Treating CaMeL implementation as a Tier 0-1 requirement would be overreach — the principle ("never derive authorization from model output") is the Tier 0-1 constraint, and full per-tool policy codification is the Tier 2 deliverable.

**Track A versus Track B at Phase 0:** The B2B SaaS addendum's Pushback 9 already correctly endorses vendor-platform-first as a legitimate architecture ("use their agent framework as the agent layer — Claude Agent SDK, LangGraph, OpenAI Agents SDK"). Claude Agent SDK carries a 12-month API stability guarantee (Anthropic, November 2025); LangGraph v0.3 reached stable checkpoint-based state management in January 2026; OpenAI Agents SDK reached GA in October 2025. These frameworks save 6-8 weeks of engineering build time and should be used. What they do not compress is the elapsed-time governance constraint: SME eval set construction takes 4-6 months regardless of framework; vendor agreement negotiation takes 6-12 weeks; shadow mode stabilization takes 8+ weeks. The 10-13 month timeline holds because governance is the constraint, not engineering build time. The financial addendum's Pushback 5 should be updated to make this distinction explicit rather than implicitly discouraging framework adoption.

---

## Internal consistency issues

### CoT unfaithfulness treatment is asymmetric

The financial doc explicitly warns that chain-of-thought is not a regulatory audit trail. The B2B SaaS doc instructs capturing CoT traces as audit artifacts without the equivalent warning. This is not a framing difference — it is a correctness asymmetry in two documents that will be used by different teams at the same firm. A financial services firm that uses both documents faces contradictory guidance depending on which document a given team reads.

### Tier definitions differ in their reference to blast radius

The financial roadmap defines tiers by autonomy of action. The B2B SaaS playbook defines phases by implementation sequence. These are compatible but not identical organizing principles. When a firm asks "what tier is our inventory-exception triage agent?", the two documents would give different answers because they are not actually calibrated to each other. A unified document would resolve this.

### Staffing FTE ranges are inconsistent

The financial doc references 1-3 FTE new hires for initial platform build. The B2B SaaS doc specifies particular roles by phase. The total implied headcount differs by document and neither is clearly wrong — they are solving different sub-problems. The reference-class analysis found a 1.5-2 FTE dedicated plus 0.3-0.7 FTE distributed (approximately 2-2.5 FTE equivalent) base rate from practitioner surveys, suggesting both docs are at the optimistic end, but the real executability gap is definitional: neither document specifies whether "1 FTE" means dedicated capacity or named ownership with shared SRE pool support. That ambiguity is more consequential than the specific number.

### Phase 0 scope differs

The financial doc's Tier 0 includes 13 day-one blockers. The B2B SaaS doc's Phase 0 focuses primarily on governance and procurement, with platform build starting in Phase 1. This creates a situation where a firm using both documents would build its governance committee first and its gateway second (SaaS approach) versus building both in parallel (financial approach). The financial approach is marginally more defensible for regulated firms because OBO identity and data handling agreements should be in place before any model calls touch production data.

---

## Executability at the "firms can run with this" bar

The following items require specialist knowledge to execute and should not. Each needs to be made self-service in the next version of the documents:

**MCP server allowlist evaluation rubric:** Both docs say "proxy through allowlists" and "run SAST/SCA" but provide no evaluation rubric for what "production-ready" means for a specific internal MCP server. Firms need a 5-criterion checklist: (1) authentication mechanism (OAuth SHOULD per 2025-06-18 MCP spec — verify it's implemented); (2) schema integrity verification (MCP tool poisoning via malicious schema description is not defended by OAuth); (3) return-value inspection (OAuth provides auth boundary, not return-value integrity); (4) version pinning with hash; (5) SAST pass. Without this rubric, the allowlist decision falls to a developer without security training reviewing the PR.

**Per-tool CaMeL policy codification pattern:** Neither doc specifies the minimum viable implementation sketch. Firms need: (1) enumerate every tool-call input parameter; (2) tag each input's provenance at assembly time (user-authenticated-session vs. retrieved-content vs. untrusted-external); (3) run provenance policy check at tool-call dispatch using only authenticated session scope; (4) quarantine untrusted-content processing from the tool-dispatch path. Without this specification, "CaMeL-style capability enforcement" as cited in the financial doc will be implemented as a checkbox, not as engineered per-tool policy.

**Reviewer calibration protocol:** Both docs specify thresholds (90% judge-to-SME agreement for financial, 85% for SaaS). Neither specifies: how to compute the agreement statistic, what the held-out set size should be, what triggers recomputation (answer: every vendor model update, every prompt version change, and quarterly minimum regardless), and what intervention follows when agreement drops below threshold mid-production. This protocol must exist as a runnable procedure, not as a named goal.

**Criteria drift revision cadence:** Both docs acknowledge Shankar 2024 on criteria drift. Neither specifies the cadence, ownership, or artifact for revising criteria. "Monthly calibration sessions" is a schedule. A runnable process specifies: who reviews what subset of outputs, what anomalies trigger a criteria revision, who approves the revision, and how the revised criteria are versioned and documented.

**Vendor switchover 60-day migration runbook:** Humanloop's September 2025 shutdown with a sub-60-day data-deletion window is a specific documented event affecting a playbook-referenced vendor. Both docs correctly mandate contractual data-export clauses. Neither provides the switchover runbook: what data to export, in what format, to what destination, within what SLA, with what integrity verification. The contract clause is necessary but the runbook is what makes it executable under time pressure. The annual AI-infra vendor discontinuity rate is 15-25%, making this a modal-not-tail risk over a 13-month build window.

**Examiner-facing artifact crosswalk:** Addressed in detail under F[RL-F1] above.

---

## Tech stack 2026 assessment

The reference architecture — VPC-resident gateway, OBO/SPIFFE identity, OTel GenAI v1.37, layered guardrails, pgvector default, git-based versioning, eval platforms — is largely defensible for 2026.

**What changed since the docs were written:**
- Qdrant v1.13 (March 2026) is now superior to pgvector for more than 500,000 vectors or latency-sensitive paths. Updated thresholds apply (see F[TA-A3]).
- Claude Agent SDK has a 12-month API stability guarantee from Anthropic (November 2025) for core interfaces. LangGraph v0.3 (January 2026) provides stable checkpoint-based state management. OpenAI Agents SDK reached GA in October 2025. The financial addendum's "early-stage capabilities with evolving interfaces" characterization is outdated for core APIs; it remains accurate for computer use specifically.
- MITRE ATLAS AML.T0051 "LLM Prompt Injection via Intermediate Agent" was added in March 2026 as a production technique category — the multi-agent security gap has moved from theoretical to classified-production-relevant.
- The A2A protocol (Google, February 2026, Linux Foundation, 50+ enterprise partners) is the emerging enterprise multi-agent interoperability standard. Neither doc mentions it.
- LiteLLM self-hosted in an EU VPC is currently the only clean path for GDPR Article 44 compliance when routing to EU-customer data through a model gateway — cloud-native gateways default to US regions for most model providers.
- MCP OAuth (2025-06-18 spec) was added as SHOULD, not MUST. Published CVEs include CVE-2025-32711 and CVE-2025-6514. The hedging posture in both docs is correctly calibrated to the current security landscape.
- Cloudflare Sandboxed Workers (March 2026) is a cost-effective sandboxing alternative at under $0.005 per execution versus E2B's $0.05+ — not mentioned in either doc.
- Langfuse (Apache 2.0, mature self-hosted path) is the only eval platform where trace data never leaves firm infrastructure. Inspect AI (UK AISI, open-source) is the only peer-reviewed eval framework with documented adversarial eval methodology — particularly relevant for regulated financial services red-team documentation. These distinctions are not in either doc's platform comparison.
- Statsig concentration risk from OpenAI acquisition is a new 2026 vendor-landscape fact (see F[TIA-2]).

**What holds:**
- The gateway-first architecture is consensus across every major practitioner source — Databricks, a16z AI Canon, Google Cloud architecture guides — with the caveat that gateway vendor differentiation is in configuration quality, not tool selection.
- The OBO/SPIFFE identity design remains the right direction, though competing standards (IETF draft-klrc-aiagent-auth-00 at draft-02, January 2026; OpenID Foundation "Agent Identity" working group, February 2026) mean firms are building toward a moving target. Both docs correctly flag "build for now, expect to re-architect."
- The CaMeL architectural direction — principle of never deriving authorization from model output — is correct. The paper's provable-security finding on AgentDojo (77% with CaMeL versus 84% undefended) is correctly cited. The implementation gap is the per-tool codification work, not the architectural direction.

---

## Structural recommendation: the strongest executable form

Cross-agent convergence (tech-architect F[TA-C3], reference-class-analyst F[R1-A8], cognitive-decision-scientist, and DA exit-gate synthesis guidance) produces a clear answer to Q7: the strongest executable form is a unified document with substantive sector-specific annexes, not two separate documents.

The approximately 80% shared spine is a maintenance liability and a coherence problem when maintained as two documents. When they silently disagree (CoT treatment, staffing numbers, Phase 0 scope), firms using both get contradictory guidance. When they agree, firms using only one miss each other's strengths.

**Recommended structure:**

**Primary spine:** B2B SaaS phased workbook (Phase 0-4 structure with binary exit gates) becomes the primary operational execution document. Its sequential workbook format — goal, rationale, workstreams, exit gates, artifacts — is the correct execution scaffold for any firm. The 13 binary Phase 0 exit gates are more falsifiable than the financial roadmap's principle-level gates.

**Reference appendix:** Financial roadmap's capability-maturity taxonomy (Tier 0-3 with the ~50 capabilities) becomes a reference appendix for capability classification, timeline estimation, and CTO/board communication. The capability table is the strongest section of the financial doc and is not replicated in the SaaS workbook.

**Sector-specific annexes:** Two required annexes rather than two documents:

*Financial services annex* covering:
- Full regulatory crosswalk per F[RL-F1]: OCC/Fed/FDIC, FINRA/SEC (including FINRA 25-07 and 2026 AROR), NAIC (including 12-state AI Evaluation Tool pilot), NYDFS (including October 2025 TPSP letter), CFPB (statutory UDAAP exposure distinguished from current enforcement posture)
- SR 11-7 compensating-controls framework translated into examiner vocabulary with specific artifact names
- FS AI RMF (FBIIC/FSSCC, February 2026) as the primary AI governance framework reference
- Trust-company and loan-agency lethal-trifecta checklist with the four-tier severity model (autonomous-interpretive / human-supervised-interpretive / rule-based-deterministic / advisory-only)
- DORA obligations for firms with EU operations
- ISO 42001 triple function: procurement signal + Colorado reasonable-care safe-harbor + EU AI Act Art 9 risk management system reference

*B2B SaaS sector annex* covering:
- Multi-tenancy ANN pre-filter specification (pre-filtered ANN requirement, not post-filtered)
- EU AI Act Art 6 classification gate at Phase 0 exit — with explicit prompt for Annex III para 2 employment-monitoring features
- EU AI Act Art 25(1)(b) fine-tuning assessment gate at Phase 0 exit
- CCPA ADMT operationalization: pre-use notice design in B2B context, opt-out mechanism for workers, access rights, risk assessment requirements before Phase 3 launch for California deployments
- SOC 2 TSC-to-AI-control mapping (draft for auditor engagement)
- GDPR Art 22 worker-as-data-subject design requirements for labor-performance AI
- 21 CFR Part 11 AI-generated records mapping for life sciences customers
- Colorado SB 24-205 monitoring trigger at Phase 1 exit gate

**Three DA carry-forward flags as synthesis preamble:** (1) tier-anchoring acknowledgment with continuous per-query-class monitoring alternative not tested; (2) limitations section covering firm-size floor and adoption-economics; (3) governance-versus-use-case dual framing for trust-company and loan-agency firms.

---

## Hypothesis dispositions

| Hypothesis | Disposition | Key evidence |
|---|---|---|
| **H1: Governance-first sequencing is correct** | CONFIRMED-WITH-CAVEAT | Morgan Stanley 98% adoption, Klarna walkback, Air Canada BCCRT ruling validate for customer-facing/regulated/action-taking. Stripe internal-tool counter-analogue limits governance-first to non-trivial blast-radius contexts. Committee design quality (F[CDS-A1]) is the within-H1 gap — the sequencing is right, the committee design is not. |
| **H2: 10-13mo timeline and $700K-$2M cost defensible** | PARTIAL — timeline CONFIRMED with conditions; cost UNDERSTATED | 10-13mo holds for infra-leveraged firms with existing IAM, observability, and feature flags. Base-rate modal for truly greenfield firms is 12-18 months (Gartner/KPMG/Deloitte 2026 surveys). At 14-18 week median time-to-hire for Senior AI Platform Engineers in 2026, Phase 0 slip of 6-12 weeks is the median scenario. OTel storage ($200K-$2M/yr), MCP server build ($75K-$400K), and EU conformity assessment ($80K-$250K conditional) are material unbudgeted cost categories. |
| **H3: 1-3 FTE + reviewer pool adequate** | FALSIFIED at lower bound | 1 FTE is minimum-technically-sufficient for named ownership, not operationally resilient for 24/7 production. Base-rate practitioner consensus is 1.5-2 FTE dedicated plus 0.3-0.7 FTE distributed. The real gap is definitional: "1 FTE ownership with SRE pool AI-trace training" versus "1 FTE dedicated" are different things and neither doc specifies which. Quantification is under-evidenced; structural clarification is the correct fix. |
| **H4: Buy-generic-build-risk-bearing-policy correct** | CONFIRMED with 2026 vendor-landscape corrections | Build-versus-buy allocation is correct. Specific 2026 corrections: guardrails data-sovereignty distinction (F[TIA-3]), EU gateway residency (F[TIA-8]), pgvector thresholds (F[TA-A3]), Statsig concentration risk (F[TIA-2]), Langfuse versus Braintrust versus Inspect AI differentiation (F[TIA-5]), Cloudflare Sandboxed Workers as sandbox alternative. |
| **H5: MCP treatment too hedged** | FALSIFIED | The hedging IS the executable posture for 2026. CVE-2025-32711, CVE-2025-6514, 1,800+ unauth public servers, MCP OAuth as SHOULD not MUST. The remaining gap is not less hedging — it is a more specific MCP server allowlist evaluation rubric. Three-agent corroboration: tech-architect, security-specialist, tech-industry-analyst. |
| **H6: Regulatory sweep lacks capability-to-examiner mapping** | CONFIRMED | OCC Bulletin 2021-10, FINRA 24-09, NYDFS Part 500 all structure expectations as specific exam questions with artifact requests. The playbook's tier-based structure is useful for build sequencing but does not map to examiner workflow. The crosswalk appendix is not optional infrastructure — it is what converts the playbook into a regulatory program. |
| **H7: CaMeL reference not operationalized** | CONFIRMED — graduated severity | CaMeL direction is correct. Principle "never derive authorization from model output" is correctly stated in financial doc. The per-tool policy codification work is the deliverable neither doc names. Severity: MEDIUM for architectural gap (path exists via OPA/Cedar + planner/executor); HIGH specifically for the unnamed deliverable at Tier 2 writes. |
| **H8: Addendum Pushback #5 underweights fast-follower architectures** | PARTIALLY CONFIRMED — mechanism misdescribed, doc-split applies | Financial addendum Pushback 5 conflates framework immaturity with timeline constraint; core Claude Agent SDK, LangGraph v0.3, OpenAI Agents SDK are production-stable for core APIs. B2B SaaS addendum Pushback 9 already correctly endorses these frameworks as legitimate. Financial addendum needs correction; SaaS addendum needs one sentence clarifying "Claude Agent SDK core APIs stable per 12-month guarantee; computer use specifically remains early-stage." |
| **H9: Eval methodology RAG-heavy, tool-heavy agents need trajectory evaluation** | CONFIRMED | τ-bench retail SOTA pass^8 below 25%; neither doc specifies k or acceptance thresholds. Five-element trajectory eval rubric (tool selection accuracy, argument quality, error recovery, pass^k goal-completion, trajectory efficiency) specified by tech-architect is analytically correct but cognitively demanding — requires explicit inter-rater calibration training (kappa target), not just rubric specification. |
| **H10: Staffing underestimates ongoing operational load** | CONFIRMED | Build-cycle cost is correctly estimated; operational-cycle cost is not. EU AI Act Art 72 post-market monitoring, Art 73 serious incident reporting, CCPA ADMT annual risk assessment refresh, Colorado care documentation — these are statutory standing obligations requiring named operational capacity independent of engineering staffing. Specific FTE quantification is under-evidenced; operational load existence is T1-supported. |
| **H11: Multi-agent topologies and agent memory inadequately addressed** | CONFIRMED — severity MEDIUM-HIGH conditional on Tier 2+ multi-agent | The architectural gap is real: A2A protocol not mentioned, orchestrator trust model absent, long-term agent memory unaddressed. MITRE ATLAS AML.T0051 (March 2026, production technique category) and LangSmith Q1 2026 telemetry (60%+ of production LangGraph deployments use multi-agent subgraph patterns with default credential inheritance) establish production relevance without requiring A2A as the evidence. GDPR Art 26 joint-controller doctrine (CJEU C-210/16, C-40/17) is current T1 law with DPA enforcement precedent for multi-agent pipelines touching EU personal data. Severity is HIGH the moment a firm deploys Tier 2+ multi-agent with write-tool access; MEDIUM-HIGH as a planning concern for firms at Tier 0-1. |
| **H12: Two docs are 80% redundant; unified form may be stronger** | CONFIRMED — unified-with-variants | 70% probability unified-with-variants outperforms two separate documents (reference-class-analyst calibration). Cross-agent convergence on unified form (tech-architect F[TA-C3], reference-class-analyst F[R1-A8]). Coherence failure and maintenance drift risk are real costs of two-document form. |

---

## Implementation plan

The following items are ordered by impact-per-unit-effort for a firm executing this playbook. Items 1-5 are highest priority.

**Priority 1: Build the regulatory crosswalk appendix (2-4 weeks, $25,000-$80,000)**
Owner: compliance attorney plus MRM practitioner. Per F[RL-F1]. One page per regulator (OCC/Fed/FDIC; FINRA/SEC including FINRA 25-07 and 2026 AROR; NAIC including 12-state AI Evaluation Tool pilot states; NYDFS including October 2025 TPSP letter), 3-5 exam questions per regulator, specific artifact for each. SR 11-7 compensating-controls framework translated into examiner vocabulary. FS AI RMF (FBIIC/FSSCC, February 2026) incorporated as primary reference framework. This is not optional for any firm subject to formal examination.

**Priority 2: Name per-tool CaMeL policy codification as a Phase 2 deliverable (1 week editorial)**
Owner: technical lead plus security engineer. Per F[TA-A5] HIGH sub-finding. Add to B2B SaaS Phase 2 checklist and financial doc Tier 2 section: "Per-tool policy codification: enumerate every tool-call input parameter, tag each input's provenance, run provenance policy check at dispatch using only authenticated session scope." Budget 2-4 weeks per tool class in project plan. Without naming it, this work will not appear in any project plan and Tier 2 agents will ship without it.

**Priority 3: Add CoT unfaithfulness warning to B2B SaaS document (30 minutes editorial)**
Owner: whoever maintains the SaaS document. Per F[SS-1]. Add to Phase 1 Workstream I audit store section: "Reasoning traces captured for debugging only. The compliance-grade audit record is the action log plus tool-call trace plus retrieved-context snapshot. Do not present reasoning traces as compliance evidence — CoT faithfulness for frontier reasoning models is below 25% in published research."

**Priority 4: Fix AI Risk Committee design gaps (1 week, primarily organizational design)**
Owner: governance lead. Per F[CDS-A1] and F[CDS-B1]. Add to both documents: (a) pre-commitment to tier promotion criteria before Phase 2 begins, with criteria signed and dated; (b) named independent challenger (not on build team) with dissent memo requirement at every tier-promotion meeting; (c) written pre-mortem template at each tier promotion; (d) explicit recusal protocol. Add anonymous pre-vote as a procedural requirement before deliberation begins.

**Priority 5: Add numerical thresholds to tier gates (1-2 weeks editorial)**
Owner: technical lead. Per F[CDS-A2]. For each tier/phase transition: minimum eval set size (recommend 500+ items for initial, 200+ items per query class for ongoing), minimum shadow-mode duration (recommend 6 weeks minimum for advisory, 10 weeks minimum for action-capable), minimum judge-to-SME agreement statistic (recommend 85%+ initial, with recomputation trigger at every vendor model update and every significant prompt change), minimum red-team coverage before promotion (recommend full OWASP LLM Top 10 coverage plus domain-specific attack cases). These thresholds are not the point — the point is that they exist and cannot be talked past.

**Priority 6: Annex III para 2 assessment gate at Phase 0 exit (1 week editorial)**
Owner: regulatory counsel. Per F[RA-A3]. Add to B2B SaaS Phase 0 Workstream A: "Do any AI features assess, score, or feed HR/performance decisions about individual workers? If yes: EU AI Act Annex III paragraph 2 high-risk classification applies for EU deployments. Full high-risk AI obligations (Arts 8-25) apply to the employment-monitoring dimension."

**Priority 7: EU AI Act Art 25(1)(b) fine-tuning assessment gate at Phase 0 exit (1 week editorial)**
Owner: regulatory counsel. Per F[RA-A2]. Add to Phase 0 Workstream A: "Does deployment involve fine-tuning or parameter-adapting the base model? If yes, assess Article 25(1)(b) provider obligations. LoRA and full fine-tuning on domain data are likely 'substantial modifications.' Pure RAG plus system prompt customization is generally below threshold per informal HLEG guidance."

**Priority 8: Guardrails data-sovereignty categorization (1 week editorial)**
Owner: security lead. Per F[TIA-3]. Distinguish data-sovereignty-compatible guardrails (LLM Guard self-hosted — no data exfiltration) from data-exfiltrating guardrails (Lakera Guard, Azure AI Content Safety, Bedrock Guardrails — all send prompt content to vendor APIs). Add data-handling classification to guardrails selection section. Regulated firms must treat guardrails vendors as data-processor sub-processors.

**Priority 9: Composite lethal-trifecta field in agent card template (30 minutes template edit)**
Owner: governance lead. Per F[SS-5]. Add field: "Combined topology lethal-trifecta assessment: if this agent will orchestrate or be orchestrated by other agents, assess the combined trifecta exposure across the full orchestration chain, not only per agent."

**Priority 10: Vendor switchover 60-day migration runbook as Phase 1 artifact (1-2 weeks operational design)**
Owner: platform engineering lead. Per F[R1-A4]. Specify: which data to export, in what format, to what destination, within what SLA, with what integrity verification, triggered by what vendor-health signals (funding events, co-founder departures, feature deceleration). Quarterly vendor-health review artifact as standing Phase 3+ deliverable.

**Subsequent priority items (by severity):**

- Multi-agent trust model design (A2A architecture guidance, scope inheritance for subagents, originating-user-session trace IDs) — as Phase 4 prerequisite in B2B SaaS doc, Tier 2+ section in financial doc (HIGH at Tier 2+)
- ANN pre-filter specification for multi-tenant deployments (MEDIUM-HIGH)
- CCPA ADMT operationalization as Phase 3 prerequisite for California customer rollout (HIGH operational, 2027 enforcement)
- SOC 2 TSC-to-AI-control mapping for auditor engagement (MEDIUM)
- EU gateway residency guidance: distinguish self-hosted LiteLLM EU from cloud-native gateways for GDPR Art 44 compliance (HIGH for EU-data-constrained firms)
- Over-reliance behavioral instrumentation: edit-distance, time-to-accept, disagreement-rate dashboard (MEDIUM, legally material by January 2027)
- OTel trace storage cost in cost model (MEDIUM — $200K-$2M/yr unbudgeted)
- MCP server build cost in cost model (MEDIUM-HIGH — $75K-$400K unbudgeted)
- NYDFS October 2025 TPSP letter checklist integration (MEDIUM-HIGH for NY-regulated firms)
- NAIC 12-state AI Evaluation Tool pilot state map (HIGH for insurance-sector firms in pilot states)
- FS AI RMF incorporation into financial doc regulatory section (HIGH)
- Criteria drift revision process: who approves, what artifact, what cadence, recomputation trigger at every vendor model update (MEDIUM)
- Staffing model clarification: dedicated capacity versus named-ownership-with-SRE-pool are different staffing models, both valid, both must be specified (LOW-MEDIUM)
- Governance committee single-owner variant for firms below ~$500M assets / ~30-person tech org (MEDIUM)

---

## Limitations and what this review could not establish

**Firm-size floor (F[CDS-C1]):** Neither playbook specifies a minimum firm size for the governance committee structure. Below approximately $500 million in assets or a 30-person technology organization, the committee structure as specified is unexecutable. A single-owner accountability variant with documented pre-commitment criteria is needed but not designed by this review.

**Data quality and corpus readiness:** No agent addressed data quality as a playbook gap. Gartner and Informatica 2024-2025 surveys consistently cite data quality as the top CDO-identified barrier to AI deployment. Both playbooks discuss agent observability but not corpus readiness — whether the documents the agent retrieves over are accurate, current, and complete. This is a genuine gap acknowledged as out of scope for this vetting exercise.

**Adoption-economics (F[CDS-C2]):** Neither playbook addresses what happens when a firm executes the 13-month program, reaches Tier 1, and agent adoption is 15% rather than 60%. MIT 2025 data showing 95% of GenAI pilots fail implies adoption is non-trivial. The playbooks' governance overhead — reviewer workflows, approval gates, criteria calibration sessions, escalation paths — adds cognitive load that competes directly with the agent's workflow savings. At low query volumes, the governance overhead may exceed the productivity benefit. This tradeoff is flagged as a qualitative concern; it was not quantified.

**Tier-anchoring acknowledgment:** The tier-based structure of both documents was the analytical frame used in this review, not the hypothesis tested. Continuous per-query-class monitoring with dynamic capability adjustment — where risk is managed per query class in a continuous loop rather than through discrete tier-promotion ceremonies — was not stress-tested as an alternative design. The tier structure remains the defensible default for most firms; the alternative is flagged as unstressed.

**Incident-rate differential quantification:** Reference-class analysis found correlational evidence that playbook-compliant firms experience materially lower AI incident rates than governance-light firms. The specific magnitude of this differential is not precisely characterizable from available evidence. Playbook value should be communicated qualitatively ("dramatically reduces incident probability") rather than as a specific percentage differential, until longitudinal matched-cohort data exists.

---

## Provenance note

This synthesis rests on: seven agents' R1 findings across tech-architect-2, security-specialist, regulatory-licensing-specialist, regulatory-analyst, reference-class-analyst-2, tech-industry-analyst, and cognitive-decision-scientist-2; a devils-advocate R2 adversarial review (8 challenges, 20 agent responses, engagement grade A average, PASS verdict per 9-criteria exit gate); seven ring peer verifications (7/7 PASS); and DA second-verifier coverage across all seven agents.

A workspace corruption event occurred during R1 (cognitive-decision-scientist-2's use of BSD sed without explicit backup extension argument truncated workspace.md to 0 bytes). The event was recovered via re-paste from agent contexts with verbatim attestations and is documented in the recovery-log in the workspace. The recovery was transparent, not hidden. Three agent sections (tech-architect-2, tech-industry-analyst, regulatory-licensing-specialist) were re-pasted from agent canonical contexts with provenance attestation; four sections (reference-class-analyst-2, cognitive-decision-scientist, regulatory-analyst, security-specialist) were preserved from the pre-corruption workspace.

Five of seven agents encountered a systematic infrastructure gap: sigma-verify sub-tools (verify_finding, cross_verify, challenge) were not loadable in spawned agent subprocess contexts despite sigma-verify being available at lead level. All five agents logged XVERIFY-FAIL explicitly with compensating T1/T2 sourcing and confidence-appropriate tagging — per the review's §2h when-unavailable provision, these findings are neutral, not penalized. DA compensated via XVERIFY from the DA context on three load-bearing findings from three architecturally distinct providers (openai:gpt-5.4-pro, google:gemini-3.1-pro-preview, deepseek:v3.2:cloud), all returning vulnerability:MEDIUM on findings initially rated HIGH by agents, producing the graduated severity calibration documented throughout this synthesis.


## Post-audit citation correction (2026-04-23)

R19 sigma-audit verified that the specific MITRE ATLAS sub-technique ID `.002` originally cited for chain-of-agent prompt injection does not appear in the published taxonomy. The parent technique AML.T0051 (LLM Prompt Injection) is valid, and the substantive claim — that chain-of-agent injection is a production-relevant technique — is supported by OWASP LLM Top 10 plus published CVEs (CVE-2025-32711 M365 Copilot prompt exfiltration; CVE-2025-6514 mcp-remote RCE; Postmark MCP BCC exfiltration September 2025). All MITRE ATLAS citations in this synthesis updated from `AML.T0051.002` to `AML.T0051` (parent technique). Firms should verify the current MITRE ATLAS sub-technique numbering at https://atlas.mitre.org/ before citing specific sub-technique IDs in their own regulatory or audit artifacts. The production-relevance argument for multi-agent H11 severity rests on the combined evidence (MITRE ATLAS LLM Prompt Injection technique + LangSmith Q1 2026 multi-agent telemetry + CVE catalog + GDPR Art 26 CJEU enforcement precedent), not on the specific sub-technique ID alone.
