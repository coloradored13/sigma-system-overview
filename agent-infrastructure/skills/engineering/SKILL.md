---
name: engineering
description: >
  Use this skill whenever the user asks about software engineering processes,
  code quality, system architecture, or technical operations. Triggers include:
  'architecture decision', 'ADR', 'code review', 'review this PR', 'debug this',
  'deploy checklist', 'incident response', 'postmortem', 'system design', 'tech
  debt', 'testing strategy', 'test plan', 'standup', or requests to review code,
  debug an error, design a system, plan a deployment, assess technical debt, or
  create a testing strategy. Requires engineering-specific context — code patterns,
  system architecture, deployment infrastructure, testing approaches. Composes
  with review-critique skill for structured evaluation frameworks and process-design
  skill for operational procedures. Do NOT use for data analysis or SQL (use
  data-analysis). Do NOT use for product specs (use structured-writing). Do NOT
  use for general process documentation without engineering context (use
  process-design).
---

# Engineering

Software engineering processes, architecture, code quality, and technical operations.

## Routing

| If the user wants to... | Read |
|---|---|
| Make or evaluate an architecture decision (ADR) | `references/architecture.md` |
| Review code — security, performance, correctness | `references/code-review.md` |
| Debug an error — reproduce, isolate, diagnose, fix | `references/debug.md` |
| Design a system, service, or architecture | `references/system-design.md` |
| Identify, categorize, and prioritize technical debt | `references/tech-debt.md` |
| Design test strategies and test plans | `references/testing-strategy.md` |
| Run incident response — triage, communicate, postmortem | `references/incident-response.md` |
| Pre-deployment verification | `references/deploy-checklist.md` |
| Write or maintain technical documentation | `references/documentation.md` |
| Generate a standup update from recent activity | `references/standup.md` |

## Gotchas

- Code review should distinguish blocking issues from suggestions — not everything is a blocker.
- Architecture decisions need reversibility assessment — one-way doors deserve more scrutiny than two-way doors.
- Incident response: stabilize first, investigate second. Never debug in production while users are affected.
- Tech debt prioritization should connect to business impact, not just engineering aesthetics.
- "Design a system" requires clarifying scale, constraints, and tradeoffs before drawing boxes and arrows.
- Testing strategy should follow the testing pyramid — unit > integration > e2e. Inverting this is expensive.

## Learning Opportunities

After producing code, explaining architecture, or walking through a technical decision, briefly offer a learning check when the topic was complex or new to the user. Not every time — only when the concept matters for their ongoing work.

**Pattern:** "Want me to walk you through why we used [pattern/approach]? Quick 2-minute exercise."

**Techniques (pick one, keep it brief):**
- **Predict-then-reveal:** "Before I show the implementation — what do you think happens when a lender's payment hits during assignment freeze?" Then show the code.
- **Trace-the-path:** "Walk me through what happens to a payment that arrives after 6:45 PM ET." Use their words, correct gently.
- **What-breaks-if:** "What would break if we removed the day-count validation step?"
- **Teach-it-back:** "How would you explain this waterfall priority to a new engineer on your team?"

**Rules:**
- Offer, don't impose. If declined, move on — never offer again in the same session.
- Max 2 per session. These are supplements, not a curriculum.
- Only for concepts the user will encounter again. One-off trivia doesn't justify the interruption.
- Pause and WAIT for their response. Don't answer your own question.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
