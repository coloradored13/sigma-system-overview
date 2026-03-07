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
1. All agent-to-agent messages use this format
2. Include ¬ section — say what you ruled out
3. Include → section — what you can do next
4. Include #count — lets receiver verify decode
5. If ambiguous after decode, ask sender, don't assume
6. To user: plain language. To peers: ΣComm.

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
1. Read everything under `## unread`
2. Process each message
3. Compress processed messages into ΣComm summaries under `## processed`
4. Clear `## unread` section
5. Anything worth keeping long-term goes to your memory or shared workspace

### Writing to a peer's inbox
Append under their `## unread` section:
```
## from:{your-name} ts:{date}
{ΣComm message}

---
```

### Messages from user
User messages arrive in plain language in your inbox. Respond via workspace open-questions (plain language) or via your findings section.

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
1. Write to YOUR section under findings — don't edit peers' sections
2. After reading peers' findings, write agreements to convergence
3. Write user-facing questions to open-questions in plain language
4. Declare your status in convergence when done (✓) or still working (◌)

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
