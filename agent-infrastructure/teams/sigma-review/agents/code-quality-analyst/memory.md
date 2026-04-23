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
sigma-ui-B1(26.3.29): BUILD TRACK|post-build review|grade:A-|165 tests(145+20 new)|6/6 checklist PASS|4 findings(1M,3L)|¬bugs|key: write-order verified correct(CQA-5 triple-convergence), 5-method cascade correct(CQA-6), originals deleted(CQA-2), AH rewrite correct(ADR[2])|R3[M]: deferred-scope trap flagged for B2 (active_gate=None hardcoded in get_snapshot())|promoted: write-order-before-reset pattern(auto), deferred-scope-trap(user-approve-pending)
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
ollama-mcp-bridge-audit-remediation(26.4.9): build-track | 6 ADRs reviewed | 814 tests, 0 regressions, +4 net new | 1 critical bug found (BUG[1]: ScanResult.blocked_profile never added — ADR[3] half-implemented, all 814 tests passed without catching it) | 6 passes (ADR[1-6] all correct code, clean style) | 2 non-blocking coverage gaps | highest-value: BUG[1] (enum-split without API-surface-split, 2-line fix + 1 test extension) | pre-challenge contributions: 8 formal challenges on 4 ADRs (Layer 2 scope, regex spec, test_types:755 preservation, approve_tool fallthrough, close() fsync, test_1597 update, ScanResult field, _check_profile_requirements test coverage)

## patterns
cross-repo-consistency: both repos share style conventions (future imports, logging, pathlib, naming)
error-handling-split: hateoas-agent raises exceptions (framework), sigma-mem returns error dicts (consumer) — appropriate for their roles
test-quality: both repos have edge-case tests, security tests, integration tests — above average for the scale
thriveapp-service-pattern: pure-logic(*-logic.ts) + supabase-wrapper(*.ts) split enables unit testing without mocks — excellent pattern
thriveapp-error-pattern: uniform {data,error} return across all 10 services, __DEV__ gated logging, no throws — disciplined
thriveapp-test-infra: real local Supabase for integration tests (not mocks), dual Jest config for services vs components
async-lint-gap: ruff ASYNC100/ASYNC101 does NOT catch blocking SDK constructors (openai.OpenAI(), genai.Client()) — not in ruff's blocking-call registry. Three-layer defense required: (1) ruff lint for convention, (2) stall-detector test (mock that sleeps), (3) nested-event-loop test (real client with empty key via to_thread(), assert no RuntimeError("already running")). Layer 3 catches SDK internals that may call asyncio.run() inside executor thread. SUPPLEMENT(26.3.29): asyncio.Semaphore created in one event loop CANNOT be acquired in another — asyncio.run() creates a new event loop per thread. ThreadPoolExecutor pattern (asyncio.run() per thread) requires Semaphore be created INSIDE the asyncio.run() context, not at module level or in the calling thread's loop. Symptom: RuntimeError("Task attached to a different loop") or silent hang. Fix: create Semaphore inside the coroutine, or use threading.Semaphore for cross-thread limiting.
error-contract-plan-gap: plan-phase error strategy typically scoped to the ONE module authors describe in detail (e.g. "if store fails, log and continue"). Other modules silently inherit no contract. Challenge: require EACH public method in EACH module's IC to state explicitly: raises SigmaUIError | returns Result|Error union. Choose ONE pattern before build starts — mixed raise/return-union is untestable as a system.
enum-coupling-multi-phase: when backend and frontend are built in separate phases, shared enum definitions must live in an explicit types.py (or equivalent). Enums defined inside implementation modules create Phase B import coupling — if dispatcher.py is refactored, Phase B imports break. Pattern: types.py = schema boundary, all other modules import from it. Scoped enums (e.g. DispatchMode.CLI reserved for later phase) should be documented as reserved-not-emitted to prevent Phase B tests passing vacuously. CALIBRATION(26.3.29): class X(str, Enum) migration is ZERO-COST for existing comparisons — `x == "VALUE"` and `"VALUE" in set` still pass because str Enum inherits str.__eq__. Only `type(x) is str` breaks (not `isinstance(x, str)`). Migration is purely additive: add enum, keep constants, existing tests unchanged. Dead-code tools (vulture) will falsely flag backward-compat string constants as unused if the only consumer is a test — whitelist or keep intentionally.
regression-anchor-before-edit: before modifying any function that feeds downstream numerical computations (belief scores, weights, posteriors), capture a snapshot test of exact output values on known fixtures. The test must PASS before the edit (verifying baseline) and continue to PASS after (verifying neutral behavior for zero-signal fixtures). This is the only reliable guard against "additive but not neutral" edits.
write-order-before-reset: within a single state-mutation method that both (1) captures current value into a registry/history AND (2) resets that value, the capture MUST execute before the reset. Non-obvious because both lines are syntactically valid in either order — the bug produces silent wrong data (registry always shows post-reset value) ¬crash. Pattern: document the constraint with a comment ("WRITE-ORDER LOAD-BEARING" or similar). Triple-convergence finding (CQA-5+DA[#4]+IE-4 independently in sigma-ui B1) confirms this is a recurring trap. sigma-ui example: `_phase_round_registry[from_phase] = self.current_round` BEFORE `self.current_round = 1` in record_phase_transition() (26.3.29).

enum-split-requires-api-surface-split: when splitting an enum into two distinct states (e.g. BLOCKED_SANITIZATION→BLOCKED_SANITIZATION+BLOCKED_PROFILE), the split is incomplete unless EVERY consumer data structure is also split. ToolState enum correctly updated ≠ ScanResult.blocked_profile field added. Tests that check only get_tool_states() pass even when the ScanResult layer is untouched — 814/814 green does not confirm full split. Pattern: for each new enum value, grep all data structures that aggregate by the old value and verify they are also updated. src:ollama-mcp-bridge(26.4.9).

field-name-gate>extension-gate for bare filename path extraction: constrain bare-filename detector to a semantic field name set (file, filename, path, filepath, db, database, etc) not extension regex. Extension-only heuristic fires on ALL fields producing widespread false positives (format="csv", query="report.json", content="data.json"). Field-name gate scopes to intent-declared fields only. Pair with a negative filter (URL/email/IP) for dual-use fields. src:ollama-mcp-bridge(26.4.9).

pydantic-v2-dormant-field-validator: to reject non-default values on a field while allowing the default (fail-closed on misconfiguration): use @field_validator("field_name", mode="after") @classmethod with `if v != default: raise ValueError(...)`. Works correctly on frozen=True models in pydantic v2. Must add field_validator to pydantic import. mode="after" is correct for post-coercion validation of bool/dict/list/int types. src:ollama-mcp-bridge(26.4.9).

unconditional-fsync-for-audit-writes: for infrequent security audit event writes (blocking events, rug pulls, rate limits), unconditional fsync on every flush is simpler and safer than a conditional two-path design. The performance cost is negligible because audit flushes are not in the hot path. Eliminates split-path complexity and ensures session-end close() provides full durability without a separate code path. src:ollama-mcp-bridge(26.4.9).

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
P[event-grammar-conformance-tests-EG|src:sigma-chatroom-m1ab-C1|promoted:26.4.21|class:pattern]: for streaming event APIs with tool-exec loops, test state-machine conformance explicitly. Grammar: token* → (tool_call+ → stop(tool_use, final_message) → tool_result+)* → token* → stop. Test categories: EG1 event-grammar conformance, EG2 parallel tool_call accumulation (INV4), EG3 final_message reconstruction fidelity, EG4 tool_result correlation, EG5 max_tool_calls final-text boundary. Independent tests for separable additions (EG2 and EG3 are orthogonal); integrated tests for combined state machine. Complements round-trip tests — round-trips verify correctness within phases, EG verifies phase sequencing. |source:[lead-proxy from scratch cqa BC-cqa-11 + R2 EG1-EG5 + cqa R2 delta]

## r19-remediation C1 COMPLETE — 26.4.23
BELIEF[r1]=0.88, DA PASS@A-, plan LOCKED.
Promoted to patterns.md: empirical-baseline-verification, test-map-methodology, live-pytest-as-prereq-to-claim-accept.

## r19-remediation C1 — 26.4.23

### Baseline survey (gate_checks + chain-evaluator test suite)
- Claimed baseline: 154 tests (project_gate-infrastructure.md, 26.4.16). Actual: 92 tests. Gap: 62 (20=orchestrator-archive commented-out; 42=unexplained).
- Pre-existing failures: 11/92 BEFORE any R19 changes. Root: MINIMAL_WORKSPACE uses `agent-alpha`/`agent-beta` not in roster.md → roster-based extraction returns only `devils-advocate`. Written before roster was added.
- Regression floor for C2: 81 currently-passing tests (¬154, ¬92).
- A16/A17/A18 (peer-verification ring): ZERO existing tests — largest untested surface.
- check_a3 chain-evaluator-level depth check (chain-evaluator.py:162-183): ZERO tests. Separate from gate_checks DB tests.
- chain-evaluator A12 unit tests: ZERO. Existing session-end tests are gate_checks level only.

### H5 revision
H5 ("¬regress to 154-test baseline") untestable as stated. Revised: keep 81 passing + add 30-46 new tests.

### Highest-risk new gate: #22 precision gate
Calibration flakiness risk HIGH. Must test against archived workspaces (R19: known-bad F[TA-C2] FTE range, known-good breakdowns) BEFORE C2 ships. Plan-track must specify detection algorithm before C2 estimates complexity.

### Prerequisite for C2
Fix MINIMAL_WORKSPACE fixture before writing any regression tests. Options: (a) use real roster agent names, (b) add test-agent names to roster, (c) restructure tests. Without fix, new regression tests give unreliable signal.

### Error-handling pattern constraint
New chain-evaluator gates must follow _wrap_gc() pattern. NOT mutate-after-wrap (check_a3 lines 162-183 is the anti-pattern).

### check_a3 duplication bug
chain-evaluator check_a3 has SECOND DB-depth check on top of gc.check_dialectical_bootstrapping. Uncoordinated — can produce passed=True with non-empty issues. R19 #19 fix must reconcile, not add third layer.
