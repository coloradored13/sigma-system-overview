# Skills Index (ARCHIVED 2026-04-15)

> **This file is documentation-only.** Claude Code's native skill router (SKILL.md frontmatter
> descriptions) handles all skill matching at runtime. The agent-skill mapping below was never
> operationalized — agents get domain knowledge from their own memory and research. See the
> agent template's "Skill Access" section for the lightweight opt-in path.
>
> To add a new skill: create `~/.claude/skills/{name}/SKILL.md` with frontmatter (name, description).
> Claude Code discovers it automatically from the description field.

# Skills Index

Categorized inventory of available Claude Code skills. Two categories: **capability** skills (triggered by what you're doing) and **domain** skills (triggered by what you're talking about). They compose — capability provides the HOW, domain provides the WHAT.

Skills must stay flat at `~/.claude/skills/{name}/SKILL.md` for Claude Code discovery.

## Sigma (Multi-Agent Team Orchestration)
| Skill | Description |
|-------|-------------|
| sigma-review | ANALYZE mode — multi-agent team review (phase-based) |
| sigma-build | BUILD mode — multi-agent implementation with plan→challenge→build→review |
| sigma-audit | Independent process quality audit of a sigma-review |
| sigma-evaluate | Multi-agent rubric evaluation of completed analysis |
| sigma-feedback | Post-review calibration loop (datum/concept tracks) |
| sigma-research | Refresh domain research for sigma-review agents |
| sigma-retrieve | Agentic RAG pipeline for structured retrieval |
| sigma-optimize | Multi-agent evolutionary prompt optimization |
| sigma-dream | Memory consolidation cycle (dedup, prune, promote) |
| sigma-single | Enhanced single-instance analysis |
| sigma-init | Initialize sigma infrastructure for a project |

## Capability Skills (verb-triggered — what you're doing)
| Skill | Triggers On | Modes/Index | Agent Relevance |
|-------|-------------|-------------|-----------------|
| research-analysis | analyze, research, synthesize, compare, benchmark | — | product-strategist, macro-rates, energy-market, geopolitical, economics |
| structured-writing | write, draft, create, compose, spec, brief | — | technical-writer, product-strategist |
| review-critique | review, critique, audit, validate, assess, triage | creative / standards / judgment | code-quality-analyst, product-designer, ux-researcher, security-specialist |
| process-design | document process, runbook, checklist, SOP, workflow | — | tech-architect, implementation-engineer |
| data-analysis | SQL, dashboard, chart, dataset, statistical test | — | portfolio-analyst, economics-analyst |
| planning-prioritization | roadmap, sprint, prioritize, forecast, scope | — | product-strategist, tech-architect |
| reporting | status report, standup, digest, briefing, summary | — | technical-writer, product-strategist |
## Behavioral Skills (mode-triggered — how you engage)
| Skill | Triggers On | Modes | Agent Relevance |
|-------|-------------|-------|-----------------|
| socratic-grill | grill me, interview me, stress test, prepare me for | socratic / grill / prepare | pre-review step, standalone |
| negotiation-coach | negotiate, difficult conversation, pushback, de-escalate | draft / response / prep / de-escalation | standalone |

## Passive Skills (always-on background — no explicit trigger)
| Skill | What It Watches For | Fires When |
|-------|--------------------|-----------| 
| passive-bootstrap | **LOAD FIRST** — bootstraps the four passives below into active context | Start of every conversation |
| skill-improver | Routing misfires, trigger overlaps, rigor misjudgments, cross-ref gaps | Skill system is active and a meaningful improvement surfaces |
| assumption-surfacer | Unexamined assumptions accumulating in substantive discussion | 3+ assumptions pile up, or one is load-bearing |
| skill-identifier | Repeated workflows, domain gaps, skill-shaped patterns | Pattern recurs with structure and value |
| memory-compiler | Decisions, position changes, new domain knowledge, project milestones | End of substantive session where something new was established |
| research-harvester | Domain knowledge flowing through info intake (web search, doc analysis) | Specific enough to draft a concrete skill update |

## Protocol Skills (notation/compilation — loaded on demand)
| Skill | Purpose | Triggers On |
|-------|---------|-------------|
| sigmacomm | ΣComm compressed notation decoder | Reading/writing CLAUDE.md, memory files, agent messages |
| persistent-wiki | Session-to-wiki compilation (06b pattern) | After substantive sessions producing reusable knowledge |

## Orchestrator Skills (workflow-triggered — chains capability + domain skills)
| Skill | Triggers On | What It Chains | Agent Relevance |
|-------|-------------|----------------|-----------------|
| product-ops | write a spec, PRD, sprint planning, metrics review, stakeholder update | structured-writing, planning-prioritization, data-analysis, reporting, research-analysis | product-strategist |
| design-ops | critique design, WCAG, accessibility audit, UX copy, design system, handoff | review-critique, structured-writing, process-design, research-analysis | product-designer, ux-researcher |
| competitive-brief | competitive analysis, battlecard, positioning, feature comparison, win/loss | research-analysis, structured-writing, negotiation-coach, review-critique | product-strategist |

## Execution-Layer Skills (hands-on complement to a parent skill)
| Skill | Parent Skill | Triggers On | What It Adds |
|-------|-------------|-------------|-------------|
| query | data-analysis | write a query, SQL, explore dataset, profile table, Snowflake, BigQuery, Postgres | SQL execution, data profiling, statistical test mechanics |
| visualize | data-analysis | build a dashboard, create a chart, plot, graph, Chart.js, matplotlib, plotly | Chart creation, dashboard building, visual output |
| financial-close | finance-accounting | journal entry, reconciliation, month-end close, SOX testing, close checklist | Close workflow execution, JE standards, reconciliation process |
| bio-tools | bio-research | scvi-tools, scVI, Nextflow, nf-core, scanpy, Allotrope, FASTQ, h5ad | Tool-specific pipeline execution, instrument data conversion |

## Domain Skills (noun-triggered — what you're talking about)
| Skill | Triggers On | Tier Structure | Agent Relevance |
|-------|-------------|----------------|-----------------|
| loan-agency | loan admin, SOFR, waterfalls, credit agreements, KYC | T1 quick-ref / T2 operational / T3 deep docs + strategic | loan-ops-tech-specialist, regulatory-licensing-specialist |
| legal | contracts, NDA, compliance, regulatory, risk | — | regulatory-analyst, regulatory-licensing-specialist |
| engineering | architecture, code review, debug, deploy, system design | — | tech-architect, implementation-engineer, code-quality-analyst |
| finance-accounting | GAAP, journal entries, SOX, reconciliation, close | — | portfolio-analyst |
| bio-research | scRNA-seq, Nextflow, Allotrope, bioinformatics | — | (domain-specific, no standing agent) |

## Shared Modules (referenced by other skills, not standalone)
| Module | What It Provides | Referenced By |
|--------|-----------------|---------------|
| analytical-hygiene | Outcome 1/2/3 forcing, source tiers T1/T2/T3, dialectical bootstrapping | research-analysis, review-critique, data-analysis, sigma-review agent template |
| prompt-decomposition | Q[]/H[]/C[] extraction from user requests | socratic-grill → sigma-review preflight, structured-writing, planning-prioritization |

---

## Agent Boot Integration

### How agents use skills

During boot (step 2 in agent template), after loading memory, agents check for relevant skills:

```
2→memory.md — identity+findings+calibration
2a→skill check: match agent domain against Skills Index "Agent Relevance" column
   → load SKILL.md router (NOT full references — progressive disclosure)
   → router tells agent which reference files exist for their domain
   → agent reads specific reference files ONLY when needed during analysis
```

### Progressive disclosure for agents (3-tier)

```
ALWAYS loaded at boot:  SKILL.md router (~100 lines, routing table + gotchas)
Loaded when relevant:   Quick-reference files (Tier 1, 2-4KB each)
Loaded only for depth:  Full reference files (Tier 2/3, varies)
```

Example: loan-ops-tech-specialist boots for a payment processing review:
```
Boot:    loan-agency/SKILL.md (router — sees all 27 reference files listed)
Tier 1:  qr-operational-mechanics.md (day-count table, waterfall summary, SOFR quick-ref)
         → sufficient for most findings
Tier 2:  loan-agency-payment-processing.md (full workflow with controls)
         → loaded only if agent needs step-by-step payment processing detail
Tier 3:  Doc3_Operational_Mechanics_Revised.md (78KB full domain doc)
         → loaded only for deep questions about SOFR methodology or payment system specs
```

### Skill-agent mapping

| Agent | Primary Skills | Load At Boot (router only) |
|-------|---------------|---------------------------|
| loan-ops-tech-specialist | loan-agency, process-design | loan-agency |
| regulatory-licensing-specialist | loan-agency (strategic), legal | loan-agency, legal |
| product-strategist | product-ops, research-analysis, planning-prioritization, competitive-brief | product-ops, research-analysis |
| tech-architect | engineering, process-design | engineering |
| implementation-engineer | engineering, process-design | engineering |
| code-quality-analyst | review-critique, engineering | review-critique |
| product-designer | design-ops, review-critique (creative mode) | design-ops |
| ux-researcher | design-ops, research-analysis (user research) | design-ops |
| technical-writer | structured-writing, reporting | structured-writing |
| portfolio-analyst | data-analysis, finance-accounting | data-analysis |
| security-specialist | engineering, review-critique (standards mode) | engineering |
| reference-class-analyst | research-analysis, data-analysis | research-analysis |
| cognitive-decision-scientist | review-critique (judgment mode) | review-critique |

### Capability skill composition during reviews

When an agent's task involves BOTH a capability and a domain:
```
loan-ops-tech-specialist reviewing a credit agreement's payment waterfall:
  → review-critique (judgment mode) provides the evaluation framework
  → loan-agency provides the domain knowledge (waterfall rules, day-count, controls)
  → agent reads review-critique/references/judgment-review.md for HOW to evaluate
  → agent reads loan-agency/references/qr-operational-mechanics.md for WHAT to look for
```

---

## Trigger Conflict Resolution

When multiple skills match a request, apply these rules:

| Ambiguous Trigger | Resolution | Rationale |
|-------------------|------------|-----------|
| "research" / "analyze" | If multi-agent context → sigma-review; if single-instance → research-analysis | sigma-review is team orchestration, research-analysis is solo |
| "review this" | If process audit → sigma-audit; if code → review-critique (standards); if design → design-ops | Match the OBJECT being reviewed, not the verb |
| "write a spec" / "PRD" | product-ops (chains structured-writing) ¬ standalone structured-writing | product-ops adds planning context around the writing |
| "SQL" / "query" | query (execution-layer) → loads data-analysis parent automatically | query is the hands-on complement |
| "chart" / "dashboard" | visualize (execution-layer) → loads data-analysis parent automatically | visualize is the hands-on complement |
| "optimize prompts" | sigma-optimize ¬ sigma-review | sigma-optimize is experimental search, not analysis |
| "journal entry" / "reconciliation" | financial-close (execution-layer) → loads finance-accounting parent | financial-close is the hands-on complement |

The skill-improver passive skill also watches for routing misfires and flags them.

---

## Adding skills

### New capability skill
1. Create `~/.claude/skills/{name}/SKILL.md` with frontmatter (name, description)
2. Add to Capability Skills table above with triggers, modes, and agent relevance
3. If agents should load it: update agent-skill mapping table

### New domain skill
1. Create `~/.claude/skills/{name}/SKILL.md` with frontmatter + references/ if multi-tier
2. Add to Domain Skills table above with triggers, tier structure, and agent relevance
3. If agents should load it: update agent-skill mapping table

### New shared module
1. Create `~/.claude/skills/{name}/` with the module content
2. Add to Shared Modules table
3. Update referencing skills to point to the module
