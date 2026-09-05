#!/usr/bin/env bash
#
# Backup ~/.claude/memory/ and settings.local.json to the repo
# Creates timestamped snapshots in agent-infrastructure/memory-snapshots/
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SNAPSHOT_DIR="$REPO_DIR/agent-infrastructure/memory-snapshots/$(date +%Y-%m-%d)"
MEMORY_DIR="$HOME/.claude/memory"
LOCAL_SETTINGS="$HOME/.claude/settings.local.json"
PROJECT_MEMORY="$HOME/.claude/projects/-Users-$(whoami)/memory"
CALIBRATION_LOG="$HOME/.claude/teams/sigma-review/shared/calibration-log.md"

# Branch guard: snapshots are meant to be committed from main. The session-end
# checklist has each memory-modifying session commit its snapshot, and a commit
# made from whatever branch happens to be checked out lands on feature branches
# (observed 26.9.5: a concurrent session's snapshot rode an open PR). The
# snapshot itself is always written — only the commit guidance changes.
CURRENT_BRANCH="$(git -C "$REPO_DIR" branch --show-current 2>/dev/null || echo unknown)"

# Create snapshot directory
mkdir -p "$SNAPSHOT_DIR"

# Backup sigma-mem memory files
if [ -d "$MEMORY_DIR" ]; then
    cp "$MEMORY_DIR"/*.md "$SNAPSHOT_DIR/" 2>/dev/null || true
    echo "Backed up $(ls "$SNAPSHOT_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ') memory files"
else
    echo "WARNING: $MEMORY_DIR not found" >&2
fi

# Backup settings.local.json
if [ -f "$LOCAL_SETTINGS" ]; then
    cp "$LOCAL_SETTINGS" "$SNAPSHOT_DIR/settings.local.json"
    echo "Backed up settings.local.json"
else
    echo "WARNING: $LOCAL_SETTINGS not found" >&2
fi

# Backup β+ calibration-log (append-only audit record for WARN-first gates)
if [ -f "$CALIBRATION_LOG" ]; then
    cp "$CALIBRATION_LOG" "$SNAPSHOT_DIR/calibration-log.md"
    echo "Backed up calibration-log.md"
fi

# Backup project-scoped auto-memory (MEMORY.md only — the rest is ephemeral)
if [ -d "$PROJECT_MEMORY" ]; then
    mkdir -p "$SNAPSHOT_DIR/project-memory"
    cp "$PROJECT_MEMORY"/MEMORY.md "$SNAPSHOT_DIR/project-memory/" 2>/dev/null || true
    # Also grab any .md files in the project memory dir
    for f in "$PROJECT_MEMORY"/*.md; do
        [ -f "$f" ] || continue
        cp "$f" "$SNAPSHOT_DIR/project-memory/"
    done
    echo "Backed up project-scoped memory ($(ls "$SNAPSHOT_DIR/project-memory/"*.md 2>/dev/null | wc -l | tr -d ' ') files)"
fi

echo ""
echo "Snapshot saved to: $SNAPSHOT_DIR"
echo "Files:"
ls -la "$SNAPSHOT_DIR"/ 2>/dev/null
echo ""
if [ "$CURRENT_BRANCH" = "main" ]; then
    echo "To commit: cd $REPO_DIR && git add agent-infrastructure/memory-snapshots/ && git commit -m 'Memory snapshot $(date +%Y-%m-%d)'"
else
    echo "⚠️  Repo is on branch '$CURRENT_BRANCH', NOT main."
    echo "⚠️  Do NOT commit the snapshot from this branch — it will ride along in"
    echo "⚠️  someone else's open PR. Snapshot files are written and safe on disk."
    echo "⚠️  When the repo returns to main: git add agent-infrastructure/memory-snapshots/ && git commit"
fi
