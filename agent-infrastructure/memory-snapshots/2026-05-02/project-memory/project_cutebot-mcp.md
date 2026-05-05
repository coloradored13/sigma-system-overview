---
name: cutebot-mcp project
description: MCP server letting Claude drive an ELECFREAKS Cutebot via two micro:bits + radio, using hateoas-agent for state-gated tool discovery. Built 26.5.2, drive live-tested + bridge UART fix + sensor pin inversion discovered 26.5.3.
type: project
originSessionId: 7a07e4bf-655f-4bdb-a008-80b66145a99f
---
# cutebot-mcp

**Repo:** `~/Projects/cutebot-mcp/` (local-only git, no remote — flag before pushing)
**Created:** 2026-05-02
**Last session:** 2026-05-03 — drive live-tested, bridge UART fix, sensor pin inversion found, v0.2 plan written

## Architecture

Claude Code (MCP client) → MCP stdio → Python server (hateoas-agent StateMachine) → pyserial @ 115200 → **bridge** micro:bit V2 (USB, displays "B") → 2.4 GHz radio → **robot** micro:bit V2 on Cutebot (battery-powered, displays 😊).

500ms watchdog on the robot side: motors stop if no command for 500ms, independent of any MCP timeout.

## Status as of session 2 (2026-05-03)

- ✅ Steps 1–6 complete (v0.1 shipped). Drive live-tested. Both motor-isolation tests run, both ergonomic line-state classification + 4-state symbol output added.
- ⚠ Open-loop calibration not converged. At `L=50,R=75` residual ~60°/ft CCW. Decision: stop tuning open-loop, ship `follow_line` closed-loop primitive in v0.2.
- ❗ Bridge UART had a latent partial-line fragmentation bug — `uart.readline()` 1.1ms timeout returns partial data on USB chunking, fragments "D,X,Y,Z\n" into multi-frame nonsense. Fixed in `firmware/bridge_microbit.py` by manual byte accumulation, re-flashed.
- ❗ Line sensor pin13/pin14 wiring inverted on this Cutebot rev vs. Krakenus reference. Host-side workaround in `primitives.py` (parse swap). Proper firmware fix bundled into next reflash (Phase B+C of v0.2 plan).
- 🔧 **Motor friction asymmetry**: right wheel has ~30-50% higher rolling resistance. At `L=R=50` bot rotates 90°+/ft CCW. Motor isolation: 90° (R-only at 50, 300ms) vs 60° (L-only at 50, 300ms). Cause is indeterminate from data (motor weakness vs. friction confounded with pivot test). Closed-loop control sidesteps the diagnosis.
- 🔧 **IR false positives on wood floor**: TCRT5000-class sensors read wood grain as "on track" (●●). Documented limitation, not a fix.

Verified live: ping, I2C headlights, ultrasonic, line sensors, beep, **drive** (now), **motor isolation tests**. The `read_line_sensors` primitive returns 4-state ELECFREAKS-style output (●●/●◌/◌●/◌◌).

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

- `src/cutebot_mcp/server.py` — `build_state_machine()` + `main()`; module-level `_bridge` singleton with lazy open
- `src/cutebot_mcp/bridge.py` — `Bridge` class + `selftest()` + `ping_robot()` + CLI (`--selftest`, `--ping-robot`)
- `src/cutebot_mcp/primitives.py` — human-readable wrappers; each takes a `Bridge` plus kwargs, returns a string
- `firmware/bridge_microbit.py` — 43 lines; `uart.init(115200)` ↔ `radio` relay; `!` namespace
- `firmware/robot_microbit.py` — 168 lines; inlines Cutebot I2C ops (no separate `cutebot.py` flashed); `display.show(HAPPY)` runs *before* any I2C so a battery-off boot still gets the visual confirmation
- `docs/protocol.md` — full wire protocol
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

v0.2 plan written 26.5.3 at `~/.claude/plans/peaceful-growing-candy.md` (sigma-single structured). Top of next session:

- **Phase B+C bundled** (one re-flash of robot µbit, ~4-8h focused work):
  - Fix line-sensor pin labels in `robot_microbit.py` (swap pin13/pin14 in `read_line()`), then revert host-side parse swap in `primitives.py`.
  - Add `set_servo` primitive (S1/S2, angle 0-180, I2C buffer position 5/6).
  - Add `follow_line` primitive — bang-bang controller in robot firmware, dispatched via `F,<speed>,<ms>` wire command. Headline v0.2 feature; sidesteps motor friction asymmetry.
  - Add `move(direction, speed, ms)` ergonomic wrapper around `drive`.
  - Document new wire protocol in `docs/protocol.md`. Note wood-floor false positive in `read_line_sensors` description.
  - State graph: hand-design (NOT promoted to strict mode for v0.2). Stay in discover. Promotion to v0.3 once API stabilizes — `Registry.get_discovery_report().to_python()` is the path (verified in installed hateoas-agent v0.2.0).
- **Defer to v0.3**: IR receiver (cutebot kit ships with remote — embodied teaching use case worth it eventually but no immediate need). Sensor-threshold heuristics for wood-floor false-positives. Persistent Registry checkpoint across MCP restarts (for data-driven state-graph promotion).
- **Verification plan** in Phase D of plan file: bridge UART regression (100x asymmetric drives), sensor pin fix (manual drift left/right), servo end-to-end (need a servo physically connected), follow_line on V1.3 track.

Outside-view says v0.2 takes 8h focused, not 4h optimistic — controller tuning is dominant time sink.

The `~/.claude.json` edit during the original build session also surfaced 3 plaintext API keys (sigma-verify env: OpenAI/Google/Anthropic). Keys were dumped to terminal during step 6 — already flagged. Rotate if transcript ever shared.
