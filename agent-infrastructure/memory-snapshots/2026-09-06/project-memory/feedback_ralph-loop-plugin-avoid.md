---
name: ralph-loop-plugin-avoid
description: Don't install the official ralph-loop plugin in any project where chain-evaluator.py is registered as a Stop hook. Extract the pattern via sigma-ralph instead.
type: feedback
originSessionId: 23e5861d-b4e3-43a6-99f1-f69f9b372243
---
Never install the `claude-plugins-official/plugins/ralph-loop` plugin in any chain-evaluator-active project. Use sigma-ralph (or pure-bash equivalent) instead.

**Why:** The plugin implements Ralph via a Stop hook that intercepts session exit and re-feeds the prompt. The user's chain-evaluator.py is also a Stop hook — non-looping by design, fires once at session end to write evaluation artifacts. Both Stop hooks fire on every iteration: chain-evaluator writes "session complete" evaluation artifacts assuming the session is over; ralph-stop blocks exit and re-feeds prompt. Result: stale workspace artifacts written every iteration, plus phase-gate firing on every iteration if inside a sigma-build.

**How to apply:** When the user asks about ralph-loop, recommend the pattern (fresh-context iteration with externalized state and completion sentinel) but route to sigma-ralph (`~/Projects/sigma-ralph/`) or external bash, NOT the plugin. The pattern is more valuable than any plugin packaging. Standalone sigma-ralph runs in non-sigma directories never trigger chain-evaluator at all because they don't enter a Claude Code session — they call the Anthropic SDK directly.

**Scope:** This is a hook-architecture conflict, not a "plugin bad" judgment. The plugin would work fine in a setup without chain-evaluator; this user has chain-evaluator and the conflict is structural. If chain-evaluator ever changes to be opt-in per project, the constraint relaxes.
