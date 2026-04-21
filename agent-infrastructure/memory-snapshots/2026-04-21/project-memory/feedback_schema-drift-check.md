---
name: Check the full data model before shipping
description: When building features, audit every schema field — either wire it or delete it. Don't leave fields that advertise functionality the app doesn't deliver.
type: feedback
originSessionId: c34a8540-25ae-4a1a-ad5f-a84fa133aa13
---
When shipping a feature, audit every column/field defined in the data model and confirm it's actually populated and surfaced. If a field is defined but unused, either wire it up now or delete it.

**Why:** On ai-pd-tracker (26.4.20), the `lesson_progress.struggled_topics` field was in the schema from day one and was returned by the progress API, but never populated. The spaced-repetition logic used a coarse `quiz_score < len(quiz)` signal for struggle — enough to halve review intervals, but losing which specific questions the user missed. The user caught it as a schema-drift observation. Surface area that looks implemented but isn't is worse than explicitly missing functionality — it lies to future readers and makes the code appear more feature-complete than it is.

**How to apply:** Before calling a feature "done":
1. Grep the schema for every column name.
2. For each, verify there is (a) at least one write path that sets it and (b) at least one read path that surfaces it to the user, OR delete it from the schema.
3. If a column is intentionally held for future work, add an explicit comment at the schema definition naming the missing wire-up ("// populated in step N — not yet built") and a tracked open-thread entry in project memory. Don't just leave it.

Same principle applies to system prompts, config flags, and API response fields — if it's in the surface but not exercised, either exercise it or remove it.
