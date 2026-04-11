---
name: planning-prioritization
description: >
  Use this skill whenever the user wants to plan, prioritize, scope, or sequence
  work. Triggers include: 'roadmap', 'sprint planning', 'sprint plan', 'capacity
  plan', 'campaign plan', 'hiring plan', 'recruiting pipeline', 'forecast',
  'pipeline review', 'OKR', 'OKRs', 'prioritize', 'RICE', 'MoSCoW', 'ICE
  framework', 'Now/Next/Later', 'backlog grooming', 'scope this', 'estimate',
  'sequence', or requests to plan a sprint, build a roadmap, prioritize features,
  plan a campaign, forecast revenue or pipeline, review pipeline health, plan
  hiring, estimate capacity, or sequence a multi-phase initiative. Also use when
  the user says 'what should we work on next', 'help me prioritize', 'plan this
  quarter', or 'scope this project'. Do NOT use for executing the plan (use the
  relevant domain skill). Do NOT use for reporting on past results (use reporting).
  Do NOT use for process documentation (use process-design).
---

# Planning & Prioritization

Frameworks for deciding what to work on, when, and in what order.

## Routing

| If the user wants to... | Read |
|---|---|
| Build or update a product roadmap, prioritize features (RICE, MoSCoW, ICE) | `references/roadmap-management.md` |
| Plan a sprint — scope, capacity, goals | `references/sprint-planning.md` |
| Define, set up, or track product metrics and OKRs | `references/metrics-tracking.md` |
| Plan a marketing campaign — strategy, channels, timeline, budget | `references/campaign-plan.md` |
| Plan team capacity — headcount, utilization, resource allocation | `references/capacity-plan.md` |
| Design org structure, plan team composition | `references/org-planning.md` |
| Manage recruiting pipeline, plan hiring sequence | `references/recruiting-pipeline.md` |
| Forecast revenue, sales pipeline, or business projections | `references/forecast.md` |
| Review pipeline health, deal progression, conversion rates | `references/pipeline-review.md` |

## Gotchas

- Roadmaps are communication tools, not commitments. Make the confidence level explicit.
- Sprint planning requires knowing team capacity and velocity — ask before estimating.
- RICE/MoSCoW/ICE are useful for structuring discussion, not for producing "the right answer."
- Forecasts should include confidence intervals, not point estimates. A single number is false precision.
- Capacity planning must account for unplanned work — typically 20-30% of engineering time.
- "What should we work on next" requires knowing the goal first. Prioritization without strategy is just opinion.

## Pre-Step

If the user is planning in a domain where they lack information (new market, unfamiliar competitive landscape, uncertain assumptions), suggest research-analysis first: "Want to research this before we plan? The plan will be stronger with current data." Don't force it — offer once, then proceed either way.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
