---
name: Spec Workshop
description: Local Streamlit app for structured spec writing with Claude API challenge/refine — v1 spec drafted 26.3.29, not yet built
type: project
---

Local tool for writing structured specs and producing AI-ready handoff documents. Evolved from prompt-coach concept (same architecture, different focus).

**Why:** User wants a proper app interface (not chat sidebar) for iterating on specs. Structured input (form fields) + Claude challenging each section + persistent storage + clean export.

**Architecture (v1 spec, 26.3.29):**
- Streamlit + Anthropic Python SDK + local file storage (`~/specs/{slug}.json`)
- 5 spec sections: What it is, Inputs/Outputs, Constraints, Acceptance criteria, Context
- Per-section "Challenge" button → Claude reviews for gaps/ambiguity
- Export to clean markdown for AI handoff
- Auto-save, sidebar spec list, no auth (local-only)
- Model: Sonnet for speed on iterative challenges

**Decisions locked (26.3.30):**
1. Prompt output → YES: both formatted spec markdown AND wrapped system prompt for Claude
2. Completeness rating → YES: Claude scores each section (e.g., 3/5 with specific gaps)
3. Versioning → YES: keep history to surface consistent strengths/weaknesses across specs

**Status:** V1 spec finalized in conversation 26.3.30. Not yet built, no repo created.
