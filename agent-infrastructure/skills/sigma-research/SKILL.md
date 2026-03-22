---
name: sigma-research
description: Refresh domain research for sigma-review agents. Agents conduct web research in their expertise areas and store findings in memory for use during reviews. Use when agent research is stale, before a major review, or when the user says "research refresh" or "update agent research".
argument-hint: "[agent-name or 'all']"
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# Sigma Research — Domain Research Refresh

Refresh research for: **$ARGUMENTS** (default: all agents)

## Pre-flight

1→recall: "sigma-review research refresh"
2→read roster: `~/.claude/teams/sigma-review/shared/roster.md`
3→determine target agents:
  - $ARGUMENTS names a specific agent → verify agent exists in roster → target that agent
  - $ARGUMENTS is empty or "all" → target all agents
  - $ARGUMENTS names multiple agents → target those agents

## Per-Agent Research

For each target agent:

1→read agent memory (global tier): `~/.claude/teams/sigma-review/agents/{name}/memory.md`
2→check ## research section:
  - ¬exists → full research needed
  - exists → check freshness (refreshed date vs now)
  - stale (>30d or >5 reviews since) → refresh needed
  - fresh → skip (report "research current for {name}")

3→read agent definition: `~/.claude/agents/{name}.md` → extract Expertise areas

4→spawn research agent (one per target agent) with prompt:

```
You are {name} conducting domain research.
Expertise: {from agent definition}

## Task
Research current best practices, frameworks, and patterns in your domain areas.

## Research Areas
{agent's expertise areas from definition}

## Instructions
1→web-search: current developments in each expertise area
2→focus: frameworks, best-practices, patterns, breaking changes, new tools
3→synthesize findings in ΣComm format
4→store via sigma-mem:
  store_agent_memory(
    tier: global,
    agent: {name},
    team: sigma-review,
    entry: "## research\nR[{topic}:{findings}|src:{sources}|refreshed:{date}|next:{target}]"
  )
5→note deltas from last refresh (what changed since previous research)

## Format
Store research as:
R[{topic}:{key-findings}|src:{source-urls}|refreshed:{YY.M.D}|next:{YY.M.D}]

Date format MUST be YY.M.D (e.g. 26.3.22 for 2026-03-22). This is required for the freshness validator.

One R[] block per topic area. Include sources for verification.
```

## Parallel Execution

When researching multiple agents, spawn all research agents in parallel using the Agent tool. Each agent researches independently in their own domain.

## Completion

After all research agents complete:

1→verify each agent's memory was updated (get_agent_memory for each)
2→report to user:
  ```
  Research refresh complete.

  {agent-name}: {summary of what was researched} (refreshed: {date})
  {agent-name}: {summary} (refreshed: {date})
  ...

  Next suggested refresh: {earliest next-refresh date across agents}
  ```
3→if any agent failed to persist → warn user + retry
