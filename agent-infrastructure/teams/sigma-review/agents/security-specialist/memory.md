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

## R19-remediation C1 [26.4.23] — plan-track

### H1 disposition: CONFIRMED
sigma-verify IS under user control at /Users/bjgilbert/Projects/sigma-verify/. Sub-tools absent from spawned agent contexts because HATEOAS StateMachine (machine.py:24 `gateway_name="init"`) gates them behind `ready` state — intentional state-gating, not a deferred-tool registry bug. Correct in-scope fix: spawn-prompt init instruction + agent-def update. Architecturally correct fix (hateoas-agent auto-init on connection) is separate build, medium priority.

### ADR[1] sed-i — XVERIFY PARTIAL
Decision: PreToolUse Bash BLOCK 3, workspace-path scope (/.claude/teams/|workspace.md), no bypass.
XVERIFY REFINEMENT (openai/gpt-5.4 PARTIAL): use shlex.split() argv tokenization NOT raw string regex. Evasion forms: `sed -e 's/x/y/' -i file`, `env sed -i`, `xargs sed -i`. Test matrix must cover env/xargs wrapping forms.

### STRIDE findings (generalizable)
- T (Tampering): XVERIFY tag presence does not equal authenticity — fabricated results not caught by A15. Known gap.
- D (DoS): sigma-verify has no programmatic rate limiting on cross_verify across 13 providers. Anthropic 1K RPM is only bound.
- E (EoP): bypassing HATEOAS state to register all tools stateless creates EoP risk for future state-gated write tools. Never do this.

### Audit-trail design (#22/#23)
No separate tamper-resistant log needed for internal framework. Workspace gate-log + A12 archive = sufficient. Escalate if framework becomes multi-user or compliance-audited.

### XVERIFY provider calibration update
openai/gpt-5.4 catches implementation-specific evasion paths that llama3.1:8b misses. Weight openai PARTIAL over llama AGREE on security implementation specifics. Google 503s during daytime demand spikes — use as third provider not primary.

### XVERIFY now working in this agent context
XVERIFY is NOT systematically broken in spawned agent contexts — it requires calling mcp__sigma-verify__init first. This is the R19 #3 root cause confirmed. After init call, verify_finding and cross_verify work correctly. Update spawn prompts accordingly.
