---
name: passive-bootstrap
description: >
  Detailed reference for the five passive background behaviors. Firing rules are now
  in CLAUDE.md (Passive Behaviors section) and activate automatically every session.
  Load this skill only if you need the full detection signals, flagging formats,
  examples, or interaction rules beyond the distilled version in CLAUDE.md.
---

# Passive Skills Bootstrap

Load this once at conversation start. It activates four background behaviors that
run continuously without explicit triggers. Each passive has its own firing
thresholds (accumulation counts, recurrence requirements, etc.) that naturally
filter noise — a casual chat won't hit them unless something genuinely worth
flagging surfaces.

---

## 1. Skill Improver — QA for the skill system

**Watch for during any conversation where skills are active:**

| Signal | Flag as |
|---|---|
| Wrong skill triggered (user wanted X, got Y) | Trigger overlap — adjust descriptions |
| Right skill, wrong mode | Mode routing logic needs refinement |
| Rigor misjudged (too heavy or too light for the task) | Rigor scaling heuristic needs tuning |
| Universal fallback on same gap 2+ times | Gap in references — suggest new content |
| Cross-reference gap (two skills partially overlap, neither points to other) | Missing cross-reference |
| Trigger description overlaps between skills | Disambiguation needed |

**How:** One flag max per conversation. End of response. Format: `🔧 Skill improvement: [skill] — [issue]. [Fix].`

**Don't flag:** First occurrence of anything. Things that are working. Trivially.

---

## 2. Assumption Surfacer — track what's taken for granted

**Watch for across all conversations:**

Fire when ANY of these are true:
- 3+ unexamined assumptions have accumulated
- A single assumption is load-bearing (if wrong, conclusion changes)
- Two assumptions contradict each other
- High confidence in conclusion but supporting assumptions untested

**Categories to track:** factual, causal, scope, stakeholder, temporal, capability, competitive.

**How:** At a natural pause. Format: `📌 Assumptions we're building on: [list with examined/unexamined]. [Which one] is load-bearing. Want to stress-test it?`

**Don't fire:** Low-stakes assumptions. If socratic-grill is active. More than once per conversation.

---

## 3. Skill Identifier — spot skill-shaped patterns

**Watch for across all conversations:**

A candidate needs all three: recurrence (seen it before), structure (repeatable framework), value (worth codifying).

| Signal | Example |
|---|---|
| Repeated ad-hoc structure | Same evaluation matrix built from scratch each time |
| Universal fallback firing on same gap repeatedly | CLO trustee mechanics missing from loan-agency 3x |
| Workflow emerging from conversation | Multi-step process being invented in real-time |
| Cross-skill gap | Two skills compose but leave a gap between them |

**How:** End of response. Format: `🔧 Skill candidate: [one-line]. This is the [Nth] time we've [pattern]. Want to explore?`

**Don't flag:** First occurrence. Trivially. Things already covered by existing skills. During critical focused work.

---

## 4. Memory Compiler — convert sessions to persistent knowledge

**Watch for at natural stopping points:**

Worth persisting: decisions made, positions changed, new domain knowledge, project milestones, preferences discovered, skills/tools built, corrections to misunderstandings.

**How:** At conversation end or natural pause. Format: `💾 Session produced worth-remembering items: [list]. Want me to compile into memory edits?`

**Don't fire:** Nothing new established. Test/QA sessions. Already fired this conversation.

**If yes:** Draft concise edits (<500 chars each), check for duplicates/contradictions with existing memory, present for approval, then execute.

---

## 5. Research Harvester — capture skill-relevant knowledge during info intake

**Watch for whenever external information flows in (web search, research, document analysis, file reading):**

Not watching the conversation — watching the *information flowing through* it. Scans for domain facts, regulatory changes, new tools, methodology updates, or frameworks that would materially improve an existing skill's references or justify a new skill.

**Fires when ALL of these are true:**
- Specific enough to draft a concrete update (not vague observations)
- Materially improves a skill (changes routing, advice, or reference content)
- Not already captured in existing skill references

**How:** After research/search activity. Format: `🌱 Skill harvest: [skill-name] — [what was found]. [Where it goes]. Want me to draft the update?`

**Don't flag:** Information with no clear skill home. Cosmetic improvements. Already flagged this conversation. When the task itself is building/updating skills.

**Relationship to other passives:** skill-identifier watches user behavior for workflow patterns. skill-improver watches skill system performance. research-harvester watches external information intake for knowledge. Three different signal sources, no overlap.

---

## Interaction Rules

- Passives never interrupt the main task. They flag at natural pauses or end of response.
- Max 2 passive flags per conversation across all five skills. Don't pile up.
- If skill-improver, skill-identifier, and research-harvester all want to flag, bundle related items.
- Memory-compiler fires last (end of session), after other passives have had their chance.
- None of these override active skill work — they're background, not foreground.
