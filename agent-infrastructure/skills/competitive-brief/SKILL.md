---
name: competitive-brief
description: >
  Use this skill when the user wants to research, compare, or position against
  competitors. Triggers include: 'competitive analysis', 'competitive brief',
  'battlecard', 'how do we compare to', 'competitive landscape', 'competitor
  research', 'positioning analysis', 'SWOT', 'differentiation', 'feature comparison',
  'win/loss analysis', 'how do they stack up', 'who are our competitors', or
  requests to research competitors for any purpose — product strategy, sales
  enablement, marketing positioning, investor decks, or executive briefings.
  Also trigger when the user names a specific company and asks how they compare,
  or when competitive context is needed for a strategic decision. Do NOT use for
  general market research without a competitive framing (use research-analysis).
  Do NOT use for account-level prospect research without competitive context
  (use research-analysis → account-research).
---

# Competitive Brief

Research competitors and produce actionable intelligence — battlecards, positioning
matrices, gap analyses, and strategic recommendations. This workflow chains
research-analysis for the investigation with structured-writing for the output.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick compare — "how does X compare to Y on pricing" | **Quick** | Direct answer. Source it. No framework. |
| Standard brief — "competitive analysis of our space", "build a battlecard" | **Standard** | Apply the full workflow below. Cover positioning, features, pricing, gaps. |
| Strategic — informs product strategy, board presentation, or M&A. OR user says "thorough", "comprehensive" | **Rigorous** | Full research-analysis rigorous protocol. Multiple source tiers. Verify claims. Include confidence levels. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Deep research on a specific competitor or market landscape | Load `research-analysis` for investigation methodology |
| A written deliverable — battlecard, one-pager, positioning doc | Load `structured-writing` for output format |
| Competitive positioning for a sales conversation | Load `negotiation-coach` for tactical framing |
| Feature comparison matrix with scoring | Load `review-critique` (standards-based mode) for evaluation framework |
| Competitive landscape as input to product roadmap | Load `planning-prioritization` → reference `roadmap-management` |
| Interactive HTML battlecard with tabs and comparison matrix | Load `research-analysis` → reference `competitive-intelligence` for HTML output spec |
| Competitive context for a product spec or strategy doc | Load `product-ops` for PM workflow context |

## Workflow

1. **Define the frame.** Who are the competitors? (Direct, adjacent, aspirational.) What's the comparison axis? (Features, pricing, positioning, GTM, technical architecture.)
2. **Research.** Use `research-analysis` methodology — entity resolution first, then web search with source tiers. Verify claims: competitor marketing ≠ competitor reality. Cross-reference product pages against reviews, case studies, and technical docs.
3. **Structure the output.** Standard competitive brief includes:
   - **Overview**: Who they are, what they do, who they serve.
   - **Positioning**: How they describe themselves vs. how the market sees them.
   - **Strengths**: What they do well — be honest, not dismissive.
   - **Weaknesses**: Where they fall short — be specific, not vague.
   - **Feature comparison**: Matrix with your product and competitors on key capabilities.
   - **Pricing**: What's public. Note what's not. Date-stamp everything.
   - **Gaps & Opportunities**: Where you can differentiate. Where they're ahead.
   - **Recommended actions**: What to do with this intelligence.
4. **Tailor for audience.** The same research produces different deliverables:
   - **Sales battlecard**: Talk tracks, objection handling, landmine questions. Load `competitive-intelligence` reference.
   - **Product strategy doc**: Gap analysis, positioning implications, roadmap input. Load `structured-writing`.
   - **Board slide**: Market position, competitive moat, risk factors. Keep it to one page.
   - **Team briefing**: What changed, what matters, what to do differently.

## Gotchas

- **Competitor marketing is not ground truth.** "AI-powered" on their website doesn't mean their product uses AI meaningfully. Verify with reviews, case studies, technical docs, and job postings.
- **Be honest about competitor strengths.** A dismissive competitive brief is useless — the sales team will get embarrassed when the prospect knows more than they do. Your own credibility depends on acknowledging where competitors are genuinely ahead.
- Feature parity ≠ capability parity. Having a feature checkbox doesn't mean the implementation is good. Depth and quality matter more than presence.
- Pricing intelligence gets stale fast. Always date-stamp and note confidence level (public pricing page vs. rumored vs. inferred from deal intel).
- **Don't just list — interpret.** "They launched X" is observation. "They launched X, which signals they're moving upmarket, which threatens our enterprise pipeline" is intelligence. The interpretation is the value.
- When doing rigorous-mode competitive work, apply the assume-wrong check from `research-analysis`: for your top 2-3 conclusions about competitive positioning, assume you're wrong and name the strongest counter-argument.
- Win/loss patterns are the highest-signal competitive data. If available, they outweigh any amount of website research.

## Pre-Step

If the competitive frame is vague — "do a competitive analysis" without specifying competitors, comparison axes, or audience — ask before researching: "Who specifically are we comparing against, what dimensions matter most, and who's the audience for this?" Bad scoping produces broad, shallow output that doesn't help anyone make a decision.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The competitive research covers feature comparison but not patent landscape analysis."
2. **Search.** Authoritative sources. T1 (SEC filings, official docs, product pages) > T2 (analyst reports, G2/Capterra reviews) > T3 (blog posts, PR).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
