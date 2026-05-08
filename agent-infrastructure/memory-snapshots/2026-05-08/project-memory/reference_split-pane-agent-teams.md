---
name: Split-pane agent teams
description: Claude Code native UX for user-as-participant multi-agent chat — user + N teammates each in their own tmux pane, all directly addressable
type: reference
originSessionId: aedeec3b-1cbf-4e69-8ccd-a39919ef4b0f
---
Use case: user wants to chat with multiple agents simultaneously, address either one directly, have agents talk to each other. Group-chat shape, not delegation.

Native answer: Claude Code experimental agent teams in split-pane (tmux) display mode.

Setup:
- `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`
- Install tmux (or use iTerm2; VS Code integrated terminal NOT supported)
- Spawn with `--teammate-mode tmux`, or set `"teammateMode": "tmux"` in settings.json. Note: ~/.claude/settings.json is symlinked to sigma-system-overview, so a global change there is a real commit.

Each teammate runs as a full independent Claude Code session in its own pane. Click into a pane to type directly to that teammate — no lead mediation. Teammates SendMessage between themselves. Shared task list across panes.

In-process mode (default, no tmux) cycles teammates with Shift+Down — feels more serial and lead-routed; not the same UX.

Limitations:
- Experimental; behavior may shift between releases
- In-process teammates lost on `claude --resume`; split-pane gets per-pane persistence, not full team resume
- No cross-session persistence — kill the lead, kill the team
- Requires tmux or iTerm2

Distinction from sigma-chatroom: split-pane = same-family Claude agents with human-in-loop dialogue; chatroom = architecturally heterogeneous models (Claude + GPT + Gemini + Ollama) for studying emergent cross-architecture behavior. Different use cases — pick by what you're optimizing for.

Does NOT trip the avoid-parallel-sessions rule — split-pane teammates are managed by one lead, not independent `claude` invocations writing to shared infra.

Doc: https://code.claude.com/docs/en/agent-teams.md (sections: "Talk to teammates directly", "Choose a display mode")
