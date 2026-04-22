# sigma-evaluate report: sigma-chatroom-m1ab

## Meta
- rounds evaluated: R2 (initial), R3 (after R3 revisions), R4 (after R4 revisions)
- target: `~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.plan.md`
- pipeline: 3 parallel haiku evaluators → sonnet judge (no anchoring)
- **R2 grade: C (2.50 / 4.0)** — evaluated 2026-04-21 (548-line plan)
- **R3 grade: B− (2.86 / 4.0)** — evaluated 2026-04-21 post-R3 (609-line plan), +0.36 crossing B threshold
- **R4 grade: C+ (2.57 / 4.0)** — evaluated 2026-04-21 post-R4 (611-line plan), −0.29 from R3 (regression)

---

# R2 Evaluation (initial, C 2.50/4.0)

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

## R2 Persistence

- **Summary entry** → `conv.md` in sigma-mem.
- **Cross-evaluator pattern** → sigma-review team memory as `empirical-gap-as-planning-assumption`:
  > Plan treats documented external failure as exploratory PM risk → BELIEF on unverified behavior held high (0.95) while anti-sycophancy claimed. Detection: cross-evaluator convergence. Mitigation: require primary-source citation for ADR BELIEF ≥0.85 + pre-compute FAIL branch for any gate-blocked estimate.
- Per-evaluator agent memories skipped (evaluators are ad-hoc pipeline agents, not persistent sigma-review roster members).

---

# R3 Re-evaluation (B− 2.86/4.0, +0.36 vs R2)

## R3 Scores & Delta

| Criterion | R2 | R3 | Δ | Evaluator Notes |
|---|---|---|---|---|
| Accuracy | 2 | **3** | **+1** | Ollama /v1 framing fixed (GH#12557 cited correctly, "documented-to-fail" acknowledged), autogen/crewai precedent dropped honestly. Remaining: mild conflation of official docs with empirically-observed GH issue. |
| Completeness | 2 | **3** | **+1** | PM[6/7/8] added (security/cost/async-debug). Gaps remain: independent security review, M1c+ adapter maintenance ownership, dependency supply-chain risk, JSONL data-privacy. |
| Logic | 3 | **2** | **−1*** | *Not regression — R3 surfaced previously-masked tensions. See analysis below. |
| Evidence | 2 | **2** | 0 | PM[2/5/7] lack base rates, F1/F2 fallback viability untested, 4-agent consensus substituted for XVERIFY. |
| Calibration | 2.5 | **3** | +0.5 | ADR[2]/PM[5] reframed conditional on SQ6c (0.70-0.75 PASS / 0.55 FAIL). Remaining: ≥95% fidelity threshold unanchored. |
| Actionability | 3 | **3** | 0 | PM[5] F1/F2 branch selection manual handoff; STEP-1 gate lacks pre-written test; H2-H5 undefined. |
| Scope Integrity | 3 | **4** | **+1** | Hard-stops verified, UD#3 pin conditional on STEP-1 verification, no M2 bleed. |

**R3 average:** 20 / 7 = **2.86** → **Grade B−**

## R3 Improvements (what worked)

1. **Conditional calibration on SQ6c.** ADR[2] / PM[5] reframed from unconditional 0.95 to conditional ranges. Substantive, not cosmetic.
2. **Scope boundary hardened.** UD#3 resolution preserved as *conditional* on STEP-1 JSONL verification. Scope-Integrity 4/4 earned, not granted.
3. **PM-track expansion without contamination.** Security (PM[6]), cost (PM[7]), async-debug (PM[8]) added with SQ29-32 tests staying in M1a/b scope.

## Logic Regression Analysis (3 → 2)

This is not deterioration of the underlying plan. R3 revisions surfaced tensions that were previously masked:

- R2 relied on autogen/crewai precedent (ADR[3]) which provided apparent support for agent-owned loops. R3 honestly drops that unverified precedent — but narrowed compensating factors now include self-reference (DB re-run conducted by the same design team defending the decision). Prior Logic evaluator didn't scrutinize this because the broader precedent absorbed attention.
- R3's conditional reframing of ADR[2] required articulating the "documented-to-fail-but-proceeds-as-primary" logic explicitly. Equivocation becomes visible where it was previously implicit.
- Two new fallacies spotted in R3 that weren't in R2 framing:
  - PM[3] escalation "simplify to sync" contradicts C5 ("streaming from day 1") — false dilemma.
  - PM[2] reliability classification from 3 runs affirms-the-consequent (0/3 fail in 3 runs → `reliable`).

Core theses (native per-SDK tool-use, tool-exec in TurnEngine, OpenAI-shaped canonical Message, schema-versioned JSONL) remain sound.

## R3 Remaining Weaknesses

1. **Evidence circularity.** PM[2/5/7] have no reference datasets. 4-agent consensus is not external evidence. F1/F2 fallback viability untested.
2. **Logic premise gaps in ADR[3-5].** ADR[4] 61% majority-provider thin; ADR[5] drift math defers empirical validation to M1a; PM[3] sync fallback contradicts C5 unresolved.
3. **Undefined thresholds blocking mechanical enforcement.** H2-H5 use qualitative triggers ("expansion," "infeasible," "expensive"). STEP-1 ≥95% fidelity has no derivation and no pre-written test. PM[8] ">1 async-debugging blocker" subjective. Gates that cannot be evaluated mechanically drift under delivery pressure.

## R4 Recommendations

- **Anchor the ≥95% fidelity threshold** with a source, error-budget derivation, or justified alternative. Write the acceptance test spec *before* M2 begins.
- **Quantify H2-H5** with measurable criteria (line-count delta, hours, dollar threshold).
- **Attempt external validation for PM[2/5/7]** — a single analogous-system measurement breaks the self-referential citation chain. If none exists, declare prior-free and widen BELIEF.
- **Resolve PM[3] / C5 tension explicitly** — either permit sync fallback as a scoped C5 exception with documented conditions, or remove "simplify to sync" as an escalation path.
- **Pre-register F1/F2 fallback viability** — minimal smoke test of `ollama` pypi AsyncClient against `/api/chat` before C2 begins.

## R3 Evaluator Disagreements

- **Scope Integrity 4/4 vs Logic's UD#3 concern** — not a contradiction. Logic lens: "claimed resolved but deferred." Scope lens: "deferral is structurally correct." Both right about different things.

## R3 Verdict

B− is a legitimate upgrade. R3 fixed the three most critical R2 findings (Ollama framing, PM[3] coverage, UD#3 resolution) without introducing scope contamination. The Logic drop reflects honest scrutiny of newly-legible reasoning, not new errors. If R4 addresses the three remaining weaknesses (especially the undefined thresholds), this crosses into B+ / A− territory.

## R3 Persistence

- **Summary entry** → `conv.md` in sigma-mem (R3 delta notation).
- **Cross-evaluator pattern** → sigma-review team memory as `R3-surfaces-R2-masked-tensions`:
  > Revision rounds that fix flagged issues can LOWER scores on orthogonal criteria by making previously-implicit reasoning explicit. Score drops post-revision aren't regression signals — read delta analysis, not raw deltas. Mitigation: judge prompts should explicitly instruct "evaluate current plan on current state; do not penalize for uncovering new issues."

---

# R4 Re-evaluation (C+ 2.57/4.0, −0.29 vs R3 — REGRESSION)

## R4 Scores & Delta

| Criterion | R2 | R3 | R4 | Δ R3→R4 |
|---|---|---|---|---|
| Accuracy | 2 | 3 | **2** | **−1** |
| Completeness | 2 | 3 | **3** | 0 |
| Logic | 3 | 2 | **2** | 0 |
| Evidence | 2 | 2 | **1** | **−1** |
| Calibration | 2.5 | 3 | **3** | 0 |
| Actionability | 3 | 3 | **3** | 0 |
| Scope Integrity | 3 | 4 | **4** | 0 |

**R4 average:** 18 / 7 = **2.57** → **Grade C+**

Trajectory: R2 C (2.50) → R3 B− (2.86) → **R4 C+ (2.57)**, net +0.07 over R2, −0.29 from R3.

## R4 Regression — The Anti-Pattern

R4 attempted to fix R3's self-referential citation problem by adding unverified external-looking citations. Three factual errors introduced:

1. **PM[7] Opus-4 pricing:** "$0.15/call" cited; actual at $25/M output tokens = **$0.0512** (3× error).
2. **PM[6] OWASP ASVS V11.1.3:** Requirement number not confirmed in ASVS 4.0.
3. **ADR[7] "OpenTelemetry + Jaeger pattern"** for per-record schema versioning: contradicted by search — OT versioning is stream-level, not per-record.

Plus **ADR[3] LangChain AgentExecutor** cited as defending N>3 SDK separation, but LangChain only establishes N=1. Accurate citation, but doesn't support the claim it's attached to.

**The anti-pattern:** "Self-referential citations" is a transparency problem. The correct fix is either (a) verified primary sources with URLs that survive a search check, or (b) declare "no external evidence; prior-free reasoning at lowered BELIEF." R4 chose a third path — unverified external-looking citations — which is worse than either correct option. A plan saying *"no external source; BELIEF 0.60"* is more trustworthy than a plan citing a contradicted OT pattern at *BELIEF 0.80-0.85*.

## What R4 Did Well

1. **Scope Integrity held at 4/4** — M2-M4 hard-stops enforced, no contamination.
2. **ADR[2] thesis decomposition** — separating core-thesis BELIEF (0.80-0.85) from M1b-channel BELIEF (0.70-0.75) is structurally sound.
3. **Carry-forward flags remain specific** — env var + $5 default, uuid7 RFC 9562, validator REQUIRED.

## What R4 Didn't Move (despite R3 recommendations)

1. **H2-H5 still qualitative** — "expansion," "infeasible," "expensive" undefined.
2. **UD#3 ≥95% still unanchored** — no derivation, no pre-written acceptance test.
3. **ADR[3] BELIEF still 0.75-0.85** on non-independent evidence. Logic evaluator says honest range is 0.55-0.70.

## Expectation Gap

Sigma-build team expected **B+** (≥3.35). Actual **C+ (2.57)** — gap of ~0.86 points. Why:

- R4 made a category error on Evidence: unverified externals replaced honest self-references → 2→1, not 2→3.
- Three criteria R3 flagged as fixable (Logic, Calibration, Actionability) did not move.
- No path to B+ without improving Evidence and Logic; R4 regressed both.

## R5 Recommendations

**Evidence is the load-bearing fix.** Every citation survives a 30-second search check before inclusion.

- **Correct Opus-4 pricing** to $25/M output tokens (≈$0.0512/call) or remove the numerical claim.
- **Remove or fix OWASP ASVS V11.1.3.**
- **Remove or reclassify the OpenTelemetry/Jaeger citation** — stream-level, not per-record.
- **Decouple the ADR[3] LangChain citation** from the N>3 claim it doesn't support.
- **Set ADR[3] BELIEF to 0.55-0.70** to reflect "reasoned but unverified" with XVERIFY gap declared.
- **Pre-register UD#3 ≥95% as executable assertion**, not prose.
- **Quantify H2-H5** with dollar amounts, latency ms, specific error counts.
- **Address F1 fallback BELIEF** — if both Ollama channels fail, thesis is half-verified.

## R4 Persistence

- **Summary entry** → `conv.md` in sigma-mem (R4 regression notation).
- **Cross-evaluator pattern** → sigma-review team memory as `unverified-citation-anti-pattern`:
  > When eval critique flags "self-referential citations," the temptation is to ADD external-looking citations without verification. This produces worse outcomes than either verified primary sources OR declared prior-free reasoning. Every citation must survive a 30-second search check before inclusion. Plans with declared gaps at lowered BELIEF are more trustworthy than plans with contradicted citations at high BELIEF.
