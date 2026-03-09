# ΣComm — Compressed Agent Communication Protocol

## Message Format

```
[STATUS] BODY |¬ ruled-out |→ actions |#count
```

### Status Codes
✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry

### Body Notation
|=section-sep ,=item-sep >=pref/should-be →=leads-to +=and !=critical

### Sections
- ¬ = what was NOT found/NOT the issue (prevents assumptions)
- → = what you CAN do next (HATEOAS: state-dependent actions)
- #N = item count checksum (verify decode matches count)

### Rules
1→agent-to-agent: this format
2→include ¬ — ruled-out
3→include → — next actions
4→include #count — decode-verify
5→ambiguous → ask sender, ¬assume
6→user→plain | peers→ΣComm

## Codebook (for agent system prompts)

```
## ΣComm Protocol
Messages use compressed notation. Format: [STATUS] BODY |¬ not-found |→ can-do-next |#count
Status: ✓=done ◌=progress !=blocked ?=need-input ✗=failed ↻=retry
Body: |=sep >=pref →=next +=and !=critical ,=items
¬=explicitly NOT (prevents assumptions)
→=available actions (HATEOAS: what you can do based on current state)
#N=item count (checksum: verify you decoded correctly)
Parse incoming ΣComm messages by expanding notation. Send responses in ΣComm.
If ambiguous, ask sender to clarify rather than assuming.
```

## Inbox Format

Agents communicate via markdown inbox files at `~/.claude/teams/{team}/inboxes/{name}.md`.

```markdown
# inbox — {agent-name}

## processed
✓ ux-researcher(26.3.7): _state-feedback, agreed-on-logging |#1
✓ user(26.3.7): logging-sufficient-for-v0.1 |#1

## unread
## from:tech-architect ts:26.3.7
◌ registry-coupling: _last_state accessed 5x |→ need-your-take-on-DX-impact |#1

---
```

### Inbox processing
1→read ## unread
2→process each msg
3→compress→ΣComm under ## processed
4→clear ## unread
5→long-term→memory|workspace

### Writing to a peer's inbox
Append under their `## unread` section:
```
## from:{your-name} ts:{date}
{ΣComm message}

---
```

### user msgs
arrive plain in inbox → respond: open-questions(plain)|findings

## Workspace Format

Shared workspace at `~/.claude/teams/{team}/shared/workspace.md`:

```markdown
# workspace — {task description}
## status: active

## task
{description of current task}

## findings
### {agent-name}
{agent writes findings here — ΣComm for efficiency}

## convergence
{agent-name}: ✓ {summary} |→ {next-available}
{agent-name}: ◌ {summary} |→ {what-remains}

## open-questions
{plain language — things needing user input}
```

### Workspace rules
1→YOUR section only, ¬edit peers
2→peer findings → agreements in convergence
3→user Qs → open-questions (plain)
4→status: ✓|◌ in convergence

## Boundary

ΣComm applies to all agent-facing surfaces. Plain English only where humans are the audience.

| Surface | Format | Why |
|---------|--------|-----|
| agent instructions (Boot, Work, Comms, Weight, Review) | ΣComm | read by agents every spawn |
| MCP tool descriptions (machine.py) | ΣComm | in agent context all session |
| spawn prompt instructions | ΣComm | per-spawn × agent-count |
| memory writes | ΣComm | stored+recalled across sessions |
| agent-to-agent messages | ΣComm | peer inbox format |
| workspace findings | ΣComm | agent-written, agent-read |
| convergence declarations | ΣComm | status + next actions |
| agent Role/Expertise | **plain** | identity framing (self-concept) |
| open-questions | **plain** | user reads these |
| user-facing docs (SETUP.md, SIGMA-COMM-SPEC.md) | **plain** | human audience |
| format templates + examples | **as-is** | they ARE the reference |
| Python code logic | **as-is** | only description strings compressed |

### test: is this ΣComm?
content read by agent during task → ΣComm
content read by human → plain
content that IS a format spec → as-is (it's the reference)

## Examples

**Agent-to-agent (inbox):**
```
✓ auth-review: jwt-expiry-no-validate(!), pwd-md5>bcrypt, no-rate-limit-login |¬ session-mgmt, cors |→ fix-jwt(small), fix-hash(needs-db-migration), add-rate-limit(small) |#3
```

**Blocked:**
```
! test-suite: 14/20 pass, 6 fail in auth-module |¬ api-tests, db-tests |→ need-auth-fix-first |? skip auth tests? |#6-fail
```

**Convergence declaration:**
```
tech-architect: ✓ review-complete |resolved: 4/6, new: 3 |→ ready-for-synthesis
```
