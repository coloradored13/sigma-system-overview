---
name: bio-tools
description: >
  Use this skill for specialized bioinformatics tool workflows — running scvi-tools
  for single-cell analysis, executing Nextflow/nf-core pipelines, converting instrument
  data to Allotrope format, performing single-cell RNA QC, or setting up a bio-research
  environment. Triggers include: 'scvi-tools', 'scVI', 'scANVI', 'totalVI', 'PeakVI',
  'MultiVI', 'Nextflow', 'nf-core', 'rnaseq pipeline', 'single-cell QC', 'scanpy',
  'Allotrope', 'ASM JSON', 'instrument data conversion', 'FASTQ', 'h5ad', 'GEO',
  'SRA', 'batch correction', 'data integration', 'CITE-seq', 'multiome', 'ATAC-seq',
  or requests to run specific bioinformatics tools and pipelines. This is the execution
  complement to bio-research — bio-research provides scientific strategy, this skill
  provides tool-specific protocols. Do NOT use for scientific strategy or problem
  selection (use bio-research). Do NOT use for general data analysis on non-biological
  data (use data-analysis).
---

# Bio Tools

Specialized bioinformatics pipelines and tool workflows. This is the execution
layer for bio-research — that skill provides scientific strategy and problem
selection; this skill provides the tool-specific protocols.

## Relationship to bio-research

These two skills compose rather than compete:
- **bio-research** = scientific strategy: problem selection, experimental design, what question to ask
- **bio-tools** = tool execution: how to run scvi-tools, Nextflow pipelines, Allotrope conversion, QC

When both trigger, bio-research provides the scientific framing and bio-tools provides
the tool mechanics. For strategy questions ("should I use scVI or scANVI"), bio-research
handles it. For execution ("run scVI on this dataset"), bio-tools leads and references
bio-research for tool-specific documentation.

## Routing

| If the user wants to... | Chain with |
|---|---|
| Single-cell analysis with scvi-tools (scVI, scANVI, totalVI, PeakVI, MultiVI, DestVI, veloVI) | Load `bio-research` → reference `scvi-tools` |
| Run nf-core pipelines (rnaseq, sarek, atacseq) on sequencing data | Load `bio-research` → reference `nextflow-development` |
| Convert instrument output files to Allotrope Simple Model (ASM) JSON | Load `bio-research` → reference `instrument-data-to-allotrope` |
| QC single-cell RNA-seq data (.h5ad/.h5) with scanpy and MAD-based filtering | Load `bio-research` → reference `single-cell-rna-qc` |
| Set up bio-research environment and check connected tools | Load `bio-research` → reference `start` |
| Choose what scientific problem to work on, or evaluate a project idea | Hand off to `bio-research` directly (scientific-problem-selection) |
| Analyze non-biological datasets | Hand off to `data-analysis` or `query` |

## Tool Selection Guide

| Data Type | Recommended Tool | Notes |
|---|---|---|
| scRNA-seq (10x, Smart-seq2) | scVI for integration, scanpy for standard analysis | Use scANVI when labels available |
| CITE-seq (RNA + protein) | totalVI | Handles both modalities jointly |
| Multiome (RNA + ATAC) | MultiVI | Joint embedding of both modalities |
| scATAC-seq | PeakVI | Peak-level analysis |
| Spatial transcriptomics | DestVI | Deconvolution of spatial spots |
| RNA velocity | veloVI | Probabilistic velocity estimation |
| Bulk RNA-seq | nf-core/rnaseq pipeline | STAR/Salmon alignment, DESeq2 |
| WGS/WES | nf-core/sarek pipeline | Variant calling, annotation |
| Bulk ATAC-seq | nf-core/atacseq pipeline | Peak calling, differential accessibility |
| Lab instrument output (PDF, CSV, Excel) | Allotrope converter | Outputs ASM JSON + flattened CSV |

## Gotchas

- **QC before analysis. Always.** Single-cell data without QC will produce garbage clusters. Run `single-cell-rna-qc` first.
- scvi-tools requires GPU for reasonable training times on large datasets. Check environment before starting.
- Nextflow pipelines need a genome reference. Confirm which genome build (GRCh38, GRCm39, etc.) before launching.
- Batch correction is not always needed. If samples were processed together, integration may introduce artifacts. Check for batch effects first.
- **Allotrope conversion is instrument-specific.** The converter auto-detects instrument type, but verify the output schema matches your LIMS expectations.
- nf-core pipeline versions matter. Pin the version for reproducibility.
- GEO/SRA data requires accession numbers (GSE, GSM, SRR). Confirm the accession before attempting download.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The bio-research references cover scvi-tools but not Cell Ranger preprocessing."
2. **Search.** Authoritative sources. T1 (tool docs, published papers) > T2 (bioinformatics forums, Bioconductor) > T3 (blog posts, tutorials).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
