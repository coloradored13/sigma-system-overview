# sigma-evaluate report: sigma-chatroom-m1ab

## Meta
- evaluated: 2026-04-21
- target: `~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.plan.md`
- target-status: plan-locked (2026-04-21)
- pipeline: 3 parallel haiku evaluators → sonnet judge (no anchoring)
- grade: **C (2.5 / 4.0)**

---

## Scores

| Criterion | Score | Evaluator Notes |
|---|---|---|
| Accuracy | 2 / 4 | Foundational Ollama /v1 streaming + tool_calls claim contradicted by official Ollama docs + GitHub #12557; Anthropic SDK ≥0.40 version claim unverifiable (current ≥0.92); autogen/crewai + LangChain "Provider-owned loop" precedents not found in documentation. |
| Completeness | 2 / 4 | Security (tool-exec injection, argument smuggling), operational cost envelope, and developer-experience (async streaming debuggability) entirely absent from PM[3]. Research-instrument framing deferred to M3 rather than articulated for M1a/b. |
| Logic | 3 / 4 | Most ADR chains are sound. Three tightness issues: ADR[3] justifies M1a/b (N=2) choice with prospective N>3 reasoning; ADR[2] "strictly worse" treats conditional claim as absolute; ADR[4] BELIEF 0.80→0.70 drop honest but unmotivated in magnitude. |
| Evidence | 2 / 4 | "Independent-research Anthropic+Ollama" cited to support 0.95 confidence but same research contradicts the core streaming assumption. Industry precedent cited as XVERIFY compensation but not found. No primary sources for `len//4`, `monotonic_ns`, or Mistral training claims. |
| Calibration | 2.5 / 4 | ADR[2] 0.95 on unverified behavior contradicts the plan's own anti-sycophancy claim. PM[1] 0.25 likely understates residual scope-creep. False precision: 2-decimal BELIEF, exact +28% R2 delta on estimated 9h, ~41h point estimate with no range. |
| Actionability | 3 / 4 | Genuine strength: executable bash commands with pass criteria; PM[2] escalation quantified (3/3, 1-2/3, 0/3). Carry-forward flags #1 (cost-cap) and #2 (session_id entropy) vague; M2 STEP-3b drifts from planning into mini-spec. |
| Scope Integrity | 3 / 4 | M1a/b code scope contamination minimal. M2 pre-gate STEP-0-3b with time-boxes reads as specification, not planning artifact. UD#3 ("rendering deferred to pre-M2 STEP-1") creates circular dependency: forward plan → UD#3 → pre-M2, which is part of the forward plan. |

**Average:** 17.5 / 7 = 2.5 → **Grade C**

---

## Strengths

1. **Mechanical verification rigor.** PM[2] escalation triggers are quantified with exact counts (3/3 fail → swap, 1-2/3 malformed → annotate, 0/3 fail → lock), and SQ6c smoke-test is explicitly declared as blocking SQ14b. Executable, not aspirational. Verification sections (lines 506-538) contain runnable bash with pass criteria.

2. **Honest downward calibration.** ADR[3] 0.88→0.84, ADR[4] 0.80→0.70, PM[1] 0.55→0.25 in R2 demonstrate genuine anti-sycophancy posture at the meta-level, even where individual magnitude justifications are missing. The pattern of deliberate downward revision after counter-evidence is creditable.

3. **Structured multi-perspective ADR format.** Build / QA / Architecture inputs recorded separately, counter-arguments enumerated (ALT1/ALT2/ALT3 for each ADR), PM risks mapped to specific mitigations with detection criteria. The scaffolding for rigorous reasoning is present.

---

## Weaknesses

### 1. Architectural load-bearing claim for M1b is contradicted by primary sources

- Ollama's official `/v1` OpenAI-compatibility documentation states tool_calls are silently dropped when streaming is enabled.
- GitHub issue #12557 confirms the same failure mode.
- The plan treats this as a **0.45-likelihood exploratory risk** in PM[5] with fallbacks, rather than a known blocker.
- If SQ6c fails (which documentation predicts), M1b's +23.5h estimate has no pre-calculated FAIL path.
- ADR[2] asserts 0.95 confidence on a behavior the plan itself gates behind an unverified smoke test.

### 2. Evidence base is internally inconsistent

- "Independent-research Anthropic+Ollama" is cited to support ADR[2]'s 0.95 confidence, but the same research domain (Ollama /v1) directly contradicts the plan's core streaming assumption.
- The autogen/crewai "N>1 location-separation" precedent cited as XVERIFY compensation for ADR[3] is not found in any documentation searched.
- A plan cannot claim independent research backing for conclusions that contradict that research, or cite an unverified precedent to close an evidence gap.

### 3. Systematic gaps in PM[3] risk coverage

- **Security absent:** tool-execution attack surface (injected tool names, malformed JSON, argument smuggling) is not in the risk matrix. First-order, not edge-case, for any M1b-style tool-exec loop.
- **Operational cost absent:** no live-test cost envelope scoped for M1a/b beyond a vague carry-forward flag (#1) with no cost-cap default.
- **Developer experience absent:** streaming async generators make breakpoint debugging hard; not discussed in Known Gaps or PM[3].
- Research-instrument framing is articulated only for M3 forward plan, not for the milestones being built now.

---

## Recommended Improvements

- **Run SQ6c before finalizing M1b scope and estimates.** If Ollama /v1 + streaming fails (as docs predict), add `stream: false` as the primary M1b implementation strategy and recalculate hours. Do not hold a confirmed failure mode at 0.45 likelihood.
- **Recalibrate ADR[2] confidence from 0.95 → 0.70–0.75**, explicitly conditioned on SQ6c outcome. Add SQ6c as a BELIEF dependency in the ADR itself rather than a separate verification section.
- **Populate PM[3] with three missing risk categories:**
  - Tool-exec injection surface — define input validation and schema enforcement for tool names and arguments.
  - Live-test cost envelope — specify a cap (default value) before any `tests/live/` runs.
  - Streaming async debuggability — name the escape-hatch (sync fallback, structured logging, or replay harness).
- **Resolve the UD#3 circular dependency.** Either decide rendering now using available information, or explicitly defer M2 STEP-1 and remove STEP-0-3b from the current planning artifact. A forward plan that depends on a decision deferred to the forward plan is not a forward plan.
- **Replace false-precision point estimates with ranges:**
  - ~41h parallelized → ~36–49h with coordination overhead explicit.
  - BELIEF scores → ranges (0.80–0.85) rather than two-decimal values.
  - Collapse PM[5] 0.45 vs 0.40 false distinction.
- **Add carry-forward flag specificity:**
  - Flag #1 needs a cost-cap default or range.
  - Flag #2 needs an entropy source named (uuid4? timestamp-nonce? hash?).
  - Flag #4 needs T1/T2/T3 missing-tag findings enumerated.
- **Verify or remove the autogen/crewai "N>1 location-separation" precedent.** Either produce primary documentation or drop it as compensating evidence for the XVERIFY miss.

---

## Evaluator Disagreements

- **Accuracy (2/4) vs Logic (3/4)** — not a contradiction. A plan can be internally coherent while resting on false external premises. Both scores are compatible and accurate characterizations of their respective domains.
- **Accuracy vs Calibration** — converge on the same root cause from different angles:
  - Evaluator 1 flagged PM[5] treating confirmed failure as 0.45 risk.
  - Evaluator 3 independently flagged ADR[2] at 0.95 on unverified behavior.
  - Both point to *empirical gaps treated as planning assumptions rather than blockers*.
  - The Ollama documentation contradiction is the single highest-severity finding.
- No other inter-evaluator contradictions identified.

---

## Revision Offer

Grade C (< B) triggers the skill's revision-offer protocol. The three highest-leverage findings to revise before re-evaluation:

1. **PM[5] / ADR[2] reframing** of Ollama /v1 streaming + tool_calls as known-broken (not exploratory), with SQ6c-PASS and SQ6c-FAIL estimate branches explicit.
2. **PM[3] expansion** with security, cost envelope, and async-debuggability risks.
3. **UD#3 circular dependency resolution** (decide now or remove STEP-0-3b from the planning artifact).

Re-run `/sigma-evaluate <path>` against the updated plan.

---

## Persistence

- **Summary entry** → `conv.md` in sigma-mem.
- **Cross-evaluator pattern** → sigma-review team memory as `empirical-gap-as-planning-assumption`:
  > Plan treats documented external failure as exploratory PM risk → BELIEF on unverified behavior held high (0.95) while anti-sycophancy claimed. Detection: cross-evaluator convergence. Mitigation: require primary-source citation for ADR BELIEF ≥0.85 + pre-compute FAIL branch for any gate-blocked estimate.
- Per-evaluator agent memories skipped (evaluators are ad-hoc pipeline agents, not persistent sigma-review roster members).
