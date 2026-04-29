---
name: source-validation
description: Use this skill whenever the user wants to assess the credibility of an information source — podcasts, newsletters, blogs, analyst firms, books, conference talks, YouTube channels, or any outlet presenting analysis or reporting. Triggers include: 'is this source reliable', 'should I trust this podcast', 'vet this analyst', 'who funds', 'conflicts of interest', 'is this just marketing', 'how captured is', 'who should I listen to on', 'what's the best source for', or any request to separate substance from self-promotion. Also trigger when the user references a specific outlet and asks whether to weight its claims heavily. Do NOT use for vetting primary research (use research-analysis). Do NOT use for fact-checking specific claims (use research-analysis with verification framing). Do NOT use for competitive-brief work (use competitive-brief).
---

# Source Validation

## Core principle

**Conflicts are not disqualifiers. The goal is calibrated ingestion, not purity.** A source can be commercially entangled and still produce true, useful content — the question is whether the substance survives the marketing wrapper. Framing to hold: "good info with some marketing is just business."

What this skill rejects: treating self-description, audience size, "best-of" lists, and peer-promotion as evidence of substance. What this skill demands: third-party validation from sources without commercial alignment to the one being vetted.

## When to fire

- User asks "is X a good source" or "should I trust X"
- User references a recommendation list and asks which entries are actually rigorous
- User is building an information diet and wants to weight sources appropriately
- User encounters a claim that feels like it might be hype and wants to assess
- User has received a recommendation from a commercially-interested party and wants independent assessment
- A recommended episode/post/talk features the creator, founder, or lead of the system being discussed (creator-on-creation conflict — fires even when the venue is otherwise high-quality)

## The three-step workflow

### Step 1: Map conflicts

Identify and name the commercial and social entanglements. Be specific — "the host is a VC" is not enough; name the firm, the portfolio overlap with recent guests, the sponsor list, the employment history. Categories to check:

- **Funding:** sponsors, donors, grants, paid subscriptions, parent company
- **Investments:** host's angel/VC portfolio; overlap with guests
- **Employment:** host's day job at a lab or company being covered
- **Guest-pipeline overlap:** are the same 3–4 companies providing most guests
- **Access relationships:** personal friendships, recurring guest patterns, NDA access
- **Format constraints:** softball interview formats, sponsored episode formats, in-house product demos
- **Network effects:** cross-promotion arrangements, podcast network ownership, donor ecology

### Step 2: Assess whether content survives the conflicts

This is the load-bearing step. A conflict doesn't automatically taint content; the question is whether the substance can be extracted. Test with three probes:

- **Technical density:** Does the conversation contain specifics (architectural decisions, numbers, mechanisms) that would be true regardless of who's selling what? High density = substance survives. Low density = conflict and content are the same thing.
- **Separable claim-vs-pitch:** Can you cleanly distinguish "here is how this system works" from "you should buy this"? If yes, extract the first and discard the second. If the pitch IS the claim (internal product demos, VC partners interviewing portfolio founders about market size), the content doesn't separate.
- **Independent corroboration:** Do claims replicate in sources without the same commercial alignment? Peer-reviewed papers, competing analysts, adversarial journalism, practitioner surveys — these are the checks.

### Step 3: Classify and annotate

Produce an honest per-source verdict with three possible outputs:

- **True:** Content survives conflicts. Extract substance, disclose conflicts, use.
- **Hype:** Content is the pitch; substance is thin or unreplicable. Skip or downgrade.
- **Mixture:** Most real cases. Name which parts survive and which don't. Example: "the technical architecture section is substantive; the market-size framing is sales; the timeline claims should be checked against independent sources."

## Third-party validation heuristics

When assessing an external source, these are what actually count as independent validation:

- Academic citation (papers referencing specific episodes/posts as sources)
- Coverage in outlets with editorial independence from the source being vetted (e.g., MIT Tech Review, FT, Economist, Nature, IEEE Spectrum, Ars Technica, Stratechery on topics unrelated to the host)
- Engagement by critical voices in the field who have no commercial reason to promote the source
- Practitioner surveys with methodology (not vendor-sponsored "top X" lists)
- Cross-referencing by peer sources that are themselves independent

What does NOT count as independent validation:

- The source's own description of itself
- "Best of" lists published by SEO-driven blogs or AI-adjacent companies
- Podcast ranking sites with unclear methodology
- Peer-promotion within an interconnected ecosystem (VC podcasts cross-endorsing VC podcasts)
- Audience size, subscriber count, or download numbers (popularity ≠ rigor)
- Sponsor testimonials or guest testimonials

## Common capture patterns to recognize

- **VC-portfolio promotion:** Host is an investor; guests are from portfolio companies; conflicts disclosed inconsistently or not at all
- **Access journalism:** Host trades critical questions for continued access to executives; format is softball-interview
- **In-house product marketing:** Company-owned podcast where employees demo the company's products as if it were editorial content
- **Lab-sponsored ad-reads on lab-employee episodes:** Sponsorship and content overlap
- **Revolving-door guests:** The same 3–4 firms provide most guests; worldview of those firms becomes the show's frame
- **Framing capture:** Softer than content capture — the show's questions are shaped by the industry's self-concept even when hosts aren't paid. Harder to see and often more consequential.
- **Creator-on-creation:** Guest is the head/founder/lead of the product or system being discussed. Their entire incentive is to make their creation look essential, transformative, or inevitable. The conflict is independent of host capture — it travels with the guest into any venue, including ones with strong adversarial hosts. Substance survives in the descriptive register (how they built it, what decisions they made, what they learned) but rarely in the predictive or evaluative register (this changes the world, this is the future, this replaces X). Strong-host shows mitigate this somewhat through pushback but cannot fully neutralize it because the format is still interview rather than debate. Listen with claim-tagging: "this is how they made a decision" → keep; "this is what the world will look like because of this" → discount.

## Output format

When presenting validation verdicts, structure the response as:

1. **Short verdict** (True / Hype / Mixture) with one-sentence reasoning
2. **Conflicts mapped** (named specifically, not abstractly)
3. **What survives** (specific content types, topics, or guest profiles worth extracting)
4. **What doesn't** (specific framings or claims to discount)
5. **Independent corroboration check** (who else says this; who disputes it)

## Anti-patterns

- **Pass/fail binary:** Real sources are almost always mixture. Don't flatten.
- **Conflict as disqualifier:** An investor host doesn't invalidate a technical interview; it just means the framing needs filtering.
- **Purity theater:** Demanding zero conflicts means accepting zero sources. Calibration beats absolutism.
- **Outsourcing validation:** "Lots of people recommend it" is audience size, not validation.
- **Ignoring format:** A softball format degrades signal even with a strong guest. Format matters as much as host.
- **Moralizing the verdict:** The skill outputs a weighting, not a judgment of the source's character. A captured source is still potentially useful; say so.

## Cross-references

- **research-analysis:** Use when the task is synthesizing claims across sources, not vetting the sources themselves
- **competitive-brief:** Use when vetting competitor messaging specifically
- **review-critique:** Use when critiquing a single artifact rather than an ongoing source
- **research-harvester (passive):** Fires when new source-validation heuristics or capture patterns surface in a conversation
