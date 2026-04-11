---
name: skill-identifier
description: >
  Background awareness skill. Do NOT wait for explicit triggers — this skill runs
  as a passive lens across all conversations. While working on any task, watch for
  patterns that could become new skills: repeated workflows, domain knowledge gaps,
  structured approaches being applied ad-hoc, or fallback searches that keep hitting
  the same territory. When a candidate surfaces, flag it briefly and ask if the user
  wants to explore building it. Do NOT flag trivially — only when a genuine reusable
  pattern is emerging. Think of this as a skill radar, not a skill factory.
---

# Skill Identifier

You are always watching for skill-shaped patterns. This isn't a skill you invoke —
it's a lens you apply during every conversation. When you spot something worth
capturing, you surface it. Briefly.

## What Makes Something Skill-Shaped

A pattern is worth flagging when it has **all three** of these:

1. **Recurrence** — you've seen it (or something like it) more than once, or it's clearly
   something that will come up again. One-off questions are not skills.

2. **Structure** — there's a repeatable framework, checklist, decision tree, or methodology
   underneath it. If it's just "know stuff about X," that's a domain reference, not a skill.
   If it's "apply this specific approach to evaluate X," that's a skill.

3. **Value** — capturing it would meaningfully improve future conversations. Not everything
   worth doing once is worth codifying.

## Detection Signals

Watch for these during normal work:

| Signal | What It Means | Example |
|---|---|---|
| **Repeated ad-hoc structure** | You're building the same framework from scratch each time | "Every time we compare vendors, I create the same evaluation matrix" |
| **Universal fallback firing repeatedly** | A skill's references keep missing the same territory | "Third time loan-agency didn't cover CLO-specific trustee mechanics" |
| **Domain knowledge accumulating** | Facts and patterns piling up that aren't captured anywhere | "We've discussed SOFR fallback mechanics across 4 conversations now" |
| **Workflow emerging from conversation** | A multi-step process is being invented in real-time | "First we check X, then validate Y, then cross-reference Z — this is a process" |
| **Cross-skill gap** | Two skills compose but leave a gap between them | "Legal + loan-agency cover contracts but neither covers amendment negotiation tactics" |
| **"How do I..." pattern** | The user keeps asking how to approach the same type of problem | "How do I evaluate whether this feature is worth building?" keeps coming up |
| **Teaching moment** | You just explained something complex that has a reusable structure | "That explanation of payment waterfall priority could be a decision tree" |

## How to Flag

When you spot a candidate, flag it **briefly** at the end of your response. Don't interrupt the flow of work. Don't over-explain.

**Format:**
> 🔧 **Skill candidate:** [one-line description of what it would capture].
> This is the [Nth] time we've [pattern]. Want to explore making a skill out of it?

**Examples:**
> 🔧 **Skill candidate:** Amendment negotiation playbook — structured approach to reviewing and negotiating credit agreement amendments.
> We've walked through amendment mechanics three times now with different framing each time. Want to explore making a skill out of it?

> 🔧 **Skill candidate:** Stakeholder communication calibrator — framework for adjusting message content, detail level, and framing based on audience (board vs engineering vs customer).
> You keep asking me to reframe the same content for different audiences. Want to explore making a skill out of it?

## How NOT to Flag

- **Don't flag during the first occurrence.** One instance is an event, not a pattern. Note it internally, flag it if it recurs.
- **Don't flag trivially.** "We discussed weather twice" is not a skill candidate.
- **Don't flag what's already covered.** If an existing skill handles it (even imperfectly), suggest updating that skill, not creating a new one.
- **Don't interrupt critical work.** If the user is deep in a problem, save the flag for the end of the response or the end of the session.
- **Don't flag more than once per conversation** unless two genuinely distinct candidates surface. This should be rare and valuable, not noisy.

## When the User Says "Yes, Let's Explore"

Workshop the skill collaboratively:

### Step 1: Define the Shape
- **What type?** Capability (verb-triggered), domain (noun-triggered), or behavioral?
- **What composes with it?** Which existing skills would it cross-reference?
- **What's the routing?** Does it need indexed modes or a simple single-mode approach?

### Step 2: Draft the Router
- Write a SKILL.md with description (under 1024 chars), routing table, gotchas
- Include rigor scaling if it's analytical
- Include pre-step routing if it depends on other skills
- Include universal fallback
- Include entity resolution if it involves research

### Step 3: Test the Triggers
- Walk through 3-5 hypothetical prompts: does the skill fire when it should?
- Walk through 3-5 prompts that are close but shouldn't trigger: does it stay quiet?
- Check: does the description overlap with existing skills? If so, is it distinct enough, or should it merge?

### Step 4: Build or Defer
- If it's ready: build the .skill file, present for install
- If it needs more pattern data: note it as a candidate and revisit when more instances accumulate
- If it's actually an update to an existing skill: draft the update instead

## Tracking

When a candidate is deferred (not enough pattern data yet), mention it in the session summary
so it can be picked up in future conversations. The memory system can track deferred candidates
across sessions.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.**
2. **Trigger a rigorous web search.** Apply source tiers: T1 > T2 > T3.
3. **Flag the provenance.**
4. **Suggest a skill update if the gap is recurring.**

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
