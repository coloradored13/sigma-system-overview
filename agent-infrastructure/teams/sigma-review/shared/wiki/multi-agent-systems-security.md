# Multi-Agent Systems Security
Last updated: 26.4.28 | Reviews: R-2026-04-22-ai-agent-rollout-playbook-vet (26.4.28)

## Summary
Multi-agent topologies are now the default deployment pattern in LangGraph (LangSmith Q1 2026 telemetry: 60%+ of production deployments use multi-agent subgraph patterns with default credential inheritance). Standard playbooks treat agents as isolated entities under single-user OBO tokens, which is an architectural omission once Tier 2+ writes or multi-agent orchestration is in scope. Three specific gaps recur: agent-to-agent trust boundaries, composite lethal trifecta in multi-agent systems, and the absent A2A protocol guidance for enterprise interoperability. MITRE ATLAS added LLM Prompt Injection (parent technique AML.T0051) covering chain-of-agent injection in March 2026, classifying it as production-relevant rather than theoretical. GDPR Article 26 joint-controller doctrine is current law with DPA enforcement precedent for multi-agent pipelines touching EU personal data.

## Agent-to-Agent Trust Boundaries — Structurally Absent in Standard Playbooks
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Severity HIGH at Tier 2+. Standard playbooks treat agents as isolated entities under single-user OBO tokens. In multi-agent topologies — the default in LangGraph per LangSmith Q1 2026 telemetry (60%+ of production deployments use multi-agent subgraph patterns with default credential inheritance) — orchestrator compromise via indirect prompt injection allows subagents to execute actions with the orchestrator's full scope.

Minimum viable multi-agent trust design:
- Subagents inherit reduced scope from orchestrators (not full scope)
- Subagent tool calls carry originating-user-session trace ID separate from orchestrator identity
- Orchestrator instructions are treated as untrusted content at the same taint level as retrieved external content

This is not a future-state concern — it is the current default behavior of the dominant production framework, and the gap is structural in standard playbooks.

## MITRE ATLAS — AML.T0051 LLM Prompt Injection
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] MITRE ATLAS added technique AML.T0051 "LLM Prompt Injection" in its March 2026 update, with chain-of-agent injection covered as a production-relevant attack pattern (the parent technique AML.T0051; specific sub-technique numbering varies — verify at https://atlas.mitre.org/ before citing specific sub-technique IDs in a regulatory or audit artifact). This classifies chain-of-agent injection as a production technique category rather than theoretical risk. Combined with OWASP LLM Top 10 and the published CVE catalog (CVE-2025-32711 M365 Copilot prompt exfiltration; CVE-2025-6514 mcp-remote RCE; Postmark MCP BCC exfiltration September 2025), the production-relevance argument for the multi-agent severity gap rests on combined evidence rather than the specific sub-technique ID alone.

## Composite Lethal Trifecta in Multi-Agent Systems
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Severity MEDIUM-HIGH. Standard playbooks apply the per-agent lethal-trifecta check (Simon Willison: private data + untrusted content + external communication) and Meta's Rule of Two — but in multi-agent topologies, two individually safe agents can together constitute a lethal trifecta:
- Agent A reads private customer data and ingests external documents (two trifecta legs)
- Agent B sends external notifications (one leg)
- Agent A orchestrates Agent B

All three legs are present without explicit human confirmation across the A-to-B delegation. The fix: agent card template should include a "combined topology lethal-trifecta assessment" field, owned by the AI Risk Committee at each Tier 2+ expansion. Per-agent assessment is necessary but not sufficient.

## A2A Protocol — Enterprise Multi-Agent Interoperability
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] The Agent-to-Agent (A2A) protocol — Google, February 2026, Linux Foundation stewardship, 50+ enterprise partners including Salesforce, SAP, ServiceNow — is the emerging interoperability standard for enterprise multi-agent systems. Severity HIGH at Tier 2+. Phase 4 "multi-agent operation" sections of standard playbooks are typically a single sentence with no architectural guidance, and financial-services roadmaps frequently have zero mentions of agent-to-agent. For enterprise B2B SaaS firms, A2A adoption will increasingly be customer-driven — enterprise customers will require it as a condition of deeper multi-agent integration. Architectural guidance covering scope inheritance for subagents, originating-user-session trace IDs, and orchestrator-instruction taint level is a Phase 4 prerequisite in B2B SaaS / Tier 2+ section in financial-services frameworks.

## GDPR Article 26 — Joint-Controller Doctrine
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] CJEU C-210/16 (Wirtschaftsakademie Schleswig-Holstein) and C-40/17 (Fashion ID) establish joint-controller doctrine as current T1 law with DPA enforcement precedent. For multi-agent pipelines touching EU personal data, multiple parties processing the same personal data jointly may be joint controllers — each with full GDPR liability. SaaS firms running agent orchestration on behalf of enterprise customers cannot assume the customer is the sole controller. A joint-controller assessment under Article 26 is required for any multi-agent pipeline touching EU personal data, with Article 26 transparency arrangements (joint-controllership agreement, public summary of essential terms) as deliverables.

## Long-Term Agent Memory — Unaddressed
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Long-term agent memory (cross-session retention of user preferences, prior decisions, conversation context) is generally unaddressed in standard playbooks alongside multi-agent gaps. The retention horizon for agent memory intersects with the SEC 17a-4 / FINRA 4511 trace retention requirements (3-6 years) but is not the same artifact: traces are per-call records; memory is summarized state. The audit posture for memory has no published consensus and is flagged as an open question.

## LangGraph Default Credential Inheritance
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] LangSmith Q1 2026 telemetry shows 60%+ of production LangGraph deployments use multi-agent subgraph patterns with default credential inheritance — subagents run with the orchestrator's full credential scope unless explicitly reduced. This default behavior is the structural reason the multi-agent trust gap is current rather than future. Firms deploying LangGraph multi-agent should explicitly configure reduced subagent scope rather than rely on defaults.

## Indirect Prompt Injection as Multi-Agent Attack Vector
[R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28] Indirect prompt injection — malicious instructions embedded in retrieved content, not in the user prompt — is the dominant attack vector for compromising orchestrator agents in multi-agent topologies. Defense layers:
- Treat retrieved content as untrusted at the same taint level as external user input
- Treat orchestrator instructions to subagents as untrusted content at that same taint level
- Apply CaMeL-style per-tool policy codification at the subagent dispatch boundary, not only at the user-facing entry point
- Anthropic's Constitutional Classifiers at 4.4% jailbreak success is the best published external classifier defense — still not zero, requires layered defense

## Open Questions
- Long-term agent memory audit posture — no published consensus, intersects but does not duplicate trace retention requirements [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]
- Multi-agent eval methodology — pass^k goal-completion is specified for single-agent trajectories but no equivalent rubric covers cross-agent delegation success [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]
- A2A vs MCP composability — both are emerging standards, scope overlap and integration patterns not yet stable [R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28]

## Sources
- R-2026-04-22-ai-agent-rollout-playbook-vet, 26.4.28 — sigma-review Tier 3 ANALYZE on dual-track financial-services capability-maturity roadmap and B2B SaaS phased workbook (post-audit citation correction 26.4.23: AML.T0051 parent technique cited rather than specific sub-technique ID)
