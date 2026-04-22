# sigma-evaluate report R4: sigma-chatroom-m1ab

## Meta
- evaluated: 2026-04-21
- target: `~/.claude/teams/sigma-review/shared/builds/2026-04-20-sigma-chatroom-m1ab.plan.md`
- target-size: 611 lines, 57.4 KB (updated 2026-04-21 22:09)
- pipeline: 3 parallel haiku evaluators → sonnet judge (no anchoring; fresh fresh re-read)
- **grade: C+ (2.57 / 4.0)** — REGRESSION from R3

## Trajectory

| Round | Plan size | Grade | Average |
|---|---|---|---|
| R2 (initial) | 548 lines | C | 2.50 |
| R3 (after R3 revisions) | 609 lines | B− | 2.86 |
| **R4 (after R4 revisions)** | **611 lines** | **C+** | **2.57** |

**Net R2 → R4: +0.07.** Net R3 → R4: **−0.29 (regression).**

---

## Scores & Delta

| Criterion | R2 | R3 | **R4** | Δ R3→R4 | Δ R2→R4 |
|---|---|---|---|---|---|
| Accuracy | 2 | 3 | **2** | **−1** | 0 |
| Completeness | 2 | 3 | **3** | 0 | +1 |
| Logic | 3 | 2 | **2** | 0 | −1 |
| Evidence | 2 | 2 | **1** | **−1** | −1 |
| Calibration | 2.5 | 3 | **3** | 0 | +0.5 |
| Actionability | 3 | 3 | **3** | 0 | 0 |
| Scope Integrity | 3 | 4 | **4** | 0 | +1 |

**Sum:** 2 + 3 + 2 + 1 + 3 + 3 + 4 = **18 / 28**
**Average:** 18 / 7 = **2.57** → **Grade C+**

---

## The Regression — Unverified Citation Anti-Pattern

R4 attempted to fix R3's self-referential citation problem (flagged Evidence 2/4 in R3) by adding external-looking citations. Three contain factual errors:

### 1. PM[7] Opus-4 pricing (3× error)

- **Plan claims:** "Opus-4 at 2048 output tokens ≈ $0.15/call"
- **Verified actual:** $25/M output tokens = **$0.0512/call** at 2048 tokens
- **Error magnitude:** ~3× overestimate

### 2. PM[6] OWASP ASVS V11.1.3 (unverified)

- **Plan claims:** OWASP ASVS V11.1.3 cited as cost-control requirement
- **Search result:** V11.1.3 requirement number not confirmed in ASVS 4.0
- **Likely:** misremembered or fabricated requirement number

### 3. ADR[7] OpenTelemetry + Jaeger pattern (contradicted)

- **Plan claims:** "OpenTelemetry + Jaeger pattern" for per-record schema versioning
- **Search result:** OpenTelemetry schema versioning operates at **stream / collection level**, NOT per-record
- **Error type:** misattribution — citing a pattern for the wrong use case

### 4. ADR[3] LangChain AgentExecutor (miscited)

- **Plan claims:** LangChain AgentExecutor "Provider-owned loop industry mode" defends N>3 SDK separation
- **Search result:** LangChain AgentExecutor is accurate, but only for **N=1** (single-SDK case)
- **Error type:** citation accurate but doesn't support the claim it's attached to

### The anti-pattern

"Self-referential citations" is a transparency problem. Two valid fixes:

1. **Verified primary sources** — URL + search-check + quote-check before inclusion.
2. **Declare prior-free** — "no external evidence available; reasoning only; BELIEF lowered accordingly."

R4 chose a third path: **unverified external-looking citations**. This is **worse than either valid fix** because:

- Unverified externals create false confidence
- Introduced factual errors pollute the BELIEF scores they were meant to support
- A plan saying *"no external source; BELIEF 0.60"* is more trustworthy than a plan citing a contradicted OT pattern at *BELIEF 0.80-0.85*

---

## What R4 Did Well

### 1. Scope Integrity held at 4/4
- M2-M4 hard-stops enforced
- sigma-verify clients.py remains read-only (C3)
- ollama-mcp-bridge C4 hard-stop holds
- sigma-mem M3 wiring deferred correctly
- No external contamination

### 2. ADR[2] thesis decomposition
- Separating core-thesis BELIEF (0.80-0.85) from M1b-channel BELIEF (0.70-0.75) is honest and structurally sound
- R3-v2 anti-sycophancy self-audit reflected genuine self-correction

### 3. Carry-forward flags remain specific
- Flag #1: `CHATROOM_MAX_SESSION_COST_USD` env var + $5 default + tier guidance
- Flag #2: uuid7 recommended, uuid4 fallback, RFC 9562 cited
- Flag #3: validator REQUIRED (not None) with jsonschema + 4 pre-checks enumerated
- Flag #4: T1/T2/T3 enumeration (2+5+1) stated

---

## What R4 Didn't Move (despite R3 recommendations)

### 1. H2-H5 still qualitative
- "Expansion," "infeasible," "expensive" remain undefined
- R3 explicitly recommended quantification (line-count delta, hours, dollar thresholds)
- Impact: build team cannot mechanically evaluate escalation triggers

### 2. UD#3 ≥95% fidelity threshold still unanchored
- No derivation of the 95% number
- No pre-written acceptance test
- No cited source
- R3 flagged this; R4 did not address

### 3. ADR[3] BELIEF still 0.75-0.85 on non-independent evidence
- Compensating factors: 4-agent consensus (not independent) + DB re-run by same design team (internal) + dropped autogen precedent (was strongest external anchor)
- Logic evaluator identifies honest range as **0.55-0.70** ("reasoned but unverified"), not "cross-validated"

### 4. PM[2] 3-run reliability classification still affirming-consequent
- "0/3 fail + 3/3 well-formed → reliability='reliable'" — three successful runs are consistent with reliability but don't prove it (small-sample fallacy)

### 5. F1 fallback (ollama pypi AsyncClient on /api/chat)
- Assumed viable, zero smoke test documented before C2 begins
- R3 recommended pre-registration

---

## Remaining Fallacies (by line)

- **ADR[2] lines ~310-551:** affirming-consequent — F1 fallback BELIEF treats logical consistency as empirical verification
- **PM[2] lines ~437-458:** affirming-consequent — 3/3 success classified as reliable
- **ADR[3] lines ~328-344:** appeal to authority — 4-agent consensus + internal re-run substituted for independent verification
- **ADR[4] lines ~369-371:** begging-the-question — "majority-provider" (8/13 = 61%) unsourced; "simpler for JSONL" undefended
- **ADR[5] lines ~376-382:** false precision — "drift ≤15% absorbed by 60% buffer" arithmetic unclear
- **H2-H5 lines ~556-583:** begging-the-question — undefined qualitative triggers
- **UD#3 lines ~98, 556:** unjustified threshold — ≥95% no derivation

---

## Missing Perspectives (Completeness gaps)

- **Data privacy / PII handling:** no redaction strategy, encryption-at-rest, session log retention policy for JSONL captures
- **Vendor lock-in:** no strategy for Anthropic / Ollama API deprecation risk
- **Multi-session observability (post-M3):** metrics aggregation undefined

---

## Expectation Gap

**Sigma-build team expected B+** (≥3.35) based on R4 commitments:
- Every evaluator-flagged contradiction addressed with substantive reframe
- All ADR BELIEFs converted to honest ranges with lower bounds < prior point estimates
- 3 previously-unpriced risk categories (PM[6/7/8])
- Circular dependency resolved
- False precision removed
- Weak evidence dropped

**Actual: C+ (2.57).** Gap: **~0.86 points below B+.**

**Why the gap:**
1. **Category error on Evidence:** unverified external citations replaced honest self-references. Evidence went 2 → 1, not 2 → 3.
2. **Three R3-flagged fixable criteria didn't move:** Logic, Calibration, Actionability all held where R3 left them despite documented recommendations.
3. **Completeness held at 3, Scope Integrity at ceiling.** No path to B+ without materially improving Evidence and Logic, both of which regressed or held.

---

## R5 Recommendations (if pursuing)

**Evidence is the load-bearing fix. Every citation must survive a 30-second search check before inclusion.**

### Accuracy fixes (mechanical)
- **Correct Opus-4 pricing:** $25/M output tokens → $0.0512/call at 2048 tokens. OR remove the numerical claim entirely.
- **Remove or fix OWASP ASVS V11.1.3:** confirm the actual requirement number in ASVS 4.0 or strike the citation.
- **Remove or reclassify OpenTelemetry/Jaeger citation:** if the pattern is used, cite what it actually covers (stream-level versioning, not per-record).
- **Decouple ADR[3] LangChain citation from N>3 claim:** the citation is accurate for N=1 but doesn't support multi-SDK separation. Either find a real N>3 precedent or drop the citation.

### Logic fixes
- **Set ADR[3] BELIEF to 0.55-0.70** to reflect "reasoned but unverified" with XVERIFY gap declared explicitly.
- **Address F1 fallback BELIEF:** if both Ollama channels fail, thesis is half-verified — BELIEF for F1 path should reflect that, not retain "0.80-0.85 (two-path)" credit.
- **Rework PM[2] 3-run rule:** "Consistent with reliability, not proof of reliability" framing. Small-sample caveat explicit.

### Calibration fixes
- **Pre-register UD#3 ≥95% as executable assertion**, not prose description. Example: `assert position_fidelity >= 0.95 on fixture_5turn_2model.jsonl after round-trip`.
- **Anchor the 95% threshold** — derive from error-budget argument or cite a source.

### Actionability fixes
- **Quantify H2-H5 triggers** with dollar amounts, latency milliseconds, or specific error counts:
  - H2: "Ollama tool_use sweep expands if >1 non-seed model fails SQ6c-equivalent smoke"
  - H3: "content_blocks escape-hatch used if >5% of fixtures require it"
  - H4: "Streamlit shim infeasible if FPS <10 on 2-model 10-turn transcript"
  - H5: "ToolCallRecord field deferred if per-call overhead >5ms"
- **Tighten PM[8]:** replace ">2h async-debugging blocker" with specific symptom triggers.

---

## Cross-Round Pattern (for sigma-review team memory)

**`unverified-citation-anti-pattern`:** When evaluation critique flags "self-referential citations," the temptation is to ADD external-looking citations without verification. This produces worse outcomes than either verified primary sources OR declared prior-free reasoning with lowered BELIEF.

- R4 observed: 3× pricing error (Anthropic $0.15 vs actual $0.0512), OWASP V11.1.3 unverified, OpenTelemetry/Jaeger misattributed, LangChain miscited for N>3
- Result: Acc 3→2, Evi 2→1, overall B− (2.86) → C+ (2.57)
- **Correct fix:** every citation survives a 30-second search before inclusion. Plans with declared gaps at lowered BELIEF are more trustworthy than plans with contradicted citations at high BELIEF.

---

## Persistence

- **Summary entry** → `conv.md` in sigma-mem (R4 regression notation)
- **Cross-evaluator pattern** → sigma-review team memory as `unverified-citation-anti-pattern`
- **Combined eval** → `2026-04-20-sigma-chatroom-m1ab.eval.md` (R2 + R3 + R4 rounds)
- **This file** → standalone R4 report for sigma-build handoff
