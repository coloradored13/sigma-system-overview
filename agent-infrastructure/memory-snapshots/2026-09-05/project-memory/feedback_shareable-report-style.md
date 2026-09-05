---
name: shareable-report-style
description: "For shareable deliverables (docx, brief, report, summary) — strip methodology, write for cold readability + non-AI voice, cite every claim with comprehensive Sources section."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef134d42-2eb7-4ad9-82dd-d18d70051009
---

When the user asks for a shareable deliverable (docx report, brief, executive summary, customer-facing analysis), apply all three filters by default.

**Filter 1: No methodology surface.** Strip all internal notation and process artifacts. No round numbers (R1/R2/R3), no agent names (DA, macro-rates-analyst, etc.), no notation (BELIEF[], DB[], F[], CAL[], PM[], DISCONFIRM[], §2 hygiene checks, T1/T2/T3 source tiers), no chain-evaluator references, no convergence/exit-gate/circuit-breaker language. The reader gets findings and conclusions, not the recipe that produced them. External-name sources are not methodology (e.g., "Stanford Search Fund Study" stays as a citable source).

**Filter 2: Cold readability + non-AI voice.** Specific tells to avoid: em-dash overuse (target 1 per 15+ sentences in body), "approximately"/"roughly" hedge (keep only where genuinely approximate), "delve into", "comprehensive", "robust", "leverage" as verb, "navigate the landscape", "in essence", "moreover"/"furthermore", "paramount"/"pivotal", "tapestry"/"plethora", "this is not just X but Y", "not merely". Vary sentence openings (not always "The X is Y"). Mix sentence lengths. Fragments are allowed for emphasis ("Closed." "Open and early."). One thought per paragraph is fine.

**Filter 3: Sources cited inline + comprehensive Sources section at end.** Every numeric and category-level claim gets a brief inline citation against the named source. Sources section at end organized by source type (federal/government, industry research, trade media, company filings, single-source/directional, practitioner). Single-source magnitudes explicitly flagged as directional only; not used as load-bearing for ranking. Include a brief "Note on triangulation" explaining the standard.

**Why:** From R-2026-05-17-k-shape-opportunities deliverable session. User flagged each filter explicitly: "do not mention any methodology, it is superfluous to the content" + "focus on cold readability and that it doesn't sound 'too AI'" + "claims and numbers should be backed up by references found during the analysis." All three apply jointly, not individually.

**How to apply:** Default ON whenever the user asks for a shareable artifact. Run a final audit pass before saving: em-dash density check, AI-tell phrase scan, citation coverage check on load-bearing claims.

Related: [[project_persona-audit]] (the personas-audit deliverable also benefited from cold-readability discipline).
