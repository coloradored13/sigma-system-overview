---
name: Synthesis is not the deliverable
description: The completed recipe chain is the deliverable, not the synthesis document — skipping post-synthesis steps produces an incomplete product
type: feedback
originSessionId: b1a4c43c-fc70-4786-8cd3-bc9d765a4d08
---
The completed chain IS the deliverable. The synthesis document is one ingredient, not the dish.

**Why:** Lead skipped promotion/compilation/sync/git after synthesis, treating post-synthesis steps as "cleanup" rather than "the product." Sent agent shutdown before chain closure. User correction: "the completed recipe is the deliverable, not the synthesis. The synthesis is like spaghetti with no sauce — part of what I asked for, but not the whole thing, and not including the sauce means it's wrong."

**How to apply:** After synthesis is written, you are NOT done. You are at step 7a of 7a-7f. Do not present results to user, do not send shutdown, do not mentally shift to "wrap-up mode" until promotion (7c), compilation (7b), sync (7d), archive (7e), and git (7f) are complete. The chain evaluator's A13 (promotion evidence) check exists for exactly this reason.

This is deeper than process-over-momentum (26.4.8) — it's not just skipping a validation step under pressure, it's misidentifying what "done" means. The visible document creates a false sense of completion that makes the invisible steps feel optional. They are not optional. They are the product.

**Mechanical fix needed:** Pre-shutdown hook that BLOCKs on empty ## promotion section. Convert this from a directive (skippable under momentum) to a gate (unskippable).
