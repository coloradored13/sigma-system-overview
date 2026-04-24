# C2 scratch — BUILD: r19-remediation
## status: booting
## mode: BUILD-C2
## build-id: 2026-04-23-r19-remediation
## team-name: r19-remediation-c2
## directives-version: build-directives.md + directives.md + protocols.md + sigma-mem/patterns.md+decisions.md (session reads 26.4.23 post-C1)
## plan-file: ~/.claude/teams/sigma-review/shared/builds/2026-04-23-r19-remediation.plan.md
## plan-lock: status=plan-locked |plan-exit-gate=PASS |plan-belief=P=0.88 |DA-grade=A- |12 ADRs |9 ICs |30 SQs |10 PMs
## c1-archive: ~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-workspace.md (252KB, git-committed d5ddaeb+6be7b78)

## pre-flight |from plan ## C2 pre-requisites + sigma-mem builder calibration
- !PF[1] test-baseline-reconciliation: TA claimed 154-collected/143-passing vs CQA claimed 92-collected/81-passing. C2 FIRST TASK: establish authoritative count via `git ls-files | grep test_` + `pytest --collect-only -q` from repo root. Authority: whichever scope covers full suite (three-file canonical set = test_chain_evaluator.py + test_phase_gate.py + test_gate_checks.py per TA calibration, but CQA's 92 may indicate file scope differs; reconcile empirically before writing new tests). |gate: cannot write any new tests (SQ[13*], CDS-6-10, SS-2) until baseline established.
- !PF[2] SQ[0] fixture-fix is prerequisite: MINIMAL_WORKSPACE fixture uses synthetic agent names; roster.md addition broke it → 11 pre-existing failures. Fix BEFORE SQ[3] + SQ[13b] + SQ[13c] test work. Owner: code-quality-analyst. ¬optional.
- !PF[3] a2a7fa8 pre-applied: chain-evaluator.py:241 rename archive_exists→archive_file_found already shipped (R19 #4 part-fix) to unblock plan-lock commit. C2 agents touching this line MUST verify-not-re-apply. Tests + directive updates + ADR documentation still in scope.
- !PF[4] A-check ID assignments LOCKED (supersedes UP[TA-B3]): A20=precision gate (§2i, CDS) |A21=RESERVED-unused |A22=governance min-artifact (#23) |A23=severity provenance (#24) |A24=sigma-verify init pre-flight (#3 belt-and-suspenders, renamed from A21 to avoid collision). Agents MUST NOT write A21.
- !PF[5] sigma-verify repo = separate commit scope. SQ[1] (machine.py) commits from ~/Projects/sigma-verify/, NOT sigma-system-overview. All other SQs commit from sigma-system-overview.
- !PF[6] section-isolation write convention (UP[TA-B2] BROAD-scope): agents write ONLY to own ### section; lead writes ## sections. Cross-section writes require lead authorization. Canonical method: atomic Python replace per IC[6] (content.replace(old_anchor, new_text, 1); raise on anchor-not-found). SQ[14] implements workspace_write() helper.
- !PF[7] C8 anthropic-exclusion on all XVERIFY/XREVIEW calls in C2 (Claude verifying Claude is not cross-model).

## build-calibration |from sigma-mem patterns.md + decisions.md
- CAL[1] chain-evaluator Stop hook non-looping: check_a12 grace-window = synchronous mtime delta, NO poll/wait/sleep in enforce_stop path (chain-evaluator.py:625-640).
- CAL[2] check_a3 layered authority: gc=presence, chain-eval=depth, sequential not conflicting. NO third layer.
- CAL[3] peer-verify regex+section-boundary coupling: canonical ### "X verifying Y" format propagated in spawn templates; NO regex change (IC[5]).
- CAL[4] sed-i BLOCK 3: shlex.split() argv tokenization (NOT raw regex). Scope: workspace paths + /.claude/hooks/. Backup-extension forms pass. Test matrix includes env-wrapper, xargs-wrapper, -i.bak, -i '' forms.
- CAL[5] sigma-verify auto-ready: ~5 LOC in build_machine() at startup when API keys present. handle_init() key-check-only, no side effects (handlers.py:1-60).
- CAL[6] atomic Python replace: content-based match eliminates anchor-movement failures under concurrent writes. anchor = section-header + first-unique-content-line. Raise WorkspaceAnchorNotFound if replace no-op.
- CAL[7] directive propagation risk-tier split: #1 sed-i = ALL 23 agent .md files (SAFETY-CRITICAL, data-loss risk; spec-count corrected from 22 C1-error to 23 live-count per TW SQ[8] exec 26.4.24); #24 severity-provenance = _template.md only (CALIBRATION/QUALITY, rare firing).
- CAL[8] ΣComm boundary: directives.md + build-directives.md = agent-facing → write in ΣComm. §8e recovery template needs ΣComm conversion before insertion.
- CAL[9] atomicity constraint: #5+#14 peer-verify = c1-plan spawn template + sigma-lead §2 + c2-build + _template.md + chain-evaluator regex (last NOT changed per CAL[3] but verified matches). Same-commit required; partial deploy reproduces R19 failure.
- CAL[10] audit-calibration-gate pattern: standalone script (NOT chain-evaluator A-check) for cross-session threshold evaluation. CAL-EMIT schema for per-firing records.
- CAL[11] TA effort estimates calibration (from C1): SQ[2] was overestimated 3x, SQ[3] underestimated 2x, SQ[13] underestimated 2-2.6x. CAL lesson: pre-map full surface before estimating.

## Files |from plan (source-of-truth)
hooks/chain-evaluator.py | hooks/phase-gate.py | teams/sigma-review/shared/gate_checks.py (preserve) | ~/Projects/sigma-verify/src/sigma_verify/machine.py | teams/sigma-review/shared/directives.md | teams/sigma-review/shared/build-directives.md | skills/sigma-build/phases/c1-plan.md | skills/sigma-build/phases/c2-build.md | agents/_template.md | agents/*.md (22 SAFETY-CRITICAL) | agents/sigma-lead.md | teams/sigma-review/shared/calibration-log.md (create) | teams/sigma-review/shared/audit-calibration-gate.py (create) | ~/Projects/sigma-system-overview/agent-infrastructure/scripts/backup-memory.sh | workspace_write() helper (create) | teams/sigma-review/shared/test_gate_checks.py

## build-assignments
Cluster decision: 3 parallel workers per plan §3a.1 recommendation ("primary IE + IE-2 + IE-3"). Role-aligned: IE(code) + TW(docs) + CQA(tests+SQ[0]) — natural fit to SQ ownership in plan.

### Cluster A — hooks/sigma-verify code |owner: implementation-engineer |worktree: code-cluster
SQs: TA SQ[1], SQ[2], SQ[3], SQ[6], SQ[7], SQ[14] | SS SQ[SS-1]
Files:
- ~/.claude/hooks/chain-evaluator.py (SQ[2] A12 24h grace, SQ[3] A3 DB extraction, CDS-6/7/8 A20/A22/A23 WARN+CAL-EMIT)
- ~/.claude/hooks/phase-gate.py (SQ[7]+SS-1 sed-i BLOCK 3)
- ~/Projects/sigma-verify/src/sigma_verify/machine.py (SQ[1] auto-ready, SEPARATE commit scope per PF[5])
- workspace_write() helper (SQ[14], new file, location TBD — propose ~/.claude/teams/sigma-review/shared/workspace_write.py)
- SQ[6] sigma-verify test suite scope confirmation (read-only investigation)
!verify-not-reapply: chain-evaluator.py:241 archive_exists→archive_file_found already shipped in a2a7fa8 per PF[3]

### Cluster B — directives/templates/agent-defs |owner: technical-writer |worktree: docs-cluster
SQs: TA SQ[4], SQ[5], SQ[8], SQ[9], SQ[10], SQ[11], SQ[12] | CDS SQ[CDS-1..5], SQ[CDS-11], SQ[CDS-12] | SS SQ[SS-3]
Files:
- ~/.claude/teams/sigma-review/shared/directives.md (§2i, §2p, §2d extension, §8e ΣComm recovery template)
- ~/.claude/teams/sigma-review/shared/build-directives.md (§2i/§2p BUILD variants)
- ~/.claude/skills/sigma-build/phases/c1-plan.md (Step 7a premise-audit, Step 11 peer-verify spawn template)
- ~/.claude/skills/sigma-build/phases/c2-build.md (peer-verify canonical format)
- ~/.claude/agents/_template.md (sed-i rule, severity-provenance tag, premise-audit ref, peer-verify canonical)
- ~/.claude/agents/*.md (23 SAFETY-CRITICAL files per CAL[7] — sed-i rule ONLY; severity-provenance stays template-only) (spec-count corrected from 22 C1-error to 23 live-count per TW SQ[8] exec 26.4.24)
- ~/.claude/agents/sigma-lead.md (§2 peer-verify canonical + section-isolation)
!atomicity-constraint: CAL[9] #5+#14 peer-verify = c1-plan + sigma-lead + c2-build + _template.md must all land in SAME commit
!ΣComm: all edits to directives.md + build-directives.md + agent .md = agent-facing → ΣComm notation required per CAL[8]

### Cluster C — test expansion + fixture |owner: code-quality-analyst |worktree: test-cluster
!GATING: PF[1] baseline reconciliation + SQ[0] fixture fix MUST complete before cluster-C test writes AND before cluster-A touches SQ[3] (chain-evaluator A3) / SQ[13b-c] test surface
SQs: SQ[0] (gating) + TA SQ[13a-g] | CDS SQ[CDS-6..10] | SS SQ[SS-2]
Files:
- ~/.claude/teams/sigma-review/shared/test_gate_checks.py (modify — 30+ new tests)
- Possibly test_hooks.py or new test files (depends on PF[1] outcome)
- ~/.claude/teams/sigma-review/shared/calibration-log.md (CREATE, empty append-only)
- ~/.claude/teams/sigma-review/shared/audit-calibration-gate.py (CREATE, standalone script, CDS SQ[CDS-10])
- ~/Projects/sigma-system-overview/agent-infrastructure/scripts/backup-memory.sh (add calibration-log.md)

### Sequencing
1. All 3 agents spawned via TeamCreate simultaneously (same team: r19-remediation-c2)
2. CQA runs PF[1] + SQ[0] FIRST (gating) → declares UNBLOCKED in scratch ## build-status
3. IE-1 (Cluster A, minus SQ[3]) and TW (Cluster B) proceed in parallel immediately
4. After CQA SQ[0] complete: IE-1 can touch SQ[3]; CQA proceeds to SQ[13*] + CDS-6-10 + SS-2
5. Cluster A workspace_write() helper interface must be documented before Cluster B writes spawn-template references (API signature contract — can be locked via early checkpoint)
6. Checkpoint at ~50% per agent → scratch ## build-status entries
7. All 3 complete → merge worktrees → run FULL test suite → MERGE-VERIFIED

### Cross-cluster API contracts
- **workspace_write() helper signature** (Cluster A → Cluster B dependency): IE-1 publishes helper signature in scratch ## build-status BEFORE 25% mark so TW can reference in spawn templates/directives. Signature format: `workspace_write(path: str, old_anchor: str, new_content: str) -> None` per IC[6]; raises WorkspaceAnchorNotFound on anchor miss.
- **CAL-EMIT schema** (Cluster B directive text ↔ Cluster A chain-evaluator emission): CDS SQ[CDS-6/7/8] chain-evaluator emits; SQ[CDS-11] directive documents format. Both must match sigma-mem pattern P[CAL-EMIT-schema]: `CAL-EMIT[{gate-id}]: review-id:{slug} |finding-ref:{F[agent-id]} |fire-reason:{trigger} |workspace-context:{agent}:{50-char-excerpt} |da-verdict:PENDING`
- **A-check ID usage** (all clusters): A20/A22/A23/A24 only; A21 RESERVED; agents write to scratch using locked IDs per PF[4].

### Worktree plan
- sigma-system-overview: 2 worktrees (docs-cluster for TW, test-cluster for CQA) — code-cluster for IE-1 operates in main checkout
- sigma-verify: IE-1 only, separate repo scope per PF[5]
- Merge order: CQA (SQ[0] first) → TW + IE-1 parallel → final merge all → full test suite

## build-status
*(Step 3-4 populates — per-agent status + checkpoints)*

### code-quality-analyst
status: SQ[0] COMPLETE |PF[1] DONE |SQ[CDS-9] DONE |SQ[CDS-10] DONE |→ ie-1 UNBLOCKED for SQ[3]

**PF[1]** DONE |→ see ## test-baseline. AUTHORITATIVE: 154/143/11.

**SQ[0] COMPLETE 26.4.24** (post-user-ratification of Option C + ie-1 gate_checks DA-filter fix):
- cqa: fixture rename (agent-alpha→tech-architect, agent-beta→implementation-engineer + F[A-*]→F[TA-*], F[B-*]→F[IE-*], WORKSPACE_WITH_CB/DIVERGENCE refs, test assertions)
- cqa: reverted `test_extract_agents` accommodation back to original contract (DA not in agents, len=2) per ie-1 signal after gate_checks fix shipped
- ie-1: gate_checks.py:220-233 roster-allowlist branch now filters `devils-advocate` (mirrors exclusion-list branch line 246; contract documented in comment 223-228)
- pytest 3-file canonical: 154/154 pass |0 fail |0 regressions
- pytest test_audit_calibration_gate.py: 31/31 pass (no collateral damage from revert)

**User-ratification path:** Option C (plan-scope expansion to gate_checks.py) ratified by user via lead broadcast 26.4.24. Decision path documented in ## findings ### code-quality-analyst.

**SQ[CDS-9] DONE 26.4.24:** calibration-log.md created (empty append-only, format-documented in fenced code blocks per directives.md §2i spec) + backup-memory.sh updated with $CALIBRATION_LOG block. `bash -n` syntax clean.

**SQ[CDS-10] DONE 26.4.24:** audit-calibration-gate.py (~240 LOC, standalone script per CAL[10]) + test_audit_calibration_gate.py (31 tests, all pass). Fixture-isolated, zero coupling to MINIMAL_WORKSPACE / roster / DA-bug. CLI end-to-end verified: PROMOTE at 4 reviews/5 verdicted/20% FP ✓, CALIBRATING <3 reviews with PENDING warning ✓, RECALIBRATE >20% FP ✓, exit codes 0/2/3 per spec. Thresholds match directives.md line 347-349 exactly.

**Test surface net 26.4.24:** 176 passed / 8 failed (unchanged — 8 fails are pre-existing DA-inclusion bug gated on ie-1 fix). +31 NEW tests in test_audit_calibration_gate.py. test_chain_evaluator.py 62/62 ✓, test_phase_gate.py 54/54 ✓. ZERO regressions from CDS-9/10 work.

**Pattern surfaced in SQ[CDS-10]:** fenced-code-block exclusion in `parse_log()` — format example in calibration-log.md header was parsed as malformed record (exit code 2 regression). Fixed by toggling `in_fence` state around ``` lines. Passive flag only; not promoting until seen recurrence.

**Still parked on:** SQ[13b-g], SQ[CDS-6..8], SS-2 — all require the gate_checks DA-inclusion fix (user ruling pending per lead bundle with ie-1 SQ[1]).

---

CHECKPOINT[cqa] 26.4.24: SQ-progress=7/8-SQs-owned |tests-written=60 |tests-planned=30-46 (plan range) — exceeded upper bound by +14 due to edge-case coverage |regressions-from-baseline=0 required=0 actual=0 ✓ |baseline-holding: yes |drift: none-material |surprises: 1 minor

**SQs owned + status:**
- PF[1] baseline reconciliation: DONE (154/143/11 authoritative)
- SQ[0] fixture fix: DONE (post-ie-1 gate_checks fix; 3-file canonical 154/154)
- SQ[13a]: COVERED-BY-SQ[0]
- SQ[13b] A12 parser tests: DONE (2 tests, TestA12ArchiveFileFoundKeyRename)
- SQ[13c] A16/A17/A18 peer-verify: DONE (10 tests, TestPeerVerifyRegexContract)
- SQ[13d] A3 DB extraction: DONE (6 tests, TestA3DBGenuineVsReference)
- SQ[13e] A12 24h grace: DONE (3 tests, TestA12GraceWindow, os.utime determinism)
- SQ[13f] A20 precision CONDITION 2: BLOCKED on CDS-6..8 scope gap (lead-owned, pending user)
- SQ[13g]+SS-2 sed-i BLOCK 4 + shlex evasion: DONE (8 tests shipped + 1 deferred to BUILD-CONCERN)
- SQ[CDS-6..8] WARN+CAL-EMIT tests: BLOCKED on scope gap (same)
- SQ[CDS-9] calibration-log + backup: DONE (file created, backup script updated, syntax-clean)
- SQ[CDS-10] audit-calibration-gate.py: DONE (240 LOC + 31 tests)

**Test count totals:**
- test_gate_checks.py: 68/68 ✓ (no cluster-C additions; peer-verify tests went to test_chain_evaluator.py per existing pattern)
- test_chain_evaluator.py: 63/63 ✓ (+21 new cluster-C: SQ[13b]=2, SQ[13c]=10, SQ[13d]=6, SQ[13e]=3)
- test_phase_gate.py: 58/58 ✓ (+8 new: TestSedInPlaceBlock4Detection=6, TestSedShlexEvasionMatrix=5 shipped of 6 planned; 1 removed as documented BUILD-CONCERN)
- test_audit_calibration_gate.py: 31/31 ✓ (new file)
- Total CQA surface: **220 passed / 0 failed**

**Effort calibration update (CAL[11] feedback loop):**
- Plan SQ[13] estimate: 10-13h
- Actual (ETA-basis): ~4-5h active work including reconnaissance + 1 BUILD-CONCERN triage
- CAL lesson: plan under-estimate was real (2-2.6x), but SS-1 wrap-up happening in ie-1 parallel + pre-written fixtures pattern accelerated test writes beyond estimate. Effort was lower than plan predicted because ie-1's code surfaces were well-documented and I could write tests in tight test-class clusters.

**Surprise flagged:** BUILD-CONCERN[cqa] xargs sed-i argv-vs-stdin bypass in phase-gate.py check_sed_in_place. Genuine code gap, not test bug. Flagged to lead; not routed to ie-1 unilaterally per post-correction discipline. Awaiting direction.

**Post-momentum discipline held:** 2 correction-triggering moments avoided this cycle — (1) xargs-bypass flagged via BUILD-CONCERN rather than accommodating with relaxed assertion; (2) SQ[13d] start request paused for explicit lead authorization rather than inferring from "now unblocked" status.

### implementation-engineer
status: ALL-SCOPE-COMPLETE +EXTENSION (100%) |SQ[14] DONE |SQ[2] DONE |SQ[7]+SS-1 DONE |SQ[6] DONE |SQ[1] DONE |gate_checks DA-filter DONE |SQ[3] DONE |SQ[CDS-6] A20 DONE |SQ[CDS-7] A22 DONE |SQ[CDS-8-IE] A23 DONE |sed-i docstring-narrow DONE

EXTENSION CHECKPOINT[ie-1] (user-ratified scope extension):
- SQ[CDS-6] check_a20_precision_gate: SHIPPED to chain-evaluator.py — §2i CONDITION 2 code-detection (>70% confidence, HIGH/CRITICAL-severity, primary-recommendation). CONDITION 1 deferred per ADR[CDS-2]+DA[#5]; suppression heuristic on same line (driver breakdown, CI notation, qualitative qualifier). WARN-only path β+.
- SQ[CDS-7] check_a22_governance_artifact: SHIPPED — §2j HIGH/CRITICAL + governance-scope (committee/approval/oversight/compliance/audit) + missing both TIER-A/B/C and ARTIFACT-GAP tag. Window search 800 chars after finding line, bounded by next F[] or section end. WARN-only.
- SQ[CDS-8-IE] check_a23_severity_provenance: SHIPPED — §2d-severity HIGH/CRITICAL + extrapolation indicator (extrapolat*, transfer-assumption, cross-domain, applied-to, by analogy) + missing |severity-basis:| tag. Window 500 chars. Scope-narrow per directive line 409: native-domain severity = no tag required. WARN-only.

CAL-EMIT schema compliance (directives.md §2i lines 351-352):
```
CAL-EMIT[{gate-id}]: review-id:{slug} |finding-ref:{F[agent-id]} |fire-reason:{trigger} |workspace-context:{agent}:{50-char-excerpt} |da-verdict:PENDING
```
- Append-only write to `~/.claude/teams/sigma-review/shared/calibration-log.md` (CQA SQ[CDS-9] target exists per their COMPLETE status)
- Write via direct file append (not workspace_write helper — append-only append, not anchor-replace)
- Record also returned in details.cal_emit_records for CQA SQ[CDS-6..8] tests (assert without filesystem dependency)

Smoke-test: **16/16 PASS** — 4 fires (A20 confidence + A20 severity + A22 gov + A23 extrap), 9 no-fires (A20 CI-suppressed, A20 driver-suppressed, A20 qualifier-suppressed, A20 no-trigger, A22 TIER, A22 GAP, A22 non-governance, A22 MEDIUM, A23 tag-present, A23 native-domain), +1 schema compliance check, +1 file-append verification.

Registered in ANALYZE_CHAIN (chain total 18→21 checks).
Regression: test_gate_checks.py 68/68 still pass (gc layer unchanged; these are chain-eval layer checks).

## git diff (extension, appended)
- M hooks/chain-evaluator.py (+~200 LOC for check_a20/a22/a23 + _emit_cal_record helper + review_id derivation + regex constants)

Total IE-1 session LOC: ~400 across 5 files, 2 repos. 8 sigma-mem patterns persisted (including today's P[path-β+-WARN-first-calibration-gate]).

FINAL CHECKPOINT[ie-1]:
- SQ[3] check_a3 DB extraction: SHIPPED to ~/.claude/hooks/chain-evaluator.py:163-235
  - **layered authority preserved (IC[4]+CAL[2]):** gc.check_dialectical_bootstrapping = presence (layer 1 upstream, unchanged); check_a3 = depth (layer 2, genuine-exercise count)
  - **R19 #19 fix:** pre-rewrite re.findall matched every DB[...] substring including reference citations; new split-by-DB + require (1)(2)(3) parenthesised-numbered-markers sequence distinguishes genuine exercises from references
  - **test matrix (3/3 smoke tests pass):** (1) 5 genuine + 5 refs in same section → genuine=5, refs=5 per plan verification 4; (2) partial exercise with only 3 markers → 1 genuine + shallow flag; (3) pure refs no exercises → 0 genuine + 2 refs
  - **details emitted:** db_genuine_by_agent (dict), db_reference_by_agent (dict), shallow_db_entries (list) — CQA SQ[13d] test surface
  - **regression:** test_gate_checks.py 68/68 still pass (check_a3 is chain-eval layer, not gc layer — gc unchanged)

## ALL CLUSTER A SQs SHIPPED
- SQ[14] workspace_write() helper — new file, IC[6] signature, dogfooded, 4/4 smoke
- SQ[2] A12 24h grace-window — chain-evaluator.py:234-275, CAL[1] honored
- SQ[7]+SS-1 sed-i BLOCK 4 — phase-gate.py:228-337, 22/22 evasion matrix
- SQ[6] sigma-verify test scope — read-only finding in scratch
- SQ[1] machine.py auto-ready (interp A) — sigma-verify repo, 300/300 tests, 28 LOC
- gate_checks.py DA-filter (plan-scope amendment) — 1-line + comment rewrite, 67/68 then 68/68 post-CQA-test-revert
- SQ[3] check_a3 DB extraction — chain-evaluator.py:163-235, layered authority preserved

## git diff (final, ¬committed)
**sigma-system-overview:**
- M hooks/chain-evaluator.py (SQ[2] A12 grace + SQ[3] check_a3 rewrite)
- M hooks/phase-gate.py (SQ[7]+SS-1 sed-i BLOCK 4)
- M teams/sigma-review/shared/gate_checks.py (DA-filter plan-amendment)
- ?? teams/sigma-review/shared/workspace_write.py (SQ[14] new)

**sigma-verify:**
- M src/sigma_verify/machine.py (SQ[1] auto-ready probe + forward-compat)

## sigma-mem patterns (5 persisted)
1. P[workspace_write-helper-dogfooded-at-callsite]
2. P[phase-gate-block-renumbering-when-plan-predates-code]
3. P[shlex-split-sed-i-evasion-matrix]
4. P[flag-interpretation-gap-as-build-concern]
5. P[plan-scope-amendment-via-user-ratification]
6. P[auto-ready-probe-forward-compat-hint]
7. P[db-split-by-marker-distinguish-exercise-from-reference]

## ready for merge
All cluster A work complete. Awaiting lead/CQA ordered merge step. No commits run by IE-1. !WAIT for promotion-round or shutdown_request.

POST-RATIFICATION CHECKPOINT[ie-1]:
- SQ[1] machine.py auto-ready (interpretation A): SHIPPED to ~/Projects/sigma-verify/src/sigma_verify/machine.py
  - +14 LOC code (probe + stderr log + forward-compat _initial_state_hint + try/except) + 14 LOC gateway-semantic-contract docstring
  - sigma-verify full suite: 300/300 pass, machine.py coverage 90%
  - startup log verified: `ΣVerify auto-ready: ready |providers=llama,gemma,nemotron,deepseek,qwen,devstral,glm,kimi,nemotron-nano,qwen-local` (10 providers on local env)
  - commit scope: sigma-verify repo (NOT sigma-system-overview per PF[5])
- gate_checks.py DA-filter fix (option C, plan-scope amendment): SHIPPED to ~/.claude/teams/sigma-review/shared/gate_checks.py
  - 1-line filter added to roster-allowlist branch (line 227-233), matches exclusion-list-branch pattern at line 246
  - Updated comment documents contract + R19 regression root-cause + reference to fallback branch
  - test_gate_checks.py post-fix: 67/68 pass (was 60/68) — remaining fail is CQA's accommodating test assertion that needs revert (handed back to CQA via SendMessage)
  - commit scope: sigma-system-overview
- SQ[3] check_a3 DB extraction: UNBLOCKED pending CQA's single-test revert. Estimated 30-45 min once CQA declares SQ[0] COMPLETE.

GIT DIFF (¬committed):
- ~/Projects/sigma-system-overview: M hooks/chain-evaluator.py, M hooks/phase-gate.py, ?? teams/sigma-review/shared/workspace_write.py, M teams/sigma-review/shared/gate_checks.py
- ~/Projects/sigma-verify: M src/sigma_verify/machine.py

CHECKPOINT[ie-1]:
- files-created: workspace_write.py (+ /tmp/ smoke tests, ephemeral)
- files-modified: chain-evaluator.py (check_a12 24h grace), phase-gate.py (BLOCK 4 sed-i)
- interfaces-matched: yes (IC[6] signature locked + published; IC[1] sed-i BLOCK wired)
- drift: none (all ADRs honored; renumbered sed-i to BLOCK 4 to preserve existing BLOCK 3 pre-shutdown semantics — minimum-disruption interpretation of plan line 161)
- surprises: (1) existing phase-gate already had BLOCK 1/2/3 defined (pre-shutdown); plan "BLOCK 3 sed-i" wording was pre-dating that. Ship as BLOCK 4, doc updated. (2) SQ[1] has an interpretation gap (see BUILD-CONCERN sent to lead); ADR[1] "auto-ready in build_machine()" can't change MCP tool advertisement without hateoas-agent cooperation — flagged via SendMessage, awaiting direction.

#### SQ[14] implementation-notes: workspace_write() helper
!signature-source-of-truth: lead's locked IC[6] spec in ## build-assignments Cross-cluster API contracts. ie-1 shipped to that signature verbatim, did not extend.

**File-location:** `~/.claude/teams/sigma-review/shared/workspace_write.py` (CREATED, 113 LOC incl. docstrings)

**Internal-helpers:** none. Implementation is stdlib-only: `os.path.expanduser` + `Path.read_text` + `str.replace(old, new, 1)` + `Path.write_text`. Zero runtime deps.

**Exception-hierarchy:** single `WorkspaceAnchorNotFound(Exception)` class — no subclasses. Raised on two conditions: (a) `old_anchor not in file_content`, (b) `updated == original` after replace (no-op guard, PM[4] silent-corruption protection). `FileNotFoundError` + `OSError` propagate unwrapped from Path.

**Test-hook surface (for CQA SQ[13] fixture):** pure function, no module-level state, no globals. CQA can assert on:
- `workspace_write(path, anchor, new) → None` on success, file content updated
- `WorkspaceAnchorNotFound` raised with message containing `anchor not found` or `replace produced no-op`
- original file content unchanged on any raise (verify via pre/post read)
- unicode-anchor roundtrip (αβγ, emoji, multi-line). No monkey-patching required.

**Self-validation (ie-1 local, not CQA work):** 4/4 smoke tests passed on /tmp/ temp-files (happy-path, missing-anchor, no-op guard, unicode) + dogfooded across 3 own-section writes to this scratch with zero anchor drift.

#### SQ[2] A12 24h grace-window — DONE
- **location:** chain-evaluator.py:234-275 (check_a12 rewritten)
- **behavior:** archive_file_found=False + workspace mtime <24h → PASS with grace-window issue note; workspace >24h old → FAIL as before
- **CAL[1] honored:** synchronous mtime delta, no poll/wait/sleep. Non-looping invariant preserved.
- **details emitted:** grace_window_applied:bool, workspace_age_hours:float (for chain-eval consumers + CAL-EMIT downstream)
- **smoke-tested both paths:** passed=True+grace=True for recent workspace ; passed=False+no-grace for 25h-old workspace (datetime.utcfromtimestamp mock via mtime manipulation)
- **test-surface for CQA SQ[13e]:** details.grace_window_applied + details.workspace_age_hours are the assertable fields

#### SQ[7]+SS-1 sed-i BLOCK — DONE (as BLOCK 4, not BLOCK 3)
- **location:** phase-gate.py:228-337 new check_sed_in_place + dispatch wire at line 274-276
- **scope:** workspace.md, teams/sigma-review/shared/, teams/sigma-optimize/shared/, /.claude/hooks/, /sigma-review/shared/, /sigma-optimize/shared/
- **tokenization:** shlex.split(posix=True) per ADR[SS-1]+IC[1]+CAL[4]
- **backup-form rule:** -i<SUFFIX> with non-empty suffix passes; bare -i, -i '', --in-place blocked (conservative interpretation of CAL[4] "backup-extension forms pass" — BSD empty-suffix treated as no-backup since it is functionally no-backup)
- **numbering rationale:** existing phase-gate has BLOCK 1 (code-write), 2 (git-commit), 3 (pre-shutdown promotion). Plan line 161 "BLOCK 3 sed-i" was written against older phase-gate (per module docstring pre-refactor). Preserving existing BLOCK 3 = zero-disruption interpretation per C5 defend-the-invocation rule. Updated docstring lists all 4 blocks + WARN 5.
- **smoke-tested 22/22** including: env wrapper, xargs -I{} positional, absolute sed path, post-&& chaining, BSD empty-suffix, multi-file, -i between flags, malformed parse-error
- **KNOWN GAP documented:** xargs with STDIN-piped paths is outside argv visibility (shlex.split scope per ADR[SS-1]). PM[SS-1] over-fire mitigation validated.

#### SQ[6] sigma-verify test scope — DONE (read-only)
- **Finding:** sigma-verify has its own test suite `~/Projects/sigma-verify/tests/` (17 test files, incl. test_machine.py 144 LOC, test_handlers.py 621 LOC)
- **Clarification:** per PF[5] sigma-verify is a SEPARATE commit scope. SQ[1] auto-ready test, if written, belongs in sigma-verify/tests/test_machine.py, NOT in sigma-system-overview test_gate_checks.py
- **Ownership recommendation:** CQA's cluster-C scope is sigma-system-overview test suite only. sigma-verify test for SQ[1] should either (a) be written by IE-1 in the sigma-verify repo (outside the ¬tests rule since separate repo + per-repo CQA doesn't exist), or (b) be deferred to a follow-up sigma-verify build. Awaiting lead decision on SQ[1] interpretation first — test shape depends on which mechanism is chosen.

#### SQ[1] sigma-verify auto-ready — BLOCKED on lead direction
- **Status:** BUILD-CONCERN[ie-1] sent to lead (see inbox). Awaiting confirmation of interpretation (A) probe+log+forward-compat-attr vs (B) server-side state-prime.
- **NOT redesigning:** following "flag and wait" per agent-def !rule ("if architecture is impractical during implementation → flag to lead + tech-architect with specific evidence"). All code prepared mentally; will ship within ~10 min of direction.

#### SQ[3] check_a3 DB extraction — BLOCKED on CQA SQ[0]
- **Status:** CQA SQ[0] MINIMAL_WORKSPACE fixture fix in-progress (task #20). IE-1 cannot touch chain-evaluator.py:162-183 (check_a3) until fixture unblocks per PF[2].
- **Prepared:** CAL[2] layered authority noted (gc=presence, chain-eval=depth, sequential not conflicting). IC[4] sequential-not-redundant contract confirmed in plan. Will split-by-DB then require (1)(2)(3) markers within segment per SQ[3] description. Est: 30-45 min post-unblock.
- **Gating check:** will monitor scratch ## build-status for CQA `UNBLOCKED` declaration before resuming.

#### test baseline (reference, not my work)
- test_gate_checks.py current state: 8 pre-existing fails / 60 pass (before my changes) — matches memory note of "MINIMAL_WORKSPACE fixture broken after roster.md addition"; confirmed non-regression by my 2 edits (ran pytest -k "session_end or archive or a12" post-edit: 2/2 pass)

#### git-status snapshot (¬committing per role boundary)
- ~/Projects/sigma-system-overview: modified chain-evaluator.py + phase-gate.py; new workspace_write.py (staged-ready)
- ~/Projects/sigma-verify: UNMODIFIED (SQ[1] pending lead direction)

#### next
- await lead on SQ[1] → ship ~8 LOC in machine.py + smoke
- await CQA SQ[0] UNBLOCKED → ship SQ[3] check_a3 rewrite
- persist execution patterns to sigma-mem patterns.md
- SendMessage lead with final completion summary


#### API-CONTRACT[ie-1→TW]: workspace_write() helper
!published-at: ~25% (start-of-work, pre-checkpoint) |gate: unblocks cluster-B directive/spawn-template references per cross-cluster contract

**File:** `~/.claude/teams/sigma-review/shared/workspace_write.py` (CREATED)
**Import:** `from workspace_write import workspace_write, WorkspaceAnchorNotFound`

**Signature (IC[6] locked):**
```python
def workspace_write(path: str, old_anchor: str, new_content: str) -> None:
    """Atomically replace old_anchor with new_content in path.

    Raises WorkspaceAnchorNotFound if old_anchor not in file, or if
    replace produces no-op (PM[4] silent-corruption guard).
    Raises FileNotFoundError if path missing.
    """
```

**Anchor rule (CAL[6]):** section-header + first-unique-content-line.
**Scope (convention, enforced at callsite):** workspace.md + builds/*/*.md + shared/workspace.md.
**Section-isolation:** agents write ONLY to own `### agent-name` section; anchor MUST include the section header so peers can write their own sections concurrently.

**Usage example (canonical pattern for spawn-template docs):**
```python
from workspace_write import workspace_write, WorkspaceAnchorNotFound

anchor = "### implementation-engineer\n*(populated by IE)*"
new_text = "### implementation-engineer\nSQ[1] DONE |SQ[2] DONE"
try:
    workspace_write(
        path="~/.claude/teams/.../c2-scratch.md",
        old_anchor=anchor,
        new_content=new_text,
    )
except WorkspaceAnchorNotFound:
    # anchor drifted — re-read file, pick fresh anchor, DO NOT blindly retry
    raise
```

**Smoke test (4/4 PASS, ie-1 local):** happy-path |missing-anchor-raises |no-op-guard-raises |unicode-anchor(αβγ emoji).

**TW action:** reference this import + signature in (a) spawn-template docs for `## workspace-write-pattern` block, (b) directives.md §X workspace-write-contract section. IC[6] is authoritative; direct quote signature rather than paraphrasing.

### technical-writer
status: in-progress |~55% complete |atomicity-constraints-coherent: yes |drift: none |surprises: none

CHECKPOINT[tw]: 8/10 SQs DONE, 2 pending |files-modified: c1-plan.md, c2-build.md, _template.md, sigma-lead.md, directives.md, build-directives.md |SQs-done: SQ[4](peer-verify atomic set), SQ[5]+SS-3(ΣVerify init), SQ[CDS-1](§2p), SQ[10/CDS-2/CDS-11](§2i), SQ[11/CDS-4](§2j governance artifact), SQ[12/CDS-3](§2d-severity + template checkboxes), SQ[CDS-12](DA CAL-EMIT verdict), §8e(corruption recovery ΣComm converted) |SQs-pending: SQ[9/CDS-5](Step 7a c1-plan.md), SQ[8](sed-i ban propagation 22 agents) |atomicity-constraints-still-coherent: yes |drift: none |surprises: none

#### atomicity compliance (CAL[9] peer-verify 4-file set)
- [x] c1-plan.md Step 11 spawn template: peer-verify canonical 3-hash "verifying" format + ΣVerify init + workspace-write rules
- [x] sigma-lead.md §2 spawn block: canonical format + section-isolation + regex-source doc
- [x] c2-build.md Step 2: SendMessage peer-verify + section-isolation + ¬sed-i
- [x] _template.md ## Peer Verification: canonical header rule + explicit ¬4-hash / ¬"verifies"
- [ ] 4-file commit staged atomically (NOT committed per lead/CQA merge-step instruction)

#### directive insertions (directives.md)
- §2i precision gate (sequential from §2h): dual-condition spec + CONDITION 2 code-detect + CONDITION 1 DIRECTIVE-only + path β+ calibration + CAL-EMIT format + A20
- §2p premise-audit pre-dispatch (non-sequential per CDS BC[TW-#5] confirmation): Step 7a workflow pointer + PA[1-4] format + sequence-constraint
- §2d-severity provenance (extension of §2d): 3-field tag + DA audit directive + A23 stub
- §2j HIGH-severity governance min-artifact: TIER-A/B/C + DA ARTIFACT-REVIEW + A22
- DA verdict on CAL-EMIT records: exit-gate format extension + PENDING handling (SQ[CDS-12])
- §8e workspace corruption recovery: 7-step ΣComm conversion (§8e-1..§8e-7) with cross-refs

#### BUILD variants (build-directives.md)
- §2i BUILD: CAL[]-compatible examples + A20 mode-agnostic
- §2p BUILD: Step 7a placement + PA[1-4] BUILD-scoped variants (tech-tier, scale-floor, data-readiness, precedent-baseline)
- §2d-severity BUILD: security/performance/test-gap severity extrapolation examples

#### agent-def updates
- _template.md: Boot step 5 ΣVerify init | Peer Verification canonical rule | Workspace Edit Rules block (¬sed-i + workspace_write helper + section-isolation) | Analytical Hygiene checkboxes §2i / §2j / §2d-severity
- sigma-lead.md: §2 peer-verify canonical + regex-source + section-isolation | ## Recovery cross-ref §8e 7-step

#### ΣComm boundary compliance (CAL[8])
- directives.md + build-directives.md + agent .md = agent-facing → ΣComm used throughout (!rule, !purpose, !when, !applies-to, !observed-failure-mode, →, ¬, |source:, PA[1-4], DB[], CAL-EMIT[])
- §8e: 7-step plain-English prose compressed to §8e-1..§8e-7 blocks with action verbs (PRESERVE/EXTRACT/REBUILD/COORDINATE/ATTEST/DOCUMENT/TRANSPARENCY) + !rule/!purpose directives. Not label-swap — genuine compression, cross-refs §8a/§8d/§6e/sigma-lead
- c1-plan.md + c2-build.md + sigma-lead.md: mixed (skill phase files semi-human-readable); ΣComm concentrated in spawn-prompt blocks + directive references per §3 ΣComm boundary

#### cross-cluster dependencies
- IE-1 workspace_write() API contract consumed via direct-import reference. Signature per IC[6]: `workspace_write(path: str, old_anchor: str, new_content: str) -> None` raising `WorkspaceAnchorNotFound`. Referenced in c1-plan.md Step 11 (## Workspace Write Rules) + sigma-lead.md §2 + c2-build.md Step 2 + _template.md ## Workspace Edit Rules
- No BUILD-CONCERN from IE-1 on signature extension — proceeding on locked contract per lead ack

#### remaining work
- SQ[9/CDS-5]: c1-plan.md Step 7a premise-audit insertion between Step 7 (user-confirmation of Q/H/C/cost) and Step 8 (prompt-understanding gate). Note: DIV[2] resolved TA's Step 7a position — sequence constraint "PA[1-4] BEFORE re-reading user H-space" preserved as implementation sub-rule within Step 7a. Add `## premise-audit-results` section to Step 10 workspace template.
- SQ[8]: sed-i ban propagation — append ## Workspace Edit Rules (sed-i sub-rule ONLY per CAL[7] risk-tier split) to 22 SAFETY-CRITICAL agent .md files. ¬#24 severity-provenance (template-only per risk-tier). [DONE — see findings]

#### final CHECKPOINT[tw]
CHECKPOINT[tw]: ALL 10 SQs DONE |files-modified: 29 (+686 lines) |SQs-done: SQ[4]+SQ[5/SS-3]+SQ[8]+SQ[9/CDS-5]+SQ[10/CDS-2/CDS-11]+SQ[11/CDS-4]+SQ[12/CDS-3]+SQ[CDS-1]+SQ[CDS-12]+§8e |atomicity-constraints-still-coherent: yes (CAL[9] 4-file peer-verify set all staged same-commit, lead/CQA to merge) |drift: none |surprises: 1 count-off-by-1 flagged to lead (23 AH-bearing agents, not 22 per CAL[7] spec — proceeded with 23-file propagation under safety-critical rule semantics)

#### SQ status summary
- SQ[4] #5+#14 peer-verify atomic: DONE |files: c1-plan.md Step 11, sigma-lead.md §2, c2-build.md Step 2, _template.md Peer Verification section |4-file atomic set ready for single commit
- SQ[5]+SQ[SS-3] ΣVerify init belt-and-suspenders: DONE |files: c1-plan.md Step 11 spawn template (## ΣVerify Init block), _template.md Boot step 5
- SQ[8] #1 sed-i ban propagation: DONE |files: _template.md + 23 SAFETY-CRITICAL agent .md files (count updated from spec 22, see flag to lead) |block: ## Workspace Edit Rules with phase-gate BLOCK 3 reference + workspace_write() helper + section-isolation
- SQ[9]+SQ[CDS-5] #21 Step 7a premise-audit: DONE |files: c1-plan.md Step 7a inserted (between Step 7 and Step 8), Step 10 scratch workspace template ## premise-audit-results section added, Preflight Phase Verification checklist extended
- SQ[10]+SQ[CDS-2]+SQ[CDS-11] §2i precision gate: DONE |files: directives.md §2i (sequential after §2h), build-directives.md §2i BUILD variant |CONDITION 2 code-detect + CONDITION 1 DIRECTIVE-only + path β+ calibration text + CAL-EMIT format
- SQ[11]+SQ[CDS-4] §2j HIGH-severity governance min-artifact: DONE |files: directives.md §2j (new section, not §3b extension per non-sequential pattern), build-directives.md pointer to §3b actionability extension |TIER-A/B/C taxonomy + DA ARTIFACT-REVIEW format + A22
- SQ[12]+SQ[CDS-3] §2d-severity provenance: DONE |files: directives.md §2d-severity extension, build-directives.md §2d-severity BUILD variant, _template.md Analytical Hygiene checkbox (template-only per CAL[7]) |3-field severity-basis tag + DA audit directive + A23
- SQ[CDS-1] §2p premise-audit directive: DONE |files: directives.md §2p (non-sequential per CDS BC[TW-#5] confirmation — sequential naming convention ends at §2h; §2p signals pre-dispatch step-tier), build-directives.md §2p BUILD variant with BUILD-scoped PA[1-4]
- SQ[CDS-12] DA verdict on CAL-EMIT: DONE |files: directives.md DA enforcement section extension |exit-gate format extension + PENDING handling + not-reviewed threshold
- §8e workspace corruption recovery: DONE |files: directives.md §8e (after §8d), sigma-lead.md ## Recovery cross-ref |ΣComm conversion from 7-step plain-English prose: §8e-1 PRESERVE through §8e-7 TRANSPARENCY, action-verb-per-step, !rule/!purpose/!trigger-conditions structure, cross-refs §8a/§8d/§6e/sigma-lead Recovery

#### final atomicity compliance
CAL[9] peer-verify 4-file atomic set: c1-plan.md Step 11 + sigma-lead.md §2 + c2-build.md Step 2 + _template.md ## Peer Verification |ALL staged same-commit-ready |regex unchanged per IC[5] (chain-evaluator.py _PEER_VERIFY_HEADER regex matches `### Peer Verification: X verifying Y` — propagated format matches exactly)
CAL[7] risk-tier split honored: sed-i = 23 agent files (SAFETY-CRITICAL fan-out); severity-provenance = _template.md only (calibration-only); precision-gate/governance-artifact = _template.md only via Analytical Hygiene checkboxes

#### cross-cluster coordination
- IE-1 workspace_write() helper consumed at 55% checkpoint + final findings via direct import (dogfooding IC[6] atomic Python replace). Two successful writes to scratch — happy-path verified. Signature per IC[6] locked: `workspace_write(path: str, old_anchor: str, new_content: str) -> None` raising `WorkspaceAnchorNotFound`.
- CAL-EMIT schema in directive text (SQ[CDS-11]) matches sigma-mem pattern P[CAL-EMIT-schema]: `CAL-EMIT[{gate-id}]: review-id:{slug} |finding-ref:{F[agent-id]} |fire-reason:{trigger} |workspace-context:{agent}:{50-char-excerpt} |da-verdict:PENDING` — CDS/IE-1 chain-evaluator emission (SQ[CDS-6..8]) must produce this exact format for audit-calibration-gate.py parsing (SQ[CDS-10]).
- A-check IDs used per PF[4] LOCKED assignment: A20 (§2i precision), A22 (§2j governance), A23 (§2d-severity), A24 (sigma-verify init pre-flight — referenced only, implementation is IE-1/CDS scope). A21 RESERVED not written anywhere.

#### surprises / drift / BUILD-CONCERNs
- none — no BUILD-CONCERN raised. Count-off-by-1 (22 vs 23 AH-bearing agents) was flagged as informational; proceeded on rule-semantics. No directive-text redesign. No content deviation from C1 DOC-CHANGE-MAP + ADRs + CDS specs.

#### verification path for C3 review
1. chain-evaluator regex match — verify _PEER_VERIFY_HEADER matches `### Peer Verification: X verifying Y` in all 4 propagated templates (c1-plan/sigma-lead/c2-build/_template)
2. phase-gate BLOCK 3 trigger — attempt `sed -i '' 'x' ~/.claude/agents/tech-architect.md` and verify BLOCK fires (SQ[7]+SS-1 code in IE-1 scope must be merged first)
3. §2i CAL-EMIT — craft workspace finding with `>70% confidence` tag + no driver breakdown → A20 WARN + CAL-EMIT record written to calibration-log.md (SQ[CDS-6] + SQ[CDS-9] code in IE-1/CQA scope)
4. §8e recovery — simulate corruption, follow §8e-1..§8e-7, verify ## recovery-log populated + attestation lines on restored sections
5. Step 7a premise-audit — run c1-plan.md through a fresh build, verify `## premise-audit-results` section appears in workspace before Step 11 spawn
6. sed-i ban propagation — `grep -l "## Workspace Edit Rules" ~/.claude/agents/*.md | wc -l` → expect 24 (23 propagated + _template.md)


## findings


## findings
*(Step 5 populates — per-agent final findings)*

### code-quality-analyst |decision-path for BUILD-CONCERN[cqa] extract_agents DA-inclusion 26.4.23

**Finding:** `gate_checks.extract_agents_from_workspace()` returns `devils-advocate` in its result list when roster.md includes DA (which it has since 26.4.11). All downstream checks that iterate this list (V3 agent-output-non-empty, V5 xverify-coverage, V6 dialectical-bootstrapping, belief-computation) fail on the DA "agent" because DA sections contain challenges/grades — not findings/DB/XVERIFY — by protocol design.

**Why this is a latent CODE bug, not test drift:**
1. Code comment at `gate_checks.py:223-224` documents stated intent: *"Also include 'devils-advocate' which is always valid but handled separately in some checks — include it in extraction"*. The phrase "handled separately in some checks" is a promise that was never kept — no downstream check filters DA.
2. Code comment AND original test assertion agree on the high-level design: DA is a special agent, not a work-producing agent; it should not be iterated for findings-content checks.
3. The exclusion-list fallback branch (`gate_checks.py:246`) ALREADY filters DA via `key != "devils-advocate"` — confirming original author intent when roster is unavailable. The roster-allowlist branch (lines 220-232) omitted this filter — inconsistent behavior across the two branches is the bug signature.
4. Git timeline: roster.md entry for devils-advocate added 2026-04-11 (via commits affecting roster). Before that addition, roster-allowlist path was effectively safe because DA wasn't in roster. Adding DA to roster flipped the runtime behavior of the allowlist branch without the filter keeping pace.

**Why NOT test-side alignment:**
Taking the "least-surprising test-update" path (update assertions to match current code behavior, i.e. expect DA in agents list + update downstream test expectations to match) would:
- Lock in the broken semantics: every future check iterating the agents list would need DA-special-case logic, defeating the point of the helper function.
- Propagate the inconsistency across test_gate_checks.py permanently (every new V-check test would need the same DA-handling workaround).
- Violate `feedback_realistic-tests.md` principle (tests must model real usage — real DA sections don't have F[]/DB[]/XVERIFY).
- Contradict the documented design intent in `gate_checks.py:223` comment.

**Routing decision:** per lead's ruling ("if latent bug → BUILD-CONCERN to ie-1"), sent BUILD-CONCERN[cqa] with 1-line fix recommendation to ie-1. Filter mirrors exclusion-list branch's existing `key != "devils-advocate"` pattern for consistency across the two branches.

**Plan-deviation flag:** plan ## Files line 162 says `gate_checks.py preserve — no edit`. This 1-line fix is a scope expansion. Rationale for flagging (not proceeding unilaterally): preserve directive was authored assuming gate_checks.py was stable; SQ[0] surfaces that it is not. Lead can ratify via confirming ie-1 fix OK, or rule otherwise.

**Alternative options considered and rejected:**
- Option A (fixture workaround): inject F[]/DB[]/XVERIFY into ### devils-advocate section. REJECTED — violates realistic-test principle, produces fixture that models no real DA output, contaminates SQ[13*] test data.
- Option B (refactor extract_agents signature): add `include_da: bool = False` parameter and update all callers. REJECTED — larger surface, every caller needs audit, not warranted for a 1-line semantics fix.

**Self-challenge (§2g DB):** (1) initial: this is a latent bug needing code fix. (2) assume-wrong: what if the design intent actually was "DA is included, callers must filter"? Then every V-check would need explicit DA-handling, which they don't — so the call sites assume DA is pre-filtered, aligning with the exclusion-list branch behavior and the original test. (3) strongest counter: the code comment is ambiguous — "handled separately" could mean DA-aware checks exist elsewhere. (4) re-estimate: examined each consumer of extract_agents in gate_checks.py — none special-case DA except check_cross_track_participation which parses `### devils-advocate` directly via regex (not via extract_agents). (5) reconciled: roster-allowlist branch missing `key != "devils-advocate"` filter is a latent bug; exclusion-list branch is correct; minimal fix = add filter to allowlist branch. source:[code-read gate_checks.py:220-250] T1-internal.

### code-quality-analyst |final findings 26.4.24

**Deliverables shipped:**
- **Files created:** test_audit_calibration_gate.py (31 tests), audit-calibration-gate.py (240 LOC script), calibration-log.md (empty append-only template)
- **Files modified (test-scope only):** test_gate_checks.py (fixture + 1 assertion pair rename), test_chain_evaluator.py (+21 tests across SQ[13b]+SQ[13c]+SQ[13d]+SQ[13e]), test_phase_gate.py (+9 tests across BLOCK 4 direct + shlex evasion + xargs positive-contract), backup-memory.sh (+5 lines: $CALIBRATION_LOG var and backup block)

**Test surface final:** 221/221 passing across full CQA test surface
- test_gate_checks.py: 68/68 |+0 new (fixture fix only)
- test_chain_evaluator.py: 63/63 |+21 new (SQ[13b]=2, SQ[13c]=10, SQ[13d]=6, SQ[13e]=3)
- test_phase_gate.py: 59/59 |+9 new (SedInPlaceBlock4 detection=6 including xargs-positive-contract, ShlexEvasionMatrix=3)
- test_audit_calibration_gate.py: 31/31 |NEW file (parse=8, evaluate=10, run=8, main=5)
- Net: +61 new tests shipped this cycle, 0 regressions against 143/143 baseline

**SQ completion status (owned by cqa):**
- PF[1] baseline reconciliation: DONE
- SQ[0] fixture fix: DONE (post-ie-1 gate_checks patch + test revert)
- SQ[13a]: covered by SQ[0]
- SQ[13b] A12 archive_file_found: DONE (2 tests)
- SQ[13c] A16/A17/A18 peer-verify: DONE (10 tests)
- SQ[13d] A3 DB genuine-vs-reference: DONE (6 tests)
- SQ[13e] A12 24h grace determinism: DONE (3 tests)
- SQ[13f] A20 precision CONDITION 2: BLOCKED — lead-owned scope gap (SQ[CDS-6..8] code doesn't exist)
- SQ[13g]+SS-2 sed-i BLOCK 4 + evasion matrix: DONE (9 tests incl. xargs positive-contract after BUILD-CONCERN resolution)
- SQ[CDS-6..8] WARN+CAL-EMIT tests: BLOCKED — same scope gap
- SQ[CDS-9] calibration-log + backup: DONE
- SQ[CDS-10] audit-calibration-gate.py: DONE

**BUILD-CONCERN[cqa] resolution:** xargs sed-i argv-vs-stdin bypass in phase-gate.py routed to ie-1 as docstring-only fix per option (a) ratified by user. I converted my removed-test comment into a positive-contract test (`test_xargs_stdin_is_known_limitation_not_blocked`) that asserts the gate does NOT block xargs stdin — locking in the documented limitation as test-enforced contract. If the implementation is ever extended to cover xargs, this test flips red and the update-is-breaking signal surfaces.

**Patterns worth persisting (will write to sigma-mem):**
- P[dataclass-python-3-14-importlib]: Python 3.14 dataclass introspection requires `sys.modules[name] = module` before `exec_module()` for `@dataclass` to resolve `cls.__module__`. Applies to any hyphen-filename script loaded via importlib.util. Seen 2x this session (audit-calibration-gate test + pre-existing chain-evaluator test pattern).
- P[fenced-code-block-parser-exclusion]: Doc-parser scripts that scan for marker-prefix lines (e.g. CAL-EMIT[) must skip content inside ``` fences or format-example documentation triggers false-positive parse errors. Encountered in audit-calibration-gate.py parse_log; fix is 3-line in_fence state toggle.
- P[positive-contract-for-known-limitations]: When a gate has an intentional blind spot (e.g. xargs stdin out-of-scope for shlex-argv), convert the would-be failing test into an asserting-False positive-contract test that documents the limitation in the test suite. Makes future implementation extensions self-signal (test flips red → update contract). Preferable to inline-comment-only documentation.
- P[ask-before-route-on-analysis-ack]: When lead says "analysis is clean," that is diagnostic validation, not routing approval. Plan-deviation routing requires explicit user ratification via lead broadcast. Rule: ask "is this ratified?" before SendMessage to peer on plan-scope items; do not infer routing approval from analysis-quality validation.

**Effort calibration datapoint for future builds (CAL[11]):**
- Plan SQ[13] estimate: 10-13h
- Actual: ~5-6h total across two cycles (3h recon + test writing, 2h BUILD-CONCERN triage + post-ratification cleanup + xargs positive-contract)
- Plan underestimate was directionally right (2-2.6x) but compressed by ie-1's well-documented code surfaces + pre-existing test-class clustering patterns
- Learn: split plan budget into (a) recon-per-SQ fixed ~30min, (b) test-writing scales with surface, (c) triage-per-BUILD-CONCERN fixed ~45min

### code-quality-analyst |cycle-2 findings (scope-extension) 26.4.24

**Scope-extension deliverables (SQ[13f] + SQ[CDS-6..8]):**
- +19 tests appended to test_chain_evaluator.py (63→82)
- Full CQA surface: **240/240 pass** (was 221/221 at cycle-1 close)
- Zero regressions from cycle-1 work
- Zero code bugs surfaced in ie-1's A20/A22/A23 shipment — all fire/suppress/schema contracts held on first test-run

**Test breakdown (cycle-2 additions):**
- **TestA20PrecisionGateCondition2** (6 tests, SQ[13f]): confidence≥70% / HIGH-severity / primary-recommendation trigger paths + 3 suppression paths (driver-breakdown, CI notation, approximately qualifier)
- **TestA20CALEmitSchema** (4 tests, SQ[CDS-6]): directive-schema compliance per line 351-352 (pipe-delimited fields in order, review-id slug, finding-ref, fire-reason, workspace-context, da-verdict:PENDING); no-fire empty-records; multi-fire per-agent; review_id fallback to date-prefix when no ## build-id header
- **TestA22GovernanceArtifact** (4 tests, SQ[CDS-7]): HIGH-sev+governance fire; TIER-A suppression in 800-char tail; ARTIFACT-GAP suppression; non-governance HIGH-sev no-fire (scope anti-gold-plating)
- **TestA23SeverityProvenance** (3 tests, SQ[CDS-8]): extrapolation+HIGH-sev fire; |severity-basis: tag suppression; native-domain HIGH-sev no-fire (scope narrow)
- **TestPathBetaPlusIntegration** (2 tests): file-write append when CALIBRATION_LOG_PATH exists (monkeypatch to tmp_path); silent-skip when file missing (record still in details)

**Discipline held throughout cycle-2:**
- Recon-first: read all three check functions + CAL-EMIT helpers + review_id derivation before writing any test (per P[sq-effort-budget-recon-plus-triage-floor] pattern I persisted)
- Fixture-isolated: monkeypatched `ce.CALIBRATION_LOG_PATH` to tmp_path for filesystem-integration tests — did not touch real `~/.claude/teams/sigma-review/shared/calibration-log.md`
- Zero BUILD-CONCERN needed — ie-1's A20/A22/A23 implementations matched directive spec exactly; all suppression heuristics and scope-narrowing contracts (MEDIUM no-fire, non-governance no-fire, native-domain no-fire) behaved as documented

**Cycle-2 effort actual:** ~45 min (30 min recon across 3 check functions + 15 min test-writing + ~2 min regression check). Total this extension: 19 tests in ~1h, consistent with the per-SQ recon + scaled-write budget from the pattern.

**Net CQA cluster-C final test surface:**
- test_gate_checks.py: 68/68 (fixture + assertion revert only)
- test_chain_evaluator.py: 82/82 (+40 new across cycle-1 SQ[13b/c/d/e] + cycle-2 SQ[13f/CDS-6..8])
- test_phase_gate.py: 59/59 (+9 new SQ[13g]+SS-2 incl. xargs positive-contract)
- test_audit_calibration_gate.py: 31/31 (NEW file, SQ[CDS-10])
- **Total: 240 passed / 0 failed | +80 net new tests this session | 0 regressions**

## cross-model-code-review
*(Step 6 populates — XREVIEW results, ¬anthropic per PF[7])*

## merge-log
MERGE-VERIFIED 26.4.24 by lead: 240/240 passed |regressions: 0 |all agent-shipped changes coexist |no worktrees (file-ownership coordination via scratch build-assignments; zero overlap across clusters)
- test_chain_evaluator.py 82/82 (cluster A ie-1 SQ[2]+SQ[3]+SQ[CDS-6..8]-emissions + cluster C cqa +40 tests)
- test_phase_gate.py 59/59 (cluster A ie-1 SQ[7]+SS-1 + xargs docstring narrow + cluster C cqa +9 tests)
- test_gate_checks.py 68/68 (cluster A ie-1 DA-filter + cluster C cqa fixture rename)
- test_audit_calibration_gate.py 31/31 (new file, cluster C cqa SQ[CDS-10])
- sigma-verify suite 300/300 (ie-1 SQ[1] in separate repo)

Cross-cluster handoff contracts verified in-production:
- IC[6] workspace_write(): dogfooded by TW at first-use (scratch writes via helper, zero anchor failures)
- CAL-EMIT schema match: TW directive §2i lines 351-352 + ie-1 chain-evaluator emission + cqa test assertions all converged on identical format
- A-check ID assignments (A20/A22/A23/A24, A21 reserved per PF[4]): honored by all clusters

## cross-model-code-review
SKIPPED — advisory per c2-build.md Step 6 ("does not block C2 exit"). Rationale: (1) build wall-time already 5h+, deferring XREVIEW to C3 where it's more critical; (2) 240/240 passing with zero regressions across 4 test files provides strong local validation; (3) C8 anthropic-exclusion narrows usable providers to google/openai which both had coverage issues this session (google 503 throughout C1, openai used in ADR XVERIFY already).
C3 will run XREVIEW as its final assessment step per sigma-build recipe.

## test-baseline
### code-quality-analyst |PF[1] resolution 26.4.23

AUTHORITATIVE-BASELINE: total=154 collected |passing=143 |failing=11 (pre-existing, SQ[0] fixture)
files (3-file canonical set, all present):
- agent-infrastructure/hooks/tests/test_chain_evaluator.py
- agent-infrastructure/hooks/tests/test_phase_gate.py
- agent-infrastructure/teams/sigma-review/shared/test_gate_checks.py (68 of 154 =44%; 11 failures here)

diagnosis: CQA C1 count (92) scoped to test_gate_checks.py alone and miscounted (actual 68, not 92). TA count (154) = three-file canonical set, correct. No test files "LOST" per auto-memory — both test_chain_evaluator.py (in hooks/tests/) + test_phase_gate.py (in hooks/tests/) present, intact, passing. Memory entry `project_hook-enforcement.md` wrong: "test_chain_evaluator.py + test_phase_gate.py LOST in refactor" is falsified — files exist at hooks/tests/, not at hooks/ root where original refactor note implied. Consolidation commits ea5ae97 + d9d21ad moved them, did NOT delete.

pytest repo-root scope: 1945 tests collected with 18 collection errors (sigma-verify tests error on missing modules, hateoas-agent test_integration.py marker warning) — out of scope for R19; C1 CQA likely hit scope confusion here.

all 11 failures trace to SQ[0] fixture-break: MINIMAL_WORKSPACE uses synthetic `agent-alpha`/`agent-beta`; gate_checks._load_roster_agents() (added 2026-04-11 per git log of gate_checks.py) + extract_agents_from_workspace() now filters via roster allowlist → synthetic names drop out → all downstream checks operate on empty or DA-only agent lists.

gate-clear: SQ[0] fixture fix UNBLOCKS: ie-1 SQ[3] (test_gate_checks.py TestV6DialecticalBootstrapping) + cqa SQ[13b-g] + CDS-6..10 + SS-2.

!flag-for-lead: while reconciling, found code/test divergence in `extract_agents_from_workspace` — code comment (gate_checks.py:223) says DA is INCLUDED from roster, but `test_extract_agents` asserts DA NOT in agents (line 193). Roster.md now includes devils-advocate. This is pre-existing drift (not SQ[0] scope) but SQ[0] fix surfaces it — I will update the test assertion to match CODE reality (DA included, len=3) as that reflects current merged behavior. Alternative would require code change to filter DA — OUT OF SCOPE for CQA test-cluster. Flagging for lead awareness, not requesting override.

POST-SQ[0]-COMPLETE 26.4.24: total=154 |passing=154 |failing=0 |regressions=0
SQ[0] COMPLETE: fixture fix (cqa) + gate_checks DA-exclusion (ie-1, user-ratified Option C) combined. Original `test_extract_agents` contract restored (DA not in agents, len=2) after ie-1 gate_checks fix shipped.
