#!/usr/bin/env bash
#
# Sigma System — Project Setup
# Initializes project-local team directories for two-tier memory.
# Run this in a project root to enable per-project findings, decisions, and patterns.
# Safe to run multiple times (idempotent).
#
# Usage:
#   cd /path/to/your/project
#   /path/to/sigma-system-overview/setup-project.sh
#
# What it creates:
#   <project>/.claude/teams/sigma-review/
#     shared/decisions.md     — project decisions
#     shared/patterns.md      — project patterns
#     shared/workspace.md     — active task workspace
#     agents/{name}/memory.md — project memory per agent
#     inboxes/{name}.md       — inbox per agent
#
# What stays global (~/.claude/):
#   agents/*.md               — agent role definitions (shared across projects)
#   teams/sigma-review/shared/roster.md — team roster
#   teams/sigma-review/agents/{name}/memory.md — global memory (identity, research, calibration)
#

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }

echo ""
echo "============================================"
echo "  Sigma System — Project Setup"
echo "============================================"
echo ""

# ─────────────────────────────────────────────
# 1. Validate global setup exists
# ─────────────────────────────────────────────
GLOBAL_TEAMS="$HOME/.claude/teams/sigma-review"
GLOBAL_ROSTER="$GLOBAL_TEAMS/shared/roster.md"

if [ ! -d "$GLOBAL_TEAMS" ]; then
    fail "Global team directory not found at $GLOBAL_TEAMS. Run setup.sh first."
fi

if [ ! -f "$GLOBAL_ROSTER" ]; then
    fail "Global roster not found at $GLOBAL_ROSTER. Run setup.sh first."
fi

ok "Global setup found at $GLOBAL_TEAMS"

# ─────────────────────────────────────────────
# 2. Read agent list from global roster
# ─────────────────────────────────────────────
info "Reading agent list from roster..."

# Parse agent names from roster: lines that start with a word followed by " |domain:"
AGENTS=()
while IFS= read -r line; do
    # Extract agent name (first field before " |")
    agent=$(echo "$line" | sed -n 's/^\([a-zA-Z][a-zA-Z0-9_-]*\) |domain:.*/\1/p')
    if [ -n "$agent" ]; then
        AGENTS+=("$agent")
    fi
done < "$GLOBAL_ROSTER"

if [ ${#AGENTS[@]} -eq 0 ]; then
    fail "No agents found in roster at $GLOBAL_ROSTER"
fi

ok "Found ${#AGENTS[@]} agents: ${AGENTS[*]}"
echo ""

# ─────────────────────────────────────────────
# 3. Create project team directory structure
# ─────────────────────────────────────────────
PROJECT_DIR="$(pwd)"
PROJECT_TEAMS="$PROJECT_DIR/.claude/teams/sigma-review"

info "Setting up project team directory at $PROJECT_TEAMS..."

mkdir -p "$PROJECT_TEAMS/shared"

# --- shared/decisions.md ---
DECISIONS="$PROJECT_TEAMS/shared/decisions.md"
if [ ! -f "$DECISIONS" ]; then
    cat > "$DECISIONS" << 'EOF'
# project decisions — expertise-weighted
EOF
    ok "Created decisions.md"
else
    ok "decisions.md already exists"
fi

# --- shared/patterns.md ---
PATTERNS="$PROJECT_TEAMS/shared/patterns.md"
if [ ! -f "$PATTERNS" ]; then
    cat > "$PATTERNS" << 'EOF'
# project patterns — cross-agent
EOF
    ok "Created patterns.md"
else
    ok "patterns.md already exists"
fi

# --- shared/workspace.md ---
WORKSPACE="$PROJECT_TEAMS/shared/workspace.md"
if [ ! -f "$WORKSPACE" ]; then
    cat > "$WORKSPACE" << 'EOF'
# workspace

## status: idle

## task
EOF
    ok "Created workspace.md"
else
    ok "workspace.md already exists"
fi

# --- Agent memory files (project-local) ---
for agent in "${AGENTS[@]}"; do
    mkdir -p "$PROJECT_TEAMS/agents/$agent"
    MEMORY="$PROJECT_TEAMS/agents/$agent/memory.md"
    if [ ! -f "$MEMORY" ]; then
        cat > "$MEMORY" << MEMORY_EOF
# $agent — project memory
MEMORY_EOF
        ok "Created $agent project memory"
    else
        ok "$agent project memory already exists"
    fi
done

# --- Inbox files ---
mkdir -p "$PROJECT_TEAMS/inboxes"
for agent in "${AGENTS[@]}"; do
    INBOX="$PROJECT_TEAMS/inboxes/$agent.md"
    if [ ! -f "$INBOX" ]; then
        cat > "$INBOX" << INBOX_EOF
# inbox — $agent

## processed

## unread
INBOX_EOF
        ok "Created $agent inbox"
    else
        ok "$agent inbox already exists"
    fi
done

echo ""

# ─────────────────────────────────────────────
# 4. Add .claude/teams/ to project .gitignore
# ─────────────────────────────────────────────
info "Checking .gitignore..."

GITIGNORE="$PROJECT_DIR/.gitignore"
TEAMS_PATTERN=".claude/teams/"

if [ -f "$GITIGNORE" ]; then
    if grep -qF "$TEAMS_PATTERN" "$GITIGNORE" 2>/dev/null; then
        ok ".claude/teams/ already in .gitignore"
    else
        echo "" >> "$GITIGNORE"
        echo "# Sigma System — project-local team data (agent findings, decisions, patterns)" >> "$GITIGNORE"
        echo "$TEAMS_PATTERN" >> "$GITIGNORE"
        ok "Added .claude/teams/ to .gitignore"
    fi
else
    cat > "$GITIGNORE" << 'EOF'
# Sigma System — project-local team data (agent findings, decisions, patterns)
.claude/teams/
EOF
    ok "Created .gitignore with .claude/teams/ entry"
fi

echo ""

# ─────────────────────────────────────────────
# 5. Success message
# ─────────────────────────────────────────────
echo "============================================"
echo -e "${GREEN}  Project setup complete!${NC}"
echo "============================================"
echo ""
echo "What was created:"
echo "  $PROJECT_TEAMS/"
echo "    shared/decisions.md     — project decisions"
echo "    shared/patterns.md      — project patterns"
echo "    shared/workspace.md     — active task workspace"
for agent in "${AGENTS[@]}"; do
    echo "    agents/$agent/memory.md"
done
for agent in "${AGENTS[@]}"; do
    echo "    inboxes/$agent.md"
done
echo ""
echo "Two-tier memory is now active for this project:"
echo "  Global (~/.claude/teams/):  identity, research, calibration, roster"
echo "  Project (.claude/teams/):   findings, decisions, patterns, workspace"
echo ""
echo "sigma-mem auto-detects this directory when Claude Code opens the project."
echo "No additional configuration needed."
echo ""
