# implementation-engineer — agent memory

## identity
Role: Backend implementation specialist
Expertise: Python implementation, API integration, test writing, error handling, refactoring, code organization, performance implementation, migration/backward compatibility

## research

### T1 — Python async patterns (26.3.24)
R[asyncio/concurrent.futures best practices | 26.3.24 | source:independent-research]
- asyncio: I/O-bound concurrency only. async def must not wrap blocking ops — blocks entire event loop
- blocking ops: use loop.run_in_executor(ThreadPoolExecutor) to offload without blocking event loop
- cross-thread: run_coroutine_threadsafe() returns concurrent.futures.Future
- CPU-bound: use multiprocessing, not asyncio (compatible: can use both)
- concurrency control: asyncio.Semaphore to cap simultaneous operations
- perf: uvloop drop-in replacement for default event loop, significant throughput gains
- LLM/API workloads: asyncio + Semaphore is canonical pattern (cap concurrent requests)
- anti-pattern: time.sleep() inside async — always use asyncio.sleep()
- urls: https://docs.python.org/3/library/asyncio-dev.html | https://www.newline.co/@zaoyang/python-asyncio-for-llm-concurrency-best-practices--bc079176

### T2 — Pydantic v2 patterns (26.3.24)
R[Pydantic v2 validators/composition/serialization | 26.3.24 | source:independent-research]
- validators: @field_validator with before/after modes — precise lifecycle control, early rejection
- model_config: use ConfigDict(from_attributes=True, populate_by_name=True, extra='forbid', str_strip_whitespace=True) as sane base
- serialization: model_dump() / model_dump_json() — nested models serialize predictably; only annotated fields included (security benefit)
- computed_field: auto-included in serialization, prefer over @property
- SecretStr: prevents accidental logging of sensitive values
- class Config deprecated — use model_config = ConfigDict(...)
- v2 is 5-50x faster than v1 (Rust core)
- versioning: use inheritance for version-layered models (v2 extends v1 schema)
- pydantic.v1 namespace available for gradual v1-to-v2 migration
- urls: https://docs.pydantic.dev/latest/concepts/models/ | https://medium.com/@ThinkingLoop/12-pydantic-v2-model-patterns-youll-reuse-forever-543426b3c003

### T3 — Error handling: Result vs exceptions (26.3.24)
R[Python Result types vs exceptions | 26.3.24 | source:independent-research]
- Result type: explicit return for known failure modes (not exceptional, expected outcomes)
- exceptions: best when failure propagation is deep and caller does not need to check every op
- `returns` library: provides Result monad, pipeline composition for functions returning Result
- decision rule: "errors we know how to deal with" use Result; "errors we don't" use exception
- e.g. zero search results = normal behavior — use Result; unexpected DB connection drop — use exception
- pattern: wrap at boundaries, return Result inward, raise at edges for unexpected failures
- urls: https://www.inngest.com/blog/python-errors-as-values | https://aaronluna.dev/blog/error-handling-python-result-class/

### T4 — pydantic-settings / configuration management (26.3.24)
R[Python config management patterns | 26.3.24 | source:independent-research]
- pydantic-settings: BaseSettings reads from env vars, .env files, with priority layering
- environment layering: defaults < .env file < env vars < CLI args
- type coercion automatic from string env vars (bool, int, list parsing)
- model_config = SettingsConfigDict(env_file='.env', env_nested_delimiter='__') for nested config
- extra='forbid' catches misconfigured env vars early at startup
- urls: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

### T5 — Testing best practices (26.3.24)
R[Python testing pyramid/strategy 2025 | 26.3.24 | source:independent-research]
MOCK STRATEGY:
- mock only what you don't control (external APIs, 3rd-party services, hardware)
- use real implementations wherever feasible — over-mocking couples tests to impl details
- always use spec= or autospec=True — ensures mock matches real interface, catches signature drift
- wrap external library calls rather than mocking the library directly
- include integration tests with real deps alongside unit tests

PROPERTY-BASED TESTING (Hypothesis):
- use for: data validation, serialization/deserialization roundtrips, algorithm correctness
- consistently finds edge cases missed by example-based tests
- integrate with pytest via @given decorator
- best targets: parsers, validators, data transforms, sorting/ranking logic

CONTRACT TESTING:
- Pact for service-to-service contracts; 2025 data: 40% reduction in integration errors reported
- define consumer-driven contracts; verify provider conformance independently

FIXTURE PATTERNS:
- pytest-asyncio for async test fixtures with proper timeout management + resource cleanup
- conftest.py scope hierarchy: session > module > function — match scope to cost
- factory fixtures preferred over raw data fixtures for complex domain objects
- urls: https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest | https://danielsarney.com/blog/python-testing-best-practices-2025-building-reliable-applications/

### T6 — Code organization: clean arch + DI (26.3.24)
R[Python clean architecture / ports-adapters / DI 2025 | 26.3.24 | source:independent-research]
LAYERS (dependencies point inward):
1. Entities/Domain — pure business objects, zero external deps
2. Use Cases/Application — orchestrate entities, depend on port interfaces (ABCs)
3. Interface Adapters — convert data between use cases and external formats
4. Frameworks/Drivers — DB, web framework, APIs (outermost, swappable)

PORTS AND ADAPTERS:
- input ports: ABCs for driving adapters (web controllers, CLI)
- output ports: ABCs for driven adapters (repos, email, ML models)
- wire in composition root via factory functions

DI WITHOUT FRAMEWORK:
- inject deps via constructor args, not class-level globals
- factory functions or composition root wires deps at startup
- `dependency-injector` lib: 25% boilerplate reduction reported (fintech case 2025)
- FastAPI Depends leaks into layers — violates clean arch; treat Depends as adapter layer only

COUPLING METRICS:
- fan-out (deps on others): keep low for domain layer
- fan-in (used by others): high fan-in = stable, change carefully
- abstraction vs concreteness: abstract at boundaries, concrete in implementations

WHEN ABSTRACTION HURTS:
- premature abstraction before requirements stabilize
- adding interface for single implementation that will never vary
- over-engineering internal modules not crossed by multiple adapters
- urls: https://www.glukhov.org/post/2025/11/python-design-patterns-for-clean-architecture/ | https://johal.in/hexagonal-architecture-design-python-ports-and-adapters-for-modularity-2026/

### T7 — Pipeline/workflow implementation (26.3.24)
R[Python data pipeline patterns 2025 | 26.3.24 | source:independent-research]
ORCHESTRATION TOOLS:
- Dagster: declarative, asset-centric model, strong for data products
- Airflow: DAG-based, widest operator library, mature ecosystem
- Prefect: Python-native, simpler API, cloud control plane option

CHECKPOINTING:
- save intermediate state at stage boundaries
- two recovery modes: replay (restart from beginning) vs checkpoint (resume from saved state)
- prefer checkpoint for long multi-stage pipelines
- design tasks as idempotent — re-run produces same result regardless of count

STATE MACHINES:
- explicit states prevent ambiguous intermediate conditions
- transitions log to persistent store for audit + recovery
- combine with checkpointing: checkpoint on state transition

RETRY / BACKOFF (tenacity library):
- @retry(wait=wait_exponential_jitter(initial=1, max=10)) — standard pattern
- wait_random_exponential for distributed retry (prevents thundering herd)
- jitter formula: min(initial * 2**n + random.uniform(0, jitter), maximum)
- async support: tenacity works with asyncio coroutines
- wait_chain: different backoff profiles per retry tier (e.g. fast then slow)
- idempotency prerequisite for safe retry

QUEUE-BASED:
- decouple producers/consumers via queue (asyncio.Queue, Redis, SQS)
- dead-letter queues for failed messages after max retries
- urls: https://github.com/jd/tenacity | https://www.abstractalgorithms.dev/data-pipeline-orchestration-pattern-dag-retries-and-recovery

### T8 — Performance and optimization (26.3.24)
R[Python profiling + performance 2025-2026 | 26.3.24 | source:independent-research]
PROFILING TOOLS:
- cProfile: deterministic, stdlib, measures every call — high overhead, use for dev/staging only
- py-spy: sampling profiler, written in Rust, zero code changes, safe on production processes
  attach to running PID: `py-spy top --pid <PID>` or flamegraph output
- workflow: baseline, profile with realistic data, optimize 20% causing 80% slowdown, measure delta

JSON / SERIALIZATION:
- orjson: Rust-based, fastest schema-less JSON, rich type support (datetime, UUID, numpy)
- msgspec: combined serialization + validation; with Struct schemas = faster than orjson alone
- decision: orjson for simple high-throughput JSON; msgspec when typed structs + validation needed
- benchmark note: msgspec float parsing ~15% slower than orjson; msgspec wins for non-float-heavy data
- avoid stdlib json in hot paths — 2-10x slower than either alternative

CONNECTION POOLING:
- httpx.AsyncClient: built-in connection pooling, reuse across requests (create once, not per-request)
- requests.Session: same for sync; never create new Session per request
- asyncpg / SQLAlchemy async pool: set pool_size, max_overflow based on expected concurrency

REQUEST BATCHING:
- batch API calls where endpoint supports it; reduces round-trips dramatically
- asyncio.gather() for concurrent independent requests with Semaphore cap

MEMORY (long-running processes):
- use generators/iterators for large data streams, avoid materializing full lists
- gc.collect() rarely needed — profile before manual GC intervention
- tracemalloc for memory leak detection in dev
- urls: https://github.com/benfred/py-spy | https://jcristharif.com/msgspec/benchmarks.html | https://morethanmonkeys.medium.com/comparing-json-and-orjson-in-python-which-json-library-should-you-use-in-2025-850cd39ecb7d

### T9 — Migration and backward compatibility (26.3.24)
R[Python schema migration / backward compat 2025 | 26.3.24 | source:independent-research]
PYDANTIC MODEL VERSIONING:
- use inheritance for version chains: ModelV2(ModelV1) extends/overrides fields
- pydantic.v1 namespace for gradual v1-to-v2 migration (no breaking change)
- Pydantic commits to no breaking changes in minor v2 releases; deprecated items survive until v3

JSONL / FILE-BASED STORAGE MIGRATION:
- add version field to every record at write time (schema_version: int)
- migration reader: reads version field, applies transform chain to normalize to current schema
- never modify records in-place; write migrated copy to new file/table then swap
- forward compatibility: use Optional fields + default=None for new additions (old readers remain valid)
- additive changes safe; removals require version gate

SQLITE MIGRATION:
- alembic for SQLAlchemy-backed SQLite; sqlalchemy-migrate for simpler cases
- write migrations as numbered scripts; never hand-edit schema
- test migration on copy of production DB before applying

FEATURE FLAGS FOR GRADUAL ROLLOUT:
- Unleash (open source): gradual rollout by percentage + stickiness (same user gets same result)
- Flipt (open source, self-hosted, Go-based): git-native config, kill switches, A/B variants
- file-based: JSON config with feature_flags array; suitable for small teams / no infra overhead
- API versioning via flags: flag controls active API version, user-level or percentage-based

API VERSIONING STRATEGIES:
- URL path versioning (/v1/, /v2/): explicit, cacheable, clear deprecation path
- header versioning (Accept: application/vnd.api+v2): cleaner URLs, harder to test/cache
- use feature flags to shadow new version before hard cutover
- maintain old version for at least 1 deprecation cycle after new version GA
- urls: https://docs.pydantic.dev/latest/migration/ | https://docs.getunleash.io/guides/gradual-rollout | https://www.builder.io/blog/feature-flags-api-versions

### T10 — Clean code principles: refactoring + code smells (26.3.24)
R[Fowler refactoring catalog / Beck four rules / code smell taxonomy | 26.3.24 | source:independent-research]
KENT BECK FOUR RULES OF SIMPLE DESIGN (priority order):
1. Tests pass — code must work
2. Reveals intention — naming and structure communicate purpose
3. No duplication (DRY) — every piece of knowledge has one representation
4. Fewest elements — remove anything not required by rules 1-3 (no speculative generality)

KEY REFACTORING CATALOG (Fowler):
- Extract Method: pull named block out of long method; improves readability + reuse; most frequently applied
- Replace Conditional with Polymorphism: swap type-checked conditionals for subclass dispatch; eliminates shotgun surgery
- Introduce Parameter Object: group related params into value object; reduces long parameter lists
- Replace Primitive with Object: wrap raw types (String for email, int for money) in domain classes
- Move Method/Field: move to class that uses it most; fixes feature envy

CODE SMELL TAXONOMY:
- Feature Envy: method uses another class's data more than its own → move to that class
- Shotgun Surgery: one change requires many small edits in many places → consolidate
- Primitive Obsession: raw strings/ints for domain concepts → replace with value objects
- Divergent Change: class changes for multiple unrelated reasons → split by responsibility
- Speculative Generality: hooks/abstractions for hypothetical future use → delete; re-add when needed
- Data Clumps: groups of data that always travel together → extract to Parameter Object

WHEN NOT TO REFACTOR:
- working code under time pressure — carry the debt, schedule paydown explicitly
- code about to be replaced/rewritten — don't refactor what will be deleted
- speculative generality — don't add abstraction for a single current implementation
- test-induced design damage: mocking heavy enough to drive bad architectural decisions
  (DHH/Fowler/Beck debate 2014, still relevant) — over-isolation for testability can distort design more than help it
- urls: https://martinfowler.com/books/refactoring.html | https://xp123.com/articles/speculative-generality/ | https://dhh.dk/2014/test-induced-design-damage.html

### T11 — Architecture patterns: hexagonal, modular monolith, event-driven (26.3.24)
R[Hexagonal / modular monolith / CQRS / event sourcing when-warranted | 26.3.24 | source:independent-research]
HEXAGONAL (PORTS AND ADAPTERS):
- operates at component level — orthogonal to mono vs. micro decision
- input ports: ABCs for driving adapters (HTTP, CLI, tests)
- output ports: ABCs for driven adapters (DB, email, queues)
- benefit: 35% lower coupling vs. layered architecture (SEI 2025 benchmark)
- overhead: adds indirection and interface boilerplate — only justified when adapters vary or swap
- anti-pattern: single adapter per port that never varies → premature abstraction

MODULAR MONOLITH (preferred starting point):
- self-contained modules with explicit APIs between them
- lower ops cost than microservices; can extract services later if needed
- hexagonal + modular monolith = good preparation: adapters become natural extraction boundaries
- real failure mode: microservices at 47 users, burning runway on distributed systems overhead
- guidance: start modular monolith, extract services at pain points with data and evidence

CQRS (Command Query Responsibility Segregation):
- separate read models from write models; can be lightweight (separate query methods) or heavy (separate DBs)
- lightweight CQRS (direct read queries + encapsulated write services) → safe default, low overhead
- heavy CQRS (separate event-sourced write store + read projections) → only when read/write perf profiles diverge significantly
- warranted: high-concurrency, audit requirements, complex domain rules, eventual consistency acceptable
- not warranted: simple CRUD, small teams, early-stage products

EVENT SOURCING:
- store sequence of events as source of truth; derive current state by replay
- benefits: full audit trail, time-travel queries, replayability
- cost: permeates entire architecture; hard to migrate away; eventual consistency required
- warranted: banking, audit-critical domains, event-driven integrations
- not warranted: small/simple domains, CRUD-heavy systems, teams unfamiliar with pattern
- key rule: CQRS and event sourcing are independent — can use either without the other

DDD LIGHTWEIGHT (bounded contexts + ubiquitous language, without full tactical ceremony):
- bounded context: explicit model boundary where a term has one meaning — prevents semantic leakage
- ubiquitous language: shared vocabulary between domain experts and developers — eliminates translation errors
- apply selectively: strategic design (contexts, relationships) > tactical patterns (repositories, factories)
- trap: getting lost in tactical DDD patterns before strategic design is clear
- when to skip full DDD: small teams, simple domains, early-stage where model is still being discovered
- urls: https://medium.com/@the_atomic_architect/architecture-patterns-that-actually-scale-in-2025-the-only-three-you-need-89d1488c60a7 | https://martinfowler.com/bliki/BoundedContext.html | https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs

### T12 — Testing philosophy: Test Desiderata, pyramid vs diamond, mutation testing (26.3.24)
R[Kent Beck Test Desiderata / pyramid-diamond / sociable-solitary / mutation testing | 26.3.24 | source:independent-research]
KENT BECK TEST DESIDERATA (12 properties — tradeoffs, not checklist):
1. Isolated — result independent of other tests
2. Composable — test dimensions separately, combine results
3. Deterministic — same result each run if nothing changed
4. Fast — run quickly
5. Writable — cheap to write relative to code cost
6. Readable — communicates why this test exists
7. Behavioral — sensitive to behavior changes
8. Structure-insensitive — don't break when code is refactored without behavior change
9. Automated — no manual steps
10. Specific — failure points clearly to source
11. Predictive — passing tests predict production behavior
12. Inspiring — test suite builds confidence
Key: no property should be sacrificed without gaining a property of greater value. Tests trade off; no single test maximizes all 12.

PYRAMID VS DIAMOND DEBATE:
- pyramid: many unit tests, fewer integration, few E2E — speed + isolation emphasis
- diamond: fewer unit tests (only critical cases), wider integration layer, some E2E — reflects reality that unit tests often erode without high-value targets
- 2025 consensus: shape depends on domain. I/O-heavy systems → diamond makes sense. Algorithmic / pure-logic systems → pyramid. Neither is universally correct.

SOCIABLE VS SOLITARY UNIT TESTS:
- solitary: stubs all collaborators; full isolation; tests one unit in vacuum
- sociable: allows real lightweight collaborators; more realistic context; fewer mocks
- over-mocking risk: tests couple to implementation rather than behavior; break on refactor even with no behavioral change
- guidance: prefer sociable when collaborators are lightweight domain objects; use solitary when crossing expensive/unstable boundaries

TEST-INDUCED DESIGN DAMAGE:
- occurs when isolation requirements drive architectural decisions that harm production code quality
- symptoms: interfaces for every dependency, excessive constructor injection, public internals exposed for testing
- antidote: use sociable tests where appropriate; mock only what you don't control; accept higher-level test scope

MUTATION TESTING (test quality assessment):
- creates small program mutations (mutants); surviving mutant = test suite missed that behavior
- quantifies test quality beyond coverage percentage (coverage ≠ effectiveness)
- Meta 2025: LLM-based mutation testing at scale — generates realistic mutants + targeted tests; reduces operational overhead
- tools: mutahunter (language-agnostic, open source), PIT (Java), cosmic-ray (Python)
- practical: run on critical paths only — mutation testing is expensive; use coverage first to find gaps, mutation to validate test effectiveness
- urls: https://medium.com/@kentbeck_7670/test-desiderata-94150638a4b3 | https://github.com/codeintegrity-ai/mutahunter | https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/

### T13 — Error handling across paradigms (26.3.24)
R[Railway-oriented programming / error categorization / circuit breaker / bulkhead | 26.3.24 | source:independent-research]
RAILWAY-ORIENTED PROGRAMMING (ROP):
- every function returns Success or Failure track; composition routes failures around subsequent steps
- implemented via Result/Either monad — errors as values, explicit in type signature
- F# origin (Scott Wlaschin); available in most languages via libraries
- Python: returns library (0.26+) implements ROP pipeline; map/bind/alt operators
- benefit: forces caller to handle failure path; eliminates silent error swallowing
- tradeoff: more verbose; unfamiliar to teams used to exception-based flow

ERROR CATEGORIZATION (3-type model):
- retryable: transient failures (network timeout, rate limit 429) — retry with backoff
- fatal: permanent failures (auth 401, bad request 400) — fail immediately, no retry
- user-facing: validation errors, business rule violations — surface with actionable message
- decision rule: categorize at boundary; propagate category, not just error text

ERROR AS VALUES VS EXCEPTIONS DEBATE:
- exceptions: good for truly exceptional / unexpected conditions; propagate across layers automatically
- values (Result): good for expected failure paths that callers should handle explicitly
- hybrid (recommended): use Result for domain failure paths; use exceptions for infrastructure failures
- C# discriminated unions (preview 2025): native language support reducing library dependency

CIRCUIT BREAKER PATTERN:
- three states: CLOSED (normal), OPEN (failing, reject fast), HALF-OPEN (probe recovery)
- prevents retry storms against dead downstream services
- threshold: N failures in M seconds → OPEN; probe after timeout → HALF-OPEN
- .NET Microsoft.Extensions.Resilience (stable .NET 9): built-in retry+circuit breaker+timeout pipelines

BULKHEAD PATTERN:
- isolate thread/connection pools per dependency: one failing service can't exhaust all resources
- prevents cascading failures across service boundaries
- used with circuit breaker: circuit breaker prevents requests to dead services; bulkhead prevents resource exhaustion from those requests
- rule of thumb: separate bulkheads for: external HTTP calls, DB connections, CPU-bound work
- urls: https://fsharpforfunandprofit.com/rop/ | https://dzone.com/articles/circuit-breaker-pattern-resilient-systems | https://www.codecentric.de/en/knowledge-hub/blog/resilience-design-patterns-retry-fallback-timeout-circuit-breaker

### T14 — API design principles (26.3.24)
R[Richardson maturity / API versioning / idempotency / pagination / rate limiting | 26.3.24 | source:independent-research]
RICHARDSON MATURITY MODEL (4 levels):
- L0: single endpoint, single verb (RPC over HTTP) — not REST
- L1: multiple resources (separate URIs per resource) — basic REST
- L2: HTTP verbs + status codes correctly used — industry standard target
- L3: HATEOAS — hypermedia links in responses drive client state; Fowler calls L3 "the glory of REST"
- practical: most APIs target L2; L3 useful for generic clients and API discoverability

API VERSIONING STRATEGIES:
- URL path (/v1/, /v2/): explicit, cacheable, easy to test and route — most widely used
- header (Accept: application/vnd.api+v2+json): cleaner URLs; harder to test manually, can't bookmark
- content negotiation: most HTTP-correct; highest implementation complexity
- deprecation rule: maintain old version ≥1 full cycle after new version GA; communicate timeline in response headers

IDEMPOTENCY IN API DESIGN:
- GET, HEAD, DELETE, PUT: idempotent by HTTP spec
- POST: not idempotent by default → implement idempotency keys (client generates UUID per request)
- pattern: store idempotency key + response; replay stored response on duplicate
- critical for: payment APIs, retry-safe mutations, webhook processing

PAGINATION:
- offset/page: simple; inconsistent under concurrent inserts (duplicate/skip records); expensive at large offsets (SQL OFFSET scans all rows)
- cursor: position-based (e.g. last seen ID or timestamp); consistent under insertion; no total count; cannot jump to arbitrary page; 17x faster than offset at deep pages
- guidance: cursor for activity feeds, real-time data, infinite scroll; offset acceptable for static reference data with small dataset
- Slack evolution: started offset, migrated to cursor as dataset scale made offset untenable

RATE LIMITING AND BACKPRESSURE:
- rate limiting: caps requests per client per time window; return 429 Too Many Requests with Retry-After header
- backpressure: signal to producer to slow down when consumer is overwhelmed; implemented via queue depth, bounded buffers, or reactive streams
- algorithms: token bucket (smooth bursts), leaky bucket (strict rate), sliding window (accurate)
- expose limits in headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
- urls: https://martinfowler.com/articles/richardsonMaturityModel.html | https://embedded.gusto.com/blog/api-pagination/ | https://slack.engineering/evolving-api-pagination-at-slack/

### T15 — Technical debt management (26.3.24)
R[Cunningham debt metaphor / debt quadrant / strangler fig / refactor vs rewrite | 26.3.24 | source:independent-research]
WARD CUNNINGHAM'S ORIGINAL METAPHOR (1992):
- "shipping first time code is like going into debt — a little debt speeds development so long as it is paid back promptly with a rewrite"
- interest = time lost on future changes due to not-quite-right code
- key intent: debt is a tool, not a failure; the danger is debt not repaid

FOWLER TECHNICAL DEBT QUADRANT (2-axis):
- axis 1: deliberate (conscious choice) vs inadvertent (lack of knowledge)
- axis 2: reckless ("no time for design") vs prudent (aware of tradeoffs)
- four cells:
  1. deliberate+prudent: "we ship now, we'll fix later" — acceptable short-term
  2. deliberate+reckless: "quick and dirty" with awareness — avoid
  3. inadvertent+prudent: discovered in hindsight as team learned — inevitable, pay down
  4. inadvertent+reckless: unknown unknowns — prevention via review, mentoring, standards

WHEN TO PAY DOWN VS CARRY DEBT:
- pay down: when debt increases cost of every future change in that area
- carry: when code is stable, not frequently changed, or about to be replaced
- Fowler: refactor opportunistically ("preparatory refactoring") — clean path before adding feature; don't schedule separate refactoring sprints

REFACTOR VS REWRITE DECISION FRAMEWORK:
- refactor when: incremental improvement is possible; tests exist or can be added; blast radius is contained
- rewrite when: fundamental architectural mismatch; no viable incremental path; tech debt interest exceeds feature velocity
- warning: rewrites consistently underestimated; "second system effect" — new code accrues new debt

STRANGLER FIG PATTERN (Fowler):
- incrementally replace legacy system by routing new functionality to new code while legacy handles remainder
- facade/proxy intercepts all requests; routes to new service or legacy based on capability
- never touch the legacy system for new features — always build new
- gradual: investment and returns visible incrementally; reduces big-bang rewrite risk
- 2025 status: "definitive architectural standard for risk-averse legacy modernization" (Thoughtworks)
- practical phases: (1) intercept, (2) migrate one capability, (3) verify, (4) repeat, (5) delete legacy
- urls: https://martinfowler.com/bliki/TechnicalDebtQuadrant.html | https://martinfowler.com/bliki/StranglerFigApplication.html | https://shopify.engineering/refactoring-legacy-code-strangler-fig-pattern

### T16 — Observability and debugging (26.3.24)
R[Three pillars / structured logging / correlation IDs / production debugging | 26.3.24 | source:independent-research]
THREE PILLARS OF OBSERVABILITY:
- logs: discrete events; archival record; structured preferred over plain text
- metrics: numerical measurements over time (latency, error rate, CPU); alerting backbone
- traces: request path across services; reveals bottlenecks and service dependencies
- relationship: metrics alert to a spike → logs explain the event → traces show where in the call chain
- key principle: observable system can answer unpredicted questions; monitoring answers predicted ones

STRUCTURED LOGGING:
- machine-parseable format (JSON); consistent field names across services
- required fields per log event: timestamp, level, service, correlation_id, trace_id, event_name, + context fields
- log levels: DEBUG (dev only), INFO (normal ops), WARN (degraded not broken), ERROR (failure requiring attention), FATAL (service cannot continue)
- anti-pattern: string interpolation in log messages — breaks field extraction; use structured fields
- SecretStr / redaction: never log raw credentials, tokens, PII — apply redaction at log sink or model layer

CORRELATION IDs:
- generated at system entry point (API gateway, first service); propagated as header (X-Correlation-ID) through all downstream calls
- enables: filter all logs for a single user request across 20 services in seconds vs hours
- implementation: generate UUID if not present in incoming request; inject into every log event and outbound call header
- trace ID vs correlation ID: trace ID is span-scoped (changes at service boundary); correlation ID is request-scoped (constant end-to-end) — use both

DEBUGGING METHODOLOGY (scientific method applied):
1. observe: reproduce symptom; gather evidence (logs, metrics, traces)
2. hypothesize: form specific testable hypotheses about root cause — ≥2 before testing any
3. experiment: change one variable; predict expected outcome before running
4. observe result: confirm or falsify; update hypothesis
5. conclude: root cause confirmed when prediction matches observation
- production debugging tools: py-spy (attach to PID, no restart), distributed tracing (Jaeger, Zipkin, OTEL), feature flags (disable suspect code path in prod)
- OpenTelemetry (OTEL): vendor-neutral instrumentation standard; instrument once, export to any backend (Jaeger, Honeycomb, Datadog)

PRACTICAL PATTERNS:
- correlation ID in every outbound HTTP call header — not optional in distributed systems
- structured logs queryable by field (Loki, CloudWatch Logs Insights, Elasticsearch)
- trace sampling: 100% in dev/staging; 1-10% in prod with head-based sampling; always sample errors
- SLO/SLI framework: define error budget; alert on budget burn rate not raw error count
- urls: https://www.ibm.com/think/insights/observability-pillars | https://microsoft.github.io/code-with-engineering-playbook/observability/correlation-id/ | https://medium.com/insiderengineering/leveraging-correlation-ids-to-increase-backend-system-observability-daa2fb0f0438

## findings
- asyncio + Semaphore is the canonical LLM/API pipeline concurrency pattern in 2025
- msgspec outperforms orjson when schemas are pre-defined (Structs); orjson wins for schema-less
- py-spy is the production-safe profiler; cProfile for dev only
- Result types (returns lib) complement exceptions: use Result for expected failure paths, exceptions for unexpected
- clean arch violation: FastAPI Depends leaks into domain — keep Depends at adapter layer
- Hypothesis property-based testing consistently finds bugs missed by example-based tests
- tenacity is the standard retry/backoff library; always add jitter for distributed retry
- schema migration safety: add version field at write, read-time transform chain, no in-place modification
- mock only what you don't control; autospec=True prevents interface drift
- [T10] test-induced design damage is real — over-mocking for isolation can harm architecture more than help; sociable tests preferred where collaborators are lightweight
- [T11] start modular monolith; hexagonal architecture makes future microservice extraction clean; event sourcing permeates entire architecture — adopt only for audit-critical domains
- [T11] CQRS without event sourcing is safe and low-cost; heavy CQRS + event sourcing only when justified by data
- [T12] Kent Beck Test Desiderata: 12 properties are tradeoffs, not checklist; mutation testing (mutahunter) reveals test effectiveness beyond coverage numbers
- [T13] circuit breaker + bulkhead used together: CB prevents retry storms to dead services; bulkhead prevents resource exhaustion from those requests
- [T14] cursor pagination: 17x faster than offset at deep pages; consistent under concurrent inserts — default for real-time/feed data; offset acceptable for small static datasets
- [T14] Richardson L2 is the practical target for most APIs; idempotency keys are essential for POST mutations at payment/critical paths
- [T15] Fowler debt quadrant: deliberate+prudent = acceptable tool; inadvertent+reckless = prevention target; carry debt on stable-infrequently-changed code; pay down on hot paths
- [T15] strangler fig is the definitive safe legacy replacement pattern (Thoughtworks 2025); intercept → migrate → verify → repeat → delete
- [T16] correlation ID is non-optional in distributed systems; propagate in every outbound header; enables minutes-vs-hours incident resolution
- [T16] OpenTelemetry is the vendor-neutral instrumentation standard; instrument once, export anywhere

## calibration
- serialization benchmarks: numbers are benchmark-specific (float-heavy data changes winner)
- clean arch overhead: premature abstraction before requirements stabilize = net negative
- feature flags: file-based suitable for simple cases; Unleash/Flipt for team-scale gradual rollout
- property-based testing: high value for data transforms/validators, lower for UI/integration tests
- test pyramid vs diamond: no universal correct shape — domain and collaborator weight determine the right ratio
- event sourcing adoption rate is low: warranted in specific domains (banking, audit), not general-purpose
- DDD tactical patterns (repositories, factories) are high ceremony; bounded contexts + ubiquitous language deliver 80% of the value with much lower cost
- strangler fig is slower than a rewrite but consistently safer; rewrites systematically underestimate cost (second system effect)
- mutation testing is expensive — run on critical paths only; use after coverage gaps already closed

## patterns (promoted 26.3.28 — sigma-ui review)

P[AsyncRunner-private-attr-coupling|src:sigma-ui|promoted:26.3.28|class:calibration]
AsyncRunner._async_start()/_async_advance() access Orchestrator private attrs directly (_current_phase, _context, _phase_history at lines 97-99, 117-128 of async_runner.py). Risk ELEVATED in systems where AsyncRunner is used as gate-enforcement trust anchor. Mitigation: asyncio.to_thread(orch.start/advance) using public Orchestrator API. ¬use AsyncRunner for gate-critical paths until private-attr bypass is resolved upstream in hateoas-agent.

P[Agent-SDK-version-check-before-dismissal|src:sigma-ui|promoted:26.3.28|class:calibration]
Agent SDK dismissed as "0.x premature" based on locally installed version — DA challenge revealed v0.1.48 with hooks+sessions+MCP write-lock had shipped (Mar 2026). Disqualification was provisional, not confirmed. Pattern: always verify current SDK version via pip/PyPI before finalizing SDK ranking in analysis. Code-read of installed version ¬sufficient when SDK evolves rapidly. ¬dismiss as premature without spike test or current API review.

P[convention-only-async=design-defect|src:sigma-ui|promoted:26.3.28|class:calibration]
Convention-only async enforcement ("use asyncio.to_thread() where needed") = design defect in FastAPI/async servers. Single blocking call (openai.OpenAI(), google.genai.Client(), file I/O) in async context stalls ALL concurrent dispatches — single-threaded event loop, no error raised, stall is silent under load. Fix: thin async adapter class wrapping ALL sync client methods at boundary + ruff ASYNC100/ASYNC101 lint rule + pytest-asyncio timeout integration tests. Framing as "acknowledged risk" is wrong — this requires architectural fix, not risk acceptance.
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.28|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore


## patterns (auto-promoted from project work)

P[strenum-derived-frozenset-validation|src:sigma-ui-B1|promoted:26.3.29|class:pattern]
When implementing string-validated enum fields in Python, derive the validation frozenset FROM the enum: `_VALID = frozenset(tag.value for tag in MyEnum)`. This guarantees a single canonical source — adding a member to the enum automatically adds it to validation. Using an independently-defined frozenset creates drift risk (add to enum, forget frozenset, or vice versa). ADR[5]/DA[#3] in sigma-ui B1 caught an independent frozenset definition and required derivation. O(1) membership check preserved. Pattern: always pair StrEnum with `_VALID_X = frozenset(tag.value for tag in X)`.
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore
S[26.3.29|agent:implementation-engineer|sdk-dispatch|fallback]: S[test] sdk-dispatch test entry — safe to ignore

→ sociable tests over purely solitary tests when isolation cost > value
