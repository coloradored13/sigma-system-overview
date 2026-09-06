---
name: pivot direction logic for differential-drive robots
description: When deducing motor wiring from in-place rotation tests, the active wheel arcs around the stationary one in the OPPOSITE direction from intuition. Verify with this rule before applying any L/R swap.
type: feedback
originSessionId: 21cb4264-b84a-4685-861b-134f9c990b70
---
When deducing motor wiring or label inversions from single-wheel rotation tests on a differential-drive robot, the active wheel traces an arc around the stationary one in the OPPOSITE direction from the bot's heading change.

Concretely, with the bot facing 12 o'clock:
- LEFT wheel forward + RIGHT wheel stopped → bot pivots around RIGHT wheel → bot's heading rotates **CW** (right turn from above) — left wheel arcs CW around right wheel
- RIGHT wheel forward + LEFT wheel stopped → bot pivots around LEFT wheel → bot's heading rotates **CCW** (left turn from above)

And for two-wheel-forward differential drive:
- LEFT faster than RIGHT (both forward) → bot turns RIGHT (slower side = inside of turn)
- RIGHT faster than LEFT (both forward) → bot turns LEFT

**Why:** During the cutebot session 2 (26.5.3), I initially mis-derived the pivot direction (assumed LEFT-only forward = CCW), which led me to claim a motor-label swap was needed. Built a wrong drive-primitive swap on top of the wrong sensor-label swap, then over-compensated calibration in the wrong direction. User caught it when L=50/R=75 produced a RIGHT veer (opposite of expected). Re-derived the pivot logic from scratch and reverted the drive swap.

**How to apply:** Before claiming any L/R label inversion in motor wiring, run two single-wheel tests and a single both-wheel test, and check that all three are internally consistent against this rule:
- L=0,R=50 should produce CCW (left turn from above) under correct wiring.
- L=50,R=0 should produce CW (right turn from above).
- L=R=50 should go straight if motors are balanced; lean direction = identifies the slower wheel (slower wheel = inside of the turn).

If user's verbal direction (CCW vs CW, "veered left" vs "veered right") contradicts your prediction, suspect the rule is being applied wrong before suspecting the hardware. Sketch the geometry on paper if needed — the wheel arc and heading change rotate in the SAME direction (both CCW or both CW), so if the bot heading rotates CCW the wheel that's moving must also be tracing a CCW arc around the stationary wheel.

This is a cheap rule to verify; expensive when wrong (compounding miscompensations across motors and sensors as you try to "fix" a bug that isn't there).
