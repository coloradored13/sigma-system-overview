# Phase 06b: Compilation

**Every step below is mandatory. This phase runs after synthesis, before promotion.**

## Purpose
Integrate this review's findings into the persistent knowledge wiki. Each review makes the wiki richer. The wiki is the compounding asset — individual reviews are snapshots, the wiki is the living picture.

## Steps

### Step 1: Read Synthesis Artifact
Read the synthesis artifact saved in Phase 06 Step 6:
`shared/archive/{date}-{task-slug}-synthesis.md`

### Step 2: Scan Existing Wiki
List pages in `shared/wiki/`:
```bash
ls ~/.claude/teams/sigma-review/shared/wiki/
```
Read `shared/wiki/INDEX.md` to understand current wiki structure.

### Step 3: Spawn Compilation Agent (MANDATORY)
Same provenance rule as synthesis — lead does NOT write wiki content.

Spawn a compilation agent with:
- The synthesis artifact path
- The wiki directory path
- INDEX.md

Compilation agent instructions:

```
You are the sigma-review compilation agent. Your job: integrate new review findings into the persistent knowledge wiki.

## Inputs
- Synthesis artifact: {path} (this review's compiled findings)
- Wiki directory: ~/.claude/teams/sigma-review/shared/wiki/
- Wiki index: shared/wiki/INDEX.md

## Process
1. Read the synthesis artifact fully
2. Read INDEX.md to understand existing pages
3. For each significant finding, entity, or domain in the synthesis:
   a. Matching wiki page exists → read it, update with new intelligence
   b. No matching page → create one
4. Update INDEX.md with any new pages

## Page Update Rules
- ADD new findings with source attribution: `[R{review-number}, {date}]`
- If new finding CONTRADICTS existing content:
  flag both: `⚠ CONFLICT: [R12] found X, but [R8] found Y. Unresolved.`
  Do NOT silently overwrite — contradictions are signal
- If new finding STRENGTHENS existing content:
  note convergence: `✓ Confirmed [R12]: {finding} (also [R8])`
- PRESERVE all source attributions. Never strip review provenance.
- Write in plain prose. Wiki pages are reference documents, not ΣComm.

## Page Structure Template
```markdown
# {Page Title}
Last updated: {date} | Reviews: R8, R12

## Summary
{2-3 sentence overview — updated with each review}

## Key Findings
{Organized by subtopic, each finding attributed to source review}

## Open Questions
{Unresolved from any review}

## Contradictions
{Where reviews disagree — both positions preserved}

## Sources
{List of review artifacts that contributed to this page}
```

## What NOT to do
- Do not editorialize beyond what agents found
- Do not merge contradictions into a false consensus
- Do not create pages for process observations (those go in patterns.md)
- Do not duplicate patterns.md content — this wiki is domain knowledge, not process knowledge
```

### Step 4: Review Compilation Output
Read what the compilation agent wrote/updated. Quick sanity check:
- Pages make sense as standalone reference documents
- Source attributions present
- No lead context leaked in

### Step 5: Update INDEX.md
Confirm INDEX.md reflects any new pages added.

### Step 6: Validate Compilation Integrity
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py validate --check compilation
```
This runs V24+V25+V26:
- V24: Source attribution on all wiki entries (`[R{number}, {date}]`)
- V25: No contradiction silently resolved (multi-source pages must have CONFLICT or Confirmed flags)
- V26: No wiki pages deleted (INDEX.md references match actual files)

If validation FAILS:
- V24 failure: compilation agent added unattributed findings → re-run compilation with explicit attribution instruction
- V25 failure: contradiction was silently merged → restore both positions with CONFLICT flag
- V26 failure: pages were deleted → investigate and restore from prior state

### Step 7: Advance Orchestrator
```bash
python3 ~/.claude/teams/sigma-review/shared/orchestrator-config.py advance --context '{"compilation_complete": true, "compilation_validated": true}'
```
Confirm returned phase = `promotion`.

## Exit Checklist

- [ ] Synthesis artifact read
- [ ] Existing wiki scanned
- [ ] Compilation agent spawned (NOT lead-written)
- [ ] Wiki pages updated/created with source attribution
- [ ] Contradictions flagged, not silently resolved
- [ ] INDEX.md current
- [ ] No process observations leaked into wiki (those belong in patterns.md)
- [ ] Compilation validation passed (V24+V25+V26)

**All items checked → read `phases/07-promotion.md`**
