# Skills Index

Categorized inventory of available Claude Code skills. Skills must stay flat at `~/.claude/skills/{name}/SKILL.md` for Claude Code discovery.

## Sigma (Multi-Agent Team Orchestration)
| Skill | Description |
|-------|-------------|
| sigma-review | ANALYZE mode — multi-agent team review (phase-based) |
| sigma-build | BUILD mode — multi-agent implementation with plan→challenge→build→review |
| sigma-audit | Independent process quality audit of a sigma-review |
| sigma-evaluate | Multi-agent rubric evaluation of completed analysis |
| sigma-feedback | Post-review calibration loop (datum/concept tracks) |
| sigma-research | Refresh domain research for sigma-review agents |
| sigma-retrieve | Agentic RAG pipeline for structured retrieval |
| sigma-optimize | Multi-agent evolutionary prompt optimization |
| sigma-dream | Memory consolidation cycle (dedup, prune, promote) |
| sigma-single | Enhanced single-instance analysis |
| sigma-init | Initialize sigma infrastructure for a project |

## Development
| Skill | Description |
|-------|-------------|
| mcp-builder | Build MCP servers (TypeScript/Python) with eval framework |

## Product Management
{empty — skills to be imported from marketplace}

## Security Research
{empty — skills to be imported from marketplace}

## Writing & Documentation
{empty — skills to be imported from marketplace}

---
Adding skills: create `~/.claude/skills/{name}/SKILL.md` with frontmatter (name, description), then add a row to the appropriate domain table above.
