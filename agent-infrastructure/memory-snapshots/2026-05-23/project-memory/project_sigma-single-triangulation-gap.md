---
name: sigma-single-triangulation-gap
description: "Sigma-single + sigma-retrieve has aggregator-tier sources (Mordor, Future Market Insights, Sacra) doing load-bearing work on live market sizing. Fix is sigma-review's triangulation policy: single-source figures flagged as directional, excluded from ranking."
metadata: 
  node_type: memory
  type: project
  originSessionId: 56c20e9b-53c2-4b9d-932a-e2a541dee18f
---

Gap identified in 26.5.17 K-shape benchmark (sigma-single scored 20/24, see [[reference_sigma-review-benchmark-2026-05-17]]).

**What works in sigma-single's current source pipeline:**
- Historical retrieval is strong. The five-case shovel-metaphor demolition (1849, dot-com, mobile/Web2, D2C, AI rush) pulled the right cautionary data — Cisco 88% drawdown / 25.7-year recovery, JDSU 99.8%, Sun $200B→$7B. This is sigma-retrieve at its best.
- Tier-1 anchors are present and correctly used (BLS, NY Fed, Stanford GSB Case E-870, Goldman Sachs Research).

**What fails:** Live market-size figures driving opportunity ranking come from aggregator-tier sources:
- Mordor Intelligence (medspa, pet hotels, concierge medicine, luxury concierge CAGRs)
- Future Market Insights (longevity clinic infrastructure, GLP-1 nutritional support)
- Sacra (CoreWeave revenue, Character.AI valuation, BetterUp)
- Sharpsheets, Franchise Direct (FDD data aggregators)

These sources are flagged honestly in sigma-single's "What this report doesn't know" section, but they're not down-weighted in the actual opportunity ranking. The T1/T2/T3 source-tiering protocol catches authority and recency but doesn't filter aggregators hard enough when their figures drive load-bearing ranking decisions.

**Fix from sigma-review's revision (Section 12 triangulation note):**
> "Where this report makes a load-bearing claim, the claim is supported by at least two of the source categories above wherever feasible... Where a magnitude rests on a single source whose figure cannot be independently corroborated — for example, the FutureMarketInsights GLP-1 sizing or the 2035 pet care projection — the report flags the figure as directional only and does not use it as load-bearing for opportunity ranking."

**How to apply:**
- Add explicit single-source-flagging step to sigma-single's stage protocol (similar to Stage 3.5 Source Bias Probe from source-validation, but for triangulation rather than capture/conflict bias)
- When ranking opportunities, exclude figures from single aggregator sources from the ranking math; use them only as directional indicators
- Require ≥2 source categories for load-bearing magnitudes; flag explicit single-source cases

This is a transferable upgrade from sigma-review → sigma-single. Source-validation skill ([[skills + hooks]] !source-validation entry) already integrated as Stage 3.5; triangulation discipline would be Stage 3.6 or a refinement of Stage 3.5.

Related: [[reference_sigma-review-benchmark-2026-05-17]], [[project_skills-architecture]].
