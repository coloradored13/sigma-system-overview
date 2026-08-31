---
name: chatgpt-dr-hedging
description: "ChatGPT deep research produces smooth, low-conviction, 'consider these lanes' deliverables on opportunity-scan tasks. Native characteristic, not editorial smoothing. Tool-selection reference."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 56c20e9b-53c2-4b9d-932a-e2a541dee18f
---

ChatGPT with deep research, on opportunity-scan / landscape-analysis tasks, produces a deliverable characterized by:

- Disclaimers framing output as "a map of opportunity lanes, not a final recommendation"
- No named public-equity positions
- No falsification benchmarks
- No specific avoid-this calls
- Heavy directional hedging language ("forecasts are directional inputs, not guarantees")
- Generic synthesis conclusions ("the strongest opportunities are not necessarily glamorous")
- Strong source hygiene (claim-to-source map appendix) but citations support directional claims rather than being integrated into argument

**Why this matters:** Initially assumed this was downstream editorial smoothing on top of stronger raw analysis. Wrong. It is the default output. Confirmed by the 26.5.17 benchmark where ChatGPT DR scored 16/24 on a 24-point rubric, lowest among the four analytical reports (Gemini Pro DR at 11 was a different failure mode — profile-anchoring + low-quality sources).

**How to apply:**
- For tasks where deliverable value is conviction (named positions, hard avoid calls, falsification criteria), ChatGPT DR is a poor tool choice
- For tasks where deliverable value is coverage (broad-but-shallow map, claim-to-source hygiene, opportunity directory), ChatGPT DR is appropriate
- Sigma-review at 24/24 and Desktop Claude DR at 22/24 both outperform ChatGPT DR on conviction-required tasks
- One distinctive contribution worth borrowing: the 5-filter "Opportunity Screen" (Buyer capacity / Urgency / Trust premium / Fragmentation / Service-first wedge) was a clean framework absent from the other reports

Related: [[reference_sigma-review-benchmark-2026-05-17]].
