# Using This Skill in Claude Code

## Setup

1. Copy this folder into your project (e.g., `.claude/skills/mcp-builder/`)
2. In your project-level `CLAUDE.md`, add a reference:

```markdown
## Skills
When building MCP servers, read `.claude/skills/mcp-builder/SKILL.md` and follow its workflow.
```

3. That's it. When you ask Claude Code to build an MCP server, tell it to read the skill first, or it will pick it up from CLAUDE.md.

## Alternative: use as a standalone project

If you want this skill to be the *entire* project context (e.g., a dedicated MCP-building workspace):

1. Place these files at the project root
2. Rename `CLAUDE.md` or merge it with your existing one
3. Claude Code will automatically read `CLAUDE.md` at the start of each session

## Notes

- The `scripts/` folder contains Python evaluation tooling — install deps with `pip install -r scripts/requirements.txt`
- The SKILL.md references fetching live SDK docs from GitHub. Claude Code can do this via its built-in web fetch if you have it enabled.
