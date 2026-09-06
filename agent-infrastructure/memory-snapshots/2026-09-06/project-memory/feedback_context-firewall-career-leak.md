---
name: Context firewall career leak
description: 5yr-PM-strategy review leaked personal career context through prompt to multiple agents (TIA, CDS) — prompt understanding must separate task from personal framing
type: feedback
---

5yr-PM-strategy review contaminated at least 2 agents (tech-industry-analyst, cognitive-decision-scientist) with personal career context (PM viability, C4 family, career framing). Same bug found independently in both during memory audit.

**Why:** Prompt understanding didn't separate "analyze PM career viability" (the analytical task) from "this is my career" (personal context that should have been firewalled). If Q/H/C included personal framing, every agent got it at spawn.

**How to apply:** Phase-based prompt understanding (step 8) now has explicit challenge/clarify gates. When user prompt contains personal context, lead must strip it before writing to workspace ## prompt-understanding. Test: "would an agent need to know this is the USER's career to do the analysis?" No → strip it.
