---
name: design-ops
description: >
  Use this skill for design evaluation, accessibility auditing, design system management,
  UX writing, and developer handoff. Triggers include: 'critique this design', 'review
  this mockup', 'accessibility audit', 'WCAG check', 'design system', 'component
  library', 'design tokens', 'developer handoff', 'UX copy', 'microcopy', 'error
  messages', 'empty state copy', 'what should this button say', 'usability test',
  'design review', 'UI feedback', 'color palette', 'typography review', 'responsive
  design', or requests to evaluate, document, or operationalize design work. Also
  trigger when the user shares a screenshot or mockup and asks for feedback. Do NOT
  use for general creative review without design context (use review-critique). Do NOT
  use for writing marketing content (use structured-writing). Do NOT use for data
  visualization design (chain through data-analysis instead).
---

# Design Ops

Evaluate, iterate, document, and ship designs. This workflow connects the design
lifecycle — from research through critique through system management through handoff.
It chains review-critique for evaluation, structured-writing for documentation, and
process-design for operational workflows.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick feedback — "what do you think of this", "does this look right" | **Quick** | Conversational feedback. Top observations. No framework. |
| Standard design work — "review this", "write copy for this", "document these components" | **Standard** | Apply the relevant routing below. Structured feedback or output. |
| Ship-grade — production release, public-facing, regulatory. OR user says "WCAG audit", "this is going to production" | **Rigorous** | Full review-critique rigorous protocol. Cite standards. Document what was and wasn't checked. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Evaluate a design for usability, hierarchy, and consistency | Load `review-critique` (creative mode) |
| Run a WCAG 2.1 AA accessibility audit | Load `review-critique` (standards-based mode) |
| Manage design tokens, component libraries, and patterns | Load `process-design` |
| Create developer handoff documentation with specs | Load `structured-writing` |
| Write or review UX microcopy — buttons, errors, empty states | See UX Writing section below |
| Plan, design, or synthesize user research | Load `research-analysis` → reference `user-research` or `user-research-synthesis` |
| Build a front-end component or artifact | Load `frontend-design` skill for implementation |
| Evaluate a design as part of a product workflow | Load `product-ops` for PM context |

## Design Lifecycle

Understanding where the user is in the lifecycle determines feedback calibration:

1. **Research** → Understand users, context, and constraints. Chain: `research-analysis`.
2. **Design** → Create solutions. (Outside Claude's scope — this happens in Figma/Sketch/etc.)
3. **Critique** → Evaluate against usability, accessibility, brand, and consistency. Chain: `review-critique`.
4. **Iterate** → Refine based on feedback. Write UX copy. Update components.
5. **Document** → Design system tokens, component specs, interaction patterns. Chain: `process-design`.
6. **Handoff** → Implementation specs, responsive behavior, edge cases, accessibility notes. Chain: `structured-writing`.
7. **Validate** → Accessibility audit on implemented version. Chain: `review-critique` (standards mode).

## UX Writing

UX copy is interface design, not copywriting. When writing or reviewing microcopy:

**Principles:**
- Clarity over cleverness. The user is trying to do something, not read prose.
- Match the user's mental model. Use the words they use, not internal jargon.
- Front-load the action. "Save changes" not "Would you like to save your changes?"
- Be specific in errors. "Email address needs an @ symbol" not "Invalid input."
- Empty states are onboarding moments. Tell the user what to do, not just that nothing's here.

**Common decisions:**
- "Sign up" vs "Create account" vs "Get started" — each signals a different commitment level.
- "Cancel" vs "Never mind" vs "Go back" — "Cancel" is ambiguous (cancel the action or the subscription?).
- "Delete" vs "Remove" — "Delete" implies permanent; "Remove" implies from a list/group.
- Error messages: state what happened, why, and what to do next. In that order.

**Review checklist for UX copy:**
- Is the action clear from the button label alone?
- Does the error message tell the user how to fix it?
- Is the tone consistent across the flow?
- Are confirmation dialogs specific about consequences?
- Do empty states guide toward first action?

## Design Critique Framework

When evaluating a design (at any stage), consider these dimensions in order of importance:

1. **Does it solve the problem?** If the user goal isn't clear, ask before critiquing.
2. **Can the user figure out what to do?** Information hierarchy, affordances, visual flow.
3. **Does it handle edge cases?** Empty states, errors, loading, long content, no permissions.
4. **Is it accessible?** Color contrast, keyboard navigation, screen reader compatibility, touch targets.
5. **Is it consistent?** With the design system, with platform conventions, with itself.
6. **Is it polished?** Spacing, alignment, typography, visual rhythm.

**Stage matters more than anything.** Pixel-level critique on a wireframe is wasted effort. Strategic feedback on a final comp is too late. Always clarify the stage before going deep.

## Accessibility Quick Reference

For rigorous audits, load `review-critique` standards-based mode. For quick checks:

| Check | Standard | How to Verify |
|---|---|---|
| Text contrast | 4.5:1 normal, 3:1 large text (WCAG AA) | Measure with contrast checker — don't eyeball it |
| Touch targets | 44×44px minimum (WCAG 2.5.5) | Check against actual rendered size |
| Focus indicators | Visible focus ring on all interactive elements | Tab through the interface |
| Alt text | All meaningful images have descriptive alt text | Review image elements |
| Heading hierarchy | h1 → h2 → h3, no skipped levels | Check DOM structure |
| Color alone | Information not conveyed by color alone | View in grayscale |

## Gotchas

- **Stage matters more than anything.** Ask "where are you in the process?" before diving into feedback. Wireframe critique ≠ final comp critique.
- Accessibility is not a phase — it's a lens applied at every stage. Don't wait for the "accessibility review" step.
- Design system documentation is only useful if it stays current. Outdated docs are worse than no docs — they create false confidence.
- Developer handoff specs must include edge cases: empty states, error states, loading states, truncation, responsive breakpoints, RTL behavior.
- **Critique without context is just opinion.** Always ask: What's the goal? Who's the user? What's the constraint?
- Color contrast ratios have specific WCAG thresholds. Don't say "this might not be accessible" — measure it.
- When reviewing screenshots/mockups, be honest about what you can and can't assess. You can evaluate layout, hierarchy, copy, and contrast. You can't test interactions, animations, or screen reader behavior from a static image.
- Dual-axis charts are almost always misleading. Pie charts fail beyond 5 segments. If the design includes data visualization, apply those principles too.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The design references cover WCAG 2.1 but not the new WCAG 2.2 success criteria."
2. **Search.** Authoritative sources. T1 (W3C specs, platform design guidelines) > T2 (A11y Project, Nielsen Norman Group) > T3 (blog posts).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
