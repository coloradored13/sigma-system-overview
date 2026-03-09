# Sigma System Setup Guide

This guide covers installing and configuring the full Sigma System: persistent AI agent teams with deterministic tool discovery, compressed communication, and HATEOAS-navigated memory.

## Quick Start

```bash
git clone --recurse-submodules https://github.com/coloradored13/sigma-system-overview.git
cd sigma-system-overview
chmod +x setup.sh
./setup.sh
```

The setup script is idempotent — safe to run multiple times without duplicating files or configs.

> **Sharing via zip?** GitHub's "Download ZIP" button does NOT include submodule contents. Use `./make-release.sh` to create a proper zip with all files included.

## What Gets Installed

### Python Packages

| Package | Source | Purpose |
|---------|--------|---------|
| `hateoas-agent` | `pip install git+https://github.com/coloradored13/hateoas-agent.git` | HATEOAS framework for AI agent tool use |
| `sigma-mem` | `pip install git+https://github.com/coloradored13/sigma-mem.git` | Persistent memory MCP server (built on hateoas-agent) |

### Files Created

```
~/.claude/
  CLAUDE.md                           # Recall-first instructions (appended, not overwritten)
  agents/
    sigma-lead.md                     # Team orchestrator protocol
    sigma-comm.md                     # Communication protocol (agent-facing)
    SIGMA-COMM-SPEC.md                # Full protocol specification
    tech-architect.md                 # Agent definition: architecture specialist
    product-strategist.md             # Agent definition: product/shipping specialist
    ux-researcher.md                  # Agent definition: developer experience specialist
    code-quality-analyst.md           # Agent definition: code quality specialist
    technical-writer.md               # Agent definition: documentation specialist
  teams/sigma-review/
    shared/
      roster.md                       # Team roster with domains and wake-for rules
      decisions.md                    # Expertise-weighted team decisions (starts empty)
      patterns.md                     # Cross-agent observations (starts empty)
      workspace.md                    # Current task workspace (starts idle)
    agents/
      tech-architect/memory.md        # Personal memory (starts empty)
      product-strategist/memory.md    # Personal memory (starts empty)
      ux-researcher/memory.md         # Personal memory (starts empty)
      code-quality-analyst/memory.md  # Personal memory (starts empty)
      technical-writer/memory.md      # Personal memory (starts empty)
    inboxes/
      tech-architect.md               # Inbox with processed/unread sections
      product-strategist.md           # Inbox with processed/unread sections
      ux-researcher.md                # Inbox with processed/unread sections
      code-quality-analyst.md         # Inbox with processed/unread sections
      technical-writer.md             # Inbox with processed/unread sections

~/.claude.json                        # MCP server config (merged with existing)
~/.claude/settings.json               # Native Agent Teams enabled
```

### MCP Server Config

The script adds a `sigma-mem` entry to the `mcpServers` section of `~/.claude.json`:

```json
{
  "mcpServers": {
    "sigma-mem": {
      "command": "/path/to/python3",
      "args": ["-m", "sigma_mem.server"]
    }
  }
}
```

The `command` path is detected automatically from whichever `python3` has `sigma-mem` installed.

### CLAUDE.md Instructions

The script appends recall-first behavior instructions to `~/.claude/CLAUDE.md`. These tell Claude to:
- Call `mcp__sigma-mem__recall` at the start of every conversation
- Use sigma-mem MCP actions for storing memories instead of writing files directly
- Use compressed notation (pipe-separated fields, checksums, dates as YY.M.D)

### Native Agent Teams

The script enables Claude Code's experimental native Agent Teams by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `~/.claude/settings.json`. This allows agents to run in true parallel with built-in messaging and task coordination, rather than being orchestrated sequentially.

> **Note**: Native Agent Teams is experimental (as of March 2026). Token usage is ~3-7x higher than sequential orchestration due to parallel context windows. Start with 2-agent teams to calibrate costs.

---

## Manual Setup

If you prefer not to run the script, follow these steps:

### 1. Install Python packages

```bash
pip install git+https://github.com/coloradored13/hateoas-agent.git
pip install git+https://github.com/coloradored13/sigma-mem.git
```

### 2. Copy agent definitions

```bash
mkdir -p ~/.claude/agents

cp agent-infrastructure/agents/sigma-lead.md ~/.claude/agents/
cp agent-infrastructure/agents/sigma-comm.md ~/.claude/agents/
cp agent-infrastructure/agents/SIGMA-COMM-SPEC.md ~/.claude/agents/
cp agent-infrastructure/agents/tech-architect.md ~/.claude/agents/
cp agent-infrastructure/agents/product-strategist.md ~/.claude/agents/
cp agent-infrastructure/agents/ux-researcher.md ~/.claude/agents/
cp agent-infrastructure/agents/code-quality-analyst.md ~/.claude/agents/
cp agent-infrastructure/agents/technical-writer.md ~/.claude/agents/
```

### 3. Create team directory structure

```bash
mkdir -p ~/.claude/teams/sigma-review/shared
mkdir -p ~/.claude/teams/sigma-review/agents/{tech-architect,product-strategist,ux-researcher,code-quality-analyst,technical-writer}
mkdir -p ~/.claude/teams/sigma-review/inboxes
```

Create `~/.claude/teams/sigma-review/shared/roster.md`:
```
# sigma-review team roster

tech-architect |domain: architecture,security,performance,infra,api-design |wake-for: technical decisions,code review,system design,debugging
product-strategist |domain: market,growth,monetization,prioritization,user-segmentation |wake-for: feature decisions,positioning,launch readiness,competitive analysis
ux-researcher |domain: usability,accessibility,mental-models,information-architecture,learnability |wake-for: user-facing changes,flow design,dual-user questions,onboarding
code-quality-analyst |domain: code-quality,test-coverage,style-consistency,dead-code,edge-cases |wake-for: code review,test analysis,quality audit,style check
technical-writer |domain: documentation,narrative,examples,onboarding,cross-doc-consistency |wake-for: documentation review,readme,setup docs,api docs,writing quality

→ actions:
→ adding a new agent → append to roster with domain+wake-for
→ checking who to wake → match task keywords against wake-for fields
→ team decision needed → route to agent whose domain matches topic
```

Create `~/.claude/teams/sigma-review/shared/decisions.md`:
```
# team decisions — expertise-weighted
```

Create `~/.claude/teams/sigma-review/shared/patterns.md`:
```
# cross-agent patterns
```

Create `~/.claude/teams/sigma-review/shared/workspace.md`:
```
# workspace

## status: idle

## task
```

Create inbox files for each agent (`~/.claude/teams/sigma-review/inboxes/{agent-name}.md`):
```
# inbox — {agent-name}

## processed

## unread
```

Create empty memory files for each agent (`~/.claude/teams/sigma-review/agents/{agent-name}/memory.md`):
```
# {agent-name} — personal memory
```

### 4. Configure MCP server

Edit `~/.claude.json` (create if it doesn't exist). Add or merge the `mcpServers` section:

```json
{
  "mcpServers": {
    "sigma-mem": {
      "command": "/path/to/your/python3",
      "args": ["-m", "sigma_mem.server"]
    }
  }
}
```

Find your Python path with: `which python3`

Make sure this is the Python where you installed sigma-mem. You can verify with:
```bash
python3 -c "import sigma_mem; print('OK')"
```

### 5. Enable native Agent Teams

Create or update `~/.claude/settings.json` to enable native Agent Teams:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

If the file already exists, merge the `env` key — do not overwrite other settings.

### 6. Add recall-first instructions

Append the following to `~/.claude/CLAUDE.md` (create if it doesn't exist):

```
# Sigma System — recall-first behavior

Always start conversations by calling mcp__sigma-mem__recall before reading memory files directly. Use its actions (search_memory, get_project, etc.) to go deeper when needed.

When storing memories, use the sigma-mem MCP actions (store_memory, log_decision, log_correction, log_failure) rather than writing files directly. Match the compressed notation format you see in the recall response — pipe-separated fields, checksums, dates as YY.M.D. See rosetta.md (via recall → decode notation) if unsure about notation.
```

---

## Verification

### Quick check

```bash
python3 -c "import hateoas_agent; print('hateoas-agent OK')"
python3 -c "import sigma_mem; print('sigma-mem OK')"
```

### Run sigma-mem tests

```bash
# From the cloned repo (with submodules)
python3 -m pytest sigma-mem/tests --quiet

# Or from the installed package
python3 -m pytest $(python3 -c "import sigma_mem, os; print(os.path.dirname(os.path.dirname(os.path.dirname(sigma_mem.__file__))))")/tests --quiet
```

### Test MCP server

Open Claude Code in any project directory. Claude should:
1. Call `recall` at the start of the conversation
2. Show core memory and navigation hints in its first response
3. Have access to actions like `search_memory`, `store_memory`, `get_project`, etc.

You can also test by asking Claude: "What do you remember about me?"

### Verify file structure

```bash
ls ~/.claude/agents/sigma-lead.md
ls ~/.claude/teams/sigma-review/shared/roster.md
ls ~/.claude/teams/sigma-review/agents/  # Should show all 5 agent directories
cat ~/.claude.json | python3 -m json.tool | grep sigma-mem
cat ~/.claude/settings.json | python3 -m json.tool | grep AGENT_TEAMS
```

---

## Customization

### Adding a new agent

1. Create an agent definition at `~/.claude/agents/{agent-name}.md`. Follow the pattern in existing agent files (role, domain expertise, behavioral rules).

2. Add the agent to the team roster at `~/.claude/teams/sigma-review/shared/roster.md`:
   ```
   {agent-name} |domain: your,domains,here |wake-for: matching,task,keywords
   ```

3. Create the agent's directory and files:
   ```bash
   mkdir -p ~/.claude/teams/sigma-review/agents/{agent-name}
   echo "# {agent-name} — personal memory" > ~/.claude/teams/sigma-review/agents/{agent-name}/memory.md
   printf "# inbox — {agent-name}\n\n## processed\n\n## unread\n" > ~/.claude/teams/sigma-review/inboxes/{agent-name}.md
   ```

### Creating a new team

Teams are instances of agent collaboration. To create a new team:

```bash
TEAM="my-team"
mkdir -p ~/.claude/teams/$TEAM/{shared,agents,inboxes}
```

Then create the same starter files (roster.md, decisions.md, patterns.md, workspace.md) with your chosen agents.

### Modifying CLAUDE.md

`~/.claude/CLAUDE.md` is your global instruction file for Claude Code. The Sigma System adds recall-first behavior, but you can add any other instructions. Common additions:

- Project-specific memory cues
- Preferred coding style
- Custom behavioral rules

The sigma-mem system will pick up whatever is in `CLAUDE.md` and return it through the recall mechanism.

### Changing the MCP server command

If you use a virtual environment or a specific Python installation, update the `command` path in `~/.claude.json`:

```json
{
  "mcpServers": {
    "sigma-mem": {
      "command": "/path/to/venv/bin/python3",
      "args": ["-m", "sigma_mem.server"]
    }
  }
}
```

Alternatively, if you have `uvx` installed and sigma-mem is published:
```json
{
  "mcpServers": {
    "sigma-mem": {
      "command": "uvx",
      "args": ["sigma-mem"]
    }
  }
}
```

---

## Uninstall

### Remove Python packages

```bash
pip uninstall sigma-mem hateoas-agent
```

### Remove agent definitions

```bash
rm ~/.claude/agents/sigma-lead.md
rm ~/.claude/agents/sigma-comm.md
rm ~/.claude/agents/SIGMA-COMM-SPEC.md
rm ~/.claude/agents/tech-architect.md
rm ~/.claude/agents/product-strategist.md
rm ~/.claude/agents/ux-researcher.md
rm ~/.claude/agents/code-quality-analyst.md
rm ~/.claude/agents/technical-writer.md
```

### Remove team data

```bash
rm -rf ~/.claude/teams/sigma-review
```

### Remove MCP config

Edit `~/.claude.json` and remove the `"sigma-mem"` entry from the `"mcpServers"` section.

### Remove recall-first instructions

Edit `~/.claude/CLAUDE.md` and remove everything from `# Sigma System — recall-first behavior` to the end of that section.

---

## Troubleshooting

### "sigma_mem module not found"

The MCP server config in `~/.claude.json` points to a specific Python binary. Make sure that binary has sigma-mem installed:

```bash
/path/to/python3 -c "import sigma_mem; print('OK')"
```

If you installed sigma-mem in a virtual environment, the `command` in `~/.claude.json` must point to that venv's Python.

### "recall returns empty"

sigma-mem reads memory from `~/.claude/memory/`. On first use, this directory won't exist — the system will initialize it. If you previously had Claude Code memory files, sigma-mem will pick those up automatically.

### MCP server not connecting

1. Verify the config: `cat ~/.claude.json | python3 -m json.tool`
2. Test the server directly: `python3 -m sigma_mem.server`
3. Restart Claude Code after config changes

### Tests fail on fresh install

Some sigma-mem tests expect memory files to exist. The core tests should pass on a clean install. If memory-dependent tests fail, that is expected — they will pass once you have used the system and memory files have been created.

### Agent not waking during team reviews

Check the roster at `~/.claude/teams/sigma-review/shared/roster.md`. The `wake-for` field controls which keywords trigger each agent. If your task description doesn't match any wake-for keywords, the agent won't be selected.

---

## Prerequisites Reference

| Requirement | Minimum Version | Check Command |
|-------------|----------------|---------------|
| Python | 3.10+ | `python3 --version` |
| pip | any | `python3 -m pip --version` |
| Claude Code CLI | any | `claude --version` |
| Git | any | `git --version` |
