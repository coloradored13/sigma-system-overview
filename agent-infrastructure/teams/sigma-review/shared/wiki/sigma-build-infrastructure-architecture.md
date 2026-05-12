# Sigma-Build Infrastructure Architecture
Last updated: 26.5.9 | Reviews: B-r19-remediation, R-2026-04-28-shared-process-hardening, R-2026-05-05-block-5-synthesis-carveout

## Summary

Sigma-build is enforced by two mechanical-gate scripts plus a calibration sidecar: `chain-evaluator.py` (atomic A-checks A1–A26, fired by the Stop hook), `phase-gate.py` (transition-time BLOCKs 1–5), and `audit-calibration-gate.py` (β+ promotion telemetry). The R19 remediation build added four new analytical-tier checks (A20/A22/A23/A24), a fourth phase-gate BLOCK (sed-i ban with shlex tokenization), the `workspace_write` helper for safe gate-log appends, and the calibration-log promotion mechanism. Several "multi-layer contract drift" defects surfaced in C3 — producer/consumer schema decoupling between chain-evaluator and audit-calibration-gate is the dominant failure class. [B-r19-remediation, 26.4.25]

[R-2026-04-28-shared-process-hardening, 26.5.2] The shared-process-hardening build added six new chain-evaluator checks (A26 plan-completeness, B5 C2 boot validation, B6 C2 exit-gate diff, A14 race fix, A25 template-drift detection, _XVERIFY_ANY_RE regex tightening), the BLOCK 5 06b pre-archive compilation gate in phase-gate.py with a multi-path workspace scan added at C3 R2, and the directives.md §8f BUILD-track variant (compilation manual-override form, lead-with-user-approval authority, honor-system enforcement model). Two directive↔hook integration defects surfaced and were closed during C3 close-out — both caught by the gate halting rather than silent-bypassing. See [Directive-Hook Integration Pattern](directive-hook-integration-pattern.md) for the meta-finding.

[R-2026-05-05-block-5-synthesis-carveout, 2026-05-09] The synthesis-carveout micro-build (WS-2 of the shared-process-hardening remediation plan) added the `_is_synthesis_archive_write` path-class predicate and a short-circuit in `check_pre_archive_gate` that exempts synthesis-archive writes from the BLOCK 5 compilation-complete precondition. The exemption resolves a structural impossibility: synthesis-archive writes occur at c3-review.md Step 13f, which must precede compilation at Step 14, so gating synthesis on compilation-complete is a logical cycle. BUILD rubric §3b mean 3.67/4.00 with both 3-scores (test-coverage, security) explicitly bundling their gaps into a proposed `block-5-synthesis-carveout-followups` micro-build under WS-3 Tier-C sequencing. Final belief P=0.91. The build also surfaced a new failure-mode class — escape-vs-spoof asymmetry in substring-matching predicates — distinct from the parent ADR[6] symlink/case-fold/`..` deferred residuals.

---

## Chain-Evaluator A-Checks

Atomic, non-looping checks fired by the Stop hook. Each `check_aN_*` function reads workspace evidence and emits a verdict; failures produce gate-log records the lead must address before chain completion.

### A12 (archive-file presence + 24h grace window)
A12 verifies that an archive file exists for the current build/review. Two R19 fixes shipped:
- **Parser key rename**: `archive_file_found` (was `archive_found`) — pre-applied in commit a2a7fa8 to unblock TA-driven downstream consumers. [B-r19-remediation, 26.4.25]
- **24h grace window**: synchronous mtime delta with literal `24.0h` threshold at `chain-evaluator.py:306`. Non-looping invariant preserved (no polling, no retry — single mtime read). [B-r19-remediation, 26.4.25]

### A20 / A22 / A23 (path-β+ analytical gates)
Three WARN-first analytical checks added in C2 cluster A, each emitting a CAL-EMIT record on fire so audit-calibration-gate can track promotion eligibility:
- **A20**: precision gate (false-precision via qualifier detection — see β+ calibration page).
- **A22**: governance min-artifact (TIER-A/B/C taxonomy + DA ARTIFACT-REVIEW format; scope narrowness via `_GOVERNANCE_MARKERS_RE`).
- **A23**: §2d severity provenance (3-required-fields format: severity + |source: + |severity-basis:; regex character-for-character identical with directive checkbox and `_template.md`).

All three share the same architectural pattern: probe → match → CAL-EMIT to calibration-log → WARN to gate-log. Lead binary-check happens at A15 (per-agent); β+ continuous tracking happens via audit-calibration-gate. [B-r19-remediation, 26.4.25]

### A24 (sigma-verify pre-flight coverage)
Added in C3 round 2 after DA[#1] surfaced it as missing-from-shipped-code despite being LOCKED in plan at five layers (PF[4] + ## Files line 162 + PM[1] mitigation + ## Verification step 3 + Scope Boundary). [B-r19-remediation, 26.4.25]

A24 fires when (a) sigma-verify is available, (b) load-bearing markers are present in workspace, (c) no XVERIFY tag is found within the 500-char window. Honors A20-style load-bearing markers and is tolerant of all three XVERIFY states per directives §2h. Path-β+ WARN-first per CDS calibration-design lens.

A24 is a per-finding β+ complement to A15's per-agent binary check. It intentionally has no Condition-1-style suppression heuristic — A20 catches false-precision via qualifiers; A24 catches missing-XVERIFY which qualifiers don't resolve. [B-r19-remediation, 26.4.25]

### A3 (DB-step parser, layered authority)
A3 extracts dialectical-bootstrapping evidence. R19 fix: split-by-DB tokenizer + (1)(2)(3) requirement detection. IC[4] layered authority preserved — `result = gc.check_dialectical_bootstrapping(content)` keeps the upstream object intact; layer-2 augments details only. No double-counting. [B-r19-remediation, 26.4.25]

### A14 (race-fix wrapper for git-status calibration-log exclusion)
[R-2026-04-28-shared-process-hardening, 26.5.2] A14 verifies the working tree is git-clean at session end. The race-fix wrapper at `chain-evaluator.py:339-449` re-runs `git status --porcelain` independently with timeout=10, applies a precise `r"calibration-log\.md$"` exclusion to filter out legitimate calibration-log writes from the dirty-file list, recomputes git_clean from the filtered list, and falls back to the gate-controller's cap-of-10 list on subprocess failure. The shared `gc.check_session_end` helper is intentionally NOT modified — A12 protection of the shared helper is preserved at the wrapper layer. Cap-at-10 fix verified via 15-file test case; `.bak` non-exclusion case (`r"\.md$"` anchored, rejects `.bak`) covered by TestA14RaceFix case (d). The wrapper layering pattern (modify-at-call-site, leave-shared-helper-untouched) is reusable when a check needs targeted exclusion that other consumers of the same helper must NOT inherit.

### A25 (template-drift detection via SHA256 normalization)
[R-2026-04-28-shared-process-hardening, 26.5.2] A25 detects drift between sigma-build template files (e.g., `_template.md`, agent boot-prompt templates) and a baseline hash sidecar. `chain-evaluator.py:1547-1655` LF-normalizes (BOM-strip + per-line rstrip) before SHA256-hashing each template. Baseline lives at `templates/.templates-hash-baseline.json`. WARN-first with recovery instructions naming `sync-templates.sh`. The companion sync script at `~/Projects/sigma-system-overview/agent-infrastructure/scripts/sync-templates.sh:40-42` embeds the SAME Python normalize heredoc (`BOM_RE.sub(...).replace("\r\n","\n").replace("\r","\n") + rstrip + SHA256`) as `chain-evaluator._a25_normalize:1605-1606`. By construction, identical input on the same Python interpreter produces byte-identical output across both tools. Cross-platform parity is **designed-in** via shared normalization sequence but NOT empirically tested across actual platforms (single-interpreter macOS Python 3.14 only). CQA C3 r1 verified 7 fixture classes byte-identical on macOS: LF, CRLF, BOM-prefix, mid-stream-BOM, mixed-EOL, unicode, trailing-WS-tabs. The "VERIFIED empirically" → "designed-in but not cross-platform-tested" wording change is a pattern-template for hash-parity verification — single-interpreter testing is not a cross-platform claim, even when the normalization is correct-by-construction.

### A26 (plan-completeness check, WARN-first)
[R-2026-04-28-shared-process-hardening, 26.5.2] A26 verifies the workspace declares its plan-file via the canonical `^## plan-file\s*$` anchored heading. `chain-evaluator.py:1187-1303` uses BOM-aware regex with fenced-code-block exclusion to avoid false positives from `## plans`, `## plan-file:`, `### plan-file`, and fenced occurrences. WARN-first per H1 ramp; `passed=True` regardless of result. Empty-section condition produces a WARN (not a crash) via the universal edge-case helpers (see ADR[9] below).

### B5 (C2 boot validation, WARN-first)
[R-2026-04-28-shared-process-hardening, 26.5.2] B5 reads the `## agent-assignments` section (canonical schema `SQ[N]: owner=AGENT |cluster=FILE,FILE2,...`) at `chain-evaluator.py:1305-1419`. Falls back to `## sub-task-decomposition` with explicit fallback WARN; emits explicit zero-parse WARN when the section is non-empty but no SQ-lines parse. The section-parse pattern is reusable for any future check that reads structured agent-assignment data — the schema lives in IC[3] and the fallback chain is intentional (allows incremental adoption while flagging non-canonical authoring).

### B6 (C2 exit-gate diff, WARN-first)
[R-2026-04-28-shared-process-hardening, 26.5.2] B6 cross-checks `## c2-exit-gate` CHECKPOINT records against the `## agent-assignments` cluster lists. Three-pass parser at `chain-evaluator.py:1421-1584`: keyword=value primary → prose fallback → parse-fail. The keyword=value primary form is the canonical schema (per IC[4]); prose fallback exists to absorb pre-canonical workspaces without forcing rewrites. Cross-checks files-diff against agent-assignments to catch "agent shipped a file not in their cluster" and "agent didn't ship a file in their cluster."

### _XVERIFY_ANY_RE bracket-required tightening
[R-2026-04-28-shared-process-hardening, 26.5.2] `chain-evaluator.py:1059-1062` (single consumer at :1130). The regex was tightened to `r"\bXVERIFY(?:-(?:FAIL|PARTIAL))?\["` — bracket-required, drops colon/paren/whitespace alternatives. Prose mentions of "XVERIFY" cannot suppress the gate; only canonical bracketed forms `XVERIFY[...]`, `XVERIFY-FAIL[...]`, `XVERIFY-PARTIAL[...]` count. PM[2] mitigation pattern (grep-audit-before-replace) confirmed the single consumer at :1130, with a documented drift from plan §:1021 to :1130 due to ~80 lines added by the A14 wrapper. Treat plan-referenced line numbers as advisory and grep-confirm before edits.

### ADR[9] universal edge-case helpers (DRY win)
[R-2026-04-28-shared-process-hardening, 26.5.2] `_strip_bom` and `_strip_fenced_blocks` shared helpers at `chain-evaluator.py:340-360`, reused across A26 (:1207), B5/B6 via `_b5_extract_section` (:1336), and A25. Always called BEFORE section search; empty-section produces WARN-not-crash. The DRY win surfaced as an IE checkpoint surprise — the third gate to need BOM/fenced handling made it cheaper to centralize than to copy. **Open**: phase-gate.py header scan does NOT yet share these helpers; CQA flagged this as GAP-D (HIGH) follow-up — promote ADR[9] to apply to phase-gate.py header scans, not just chain-evaluator gates. Same edge-case classes (BOM, fenced-code, empty-section) apply to both files; sharing the helpers prevents drift.

---

## Phase-Gate BLOCK 4 (sed-i Ban)

Phase-gate.py enforces transition-time hard blocks. R19 added BLOCK 4 (renumbered from a previous BLOCK 3 that was already in the codebase — this drift caused 27 stale "BLOCK 3" doc references swept by TW in C3-r2 OPTION 2 phrasing).

**Mechanism**: scope-pattern-match (path) + `shlex.split(posix=True)` tokenization. The shlex tokenizer collapses `-i""` / `-i ''` / joined `-i''` into a bare `-i` flag, neutralizing zero-space evasion variants. Empirically traced 7 evasion forms and passed all 7: BSD `-i ''`, joined `-i''`, env-wrapper, xargs-positional, absolute `/usr/local/bin/sed`, backup `-i.bak`, xargs-stdin. [B-r19-remediation, 26.4.25]

**Known limitation (xargs stdin)**: the bypass enumeration is preserved in `phase-gate.py:300` as inspectable contract. SS dissented from DA[#4]'s framing concern that listing bypasses in the docstring "advertises" them — SS's position (lead-accepted): listing specific bypass forms in the enforcement file IS the contract; concealing them would be worse security hygiene. Threat model is accidental silent corruption, not sophisticated-adversary evasion. [B-r19-remediation, 26.4.25]

The OPTION 2 phrasing introduced post-hoc — "phase-gate enforces the sed-i BLOCK mechanically" (drops numeric identifier) — is block-number-agnostic and future-renumber-immune. CAL[R3-2-canonical-block-hash-identity] subsumes the weaker CAL[R2-OPTION2-phrasing] after R3-2 resync. [B-r19-remediation, 26.4.25]

---

## Phase-Gate BLOCK 5 (06b Pre-Archive Compilation Gate)

[R-2026-04-28-shared-process-hardening, 26.5.2] BLOCK 5 enforces that compilation runs before any archive write. It fires when the workspace lacks the required `## compilation-complete: [R-{id}]` header at the time an archive-op is attempted.

**Header schema and regex** (`phase-gate.py:386-503`):

```
## compilation-complete: [R-{id}]
## compilation-complete: [R-{id}, manual-override, reason: {reason}]
```

Matched by `^## compilation-complete: \[R-([^,\]]+)(?:, manual-override, reason: ([^\]]+))?\]$`. The bracketed-and-anchored form prevents prose mentions and accidental near-matches. `_is_sigma_session()` FP guard fires before archive-op detection so non-sigma sessions are not blocked.

**Why BLOCK day-one (not WARN-first ramp)**: ADR[6] decided the gate semantics are sequencing-not-analytical (the gate enforces "compilation-came-first," which is binary, not a quality judgment). WARN-first ramps make sense when calibration data is needed to set the FP threshold; BLOCK 5 has no FP threshold to set — either compilation completed before the archive write or it didn't. INDEX-scan implementation alternative was rejected during ADR resolution due to coupling concerns (BLOCK 5 should not require the wiki INDEX to be authoritative on which archive-paths exist).

**Multi-path workspace scan (C3 R2 + R2-micro fix)** [R-2026-04-28-shared-process-hardening, 26.5.2]: BLOCK 5 originally read only from `DEFAULT_WORKSPACE = ~/.claude/teams/sigma-review/shared/workspace.md` (hardcoded at `phase-gate.py:43`). This was correct for ANALYZE-track sessions but mechanically unreachable for BUILD-track sessions, because `directives.md §8f BUILD variant` instructs the lead to write the manual-override header to BUILD scratch (`builds/{id}/c{N}-scratch.md`), not to workspace.md. The hook never read BUILD scratches. R2 added `BUILDS_DIR` plus a multi-source `_is_sigma_session()` (reads workspace.md OR any `builds/{id}/c{N}-scratch.md` modified within a 7-day window) and a multi-path `_has_compilation_complete()` (checks workspace.md AND active build scratches). The R2-micro short-circuit (5-line addition) closes the cross-build authorization bypass that R2 introduced: when `archive_path` can derive a preferred-build AND that build's directory exists AND its scratch has no override, return False BEFORE the broad-glob fallback fires. Broad-glob fallback now fires ONLY when preferred-build is undeterminable. TA empirically verified PASS via three scenarios: cross-build r19 BLOCK, in-build PASS, cross-build sigma-v2 BLOCK.

**Manual-override recovery form**: `## compilation-complete: [R-{id}, manual-override, reason: {reason}]`. Authority is `lead-with-user-approval ONLY`. Three AND-joined preconditions: (a) compilation-spawned-failed, (b) ≥1 retry documented, (c) user-approval recorded. The reason text must name the specific failure mode (compilation-agent error, MCP unrecoverable, wiki-write blocked) and reference the retry attempt by timestamp or workspace section. Generic reasons ("skipped", "ran out of time") fail audit. The lead writes the manual-override form to workspace; user approval is recorded in conversation; the reason field captures user-supplied justification, not lead self-justification. See `directives.md §8f` for the full criterion.

**Honor-system enforcement model — explicitly acknowledged residual**: `_COMPILATION_COMPLETE_RE` in phase-gate.py cannot mechanically verify the user actually approved. Authority is honor-system reinforced by audit (reason-field text + sigma-audit BUILD-CONCERN on generic reasons). Mechanical enforcement of authority (cryptographic approval, separate user-write file, role-based ACL) is OUT-OF-SCOPE per ADR[6] day-1 BLOCK mandate. The directive content names this residual openly rather than concealing it. This is the canonical pattern for honor-system gates: when a gate's mechanical enforcement covers the *occurrence* but not the *authorization*, name the gap in the directive text rather than letting it surface only via post-hoc audit.

**KNOWN LIMITATIONS docstring on `_path_is_archive`** (`phase-gate.py:429-457`) — doc-only addition parallel to `check_sed_in_place ADR[SS-1]` template at `phase-gate.py:280-311`. Documents three bypass classes: (a) symlinks, (b) cwd-relative `..` traversal canonicalization mismatch, (c) macOS-specific case-insensitivity bypass. Names `os.path.realpath` + case-folding canonicalization as the closure path. Plan-faithful day-1 acceptance per plan §P2.A row 119 — mechanical fix would have been scope-expansion past the locked plan.

**Tool-name dispatch gap** (DA[#4], accept-with-documentation): `phase-gate.py:445` enumerates only `tool_name in ("Write", "Edit")` for direct path detection. MultiEdit and NotebookEdit accept `file_path`/`notebook_path` arguments and could legitimately write to archive paths without triggering BLOCK 5. Bash regex coverage is also incomplete (redirects without `cat`, shell expansions, command substitution, nested `bash -c`, scripting-language indirection). Logged as follow-up SQ for next build; promotion-candidate pattern: phase-gate dispatch must enumerate ALL tool_names that can write paths, not just Write/Edit.

**Synthesis-archive carve-out (ADR[1] of R-2026-05-05-block-5-synthesis-carveout)** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: BLOCK 5 has a path-class exemption for synthesis-archive writes. Two-condition predicate `_is_synthesis_archive_write(path: str) -> bool` at `phase-gate.py:623-646` returns True iff BOTH (a) Condition A: `os.path.basename(path)` ends with `-synthesis.md` (exact suffix, case-sensitive); and (b) Condition B: any marker from `_ARCHIVE_PATH_MARKERS` is a substring of `path` (mirrors `_path_is_archive`). Both required; ambiguity → False (gate fires on doubt). Input normalization: accept `str` only, strip leading/trailing whitespace + BOM, empty/whitespace-only → False, case-sensitive (no case-folding), no symlink resolution, no relative-path normalization. Consumer short-circuit lives in `check_pre_archive_gate` at `phase-gate.py:684-687`, positioned AFTER `if not is_archive_op: return False, ""` (the outer `is_archive_op` guard) and BEFORE `_has_compilation_complete`, with an `archive_path and` guard so Bash-extraction-failed (`archive_path=None`) falls through to broad-glob fail-safe (PM[4]). Three alternatives explicitly rejected during ADR resolution: §a1 regex on full path (audit-fragile), §a2 INDEX-based scan (introduces I/O dependency), §a3 A28 WARN-only advisory (does not resolve structural impossibility — hard carve-out required), §a4 blanket archive exemption (over-broad; only synthesis writes have the structural-impossibility argument).

**Rationale**: synthesis-archive write occurs at c3-review.md Step 13f; compilation-complete header is written at Step 14. Synthesis→compilation is the dependency order. Gating synthesis archive write on compilation-complete creates a logical cycle. Confirmed empirically — the trap that motivated this build was a synthesis-archive write to `2026-04-28-shared-process-hardening-synthesis.md` blocked because no compilation-complete header existed yet. Replay of the original trap with the carve-out present returns exit=0 (would have eliminated both close-out events in the parent build).

**ADR[1] AMENDMENT r3 (post-DA[#1] amendment-drift fix)** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: the original "no new bypass class" claim was too absolute. Corrected to "no new bypass class **beyond the deferred-residual limitations already accepted in ADR[6]** of parent build" (KNOWN LIMITATIONS docstring + mechanical fix DEFERRED — not a threat-model exclusion). Inherits ADR[6]'s symlink/HFS+ case-fold/relative-`..` limitations flat at the predicate level; **compounds them at the consequence level** (gate-removal for synthesis-write path vs archive-classification-only for `_path_is_archive`). The compilation-complete header is an integrity boundary, not merely a convenient precondition (gpt-5.4-pro reasoning-tier reframe absorbed). Bounded by: (1) single-user hook context (write origin is Claude Code agent under BLOCK 1 plan-lock), (2) visibility — `-synthesis.md` construction in archive dir is visible in session history, (3) multi-layer chain — compilation-complete is one integrity layer, not the sole control.

**Escape-vs-spoof asymmetry as a separate failure class** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: C3 DA[#1] (external `challenge` gpt-5.4-pro reasoning-tier vuln=HIGH) surfaced substring-overmatch as a failure class **independent of ADR[6] inheritance**. AMENDMENT r3 line 104 covers escape-direction (an in-archive path appearing to be out-of-archive via symlinks/`..` — ADR[6] inheritance) but NOT spoof-direction (an out-of-archive path appearing to be in-archive via substring match). Concrete vector: `/tmp/sigma-review/shared/archive/foo-synthesis.md` (a /tmp path containing the marker as substring) returns True from `_is_synthesis_archive_write`. The same flaw exists in the parent `_path_is_archive` (`_ARCHIVE_PATH_MARKERS` substring check, no boundary anchoring). Resolution: TA DEFEND-WITH-COMPROMISE — keep code, bundle boundary-aware-matching into `block-5-synthesis-carveout-followups` micro-build applied symmetrically across `_path_is_archive` + `_is_synthesis_archive_write` (architectural unit). DA ACCEPTED. The unified hardening would close DA[#1] + DA[#2] + the parent ADR[6] symmetry gap together. This makes escape-vs-spoof a distinct named failure class joining the existing inheritance residuals.

**Test coverage** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: `TestBlock5SynthesisCarveOut` at `test_phase_gate.py:1293-1464` ships 5 tests — (a) main path PASS without compilation header, (b) carve-out short-circuit DIRECTLY (with dual pre/post sanity assertions at :1363+:1371 mechanically proving the short-circuit branch is the load-bearing resolution path, not the FP guard), (c) WS-1 R2-micro multi-path regression preserved, (d) Condition A failure (non-`-synthesis.md` filename still blocks), (e) Condition B failure (synthesis-named path outside archive dir still blocks). PM[5] over-broad-short-circuit caught by tests (d)+(e). Hook-suite parity 1286/14/0 across three independent runs (IE C3-boot 10.69s, IE post-fix 10.60s, CQA fix-validation 10.96s). 2 pre-existing tests in `TestBlock5MultiPathWorkspace` were re-targeted from `-synthesis.md` to `-workspace.md` to preserve invariants that the carve-out short-circuit was shadowing (sibling `test_build_id_extraction_from_archive_path` confirms `_build_id_from_archive_path` strips both suffixes identically; intent preserved). DA[#2] OVERMATCH near-miss test is a documented gap deferred to followups; bundling rationale is symmetric with DA[#1] boundary-aware-matching.

**Cross-references** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: a Tier-1 ΣComm cross-ref lives at `directives.md:1353` (§8f BUILD variant) naming the predicate, both Conditions, and the ADR[1] source-tag; a Tier-3 plain-English cross-ref lives at `sigma-lead.md:207` (Step 7b) with all four required tokens present (Step 13f, synthesis, compilation-complete, carve-out). Boundary-aware matching is the recommended next architectural pass (followups micro-build) applied **symmetrically** across `_path_is_archive` and `_is_synthesis_archive_write` — fixing only the synthesis predicate would leave the parent ADR[6] symmetry gap and produce divergent boundary semantics across two functions in the same file.

**Followups bundling (proposed `block-5-synthesis-carveout-followups`)** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: three-witness C3 convergence (IE proposed → TA endorsed → DA accepted → CQA concurred) for a single WS-3 Tier-C micro-build bundling four items that share the parent ADR[6] symmetry boundary or are doc-correctness companions to it. (a) DA[#1] boundary-aware-matching applied symmetrically across `_path_is_archive` + `_is_synthesis_archive_write` (MEDIUM — closes ADR[6] escape-vs-spoof asymmetry); (b) DA[#2] OVERMATCH test class for the near-miss path coverage (LOW); (c) DA[CF-1] `:1056` `test_header_in_build_scratch_passes_block5` split into one synthesis-test plus one `-workspace.md` multi-path-test (LOW — coverage-shadow pattern: the test still passes post-carve-out but for a different reason than its documented intent, ASYMPTOMATIC, 3-eye + IE-peer-verify CONCUR on deferral); (d) optional F[CQA-8] scope-boundary doc-drift correction (LOW). Bundling rationale: items (a)+(b) are architectural-unit pairs, item (c) is the same coverage-shadow pattern, item (d) is optional doc-track companion. The proposed micro-build is the residual-handling vehicle for the §3b 3-scores (test-coverage and security), not an r2 trigger.

---

## workspace_write Helper (IC[6])

A stdlib-only helper for atomic gate-log appends. Signature exact-to-spec (deviation from spec triggers IE refusal-and-flag at boot validation per protocol).

**Defense pattern (PM[4] silent-corruption mitigation)**:
- Pre-check: anchor-presence verification at `workspace_write.py:95-99` — raises `WorkspaceAnchorNotFound` if anchor not present.
- Post-check: no-op-guard at lines 106-110 — second guard that detects no-replacement-occurred (atomic Python `str.replace` returning unchanged string).
- Combined effect: multi-byte-Unicode anchor edge cases (αβγ, emoji) cannot silently corrupt the file. [B-r19-remediation, 26.4.25]

**Production hardening**: 67 successful workspace_write helper writes through C3 with 0 WorkspaceAnchorNotFound exceptions. Helper signature exact-to-spec, section-isolation convention validated empirically. IC[6] is now considered hardened in production. [B-r19-remediation, 26.4.25]

**Section-isolation convention**: each agent writes only to its own anchor-bounded section in the gate-log. The helper enforces this at write-time (anchor must match caller-declared section). Cross-agent writes require explicit lead intervention.

---

## audit-calibration-gate.py (β+ Promotion Sidecar)

Append-only telemetry script that consumes CAL-EMIT records from `calibration-log.md` and produces PROMOTE / RECALIBRATE / HOLD decisions per gate-id.

**VALID_GATES allowlist** (post-R3 fix): `{A20, A22, A23, A24}`. Producer/consumer schema sync is single-source — argparse `choices` auto-syncs from `sorted(VALID_GATES)` (preventing the kind of drift that surfaced as the A24 bug in C3-r2). [B-r19-remediation, 26.4.25]

**Decision ordering**: exhaustive without overlap (CDS r1 verified). Threshold constants:
- ≥3 reviews fired
- ≤20% false-positive rate (DA-verdict driven)
- ≥5 DA-verdicted records

These match `directives.md` exactly. See [β+ Calibration Pattern](beta-plus-calibration-pattern.md) for full mechanics.

**Stall detection**: `audit-calibration-gate.py:160-165` — fires automatic warning when >30% of records are PENDING-not-reviewed, mitigating PM[CDS-2] (DA verdict pile-up).

**Known telemetry recovery**: the C3 round-3 VALID_GATES fix immediately surfaced 13 historical A24 PENDING records that had been silently malformed. Bonus production benefit beyond synthetic-fixture verification. [B-r19-remediation, 26.4.25]

---

## Multi-Layer Contract Drift (Recurring Failure Class)

Four instances confirmed in this build of the same architectural failure pattern:

| Instance | Producer | Consumer | Drift |
|---|---|---|---|
| BLOCK 3→4 | phase-gate.py code (BLOCK 4) | 27 doc files (BLOCK 3) | doc lies about machine state |
| CAL-EMIT pipe-escape (r1) | chain-evaluator.py:613 producer | audit-calibration-gate consumer regex | producer didn't sanitize pipe; consumer assumed clean |
| A24 VALID_GATES (r2) | chain-evaluator A24 emit | audit-calibration-gate VALID_GATES | producer emits A24; consumer allowlist excludes it |
| §-enumeration (r3) | directives.md:456+462 enumerate 3 §-tiers | A24 added 4th gate without doc update | directive lies about machine source-of-truth |

Pattern: **hardcoded enumeration in human-facing context that diverges from machine-enforced source-of-truth**. When shipping a new gate-id / block-number / schema-element, audit ALL human-facing enumerations (directives, agent files, skill phase docs) for stale lists. [B-r19-remediation, 26.4.25]

The single-source mitigation pattern (argparse `choices = sorted(VALID_GATES)`) is the structural fix; the manual enumeration sweep (TW R3-2 canonical-block-hash-identity invariant) is the operational fix.

[R-2026-04-28-shared-process-hardening, 26.5.2] **Confirmed: stale-line-ref recurring-cost is a fifth instance** of the contract drift pattern. DA[#8] in this build flagged that `phase-gate.py:467` BLOCK-message documentation referenced `sigma-lead.md:176`, but TW SQ[10] half-2 inserted ~31 lines at sigma-lead.md Step 1 ~38-72 (premise-audit pre-dispatch sub-step), so the correct line was `:207`. The fix moved the doc-text reference; behavioral surface unchanged. DA[#9] generalized this as the "stale-line-ref recurring-cost pattern" — promotion-candidate "stale-line-number lint rule" for next build's plan-track (e.g., sigma-audit grep `sigma-lead\.md:\d+` references against current line numbers). Same root pattern as BLOCK 3→4 doc drift: machine-source-of-truth advances ahead of human-facing reference.

[R-2026-04-28-shared-process-hardening, 26.5.2] **Sixth instance — directive↔hook integration drift**: see [Directive-Hook Integration Pattern](directive-hook-integration-pattern.md) for the meta-finding. Briefly: a directive (`directives.md §8f BUILD variant`) instructed lead to write a recovery header to BUILD scratch, but the hook (`phase-gate.py BLOCK 5`) only read from `DEFAULT_WORKSPACE`. Both shipped in the same build; their integration was never co-tested end-to-end. The recovery hatch the directive promised was mechanically unreachable. Closed via in-build R2 fix (multi-path scan + R2-micro short-circuit). This is the contract-drift pattern's most subtle form — the producer/consumer aren't divergent enumerations; they are divergent files-being-read.

---

## Open Questions

- **xargs framing minor concern** (DA[#4]): bypass enumeration in phase-gate.py docstring is unusual. SS dissented in favor of keeping it as inspectable contract; lead accepted SS. Reconsider if framing concern strengthens. [B-r19-remediation, 26.4.25]
- **A24 §-enumeration gap** (DA r3 spot-check): directives.md:456 + 462 enumerate `(§2i/§2j/§2d-severity)` for path-β+ gates; A24's §-tier still missing. 4th instance of doc-enumeration-drift, deferred to future build. [B-r19-remediation, 26.4.25]
- **A24 docstring attribution drift** (DA r2 cosmetic): chain-evaluator.py:959 attributes scope-narrowing to "SS recommendation" but A24 missing-check was DA[#1]. Lead-discretion fix. [B-r19-remediation, 26.4.25]
- **_XVERIFY_ANY_RE over-suppression** (CQA r3 bonus): regex at chain-evaluator.py:950-953 matches literal English word "XVERIFY" + whitespace including newline (false-suppression on prose like "XVERIFY was not run"). Severity LOW, separate-build candidate. [B-r19-remediation, 26.4.25]

[R-2026-04-28-shared-process-hardening, 26.5.2] Closed in this build: the bracket-required form `r"\bXVERIFY(?:-(?:FAIL|PARTIAL))?\["` at `chain-evaluator.py:1059-1062` drops colon/paren/whitespace alternatives. Prose mentions can no longer suppress.

- **GAP-D (HIGH, R12)** [R-2026-04-28-shared-process-hardening, 26.5.2]: `_strip_fenced_blocks` parity with chain-evaluator ADR[9] missing in phase-gate.py header scan; promote ADR[9] universal edge-case helpers from `chain-evaluator.py:340-360` to apply to phase-gate.py header scans, not just chain-evaluator gates. Memory-compile candidate: parallel-solution opportunity — same edge-case classes (BOM, fenced-code, empty-section) apply to both files.
- **GAP-E (low, R12)** [R-2026-04-28-shared-process-hardening, 26.5.2]: trailing-WS `$` anchor in `_COMPILATION_COMPLETE_RE`. Cosmetic regex tightening; does not change behavior under canonical authoring.
- **CONCERN-2 (LOW, R12)** [R-2026-04-28-shared-process-hardening, 26.5.2]: suffix-stripper extension for archive-name conventions (`-c{N}-scratch`, `-audit`, `-eval`, `-vet`). Current suffix-stripper covers common cases but not all sigma-track archive name shapes.
- **DA[#4] tool-name dispatch + Bash regex coverage** [R-2026-04-28-shared-process-hardening, 26.5.2]: `phase-gate.py:445` covers only Write/Edit for direct path detection. MultiEdit/NotebookEdit accept file_path/notebook_path; Bash regex misses redirects without `cat`, shell expansions, command substitution, nested `bash -c`, scripting-language indirection. Accept-with-documentation per plan §P2.A row 119 day-1 BLOCK mandate; logged as follow-up SQ.
- **DA[#5] `_path_is_archive` substring-match bypass** [R-2026-04-28-shared-process-hardening, 26.5.2]: symlinks, `..` traversal, case differences. KNOWN LIMITATIONS docstring added in-build at `phase-gate.py:429-457`; mechanical fix deferred. Closure path: `os.path.realpath` + case-folding canonicalization.
- **Synthesis-precedes-compilation sequencing trap** [R-2026-04-28-shared-process-hardening, 26.5.2]: surfaced 2026-05-01 at synthesis dispatch when phase-gate BLOCK 5 fired on the synthesis-archive write attempt for this build. Compilation cannot structurally precede synthesis (compilation reads synthesis as input per c3-review.md Step 14a). Resolution path is structural, not a one-line fix. Plan ## Build Review Summary records four ranked options for next build: (1) BLOCK 5 synthesis carve-out, (2) c3-review.md re-ordering, (3) directives.md §8f criterion extension with synthesis-precondition class, (4) make synthesis NOT an archive write (write to non-archive path first, archive at compilation completion). **CLOSED via Option 1** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: WS-2 micro-build shipped the BLOCK 5 synthesis carve-out per ADR[1]. See the BLOCK 5 carve-out section above for the predicate, short-circuit placement, AMENDMENT r3 doctrine, and escape-vs-spoof asymmetry surfaced during C3.
- **Escape-vs-spoof asymmetry in substring-matching predicates** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: substring-overmatch is a failure class independent of ADR[6] symlink/case-fold/`..` inheritance. Both `_path_is_archive` and `_is_synthesis_archive_write` use unanchored `_ARCHIVE_PATH_MARKERS` substring checks; an out-of-archive path containing the marker as substring (e.g., `/tmp/sigma-review/shared/archive/foo-synthesis.md`) returns True from both predicates. Bundled into proposed `block-5-synthesis-carveout-followups` micro-build for symmetric boundary-aware-matching hardening. Residual ACCEPTED for r1 close-out at TIER-1 P=0.91 with bounded single-user hook context.
- **directives.md §2h companion-list "security-adjacent named predicates" registry** [R-2026-05-05-block-5-synthesis-carveout, 2026-05-09]: surfaced from DA[#4] DEFEND. The right artifact for tracking which named predicates are security-adjacent is a directives.md §2h companion-list, not inline drift in every docstring. Promotion-candidate observation, not in-build fix. The IC[1] verbatim-spec preservation discipline + parent `_path_is_archive` precedent argue against inline expansion.

## Contradictions

None unresolved. All cross-agent tensions in C3 (TA "non-blocking" vs DA "3 blockers"; SS dissent on xargs framing; A24 ship vs defer) were resolved by lead ruling on evidence weight, with reasoning preserved in the synthesis archive.

## Sources

- B-r19-remediation synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md`
- R-2026-04-28-shared-process-hardening synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-synthesis.md`
