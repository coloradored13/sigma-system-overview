# AI Agent Reference Architecture — 2026
Last updated: 26.4.28 | Reviews: R-2026-04-22-ai-agent-rollout-playbook-vet (26.4.28)

## Summary
The shared technical spine for production AI agent deployments is approximately 80% common across regulated finserv and B2B SaaS contexts, and is largely defensible as of 2026. The reference architecture: VPC-resident model gateway as single chokepoint; OBO/SPIFFE per-user scoped tokens with short TTL (no shared service accounts); OpenTelemetry GenAI v1.37 for observability; layered guardrails (defense-in-depth); kill switch with sub-60-second propagation; git-based prompt and tool versioning with PR review; agent inventory with risk assessment and agent card; third-party risk review including model providers and MCP servers; and a buy-generic / build-risk-bearing-policy allocation. What changed in 2026 is concentrated in vendor landscape and threshold updates.

## Gateway Architecture
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] VPC-resident model gateway is the single chokepoint for data egress, cost, and logging — a day-one non-negotiable for regulated firms. LiteLLM, Portkey, and Kong are all reasonable choices. Gateway-first architecture is consensus across every major practitioner source (Databricks, a16z AI Canon, Google Cloud architecture guides). Gateway vendor differentiation is in configuration quality, not tool selection. For EU-data-constrained firms, see EU residency note below.

## Identity — OBO/SPIFFE
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] On-behalf-of style per-user scoped tokens with short TTL, no shared service accounts. Shared service accounts are the most common early mistake and the one regulators find first. The OBO/SPIFFE direction remains the right approach in 2026, though competing standards mean firms are building toward a moving target: IETF draft-klrc-aiagent-auth-00 (draft-02, January 2026) and the OpenID Foundation "Agent Identity" working group (February 2026) are the active standardization efforts. Build for now, expect to re-architect.

## Observability — OpenTelemetry GenAI v1.37
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] OpenTelemetry GenAI v1.37 reached stability in 2025; Datadog supports it natively. The mandate is full-fidelity retrieval-context capture in the trace — not a pointer to retrieval, but the actual retrieved content. Cost implication: at 50-200KB per trace and 3-6 year retention under SEC 17a-4 / FINRA 4511, storage costs reach $200K-$2M per year. This is typically unbudgeted and must be modeled explicitly.

## Vector Store Thresholds — 2026 Update
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] pgvector-on-managed-Postgres is no longer the universal day-one default for 2026. Updated thresholds:
- pgvector — appropriate for fewer than 500K vectors, or latency-tolerant applications
- Qdrant v1.13 (released March 2026) — appropriate for more than 500K vectors, or when p95 latency must stay below 50ms; Qdrant matches pgvector on operational simplicity while exceeding it 3-5x on filtered-vector-search latency at volumes above 1M vectors
- Turbopuffer — dominant choice for multi-tenant cold-start retrieval

Tenant-partitioned indexing remains architecturally correct regardless of which store is selected. ANN pre-filter (filter before similarity scoring, not after) is required for true tenant isolation; default ANN configurations on pgvector and Qdrant do not provide it.

## MCP Security Posture — 2026
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] The correct 2026 posture is hedging-as-execution: pin by hash, proxy through allowlists, SAST/SCA on every server, avoid community servers in production. The hedging is the executable posture, not fence-sitting. Evidence base:
- CVE-2025-32711 (M365 Copilot prompt exfiltration)
- CVE-2025-6514 (mcp-remote RCE)
- 1,800+ public MCP servers without authentication as of April 2026
- MCP OAuth (2025-06-18 spec) added as SHOULD, not MUST
- Postmark MCP BCC exfiltration September 2025

Internal MCP server build cost is material: a single production-grade internal MCP server requires 3-6 weeks of senior engineering time. A typical Tier 1-2 deployment uses 3-8 MCP servers (data retrieval, document access, notification, CRM lookup) — 10-50 weeks of engineering effort, $75K-$400K. This cost is typically unbudgeted.

## MCP Server Allowlist Evaluation — 5-Criterion Rubric
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] "Run SAST/SCA" alone is too generic to be self-service. A specific 5-criterion rubric is needed for what "production-ready" means for any internal MCP server:
1. Authentication mechanism — OAuth SHOULD per 2025-06-18 MCP spec; verify it's implemented
2. Schema integrity verification — MCP tool poisoning via malicious schema description is not defended by OAuth
3. Return-value inspection — OAuth provides auth boundary, not return-value integrity
4. Version pinning with hash
5. SAST pass

Without this rubric, the allowlist decision falls to a developer without security training reviewing a PR.

## Guardrails — Data Sovereignty Distinction
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Guardrail platforms are not equivalent on data sovereignty:
- Lakera Guard, Azure AI Content Safety, Bedrock Guardrails — send prompt content to vendor APIs. Every input classified becomes a data flow to a third-party processor, requiring sub-processor disclosure and vendor agreement coverage
- LLM Guard (self-hosted OSS) — sends nothing

For firms under NYDFS Part 500, EU GDPR Article 28, or handling healthcare PHI, this is a compliance decision before a product decision. Severity MEDIUM-HIGH for regulated deployments. Anthropic's Constitutional Classifiers at 4.4% jailbreak success is the best published number for external classifier defense; this is still not zero, and layered defense-in-depth is required.

## Kill Switch
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Sub-60-second propagation is the correct design target for a kill switch.

## Prompt and Tool Versioning
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Git-based versioning with PR review is the correct audit-defensible pattern for prompts and tools.

## Agent Inventory and Agent Card
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Agent inventory + risk assessment + agent card is the spine of every regulatory conversation. The agent card should include — at minimum — applicable lethal-trifecta legs (private data access, untrusted content ingestion, external communication), tool scope, identity model, retention model, and a "combined topology lethal-trifecta assessment" field for agents that orchestrate or are orchestrated by other agents.

## Build-Versus-Buy Allocation
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Buy generic plumbing (gateway, identity, observability, vector store, eval platform, feature flags, sandboxing, guardrails). Build risk-bearing policy (per-tool authorization codification, eval criteria, audit artifacts, examiner-facing crosswalks). This allocation is the correct 2026 default and is validated by reference-class analysis. Vendor frameworks (Claude Agent SDK with 12-month API stability guarantee from Anthropic November 2025; LangGraph v0.3 stable checkpoint-based state management January 2026; OpenAI Agents SDK GA October 2025) save 6-8 weeks of engineering build time on the agent layer; computer-use APIs specifically remain early-stage.

## CaMeL — Architectural Direction and Per-Tool Codification
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] The CaMeL principle "never derive authorization from model output" is the correct architectural direction. The paper's provable-security finding on AgentDojo (77% with CaMeL versus 84% undefended) is correctly cited. The implementation gap is per-tool policy codification — connecting the invariant to each tool's actual input parameters. OPA/Cedar policy engines and brokered tool execution are mature patterns for this work. The work is unnamed in standard playbooks, so it does not appear in project plans. Specification:
1. Enumerate every tool-call input parameter
2. Tag each input's provenance at assembly time (user-authenticated-session vs. retrieved-content vs. untrusted-external)
3. Run provenance policy check at tool-call dispatch using only authenticated session scope
4. Quarantine untrusted-content processing from the tool-dispatch path

Severity MEDIUM for the architectural gap (path exists via OPA/Cedar + planner/executor); HIGH specifically for the unnamed Phase 2 / Tier 2 deliverable.

## Eval Platform Differentiation
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Eval platform choice is not undifferentiated:
- Langfuse (Apache 2.0, mature self-hosted path) — the only eval platform where trace data never leaves firm infrastructure
- Inspect AI (UK AISI, open-source) — the only peer-reviewed eval framework with documented adversarial eval methodology, particularly relevant for regulated financial services red-team documentation
- Braintrust, LangSmith, others — vendor-hosted; data flows out

For data-sovereignty-constrained firms, Langfuse is the differentiated default. For regulated firms requiring red-team documentation, Inspect AI's adversarial methodology is the published baseline.

## Trajectory Evaluation for Tool-Heavy Agents
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] τ-bench retail SOTA pass^8 is below 25%. RAG-heavy evaluation alone is insufficient for tool-heavy agents. Five-element trajectory eval rubric:
1. Tool selection accuracy
2. Argument quality
3. Error recovery
4. pass^k goal-completion (for chosen k)
5. Trajectory efficiency

Specifying k and acceptance thresholds is required — neither principle-level nor monthly-calibration framing substitutes. Rubric specification alone is insufficient — explicit inter-rater calibration training (kappa target) is required because the rubric is cognitively demanding.

## Sandboxing — 2026 Cost-Effective Alternative
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Cloudflare Sandboxed Workers (March 2026) is a cost-effective sandboxing alternative at under $0.005 per execution versus E2B's $0.05+. Material cost difference at production volumes; not yet in standard playbook recommendations.

## Statsig / OpenAI Acquisition — Concentration Risk
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Statsig was acquired by OpenAI in 2025. Firms using OpenAI models behind a Statsig feature flag concentrate vendor dependency at two stack points — model provider and feature-flag platform. Under NYDFS Part 500 expectations, this is a TPRM event requiring documented assessment. LaunchDarkly remains the unaffiliated alternative. Severity MEDIUM.

## EU Gateway Residency
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] "Data residency is binding" must apply to gateway and model API calls, not just embeddings and vector store. Routing defaults:
- Bedrock — US regions by default; EU regions exist but require explicit configuration; not all models available in EU
- Azure AI Foundry — EU residency for Azure OpenAI; not for Anthropic-on-Azure (US East routing)
- Self-hosted LiteLLM in an EU VPC — currently the only clean path for GDPR Article 44 compliance when routing to EU-hosted models

Severity HIGH for EU-data-constrained firms.

## Vendor Switchover — 60-Day Migration Runbook
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Humanloop's September 2025 shutdown with a sub-60-day data-deletion window is a specific documented event affecting a previously-recommended vendor. Annual AI-infra vendor discontinuity rate is 15-25%, making vendor migration a modal-not-tail risk over a typical 13-month build window. Contractual data-export clauses are necessary but not sufficient. The runbook is what makes them executable under time pressure: which data to export, in what format, to what destination, within what SLA, with what integrity verification, triggered by what vendor-health signals (funding events, co-founder departures, feature deceleration). Quarterly vendor-health review is a Phase 3+ standing artifact.

## Feature-Flag Platform — Vendor Health
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Feature-flag platforms are required for production AI agent rollout (gradual exposure, kill-switch propagation, per-tenant gating). LaunchDarkly is the unaffiliated mature option. Statsig has the OpenAI concentration risk noted above.

## Use-Case Selection Discipline
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] First-agent selection criteria — low blast radius, advisory rather than action-taking, bounded scope, real users, SME availability — are correct and should not be relaxed. The lethal trifecta check applies at use-case selection (B2B SaaS Phase 0 use-case criteria) and at inventory time (financial agent card). For multi-agent topologies, the per-agent check is necessary but not sufficient — see multi-agent-systems-security wiki page for composite trifecta assessment.

## Sources
- R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28 — sigma-review Tier 3 ANALYZE on dual-track financial-services capability-maturity roadmap and B2B SaaS phased workbook
