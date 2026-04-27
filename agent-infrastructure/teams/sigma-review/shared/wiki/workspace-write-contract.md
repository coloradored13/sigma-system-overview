# workspace_write Contract (IC[6])
Last updated: 26.4.25 | Reviews: B-r19-remediation

## Summary

`workspace_write` is the canonical helper for atomic gate-log appends in sigma-build/sigma-review workspaces. It enforces a section-isolation convention (each agent writes only to its own anchor-bounded section) and defends against silent corruption via a double-guard: anchor-presence pre-check plus no-replacement-occurred post-check. Production-hardened across C3 of the R19-remediation build with 67 successful writes and zero `WorkspaceAnchorNotFound` exceptions. [B-r19-remediation, 26.4.25]

---

## Signature

`workspace_write(workspace_path, agent_anchor, payload)` — exact-to-spec per IC[6]. Deviation from this signature triggers IE refusal-and-flag at boot validation under sigma-build agent protocol; the spec is the contract, and silent signature drift would defeat section-isolation guarantees. [B-r19-remediation, 26.4.25]

The helper is stdlib-only (no runtime dependencies). This was an intentional design constraint — gate-log appends must work in any agent context, including minimal-environment agents.

---

## Defense Pattern: Anchor-Presence + No-Op Double-Guard

Two independent guards mitigate PM[4] (atomic Python `str.replace` edge-case failure with multi-byte-Unicode anchors leading to silent corruption):

### Guard 1: Anchor-Presence Pre-Check (workspace_write.py:95-99)
Before performing the replace, the helper verifies the anchor string is present in the file content. If the anchor is missing, raises `WorkspaceAnchorNotFound` — never silently writes to wrong location. [B-r19-remediation, 26.4.25]

### Guard 2: No-Op Post-Check (workspace_write.py:106-110)
After the replace, the helper verifies the resulting string is different from the original. If `str.replace` returned the unchanged string (e.g., due to a Unicode-normalization edge case where the anchor appeared visually present but didn't match byte-for-byte), the no-op guard fires `WorkspaceAnchorNotFound`. [B-r19-remediation, 26.4.25]

The double-guard is necessary because Python's `str.replace` is silent on no-match. Either guard alone would miss a class of failures: pre-check misses Unicode normalization mismatches; post-check alone would not distinguish "anchor missing entirely" from "anchor present but write produced no diff."

**Smoke-tested** in C2 by IE-1 with αβγ + emoji anchors. Both guards engaged correctly on simulated drift scenarios. [B-r19-remediation, 26.4.25]

---

## Section-Isolation Convention

Each agent writes only to its own anchor-bounded section in the gate-log. The helper enforces this at write-time — the `agent_anchor` parameter must match a section header the caller is authorized to modify. Cross-agent writes require explicit lead intervention.

This convention is what makes the gate-log auditable: a section's contents are attributable to a single author (the agent owning the anchor), so DA can assess analytical provenance without needing to track cross-writes. [B-r19-remediation, 26.4.25]

---

## Production Hardening

C3 use of the helper across all rounds:
- 67 successful writes through C3 (cumulative).
- 0 `WorkspaceAnchorNotFound` exceptions.
- IC[6] dogfooded by TW for the R3-2 canonical-block resync (29 agents resynced from `_template.md:140-152` to byte-identical hash via the helper). [B-r19-remediation, 26.4.25]

Hardening surfaced two sub-patterns worth noting:

### "Atomic Python replace" pattern
The replace is atomic in the sense that either it succeeds (file content modified) or it raises (no partial write). There is no intermediate state where the file has been opened for write but not finalized — the helper reads, replaces in memory, and writes the full new content in a single `Path.write_text` call.

### Recursive-self-reference anti-pattern (TW R3-2 lesson)
TW used pre-R2 technical-writer.md propagated block as reference instead of authoritative `_template.md`. Result: 29 propagated agents carried legacy block vintage. Corrected via R3-2 hash-identity invariant. The general lesson: **propagate from source-of-truth, not from prior instance**, even when prior instances are syntactically identical at the time of reading. [B-r19-remediation, 26.4.25]

---

## Open Questions

- **Template-vs-instance drift** (TW R3-2 design discussion): two complementary approaches surfaced — sync script (explicit re-sync from canonical `_template.md`) and chain-evaluator A25 hash-identity-based content-drift detection. User ruling: duplication preserves rule-following safety (sync script over generator); mechanical detection prevents drift. Both are deferred to future builds. [B-r19-remediation, 26.4.25]

## Contradictions

None.

## Sources

- B-r19-remediation synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-23-r19-remediation-synthesis.md`
