---
name: structured-writing
description: >
  Use this skill whenever the user wants to write, draft, or create a structured
  document or communication. Triggers include: 'PRD', 'product spec', 'feature spec',
  'write a brief', 'draft an email', 'KB article', 'knowledge base article',
  'stakeholder update', 'content creation', 'blog post', 'outreach email',
  'email sequence', 'offer letter', 'technical documentation', 'API docs',
  'announcement', 'UX copy', 'microcopy', 'error messages', 'design handoff',
  'brand guidelines', 'style guide', 'customer response', or requests to write, draft,
  compose, or create any document with a defined audience and structure. Also use when
  the user says 'help me write', 'draft this', 'put together a brief on', or 'create
  a spec for'. Do NOT use for process documentation or runbooks (use process-design).
  Do NOT use for reports or metric summaries (use reporting). Do NOT use for
  research/analysis that precedes writing (use research-analysis first).
---

# Structured Writing

Frameworks for creating documents and communications with a defined audience, purpose, and structure.

## Routing — What Are You Writing?

| Document type | Read |
|---|---|
| Product spec, PRD, feature requirements, acceptance criteria | `references/feature-spec.md` |
| Stakeholder update — executives, engineering, customers, cross-functional | `references/stakeholder-comms.md` |
| Marketing content — blog posts, landing pages, social, thought leadership | `references/content-creation.md` |
| Email sequence — nurture, onboarding, re-engagement, drip campaigns | `references/email-sequence.md` |
| Knowledge base article, help documentation, support content | `references/kb-article.md` |
| Customer response — support reply, escalation response | `references/draft-response.md` |
| Technical documentation — README, API docs, architecture docs, guides | `references/documentation.md` |
| UX copy — microcopy, error messages, empty states, CTAs, onboarding | `references/ux-writing.md` |
| Design handoff — developer specs, implementation notes, component docs | `references/design-handoff.md` |
| Brand voice guidelines — discover, document, or enforce brand voice | `references/discover-brand.md` + `references/brand-voice-enforcement.md` |
| Sales outreach — cold email, follow-up, intro, meeting request | `references/outreach.md` |
| Offer letter or hiring communication | `references/offer-letter.md` |

## Gotchas

- Always clarify the audience before writing. Executive summary ≠ engineering spec ≠ customer-facing.
- First drafts should be structured, not polished. Get the skeleton right before wordsmithing.
- Stakeholder updates for executives: lead with decisions needed and outcomes, not activity.
- UX copy should be tested with users when possible — what sounds clear to the writer often confuses users.
- Technical documentation should include a "Quick Start" that gets someone to first success in < 5 minutes.
- Brand voice is a constraint, not an afterthought. Apply it during writing, not as a polish pass.

## Pre-Step

If the user's requirements are vague, underspecified, or they're "thinking out loud" about what to write, suggest running socratic-grill Extract mode first: "Want me to ask you some questions before we start writing? It usually produces a better spec." Don't force it — offer once, then proceed either way.

## Learning Opportunities

After explaining a complex framework (RICE prioritization, stakeholder mapping, PRD structure), briefly offer a check: "Want to try applying that framework to one of your current projects? Quick exercise." Only when the framework is new to the user and they'll use it again. Offer once, don't push.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
