---
name: persistent-wiki
description: >
  Compile findings from a session into the persistent local wiki (06b compilation
  pattern). Trigger after substantive tasks — research, analysis, reviews, or any
  session that produced reusable knowledge. Triggers include: 'save this to the wiki',
  'compile this', 'add to wiki', 'persist this', 'log this decision', or when
  memory-compiler fires and identifies wiki-worthy content (domain knowledge, research
  findings, decision rationale). Do NOT fire for trivial tasks or pure conversation.
  Do NOT duplicate what memory-compiler handles (behavioral preferences, corrections,
  shorthand). Memory-compiler handles what changes Claude's behavior; persistent-wiki
  handles what a human would look up later.
---

# Persistent Wiki — 06b Compilation

Convert session outputs into persistent, searchable wiki entries.

## The Boundary

| Content Type | Goes To | Why |
|---|---|---|
| Behavioral preferences, corrections, shorthand | **memory-compiler** → CLAUDE.md / memory/ | Changes how Claude responds |
| Domain knowledge, research findings, decision logs | **persistent-wiki** → wiki/ | Human-readable reference for later lookup |

These skills don't overlap if the boundary is respected. memory-compiler fires first
(end of session) for behavioral edits. persistent-wiki fires for domain/decision content.

## Wiki Location

The wiki lives at `wiki/` relative to the project root. Standard structure:

```
wiki/
├── INDEX.md          ← Master page listing all entries
├── decisions/        ← Strategic choices with rationale
│   └── {decision}.md
├── domains/          ← Domain knowledge, research findings
│   └── {topic}.md
└── digests/          ← Weekly/periodic consolidation summaries
    └── YYYY-WNN.md
```

## When to Fire

After a session that produced **reusable knowledge** — not just completed a task.

| Signal | Wiki-Worthy | Entry Type |
|---|---|---|
| **Research completed** | Competitor analysis, market research, account research | `domains/{topic}.md` |
| **Strategic decision** | Architecture choice, market positioning, go/no-go | `decisions/{decision}.md` |
| **Domain deep-dive** | Loan admin mechanics, GAAP standards, bioinformatics protocols | `domains/{topic}.md` |
| **Framework created** | Evaluation criteria, scoring rubric, decision matrix | `domains/{framework}.md` |
| **Tool/skill built** | New skill, workflow, integration | `decisions/{what-was-built}.md` |

**Not wiki-worthy:**
- Routine task completion (wrote an email, formatted a doc)
- Behavioral preferences (→ memory edits instead)
- Test/QA sessions
- Conversations that rehashed existing knowledge

## How to Offer

At a natural stopping point, if the session produced wiki-worthy content:

> 📚 **This session produced some reusable knowledge:**
> - [finding/decision 1]
> - [finding/decision 2]
>
> Want me to compile these into the wiki?

## If the User Says Yes

### Step 1: Classify and Route

For each item, determine:
- **Entry type:** `decisions/` or `domains/`
- **File name:** kebab-case, descriptive (e.g., `competitor-alter-domus.md`, `gaap-revenue-recognition.md`)
- **New file or update?** Check if a wiki page already exists for this topic.

### Step 2: Draft the Entry

**For domain knowledge (`domains/`):**

```markdown
# {Topic Title}

**Last updated:** YYYY-MM-DD [{session context}]

## Summary
[2-3 sentence overview]

## Key Findings
- [finding with source attribution]
- [finding with source attribution]

## Details
[Substantive content — dense reference material, not narrative]

## Open Questions
- [what we don't know yet]

## Sources
- [{session type}, YYYY-MM-DD] — {what was established}
- [Web research, T1/T2/T3] — {source name}
```

**For decisions (`decisions/`):**

```markdown
# {Decision Title}

**Decided:** YYYY-MM-DD [{session context}]

## Decision
[What was decided — one clear statement]

## Rationale
[Why this choice over alternatives]

## Alternatives Considered
- [Option A — why rejected]
- [Option B — why rejected]

## Implications
- [What this means going forward]

## Review Trigger
[When should this decision be revisited?]
```

### Step 3: Handle Conflicts

Before writing, check existing wiki entries for:

- **Existing page on same topic** → Update, don't duplicate. Add new findings with
  date attribution. If new findings contradict existing content:
  ```
  ⚠ CONFLICT: [session YYYY-MM-DD] found X, [session YYYY-MM-DD] found Y
  ```
- **Convergence** → Note when multiple sessions confirm the same finding:
  ```
  ✓ Confirmed: {finding} (sessions YYYY-MM-DD, YYYY-MM-DD)
  ```

### Step 4: Update INDEX.md

Add or update the page listing in `wiki/INDEX.md` under `## Pages`.

### Step 5: Present for Approval

Show the draft wiki entries. Ask: "These look right? Any to adjust or skip?"

Wait for confirmation before writing files.

## Compilation Principles

- **Preserve source attribution.** Always include session date and source tier.
- **Don't silently resolve contradictions.** Flag both sides. Let the user decide.
- **Separate domain from decisions.** Research findings go in `domains/`. Choices go
  in `decisions/`. A research session that led to a decision produces entries in both.
- **Compress, don't summarize.** Wiki entries are for looking things up, not for
  reading cover-to-cover. Dense > narrative.
- **Include open questions.** What we DON'T know is as important as what we do. It
  prevents false confidence and flags future research.
- **Wiki entries are plain English.** ΣComm is for memory files and agent messages.
  Wiki is human-readable reference material.

## Interaction with Other Skills

- **memory-compiler** fires first for behavioral/preference edits. persistent-wiki
  fires for domain/decision content. They don't overlap if the boundary is respected.
- **sigma-dream** (weekly consolidation) checks for wiki gaps — sessions that produced
  knowledge but didn't get compiled. The digest flags these as "Suggested Actions."
- **research-analysis** and **competitive-brief** are the most common upstream skills
  that produce wiki-worthy output.

## Gotchas

- **Don't wiki everything.** A quick email draft isn't worth a wiki entry. The bar is:
  "Would I want to find this 3 months from now?"
- **Keep entries self-contained.** Each wiki page should make sense without reading the
  session transcript. If you need context from the conversation to understand the
  entry, you haven't compressed enough.
- **Date entries, not just pages.** Individual findings within a page should have dates,
  not just the page header. Knowledge accumulates over time.
