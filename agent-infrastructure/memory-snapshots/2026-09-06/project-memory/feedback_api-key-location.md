---
name: API key location for MCP servers
description: sigma-verify and sigma-mem API keys live in ~/.claude.json mcpServers env, NOT in .env files. Use claude mcp add/remove to manage.
type: feedback
---

MCP server API keys are stored in `~/.claude.json` under `mcpServers.{name}.env`, NOT in `.env` files.

**Why:** User corrected assumption that keys were in `~/Projects/Zoltar/sigma-predict/.env`. That file exists but is used by cross_model_test.py directly, not by the MCP server. The MCP server gets its env vars from the Claude Code config.

**How to apply:**
- To check keys: `claude mcp get sigma-verify` or read `~/.claude.json` programmatically
- To add keys: edit `~/.claude.json` directly (nano) or `claude mcp remove` + `claude mcp add` with `-e` flags
- Syntax for `claude mcp add`: name comes AFTER `add`, options after name: `claude mcp add sigma-verify -s user -e KEY=val -- command args`
- NEVER print key values in conversation — redact with `=***`
- `~/.claude.json` is large (~900+ lines) — be careful with nano edits, they can truncate the file
