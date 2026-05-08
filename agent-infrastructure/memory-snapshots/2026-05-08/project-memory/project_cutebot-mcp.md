---
name: cutebot-mcp project
description: MCP server letting Claude drive an ELECFREAKS Cutebot via three micro:bits + radio, using hateoas-agent for state-gated tool discovery. v0.2 code complete 26.5.7 — full sensorium expansion (22 actions: actuators + ultrasonic/line/compass/accel/motion/light/temp/sound/buttons/RSSI/scan_distance/pose). Pending hardware re-flash + verification.
type: project
originSessionId: 7a07e4bf-655f-4bdb-a008-80b66145a99f
---
# cutebot-mcp

**Repo:** `~/Projects/cutebot-mcp/` (local-only git, no remote — flag before pushing)
**Created:** 2026-05-02
**Last session:** 2026-05-07 — v0.2 code complete: full sensorium (22 actions), beacon firmware added for hide-and-seek, host-side L/R workaround removed, working tree dirty pending review/commit/re-flash

## Architecture

Claude Code (MCP client) → MCP stdio → Python server (hateoas-agent StateMachine) → pyserial @ 115200 → **bridge** micro:bit V2 (USB, displays "B", group 42) → 2.4 GHz radio → **robot** micro:bit V2 on Cutebot (battery-powered, displays 😊, group 42 default + retunes for R/T) ⤳ optional **beacon** micro:bit (handheld, group 99) for hide-and-seek games.

500ms watchdog on the robot side: motors stop if no command for 500ms, independent of any MCP timeout. Watchdog refresh added in v0.2 after every `handle()` return so long blocking commands don't trigger spurious motor stops.

## Status as of v0.2 code complete (2026-05-07)

**Action surface: 22 MCP actions (was 8 in v0.1).**

Actuators: connect_robot (gateway), drive, stop, move, set_headlight, set_servo, beep, follow_line, send_radio, ping (10).

Senses: read_ultrasonic, scan_distance (firmware-side polar sweep ≤6 angles), read_line_sensors, read_compass, calibrate_compass, read_accel, read_motion, read_pose (composite), read_light, read_temperature, read_sound (V2-only with graceful "unavailable" on V1), read_buttons, sample_rssi (12).

**Code-complete checklist:**
- ✅ All 22 primitives implemented in `primitives.py` (host-side pitch/roll computation via math.atan2)
- ✅ All 22 actions registered in `server.py` with full descriptions; matching `@sm.on_action` handlers
- ✅ Robot firmware: 14 new wire-command branches (R/T/V/F/C/CAL/A/G/W/E/O/K/N/Z), pin13↔pin14 swap in read_line(), set_servo helper, watchdog refresh after handle()
- ✅ Beacon firmware: new file `firmware/beacon_microbit.py`, MicroPython port of user's TS STALKER handheld (group 99, 5Hz HB heartbeat, skull animation on FOUND, button A reset)
- ✅ docs/protocol.md: 14 wire commands + 11 response shapes + reserved-groups section + V1/V2 caveats
- ✅ README.md: actuator + sense action tables, three-µbit topology
- ✅ Python parses cleanly, state machine builds, 22 primitives ↔ 22 actions verified

**Live-verified 2026-05-08 (15 of 22 actions end-to-end):**
- ✅ ping, read_ultrasonic, read_line_sensors, read_compass (uncalibrated guard), read_accel, read_motion, read_light, read_temperature, read_sound (V2), read_buttons, read_pose
- ✅ set_headlight (red→green→blue→off cycle visible), beep (audible)
- ✅ drive (in-place ~30° right pivot visible)
- ✅ scan_distance([-30,0,30]) returned `-30°: 61cm | 0°: 60cm | +30°: 56cm` — firmware-side polar sweep working

**Live-discovered bugs and fixes (committed as 6dcf795):**
- handle() with all 22 branches exceeded MicroPython's per-function bytecode budget on the live µbit, crashing at boot with '504' memory error. Refactored into 7 sub-dispatchers (_h_motion, _h_sensor, _h_imu, _h_actuator, _h_radio, _h_follow, _h_scan).
- compass.heading() auto-triggers an interactive gesture-game calibration on uncalibrated bots, hanging the main loop while the µbit is mounted on the Cutebot. Guarded the C and Z handlers with is_calibrated().
- accelerometer.get_strength() not available on this µbit's MicroPython build. Replaced with manual sqrt(x²+y²+z²) over raw axes in the G handler.

**New firmware variant (unplanned, added during recovery):**
- `firmware/direct_robot_microbit.py` — combined bridge+robot in one µbit (UART command channel + radio for RSSI/transmit). Display: 😎 FABULOUS. Created when the original bridge µbit was lost mid-session; not the current production setup but useful for single-µbit dev workflows.

**Still pending (needs hardware/setup):**
- ⏳ follow_line — needs V1.3 track
- ⏳ set_servo — needs physical servo connected to S1 or S2
- ⏳ calibrate_compass — user must tilt µbit through LED gesture game
- ⏳ sample_rssi + send_radio full loop — primitives validated by command-ack but full hide-and-seek needs a third µbit running `beacon_microbit.py`

**Current 2-µbit topology (down from 3 — beacon µbit was sacrificed to replace lost original bridge):**
- µbit on laptop USB: `bridge_microbit.py` (displays "B")
- µbit on Cutebot: `robot_microbit.py` v0.2.1 (displays 😊)
- No beacon µbit. Hide-and-seek game needs a third µbit to restore.

**Commits as of 2026-05-08:**
- 61f8ee1 v0.1 baseline
- b21a242 v0.1.1 bridge UART + line sensor 4-state
- 3f5bc45 v0.2 sensorium (22 actions)
- 6dcf795 v0.2.1 firmware fixes (handle split + compass guard + motion fix)

Working tree clean.

**v0.1 known issues now addressed:**
- ❗ Bridge UART partial-line bug — fixed 26.5.3, already in main
- ❗ Line sensor pin13/pin14 inversion — firmware now correctly labels pin14=left, pin13=right; host-side parse swap workaround REMOVED
- ⚠ Open-loop motor calibration drift — sidestepped via firmware-side `follow_line` bang-bang controller

**v0.1 known issues still live (carryover):**
- 🔧 Motor friction asymmetry (right wheel ~30-50% higher rolling resistance) — closed-loop follow_line compensates; open-loop drives still drift CCW
- 🔧 IR false positives on wood floor — documented limitation, not a fix; user keeps bot on V1.3 track

Verified live (v0.1 only — v0.2 verification still pending hardware): ping, I2C headlights, ultrasonic, line sensors, beep, drive, motor isolation tests.

## Key design decisions

**hateoas-agent `mode="discover"` for v0.1.** No `from_states` constraints — every primitive callable from any state. Why: we don't yet know the right state graph, want to observe Claude's actual usage patterns first. How to apply: v0.2 will run `StateMachine.report().to_python()` against accumulated transitions to lock down strict guards.

**Single state "connected" after `connect_robot` gateway.** Gateway opens serial + sends `P` → expects `PONG` → returns `_state: "connected"`. Why: keeps the v0.1 model dead-simple; transitions exist only as gateway→connected.

**Radio: channel=7, group=42, length=64.** Why: 7 is the µbit default (overlaps Wi-Fi ch1 at 2407 MHz, but fine for single-home use; honest reasoning: simplicity, not Wi-Fi avoidance); group 42 arbitrary; length bumped from default 32 for headroom on `H,B,255,128,0`-shape packets. How to apply: change channel on **both** firmware files if interference appears.

**`!` prefix reserved for bridge admin.** Bridge intercepts `!PING`→`!PONG` locally without radio forward. Why: needed to verify bridge connectivity in step 3 when the robot wasn't flashed yet; otherwise no way to test bridge in isolation. Robot protocol uses letter prefixes (D/S/U/L/H/B/P), no collision.

**Beep capped at 200ms** server-side and robot-side. Why: `music.pitch()` blocks the µbit main loop; longer beeps would let the 500ms watchdog window expire and motors couldn't be stopped during a beep.

**No underglow primitive.** Cutebot has two front RGB headlights via I2C (commandable) PLUS two underbody LEDs that are auto-driven by the line sensor circuitry on the Cutebot board itself (NOT commandable from firmware). Both LEDs blue when both line sensors detect the line. Confirmed by user 26.5.3 — visual feedback for free, no I2C cycle needed. Krakenus library agrees: no underglow API. How to apply: use as a real-time visual indicator for line tracking; don't try to control them via I2C, they're not on the bus.

**`Bridge.request()` retries once on timeout** by default. Why: 2.4 GHz drops occasional packets — observed one during build session step 4. Single retry tolerates that without making the API harder to use. Double-drop still raises `TimeoutError`. How to apply: `retries=0` for fast-fail diagnostics like `--selftest`.

**Pinout sourced from github.com/Krakenus/microbit-cutebot-micropython (MIT).** Why: ELECFREAKS docs returned 403 to WebFetch; Krakenus's full source was readable via curl. Verified pin map directly from the file. How to apply: re-fetch from `/tmp/cutebot-ref/cutebot.py` during build session if extending; library doesn't cover IR receiver or buzzer.

## Pin / I2C map (Cutebot v2)

- **I2C address 16** — motors / RGB headlights / servos. 4-byte buffers:
  - motors: `[motor_pos, dir, abs(speed), 0]` (motor_pos: 1=left, 2=right; dir: 1=back, 2=forward)
  - RGB: `[led_pos, R, G, B]` (led_pos: 4=left, 8=right)
  - servos: `[servo, angle, 0, 0]` (servo: 5=S1, 6=S2; not exposed in v0.1)
- **GPIO pin8** ultrasonic trigger; **pin12** echo (`time_pulse_us(pin12, 1, 30000)`)
- **GPIO pin13** left line sensor; **pin14** right (both **active low** — black returns 0, our firmware inverts so "1=on-track")
- **micro:bit V2 built-in MEMS speaker** for beep via `music.pitch(freq, ms)`

## File layout

- `src/cutebot_mcp/server.py` — `build_state_machine()` + `main()`; module-level `_bridge` singleton with lazy open; 22 actions registered
- `src/cutebot_mcp/bridge.py` — `Bridge` class + `selftest()` + `ping_robot()` + CLI (`--selftest`, `--ping-robot`)
- `src/cutebot_mcp/primitives.py` — 22 human-readable wrappers; pitch/roll computed host-side via `math.atan2`
- `firmware/bridge_microbit.py` — `uart.init(115200)` ↔ `radio` relay; `!` namespace; UNCHANGED in v0.2
- `firmware/robot_microbit.py` — inlines Cutebot I2C ops; v0.2 expanded: 14 new wire-command branches, V2-only senses guarded with `_HAS_MIC`/`_HAS_LOGO` flags; `display.show(HAPPY)` runs before any I2C so a battery-off boot still gets visual confirmation
- `firmware/beacon_microbit.py` — NEW in v0.2; handheld broadcaster for hide-and-seek games (group 99)
- `docs/protocol.md` — full wire protocol; 14 commands + 11 response shapes + reserved-groups
- `pyproject.toml` — hatchling, hateoas-agent + mcp + pyserial deps; `cutebot-mcp` script entry

## Hardware setup

- 2× BBC micro:bit V2. Bridge stays plugged into laptop USB at `/dev/tty.usbmodem1102`. Robot is on the Cutebot, battery-powered.
- Both flashed with `uflash <firmware> /Volumes/MICROBIT` (uflash 2.0.0 in venv — V2-compatible, single-hex deploy).
- Bridge LED matrix: "B". Robot LED matrix: 😊 (`Image.HAPPY`).

## ~/.claude.json wire-in

Backup at `~/.claude.json.bak.cutebot-step6`. Top-level `mcpServers.cutebot`:
```
"command": "/Users/bjgilbert/Projects/cutebot-mcp/.venv/bin/python"
"args": ["-m", "cutebot_mcp.server"]
"env": {}
```

## Carryover for next session

v0.2 code shipped 26.5.7 (active plan: `~/.claude/plans/i-tried-to-create-serialized-teacup.md`; original sigma-single plan at `~/.claude/plans/peaceful-growing-candy.md` retained as historical record). Scope expanded mid-session from RSSI-hunt-only to full sensorium per user redirect.

**Top of next session:**
- **Re-flash µbits** (cannot test anything without this):
  - `cd ~/Projects/cutebot-mcp && uflash firmware/robot_microbit.py /Volumes/MICROBIT` (robot µbit)
  - Then unplug + plug a third µbit + `uflash firmware/beacon_microbit.py /Volumes/MICROBIT` (beacon)
- **Run verification ladder** (13 steps in plan; gates each next step on prior pass):
  1. `python -m cutebot_mcp.bridge --selftest` + `--ping-robot`
  2. Bridge UART regression (100× asymmetric drives)
  3. Pin fix verification (manual drift L/R, expect correct symbols)
  4. Compass calibration (`calibrate_compass` → tilt-and-fill the 25 LEDs)
  5. Pose snapshot (tilt forward → +pitch; tilt right → +roll; shake → gesture)
  6. Light (cover sensor → <30; flashlight → >200)
  7. Sound (V2 only; clap → peak above quiet)
  8. scan_distance (clear forward arc + obstacle to one side → expected polar pattern)
  9. RSSI baseline at 0.5m vs 3m
  10. RSSI gradient (3-way scan with `move`+`sample_rssi`)
  11. Capture signal (`send_radio(99, "FOUND")` → beacon skull animation)
  12. follow_line on V1.3 track
  13. End-to-end Claude nav using scan_distance + read_compass + sample_rssi
- **Commit**: working tree dirty; suggested message in plan file
- **Defer to v0.3**: battery telemetry (Cutebot voltage read across revs), IR receiver, strict-mode state graph promotion, async sensor reads, servo integration testing (gated on physical servo)

**Compass UX note (v0.2 limitation):** calibration is awkward with µbit seated in Cutebot — user must tilt the whole bot through the LED gesture game. Document workaround: detach µbit for calibration, reattach. Compass needs re-calibration on every power-cycle.

**Plan file divergence**: the user redirected scope mid-execution from "RSSI hunt for hide-and-seek" → "maximize Claude's sensory input for self-navigation." Original plan (peaceful-growing-candy) kept as record; new plan (i-tried-to-create-serialized-teacup) reflects delivered surface.

The `~/.claude.json` edit during the original build session also surfaced 3 plaintext API keys (sigma-verify env: OpenAI/Google/Anthropic). Keys were dumped to terminal during step 6 — already flagged. Rotate if transcript ever shared.
