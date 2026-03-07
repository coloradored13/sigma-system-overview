# tech-architect — personal memory

## identity
role: technical architecture specialist
domain: architecture,security,performance,infra,api-design
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known codebases
sigma-mem[4 modules ~430 LOC, HATEOAS state machine via hateoas-agent, MCP server|handlers.py is largest|26.3.7]
hateoas-agent[13 modules ~2K LOC, 250+ tests(9 skipped), 3 APIs (declarative/action-centric/class-based), MCP server, composite multi-resource, discovery mode, guards, persistence, validate() on both APIs, CI 3.10-3.13|26.3.7]
sigma-review-team[persistent team memory at ~/.claude/teams/sigma-review/, agents/shared/inboxes dirs, boot-sequence pattern, expertise-weighted decisions|26.3.7]

## past findings (on sigma-mem, NOT on hateoas-agent)
review-1(26.3.7): path-traversal(!fixed), checksum-logic(docstring-fixed), state-detection(rewritten to scoring), dead-code(removed), no-tests(32 added) |#5
review-2(26.3.7): _detect_state missing memory_dir passthrough(fixed), unused import re(fixed) |#2
review-3(26.3.7): team-memory-arch-review: inbox-proliferation(16 files, no GC), no-shared-file-write-coordination, sigma-mem-team-bridge-missing, no-schema-versioning, {team-name}-placeholder-ok, cross-agent-read-intentional |#6

## past findings (on hateoas-agent)
review-4(26.3.7): arch(A-) api(B+) security(A) release(B) | _state-magic-key-footgun, ActionResult-unused-but-exported, RunResult-not-dataclass, anthropic-hard-dep(should-be-optional), registry-private-state-leakage(runner+persistence access _last_state), mcp-error-leaks-exceptions, no-__version__, .DS_Store/dist-in-repo, deprecated-persistence-funcs-still-exported
review-5(26.3.7): arch(A-) api(A-) security(A) release(B+) | 6 review-4 items resolved(anthropic-optional,validate-at-init,quick-start-runnable,LICENSE-author,__version__,runner-exception-safe), _state-docs-still-needed, Resource-validate-parity
review-6(26.3.7): arch(A) api(A-) security(A) release(A-) | review-4: 5-resolved+2-acceptable+1-partial(mcp-error-leak)+1-reclassified | review-5: 2/2-resolved | new: HasHateoas-Protocol-incomplete(minor), mcp-error-leak-to-LLM(minor,security), dist-stale(trivial) |#3

## calibration
C[user values honest assessment over diplomatic framing|1|26.3]
C~[codebase is clean but early — alpha quality|1|26.3] → upgraded: ship-quality alpha, grades A/A- across all dimensions
C[hateoas-agent is publication-quality code — security model is genuinely novel for AI agent tooling|1|26.3]
C[test suite quality: 250+ tests(9 skipped) + adversarial + integration = excellent for ~2K LOC|2|26.3]

## patterns
multiple-instance-convergence: when I reviewed as 3 separate instances, all found path-traversal independently → high-confidence signal
hateoas-agent-framework: handles action advertisement automatically — don't flag handler-level navigation as missing HATEOAS
team-memory-as-files: simple file-based persistence scales to ~5 agents, shared files need coordination beyond that
sigma-mem-team-gap: personal memory (sigma-mem MCP) and team memory (raw files) are separate systems — bridging them would be high-value
_state-magic-key: implicit conventions are harder to maintain than explicit types for published APIs
optional-deps-for-providers: framework should work without any specific LLM provider installed
protocol-incomplete: Python Protocol types should include all methods that are checked via hasattr — confirmed again in review-6 (HasHateoas missing filter_actions, get_transition_metadata, validate)
delta-review-severity-decay: review-4 found 9 issues, review-5 found 3 new + resolved 6, review-6 found 3 minor + resolved all remaining substantive issues — confirms review-rounds-converge pattern
mcp-vs-runner-consistency: MCP server and Runner should share error-handling patterns — found inconsistency in exception message exposure (mcp exposes raw, runner sanitizes)

¬[over-engineering concerns — codebase is lean ~430 LOC]

## team decisions
arch:weighted-state-detection, arch:path-validation-via-resolve (both for sigma-mem)
product:alpha-quality-reached for sigma-mem, blocker: hateoas-agent must publish first

## team patterns
review-rounds-converge: round-1=correctness, round-2=polish, round-3+=diminishing returns (confirmed by review-6: only minor/trivial findings)
agent-overlap-valuable: tech+ux catch different aspects of same issue
delta-review-format-effective: checking previous findings systematically works well, prevents re-flagging resolved issues

## research

R[OWASP-agentic-top10-2026: ASI01-goal-hijack, ASI02-tool-misuse, ASI03-identity-privilege-abuse, ASI04-supply-chain(tool-poisoning,rug-pulls), ASI05-unexpected-code-exec, ASI06-memory-context-poisoning | defense: input-validation-all-sources, goal-lock, tool-sandboxing-least-priv, HITL-for-high-impact | directly relevant to sigma-mem+hateoas-agent security model |src: genai.owasp.org, paloaltonetworks.com/blog |refreshed: 26.3.7 |next: 26.4]

R[MCP-security-landscape: 43%-of-MCP-servers-have-cmd-injection(Equixly), CVE-2025-6514-mcp-remote-RCE(437K-downloads), tool-poisoning=hidden-instructions-in-tool-descriptions(invisible-to-user,visible-to-LLM), rug-pull=tool-definition-mutates-post-approval, confused-deputy=server-cant-differentiate-users, credential-theft-via-agent-exfiltration | mitigations: pin-server-versions, alert-on-description-change, scope-tokens-minimally, carry-user-context-to-server | hateoas-agent's action-advertisement-model naturally constrains tool surface area(good) |src: invariantlabs.ai, simonwillison.net, checkmarx.com, practical-devsecops.com |refreshed: 26.3.7 |next: 26.4]

R[prompt-injection-design-patterns: action-selector-pattern(agent=selector-only,no-tool-feedback-loop), plan-then-execute(fixed-action-list,no-runtime-deviation), second-order-injection(low-priv-agent-tricks-high-priv-agent) | arxiv:2506.08837 formalizes these as reusable security patterns | relevant: hateoas-agent guards+state-machine already implement constrained-action-selection |src: arxiv.org/abs/2506.08837, christian-schneider.net |refreshed: 26.3.7 |next: 26.4]

R[HATEOAS-for-AI-agents-validated: Nordic-APIs+Amundsen confirm HATEOAS is "API style waiting for AI", GRAIL-framework(Goal-Resolution-through-Affordance-Informed-Logic) demonstrates hypermedia-driven-agent-navigation, key-insight: "actionability is perceived not inferred"=agents detect affordances rather than predict, workflows-discovered-at-runtime-not-designed | directly validates hateoas-agent architecture — we're ahead of the curve |src: nordicapis.com, mamund.substack.com, tldrecap.tech/apidays-paris |refreshed: 26.3.7 |next: 26.4]

R[A2A-protocol-launched: Google Agent2Agent protocol(Feb 2026, Linux Foundation, 50+ partners), complements MCP(tools+context) with agent-collaboration(communication+coordination), built on HTTP+SSE+JSON-RPC, Agent-Cards for capability-discovery, task-lifecycle-management, gRPC-support added | A2A=inter-org-agent-comm, MCP=agent-tool-comm, our ΣComm=intra-team-agent-comm — three distinct layers |src: developers.googleblog.com, a2a-protocol.org, cloud.google.com/blog |refreshed: 26.3.7 |next: 26.4]

R[multi-agent-orchestration-patterns: sequential,concurrent,group-chat,handoff,magnetic,hierarchical,event-driven | Microsoft-Agent-Framework merges AutoGen+Semantic-Kernel: session-state, type-safety, middleware, telemetry, explicit-workflow-control | centralized-vs-federated orchestration models | our sigma-review uses centralized(lead-mediates)+federated(agents-self-curate) hybrid |src: learn.microsoft.com/azure/architecture, learn.microsoft.com/agent-framework |refreshed: 26.3.7 |next: 26.4]

R[python-typing-3.13-3.14: TypeIs(PEP-742) narrows both if+else branches(unlike TypeGuard=if-only), requires narrowed-type compatible-with-input, 3.14-adds-lazy-annotations | review-relevance: recommend TypeIs for state-detection guards in hateoas-agent, replace hasattr checks with typed narrowing |src: peps.python.org/pep-0742, docs.python.org/3/library/typing.html |refreshed: 26.3.7 |next: 26.4]

R[python-packaging-2026: uv-is-default(Rust-based,10-100x-faster-than-pip,replaces-pip+pipx+pyenv+virtualenv+twine), uv_build=zero-config-backend-for-pure-Python, uv.lock=cross-platform-reproducible, Poetry-still-preferred-for-library-PyPI-publishing | hateoas-agent+sigma-mem should evaluate uv migration, uv.lock for reproducibility |src: learn.repoforge.io, scopir.com, docs.astral.sh/uv |refreshed: 26.3.7 |next: 26.4]

R[python-api-design-2026: Pydantic-v2-ecosystem=standard-for-validation, FastAPI=default-for-async-APIs, circuit-breaker+exponential-backoff=standard-error-patterns, EAFP-over-LBYL | review-relevance: Pydantic for MCP handler input validation, explicit error types over bare exceptions |src: easyparser.com, talent500.com, khaled-jallouli.medium.com |refreshed: 26.3.7 |next: 26.4]

→ actions:
→ reviewing sigma-mem again → check if past findings still apply
→ new codebase to review → start with architecture overview before diving in
→ disagreement with another agent → record both positions in shared/decisions.md
→ next research round → refresh 26.4, check OWASP agentic updates, A2A spec evolution, uv adoption status
