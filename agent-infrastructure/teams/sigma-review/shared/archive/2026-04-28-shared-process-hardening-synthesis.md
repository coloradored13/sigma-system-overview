# Synthesis — sigma-build C3 close: shared-process-hardening (2026-04-28)

- build-id: 2026-04-28-shared-process-hardening
- tier: BUILD TIER-2 (score 16/25)
- C1 plan-locked: 2026-04-28
- C2 build-locked: 2026-04-29
- C3 review-completed: 2026-05-01
- C3 R2 (BLOCK 5 directive↔hook integration fix): closed 2026-05-02
- final build-belief: P=0.91 (R1 P=0.92 → 0.88 post-event-1 → 0.91 post-R2 close; final cap below 0.92 reflects two directive↔hook defects shipped + caught only by gate halt during close-out, not by test design)
- final build-exit-gate: PASS
- BUILD rubric: 22/24 = 3.67/4.0 (R1 22/24 → 21/24 post-event-1 → 22/24 post-R2; meets ≥A target ≥3.5/4.0)

## Prompt Understanding

Lifted verbatim from plan file `## Prompt Understanding (user-confirmed 2026-04-28)`.

**Q[]** (11):
- Q1 — A26 plan-completeness check
- Q2 — B5 C2 boot validation
- Q3 — TW Gap-Handling Rules
- Q4 — B6 C2 exit-gate diff
- Q5 — A14 race fix (exclude calibration-log)
- Q6 — A25 template-drift detection
- Q7 — _XVERIFY_ANY_RE regex tightening
- Q8 — Post-exit-gate workspace-headers directive
- Q9 — 06b compilation pre-archive gate
- Q10 — Premise-audit Step 7a sigma-review placement
- Q11 — Tests for all of the above

**H[]** (7):
- H1 — WARN-first ramp for items 1/2/4/6/8 (path β+)
- H2 — parser robustness incrementally normalizable (partially falsified at C1: keyword=value canonical, prose fallback)
- H3 — B5 boot-prompt format un-standardized (validated; new IC[8] schema created)
- H4 — A14 race fix has no behavioral side effects (validated wrapper-level only)
- H5 — item #9 marker vs INDEX scan (resolved → workspace-header)
- H6 — 10 items in one TIER-2 build (user-confirmed)
- H7 — Step 7a verbatim reuse (partially falsified: label dropped, structure survived)

**C[]** (10): see archived workspace `## prompt-understanding` for full text. Key:
- C2 — A14 race-fix MUST ship before A14 promotion event (out of scope)
- C3 — WARN-first default for new BLOCK gates
- C4 — A27 deferred
- C5 — P2.D follows P2.A
- C6 — zero regression on archived workspaces
- C10 — TeamCreate required, XVERIFY excludes anthropic

## Findings

### Hooks — chain-evaluator.py additions and modifications

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| A26 plan-completeness check (WARN-first) | check_a26_plan_completeness; chain-evaluator.py:1187-1303 | Anchored `^## plan-file\s*$` regex (BOM-aware, fenced-code excluded); fires WARN on missing/unresolvable plan-file ref; passed=True regardless. Excludes `## plans`, `## plan-file:`, `### plan-file`, fenced occurrences. | F[IE-3], ADR[3]/IC[2] |
| B5 C2 boot validation (WARN-first) | check_b5_c2_boot; chain-evaluator.py:1305-1419 | Reads `## agent-assignments` (canonical schema `SQ[N]: owner=AGENT \|cluster=FILE,FILE2,...`); falls back to `## sub-task-decomposition` with explicit fallback WARN; explicit zero-parse WARN when section is non-empty but no SQ-lines parse. | F[IE-4], ADR[2]/IC[3] |
| B6 C2 exit-gate diff (WARN-first) | check_b6_c2_exit_gate; chain-evaluator.py:1421-1584 | 3-pass CHECKPOINT parser: keyword=value primary → prose fallback → parse-fail. Cross-checks files-diff against `## agent-assignments`. | F[IE-5], ADR[4]/IC[4] |
| A14 race fix (wrapper-level) | check_a14 wrapper + `_a14_filtered_uncommitted` helper; chain-evaluator.py:339-449 | Wrapper re-runs `git status --porcelain` independently with timeout=10; applies `r"calibration-log\.md$"` exclusion; recomputes git_clean from filtered list; falls back to gc capped list on subprocess failure. gc.check_session_end UNCHANGED — A12 protection of shared helper preserved. Cap-at-10 fix verified via 15-file test. | F[IE-1], ADR[1]/IC[1] |
| A25 template-drift detection | check_a25_template_drift + `_a25_normalize`/`_a25_hash`; chain-evaluator.py:1547-1655 | LF-normalize + BOM-strip + per-line rstrip → SHA256. Baseline sidecar at templates/.templates-hash-baseline.json. WARN-first with recovery instructions naming sync-templates.sh. | F[IE-6], ADR[5]/IC[5] |
| _XVERIFY_ANY_RE regex tightening | chain-evaluator.py:1059-1062 (single consumer at :1130) | Bracket-required form `r"\bXVERIFY(?:-(?:FAIL\|PARTIAL))?\["` — drops colon/paren/whitespace alternatives so prose mentions cannot suppress. PM[2] mitigation honored: SQ[7] step 1 grep-audit confirmed single consumer (drifted from plan §:1021 to :1130 due to ~80 lines added by A14 wrapper). | F[IE-2], ADR[7]/IC[7] |
| ADR[9] universal edge-case helpers | shared `_strip_bom` + `_strip_fenced_blocks`; chain-evaluator.py:340-360 | Reused across A26 (:1207), B5/B6 via `_b5_extract_section` (:1336), A25; called BEFORE section search; empty-section → WARN-not-crash. DRY win surfaced as IE checkpoint surprise. | ADR[9], IC[8] |

### Phase-gate — BLOCK 5 06b pre-archive compilation gate

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| BLOCK 5 06b pre-archive compilation gate | phase-gate.py:386-503; new helpers + dispatch | Workspace header `## compilation-complete: [R-{id}]` checked via regex `^## compilation-complete: \[R-([^,\]]+)(?:, manual-override, reason: ([^\]]+))?\]$`. BLOCK fires when header absent on archive-write attempt. Manual-override form recovery: `## compilation-complete: [R-{id}, manual-override, reason: {reason}]`. `_is_sigma_session()` FP guard fires before archive-op detection. INDEX scan rejected (coupling); A28 WARN rejected (sequencing-gate semantics favor hard enforcement). | F[IE-7], ADR[6]/IC[6] |
| BLOCK message recovery instructions | phase-gate.py:467 (post-C3 r1: :495) | C3 r1 fix-1 corrected stale `sigma-lead.md:176` → `:207` after TW SQ[10] half-2 inserted ~31 lines at sigma-lead.md Step 1 ~38-72. Documentation-text fidelity fix; behavioral surface unchanged. | DA[#8], TA C3 r1 convergence |
| `_path_is_archive` KNOWN LIMITATIONS docstring | phase-gate.py:429-457 | Doc-only addition parallel to check_sed_in_place ADR[SS-1] template (phase-gate.py:280-311). Documents three bypass classes: (a) symlinks, (b) cwd-relative `..` traversal canonicalization mismatch, (c) macOS-specific case-insensitivity bypass. Names `os.path.realpath` + case-folding canonicalization as the closure path. Plan-faithful day-1 acceptance per plan §P2.A row 119. | DA[#5] accept-with-documentation |
| BLOCK 5 multi-path workspace scan (C3 R2 + R2-micro fix) | phase-gate.py: `BUILDS_DIR` + `_is_sigma_session` multi-source + `_has_compilation_complete` multi-path + archive_path-derived preferred-build short-circuit | R2 landed multi-path scan: `_is_sigma_session()` reads from workspace.md OR any `builds/{id}/c{N}-scratch.md` modified within 7-day window; `_has_compilation_complete()` checks workspace.md AND active build scratches. R2-micro fix (5-line short-circuit) closes TA CONCERN-1 cross-build authorization bypass: when archive_path can derive a preferred-build AND that build's directory exists AND it has no override, return False BEFORE the broad-glob fallback fires. Broad-glob fallback now fires ONLY when preferred-build is undeterminable. TA re-verified PASS with 3 empirical scenarios (cross-build r19 BLOCK, in-build PASS, cross-build sigma-v2 BLOCK). | C3 R2 IE-FIX, TA peer-verify, CQA regression |

### Directives — directives.md changes

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| §8f post-exit-gate workspace-headers | directives.md (between §8e and §9); A27 chain-eval gate WARN-first | Mandates four post-exit-gate headers: `## synthesis-complete`, `## promotion`, `## sync` (NEW — A27 WARN-first), `## archive-complete`. ADR[10] threshold preserved verbatim: ≥3 reviews where `## sync` absent + ≤20% FP per β+ A20 precedent (NOT "2+", which would have been silent threshold drift). DC[1-3] cross-refs incl. bidirectional §2p↔§8f. | F[TW-2], ADR[10] |
| TW Gap-Handling Rules section | technical-writer.md (between `## Weight` and `## Workspace Edit Rules`) | Paraphrase tests active: Q3-orphan-file (file in §Files, no SQ refs it) / Q3-undeclared-file (SQ refs file, not in §Files) / Q3-incomplete-row (Action\|Description blank). Escalation: BUILD-CONCERN blocks plan-exit-gate. PM[7] mitigation. | F[TW-1] |
| §8f BUILD-track variant (added in C3) | directives.md §8f new sub-section after existing line-1284 ANALYZE-side `## sync` form, before `!cross-references:` block at 1288-1294 | Compilation manual-override form (`## compilation-complete: [R-{id}, manual-override, reason: {reason}]`); authority = `lead-with-user-approval ONLY. ¬lead-only, ¬user-only`; AND-joined preconditions (a) failure-after-spawn (b) ≥1 retry documented (c) user-approval recorded; enforcement-model HONOR-SYSTEM with explicit acknowledgment that mechanical enforcement of authority (cryptographic approval, separate user-write file, role-based ACL) is OUT-OF-SCOPE this build; DC[4] cross-ref appended. Closes addressable portion of GAP[#5]; unaddressable portion documented as residual. | TW-FIX[#4], DA[#1] (4) |

### Agent-defs — sigma-lead.md changes

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| Premise-audit pre-dispatch sub-step | sigma-lead.md Step 1 (lines ~38-72) | Mirrors c1-plan.md:62 Step 7a HARD GATE: PA[1-4] tier-necessity / firm-size-floor / data-readiness / adoption-baseline; sequence-constraint (PA before H-space re-read); PREMISE-AUDIT[pre-dispatch] workspace template; decision line REQUIRED (chain-evaluator §2p presence-check); CHALLENGED/GAP rules; DA r2 cross-check at Step 5 (ANALYZE numbering). "Step 7a" label dropped on ANALYZE side per H7 r2 falsification (structure survives, label dropped to avoid renumber-cascade). | F[TW-4], SQ[10] half-2 |
| Compilation manual-override wording (C3 r1 fix-2) | sigma-lead.md:207 | Replacement: "If the compilation agent fails after at least one retry, the lead may invoke the manual-override form **only with explicit user approval in conversation**: `## compilation-complete: [R-{review-id}, manual-override, reason: {reason}]`. The reason text must name the specific failure mode (compilation-agent error, MCP unrecoverable, wiki-write blocked) and reference the retry attempt by timestamp or workspace section. Generic reasons (\"skipped\", \"ran out of time\") fail audit. The lead writes the manual-override form to workspace; user approval is recorded in conversation; the reason field captures user-supplied justification, not lead self-justification. See directives.md §8f for the full criterion and audit-trail expectation." Replaces previous wording "If compilation fails or is skipped intentionally, the operator may unblock with the manual-override form: ... requires an audit-traceable reason." Closes VP[1] wording-level concern. | TW-FIX[#3], IE-FIX[#2], DA[#1] (3) |

### Skills — sigma-review/SKILL.md changes

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| Premise-audit Step 1 extension | SKILL.md Step 1 Prepare extension | Mirrors c1-plan.md:62 Step 7a HARD GATE structure (PA[1-4], sequence-constraint, ## premise-audit-results section, decision line, CHALLENGED/GAP rules, DA r2 cross-check). "Step 7a" label dropped on ANALYZE side. Grep-audit (PM[8] mitigation) clean pre+post: "Step 7a" appears only in BUILD contexts (sigma-build/phases/c1-plan.md:62/137/138/174, build-directives.md:144/151) plus the deliberately bounded DC[3] cross-ref in directives.md. | F[TW-3], SQ[10] half-1 |

### Sync — sync-templates.sh and hash-identity utility

| Item | Implementation site | Behavior | Source |
|---|---|---|---|
| sync-templates.sh + hash baseline | ~/Projects/sigma-system-overview/agent-infrastructure/scripts/sync-templates.sh (NEW); chain-evaluator `_a25_normalize`/`_a25_hash` :1599-1610 | Python-embedded normalization (sync-templates.sh:40-42 embeds the same `BOM_RE.sub(...).replace(\r\n,\n).replace(\r,\n) + rstrip + SHA256` as chain-evaluator._a25_normalize:1605-1606). Same Python bytecode on identical input → identical output by construction. Baseline sidecar at templates/.templates-hash-baseline.json. | F[IE-6], ADR[5]/IC[5] |

### Tests

| Suite | Coverage | Result |
|---|---|---|
| chain-evaluator + phase-gate suites (post-fixes, R1) | 207/207 PASS in 2.93s; broader chain+phase+archive+step7a 251/251 PASS in 9.50s | clean baseline |
| Full hook-suite (R1 close) | 1245 passed / 14 skipped / 1 failed (1260 collected) — exact match to C2 baseline | zero new regressions |
| Full hook-suite (R2 close) | 1253 passed / 14 skipped / 1 failed (1268 collected) — +8 new tests from R2 multi-path scan | zero regressions vs C2 baseline |
| Sole failure (unchanged) | `test_structural_validation.py::TestSettingsJsonHooks::test_existing_settings_preserved` (settings.json `effortLevel='xhigh'` vs `'high'`) | pre-existing, predates C1 lock; documented as separate maintenance item |
| New tests added by C2 | 103 total: 59 IE + 7 TW + 37 CQA — all passing | — |
| New IE tests | TestA14RaceFix(7), TestA26PlanCompleteness(9), TestB5C2Boot(9), TestB6C2ExitGate(8), TestA25TemplateDrift(9), TestA24SigmaVerifyInitPreFlight(5 new), TestPreArchiveCompilationGate(12) | 59/59 PASS |
| New TW tests | test_step7a_cross_ref.py(7) — label-presence-in-BUILD, label-absence-from-ANALYZE-files (parametrized SKILL.md+sigma-lead.md), premise-audit-results-section-referenced, directives §2p cross-refs BUILD variant, directives §8f cross-ref to §2p, bounded-grep-audit | 7/7 PASS |
| New CQA tests | TestArchivedWorkspacePassthrough(18) on r19-remediation-workspace + ai-agent-rollout-playbook-vet 26.4.22 + sigma-chatroom-m1ab-workspace; TestDA12UniversalEdgeCases(13); TestVerificationSpotChecks(6) | 37/37 PASS |
| CQA C3 r1 cross-tool digest verification (added in C3 r1) | 7-fixture-class cross-tool digest equality run independently across LF, CRLF, BOM-prefix, mid-stream-BOM, mixed-EOL, unicode, trailing-WS-tabs (compares sync-templates.sh digest vs chain-evaluator._a25_hash on same input) | 7/7 cross-tool digest classes byte-identical |
| New tests added by C3 R2 (BLOCK 5 multi-path scan) | 8 total: 6 multi-path scan cases + 2 cross-build authorization cases | 8/8 PASS |

## Convergence and Tensions

### Convergences (independent derivation paths landed on same disposition)

- **Quad-convergence on GATE-1 actor authority** (`lead-with-user-approval`):
  - DA derivation: confirmation-rail (CLAUDE.md destructive-operations) + workspace-convention (lead writes `##` sections; `_COMPILATION_COMPLETE_RE` cannot itself verify user approval — honor-system reinforced by audit). [DA[#1]]
  - TA derivation: architectural precedent — sigma-lead.md §7c.5 promotion phase user-approval gate + CLAUDE.md destructive-operations confirmation rail; manual-override is hard-to-reverse, observable to next session, procedurally weak if lead-only. [TA C3 r1 ENGAGE[GATE-1]]
  - openai gpt-5.4 XVERIFY: medium-confidence agree — proposal "internally consistent... balances audit provenance and human-in-the-loop control better than either lead-only or user-only".
  - TW derivation: CLAUDE.md "Executing actions with care" rail + §8e RECOVERY attestation precedent + practical workflow under MCP-flap (feedback_user-approval-gate-non-bypassable.md 26.4.28: transport-failure ≠ gate-skip). [F[TW-C3-1]]

- **Triple-convergence on F[IE-6] disposition** (RESTATE not RETRACT):
  - DA: single-input induction → CQA's expanded run + TA's deductive proof jointly upgrade evidence base; restate per CQA wording is the right disposition. [DA[#2]]
  - TA: deductive code-construction proof — sync-templates.sh:40-42 embeds the same Python `normalize()` heredoc as chain-evaluator._a25_normalize:1605-1606; identical bytecode on identical input → identical output by construction. Same-platform byte-identity is deductively guaranteed. [TA ENGAGE[F[IE-6]]]
  - CQA: independent re-run on 7 fixture classes (LF, CRLF, BOM-prefix, mid-stream-BOM, mixed-EOL, unicode, trailing-WS-tabs) — 7/7 cross-tool digest byte-identical. Cross-platform parity remains designed-in (shared normalize sequence) but NOT empirically tested across actual platforms (single-interpreter macOS Python 3.14). [CQA C3 r1]

- **Two-layer landing on cleanup-pass precedence rule** (per DA[#7] correction): in-build ratification (one-line plan ## Close Status) AND memory-compile candidate (global pattern at sigma-mem ^patterns.md, Step 15 user-approval gate). TW initially framed as memory-compile-only; DA[#7] argued in-build ratification is required so future archive readers see editorial verdicts disguised as cleanup with explicit in-build correction; TW updated to two-layer landing.

### Tensions and disaggregation

- **VP[1] vs GAP[#5] disaggregation per DA[#3]**: cleanup pass framed VP[1]+GAP[#5] as "two reviewers flag the same governance gap." More accurate framing (now adopted in close):
  - VP[1] |severity:LOW |scope:wording at sigma-lead.md:207 |reviewer:TW peer-verify of IE F[IE-7] — closed via TW-FIX[#3] / IE-FIX[#2] sigma-lead.md:207 wording change.
  - GAP[#5] |severity:MED |scope:enforcement-model gap on regex/path-match surface |reviewer:openai gpt-5.4 XREVIEW phase-gate.py BLOCK 5 — addressable portion closed via TW-FIX[#4] directives.md §8f directive honor-system acknowledgment; unaddressable portion (mechanical authority enforcement) accepted as documented residual.
  - Close-status presents these as TWO separate line-items, not a single combined deliverable.

- **NEW tension surfaced in C3 r1 (not in C2 inventory)**: DA[#4] documented MultiEdit/NotebookEdit dispatch gap — phase-gate.py:445 dispatch covers only `tool_name in ("Write", "Edit")` for direct path detection; MultiEdit and NotebookEdit accept file_path/notebook_path arguments and could legitimately write to archive paths without triggering BLOCK 5. Disposition: accept-with-documentation; logged as follow-up SQ for next build. NOT a fix here (would be scope-expansion past locked plan §P2.A row 119 day-1 BLOCK mandate).

- **TWO directive↔hook integration events surfaced at C3 close** (both flagged by synthesis-agent halting on the BLOCK rather than silently bypassing — the gate working as designed):
  - Event 1 — synthesis-precedes-compilation sequencing trap (2026-05-01): phase-gate BLOCK 5 fired correctly at the synthesis-agent's archive-write attempt because c3-scratch did not contain the required `## compilation-complete` header. Trap is structural — c3-review.md Step 14a defines compilation as reading synthesis as input, so compilation cannot structurally precede synthesis. Resolved via lead-with-user-approval manual-override under exception clause; logged as next-build follow-up SQ with 4 ranked options.
  - Event 2 — BLOCK-5-WORKSPACE-PATH defect (2026-05-02): even after lead wrote the override header to c3-scratch.md, BLOCK 5 continued firing. Code-read of phase-gate.py revealed `DEFAULT_WORKSPACE = Path.home() / ".claude/teams/sigma-review/shared/workspace.md"` (line 43, hardcoded) — `_has_compilation_complete()` and `_is_sigma_session()` both read ONLY from this path. The directive this build ratified (directives.md §8f BUILD variant) instructs lead to write the header to BUILD scratch (`builds/{id}/c{N}-scratch.md`), but the hook never reads BUILD scratches. The recovery hatch was structurally unreachable for any BUILD-track session. Surfaced because workspace.md still held the unrelated 2026-04-23 ai-agent-rollout-playbook-vet ANALYZE workspace, also misclassifying THIS session as in-sigma based on stale file content. **Resolved via in-build R2 fix (option b)**: IE landed multi-path scan + R2-micro short-circuit; TA flagged + verified CONCERN-1 (cross-build authorization bypass via broad-glob fallback) closed; CQA regression clean; 8 new tests; full suite 1253/14/1.

## DA Roll-up

| # | Target | Severity | Disposition | Resolution mechanism |
|---|---|---|---|---|
| DA[#1] | GATE-1 — VP[1]+GAP[#5] manual-override actor authority | HIGH | concede/fix | 4 deliverables shipped: actor lock (`lead-with-user-approval`) + 3-precondition criterion (compilation-spawned-failed AND ≥1-retry AND user-approval-recorded) + sigma-lead.md:207 verbatim wording replacement + directives.md §8f BUILD variant sub-section with honor-system acknowledgment |
| DA[#2] | F[IE-6] "VERIFIED empirically" wording | MED | concede/fix (RESTATE not RETRACT) | F[IE-6] restated to "VERIFIED empirically on macOS Python 3.14 across 7 fixture classes... Cross-platform parity is **designed-in** via shared normalization sequence but NOT empirically tested across actual platforms"; sigma-mem pattern `hash-parity-empirical-verify` flagged for revision at Step 15 promotion |
| DA[#3] | Dual-confirm framing on VP[1]+GAP[#5] | MED | concede/fix | VP[1] (LOW, wording) and GAP[#5] (MED, enforcement-model) preserved as SEPARATE artifacts; close-status presents two separate line-items, NOT a single combined deliverable |
| DA[#4] | GAP[#1+#3] Bash regex incomplete coverage in BLOCK 5 + NEW MultiEdit/NotebookEdit dispatch gap | MED | accept-with-documentation | Plan-faithful day-1 BLOCK accepts residual per plan §P2.A row 119; tightening would be scope-expansion past locked plan; logged as follow-up SQ for next build (memory-compile pattern: phase-gate dispatch must enumerate ALL tool_names that can write paths, not just Write/Edit) |
| DA[#5] | GAP[#2] path normalization in `_path_is_archive` (substring-match bypass) | LOW-MED | accept-with-documentation | KNOWN LIMITATIONS docstring block added to `_path_is_archive` (parallel to check_sed_in_place ADR[SS-1] precedent at phase-gate.py:280-311); mechanical doc-only addition; no behavior change |
| DA[#6] | §2d source-provenance audit on F[TW-1..4] (no canonical `\|source:` tags) | LOW | accept-and-route | promotion-candidate (c) §2d enum extension with [doc-edit]/[directive-write]/[cross-ref-grep] types — separate build (P2.D follows P2.A per plan); not a C3 close-out blocker |
| DA[#7] | Cleanup-pass structural conflation (mechanical canonicalization vs editorial classification) | MED-meta | concede/fix | Two-layer landing: in-build ratification (one-line in plan ## Close Status) + memory-compile candidate (global pattern, ΣComm at sigma-mem ^patterns.md, Step 15 user-approval gate) |
| DA[#8] | phase-gate.py:467 stale BLOCK-message line ref (sigma-lead.md:176 → :207) | LOW | concede/fix | IE-FIX[#1] applied: phase-gate.py:467 (post-edit :495) updated to `sigma-lead.md:207`; 207/207 phase-gate+chain-evaluator tests PASS |
| DA[#9] | Stale line-numbers recurring-cost pattern | LOW | accept-with-documentation | Reader-side reconciliation accepted for this build; promotion-candidate "stale-line-number lint rule" pattern logged for next build's plan-track |

CB-not-fired: 9 substantive challenges (≥3 required). DA grade: B+ CONDITIONAL-PASS r1 → effective PASS post-fix (all dispositions resolved; 6 concede/fix + 3 accept-with-documentation per DA's own recommendation).

## BUILD Rubric

Per build-directives §3b (1-4 each). Score trajectory across close-out events:

| Dimension | C3 r1 | post-event-1 | post-R2 (final) | Rationale (final) |
|---|---|---|---|---|
| correctness | 4/4 | 4/4 | 4/4 | All 12 SQs DONE C2 + all 4 C3 r1 fixes applied cleanly + R2 multi-path scan + R2-micro CONCERN-1 fix applied cleanly + ADRs satisfy contracts + IC[6] regex matches verbatim (TA peer-verify confirmed regex+helpers UNCHANGED post-FIX-2 and post-R2; behavioral surface preserved beyond authorization narrowing) |
| test-coverage | 3/4 | **2/4** | **3/4** | Original tax: F[IE-6] hash-parity tests use same `_a25_hash` on both sides. Event-1 tax: test design did not exercise synthesis-write-before-compilation-header sequencing. **R2 restoration**: 8 new tests for multi-path scan + cross-build authorization (TA-empirical 3 scenarios) recover the missing sequencing-and-integration coverage on this gate. Not 4/4 due to documented residuals (CONCERN-2 suffix-stripper coverage; GAP-D fenced-block parity with chain-evaluator ADR[9]) |
| maintainability | 4/4 | 4/4 | 4/4 | KNOWN LIMITATIONS docstring parallel to ADR[SS-1] convention + ΣComm in directive content + plain English in agent-prose per sigmacomm boundary + stale-line-number drift fixed + cleanup-pass precedence rule ratified + R2 short-circuit pattern preserves the broad-glob fallback for legitimate fall-through cases |
| performance | 4/4 | 4/4 | 4/4 | Single-user O(1) hook fires (~10-50/day); no performance considerations. R2 multi-path scan uses 7-day mtime window so glob count remains bounded |
| security | 3/4 | 3/4 | 3/4 | BLOCK 5 enforces against accidental archive writes + honor-system enforcement-model openly acknowledged + GAP[#1+#3] (Bash regex bypass) and GAP[#2] (path normalization) accepted-with-documentation. R2-micro CONCERN-1 short-circuit ALSO closes a fresh authorization-bypass class introduced by the multi-path scan (cross-build override leakage via broad-glob fallback). Tax: residuals remain documented |
| api-design | 4/4 | 4/4 | 4/4 | Header schema `## compilation-complete: [R-{id}]` clean and matches IC[6] regex char-for-char + manual-override form parameterized + bidirectional cross-refs sigma-lead.md:207 ↔ directives.md §8f. R2 multi-path scan API contract: archive_path-derived preferred-build is explicit input; broad-glob is fallback only |

**Total: 22/24 = 3.67/4.0** (R1: 22/24 → post-event-1: 21/24 → post-R2: 22/24). Meets c3-quality-targets ≥A (≥3.5/4.0). Beats R18+R19 recurring B 3.14 weakness profile.

## Pre-mortem Tracking

| PM | Failure mode | Mitigation | Activated? | Failure avoided in practice |
|---|---|---|---|---|
| PM[1] (TA) | A26+B5+B6 false-positives on archived workspaces silently accumulate | SQ[11] WARN-only mode + counts-logged + ≥3 archives covered | Yes | TestArchivedWorkspacePassthrough 37/37 PASS on 3 frozen archives (r19-remediation-workspace + ai-agent-rollout-playbook-vet 26.4.22 + sigma-chatroom-m1ab-workspace); WARN-only invariant + no-regression invariant VERIFIED |
| PM[2] (TA) | SQ[7] _XVERIFY_ANY_RE replacement breaks existing test fixtures | SQ[7] step 1 grep-audit before replace | Yes | Step 1 grep-audit completed BEFORE replace; confirmed single consumer at chain-evaluator.py:1130 (drifted from plan §:1021 due to A14 wrapper +80 lines); zero risk to existing fixtures; 17/17 TestA24 + cross-coverage PASS |
| PM[3] (TA) | A14 race-fix overly-broad glob accidentally excludes legitimate dirty files | Precise regex `r"calibration-log\.md$"` + .bak non-exclusion test | Yes | TestA14RaceFix case (d) `.bak` non-exclusion test PASSES; anchored `\.md$` rejects `.bak` |
| PM[4] (TA) | A25 sync-script hash drifts on macOS LF vs Windows CRLF | Normalize before hash (LF, BOM-strip, rstrip) | Yes (partially) | Same-platform parity demonstrated empirically (CQA C3 r1: 7/7 cross-tool digest classes byte-identical on macOS Python 3.14); cross-platform parity remains designed-in via shared normalization sequence but NOT empirically tested across actual platforms — restated wording captures this distinction |
| PM[5] (TA) | item #9 phase-gate.py BLOCK misfires on non-sigma sessions | `_is_sigma_session()` guard + manual-override recovery form | Yes | `_is_sigma_session()` FP guard fires before archive-op detection; manual-override form available with workspace-recorded reason. **Note (post-event-1+2)**: at synthesis dispatch the FP guard correctly classified the session as in-sigma; the trap was in the sequencing model AND in the workspace-path lookup (event-2). Both gaps surfaced and closed at close-out. R2 multi-path scan now reads workspace.md OR active build scratches |
| PM[6] (TA) | SQ[9] split risks one-of-pair shipping without sibling | B1 option-i single-owner consolidation eliminates split | Yes | SQ[9] single-owner IE; phase-gate.py + sigma-lead.md:176 (post-TW-SQ[10]: :207) + tests delivered atomically |
| PM[7] (TW) | Directive ambiguity → agent misinterpretation | Paraphrase test in DC review; canonical wording in gate-log | Yes | TW Gap-Handling Rules paraphrase tests Q3-orphan-file/Q3-undeclared-file/Q3-incomplete-row active; CQA C3 r1 paraphrase tests on sigma-lead.md:207 + directives §8f BUILD variant returned UNAMBIGUOUS verdict |
| PM[8] (TW) | Workflow-step renumbering breaks cross-refs | SQ[10] grep-audit step | Yes | Pre+post grep-audit clean; "Step 7a" only in BUILD contexts (sigma-build/phases/c1-plan.md:62/137/138/174 + build-directives.md:144/151) plus the deliberately bounded DC[3] cross-ref in directives.md |
| PM[9] (TW) | ΣComm/plain-English boundary violation in directive content | sigmacomm skill compliance check at C2 review | Yes | sigmacomm boundary maintained: ΣComm for directive content (agent-facing) + plain English for sigma-lead.md operational instruction (human-facing) + plain English for in-build ratification line in close-status |
| **PM[NEW-1] (post-event-1)** | **Synthesis-archive write blocked because compilation cannot structurally precede synthesis (compilation reads synthesis as input per c3-review.md Step 14a)** | **None — failure mode not anticipated in pre-mortem; no mitigation pre-built** | **Fired at synthesis dispatch 2026-05-01** | **Failure avoided via lead-with-user-approval manual-override; user-supplied justification recorded; logged as follow-up SQ for next build with 4 ranked resolution options** |
| **PM[NEW-2] (post-event-2)** | **BLOCK 5 reads only DEFAULT_WORKSPACE (workspace.md) but directives.md §8f BUILD variant instructs lead to write override header to BUILD scratch — recovery hatch mechanically unreachable for BUILD-track sessions; FP guard misclassified session via stale workspace.md content** | **None — failure mode not anticipated in pre-mortem; no test exercised the directive↔hook integration end-to-end** | **Fired post-event-1 retry 2026-05-02 when lead-written c3-scratch override produced no visible change in gate behavior** | **Closed via in-build R2 fix (option b): IE multi-path scan + R2-micro CONCERN-1 short-circuit + TA empirical 3-scenario peer-verify + CQA regression + 8 new tests; full suite 1253/14/1; gate now reads workspace.md OR active build scratches with archive_path-derived preferred-build authorization** |

## Open Questions

### C3 advisory carry-forwards (accept-with-documentation; logged as follow-up SQ for next build)

- **DA[#4]** — GAP[#1+#3] Bash regex incomplete coverage in BLOCK 5 (redirects without `cat`, shell expansions, command substitution, nested `bash -c`, scripting-language indirection) + **NEW C3 r1 finding**: MultiEdit / NotebookEdit dispatch gap not in C2 inventory (phase-gate.py:445 dispatch enumerates only Write/Edit; MultiEdit and NotebookEdit accept file_path/notebook_path and can legitimately write to archive paths without triggering BLOCK 5).
- **DA[#5]** — GAP[#2] `_path_is_archive` substring-match bypass surface (symlinks, `..`, case differences). KNOWN LIMITATIONS docstring added in-build; mechanical fix deferred (out of scope per plan §P2.A row 119 day-1 BLOCK mandate per ADR[6]).
- **DA[#9]** — Stale-line-ref recurring-cost pattern → promotion-candidate "stale-line-number lint rule" (e.g., /sigma-audit grep `sigma-lead\.md:\d+` references against current line numbers) for next build's plan-track.
- **(Event-1 origin) Synthesis-precedes-compilation sequencing trap** — surfaced 2026-05-01 at synthesis dispatch when phase-gate BLOCK 5 fired on the synthesis-archive write attempt for this very build. Resolution path is structural, not a one-line fix. Plan ## Build Review Summary advisory carry-forwards records 4 ranked resolution options for next build:
  1. BLOCK 5 synthesis carve-out — exempt synthesis-archive paths from the gate (narrow tool_name + path-pattern carve-out at phase-gate.py:471-485) so synthesis can write before compilation runs.
  2. c3-review.md re-ordering — flip Step 13f and Step 14a so compilation precedes synthesis-archive write; requires compilation to read scratch (not synthesis) as input.
  3. directives.md §8f BUILD variant criterion extension — add a fourth precondition class (d) "synthesis-precedes-compilation structural exception" with documented criteria so the manual-override path is the canonical resolution rather than a per-event exception.
  4. Make synthesis NOT an archive write — write synthesis to a non-archive workspace path first, then archive at compilation completion; decouples synthesis dispatch from the archive gate.

### CQA-surfaced follow-up SQ (R2 close)

- **GAP-D (HIGH)** — `_strip_fenced_blocks` parity with chain-evaluator ADR[9] missing in phase-gate.py header scan; promote ADR[9] universal edge-case helpers from chain-evaluator.py:340-360 to apply to phase-gate.py header scans, not just chain-evaluator gates. Memory-compile candidate: parallel-solution opportunity — same edge-case classes (BOM, fenced-code, empty-section) apply to both files; sharing the helpers prevents drift.
- **GAP-A/B/C** — correct-by-construction edge cases for BLOCK 5 multi-path scan (no explicit tests; consider adding); R2 ships with property-correct logic but explicit edge-case tests would harden.
- **GAP-E (low impact)** — trailing-WS `$` anchor in `_COMPILATION_COMPLETE_RE`.
- **CONCERN-2 (LOW)** — suffix-stripper extension for archive-name conventions (`-c{N}-scratch`, `-audit`, `-eval`, `-vet`); current suffix-stripper covers the common cases but not all sigma-track archive name shapes.

### GAP[#5] unaddressable portion (documented residual)

`_COMPILATION_COMPLETE_RE` in phase-gate.py cannot mechanically verify the user actually approved. Authority is honor-system reinforced by audit (reason-field text + /sigma-audit BUILD-CONCERN on generic reasons). Mechanical enforcement of authority (cryptographic approval, separate user-write file, role-based ACL) is OUT-OF-SCOPE this build per ADR[6] day-1 BLOCK mandate. Explicitly named as residual in directives.md §8f BUILD variant `enforcement-model: HONOR-SYSTEM` paragraph.

### Separate maintenance item (not blocking)

Pre-existing test failure: `test_structural_validation.py::TestSettingsJsonHooks::test_existing_settings_preserved` (settings.json `effortLevel='xhigh'` vs `'high'`). Predates C1 lock; surface to backlog.

## In-build ratification — cleanup-pass precedence rule

Per TW-MEMO[#2] / DA[#7] in-build ratification requirement, ratified for the shared-process-hardening build C3 close-status snapshot (plain English):

> Mechanical edits in cleanup passes (line-number reconciliation, test-count reconciliation, typo fixes, schema-tag presence checks) are lead-authoritative and need no adversarial layer. Editorial verdicts in cleanup passes (severity-tier reclassification, source-tag categorization when judgment-call, promotion-candidate flagging, retroactive elevation of carry-forwards) require either an adversarial-layer engagement or an explicit lead-with-criterion (named decision rule + named decision-maker — same shape as GATE-1) before they can be made under a "cleanup" label. This precedence rule is ratified for the shared-process-hardening build C3 close-status snapshot.

The corresponding global rule (memory-compile candidate at sigma-mem ^patterns.md, Step 15 user-approval gate per CLAUDE.md "Lead Role Boundaries" + feedback_user-approval-gate-non-bypassable.md) extends the rule with a presentation rule (separate sub-sections, ¬commingle under one heading) and an audit hook (sigma-audit Check N+1 — editorial subsection without authority-path citation → BUILD-CONCERN).

## Process-Integrity Notes

### Two integration events surfaced during close-out (both flagged by synthesis-agent halting on the BLOCK rather than silently bypassing)

**Event 1 — Synthesis-precedes-compilation sequencing trap** (surfaced 2026-05-01): at synthesis dispatch, phase-gate BLOCK 5 (the 06b pre-archive compilation gate this very build shipped) correctly fired on the synthesis-agent's archive-write attempt because the workspace did not contain the required `## compilation-complete: [R-{id}]` header. The trap is structural — c3-review.md Step 14a defines compilation as reading synthesis as input, so compilation cannot structurally precede synthesis, but BLOCK 5 expects compilation-complete in workspace before any archive op. Resolved via lead-with-user-approval manual-override under exception clause (precondition-gap exception, user-supplied justification recorded by lead at c3-scratch.md:801). Logged as follow-up SQ for next build with 4 ranked resolution options.

**Event 2 — BLOCK-5-WORKSPACE-PATH defect** (surfaced 2026-05-02): even after the lead wrote the override header to c3-scratch.md, BLOCK 5 continued firing on retry. Code-read of phase-gate.py revealed `DEFAULT_WORKSPACE` was hardcoded at line 43 to `~/.claude/teams/sigma-review/shared/workspace.md` (ANALYZE convention), and both `_has_compilation_complete()` and `_is_sigma_session()` read ONLY from that path. The directive this build ratified (directives.md §8f BUILD variant) instructs lead to write the override header to BUILD scratch (`builds/{id}/c{N}-scratch.md`), but the hook never reads BUILD scratches. The recovery hatch was mechanically unreachable for any BUILD-track session. Compounding: the workspace.md file held an unrelated 2026-04-23 ai-agent-rollout-playbook-vet ANALYZE workspace, so `_is_sigma_session()` was misclassifying THIS session as in-sigma based on stale file content. **Closed via in-build R2 fix (option b)**: IE landed multi-path scan (BUILDS_DIR + 7-day window + multi-source `_is_sigma_session` + multi-path `_has_compilation_complete` with archive_path-derived preferred-build); TA flagged CONCERN-1 cross-build authorization bypass via broad-glob fallback; IE landed R2-micro short-circuit (5-line: when preferred-build derivable + dir-exists + no override → return False before broad-glob fires); TA re-verified PASS with 3 empirical scenarios (cross-build r19 BLOCK, in-build PASS, cross-build sigma-v2 BLOCK); CQA regression clean; 8 new tests; full suite 1253/14/1.

### IE calibration self-disclosure (positive signal)

During R2 close, IE pre-emptively flagged that their first R2 empirical test (PM-NEW-2 verification) had omitted `hook_event_name` from the JSON payload, causing main() to short-circuit exit=0 regardless of gate logic. The R2 empirical claim was therefore non-load-bearing on actual gate behavior. Same anti-pattern class as F[IE-6] (single-input demo masquerading as evidence) — but caught and disclosed by IE themselves rather than by an adversarial pass. R2-micro re-verified with correct JSON shape and produced a load-bearing empirical claim.

This is a process-integrity positive: P3.4 anecdotal-vs-hardened distinction is being internalized by the agent that originated F[IE-6]. The same class of error was made twice (single-input demo without checking that the demo actually exercises the path it claims to) but the second instance was caught by the agent before it shipped, not after. Memory-compile pattern reinforced: when running empirical tests against a hook, verify the harness invocation actually reaches the code path under test before reporting the result.

### Process-integrity meta-finding

The build's own honor-system enforcement (BLOCK 5 + the lead-with-user-approval directive at directives.md §8f BUILD variant, both shipped + ratified in this very build) worked as designed. Synthesis-agent halted twice without silent bypass. The recovery hatch was structurally broken in BOTH events — but each was surfaced by gate-halt + agent honesty rather than missed:
- The gate fired when it was supposed to (event 1: archive write without compilation-complete; event 2: same, after override written to wrong file).
- The agent halted instead of routing around (writing to a non-archive path, forging a header in workspace.md, asking for a "creative" workaround).
- The lead refused to silently elevate to manual-override without user-supplied justification AND, when the override didn't work, escalated rather than concluding "the gate is broken, ship anyway."
- The build ran the in-build R2 fix through the same multi-agent process (IE + TA peer-verify + CQA regression) rather than letting the lead patch and ship.

The honor-system limitation acknowledged in directives.md §8f §"enforcement-model: HONOR-SYSTEM" is what made these events recoverable. If the gate had been silently bypassable, neither event would have surfaced; the synthesis would have been written, the directive↔hook integration defect would have shipped invisibly, and the next BUILD-track session would have hit the same wall.

### Other notes

- **build-exit-gate semantic drift**: c3-review.md Step 1 expects PENDING; current convention (precedent: r19-remediation) sets PASS at C2 close, with C3 reaffirming after review. Documentation-hygiene candidate flagged in c3-scratch BOOT validation; not blocking.
- **chain-evaluator A14 reports legitimate drift carried from C2**: 3 files modified (sigma-system-overview: patterns.md, .retro-last-hash, .skill-usage.jsonl). Race-fix correctly NOT masking legitimate drift; resolved at Step 16 sync per c3-scratch gate-log.
- **Honor-system limitation explicitly acknowledged**: directives.md §8f BUILD variant `enforcement-model: HONOR-SYSTEM` paragraph names mechanical alternatives (cryptographic approval, separate user-write file, role-based ACL) as OUT-OF-SCOPE this build per ADR[6] day-1; closes addressable portion of GAP[#5]; mechanical enforcement OUT-OF-SCOPE per ADR[6] day-1.
- **Contamination check**: clean. Session-topics-outside-scope: none. Agent context firewalls held — DA + TA + IE + TW + CQA each operated on plan file + scratch + named source files only. Lead-side dispatch references only build-internal artifacts.
- **Sycophancy check**: clean. No softening, no selective-emphasis, no dissent-reframed. F[IE-6] "VERIFIED empirically" wording was changed (not defended); DA[#7] cleanup-pass precedence rule was ratified in-build (not deferred); honor-system limitation openly acknowledged in directive content (not hidden); two integration events reported as real test-design gaps with rubric tax accepted (not minimized as procedural hiccups); IE's self-disclosed empirical-harness error reported as positive calibration signal (not buried). Quad-convergence on GATE-1 actor (DA + TA + openai gpt-5.4 + TW) and triple-convergence on F[IE-6] (DA + TA + CQA) are real with documented independent derivation paths — not artifactual agreement-seeking.
- **Peer-verify ring closed**: TA→IE PASS 4/4 (R1 FIX-1+2+3+4) + CQA→TW PASS (directive Edit + dual-confirm disaggregation) + IE→CQA from C2 still holds (regression baseline preserved 1253/14/1 post-R2) + TA→IE PASS on R2 multi-path scan + R2-micro CONCERN-1 short-circuit (3 empirical scenarios verified).
- **XVERIFY**: openai gpt-5.4 single-provider verify_finding per build-directives §2h fallback (cross_verify multi-provider hung per known infra issue); anthropic excluded per CLAUDE.md feedback_xverify-anthropic-excluded:26.4.23. Result: partial / medium-confidence on ADR[6]/IC[6] BLOCK 5 compliance — agreed regex+FP-guard verbatim; flagged same `:176` stale ref TA flagged independently (DA[#8] convergence).
- **User-approval gate**: GATE-1 went through AskUserQuestion before dispatch (not auto-elevated by lead). Per feedback_user-approval-gate-non-bypassable.md (26.4.28): transport-failure does not authorize gate-skip. Event-1 manual-override and Event-2 R2 in-build-fix were likewise user-approved per the directive this build ratified, not lead-self-authorized.
- **Lead role boundary**: zero analytical tools called by lead. Routing/dispatch only. Synthesis written by separate agent at Step 13.
