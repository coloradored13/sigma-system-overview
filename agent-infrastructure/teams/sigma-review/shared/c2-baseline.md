# c2-build Engineer Single-Pass Baseline (Phase 2 Gate measurement log)

Drives the Phase 2 Gate decision per `~/.claude/plans/glowing-hugging-wilkinson.md`.

## How to use

After every c2-build session, lead appends ONE line below in this format:

```
BUILD[{date}-{slug}]: tier={1|2|3} |SQs:{count} |single-pass-clean:{count} |c3-fixups:{count} |fix-causes:{cause1,cause2,...}
```

**Field definitions:**
- `tier` — 1, 2, or 3 from c1-plan complexity assessment
- `SQs` — total SQ[] items in the plan
- `single-pass-clean` — count of SQ[] items that exited c2 without needing c3 fixup work
- `c3-fixups` — count of SQ[] items that required fixes during c3-review
- `fix-causes` — comma-separated tags from {`test-gap`, `impl-bug`, `spec-ambiguity`, `flaky-test`, `external-dep`, `other`}. Empty when c3-fixups=0.

## Trigger conditions for Phase 2 build (any one)

1. Single-pass-clean rate < 70% over 5+ recent c2-build runs
2. ≥30% of c3-fixup cycles trace to `test-gap`
3. ≥2 incidents where engineer emitted "tests passing" while ICs were not actually satisfied — OR — 1 incident plus explicit qualitative judgment that the same pattern is recurring

## Mechanical analysis

```
python3 ~/Projects/sigma-ralph/scripts/analyze_c2_baseline.py
```

Prints rates, fix-cause distribution, and `GATE: TRIPPED|NOT TRIPPED` for triggers 1 and 2. Trigger 3 (incidents) requires qualitative judgment and is not auto-detected.

## Gate decision artifact

After two-week measurement window, write `phase-2-gate-decision.md` in this same directory with date, raw stats, decision (BUILD PHASE 2 | DEFER | SKIP-PERMANENT), reasoning (≤200 words), and next review date if DEFER.

## Builds (append below this line)

<!-- one BUILD[...] line per c2-build session -->
