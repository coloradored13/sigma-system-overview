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

→ actions:
→ new pattern observed → append with |agents and |signal
→ pattern contradicted → move to ¬ section with explanation
