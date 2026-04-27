# Sigma-Build Infrastructure Architecture
Last updated: 26.4.25 | Reviews: B-r19-remediation

## Summary

Sigma-build is enforced by two mechanical-gate scripts plus a calibration sidecar: `chain-evaluator.py` (atomic A-checks A1–A24, fired by the Stop hook), `phase-gate.py` (transition-time BLOCKs 1–4), and `audit-calibration-gate.py` (β+ promotion telemetry). The R19 remediation build added four new analytical-tier checks (A20/A22/A23/A24), a fourth phase-gate BLOCK (sed-i ban with shlex tokenization), the `workspace_write` helper for safe gate-log appends, and the calibration-log promotion mechanism. Several "multi-layer contract drift" defects surfaced in C3 — producer/consumer schema decoupling between chain-evaluator and audit-calibration-gate is the dominant failure class. [B-r19-remediation, 26.4.25]

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

---

## Phase-Gate BLOCK 4 (sed-i Ban)

Phase-gate.py enforces transition-time hard blocks. R19 added BLOCK 4 (renumbered from a previous BLOCK 3 that was already in the codebase — this drift caused 27 stale "BLOCK 3" doc references swept by TW in C3-r2 OPTION 2 phrasing).

**Mechanism**: scope-pattern-match (path) + `shlex.split(posix=True)` tokenization. The shlex tokenizer collapses `-i""` / `-i ''` / joined `-i''` into a bare `-i` flag, neutralizing zero-space evasion variants. Empirically traced 7 evasion forms and passed all 7: BSD `-i ''`, joined `-i''`, env-wrapper, xargs-positional, absolute `/usr/local/bin/sed`, backup `-i.bak`, xargs-stdin. [B-r19-remediation, 26.4.25]

**Known limitation (xargs stdin)**: the bypass enumeration is preserved in `phase-gate.py:300` as inspectable contract. SS dissented from DA[#4]'s framing concern that listing bypasses in the docstring "advertises" them — SS's position (lead-accepted): listing specific bypass forms in the enforcement file IS the contract; concealing them would be worse security hygiene. Threat model is accidental silent corruption, not sophisticated-adversary evasion. [B-r19-remediation, 26.4.25]

The OPTION 2 phrasing introduced post-hoc — "phase-gate enforces the sed-i BLOCK mechanically" (drops numeric identifier) — is block-number-agnostic and future-renumber-immune. CAL[R3-2-canonical-block-hash-identity] subsumes the weaker CAL[R2-OPTION2-phrasing] after R3-2 resync. [B-r19-remediation, 26.4.25]

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

---

## Open Questions

- **xargs framing minor concern** (DA[#4]): bypass enumeration in phase-gate.py docstring is unusual. SS dissented in favor of keeping it as inspectable contract; lead accepted SS. Reconsider if framing concern strengthens. [B-r19-remediation, 26.4.25]
- **A24 §-enumeration gap** (DA r3 spot-check): directives.md:456 + 462 enumerate `(§2i/§2j/§2d-severity)` for path-β+ gates; A24's §-tier still missing. 4th instance of doc-enumeration-drift, deferred to future build. [B-r19-remediation, 26.4.25]
- **A24 docstring attribution drift** (DA r2 cosmetic): chain-evaluator.py:959 attributes scope-narrowing to "SS recommendation" but A24 missing-check was DA[#1]. Lead-discretion fix. [B-r19-remediation, 26.4.25]
- **_XVERIFY_ANY_RE over-suppression** (CQA r3 bonus): regex at chain-evaluator.py:950-953 matches literal English word "XVERIFY" + whitespace including newline (false-suppression on prose like "XVERIFY was not run"). Severity LOW, separate-build candidate. [B-r19-remediation, 26.4.25]

## Contradictions

None unresolved. All cross-agent tensions in C3 (TA "non-blocking" vs DA "3 blockers"; SS dissent on xargs framing; A24 ship vs defer) were resolved by lead ruling on evidence weight, with reasoning preserved in the synthesis archive.

## Sources

- B-r19-remediation synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md`
