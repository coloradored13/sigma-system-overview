---
name: Skills integration v3
description: 29 claude.ai skills installed to ~/.claude/skills/ with agent boot integration, progressive disclosure, and socratic-grill handoff
type: project
originSessionId: d7eadd85-5bd2-4be5-8e47-6169aa3c139b
---
Installed claude.ai skill ecosystem v3 into Claude Code (26.4.11). 29 skills across 7 categories, coexisting with 11 sigma skills + mcp-builder.

**Why:** Skills provide structured reference material for agents during sigma-review/build. Previously agents relied on memory-only domain knowledge. Skills give them curated frameworks (research-analysis, review-critique) and domain references (loan-agency 3-tier, legal, engineering).

**How to apply:** Agents load skill routers at boot step 2a (max 2, ~100 lines each), then read specific reference files during Work phase (progressive disclosure). Skills are T1 sources (user-authored). Skill + independent research = strongest provenance.

## Categories
- 7 capability: research-analysis, structured-writing, review-critique, process-design, data-analysis, planning-prioritization, reporting
- 5 domain: loan-agency (3-tier, 29 refs), legal, engineering, finance-accounting, bio-research
- 3 orchestrator: product-ops, design-ops, competitive-brief
- 4 execution-layer: query, visualize, financial-close, bio-tools
- 2 behavioral: socratic-grill, negotiation-coach
- 6 passive: passive-bootstrap, skill-improver, assumption-surfacer, skill-identifier, memory-compiler, research-harvester
- 2 protocol: sigmacomm (ΣComm decoder), persistent-wiki (06b compilation)

## Integration points
- _template.md step 2a: agents load skill routers at boot
- 00-preflight.md Step 8: socratic-session conditional for warm Q/H/C decomposition
- INDEX.md: full categorized inventory with agent-skill mappings
- Source tagging: |source:skill(loan-agency/qr-operational-mechanics):T1|
