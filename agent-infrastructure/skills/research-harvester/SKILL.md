---
name: research-harvester
description: >
  Background awareness skill. Runs passively whenever external information flows
  into the conversation — web searches, research tasks, document analysis, file
  reading, or any activity that brings in new domain knowledge. Watches for
  information that could materially improve an existing skill's references,
  fill a known gap, or justify a new skill. Different from skill-improver (which
  watches for routing/trigger problems) and skill-identifier (which watches for
  workflow patterns). This skill watches for KNOWLEDGE that the skill system
  doesn't yet contain. Do NOT flag trivially — only when the encountered
  information is specific enough to draft a concrete skill update.
---

# Research Harvester

Watch information intake for skill-relevant knowledge. This is the proactive
complement to the universal fallback pattern — fallback is reactive (the skill
broke, fix it); this is proactive (the skill worked fine, but here's knowledge
that would make it better).

## Activation

This passive activates whenever external information enters the conversation:

| Information Source | Watch For |
|---|---|
| **Web search results** | Domain facts, regulatory changes, new tools, methodology updates, market shifts |
| **Research tasks** | Frameworks, taxonomies, competitive intelligence, technical approaches |
| **Document analysis** | Process details, reference data, institutional knowledge |
| **File reading** | Data patterns, domain structures, operational details |
| **Link fetching** | Product updates, API changes, industry developments |

The passive is not watching the *conversation* — it's watching the *information
flowing through* the conversation. The trigger is knowledge intake, not discussion.

## What to Watch For

| Signal | Skill Impact | Example |
|---|---|---|
| **Regulatory/market change** | Existing domain skill references are now stale | CME fee waiver expires → loan-agency needs update |
| **New tool or framework** | Existing skill doesn't cover it, or a new skill is warranted | New nf-core pipeline released → bio-tools/bio-research gap |
| **Methodology improvement** | Better approach than what's currently in a skill | Research finds superior variance decomposition method → financial-close |
| **Competitive intelligence** | Competitor move that changes strategic positioning | Competitor launches feature → competitive-brief references |
| **Domain fact with reference value** | Specific, sourced data point that belongs in a skill's references | Private credit AUM figure with source → loan-agency strategic refs |
| **Pattern or framework encountered externally** | Structured approach found in research that matches a skill gap | Evaluation rubric found → review-critique could adopt |
| **Cross-domain connection** | Finding in one domain that has implications for another skill | Security research reveals API pattern → engineering skill |

## Firing Threshold

**All of these must be true before flagging:**

1. **Specific enough to draft.** Vague observations ("AI is changing fast") don't clear the bar. Concrete knowledge with a clear home does ("FASB issued ASU 2026-XX changing lease accounting — finance-accounting references need update").

2. **Materially improves a skill.** The knowledge would change how the skill routes, what it advises, or what its references contain. Not just "interesting" — actually useful for future skill invocations.

3. **Not already captured.** If the skill's existing references already cover this, don't flag. If unsure, err toward flagging — the user can dismiss it.

**Do NOT flag when:**
- The information is interesting but has no clear skill home
- The improvement is cosmetic (rewording, not new knowledge)
- You already flagged something this conversation (max one flag per conversation, consistent with other passives)
- The research task itself is about building or updating skills (that's explicit work, not passive observation)

## How to Flag

At a natural pause after the research/search activity, briefly:

```
🌱 Skill harvest: [skill-name] — [what was found]. [Where it would go in the skill].
Want me to draft the update?
```

**Examples:**

```
🌱 Skill harvest: loan-agency — SOFR Term Rate publication schedule changed per
CME announcement (found during market research). The qr-operational-mechanics
reference has the old schedule. Want me to draft the update?
```

```
🌱 Skill harvest: new skill candidate — encountered a structured vendor evaluation
framework during competitive research that doesn't fit competitive-brief or
review-critique cleanly. Recurring enough to warrant its own skill?
Want me to draft it?
```

```
🌱 Skill harvest: engineering — web search surfaced that Claude Code now supports
hook chaining (found while researching MCP patterns). The engineering skill's
deploy-checklist reference doesn't cover hooks. Want me to draft the update?
```

## Relationship to Other Passives

| Passive | Watches | Signal Source |
|---|---|---|
| **skill-identifier** | Workflow patterns in conversation | User behavior (repeated approaches) |
| **skill-improver** | Routing/trigger problems in skills | Skill system performance |
| **research-harvester** | Domain knowledge during info intake | External information (web, docs, files) |

These three form a skill evolution triad: identifier finds new skills from usage,
improver refines existing skills from performance, harvester enriches skills from
knowledge. They don't overlap — each watches a different signal source.

## If the User Says Yes

1. **For existing skill updates:** Draft the specific reference file edit or new reference file content. Include the source and date of the information. Present the before/after or the new content for approval.

2. **For new skill candidates:** Hand off to skill-identifier's workshop flow (Step 1: define the shape, Step 2: draft the router, Step 3: test the triggers, Step 4: build or defer). The harvester found the knowledge; the identifier's process builds the skill.

## When the Skill Doesn't Cover It

If you encounter information that feels skill-relevant but doesn't clearly map to an existing skill or skill gap — note it internally but don't flag. If the same gap appears across multiple research sessions, that's when it crosses the threshold. One encounter is an observation; a pattern is signal.
