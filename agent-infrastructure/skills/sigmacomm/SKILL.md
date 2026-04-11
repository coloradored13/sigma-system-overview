---
name: sigmacomm
description: >
  ΣComm compressed notation protocol for AI-read content. ALWAYS load this skill
  before reading or writing CLAUDE.md, memory/ files, agent-to-agent messages,
  or workspace findings. Teaches the notation so you can decode existing memory
  entries and write new ones correctly. Triggers on: any memory read/write,
  memory-compiler output, persistent-wiki updates, sigma-dream consolidation,
  or any task where you need to read/write compressed agent notation.
  Do NOT apply ΣComm to user-facing output — that stays plain English.
---

# ΣComm — Compressed Notation Protocol

ΣComm saves tokens in AI-read content: memory files, agent messages, workspace
findings. **Never use ΣComm in user-facing output** — humans get plain English.

## When to Use

| Content | Format | Why |
|---------|--------|-----|
| CLAUDE.md (hot cache) | ΣComm | Read every session start |
| memory/ files | ΣComm | Agent-read reference |
| Agent-to-agent messages | ΣComm | High-frequency, agent-read |
| Workspace findings | ΣComm | Agent-written, agent-read |
| wiki/ entries | **Plain English** | Human reference docs |
| User-facing output | **Plain English** | Humans read this |

**The test**: Will an AI agent read this during a task? → ΣComm.
Will a human read this? → Plain English.

---

## Message Format

```
[STATUS] BODY |¬ ruled-out |→ actions |#count
```

### Status Codes

| Code | Meaning |
|------|---------|
| ✓ | Done / complete |
| ◌ | In progress |
| ! | Blocked or critical |
| ? | Needs input |
| ✗ | Failed |
| ↻ | Retry |

### Body Notation

| Symbol | Meaning | Example |
|--------|---------|---------|
| `\|` | Section separator | `finding-A \| finding-B` |
| `,` | Item separator | `item1, item2, item3` |
| `>` | Preference / "over" | `honest>polish` |
| `→` | Leads to / next action | `fix-bug → retest` |
| `+` | And | `auth + logging` |
| `!` | Critical | `jwt-expiry(!)` |
| `@` | At / time / location | `proj@21-02` |
| `^` | File reference | `^projects.md` |

### Three Mandatory Sections (when applicable)

1. **`¬` (NOT)** — What was explicitly ruled out. Prevents wrong assumptions.
2. **`→` (Actions)** — Available next steps (HATEOAS-inspired).
3. **`#N` (Count)** — Checksum of items so reader can verify decode.

### Full Example

```
✓ auth-review: jwt-expiry-no-validate(!), pwd-md5>bcrypt, no-rate-limit-login |¬ session-mgmt, cors |→ fix-jwt(small), fix-hash(needs-db-migration), add-rate-limit(small) |#3
```

Reading: Review done. 3 findings: JWT expiry not validated (critical), passwords
should use bcrypt not MD5, no rate limiting on login. Session management and CORS
are fine. Three available actions with effort estimates.

---

## Memory Entry Types

| Prefix | What It Stores | Example |
|--------|---------------|---------|
| `C[]` | Calibration — behavioral observation | `C[detects perf, honest>polish\|3\|26.3]` |
| `C~[]` | Tentative calibration — observed once | `C~[prefers-TDD]` |
| `R[]` | Research — domain finding with source + date | `R[api-latency-p99=120ms\|src:grafana\|26.4.1]` |
| `P[]` | Pattern — recurring observation promoted from findings | `P[distribution>technology-for-finserv-moat]` |
| `F[]` | Finding — specific review/analysis result | `F[26.3.12] r1: 10 findings(4H,2MH,4M)` |
| `¬[]` | Anti-memory — something explicitly NOT true | `¬[developer(leader learning to build)]` |
| `D[]` | Decision — recorded choice with rationale | `D[build-sequence]: waterfall+distribution=STAGGERED` |

## Section Prefixes

| Prefix | Domain |
|--------|--------|
| `U` | User profile |
| `X` | Preferences |
| `P` | Project |
| `C` | Calibration |
| `S` | Self-awareness |
| `Λ` | Meta-cognition |
| `R` | Research / heuristics |
| `L` | Lessons learned |
| `T` | Tech reference |
| `H` | History |
| `D` | Decisions |

## Confidence & Dates

| Marker | Meaning |
|--------|---------|
| `~` | Tentative — single observation, needs confirmation |
| *(none)* | Confirmed — multiple sessions/sources |

Dates: `YY.M.D` → `26.4.10` = April 10, 2026
Counts: `\|N\|YY.M` → `\|3\|26.3` = observed 3 times since March 2026

---

## Anti-Memory (`¬`)

Anti-memories record what is explicitly NOT true to prevent wrong assumptions.

```
¬[developer(leader learning to build)]
```

This means: "Do NOT assume this person is a developer. They are a leader who is
learning to build." Without this, an AI might see coding activity and incorrectly
categorize the user.

Anti-memories are especially valuable for:
- Correcting natural assumptions (`¬[wants code handed over]` → they want to learn)
- Recording ruled-out hypotheses (`¬ session-mgmt, cors` → checked and fine)
- Preventing regression after corrections

---

## Writing Rules

1. **Compress but don't lose meaning.**
   Good: `C[detects perf, honest>polish|3|26.3]`
   Bad: `C[dp,h>p|3|26.3]` (unreadable)
   Bad: `C[The user detects performative responses...]` (too verbose)

2. **Always include ¬ when you've ruled something out.** Future reads need
   to know what was checked.

3. **Include sources and dates on research entries.**
   `R[topic|finding|src:name|refreshed:YY.M.D]`

4. **Use count fields for calibration confidence.**
   `|3|26.3` = observed 3 times since March 2026.

5. **Use ~ for first observations.** Promote after second confirmation.

---

## Quick Reference Card

```
STATUS:  ✓=done  ◌=progress  !=blocked  ?=need-input  ✗=failed  ↻=retry
BODY:    |=sep  ,=items  >=pref  →=next  +=and  !=critical  @=at  ^=file
SECTIONS: ¬=NOT(ruled-out)  →=actions(next-steps)  #N=count(checksum)
ENTRIES: C[]=calibration  R[]=research  P[]=pattern  F[]=finding  ¬[]=anti-memory  D[]=decision
CONFIDENCE: ~=tentative  (none)=confirmed
DATES:   YY.M.D format (26.3.14 = March 14, 2026)
COUNTS:  |N| = observation count  |N|YY.M = count since date
```

---

## Practice (verify your decode)

```
✓ loan-admin-review: 10 findings(3H,4MH,3M) |¬ critical-errors |→ ready-for-DA-challenge |#10
```
→ Review complete. 10 findings (3 high, 4 medium-high, 3 medium). No critical
errors. Ready for devil's advocate challenge. Verify: 10 findings.

```
C[honest>polish, probes, detects-perf|5|26.3]
```
→ Calibration: user prefers honesty over polish, tends to probe, detects
performative responses. Observed 5 times since March 2026. Confirmed.

```
D[skill-arch]: capability/domain>role-based | 3-tier |¬ role-based-org |26.4.10
```
→ Decision: skill architecture uses capability/domain over role-based.
Three-tier system. Role-based organization was explicitly rejected. April 10, 2026.

```
R[PC-AUM:$3-3.5T(broad)|src:AIMA,Morgan-Stanley|refreshed:26.4]
```
→ Research: Private credit AUM is $3-3.5 trillion broadly measured. Sources: AIMA
and Morgan Stanley. Last refreshed April 2026.
