# claude-md (archived)

This directory previously held modular CLAUDE.md sources with an `assemble.sh` script
that concatenated numbered fragments into `~/.claude/CLAUDE.md`.

**Retired 2026-04-15.** The modular approach caused two problems:

1. **ΣComm boundary violation** — source fragments were written in ΣComm notation,
   but CLAUDE.md is human-facing and must be plain English per the notation boundary rule.

2. **Destructive overwrite** — `assemble.sh` silently replaced hand-maintained content,
   wiping behavioral rails that had been refined through correction history.

CLAUDE.md is now maintained directly at `~/.claude/CLAUDE.md` as the single source of truth.
At 83 lines it does not benefit from modular assembly. Setup.sh no longer calls assemble.sh.
