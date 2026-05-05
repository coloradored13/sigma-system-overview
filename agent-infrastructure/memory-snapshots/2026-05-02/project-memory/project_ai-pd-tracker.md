---
name: AI PD Tracker
description: Local FastAPI+SQLite tracker for ai-pd-curriculum.md — all 10 build-brief steps shipped 26.4.20; private repo at coloradored13/ai-pd-tracker; coach validated via test_coach.py
type: project
originSessionId: 94ee6e68-5400-4953-9051-035d791b124d
---
# AI PD Tracker

**Location:** `~/Projects/ai-pd-tracker/`
**Remote:** `github.com/coloradored13/ai-pd-tracker` (private, main)
**Started:** 2026-04-19
**Status (2026-04-20):** Feature-complete. All 10 build-brief steps shipped + browser-verified. Coach infra + vague-answer harness validated against claude-sonnet-4-6. Repo initialized and pushed private.

## What it is

Local personal learning tracker for the user's 8-week AI professional development curriculum. Runs on user's laptop, no cloud, SQLite for persistence, Anthropic API for the AI Coach. Single-user, single-machine (brief is explicit).

## Authoritative references (on disk)

- `build-brief.md` — full build spec, source of truth. Byte-identical to the original prompt zip.
- `ai-pd-curriculum.md` — source curriculum (~40K).
- `curriculum.json` — parsed output, what the app reads.

## Stack decisions (non-obvious)

- **FastAPI + vanilla JS + Tailwind CDN**, not Streamlit or React. No build step.
- **SPA with hash routing**, not server-rendered templates.
- **Curriculum parsed once at startup from JSON.** Parser is one-way: run `python parse_curriculum.py` after editing the `.md`.
- **Slugify converts `.` to `-`**: "Module 1.1" → `module-1-1`, not `module-11`.
- **Dev no-cache middleware** on `/` and `/static/` — required because Chrome aggressively caches SPA assets on disk even with ETag/Last-Modified. Without this, HTML edits don't show up until hard-reload.

## Key files

| File | Purpose |
|---|---|
| `parse_curriculum.py` | Markdown → JSON; re-run after editing curriculum.md |
| `app.py` | FastAPI backend, SQLite, all endpoints |
| `coach.py` | AI Coach system prompt + Anthropic API wrapper |
| `test_coach.py` | Vague-answer harness (risk callout from brief line 190) |
| `static/index.html` | SPA shell (Tailwind CDN) |
| `static/app.js` | Client-side router + all views |
| `static/styles.css` | Minimal custom CSS |
| `curriculum.json` | Parsed curriculum (don't hand-edit) |
| `data.db` | SQLite, gitignored |
| `.env` | API key (gitignored, mode 0600) |
| `.backups/` | Auto-snapshots of data.db on startup, last 10 kept, gitignored |
| `requirements.txt` | fastapi, uvicorn, anthropic, python-dotenv, pydantic |

## Run command

```bash
cd ~/Projects/ai-pd-tracker
source .venv/bin/activate
python -m uvicorn app:app --reload --port 8000
```

Then http://localhost:8000.

## API key wiring (non-obvious)

The `.env` ANTHROPIC_API_KEY for this project reuses the same key the sigma-verify MCP uses. Canonical source:

```
~/.claude.json → mcpServers.sigma-verify.env.ANTHROPIC_API_KEY
```

If the user rotates the key, update `.claude.json` (via `claude mcp add` or direct edit) AND copy the new value to `ai-pd-tracker/.env`. `load_dotenv()` runs once at server startup — touch `app.py` to force uvicorn reload after `.env` edits.

## Coach validation (step 5 risk callout)

Brief line 190 warns: "If the coach just agrees with the user, the whole testing premise fails." Harness in `test_coach.py` feeds four deliberately vague / pattern-matched / surface-level messages and checks replies for pushback markers.

Results (26.4.20, claude-sonnet-4-6, 6 scenarios): 6/6 pass end-to-end. Full sample run saved at `~/Downloads/ai-pd-tracker-coach-harness-2026-04-20.md`. Earlier "empty reply / non-determinism" note was a harness bug, not a model issue — one scenario pointed at a lesson without an `ai_coach` block (day-5-from-chat-to-api) and `run_one` was silently returning `{"skipped": ...}` which the main loop misrendered as a 0-char failure. Fix: scenario lesson_id moved to `day-6-7-anthropic-agent-guides` and the skip path now raises ValueError so future misconfigurations are loud.

System prompt in `coach.py` embeds the user's two real work projects by name (natural-language dashboard, credit agreement extraction) — this is why the repo is private. If it ever goes public, genericize the persona first.

## Ollama decision

User has local Ollama (M3 16GB, 4-8B models). Not used here. Coach's value is catching subtle thinking failures where small models break down (agreeableness, generic responses). Token cost on Sonnet for coach conversations is trivial (~1k per turn). Ollama might fit later for non-adversarial features (note auto-summary, quick-check generator) — not the coach.

## Dashboard features shipped

Overall progress %, lessons completed (lessons_completed / lessons_total), this-week hours vs. configurable weekly target, streak counter (consecutive days with logged time), coach-checks-pending count, phase progress bars, next-lesson card, portfolio + journal link tiles, recent journal strip, review queue (due items + next up), Week 8 checkpoint link, reset-all-progress button (with confirmation).

## Lesson view features shipped

Title, objectives, resources, deliverable, instructions, sign-off button, interactive quiz with per-question explanation reveal on submit, 70% pass threshold (`QUIZ_PASS_THRESHOLD` in app.py), AI Coach chat with 4+ turn gate on mark-passed, notes autosave on blur, mark-complete button gated on (signed_off AND quiz_passed AND coach_passed).

## Open threads

- **(RESOLVED 26.4.20) struggled_topics wire-up:** now populated on quiz submission (`api_submit_quiz` saves wrong question-numbers as JSON), exposed as `struggled_questions` in the review-queue response, and rendered on the review card as "Focus on: Q3, Q6". DB column name kept as `struggled_topics` — no migration.
- **(RESOLVED 26.4.20) coach grounding accountability:** `COACH_PERSONA` rule #2 in coach.py rewritten to keep the default demanding but require the coach to *defend* each grounding demand. Coach can now pivot to mechanism-pushback for theoretical concepts (attention math, tokenizer internals) and will concede when a learner challenges an unjustifiable demand. Validated: `test_coach.py` added "theoretical_accepted" and "justify_or_concede" scenarios, both pass (empirical replies: coach says "this is a theoretical topic — I won't force that analogy" and "You're right. I can't construct a justification."). Work-context embedding in `USER_CONTEXT` unchanged — still references dashboard + extraction by name, so a work pivot still means editing `USER_CONTEXT` in coach.py.
- **(RESOLVED 26.4.20) Coach "empty-reply intermittent":** root-caused to a harness bug (scenario targeted a lesson with no ai_coach block; silent skip rendered as 0-char fail). Fixed by moving the scenario and making skips raise. Not actually non-determinism — no retry-on-empty needed in coach.py.
- **(RESOLVED 26.4.20) Coach mark-passed backend gate:** `api_coach_mark_passed` now requires `≥ COACH_MIN_USER_TURNS` user turns in transcript before allowing the flag to be set. Constant exported to `/api/stats` so UI and backend agree.

## Code-review open threads (logged 26.4.20, not yet fixed)

Full review at `~/Downloads/ai-pd-tracker-code-review-2026-04-20.md`. Remaining items ordered by severity:

- **High — timezone handling.** `_now_iso`, `_week_start_iso`, `_compute_streak`, `_review_due_date` all use implicit local time. Works fine for a single-user laptop but edge cases exist across DST and machine time-zone changes. Decide: (a) switch to TZ-aware timestamps in DB (cleanest), or (b) document the local-time assumption and make `.backups/` the recovery path. Not urgent.
- **Medium — coach prompt caching.** `coach.send_message` sends full persona + user_context + lesson block (~1.4k tokens) every turn. Anthropic `cache_control` on the static prefix would cut per-turn cost. Defer unless conversations start extending past 6+ turns routinely.
- **Medium — coach message persistence order.** `api_coach_message` saves transcript only after the API call returns. If DB write fails post-API-success, the reply is shown then lost. Fix: persist user turn first, append assistant turn after — or wrap in a single transaction.
- **Medium — `api_reset` has no confirmation token.** UI has `window.confirm`, backend is naked. Localhost mitigates; an `X-Confirm-Reset` header would tighten.
- **Medium — `coachByLesson` client-side map never GC'd.** 15-lesson ceiling makes it a non-issue today.
- **Medium — `api_review_queue` rebuilds lesson map per-request.** Cache at module scope since CURRICULUM is immutable after startup.
- **Medium — `test_coach.py` has no token budget.** Add a `MAX_TOTAL_TOKENS` hard stop to prevent runaway scenario costs.
- **Low — magic numbers scattered.** `QUIZ_PASS_THRESHOLD`, `REVIEW_INTERVALS_DAYS`, `BACKUP_KEEP`, `max_tokens` in coach, `COACH_MIN_USER_TURNS`. Consolidate into one CONFIG block.
- **Low — `h({html: ...})` in app.js relies on unwritten invariant.** Rename or comment to document that `html:` is only safe via `renderProse` (which calls `escapeHTML` first).
- **Low — inconsistent list response shapes.** `api_list_portfolio` → `{items}`, `api_list_time` → `{entries, since}`, `api_list_journal` → `{entries}`. Align for future API docs.
- **Low — `coach.py max_tokens=1024` hardcoded.** Could truncate deep mechanism explanations; bump to 2048 or parameterize.
- **Next-level tuning:** `QUIZ_PASS_THRESHOLD` at 0.7 and default weekly target at 420 min are settable from UI (target button on dashboard). Pass threshold requires code edit.
- **Weekly target for sprint vs. normal weeks:** brief suggests 7h/5h split. Currently single configurable value. Upgrade if user wants per-phase targets.

## User context for this project

Senior PM in loan administration, non-developer, "prefer simple code over clever code." Learning > delegating. Two work projects this curriculum feeds: natural-language dashboard + credit agreement extraction. Both are embedded in the coach system prompt.

---

## Updates 2026-04-29 to 2026-04-30 (persona-recentering work)

The repo has expanded beyond the original curriculum tracker into a workbench for the AI Product Operator persona-becoming plan at `/Users/bjgilbert/.claude/plans/velvety-swinging-coral.md`. Three new top-level subdirectories and a curriculum schema expansion.

### Field Guide work area (26.4.29, commit `f36da73`)

- `field-guide-source/` — extractions from 3 docx files in `~/Downloads/production_ai_agent_readiness_*.docx` (brief, field-guide, one-pager) + Husain 2026 reframes + citation insertion plan + ~600-word lending-specific governance sidebar drafted as canonical edit guide for Stream 1 publish
- `notebooklm/sources-verified.md` — 23-source verification ledger, all VERIFIED at primary canonical URLs (zero drops; SR 26-2, OCC 2026-13, Lethal Trifecta, MA AG Earnest, 4 CVEs all real)
- `pretest-dossier-deferred/DEFERRED.md` — formal sigma-build pretest deferred indefinitely with 4 re-trigger criteria, Husain 2026 reframe of Eval Discipline veto cell, MVP diagnostic spec

### Curriculum schema additions (26.4.30, commit `7167913`)

8 new optional fields on each lesson, parsed from `**Label:** value` blocks in markdown:

- `track` (default `"A"`) — `"A"` (AI Product) or `"B"` (Operator)
- `prerequisites` (default `[]`) — list of lesson IDs
- `estimated_hours` (default `None`) — float; falls back to None on parse error
- `artifact_required` (default `False`) — bool; accepts true/yes/y/1
- `artifact_type` (default `None`) — string label
- `gate_type` (default `"learning"`) — `"learning" | "foundational" | "veto"`
- `risk_level` (default `"low"`) — `"low" | "medium" | "high"`
- `notebook_id` (default `None`) — optional NotebookLM mapping (e.g., `nb-6-operator`)

10 new tests in `tests/test_parser.py` cover defaults + parsing + type validation + edge cases (invalid hours fallback, yes/no aliases for booleans). Full suite **91 passed / 1 skipped** (no regression).

Track A: 17 lessons preserved, all with default values for new fields. Track B: 0/8 markdown content; schema is ready to receive Track B modules in a fresh session.

Track B label syntax pattern (from plan):

```markdown
**Track:** B
**Prerequisites:**
- (none for M1)
**Estimated hours:** 4
**Artifact required:** yes
**Artifact type:** git-rescue-drill
**Gate type:** foundational
**Risk level:** medium
**Notebook:** nb-6-operator
```

### NotebookLM source manifests (26.4.30, commit `7167913`)

6 per-notebook manifests + README at `notebooklm/`. Build order 6 → 3 → 4 → 5 → 2 → 1:

| Notebook | Sources | Purpose |
|---|---|---|
| `notebook-06-operator.md` | 22 | Track B Modules 1–8 + pretest §7 |
| `notebook-03-agent-architecture.md` | 16 | §2 veto-cell mastery, Lethal Trifecta canonical |
| `notebook-04-eval-discipline.md` | 14 | §4 veto-cell, Husain + Shankar 2026 FAQ as canonical primary |
| `notebook-05-regulated-finance.md` | 21 | SR 26-2, OCC 2026-13, MA AG Earnest, Moffatt anchors |
| `notebook-02-reference.md` | 42–48 | Reference search corpus (deltas + padding to specialty union) |
| `notebook-01-audio-overview.md` | 30 | Narrative-friendly reflex install for daily commute |

Each manifest cites verified URLs from `sources-verified.md`, maps to pretest cells + Track B modules, includes audio prompt template + calibration check + refresh cadence. Actual NotebookLM creation is the user's manual work in Google's NotebookLM service (cannot be done autonomously); ~28-30h split across 3-4 sittings to load + generate audio + run calibration.

### Open threads (Stream 3 specifically)

- **Track B markdown content (8 modules, ~40-60h)** — pending. Schema ready, source mapping ready (in `notebook-06-operator.md`), Track A patterns are the style template. Plan says: "fresh session opens, reads `velvety-swinging-coral.md`, writes Track B."
- **Frontend Track A/B toggle** — pending. Plan calls for `track: A | B` toggle in dashboard + `notebook_id` link in lesson view ("Open study notebook"). Optional artifact submission form for `artifact_required: true` lessons. Wire in `static/app.js` after Track B markdown ships.
- **Gap Report ingestion endpoint** — DEFERRED indefinitely (only build if pretest re-trigger criteria fire per `pretest-dossier-deferred/DEFERRED.md`).
