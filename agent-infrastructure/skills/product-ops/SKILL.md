---
name: product-ops
description: >
  Use this skill for product management execution — writing specs, planning sprints,
  updating roadmaps, reviewing metrics, synthesizing research, and communicating to
  stakeholders. Triggers include: 'write a spec', 'PRD', 'feature spec', 'sprint
  planning', 'plan this sprint', 'roadmap update', 'update the roadmap', 'metrics
  review', 'how are our metrics', 'stakeholder update', 'weekly update', 'synthesize
  this research', 'user research synthesis', or requests to execute product management
  workflows. Also trigger on implicit PM context: 'what should we ship next', 'scope
  this feature', 'write up the requirements', 'prepare for sprint', 'update leadership',
  or any request combining product thinking with a deliverable. Do NOT use for
  prioritization frameworks or deciding what to work on (use planning-prioritization).
  Do NOT use for general research (use research-analysis). Do NOT use for general
  writing without PM context (use structured-writing).
---

# Product Ops

Execute product management workflows — spec → plan → ship → measure → communicate.
This is the PM-specific orchestrator that chains planning-prioritization (for decisions),
structured-writing (for documents), research-analysis (for investigation), and
reporting (for stakeholder communication).

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick task — "draft a user story for X", "update stakeholders on Y" | **Quick** | Generate the output directly. Standard format. |
| Standard PM workflow — "write a spec for", "plan this sprint", "review our metrics" | **Standard** | Apply the relevant routing below. Full structure. |
| High-stakes — new product area, major pivot, board-level. OR user says "this is for the exec team", "be thorough" | **Rigorous** | Full protocol: research first, validate assumptions, include confidence levels, get explicit on unknowns. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Write a PRD or feature spec | Load `structured-writing` → reference `feature-spec` |
| Plan a sprint — scope, capacity, goals | Load `planning-prioritization` → reference `sprint-planning` |
| Update or reprioritize a roadmap | Load `planning-prioritization` → reference `roadmap-management` |
| Review product metrics with trend analysis | Load `data-analysis` → reference `metrics-tracking` |
| Generate a stakeholder update | Load `reporting` + `structured-writing` → reference `stakeholder-comms` |
| Synthesize user research into insights | Load `research-analysis` → reference `user-research-synthesis` |
| Run a competitive analysis for product strategy | Load `competitive-brief` workflow |
| Evaluate a design, review a mockup, write UX copy | Load `design-ops` workflow |
| Build a metrics dashboard | Load `data-analysis` → reference `interactive-dashboard-builder` |
| Scope or estimate a feature | Load `planning-prioritization` for framework, `engineering` for technical estimation |

## The Product Cycle

Understanding where the user is in the cycle determines which skills to chain:

1. **Research** → Understand users, market, and competitors. Chain: `research-analysis`, `competitive-brief`.
2. **Prioritize** → Decide what to build and in what order. Chain: `planning-prioritization`.
3. **Spec** → Define what you're building and why. Chain: `structured-writing`.
4. **Plan** → Break into sprints, estimate capacity, set goals. Chain: `planning-prioritization`.
5. **Ship** → Execution happens outside this skill.
6. **Measure** → Track metrics, review progress, identify issues. Chain: `data-analysis`, `reporting`.
7. **Communicate** → Update stakeholders on progress, decisions, and direction. Chain: `reporting`.

## Gotchas

- **Specs without problem statements are feature requests.** Every PRD must answer "what problem are we solving and for whom" before "what are we building."
- Sprint planning requires knowing velocity and capacity. Don't estimate in a vacuum — ask about the team.
- Roadmaps are communication tools, not commitments. Make confidence levels explicit (high/medium/low or committed/planned/exploring).
- **Metrics without context are just numbers.** "DAU is 12,000" means nothing without: trend direction, comparison period, target, and what's driving the change.
- Stakeholder updates should lead with decisions needed, not status. Executives want "here's what I need from you" not "here's what I did."
- User research synthesis must distinguish observations (what users said/did) from interpretations (what it means) from recommendations (what to do about it).
- **"Ship it and see" is a valid strategy for low-stakes features. It's negligent for high-stakes ones.** Match rigor to consequences.
- When composing with `review-critique`, use judgment mode for prioritization decisions, standards mode for spec completeness, creative mode for UX/design evaluation.

## Pre-Step

If the user jumps straight to a deliverable without context — "write me a PRD" with no problem statement, user context, or constraints — suggest `socratic-grill` Extract mode first: "Want me to ask you some scoping questions before I draft this? The spec will be sharper." The extraction produces the problem/user/constraint frame that makes the downstream deliverable useful.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The PM references cover B2B SaaS product workflows but not hardware product development."
2. **Search.** Authoritative sources. T1 (Marty Cagan, Reforge, official frameworks) > T2 (product blogs, case studies) > T3 (opinion pieces).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
