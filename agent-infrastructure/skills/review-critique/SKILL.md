---
name: review-critique
description: >
  Use this skill whenever the user wants something evaluated, reviewed, audited, validated, triaged, or quality-checked. Triggers: 'review this', 'critique', 'audit', 'feedback on', 'validate', 'assess the risk', 'triage', 'QA this', 'accessibility review', 'WCAG', 'compliance check', 'risk assessment', 'vendor assessment', 'SEO audit', 'brand review', 'performance review', 'data validation', 'NDA review', 'pre-mortem', 'what could go wrong', 'what am I missing', or any request to evaluate quality or provide structured feedback. Three modes: creative (design, brand, content, UX), standards-based (accessibility, compliance, data validation, audit), judgment-based (contracts, risk, vendors, triage, performance, pre-mortem). Domain skills provide specialized knowledge; this skill provides the review FRAMEWORK. Do NOT use for writing new content (use structured-writing) or building reports (use reporting).
---

# Review & Critique

Structured evaluation across three review modes. Each mode has a different
evaluation approach, feedback style, and quality bar.

## Routing — Which Review Mode?

Read the user's request and match to the right mode. **If unclear, ask.**

| Signal in the request | Mode | Load |
|---|---|---|
| Design, mockup, wireframe, layout, visual, brand, content quality, tone, UX copy, "what do you think of this" | **Creative** | `references/creative-review.md` |
| WCAG, accessibility, compliance, regulatory, data quality, validation, schema, audit, SOX, SEO, checklist, standards | **Standards-Based** | `references/standards-review.md` |
| Contract, risk, vendor, NDA, triage, escalation, performance review, assessment, "should we do this", red flags, due diligence, **pre-mortem, "what could go wrong", "what am I missing"** | **Judgment-Based** | `references/judgment-review.md` |

**Multiple modes can apply.** A design accessibility audit is creative (visual hierarchy feedback) + standards-based (WCAG compliance). A vendor contract is judgment-based (business risk) + possibly standards-based (compliance requirements). Load both when needed.

**Domain skills compose with review modes:**

| If reviewing... | Also load |
|---|---|
| A contract or legal agreement | `legal` skill for domain knowledge |
| Code, architecture, or a PR | `engineering` skill for code patterns |
| Financial statements or reconciliation | `finance-accounting` skill for GAAP standards |
| Loan agency workflows or credit agreements | `loan-agency` skill for domain context |
| A dataset or analysis | `data-analysis` skill for statistical rigor |

---

## Rigor Scaling

Not every review needs the same depth. Match rigor to stakes.

| Signal | Level | What Changes |
|---|---|---|
| Quick gut check, early draft, "does this seem right" | **Glance** | Conversational feedback. Top 2-3 observations. No framework. |
| Standard review — "review this", "give me feedback", "what do you think" | **Standard** | Apply the relevant mode framework. Use severity levels. Cover all dimensions in the mode. |
| High-stakes review — going to a client, board, production, or regulatory body. OR user says "thorough", "audit-level", "this matters" | **Rigorous** | Full mode framework PLUS the discipline below. |

### Rigorous Review Protocol

**1. Explicit criteria.** State what you're evaluating against BEFORE reviewing. "I'm checking this against: [list]." If the criteria aren't clear, ask.

**2. Evidence on every blocker.** 🔴 findings must cite the specific standard, principle, or evidence. "This fails because [specific reason]" not "this doesn't feel right."

**3. Confidence per finding.** For judgment-based reviews especially: "High confidence this is a problem" vs "I'm uncertain but flagging it." Don't present speculation with the same weight as confirmed issues.

**4. What you DIDN'T check.** Explicitly state the boundaries of your review. "I reviewed for X and Y. I did NOT check Z — that would require [expertise/access/time]."

**5. Assume-wrong on your harshest critique.** For your most critical finding, run the check: if you're wrong about this, what's the consequence of the user acting on bad feedback? This prevents over-flagging driven by caution rather than evidence.

**6. Steelman before critique.** For judgment-based reviews: before saying "don't do this," articulate the strongest version of why they SHOULD. If the steelman is strong, your critique needs to be stronger to hold.

---

## Universal Review Principles (Apply to All Modes)

### Before You Review
1. **Clarify the stage.** Early exploration gets directional feedback, not polish. Final deliverable gets precision. Ask if unclear.
2. **Clarify the audience.** Internal working doc ≠ client-facing deliverable ≠ regulatory submission.
3. **Clarify the ask.** "What do you think" is different from "is this compliant" is different from "should we proceed."

### How to Give Feedback
- **Be specific.** "The CTA competes with the navigation" not "the layout is confusing."
- **Explain why.** Connect feedback to principles, standards, or user impact.
- **Suggest alternatives.** Don't just identify problems — propose solutions.
- **Acknowledge what works.** Good feedback includes positive observations.
- **Prioritize.** Distinguish blockers from suggestions. Not everything is critical.
- **Match the register.** Casual check-in gets conversational feedback. Formal audit gets structured findings.

### Feedback Severity Framework

| Level | Meaning | Action |
|---|---|---|
| 🔴 **Blocker** | Must fix before proceeding. Compliance failure, critical usability issue, material risk. | Cannot ship/approve/sign without resolution. |
| 🟡 **Issue** | Should fix. Meaningful quality or risk concern, but not blocking. | Fix in current cycle if possible, or document as known issue. |
| 🔵 **Suggestion** | Could improve. Nice-to-have, polish, alternative approach. | Consider for this iteration or future. |
| ✅ **Strength** | Working well. Explicitly call out to preserve in future iterations. | Keep doing this. |

---

## Gotchas

- **Don't review what wasn't asked.** If someone asks for accessibility feedback, don't also redesign their layout unless invited.
- **Stage mismatch is the most common review failure.** Pixel-level critique on an early wireframe wastes everyone's time. Strategic feedback on a final deliverable is too late.
- **"Looks good" is not a review.** If you can't find anything to improve, you haven't looked hard enough — or you should say so explicitly with what you checked.
- **Compliance reviews require citing the standard.** "This doesn't feel accessible" is a creative opinion. "This fails WCAG 2.1 SC 1.4.3 — contrast ratio is 3.2:1, minimum is 4.5:1" is a standards review.
- **Judgment-based reviews must separate fact from opinion.** "This contract has a broad indemnification clause" (fact) vs. "I wouldn't sign this" (opinion). Present both, label both.
- **The review framework tells you HOW to evaluate. The domain skill tells you WHAT to look for.** If you're reviewing a credit agreement, the review skill structures your evaluation; the legal skill tells you about sacred rights, erroneous payment provisions, and LME blockers.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.

## Entity Resolution

When reviewing material that references companies, people, products, or acronyms, verify entity identity before evaluating claims. "SRSA" could mean multiple things; "Loan IQ" has changed ownership. Misidentified entities produce confident wrong reviews. See research-analysis skill for the full resolution protocol.
