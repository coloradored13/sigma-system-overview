---
name: memory-compiler
description: >
  Background awareness skill. Runs passively during all conversations.
  After sessions where key decisions were made, positions changed, new domain
  knowledge surfaced, or project direction shifted, offer to distill the session
  into memory edits. This is the 06b compilation pattern adapted for chat —
  converting conversation into persistent knowledge. Do NOT fire when nothing
  new was established. Do NOT fire more than once per conversation.
---

# Memory Compiler

Convert substantive conversations into persistent knowledge.

## When to Fire

At the end of a conversation (or at a natural stopping point), assess whether
the session produced anything worth persisting:

| Signal | Worth Persisting | Memory Edit Type |
|---|---|---|
| **Decision made** | "We decided to structure skills as capability/domain" | Decision + rationale |
| **Position changed** | User updated their view on something based on discussion | Updated belief or preference |
| **New domain knowledge** | Complex topic explored, frameworks established | Domain context |
| **Project milestone** | Significant progress on a project, new direction set | Project status |
| **Preference discovered** | User's working style, communication preference, or value surfaced naturally | Behavioral preference |
| **Skill/tool built** | New skill, tool, or framework created and delivered | What was built + key design decisions |
| **Correction** | User corrected a misunderstanding or factual error | Anti-pattern / "don't do X" |

**Do NOT fire when:**
- Nothing new was established (rehashing known territory)
- The session was a test/QA exercise (remember: test personas are not real)
- You already fired earlier in this conversation

## How to Offer

At a natural stopping point:

> 💾 **Session produced some worth-remembering decisions/knowledge:**
> - [key item 1]
> - [key item 2]
> - [key item 3]
>
> Want me to compile these into memory edits?

## If the User Says Yes

### Step 1: Draft Memory Edits

For each item, draft a concise memory edit (under 500 chars). Follow these rules:

- **Decisions:** Include the choice AND the rationale. "Brad decided X because Y" not just "Brad decided X."
- **Domain knowledge:** Compress to the essential insight. Don't persist the full explanation — persist the conclusion.
- **Preferences:** Frame as behavioral guidance. "Brad prefers X over Y when Z" not just "Brad likes X."
- **Corrections:** Frame as anti-patterns. "X is wrong because Y — correct answer is Z."
- **Project status:** Current state + key decision + what's next. Not a full project history.

### Step 2: Check for Conflicts

Before adding, check existing memory for:
- **Duplicates** — already captured from a previous session
- **Contradictions** — new knowledge conflicts with existing memory (update, don't stack)
- **Superseded info** — old memory that this new knowledge replaces (replace, don't just add)

### Step 3: Present for Approval

Show the draft edits. Ask: "These look right? Any to adjust or skip?"

Wait for confirmation before writing.

### Step 4: Execute

Use memory_user_edits tool to add/replace as approved.

## Compilation Principles (from sigma-review 06b)

- **Preserve source attribution.** "Decided during [session topic] on [date]" — not just the fact.
- **Don't silently resolve contradictions.** If new knowledge contradicts existing memory, flag both and let the user decide.
- **Separate domain knowledge from process observations.** "The loan admin market is $X" is domain knowledge. "We found that Tier 1 quick-refs are more useful than full docs" is process knowledge. Both are worth persisting but they're different types.
- **Compress, don't summarize.** Memory edits should be dense signals, not readable prose. The memory system is for recall, not for reading.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.**
2. **Trigger a rigorous web search.** Apply source tiers: T1 > T2 > T3.
3. **Flag the provenance.**
4. **Suggest a skill update if the gap is recurring.**

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
