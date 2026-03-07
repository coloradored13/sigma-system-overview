# team decisions — expertise-weighted

## sigma-mem v0.1 review (26.3.7)

arch:weighted-state-detection |by:tech-architect |weight:primary
  |ctx: replaced first-match keywords with scoring system, all reviewers confirmed improvement
  |alt: ML classifier (ruled out — overkill for current scale)

arch:path-validation-via-resolve |by:tech-architect |weight:primary
  |ctx: _validate_path uses resolve()+is_relative_to(), product-strategist confirmed as shipping prerequisite

product:alpha-quality-reached |by:product-strategist |weight:primary
  |ctx: 0→32 tests, security hardened, tech-architect confirmed fixes correct
  |blockers: README, LICENSE, git init, hateoas-agent publish for PyPI

ux:dual-user-tension-acknowledged |by:ux-researcher |weight:primary
  |ctx: AI-optimized notation vs human maintainer, tech-architect noted rosetta.md helps, product-strategist noted this is moat+barrier
  |status: accepted tradeoff, not resolved

## hateoas-agent v0.1.0 release review (26.3.7)

product:ship-ready |by:product-strategist |weight:primary
  |ctx: README exceptional, packaging complete, only trivial blockers (LICENSE author, repo cleanup)
  |ctx: tech-architect confirmed arch(A-) security(A), ux-researcher confirmed DX(B+)

arch:_state-convention-is-footgun |by:tech-architect |weight:primary
  |ctx: ux-researcher independently flagged silent failure when _state omitted, both recommend explicit return type or warning
  |decision: document prominently for v0.1, consider ActionResult wrapper for v0.2

arch:anthropic-should-be-optional-dep |by:tech-architect |weight:primary
  |ctx: product-strategist noted anthropic-only limits audience, model-agnostic Runner is #1 growth lever
  |decision: make optional before publish if feasible, otherwise v0.2

ux:add-startup-validation |by:ux-researcher |weight:primary
  |ctx: tech-architect confirmed missing handlers only caught at runtime, ux-researcher identified as highest-impact DX improvement
  |decision: add StateMachine.validate() called by Runner.__init__

product:readme-keep-as-is |by:product-strategist |weight:primary
  |ctx: all three reviewers praised README quality, minor fixes only (quick-start runnability, example count)

## hateoas-agent v0.1.0 delta review (26.3.7)

review-5-resolved |by:all-three |weight:consensus
  |ctx: anthropic-optional(✓), validate-at-init(✓), quick-start-runnable(✓), LICENSE-author(✓), __version__(✓), runner-exception-safe(✓)
  |grades: arch(A-) api(A-) security(A) release(B+) DX(A-)

product:ship-go |by:product-strategist |weight:primary
  |ctx: all substantive blockers resolved, 3 mechanical prereqs remain (git-init, rebuild-dist, update-examples-in-README)

arch:_state-docs-still-needed |by:all-three |weight:consensus
  |ctx: team decision from review-4 to "document prominently" was not executed, all three re-flagged independently

ux:Resource-validate-parity |by:ux-researcher,tech-architect |weight:primary
  |ctx: StateMachine.validate() exists but Resource class has none, Runner silently skips via hasattr

## team infrastructure v2 (26.3.7)

arch:self-sufficient-agents |by:user+lead |weight:directive
  |ctx: agents read own files at boot, no memory injection by lead
  |replaces: lead-injects-memory-into-prompt

arch:markdown-inboxes |by:user+lead |weight:directive
  |ctx: replaced JSON inboxes with markdown/ΣComm format, summarize-and-clear pattern
  |replaces: JSON inbox files (unused)

arch:shared-workspace |by:user+lead |weight:directive
  |ctx: shared/workspace.md for current task, agents write to own section, declare convergence
  |new: workspace.md, agent-declared convergence in workspace

arch:user-can-address-agents |by:user+lead |weight:directive
  |ctx: @agent-name routes user message to agent inbox in plain language, agent gets shared context

→ actions:
→ new team decision → format: topic:decision |by:expert |weight:primary/advisory
→ disagreement → record both positions with |ctx from each agent
→ revisiting old decision → check if conditions changed, note in ctx
