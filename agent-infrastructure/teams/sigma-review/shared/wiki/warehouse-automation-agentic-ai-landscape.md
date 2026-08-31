# Warehouse Automation & Agentic AI Landscape

Domain-level competitive and technology reference for the intralogistics / warehouse-automation industry (design-build integrators, WES/WCS software, AMR/robotics vendors) and how "agentic AI" claims across that industry hold up against a strict definition. First populated from a Fortna competitive-intelligence review; see [Fortna — Competitive Position and Agentic AI Posture](fortna-competitive-position.md) for company-specific findings.

## Market size and growth dispersion

Published 2026 estimates for "intralogistics automation" range from roughly $31B to $64B depending on scope definition — no single market-research vendor's figure should be treated as ground truth. Better-corroborated across independent sources: warehouse labor shortage/turnover (industry turnover ~36%), e-commerce volume growth, 3PL margin pressure, and reshoring/nearshoring are all pushing automation spend up. Sector order intake grew ~7% in 2025 with ~6% forecast for 2026, but that average masks extreme vendor-level dispersion: Dematic and Toyota Industries Logistics Systems posted 50-65% order-intake growth through the first three quarters of 2025, TGW grew 55%, while AutoStore declined 5% and Honeywell's warehouse division fell 37% before a partial 2025 recovery. **In a market growing in the single digits with that much spread, outcomes are being decided by share capture and execution, not category tailwinds.** [R-fortna-agentic-ci, 2026-08-31]

## Competitor set

Beyond the usual tier-1 shortlist — Dematic (KION), Honeywell Intelligrated, Vanderlande (Toyota Industries subsidiary), Daifuku (global revenue leader, ~$4.6B), SSI Schäfer, Knapp (~$2.1B), Swisslog (KUKA) — a complete competitive set should include TGW Logistics (~$925M), Witron, Beumer Group, and Interlake Mecalux, all comparable scale and frequently benchmarked in trade-press rankings alongside the majors. [R-fortna-agentic-ci, 2026-08-31]

**AutoStore is worth a specific correction if treated as a pure rival:** it is more accurately an integration partner than a direct competitor for design-build integrators — it has published joint case studies as a channel partner (e.g. with Fortna: SK Pharma, South West Healthcare, Alza) even though it also partners with several of those same integrators' direct competitors. [R-fortna-agentic-ci, 2026-08-31]

**Manhattan Associates, Blue Yonder, and Infios** (formerly Körber) sit one layer up the stack (WMS rather than WES/WCS) — design-build integrators both compete with and are frequently implemented alongside them, making them adjacent-layer rather than direct rivals. [R-fortna-agentic-ci, 2026-08-31]

**Structural consolidation:** Toyota Industries folded three separate integrator brands — Vanderlande, Bastian Solutions, and viastore — into a single new unit, Toyota Automated Logistics, effective April 1, 2026, reducing the competitor count by two brands independent of any AI narrative. [R-fortna-agentic-ci, 2026-08-31]

**Honeywell is the sharpest cautionary case in the sector for "does a better AI/software layer save you":** it shipped a new modular warehouse analytics platform, Momentum Core, on April 13, 2026 — and ten days later, April 23, announced it was selling its entire Warehouse & Workflow Solutions division (Intelligrated + Transnorm) to American Industrial Partners. A credible new software platform did not change the strategic outcome. Direct evidence against "a better AI layer alone is sufficient to win in this market." [R-fortna-agentic-ci, 2026-08-31]

## The agentic-AI bar and how the industry scores against it

**Definition used:** systems that plan, act, and iterate using tools toward a goal — as distinct from classic machine-learning/reinforcement-learning optimization, rules-driven real-time optimization, or a chat interface. Applied consistently across vendors, this reclassifies much of the industry's "AI" marketing. [R-fortna-agentic-ci, 2026-08-31]

**Reclassified out — analytics or classic optimization dressed as "AI," not agentic:**
- Dematic Command Center — described in Dematic's own materials as an "Analytics Platform," with "more advanced autonomous and agentic capabilities" explicitly on the future roadmap, not shipped.
- Symbotic's routing capability — reinforcement-learning-based combinatorial pathfinding (same category as classic RL-based dispatch optimization, not agentic).
- GreyOrange DeepNav — reinforcement-learning-based dispatch optimization.
- AutoStore "Intelligence" platform — analytics-branded, agentic architecture underneath unconfirmed. [R-fortna-agentic-ci, 2026-08-31]

**Confirmed survivors, at varying confidence:**
- **Manhattan Associates — strongest case in the market.** Nine named production agents live across its platform, including a specific customer deployment (a wave-coordination agent at Giant Eagle); its NL requirements-to-configuration tool is described by the company as "already using the tool in targeted engagements... not a demo or a roadmap item." Even so, Manhattan's own CFO describes AI revenue contribution as "still a pretty small contribution," with roughly a tenth of the installed base merely "touched" by a pilot or subscription — a commercial-adoption metric, not a value-realization one. Treat as ahead, not as proof agentic AI is already paying off at scale even for the strongest player in the market.
- **Locus Robotics (LocusONE)** — marketed explicitly as agentic, a distinct reasoning layer running a continuous observe-decide-act loop above the dispatch engine, live at 150+ sites — but this rests entirely on vendor self-description, no independent audit or named customer deployment found.
- **Blue Yonder** — narrower than headlines suggest: most agents are advisory recommendation engines for human planners, with one specific narrower example of autonomous action (reprioritizing orders during a disruption). [R-fortna-agentic-ci, 2026-08-31]

**Practical implication for any competitive-intelligence review in this space:** don't take vendor "agentic AI" marketing at face value — check whether the capability plans/acts/iterates with tool use versus being RL-based optimization or a roadmap item. Applying the bar consistently tends to narrow, not widen, the gap between whichever company is being assessed and its closest same-business-model peer, while widening the gap to genuine outliers (Manhattan). [R-fortna-agentic-ci, 2026-08-31]

## Demand-side readiness

Survey data from 2025 puts roughly 52% of fulfillment operations as mostly or fully manual, with only ~4% "highly automated" — the publisher of the leading supply-chain AI adoption survey attributes low adoption specifically to "data readiness and visibility maturity," not lack of interest. Agentic orchestration needs a live, instrumented control surface to act on; most prospects don't have one yet. This is a **demand-side constraint, not a technology-maturity one** — it caps how fast an autonomy-led sales story can land, but it also means the market for "get your operation instrumented and ready" is several times larger than the market for "deploy autonomous agents today." Any vendor's near-term agentic opportunity in this industry is narrower than "catch up on AI broadly" — the market itself isn't ready for the sweeping version of that pitch. [R-fortna-agentic-ci, 2026-08-31]

No evidence was found (across two independent searches, in the source review) that agentic capability is currently a formally scored criterion in intralogistics RFPs. Multi-year capital-project buyers in this market weight trust and delivery track record heavily. [R-fortna-agentic-ci, 2026-08-31]

## Industry failure precedents — where pilots actually break

Three named failures illustrate that this industry's worst outcomes are pilot-to-scale failures, not technology-proof-of-concept failures, and that narrative running ahead of delivered substance is a recurring pattern buyers have now seen play out:
- **Takeoff Technologies** — Chapter 11 in 2024, after failing to expand micro-fulfillment pilot customers past roughly three sites each.
- **Attabotics** — insolvency filing in 2025, days after announcing a marquee retail partnership.
- **Berkshire Grey** — went from a ~$10 SPAC listing to a $1.40 take-private in two years (2021-2023).

**Implication for any business case in this space:** explicitly model the probability that a pilot expands past its first two or three customer sites — that specific transition point, not the tech-proof-of-concept stage, is where this industry's worst-known failures broke down. A buyer base that has watched this pattern is unlikely to reward unproven agentic claims. [R-fortna-agentic-ci, 2026-08-31]

## Architectural principle: where agentic reasoning belongs in industrial control stacks

Agentic reasoning does not belong at the real-time equipment-control layer — sub-100-millisecond response budgets don't fit multi-step reasoning loops; that layer should stay fast, deterministic, and separate. It belongs at the orchestration layer and above, where seconds-to-minutes of slack exist. **But this solves a timing problem, not a safety one:** a fast, reliable execution layer carries out a wrong high-level decision exactly as faithfully as a right one. Any agentic capability touching an irreversible or safety-rated action needs an explicit approval/validation gate between the reasoning layer and the execution layer — architectural separation alone is not sufficient. [R-fortna-agentic-ci, 2026-08-31]

*(See also [AI Agent Reference Architecture — 2026](ai-agent-reference-architecture-2026.md) for the equivalent gateway/guardrail architecture in enterprise software/finserv contexts — a different domain, no direct overlap confirmed, but the general principle of explicit approval gates ahead of consequential agent actions recurs across both.)*

**Regulatory driver:** the EU Product Liability Directive (implementation deadline December 2026) classifies AI software as a "product" subject to strict liability for defects — a live consideration for any EU-market deployment of autonomous decision features in this industry. [R-fortna-agentic-ci, 2026-08-31]

## Bid-surface framing: floor, not premium

Across this industry, agentic-AI capability is best modeled as a **floor, not a premium** on the bid/sales side: the risk being guarded against is being penalized for having *nothing* to say about agentic AI as claims become standard across the industry, not gaining a competitive edge from having *something* to say. Whether it's genuinely decisive in vendor selection (vs. table stakes) is a materially lower-confidence, more provisional estimate than whether it has *some* effect at all. This framing should be checked against fresh evidence for any given company/period rather than assumed to transfer indefinitely. [R-fortna-agentic-ci, 2026-08-31]

## Source basis

Trade and business press (Modern Materials Handling "Top 20 Systems Suppliers," DC Velocity, Robotics 24/7, Logistics Viewpoints, Supply & Demand Chain Executive, Robotics and Automation News, BusinessWire, Fast Company); Interact Analysis (AMR/order-fulfillment deployment data, 2025 order-intake dispersion by vendor); company disclosures (Manhattan Associates Q2 FY2026 earnings call, Momentum 2026 conference materials); industry surveys (Gartner 2026 CIO/Tech Executive Survey, Gartner Hype Cycle for Supply Chain Execution Technologies, McKinsey "The State of AI" 2026, Sage "2026 State of Supply Chain," MIT NANDA "The GenAI Divide" 2025, First Analysis July 2026); legal/regulatory (EU Product Liability Directive client alerts — Foley & Lardner, Baker McKenzie, Squire Patton Boggs; CISA 2026 agentic-AI deployment risk guidance); named case coverage (Takeoff Technologies, Attabotics, Berkshire Grey). Full source list and inline citations in the synthesis archive: `~/.claude/teams/sigma-review/shared/archive/2026-08-31-fortna-agentic-ci-synthesis.md`. [R-fortna-agentic-ci, 2026-08-31]
