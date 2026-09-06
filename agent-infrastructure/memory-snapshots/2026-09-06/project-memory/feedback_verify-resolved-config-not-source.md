---
name: verify-resolved-config-not-source
description: Verifying a config/model default change by grepping source is insufficient; read the runtime-resolved value or the value recorded in outputs, because env layers override code defaults silently
metadata:
  type: feedback
---

When a change to a code default (model id, endpoint, feature flag) is verified by grepping the source, the check can pass while the runtime keeps the old value. Environment layers (`.env`, LaunchAgent plists, shell exports) override code defaults silently, and tracked `*.example` files seed those layers with stale values.

**Why:** In ai-pd-tracker on 2026-09-05 the plan's verification was `grep -c "claude-sonnet-4-6" coach.py = 0`. It passed. The user's `.env`, seeded from the tracked `.env.example`, set `COACH_MODEL=claude-sonnet-4-6`, so Sonnet 5 never ran and every gold-set calibration run recorded the old model. It was caught a day later only because the eval runner records the `model` field per result. Found while answering the user's "are we on opus or sonnet?" (2026-09-06).

**How to apply:** After changing a default, read the resolved value in-process (load the same env the service loads, then print what the code resolves) or read the field recorded in the run's outputs. Make every experiment artifact record the effective value it used. Ship `*.example` files with overrides commented out. Add the env layers to the verification list whenever a plan says "default → X". Related: [[no-tautological-assertions]], [[mock-tests-false-confidence]].
