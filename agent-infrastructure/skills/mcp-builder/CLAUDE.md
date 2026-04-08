# MCP Builder Skill

This directory contains a ported skill from Claude.ai's artifacts environment. It provides structured guidance, reference docs, and evaluation scripts for building high-quality MCP servers.

## How to use

When working on MCP server development, read `SKILL.md` first — it's the main workflow guide. It references files in `reference/` and `scripts/` that you should load as needed.

### Key files

- `SKILL.md` — Main process guide (phases 1–4: research, implement, review, evaluate)
- `reference/mcp_best_practices.md` — Universal MCP design guidelines
- `reference/node_mcp_server.md` — TypeScript implementation patterns
- `reference/python_mcp_server.md` — Python/FastMCP implementation patterns
- `reference/evaluation.md` — How to create eval question sets
- `scripts/` — Evaluation runner scripts (Python)

### Quick start

When I ask you to build an MCP server:
1. Read `SKILL.md` for the full workflow
2. Load the relevant language guide from `reference/`
3. Load `reference/mcp_best_practices.md` for design principles
4. After implementation, load `reference/evaluation.md` to create evals
