---
name: process-design
description: >
  Use this skill whenever the user wants to document, optimize, or create an
  operational process, workflow, checklist, or runbook. Triggers include: 'runbook',
  'playbook', 'SOP', 'standard operating procedure', 'process documentation',
  'workflow', 'checklist', 'onboarding plan', 'change request', 'incident response
  plan', 'deploy checklist', 'compliance tracking', 'process optimization',
  'org design', 'design system management', 'month-end close process', or requests
  to document how something works, standardize a process, create step-by-step
  procedures, design an onboarding flow, or optimize an operational workflow. Also
  use when the user says 'how should we structure this process', 'create a checklist
  for', 'document our workflow for', or 'build a playbook'. Do NOT use for writing
  one-off documents (use structured-writing). Do NOT use for planning what to work
  on (use planning-prioritization). Do NOT use for reviewing a process (use
  review-critique).
---

# Process Design

Frameworks for documenting, standardizing, and optimizing repeatable processes.

## Routing

| If the user wants to... | Read |
|---|---|
| Document a process, create an SOP, write procedures | `references/process-doc.md` |
| Optimize an existing process, reduce waste, improve throughput | `references/process-optimization.md` |
| Create a runbook for operational procedures | `references/runbook.md` |
| Structure a change request or change management process | `references/change-request.md` |
| Track compliance deadlines, regulatory requirements, recurring obligations | `references/compliance-tracking.md` |
| Build an incident response plan or postmortem process | `references/incident-response.md` |
| Create a deployment checklist or release process | `references/deploy-checklist.md` |
| Design an onboarding flow for new hires | `references/onboarding.md` |
| Plan org structure, team design, role definitions | `references/org-planning.md` |
| Manage a design system — tokens, components, patterns, governance | `references/design-system-management.md` |
| Document or optimize a month-end close process | `references/close-management.md` |

## Gotchas

- A process document is not a process. If nobody follows it, it's just documentation theater.
- Checklists work best when each item is a binary check (done/not done), not a paragraph of instructions.
- Runbooks should be executable by someone who has never seen the system before. Test with a fresh pair of eyes.
- Incident response: stabilize first, investigate second. Never debug in production while users are affected.
- Process optimization should measure before and after. "It feels faster" is not optimization evidence.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
