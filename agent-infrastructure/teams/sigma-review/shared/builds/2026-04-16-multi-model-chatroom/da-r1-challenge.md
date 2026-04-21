# DA R1 Challenge — multi-model-chatroom plan

> Author: devils-advocate
> Build: 2026-04-16-multi-model-chatroom
> Phase: PLAN, Round 1 adversarial challenge
> Scope: first adversarial stress-test following plan-track convergence (R1 de novo + R2 compare against draft + Brad critique)
> Status: FAIL → 5 named conditions for PASS in next round

---

## Summary

DA[plan-r1]: challenges:#10 |severity:{HIGH:#3, MED:#5, LOW:#2} |exit-gate:FAIL →5-named-conditions-for-PASS-next-round

---

## PROMPT-AUDIT (§7d)

- **echo-count:** 3/11 — H1, H2, H3 are near-verbatim echoes of prompt framing ("purpose-built > sigma-verify", "native > /recall", "tool-exec in TurnEngine")
- **unverified-prompt-claim:** H5(60-70%) upgraded to "plausible" via Brad-corroboration, ¬independent numeric verification. However 3-way corroboration (Brad + build-track BC[11] SQ-sum→6d + strategist §2b gap) now UPGRADES to **CONFIRMED under 80th percentile assumptions**
- **missed-claim:** "research instrument not product" treated as axiom — no agent challenged whether C2(Streamlit) is consistent with research-instrument framing (Chainlit is the research-instrument default per designer's own T2 evidence)
- **H-confirm-ratio:** 10/0 (ALL H[] confirmed or partial-confirmed, **ZERO rejected**) — matches P[unanimous-hypothesis-confirmation], **HIGH prompt-laundering signal**
- **methodology:** MIXED — investigative on ADR[6](Ollama native, T1 independently-sourced) + Q1-framing(novel) | confirmatory on H1/H2/H3/H4/H11 (architectural premises universally confirmed)
- **echo-cluster-3+:** NO (agents took different primary focus; no 3+ agents echo same claim)
- **verdict:** pass-with-warning on raw metrics, concerning on H-confirm-ratio pattern

---

## ENGAGEMENT GRADES (plan-r2 compare)

- **tech-architect: B+** — 10 DIV, concede-rate 70% (7/10), 1 DEFEND (Ollama native, T1-evidenced), 1 COMPROMISE, 1 ALIGN. Engaged 7/7 Brad points with specific ADR-impact revisions. Concern: high concede rate is ALSO a compliance pattern — DIV[3,4,7,8,9] absorbed draft choices without the adversarial pressure that a 3rd-party stress-test provides.
- **product-designer: A-** — maintained P=0.65 vs tech-architect P=0.87 **without papering over**. This is the exact signal DA is directed to amplify per task §rule. Explicitly named that the two P values answer DIFFERENT questions. Proposed specific falsifiable M0 test-expansion (render cost <300ms at 80 turns; event-driven trigger doesn't race with timer-rerun). Conceded name-badge framing genuinely (T1 docs finding). DEFENDED neutral-preamble-default with research-instrument reasoning.
- **product-strategist: B+** — 6 DIV, 3 defend (research-question-first, Q1-vs-a, Ollama-native), 2 concede, 1 compromise. Engaged Brad M1-60-70% substantively with partial concede + CAL[M1] revision flag. flag-for-user (OQ[4]) correct process move.
- **implementation-engineer: A-** — 12 BC items substantive, 3-way corroboration with DA on M1 effort (BC[11] 6d point), pairing invariant (BC[6] API-400 risk), Gemini asymmetry (BC[3]), fragment race (BC[9]).
- **code-quality-analyst: A-** — test-coverage=0.52 with specific mock-risk assertions; independently reaches DA[#7] SQ[12] underspec verdict.

---

## BUILD-TRACK CORROBORATION (triangulation, not anchoring)

- BC[5] multi-tool-call policy ↔ DA[#7] SQ[12] fixtures
- **BC[6] pairing invariant on truncation ↔ DA[#7] SQ[12] fixtures** (API-400 risk, HIGH severity — independent find)
- **BC[11] CAL 5d→6d via SQ-sum ↔ DA[#10] CAL-Brad-gap** (3-way agreement: Brad + DA + BC)
- BC[3] Gemini asymmetric-adapter ¬shared-mapping ↔ DA[#9] cross-SDK turn chain
- **BC[9] @st.fragment race ↔ DA[#1] DIV[5] amplification** + designer's (c) condition
- BC[12] SQ[11] ¬parallelizable with SQ[7,8] ↔ DA[#3] IC[7] premature-abstraction
- BC[4] Ollama streaming tool_call chunk shape empirically unverified ↔ DA[#1] extends M0 scope with 4th condition (d)

---

## CHALLENGES

### DA[#1]: VIABILITY P DIVERGENCE NOT RESOLVED (DIV[5] amplification)
**target:** tech-architect + product-designer + lead — SQ[1] M0 scope + VIABILITY[H11] consolidation
**severity:** HIGH

Tech-arch P(go)=0.87; designer P(go)=0.65. Designer refused to converge, named the gap precisely: tech-arch M0 tests "async bridge + tool events" (2h = the (a) condition only); designer requires ALSO **(b) render cost <300ms at 80 turns** + **(c) event-driven trigger does not race with timer-rerun**. Locked SQ[1] M0 scope is tech-arch's narrower (a)-only. Per task directive: this is the **"both-right divergence to amplify."** Resolution is ¬compromise-P, it is EXPANDING M0 scope OR locking plan with P=0.65 and named uncertainty. BC[9] independently confirms fragment race is real risk.

**evidence:** SCRATCH line 1192 "The divergence is load-bearing. DA should assess as such." | DB[DS1](3) concrete math: "80-item list + 80 chat_message calls @ 50ms each = 4s loop, exceeds 1s rerun interval → backlog" | SQ[F6] 2-4h (designer) vs SQ[1] 2h (tech-arch) | BC[9] fragment race flagged by build-track | outcome 3 (gap)

**→ REVISE:** SQ[1] M0 expanded to 3-4h with four pass-conditions (a)+(b)+(c)+(d) where (d) = BC[4] Ollama native streaming tool_call chunk shape verification. All-pass → P converges 0.85+. Only (a) passes → P=0.65 is correct, plan locks with named risk.

### DA[#2]: M0 FALLBACK MISSING ADR (§4b + §2e)
**target:** tech-architect + lead — ADR[5] kill-switch ownership
**severity:** HIGH

Lead flagged M0-kill-switch-ownership at step-17. Strategist says "user decides instrument shape"; tech-arch ADR[5] fallback is "queue-based bridge" addressing ONLY async-bridge failure; strategist Alt-C (headless JSONL + Jupyter) never adopted into any locked ADR. Plan has kill-switch (M0 gate) but **NO ADR for what happens when the kill fires**. Punted decision is not architecture — it's deferral. §2e(4): "if most speculative assumption is wrong, what's the fallback?" — no locked fallback exists.

**evidence:** SCRATCH line 1739 lead-flagged | ADR[5] fallback is narrow | strategist Alt-C is proposal ¬ADR | outcome 3 (gap)

**→ REVISE:** lock ADR[9] M0-fallback decision tree:
- (a) async-bridge fails → queue-bridge (tech-arch)
- (b) 80-turn render fails → windowed-render OR Textual TUI (designer)
- (c) both fail → headless JSONL + Jupyter (strategist Alt-C)
- (d) Ollama native streaming chunk-shape wrong → OllamaProvider non-streaming-for-tools mode (BC[4])

Pre-commit tree replaces "user decides" handoff.

### DA[#3]: IC[7] ChatOrchestrator PREMATURE ABSTRACTION (§4c gold-plating)
**target:** tech-architect — IC[7] + SQ[11]
**severity:** MED

IC[2] TurnEngine.run_turn yields AsyncIterator[ChatEvent] for one FULL turn including tool loops. IC[7] ChatOrchestrator.run_round loops "each provider in roster order takes one turn"; run_autonomous(max_rounds) loops rounds. At v1 (3 models, sequential, YieldNextPolicy) what does IC[7] OWN that isn't a for-loop wrapping IC[2]? SQ[11]=5h for YieldNextPolicy(~30 LOC) + session-writer dispatch(~20 LOC) + loop(~15 LOC). Module for a function. IC[7].§2c check is **MISSING** — no explicit justification of the abstraction beyond IC[2]. BC[12] adds: SQ[11] cannot parallelize with SQ[7,8] — further confirms it's a thin coordinator, not module-scale.

**evidence:** IC[7] has no peers (only cli.py + streamlit_app.py consume it) | YieldNextPolicy already separate (yield_policy.py) | §2c justification absent for IC[7] | BC[12] sequencing constraint | outcome 3 (gap)

**→ DEFEND-or-revise:** (a) justify IC[7] with concrete v1 responsibilities not covered by IC[2]+YieldNextPolicy+SessionWriter, OR (b) collapse IC[7] into cli.py/streamlit_app.py as ~20-line coordinator. P[unconditional-infrequent-ops] applies: single-consumer orchestration ¬needs class.

### DA[#4]: SQ[17] 13-PROVIDER YAML AT v1 = GOLD-PLATING (§4c)
**target:** tech-architect — SQ[17]
**severity:** MED

v1 ship gate = "3-model autonomous, sigma_mem_recall available." SQ[17] ships 13-provider YAML + env-key discovery for 10 providers that are tool_use_reliability="unknown" (never empirically tested). §4c: v1 requires 3 providers, not 13. "Unknown" default is literal signal we haven't tested them; why ship what we can't characterize?

**evidence:** v1 ship-gate = "3-model" ¬"13-available" | tool_use_reliability=unknown for 10/13 at v1 | SQ[17]=3h is 10% of M3 budget for speculative capacity | outcome 3 (gap)

**→ REVISE:** SQ[17] at v1 ships only providers with empirical tool_use_reliability != "unknown" (likely 3-5 per project memory: claude-opus-4-7, one OpenAI, one Gemini, one Ollama cloud, one Ollama local). Other 8-10 commented-out with "pending empirical test." Graduate providers as they move off "unknown." Saves 2h, better instrument honesty.

### DA[#5]: ADR[6] OLLAMA-NATIVE REVERSAL CONDITION UNREACHABLE (CQoT-6)
**target:** tech-architect — ADR[6]
**severity:** MED

ADR[6] states "IF Ollama native /api/chat ALSO exhibits streaming tool_call drop THEN disable tool-use for Ollama." Fires on tail-risk of DIFFERENT bug in DIFFERENT endpoint. Does NOT address the natural future state: **IF Ollama patches compat layer (tracked in issue #11828 per plan's own evidence)** THEN ADR[6] is unnecessary complexity and compat subclass would save effort. CQoT-6: is reversal condition reachable? As-stated = tail-risk-bug. As-unstated-but-natural = upstream-fix. Plan locks workaround without sunset/check-fix cadence.

**evidence:** issue #11828 is tracked-not-fixed per plan evidence | ADR[6] has no re-evaluate trigger | outcome 2 (confirm with gap)

**→ REVISE:** add re-evaluation trigger: "re-evaluate ADR[6] at every ollama-python minor bump; IF changelog mentions #11828 fix + compat-streaming-tool support confirmed THEN M0-style retest + consider OpenAI-compat subclass at M4." Gives ADR[6] a life-cycle.

### DA[#6]: DS[2] T3-CONTRAST-MATH UNGATED (§2d+ load-bearing T3 violation)
**target:** product-designer — DS[2] 13-hue palette WCAG claim
**severity:** MED

§2d+ rule: "architecture decisions resting on T3 sources → DA challenge in r2." Two T3 sources in load-bearing positions:
- (a) DS[4] tool-badge novel-pattern: designer self-flagged, **GATED by F6 prototype ✓**
- (b) DS[2] WCAG 4.5:1 via HSL math: "claimed via HSL math... FLAGGED: T3... validate before ship" — **UNGATED ✗**, deferred to "UI engineer validates before ship"

A 10-min contrast-checker run (webaim.org) resolves this pre-lock. Deferring = build starts against unvalidated palette.

**evidence:** DS[2] line 757 self-flagged T3 | DS[4] has F6 gate; DS[2] has no gate | outcome 3 (gap)

**→ REVISE:** run contrast checker on 13-hue palette **BEFORE plan-lock**. If any hue fails 4.5:1 → revise. Converts T3→T1 in 10 min.

### DA[#7]: SQ[12] M1 INTEGRATION TEST UNDERSPECIFIED (§4d test integrity)
**target:** tech-architect — SQ[12]
**severity:** HIGH

SQ[12] = "headless 2-model session (Anthropic+Ollama), one tool call, JSONL verified." §4d: does this catch plan's named risks?
- **Gemini function_response round-trip?** NO (Gemini ¬in seed pair; biggest PM[1] risk; deferred where?)
- **Ollama malformed-tool silent-drop (H8)?** "one tool call" = happy-path; null-case not asserted
- **Multi-turn tool-call fixture per ADR[4] "merge gate"?** "Hardest fixture: 3-turn conversation with one tool call mid-turn." SQ[12] says "one tool call" ¬"mid-turn in 3-turn."
- **Session state corruption (PM[4])?** Not tested.
- **Concurrent provider rate-limit?** Not tested.
- **BC[6] pairing invariant on truncation?** Not tested (produces API-400 in production).
- **BC[5] multi-tool-call-per-response handling?** Not tested.

§4d: tests verify REQUIREMENTS. SQ[12] as-spec could pass with single-turn echo happy-path and miss 5+ named integration risks. BC[10] and code-quality-analyst independently reach same conclusion.

**evidence:** ADR[4] merge-gate fixture = "3-turn with mid-tool-call" — SQ[12] doesn't call it | PM[1,4,5] ¬mapped to assertions | PM[D2] raw-event precondition ¬asserted in SQ[12] | BC[6] pairing-invariant API-400 risk | outcome 1 (revise)

**→ REVISE:** SQ[12] explicit fixtures:
- (i) 3-turn Anthropic+Ollama with mid-conversation tool call (ADR[4] merge-gate)
- (ii) Ollama-declined-tool null-case asserting raw sidecar captures SDK response even when tool_result empty
- (iii) session_state persistence across 2 tool-loop iterations
- (iv) truncation preserving tool_call/tool_result pairing (BC[6])
- (v) multi-tool-call-per-response handling (BC[5])

Add SQ[12b]: 4-SDK adapter round-trip fixture test matching ADR[4] merge gate BEFORE M1d sign-off, ¬pushed to M3.

### DA[#8]: ADR[5] CQoT STEELMAN OF CONCURRENT STREAMING WEAK (CQoT-7)
**target:** tech-architect — ADR[5] DB[]
**severity:** LOW

ADR[5] rejects concurrent multi-model streaming with 3 reasons:
1. models need to read each other's output — valid research-instrument argument
2. Streamlit threading fragile — ENVIRONMENT argument ¬architecture argument
3. turn-ordering is experimental variable — valid

Strongest steelman ¬tested: **Poe Group Chats handles 200 models concurrently** (designer's OWN DS[2] cites Poe as precedent). Plan did not engage with "why can Poe do concurrent if we can't?" Answer: Poe is custom React ¬Streamlit. ADR[5] resolves to: "Streamlit forces sequential; different UI tech makes concurrent viable." Matters because Alt-C (headless JSONL) and Textual TUI both support concurrent — M0-failure fallbacks UNLOCK concurrent streaming.

**evidence:** DS[2] cites "Poe Group Chats (up to 200 models)" as precedent | ADR[5] rejects concurrent with Streamlit-threading reason | DB[ADR-5] did not steelman Poe | outcome 2 (acknowledged weakness)

**→ DEFEND-or-note:** not asking to change ADR[5]. Asking explicit note: "ADR[5] sequential-turn-taking is Streamlit-constrained; IF M0 fails and fallback is Textual TUI or headless, concurrent streaming becomes viable and ADR[5] does not carry over." Preserves design clarity for fallback path.

### DA[#9]: IC[2]↔IC[3]↔IC[7] CROSS-SDK TURN CHAIN UNTESTED (§4b assumption conflict)
**target:** cross-agent — interface contracts for multi-provider history round-trip
**severity:** MED

DIV[3] settled canonical Message = OpenAI-shaped; adapters own complexity. Creates REVERSE round-trip question: when Gemini emits function_call output via gemini_provider.stream(), Provider must reverse-translate Gemini's function_call-in-part → OpenAI-canonical tool_call before emitting into ChatEvent. SQ[5] Gemini=5h includes reverse adapter. But ADR[4] "round-trip fixture test" is the FORWARD direction (canonical → Gemini). Where is the assertion that a Gemini response correctly reverse-maps to an OpenAI-canonical Message that Anthropic reads on the next turn? Chain = Gemini-response → reverse-adapter → canonical → forward-adapter → Anthropic-input. Two hops. Plan does not state whether CROSS-SDK turn chain is tested. BC[3] independently flags Gemini asymmetric-adapter cannot share message_mapping with other providers.

**evidence:** ADR[4] "parse_response(sdk_response) → CanonicalMessage" = reverse direction | SQ[5]=5h but BC[3] argues 6-8h | no SQ[] explicitly asserts "Gemini-tool-call on turn N, Anthropic reads on turn N+1" | BC[3] asymmetric-adapter | outcome 3 (gap)

**→ REVISE:** add to SQ[12b]: cross-SDK turn chain fixture — Gemini emits tool_call on turn 1, Anthropic reads history on turn 2, tool_call appears correctly in Anthropic's input as content-blocks. This is the hard part of message-mapping that plan names as hard but does not test.

### DA[#10]: CAL[M1] 4d→5d INSUFFICIENT CLOSURE OF BRAD GAP (§2b) — 3-way corroborated
**target:** tech-architect — CAL[M1-engine]
**severity:** LOW

Brad's 60-70% is independent external review. CAL revised 4d→5d (20%). Strategist computed Brad's 60-70% requires M1≈6-7d of total=10-12d. Build-track BC[11] computes SQ-sum → 6d point. **3-way agreement (Brad+BC[11]+DA-reasoning) on 6d being better estimate than 5d.** §2b: revision doesn't close gap with 3 independent sources.

**evidence:** CAL[M1] 90%=10d, total 90%=18d | Brad 60-70% × total=15-17d → M1=10-12d | BC[11] SQ-sum breakdown → 6d | outcome 2 (confirmed)

**→ REVISE:** accept BC[11] recommendation. CAL[M1] point=6d, 80%=[4.5d,9d]. Ship-date communication: "v1 ready" = 14-18d ¬10-11d.

---

## EXIT-GATE VERDICT

```
DA-exit-gate plan-r1: FAIL
|engagement: tech-architect=B+ product-designer=A- product-strategist=B+ implementation-engineer=A- code-quality-analyst=A-
|unresolved: DIV[5]-VIABILITY-P-divergence, M0-fallback-ADR-missing, IC[7]-abstraction-justification, SQ[12]-fixture-underspec, DS[2]-T3-contrast-pre-lock-validation, ADR[6]-falsifiability, BC[5]-multi-tool-call-policy, BC[6]-pairing-invariant
|hygiene: pass(§2a/§2b/§2c/§2d/§2e all outcome-tagged across agents)
|prompt-contamination: fail-H-confirm-ratio-10/0-unanimous-confirmation-pattern
|cqot: fail-6(ADR[6] reversal unreachable-for-natural-failure-mode), fail-7(ADR[5] Poe-steelman absent)
|xverify: skip-reasoned-accepted-by-lead-step-15
```

### FAIL criteria detail (per AGENT-DEF exit-gate)

- **(2) unresolved:** DIV[5] load-bearing P divergence papered-over by dual-declaration, ¬resolved at plan level; M0 fallback missing ADR; BC[5]+BC[6] interfaces not updated
- **(3) new-consensus-without-stress-test:** R2 DIV[3,4,6,7,8,9] absorbed draft choices without adversarial pressure — DA[#3] IC[7] + DA[#4] 13-provider-YAML are first adversarial stress on these
- **(5) prompt-contamination:** 10/0 H-ratio hits P[unanimous-hypothesis-confirmation]
- **(6,7) CQoT falsifiability + steelman:** ADR[6] reversal unreachable for natural failure mode; ADR[5] Poe steelman absent

### CONDITIONS FOR PASS (5 named, per T[exit-gate-condition-setting-as-leverage])

1. **DIV[5] resolved** — expand SQ[1] M0 to cover designer's (b)+(c) + BC[4]'s (d) OR lock plan with P=0.65 + named uncertainty
2. **ADR[9] M0-fallback decision tree locked** (per DA[#2]) with 4 branches
3. **SQ[12] fixtures explicitly named** consolidating DA[#7]+DA[#9]+BC[5]+BC[6]
4. **DS[2] contrast math validated with tool (10-min) BEFORE plan-lock** OR palette revised — DA[#6]
5. **One of:** IC[7] justified concretely with v1 responsibilities OR collapsed to cli.py coordinator — DA[#3]

not-blocking for PASS but recommended: DA[#4] 13-provider-YAML (scope question, lead decides), DA[#5] ADR[6] sunset trigger, DA[#8] ADR[5] Poe-steelman note, DA[#10] CAL→6d (accept BC[11])

### Recommendation

**ANOTHER ROUND.** P(plan-ready) ≈ 0.55-0.65 after this challenge. ¬Toulmin-needed (5 conditions mechanical + specific). IF conditions addressed in R2 → exit-gate re-eval likely PASS → lock-plan.

---

## Source-provenance audit (§2d+)

- **T1 load-bearing:** ADR[6] Ollama-compat-bug (ollama#12557 maintainer-confirmed), Streamlit async-gen support (docs.streamlit.io), BFCL V4 (strategist Q1 anchor), Brad preamble-as-study-variable, BC[1,2,6,7,8] SDK docs
- **T2 load-bearing:** Streamlit SSE perf (markaicode.com), st.fragment (docs.streamlit.io), Chainlit comparison, sigma-ui fragment precedent (cross-agent memory), BC[3,4,9,10] community+migration docs, BC[10] project-memory-mock-tests-pattern
- **T3 load-bearing:** DS[4] tool-badge novel-pattern — **GATED by F6 ✓** | DS[2] WCAG-math — **UNGATED ✗** | ADR[2] TurnEngine-as-loop (convention, low risk) | ADR[5] sequential-turn (autogen/crewai precedent T2 + steelman T3) | BC[5,11,12] agent-inference architectural-judgment

**tier distribution:** acceptable IF DA[#6] revision executed (validate DS[2] pre-lock). Without it: 2 ungated T3 in load-bearing positions exceeds tolerance.

---

## Both-right-is-fine (per task §rule)

product-designer P=0.65 maintenance is **explicitly stronger analysis** than tech-architect P=0.87. The two answer different questions. Designer named it, proposed specific falsifiable test-expansion, did not collapse. This is A-grade DA-aligned behavior and should be structurally reinforced: **plan-lock must preserve the distinct P values with named conditions, not average them.**

---

## BELIEF[plan-r1] — devils-advocate component

- ADR[6] Ollama-native: **P=0.90** (T1 evidence + tech-arch defend) | falsifiability gap noted DA[#5]
- ADR[5] sequential-turn-taking: **P=0.80** (framework-constrained, not architecture-pure) | steelman gap noted DA[#8]
- ADR[4] OpenAI-canonical message shape: **P=0.80** (R2 convergence + LiteLLM/LangChain T2) | BC[6] pairing invariant must be addressed in IC[3]
- IC[7] ChatOrchestrator abstraction at v1: **P=0.45** (DA[#3] premature abstraction) | BC[12] sequencing confirms
- **VIABILITY[H11] UI-complete: P=0.65** (designer maintained, DA amplifies) ← LOAD-BEARING
- VIABILITY[H11] async-bridge-only: **P=0.85** (tech-arch narrower question)
- M1 effort vs reference class: **P(CAL-5d-point-hits)=0.30** (§2b + 3-way corroboration argues 6d) | P(CAL-90%-band-hits)=0.75
- SQ[12] as-written catches integration risks: **P=0.30** (DA[#7] + BC[10] + code-quality-analyst)
- CAL[M1-engine]=6d more accurate than 5d: **P=0.80** (BC[11]+Brad+DA 3-way)
- Brad critique unaddressed point exists: **P=0.15** (7/7 engaged)

→ **P(plan-ready) ≈ 0.55-0.65**

---

## Status

DA ¬terminate-post-r1 | awaiting-lead-message for next-round-signal OR lock-plan-signal | per AGENT-DEF DA controls exit timing, 3-round-minimum, 5-round-max | **WAIT**
