#!/usr/bin/env bash
#
# Sigma System Setup
# Installs hateoas-agent, sigma-mem, agent definitions, team structure, and MCP config.
# Safe to run multiple times (idempotent).
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
CLAUDE_JSON="$HOME/.claude.json"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"
AGENTS_DIR="$CLAUDE_DIR/agents"
TEAMS_DIR="$CLAUDE_DIR/teams/sigma-review"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; exit 1; }

echo ""
echo "============================================"
echo "  Sigma System Setup"
echo "============================================"
echo ""

# ─────────────────────────────────────────────
# 1. Check prerequisites
# ─────────────────────────────────────────────
info "Checking prerequisites..."

# Python 3.10+
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 10 ]; then
        ok "Python $PY_VERSION found"
    else
        fail "Python 3.10+ required, found $PY_VERSION"
    fi
else
    fail "Python 3 not found. Install Python 3.10+ first."
fi

# pip
if python3 -m pip --version &>/dev/null; then
    ok "pip found"
else
    fail "pip not found. Install pip first (python3 -m ensurepip or your package manager)."
fi

# Claude Code CLI
if command -v claude &>/dev/null; then
    ok "Claude Code CLI found"
else
    warn "Claude Code CLI not found. Install it from https://docs.anthropic.com/en/docs/claude-code"
    warn "Continuing setup — you'll need Claude Code to use the system."
fi

echo ""

# ─────────────────────────────────────────────
# 2. Optional: Anthropic API key
# ─────────────────────────────────────────────
info "Anthropic API key (optional — only needed for hateoas-agent integration tests)"
read -rp "  Enter your API key (or press Enter to skip): " API_KEY

if [ -n "$API_KEY" ]; then
    ENV_FILE="$SCRIPT_DIR/.env"
    if [ -f "$ENV_FILE" ]; then
        # Update existing key if present, otherwise append
        if grep -q "^ANTHROPIC_API_KEY=" "$ENV_FILE" 2>/dev/null; then
            sed -i.bak "s/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$API_KEY/" "$ENV_FILE" && rm -f "$ENV_FILE.bak"
            ok "Updated API key in .env"
        else
            echo "ANTHROPIC_API_KEY=$API_KEY" >> "$ENV_FILE"
            ok "Added API key to .env"
        fi
    else
        echo "ANTHROPIC_API_KEY=$API_KEY" > "$ENV_FILE"
        ok "Created .env with API key"
    fi
    # Ensure .env is gitignored
    GITIGNORE="$SCRIPT_DIR/.gitignore"
    if [ -f "$GITIGNORE" ]; then
        if ! grep -qx ".env" "$GITIGNORE" 2>/dev/null; then
            echo ".env" >> "$GITIGNORE"
            ok "Added .env to .gitignore"
        fi
    else
        echo ".env" > "$GITIGNORE"
        ok "Created .gitignore with .env entry"
    fi
else
    info "Skipping API key setup"
fi

echo ""

# ─────────────────────────────────────────────
# 3. Install hateoas-agent
# ─────────────────────────────────────────────
info "Installing hateoas-agent..."
if python3 -c "import hateoas_agent" &>/dev/null; then
    ok "hateoas-agent already installed"
else
    python3 -m pip install "git+https://github.com/coloradored13/hateoas-agent.git" --quiet
    ok "hateoas-agent installed"
fi

# ─────────────────────────────────────────────
# 4. Install sigma-mem
# ─────────────────────────────────────────────
info "Installing sigma-mem..."
if python3 -c "import sigma_mem" &>/dev/null; then
    ok "sigma-mem already installed"
else
    python3 -m pip install "git+https://github.com/coloradored13/sigma-mem.git" --quiet
    ok "sigma-mem installed"
fi

echo ""

# ─────────────────────────────────────────────
# 5. Copy agent definitions
# ─────────────────────────────────────────────
info "Setting up agent definitions in $AGENTS_DIR..."

mkdir -p "$AGENTS_DIR"

AGENT_FILES=(
    "sigma-lead.md"
    "sigma-comm.md"
    "tech-architect.md"
    "product-strategist.md"
    "ux-researcher.md"
    "code-quality-analyst.md"
    "technical-writer.md"
    "SIGMA-COMM-SPEC.md"
)

SRC_AGENTS="$SCRIPT_DIR/agent-infrastructure/agents"

for file in "${AGENT_FILES[@]}"; do
    src="$SRC_AGENTS/$file"
    dest="$AGENTS_DIR/$file"
    if [ ! -f "$src" ]; then
        warn "Source file $src not found — skipping"
        continue
    fi
    if [ -f "$dest" ]; then
        # Check if content differs
        if cmp -s "$src" "$dest"; then
            ok "$file already up to date"
        else
            warn "$file already exists at $dest with different content"
            read -rp "  Overwrite? (y/N): " overwrite
            if [[ "$overwrite" =~ ^[Yy]$ ]]; then
                cp "$src" "$dest"
                ok "$file updated"
            else
                info "Keeping existing $file"
            fi
        fi
    else
        cp "$src" "$dest"
        ok "$file installed"
    fi
done

echo ""

# ─────────────────────────────────────────────
# 6. Create team directory structure
# ─────────────────────────────────────────────
info "Setting up team directory at $TEAMS_DIR..."

mkdir -p "$TEAMS_DIR/shared"
mkdir -p "$TEAMS_DIR/agents/tech-architect"
mkdir -p "$TEAMS_DIR/agents/product-strategist"
mkdir -p "$TEAMS_DIR/agents/ux-researcher"
mkdir -p "$TEAMS_DIR/inboxes"

# --- shared/roster.md ---
ROSTER="$TEAMS_DIR/shared/roster.md"
if [ ! -f "$ROSTER" ]; then
    cat > "$ROSTER" << 'ROSTER_EOF'
# sigma-review team roster

tech-architect |domain: architecture,security,performance,infra,api-design |wake-for: technical decisions,code review,system design,debugging
product-strategist |domain: market,growth,monetization,prioritization,user-segmentation |wake-for: feature decisions,positioning,launch readiness,competitive analysis
ux-researcher |domain: usability,accessibility,mental-models,information-architecture,learnability |wake-for: user-facing changes,flow design,dual-user questions,onboarding

→ actions:
→ adding a new agent → append to roster with domain+wake-for
→ checking who to wake → match task keywords against wake-for fields
→ team decision needed → route to agent whose domain matches topic
ROSTER_EOF
    ok "Created roster.md"
else
    ok "roster.md already exists"
fi

# --- shared/decisions.md ---
DECISIONS="$TEAMS_DIR/shared/decisions.md"
if [ ! -f "$DECISIONS" ]; then
    cat > "$DECISIONS" << 'DECISIONS_EOF'
# team decisions — expertise-weighted
DECISIONS_EOF
    ok "Created decisions.md"
else
    ok "decisions.md already exists"
fi

# --- shared/patterns.md ---
PATTERNS="$TEAMS_DIR/shared/patterns.md"
if [ ! -f "$PATTERNS" ]; then
    cat > "$PATTERNS" << 'PATTERNS_EOF'
# cross-agent patterns
PATTERNS_EOF
    ok "Created patterns.md"
else
    ok "patterns.md already exists"
fi

# --- shared/workspace.md ---
WORKSPACE="$TEAMS_DIR/shared/workspace.md"
if [ ! -f "$WORKSPACE" ]; then
    cat > "$WORKSPACE" << 'WORKSPACE_EOF'
# workspace

## status: idle

## task
WORKSPACE_EOF
    ok "Created workspace.md"
else
    ok "workspace.md already exists"
fi

# --- Agent memory files ---
for agent in tech-architect product-strategist ux-researcher; do
    MEMORY="$TEAMS_DIR/agents/$agent/memory.md"
    if [ ! -f "$MEMORY" ]; then
        cat > "$MEMORY" << MEMORY_EOF
# $agent — personal memory
MEMORY_EOF
        ok "Created $agent/memory.md"
    else
        ok "$agent/memory.md already exists"
    fi
done

# --- Inbox files ---
for agent in tech-architect product-strategist ux-researcher; do
    INBOX="$TEAMS_DIR/inboxes/$agent.md"
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
# 7. Configure MCP server in ~/.claude.json
# ─────────────────────────────────────────────
info "Configuring sigma-mem MCP server in $CLAUDE_JSON..."

# Find where sigma-mem's server module lives
SIGMA_MEM_SERVER=$(python3 -c "import sigma_mem; import os; print(os.path.dirname(sigma_mem.__file__))" 2>/dev/null || echo "")
PYTHON_PATH=$(command -v python3)

if [ -z "$SIGMA_MEM_SERVER" ]; then
    warn "Could not locate sigma_mem module. MCP config skipped — see SETUP.md for manual instructions."
else
    if [ -f "$CLAUDE_JSON" ]; then
        # Check if sigma-mem is already configured
        if python3 -c "
import json, sys
with open('$CLAUDE_JSON') as f:
    data = json.load(f)
servers = data.get('mcpServers', {})
if 'sigma-mem' in servers:
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
            ok "sigma-mem MCP server already configured"
        else
            # Merge sigma-mem into existing config
            python3 -c "
import json
with open('$CLAUDE_JSON') as f:
    data = json.load(f)
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['sigma-mem'] = {
    'command': '$PYTHON_PATH',
    'args': ['-m', 'sigma_mem.server']
}
with open('$CLAUDE_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
            ok "Added sigma-mem MCP server to $CLAUDE_JSON"
        fi
    else
        # Create new .claude.json with just the MCP config
        python3 -c "
import json
data = {
    'mcpServers': {
        'sigma-mem': {
            'command': '$PYTHON_PATH',
            'args': ['-m', 'sigma_mem.server']
        }
    }
}
with open('$CLAUDE_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
        ok "Created $CLAUDE_JSON with sigma-mem MCP server"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 8. Append recall-first instructions to ~/.claude/CLAUDE.md
# ─────────────────────────────────────────────
info "Configuring recall-first behavior in $CLAUDE_MD..."

RECALL_MARKER="# Sigma System — recall-first behavior"

mkdir -p "$CLAUDE_DIR"

if [ -f "$CLAUDE_MD" ]; then
    if grep -qF "$RECALL_MARKER" "$CLAUDE_MD" 2>/dev/null; then
        ok "Recall-first instructions already present"
    else
        cat >> "$CLAUDE_MD" << 'CLAUDE_MD_EOF'

# Sigma System — recall-first behavior

Always start conversations by calling mcp__sigma-mem__recall before reading memory files directly. Use its actions (search_memory, get_project, etc.) to go deeper when needed.

When storing memories, use the sigma-mem MCP actions (store_memory, log_decision, log_correction, log_failure) rather than writing files directly. Match the compressed notation format you see in the recall response — pipe-separated fields, checksums, dates as YY.M.D. See rosetta.md (via recall → decode notation) if unsure about notation.
CLAUDE_MD_EOF
        ok "Appended recall-first instructions to $CLAUDE_MD"
    fi
else
    cat > "$CLAUDE_MD" << 'CLAUDE_MD_EOF'
# Sigma System — recall-first behavior

Always start conversations by calling mcp__sigma-mem__recall before reading memory files directly. Use its actions (search_memory, get_project, etc.) to go deeper when needed.

When storing memories, use the sigma-mem MCP actions (store_memory, log_decision, log_correction, log_failure) rather than writing files directly. Match the compressed notation format you see in the recall response — pipe-separated fields, checksums, dates as YY.M.D. See rosetta.md (via recall → decode notation) if unsure about notation.
CLAUDE_MD_EOF
    ok "Created $CLAUDE_MD with recall-first instructions"
fi

echo ""

# ─────────────────────────────────────────────
# 9. Run sigma-mem tests to verify installation
# ─────────────────────────────────────────────
info "Verifying installation by running sigma-mem tests..."

SIGMA_MEM_PKG_DIR=$(python3 -c "import sigma_mem, os; print(os.path.dirname(os.path.dirname(os.path.dirname(sigma_mem.__file__))))" 2>/dev/null || echo "")

if [ -n "$SIGMA_MEM_PKG_DIR" ] && [ -d "$SIGMA_MEM_PKG_DIR/tests" ]; then
    if python3 -m pytest "$SIGMA_MEM_PKG_DIR/tests" --quiet --tb=short 2>/dev/null; then
        ok "All sigma-mem tests passed"
    else
        warn "Some sigma-mem tests failed. This may be expected if memory files haven't been initialized yet."
        warn "Run 'python3 -m pytest' in the sigma-mem directory to debug."
    fi
else
    # Try running tests from the submodule if available
    if [ -d "$SCRIPT_DIR/sigma-mem/tests" ]; then
        if python3 -m pytest "$SCRIPT_DIR/sigma-mem/tests" --quiet --tb=short 2>/dev/null; then
            ok "All sigma-mem tests passed (from submodule)"
        else
            warn "Some sigma-mem tests failed. Run 'python3 -m pytest sigma-mem/tests' to debug."
        fi
    else
        warn "Could not locate sigma-mem tests. Verify manually: python3 -c 'import sigma_mem; print(\"OK\")'"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 10. Success message
# ─────────────────────────────────────────────
echo "============================================"
echo -e "${GREEN}  Sigma System setup complete!${NC}"
echo "============================================"
echo ""
echo "What was installed:"
echo "  - hateoas-agent (Python package)"
echo "  - sigma-mem (Python package + MCP server)"
echo "  - Agent definitions in ~/.claude/agents/"
echo "  - Team structure in ~/.claude/teams/sigma-review/"
echo "  - MCP config in ~/.claude.json"
echo "  - Recall-first instructions in ~/.claude/CLAUDE.md"
echo ""
echo "Next steps:"
echo "  1. Open Claude Code in any project directory"
echo "  2. Claude will automatically call recall at the start of each conversation"
echo "  3. To run a team review, tell Claude:"
echo "     \"Run a sigma-review of this project\""
echo "  4. To talk to a specific agent:"
echo "     \"@tech-architect review the auth module\""
echo ""
echo "For more details, see SETUP.md in this repository."
echo ""
