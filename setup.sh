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
VENV_DIR="$CLAUDE_DIR/sigma-venv"

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

# ─────────────────────────────────────────────
# Pull mode: import new/changed files from installed → repo
# Usage: ./setup.sh pull
# ─────────────────────────────────────────────
if [ "${1:-}" = "pull" ]; then
    echo ""
    echo "============================================"
    echo "  Sigma System Pull (installed → repo)"
    echo "============================================"
    echo ""

    SRC_AGENTS="$SCRIPT_DIR/agent-infrastructure/agents"
    SRC_SHARED="$SCRIPT_DIR/agent-infrastructure/teams/sigma-review/shared"

    # Pull agents: find installed agents not in repo, or modified
    info "Checking agents..."
    new_count=0
    modified_count=0
    for installed in "$AGENTS_DIR"/*.md; do
        [ -f "$installed" ] || continue
        file=$(basename "$installed")
        repo="$SRC_AGENTS/$file"
        if [ ! -f "$repo" ]; then
            warn "NEW agent not in repo: $file"
            read -rp "  Import to repo? (y/N): " import
            if [[ "$import" =~ ^[Yy]$ ]]; then
                cp "$installed" "$repo"
                ok "Imported $file to repo"
                ((new_count++))
            fi
        elif ! cmp -s "$installed" "$repo"; then
            warn "MODIFIED: $file (installed differs from repo)"
            read -rp "  Import installed version to repo? (y/N): " import
            if [[ "$import" =~ ^[Yy]$ ]]; then
                cp "$installed" "$repo"
                ok "Updated $file in repo"
                ((modified_count++))
            fi
        fi
    done

    # Pull shared files: roster, directives, protocols
    info "Checking shared files..."
    for shared_file in roster.md directives.md protocols.md; do
        installed="$TEAMS_DIR/shared/$shared_file"
        repo="$SRC_SHARED/$shared_file"
        [ -f "$installed" ] || continue
        if [ ! -f "$repo" ]; then
            warn "NEW shared file not in repo: $shared_file"
            read -rp "  Import to repo? (y/N): " import
            if [[ "$import" =~ ^[Yy]$ ]]; then
                cp "$installed" "$repo"
                ok "Imported $shared_file to repo"
                ((new_count++))
            fi
        elif ! cmp -s "$installed" "$repo"; then
            warn "MODIFIED: $shared_file (installed differs from repo)"
            read -rp "  Import installed version to repo? (y/N): " import
            if [[ "$import" =~ ^[Yy]$ ]]; then
                cp "$installed" "$repo"
                ok "Updated $shared_file in repo"
                ((modified_count++))
            fi
        fi
    done

    # Pull skills
    info "Checking skills..."
    INSTALLED_SKILLS="$CLAUDE_DIR/skills"
    SRC_SKILLS="$SCRIPT_DIR/agent-infrastructure/skills"
    if [ -d "$INSTALLED_SKILLS" ]; then
        for skill_dir in "$INSTALLED_SKILLS"/*/; do
            [ -d "$skill_dir" ] || continue
            skill_name=$(basename "$skill_dir")
            installed="$skill_dir/SKILL.md"
            repo="$SRC_SKILLS/$skill_name/SKILL.md"
            [ -f "$installed" ] || continue
            if [ ! -f "$repo" ]; then
                warn "NEW skill not in repo: $skill_name"
                read -rp "  Import to repo? (y/N): " import
                if [[ "$import" =~ ^[Yy]$ ]]; then
                    mkdir -p "$SRC_SKILLS/$skill_name"
                    cp "$installed" "$repo"
                    ok "Imported $skill_name skill to repo"
                    ((new_count++))
                fi
            elif ! cmp -s "$installed" "$repo"; then
                warn "MODIFIED: $skill_name skill (installed differs from repo)"
                read -rp "  Import installed version to repo? (y/N): " import
                if [[ "$import" =~ ^[Yy]$ ]]; then
                    cp "$installed" "$repo"
                    ok "Updated $skill_name skill in repo"
                    ((modified_count++))
                fi
            fi
        done
    fi

    # Check CLAUDE.md for sigma-specific content drift
    info "Checking ~/.claude/CLAUDE.md for sigma-related content..."
    if [ -f "$CLAUDE_MD" ]; then
        SIGMA_LINES=$(grep -c -E '(sigma-mem|recall|store_memory|log_decision|check_integrity|ΣComm|sigma-comm)' "$CLAUDE_MD" 2>/dev/null || echo "0")
        if [ "$SIGMA_LINES" -gt 0 ]; then
            ok "CLAUDE.md contains $SIGMA_LINES sigma-related lines"
            # Save a snapshot for reference
            CLAUDE_SNAPSHOT="$SCRIPT_DIR/agent-infrastructure/claude-md-snapshot.txt"
            grep -E '(sigma-mem|recall|store_memory|log_decision|check_integrity|ΣComm|sigma-comm|session-end)' "$CLAUDE_MD" > "$CLAUDE_SNAPSHOT.new" 2>/dev/null || true
            if [ -f "$CLAUDE_SNAPSHOT" ] && ! cmp -s "$CLAUDE_SNAPSHOT" "$CLAUDE_SNAPSHOT.new"; then
                warn "Sigma-related content in CLAUDE.md has changed since last pull"
                echo "  Review: diff $CLAUDE_SNAPSHOT $CLAUDE_SNAPSHOT.new"
                cp "$CLAUDE_SNAPSHOT.new" "$CLAUDE_SNAPSHOT"
                ((modified_count++))
            elif [ ! -f "$CLAUDE_SNAPSHOT" ]; then
                cp "$CLAUDE_SNAPSHOT.new" "$CLAUDE_SNAPSHOT"
                ok "Saved CLAUDE.md sigma content snapshot"
            fi
            rm -f "$CLAUDE_SNAPSHOT.new"
        else
            warn "CLAUDE.md has no sigma-related content — may need re-setup"
        fi
    fi

    echo ""
    echo "Pull complete: $new_count new, $modified_count modified"
    echo "Run 'git diff' to review changes before committing."
    exit 0
fi

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
# 3. Create venv and install packages
# ─────────────────────────────────────────────
info "Setting up Python environment at $VENV_DIR..."

VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    ok "Created virtual environment"
else
    ok "Virtual environment already exists"
fi

# Pinned dependency versions (commit hashes)
# Update these when upgrading — run tests after changing
HATEOAS_AGENT_PIN="5d272d5aad1cd19ce9ac43628f98dd264bd372ca"  # 2026-03-11
SIGMA_MEM_PIN="d45cbabd667d8ec6daea95332099d4b82ce73882"      # 2026-03-12 (CI fix + P[] block recognition)

# Track installed pins to detect when upgrade needed
PIN_FILE="$VENV_DIR/.pinned-versions"

# Install/upgrade hateoas-agent
info "Installing hateoas-agent (pinned: ${HATEOAS_AGENT_PIN:0:7})..."
INSTALLED_HA_PIN=$(grep "^hateoas-agent=" "$PIN_FILE" 2>/dev/null | cut -d= -f2 || echo "")
if "$VENV_PYTHON" -c "import hateoas_agent" &>/dev/null && [ "$INSTALLED_HA_PIN" = "$HATEOAS_AGENT_PIN" ]; then
    ok "hateoas-agent already installed at pinned version"
else
    "$VENV_PIP" install --force-reinstall "git+https://github.com/coloradored13/hateoas-agent.git@${HATEOAS_AGENT_PIN}" --quiet
    ok "hateoas-agent installed (${HATEOAS_AGENT_PIN:0:7})"
fi

# Install/upgrade sigma-mem
info "Installing sigma-mem (pinned: ${SIGMA_MEM_PIN:0:7})..."
INSTALLED_SM_PIN=$(grep "^sigma-mem=" "$PIN_FILE" 2>/dev/null | cut -d= -f2 || echo "")
if "$VENV_PYTHON" -c "import sigma_mem" &>/dev/null && [ "$INSTALLED_SM_PIN" = "$SIGMA_MEM_PIN" ]; then
    ok "sigma-mem already installed at pinned version"
else
    "$VENV_PIP" install --force-reinstall "git+https://github.com/coloradored13/sigma-mem.git@${SIGMA_MEM_PIN}" --quiet
    ok "sigma-mem installed (${SIGMA_MEM_PIN:0:7})"
fi

# Record installed pins
cat > "$PIN_FILE" <<PINS
hateoas-agent=$HATEOAS_AGENT_PIN
sigma-mem=$SIGMA_MEM_PIN
PINS

echo ""

# ─────────────────────────────────────────────
# 4. Copy agent definitions
# ─────────────────────────────────────────────
info "Setting up agent definitions in $AGENTS_DIR..."

mkdir -p "$AGENTS_DIR"

SRC_AGENTS="$SCRIPT_DIR/agent-infrastructure/agents"

# Deploy all .md files from repo (dynamic — no hardcoded list)
for src in "$SRC_AGENTS"/*.md; do
    file=$(basename "$src")
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
# 5. Copy skills
# ─────────────────────────────────────────────
info "Setting up skills in $CLAUDE_DIR/skills/..."

SKILLS_DIR="$CLAUDE_DIR/skills"
SRC_SKILLS="$SCRIPT_DIR/agent-infrastructure/skills"

if [ -d "$SRC_SKILLS" ]; then
    for skill_dir in "$SRC_SKILLS"/*/; do
        skill_name=$(basename "$skill_dir")
        src="$skill_dir/SKILL.md"
        dest_dir="$SKILLS_DIR/$skill_name"
        dest="$dest_dir/SKILL.md"

        if [ ! -f "$src" ]; then
            continue
        fi

        mkdir -p "$dest_dir"

        if [ -f "$dest" ]; then
            if cmp -s "$src" "$dest"; then
                ok "$skill_name skill already up to date"
            else
                warn "$skill_name skill already exists with different content"
                read -rp "  Overwrite? (y/N): " overwrite
                if [[ "$overwrite" =~ ^[Yy]$ ]]; then
                    cp "$src" "$dest"
                    ok "$skill_name skill updated"
                else
                    info "Keeping existing $skill_name skill"
                fi
            fi
        else
            cp "$src" "$dest"
            ok "$skill_name skill installed"
        fi
    done
else
    warn "Skills source directory not found at $SRC_SKILLS — skipping"
fi

echo ""

# ─────────────────────────────────────────────
# 6. Create team directory structure
# ─────────────────────────────────────────────
info "Setting up team directory at $TEAMS_DIR..."

mkdir -p "$TEAMS_DIR/shared"
mkdir -p "$TEAMS_DIR/shared/debates"
mkdir -p "$TEAMS_DIR/inboxes"

# Create agent dirs and inboxes dynamically from repo agent files
for src in "$SRC_AGENTS"/*.md; do
    agent=$(basename "$src" .md)
    # Skip protocol/template files — only create dirs for actual agents
    case "$agent" in
        sigma-lead|sigma-comm|SIGMA-COMM-SPEC|_template) continue ;;
    esac
    mkdir -p "$TEAMS_DIR/agents/$agent"
done

# --- shared files from repo (roster, directives, protocols) ---
SRC_SHARED="$SCRIPT_DIR/agent-infrastructure/teams/sigma-review/shared"
for shared_file in roster.md directives.md protocols.md; do
    src="$SRC_SHARED/$shared_file"
    dest="$TEAMS_DIR/shared/$shared_file"
    if [ ! -f "$src" ]; then
        warn "Source $shared_file not found in repo — skipping"
        continue
    fi
    if [ ! -f "$dest" ]; then
        cp "$src" "$dest"
        ok "Created $shared_file"
    elif cmp -s "$src" "$dest"; then
        ok "$shared_file already up to date"
    else
        warn "$shared_file differs from repo"
        read -rp "  Overwrite with repo version? (y/N): " overwrite
        if [[ "$overwrite" =~ ^[Yy]$ ]]; then
            cp "$src" "$dest"
            ok "$shared_file updated"
        else
            info "Keeping existing $shared_file"
        fi
    fi
done

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

# --- shared/portfolio.md ---
PORTFOLIO="$TEAMS_DIR/shared/portfolio.md"
if [ ! -f "$PORTFOLIO" ]; then
    cat > "$PORTFOLIO" << 'PORTFOLIO_EOF'
# portfolio — projects reviewed
PORTFOLIO_EOF
    ok "Created portfolio.md"
else
    ok "portfolio.md already exists"
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

# --- Agent memory and inbox files (dynamic from repo agent files) ---
for src in "$SRC_AGENTS"/*.md; do
    agent=$(basename "$src" .md)
    case "$agent" in
        sigma-lead|sigma-comm|SIGMA-COMM-SPEC|_template) continue ;;
    esac

    MEMORY="$TEAMS_DIR/agents/$agent/memory.md"
    if [ ! -f "$MEMORY" ]; then
        cat > "$MEMORY" << MEMORY_EOF
# $agent — personal memory
MEMORY_EOF
        ok "Created $agent/memory.md"
    fi

    INBOX="$TEAMS_DIR/inboxes/$agent.md"
    if [ ! -f "$INBOX" ]; then
        cat > "$INBOX" << INBOX_EOF
# inbox — $agent

## processed

## unread
INBOX_EOF
        ok "Created $agent inbox"
    fi
done

echo ""

# ─────────────────────────────────────────────
# 7. Configure MCP server in ~/.claude.json
# ─────────────────────────────────────────────
info "Configuring sigma-mem MCP server in $CLAUDE_JSON..."

# Verify sigma-mem is importable in the venv
if ! "$VENV_PYTHON" -c "import sigma_mem" &>/dev/null; then
    warn "Could not locate sigma_mem in venv. MCP config skipped — see SETUP.md for manual instructions."
else
    if [ -f "$CLAUDE_JSON" ]; then
        # Check if sigma-mem is already configured with the correct venv path
        if python3 -c "
import json, sys
with open('$CLAUDE_JSON') as f:
    data = json.load(f)
servers = data.get('mcpServers', {})
sm = servers.get('sigma-mem', {})
if sm.get('command') == '$VENV_PYTHON':
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
            ok "sigma-mem MCP server already configured"
        else
            # Merge sigma-mem into existing config (or update existing entry)
            python3 -c "
import json
with open('$CLAUDE_JSON') as f:
    data = json.load(f)
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['sigma-mem'] = {
    'command': '$VENV_PYTHON',
    'args': ['-m', 'sigma_mem.server']
}
with open('$CLAUDE_JSON', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
"
            ok "Added sigma-mem MCP server to $CLAUDE_JSON (using venv Python)"
        fi
    else
        # Create new .claude.json with just the MCP config
        python3 -c "
import json
data = {
    'mcpServers': {
        'sigma-mem': {
            'command': '$VENV_PYTHON',
            'args': ['-m', 'sigma_mem.server']
        }
    }
}
with open('$CLAUDE_JSON', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
"
        ok "Created $CLAUDE_JSON with sigma-mem MCP server"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 8. Enable native Agent Teams in settings.json
# ─────────────────────────────────────────────
info "Enabling native Agent Teams in $CLAUDE_DIR/settings.json..."

SETTINGS_JSON="$CLAUDE_DIR/settings.json"

if [ -f "$SETTINGS_JSON" ]; then
    if python3 -c "
import json, sys
with open('$SETTINGS_JSON') as f:
    data = json.load(f)
env = data.get('env', {})
if env.get('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS') == '1':
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        ok "Agent Teams already enabled"
    else
        python3 -c "
import json
with open('$SETTINGS_JSON') as f:
    data = json.load(f)
if 'env' not in data:
    data['env'] = {}
data['env']['CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS'] = '1'
with open('$SETTINGS_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
        ok "Enabled Agent Teams in $SETTINGS_JSON"
    fi
else
    python3 -c "
import json
data = {
    'env': {
        'CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS': '1'
    }
}
with open('$SETTINGS_JSON', 'w') as f:
    json.dump(data, f, indent=2)
"
    ok "Created $SETTINGS_JSON with Agent Teams enabled"
fi

echo ""

# ─────────────────────────────────────────────
# 9. Append recall-first instructions to ~/.claude/CLAUDE.md
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
# 10. Run sigma-mem tests to verify installation
# ─────────────────────────────────────────────
info "Verifying installation by running sigma-mem tests..."

# Ensure pytest is available in the venv
"$VENV_PIP" install pytest --quiet 2>/dev/null

SIGMA_MEM_PKG_DIR=$("$VENV_PYTHON" -c "import sigma_mem, os; print(os.path.dirname(os.path.dirname(os.path.dirname(sigma_mem.__file__))))" 2>/dev/null || echo "")

if [ -n "$SIGMA_MEM_PKG_DIR" ] && [ -d "$SIGMA_MEM_PKG_DIR/tests" ]; then
    if "$VENV_PYTHON" -m pytest "$SIGMA_MEM_PKG_DIR/tests" --quiet --tb=short 2>/dev/null; then
        ok "All sigma-mem tests passed"
    else
        warn "Some sigma-mem tests failed. This may be expected if memory files haven't been initialized yet."
        warn "Run '$VENV_PYTHON -m pytest' in the sigma-mem directory to debug."
    fi
else
    # Try running tests from the submodule if available
    if [ -d "$SCRIPT_DIR/sigma-mem/tests" ]; then
        if "$VENV_PYTHON" -m pytest "$SCRIPT_DIR/sigma-mem/tests" --quiet --tb=short 2>/dev/null; then
            ok "All sigma-mem tests passed (from submodule)"
        else
            warn "Some sigma-mem tests failed. Run '$VENV_PYTHON -m pytest sigma-mem/tests' to debug."
        fi
    else
        warn "Could not locate sigma-mem tests. Verify manually: $VENV_PYTHON -c 'import sigma_mem; print(\"OK\")'"
    fi
fi

echo ""

# ─────────────────────────────────────────────
# 11. Success message
# ─────────────────────────────────────────────
echo "============================================"
echo -e "${GREEN}  Sigma System setup complete!${NC}"
echo "============================================"
echo ""
echo "What was installed:"
echo "  - Python venv at ~/.claude/sigma-venv/"
echo "  - hateoas-agent (in venv)"
echo "  - sigma-mem (in venv, MCP server)"
echo "  - Agent definitions in ~/.claude/agents/"
echo "  - Skills in ~/.claude/skills/ (sigma-review, sigma-init, sigma-research)"
echo "  - Team structure in ~/.claude/teams/sigma-review/"
echo "  - MCP config in ~/.claude.json (using venv Python)"
echo "  - Native Agent Teams enabled in ~/.claude/settings.json"
echo "  - Recall-first instructions in ~/.claude/CLAUDE.md"
echo ""
echo "Next steps:"
echo "  1. In any project, run /sigma-init to set up project-local teams:"
echo "     cd /path/to/your/project && claude"
echo "     /sigma-init My awesome project"
echo ""
echo "  2. Or manually: $SCRIPT_DIR/setup-project.sh"
echo ""
echo "  3. Available skills (type / in Claude Code):"
echo "     /sigma-review <task>     — full multi-agent team review"
echo "     /sigma-init              — initialize sigma-review for a project"
echo "     /sigma-research [agent]  — refresh agent domain research"
echo ""
echo "  4. After reviews create new agents or modify existing ones:"
echo "     ./setup.sh pull          — import changes from installed → repo"
echo ""
echo "Note: setup-project.sh is optional. Without it, all data lives in"
echo "~/.claude/teams/ (single-tier, backward compatible)."
echo ""
echo "For more details, see SETUP.md in this repository."
echo ""
