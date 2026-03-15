# Knowledge Graphs -- Sigma-Review Infrastructure

Knowledge graphs provide structured domain knowledge for sigma-review agents, enabling relationship-aware analysis that goes beyond text search.

## Purpose

Agents conducting reviews need domain context: who competes with whom, what integrates with what, which technologies underpin which products. Flat text files capture facts but lose structure. Knowledge graphs preserve the relationships between entities, enabling multi-hop reasoning (e.g., "Company A acquired Company B, which competes with Company C in segment X -- so Company A is now an indirect competitor in segment X").

## Design Principles

- **Markdown-based**: Human-readable, git-trackable, no external database required. Agents read these files directly via file read operations.
- **Parseable format**: Entity lines start with `E[...]`, relationship lines with `R[...]`. Agents can grep for specific entities or relationship types.
- **One domain per subdirectory**: Each domain graph is self-contained. Domains can reference each other but are independently useful.
- **Source attribution**: Every metric and data point includes its source and date. Agents can assess freshness and credibility.
- **Append-friendly**: New entities and relationships are added at the end of their section. No need to reorganize existing entries.

## Directory Structure

```
knowledge-graphs/
  README.md                    -- this file
  warehouse-supply-chain/      -- warehouse, logistics, robotics, labor management
    entities.md                -- entity type definitions (schema)
    relationships.md           -- relationship type definitions (schema)
    graph.md                   -- the actual graph data (instances)
```

## How Agents Use Knowledge Graphs

1. **Pre-review context loading**: Read `graph.md` to understand the competitive landscape before analysis begins.
2. **Entity lookup**: Grep for a specific company or product to get its attributes and relationships.
3. **Relationship traversal**: Follow relationship chains to discover indirect connections (A competes-with B, B acquired C, therefore A competes-with C's former products).
4. **Metric grounding**: Look up specific metrics with source attribution to validate or challenge claims during review.
5. **Gap detection**: Identify entities that lack expected relationships (e.g., a product with no `serves-segment` relationship suggests incomplete analysis).

## Format Reference

### Entity Format
```
E[entity-name|field:value|field:value|...]
```

### Relationship Format
```
R[source-entity|relationship-type|target-entity|property:value|...]
```

### Conventions
- Use hyphens for multi-word values within fields: `type:vendor-agnostic`
- Use commas for lists within a field: `products:WMS,LMS,WES`
- Use parentheses for context: `TAM:$719M(2025)`
- Pipe `|` separates fields within brackets
- Source attribution format: `source:Name-Date` or `src:abbreviated-source`

## Adding New Domains

1. Create a new subdirectory under `knowledge-graphs/`
2. Copy `entities.md` and `relationships.md` from an existing domain as templates
3. Define entity types relevant to the new domain
4. Define relationship types relevant to the new domain
5. Populate `graph.md` with data from sigma-review analyses
6. Update this README with the new domain listing
