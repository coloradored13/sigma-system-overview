# code-quality-analyst — personal memory

## identity
role: code quality specialist
domain: code-quality,test-coverage,dead-code,style-consistency,edge-cases,error-handling
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known codebases
hateoas-agent|~/Projects/hateoas-agent|19 src files,26 test files,1381 LOC,439 tests(6 skipped),91% coverage
sigma-mem|~/Projects/sigma-mem|5 src files,5 test files,~1.4K LOC,165 tests
thriveapp|~/Projects/thriveapp|~35 src files,13 test files,~10K LOC,365+ tests|Expo/RN+TS strict+Supabase+NativeWind
sigma-ui|~/Projects/sigma-ui|6 src files,8 test files,~1.2K LOC,112+ tests|Python 3.11+asyncio+hateoas-agent+sigma-mem+sigma-verify|Phase A backend (26.3.28)

## past findings
hateoas-agent(26.3.25): grade A-|no bugs|no security issues|6 CQ + 7 TG findings
  CQ1[M]: run_agent() silently swallows executor exceptions — no phase-level warning (xverified gpt-4o:agree:high). Fix: logger.warning after status=ERROR
  CQ2-CQ4[L]: unused import (persistence.py:10), unused exc var (mcp_server.py:115), unused loop var (orchestrator_visualization.py:47) — all auto-fixable
  CQ5[L]: advertisement.py DRY 80% duplication — carried from review-7, still unaddressed
  TG1[M]: runner.py NoHandlerError catch path (226-238) untested
  TG2[M]: runner.py on_transition callback (200-201) untested
  TG3-TG6[L]: runner multi-resource init, resource filter_actions guard-raise, composite fallback, async_runner ValueError
  H1: PARTIAL — core StateMachine/Resource/Registry/Runner adoption-ready; orchestration needs CQ1+TG1+TG2
  pattern: silent failures concentrated in guard+executor error paths across all 3 APIs — corroborates ux-researcher F-UX1
thriveapp(26.3.8): grade A-|SHIP-phase-4|9 findings(0C,0H,4M,3L,2I)+3 test gaps
  ts-strict: 5 `any`(3 justified:platform CSS gaps, 1 borderline:useAuth error cast, 1 unjustified:data-export.ts:155)
  DRY: CQ1 streak.ts:224-246 reimplements streak-logic.ts:56-67 week boundary funcs
  input-validation: CQ2+CQ3 service layer trusts callers, no runtime JSONB or quality_rating validation
  error-handling: CQ4 journal.ts:112 empty catch hides decrypt failures
  test-gaps: TG1 concurrent check-in race, TG2 encrypted journal export, TG3 onboarding partial failure
  positive: uniform {data,error} pattern, no dead code, Tier 1 7/7, Tier 2 9/9, real Supabase integration tests
  cross-agent: confirmed tech-architect S4, technical-writer D3+D12, product-strategist F1
review-7(26.3.7): grade A-|1 bug+2 DRY+3 test-gaps
  bug: resource.py:166-172 drops required field in ActionDef copy (StateMachine version correct)
  DRY: advertisement.py format_result/format_error 80% duplication, handlers.py 3 team-write handlers share pattern
  test-gaps: Runner+CompositeRegistry integration untested, _get_project_names parsing untested, handle_check_integrity wrapper untested
  style: handlers.py:420 uses `l` variable (PEP8 ambiguous)
  concern: handle_update_belief content.replace without section validation
  positive: no dead code, no unused imports, no security issues, excellent error handling, consistent cross-repo style
hateoas-agent(26.3.25): grade A(upgraded from A- after R2)|no bugs|no security|6CQ(all L/I)+7TG(TG1+TG2 M)|xverify gpt-4o CQ1
  CQ1[L→DA-accepted]: run_agent() silent ERROR swallow — logger.warning QoL fix only
  TG1[M]: runner.py:226-238 NoHandlerError catch path untested
  TG2[M]: runner.py:200-201 on_transition callback untested (public API)
  TG3-TG6[L]: composite fallback, resource filter_actions guard-raise, async_runner ValueError, runner multi-resource init
  auto-fixable: F401+F841+B007+PERF102+SIM103+SIM114(ruff --fix)
  DRY: advertisement.py still open from review-7
sigma-ui(26.3.28): BUILD TRACK|6 modules reviewed|grades: orchestrator_wrapper(A), dispatcher(A-), context_builder(A-), review_state(A), tier_a_observables(A), async_adapter(PENDING-sigma_verify-not-installed)
  GAP-1[M]: context_builder 4-item injection vs 7-item locked ADR[3] — sigma-comm.md + Comms + workspace_target missing. H3 mitigation partially incomplete.
  GAP-2[L]: review_state._build_phase_nodes() shows 0 completed_rounds for historical phases — Phase B phase strip breaks
  GAP-3[L]: orchestrator_wrapper.restore_checkpoint() calls _make_state() — ADR[1] "no private attr" constraint exception
  GAP-4[L]: No types.py — DS enum tests remain skipped
  GAP-5[L]: sigma_verify not pip-installed in test env — async_adapter suite blocked
  positive: SC2 stagger correctly on WRITE path (not dispatch path), BC[IE-6] task registry correctly prevents parsing task from output, CQ6 regression anchor passes pre+post extension

## calibration-corrections
§2d source tags: use [independent-research] ¬"direct-code-analysis" — DA correction 26.3.25
severity rule: 1-line fix + conceded design intent = LOW regardless of downstream failure class — DA confirmed 26.3.25

## calibration
first-review: thorough line-level sweep of 18+24 files. Found 1 real bug others missed (Resource required field). DRY findings minor. Test gap identification useful but not blocking.
second-review(thriveapp): first external project, first TS/RN codebase. Reviewed ~35 src + 13 test files. No bugs found (codebase is clean). DRY violation real but low-impact. Input validation gap (B+) is main weakness — service layer trusts UI callers. Test coverage assessment (Tier 1/2 matrix mapping) was highest-value deliverable. A- grade consistent with team consensus (all 4 agents graded A-).
sigma-ui-build(26.3.28): build-track first time. Challenge round (7 challenges, all accepted or compromised). Test infra built alongside IE. 112 passing, 11 skipped. Highest-value contributions: CQ3 error-contract challenge (prevented mixed raise/return-union across 5 modules), CQ6 regression anchor test (captured posteriors before gate_checks.py edit), GAP-1 identification (4-item vs 7-item injection gap vs locked ADR[3]).

## patterns
cross-repo-consistency: both repos share style conventions (future imports, logging, pathlib, naming)
error-handling-split: hateoas-agent raises exceptions (framework), sigma-mem returns error dicts (consumer) — appropriate for their roles
test-quality: both repos have edge-case tests, security tests, integration tests — above average for the scale
thriveapp-service-pattern: pure-logic(*-logic.ts) + supabase-wrapper(*.ts) split enables unit testing without mocks — excellent pattern
thriveapp-error-pattern: uniform {data,error} return across all 10 services, __DEV__ gated logging, no throws — disciplined
thriveapp-test-infra: real local Supabase for integration tests (not mocks), dual Jest config for services vs components
async-lint-gap: ruff ASYNC100/ASYNC101 does NOT catch blocking SDK constructors (openai.OpenAI(), genai.Client()) — not in ruff's blocking-call registry. Three-layer defense required: (1) ruff lint for convention, (2) stall-detector test (mock that sleeps), (3) nested-event-loop test (real client with empty key via to_thread(), assert no RuntimeError("already running")). Layer 3 catches SDK internals that may call asyncio.run() inside executor thread.
error-contract-plan-gap: plan-phase error strategy typically scoped to the ONE module authors describe in detail (e.g. "if store fails, log and continue"). Other modules silently inherit no contract. Challenge: require EACH public method in EACH module's IC to state explicitly: raises SigmaUIError | returns Result|Error union. Choose ONE pattern before build starts — mixed raise/return-union is untestable as a system.
enum-coupling-multi-phase: when backend and frontend are built in separate phases, shared enum definitions must live in an explicit types.py (or equivalent). Enums defined inside implementation modules create Phase B import coupling — if dispatcher.py is refactored, Phase B imports break. Pattern: types.py = schema boundary, all other modules import from it. Scoped enums (e.g. DispatchMode.CLI reserved for later phase) should be documented as reserved-not-emitted to prevent Phase B tests passing vacuously.
regression-anchor-before-edit: before modifying any function that feeds downstream numerical computations (belief scores, weights, posteriors), capture a snapshot test of exact output values on known fixtures. The test must PASS before the edit (verifying baseline) and continue to PASS after (verifying neutral behavior for zero-signal fixtures). This is the only reliable guard against "additive but not neutral" edits.

¬[no dead code found, no unused imports, no security issues in code review]

## research

R[linting: ruff dominates(900+ rules, replaces black+isort+flake8+pylint-lint), rust-speed(.4s vs pylint 2.5min/250kLOC), default=F+E rules, preview=412 defaults incl B+UP+RUF, key cats: F,W,E,I,UP,C4,B,SIM,RET,PTH,TD|ruff !replaces mypy/pyright—pair ruff+mypy for full coverage|src: docs.astral.sh/ruff, pythonspeed.com|refreshed: 26.3.7|next: 26.9]

R[typing: mypy --strict ideal for new/small codebases, native generics list[str] not List[str], int|str unions, Protocol for structural subtyping, TypeGuard for narrowing|install type stubs(types-requests etc), reveal_type()+--warn-return-any to find Any leaks|src: mypy.readthedocs.io, realpython.com|refreshed: 26.3.7|next: 26.9]

R[test-quality: property-based(hypothesis) finds ~50x more mutations than unit tests per test, mutmut+hypothesis boosted mutation score 70→92% on async|mutation: mutmut(active), mutpy(mature)|pair example+property+mutation for full quality|src: OOPSLA'25 PBT eval, johal.in/mutmut|refreshed: 26.3.7|next: 26.9]

R[dead-code: vulture(best-known, AST, 60-100% confidence, --make-whitelist), deadcode(newer, TOML, strict/dry-run)|coverage.py more reliable but needs runtime|combo vulture+deadcode for broad detect|src: github.com/jendrikseipp/vulture, ep2024.europython.eu|refreshed: 26.3.7|next: 26.9]

R[error-handling: EAFP>LBYL, catch narrowest, !bare except, py3.11 ExceptionGroups for concurrent, add_note() for context|custom: small hierarchy from Exception, prefer builtins|context managers for cleanup, error aggregation for batch|src: realpython.com, miguelgrinberg.com, qodo.ai|refreshed: 26.3.7|next: 26.9]

R[code-smells: Large Class+Long Method most prevalent Python, Extract Method most effective refactor|tools: ruff B rules(bugbear), SonarLint(IDE)|SRP check: non-descriptive names signal violations|src: refactoring.guru, codeant.ai|refreshed: 26.3.7|next: 26.9]

R[style: PEP8 stable—snake_case funcs/vars, CamelCase classes, UPPER_SNAKE constants, typing.Final(3.10+)|Google: 80 char, test_<method>_<state>, descriptive public APIs|src: peps.python.org/pep-0008, google.github.io/styleguide/pyguide.html|refreshed: 26.3.7|next: 26.9]

R[monorepo: consistency=top priority, single ruff/mypy config at root, shared pre-commit|editable installs(-e) for cross-pkg, path-based deps for internal|pants overkill for 2-pkg ~3.5kLOC|src: tweag.io, llamaindex.ai|refreshed: 26.3.7|next: 26.9]

R[DRY/SOLID: SRP via naming+size, OCP via Protocol/ABC, DIP via injection|checklist: (1)dup→extract (2)long func→split (3)broad except→narrow (4)missing types→annotate (5)dead imports→rm (6)test gaps→cover|src: realpython.com/solid, jetbrains.com/qodana|refreshed: 26.3.7|next: 26.9]

## review-tools
- ruff check --select ALL: full rule sweep on target codebase
- mypy --strict: type coverage audit
- vulture: dead code scan (complement manual review)
- mutmut: mutation testing to assess test suite quality
- hypothesis: property-based tests for data-heavy modules (serialization, state machines)
- ruff B rules: bugbear catches common Python pitfalls I should flag in review
