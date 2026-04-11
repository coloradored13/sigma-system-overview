---
name: bio-research
description: >
  Use this skill whenever the user works on bioinformatics or scientific research
  workflows. Triggers include: 'single-cell RNA', 'scRNA-seq', 'scvi-tools',
  'Nextflow', 'Allotrope', 'bioinformatics', 'genomics QC', 'scientific analysis',
  'instrument data', 'pipeline development', or requests involving genomics pipelines,
  lab data processing, or scientific problem selection. Do NOT use for general data
  analysis or statistics (use data-analysis). Do NOT use for general process
  documentation (use process-design).
---

# Bio-Research

Bioinformatics and scientific research workflows.

## Routing

| If the user wants to... | Read |
|---|---|
| Convert instrument data to Allotrope format | `references/instrument-data-to-allotrope.md` |
| Develop or modify Nextflow pipelines | `references/nextflow-development.md` |
| Select and scope a scientific research problem | `references/scientific-problem-selection.md` |
| Use scvi-tools for single-cell analysis | `references/scvi-tools.md` |
| QC single-cell RNA sequencing data | `references/single-cell-rna-qc.md` |
| Get started with the bio-research workflow | `references/start.md` |

## Gotchas

- Bioinformatics pipelines should be version-controlled and reproducible. Document every parameter.
- QC should happen before analysis — never skip quality checks on sequencing data.
- Allotrope conversion requires validating output against the original instrument data.

## When the Skill Doesn't Cover It

If you load this skill and the reference material does not answer the question — do NOT guess, generalize, or answer from general knowledge alone. Instead:

1. **Say what the skill covers and where the gap is.** "The loan-agency references cover payment waterfalls but not CLO compliance testing mechanics."
2. **Trigger a rigorous web search.** Search for current, authoritative sources. Apply source tiers: T1 (official/peer-reviewed) > T2 (industry reports) > T3 (blogs/PR).
3. **Flag the provenance.** "This answer comes from web research, not the skill references — [source, tier]."
4. **Suggest a skill update if the gap is recurring.** "This came up before — worth adding to the skill?"

The worst outcome is a confident wrong answer built on stale knowledge. A searched answer with source attribution is always better than an unsourced guess.
