# Directive-Hook Integration Pattern
Last updated: 26.5.2 | Reviews: R-2026-04-28-shared-process-hardening

## Summary

Directives that specify recovery paths must be co-tested with the hooks that enforce the gates they recover from. Shipping a directive and a hook that share a contract — without an integration test that exercises the directive's recovery action against the hook's gate logic end-to-end — produces a class of defect where the recovery hatch is mechanically unreachable. The shared-process-hardening build surfaced this pattern via two close-out events on the same gate (BLOCK 5 06b pre-archive compilation gate). Both were caught by the gate halting rather than silent-bypassing — the honor-system enforcement model worked as designed; the failure was in test-design coverage, not in gate behavior. [R-2026-04-28-shared-process-hardening, 26.5.2]

---

## The Pattern

A directive (in `directives.md` or an agent-defs file) names a recovery action: "if X fails, do Y to unblock." A hook (in `chain-evaluator.py` or `phase-gate.py`) enforces a gate: "block when condition Z is not satisfied." The directive promises that doing Y will satisfy Z. The integration claim is implicit: "Y produces a state the hook reads as Z-satisfied."

When the directive and the hook are co-authored in the same build but the integration claim is not co-tested, three failure modes can ship invisibly:

1. **Recovery action writes to the wrong file/path** — the directive instructs writing to file F1, but the hook only reads from F2. The state never reaches the hook.
2. **Recovery action uses non-canonical schema** — the directive describes the recovery format prosaically, but the hook regex expects an exact bracketed form. Free-prose recovery does not match.
3. **Recovery action triggers the gate's own logic again** — the directive instructs an action that itself causes a re-fire of the gate (e.g., "write the recovery header to the archive" when the gate guards archive writes). The recovery is structurally impossible.

[R-2026-04-28-shared-process-hardening, 26.5.2]

---

## The Two Close-Out Events (case study)

**Event 1 — Synthesis-precedes-compilation sequencing trap** (2026-05-01). At synthesis dispatch, phase-gate BLOCK 5 (the 06b pre-archive compilation gate this very build shipped) correctly fired on the synthesis-agent's archive-write attempt because the workspace did not contain the required `## compilation-complete: [R-{id}]` header. The trap is structural — `c3-review.md Step 14a` defines compilation as reading synthesis as input, so compilation cannot structurally precede synthesis, but BLOCK 5 expects compilation-complete in workspace before any archive op. This is failure mode 3 from the list above: the directive's recovery action (run compilation before archive write) cannot occur because compilation requires the synthesis archive as input. Resolved via lead-with-user-approval manual-override under exception clause; logged as follow-up SQ for next build with four ranked resolution options (BLOCK 5 synthesis carve-out / c3-review.md re-ordering / directives.md §8f criterion synthesis-precondition clause / make synthesis NOT an archive write).

**Event 2 — BLOCK-5-WORKSPACE-PATH defect** (2026-05-02). Even after the lead wrote the override header to `c3-scratch.md`, BLOCK 5 continued firing on retry. Code-read of `phase-gate.py` revealed `DEFAULT_WORKSPACE` was hardcoded at `phase-gate.py:43` to `~/.claude/teams/sigma-review/shared/workspace.md` (an ANALYZE-track convention), and both `_has_compilation_complete()` and `_is_sigma_session()` read ONLY from that path. The directive this build ratified (`directives.md §8f BUILD variant`) instructs lead to write the override header to BUILD scratch (`builds/{id}/c{N}-scratch.md`), but the hook never reads BUILD scratches. The recovery hatch was mechanically unreachable for any BUILD-track session. This is failure mode 1 from the list above.

Compounding: `workspace.md` held an unrelated 2026-04-23 ai-agent-rollout-playbook-vet ANALYZE workspace, so `_is_sigma_session()` was misclassifying THIS session as in-sigma based on stale file content. The FP guard was returning the right verdict for the wrong reason.

**Closed via in-build R2 fix**: IE landed multi-path scan (BUILDS_DIR + 7-day window + multi-source `_is_sigma_session` + multi-path `_has_compilation_complete` with archive_path-derived preferred-build); TA flagged CONCERN-1 cross-build authorization bypass via broad-glob fallback; IE landed R2-micro short-circuit (5-line: when preferred-build derivable + dir-exists + no override → return False before broad-glob fires); TA re-verified PASS with three empirical scenarios (cross-build r19 BLOCK, in-build PASS, cross-build sigma-v2 BLOCK); CQA regression clean; 8 new tests; full hook-suite 1253 passed / 14 skipped / 1 failed (matches C2 baseline + 8 new tests). [R-2026-04-28-shared-process-hardening, 26.5.2]

---

## Why the Honor-System Enforcement Worked

Both events shipped through C2 because the C2 test design did not cover directive↔hook integration end-to-end. The C2 unit tests for BLOCK 5 covered "blocks Write archive without header / passes with header / passes with manual-override" — but did NOT exercise "synthesis-write before compilation header" (event 1) or "header written to BUILD scratch instead of workspace.md" (event 2). Neither failure mode was within the test fixture's parameter space.

What surfaced both events at C3 close was the gate halting non-silently combined with agent honesty:

- The gate fired when it was supposed to (event 1: archive write without compilation-complete; event 2: same, after override written to wrong file).
- The agent halted instead of routing around (writing to a non-archive path, forging a header in workspace.md, asking for a "creative" workaround).
- The lead refused to silently elevate to manual-override without user-supplied justification AND, when the override didn't work on event 2, escalated rather than concluding "the gate is broken, ship anyway."
- The build ran the in-build R2 fix through the same multi-agent process (IE + TA peer-verify + CQA regression) rather than letting the lead patch and ship.

The honor-system limitation acknowledged in `directives.md §8f §"enforcement-model: HONOR-SYSTEM"` is what made these events recoverable. If the gate had been silently bypassable, neither event would have surfaced; the synthesis would have been written, the directive↔hook integration defect would have shipped invisibly, and the next BUILD-track session would have hit the same wall. [R-2026-04-28-shared-process-hardening, 26.5.2]

---

## Recommended Pattern for Future Co-Authored Directive+Hook Pairs

When a build introduces a new gate AND a new directive that references the gate's recovery path, co-test the integration end-to-end:

1. **Trace the recovery contract.** Name the file/path the recovery action writes to (per the directive). Name the file/path the hook reads from (per the code). Confirm they match.
2. **Trace the recovery schema.** Name the schema the recovery action produces (per the directive). Name the regex/parser the hook expects (per the code). Confirm they match character-for-character — the bracket-required form, anchor-required form, etc.
3. **Trace the recovery sequencing.** Identify whether the recovery action is itself within the gate's enforcement scope (e.g., "write header to archive" when the gate guards archive writes). If yes, the recovery is structurally impossible without a carve-out.
4. **Add an integration test.** Beyond the unit tests for "gate blocks when condition unmet" and "gate passes when condition met," add a test for "directive recovery action produces a state the gate accepts." This test must invoke the actual hook (not a stub) on a workspace shaped by the actual directive recovery (not a fixture).
5. **Sanity-check the FP guard.** The hook's FP guard (e.g., `_is_sigma_session()`) reads some file or set of files to classify the session. Confirm that file's content cannot stale-classify a non-sigma session as in-sigma (event 2 was compounded by stale workspace.md content).

This is one of the higher-leverage test-design extensions a build can ship: not "does the gate work?" but "does the gate's documented recovery actually work?" The cost is small (one or two integration tests per directive↔hook pair); the failure mode is severe (a recovery hatch that doesn't exist). [R-2026-04-28-shared-process-hardening, 26.5.2]

---

## Relationship to Producer/Consumer Contract Drift

This pattern is adjacent to the producer/consumer contract drift class documented in [β+ Calibration Pattern](beta-plus-calibration-pattern.md) and [Sigma-Build Infrastructure Architecture](sigma-build-infrastructure-architecture.md). Producer/consumer drift is about divergent enumerations or escape rules between two co-evolving artifacts. Directive↔hook integration drift is about divergent **files-being-read-or-written** between a directive (which names where to write) and a hook (which names where to read).

Both classes share the same underlying root cause: human-facing context (directives, doc) and machine-enforced source-of-truth (hook code) advance independently when not co-tested. The mitigation patterns are correspondingly similar — single-source-of-truth where mechanically possible (e.g., derive directive language from a constant the hook also imports), and operational mitigation (canonical-source guarding, integration-test coverage) where it is not. [R-2026-04-28-shared-process-hardening, 26.5.2]

---

## Open Questions

- **Where does the integration test live?** Unit tests sit beside the hook (in `tests/`); directive specs sit in `directives.md`. The integration test bridging them is structurally orphaned. Candidate placement: a build-track integration-test suite that exercises both halves of each shipped directive↔hook pair. Logged for next build's plan-track. [R-2026-04-28-shared-process-hardening, 26.5.2]
- **Pre-mortem template extension.** PM[NEW-1] and PM[NEW-2] in this build were not anticipated in the C1 pre-mortem. The PM template should add a category for directive↔hook integration risk specifically, prompting the C1 lead to enumerate the recovery contracts and confirm co-testing. Memory-compile candidate. [R-2026-04-28-shared-process-hardening, 26.5.2]

## Contradictions

None.

## Sources

- R-2026-04-28-shared-process-hardening synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-28-shared-process-hardening-synthesis.md`
