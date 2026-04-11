---
name: visualize
description: >
  Use this skill when the user wants to create charts, dashboards, or visual
  representations of data. Triggers include: 'build a dashboard', 'create a chart',
  'visualize this', 'graph', 'plot', 'interactive dashboard', 'Chart.js', 'matplotlib',
  'seaborn', 'plotly', 'bar chart', 'line chart', 'heatmap', 'scatter plot', 'funnel',
  'KPI dashboard', or requests to turn data into visual outputs. Complements
  data-analysis and query: those skills help you understand and extract data; this
  skill helps you show it to someone else. Do NOT use for data exploration or profiling
  without a visual output goal (use query or data-analysis). Do NOT use for written
  reports or summaries (use reporting).
---

# Visualize

Turn data into charts, dashboards, and interactive visual outputs. This is the
output-focused complement to data-analysis and query — those skills help you
understand and extract data; this skill helps you present it.

## Rigor Scaling

| Signal | Level | What Changes |
|---|---|---|
| Quick chart — "plot this", "bar chart of X" | **Quick** | Generate the chart. Sensible defaults. No framework needed. |
| Standard visualization — "build a dashboard", "visualize this dataset" | **Standard** | Apply routing table. Consider audience, chart selection, layout. |
| Stakeholder-grade — board deck, client deliverable, published report. OR user says "this is for leadership", "make it polished" | **Rigorous** | Full protocol: audience-first design, accessibility, annotation, narrative arc. |

## Routing

| If the user wants to... | Chain with |
|---|---|
| Build an interactive HTML dashboard with filters and multiple panels | Load `data-analysis` → reference `interactive-dashboard-builder` |
| Create publication-quality charts with Python (matplotlib, seaborn, plotly) | Load `data-analysis` → reference `data-visualization` |
| Visualize financial data — income statements, variance waterfalls, close status | Load `finance-accounting` for domain context, then build the visual |
| Visualize product metrics — funnels, cohorts, retention curves | Load `planning-prioritization` → reference `metrics-tracking` for what to measure, then build the visual |
| Extract or prepare the data before visualizing | Hand off to `query` for SQL/data extraction first |
| Write the narrative around the visualization | Hand off to `reporting` for commentary and framing |
| Design critique of a visualization | Hand off to `design-ops` for evaluation |

## Workflow

1. **Start with the decision.** "What decision will the viewer make from this?" If you can't answer that, the dashboard will be decoration.
2. **Choose the right chart type.** Comparison → bar. Trend → line. Composition → stacked bar or pie (sparingly). Relationship → scatter. Distribution → histogram or box plot.
3. **Reduce to essentials.** Remove gridlines, legends, and labels that don't aid comprehension. Every element should earn its place.
4. **Annotate the insight.** A chart without context is a Rorschach test. Add titles that state the takeaway, not just the metric name. "Revenue grew 23% QoQ" not "Revenue by Quarter."
5. **Test accessibility.** Color-blind safe palettes. Sufficient contrast. Labels on the data, not just in the legend.

## Gotchas

- Dashboards are for monitoring, not storytelling. If the user needs a narrative, chain with `reporting`.
- Dual-axis charts are almost always misleading. Prefer two separate charts.
- Pie charts fail beyond 5 segments. Use horizontal bar instead.
- Interactive dashboards (HTML/Chart.js) are self-contained — no server needed. Good for sharing.
- Python visualizations (matplotlib/plotly) are better for analysis and publication. Know which context you're in.
- **Don't visualize before profiling.** If the data hasn't been explored, hand off to `query` or load `data-analysis` first. Bad data makes pretty bad charts.

## Relationship to data-analysis and query

`data-analysis` owns the analytical framework and reference files (including `data-visualization.md` and `interactive-dashboard-builder.md`). `query` handles data extraction and profiling. This skill is the visual output entry point — when the user says "chart this" or "build a dashboard," start here. For data preparation, defer to `query`. For analytical rigor, defer to `data-analysis`.

## When the Skill Doesn't Cover It

If the reference material does not answer the question — do NOT guess. Instead:

1. **Name the gap.** "The visualization references cover Chart.js and Python but not D3.js bindings for React."
2. **Search.** Find authoritative sources. Apply tiers: T1 (docs/specs) > T2 (tutorials) > T3 (blog posts).
3. **Flag provenance.** "This comes from web research — [source, tier]."
4. **Suggest a skill update if recurring.**
