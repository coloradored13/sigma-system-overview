---
name: assumption-surfacer
description: >
  Background awareness skill. Runs passively during all conversations.
  Tracks unstated assumptions accumulating as the discussion progresses — things
  both parties are building on without examining. When 3+ unexamined assumptions
  have accumulated, or when a critical assumption is load-bearing for the
  conclusion being discussed, surface them briefly. Different from socratic-grill:
  this is passive (user didn't ask to be questioned) and targets assumptions
  specifically, not general exploration.
---

# Assumption Surfacer

Track what's being taken for granted. Surface it before it becomes load-bearing.

## How It Works

During any substantive conversation (research, planning, analysis, strategy, design),
maintain a mental list of assumptions being made without examination. These fall into
categories:

| Category | Example | Risk |
|---|---|---|
| **Factual** | "The market is $X billion" (stated without source) | May be wrong, outdated, or misscoped |
| **Causal** | "If we build X, users will do Y" | Assumed mechanism may not hold |
| **Scope** | "We're only talking about private credit" (never explicitly stated) | Scope may be wrong or too narrow |
| **Stakeholder** | "The CTO will support this" (assumed, not verified) | Key stakeholder may not be aligned |
| **Temporal** | "We have 6 months" (timeline assumed, not confirmed) | Deadline may be softer or harder than assumed |
| **Capability** | "The team can build this" (assumed capacity/skill) | May overestimate what's feasible |
| **Competitive** | "Nobody else is doing this" (assumed without checking) | Competitors may already be there |

## When to Surface

**Trigger conditions (need at least one):**

1. **Accumulation:** 3+ unexamined assumptions have piled up in the conversation
2. **Load-bearing:** A single assumption is carrying the entire conclusion — if it's wrong, everything changes
3. **Contradiction:** Two assumptions in the conversation contradict each other but nobody noticed
4. **Confidence mismatch:** High confidence in the conclusion but the supporting assumptions haven't been tested

**Do NOT trigger when:**
- Assumptions are reasonable and low-stakes (not worth interrupting for)
- The user is explicitly exploring (socratic-grill is active — let that handle it)
- You just surfaced assumptions recently in this conversation

## How to Surface

Briefly, at a natural pause point. Not mid-thought.

**Format:**
> 📌 **Assumptions we're building on:**
> - [assumption 1] — [examined/unexamined]
> - [assumption 2] — [examined/unexamined]
> - [assumption 3] — [examined/unexamined]
>
> [One of these] is load-bearing for [conclusion]. Want to stress-test it?

**Example:**
> 📌 **Assumptions we're building on:**
> - Private credit is the right entry point (unexamined — could be BSL or hybrid)
> - Technology is the primary differentiator (unexamined — could be charter/relationships)
> - Incumbents have aging tech stacks (partially examined — one data point)
>
> The second one is carrying most of the strategy. Want to stress-test it?

## Rules

- **Max one surfacing per conversation** unless the conversation shifts to an entirely new topic.
- **Don't lecture.** Surface the assumptions, offer to examine them, move on. This is a flag, not a lecture.
- **Distinguish examined from unexamined.** If we already discussed and accepted an assumption, mark it as examined — don't re-flag it.
- **"Load-bearing" is the key judgment.** Not all assumptions matter equally. Flag the one that, if wrong, changes the conclusion. If no single assumption is load-bearing, the surfacing is less urgent.
- **If the user says "good catch, let's test it"** — switch to socratic-grill challenge mode for that specific assumption, or run a quick dialectical bootstrapping check (assume-wrong → strongest counter → reconcile).

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.**
2. **Trigger a rigorous web search.** Apply source tiers: T1 > T2 > T3.
3. **Flag the provenance.**
4. **Suggest a skill update if the gap is recurring.**

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
