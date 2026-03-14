# code-quality-analyst — personal memory

## identity
role: code quality specialist
domain: code-quality,test-coverage,dead-code,style-consistency,edge-cases,error-handling
protocol: ΣComm (see ~/.claude/agents/sigma-comm.md)

## known codebases
hateoas-agent|~/Projects/hateoas-agent|13 src files,18 test files,~2K LOC,253 tests
sigma-mem|~/Projects/sigma-mem|5 src files,5 test files,~1.4K LOC,165 tests
thriveapp|~/Projects/thriveapp|~35 src files,13 test files,~10K LOC,365+ tests|Expo/RN+TS strict+Supabase+NativeWind

## past findings
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

## calibration
first-review: thorough line-level sweep of 18+24 files. Found 1 real bug others missed (Resource required field). DRY findings minor. Test gap identification useful but not blocking.
second-review(thriveapp): first external project, first TS/RN codebase. Reviewed ~35 src + 13 test files. No bugs found (codebase is clean). DRY violation real but low-impact. Input validation gap (B+) is main weakness — service layer trusts UI callers. Test coverage assessment (Tier 1/2 matrix mapping) was highest-value deliverable. A- grade consistent with team consensus (all 4 agents graded A-).

## patterns
cross-repo-consistency: both repos share style conventions (future imports, logging, pathlib, naming)
error-handling-split: hateoas-agent raises exceptions (framework), sigma-mem returns error dicts (consumer) — appropriate for their roles
test-quality: both repos have edge-case tests, security tests, integration tests — above average for the scale
thriveapp-service-pattern: pure-logic(*-logic.ts) + supabase-wrapper(*.ts) split enables unit testing without mocks — excellent pattern
thriveapp-error-pattern: uniform {data,error} return across all 10 services, __DEV__ gated logging, no throws — disciplined
thriveapp-test-infra: real local Supabase for integration tests (not mocks), dual Jest config for services vs components

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
