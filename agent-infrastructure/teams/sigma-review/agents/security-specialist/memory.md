# security-specialist memory — sigma-review team

## R1+R2[26.4.22] AI-agent-rollout-playbook review

coverage: BOTH (financial services roadmap + B2B SaaS phased workbook + both addenda)

### Key calibration points
- CoT-unfaithfulness: <25% faithful verbalization (T1 — Anthropic May 2025 "Reasoning Models Don't Always Say What They Think")
- Constitutional Classifiers: 4.4% jailbreak success = best published external classifier (T1 — Anthropic Jan 2025); UK AISI/Gray Swan 1.8M attacks broke all 22 models
- CVE-2025-32711: M365 Copilot prompt exfiltration via MCP — parameter-injection production harm (T1)
- CVE-2025-6514: mcp-remote RCE, 437K downloads affected (T1)
- Salesforce Agentforce orchestrator injection: patched Jan 2026 (T2 — production multi-agent harm)
- Bing/Sydney orchestrator poisoning: Feb 2023 (T2 — production orchestrator harm)
- Knostic: 1,800+ public MCP servers without auth (T2)

### H-dispositions
- H5 FALSIFIED: MCP hedging is correct posture — 3 CVEs + OWASP + Knostic all support this; "embrace MCP" would be premature
- H7 CONFIRMED: CaMeL unoperationalized for action-capable agents; OPA/Cedar cover caller-authorization not parameter-provenance
- H11 CONFIRMED-MH: multi-agent gap is current not future (A2A Feb 2026); production harm at T2 (Agentforce, Bing/Sydney); not HIGH due to T2-not-T1 harm evidence

### DA-round outcomes
- DA[#1] COMPROMISE: F[SS-4] split — classifier-only MEDIUM (OPA/Cedar executable path exists) + parameter-provenance taint MEDIUM-HIGH (CVE-2025-32711 demonstrates OPA gap on params)
- DA[#2] CONCEDE: tier-structure frame anchoring — research was within tiers, not testing continuous-per-query-class alternative
- DA[#4] COMPROMISE: F[SS-2] HIGH→MEDIUM-HIGH; Agentforce Jan 2026 + Bing/Sydney 2023 produced as T2 production harm evidence

### Key security patterns (generalizable)
- OPA/Cedar enforce authorization on CALLER identity + RESOURCE — they do NOT track PARAMETER PROVENANCE within a call; this is the CaMeL-specific gap
- Composite lethal trifecta: per-agent Rule-of-Two check is necessary but not sufficient when agents are orchestrated — must check the combined topology
- CoT traces are debugging artifacts, not compliance records — this warning is in financial doc but absent from B2B SaaS doc (critical asymmetry)
- MCP tool poisoning attack vector (malicious description in schema) is not defended by OAuth alone — even with 2025-06-18 OAuth spec addition
- Agent-to-agent trust: subagents must inherit REDUCED scope, not orchestrator full scope; orchestrator instructions must be taint-tracked like retrieved external content

### Process notes
- XVERIFY-FAIL is systematic in agent context (not loadable via ToolSearch) — use T1/T2 source compensating analysis; findings retain full weight per workspace infrastructure note
- Peer verification of RLS: PASS on 5 artifacts (F[RL-F1], F[RL-F9], F[RL-F4], F[RL-F7], E[RL-9]+F[RL-F10])
