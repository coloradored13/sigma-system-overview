---
name: research-analysis
description: >
  Use this skill whenever the user wants to research, analyze, compare, or synthesize
  information across any domain. Triggers include: 'competitive analysis', 'user research',
  'market research', 'account research', 'research synthesis', 'knowledge synthesis',
  'comp analysis', 'benchmark', 'landscape analysis', 'SWOT', or requests to compare
  competitors, synthesize interview findings, explore a market, profile an account or
  contact, analyze compensation data, or investigate a topic across multiple sources.
  Also use when the user says 'analyze this', 'research this', 'what does the competitive
  landscape look like', 'synthesize these findings', 'compare X and Y', or 'what do we
  know about [company/person/market]'. Do NOT use for SQL, dashboards, or statistical
  tests (use data-analysis). Do NOT use for writing deliverables from research (use
  structured-writing). Do NOT use for financial statements (use finance-accounting).
---

# Research & Analysis

Structured approaches to research, comparison, and synthesis across any domain.

## Rigor Scaling

Before starting, assess the task. Not all research needs the same discipline.

| Signal | Level | What Changes |
|---|---|---|
| Quick factual lookup, single source sufficient, low stakes | **Lookup** | Just answer. No framework needed. |
| Multi-source research, comparison, synthesis, or anything informing a decision | **Standard** | Apply routing table below. Resolve entities before searching. Tag key claims with source quality. Note gaps. |
| High-stakes research informing strategy, investment, hiring, or market entry — OR user says "be rigorous", "high confidence", "I need to be sure" | **Rigorous** | Full analytical discipline (see below). |

### Rigorous Mode Protocol

When rigorous research is warranted, apply these before presenting findings:

**1. Decompose first.** Break the question into 3-5 independent sub-questions.
Don't research a blob — research specific, answerable pieces.

**2. Entity resolution.** Before any searches fire, resolve ambiguous names and entities bidirectionally:
- Person → company, role, handles, related entities ("Dario Amodei" → Anthropic CEO, @DarioAmodei)
- Company → key people, products, subsidiaries, common abbreviations ("SRSA" → SRS Acquiom)
- Product → maker, competitors, version history ("Loan IQ" → Finastra, formerly Misys)
- Acronym → full name AND full name → acronym ("SOFR" → Secured Overnight Financing Rate)
- If the entity is ambiguous (multiple possible matches), resolve it BEFORE searching. Ask the user if needed.
This prevents searching for the wrong entity, missing relevant results, or conflating similarly-named things.

**3. Source tier every claim.**
- T1: Peer-reviewed, regulatory filing, official data, primary source code
- T2: Industry report, corroborated company data, established journalism
- T3: Blog post, PR, advocacy, single-source claim
- Rule: Load-bearing conclusions built on T3 alone get flagged explicitly

**4. Assume-wrong check on top conclusions.** For your 2-3 highest-conviction findings:
- State the finding
- Assume it's wrong — what would that mean?
- Name the strongest counter-argument
- Reconcile: does the finding hold, weaken, or change?
- Present the reconciled position, not just the initial one

**5. Confidence and gaps.** For each key conclusion:
- State your confidence (low / medium / high) with what drives it
- Name what evidence would change your mind
- Name what you couldn't find or verify

**6. Anti-findings.** Explicitly state what you looked for and did NOT find.
Absence of evidence is itself a finding when documented.

The goal: research you'd feel confident presenting to someone who will make a
real decision based on it. Not sigma-review depth, but more than "I searched and here's what I found."

---

## Routing

| If the user wants to... | Read |
|---|---|
| Compare competitors, analyze market positioning, feature matrices | `references/competitive-analysis.md` |
| Synthesize user research — interviews, surveys, feedback — into insights | `references/user-research-synthesis.md` |
| Plan or conduct user research — interview guides, usability tests | `references/user-research.md` |
| Profile and explore a dataset before analysis | `references/data-exploration.md` |
| Synthesize information from multiple internal or external sources | `references/knowledge-synthesis.md` |
| Design a research strategy — what sources, what approach, what sequence | `references/search-strategy.md` |
| Gather competitive intelligence for sales positioning | `references/competitive-intelligence.md` |
| Research an account, company, or contact | `references/account-research.md` |
| Benchmark compensation, analyze pay equity | `references/comp-analysis.md` |

## Gotchas

- **Rigor should match stakes, not effort.** A quick competitive scan doesn't need dialectical bootstrapping. A market entry analysis does. If unsure, ask: "Is someone making a decision based on this?"
- Research and analysis are different activities. Research = gathering information. Analysis = making sense of it. Do both.
- Competitive analysis should focus on positioning implications, not just feature checklists.
- User research synthesis should preserve participant voice — don't sanitize findings into what stakeholders want to hear.
- Account research should be actionable — "here's what to say in the meeting" not just "here's what I found."
- Always identify what you DON'T know. Gaps in research are as important as findings.
- **T3 sources aren't invalid — they're just not load-bearing.** A blog post can provide a lead. It can't be the foundation of a strategic conclusion.
- **"I found 5 sources that agree" ≠ high confidence** if they're all citing the same original source. Trace the citation chain.
- **The assume-wrong check is not theater.** If you can't articulate a genuine counter-argument, either the finding is trivially true (doesn't need rigorous treatment) or you haven't looked hard enough.

## Pre-Step

If the user hasn't fully articulated what they need researched — vague scope, unclear questions, unstated assumptions — suggest socratic-grill Extract mode first: "Want me to ask you some questions to scope this before I start researching? It usually produces more targeted results." The socratic-grill session produces a Q/H/C decomposition that feeds directly into rigorous-mode research.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
