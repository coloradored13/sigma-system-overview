---
name: verify-loss-before-cutting
description: Before cutting a module, lesson, or feature as redundant, enumerate what it uniquely exercises against the things claimed to cover it; move any uncovered piece first, then cut
metadata:
  type: feedback
---
Do not cut content or features on a redundancy claim alone. List every behavior/probe the candidate exercises, map each to the specific place that covers it at equal or greater depth, and move anything uncovered into an existing home before deleting.

**Why:** User instruction 2026-09-05 on Module 1.1: "I don't want to preserve the whole module just because it exists, but I also don't want the persona recalibration to accidentally remove a useful Product-craft refresher." The check found one uncovered behavior (V1-vs-later boundary drawing) out of five probes; it moved to P.2 (+0.5 h), then 1.1 was cut (−3 h).

**How to apply:** Also check for dependents (`prerequisites`, imports, references) before removal. Report the mapping table, not just the verdict. Related: [[schema-drift-check]].
