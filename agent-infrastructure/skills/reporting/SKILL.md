---
name: reporting
description: >
  Use this skill whenever the user wants to create a summary, report, digest,
  or briefing about what happened or what's current. Triggers include: 'status
  report', 'performance report', 'metrics report', 'standup', 'standup update',
  'daily briefing', 'weekly digest', 'channel digest', 'call summary', 'meeting
  summary', 'people report', 'KPI review', 'executive summary', or requests to
  summarize recent activity, create a status update, digest information, generate
  a standup, brief someone on current state, or report on performance. Also use
  when the user says 'summarize what happened', 'give me a status update',
  'what is the latest on', 'brief me on', or 'recap this'. Do NOT use for
  building dashboards with live data (use data-analysis). Do NOT use for
  planning what to do next (use planning-prioritization). Do NOT use for
  writing original content (use structured-writing). Do NOT use for deep
  research (use research-analysis).
---

# Reporting

Frameworks for summarizing what happened, what's current, and what matters — for different audiences and cadences.

## Routing

| If the user wants to... | Read |
|---|---|
| Create a status report — project, team, or organizational | `references/status-report.md` |
| Report on marketing or business performance — campaigns, KPIs, trends | `references/performance-report.md` |
| Create a people/HR report — headcount, attrition, engagement | `references/people-report.md` |
| Generate a daily sales briefing or pipeline update | `references/daily-briefing.md` |
| Summarize a call, meeting, or conversation | `references/call-summary.md` |
| Generate a standup update from recent activity | `references/standup.md` |
| Digest information from multiple sources into a summary | `references/digest.md` |

## Gotchas

- Reports should lead with "so what" — the insight or decision, not the data.
- Executive reports: 3-5 bullets max, decisions needed, risks flagged. No activity lists.
- Standups are for coordination, not status theater. Focus on blockers and handoffs.
- Call summaries should capture decisions and action items, not a transcript.
- Performance reports need context — "revenue was $2M" means nothing without "vs. $1.8M target."
- Match the cadence to the audience. Daily for ops teams. Weekly for stakeholders. Monthly for executives.

## Pre-Step

If the user wants a report but the underlying data hasn't been analyzed yet (raw CSV, unprocessed metrics, no existing dashboard), suggest data-analysis first: "Want me to analyze the data before writing the report? I can profile it and surface the key findings, then we write it up." Don't force it — offer once, then proceed either way.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.

## Entity Resolution

Before researching context for a report, resolve ambiguous names and entities: person → company/role, company → products/abbreviations, acronym → full name. Prevents reporting on the wrong entity or conflating similarly-named things. See research-analysis skill for the full protocol.
