#!/usr/bin/env bash
#
# Assemble modular CLAUDE.md sources into ~/.claude/CLAUDE.md
# Sources are numbered NN-*.md files in this directory, concatenated in sort order.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$HOME/.claude/CLAUDE.md"

# Collect source files in sort order
sources=()
for f in "$SCRIPT_DIR"/[0-9][0-9]-*.md; do
    [ -f "$f" ] || continue
    sources+=("$f")
done

if [ ${#sources[@]} -eq 0 ]; then
    echo "ERROR: No source files found in $SCRIPT_DIR" >&2
    exit 1
fi

# Assemble: concatenate with blank line between sections
# Note: $(cat) strips trailing newlines, so we use \n\n between sections
# to produce the expected blank-line separator
first=true
assembled=""
for f in "${sources[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        assembled+=$'\n\n'
    fi
    assembled+="$(cat "$f")"
done

# Write output (echo adds trailing newline)
echo "$assembled" > "$TARGET"

# Report
line_count=$(wc -l < "$TARGET" | tr -d ' ')
echo "Assembled ${#sources[@]} sources -> $TARGET ($line_count lines)"

if [ "$line_count" -gt 70 ]; then
    echo "WARNING: CLAUDE.md exceeds 70 lines ($line_count). Consider trimming." >&2
fi
