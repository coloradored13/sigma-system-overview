---
name: sigma-dream
description: "Run sigma-mem dream consolidation cycle — dedup, prune stale entries, promote beliefs, index integrity. Use when memory feels cluttered, before major reviews, or on a schedule. Dry-run by default, 'apply' to execute."
argument-hint: "[scope: personal|team|all] [apply]"
allowed-tools: Read, Bash, Agent, mcp__sigma-mem__recall, mcp__sigma-mem__dream, mcp__sigma-mem__check_integrity
---

# Sigma Dream — Memory Consolidation Cycle

Run dream consolidation for: **$ARGUMENTS** (default: all, dry-run)

## Parse Arguments

1→parse $ARGUMENTS:
  - scope: "personal", "team", or "all" (default: "all")
  - "apply" keyword present → apply=true, else apply=false
  - team name if specified (default: all teams discovered)
  - examples:
    - `/dream` → scope=all, dry_run
    - `/dream apply` → scope=all, apply
    - `/dream personal` → scope=personal, dry_run
    - `/dream team sigma-review apply` → scope=team, team=sigma-review, apply

## Execute

1→invoke `mcp__sigma-mem__dream` with parsed params:
  - scope: {parsed scope}
  - team_name: {parsed team or ""}
  - apply: {"true" if apply else "false"}

2→receive dream journal (structured report)

## Present Results

Format the journal as a concise summary for the user:

### Dry-run output
```
## Dream Journal — {date}
Mode: dry-run (use `/dream apply` to execute)

### Personal Memory ({total_lines} lines across {file_count} files)

**Consolidate**: {n} duplicates found
{list files with dupe counts}

**Prune**: {n} stale entries
- R[] expired: {list}
- Old corrections (>90d): {count}
- Old failures (>90d): {count}

**Reorganize**:
- Promotable beliefs (C~→C): {count}
  {list beliefs and where found}
- Systemic patterns (≥3 occurrences): {count}
  {list topics}

**Index**: {checksum_issues} checksum issues
Confidence: {distribution}

### Team: {name} ({shared_lines} shared, {agent_count} agents)

**Consolidate**: {n} duplicates in shared files
**Prune**: {stale_agents} agents with stale research, {clearable} inboxes clearable
**Reorganize**: {canonical} canonical pattern candidates
**Index**: {stats}

---
Proposed actions: {total}
To apply safe changes (dedup removal): `/dream apply`
```

### Apply output
```
## Dream Journal — {date}
Mode: apply

### Changes Applied
- Removed {n} duplicate lines from {files}
{before/after line counts}

### Advisory (requires manual review)
- {stale entries to review}
- {beliefs to consider promoting}
- {systemic patterns detected}
```

## Rules

- Never modify ΣComm notation — dream works WITH compressed format, not against it
- Apply mode only executes dedup (safest operation) — prune/reorganize are advisory
- If journal shows 0 proposed actions → report "memory is clean, no consolidation needed"
- Include the date in every journal for freshness tracking
