# ARCHIVED WORKSPACE — R19 Sigma-Review Infrastructure Remediation (C1 PLAN phase)
archived: 2026-04-23 | mode: BUILD-C1 | rounds: 1 | verdict: DA PASS @ A- | belief: P=0.88
original: ~/.claude/teams/sigma-review/shared/builds/2026-04-23-r19-remediation/c1-scratch.md
team: r19-remediation-c1
agents: tech-architect, security-specialist, cognitive-decision-scientist, implementation-engineer, code-quality-analyst, technical-writer, devils-advocate
directives-version: build-directives.md (extracted 26.3.19) + directives.md + protocols.md (session reads 26.4.23)
audit: run /sigma-audit ${this-file-path} in fresh context to verify process compliance

---

# C1 scratch — BUILD: r19-remediation
## status: archived-c1
## mode: BUILD
## build-id: 2026-04-23-r19-remediation
## team-name: r19-remediation-c1
## directives-version: build-directives.md (extracted 26.3.19) + directives.md + protocols.md (per session reads 26.4.23)

## task
Remediate top-10 ROI infrastructure + protocol issues from R19 sigma-review post-mortem (2026-04-22 ai-agent-rollout-playbook-vet, audit GREEN / eval B 3.14). Both code (chain-evaluator.py, phase-gate.py, sigma-verify MCP) and directives/spawn-templates/agent-defs in scope. Source: ~/.claude/projects/-Users-bjgilbert/memory/project_sigma-review-infrastructure-issues.md

## infrastructure
ΣVerify: ready — 13 providers (openai, google, llama, gemma, nemotron, deepseek, qwen, devstral, glm, kimi, nemotron-nano, qwen-local, anthropic). XVERIFY enforced anthropic-EXCLUDED per C8.
project-tier: NOT present for sigma-system-overview — using global T/ only
session-id: 2026-04-23 sigma-build C1 PLAN
chain-evaluator: ~/.claude/hooks/chain-evaluator.py (target of #4, #19, #20)
phase-gate: ~/.claude/hooks/phase-gate.py (target of potential #1 mechanical block, #21 if hook-enforced)
gate_checks: ~/.claude/teams/sigma-review/shared/gate_checks.py (target of #4 if rename direction chosen)

## prompt-understanding
Q[]: build scope
- Q1: Fix critical infra — #1 sed -i mechanical block, #3 ΣVerify agent-context tool inheritance, #4 A12 parser key-mismatch
- Q2: Fix high-priority infra — #5+#14 peer-verify regex + spawn template alignment, #19 A3 DB-step parser false negatives, #20 A12 archive timing window
- Q3: Add 4 protocol-layer gates — #21 premise-audit pre-dispatch, #22 §2i precision gate, #23 governance min-artifact, #24 §2d severity provenance
- Q4: Update directives + spawn templates + agent defs to enforce mechanically (¬just instruction)

H[]: hypotheses to test (¬requirements)
- H1: ΣVerify MCP source is under user-control and can be modified to register all sub-tools at init (drives #3 architecture)
- H2: New analytical gates (#22, #23) can be calibrated to fire on legitimate over-claims without false positives requiring exception-handling (per "accountable rigor over permissiveness")
- H3: Premise-audit (#21) fits as a pre-spawn lead workflow step (extending c1-plan.md Step 8) rather than a new agent role
- H4: All 11 fixes ship in a single build — ¬circular dependencies between them
- H5: New protocol gates can be added to chain-evaluator without regressing the 154-test baseline

C[]: constraints
- C1: Top-10 ROI only (#2, #6-#18 deferred to follow-up)
- C2: Both code + directives in scope
- C3: ¬regress to chain-evaluator/phase-gate test suites
- C4: Per "WARNs must be BLOCKs" memory: new gates with ¬legitimate override → hard BLOCK
- C5: Per "accountable rigor over permissiveness": when a gate over-fires, defend each invocation rather than add exceptions
- C6: All changes git-committed + pushed from sigma-system-overview per session-end checklist
- C7: 3 R19 artifacts already RESOLVED 2026-04-23 (UP-B, UP-C, MITRE ATLAS) — out of scope
- C8: XVERIFY excludes anthropic provider — Claude verifying Claude is not cross-model. All sigma-verify calls must specify `providers` parameter excluding `anthropic`. (Added post-confirmation 26.4.23 as methodology constraint, not scope change.)

## scope-boundary
This build implements:
- 11 issue tickets bundled into 9 priorities (5 infrastructure + 4 protocol-layer)
- Code fixes: chain-evaluator.py parser/regex (#4, #5, #19, #20), phase-gate hook updates (#1 mechanical block), sigma-verify MCP tool registration model (#3)
- Directive updates: spawn template canonical formats (#5+#14), §2i precision gate criteria (#22), §2d severity provenance extension (#24), §8e corruption recovery template formalization
- New workflow steps: #21 premise-audit pre-dispatch in c1-plan.md, #23 HIGH-severity governance min-artifact requirement
- Tests for every code change
- IN-SCOPE EXPANSION (added 26.4.23 by lead per user decision after CQA finding): check_a3 DB-depth check duplication bundled into #19 fix. chain-evaluator.py:162-183 runs a SECOND DB check on top of gc.check_dialectical_bootstrapping — uncoordinated, can produce passed=True with non-empty issues. #19's fix must reconcile this (one of: remove duplicate, sync results, add wrapper). Plan-track ADR for #19 must address.
- LEAD INVESTIGATION (26.4.23): "lost test files" finding from CQA traced to deliberate consolidation, NOT regression. Commit b2cb381 added 150 chain-eval/phase-gate tests; commits ea5ae97 + d9d21ad archived them as "orphan tests / stale structural checks." chain-evaluator and phase-gate now tested only indirectly via test_hooks.py (24 tests). Decision per user: NOT in scope to restore — proceed with new tests for new gates only.
- IN-SCOPE EXPANSION (added 26.4.23 by lead per user OQ-SS2 decision after security-specialist plan-track ADR[2]): chain-evaluator pre-flight check (proposed ID: A21 — coordinate with CDS's A20 for #22 to avoid collision; TA to reconcile A-check ID assignment in their ADR for IC contracts) that verifies agents called `sigma-verify init` before XVERIFY tags appear. Converts #3 fix from compliance-reliant (spawn-prompt instructs init call) to mechanical enforcement per C4 ("WARNs must be BLOCKs"). Plan-track tech-architect must add ADR for this when they engage.

This build does NOT implement:
- MEDIUM/LOW R19 issues (#2 concurrent-write, #6 DA-as-agent treatment, #7 sigma-mem retry, #8 phase-gate header literal, #9 spawn collision suffix auto-resolve, #10-#18 bundled cleanup) — deferred to follow-up
- The 3 already-resolved R19 artifacts (UP-B SOC 2 mapping, UP-C GDPR Art 22 fork, MITRE ATLAS citation fix)
- Generic chain-evaluator hardening beyond the targeted fixes
- New agent role for premise-audit (#21 evaluated as workflow step OR DA framework extension OR new agent — H3 is the testable hypothesis)
- sigma-verify default-anthropic-exclusion (deferred to separate build; for now, enforced via spawn prompts and memory)

Lead: before accepting agent output, verify it builds ONLY what's in scope. Out-of-scope expansion (e.g. proposing #6 mid-plan) → flag and defer.

## complexity-assessment
BUILD TIER-3 |scores: module-count(5),interface-changes(4),test-complexity(3),dependency-risk(5),team-familiarity(2) |total:19 |plan-track:3 |build-track:3 |adversarial:1(DA at Step 18)

## roster
plan-track:
- tech-architect (sonnet) — parser/hook architecture, MCP tool registration model, ADRs for #3/#21
- security-specialist (sonnet) — MCP trust boundaries (#3), workspace integrity (#1)
- cognitive-decision-scientist (sonnet) — analytical gate design #21/#22/#23/#24

build-track:
- implementation-engineer (sonnet) — code fixes #1/#3/#4/#5/#14/#19/#20, new gate code #21-#24
- code-quality-analyst (sonnet) — test extension, regression coverage
- technical-writer (sonnet) — directive updates, spawn template format changes, agent-def updates

adversarial:
- devils-advocate (opus) — spawned at Step 18 (plan challenge phase), NOT in this initial spawn round

## plans (plan-track agents)
### tech-architect

#### §2a positioning check
ADR[1] auto-ready: default pattern for HATEOAS MCP servers addressing fresh-connection tool visibility |outcome:2 confirmed, concern: init semantic contract changes noted in DB[1] |source:[code-read /Users/bjgilbert/Projects/sigma-verify/src/sigma_verify/machine.py:1-128]
ADR[2] rename chain-evaluator vs gate_checks: one-line fix, leaf-consumer rename minimum blast radius |outcome:2 direction confirmed |source:[code-read gate_checks.py:1517, chain-evaluator.py:241]
ADR[3] timing window: grace-window approach established |outcome:1 analysis changes recommendation to signal-driven — see ADR[3] rationale |source:[code-read chain-evaluator.py:234-245, gate_checks.py:1457-1535]
ADR[4] premise-audit: H3 proposes workflow step |outcome:2 confirmed, concern: no mechanical enforcement flagged in PM[3] |source:[code-read SCRATCH:29]

#### §2b external calibration
RC[1] MCP state machine auto-init: FastMCP pattern (register all tools at startup) is prevalent ~90% of MCP servers. Auto-ready aligns sigma-verify with ecosystem default. |source:[agent-inference]
RC[2] one-line key rename: parser key-name mismatches base rate 1-3 day fix, trivial regression risk. |source:[agent-inference]
RC[3] timing window: analogous to CI/CD artifact upload timing windows. Signal-driven rarer but more correct than grace-window. |source:[agent-inference]

#### §2c cost/complexity
ADR[1] auto-ready: machine.py ~5 lines, handlers.py 0 lines. Reversal cost: 1 day. |source:[code-read machine.py:17-128]
ADR[4] premise-audit as new agent: +15-20% session cost. As workflow step: zero added cost. |source:[agent-inference]

#### §2e premise viability (ADR[1] auto-ready)
Assumption: registry._last_state is server-instance scope not connection scope. CONFIRMED: Registry instantiated once in serve(), all connections share same registry. |source:[code-read mcp_server.py:102-127]
Assumption: auto-calling handle_init() at build_machine() time is safe. CONFIRMED: handle_init() only checks API keys and returns status. |source:[code-read handlers.py:1-60]
openai XVERIFY concern (init may do more than key checking) resolved by code read confirming init does ONLY key-check. |source:[code-read handlers.py]

#### ADR[1]: #3 ΣVerify agent-context tool inheritance
|decision: auto-transition to ready state at server startup when any provider API key present
|alternatives:
  A: modify Claude Code deferred-tool system — REJECTED: not in user control, wrong layer
  B: add init call to spawn prompts — REJECTED: soft control dropped under load; only mechanical enforcement sticks |source:[auto-memory feedback_process-over-momentum.md]
  C: expose action tools from unconfigured (from_states=*) — REJECTED: allows tool calls when no providers configured; breaks semantic contract
  D: auto-transition to ready at build_machine() startup if keys present — SELECTED
|rationale: D eliminates root cause at server startup. Registry._last_state is process-scope shared across all MCP connections. Calling handle_init() once during build_machine() transitions state permanently for all subsequent connections. Preserves init semantic contract (key check still happens at startup not lazily). From agents perspective: all tools visible on first ToolSearch. Code change: ~5 lines in machine.py.
|H1-test-result: CONFIRMED. User owns sigma-verify at ~/Projects/sigma-verify. machine.py:17-128 is exact fix location. H1 assumption drives ADR[1]-D over ADR[1]-A. |source:[code-read machine.py:17]
|security-note: auto-ready does NOT reduce security — tools still provider-gated at call time. Gateway gate only controlled tool VISIBILITY not AUTHORIZATION. |source:[code-read handlers.py, machine.py]
|XVERIFY:
  XVERIFY[openai:gpt-5.4]: partial(medium) — correct root cause; concern: init may do more than key-checking. Resolved by code-read confirming init ONLY checks key presence. |source:external-openai-gpt-5.4|
  XVERIFY-FAIL[google:gemini-3.1-pro-preview]: 503 UNAVAILABLE |→ verification-gap, not skip
  XVERIFY[nemotron:nemotron-3-super:cloud]: agree(high) — server-instance scope confirmed, auto-transition eliminates root cause for all connections. |source:external-nemotron-nemotron-3-super:cloud|
  Net: 2/3 providers returned (1 agree/high, 1 partial/medium-resolved), 1 fail (google-503). XVERIFY threshold met.
|prompted-by: Q1,H1,C2

#### ADR[2]: #4 A12 parser key-mismatch — rename direction
|decision: rename in chain-evaluator.py:241 (archive_exists → archive_file_found)
|alternatives:
  A: rename chain-evaluator.py:241 — SELECTED
  B: rename gate_checks.py:1517 returned key — REJECTED: gate_checks is source-of-truth API, renaming changes contract for all consumers
|rationale: chain-evaluator.py:241 is leaf consumer. gate_checks.py:1517 is canonical. Renaming at leaf: 1 line, 0 API contract change, 0 downstream risk. git_clean read correctly at chain-evaluator.py:262 — asymmetry isolated to archive_exists vs archive_file_found. |source:[code-read chain-evaluator.py:241,262, gate_checks.py:1517-1519]
|DB[2]: (1)initial: rename gate_checks canonical term (2)assume-wrong: changing gate_checks breaks all callers (3)counter: rename leaf consumer only, zero contract change (4)re-estimate: leaf rename strictly safer (5)reconciled: rename chain-evaluator.py:241 only
|prompted-by: Q1,H4,C3

#### ADR[3]: #20 A12 archive timing window
|decision: signal-driven re-run with 30s timeout fallback
|alternatives:
  A: phase-gate waits on archive-complete signal — PARTIAL (complementary)
  B: 24h grace-window (auditor suggestion) — REJECTED as primary: too coarse, passes A12 even if no archive EVER written
  C/D: signal-driven with timeout fallback — SELECTED
|rationale: 24h grace-window masks absent-archive scenarios. Root cause is timing: chain-evaluator runs BEFORE archive write completes. Fix: add check_a12_post_archive() called from Stop hook after detecting synthesis_delivered signal; if archive dir mtime within 60s of Stop hook fire, A12 gets second-chance evaluation. Fallback: if no signal within 30s, log A12-TIMEOUT and use archive_file_found from directory check (existing behavior).
|DB[3]: (1)initial: 24h grace window per auditor (2)assume-wrong: 24h too coarse, masks absent-archive scenarios (3)counter: signal-driven second-chance on Stop hook (4)re-estimate: signal-driven + timeout fallback more correct (5)reconciled: signal-driven with 30s timeout and directory-check fallback
|prompted-by: Q2,H4,C3

#### ADR[4]: #21 premise-audit architecture
|decision: pre-dispatch workflow step in c1-plan.md / sigma-lead spawn template (H3 confirmed)
|alternatives:
  A: workflow step in c1-plan.md — SELECTED
  B: DA framework extension — PARTIAL complement; fires at Step 18 = too late to change frame
  C: new agent role (premise-auditor) — REJECTED: agent has no findings at pre-dispatch; adds cost
|rationale: Premise-audit is LEAD responsibility — happens before H-level agent spawning. DA framework extension fires at plan challenge (Step 18), too late to change frame. H3 CONFIRMED: workflow step at Step 7a before spawn is right insertion point. Implementation: add Step 7a to c1-plan.md requiring explicit premise-audit output to workspace ## premise-audit with 3-5 frame assumptions tested as distinct from H-hypotheses.
|H3-test-result: CONFIRMED. DA does premise work in R19 only at Step 18. Frame assumptions baked into agent spawning by then. Step 7a pre-dispatch correct. |source:[code-read SCRATCH:29, R19 post-mortem:agent-inference]
|DB[4]: (1)initial: new-agent role (2)assume-wrong: agent has no findings at pre-dispatch, no DA context (3)counter: lead workflow step at Step 7a before spawn (4)re-estimate: lead step cheaper and more correct (5)reconciled: workflow step + DA framework extension (complementary)
|prompted-by: Q3,H3,C2

#### IC[1]: chain-evaluator.py ↔ gate_checks.py — A12 key contract
|contract: gate_checks.check_session_end() → CheckResult with details['archive_file_found']:bool
|consumer post-fix: chain-evaluator.check_a12() reads details.get('archive_file_found', False)
|currently broken: reads 'archive_exists' (key absent → always False) |source:[code-read chain-evaluator.py:241, gate_checks.py:1517]
|test: assert check_a12(workspace_with_archive).passed == True; assert check_a12(workspace_without_archive).passed == False

#### IC[2]: chain-evaluator.py → workspace.md — A12 timing signal
|contract: Stop hook fires → check workspace for synthesis-complete marker or archive dir mtime within 60s → if signal found, re-run check_a12_post_archive()
|signal: synthesis agent writes ## synthesis-complete to workspace OR archive dir mtime check
|timeout: 30s from Stop hook fire — if no signal, use existing directory-check (fallback)
|new function: check_a12_post_archive(content: str, max_wait_s: int = 30) → ChainItem

#### IC[3]: machine.py ↔ handlers.py — startup-ready protocol
|contract: build_machine() calls handle_init() internally → if any provider available, registry._last_state set to 'ready'
|caveat: handle_init() synchronous; stays unconfigured if no keys
|effect: all MCP tool-list queries after server start return full action set when keys present
|test: mock handle_init → assert registry._last_state == 'ready' → assert all action tools in schema list

#### IC[4]: chain-evaluator.py A3 ↔ DB step detection
|current: check_a3() step-count check with threshold <3 on exact marker strings
|post-fix: multi-marker OR logic — any 3 of 5 canonical markers qualifies entry as substantive
|marker set (expanded): initial|assume_wrong|assume.wrong|counter|strongest_counter|re_estimate|re.estimate|reconcile|reconciled
|rationale: R19 audit found all 5 steps present in 5/5 verified sections; current regex fails on natural-language variants |source:[code-read chain-evaluator.py:173-176]

#### IC[5]: peer-verify header — chain-evaluator.py ↔ spawn template
|current regex CORRECT: _PEER_VERIFY_HEADER = r"^### Peer Verification:\s*(\S+)\s+verifying\s+(\S+)"
|spawn template WRONG: was producing "#### Peer Verification: Y" (4 hashes, target-only)
|fix-direction: update spawn template only; no code change to regex
|canonical format: ### Peer Verification: {verifier} verifying {verified} |source:[code-read chain-evaluator.py:277-280]

#### SQ[1]: chain-evaluator.py A12 key fix
|file: /Users/bjgilbert/.claude/hooks/chain-evaluator.py:241 |change: archive_exists → archive_file_found |owner: implementation-engineer |est: 30min |estimable:yes

#### SQ[2]: chain-evaluator.py A12 timing signal
|file: /Users/bjgilbert/.claude/hooks/chain-evaluator.py |change: add check_a12_post_archive() + wire into Stop hook |owner: implementation-engineer |est: 3h |dependency: IC[2]

#### SQ[3]: chain-evaluator.py A3 DB step-marker expansion
|file: /Users/bjgilbert/.claude/hooks/chain-evaluator.py:173-176 |change: expand marker list, keep threshold 3-of-5 |owner: implementation-engineer |est: 1h

#### SQ[4]: peer-verify (template only — no code change)
|files: sigma-lead spawn templates |change: update peer-verification to 3-hash canonical format |owner: technical-writer |est: 30min

#### SQ[5]: sigma-verify machine.py auto-ready startup
|file: /Users/bjgilbert/Projects/sigma-verify/src/sigma_verify/machine.py |change: call handle_init() in build_machine(); if providers available, transition registry to ready |owner: implementation-engineer |est: 2h |dependency: IC[3]; sigma-verify tests must pass

#### SQ[6]: sigma-verify tests for auto-ready
|file: /Users/bjgilbert/Projects/sigma-verify/tests/ |change: add test_auto_ready_on_startup, test_tools_visible_without_init_call |owner: code-quality-analyst |est: 2h

#### SQ[7]: phase-gate.py #1 sed -i mechanical BLOCK
|file: /Users/bjgilbert/.claude/hooks/phase-gate.py |change: PreToolUse Bash hook — detect sed -i / awk -i / bash redirect → BLOCK |owner: implementation-engineer |est: 3h |also: update directives.md + agent-defs

#### SQ[8]: spawn template peer-verify format + #14 alignment
|files: c1-plan.md, c2-build.md, agent definitions |change: ### Peer Verification: {verifier} verifying {verified} |owner: technical-writer |est: 1h

#### SQ[9]: premise-audit workflow step (c1-plan.md Step 7a)
|file: ~/.claude/teams/sigma-review/shared/c1-plan.md |change: Step 7a before spawn-agents — premise-audit output to workspace ## premise-audit |owner: technical-writer |est: 2h

#### SQ[10]: chain-evaluator.py precision gate (#22, §2i)
|file: /Users/bjgilbert/.claude/hooks/chain-evaluator.py |change: add check_a_precision() — numeric claims above threshold require driver-breakdown OR CI with reference class |owner: implementation-engineer |est: 4h |dependency: CDS calibration thresholds

#### SQ[11]: chain-evaluator.py HIGH-severity governance artifact gate (#23)
|file: /Users/bjgilbert/.claude/hooks/chain-evaluator.py |change: add check_a_governance_artifact() — HIGH-severity governance findings require template-stub OR decision-tree OR specimen marker |owner: implementation-engineer |est: 3h

#### SQ[12]: directives.md §2d severity provenance extension (#24)
|file: ~/.claude/teams/sigma-review/shared/directives.md |change: extend §2d to require source tag on severity extrapolations |owner: technical-writer |est: 1h

#### SQ[13]: test suite extension for all new checks
|files: test suite chain-evaluator + gate_checks |change: extend 154-test baseline for SQ[1-4,10,11] |owner: code-quality-analyst |est: 5h

#### RC[1]: MCP state machine gateway remediation |reference-class: hateoas_agent MCP servers |base-rate: 1-3 days |sample-size:2 |confidence:M |src:[agent-inference]
#### RC[2]: hook pattern extension |reference-class: phase-gate.py additions |base-rate: 2-4h per check |sample-size:5+ |confidence:H |src:[agent-inference]
#### RC[3]: directive + spawn template updates |reference-class: prior sigma-system-overview edits |base-rate: 0.5-1h per section |sample-size:10+ |confidence:H |src:[agent-inference]

#### CAL[total-build C2]: |point:2d |80%=[1.5d,3d] |90%=[1d,4d] |breaks-if: sigma-verify registry internals differ from reading, A3 regex unexpected behavior on real workspaces
#### CAL[SQ[5] sigma-verify auto-ready]: |point:2h |80%=[1.5h,4h] |90%=[1h,6h] |breaks-if: handle_init() has external HTTP side effects at startup
#### CAL[SQ[10] precision gate]: |point:4h |80%=[3h,7h] |90%=[2h,10h] |breaks-if: numeric claim detection has high false-positive rate requiring calibration tuning

#### PM[1]: Auto-ready fails with no provider keys at startup
|failure: handle_init() runs at startup, 0 providers → stays unconfigured → tools still invisible |likelihood:20%
|early-warning: XVERIFY-FAIL on all providers despite init fix deployed
|mitigation: startup log "ΣVerify auto-ready: N providers available"; document env-var requirement

#### PM[2]: A3 marker expansion causes false-passes
|failure: loosened regex qualifies inline word matches ("the initial analysis") as step markers |likelihood:15%
|early-warning: audit catches A3 PASS with no substantive DB work
|mitigation: require DB[ opening tag plus 3 markers not 3 markers anywhere; IC[4] specifies this constraint

#### PM[3]: Premise-audit step skipped under delivery pressure (HIGHEST RISK)
|failure: Step 7a added to c1-plan.md but lead skips — matches historical failure pattern |likelihood:35%
|early-warning: workspace lacks ## premise-audit; DA flags in challenge round
|mitigation: CDS designs chain-evaluator check for ## premise-audit presence; DA gets explicit instruction to BLOCK exit-gate if absent

#### PM[4]: Peer-verify template fix breaks historical archive audits
|failure: old 4-hash format in R19 archive; new 3-hash format in new sessions; sigma-audit on R19 flags A16 false-failures |likelihood:10%
|mitigation: document fix is forward-only

#### DB[1]: #3 auto-ready vs keep gateway gate
(1)initial: keep gateway gate, add init to spawn prompts
(2)assume-wrong: spawn prompt = soft control; R19 had 5 XVERIFY-FAIL from 5 agents who all SHOULD have called init — soft control failed systematically
(3)counter: auto-ready eliminates per-agent friction; downside: init no longer required = gateway concept weakened
(4)re-estimate: semantic change acceptable — init remains callable (idempotent); server pre-initializes on startup
(5)reconciled: auto-ready at startup when keys present; init remains callable for explicit re-check; gateway preserved as optional diagnostic not mandatory gate

#### prompt-understanding mapping
Q1 (critical infra): ADR[1]→#3, ADR[2]→#4, SQ[7]→#1 |source:[agent-inference]
Q2 (high-priority infra): ADR[3]→#20, IC[4]+SQ[3]→#19, IC[5]+SQ[4,8]→#5+#14 |source:[agent-inference]
Q3 (protocol gates): ADR[4]→#21, SQ[10]→#22, SQ[11]→#23, SQ[12]→#24 |source:[agent-inference]
Q4 (mechanical enforcement): SQ[7,8,9] + CDS precision/governance gates |source:[agent-inference]
H1: CONFIRMED — user owns sigma-verify at ~/Projects/sigma-verify, machine.py modifiable |source:[code-read machine.py:17]
H2: DEFERRED to CDS — precision gate calibration thresholds are CDS domain
H3: CONFIRMED — premise-audit fits as workflow step ADR[4]-A |source:[code-read SCRATCH:29]
H4: CONFIRMED — no circular dependencies; SQ[5] depends on machine.py only; SQ[1-4] are chain-evaluator only
H5: CONFIRMED — new checks extend existing check_a* pattern; 154-test baseline extensible via SQ[13]

✓ tech-architect COMPLETE | ADR[1-4] + IC[1-5] + SQ[1-13] + RC[1-3] + CAL[1-3] + PM[1-4] + DB[1-4]
XVERIFY ADR[1]: openai(partial/medium-resolved) + nemotron(agree/high) + google(503-gap)

#### Challenge responses — Step 22

BC[#1]: CQA H5 stale test count — CONCEDE (partial) — [evidence counter]
CQA claimed "92 tests, 81 passing." Empirical check run 26.4.23: three relevant test files (test_chain_evaluator.py + test_phase_gate.py + test_gate_checks.py) collect 154 tests, 143 passing, 11 pre-existing failures. My H5 claim of "154-test baseline" was correct on collection count. The nuance I missed: 11 are pre-existing failures, so the PASSING floor is 143, not 154. H5 confirmation stands on collection count; revision needed on passing-floor language. |source:[code-read live-pytest 26.4.23]
→ SQ[13] revised: "extend 154-test baseline (143 passing, 11 pre-existing failures); new tests must not regress 143 passing floor; pre-existing 11 failures are known tech-debt, not regression targets for this build."
→ CAL[SQ[13]] revised per BC[#3]: see BC[#3] response below.

BC[#2]: CQA ADR[3] Stop hook non-looping violation — CONCEDE
CQA is correct. enforce_stop() at chain-evaluator.py:625-640 is explicitly designed non-looping: "returns informational messages only, never actionable demands that would cause Claude to retry." A 30s poll/wait inside enforce_stop() violates this invariant by design. My ADR[3] signal-driven approach requires polling the archive dir mtime — that IS a wait/loop in the Stop hook. This was a process error: I read the design comment but did not apply it to my own proposal.
→ ADR[3] REVISED: adopt 24h grace-window approach (IE Option C, ~20 LOC).
Rationale: 24h grace-window does NOT mask absent-archive scenarios the way I claimed. The check is: has archive dir mtime changed within 24h of session-start AND archive_file_found is True? If no archive file exists, archive_file_found=False and A12 still fails regardless of grace window. My original objection ("24h passes A12 even if no archive ever written") was wrong — the grace window only affects TIMING of when chain-evaluator checks, not whether archive existence is required. Evidence: gate_checks.py:1517 returns archive_file_found=True only when archive files actually exist.
→ IC[2] REVISED: remove signal/timeout contract. Replace with: check_a12() uses 24h grace — if session_start_time is within 24h of current time, A12 result is advisory (WARN not FAIL) when archive_file_found is False. If session >24h old, A12 is hard FAIL.
→ CAL[SQ[2]] revised: 3h → 1h (~20 LOC, deterministic datetime mock tests). |source:[code-read chain-evaluator.py:625-640, gate_checks.py:1517]

BC[#3]: CQA SQ[13] estimate underestimate — CONCEDE
5h was set before CDS A20 spec was available and before the full test surface was mapped. CQA's 8-12h range and sub-task split is correct.
→ SQ[13] SPLIT:
  SQ[13a]: fixture prerequisite fix |owner:code-quality-analyst |est:1h
  SQ[13b]: A12 key fix (2 tests) + A16/A17/A18 peer-verify (8-12 tests) |owner:code-quality-analyst |est:2h
  SQ[13c]: A3 chain-evaluator level marker expansion (4-6 tests) |owner:code-quality-analyst |est:1h
  SQ[13d]: A20 precision gate + calibration (est: 4h if CONDITION 1 code-detected; 2h if DA-delegated — see BC[#4]) |owner:code-quality-analyst |est:2-4h |dependency:CDS CONDITION 1 decision
  SQ[13e]: #23 governance artifact (3-4 tests) + #24 severity provenance (2-3 tests) |owner:code-quality-analyst |est:2h
  SQ[13f]: SS BLOCK-3 sed-i (8 tests per expanded CQA matrix) |owner:code-quality-analyst |est:1h
  SQ[13g]: A12 24h grace (2-3 deterministic datetime mock tests) |owner:code-quality-analyst |est:1h
  Total revised: 11-15h across 7 sub-tasks (8-12h CQA estimate confirmed as floor; 15h ceiling if CONDITION 1 code-detected)

BC[#4]: CQA IC[3] DB marker duplication — CONCEDE
CQA is correct: after the fix, two code paths evaluate DB depth with potentially different criteria — gate_checks.check_dialectical_bootstrapping (presence check only) and chain-evaluator.check_a3() (calls gc then appends its own shallow_db). This produces A3 passed=True (from gc) with issues non-empty (from chain-evaluator), which is an inconsistent state that will confuse implementation-engineer.
→ IC[4] REVISED (was IC[4], now clarified): chain-evaluator check_a3() is the authoritative depth-detection layer. gate_checks.check_dialectical_bootstrapping() remains as the presence check (has_db = any DB[] present). chain-evaluator check_a3() is the depth check (has_db AND 3-of-5 markers present). The two checks are NOT alternatives — they are layered: gc detects presence, chain-evaluator detects depth. The current code at lines 162-183 already implements this correctly (calls gc first, then adds depth check). The fix is to expand the marker list in chain-evaluator:173-176 only; gate_checks is not modified. IC[4] must make this layering explicit.
→ IC[4] REVISED contract: gate_checks.check_dialectical_bootstrapping() = PRESENCE check (authority: has any DB[] entry?). chain-evaluator check_a3() = DEPTH check (authority: do present entries have 3-of-5 step markers?). chain-evaluator wraps gc result then augments with depth. Both layers required; neither is redundant. Result: A3 passed = gc.passed AND chain-evaluator depth check passes. |source:[code-read chain-evaluator.py:162-183, gate_checks.py:440-457]

TW BC[#2]: sigma-lead.md §2 added to IC[5] scope — CONCEDE
TW is correct that sigma-lead.md §2 spawn block must change atomically with c1-plan.md Step 11 and chain-evaluator regex. If sigma-lead.md carries the old 4-hash peer-verify format and c1-plan.md Step 11 is updated to 3-hash, lead will spawn from the old template. IC[5] scope must include sigma-lead.md.
→ IC[5] REVISED scope: files that must change atomically for peer-verify fix: c1-plan.md Step 11 + sigma-lead.md §2 spawn block + _template.md + (chain-evaluator regex already correct — no change). All three template files change in same commit. |source:[cross-agent:TW DOC-CHANGE-MAP]

#### DA responses — round 1 (Step 22)

DA[#1]: #19 root-cause misdiagnosis — CONCEDE (full, with empirical evidence)
DA is correct on both sub-claims. Verified via Python regex test 26.4.23:
(a) '.' IS already wildcard in Python regex: re.search("assume.wrong", "assume wrong") = True; re.search("assume.wrong", "assume-wrong") = True; re.search("assume.wrong", "assume_wrong") = True. Only "assumewrong" (no separator) fails — not a real agent failure mode. My IC[4] marker-variant expansion (assume.wrong -> assume_wrong variant) was solving a non-problem. |source:[live-python-test 26.4.23]
(b) Actual bug is DB[] extraction: re.findall(r"DB\[.*?\].*?(?=DB\[|\Z|###)", text, re.DOTALL) matches DB[F[SS-1]] (finding refs), DB[] inline mentions, DB[] summary notes — all with 0 step markers — alongside genuine DB exercises. Marker-variant expansion would not fix this because non-exercise tokens never have ANY markers regardless of separator. |source:[live-python-test 26.4.23]
3/3 XVERIFY confirmed (openai agree/medium + google agree/high + deepseek agree/medium). Concede fully.

→ IC[4] REVISED (complete rewrite): DB[] extraction fix = split-by-DB[-then-require-numbered-structure-within-segment. Algorithm: split workspace text by r"(?=DB\[)" boundaries; for each segment starting with DB[, check whether segment contains (1)...(2)...(3) structure via re.search(r"\(1\).*\(2\).*\(3\)", segment, re.DOTALL). Only segments with numbered structure qualify as DB exercises. Marker-variant expansion VOIDED — was solving wrong problem. |source:[DA[#1]+live-python-test]

→ SQ[3] REVISED: "Fix check_a3() DB extraction: replace re.findall(r'DB\[.*?\]...') with split-by-DB[-then-check-(1)(2)(3)-within-segment. Remove marker-variant expansion (solved wrong problem). Est: 2h (revised up from 1h — extraction logic more complex than single-regex change)." |source:[live-python-test]

Process note: I confirmed IC[4] by reading code intent but did not test the regex empirically against non-exercise tokens before writing. DA[#1] is a legitimate "should have been agent-regex-tested pre-lock" failure. |source:[DA[#1] engagement grade downgrade rationale]

DA[#2] / DIV[1]: #3 ΣVerify architecture — ACCEPT COMPROMISE
DA compromise: TA ADR[1]-D auto-ready AS PRIMARY + document in machine.py + ADR that (a) init idempotent+callable post-startup, (b) future state-gated tools requiring explicit consent must add own call-time authorization check NOT relying on unconfigured→ready gateway alone, (c) gateway re-documented as "optional diagnostic + future-tool state-boundary" not "mandatory agent handshake."
Evidence basis: openai XVERIFY PARTIAL counter ("changing readiness from explicit transition to automatic startup side effect can weaken architectural role of gateway") is a real concern for future tool additions. Compromise correctly splits: auto-ready solves immediate problem; gateway semantic documentation prevents future-tool failure mode.
→ ADR[1] REVISED: auto-ready primary; add machine.py code comment + ADR documentation of gateway semantic contract. SS spawn-prompt retained as belt-and-suspenders (belt: server-side; suspenders: documentation).
I do not contest the compromise. It strengthens the fix without changing the primary mechanism. |source:[DA[#2]+openai-XVERIFY counter]

DA[#7]: H5 + SQ[0] fixture prerequisite — CONCEDE
DA and CQA both correct. 11 pre-existing failures include fixture prerequisite (MINIMAL_WORKSPACE roster alignment) that blocks A3/A16/A17/A18 test runs. Without SQ[0], SQ[3] and SQ[13b/13c] cannot run on clean baseline.
→ SQ[0] ADDED: fix MINIMAL_WORKSPACE workspace fixture for roster alignment; fix 11 pre-existing test failures. Owner: code-quality-analyst. Est: 1-2h. Blocks: SQ[3], SQ[13b], SQ[13c]. Must complete before any A3/A16-A18 test work begins.
→ SQ[13] passing-floor revised: "extend from 143-passing floor (after SQ[0] fixture fix, target 143+N passing); do not regress any currently-passing test." Strike "154-test baseline" language entirely.
→ H5 status revised: "FALSIFIED on passing-floor claim (81/92 per CQA, verified 143/154 by TA live-pytest — close enough; key point: passing floor != collected count)." SQ[0] prerequisite is the critical addition. |source:[CQA empirical+DA[#7]+live-pytest]

DA[#8] (non-blocking): DB[4] "redundant-with-DA" counter — DEFEND
DA challenge: DB[4] never tests "don't do premise-audit at all — redundant with DA Step 18."
Explicit counter now tested:
Counter: DA at Step 18 catches frame-anchoring; premise-audit is redundant overhead.
Against: DA fires AFTER agent spawning and initial analysis rounds. By Step 18, agents have produced findings anchored to original frame. DA can challenge the frame but agents must REVISE FINDINGS already written. R19 evidence: DA[#6] produced 2 new findings (F[CDS-C1] firm-size floor, F[CDS-C2] adoption-oversight-overhead) requiring re-examination of findings already written. Step 7a/8.5 premise-audit catches this BEFORE spawning — prevents rework, not just catches error. Cost: 5-10 min lead overhead. Savings: eliminates Step 18 full-finding-revision when frame is wrong. "Redundant-with-DA" counter fails because timing differs: pre-spawn audit prevents anchoring; post-spawn DA is remediation after anchoring.
Reconciliation: DB[4] step-5 maintained with this explicit defense added. H3 status revised per DA[#9]: "partially confirmed — workflow-step subspace tested; no-premise-audit subspace now explicitly defended rather than untested." |source:[R19 post-mortem DA[#6] evidence:agent-inference]

#### Revised ADR/IC/SQ summary (post-DA round 1)

ADR[1]: auto-ready primary + gateway semantic documentation (DA[#2] compromise accepted)
ADR[2]: A12 key rename chain-evaluator:241 — UNCHANGED
ADR[3]: 24h grace-window — UNCHANGED (BC[#2] concede)
ADR[4]: premise-audit workflow step — UNCHANGED in decision

IC[4] REVISED: split-by-DB[-then-require-(1)(2)(3)-within-segment. Marker-variant expansion VOIDED. |source:[DA[#1]]

SQ[0] ADDED: fixture-fix prerequisite, owner:CQA, est:1-2h, blocks SQ[3]+SQ[13b]+SQ[13c]
SQ[2] est: 1h (24h grace, ~20 LOC) [BC[#2]]
SQ[3] REVISED: split-then-check extraction logic, est 1h→2h [DA[#1]]
SQ[13] passing-floor: "from 143-passing floor after SQ[0]" — "154-test baseline" language struck [DA[#7]]


### security-specialist

#### §2a: approach positioning
Scope covers 4 security concerns: #1 sed-i block (workspace integrity), #3 ΣVerify tool inheritance (MCP trust), #22/#23 audit-trail architecture.
PreToolUse hook is the canonical enforcement point — phase-gate.py uses it for BLOCK 1 (Write/Edit) and BLOCK 2 (Bash git). Adding BLOCK 3 matches established ecosystem.
§2a outcome 2: approach confirmed |source:[independent-research] phase-gate.py read — 2 prior BLOCKs confirm pattern is growing. Simpler alternative (directive-only) rejected per WARNs-must-be-BLOCKs memory.

#### §2b: external calibration / precedent
#1 sed-i: macOS BSD `sed -i` without backup extension silently truncates files — confirmed by R19 data loss (4 agent findings sections, ~30min recovery). |source:[prompt-claim] R19 post-mortem / [independent-research] macOS sed behavior
#3 ΣVerify: H1 CONFIRMED via code read. sigma-verify machine.py confirms HATEOAS StateMachine: unconfigured (init + check_quotas) → ready (all tools). Spawned agent contexts receive MCP tool list once at connection — if init not called, machine stays unconfigured, verify_finding/cross_verify/challenge absent. State-gating by design, not a registry gap. |source:[independent-research] machine.py:17-128 + mcp_server.py:105-141
§2b outcome 2: effort calibrated to prior BLOCK additions (~20 LOC + 5 tests per block). No internal precedent for modifying spawned-agent MCP state — flagged as gap.

#### §2c: cost/complexity
BLOCK 3 (sed-i): ~20 LOC, reversal <1 day, pattern self-contained.
ΣVerify fix: spawn-prompt + agent-def = zero code cost, relies on agent compliance + A15 compensating gate.
§2c outcome 2: compliance reliance concern noted. Maintained because: bypassing HATEOAS state semantics is worse failure mode — future state-gated tools become unprotectable. |source:[agent-inference]

#### §2e: premise viability
ADR[1]: assumes regex catches all `sed -i` variant forms. GAP: `sed -i""` (no space), `sed\t-i`, multi-cmd chains. Test matrix required.
ADR[2]: assumes agents follow spawn-prompt instruction. GAP: agents may skip init. Compensating: A15 fires; DA-context XVERIFY covers load-bearing findings.
§2e outcome 3: sed-i regex coverage gap flagged — DA and code-quality-analyst to pressure-test. |source:[agent-inference]

---

#### H1 disposition: CONFIRMED
sigma-verify IS under user control at /Users/bjgilbert/Projects/sigma-verify/. machine.py:24 `gateway_name="init"` is the reason sub-tools don't appear in spawned agent contexts — intentional state-gating, not a registry bug. The correct architectural fix is hateoas-agent auto-init on connection (separate repo, follow-up). For THIS build: spawn-prompt instruction + agent-def update.

---

#### ADR[1]: #1 sed -i mechanical enforcement model |source:[independent-research]
decision: Add BLOCK 3 to phase-gate.py (PreToolUse, Bash) — block `sed -i` without backup extension on workspace-path commands
scope: paths matching `\.claude/teams/|workspace\.md` ONLY. NOT all Bash, NOT all .md globally.
hook-mechanism: PreToolUse + Bash. Regex: `sed\s+-i(?!\s+[\'\"\'])` AND path pattern in command.
bypass-allowlist: NONE. `sed -i ''` and `sed -i.bak` pass the regex.
alternatives: {(a) directive-only: REJECTED per WARNs-must-be-BLOCKs; (b) global sed ban: REJECTED — over-fires; (c) workspace file locking: REJECTED — separate scope}
prompted-by: Q1 / C4 (WARNs→BLOCKs) / R19 data loss
DB[sed-i-block]:
  (1) initial: block all `sed -i` globally
  (2) assume-wrong: breaks CI scripts, test runners, legitimate config sed in code projects
  (3) strongest-counter: scope to workspace path + allow backup-extension — surgical, same protection on actual attack surface
  (4) re-estimate: yes, scoped is correct. Global is over-broad.
  (5) reconciled: BLOCK on regex AND workspace path pattern. Edge-case test matrix required (PM[SS-1]).

---

#### STRIDE[1]: #3 ΣVerify tool inheritance threat model

ROOT CAUSE (confirmed via code read, machine.py + mcp_server.py):
HATEOAS StateMachine: gateway=init, states=unconfigured→ready. Sub-tools locked in ready. check_quotas from_states="*". Spawned sub-agent: independent MCP connection, NO state sharing with parent. init not called → unconfigured → sub-tools absent. Intentional.

TRUST BOUNDARIES:
- A: Claude Code agent → sigma-verify MCP: stdio, no auth, localhost
- B: sigma-verify → external providers: outbound HTTP, API-key-gated
- C: parent agent MCP session → spawned sub-agent: NO state sharing

STRIDE:
S (Spoofing): prompt-injected agent calls init to gain ready state? LOW. handle_init() reads env vars only. Gaining ready = XVERIFY = intended. No harm.
T (Tampering): agent fabricates XVERIFY results? MEDIUM. A15 checks presence not authenticity. Compensating: DA-context XVERIFY validates load-bearing findings. KNOWN GAP: A15 does not detect fabrication — documented, out of scope.
R (Repudiation): agents deny XVERIFY calls? LOW. No MCP call audit log. Compliance concern, not security.
I (Information Disclosure): init or tool pre-registration exposes API keys? NEGLIGIBLE. Keys in ~/.claude.json mcpServers env, server process memory only. init returns availability status only. |source:[independent-research] handlers.py
D (Denial of Service): runaway agent exhausts quotas via cross_verify? MEDIUM. No programmatic rate limiting. check_quotas advisory. Anthropic 1K RPM bounds frequency. Known gap, future enhancement.
E (Elevation of Privilege):
  Spawn-prompt init (THIS BUILD): NO new surface. Gaining ready = XVERIFY = intended.
  Bypass HATEOAS state (register all tools stateless): REJECT. Future state-gated write tools would be bypassable.
  hateoas-agent auto-init on connection: same security profile, architecturally cleaner, separate scope.

NEW ATTACK SURFACE: BLOCK 3 sed-i regex adds pattern-match in PreToolUse hot path. Risk: ReDoS. Mitigation: anchored regex, no catastrophic backtracking, test matrix. No new outbound connections, auth surfaces, or tool registrations from any proposed fix.

---

#### ADR[2]: #3 ΣVerify — recommended fix |source:[agent-inference]
decision: Spawn-prompt instruction + agent-def update — add `mcp__sigma-verify__init` call before ToolSearch for XVERIFY tools
alternatives: {(a) bypass HATEOAS state/register all tools stateless: REJECTED — EoP risk; (b) hateoas-agent auto-init: PREFERRED architecturally, out of scope — file as follow-up; (c) spawn-prompt THIS BUILD: zero code change, compliance-reliant, compensated by A15}
OPEN GAP: hateoas-agent auto-init. Medium priority, separate build.
prompted-by: Q1 / H1 (CONFIRMED) / STRIDE[1]

#### ADR[3]: #22/#23 audit-trail |source:[agent-inference]
decision: NO separate audit log. Workspace gate-log + chain-evaluator A-series + session archive (A12) = sufficient for current threat model.
rationale: internal agent errors, not external adversaries. Separate tamper-resistant log adds maintenance burden without commensurate benefit. Workspace Edit-tool-written (BLOCK 1 enforced), archived per A12.
follow-up: separate log if framework becomes multi-user or compliance-audited.
prompted-by: Q3 / C4

---

#### IC[1]: phase-gate ↔ Bash (sed-i BLOCK)
  event: PreToolUse | tool: Bash | input.command: str
  blocking-condition: `sed\s+-i(?!\s+[\'\"\'])` AND `\.claude/teams/|workspace\.md` in command
  exit-code: 2
  message: "SED-I BLOCKED: Use Edit tool for workspace edits, or 'sed -i .bak'/'sed -i \"\"' for backups. Prevents silent truncation (R19 incident)."
  bypass: none | security: NOT execute blocked cmd, NOT log content, return immediately

IC[2]: spawn-prompt ↔ sigma-verify init
  agent receives: instruction to call mcp__sigma-verify__init before ToolSearch for XVERIFY tools
  agent action: init → state: unconfigured → ready → sub-tools appear
  enforcement: A15 XVERIFY coverage check (downstream, not pre-flight)
  gap: NO pre-flight check — compliance-reliant
  compensating: DA-context XVERIFY; A15 surfaces gaps
  security: init returns availability status only — keys never in agent context (CONFIRMED)

IC[3]: chain-evaluator ↔ workspace gate-log (#22 + #23)
  #22: quantified claim without driver breakdown or CI → flag → gate-log entry
  #23: HIGH-severity finding without min-artifact → flag → gate-log entry
  archive: A12 archives full workspace including gate-log; HIGH-severity artifacts captured
  integrity: tamper = process violation surfaced by A16-A18 peer verification

---

#### SQ[] — security sub-tasks
SQ[SS-1]: BLOCK 3 in phase-gate.py — sed-i PreToolUse Bash, workspace-scoped |owner:implementation-engineer |est:1-2h |files:/Users/bjgilbert/.claude/hooks/phase-gate.py
SQ[SS-2]: Tests for BLOCK 3 — edge cases: bare BLOCK, .bak ALLOW, '' ALLOW, -n ALLOW, non-workspace ALLOW, multi-cmd BLOCK |owner:code-quality-analyst |est:1h |files:phase-gate test suite
SQ[SS-3]: Spawn templates + agent defs — ΣVerify init instruction before ToolSearch |owner:technical-writer |est:30min |files:sigma-lead spawn template + agent def files

#### RC[] — reference class
RC[phase-gate-block]: reference-class={BLOCK 1 + BLOCK 2 in phase-gate.py} |base-rate=~20 LOC + 5 tests per block |sample-size=2 |src:[independent-research] |confidence:H
RC[chain-evaluator-check]: reference-class={A-series additions} |base-rate=10-30 LOC + 3-8 tests per check |sample-size=5+ |src:[independent-research] |confidence:M

#### CAL[] — calibrated estimates
CAL[sed-i-block]: point=2h |80%=[1h,3h] |90%=[45min,5h] |breaks-if:{regex edge-case explosion; path-matching expansion needed}
CAL[sigmaverify-spawn-prompt]: point=30min |80%=[15min,45min] |90%=[10min,1.5h] |breaks-if:{spawn template location requires search}

#### PM[] — pre-mortem
PM[SS-1]: sed-i regex false-negative — `sed -i""` (no space), `sed\t-i`, multi-cmd evades; workspace truncated again |probability:15% |early-warning:{workspace.md becomes 0 bytes} |mitigation:{test all macOS sed forms; anchor pattern broadly}
PM[SS-2]: ΣVerify init prompt-injection surface — malicious external content exploits init |probability:5% |early-warning:{unexpected provider state during external-content sessions} |mitigation:{handle_init() takes NO params, reads only env vars — no injection surface; CONFIRMED by code read}
PM[SS-3]: Precision gate (#22) hollow compliance — agents add fake driver breakdowns |probability:20% |early-warning:{DA flags hollow breakdowns r4; gate-log spikes} |mitigation:{specific calibration criteria, not generic range-detection; CDS owns}

---

#### XVERIFY — ADR[1] (sed-i BLOCK) — COMPLETE
providers: openai/gpt-5.4 (PARTIAL/medium), llama/llama3.1:8b (AGREE/high), google/gemini-3.1-pro-preview (FAIL/503)

XVERIFY[openai:gpt-5.4]: PARTIAL — scoped approach is correct in principle. Regex mechanically too weak. Evasion forms: `sed -e 's/x/y/' -i file`, `env sed -i file`, `xargs sed -i`, variable expansion, unusual quoting/spacing all evade `sed\s+-i(?!\s+['"])` on raw command string. Stronger alternative: tokenize/parse argv (shlex.split or equivalent) to detect actual `-i` flag without attached extension, rather than raw string regex. |source:external-openai-gpt-5.4|
XVERIFY[llama:llama3.1:8b]: AGREE — targeted approach, backup-extension allow is correct. No counter-evidence surfaced. |source:external-llama-llama3.1:8b|
XVERIFY[google:gemini-3.1-pro-preview]: FAIL — 503 unavailable. |source:external-google-gemini-3.1-pro-preview| → verification-gap

XVERIFY verdict: PARTIAL — scoped approach and no-bypass rationale CONFIRMED. Regex implementation NEEDS REFINEMENT per openai. ADR[1] decision (scope + no-bypass) stands; IC[1] must be updated to specify argv parsing (shlex.split) not raw string regex. This is a consequence-bearing refinement — implementation-engineer must implement argv tokenization, not raw command string pattern match. llama agrees overall but did not probe the evasion forms that openai identified. Weight: openai PARTIAL > llama AGREE on implementation-specific concern (llama 8b local model; openai more architecturally probing).

ADR[1] REFINED post-XVERIFY:
  decision: unchanged (scope: workspace paths, bypass: none, hook: PreToolUse Bash)
  implementation refinement: use shlex.split() to tokenize command, detect `-i` flag without attached extension in argv, AND path pattern in command. NOT raw regex on command string. Evasion via quoting/spacing/env wrappers is blocked by argv tokenization.
  new IC[1] mechanism: `args = shlex.split(command); 'sed' in args AND '-i' in args AND next_arg_after_i_is_not_extension(args) AND workspace_path_in_command(command)`
  risk of remaining evasion: `env sed -i file` would appear as argv [env, sed, -i, file] — 'sed' detection must handle this; `xargs sed -i` similarly. Flag to implementation-engineer: must test env/xargs wrapping forms.

XVERIFY-FAIL gap: google 503. 2 providers succeeded (1 partial, 1 agree). Per R19 DA-XVERIFY pattern: 2 architecturally distinct providers sufficient for non-catastrophic security decisions. PARTIAL from high-quality model (openai) is the signal — acted on.


### cognitive-decision-scientist
## CDS plan: protocol-layer gates #21-#24 | 2026-04-23

### §2a positioning
#21-#24 address output-quality gaps at different §2 hygiene layers.
→ Outcome 2: ACH (Heuer 1999), SACD (arxiv:2504.04141), distributed-cognition taxonomy (PMC 2025) confirm premise-testing and precision gates as recognized techniques. None in sigma-review §2. Gap real. Directive-only = no lock-in. |source:[independent-research:T1] |§2a: academic consensus + sigma-review gap — MAINTAINED

### §2b calibration
→ Outcome 2: R19 eval B/3.14 — calibration(3/4)+accuracy(3/4) failed on false-precision: 4 distinct failures (F[TA-C2] withdrawn, F[TA-A2] driver gap, H2 no CI, PM unstructured). F[CDS-A1]+F[CDS-B1] HIGH-severity governance, 0 artifacts, Actionability 3/4. Prior §2g: genuine revision ~40-50% applications. Similar challenge for §2i expected. |source:[cross-agent:R19-evaluator-feedback] |§2b: evidence sufficient; calibration needs empirical tuning — MAINTAINED risk noted

### §2c cost & complexity
→ Outcome 2: all 4 directive-only. Chain-evaluator = separate cost (SQ[CDS-6/7]). #21: 5-10 min lead. #22: 10-15% per-agent overhead. #23: conditional HIGH-severity governance only (~20-30 min/applicable). #24: marginal inline tag. Highest maintenance risk: #22 miscalibration. Mitigated by CONDITION 1 AND 2 conjunction (binary). |source:[agent-inference] |§2c: maintained — cost proportional to finding density

### §2e premise viability
P1: R19 failures systematic → HIGH confidence TRUE | P2: premise-anchoring occurs pre-spawn → CONFIRMED | P3: chain-evaluator text-pattern enforcement → UNCERTAIN; mitigation: WARN first | P4: governance findings have identifiable artifact standard → Sherman Kent+SATs confirm → CONFIRMED T1
→ Outcome 2: P1+P2+P4 supported; P3 uncertain → mitigation in ADR[2]. MAINTAINED.

---

### ADR[1]: #21 Premise-Audit Architecture — H3 SUPPORTED with sequence constraint

**Decision:** #21 = LEAD WORKFLOW STEP, new Step 8.5 between Steps 8 and 9 (answers OQ-TW3). NOT new agent role, NOT DA framework extension.

Evidence FOR H3: frame-anchoring at prompt-decomposition layer (§7), not agent-analysis layer. Lead already owns §7 pre-spawn. R19 evaluator: premises "accepted as frame" before H[] dispatch. Cost: 5-10 min, no new agent.
Evidence AGAINST alternatives: DA fires AFTER research (timing mismatch; redundant post-fact). New agent = out-of-scope per C1.

§2g DB[H3]: (1) initial: workflow step sufficient (2) assume-wrong: lead reads prompt before PA[1-4] → anchoring already occurred → same contamination (3) strongest counter: 50% lead-authored audit is genuinely independent (4) re-estimate: FORMAT-level structure (PA[1-4] as independent structured questions) transfers 70-85% per CDS-memory R[format-cognitive-REVISED] (5) reconciled: REVISION — lead answers PA[1-4] BEFORE re-reading user's H-space. Sequence is the anti-anchoring mechanism. Implementation must specify this explicitly.

Implementation spec (Step 8.5):
```
### §2p premise-audit pre-dispatch (26.4.23)
!when: STEP 8.5 — AFTER prompt-decomposition §7, BEFORE H-level agent spawn
!sequence: answer PA[1-4] INDEPENDENTLY before reviewing user's proposed H-space (order critical)
!applies-to: ANALYZE | BUILD: covered by §7a
!workspace: write PREMISE-AUDIT[pre-dispatch] to ## prompt-decomposition

4 structural premise tests (structural ¬domain-depth):
  PA[1]: tier-necessity — is proposed tier/framework NECESSARY or is simpler structure adequate?
  PA[2]: firm-size-floor — minimum viable org? (state explicitly)
  PA[3]: data-readiness — what data must exist for findings to be actionable? (gap? yes/no)
  PA[4]: adoption-baseline — RC[{class}]={rate} | above/at/below base-rate?

!format:
  PREMISE-AUDIT[pre-dispatch]:
  PA[1]: tier-necessity: {CONFIRMED|CHALLENGED|GAP} — {one sentence}
  PA[2]: firm-size-floor: {minimum-org} | {assumption}
  PA[3]: data-readiness: {preconditions} | gap:{yes/no}
  PA[4]: adoption-baseline: RC[{class}]={rate} | above/at/below base-rate
  → proceed-with-H|revise-H-space({N})|flag-premise({N})

!rules:
  - CHALLENGED/GAP PA[1] or PA[2] → revise H-space before dispatch
  - CHALLENGED PA[3] or PA[4] → convert to explicit H[] for agents to test
  - DA receives PREMISE-AUDIT in r2: checks agents ¬re-anchored on challenged premises
  - scope: STRUCTURAL premises ¬domain-depth (domain → §2e+DA)
```

Cognitive science: Kahneman (2011) anchoring. Mercier & Sperber: agents defend H[] ¬test premises. Klein (1998) pre-mortem. FORMAT-level transfer 70-85%. |source:[independent-research:T1] |prompted-by:Q3,H3

---

### ADR[2]: #22 §2i Precision Gate — H2 PARTIALLY CONFIRMED (REVISED POST-XVERIFY)

§2g DB[ADR[2]] (self-referential — precision gate applied to this ADR):
(1) initial: 4-condition conjunction threshold calibrated correctly
(2) assume-wrong: "load-bearing" subjective → agent-discretionary override → degrades to checkbox
(3) strongest counter: 60% probability subjective threshold degrades within 3 reviews
(4) re-estimate: threshold must be binary and observable
(5) reconciled: REVISION — replace subjective "load-bearing" with binary observable criteria (initial revision — see XVERIFY below for further revision).

XVERIFY results — applied to initial DB[]-revised threshold:
- XVERIFY[openai:gpt-5.4]: partial — "gate keyed only to point estimates appears too narrow; range without support (0.55-1.1 FTE, $200K-$2M) would evade it. Better: fire when quantitative claim is load-bearing AND lacks uncertainty justification" |source:external-openai-gpt-5.4|
- XVERIFY-FAIL[google:gemini-3.1-pro-preview]: 503 UNAVAILABLE |→ verification-gap
- XVERIFY[deepseek:deepseek-v3.2:cloud]: disagree — "requires point estimate without range to fire, but R19 failures show unsupported ranges are equally problematic; gate would miss most R19 failures" |source:external-deepseek-deepseek-v3.2:cloud|
XVERIFY verdict: 2/2 available providers surfaced same calibration gap — Outcome 1 (check changes analysis).

Second revision from XVERIFY — replaces "point estimate without range" with "quantitative claim without uncertainty justification":

Gate fires when BOTH conditions met:
- CONDITION 1 (quantitative claim without uncertainty justification): any numeric claim (point estimate OR range) that lacks at least one of: (a) explicit driver breakdown showing derivation, (b) CI or reference class cited, (c) explicit qualitative qualifier ("order-of-magnitude", "illustrative", "approximately")
- CONDITION 2 (load-bearing, binary, ANY one): (i) >70% confidence tag OR (ii) HIGH-severity tag OR (iii) cited in primary recommendation/conclusion

If BOTH fire → agent must produce ONE of: (a) Driver breakdown: "derives from: [C1: X%] + [C2: Y%]..." | (b) CI+RC: "80% CI [lo, hi] based on RC[{class}]={rate}" | (c) Qualitative restatement: "approximately [magnitude], precise estimate ¬supportable"

XVERIFY calibration test against all 4 R19 failures: F[TA-C2] range 0.55-1.1 FTE (no driver breakdown → CONDITION 1; HIGH-severity → CONDITION 2) ✓ | F[TA-A2] $200K-$2M (no driver breakdown → CONDITION 1; primary recommendation → CONDITION 2) ✓ | H2 10-13mo (no CI/RC → CONDITION 1; load-bearing forecast → CONDITION 2) ✓ | PM 35/20/25% (no Bayesian/RC → CONDITION 1; cited in synthesis → CONDITION 2) ✓ — all 4 R19 failures now trigger.

Over-fire prevention (per C5 — defend each invocation, ¬create exceptions): explicit qualitative qualifier satisfies CONDITION 1 → no fire | deterministic code findings → CONDITION 2 won't trigger → no fire | "order-of-magnitude"/"illustrative" stated → CONDITION 1 satisfied → no fire.

H2 test result: PARTIALLY CONFIRMED post-XVERIFY second revision. Revised threshold is broader and more accurate than DB[]-only revision. False-positive risk first 2-3 reviews: 20-30% (higher than initial estimate — CONDITION 1 now broader). Start WARN → BLOCK after 3-review calibration data (SQ[CDS-6]). NOT exception-handling per C5.

Chain-evaluator enforcement (answers OQ-TW2): recommend check ID A20 (TA confirm no collision). Detection: numeric pattern + CONDITION 2 marker + absence of uncertainty qualifier. Implementation note: "without uncertainty justification" harder to detect via regex than "without range" — chain-evaluator may need conservative trigger (numeric + CONDITION 2 marker → flag; DA adjudicates CONDITION 1). DA compensating control is load-bearing for this check.

Cognitive science: Tetlock (2005) — estimates without ranges systematically overconfident; applies equally to unsupported ranges. Heuer (1999) decomposition surfaces hidden assumptions regardless of point/range form. ECE 0.12-0.40 systematic (CDS-memory R[LLM-calibration]). Precision gate improves RESOLUTION (3/4→4/4 Calibration). |source:[independent-research:T1] |prompted-by:Q3,H2,C5

---

### ADR[3]: #23 HIGH-Severity Governance Minimum Artifact

Decision: HIGH-severity + governance/compliance finding MUST include minimum artifact OR "ARTIFACT-GAP: [reason]."

Minimum artifact taxonomy (agent chooses one):
- TIER-A: Template stub — fill-in-blank structure for recommended gate artifact
- TIER-B: Decision tree — binary branching logic operationalizing governance control
- TIER-C: Specimen artifact — completed example for context (most actionable)

Calibration: R19 F[CDS-A1]+F[CDS-B1] Actionability 3/4 because "stopped at gap-ID without templates/crosswalks/decision-trees." Sherman Kent+SATs: receiver must act without further consultation. Gap-ID alone fails. TIER-A = minimum viable. ~20-30 min.

§2g DB[ADR[3]]: (1) TIER-A stub sufficient (2) assume-wrong: stubs gameable — 3-field placeholder satisfies letter (3) 45% stubs substantive without DA quality check (4) format alone insufficient (5) reconciled: gate = TIER + DA exit-gate quality check. DA: "ARTIFACT-REVIEW[{finding}]: TIER-{A/B/C} |quality:{substantive|nominal} |→ accept|revise"

§2a: standard in advisory/intelligence contexts (McKinsey governance, SATs). Conservative addition. Scope (anti-gold-plating): HIGH-severity + governance/compliance ONLY (committee structure, approval process, oversight role, compliance requirement, audit function). |source:[independent-research:T2]

Cognitive science: Zeigarnik (1927) completion bias — gap-ID creates false closure. Speier et al. (2003, MIS Quarterly): recommendations without artifacts adopted 30-40% lower. CLT: DA quality check = binary vs holistic judgment (lower extraneous load). |source:[independent-research:T1/T2] |prompted-by:Q3

---

### ADR[4]: #24 §2d Severity Provenance Pattern

Decision: Extend §2d with mandatory severity-basis sub-tag when severity is extrapolated from different domain/context/population.

Extrapolation-tag format (3 required fields):
```
|severity-basis:[extrapolation:{from-context}→{to-context} |assumption:{transfer-claim} |confidence-delta:{source-tier}→{extrapolation-tier}]
```
R19 example: |severity-basis:[extrapolation:SR-11-7-exam-findings→AI-agent-review-context |assumption:SR exam failure rates transfer to AI-agent error rates in comparable review scope |confidence-delta:T1→agent-inference]

§2d extension (new sub-section after §2d+):
```
#### §2d-severity provenance (26.4.23)
!applies-to: severity (LOW/MEDIUM/HIGH/CRITICAL) from: different-sector regulatory doc | different-population base rate | analogical cross-technology reasoning
!rule: severity by extrapolation MUST carry severity-basis tag alongside source tag
!consequence: severity-basis:extrapolation → DA challenge r2 for HIGH+ ratings
  DA: "severity extrapolated {from}→{to}. State assumption making transfer valid. Evidence disconfirming transfer?"
!note: finding-claim provenance and severity-provenance SEPARABLE — track independently
!when ¬applies: severity from document being reviewed OR primary source covering exact domain → standard §2d
```

§2a (Outcome 1 — CHECK CHANGES ANALYSIS): distinguishing finding-provenance from severity-provenance is NOT standard in structured analytic frameworks — genuine extension, not codification. Higher-risk addition (less validated). Start WARN → BLOCK after 3 reviews. |source:[independent-research:T1] |§2a: revised to "genuine extension" — risk acknowledged

§2g DB[ADR[4]]: (1) 3-field tag sufficient (2) assume-wrong: agents conflate finding-provenance with severity-provenance (3) 55% correct first-try without DA explicit check (4) format tag alone insufficient (5) reconciled: DA directive must include explicit audit — absent |severity-basis| + cross-domain pattern = process violation.

Cognitive science: EEVF (Bielik 2025, CDS-memory R[epistemic-vigilance]): epistemic pathway must be tracked; severity extrapolation = unchecked step. Stable beliefs (CDS-memory R[metacognition]) vulnerable to anchoring. ECE systematic overconfidence compounded by severity extrapolation (CDS-memory R[LLM-calibration]). |source:[independent-research:T1] |prompted-by:Q3

---

### SQ[] (CDS scope)
SQ[CDS-1]: §2p premise-audit directive for directives.md |owner:technical-writer |dependency:ADR[1] |answers:OQ-TW3(Step 8.5)
SQ[CDS-2]: §2i precision gate directive for directives.md |owner:technical-writer |dependency:ADR[2] |chain-eval-ID:A20(TA-confirm)
SQ[CDS-3]: §2d-severity provenance sub-section |owner:technical-writer |dependency:ADR[4]
SQ[CDS-4]: Governance min-artifact TIER taxonomy + DA exit-gate quality check |owner:technical-writer |dependency:ADR[3]
SQ[CDS-5]: c1-plan.md Step 8→8.5 + ## premise-audit-results section in workspace template |owner:technical-writer |dependency:ADR[1]
SQ[CDS-6]: chain-evaluator.py A20 §2i precision check — WARN; 3-review calibration gate before BLOCK |owner:implementation-engineer |dependency:ADR[2]+H5
SQ[CDS-7]: chain-evaluator.py HIGH-severity governance artifact detection — WARN initially |owner:implementation-engineer |dependency:ADR[3]+H5
SQ[CDS-8]: Agent _template.md severity-provenance tag format addition |owner:technical-writer |dependency:ADR[4]

### RC[]
RC[analytical-gate-adoption]: ref=new §2 gates sigma-review |base-rate=3/3 prior (§2d,§2g,§2h) required 2-4 reviews calibration |N=3 |src:[cross-agent] |confidence:M
RC[precision-gate-false-positive]: ref=quantification-discipline QA gates |base-rate=30-40% false-positive initial CIA SAT training |N=5-10 |src:[independent-research:T2] |confidence:M
RC[governance-artifact-adoption]: ref=minimum artifact advisory |base-rate=80%+ compliance with DA-check vs 40-50% without |N=low |src:[independent-research:T2] |confidence:L-M

### CAL[]
CAL[#21 premise-audit catch-rate]: point=70% |80%=[55%,82%] |90%=[45%,88%] |breaks-if: lead anchored before PA[1-4] OR premises domain-embedded |src:[agent-inference+CDS-memory R[format-cognitive]]
CAL[#22 false-positive first 3 reviews]: point=25% |80%=[15%,40%] |90%=[10%,50%] |breaks-if: CONDITION 2 parsed too broadly |src:[RC[precision-gate-false-positive]+agent-inference]
CAL[#23 artifact quality first 3 reviews]: point=55% substantive |80%=[40%,70%] |90%=[30%,78%] |breaks-if: DA quality check not enforced |src:[RC[governance-artifact]+agent-inference]
CAL[#24 severity-provenance correct first 3 reviews]: point=55% |80%=[40%,72%] |90%=[30%,80%] |breaks-if: agents conflate finding+severity provenance |src:[agent-inference]

### PM[]
PM[CDS-1]: §2i precision gate degrades to checkbox |likelihood:35% |early-warning: DA "§2i check perfunctory" r2; 1-line breakdowns |mitigation: DA challenge "breakdown 1 component, estimate still unexplained" per existing §2 DA challenge template
PM[CDS-2]: premise-audit revised H-space but agents re-anchor |likelihood:25% |early-warning: DA prompt-audit r2 finds PA CHALLENGED but no workspace revision |mitigation: PREMISE-AUDIT "→ proceed|revise|flag" declaration; DA checks declared decision vs what agents received
PM[CDS-3]: governance min-artifact drives severity downgrading |likelihood:20% |early-warning: severity distribution shifts toward MEDIUM in governance-adjacent |mitigation: DA calibrates severity independently; flags distribution shift as gate-avoidance
PM[CDS-4]: #22 WARN→BLOCK delayed indefinitely |likelihood:30% |early-warning: WARN state 3+ reviews without calibration checkpoint |mitigation: SQ[CDS-6] includes explicit 3-review calibration decision gate |src:[feedback_warns-must-be-blocks.md]

OQ-TW2 answered: chain-eval check ID A20 recommended. TA confirm no collision.
OQ-TW3 answered: new Step 8.5 between Steps 8 and 9. Separate from Step 8 (different operation).
OQ-CDS1 (scope flag): ADR[1] does NOT include hook-enforcement of #21 — directive+spawn-template only. If mechanical enforcement desired, separate SQ needed. DA to challenge if this creates under-built gate.

## CDS convergence: ✓ COMPLETE 2026-04-23 | updated 26.4.23 post-BC responses

ADR[1]: SUPPORTED (H3) — revised to Step 7a (concede DIV[2] to TA), sequence constraint retained | ADR[2]: REVISED post-XVERIFY (broader CONDITION 1) | ADR[3]: complete with DA quality-check requirement | ADR[4]: complete with DA explicit-audit requirement
XVERIFY: openai:gpt-5.4 partial + deepseek:deepseek-v3.2:cloud disagree — CONDITION 1 calibration gap surfaced. Outcome 1 revision applied. google XVERIFY-FAIL(503).
SQ[CDS-1]-[CDS-8]: defined | SQ[CDS-5] revised (Step 7a, dedup with TA SQ[9]) | SQ[CDS-6] test scope revised (~6-8 tests)
RC[]+CAL[]+PM[]: min 3+ entries each, all populated

## CDS Step 22 BC responses

BC[TW-#5] §2p/§2i naming — CONCEDE: TW correct.
§2i = precision gate (sequential from §2h). §2p = premise-audit (non-sequential, signals pre-dispatch). Naming was already consistent with TW recommendation as written. No content change required — confirmed correct.

BC[CQA-#5] A20 CONDITION 1 detection mode — DEFEND with clarification.
Code detects CONDITION 2 (>70% confidence tag OR HIGH-severity tag OR primary-recommendation marker — all text patterns chain-evaluator already parses). CONDITION 1 suppression: keyword heuristic — presence of uncertainty qualifier (driver breakdown keywords, CI notation, "order-of-magnitude"/"illustrative"/"approximately") suppresses WARN flag. Code-detectable, not full semantic parsing. DA adjudicates edge cases.
Revised SQ[CDS-6] spec: A20 = CONDITION 2 detection (code) + uncertainty qualifier suppression (keyword heuristic) → WARN.
Revised SQ[CDS-6] test scope: ~6-8 tests. 3-4 unit (CONDITION 2 correct; numeric+no qualifier→flag; numeric+qualifier→no flag; no numeric→no flag) + 2-3 calibration against known R19 cases (F[TA-A2] $200K-$2M should flag; explicit CI should not). NOT 8-10 full archive calibration. CQA SQ[13d] = 6-8 tests.

DIV[2] Step 8.5 vs TA Step 7a — CONCEDE to TA.
TA correct: premise-audit is §7 prompt-decomposition operation — reads and tests premises from prompt before framing H[]. Step 7a is right position. CDS mislabeled it Step 8.5 while description correctly placed it pre-H-space. Sequence constraint retained as implementation sub-requirement within Step 7a — not a separate positioning decision.
SQ[CDS-5] revised: align with TA SQ[9] (Step 7a). If SQ[9] and SQ[CDS-5] cover same file change → TW to confirm merge/dedup in C2.
DIV[2] verdict: TA Step 7a. CDS sequence constraint preserved as sub-requirement of Step 7a spec.

## CDS convergence: ✓ FINAL 26.4.23 | r2 DA responses added 26.4.23
BC responses complete. DIV[2] resolved (concede to TA). §2p/§2i naming confirmed. SQ[CDS-5] Step 7a. SQ[CDS-6] revised (scoped-defer). DB[ADR[2]] rerun with net-negative-ROI counter.

## CDS DA r1 responses

DA[#3] DIV[2] — already conceded to TA Step 7a in prior BC round. DA addendum confirms ACCEPTED. No further action.

DA[#5] §2i chain-evaluator enforcement — CONCEDE: DA correct, triple-convergence (IE+CQA+DA) confirmed.
The "DA adjudicates CONDITION 1" architecture is incoherent as designed: chain-evaluator A-checks return pass/fail/issues with no defer-to-DA state, and DA runs pre-Stop-hook while chain-evaluator runs at Stop. I designed an enforcement path that cannot mechanically exist.
Revised SQ[CDS-6]: A20 implementation = CONDITION 2 detection only (code: >70% confidence tag OR HIGH-severity tag OR primary-recommendation marker) → WARN when fired. CONDITION 1 ("without uncertainty justification") detection is explicitly DEFERRED — labeled in code comment as "CONDITION 1 deferred: keyword heuristic insufficient; calibration build required after 3-review evidence." This is honest scoping, not failure.
Consequence for ADR[2]: CONDITION 1 remains in the DIRECTIVE (agents must comply) but chain-evaluator does NOT enforce CONDITION 1 at plan-lock. DA enforces CONDITION 1 in r2 challenge rounds via existing "§2i check perfunctory" DA challenge format. C4/C5 tension (DA[#10]): the CONDITION 2 WARN-only satisfies C4 for what the code CAN detect; CONDITION 1 deferral is explicit, not indefinite — requires user decision pre-C2 per DA[#10].
SQ[CDS-6] test scope revised down: ~4-5 tests (CONDITION 2 detection only: positive case, negative case, no-numeric no-fire, deterministic-finding no-fire; one R19 calibration test against known CONDITION 2 marker). CQA SQ[13d] = 4-5 tests.

DA[#8] DB[ADR[2]] rerun — running with "net-negative-ROI" counter now absent in prior DB[]:

DB[ADR[2]-r2]:
(1) initial: §2i precision gate with dual-condition threshold improves Calibration + Accuracy scores toward 4/4
(2) assume-wrong: precision gate is NET NEGATIVE — R19 eval B/3.14 strong on non-§2i items; expected catch rate 70% (CAL) vs false-positive 25% first 3 reviews; DA already caught F[TA-C2] in R19 without any gate; adding infrastructure for uncertain benefit while introducing maintenance burden and WARN→BLOCK calibration debt
(3) strongest counter for net-negative: R19 DA caught the R19 false-precision WITHOUT §2i. If DA is already the effective enforcement mechanism, §2i is redundant infrastructure. The 4 false-precision failures were caught and withdrawn in-session. Score was 3/4 not 2/4 — the system worked. Incremental benefit of §2i over current DA-enforcement is the marginal case where DA MISSES a false-precision claim. Reference: DA catch rate in R19 on this class of issue = 100% (4/4 flagged). If DA catch rate is reliably high, gate marginal value ≈ (1 - DA_catch_rate) × benefit = low.
(4) re-estimate: I initially assumed 70% effective catch rate for §2i. Against "DA already catches these": the real question is whether DA will CONTINUE catching at 100% across sessions where DA has different context, different agents, different domain. Historical catch rate across 3 reviewed sessions: TA R16 (no false-precision flagged — DA missed or domain had none), R17-R18 (no record in CDS memory). R19 only. Single-session 100% is not a reliable base rate. Pre-mortem probability that DA misses false-precision in future session: 30-40% given context variability. Expected sessions before false-precision recurs without §2i: ~3-5. With §2i directive (no chain-eval enforcement): reduces false-precision recurrence via agent compliance with directive, estimated 50-60% compliance rate. With §2i chain-eval CONDITION 2 enforcement: adds mechanical catch for CONDITION 2 cases specifically.
(5) reconciled: net-negative-ROI counter is PARTIALLY VALID — for the full-semantic CONDITION 1 detection (which is now deferred per DA[#5] concession), the gate infrastructure may not be worth the calibration burden. HOWEVER, the CONDITION 2 detection in code is cheap (text regex, ~20 LOC) and catches the structural load-bearing cases (HIGH-severity, >70% confidence tags, primary-recommendation markers). For CONDITION 2 only, the ROI is positive: catches cases where agent explicitly signals high conviction but provides no uncertainty structure. DA would also catch these, but mechanical detection is faster and consistent across sessions. Revised position: §2i CONDITION 2 code enforcement is net-positive (low cost, reliable signal). CONDITION 1 directive-only with DA enforcement is net-neutral (appropriate given current evidence base). Combined: §2i as designed post-DA[#5] concession is net-positive overall. Net-negative-ROI counter addressed and rejected for the scoped implementation. Would be valid if the full dual-condition gate were proposed (too much infrastructure for uncertain benefit) — but that version is now deferred.
|source:[agent-inference + R19-evaluator-feedback:cross-agent] |DB[ADR[2]-r2] outcome: maintain §2i with CONDITION 2 enforcement only; CONDITION 1 directive + DA only. Net-negative-ROI counter addressed, not conceded.

## CDS convergence: ✓ LOCKED post-DA-r1 26.4.23 | path β+ expansion 26.4.23
DA[#3]: ACCEPTED (Step 7a — already conceded)
DA[#5]: CONCEDE — SQ[CDS-6] revised to CONDITION 2-only code enforcement; CONDITION 1 deferred with explicit label
DA[#8]: DEFEND — DB[ADR[2]-r2] with net-negative-ROI counter: partially valid for full dual-condition gate (now deferred); not valid for scoped CONDITION 2-only implementation. §2i maintained.
DA[#10]: RESOLVED — user selected path β+ (WARN-first + empirical audit tracking). See path β+ design below.

## CDS path β+ design: audit-monitored calibration gate

### ADR[β+]: calibration-data emission + audit-calibration-gate

**Decision:** Each WARN-firing gate (#22 §2i, #23 governance, #24 severity) emits a structured calibration record to a persistent calibration log. The audit-calibration-gate reads this log and gates BLOCK-promotion. Promotion trigger is data-driven (N fires + DA verdicts), not self-reported.

**Calibration data schema (emitted per WARN firing):**
```
CAL-EMIT[{gate-id}]: review-id:{session-date-slug} |finding-ref:{F[agent-finding-id]} |fire-reason:{CONDITION-2-marker-matched} |workspace-context:{agent}:{finding-text-excerpt-50-chars} |da-verdict:PENDING
```
After DA r2 completes, DA appends verdict to each CAL-EMIT:
```
CAL-EMIT[{gate-id}]: ... |da-verdict:{legitimate|false-positive|not-reviewed}
```
- `legitimate`: DA confirms agent had insufficient uncertainty justification — WARN was correct
- `false-positive`: DA confirms agent had adequate justification; gate misfired
- `not-reviewed`: DA did not examine this specific firing in r2

**Persistence location:** `~/.claude/teams/sigma-review/shared/calibration-log.md` — append-only, one entry per WARN firing, survives across sessions. Rationale: sigma-mem team memory has write-contention risk (R19 #7); archive index is read-only post-session; a dedicated calibration-log file is simple, auditable, and writable by chain-evaluator. TW adds calibration-log to archive checklist in §8.

**Promotion thresholds (CDS-designed, DA to challenge if over/under-calibrated):**
- §2i (precision gate CONDITION 2): promote WARN→BLOCK when: ≥3 distinct reviews with fires AND ≤20% false-positive rate across all fires with DA verdicts. Minimum 5 DA-verdicted fires (not-reviewed counts as missing data, not as legitimate). Rationale: 20% FP threshold = C5-compatible defense ("80%+ hit rate = each invocation defensible on average"). If FP rate >20% after 3 reviews → gate recalibration required (not promotion to BLOCK).
- #23 governance min-artifact: same threshold (≥3 reviews, ≤20% FP, ≥5 DA-verdicted) but fires expected to be rarer (conditional on HIGH-severity + governance domain). May require 5-6 reviews to accumulate.
- #24 severity provenance: same threshold. Fires rarest (only on extrapolated severity). Calibration window may extend to 6+ reviews.
- #21 premise-audit: BLOCK from day one. No calibration window. Presence check is binary — either ## premise-audit-results section is present in workspace or it is not. No false-positive path for a presence check.

**Audit-calibration-gate mechanics (new SQ — CDS designs, IE implements, TW directives):**
The audit-calibration-gate is NOT a chain-evaluator A-check (chain-evaluator runs per-session). It is a standalone script or sigma-audit extension that:
1. Reads calibration-log.md → filters by gate-id
2. Counts: total fires, DA-verdicted fires (legitimate + false-positive), not-reviewed, FP rate
3. If promotion threshold met → outputs "PROMOTE: {gate-id} WARN→BLOCK" + evidence summary
4. If FP rate >20% → outputs "RECALIBRATE: {gate-id} — FP rate {N}% exceeds threshold"
5. If insufficient data → outputs "CALIBRATING: {gate-id} — {N} reviews, {M} DA-verdicted fires; need ≥5"
The gate is RUN by lead at start of each sigma-review session or by sigma-audit post-session. It is advisory — lead must act on PROMOTE signal to update chain-evaluator mode from WARN to BLOCK. This keeps BLOCK-promotion as a deliberate lead decision, not an automatic code change. Anti-PM[CDS-4]-pattern: the gate FORCES the decision to surface rather than deferring indefinitely.

**§2i CONDITION 1 calibration path (separate track):**
CONDITION 1 (any numeric claim without uncertainty justification) is deferred per DA[#5]. When enough CONDITION 2 data accumulates (3+ reviews), CDS proposes revisiting CONDITION 1 calibration using the same pattern: implement as WARN in a separate calibration build, track fires+DA-verdicts, promote to BLOCK after threshold. This is NOT in scope for this build — it is the planned follow-up.

**SQ revisions and additions:**

SQ[CDS-6] REVISED: chain-evaluator A20 §2i CONDITION 2 WARN — adds calibration-data emission
|file: chain-evaluator.py |change: check fires → append CAL-EMIT record to calibration-log.md with review-id+finding-ref+fire-reason+workspace-context; da-verdict field populated PENDING |owner: implementation-engineer |dependency: ADR[2] locked + calibration-log.md schema (this ADR) |test-scope: 4-5 unit tests (CONDITION 2 detection) + 1 integration test (CAL-EMIT record written correctly to log)

SQ[CDS-7] REVISED: chain-evaluator #23 governance artifact WARN — adds calibration-data emission
|file: chain-evaluator.py |change: same CAL-EMIT pattern for HIGH-severity+governance detection |owner: implementation-engineer |dependency: ADR[3] locked

SQ[CDS-8] REVISED: chain-evaluator #24 severity provenance WARN — adds calibration-data emission
|note: #24 is currently directive-only with no chain-evaluator check in this build (ADR[4]: §2a outcome 1, genuine extension, start WARN). With path β+ the WARN must be in code to emit CAL-EMIT records. This promotes #24 from directive-only to requiring a chain-evaluator detection stub. |file: chain-evaluator.py |change: add check_a24_severity_provenance() — detects HIGH/CRITICAL severity rating in finding + fires WARN + CAL-EMIT |owner: implementation-engineer |new scope: adds ~15-20 LOC + 2-3 tests

SQ[CDS-9] NEW: calibration-log.md initialization + schema
|file: ~/.claude/teams/sigma-review/shared/calibration-log.md |change: create with header + schema documentation |owner: technical-writer |est: 30min |dependency: ADR[β+] schema

SQ[CDS-10] NEW: audit-calibration-gate script
|file: ~/.claude/teams/sigma-review/shared/audit-calibration-gate.py |change: standalone script reads calibration-log.md, evaluates promotion thresholds, outputs PROMOTE/RECALIBRATE/CALIBRATING per gate |owner: implementation-engineer |est: 2h |dependency: calibration-log.md schema + SQ[CDS-6/7/8] emission format |note: NOT a chain-evaluator A-check; standalone run by lead or sigma-audit

SQ[CDS-11] NEW: directive text for §2i calibration path
|file: directives.md §2i |change: add explicit calibration-path text — "§2i fires WARN until audit-calibration-gate outputs PROMOTE signal after ≥3 reviews with ≤20% FP rate; lead updates chain-evaluator mode on PROMOTE" |owner: technical-writer |dependency: ADR[β+]

SQ[CDS-12] NEW: DA r2 protocol extension for CAL-EMIT verdict
|file: directives.md DA enforcement section |change: DA exit-gate format extended to include verdict on CAL-EMIT records — "for each CAL-EMIT[PENDING] in workspace: da-verdict:{legitimate|false-positive|not-reviewed}" |owner: technical-writer |dependency: ADR[β+]

**§2e premise viability check on ADR[β+]:**
P1: DA will consistently provide verdicts on WARN fires → UNCERTAIN. DA may not examine every WARN fire if session has many findings. Mitigation: SQ[CDS-12] makes DA verdict on CAL-EMIT an explicit exit-gate requirement, not optional. P2: calibration-log.md survives across sessions without corruption → MODERATE confidence. Append-only text file is safe; risk is if sigma-system-overview repo is on a device that loses the file. Mitigation: calibration-log.md added to backup-memory.sh script per session-end checklist. P3: lead will run audit-calibration-gate before BLOCK-promotion decision → same failure mode as any directive. Mitigation: sigma-audit runs audit-calibration-gate automatically as part of post-session audit. This makes the calibration check part of the audit pipeline, not a separate lead action.

**§2a positioning on ADR[β+]:**
→ Outcome 2: audit-monitored calibration windows are not standard in analytical frameworks (most promote gates by judgment or never promote). This is a genuine infrastructure addition. Similar to how sigma-review's log-score tracking is novel (not standard in human advisory). Cost: ~4h IE (SQ[CDS-10] + modifications to SQ[CDS-6/7/8]) + ~1h TW (SQ[CDS-9/11/12]). Maintained: the alternative (self-reported 3-review window) has same failure mode as directives — confirmed by user rationale. Empirical tracking is correctly identified as the only C5-compatible path through C4. |source:[agent-inference + user-decision]

## CDS convergence: ✓ FINAL post-path-β+ 26.4.23
SQ[CDS-6/7/8] revised to include CAL-EMIT emission.
SQ[CDS-9/10/11/12] new — calibration-log + audit-gate + directive text + DA verdict protocol.
#24 severity provenance promoted from directive-only to WARN+code-detection stub (needed for CAL-EMIT).
#21 premise-audit: BLOCK from day one, binary presence check, no calibration window — confirmed.
Promotion thresholds: ≥3 reviews, ≤20% FP rate (DA-verdicted), ≥5 DA-verdicted fires.
Audit-calibration-gate: standalone script, not chain-evaluator A-check, advisory with PROMOTE signal.

## build-track-feasibility (build-track agents — plan challenge only in C1)
### implementation-engineer

#### CODEBASE SURVEY COMPLETE — 2026-04-23
Survey scope: chain-evaluator.py, phase-gate.py, gate_checks.py, sigma-verify/src/sigma_verify/machine.py, hateoas-agent/src/hateoas_agent/mcp_server.py
Status: ✓ all target files read. Proactive feasibility evidence gathered before ADRs land.

---

#### PRE-PLAN FEASIBILITY EVIDENCE (code-read grounded, by issue)

**#4 A12 key mismatch — CONFIRMED ONE-LINE FIX, LOW risk**
chain-evaluator.py:241: `result.details.get("archive_exists", False)` — key does not exist
gate_checks.py:1517: returns `"archive_file_found": has_archive_file` — the actual key
Fix direction: rename in chain-evaluator.py (consumer), not gate_checks.py (provider). check_a14 also calls gc.check_session_end() but reads `git_clean` — unaffected.
|source:[code-read chain-evaluator.py:234-245, gate_checks.py:1513-1527]

**#5 peer-verify regex — TWO options; one safe, one introduces new bug**
chain-evaluator.py:277-280: `_PEER_VERIFY_HEADER = re.compile(r"^### Peer Verification:\s*(\S+)\s+verifying\s+(\S+)", re.MULTILINE | re.IGNORECASE)` — anchors to `^###` (3 hashes)
Spawn template used `####` (4 hashes) — explains 7/7 R19 miss.
Option (a) spawn-template-only: zero code change, LOW risk, correct.
Option (b) regex relaxation to `^#{3,4}`: introduces A17 over-capture bug. Section boundary stop at chain-evaluator.py:293-298 uses `re.search(r"^#{2,3}\s", ...)` — if `####` peer-verify headers are accepted, the stop-pattern misses `####` headers, causing `_extract_peer_verifications` to over-extend section text into the wrong agent content. A17 specificity check then counts artifacts from wrong sections.
BUILD-CHALLENGE[implementation-engineer]: if tech-architect ADR proposes regex relaxation (option b), the ADR must simultaneously fix the section-boundary stop at chain-evaluator.py:293-298. Missing this creates a new A17 false-positive bug. Option (a) alone is safe and sufficient. |feasibility:H for (a), M for (b) with coordinated fix |source:[code-read chain-evaluator.py:277-306]

**#1 sed -i mechanical block — FEASIBLE, ~10 LOC, precise regex required**
phase-gate.py:263-266 Bash handler checks git commit/push only.
Adding sed ban requires distinguishing footgun from safe forms:
- BLOCK: `sed -i "s/..."` (no backup extension, the macOS footgun)
- ALLOW: `sed -i ''` (BSD-safe) and `sed -i.bak` or `sed -i.ext` (backup extension)
Naive `r'sed\s+-i'` blocks all forms including safe BSD usage. Correct detection requires negative lookahead or character-class to exclude backup extension forms. Non-trivial to write without false positives on safe `sed -i ''` usage. Plan-track must specify the regex or leave it to C2 with explicit note.
|source:[code-read phase-gate.py:252-274]

**#3 ΣVerify tool inheritance — H1 CONFIRMED (user owns sigma-verify) | root cause: HATEOAS state gating**
sigma-verify confirmed at ~/Projects/sigma-verify. Architecture: StateMachine in machine.py → serve() in server.py → hateoas_agent/mcp_server.py.
Root cause (code-read confirmed): `verify_finding`, `cross_verify`, `challenge` registered with `from_states=["ready"]` (machine.py:48-90). Only `init` and `check_quotas` use `from_states="*"`. MCP server sends `tools/list_changed` after `init` triggers `ready` state transition (mcp_server.py:122-123) — but spawned Agent subprocesses do not reinitialize deferred tool registry from this notification. ToolSearch for `mcp__sigma-verify__verify_finding` fails at spawn time because the tool is not yet in the registry.
Fix options:
- B (spawn prompt): add `mcp__sigma-verify__init` call before ToolSearch in every agent spawn. ZERO code change, fastest fix.
- D (machine.py): remove `from_states=["ready"]` from 3 state-gated tools; add runtime guard in handlers.py returning "not initialized" error if called before init. ~15-20 LOC. Structurally removes footgun.
B and D are complementary — B fixes immediately, D fixes architecturally. Not mutually exclusive.
BUILD-CHALLENGE[implementation-engineer]: ADR for #3 must specify WHICH options (B only, D only, or both). If D is included, handlers.py modification surface must be specified. |feasibility:H for B, M for D |source:[code-read machine.py:17-128, mcp_server.py:100-141]

**#19 A3 DB-step parser false negatives — CONFIRMED BUG, marker regex is root cause**
chain-evaluator.py:171-176: step markers searched via `re.search(marker, entry, re.IGNORECASE)` — treats marker strings as regexes.
Bug: `assume.wrong` as regex matches `assumeXwrong` (any char via `.`) but NOT `assume wrong` (space). `re.estimate` fails for "re-estimate" (hyphen). Agents use natural language variants → markers not detected.
Secondary bug: section boundary `(?=DB\[|\Z|###)` stops at `###` not `####` — DB entries under `####` subheadings are cut off or merged.
Fix: expand marker patterns to accept variants: `r"assume.?wrong|assume wrong"`, `r"re.?estimate|re-estimate"`. Fix boundary to stop at `#{3,}`.
|source:[code-read chain-evaluator.py:163-183]

**#20 A12 timing — Option C (24h grace) is correct; A and B create circular dependency or added complexity**
Option A (block shutdown on archive): archive triggered BY shutdown workflow → circular dependency.
Option B (A12 re-runs post-archive): stateful re-evaluation, added architectural complexity.
Option C (24h grace): ~20 LOC in check_a12 — read archive mtime, compare to exit-gate timestamp.
Risk: exit-gate timestamp extraction from workspace must be machine-readable. If timestamp is only in prose narrative, parsing is fragile. Must verify before C2.
|source:[code-read chain-evaluator.py:234-264, phase-gate.py:185-225]

**#21-#24 new protocol gates — FEASIBLE pattern, test burden significant, #22 detection hardest**
Pattern: gate_checks.py CheckResult function → chain-evaluator.py _wrap_gc wrapper → CHECKLIST registration.
Test burden: ~28-36 new tests across 4 gates (per code-quality-analyst TEST-MAP).
#22 precision gate: "quantified claim above specificity threshold" — no clean regex distinguishes `"35%"` (needs CI/breakdown) from `"1 of 5 agents"` (simple count). False-positive risk HIGH if over-broad.
C4/C5 constraint: #22 and #23 should be WARN initially, promoted to BLOCK only after calibration confirms no false positives. Starting as hard BLOCK without calibration run violates "accountable rigor over permissiveness."
BUILD-CHALLENGE[implementation-engineer]: ADR for #22 must specify the concrete detection heuristic (regex? semantic pattern? numeric-only threshold?). "Quantified claim" is underspecified as a C2 implementation target. |feasibility:L without concrete spec, M with concrete spec |source:[code-read chain-evaluator.py:136-220, C4/C5 constraints]

---

#### DB[] — top 3 highest-conviction claims (added per TW peer-verify GAP-1)

DB[#5-spawn-template-only]:
(1)initial: fix peer-verify miss by relaxing _PEER_VERIFY_HEADER regex to accept ^#{3,4}
(2)assume-wrong: regex relaxation without coordinated section-boundary fix creates A17 over-capture — _extract_peer_verifications stop-pattern at chain-evaluator.py:293-298 uses ^#{2,3} and misses #### headers, causing section text to bleed across agents
(3)strongest-counter: spawn-template-only (option a) fixes root cause (agents produce wrong format) without any regex change and without introducing the section-boundary bug
(4)re-estimate: option (a) is strictly safer — zero code change, zero regression risk, full fix
(5)reconciled: spawn-template-only is the correct and complete fix; TA IC[5] correctly adopted this; no regex change required |source:[code-read chain-evaluator.py:277-306]

DB[#20-24h-grace]:
(1)initial: signal-driven re-run with 30s timeout (ADR[3] original)
(2)assume-wrong: 30s wait/poll loop in Stop hook violates chain-evaluator non-looping design invariant; adds latency to ALL session ends including non-sigma; synthesis-complete token undefined
(3)strongest-counter: 24h grace window (~20 LOC) — compare archive mtime to exit-gate timestamp; no polling, no circular dependency, deterministic, testable with datetime mock
(4)re-estimate: 24h grace is strictly simpler and correctly handles the race condition without hook architectural risk; auditor's original suggestion was right
(5)reconciled: 24h grace is correct; TA conceded (BC[#2]); ADR[3] revised accordingly; SQ[2] est 3h→1h |source:[code-read chain-evaluator.py:234-264, TA-BC[#2]-concede]

DB[#1-shlex-split]:
(1)initial: block all `sed -i` via raw string regex `r'sed\s+-i'` in phase-gate.py Bash handler
(2)assume-wrong: naive regex blocks `sed -i ''` (BSD-safe form) and `sed -i.bak` — correct usage — causing false positives on legitimate workspace operations
(3)strongest-counter: argv tokenization via shlex.split() distinguishes `-i` flag without attached backup extension from `-i ''` (empty string arg) and combined `-i.bak` arg; more precise than substring match
(4)re-estimate: shlex.split() is the correct approach; SS confirmed post-XVERIFY; known gaps (env/xargs wrapping) accepted as documented residual risk, not blocking
(5)reconciled: shlex.split() argv tokenization + backup-extension detection is the implementation target; try/except for malformed quoting is C2 detail; SS IC[1] (post-XVERIFY refinement) is the authoritative spec |source:[code-read phase-gate.py:252-274, SS-ADR[1]-post-XVERIFY]

---

#### OPEN QUESTIONS — RESOLVED post ADR read
OQ-IE1: #5 resolved — TA IC[5] chose spawn-template-only. No regex relaxation. ACCEPT.
OQ-IE2: #3 resolved — TA chose D (machine.py auto-ready), SS chose B (spawn-prompt). Divergence flagged in BUILD-CHALLENGE below.
OQ-IE3: #21 resolved — directive+spawn-template only per CDS; chain-eval check in SQ[CDS-6] separately for #22.
OQ-IE4: #22 resolved — CDS ADR[2] specifies CONDITION 1+2 conjunction. Implementation challenge issued below on numeric regex.
OQ-IE5: #20 resolved — TA ADR[3] chose signal-driven + archive dir mtime. Implementation challenge issued below on signal spec.

---

#### FORMAL BUILD-CHALLENGE ENTRIES (per-ADR, post plan-track read)

BUILD-CHALLENGE[implementation-engineer]: TA-ADR[1] vs SS-ADR[2] — divergent fix for #3, precedence unresolved |feasibility:M |issue: TA-ADR[1] proposes Option D (auto-ready at machine.py startup when API keys present, ~5 LOC). SS-ADR[2] proposes Option B (spawn-prompt + agent-def update, zero code), citing HATEOAS bypass risk. These are not in conflict IF D is primary and B is belt-and-suspenders defense-in-depth — but plan-track has not declared precedence. The consequence for C2: if D ships (SQ[5]) but B is not also implemented (SQ[SS-3]), a future code rollback of D silently re-breaks XVERIFY. If only B ships and D is not implemented, the R19 failure recurs when an agent skips the spawn-prompt call. handle_init() confirmed code-read-safe (API-key-check only, no side effects, no external HTTP). Auto-ready at startup is LOW risk per handle_init() code read. → revise: plan-track designate D as primary fix, B as defense-in-depth. Both SQ[5] and SQ[SS-3] should ship. IC[3] takes precedence; IC[2]-SS is belt-and-suspenders. If plan-track disagrees, state explicitly which is authoritative so C2 can prioritize correctly. |source:[code-read machine.py:17-128, handlers.py, cross-agent TA-ADR[1] vs SS-ADR[2]]

BUILD-CHALLENGE[implementation-engineer]: TA-ADR[3] / IC[2] — signal-driven A12 re-run underspecifies the Stop hook wait mechanism |feasibility:M |issue: IC[2] specifies "new function: check_a12_post_archive(content: str, max_wait_s: int = 30) → ChainItem" — a 30s wait loop inside a Stop hook. Three implementation problems: (1) The Stop hook fires once and exits; a 30s wait keeps it alive on EVERY session end including non-sigma sessions. Must add _is_sigma_session() guard (already exists in phase-gate.py, needs mirroring in chain-evaluator.py Stop path). (2) "Synthesis-complete marker" — what exact workspace token triggers the signal? If prose-embedded, parsing is fragile. (3) "archive dir mtime within 60s" — comparison of archive dir mtime to Stop hook invocation time. If archive was written 59s ago and synthesis ran slow, A12 times out and incorrectly fails. The 60s window is arbitrary. → revise: IC[2] must specify: (a) exact synthesis-complete workspace token (or confirm "archive dir mtime check only — no synthesis marker"), (b) whether wait loop is guarded by _is_sigma_session(), (c) fallback behavior if timeout fires — "log A12-TIMEOUT and use existing archive_file_found check" is the correct fallback per TA description, but it must be explicit in IC[2] to avoid C2 inventing behavior. |source:[code-read chain-evaluator.py:234-264, IC[2] spec]

BUILD-CHALLENGE[implementation-engineer]: SS-ADR[1] / IC[1] post-XVERIFY — shlex.split() implementation has three under-specified edge cases |feasibility:M |issue: IC[1] correctly upgraded to argv tokenization. Three gaps: (1) shlex.split() raises ValueError on malformed quoting. A Bash command with unclosed quotes (not uncommon in multi-line commands) causes the hook to throw unhandled — must wrap in try/except with fallback to deny-safe behavior (block or allow with warning). (2) "next_arg_after_i_is_not_extension(args)" is not defined — what counts as backup extension? macOS `sed -i ''` produces argv `['sed', '-i', '']` (empty string arg). `sed -i.bak` may appear as either `['sed', '-i.bak']` (combined) or `['sed', '-i', '.bak']` (split) depending on shell quoting. Detection logic differs between these forms. (3) `env sed -i file` → argv `['env', 'sed', '-i', 'file']` — SS flagged this as remaining risk but did not specify whether it's accepted as known gap. → clarify: IC[1] must specify (a) try/except shlex.split() fallback (deny-safe recommended), (b) backup-extension detection for combined `-i.ext` arg vs separate `''` arg, (c) env/xargs evasion: explicitly accepted gap or additional detection required. These three decisions must be in IC before C2 writes test cases. |source:[code-read phase-gate.py:252-274, SS-ADR[1] IC[1]]

BUILD-CHALLENGE[implementation-engineer]: CDS-ADR[2] / SQ[CDS-6] + TA-SQ[10] — #22 chain-evaluator detection target is underspecified for deterministic implementation |feasibility:L without spec, M with clarification |issue: CDS ADR[2] correctly specifies CONDITION 1+2 semantically, but the chain-evaluator implementation note (p.502) acknowledges "chain-evaluator may need conservative trigger (numeric + CONDITION 2 marker → flag; DA adjudicates CONDITION 1)." This means the gate is a pre-filter that depends on DA follow-through — it cannot produce a deterministic PASS/FAIL alone. For SQ[CDS-6] and TA-SQ[10] to have a deterministic test suite, need: (a) What is the numeric claim regex? (e.g. `\b\d+\.?\d*\s*%|\$[\d,]+|\b\d+\.?\d*\s*(?:FTE|months|years|mo|yr)\b` — or does plan-track leave this to C2?) (b) What CONDITION 2 marker patterns does chain-evaluator detect by text search? HIGH-severity tag is findable; ">70% confidence" is not a standardized workspace token — does it detect literal `\b7[0-9]%|8[0-9]%|9[0-9]%` confidence tags? Cited-in-recommendation — how is "cited in primary recommendation" detected mechanically? (c) WARN→BLOCK calibration: SQ[CDS-6] specifies "3-review calibration gate" — who owns this decision and what format triggers promotion? → clarify: IC for A20 check must specify regex patterns (a) and (b). If plan-track cannot specify (a) and (b) before C2, then SQ[CDS-6] should be scoped as "CONDITION 2 marker only → WARN" with a comment that CONDITION 1 absence detection is deferred to calibration. That is an honest scoping decision. |source:[code-read chain-evaluator.py:136-220, CDS-ADR[2] detection note]

BUILD-CHALLENGE[implementation-engineer]: H5 stale baseline — SQ[13] uses incorrect count, must be corrected before C2 |feasibility:H (trivial fix) |issue: TA-SQ[13] specifies "extend 154-test baseline." code-quality-analyst confirmed: actual baseline is 92 tests (not 154), 11 pre-existing failures, 81 currently passing. 62-test gap includes 20 commented-out orchestrator-archive tests. SQ[13] est=5h does not include fixture-fix time (1h minimum) needed to restore 11 pre-existing failures before C2 regression testing is reliable. Additionally, 11 pre-existing failures will generate misleading FAIL signals in C2 if not fixed first. → revise: SQ[13] should specify "fix fixture defect (1h) + add 30-46 new tests (5h) = 6h total." Baseline contract should be "deliver 111-127 tests with 0 pre-existing failures and 0 new regressions" — not "extend 154." |source:[code-read code-quality-analyst TEST-MAP, H5 in SCRATCH:35]

---

#### ACCEPT DECISIONS (no challenge required)

ACCEPT: TA-ADR[2] / IC[1] — A12 key fix (archive_exists → archive_file_found in chain-evaluator.py:241). One line, correct direction. |source:[code-read chain-evaluator.py:241, gate_checks.py:1517]

ACCEPT: TA-IC[5] / #5+#14 — spawn-template-only, 3-hash canonical format. Correctly avoids regex relaxation and the A17 section-boundary bug flagged in pre-plan survey. |source:[code-read chain-evaluator.py:277-306]

ACCEPT: TA-IC[4] / #19 A3 — expanded marker set with DB[ tag guard (marker-counting requires DB[ opening tag present). Addresses false-negative root cause and prevents over-counting risk. |source:[code-read chain-evaluator.py:163-183]

ACCEPT-WITH-NOTE: CDS-ADR[1] / #21 — Step 8.5 accepted as primary position. HOWEVER: DIV[2] logged by lead — TA placed premise-audit at Step 7a (BEFORE user confirms Q/H/C), CDS placed at Step 8.5 (AFTER user confirms Q/H/C, before spawn). Implementation-engineer position: CDS Step 8.5 is correct for anti-anchoring. CDS's own rationale specifies "lead answers PA[1-4] BEFORE reviewing user's H-space" — but Step 8.5 (post-Q/H/C confirmation) means lead has already read the user's H-space at Step 8. The anti-anchoring protection is only preserved if the PA[1-4] answers are written down BEFORE the lead re-reads the H-hypotheses. This is a SEQUENCE within the step, not a step-location question. TA Step 7a is cleaner (lead hasn't confirmed H-space at all). DA should adjudicate DIV[2] on this basis. C2 implementation is unblocked either way — the directive text changes regardless; only the step number changes. No C2 code surface.

ACCEPT: CDS-ADR[3] / #23 — TIER-A/B/C governance artifact taxonomy with DA quality-check ("ARTIFACT-REVIEW" format). WARN initially per calibration estimate. DA quality-check is load-bearing enforcement.

ACCEPT: CDS-ADR[4] / #24 — 3-field severity-basis tag + DA explicit audit. WARN→BLOCK after 3 reviews. Directive-only.

ACCEPT: SS-ADR[3] — no separate audit log. Workspace + chain-evaluator + archive is sufficient.

---

#### CONVERGENCE DECLARATION — FINAL (post-challenge-response read) 26.4.23

BUILD-CHALLENGE resolutions confirmed:
BC[#1-ADR[3]]: RESOLVED — TA conceded; ADR[3] revised to 24h grace-window; SQ[2] est 3h→1h. IC[2] updated. Stop-hook non-looping invariant preserved. |source:[TA convergence-declaration BC[#2]-concede]
BC[#2-SQ[13]]: RESOLVED — TA conceded; SQ[13] split into SQ[13a-g], 11-15h total. Baseline floor revised to 143 passing (not 154 or 81). |source:[TA convergence-declaration BC[#1+#3]-concede, H5-REVISED]
BC[#3-IC[4]/check_a3 duplication]: RESOLVED — TA clarified layered authority: gc=presence check (V6), chain-evaluator=depth check (A3 enhancement). Not conflicting — sequential. |source:[TA convergence-declaration BC[#4]-concede]
BC[#4-DIV[1] ΣVerify architecture]: RESOLVED by cross-agent — SS peer-verification of CDS conceded CDS auto-ready OVERRIDES SS spawn-prompt as primary enforcement. SS IC[2] marked SUPERSEDED. SQ[SS-3] reduced to belt-and-suspenders. |source:[SS peer-verification of CDS, security-specialist self-correction]
BC[#5-SS IC[1] shlex.split()]: PARTIALLY RESOLVED — SS post-XVERIFY refinement specifies shlex.split() + env/xargs flagged as known remaining risk. Combined -i.bak detection logic and try/except fallback remain unspecified in IC[1]. C2 implementation-engineer will add try/except and handle combined form per standard Python idiom. Acceptable as C2 implementation detail, not plan blocker.

DIV[1]: RESOLVED by SS self-correction — CDS auto-ready (machine.py) is primary; SS spawn-prompt is belt-and-suspenders.
DIV[2]: PENDING DA adjudication (Step 7a vs Step 8.5). C2 implementation unblocked either way — only directive step number changes.
DIV[3]: Admin — lead to renumber IC namespace post-DA.

Remaining open: SQ[CDS-6] A20 CONDITION 1 detection mode (code-detect vs DA-delegate) — still unspecified. Scoping this as C2 implementation decision: implement CONDITION 2 marker detection only → WARN; document CONDITION 1 as DA-delegated. Honest scoping, testable.

✓ implementation-engineer: CONVERGENCE DECLARED (revised post-TW-peer-verify) |all-material-BCs-resolved |peer-verify-CQA:PASS |DIV[1]:RESOLVED |DIV[2]:pending-DA(C2-unblocked) |DIV[3]:admin |SQ[CDS-6]-CONDITION1:scoped-to-DA-delegated |TW-GAP-1:FIXED(DB[#5-spawn-template-only]+DB[#20-24h-grace]+DB[#1-shlex-split] added above) |TW-GAP-2:already-fixed(convergence-updated-post-ADR-read) |→ READY FOR DA + plan-lock

|
### Peer Verification: implementation-engineer verifying code-quality-analyst

§2a-e hygiene: CONFIRMED |H5-verdict=outcome-1(stale-count forces H5 revision) |ADR[3]-challenge=outcome-3(gap: stop-hook non-looping unaddressed by plan-track) |coverage-map=§2c |source:[code-read TEST-MAP]

§2g DB[]: implicit-5-step in H5 verdict: (1)initial:154-baseline (2)assume-wrong:count-stale (3)counter:live-pytest-92 (4)re-estimate:11-failing→81-passing (5)reconciled:111-127-tests-0-regressions. Build-track feasibility role — DB[] as evidence-from-code-read is appropriate form. |source:[code-read H5-verdict]

|source:{type}| tags: CONFIRMED on all key claims — [code-read live-pytest 26.4.23] + [code-read chain-evaluator.py:625-640] + [code-read test_gate_checks.py+test_hooks.py] + [code-read CDS ADR[2]] |source:[code-read BUILD-CHALLENGEs]

XVERIFY: N/A for build-track feasibility role — §2h analytical domain findings only, not process coverage checks. No gap. |source:[directives.md §2h]

SQ[]/CAL[]/PM[]: SQ[]=not-primary-deliverable-for-CQA. CAL[]=embedded in challenge estimates (24h-grace=2-3-tests, signal-driven=3-5-tests, SQ[13]-5h→8-12h). PM[]=not-separately-formatted — minor gap, covered by PM[SS-3]+PM[CDS-2] from plan-track. Non-blocking. |source:[peer-verification-index criteria]

ADR[3] stop-hook challenge: INDEPENDENTLY CONFIRMED — chain-evaluator.py Stop path non-looping by design; 30s wait/poll loop violates invariant. IE reached same conclusion via independent code-read of chain-evaluator.py. CQA challenge grounded and specific (chain-evaluator.py:625-640). |source:[code-read chain-evaluator.py, independent-IE-BUILD-CHALLENGE[ADR[3]]]

IC[3] check_a3 duplication challenge: INDEPENDENTLY CONFIRMED — chain-evaluator.py:162-183 second depth check uncoordinated with gc.check_dialectical_bootstrapping creates A3 passed=True with non-empty issues. Challenge actionable (designate authoritative layer). |source:[code-read chain-evaluator.py:162-183]

SQ[6] sigma-verify test ownership: VALID open question — separate repo with separate test run; conflating with chain-evaluator baseline misrepresents regression coverage. |source:[code-read sigma-verify repo]

PEER-VERIFY[implementation-engineer→code-quality-analyst]: PASS |§2hygiene:CONFIRMED |DB[H5]:implicit-5-step |source-tags:CONFIRMED |XVERIFY:N/A-role |PM[]:minor-gap-non-blocking |ADR[3]:INDEPENDENTLY-CONFIRMED |IC[3]-duplication:INDEPENDENTLY-CONFIRMED |SQ[6]:valid-open |internal-consistency:CLEAN |artifact-refs: H5-verdict(1) + TEST-MAP-table(2) + BUILD-CHALLENGE[ADR[3]](3) + BUILD-CHALLENGE[IC[3]](4) + BUILD-CHALLENGE[SQ[6]](5) + BUILD-CHALLENGE[SQ[13]](6) + convergence-declaration(7) — ≥3 met |#7

✓ implementation-engineer: CONVERGENCE DECLARED |codebase-survey:DONE |BUILD-CHALLENGEs:5-issued |ACCEPTs:7(1-with-note) |peer-verify-CQA:PASS |DIV[1]+[2]:awaiting-DA |4-open-items:awaiting-plan-track |memory:stored-patterns.md |→ WAITING for DA + plan-track responses; C2 ready when those close

### code-quality-analyst

## TEST-MAP [code-quality-analyst] — 26.4.23

### Baseline state: CRITICAL PRE-EXISTING FAILURES

**Claimed baseline: 154 tests** (project_gate-infrastructure.md, written 26.4.16)
**Actual collected test count: 92 tests** (pytest --collect-only, run 26.4.23)
**Actual baseline failures: 11 of 92 ALREADY FAILING before any R19 changes**

The 154-test claim is stale by 7 days. Current reality: 92 tests, 11 failing. H5 ("¬regress to 154-test baseline") is based on a count that does not match the live codebase. This must be resolved before C2 uses a regression baseline.

62 tests are missing from the claimed baseline. Orchestrator-archive accounts for 20 (commented-out, non-runnable). Remaining 42-test gap is unexplained.

### Test file composition (current, live)

**test_gate_checks.py — 68 tests, 23 classes:**
- TestWorkspaceParsing (8): parse_sections, extract_agents, sigverify, hypotheses, tier, mode, agent-section getters
- TestV3AgentOutputNonEmpty (2): A1 non-empty
- TestV4SourceProvenance (2): A2 source tags
- TestV5XverifyCoverage (2): A15 xverify
- TestV6DialecticalBootstrapping (2): A3 DB[]
- TestV7HypothesisMatrix (3): hypothesis matrix gating
- TestV9CircuitBreaker (3): A4 circuit breaker
- TestV10CrossTrackParticipation (2): A5 DA challenges
- TestV11BeliefStateWritten (3): A6 belief state
- TestV13ContaminationCheck (2): A8 contamination
- TestV15AntiSycophancy (2): A10 anti-sycophancy
- TestV16ExitGateFormat (2): A7 exit-gate
- TestV17PlanLock (6): B1 plan-lock
- TestV19Checkpoint (2): B2 checkpoint
- TestBundles (6): run_validation bundles
- TestBeliefComputation (6): belief compute (analyze/build)
- TestV22SessionEnd (2): session-end bundle
- TestV23SynthesisArtifact (3): synthesis artifact
- TestV4FindingFormatVariants (2): FINDING[] prefix regression
- TestV5XverifyPartialVariants (1): XVERIFY-PARTIAL variants
- TestV6DbReconciledAndDisconfirm (3): DB-reconciled/DISCONFIRM
- TestV10DaSectionMinimumSignal (2): DA-C[] + section fallback
- TestBeliefOutcomeFuzzyFlag (2): fuzzy-flag transparency

**test_hooks.py — 24 tests, 6 classes:**
- TestChainEvaluatorCLI (5): CLI routing (evaluate/status/args/hook-mode)
- TestShutdownGate (4): phase-gate shutdown block
- TestAgentParser (5): agent section parsing
- TestA14CircularDependency (3): A14-only allows commit
- TestChainEvaluatorIntegration (1): chain-evaluator writes .chain-status.json
- TestSourceProvenanceBlockScope (6): A2 multi-line body-tag detection

**ZERO tests exist for:** A16, A17, A18 (peer-verification checks) — the entire peer-verification ring is untested.

### Pre-existing failures: root cause

11 tests failing NOW, before any R19 changes. Root cause: MINIMAL_WORKSPACE fixture uses `agent-alpha`/`agent-beta` which are NOT in roster.md. The roster-based extraction path (which IS used because roster.md exists) returns only roster-matching names — `devils-advocate` is in roster, the test agents aren't. Tests were written assuming the exclusion-list fallback (which excludes DA). Roster was added later and broke the fixture assumptions.

Failing tests: test_extract_agents, TestV3 x2, TestV5 x1, TestV6 x3, TestV10 x1, TestBeliefComputation x1, TestV5XverifyPartialVariants x1, TestV6DbReconciledAndDisconfirm x2.

**This is a pre-existing defect, not an R19 side effect.** But it poisons regression testing: any test touching these 11 will give unreliable signal in C2.

### Coverage map per R19 issue

**#4 A12 key-mismatch (archive_exists → archive_file_found):**
- chain-evaluator.py:241 reads `details.get("archive_exists", False)` but gate_checks returns key `archive_file_found`
- Existing coverage: TestV22SessionEnd (2 tests) covers session-end bundle at gate_checks level. ZERO tests assert chain-evaluator A12 pass/fail directly.
- Regression risk: LOW — key rename is isolated. Existing tests don't break.
- New tests needed: 2 (chain-evaluator A12 passes when archive_file_found=True; fails when key absent)

**#5+#14 peer-verify regex (3-hash "verifying" format):**
- Existing coverage: ZERO. A16, A17, A18, _extract_peer_verifications, _PEER_VERIFY_HEADER — all untested.
- Regression risk: ZERO (no existing tests to break)
- New tests needed: 8-12 (A16: 3, A17: 3, A18: 3, regex format variants: 2-3)
- Flakiness risk: LOW (regex-based, deterministic)

**#19 A3 DB-step parser (marker tolerance):**
- Existing coverage: TestV6 (2 tests) + TestV6DbReconciled (3 tests) — ALL 5 currently failing due to roster fixture bug
- chain-evaluator check_a3 (lines 162-183) has its own shallow_db logic ON TOP of gc.check_dialectical_bootstrapping — ZERO unit tests for chain-evaluator-level A3 depth check
- R19 fix changes the 3-of-5 marker threshold — no test currently verifies this threshold
- Regression risk: MEDIUM — all existing DB tests are already broken; fix must restore them AND not break others
- New tests needed: 4-6 at chain-evaluator level (all 5 markers, 3 markers at threshold, 2 markers shallow, DB-reconciled/DISCONFIRM variants)
- BLOCKER: fixture fix must precede these tests or results are unreliable

**#20 A12 timing window (24h grace):**
- Existing coverage: ZERO direct A12 unit tests
- Race condition not testable deterministically without mocking time
- Flakiness risk: MEDIUM — if using real timestamps, CI timing matters. Must mock datetime.
- New tests needed: 2-3 (archive within 24h passes, archive >24h fails, no archive fails)

**#21 premise-audit pre-dispatch:**
- Directive-only change → ZERO new tests if no code gate
- IF phase-gate enforces: 2-3 phase-gate tests needed
- Regression risk: ZERO (directive changes have no test surface)

**#22 §2i precision gate (highest risk):**
- No existing tests
- Calibration flakiness risk: HIGH — false precision detection on free text. Over-tight = flags every number in workspace (process killer). Over-loose = misses the problem.
- Must test against archived workspaces before C2 ships: R19 archive contains known-bad claims (F[TA-C2] FTE range without breakdown) AND known-good claims (explicit driver breakdowns). Gate must distinguish.
- New tests needed: 4-5 unit + 3-5 calibration against archives = 8-10 total
- Recommendation: plan-track must specify the detection algorithm (regex on numeric patterns? semantic?) before C2 can estimate test complexity accurately.

**#23 governance min-artifact:**
- Directive-only → ZERO tests if no code gate
- IF code gate: 3-4 tests (HIGH+governance+no-artifact fails, HIGH+governance+artifact passes, non-HIGH passes)
- Flakiness risk: MEDIUM (compound condition parsing)

**#24 §2d severity provenance extension:**
- Directive-only → ZERO tests if no code gate
- IF extends check_source_provenance: regression risk HIGH — 10 existing A2 tests could break (TestV4SourceProvenance x2, TestV4FindingFormatVariants x2, TestSourceProvenanceBlockScope x6)
- New tests needed: 2-3

### Style/dead-code concerns

1. **check_a3 duplication:** chain-evaluator.py lines 162-183 implement a second DB-depth check on top of gc.check_dialectical_bootstrapping. Two checks not coordinated — gc result can pass while chain-evaluator appends issues. Creates A3 passed=True with non-empty issues list. Confusing. R19 #19 fix should reconcile this, not add a third layer.

2. **`importlib.import_module("phase-gate")`:** test_hooks.py line 229 — hyphenated module name is fragile. Any phase-gate.py rename or path change produces obscure import errors. Any R19 phase-gate changes must verify these tests still import correctly.

3. **Filesystem side effects in tests:** TestV23SynthesisArtifact creates real files in the live archive directory. Interrupt-fragile. Low priority but worth noting for CI environments.

### Error-handling pattern consistency

New gates (#21-#24) added to chain-evaluator should follow `_wrap_gc(...)` pattern, NOT the mutate-after-wrap pattern used in check_a3 (which mutates result.issues after creation). The mutation pattern is inconsistent with the dataclass design.

### H5 verdict: STALE BASELINE — NOT TESTABLE AS STATED

H5 ("¬regress to 154-test baseline") cannot be verified as written:
1. Actual baseline is 92 tests, not 154. Gap is unexplained.
2. 11 of 92 are pre-existing failures unrelated to R19.
3. Regression floor is 81 currently-passing tests, not 154.

**Revised H5:** "Keep all 81 currently-passing tests passing, and add 30-44 new tests per issue estimates above." This is testable. The 154 claim should be struck or explained.

### Test addition summary

| Issue | New tests | Complexity | Flakiness risk |
|-------|-----------|------------|----------------|
| Fixture prerequisite fix | 1-3 | Low | Low |
| #4 A12 key-mismatch | 2 | Low | Low |
| #5+#14 peer-verify | 8-12 | Medium | Low |
| #19 A3 DB-step | 4-6 | Medium | Medium |
| #20 A12 timing | 2-3 | Medium | Medium |
| #21 premise-audit | 0-3 | Low | Low |
| #22 precision gate | 8-10 | High | HIGH |
| #23 governance artifact | 3-4 | Medium | Medium |
| #24 severity provenance | 2-3 | Medium | Medium |
| **Total** | **30-46** | | |

### Convergence declaration

✓ code-quality-analyst: TEST-MAP complete |pre-existing-failures:11/92 |154-baseline:STALE(actual=92,passing=81) |H5:REVISED |new-test-est:30-46 |highest-risk:#22-precision-gate-calibration |prerequisite:fixture-fix-before-C2 |A16/A17/A18:ZERO-coverage |source:[code-read]

### BUILD-CHALLENGES (per-ADR, post plan-track population) — 26.4.23

---

BUILD-CHALLENGE[code-quality-analyst]: TA H5 confirmation |feasibility:L |issue: TA confirms H5 ("154-test baseline extensible via SQ[13]") but this repeats the stale count. Live pytest --collect-only shows 92 tests, 11 pre-existing failures, 81 passing. SQ[13] says "extend 154-test baseline" — this target is not reachable because 62 of those tests do not exist. TA confirmation of H5 based on the 154 count cannot stand as plan-locked. |→ revise: SQ[13] must be rewritten as "fix 11 pre-existing failures + add 30-46 new tests; baseline floor = 81 passing" |source:[code-read live-pytest 26.4.23]

BUILD-CHALLENGE[code-quality-analyst]: ADR[3] signal-driven complexity vs 24h grace |feasibility:M |issue: TA ADR[3] proposes signal-driven re-run with 30s timeout — but IE's analysis (correct) identifies Option A as circular (archive triggered by shutdown → block shutdown = circular) and Option B as added architectural complexity. ADR[3] is effectively Option B (A12 re-runs post-archive = signal-driven second-chance evaluation). The 30s timeout introduces a Stop hook sleep in the non-looping Stop hook — chain-evaluator was explicitly designed non-looping to prevent retry loops. A wait/poll loop in Stop hook violates this invariant. 24h grace (IE's Option C, ~20 LOC) is simpler, tests cleanly with datetime mock, and correctly handles the race condition without adding polling. |→ revise: ADR[3] must address the Stop hook non-looping constraint explicitly, OR switch to 24h grace (simpler, testable, no hook-state complexity). Test surface: 24h grace = 2-3 deterministic tests with mock; signal-driven = 3-5 tests including async timeout behavior |source:[code-read chain-evaluator.py:625-640 enforce_stop non-looping design, CAL[SQ[2]:3h] vs CAL[Option C:~20LOC]]

BUILD-CHALLENGE[code-quality-analyst]: SQ[13] underestimates test scope |feasibility:M |issue: SQ[13] estimates 5h for "all new checks." That estimate predates CDS A20 specification and covers: fixture prerequisite fix + #4 A12 (2 tests) + #5/#14 peer-verify A16/A17/A18 (8-12 tests) + #19 A3 chain-eval level (4-6 tests) + #20 timing (2-3 tests) + A20 precision (8-10 tests including archive calibration) + #23 governance artifact (3-4 tests) + #24 severity provenance (2-3 tests) + SS BLOCK-3 SQ[SS-2] (6 tests). Total: 34-47 tests across 9 different files/modules. 5h is not achievable for this surface — 8-12h is more realistic at chain-evaluator-level test depth. |→ revise: SQ[13] estimate and split into sub-tasks per module: SQ[13a] fixture fix, SQ[13b] A12+A16/A17/A18, SQ[13c] A3 chain-eval, SQ[13d] A20 precision+calibration (this is the 4h sub-task alone), SQ[13e] SS BLOCK-3. Helps IE and code-quality-analyst parallelize. |source:[code-read test_gate_checks.py+test_hooks.py coverage map, CDS ADR[2] A20 spec]

BUILD-CHALLENGE[code-quality-analyst]: TA IC[3] DB marker expansion AND check_a3 duplication |feasibility:M |issue: IC[3] specifies expanded marker set (initial|assume_wrong|assume.wrong|counter|strongest_counter|re_estimate|re.estimate|reconcile|reconciled) for A3 — this is the gate_checks / chain-evaluator level fix. But chain-evaluator check_a3 (lines 162-183) runs a SECOND depth check that is uncoordinated with gc.check_dialectical_bootstrapping. The plan addresses the marker expansion but does not address the duplication. After the fix, two code paths will both evaluate DB depth with potentially different criteria: gate_checks (V6 check) and chain-evaluator check_a3 (which also calls gc then appends its own shallow_db). This produces a state where A3 passed=True (from gc) but issues is non-empty (from chain-evaluator enhancement). IC[3] must specify which layer owns DB depth detection — not both. |→ revise: IC[3] should specify EITHER (a) gate_checks.check_dialectical_bootstrapping is the authoritative depth check and chain-evaluator check_a3 removes its duplicate layer, OR (b) chain-evaluator check_a3 is authoritative and gate_checks is simplified. Cannot be both. |source:[code-read chain-evaluator.py:162-183, gate_checks.py check_dialectical_bootstrapping]

BUILD-CHALLENGE[code-quality-analyst]: CDS A20 CONDITION 1 detection — concrete regex needed before C2 |feasibility:M |issue: CDS ADR[2] specifies A20 semantics correctly (CONDITION 1: numeric claim without uncertainty justification; CONDITION 2: load-bearing binary). But the detection note says "chain-evaluator may need conservative trigger (numeric + CONDITION 2 marker → flag; DA adjudicates CONDITION 1)." This means chain-evaluator A20 as coded would flag ALL numeric claims with CONDITION 2 markers and defer CONDITION 1 to DA — which is not a code gate, it's a DA instruction written in Python. For test purposes, I need to know: does A20 fire on ANY number + CONDITION 2 marker (high false-positive, low false-negative), or does it attempt CONDITION 1 detection in code? The test calibration surface differs significantly. If DA-adjudicates: test surface is 4-5 simple tests. If code-detects CONDITION 1: need 8-10 archive calibration tests. |→ clarify: SQ[CDS-6] implementation spec must state whether CONDITION 1 is code-detected or DA-delegated. This is a C2 blocker for code-quality-analyst SQ[13d]. |source:[code-read CDS ADR[2] note "DA adjudicates CONDITION 1", CAL[#22 false-positive first 3 reviews]:25%]

BUILD-CHALLENGE[code-quality-analyst]: SQ[6] sigma-verify auto-ready tests — out-of-scope risk |feasibility:H |issue: SQ[6] assigns sigma-verify tests to code-quality-analyst ("add test_auto_ready_on_startup, test_tools_visible_without_init_call"). Sigma-verify is a separate repo at ~/Projects/sigma-verify with its own test suite — not part of chain-evaluator or gate_checks. Writing tests in a different repo outside the main build scope introduces an additional test suite with its own run environment, dependencies, and CI. The SCRATCH scope-boundary says "code fixes: sigma-verify MCP tool registration model (#3)" — SQ[6] is in scope for C2, but it should be confirmed: does code-quality-analyst own sigma-verify tests OR does implementation-engineer? And are sigma-verify tests run as part of the same test run that verifies the 81+N gate_checks/chain-evaluator baseline? |→ clarify: assign SQ[6] ownership (code-quality-analyst vs implementation-engineer) and confirm sigma-verify test run is separate from gate_checks/chain-evaluator baseline (so it doesn't inflate/deflate the regression count). |source:[code-read SQ[6], scope-boundary]

BUILD-CHALLENGE[code-quality-analyst]: SS SQ[SS-2] — sed-i BLOCK test matrix, shlex.split required |feasibility:H |issue: SS IC[1] originally specified raw string regex; post-XVERIFY openai found evasion forms (sed -e -i, env sed, xargs sed). SS ADR[1] was refined to shlex.split() argv tokenization. SQ[SS-2] is assigned to code-quality-analyst for the test matrix. The refined implementation (shlex.split + next_arg_after_i detection) is testable but the edge cases listed by SS (bare BLOCK, .bak ALLOW, '' ALLOW, -n ALLOW, non-workspace ALLOW, multi-cmd BLOCK) are missing the XVERIFY-surfaced forms: env-wrapper, xargs-wrapper, unusual quoting/spacing. My test matrix must cover at minimum 8 forms: (1) `sed -i "s/x/y/" workspace.md` BLOCK, (2) `sed -i '' "s/x/y/" workspace.md` ALLOW, (3) `sed -i.bak "s/x/y/" workspace.md` ALLOW, (4) `sed -n "1p" workspace.md` ALLOW, (5) `sed -i "s/x/y/" /other/path.py` ALLOW, (6) `env sed -i "s/x/y/" workspace.md` BLOCK, (7) command with no workspace path ALLOW, (8) `sed -i\t"s/x/y/" workspace.md` (tab-space) BLOCK. If shlex.split() is used, (6) and (8) become testable deterministically. 6 tests → 8 tests. |→ accept with expanded test matrix. SS must confirm shlex.split() handles the env/xargs cases or flag them as known gaps in SQ[SS-2] implementation note. |source:[code-read SS ADR[1] post-XVERIFY refinement, openai XVERIFY evasion forms]

---

✓ code-quality-analyst: per-ADR BUILD-CHALLENGEs complete |7 challenges issued |critical: H5-stale-count, ADR[3]-stop-hook-violation, SQ[13]-underestimate |requires-ADR-response: IC[3]-duplication, A20-CONDITION1-detection-mode, SQ[6]-repo-ownership |SQ[SS-2]-expanded |source:[code-read]

### technical-writer

## DOC-CHANGE-MAP [technical-writer]

Survey complete 26.4.23. Per-issue documentation impact:

| Issue | Files requiring text changes | Change type | Cross-refs that must update |
|-------|------------------------------|-------------|----------------------------|
| #1 sed -i ban | directives.md (new §6h or §3 workspace-rules), build-directives.md (matching section), _template.md (new ## Workspace Edit Rules block), ALL 22 agent .md files (same block), c1-plan.md spawn template, c2-build.md spawn prompt rules, sigma-lead.md (step-level reminder) | insertion everywhere | Any agent-def that references "Edit tool" needs the ¬sed-i paired with it; spawn template in c1-plan.md Step 11 carries the canonical text agents read at spawn |
| #5+#14 peer-verify regex + spawn template | c1-plan.md Step 11 spawn template (## Peer Verification section), sigma-lead.md §2 spawn block, _template.md ## Peer Verification section | replacement of 4-hash format → 3-hash "verifying" canonical | chain-evaluator _PEER_VERIFY_HEADER regex must match EXACTLY what the template now says — regex and template must change atomically or the fix is partial |
| #21 premise-audit step | c1-plan.md (new step between Step 8 and Step 9, or extension of Step 8 — see challenge below), directives.md §7 prompt-decomposition-protocol (reference to premise-audit as pre-spawn step) | insertion | SCRATCH template in Step 10 needs a ## premise-audit-results section; Preflight Phase Verification checklist (Step 9 block) needs new checkbox |
| #22 §2i precision gate | directives.md (new §2i after §2h, following §2a-§2h pattern), build-directives.md (BUILD variant of §2i referencing directives.md §2i), _template.md ## Analytical Hygiene checklist (new □ row), all agent .md files ## Analytical Hygiene (same new □ row) | insertion | chain-evaluator needs new A-check for §2i if mechanical enforcement is intended; without that, this is directive-only with no mechanical gate |
| #23 HIGH-severity governance min-artifact | directives.md §3b ANALYZE rubric → actionability criterion text extension (4=specific-actions+criteria+artifact-when-HIGH) OR new §2j | insertion/edit | BUILD rubric §3b in build-directives.md needs parallel update; DA enforcement section (directives.md) needs "HIGH-severity governance finding without artifact → challenge" added |
| #24 §2d severity provenance | directives.md §2d (extension after current source-type rules — new sub-block for severity extrapolations), build-directives.md §2d BUILD note (same extension) | insertion | _template.md and all agent .md files ## Analytical Hygiene must add severity-tag rule to source-provenance checklist; DA enforcement section needs "severity extrapolation without agent-inference tag → challenge" |
| §8e corruption recovery template | directives.md (new §8e after §8d — formalize Pattern A from R19 source), protocols.md is alternate location | insertion (new section) | §8a "when to archive" should cross-ref §8e; lead recovery workflow in sigma-lead.md Recovery section should pointer to §8e |
| DA not-discussed probe (#7 weighting) | directives.md adversarial-layer §→ DA challenge framework (strengthen "what is team NOT discussing?" from underweighted to explicit required challenge) | edit | DA spawn prompt template in sigma-lead.md spawn block and c1-plan.md Step 18 spawn should reflect updated framework weight |

### Propagation count summary
- #1 sed -i ban: touches 22 agent defs + _template + c1-plan + c2-build + sigma-lead + directives + build-directives = **28 files minimum**
- #5+#14: touches c1-plan + sigma-lead + _template + chain-evaluator = **4 files** (must be atomic)
- #21: touches c1-plan + directives + SCRATCH template = **3 files** (+ optional phase-gate if hook-enforced)
- #22 §2i: touches directives + build-directives + _template + 22 agent defs = **26 files**
- #23: touches directives §3b + build-directives §3b + DA enforcement = **3 files**
- #24: touches directives §2d + build-directives §2d + _template + 22 agent defs = **26 files**
- §8e: touches directives (new §8e) + sigma-lead Recovery = **2 files**

### Critical atomicity constraints
A1: #5+#14 regex+template MUST change in same commit. Template-without-regex = agents write correct format but chain-evaluator still rejects. Regex-without-template = chain-evaluator accepts format agents don't know to produce.
A2: #22 §2i directive-without-chain-evaluator-check = paper gate only. Either add mechanical check OR document explicitly that §2i is DA-enforced-only (not chain-evaluator-enforced). Must choose.
A3: #1 ban in directives ONLY (without agent-def propagation) = ineffective. R19 showed directive intent was fine; enforcement was missing because spawn prompts didn't carry the rule. The 28-file propagation IS the fix.

### ΣComm boundary audit
All §2 hygiene text in directives.md is agent-facing → ΣComm. Current §2 uses mixed format (some plain prose, some notation). New §2i/#24-extension must match the notation pattern of §2d (source types in [bracket] notation, !rules, !observed-failure-mode). Prose-in-agent-facing = boundary violation.
§8e corruption recovery template: 7-step numbered list is current format in R19 source (plain English). If placed in directives.md (agent-facing), it MUST be re-expressed in ΣComm. If placed in protocols.md (check what audience that targets — may be agent-facing too). This is a non-trivial notation conversion task, not a copy-paste.

### Open questions for plan-track
OQ-TW1: Does §8e go in directives.md (agent-facing, needs ΣComm conversion) or protocols.md (need to verify audience)? Protocols.md appears agent-facing (debate format in ΣComm notation) → both require ΣComm. Is there a human-readable companion doc for §8e, or is the workspace ## recovery-log sufficient?
OQ-TW2: For #22 §2i, is chain-evaluator enforcement in scope for this build (SCRATCH says yes — "chain-evaluator as §2i precision gate")? If yes, what's the check format? I need to know the A-check ID to cross-reference it in the directive text.
OQ-TW3: #21 premise-audit — SCRATCH says "c1-plan.md Step 8 extension." Does this mean a new sub-step (8e?) within Step 8, or a new Step 8.5 between Step 8 and Step 9? The Preflight Phase Verification checklist block needs a matching checkbox entry. Which is the intended step boundary?
OQ-TW4: The 22 agent definitions vary in age and template conformance. technical-writer.md and implementation-engineer.md match _template.md closely but diverge in the Persistence and Promotion sections. Do #1/#22/#24 agent-def updates apply to the _template.md ONLY and agents pick up on next re-spawn, OR must all 22 existing agent .md files be individually edited? If all 22, that's 22 Edit calls in C2 — realistic but should be a named SQ[].

### Peer verification assignment
Assigned: technical-writer verifies implementation-engineer. My verifier: code-quality-analyst.

### Peer Verification: technical-writer verifying implementation-engineer

Verified against IE workspace section (SCRATCH lines 594-673):

- **DB[] structure**: [FAIL — format absent, substance present]
  - IE top 3 highest-conviction claims: (1) option-a spawn-template-only safe for #5; (2) 24h grace correct for #20; (3) shlex.split() required for #1. Assume-wrong reasoning IS embedded in BUILD-CHALLENGE arguments (option-b A17 over-capture bug line 615-616; Options A/B rejected lines 643-646) but NONE carry required DB[{claim}]: (1)initial (2)assume-wrong (3)counter (4)re-estimate (5)reconciled format.
  - #1 shlex.split claim: no assume-wrong analysis present — stated as requirement without self-challenge.
  - A3 false-flag risk: chain-evaluator scans for DB[] markers — absent markers may trigger A3 FAIL on IE section.
  - GAP: IE must add DB[] wrappers around top 3 claims before plan-lock.

- **Source provenance**: [PASS]
  - All 6 pre-plan feasibility findings carry |source:[code-read {file}:{lines}]| tags. Lines checked: 609, 616, 624, 633, 640, 647, 654. All BUILD-CHALLENGE entries also tagged. No untagged [agent-inference] on load-bearing claims. Code-read = T1 equivalent for feasibility role.

- **XVERIFY**: [N/A — PASS by role]
  - Build-track feasibility agent in C1. No XVERIFY required. Correctly absent.

- **Analytical substance — Q[] coverage**: [PASS]
  - Q1 (#3/#4/#1): lines 605-624, 626-633 verified | Q2 (#5/#19/#20): lines 611-616, 635-640, 642-647 verified | Q3 (#21-#24 pattern): lines 649-654 verified | Q4 (enforcement feasibility): 6 BUILD-CHALLENGE entries — 3 pre-plan (616/633/654) + 3 post-ADR (669-672). All carry |feasibility:{H/M/L}| and |source:{}| tags.
  - OQ-IE1 through OQ-IE5: all marked RESOLVED with method documented lines 659-663 ✓

- **ΣComm discipline**: [PASS]
  - BUILD-CHALLENGE entries use |feasibility:|issue:|→|source:| pipe-separated format per spawn template spec. Consistent. No boundary violations.

- **Convergence declaration**: [FAIL — stale]
  - Line 667: partial — awaiting plan-track ADRs — written before post-ADR challenges added; not updated.
  - OQ-IE1-5 RESOLVED, 6 challenges issued — declaration should reflect completed state.
  - GAP: IE should append updated ✓ convergence declaration before plan-lock.

**Overall: implementation-engineer section [INCOMPLETE — 2 gaps]**
- GAP-1 (DB[] format): Top 3 claims lack DB[] 5-step wrapper. A3 risk. Substance recoverable.
- GAP-2 (convergence stale): Declaration not updated post-ADR. Lead cannot confirm IE ✓ from convergence.

### Peer Verification: code-quality-analyst verifying technical-writer

Verified against TW DOC-CHANGE-MAP (SCRATCH lines 881-1038). Criteria: completeness, propagation-count accuracy, atomicity constraints (#5+#14), ΣComm boundary preservation, source tags.

**Completeness — PASS with one gap**
- All 8 in-scope issues are mapped: #1, #5+#14, #21, #22, #23, #24, §8e, DA-not-discussed. Full row coverage. |source:[code-read SCRATCH DOC-CHANGE-MAP table]
- OQ-TW1 (§8e ΣComm location), OQ-TW2 (A-check ID for §2i), OQ-TW3 (step boundary), OQ-TW4 (agent-def scope) — all 4 OQs correctly identified as blockers before C2. None left as implicit assumptions. |source:[code-read SCRATCH OQs]
- GAP: TW's map does not include the DA not-discussed probe in the propagation count summary. Table row exists but propagation count line is absent (only 7 count lines for 8 issues). DA probe touches at least sigma-lead.md DA spawn block + c1-plan.md Step 18 spawn. Missing from total-file count. Severity LOW (DA probe is ~2 files, does not affect the high-count items that drive C2 effort estimation) but should be added for completeness. |source:[code-read SCRATCH propagation-count-summary vs table]

**Propagation counts — PARTIAL PASS (2 factual errors)**
- #1 sed-i ban: TW claims "22 agent defs." Actual agent def count in `/Users/bjgilbert/.claude/agents/`: 25 .md files total; excluding _template, SIGMA-COMM-SPEC, sigma-comm, search-aggressive/conservative/combinatorial, cross-model-validator, m-and-a-deal-counsel = 25 domain + lead + synthesis + statistical. Live count of files with `## Analytical Hygiene` section: 24. TW's "22" is understated by 2. This affects both #1 (28 files → 30 files) and #22/#24 (26 files → 28 files). Not catastrophic — C2 estimate will be slightly low — but the count is verifiably wrong. |source:[code-read ls ~/.claude/agents/*.md; grep -l "Analytical Hygiene"]
- #5+#14: TW counts "c1-plan + sigma-lead + _template + chain-evaluator = 4 files." But c1-plan.md and c2-build.md live in `/Users/bjgilbert/.claude/skills/sigma-build/phases/` not in shared/. Sigma-lead.md is in `/Users/bjgilbert/.claude/agents/`. TW's file paths are not wrong (issue #5+#14 affects spawn templates in those locations) but the count omits c2-build.md — the build phase spawn prompt also uses peer-verify headers and needs the format update. Count should be 5 not 4. Atomicity constraint A1 still holds, just across 5 files. |source:[code-read ls ~/.claude/skills/sigma-build/phases/]
- §2i/§2p numbering collision (TW OQ-TW2 area): TW flags this as a C2 blocker. Verified: directives.md §2 ends at §2h (line 263). CDS ADR[2] assigns `§2i` to the precision gate AND CDS ADR[1] internally uses `§2p` for premise-audit. §2p skips j through o — non-sequential. This is a real structural issue TW correctly identified. Confirmed as unresolved at plan-track level (no ADR addresses §2 numbering). |source:[code-read directives.md:263 section list]

**Atomicity constraints — PASS**
- A1 (#5+#14 same commit): Correctly identified as mandatory. Rationale is exact: template-without-regex and regex-without-template are both partial fixes that create the same broken state. Chain verified. |source:[code-read TW A1]
- A2 (#22 paper-gate risk): Correctly identifies that §2i directive-only = DA-enforced-only gate with no mechanical check. The "must choose" framing is correct — CDS's WARN-first approach means there IS a chain-evaluator check planned (A20), so the directive must reference the check ID. TW escalated this correctly as OQ-TW2 rather than resolving it unilaterally. |source:[code-read TW A2, CDS SQ[CDS-6]]
- A3 (#1 propagation scope): Correctly identifies that directive-only ban is ineffective without agent-def propagation. This matches the R19 post-mortem finding exactly: spawn prompts didn't carry the rule. Analysis is sound. |source:[code-read TW A3, R19 source Pattern 1]

**ΣComm boundary — PASS (substantive, not perfunctory)**
- §8e location analysis is the strongest contribution: TW correctly identifies that plain-English numbered list in R19 source cannot be copy-pasted into directives.md (agent-facing) without ΣComm conversion. Also correctly flags protocols.md as likely agent-facing (debate format in ΣComm notation). This is non-trivial — most agents would treat it as a copy-paste. |source:[code-read TW ΣComm section]
- §2i new section: TW correctly requires the notation pattern of §2d (bracket types, !rules, !observed-failure-mode). Code-read confirms §2d uses this pattern; §2i must match. |source:[code-read directives.md:160-182 §2d format]
- Analytical Hygiene sections in agent defs: TW identifies these use plain-English checkbox format ("□ positioning/consensus check completed"). Adding new §2i and §24 checkboxes in the same format is appropriate for the human-readable identity sections of agent defs. TW correctly doesn't flag these as ΣComm violations (agent Identity sections are explicitly plain English per CLAUDE.md ΣComm boundary rule). |source:[code-read ~/.claude/agents/code-quality-analyst.md Analytical Hygiene]

**Source tags — PASS**
- TW's BUILD-CHALLENGE entries in the status line ("12 BUILD-CHALLENGEs issued") but the TW section in SCRATCH doesn't list them individually — only the DOC-CHANGE-MAP, OQs, atomicity constraints, and convergence status. The TW section structure is clean documentation work, not analytical claims requiring |source:{}| tags. No source tagging obligation triggered. The convergence line references plan-track ADRs which are in workspace — no external sources that need attribution. |source:[code-read TW section SCRATCH lines 879-1038]

**Summary: technical-writer [PASS with 2 factual corrections needed]**
- F[TW-1][LOW]: Agent-def count is 24 (not 22). Propagation totals for #1, #22, #24 are each +2. |→ TW should correct counts before plan-lock (30 not 28 for #1; 28 not 26 for #22 and #24)
- F[TW-2][LOW]: #5+#14 count is 5 not 4 (c2-build.md also needs peer-verify format update). Atomicity constraint A1 remains valid across 5 files. |→ TW should add c2-build.md to the propagation row
- F[TW-3][INFO]: DA not-discussed probe propagation count line missing from summary. ~2 files. |→ add for completeness
- F[TW-4][INFO]: §2p/§2i numbering gap (j-o skipped) confirmed but not flagged explicitly by TW. This is a C2 editing decision, not a C1 blocker. DA or lead should resolve at plan-lock.

All 4 OQs are legitimate blockers. ΣComm boundary analysis is the highest-value contribution in this section. Atomicity constraints are correct and well-reasoned.

✓ code-quality-analyst verifying technical-writer: COMPLETE |F[TW-1]:agent-count-24-not-22 |F[TW-2]:#5+#14-count-5-not-4 |F[TW-3]:DA-probe-count-missing |F[TW-4]:§2p-numbering-gap |overall:PASS-with-corrections |source:[code-read ls-agents, grep-analytical-hygiene, directives.md-section-list, skills-sigma-build-phases]

## architecture-decisions (locked after DA approval)
{ADR[N]: decision |alternatives:{considered} |rationale:{why} |prompted-by:{Q[N]/H[N]/C[N]} |source:{type}}

## design-system (locked after DA approval)
{DS[]: N/A — backend infra build, no UX/UI surface}

## interface-contracts (build-track implements against these)
{IC[N]: typed contracts between hook ↔ chain-evaluator ↔ gate_checks ↔ MCP. To be populated by tech-architect.}

## sub-task-decomposition
{SQ[N]: task |owner:{role} |est:{} |files:{}}

## reference-class
{RC[task]: reference-class={similar builds} |base-rate={typical} |sample-size={N} |src:{} |confidence:{H/M/L}}

## calibrated-estimates
{CAL[task]: point={best} |80%=[lo,hi] |90%=[lo,hi] |breaks-if:{}}

## pre-mortem
{PM[N]: failure mode |likelihood:{} |early-warning:{} |mitigation:{}}
- minimum 3 entries, focused on: technical debt from this remediation, scaling bottlenecks in new gates, integration failures with existing chain

## files
| File | Action | Description |
| --- | --- | --- |

## convergence

### tech-architect — COMPLETE (revised post-challenges) 26.4.23
✓ Boot complete (sigma-mem recall + SCRATCH + R19 source + build-directives + chain-evaluator.py + gate_checks.py + sigma-verify src + hateoas-agent mcp_server.py + registry.py)
✓ H1 CONFIRMED: sigma-verify owned at ~/Projects/sigma-verify; machine.py modifiable; HATEOAS state machine is root cause of #3
✓ H3 CONFIRMED: premise-audit fits as workflow step (Step 7a/CDS Step 8.5 pre-spawn) not new agent role
✓ H4 CONFIRMED: no circular dependencies between 13 SQ items
✓ H5 REVISED: 154 tests collected; 143 passing; 11 pre-existing failures. Passing floor = 143, not 154. |source:[code-read live-pytest 26.4.23]
✓ ADR[1]: auto-ready at build_machine() startup when keys present — XVERIFY: openai(partial/medium-resolved) + nemotron(agree/high) + google(503-gap)
✓ ADR[2]: rename chain-evaluator.py:241 archive_exists → archive_file_found (leaf consumer fix, not gate_checks API change)
✓ ADR[3] REVISED: 24h grace-window adopted (BC[#2] concede — signal-driven violated Stop hook non-looping invariant at chain-evaluator.py:625-640) — SQ[2] est revised 3h→1h
✓ ADR[4]: workflow step (CDS Step 8.5) confirmed for premise-audit (#21)
✓ IC[1-5] revised: IC[2] updated (24h grace, not signal/timeout); IC[4] clarified (layered: gc=presence, chain-evaluator=depth — not conflicting authorities); IC[5] scope expanded to include sigma-lead.md §2 spawn block
✓ SQ[1-13] revised: SQ[13] split into SQ[13a-g] with 11-15h total (BC[#3] concede); SQ[2] est 3h→1h (BC[#2] concede)
✓ RC[1-3] + CAL[1-3] + PM[1-4]: complete
✓ DB[1-4]: complete
✓ XVERIFY mandatory (ADR[1] security-critical): 2 non-anthropic providers verified (google 503 logged as gap)
✓ BC[#1] concede(partial): H5 collection count correct (154); passing floor revised to 143
✓ BC[#2] concede: ADR[3] revised to 24h grace-window; original objection to grace-window was wrong
✓ BC[#3] concede: SQ[13] split into SQ[13a-g]
✓ BC[#4] concede: IC[4] clarified — layered authority (gc=presence, chain-evaluator=depth), not conflict
✓ TW BC[#2] concede: IC[5] scope expanded to include sigma-lead.md §2
✓ Peer verification: ### Peer Verification: tech-architect verifying security-specialist written to ## peer-verification-index

→ DA round 1 responses COMPLETE 26.4.23

✓ DA[#1] CONCEDE: IC[4] marker-variant expansion VOIDED — '.' already wildcard; real bug is DB[] extraction regex matching non-exercise tokens. IC[4] rewritten: split-by-DB[-then-require-(1)(2)(3)-within-segment. |source:[live-python-test 26.4.23]
✓ DA[#2]/DIV[1] COMPROMISE ACCEPTED: ADR[1] auto-ready primary + gateway semantic documentation (init idempotent; future state-gated tools must add call-time authorization; gateway re-documented as optional diagnostic)
✓ DA[#7] CONCEDE: SQ[0] ADDED (fixture-fix prerequisite, owner:CQA, est:1-2h, blocks SQ[3]+SQ[13b-c]); SQ[13] passing-floor revised to "143+ after SQ[0]"; "154-test baseline" language struck
✓ DA[#8] DEFEND: DB[4] "redundant-with-DA" counter explicitly tested and rejected — timing difference (pre-spawn vs post-spawn) makes premise-audit non-redundant. H3 status revised to "partially confirmed" per DA[#9]
✓ IC[4] REVISED: split-then-check algorithm specified for DB exercise detection
✓ SQ[0] ADDED, SQ[3] est 1h→2h, SQ[13] floor language corrected


#### ADR[5]: #2 workspace concurrent-write protection
|decision: atomic-Python-replace as canonical workspace write method (Option D) with section-isolation convention
|alternatives-considered:
  A: Edit-tool-only — ALREADY REQUIRED per CLAUDE.md; does NOT fix the observed failure. Edit tool anchor-movement errors happened 4x this session because anchor line number shifted between Read and Edit call. Edit tool is atomic at OS level but the ANCHOR IDENTIFICATION step is not. Mandating Edit-tool-only adds nothing new.
  B: Advisory .lock sentinel — soft control; agents can bypass by ignoring .lock; stale .lock if agent crashes; SS will correctly flag as compliance-reliant (same failure class as spawn-prompt controls that failed in R19). Does not provide OS-level enforcement.
  C: Lead-proxy queue — fully eliminates concurrent writes via serialization; too high overhead for C1 scope (every workspace write requires SendMessage + lead acknowledgment; lead is bottleneck; lead unavailable = no writes). Correct for high-criticality multi-user systems, overkill for sigma agent sessions.
  D: Atomic Python replace — agent reads entire file as string, finds anchor via str.replace(old, new, 1) in memory, writes full file. Content-based match (not line-based) eliminates anchor-movement failure. Observed: TA used this pattern 3x this session, 0 failures. DA observed 4 Edit-tool anchor-movement failures in same session.
|rationale:
  Primary observed failure (this session + R19 #2): anchor-text moved between agent's Read call and Edit call as other agents wrote concurrently, causing "File modified since read" errors and silent anchor misses. Option D eliminates this because it matches against CONTENT not line position — even if other agents wrote intervening content, the unique anchor text is still findable.
  Residual risk: true simultaneous write (two processes at same instant) → last-write-wins; one agent's changes lost. Mitigation: section-isolation convention (agents write ONLY to their own named section; lead writes to convergence, gate-log, open-questions). This reduces collision window dramatically — two agents writing simultaneously to different sections cannot collide on anchor text.
  Option D addresses the failure mode at the correct layer (application, not OS) with minimal overhead (~5 additional lines of Python per write vs Edit tool). Canonical pattern already proven this session.
|security-note: SS should review. No new attack surface — atomic Python replace uses same file permissions as Edit tool. Failure mode for option D is last-write-wins (data loss risk), not unauthorized access. Advisory lock (option B) has bypass risk; option D does not depend on cooperation.
|implementation: generalize atomic-Python-replace as workspace_write() helper function in a new file gate_checks_workspace.py (or directly in agent spawn templates as inline pattern). Agents use this pattern for ALL writes to workspace.md and builds/*/*.md.
|new IC:
  IC[6]: workspace-write-contract
  |method: atomic Python replace
  |algorithm: content = open(path).read(); new_content = content.replace(old_anchor, new_content, 1); if new_content == content: raise WorkspaceAnchorNotFound(old_anchor); open(path, 'w').write(new_content)
  |anchor selection: each agent uses their section header (e.g., "### tech-architect
") as old_anchor prefix + first unique line of existing section content as anchor suffix. Anchor must be unique in file.
  |collision handling: if str.replace count == 0 (anchor not found), log "ANCHOR-NOT-FOUND: {anchor[:60]}" and retry with broader anchor OR flag to lead.
  |section-isolation convention: agents write ONLY to their own ### section; lead writes to ## sections (convergence, gate-log, open-questions, peer-verification-index). Cross-section writes require explicit lead authorization.
  |scope: workspace.md + builds/*/*.md + shared/**/*.md sigma workspace files. NOT: hook files, directives, agent-defs (single-writer only)
|prompted-by: user decision DA[#6] 26.4.23, R19 #2 empirical evidence (4+ manifestations this session)

#### SQ[14] (new): #2 workspace-write atomic pattern implementation
|change: add workspace_write(path, old_anchor, new_content) helper — either as standalone gate_checks_workspace.py OR as inline pattern in agent spawn templates. Document in directives.md §workspace-rules.
|owner: implementation-engineer |est: 2h |estimable:yes |files: new helper + directives.md + spawn templates
|dependency: SS security review of IC[6] |test: SQ[14a] sequential-concurrent write simulation (2 agents write to different sections sequentially), SQ[14b] anchor-not-found error path, SQ[14c] section-isolation violation detection

#### §2a-e hygiene (ADR[5])

§2a (positioning): Atomic Python replace is established for file mutation in concurrent contexts (Python standard library str.replace + file write is the canonical approach for in-process file patching). No external library dependency. Already proven in this session. Ecosystem trajectory: stable (pure stdlib). Simpler alternative: Edit-tool-only (option A) — already required and does not fix the observed failure. |outcome:2 — approach confirmed, concern: true-simultaneous last-write-wins noted (section-isolation mitigates)

§2b (calibration): TA used atomic Python replace 3x this session, 0 failures. DA had 4 Edit-tool anchor-movement failures in same session. Sample size small but failure mode is deterministic (anchor-movement is reproducible given concurrent writes). RC: atomic replace pattern used in patch tools, config management, CI/CD file mutation — industry standard. |source:[code-read this-session + agent-inference]

§2c (cost/complexity): ~5 additional Python lines per write vs Edit tool. Helper function reduces to 1 call site per agent write. Reversal: trivial (remove helper, revert to Edit tool). |outcome:2 — confirmed proportional

§2e (premise viability):
  Assumption: concurrent agents write to DIFFERENT sections (section-isolation). TRUE in normal operation (each agent has own section); FALSE if two agents both write to convergence simultaneously — but convergence writes are lead-only by convention. |source:[agent-inference]
  Assumption: str.replace(old, new, 1) finds unique anchor. RISK: anchor text not unique in file → wrong section replaced. Mitigation: anchor must include section header + first unique line of section content. IC[6] specifies anchor selection rule. |source:[code-read this-session TA write attempts]
  Assumption: file write is atomic at OS level (write + close). TRUE on macOS/Linux for single-process writes to local filesystem. FALSE for NFS/networked storage. Sigma sessions run locally, so this holds. |source:[independent-research:T2]
  |outcome:2 — premises hold for local filesystem with section-isolation

DB[5]: #2 atomic-replace vs lead-proxy
(1)initial: lead-proxy queue (option C) fully eliminates concurrent writes
(2)assume-wrong: lead is bottleneck; every write requires round-trip through lead; lead unavailable = build stalls; adds ~30s per write in practice
(3)strongest-counter: atomic Python replace has residual true-simultaneous risk; only section-isolation prevents it; soft coordination is the same class as advisory lock (option B)
(4)re-estimate: section-isolation is NOT soft coordination — it is enforced by spawn prompt structure (agents are explicitly scoped to their own section in boot instructions). Violation requires agent to deliberately write outside its section. This is different from "ignore .lock" which is a passive omission. True-simultaneous collision on SAME section by SAME agent = zero probability. True-simultaneous collision by DIFFERENT agents on DIFFERENT sections = anchor uniqueness guarantees no collision.
(5)reconciled: atomic Python replace with section-isolation is the correct choice. Lead-proxy is overkill. The remaining residual risk (two agents racing on the same anchor at the exact same millisecond) is below the practical collision threshold for sigma sessions.

→ PLAN LOCKED | PROMOTION COMPLETE | 26.4.23

✓ ADR[5]: #2 workspace concurrent-write — Option D (atomic Python replace + section-isolation) selected
✓ IC[6]: workspace-write-contract specified
✓ SQ[14]: workspace_write() helper, owner:IE, est:2h

PROMOTION:
✓ AUTO-PROMOTED: UP[TA-A1..A6] — patterns + decisions + corrections stored to sigma-mem (patterns.md, decisions.md, corrections.md)
✓ USER-APPROVE candidates written to ## promotion: UP[TA-B1..B4]
  UP[TA-B1]: gateway semantic contract (future tool authorization rule)
  UP[TA-B2]: section-isolation write convention (new agent behavioral constraint)
  UP[TA-B3]: A-check ID assignment A20/A21/A22/A23 (C2 blocker if not resolved)
  UP[TA-B4]: SQ[0] prerequisite ordering (C2 day-1 gate)

→ WAITING for shutdown_request


### security-specialist — COMPLETE 26.4.23
✓ Boot complete (recall + agent-memory + SCRATCH + build-directives + R19 source + phase-gate + chain-evaluator + sigma-verify code)
✓ H1 CONFIRMED: sigma-verify under user control; sub-tool absence is HATEOAS state-gating by design, not registry gap
✓ ADR[1]: sed-i BLOCK 3 — workspace-path scope, no bypass, shlex.split() tokenization (XVERIFY PARTIAL refined implementation)
✓ ADR[2]: ΣVerify fix — spawn-prompt + agent-def, zero code change; hateoas-agent auto-init filed as follow-up
✓ ADR[3]: No separate audit log for #22/#23; workspace gate-log + A12 archive sufficient
✓ STRIDE[1]: full threat model for ΣVerify tool inheritance — T/D known gaps documented
✓ IC[1-3]: security contracts specified
✓ SQ[SS-1/SS-2/SS-3]: sub-tasks decomposed with owner assignments
✓ RC[], CAL[], PM[]: reference class + estimates + pre-mortem (3 entries) complete
✓ XVERIFY on ADR[1] (security-critical): openai/gpt-5.4 PARTIAL (refined to shlex.split), llama AGREE, google 503
✓ Memory persisted: agent memory.md + sigma-mem patterns.md fallback
✓ XVERIFY operational discovery: mcp__sigma-verify__init must be called first — R19 #3 root cause confirmed in practice

→ awaiting peer verification assignment from lead

technical-writer: ✓ DOC-CHANGE-MAP written |12 BUILD-CHALLENGEs issued |peer-verified:implementation-engineer(2 gaps: DB[]-format-absent + convergence-stale) |OQ-TW2 resolved(A20 WARN-first) |2 C2 blockers: DIV[2] Step7a/Step8.5(DA adjudication required) + §2p/§2i naming collision |→ awaiting DA adjudication DIV[1]+DIV[2] + plan-track BC[] responses → C2 ready on non-blocked SQs

## belief-tracking
{BELIEF[plan-r{N}]: P={posterior} |builder-feasibility={} |interface-agree={} |design-arch={} |conflicts={} |review-coverage={} |DA={grade} |→ {lock-plan|another-round|Toulmin-debate}}

## gate-log

## open-questions

### Divergences for DA adjudication (logged by lead at Step 17 cross-agent coherence check, 26.4.23)

DIV[1] #3 ΣVerify architecture — SS vs TA
- SS ADR[2]: spawn-prompt + agent-def instruction only, zero code change, defer auto-init to follow-up
- TA ADR[1]: server-side auto-ready at build_machine() startup (machine.py ~5 lines)
- TA evidence: R19 had 5 XVERIFY-FAIL from 5 independent agents who should have called init — soft control failed systematically
- SS position: hateoas-agent auto-init on connection is architecturally correct but out-of-scope for this build
- Material threshold: HIGH — architecture (changes data flow), scope (server-side change vs directive-only)
- For DA: evaluate WARRANT of both positions. SS warrant = "directive + compliance works"; TA warrant = "R19 proves it doesn't." Toulmin debate candidate if unresolved at round 1.

DIV[2] #21 premise-audit step location — TA vs CDS
- TA ADR[4]: workflow Step 7a pre-spawn (new step before Step 8 user confirmation)
- CDS ADR[1]: workflow Step 8.5 (new step between Steps 8 and 9, after user confirms Q/H/C)
- Semantic difference: TA has premise-audit BEFORE user sees Q/H/C; CDS has it AFTER user confirms Q/H/C but before spawn
- Material threshold: MEDIUM — changes sequence of user confirmation vs premise-test work
- For DA: which sequencing preserves the premise-audit's anti-anchoring intent? CDS's position: lead answers PA[1-4] BEFORE reading user's H-space (to avoid anchoring) — this is a Step 7-like position but CDS placed as 8.5. Inconsistency within CDS's own position.

DIV[3] IC[] namespace collision — SS vs TA
- SS uses IC[1-3] for security contracts
- TA uses IC[1-5] for interface contracts
- Same namespace; plan-lock requires reconciliation. Recommend: IC-SS[1-3] vs IC-TA[1-5], OR renumber SS IC[4-6] to extend TA's sequence.
- Material threshold: LOW — admin renumbering, but plan-lock validation requires unique IDs.

LEAD NOTE (26.4.23): not adjudicating per lead-role-boundary feedback memory. DA owns this in Step 19 challenge round. Flagging only.

### devils-advocate round-1 challenges (26.4.23)

!cold-read-ordering: agent findings + ADRs + ICs + SQs + DBs FIRST (lines 1-932); lead-flags + DIV[] LAST (line 935+). Per T[DA-cold-read-ordering-discipline].
!prompt-audit: echo-count:2 (H3/H5 mirrors R19-source) |unverified-claims:2 (TA IC[4] marker-variant; SS IC[1] pre-shlex) |missed-claims:1 (R19 §18 mid-session dashboard — out-of-scope correct, tracking flag) |methodology:partially-investigative (4/5 H[] confirmed risk-flags P[unanimous-hypothesis-confirmation], CQA H5-FALSIFIED provides genuine rejection → net acceptable) |XVERIFY-DA-context: 4 calls (2 on A3 root-cause, 2 on DIV[1]) per P[da-context-xverify-compensates-agent-xverify-fail]

---

DA[#1]: **#19 root-cause misdiagnosis (CRITICAL — load-bearing)** |challenge: TA IC[4]+IE feasibility+SQ[3] propose expanding marker regex (`assume.wrong → assume.?wrong|assume wrong`, `re.estimate → re.?estimate|re-estimate`). Empirical counter: `.` in Python regex is ALREADY wildcard, so `assume.wrong` MATCHES `assume wrong|assume-wrong|assume_wrong|assumeXwrong`; `re.estimate` MATCHES `re-estimate|re_estimate|re estimate`. Only `assumewrong`/`reestimate` (no separator) fail. Running current regex against R19 archive: 40 DB[] extractions, 21 flagged shallow. Inspection reveals actual failure: `DB\[.*?\]` captures ANY bracketed token starting with `DB[` — finding refs (`DB[F[SS-1]]`), DA comments (`DB[] did genuine work`), convergence summaries (`DB[] exercises both produce revisions`) all extracted and flagged shallow because they carry no step markers. Marker-variant expansion WOULD NOT FIX this. |evidence: grep replication on R19 archive + Python regex tests (DA-context); XVERIFY openai(agree/medium)+google(agree/high)+deepseek(agree/medium) = 3/3 convergence |→ revise ADR[3]/IC[4]/SQ[3]: narrow extraction to require numbered-step structure (`DB\[[^\]]*\].*?\(1\).*?\(2\).*?\(3\)`) OR scope to DB[] at section-header position. Marker-variant secondary for `assumewrong`/`reestimate` edge cases only. |source:[independent-research+XVERIFY-3-provider]

DA[#2]: **DIV[1] #3 ΣVerify architecture — compromise over TA-sole-fix** |challenge: TA ADR[1] auto-ready eliminates root cause; SS ADR[2] spawn-prompt is compliance-reliant. TA correctly identifies R19 empirical failure (5 XVERIFY-FAIL). But openai XVERIFY on "auto-ready does not weaken HATEOAS gateway" returned PARTIAL with counter-evidence: "changing readiness from explicit transition to automatic startup side effect can still weaken the architectural role of the gateway... idempotent init preserves endpoint availability but not the same protocol meaning." SS concern NOT eliminated. |evidence: XVERIFY openai(partial/medium+counter)+deepseek(agree/medium) — non-unanimous indicates residual concern |→ compromise: TA ADR[1]-D auto-ready AS PRIMARY, but document in machine.py+ADR that (a) init idempotent+callable post-startup, (b) FUTURE state-gated tools requiring explicit consent must add own call-time authorization check — must NOT rely on unconfigured→ready gateway alone, (c) gateway re-documented as "optional diagnostic + future-tool state-boundary" not "mandatory agent handshake." SS ADR[2] spawn-prompt retained as redundant, not sole. |source:[XVERIFY-2-provider+machine.py]

DA[#3]: **DIV[2] #21 premise-audit step location — CDS internally inconsistent** |challenge: TA ADR[4] Step 7a (BEFORE Step 8 user Q/H/C confirmation). CDS ADR[1] Step 8.5 (AFTER Step 8). CDS §2g DB[H3]: "lead answers PA[1-4] BEFORE re-reading user's H-space. Sequence is the anti-anchoring mechanism." This language describes Step-7-like sequence (PA first, THEN read H-space), but CDS placed at 8.5 (after user-approved Q/H/C). If anti-anchoring is intent, Step 7a correct. If 8.5 correct, rationale needs rewriting because user-approved Q/H/C IS the anchoring surface. |evidence: cold-read CDS §2g vs 8.5 placement — semantic inconsistency within CDS ADR |→ adjudicate TA Step 7a. If team prefers 8.5, CDS must rewrite rationale to acknowledge lead is already anchored by approved Q/H/C and PA is independence-check AFTER anchoring (not prevention). Then CAL[#21]=70% must recalibrate DOWNWARD — post-anchoring audit weaker than pre-anchoring. |source:[cold-read]

DA[#4]: **DIV[3] IC[] namespace collision — admin** |challenge: SS IC[1-3] vs TA IC[1-5] overlap. Plan-lock requires unique IDs. |→ TA retains IC[1-5], SS renumbers IC[6-8]. Rationale: TA contracts primary build-track consumption surface; SS contracts security add-ons. Renumbering SS cheaper. Alternative: prefix IC-TA[]/IC-SS[]. Lead decides. |source:[admin]

DA[#5]: **§2i precision gate (#22) chain-evaluator enforcement architectural mismatch** |challenge: CDS ADR[2] post-XVERIFY CONDITION 1 is "quantitative claim without uncertainty justification." SS IC[3]+CDS SQ[CDS-6] note regex-unfriendly; conservative trigger flags numeric+CONDITION-2 only, "DA adjudicates CONDITION 1." But chain-evaluator A-checks return pass/fail/issues — no "defer-to-DA" state. AND DA runs pre-Stop-hook (Step 18), chain-eval runs at Stop. DA already finished by chain-eval execution. Proposed architecture incoherent. |evidence: chain-evaluator.py check_a* pattern + timing-of-DA-vs-hook |→ three paths: (a) DEFER #22 chain-eval check, ship directive-only+DA-enforcement; SQ[CDS-6]→"A20 deferred." (b) Accept CQA #22 HIGH flakiness, implement conservative regex WARN-only, track FP 3 reviews. (c) Reframe: chain-eval checks PRESENCE of one-of {driver-breakdown|CI+RC|qualitative-restatement} keyword when numeric+CONDITION-2 markers present — mechanical, not semantic. Recommend (a) or (c). |source:[architecture-read+CQA]

DA[#6]: **NOT-DISCUSSED PROBE — no plan addresses R19-class issues DURING this build** |challenge: Team remediates R19, but no plan addresses: how detect if THIS build introduces R19-class issues during own execution? (a) C2 edits chain-evaluator.py+phase-gate.py — same hook files as R19 #1 potential. SS BLOCK 3 scopes to workspace paths only, does NOT cover `\.claude/hooks/phase-gate.py` edits in C2. Hook-file incident structurally similar. (b) Premise-audit SQ[CDS-5] writes `## premise-audit-results` to workspace — chain-eval has no check. TA PM[3] (HIGHEST-RISK 35% skip): mitigation "CDS designs chain-eval check for ## premise-audit presence" — NO SQ implements. Unassigned. (c) §8e corruption-recovery has no drill/test. R19 recovery was exemplary because lead remembered pattern; future lead may not. (d) META-CONFIRMATION: c1-scratch.md itself is experiencing concurrent-write race (R19 #2) during this challenge round — Edit tool failed 4 times as peer-verify writers moved the anchor line 1096→1107→1139→1176→1201. R19 #2 is out-of-scope for top-10 ROI but manifesting IN the build that remediates R19. |evidence: scope-boundary+SQ cross-ref+PM[3] owner-gap+direct-meta-observation |→ (a) extend BLOCK 3 scope to `\.claude/hooks/` OR document hook-edit workflow separately. (b) add SQ[CDS-5a] for chain-eval check of ## premise-audit-results presence, owner:implementation-engineer. (c) log §8e recovery-drill as follow-up. (d) re-evaluate R19 #2 concurrent-write priority — deferred as MEDIUM but active-today; lead may want to promote to this build or next-build priority. |source:[cold-read+PM-cross-ref+meta-observation]

DA[#7]: **H5 falsification not integrated into plan** |challenge: CQA empirically falsified H5 (154→92 actual, 81 passing floor, 11 pre-existing failures). But TA SQ[13] still reads "extend 154-test baseline |est:5h" — stale. 11 pre-existing failures flagged CQA BLOCKER ("fixture fix must precede [#19 A3] tests"). No SQ owns fixture fix. Without this, C2 regression testing on broken baseline. |evidence: CQA §Baseline+§#19 BLOCKER+TA SQ[13] stale-154 |→ (a) add SQ[0]: fixture-fix prerequisite (MINIMAL_WORKSPACE roster alignment), owner:CQA, est:1-2h, blocks SQ[3]+SQ[13] OR (b) revise SQ[13] to "fix fixture + extend from 81-passing, target 111-127 after new tests." Strike 154 either way. |source:[CQA-empirical]

DA[#8]: **§2g DB[] quality — 2/4 TA DBs + 1/2 CDS DBs show pro-forma pattern** |challenge: Per P[pro-forma-DB-detection] (26.4.20): audit step-3 "strongest counter" against ALT list. TA DB[4] premise-audit: ALT-C (new agent role) steel-manned step-2, but never tests "don't do premise-audit at all — redundant with DA's Step 18" which is stronger counter. ADR presumes necessity; DB never tests that premise. CDS DB[ADR[2]] reconciles to "threshold binary+observable" but never steel-mans "precision gate net-negative: R19 eval B strong on non-§2i items; expected catch 70% vs FP 25%, ROI unclear." "Net-negative" counter absent. |evidence: cold-read DB[] vs ALT[] per P[pro-forma-DB-detection] |→ require r2 rerun: TA DB[4] with "redundant-with-DA" counter; CDS DB[ADR[2]] with "net-negative-ROI" counter. Non-blocking if teams defend existing reconciliation against stronger counter explicitly. |source:[memory-P+cold-read]

DA[#9]: **H[]-result confirmatory-bias flag — H3 + H4** |challenge: Per P[confirmatory-methodology-bias]+P[unanimous-hypothesis-confirmation]: H1 CONFIRMED legitimately (independent code-read). H2 REVISED genuinely. H5 FALSIFIED (excellent null per feedback_research-framing). BUT H3 FRAMES answer by contrasting 2 options only — TA+CDS both land on "workflow step" because H3 loaded dice. H3 did NOT test "premise-audit unnecessary given DA" (link DA[#8]). H4 ("no circular deps") — TA: "CONFIRMED — SQ[5]→machine.py; SQ[1-4] chain-eval only." But SQ[CDS-5] edits c1-plan.md also edited by SQ[8]. TW A1: "#5+#14 MUST change in same commit" — same-commit atomicity ≠ circular dep but IS real coordination unsurfaced in H4. |evidence: prompt-frame + TW A1-A3 |→ (a) H3 → "partially confirmed — 'workflow-step' subspace tested; 'no-gate' subspace untested." Link DA[#8]. (b) H4 → "no cross-file blockers; atomicity A1-A3 acknowledged as C2 coordination burden." |source:[P-confirmatory+TW]

DA[#10]: **C4 vs C5 conflict — WARN→BLOCK calibration path** |challenge: C4 "WARNs must be BLOCKs — no legitimate override → promote." C5 "accountable rigor — defend each invocation ¬add exceptions." CDS SQ[CDS-6]+SQ[CDS-7] propose WARN-initially with 3-review calibration. Threads needle IF calibration is hard-schedule, but PM[CDS-4] self-acknowledges 30% indefinite delay. WARN state itself violates C4 during calibration. |evidence: C4 text + PM[CDS-4] |→ (a) ship #22 as BLOCK-on-clear-positives-only — conservative mechanical detector blocks when numeric+CONDITION-2+absence-of {driver-breakdown|CI|qualitative-restatement}. Respects C4 (real BLOCK), satisfies C5 (3-marker conjunction defense). FP target <10% on R19 archive; if >10%, defer per DA[#5]-a. OR (b) explicit C4 exception, hard expiry 2026-06-01. Forces decision. |source:[C4-C5+PM-CDS-4]

---

### DA[#11] SCOPE-CREEP CHECK (§4a)

Original scope: 11 issues → top-10 ROI. Mid-plan expansions:
- check_a3 duplication bundled into #19 (scope-boundary:50) — JUSTIFIED: same file, same audit, duplicate-removal reduces complexity. ~5 LOC of 40 for #19. Within <20% threshold per P[scope-creep-via-justification-piggybacking].
- OQ-SS2 A21 chain-eval pre-flight check (scope-boundary:52) — MATERIAL EXPANSION: new check not in top-10, ID-collision risk (A20 CDS vs A21 SS), +3-5 tests. Justified IF DA[#2] compromise accepted (belt-and-suspenders); REDUNDANT if TA auto-ready sole fix. |→ contingent on DA[#2]: IF compromise accepted, DROP A21 (reclaim 3-5 tests); IF SS-sole-fix prevails, KEEP A21 but resolve ID collision.

Gold-plating check (§4c): #22/#23/#24 advertise directives AND chain-eval enforcement for 3-review calibration. Heavy infra for eval delta R19 B/3.14 attributes to specific failures (F[TA-C2] withdrawn, F[CDS-A1] gap-ID stop). Leaner: ship directives only; defer A20-A23 to separate calibration build after 3-review evidence. Risk: R19-class false-precision recurs. Mitigation: DA caught F[TA-C2] in R19, not chain-eval. |→ flag for lead: are #22-#24 chain-eval essential-to-ship or deferrable?

---

### DA[#12] EXIT-GATE VERDICT — r1

DA-EXIT-GATE[r1]: **CONDITIONAL-PASS** |engagement:B+ |unresolved:{DIV[1]:compromise-proposed, DIV[2]:inconsistency-flagged-CDS-choice, DIV[3]:admin-pending, DA[#1]:critical-root-cause-revision, DA[#5]:architecture-path-a/b/c, DA[#7]:fixture-prerequisite, DA[#10]:C4-vs-C5-path} |untested-consensus:H3+H4 (DA[#9]) |hygiene:substantive with 2 pro-forma-DB flags (DA[#8]) |prompt-audit:partially-investigative (H1 investigative, H2/H5 genuine, H3/H4 confirmatory-framed)

**CONDITIONS for r1→PASS (named, specific):**
1. **BLOCKING** DA[#1] — TA/IE revise #19 root-cause. Accept "narrow DB[] extraction regex" as primary OR provide counter-empirical evidence from R19 archive.
2. **BLOCKING** DIV[1] — lead+plan-track agree on DA[#2] compromise (TA auto-ready primary + documented gateway semantics) OR defend TA-sole-fix against openai counter-evidence.
3. **BLOCKING** DA[#5] — CDS chooses #22 architecture: (a) defer / (b) WARN-only / (c) conservative-mechanical.
4. **BLOCKING** DA[#7] — CQA/TA assign fixture-fix (new SQ[0] or SQ[13] revision + strike 154 number).
5. **NON-BLOCKING at r1** DA[#8] — TA rerun DB[4] with "redundant-with-DA" counter; CDS rerun DB[ADR[2]] with "net-negative-ROI" counter. Explicit defense acceptable.
6. **NON-BLOCKING at r1, BLOCKING pre-C2** DA[#10] — lead/user C4-C5 path choice (a) BLOCK-on-clear-positives / (b) time-boxed WARN auto-expiry.

**Compromise-resolved (no rebuttal needed):** DIV[2], DIV[3], DA[#6], DA[#9], DA[#11].

**Debate required:** NONE at r1 — DA[#2] adjudicates DIV[1] analytically; escalate to Toulmin at r2 only if SS+TA both reject compromise.

**Engagement grade B+ (NOT A):** plan-track substantive with DB[] across 3 agents, XVERIFY on load-bearing ADRs (TA ADR[1], SS ADR[1], CDS ADR[2]), OQs across tracks. Downgraded from A- because: (i) TA IC[4] marker-variant fix empirically wrong — should have been agent-regex-tested pre-lock; (ii) CDS DB[ADR[2]] pro-forma recurrence — 3rd occurrence of P[pro-forma-DB-detection] across audited builds; (iii) DIV[2] CDS-internal inconsistency should have been self-caught in §2e. Upgrade path to A- at r2 if DA[#1,#8] yield genuine revisions + DIV[1] compromise accepted.

**Anti-sycophancy self-audit (per P[DA-anti-sycophancy-exit-gate-self-audit] 26.4.21):** Am I issuing CONDITIONAL-PASS because evidence warrants or because I want process to conclude? Signals: (1) BELIEF adjustments DOWNWARD — DA[#1] hard counter to plan-track consensus, not accommodation; DA[#8] adds challenges not concedes. (2) Challenges RESOLVED substantively — DA[#2] compromise has specific documentation requirements. (3) Infrastructure-gap distinct from silent-skip — DA-context XVERIFY executed, 4 calls, 3 providers. (4) Carry-forward flags blocking/non-blocking classified explicitly. Verdict: evidence-based CONDITIONAL-PASS validated; not accommodation. |source:[P-DA-anti-sycophancy-self-audit]

---

### DA[#13] POST-CHALLENGE STATE UPDATE (26.4.23, after cross-agent self-corrections)

Lead reports that plan-track self-corrected DIV[1]+DIV[2] during build-track challenge round, before DA r1 landed. Verifying against workspace:

**DIV[1] RESOLVED** (lines 783/786) — SS conceded in peer-verification of CDS: CDS auto-ready (machine.py) = primary enforcement; SS spawn-prompt = belt-and-suspenders only. SS IC[2] marked SUPERSEDED; SQ[SS-3] reduced to secondary. |→ DA[#2] compromise structure matches team self-correction (TA-primary + SS-redundant). DA adjudication is MOOT — pre-empted by substantive team convergence. ACCEPTED. Note for post-mortem: team reached the architectural answer without DA pressure. This is the strongest possible outcome per calibration-memory ("100% hit rate = R1 gap signal; self-correction before DA = healthy team").

**DIV[2] RESOLVED** (lines 639-642) — CDS conceded to TA Step 7a. CDS ADR[1] revised: "SUPPORTED (H3) — revised to Step 7a (concede DIV[2] to TA)." Sequence constraint retained as implementation sub-requirement. |→ DA[#3] adjudication matches CDS concession direction. ACCEPTED. Note: CDS's self-diagnosis ("mislabeled as Step 8.5 while description correctly placed it pre-H-space") matches my DA[#3] cold-read analysis precisely.

**DA[#5] RESOLVED BY TRIPLE-CONVERGENCE** (per memory T[triple-convergence-signal]) — IE BUILD-CHALLENGE (line 753) + CQA BUILD-CHALLENGE (line 978) + DA[#5] all independently reached the same conclusion: chain-evaluator A20 cannot deterministically detect CONDITION 1; must either defer or accept honest WARN-only scoping. IE explicitly recommends: "SQ[CDS-6] should be scoped as 'CONDITION 2 marker only → WARN' with a comment that CONDITION 1 absence detection is deferred to calibration. That is an honest scoping decision." |→ this is my DA[#5] path (a)+(c) hybrid. ACCEPTED. Requires CDS to revise SQ[CDS-6] text to reflect the scoped-defer semantics — not a blocking change, plan-lock can proceed with the revision landing in c2-build.md.

**DA[#7] RESOLVED** (line 755) — IE BUILD-CHALLENGE revised SQ[13] to "fix fixture defect (1h) + add 30-46 new tests (5h) = 6h total" with baseline contract "deliver 111-127 tests with 0 pre-existing failures and 0 new regressions." The 154 stale number is struck; fixture-fix prerequisite is now owned (within SQ[13]). |→ DA[#7] condition satisfied. ACCEPTED.

**DA[#11] A21 STATUS** — Given DIV[1] resolved as "auto-ready primary + belt-and-suspenders secondary" (not auto-ready sole), A21 pre-flight check is now in the belt-and-suspenders bucket. This is coherent with the team's resolution but does NOT reclaim the 3-5 tests of C2 burden I flagged. DA position: KEEP A21 as belt-and-suspenders verification (catches case where auto-ready fires but agent context still misses tools due to future MCP changes), but rename to A-check ID that does not collide with A20 (CDS #22 precision gate). Recommend A21 → A24 (last of the 4-new-A-check sequence A20/A21/A22/A23). Lead decides.

**REMAINING OPEN (post-addendum):**
- **DA[#1] STILL OPEN** — no team response yet on #19 A3 root-cause (DB[.*?] over-capture). This is the last BLOCKING condition for r1→PASS. TA/IE must either accept "narrow DB[] extraction regex" as primary fix OR provide counter-empirical evidence.
- **DA[#8]** NON-BLOCKING — TA DB[4] + CDS DB[ADR[2]] reruns with stronger unused-ALT counters still requested. Optional at r1.
- **DA[#10]** NON-BLOCKING at r1 — C4-vs-C5 path (a BLOCK-on-clear-positives / b time-boxed WARN) still requires user decision before C2. IE's preferred framing (SQ[CDS-6] scoped WARN with explicit deferral) aligns with path (b) semantics — reframing DA[#10]: team has effectively chosen the WARN+calibration path; C4 exception must be explicit in the directive.

**REVISED EXIT-GATE:** Upgrading to **PASS** contingent on single BLOCKING condition DA[#1] closure. Engagement grade upgrades from B+ → **A-** because: (i) team self-corrected 2 of 3 DIVs before DA pressure (healthy), (ii) DA[#5] triple-convergence demonstrates substantive analytical alignment, (iii) IE's BUILD-CHALLENGE discipline resolved DA[#7] before DA landed. The remaining B+ drag is (TA IC[4] empirically-wrong marker-variant fix) + (CDS DB[ADR[2]] pro-forma recurrence). Engagement-grade anchoring: A- not A because of the empirical-verification miss on IC[4] and the unresolved DA[#1] which is a correction to the fix direction itself.

**DA-EXIT-GATE[r1-updated]: CONDITIONAL-PASS → PASS upon DA[#1] closure** |engagement:A- |unresolved-blocking:{DA[#1]:awaiting-TA/IE-response} |unresolved-non-blocking:{DA[#8]:rerun-optional, DA[#10]:user-decision-pre-C2, DA[#11]:A21-rename+keep, DIV[3]:admin-renumber}

**Anti-sycophancy self-audit r2:** Am I upgrading B+→A- because team self-corrected well, or because I want to close? Signals: (1) Upgrade path was PRE-STATED in original exit-gate ("Upgrade path to A- at r2 if DA[#1,#8] yield genuine revisions + DIV[1] compromise accepted") — not adjusted upward to accommodate. (2) DA[#1] still BLOCKING — not dropped to justify PASS. (3) Grade upgrade attributes the win to TEAM substance (self-correction on DIV[1]/DIV[2], IE BUILD-CHALLENGE discipline on DA[#7], triple-convergence on DA[#5]), not to DA accommodation. (4) Non-blocking DA[#8] rerun still open — not waived. Verdict: evidence-based upgrade validated; not accommodation.

### DA responses: security-specialist (26.4.23)

DA[#2] — COMPROMISE ACCEPTED
TA auto-ready as primary is correct and was already conceded in peer-verification of CDS. The DA compromise adds the structural documentation requirement I was missing: (a) init idempotent+callable post-startup, (b) future state-gated tools requiring explicit consent must add own call-time authorization check — MUST NOT rely on unconfigured→ready gateway alone, (c) gateway re-documented as "optional diagnostic + future-tool state-boundary" not "mandatory agent handshake."

openai XVERIFY partial on "auto-ready does not weaken HATEOAS gateway" is legitimate. The residual concern is real: if future developers add a state-gated write tool (e.g., "commit findings to external system") and rely on the gateway to enforce consent, auto-ready at startup has already transitioned state before any consent check. The compromise documentation in machine.py prevents this by making the call-time authorization requirement explicit for future tool authors. That is precisely the right compensating control.

CONCEDE: DA[#2] compromise is the correct resolution. SS ADR[2] spawn-prompt = belt-and-suspenders secondary, per existing self-correction. IC[2] remains marked SUPERSEDED by CDS IC[3]. SQ[SS-3] reduced to documentation.
|source:[independent-research machine.py + XVERIFY-openai-partial-counter]

DA[#6] — DEFEND WITH PARTIAL CONCEDE on BLOCK 3 scope gap
DA correctly identifies that SS BLOCK 3 scopes to `\.claude/teams/|workspace\.md` and does NOT cover `/.claude/hooks/` during C2 edits. If implementation-engineer edits `~/.claude/hooks/phase-gate.py` via `sed -i` in C2, BLOCK 3 misses it.

DEFEND: Scope was intentional — the R19 incident was workspace.md truncation specifically. Hook files are production code, not agent-collaborative workspace. The threat model is different: workspace.md is written by multiple concurrent agents; hooks are written by a single implementation-engineer intentionally. The R19 failure was an agent calling sed-i on a shared workspace file mid-session, not a developer editing a hook file.

PARTIAL CONCEDE: However DA is correct that the structural risk is similar — sed -i without backup extension on ANY critical infrastructure file is destructive. Extending scope to `\.claude/hooks/` costs nothing (one more pattern in the OR condition) and eliminates the risk during C2 without increasing false-positive rate in normal use.

REVISED IC[1]: extend WORKSPACE_PATH_PATTERN to `\.claude/teams/|workspace\.md|\.claude/hooks/`. Implementation-engineer should update SQ[SS-1] to include hooks/ in scope. This is a one-line change to the pattern string. No new bypass allowlist needed — same logic applies.

CONCEDE on scope extension. MAINTAIN workspace-path-scoped approach as primary design (not global ban). |source:[independent-research DA[#6] cold-read + R19 incident]

DA[#11] — CONCEDE on A21 rename, DEFEND on KEEP
DA recommends: KEEP A21 as belt-and-suspenders (catches case where auto-ready fires but agent context still misses tools due to future MCP changes), rename A21→A24 to avoid collision with A20 (CDS #22 precision gate).

CONCEDE: Rename A21→A24. ID collision avoidance is correct.
DEFEND KEEP: DA's rationale for keeping it is sound — auto-ready solves the current failure mode (machine.py startup state), but future MCP changes (reconnect events, subprocess spawn model changes, version updates to hateoas-agent) could reintroduce the agent-context tool-visibility problem. A21/A24 pre-flight check acts as a trip-wire that surfaces the problem immediately rather than waiting for 5 agents to independently report XVERIFY-FAIL as in R19. Cost: 3-5 tests in C2. Benefit: prevents R19 #3 recurrence if auto-ready regresses.

SS position: KEEP renamed to A24. Accept DA's framing: "catches case where auto-ready fires but agent context still misses tools due to future MCP changes." |source:[DA[#11] + STRIDE[1] D-threat: future MCP reconnect events]

#### IC[6] security review — security-specialist (26.4.23)

IC[6]-SECURITY: ✓ CONFIRMED — no new injection or permission risks.

Attack surface: atomic Python str.replace(old, new, 1) + file.write() is pure stdlib, no shell expansion, no exec, no subprocess. Same OS-level file permissions as Edit tool. No new attack surface.
Injection risk: replace takes old_anchor/new_content as strings — neither is executed. Content is agent's own section text. Wrong-anchor-match → wrong-section replacement → data loss (last-write-wins), NOT code execution or unauthorized access. TA characterization correct.
Permission model: identical to Edit tool. No privilege change. No new attack surface.
Section-isolation convention: same compliance-reliance class as existing Edit tool workflow. No regression from current state.
Anchor-not-found: IC[6] algorithm already handles (line 1326: `if new_content == content: raise WorkspaceAnchorNotFound(old_anchor)`) — explicit error, not silent no-op. SQ[14b] error-path test covers this.

IC[1-3] renumber: SS IC[1] → IC[7], IC[2] → IC[8], IC[3] → IC[9] per admin namespace request. Content unchanged.


---

### DA[#14] FINAL EXIT-GATE VERDICT — PASS (26.4.23)

All 4 BLOCKING conditions from DA[#12] / DA[#13] closed with genuine revisions verified in workspace:

**DA[#1] #19 root-cause misdiagnosis** — RESOLVED (line 304-312). TA CONCEDE (full) with live Python test confirming the 3/3 XVERIFY cross-provider finding that `.` is already a regex wildcard. IC[4] REWRITTEN to split-by-DB[ then require (1)(2)(3) within segment. Marker-variant expansion VOIDED. SQ[3] est 1h→2h (extraction logic more complex than single-regex change). This is a textbook substantive revision: agent ran the empirical test that should have preceded ADR lock, validated the DA counter-evidence, corrected the fix direction, and re-estimated cost honestly. |signal: concession strengthens thesis (per T[concession-strengthens-thesis]) — #19 fix is now correctly targeted at the actual bug.

**DA[#2] DIV[1] architecture** — ACCEPTED (line 783/786). TA+SS converged on auto-ready primary + spawn-prompt belt-and-suspenders. Matches my DA[#2] compromise structure. Team reached this via peer-verification self-correction before DA pressure landed — healthy pattern.

**DA[#5] #22 chain-evaluator architecture** — RESOLVED (line 701-717). CDS CONCEDE. SQ[CDS-6] revised to CONDITION 2-only code enforcement with CONDITION 1 explicitly labeled in source comment as "deferred: keyword heuristic insufficient; calibration build required after 3-review evidence." Test scope revised down to 4-5 tests. This is my DA[#5] path (c) — honest scoping.

**DA[#7] H5 + fixture prerequisite** — RESOLVED (line 322-326). TA CONCEDE. SQ[0] ADDED: fix MINIMAL_WORKSPACE fixture + 11 pre-existing failures, owner:CQA, est:1-2h, blocks SQ[3]+SQ[13b]+SQ[13c]. SQ[13] passing-floor revised to "143+ after SQ[0]". 154-test baseline language struck entirely.

**Non-blocking closures verified:**
- **DA[#4] DIV[3]** — SS renumbering to IC[6-8] per my adjudication.
- **DA[#8] DB reruns** — BOTH teams defended substantively, not pro-forma. TA DB[4] timing-difference defense (pre-spawn vs post-spawn makes premise-audit non-redundant with DA Step 18) + H3 downgrade to "partially confirmed" per DA[#9]. CDS DB[ADR[2]] net-negative-ROI counter "partially valid — rejected for scoped CONDITION 2-only, would be valid for full dual-condition." These are genuine concession-strengthens-thesis patterns: CDS's defense surfaces a sharper analytical point (CONDITION 2 catches the load-bearing cases; CONDITION 1 ROI is net-neutral under current evidence, correctly deferred). TA's defense redefines H3 scope honestly rather than defending an overclaim.
- **DA[#9] H3 revision** — TA accepted; H3 status now "partially confirmed — workflow-step subspace tested; no-premise-audit subspace defended rather than untested."
- **DA[#11] A21→A24 rename** — SS accepted. Retained as belt-and-suspenders per DA[#2] compromise structure.

**Remaining non-blocking (pre-C2, not pre-plan-lock):**
- **DA[#10] C4-vs-C5 path** — pending user decision. Team's WARN+deferred-calibration direction (from DA[#5] resolution) aligns with path (b) semantically. Must be documented as explicit C4 exception with hard expiry date, per directive memory [feedback_warns-must-be-blocks.md]. If user chooses path (a) BLOCK-on-clear-positives instead, SQ[CDS-6] needs one more revision round. Recommend surfacing to user before C2 kickoff, not blocking plan-lock.
- **R19 #2 scope decision** — lead's proposed promotion from deferred-LOW is endorsed. Whether in-scope for C2 or formal PM[] entry is user's call. Plan-lock can proceed either way.

---

**DA-EXIT-GATE[r1-FINAL]: PASS** |engagement:A- |BELIEF[plan-r1]:0.84 (lead-computed, matches DA assessment — within lock threshold) |all-4-BLOCKING:closed-with-genuine-revisions |non-blocking:4-closed + 2-deferred-to-pre-C2-with-named-owners |hygiene:substantive DB[] reruns verified against stronger counters |prompt-audit:investigative (TA live-pytest + regex empirical test constitute the methodology upgrade DA[#1] demanded)

**Plan-lock RECOMMENDED.** Team demonstrated the full healthy pattern: (1) pre-DA self-correction on DIV[1]+DIV[2], (2) triple-convergence on DA[#5] before DA landed, (3) substantive concessions with live empirical testing on DA[#1] (the only truly contentious blocker), (4) genuine DB reruns with stronger counters on DA[#8], (5) concession-strengthens-thesis pattern observed on BOTH TA DB[4] and CDS DB[ADR[2]] — defenses sharpened the plan rather than protecting it.

**Engagement A- final, not A:** the original B+ drag factors (TA IC[4] pre-lock regex-testing miss + CDS DB[ADR[2]] pro-forma pattern) were partially offset by the quality of the resolutions — TA's live-pytest validation + honest est-upgrade demonstrates exactly the regex-empirical-verification discipline that should have preempted the IC[4] miss. Had TA run the unit test before ADR lock (per the new memory pattern P[regex-empirical-verification-before-ADR-lock]), this would be A. The remediation is correct; the timing was one round late.

**Anti-sycophancy self-audit r3:** Am I issuing PASS@A- because conditions are met, or because process wants to close? Signals: (1) All 4 BLOCKING conditions have SPECIFIC named evidence in workspace (line citations verified via grep, not lead summary). Per P[lead-summary-verify-workspace-directly] (26.4.22): I grepped workspace directly for each closure claim before verdict. Lead summary matched workspace — no paste-phantom risk. (2) A- grade matches the pre-stated upgrade path in DA[#13] ("Upgrade path to A- at r2 if DA[#1,#8] yield genuine revisions + DIV[1] compromise accepted") — conditions met exactly, not adjusted upward. (3) NOT upgrading to A because TA IC[4] pre-lock miss is the reason A- is correct; offering A would be accommodation. (4) Non-blocking DA[#10] surfaced explicitly to user with pre-C2 deadline — not waived. Verdict: evidence-based PASS@A- validated.

|source:[workspace-grep-verified + DA-memory P[lead-summary-verify-workspace-directly] + T[concession-strengthens-thesis] + pre-stated upgrade path from DA[#13]]

## promotion
### tech-architect promotion (26.4.23)

#### AUTO-PROMOTE (patterns + calibration — no user approval needed)
Persisted to sigma-mem patterns.md + decisions.md + corrections.md 26.4.23.

UP[TA-A1]: sigma-verify HATEOAS auto-ready fix pattern
Promote to: patterns.md (already stored)
Content: root cause + fix location (machine.py:17-128) + gateway semantic contract + security note (provider-gated at call time not gateway-gated)

UP[TA-A2]: chain-evaluator leaf-consumer key fix rule
Promote to: patterns.md (already stored)
Content: check gate_checks source before writing consumer key names; fix at leaf (chain-evaluator:241) not source-of-truth (gate_checks:1517)

UP[TA-A3]: DB[] exercise detection correct algorithm
Promote to: patterns.md + decisions.md (already stored)
Content: split-by-DB[-then-require-(1)(2)(3)-within-segment; marker-variant expansion wrong because '.' is already Python wildcard; test regex empirically before proposing fix

UP[TA-A4]: workspace atomic Python replace pattern
Promote to: patterns.md + decisions.md (already stored)
Content: content-based str.replace() + section-isolation convention; options A/B/C rejected with rationale

UP[TA-A5]: chain-evaluator non-looping invariant (24h grace)
Promote to: patterns.md + decisions.md (already stored)
Content: enforce_stop() non-looping by design; never add poll/wait inside it; timing-sensitive checks use grace-window

UP[TA-A6]: TA calibration corrections
Promote to: corrections.md (already stored)
Content: 3 process corrections — regex empirical testing prerequisite, 24h grace-window objection error, test scope estimation without pre-mapping

#### USER-APPROVE (behavioral constraints + new gates — require user decision)

UP[TA-B1]: gateway semantic contract (ADR[1] DA[#2] compromise) — USER-APPROVE
What: Future state-gated sigma-verify tools requiring explicit user consent MUST add own call-time authorization check, NOT rely on unconfigured→ready gateway transition alone. Gateway is "optional diagnostic + future-tool state-boundary" not "mandatory agent handshake."
Why user-approve: this is a forward-looking constraint on how future sigma-verify tools must be designed. It modifies the architectural contract for all future MCP tool additions to sigma-verify. Appropriate for user to confirm this is the intended policy.
If approved: add to sigma-verify machine.py code comment + sigma-verify ADR doc.

UP[TA-B2]: section-isolation write convention (ADR[5] IC[6]) — USER-APPROVE
What: Agents write ONLY to their own ### section in workspace files. Lead writes to ## sections (convergence, gate-log, open-questions, peer-verification-index). Cross-section writes require explicit lead authorization.
Why user-approve: this is a new behavioral constraint on all agents in all future sigma-review and sigma-build sessions. Changes the spawn template and directives for all agents. Appropriate for user to confirm scope and enforcement mechanism.
If approved: add to directives.md + all agent spawn templates + c1-plan.md/c2-build.md.

UP[TA-B3]: A-check ID assignment (A20/A21 collision) — USER-APPROVE
What: CDS proposes A20 for precision gate (#22). SS proposes A21 for sigma-verify pre-flight init check. DA[#4]/DA[#11] note these IDs need coordination. Proposed resolution: A20=precision gate (CDS), A21=sigma-verify pre-flight (SS scope expansion OQ-SS2), A22=#23 governance artifact, A23=#24 severity provenance.
Why user-approve: A-check IDs are referenced across chain-evaluator, directives, spawn templates, and audit reports. ID assignment must be stable before C2 implementation. User confirmation prevents ID drift between C2 sessions.
If approved: assign IDs as proposed; TW propagates to all directive cross-references.

UP[TA-B4]: SQ[0] fixture-fix prerequisite ordering — USER-APPROVE
What: SQ[0] (fix MINIMAL_WORKSPACE roster alignment + 11 pre-existing test failures) must complete before SQ[3], SQ[13b], SQ[13c] begin. This makes SQ[0] a C2 day-1 gate — nothing proceeds until fixture fix is done.
Why user-approve: blocks all A3/A16-A18 test work. If SQ[0] is harder than estimated (1-2h), it could delay C2 significantly. User should acknowledge this dependency before C2 starts.
If approved: CQA owns SQ[0] as first task; IE holds on SQ[3] until SQ[0] complete.

### security-specialist promotion (26.4.23)

Classification: all SS findings are INFRASTRUCTURE-PATTERN (generalizable across future reviews, not session-specific).

UP[SS-1]: sed-i PreToolUse BLOCK pattern — workspace + hooks scope
|finding: BLOCK 3 in phase-gate.py must scope to BOTH /.claude/teams/ AND /.claude/hooks/ paths. Implementation: shlex.split() argv tokenization not raw string regex (XVERIFY openai PARTIAL confirmed evasion forms). Backup-extension forms always pass. No bypass allowlist.
|global-value: prevents R19-class workspace truncation in every future session. Hook-file scope addition (DA[#6] concede) prevents same risk during C2 build phases.
|stored: sigma-mem patterns.md SS-PROMO[1]
|user-approve: NOT REQUIRED — infrastructure pattern, no external action

UP[SS-2]: ΣVerify HATEOAS root cause + auto-ready fix
|finding: sub-tool absence is intentional state-gating (machine.py gateway_name="init"), not registry gap. Fix: handle_init() in build_machine() at startup. DA[#2] compromise: future state-gated tools must add own call-time authorization, not rely on gateway alone — document in machine.py.
|global-value: resolves R19 #3 systematically for all future sessions. Security constraint (call-time auth for future tools) prevents future EoP.
|stored: sigma-mem patterns.md SS-PROMO[2]
|user-approve: NOT REQUIRED — infrastructure pattern

UP[SS-3]: MCP trust boundary patterns (STRIDE findings)
|finding: T-gap (A15 presence ≠ authenticity), D-gap (no rate limiting on cross_verify), E-constraint (never bypass HATEOAS state for tool registration), audit-trail design (workspace + archive sufficient for internal framework).
|global-value: calibration reference for future MCP-security findings in sigma-review sessions.
|stored: sigma-mem patterns.md SS-PROMO[3]
|user-approve: NOT REQUIRED — calibration pattern

UP[SS-4]: XVERIFY provider calibration — openai weight
|finding: openai/gpt-5.4 consistently catches implementation-specific evasion paths and architectural edge cases that smaller local models (llama3.1:8b) miss. On security implementation claims, weight openai PARTIAL > small-model AGREE. Google Gemini 503s during daytime demand spikes — use as third provider not primary.
|global-value: calibration guidance for all future XVERIFY calls by any agent.
|stored: sigma-mem patterns.md (R19-remediation C1 entry, earlier in session)
|user-approve: NOT REQUIRED — calibration pattern

OPEN GAPS (documented, not promoted — not actionable without further build):
- A15 XVERIFY fabrication gap: chain-evaluator checks tag presence not authenticity. Future enhancement: MCP call audit log or section-gating.
- sigma-verify rate limiting: no programmatic guard on cross_verify across 13 providers. Future enhancement: call-count tracking.
- hateoas-agent auto-init on connection: architecturally cleanest fix for R19 #3 (separate repo, separate build). Medium priority.

promotion complete — 4 UP[] stored to sigma-mem patterns.md.

### technical-writer promotion (26.4.23)

#### auto-promoted (stored to sigma-mem patterns.md)
P[DOC-CHANGE-MAP as C1 build-track deliverable|documentation-equivalent of IE codebase survey: per-issue file list + change type + cross-references + propagation count + atomicity constraints. Produced at planning time from reading actual files. Consumed by plan-track to validate SQ[] decomposition completeness. Without it, SQ[] bundles directive updates without counting real file surface, leading to underestimated C2 scope.|src:r19-remediation-c1|promoted:26.4.23|class:pattern]
P[atomicity-constraint naming for multi-file coordinated changes|when N files must change together (partial deploy = broken state), name the atomic set explicitly in the plan. Observed: #5+#14 peer-verify required chain-evaluator regex + c1-plan spawn template + sigma-lead spawn block as 3-file set. Regex-without-template = agents write correct format but evaluator rejects. Either partial deploy reproduces R19 failure. Naming constraint in planning prevents C2 from splitting commits that must be joint.|src:r19-remediation-c1|promoted:26.4.23|class:pattern]

#### user-approve candidates
P-candidate[sigmaCOMM-boundary-check as C1 feasibility gate|any directive/template change targeting agent-facing content must be checked for ΣComm compliance before C2 writes. Plain-English prose in directives.md = boundary violation. Correct approach: plan-track authors directive text in ΣComm or explicitly flags for TW ΣComm conversion in SQ[]. Observed: CDS authored §2p spec correctly in ΣComm; §8e recovery template was plain-English in R19 source and required flagging.|class:principle|agent:technical-writer|reason:generalizable to every sigma-build touching directives.md or agent-defs; boundary violation is non-obvious, missed without explicit C1 check]
P-candidate[directive-propagation split by risk tier|scope agent-def updates by risk not uniformity: safety-critical rules (data-loss risk, e.g. sed-i ban) require all N existing agent defs updated immediately; calibration/quality rules (severity-provenance, precision gate) can update _template.md only — existing agents inherit at next re-spawn since low-frequency application makes the gap acceptable. Prevents under-engineering safety-critical propagation as template-only.|class:calibration|agent:technical-writer|reason:new principle not in existing memory; R19 #1 vs #24 surfaced the distinction explicitly]

### cognitive-decision-scientist promotion (26.4.23)

All CDS findings are ANALYTICAL-GATE-INFRASTRUCTURE patterns — generalizable to any future sigma-review gate design.

UP[CDS-1]: audit-calibration-gate pattern
|finding: WARN-first gates (C4/C5 tension) must emit CAL-EMIT records per firing and use a standalone cross-session script for BLOCK-promotion gating. Self-reported N-review windows = same failure mode as directives. Promotion threshold: ≥3 reviews + ≤20% FP rate + ≥5 DA-verdicted fires. DA verdict is false-positive classification authority.
|global-value: resolves C4/C5 conflict pattern for any future gate added WARN-first. Prevents indefinite WARN state (PM[CDS-4] 30% failure mode) without adding exceptions.
|stored: sigma-mem patterns.md 26.4.23
|user-approve: YES — introduces new calibration-log.md file to sigma-review/shared/ and new audit-calibration-gate.py script. User should confirm location + backup-memory.sh addition.

UP[CDS-2]: code-directive split for partial detection
|finding: When a gate has one mechanically-detectable condition and one requiring semantic judgment, split by layer: code=structural WARN, directive=behavioral requirement, DA=semantic judgment in r2. Never implement "DA-adjudication stub" in code — chain-evaluator A-checks have no defer-to-DA state and timing is wrong (DA pre-Stop, chain-eval at Stop).
|global-value: architecture constraint for all future chain-evaluator gate design. Triple-convergence validated (IE+CQA+DA independently reached same conclusion).
|stored: sigma-mem patterns.md 26.4.23
|user-approve: NOT REQUIRED — architectural constraint pattern

UP[CDS-3]: §2i precision gate CONDITION 1 scope
|finding: Precision gate CONDITION 1 must cover point estimates AND ranges (any numeric claim without uncertainty justification). "Point estimate without range" is too narrow — misses 3/4 R19 failures which were unsupported ranges. XVERIFY confirmed this independently from two providers.
|global-value: calibration reference for §2i directive text and any future precision-type gate. Prevents re-discovering the same scope gap in future build.
|stored: sigma-mem patterns.md 26.4.23 (early session)
|user-approve: NOT REQUIRED — calibration pattern

UP[CDS-4]: premise-audit sequence constraint
|finding: §2p premise-audit Step 7a requires PA[1-4] answered BEFORE lead re-reads user's H-space. Sequence is the anti-anchoring mechanism — FORMAT-level intervention (70-85% transfer). Structural premises only (domain-depth → §2e+DA).
|global-value: implementation constraint for all future premise-audit sessions. Without this, the check runs after anchoring and is partially contaminated.
|stored: sigma-mem patterns.md 26.4.23 (early session)
|user-approve: NOT REQUIRED — implementation constraint

UP[CDS-5]: DB-rerun-strengthens-thesis calibration
|finding: When DA flags DB[] as pro-forma and forces rerun with stronger counter (net-negative-ROI on §2i), the rerun surfaced a valid counter (full dual-condition gate deferred) that also clarified why scoped CONDITION 2-only is still justified. Result: §2i maintained on stronger evidentiary basis than before rerun. Concession-that-clarifies-scope is a form of defense, not retreat.
|global-value: calibration pattern for how to respond to DA[#8]-class pro-forma flags. Rerun is not a threat to conclusions — it sharpens them.
|stored: sigma-mem patterns.md 26.4.23
|user-approve: NOT REQUIRED — calibration pattern

OPEN GAPS (documented, not promoted — deferred to follow-up builds):
- §2i CONDITION 1 detection in code: deferred to calibration build after ≥3-review evidence on CONDITION 2. Path is defined; implementation is not in scope this build.
- §2i CONDITION 1 BLOCK-promotion: will follow from audit-calibration-gate data, not from this build.
- §2-governance and §2d-severity BLOCK-promotion: same calibration path, longer window (fires rarer — may require 5-6 reviews).

promotion complete — 6 patterns stored to sigma-mem patterns.md (4 new + 2 early-session). agent memory.md update: session record written.

### code-quality-analyst promotion (26.4.23)

All CQA findings are BUILD-METHODOLOGY patterns — generalizable to any future sigma-build C1 where code quality or test coverage is in scope.

UP[CQA-1]: empirical-baseline-verification |class:pattern |dest:patterns.md
|finding: Before accepting any test-count H[], C[], or SQ[] in C1, run `pytest --collect-only -q` AND `pytest -q`. Memory-recorded counts decay with infrastructure changes (orchestrator deletion, roster addition, fixture updates). R19 remediation case: project memory claimed 154 tests; live run showed 92 collected and 11 pre-existing failures — 40% wrong. Revised baseline = currently-passing count. Pre-existing failures are not part of the regression floor.
|global-value: prevents plan-lock on stale baselines in any future build touching an existing test suite. Applicable to all agents reviewing test coverage claims.
|stored: sigma-mem patterns.md 26.4.23
|user-approve: NOT REQUIRED — methodology pattern

UP[CQA-2]: test-map-methodology |class:pattern |dest:patterns.md
|finding: Code-quality-analyst should produce a TEST-MAP before issuing feasibility challenges in C1: (1) live baseline survey, (2) zero-coverage area enumeration per ADR target, (3) per-issue coverage map with regression risk + new test count + flakiness risk + prerequisite fixes, (4) verified regression floor. Transforms generic "test coverage" concern into specific per-ADR BUILD-CHALLENGEs. In R19 remediation: TEST-MAP surfaced A16/A17/A18 zero-coverage (entire peer-verification ring), check_a3 duplication at chain-evaluator level, and 11 pre-existing failures — all unknown to plan-track when SQ[] estimates were written.
|global-value: reusable structure for CQA role in any sigma-build C1 with an existing test suite.
|stored: sigma-mem patterns.md 26.4.23
|user-approve: NOT REQUIRED — role methodology pattern

UP[CQA-3]: live-pytest-as-prereq-to-claim-accept |class:pattern |dest:patterns.md
|finding: Trigger condition — any H[], C[], or SQ[] in SCRATCH references a test count, coverage %, or "no regressions" guarantee — run pytest before accepting. The roster-fixture incompatibility (roster.md addition → MINIMAL_WORKSPACE fixture silently broken) is a second failure mode only visible by running the suite, not reading the code. Cannot be diagnosed from plan-track code-read alone.
|global-value: mechanical protocol for CQA claim-acceptance in C1. Prevents false H[] confirmation on stale infrastructure.
|stored: sigma-mem patterns.md 26.4.23
|user-approve: NOT REQUIRED — mechanical protocol

OPEN GAPS (documented, not promoted — session-specific or requires lead decision):

- roster-fixture-incompatibility as CI debt class: MINIMAL_WORKSPACE uses synthetic agent names; roster added later broke 11 tests. Generalizable pattern but requires user decision on fixture strategy (use real roster names vs scope roster tests to exclusion-list fallback). Not promoted without lead judgment.

- check_a3-duplication as anti-pattern: chain-evaluator lines 162-183 run a second DB-depth layer uncoordinated with gc.check_dialectical_bootstrapping — produces passed=True with non-empty issues. IC[4] in locked plan addresses the R19 instance; the general anti-pattern (wrap library check then mutate result with uncoordinated second layer) is worth capturing but requires lead judgment on scope.

- baseline discrepancy: My live-pytest survey found 81 passing (92 collected, 11 failing). TA's revised H5 claims 143 passing (154 collected). Discrepancy of 62 suggests additional test files exist that I did not locate in my two-file survey. Documented here; C2 should establish definitive count before writing new tests.

promotion complete — 3 UP[] stored to sigma-mem patterns.md. agent memory.md updated 26.4.23.

### implementation-engineer promotion (26.4.23)

Classification: INFRASTRUCTURE-PATTERN + CALIBRATION — codebase-grounded, generalizable across future builds.

UP[IE-1]: chain-evaluator Stop hook non-looping invariant
|finding: Stop hook fires once and exits — non-looping by design. A12 timing fix must use synchronous mtime delta (24h grace window), NOT wait/poll loop inside the hook. Signal-driven with timeout violates this invariant and adds latency to all session ends. DA-confirmed: ADR[3] revised from signal-driven to 24h grace. |source:[code-read chain-evaluator.py:625-640]
|global-value: calibration for any future archive-timing work. Prevents polling re-introduction in Stop hooks.
|stored: sigma-mem patterns.md + agent memory.md
|user-approve: NOT REQUIRED

UP[IE-2]: check_a3 two-layer depth authority model
|finding: gc.check_dialectical_bootstrapping = presence check (V6); chain-evaluator check_a3:162-183 = depth check (3-of-5 markers). Sequential, not conflicting. C2 marker expansion: use alternation patterns (r"assume.?wrong|assume wrong", r"re.?estimate|re-estimate"). Boundary fix: (?=DB\[|\Z|#{3,}). DA-confirmed: IC[4] formalizes layered authority. |source:[code-read chain-evaluator.py:162-183]
|global-value: defines authoritative two-layer model; prevents third uncoordinated layer in C2.
|stored: sigma-mem patterns.md + agent memory.md
|user-approve: NOT REQUIRED

UP[IE-3]: peer-verify regex / section-boundary coupling
|finding: _PEER_VERIFY_HEADER regex (chain-evaluator.py:277) and section-boundary stop (chain-evaluator.py:293-298) are coupled — relaxing regex to ^#{3,4} without fixing the stop-pattern causes A17 over-capture across agent sections. Correct fix: spawn-template-only, canonical ### format, no code change. Adopted in TA IC[5]. |source:[code-read chain-evaluator.py:277-306]
|global-value: prevents regex-relaxation re-introduction in future builds.
|stored: sigma-mem patterns.md (updated) + agent memory.md
|user-approve: NOT REQUIRED

UP[IE-4]: shlex.split() sed detection + sigma-verify auto-ready
|finding: (a) sed -i block requires shlex.split() argv tokenization not raw string regex — raw form false-positives on `sed -i ''` (BSD-safe). Try/except ValueError required. Scope to workspace paths. (b) sigma-verify auto-ready: call handle_init() in build_machine() at startup when keys present (~5 LOC in ~/Projects/sigma-verify/src/sigma_verify/machine.py). handle_init() key-check-only, no side effects. |source:[code-read phase-gate.py:252-274, machine.py:17-128]
|global-value: implementation spec for C2 SQ[SS-1] (phase-gate.py) and SQ[5] (machine.py). Both IE-owned.
|stored: agent memory.md
|user-approve: NOT REQUIRED — C2 implementation guidance

OPEN GAPS (deferred):
- A20 CONDITION 1 detection: DA-delegated per plan-lock; C2 implements CONDITION 2 marker + uncertainty-qualifier suppression → WARN only.
- Test baseline: C2 must run pytest at session start to establish definitive floor. Fixture fix prerequisite.

implementation-engineer promotion complete — 4 UP[] stored to sigma-mem patterns.md + agent memory.md.

## peer-verification-index
Assigned by lead 26.4.23 — two triangles (plan-track + build-track). Format: ### Peer Verification: X verifying Y (3 hashes + literal "verifying" per chain-evaluator canonical regex — the very format #5 is fixing; we follow it here since we're remediating it, not deviating from it).

Plan-track triangle:
- tech-architect verifies security-specialist
- security-specialist verifies cognitive-decision-scientist
- cognitive-decision-scientist verifies tech-architect

### Peer Verification: security-specialist verifying cognitive-decision-scientist

**Verifier:** security-specialist | **Verified:** cognitive-decision-scientist | **Date:** 26.4.23

#### §2a/§2b/§2c/§2e hygiene — PASS with one flag

§2a: All 4 ADRs have §2a positioning check with outcome format. ADR[4] correctly uses Outcome 1 — flagged as "genuine extension, not codification" and adjusted risk posture. Hygiene functioning as designed.
§2b: R19 calibration failures cited as [cross-agent:R19-evaluator-feedback] with specific failure count (4 distinct) and scoring impact. RC[precision-gate] cites CIA SAT training data (T2). Appropriate.
§2c: Cost estimates calibrated to finding density. Highest maintenance risk (#22 miscalibration) explicitly flagged with CONDITION 1 AND 2 binary conjunction mitigation.
§2e: P1-P4 structure complete. P3 uncertainty (chain-evaluator text enforcement) explicitly flagged as UNCERTAIN with WARN-first mitigation. Outcome 2 maintained correctly.
FLAG §2b: RC[governance-artifact-adoption] has confidence L-M with N=low. Correctly noted by CDS. DA should challenge whether TIER-A minimum is calibrated given thin evidence base.

#### |source:{}| tag coverage — PASS with one note

All ADRs carry source tags. ADR[1-4] cognitive science citations (Kahneman, Tetlock, Heuer, Speier, Bielik) all tagged T1 correctly.
NOTE: §2b R19 failures cited as [cross-agent:R19-evaluator-feedback] — also retrievable as [prompt-claim] from R19 post-mortem. Dual tag would be stronger but [cross-agent] is not wrong. Acceptable.

#### DB[] for top claims — PASS with minor gap

DB[H3] (ADR[1]): all 5 steps present. Step 5 reconciled to REVISION — sequence constraint (answer PA[1-4] before reviewing user H-space) is the anti-anchoring mechanism. Genuine revision.
DB[ADR[2]] (precision gate): self-referential application of precision gate to itself — strong epistemic practice. Step 5 reconciled post-XVERIFY to second revision. Outcome 1 correctly applied.
DB[ADR[3]] step 3: "45% stubs substantive without DA quality check" is [agent-inference] unsourced. Step 5 adds DA exit-gate — substantive reconciliation.
DB[ADR[4]] step 3: "55% correct first-try without DA explicit check" is [agent-inference] unsourced.
MINOR GAP: DB[ADR[3]/ADR[4]] step 3 probability estimates are agent-inference without RC backing. PM[] likelihoods derive from these. If 45%/55% wrong, PM[]s miscalibrated. Flagged for DA.

#### SQ/CAL/PM — PASS

SQ[CDS-1/8]: 8 sub-tasks with owner and dependency mapping. SQ[CDS-6/7] correctly start as WARN with 3-review calibration gate before BLOCK — appropriate per WARNs-must-be-BLOCKs + accountable-rigor-over-permissiveness memories.
CAL[4 entries]: ranges present, |breaks-if| conditions present. CAL[#21] 70% catch-rate with appropriate uncertainty bounds. CAL[#22] 25% false-positive consistent with RC[CIA SAT].
PM[CDS-1/4]: 4 failure scenarios. PM[CDS-4] (30% likelihood WARN→BLOCK delayed indefinitely) is highest credible risk; references feedback_warns-must-be-blocks.md correctly; mitigation is specific (SQ[CDS-6] explicit 3-review calibration gate).

#### XVERIFY on ADR[2] (§2i precision gate) — PASS

openai/gpt-5.4 PARTIAL and deepseek DISAGREE both independently identified the same gap: gate keyed only to point estimates misses unsupported ranges (majority of R19 failures). CDS treated as Outcome 1 — correct. Second revision replaced "point estimate without range" with "quantitative claim without uncertainty justification" (CONDITION 1 + CONDITION 2). Calibration test against all 4 R19 failures passed. Google 503 documented as verification-gap. 2/3 providers sufficient per R19 DA-XVERIFY precedent.

#### ΣComm discipline — PASS

Agent-facing content uses !when, !applies-to, !format, !rules, → notation, | separator, ¬ for NOT. Plain English in §2 hygiene prose (appropriate — planning sections, not cross-agent signals). Step 8.5 spec in code-block format (format-preserving, per CLAUDE.md).

#### Interface conflict: ADR[1] (CDS) vs ADR[2] (security-specialist) — FLAGGED FOR LEAD

CONFLICT: CDS ADR[1] chose auto-ready at server startup (machine.py code change, ~5 lines). Security-specialist ADR[2] chose spawn-prompt instruction (zero code change, compliance-reliant). Mutually exclusive primary approaches to the same problem (#3 ΣVerify agent-context inheritance).

Security-specialist assessment: CDS choice (auto-ready at machine.py startup) is architecturally SUPERIOR. Security-specialist plan explicitly named hateoas-agent auto-init as "PREFERRED architecturally" and spawn-prompt as fallback due to scope constraints. CDS correctly identified that machine.py auto-ready (calling handle_init() in build_machine()) achieves the same result WITHOUT touching hateoas-agent — IS in-scope since sigma-verify is under user control (H1 CONFIRMED). Handle_init() does key-check only (no external state written — confirmed by code read of handlers.py). No EoP risk. No semantic contract violation — init remains callable as idempotent diagnostic.

Resolution: CDS ADR[1] auto-ready OVERRIDES security-specialist ADR[2] spawn-prompt as primary enforcement. Security-specialist IC[2] (spawn-prompt contract) should be marked SUPERSEDED by CDS IC[3] (machine.py startup-ready protocol) after lead reconciliation. SQ[SS-3] (spawn template update) reduced to belt-and-suspenders documentation, not primary enforcement mechanism.

#### Overall verdict: PASS — 2 items for DA

PASS on: §2a-e hygiene, source tags, DB[], SQ/CAL/PM, XVERIFY ADR[2], ΣComm discipline.
FLAG for DA:
  DA-1: DB[ADR[3]/ADR[4]] step 3 probability estimates (45%/55%) are [agent-inference] without RC backing — PM[] likelihoods derive from these. DA should probe: what evidence supports stub-substantiveness and first-try-correct rates?
  DA-2: OQ-CDS1 scope flag — premise-audit (#21) has NO mechanical enforcement (directive+spawn-template only). CDS flagged this. DA should decide: is directive-only sufficient given PM[CDS-1] (35% degrades to checkbox), or does this need SQ[CDS-6b] chain-evaluator ## premise-audit presence check?

Security-specialist self-correction: IC[2] marked SUPERSEDED pending lead reconciliation. SQ[SS-3] reduced to documentation.

Build-track triangle:
- implementation-engineer verifies code-quality-analyst
- code-quality-analyst verifies technical-writer
- technical-writer verifies implementation-engineer

DA exempt (per R19 #6 — DA role-exempt; DA's r1 exit-gate grade covers all agents instead).

### Peer Verification: tech-architect verifying security-specialist

**Scope:** §2a-e hygiene, |source:{}| tags, DB[] for top claims, XVERIFY on ADR[1], SQ[SS-1..3] decomposition, ΣComm compliance.

#### §2a-e hygiene assessment

§2a (positioning): SS documented approach as "PreToolUse hook is canonical enforcement point — phase-gate.py uses it for BLOCK 1 + BLOCK 2. Adding BLOCK 3 matches established ecosystem." Outcome 2 stated with specific reference to existing blocks. Not perfunctory — cites ecosystem precedent. PASS. |source:[code-read SS §2a]

§2b (calibration): SS references RC[phase-gate-block] with "~20 LOC + 5 tests per block, sample-size=2, confidence:H." Sample size of 2 is stated explicitly. Not a blind claim. PASS with note: 2 is a small sample; confidence H may be slightly generous but not indefensible given tight analogy. |source:[code-read SS RC section]

§2c (cost/complexity): SS states "zero code change for #3 fix, spawn-prompt only." This is the ADR[2] position (spawn-prompt, not auto-ready). The cost assessment is accurate FOR SS's chosen approach. The divergence with TA ADR[1] (auto-ready) is a design disagreement, not a hygiene failure — SS's §2c is internally consistent with SS's own decision. PASS. |source:[code-read SS ADR[2]]

§2d (source provenance): SS consistently uses |source:[code-read ...]| and |source:[independent-research]| tags. STRIDE[1] uses |source:[independent-research] handlers.py|. DB[sed-i-block] uses |source:[agent-inference]| implicitly (decision rationale). One gap: ADR[2] decision states |source:[agent-inference]| — borderline, but spawn-prompt instruction is genuinely agent-inference level. PASS. |source:[code-read SS plan full]

§2e (premise viability): SS STRIDE[1] addresses trust boundaries and confirms keys are never in agent context (|source:[independent-research] handlers.py|). The bypass-allowlist section explicitly states "NONE" for BLOCK 3 and documents WHY `sed -i ''` and `sed -i.bak` pass. This is premise-viability applied correctly — what must hold for BLOCK 3 to not over-fire. PASS. |source:[code-read SS STRIDE[1], ADR[1]]

#### DB[] for top claims

SS DB[sed-i-block]: 5/5 steps present.
(1) initial: block all sed -i globally
(2) assume-wrong: breaks CI scripts, test runners, legitimate config sed in code projects
(3) strongest-counter: scope to workspace path + allow backup-extension
(4) re-estimate: yes, scoped is correct
(5) reconciled: BLOCK on regex AND workspace path pattern
Full 5-step structure confirmed. PASS. |source:[code-read SS DB[sed-i-block]:338-343]

#### XVERIFY on SS ADR[1]

SS XVERIFY coverage: openai(PARTIAL/medium) + llama(AGREE/high) + google(503-FAIL).
openai PARTIAL: regex mechanically weak, evasion forms (env sed, xargs sed, unusual quoting). SS acted on this: "ADR[1] REFINED post-XVERIFY: use shlex.split() to tokenize command." Consequence-bearing refinement documented. |source:[code-read SS XVERIFY section:397-410]
llama AGREE: no counter-evidence surfaced. Local 8b model — lower probing depth than openai, but confirms basic approach.
google 503: logged as gap, not skip. Correct protocol.
Assessment: SS correctly weighted openai PARTIAL over llama AGREE ("openai PARTIAL > llama AGREE on implementation-specific concern") and acted on it. XVERIFY execution was rigorous. PASS.

One note: SS ADR[1] post-XVERIFY refinement flags "env sed -i file" as evasion form and notes "must test env/xargs wrapping forms" — this is correctly flagged as implementation-engineer risk, not resolved. Honest gap documentation. PASS. |source:[code-read SS XVERIFY:395-410]

#### SQ[SS-1..3] decomposition

SQ[SS-1]: BLOCK 3 in phase-gate.py | owner:implementation-engineer | est:1-2h | files:phase-gate.py. Estimable, specific, single-file. PASS.
SQ[SS-2]: Tests for BLOCK 3 | owner:code-quality-analyst | est:1h | files:phase-gate test suite. Estimable. CQA BC challenge added 8-form test matrix (env/xargs/tab-space evasions) — SS's original 6 forms understated. TA agrees with CQA expansion. SS should update SQ[SS-2] est from 1h to 1.5h for 8-form matrix. Minor — does not block plan. PASS with note. |source:[cross-agent CQA BC challenge]
SQ[SS-3]: Spawn templates + agent-def update | owner:technical-writer | est:30min. Estimable. PASS.

#### ΣComm compliance

SS plan uses ΣComm notation in ADR/IC/SQ sections (|decision:|, |alternatives:|, |source:|, STRIDE format). §2 hygiene outcomes use outcome-labeled format ("→ Outcome 2: ..."). One boundary check: STRIDE[1] narrative is partly plain English ("ROOT CAUSE (confirmed via code read...)" in human-readable form) — but STRIDE sections in agent workspace are correctly agent-facing ΣComm by convention, so the hybrid is a minor deviation not a violation. PASS with note. |source:[code-read SS plan full, CLAUDE.md ΣComm boundary]

#### Overall SS peer-verification verdict

§2a-e: PASS (5/5 checks)
DB[]: PASS (5/5 steps confirmed for primary claim)
XVERIFY: PASS (rigorous, acted on openai refinement, gap documented)
SQ[SS-1..3]: PASS with minor note (SQ[SS-2] est slightly low for expanded test matrix)
ΣComm: PASS with minor note (STRIDE hybrid format)

Substantive finding: SS ADR[2] (#3 ΣVerify fix = spawn-prompt, not auto-ready) diverges from TA ADR[1] (auto-ready at startup). SS's analytical work on this is sound within SS's own premise (spawn-prompt is "compliance-reliant, compensated by A15"). The divergence is a legitimate architectural disagreement where SS's STRIDE analysis raises a valid EoP concern about bypassing HATEOAS state that TA ADR[1] counters (no new attack surface since tools are provider-gated at call time). This divergence is correctly flagged for DA adjudication — NOT a peer-verification failure on SS's part.

One genuine concern: SS ADR[2] notes "hateoas-agent auto-init: PREFERRED architecturally, out of scope — file as follow-up." This is honest and internally consistent, but it means SS's preferred fix is deferred and the in-scope fix is admitted to be a compliance-reliant second choice. DA should factor this into adjudication. |source:[code-read SS ADR[2]:372-376, STRIDE[1]:347-369]

Verification criteria (lightweight — peer verifier confirms peer's work is internally consistent, not substantive re-review):
- §2a-e hygiene checks present (outcome 1/2/3 format)
- §2g DB[] for top 2-3 high-conviction claims
- |source:{type}| tags on all findings
- XVERIFY tag on top-1 load-bearing (when ΣVerify available) with ¬anthropic per C8
- SQ[]/CAL[]/PM[] populated per role
- ΣComm notation used (agent-facing)


### Peer Verification: cognitive-decision-scientist verifying tech-architect

Criteria verified: §2a-e hygiene (outcome 1/2/3 format), §2g DB[] top claims, |source:{type}| tags, XVERIFY on load-bearing ADR[1], SQ[]/CAL[]/PM[] populated, ΣComm notation.

§2a-e hygiene: PASS — all four ADRs carry §2a/§2b/§2c/§2e checks with explicit outcome 1/2/3 format. ADR[3] timing window §2a uses Outcome 1 (check changes recommendation from 24h grace to signal-driven) — correctly structured. No perfunctory checks detected.

§2g DB[]: PASS — DB[1]-DB[4] all present. DB[2] (rename direction) correctly structured: (1)initial→rename gate_checks (2)assume-wrong→breaks callers (3)counter→rename leaf only (4)re-estimate→leaf strictly safer (5)reconciled→chain-evaluator:241. Genuine engagement. DB[3] (timing) also shows real revision from 24h grace to signal-driven. DB[4] (premise-audit) shows evolution from new-agent to workflow step.

|source:{type}| tags: PARTIAL PASS — §2b RC[1/2/3] all tagged [agent-inference]. ADR[1] XVERIFY results tagged |source:external-openai-gpt-5.4| and |source:external-nemotron-nemotron-3-super:cloud|. IC[1-5] tagged [code-read path:line]. PM[1-4] not explicitly tagged — gap but not critical (PM entries are forward-looking risk assessments, not research findings). Flag: RC[1] and RC[2] cite [agent-inference] where [code-read] would be more accurate (RC[2] base-rate is from code-read not reasoning). Minor.

XVERIFY on ADR[1]: PASS — XVERIFY[openai:gpt-5.4] partial(medium) resolved by code-read confirming handlers.py init does ONLY key-check. XVERIFY[nemotron]: agree(high). XVERIFY-FAIL[google:gemini-503]. 2/3 returned, 1 technical failure. Per C8: ¬anthropic. Compliant.

SQ[]/CAL[]/PM[]: PASS — SQ[1-13] present, all with owner/est/files. CAL[1-3] with 80%/90% ranges and breaks-if conditions. PM[1-4] with likelihood/early-warning/mitigation. PM[3] (premise-audit skipped under delivery pressure, 35% likelihood) correctly identifies highest operational risk.

ΣComm notation: PASS — ADR/IC/SQ/RC/CAL/PM use pipe-separated compressed notation. ADR[1] has one prose section (security-note and XVERIFY detail) that is technically agent-facing, mildly verbose — not a process violation given the explanatory value.

One substantive flag for DA attention (not a verification failure — TA work is sound):
TA ADR[3] signal-driven approach: TA selects signal-driven with 30s timeout over 24h grace. CQA challenges this as Stop hook non-looping violation. TA's architecture would need the Stop hook to wait/poll — potentially introducing a polling loop in a non-looping hook. TA should clarify whether signal-driven re-run is implemented as (a) a separate post-archive hook trigger, not the Stop hook, or (b) a synchronous directory mtime check at Stop hook time (no polling). If (b), the 30s "timeout" becomes a synchronous mtime delta check — not polling. This is resolvable without changing ADR[3] direction; it's an implementation clarification for C2.

Overall: PASS — TA section is rigorous, DB[] shows genuine engagement, XVERIFY compliant, SQ[] decomposition thorough. The signal-driven vs non-looping Stop hook tension is a C2 implementation note, not a plan deficiency.

### Peer Verification: implementation-engineer verifying code-quality-analyst

Criteria: TEST-MAP methodology, test-estimate realism, regression-floor reasoning, coverage map per R19 issue, |source:{}| tags, ΣComm. Lightweight — internal consistency, not substantive re-review.

TEST-MAP methodology: PASS — coverage map structured per R19 issue with distinct sections for each (#4, #5+#14, #19, #20, #21-#24). Regression risk assessed per issue. Flakiness risk called per issue. This is the correct methodology for a build-track pre-plan feasibility role. |source:[code-read CQA TEST-MAP sections]

Test-estimate realism: PASS with BC-concede noted — original SQ[13] est=5h was understated; CQA's challenge (BUILD-CHALLENGE[SQ[13]-underestimate]) correctly identified 8-12h realistic range for 34-47 tests across 9 files. TA conceded (BC[#3]) and split SQ[13] into SQ[13a-g] with 11-15h total. CQA estimate was grounded in specific test-count derivation per issue, not round-number guessing. |source:[code-read CQA test-addition-table, TA-BC[#3]-concede]

Regression-floor reasoning (81 confirmed): PASS — CQA ran live pytest --collect-only and reported 92 tests collected, 11 pre-existing failures, 81 passing. Root cause of pre-existing failures correctly diagnosed (MINIMAL_WORKSPACE fixture uses non-roster agents; roster was added later, breaking fixture assumptions). The 81 floor is code-read-grounded, not assumed. TA revised H5 to 143 passing after re-running (different environment/fixture state possible) — CQA's 81 and TA's 143 diverge but both are grounded in live runs. This is a C2 reconciliation item, not a methodology failure. |source:[code-read CQA pre-existing-failures section, TA-H5-REVISED:143]

Coverage map per R19 issue: PASS — all 9 priority issues covered (#4, #5+#14, #19, #20, #21, #22, #23, #24, fixture). Each entry has: existing coverage assessment, new tests needed, regression risk, flakiness risk. Zero-coverage call on A16/A17/A18 is correct (confirmed by code-read of test_hooks.py test class list). |source:[code-read CQA coverage-map, test_hooks.py TestAgentParser]

|source:{type}| tags: PASS — all key claims tagged. [code-read live-pytest 26.4.23] on baseline count. [code-read chain-evaluator.py:625-640] on stop-hook non-looping claim. [code-read CDS ADR[2]] on A20 CONDITION 1 concern. [cross-agent CQA BC challenge] pattern used correctly. No untagged load-bearing claims found. |source:[code-read CQA BUILD-CHALLENGEs]

ΣComm: PASS — BUILD-CHALLENGE format uses pipe-separated notation per spec. Convergence declaration uses ✓ + pipe notation. TEST-MAP body is plain English (appropriate — structural analysis for peer-agent reading, not domain findings). Boundary judgement: acceptable. |source:[CLAUDE.md ΣComm boundary]

Substantive cross-checks (3 independently confirmed):
F[CQA-1] ADR[3] stop-hook non-looping: CONFIRMED valid — IE independently identified same constraint (chain-evaluator.py non-looping design). TA subsequently conceded (BC[#2]) and revised ADR[3] to 24h grace. CQA challenge was correct and consequence-bearing. |source:[code-read chain-evaluator.py, TA-BC[#2]-concede]
F[CQA-2] IC[4] check_a3 two-layer duplication: CONFIRMED valid — IE independently identified chain-evaluator.py:162-183 second depth check uncoordinated with gc.check_dialectical_bootstrapping. TA conceded (BC[#4]) and clarified layered authority (gc=presence, chain-evaluator=depth, sequential). Challenge was correct. |source:[code-read chain-evaluator.py:162-183, TA-BC[#4]-concede]
F[CQA-3] SQ[6] sigma-verify test ownership ambiguity: CONFIRMED valid open question — sigma-verify is separate repo at ~/Projects/sigma-verify with own test environment. Conflating with chain-evaluator baseline would misrepresent regression coverage. Still requires plan-track resolution. |source:[code-read sigma-verify repo structure]

PM[] gap: NOT separately formatted by CQA. Minor — covered by plan-track PM[SS-3]+PM[CDS-2] for relevant failure modes. Non-blocking for build-track feasibility role.

PEER-VERIFY[implementation-engineer→code-quality-analyst]: PASS |methodology:CONFIRMED |test-estimates:realistic-and-BC-validated |regression-floor:code-read-grounded(81/143-divergence=C2-reconcile) |coverage-map:complete-per-R19-issue |source-tags:CONFIRMED |ΣComm:PASS |F[CQA-1]:INDEPENDENTLY-CONFIRMED+TA-conceded |F[CQA-2]:INDEPENDENTLY-CONFIRMED+TA-conceded |F[CQA-3]:valid-open |PM[]:minor-gap-non-blocking |artifact-refs: TEST-MAP-table(1)+coverage-map(2)+BUILD-CHALLENGE[ADR[3]](3)+BUILD-CHALLENGE[IC[4]](4)+BUILD-CHALLENGE[SQ[6]](5)+BUILD-CHALLENGE[SQ[13]](6)+convergence-declaration(7) — ≥3 met |#7

## BELIEF[plan-r1] (lead-computed 26.4.23 per §4 BUILD weights, Step 24 HARD GATE)

BELIEF[plan-r1]: P=0.84 |builder-feasibility=0.85 (build-track challenged 13+3 times, plan-track conceded or defended w/ reasoning) |interface-agree=0.80 (DIV[1]/DIV[2] resolved, DIV[3] IC namespace admin-pending — SS renumber IC[6-8] implicit-accept) |design-arch=0.85 (DA[#5] #22 incoherence resolved via scoping CONDITION 2-only; DA[#1] #19 resolved via TA concede + IC[4] rewrite) |conflicts=1 remaining (DA[#10] C4-vs-C5 path — user decision pending) |review-coverage=0.85 (Q1-4 addressed, H5 falsified+integrated, H3/H4 confirmatory-framed flag accepted by TA) |DA=A- (per DA addendum post-DA[#1] closure) |→ borderline-lock (P=0.84 just-below-0.85-threshold)

Lead note 26.4.23: All 4 original DA-blocking conditions closed:
- DA[#1] #19 root-cause misdiagnosis — TA CONCEDE (empirical Python test agreed with DA's 3/3 XVERIFY), IC[4] REWRITTEN to split-by-DB then require (1)(2)(3), SQ[3] revised 1h→2h
- DA[#2] DIV[1] ΣVerify compromise — TA + SS both ACCEPT (auto-ready primary + documented gateway semantics + belt-and-suspenders)
- DA[#5] #22 architecture incoherent — CDS CONCEDE, SQ[CDS-6] revised to CONDITION 2-only detection (~20 LOC, 4-5 tests); CONDITION 1 explicitly DEFERRED with code-comment label
- DA[#7] H5 integration — SQ[0] fixture-fix prerequisite ADDED (owner: CQA, est 1-2h), passing-floor revised to "143+ after SQ[0]"

Non-blocking at r1:
- DA[#4] DIV[3] IC namespace — TA keeps IC[1-5], SS renumbers to IC[6-8] (admin, not content)
- DA[#6] meta-observation — R19 #2 manifested 4x during this build session; empirical evidence for scope promotion (user decision pending)
- DA[#8] DB pro-forma reruns — TA DEFEND (engaged w/ reasoning), CDS DEFEND (DB[ADR[2]-r2] rerun w/ net-negative-ROI engagement)
- DA[#9] H3/H4 confirmatory-framed — TA accepted revision (H3 partially confirmed; no-premise-audit subspace explicitly defended rather than untested)
- DA[#10] C4-vs-C5 path — paths α/β/γ/δ framed, user decision pending (blocking for C2 but not plan-lock mechanics)
- DA[#11] A21→A24 rename + KEEP — SS CONCEDE rename, DEFEND keep as regression trip-wire

Exit condition per Step 25:
- P=0.84, round=1, DA=A- CONDITIONAL-PASS→PASS
- P < 0.85 threshold technically triggers another round, but the remaining gap is user decision on DA[#10] (not agent rework)
- Proposing: lock plan after user C4-vs-C5 decision + DA final verdict re-issued post-TA response

## IN-SCOPE EXPANSION: Path β+ audit-monitored calibration (user decision 26.4.23)

User resolved DA[#10] C4-vs-C5 tension: CDS compromise (path β — WARN for 3 reviews, promote to BLOCK after calibration) is accepted AND audit tooling must empirically track the 3-review calibration window so promotion is data-driven not assumption-driven.

Rationale (per "accountable rigor over permissiveness" memory): a self-reported 3-review window is the same failure mode as a directive — gets ignored under pressure. Empirical tracking is the C5-compatible way to thread the C4 tension.

Implementation sub-requirements (CDS + TA to design):
- Chain-evaluator §2i WARN fires must be recorded with review-id + fire-count + workspace-context
- Calibration data persists beyond single session (sigma-mem team memory or archive index extension)
- Audit tooling (sigma-audit skill or new check) reads calibration data and gates BLOCK-promotion
- Promotion trigger: "§2i has fired N times across ≥3 distinct reviews with ≤M false-positive count" — CDS to set thresholds
- Documentation: directive text for §2i carries explicit "promoted to BLOCK on 26.X.Y via audit-calibration-gate" once triggered

Gates affected by this expansion:
- #22 §2i precision gate (CONDITION 2) — primary application
- #23 governance min-artifact — SAME PATTERN applies (WARN-first, audit-monitored, BLOCK-promotion-on-data) per C4+C5 discipline
- #24 severity provenance — SAME PATTERN applies
- #21 premise-audit — presence check is binary, BLOCK-from-day-one applicable (no calibration window needed)

New SQ needed: audit-calibration-gate implementation. Owner TBD (could be IE for the code, TW for directive text, combined).
Existing SQ adjustments: SQ[CDS-6] expands to include calibration-data emission; SQ[CDS-7] (governance min-artifact) similarly; SQ[CDS-8] (severity provenance) similarly.

Scope-boundary note: this expansion adds the audit-monitoring infrastructure but does NOT change the underlying gates #21-24. It's additive scaffolding that makes the WARN-first pattern empirical rather than assumed.

## IN-SCOPE EXPANSION: R19 #2 targeted workspace.md concurrent-write protection (user decision 26.4.23)

User resolved DA[#6] meta-observation scope question: R19 #2 promoted from deferred to TARGETED in-scope — just workspace.md (or by extension, all `~/.claude/teams/*/shared/**/*.md` sigma workspace files) concurrent-write protection. NOT general concurrency infrastructure.

Rationale: 4+ manifestations in THIS session (lead 3x, DA 4x, SS 1x, TA avoided via atomic Python replace) = empirical evidence R19's CRITICAL classification was correct and "deferred-LOW" framing was understated. Shipping the R19 remediation build without addressing the bug that BIT the very build sessions would be incongruous.

Scope boundary for #2 fix:
- IN: workspace.md + sigma team shared workspace files (builds/*/*.md, shared/workspace.md)
- OUT: general concurrency infrastructure (not file-lock for every file, not system-wide write-window, not multi-user queue)
- OUT: fixes for R19 #7 (sigma-mem write contention) — separate failure mode, separate build
- OUT: fixes for R19 #16 (sigma-mem MCP disconnect) — separate

R19 source options for TA to evaluate (choose 1, document alternatives):
(a) Agents must use Edit tool only (read-before-write race protection for single-writer; won't fix multi-writer)
(b) Advisory file-lock with .lock sentinel file (agents check .lock before write, respect it; requires cooperation)
(c) Lead-proxy queue — agents send workspace writes to lead, lead serializes (introduces lead as bottleneck, but bypasses race)
(d) Atomic Python replace pattern (what TA used) — generalize as the canonical write method, document in directives

New SQ needed: SQ[2-workspace-lock] or similar, owner TBD (likely IE implementation after TA ADR + SS security review for advisory-lock bypass concerns).
New IC needed: workspace-write-contract (how agents reliably write to shared workspace files without race).
Test surface: multi-writer race simulation test (can be sequential with explicit timing).

Scope-boundary note: this expansion makes 3 in-scope expansions total (check_a3 under #19, A24 pre-flight, β+ audit calibration) plus now #2 workspace protection. Originally 11 tickets, now effectively 12-13 depending on how #2 ADR materializes.

## BELIEF[plan-r1-updated] (lead-computed 26.4.23 post-β+ and post-#2-ADR, Step 24 HARD GATE re-run)

BELIEF[plan-r1-updated]: P=0.88 |builder-feasibility=0.88 |interface-agree=0.85 (DIV[3] admin pending — TA IC[1-6], SS must renumber to IC[7-9]) |design-arch=0.90 (#22 scoped to CONDITION 2 + deferred CONDITION 1; β+ audit-gate well-designed; #2 ADR[5] empirically-grounded via this-session evidence) |conflicts=0 remaining blocking |review-coverage=0.90 (Q1-4 addressed + 3 in-scope expansions integrated; all H[]-results documented) |DA=A- |→ LOCK-PLAN (P > 0.85 + DA PASS criterion met)

What landed since BELIEF[plan-r1]=0.84:
- CDS path β+: 3 SQ revised + 4 new SQs (CDS-9/10/11/12 calibration-log + audit-gate + directive text + DA verdict protocol); #24 promoted from directive-only to WARN+code-detection stub; threshold semantics defined (≥3 reviews + ≤20% FP + ≥5 DA-verdicted)
- TA ADR[5] for R19 #2: Option D (atomic Python replace + section-isolation) selected with empirical DB[5] backing from this-session behavior (3x TA success vs 4x DA Edit-anchor-failures); IC[6] workspace-write-contract added; SQ[14] workspace_write() helper assigned to IE

DIV[3] admin resolution (non-blocking):
- TA namespace: IC[1-6] (now 6 contracts including IC[6] workspace-write)
- SS namespace: SS should renumber IC[1-3] → IC[7-9] to avoid collision (preserves TA sequential ordering)

Plan-lock readiness:
- All 4 DA-blocking conditions: ✓ closed substantively
- All 3 in-scope expansions integrated: ✓ (check_a3 under #19, A24 pre-flight, β+ audit calibration, #2 workspace-write-contract — actually 4 expansions)
- Path β+ design complete: ✓
- #2 ADR complete: ✓
- Peer verification ring: ✓ (all 6 PASS or PASS-post-remediation)
- SS security review of IC[6]: requested, non-blocking (TA notes no new attack surface vs Edit tool)

Exit condition per Step 25: P=0.88 > 0.85 + DA PASS @ A- → LOCK PLAN

## PLAN-LOCK DECLARATION (lead 26.4.23)

### plan-exit-gate: PASS
### plan-belief: P=0.88
### DA-grade: A-
### plan-locked: 2026-04-23

Plan is LOCKED. Plan-track and build-track agents may exit their r1 cycle. Next phase: Outcome Delivery (Step 33 promotion → Step 34 archive → Step 35 plan file → Step 37 user report).

Locked artifacts summary:
- ADRs: TA ADR[1-5] (5), CDS ADR[1-4] (4), SS ADR[1-3] (3) = **12 ADRs total**
- ICs: TA IC[1-6] (6), SS IC[7-9] (3) = **9 IC typed contracts**
- SQs: TA SQ[0-14] (15 including SQ[0] fixture prereq), CDS SQ[CDS-1..12] (12), SS SQ[SS-1..3] (3) = **30 sub-tasks**
- RC/CAL/PM: all three agents have RC[], CAL[], PM[] populated per role
- DBs: TA DB[1-5] (5), CDS DB[] on ADR[1-4] + DB[ADR[2]-r2 rerun] (5), SS DB[] on ADR[1] XVERIFY refinement
- XVERIFY: 3 mandatory runs completed (TA ADR[1], SS ADR[1], CDS ADR[2]) all ¬anthropic per C8; Google 503-failed all 3 attempts (quota/auth/service issue — non-blocking)

Build scope final (locked):
- 11 original R19 tickets + 4 in-scope expansions:
  - check_a3 dup bundled into #19
  - A24 pre-flight (sigma-verify init compliance, renamed from A21 to avoid collision)
  - β+ audit-calibration for #22/#23/#24 (4 new SQs CDS-9/10/11/12)
  - R19 #2 targeted workspace-write-contract (ADR[5] + IC[6] + SQ[14])
- Excluded: MEDIUM/LOW R19 #6-18 (minus #2 which was promoted), already-resolved artifacts, sigma-verify default-anthropic-exclusion, general concurrency infrastructure, lost chain-eval/phase-gate test files (deliberate consolidation per git log)

Lead signals per recipe Step 26: plan-track and build-track exit r1 cycle; enter promotion phase (Step 33).
