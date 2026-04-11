---
name: skill-improver
description: >
  Background awareness skill. Do NOT wait for explicit triggers — this skill runs
  passively during all conversations where other skills are active. Watches for
  routing misfires (wrong skill triggered), incomplete gotchas, rigor scaling
  misjudgments, universal fallback firing repeatedly on the same gap, cross-reference
  gaps, and trigger description overlaps. When an improvement surfaces, flag it
  briefly at the end of the response. Do NOT flag trivially — only when the
  improvement would meaningfully change skill behavior. Think of this as QA for
  the skill system itself.
---

# Skill Improver

Passive quality layer for the skill ecosystem. Watches how skills perform in real
conversations and surfaces improvement opportunities.

## Detection Signals

| Signal | What It Means | Flag As |
|---|---|---|
| **Wrong skill triggered** | User wanted review-critique but research-analysis fired, or vice versa | Trigger overlap — adjust descriptions to disambiguate |
| **Right skill, wrong mode** | review-critique fired but selected standards mode when judgment was needed | Mode routing logic needs refinement |
| **Rigor misjudged** | Applied rigorous protocol to a casual question, or gave a quick answer to something that needed rigor | Rigor scaling heuristic needs tuning |
| **Universal fallback on same gap 2+ times** | Skill references don't cover the same territory repeatedly | Gap in references — suggest adding content or a new reference file |
| **Cross-reference gap** | Two skills both partially cover a topic but neither points to the other | Missing cross-reference — suggest adding |
| **Gotcha proved wrong** | A gotcha warned against something that turned out to be the right approach | Gotcha is too broad or outdated — suggest revising |
| **Skill never fires** | A skill hasn't triggered in many conversations despite relevant topics coming up | Description may not match how the user actually phrases requests |
| **Pre-step ignored** | A skill suggested running another skill first but the suggestion wasn't useful | Pre-step routing is too aggressive or wrong context |

## How to Flag

At the end of the response, briefly:

> 🔧 **Skill improvement:** [skill name] — [one-line issue]. [One-line fix suggestion].
> Want me to draft the update?

**Examples:**

> 🔧 **Skill improvement:** research-analysis — rigor scaling triggered rigorous mode for a quick competitive lookup. The "informing a decision" heuristic is too broad. Suggest adding: "multi-source research with synthesis" as the standard trigger, reserving rigorous for explicit stakes signals.
> Want me to draft the update?

> 🔧 **Skill improvement:** loan-agency — third time the fallback fired on CLO trustee mechanics. The qr-operational-mechanics.md doesn't cover CLO-specific workflows. Suggest adding a qr-clo-mechanics.md quick-reference.
> Want me to draft the update?

## Rules

- **Max one flag per conversation.** Skill improvement is background, not the main event.
- **Don't flag during the first occurrence.** One misfire is noise. A pattern is signal.
- **Don't flag what's working.** If the skill routed correctly and the user got what they needed, there's nothing to improve.
- **Bundle related issues.** If trigger overlap AND mode routing are both off for the same skill, flag them together as one improvement.
- **When the user says "yes, draft the update"** — produce the specific edit (description change, new gotcha, reference file content, cross-reference addition) ready to apply. Don't produce a plan — produce the fix.

## Trial Period (Lightweight Shadow Mode)

Claude.ai can't run two skill versions in parallel like Claude Code can. But we can
approximate shadow mode through a trial period:

**When a skill update is proposed and accepted:**

1. **Don't apply immediately.** Instead, note the proposed change and mentally apply it
   for the next 3-5 invocations of that skill.
2. **Track outcomes.** After each invocation during the trial: did the proposed change
   improve routing/rigor/output? Would the old behavior have been better?
3. **Report back.** After 3-5 uses:

> 🔧 **Trial report:** [skill-name] update — [change description]
> Tested across [N] invocations. Result: [improved / no difference / made things worse].
> [One-line evidence]. Apply permanently? [yes / reject / extend trial]

4. **If approved:** Build the updated .skill file and present for install.
5. **If rejected:** Note why it didn't work — that's valuable calibration data too.

**The principle:** Changes are cheap to propose, expensive to get wrong. A few conversations
of mental A/B testing costs nothing. A bad skill update degrades every future conversation
that triggers it.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.**
2. **Trigger a rigorous web search.** Apply source tiers: T1 > T2 > T3.
3. **Flag the provenance.**
4. **Suggest a skill update if the gap is recurring.**

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
