# product-strategist — personal memory

## identity
role: product strategy specialist
domain: market,growth,monetization,prioritization,user-segmentation
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known products
sigma-mem[HATEOAS memory MCP server, personal+team memory, alpha quality|26.3.7]
hateoas-agent[HATEOAS framework for AI agents, v0.1.0, ship-ready|README exceptional, 259 tests, 12 examples, Resource.validate()+_state docs added|26.3.7]
sigma-comm[protocol spec, potentially more shareable than sigma-mem|26.3.7]

## past findings
review-1(sigma-mem,26.3.7): strong differentiation(HATEOAS unique), audience-of-one risk, no docs/README |#4
review-2(sigma-mem,26.3.7): alpha quality reached, shipping blockers(README,LICENSE,git,hateoas-agent-publish) |#3
review-3(sigma-mem,26.3.7): persistent-teams=category-change, three-product-portfolio |#4
review-4(hateoas-agent,26.3.7): SHIP-READY, README best-in-class, positioning genuine(deterministic-vs-probabilistic), name keep-for-v0.1, LICENSE needs author, anthropic-only limits audience, api-surface large-for-alpha |#6
review-5(hateoas-agent,26.3.7): SHIP-GO, all substantive blockers resolved, 3 mechanical prereqs remain(git-init,rebuild-dist,update-examples-in-README) |#3
review-6(hateoas-agent,26.3.7): delta confirms 3/5 review-5 items resolved(_state-docs,Resource.validate,examples-list), 2 mechanical blockers remain(git-init,rebuild-dist), grade:A-, market position unchanged+strong |#6

## calibration
C[user builds side projects at night, ships when ready not when told|1|26.3]
C[sigma-mem evolved toward persistent team memory — confirmed|2|26.3]
C[hateoas-agent more polished than expected for side project alpha|1|26.3]
C[hateoas-agent README is ship-ready, exceptional quality|1|26.3]
C[MCP adapter is forward-looking — positions for Claude Desktop ecosystem|1|26.3]
C[team decisions get executed within 1-2 review cycles — _state docs + Resource.validate both done by review-6|1|26.3]
C[delta reviews effective — severity decreasing with each iteration confirms convergence pattern|2|26.3]

## strategic insights
dep-chain: sigma-mem→hateoas-agent — can't ship one without the other
three-products: sigma-mem(memory engine) + ΣComm(protocol spec) + persistent-team-infra(coordination layer)
headline-narrative: "Persistent agent teams that learn across sessions — using nothing but markdown files"
competitive-advantage: cross-session persistence + human-auditable + no-infrastructure + expertise-attribution
hateoas-agent-positioning: library-not-framework, can integrate with LangChain/CrewAI, deterministic-vs-probabilistic
hateoas-agent-growth: model-agnostic Runner is #1 growth lever for v0.2
hateoas-agent-mvr: git-init + uv-build + PyPI-publish (2 mechanical steps only, all substantive work done)

¬[monetization — these are personal/OSS tools, not a business]

→ actions:
→ evaluating shipping readiness → check gap table from review-4
→ new product idea → assess audience, differentiation, effort
→ feature prioritization → severity × reach × confidence

## research

R[agent-framework-landscape: LangGraph=production-leader(complex-stateful-workflows,graph-based,model-agnostic,checkpointing), CrewAI=surging(44.6k-stars,450M-monthly-workflows,100k-certified-devs,claims-5.76x-faster-than-LangGraph,rebuilt-independent-no-deps), AutoGen=dead(merged-into-Microsoft-Agent-Framework-with-Semantic-Kernel,1.0-GA-Q1-2026), OpenAI-Agents-SDK=new-entrant(open-source,python+typescript,MCP-native,non-OpenAI-models-supported), three-clear-leaders: LangGraph+CrewAI+MS-Agent-Framework, trend: lean+fast>bloated+featured |¬ no-HATEOAS-pattern-in-any-framework, no-cross-session-persistence-as-core, no-markdown-based-memory |src: o-mega.ai,turing.com,alphamatch.ai,tldl.io |refreshed: 26.3.7 |next: 26.4] #8

R[MCP-ecosystem: MCP=industry-standard(donated-to-Linux-Foundation-Agentic-AI-Foundation-Dec-2025), 97M-monthly-SDK-downloads, 10k+-active-servers, 300+-clients, backed-by-Anthropic+OpenAI+Google+Microsoft+AWS+Block, enterprise-adoption(Salesforce,ServiceNow,Workday,Accenture,Deloitte), OpenAI-adopted-MCP-Mar-2025-across-all-products, 2026=experimentation→production-transition |¬ MCP-not-contested-anymore — it won |src: anthropic.com,thenewstack.io,pento.ai,cdata.com |refreshed: 26.3.7 |next: 26.4] #6

R[python-publishing: trusted-publishing=standard(OIDC-tokens,no-long-lived-API-keys,GitHub-Actions-native), uv=dominant-package-mgr(10-100x-faster-than-pip,Rust-based,Astral/Ruff-team,handles-install+venv+python-versions+lockfiles), uv-publish=two-commands(uv-build+uv-publish), Poetry-still-66M-downloads-but-no-longer-default-rec, src-layout=recommended, tag-based-release-automation=standard-pattern |¬ pip-not-dead-but-uv-drop-in-replacement, Poetry-not-dead-but-narrowing-to-library-publishing |src: docs.pypi.org,cuttlesoft.com,scopir.com,docs.bswen.com |refreshed: 26.3.7 |next: 26.4] #6

R[oss-launch-strategy: GitHub-36M-new-devs-2025(India-5.2M-led-growth), AI-accelerates-adoption(lowers-barrier-to-entry+helps-understand-unfamiliar-codebases), AI-slop-risk(low-quality-PRs-flooding-projects), time-to-milestone-shortened(repos-hitting-attention-in-single-quarter), winning-traits: 10x-better-not-incremental+challenge-incumbents+faster-simpler-more-accessible, org-priorities: sponsor-OSS(44%)+train-devs(41%)+increase-contributions(39%) |src: github.blog,eclipse-foundation.blog |refreshed: 26.3.7 |next: 26.4] #5

R[dev-adoption-patterns: AI-compatibility=primary-driver(AI-handles-boilerplate→devs-pick-on-utility-not-overhead), Python-overtaking-JS-as-most-used-lang(AI+data-science-influence), framework-agnosticism=norm(pick-per-task-not-one-size), convenience-loops-drive-lock-in(AI-suggests-what-it-knows-best→reinforcing-cycle), README-quality+examples+time-to-hello-world=adoption-predictors |¬ monolithic-framework-preference-dead |src: paul-dzitse.medium.com,github.blog,keyholesoftware.com |refreshed: 26.3.7 |next: 26.4] #5

R[strategic-implications-for-sigma-portfolio: hateoas-agent-positioning-validated(no-competitor-uses-HATEOAS,library-not-framework=matches-agnosticism-trend), MCP-bet-validated(industry-standard-now,sigma-mem-MCP-server=right-integration-surface), uv-adoption-recommended(switch-from-pip/poetry-for-publishing-speed), cross-session-persistence=uncontested-differentiator(no-framework-offers-this-natively), CrewAI-is-closest-competitor-for-team-orchestration(but-no-persistence+no-human-auditable-memory), launch-window-good(time-to-milestone-shortening+AI-agent-category-hot+dev-adoption-AI-accelerated) |refreshed: 26.3.7 |next: 26.4] #6
