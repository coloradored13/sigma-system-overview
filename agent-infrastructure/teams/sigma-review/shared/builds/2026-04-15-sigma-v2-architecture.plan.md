# sigma-build plan: sigma-v2-architecture

## Meta
- created: 2026-04-15
- build-id: 2026-04-15-sigma-v2-architecture
- tier: BUILD TIER-2
- status: plan-locked
- plan-exit-gate: PASS
- plan-belief: P=0.82
- build-exit-gate: PENDING
- build-belief: P=0.00
- output-label: lead-framed, team-validated refinement of existing analysis with paradigm shift exploration

---

## Context

The sigma stack (sigma-review, sigma-build, sigma-verify, sigma-mem, hateoas-agent, orchestrator, hooks, agents, skills, teams) was built across 8+ repos over 2 months. It works: 10 reviews, 7 builds, hard-won calibration data. The question this build addresses: if we rebuilt the entire stack from scratch today — with full knowledge of every correction, audit failure, process violation, and lesson learned — what would we build differently?

An existing analysis (buzzing-painting-thompson.md) proposes 7 changes. The team was tasked to independently assess the codebase, form their own conclusions, compare to the analysis, and produce a prioritized, phased implementation plan.

The user's goal is highest analytical output quality, not simplest architecture. Simplification is only justified where it demonstrably serves quality or removes friction without degrading enforcement.

**Important methodological constraint (DA[#13] finding):** The team's output is a validated refinement of the existing analysis, not an independently derived architecture. Agents were anchored to the analysis's 7-proposal frame from the start. This is accurately labeled here. The paradigm shift section (Options 1-3) is the genuinely greenfield contribution.

---

## Prompt Understanding

### Q[] — What to answer
- Q1: If we rebuilt the sigma-stack from scratch today, what would we build differently?
- Q2: Where team findings overlap with the analysis's 7 proposals, validate the reasoning. Where they diverge, explain why.
- Q3: Produce a prioritized, sequenced implementation plan. Multi-session build expected. Phase 1 = highest-impact changes.
- Q4: Design an A/B comparison methodology — run baseline prompts through V1 and V2 for measurable quality comparison across both ANALYZE and BUILD paths.

### H[] — Claims to test
- H1: Most value comes from process, most complexity from infrastructure. (Load-bearing thesis.)
- H2: ΣComm adds overhead without proportional value — plain English suffices.
- H3: Mono-repo for sigma-system would reduce maintenance overhead.
- H4: Auto-memory creates drift — removing it simplifies without quality loss.
- H5: Three messaging mechanisms are redundant — two suffice.
- H6: 42 skills consuming context when <10 are used (under-tested: 2 weeks, one corrupted session).
- H7: Same process enforcement + simpler infrastructure = equivalent or better output quality.

### H[] verdicts (post-team-analysis)
- H1: PARTIALLY TRUE but imprecisely framed. Enforcement infrastructure IS what makes process reliable. H1 implies infrastructure is separable overhead — evidence refutes this. False dichotomy: "most complexity from infrastructure" is true, but that complexity is load-bearing for the process quality.
- H2: LIKELY TRUE — SIMPLIFY NOT DROP. Mandatory-field structure is the functional value, not compression. BUT: this is not fully proven without A/B test (A/B-before-Phase-3 constraint). ΣComm in sigma-mem entries (200-line constraint) is a separate question from agent workspace format.
- H3: CONFIRMED FOR OVERHEAD — WRONG FIX. setup.sh grew +68% to 724 lines (compounding signal). pip deps (not source-package merge into mono-repo) is the correct fix. Namespace rename adds ~420 test rewrites.
- H4: WEAKLY CONFIRMED — WRONG FIX. Platform constraint: MEMORY.md is loaded by Claude Code platform regardless of code changes. Full removal not achievable. Stub-redirect is the achievable path.
- H5: CONFIRMED AND STRENGTHENED. CQA M5 empirical evidence: all 20 markdown inbox files are 1 byte. Inboxes are never used. Correct label: the markdown inbox boot step is dead code. JSON inboxes ARE SendMessage (TeamCreate native) — they're not a separate mechanism.
- H6: UNCERTAIN, LOW PRIORITY. Domain skills don't load unless invoked. Listing is ~997 tokens always. Context cost claim needs measurement. The concern is routing signal degradation at scale, not context window performance.
- H7: UNPROVEN. Load-bearing hypothesis. No empirical test run. Burden of proof is against H7 given enforcement gaps are the primary failure mode. Do NOT assume H7 true. A/B test is the gate.

### C[] — Constraints
- C1: Self-reference problem — agents assessing their own infrastructure. Acknowledged; flagged throughout.
- C2: Working system. Any change must clear "demonstrably better," not "aesthetically cleaner."
- C3: Goal is highest quality analytical/build output. Not simplest, not fewest repos.
- C4: Multi-model vision is roadmap, not current requirement.
- C5: Process enforcement (hooks, gates, mechanical checks) is non-negotiable.
- C6: Multi-session build expected. Plan should be phased and sequenced by priority/impact.
- C7: Full stack in scope — sigma-mem, sigma-verify, hateoas-agent internals included.

---

## Scope Boundary

**This build implements:** A prioritized, sequenced plan for rebuilding the sigma-stack based on team-validated findings. Phase 1 changes only in C2 (the build conversation). Paradigm shift architecture decisions documented but not implemented until Phase 3+.

**This build does NOT implement:** All changes in a single session. Multi-model agent spawning. New sigma-predict or sigma-optimize features. The Option 1 orchestrator-as-driver system (documented here as the V2 target architecture; implementation is Phase 4). Full role decomposition (Option 3 — V3+ after Option 1 observables validated).

---

## Architecture Decisions (locked)

**ADR[1]: sigma-system-overview → sigma-core with pip deps for sigma-mem/sigma-verify.**
Current: 3 submodules (hateoas-agent, sigma-mem, sigma-verify), setup.sh at 724 lines (+68% growth). Problem: submodule pinning + installed-vs-repo drift + conceptual confusion (where to edit?). Fix: sigma-mem and sigma-verify as pip deps (PyPI publish), not source subpackages merged into mono-repo. Rationale for pip over source merge: ~420 test rewrites + namespace rename + MCP re-registration if import paths change. Pip deps eliminate submodule pinning without touching import chains. Migration sequence: PyPI publish → test installed packages → update .claude.json → THEN remove submodules. hateoas-agent stays separate (genuine standalone library, public, has its own users). Effort: MEDIUM (3-4 sessions).

**ADR[2]: ΣComm → structured-field format with named mandatory fields.**
Preserve ✓◌!?✗↻ status codes as header signals (XVERIFY finding: two external models confirmed rapid-routing function; 90% preservation claim withdrawn). Drop compressed body notation (|,>=! symbols in body text). Preserve ¬ and → as mandatory named fields (ruling-out, next-actions). PRIMARY MOTIVATION: operator auditability (corrected from "agent token savings" per DA[#1] — CQA measured 147 lines/agent overhead but never measured operator audit time; 10/12 corrections are operator verification failures). SECONDARY MOTIVATION: machine-readable workspace format is a prerequisite for automated gate checking in Option 1 orchestrator (ADR[8] dependency). Scope: agent messages and workspace. sigma-mem entries retain ΣComm (200-line constraint applies there). CONSTRAINT: SQ[9] (hook regex update) must complete BEFORE SQ[7/8] (agent format change) — window between format change and regex update leaves enforcer failing open. Effort: MEDIUM (2-3 sessions + 1 session hook regex).

**ADR[3]: memory-sync-reminder.py NUDGE → BLOCK for GLOBAL_PATTERNS writes.**
memory-sync-reminder.py (188 lines) declares "NUDGE, not a BLOCK — exit code 0 always." feedback_warns-must-be-blocks.md principle: a WARN the lead can ignore has the same failure mode as a directive it can ignore. For GLOBAL_PATTERNS writes, there is no legitimate override case. Fix: ~20 LOC change to return exit code 2 for GLOBAL_PATTERNS writes. This is prophylactic hardening (no documented failure of this specific path); labeled accurately as such, not as "highest-confidence fix." Effort: LOW (0.5 session).

**ADR[4]: sigma-verify as pip dep (not submodule).**
Same rationale as ADR[1] for sigma-mem. sigma-verify's OllamaBaseProvider (clients.py:~202) is the future multi-model routing interface — keeping it as a pip dep (not embedding in mono-repo) is correct regardless of multi-model timeline. Effort: LOW-MEDIUM (1-2 sessions).

**ADR[5]: Remove dead 13-phase BUILD workflow from orchestrator-config.py.**
orchestrator-config.py (1,052 lines, ZERO tests) defines both ANALYZE and BUILD workflows. BUILD workflow defines 13 phases that are NEVER USED — actual BUILD uses 3-conversation phase files (c1-plan.md, c2-build.md, c3-review.md). The phase-compliance-enforcer's BUILD_PHASE_MAP contains both legacy (00-preflight through 10-shutdown) and v2 (c1-plan, c2-build, c3-review) entries. Dead code must be removed. ATOMIC: orchestrator-config.py and BUILD_PHASE_MAP in enforcer must change together. Depends on SQ[0] (orchestrator tests must exist before modifying orchestrator). Effort: LOW (0.5 session, after SQ[0]).

**ADR[6]: Extract _protocol.md; formalize injection pattern as BUG-B workaround.**
BUG-B (#24316): agent definitions cannot be team templates; lead embeds full Role+Expertise+ΣComm codebook inline in every spawn prompt. Consequence: _protocol.md extraction provides NO token savings while BUG-B is active (lead inlines anyway). Architectural value NOW: single source of truth for protocol changes (currently updating a rule means updating the template and hoping agents pick it up). Token savings WHEN #24316 closes. CQA M1: 65.5% of agent content (1,897 lines across 24 agents) is template-duplicated. Effort: LOW (0.5 session). Best combined with SQ[7/8] to save one agent-definition rewrite pass.

**ADR[7]: Drop markdown inbox boot step from agent template.**
CQA M5 empirical finding: all 20 markdown inbox files are 1 byte (empty). The markdown inbox format (sigma-comm.md: ~/.claude/teams/{team}/inboxes/{name}.md) is LEGACY, superseded by JSON inboxes (TeamCreate native). Active teams use JSON inboxes — these ARE SendMessage, not a separate mechanism. Boot step 3 ("process inbox .md") is dead code. Fix: remove Boot step 3 from _template.md and all 32 agent spawn instructions. Do NOT remove JSON inbox infrastructure (it is SendMessage). Effort: LOW (1-2 hours).

**ADR[8]: DA Function A (gate authority) → orchestrator mechanical advance() check.**
PS XVERIFY finding (3 external models): DA role bundles two separable functions. Function A = exit-gate authority (mechanical — blocks synthesis, forces round completion). Function B = adversarial content generation (analytical — surfaces confirmation bias, herding, framing errors). External models confirmed: Function A is separable and replicable at lower cost. Function B is the DA-specific value (checklist gates cannot catch analysis-quality failures like H1 divergence between agents, integration risk gaps, failure catalogue incompleteness). V2 implementation: move Function A to orchestrator's advance() gate check (parses workspace for DA-PASS mechanically, string match against structured-field format — ADR[2] dependency). DA agent keeps Function B only (lightweight challenge agent, no gate authority). This is also the first concrete step toward Option 1 (orchestrator-as-driver). Effort: MEDIUM (0.5-1 session). Depends on ADR[2] structured format being parseable.

**IC[2] removed:** sigma-verify VerificationProvider Protocol interface was proposed as ADR but removed per DA[#15] (premature abstraction — C4 states multi-model is roadmap not current requirement; no corresponding SQ; designing for unvalidated use case). Can be designed when multi-model validation produces actual requirements.

---

## Interface Contracts (locked)

**IC[1]: V2 agent output structured-field format (updated post-XVERIFY).**
```
### {agent-name}: {✓|◌|!|?|✗} {one-line summary}
- Finding: {specific claim with location} |source:{type}({quality-tier})
- Ruling out: {what was checked and not the issue — required when DA challenge exists}
- Next actions: {what can be done based on this finding}
- DA-response: DA[#N]: {concede|defend|compromise} — {evidence}
```
Status header symbols kept (✓◌!?✗↻ — XVERIFY confirmed rapid-routing function). Compressed body notation removed from all fields except header symbol. Mandatory named fields (ruling-out, next-actions) replace ¬ and → notation.

**IC[3]: Cross-session BUILD bridge (workspace section, replaces inboxes for cross-conversation state).**
```
plan-locked | plan-file | phase:{c1|c2|c3} | open-SQs | open-ADRs | last-updated
```
sigma-mem persists at C1 end; C2 boot reads via recall. This is how all 3-conversation builds (and future ANALYZE conversation-boundary model) bridge context across sessions.

---

## Sub-task Decomposition

### Phase 1: V1 hotfixes (ship NOW, no V2 dependency)

**SQ[1]: Verify never-advance loophole coverage — V1 HOTFIX.**
Effort: 0.25 session (verification, not implementation). IE CRITICAL CORRECTION: Layer 1c SendMessage BLOCK already exists in phase-compliance-enforcer.py (lines 446-488, added 26.4.13) — fires on SendMessage during non-build phases when content matches implementation dispatch patterns. SQ[1] scope is NOT "implement from scratch" — it is: (a) verify TeamCreate agent-spawning path has equivalent BLOCK coverage (likely a gap), (b) verify code-write authorization gate covers all write/edit B7 dispatch vectors. V1-applicable, no V2 dependency.

**SQ[2]: Promote XVERIFY-unused WARN → BLOCK — V1 HOTFIX.**
Effort: 0.25 session (~5 LOC). Lines 792-796 of phase-compliance-enforcer.py: XVERIFY unused check appends to warnings array (soft WARN, exit code 0). Promotion: route XVERIFY-unused case to exit code 2 instead. V1-applicable, no V2 dependency. IE confirmed: fully open, zero progress since correction file written.

**SQ[3]: Drop markdown inbox boot step — V1 HOTFIX.**
Effort: 1-2 hours. Remove Boot step 3 from _template.md. Update 32 agent spawn instruction sets. CQA M5 empirical basis (all 20 inbox files = 1 byte). No coordination regression risk (JSON inboxes/SendMessage unaffected).

### Phase 2: V1 structural cleanup

**SQ[0]: Write orchestrator-config.py tests — PREREQUISITE to SQ[4].**
Effort: 1 session (~50 tests). orchestrator-config.py (1,052 lines, 0 tests) contains phase transition guards, belief computation, checkpoint/restore, BUILD sub-workflows. Gate_checks.py has 84 tests; orchestrator has zero. Modifying untested enforcement substrate is the B7-class gap category (system appeared to work, had a hole). Must complete before SQ[4]. Tests cover: phase transition guards, context evaluation, belief computation, checkpoint/restore, BUILD sub-workflow transitions.

**SQ[4]: Decide and clean orchestrator BUILD strategy — depends on SQ[0].**
Effort: 0.5 session. Resolve: does BUILD use orchestrator state machine or manual phase-file reading? Currently both exist (dead 13-phase orchestrator workflow + live 3-conversation phase files). Correct answer per IE+CQA: 3-conversation model IS the architecture, orchestrator BUILD mode was updated 26.4.13 to match. Remove legacy 13-phase entries. ATOMIC: orchestrator-config.py and BUILD_PHASE_MAP in enforcer change together. Verify with BUILD phase sequence after change.

**SQ[5]: Mono-repo consolidation (without namespace rename) — depends on SQ[4]+PyPI prereqs.**
Effort: 1-1.5 sessions. Consolidate sigma-system-overview structure; sigma-mem + sigma-verify as pip deps (requires SQ[4] + PyPI publish from SQ[6-repo steps]). Keep existing package names (no import chain rewrite, no ~420 test rewrites). MCP re-registration is the critical migration step — test `claude mcp list` + sigma-mem recall in a fresh session BEFORE decommissioning old repos. Keep old repos 2 weeks post-migration.

**SQ[6]: Memory stub-redirect — depends on SQ[5] MCP verification.**
Effort: 0.5 session. MEMORY.md (platform-loaded, cannot be removed) → stub that routes to sigma-mem recall. Achieves the "two-layer" memory goal within the platform constraint. SEQUENCING DEPENDENCY: SQ[5] MCP re-registration must be verified first (CQA M4xM6 interaction: stub redirects to sigma-mem path; if path changed by mono-repo migration, stub redirects silently to broken path).

**SQ[9]: Update hook regex patterns for structured-field format — depends on ADR[2] format definition, MUST PRECEDE SQ[7/8].**
Effort: 0.5 session. phase-compliance-enforcer.py lines 44-122, 293, 324, 654-655: regex patterns for exit.gate:.*PASS, BELIEF\[, CB\[], XVERIFY[]. If format changes to structured plain English BEFORE regex updates, enforcer fails open during the transition window (no DA exit-gate detection, no BELIEF requirement, no CB evidence check). SQ[9] MUST complete and be tested before SQ[7] goes live. Extend test_gate_checks.py to cover new format.

**ADR[8] implementation (DA Function A → orchestrator): parallel with Phase 2.**
Effort: 0.5-1 session. Update orchestrator-config.py advance() to parse workspace for DA-PASS mechanically (string match against structured-field format from IC[1]). DA agent no longer holds gate authority — orchestrator evaluates PASS condition. DA still generates challenges. Depends on ADR[2] format being finalized (SQ[9]).

### Phase 3: Protocol simplification (GATED on H7 A/B test)

**V1 A/B baseline — run BEFORE Phase 3 commits.**
ANALYZE: loan-admin KB coverage evaluation prompt (existing review 26.3.13, operator has V1 ground truth). Not circular — agents analyzing loan-admin documents have no knowledge of sigma architecture. BUILD: SQ[3] (inbox removal) — concrete implementation task. Methodology: N=3 paired comparisons, per-gate pass/fail measurement (28 gate functions × N sessions = ~84 binary observations), user as blind evaluator of synthesis output quality, pre-registered pass threshold. Phase 3 DOES NOT proceed until V1 baseline is established.

**SQ[7]: Rewrite agent template in structured plain English — depends on SQ[9].**
Effort: 1 session.

**SQ[8]: Update 32 agent definition files — depends on SQ[7].**
Effort: 2 sessions.

**SQ[10]: Conversation-boundary ANALYZE (Option 2 paradigm test) — parallel with SQ[7/8].**
Effort: 1-2 sessions. Replace 12 ANALYZE phase files with 3-conversation model (C0:preflight+spawn, C1:research+circuit-breaker, C2:challenge+debate, C3:synthesis+tail). Update phase-compliance-enforcer ANALYZE_PHASE_MAP. sigma-mem bridges conversations (IC[3]). This is the Option 2 paradigm test — conservative structural change, validates whether conversation-boundary enforcement addresses tail-phase skip without breaking within-conversation quality.

**SQ[6-ext]: Extract _protocol.md + injection pattern (ADR[6]) — combine with SQ[7/8].**
Effort: combined in SQ[7/8] sessions. Save one agent-definition rewrite pass by doing protocol extraction and format change together.

### Phase 4: Orchestrator-as-driver (Option 1) — sigma-ui completion

**sigma-ui Phase C: promote to production.**
Effort: 2-3 sessions. sigma-ui is 70% complete (Phase B3: 16 modules, 280 tests, execution_loop.py bridge). Remaining work: (a) remove TIER-1 human-gate blocking (orchestrator advances autonomously when mechanical conditions met), (b) add criterion pre-registration interface at session start (user sets acceptance criteria once: BELIEF threshold, source coverage requirements, XVERIFY coverage), (c) reduce TIER-2 checkpoints to 2-3 per review (post-R1 scope confirmation, post-exit-gate synthesis approval, final output review). TIER-A observables (gaming-resistant, orchestrator-produced) are already built in sigma-ui Phase A — convergence markers, XVERIFY coverage, source provenance, BELIEF divergence.

**A/B test: LLM-lead-driven (V1.5) vs. orchestrator-driven (V2) on same prompt.**
Same loan-admin prompt used for Phase 3 A/B. Metric: does orchestrator-driven review produce equivalent or better quality at equivalent or lower process violation rate? Pre-registered criteria. User evaluates synthesis outputs blind.

### Phase 5+: Full role decomposition (Option 3) — after Option 1 observables validated

Proceed only after: Option 1 is in production, TIER-A observables have been validated across N≥3 reviews as sufficient for autonomous gate advancement. Option 3 removes all LLM process authority. Agents are pure analytical workers. Python orchestrator validates every agent submission mechanically. Coordinator agent (LLM) summarizes and routes but cannot advance or gate. DA Function B (adversarial content) remains as agent role. Estimated 4-6 sessions. Not in V2 scope.

---

## Pre-mortem

**PM[1]: MCP registration breaks mid-migration.**
Probability: MEDIUM. Mitigation: test pip install + MCP in isolation before touching submodules. Keep old repos 2 weeks post-migration. Test `claude mcp list` + sigma-mem recall in fresh session before decommissioning. SQ[6] depends on SQ[5] MCP verification being confirmed first (CQA M4xM6 interaction).

**PM[2]: Structured-field format degrades DA challenge quality.**
Probability: MEDIUM (C1 self-reference — ΣComm simplification motivated in part by agent convenience). Mitigation: A/B test measures DA challenge evidence-rate; if drops >10% → partial ADR[2] reversion (restore ¬ notation; keep structured fields). ADR[2] conclusion may be correct but team arrived at it partially for the wrong reason (agent token savings rather than operator auditability). The correct reason (operator auditability) is load-bearing but was measured in the wrong dimension.

**PM[3]: Hook regex updates incomplete → process violations go undetected.**
Probability: HIGH if SQ[9] done after SQ[7/8]. Mitigation: SQ[9] must complete and be tested before SQ[7] goes live (hard sequencing dependency). Extend test_gate_checks.py to cover new format explicitly. Window between format change and regex update = enforcer fails open.

**PM[4]: H7 assumption baked into Phase 3 before A/B validates it.**
Probability: MEDIUM. Phase 3 (notation change) must be gated on A/B test establishing V1 baseline. Do not commit to Phase 3 SQ[7/8] until V1 baseline established. If V2 degrades on DA challenge evidence-rate or process compliance → targeted reversion, not full rollback.

**PM[5]: ADR[5] dead-workflow removal triggers enforcer inconsistency.**
Probability: MEDIUM if not atomic. Mitigation: orchestrator-config.py and BUILD_PHASE_MAP in enforcer change in one session. Verify with BUILD phase sequence after change. SQ[0] must precede (no modification to untested orchestrator code).

**PM[O1]: Convergence-theater failure (Option 1 / orchestrator-as-driver).**
Probability: MEDIUM. Agents learn what TIER-A observable patterns trigger orchestrator advancement (workspace ✓ + BELIEF[] + XVERIFY called). Produce process-compliant but analytically shallow findings that pass all mechanical checks. Mitigation: criterion pre-registration puts quality thresholds in user's hands, not system's. TIER-A observables measure proxies, not analytical substance. Monitor for review quality degradation in first 3 orchestrator-driven reviews. Fallback: human review of agent workspace sections at TIER-2 checkpoints.

**PM[O2]: Conversation-boundary skipping (Option 2).**
Probability: MEDIUM. C3 (tail phases) is still voluntary to open. Lead declares review complete at C2 synthesis and doesn't start C3. Mitigation: C2 must produce a hand-off artifact (sigma-mem project entry with explicit C3-PENDING flag) that sigma-mem integrity check detects. C3 opening is forced by build-review conversation reading IC[3] bridge state. Not fully enforced by conversation existence alone.

**PM[O3]: Contamination-at-source failure (Option 3 / full decomposition).**
Probability: MEDIUM-HIGH. Under full decomposition, the coordinator agent summarizes convergence and routes information but cannot exercise judgment. If the coordinator summarizes findings inaccurately or routes context incorrectly, the Python orchestrator acts on bad inputs — enforcing process over contaminated analytical content. This failure mode is harder to detect than V1's skip pattern (a skipped phase is visible in the audit log; a misleading summary is not). Mitigation: coordinator output must be written to workspace (auditable), not just communicated as a message. Comparison: V1 has a sycophantic lead that skips process but can recognize shallow analysis; Option 3 has a rigorous orchestrator that enforces process over potentially contaminated coordinator output. Trade-off is real; must be validated in production before full authority removal.

---

## Files

| File | Action | Description |
|------|--------|-------------|
| `~/.claude/agents/_template.md` | Modify | Remove Boot step 3 (markdown inbox), rewrite shared sections in structured plain English, extract _protocol.md |
| `~/.claude/agents/_protocol.md` | Create | Shared agent protocol (120 lines extracted from template) |
| `~/.claude/agents/*.md` (32 files) | Modify | Update to reference _protocol.md; remove ΣComm body notation; keep status codes |
| `~/Projects/sigma-system-overview/agent-infrastructure/hooks/phase-compliance-enforcer.py` | Modify | Regex pattern updates for structured-field format (SQ[9]); XVERIFY WARN→BLOCK (SQ[2]); verify TeamCreate coverage (SQ[1]); promote memory-sync NUDGE→BLOCK (ADR[3]) |
| `~/Projects/sigma-system-overview/agent-infrastructure/teams/sigma-review/shared/orchestrator-config.py` | Modify | Remove dead 13-phase BUILD workflow (SQ[4]/ADR[5]); add DA-PASS mechanical gate in advance() (ADR[8]) |
| `~/Projects/sigma-system-overview/agent-infrastructure/hooks/memory-sync-reminder.py` | Modify | NUDGE→BLOCK for GLOBAL_PATTERNS writes (ADR[3]) |
| `~/Projects/sigma-system-overview/setup.sh` | Modify | Rewrite for pip deps (SQ[5]/ADR[1]); remove submodule steps |
| `~/.claude/projects/-Users-bjgilbert/memory/MEMORY.md` | Modify | Stub-redirect to sigma-mem recall (SQ[6]) |
| `~/Projects/sigma-ui/` | Extend | Phase C: remove TIER-1 human-gate blocking, add criterion pre-registration, reduce to 2-3 TIER-2 checkpoints (Phase 4) |
| `~/.claude/skills/sigma-review/phases/` | Replace | 12 ANALYZE phase files → 3 conversation phase files (SQ[10]/Option 2) |

---

## Plan Challenge Summary

- DA challenges: 21 vectors (including 4 post-disclosure supplementary vectors + 1 post-IE-correction) | DA grade: A | DA exit-gate: CONDITIONAL-PASS → PASS (3 conditions satisfied)
- Circuit-breaker: fired by DA (DA[#8/13] — zero inter-agent disagreements detected), NOT fired by lead. Process failure logged: lead did not run circuit-breaker check after R1 unanimity.
- Concessions (plan-track): 8 | Defenses: 3 | Compromises: 2
- XVERIFY sessions: 2 (ADR[2] — 2 providers; DA value claim — 3 providers)

**Key corrections integrated:**
- SQ[1] scope correction (IE): never-advance loophole BLOCK already exists as Layer 1c (26.4.13). SQ[1] is verification of coverage gaps, not implementation from scratch.
- ADR[2] motivation restated (DA[#1]): operator auditability, not agent token savings. CQA measured agent overhead (147 lines/agent) but not operator audit time. 10/12 corrections are operator verification failures.
- DA value claim corrected (PS + XVERIFY): "100% challenge hit rate" was conditional (systematically-optimistic-R1 class) misrepresented as universal. Archive-validated rate: ~60-80%. PS error: used memory entry without verifying against archive evidence.
- Output relabeled (DA[#8/13]): "independently derived architecture" → "validated refinement of existing analysis with 5 enforcement/architectural additions not in original analysis." The 5 genuine additions: (1) never-advance loophole enforcement gap, (2) memory-sync-reminder unimplemented correction, (3) dead BUILD orchestrator workflow resolution, (4) XVERIFY WARN→BLOCK upgrade, (5) pip-dep vs. subpackage distinction.
- A/B prompt replaced (DA[#7]): circular self-evaluating prompt → loan-admin KB coverage gap analysis (operator has V1 ground truth from 26.3.13 review).
- SQ[1+2] reclassified as V1 hotfixes (DA[#16]): no V2 architecture dependency. Remove from V2 scope; implement now to close open exposure.
- IC[2] removed (DA[#15]): premature abstraction, no corresponding SQ, multi-model is roadmap not current requirement.

---

## Paradigm Shift Findings

The DA (DA[#4]) correctly identified the team answered "how to improve V1" not "what V2 looks like from scratch." The paradigm shift analysis is the genuinely greenfield output of the session.

**The lead problem framed precisely (CQA):**
The current architecture is NOT orchestrator-driven. It is: a CLI tool (orchestrator-config.py) that the LLM lead calls via Bash to advance phase state + a hook layer (phase-compliance-enforcer.py) that fires on tool calls and BLOCKs specific violations. The lead IS the driver. The orchestrator is a state machine the lead advances manually. Every V1 fix adds another hook to constrain the LLM lead, but the LLM lead is the outer loop — it runs the hooks, reads the results, and decides what to do.

**OPTION 1 — Orchestrator-as-driver (Python script drives, lead becomes one agent):**
The call direction inverts. Instead of Lead → `python3 orchestrator-config.py advance`, it becomes: Orchestrator → spawn_agent(prompt) → evaluate convergence → advance → spawn next. The LLM lead is demoted to analytical coordinator; cannot control phase advancement, gate evaluation, or agent dispatch timing.

sigma-ui is 70% complete (Phase B3: execution_loop.py bridge, 16 modules, 280 tests). sigma-ui was paused because it made the HUMAN the gate enforcer at every gate, not because orchestrator-as-driver is unworkable. The concept was right; the execution (human approves every gate) was wrong.

Design constraint: orchestrator runs autonomously against pre-registered acceptance criteria. User approves criteria ONCE at session start (BELIEF threshold, XVERIFY coverage, source provenance requirements). TIER-1 mechanical gates advance autonomously. TIER-2 analytical gates have 2-3 human checkpoints per review (post-R1 scope confirmation, post-exit-gate synthesis approval, final output review) — not one per phase.

Failure mode: convergence-theater (PM[O1]). Agents produce process-compliant but analytically shallow findings that satisfy all TIER-A mechanical checks. Current system has an unreliable lead but one that can recognize shallow analysis. Orchestrator-driven system has rigorous process but cannot evaluate analytical substance. Mitigation: criterion pre-registration + user review at TIER-2 checkpoints.

Incremental: YES. sigma-ui was designed as incremental evolution from V1. orchestrator-config.py imports as library (Phase A H1 CONFIRMED).

**OPTION 2 — Conversation-boundary enforcement for ANALYZE:**
ANALYZE adopts BUILD's 3-conversation model. Proposed split: C0 (preflight+spawn), C1 (research+circuit-breaker), C2 (challenge+debate+exit-gate), C3 (synthesis+compilation+promotion+sync+archive). The B7 tail-phase skip pattern (lead skips phases 06-10) is addressed by C3 — lead must enter a separate conversation to complete.

Failure mode: within-conversation skipping is unchanged. B7 never-advance loophole occurred WITHIN a phase (plan phase), not across phases. Conversation boundaries prevent cross-boundary skips; within-conversation violations remain LLM-discipline-dependent. C3 is still voluntary to open. Context loss at conversation boundaries: R2 adversarial agents must re-read R1 workspace rather than carry R1 context.

Incremental: YES — trivially. Replace 12 phase files with 3 conversation phase files (already the BUILD pattern). Most conservative structural change.

**OPTION 3 — Full role decomposition:**
Apply DA Function A/B decomposition to ALL roles. Python orchestrator owns ALL process. LLM agents own ALL content. No LLM has process authority over any other LLM. The coordinator agent summarizes and routes but cannot advance or gate.

User's concern correctly identified: distributed enforcement = no enforcement. Option 3's answer is concentration, not distribution — enforcement moves to a SINGLE Python orchestrator, not distributed across agents. Agents lose all process authority entirely.

Failure mode: contamination-at-source (PM[O3]) and the judgment gap. The Python orchestrator enforces process over coordinator output that may be inaccurate. Removing LLM oversight of analytical quality is harder to recover from than removing LLM oversight of process. The current system's LLM lead can recognize shallow analysis even when it skips process; Option 3 eliminates that recognition.

Incremental: NO in its full form. Requires Option 1 as stepping stone. Option 1 first (orchestrator-as-driver with LLM lead as advisor), then progressively strip lead authority as TIER-A observables are validated as robust.

**Team consensus on progression:**
- V1.5 (current plan, Phases 1-3): enforcement fixes + simplification + A/B baseline. Correct and should ship.
- V2 (Phase 4): Option 1 orchestrator-as-driver with criterion pre-registration + tiered autonomy + Option 2 conversation-boundary ANALYZE in parallel as conservative test.
- V3 (Phase 5+): Option 3 full decomposition, after Option 1 TIER-A observables validated across N≥3 production reviews.

**ADR[8] connection:** DA Function A → orchestrator mechanical advance() check is the first V1/V2 step toward Option 1. Machine-readable DA exit-gate (ADR[2] structured format) is the prerequisite. ADR[2] → ADR[8] → Option 1 is the dependency chain.

---

## Process Observations

- **Zero-dissent circuit-breaker not fired by lead.** R1 produced unanimous convergence from 4 Claude agents. The lead did not run the circuit-breaker check. DA issued DA[#8/13] forcing the herding acknowledgment. This is a documented process failure — logged, not remediated in this session. CB enforcement is currently a hook check in the gate bundle, not a hard BLOCK. If CB should always fire on R1 unanimity, it needs a PreToolUse BLOCK not just a bundle check.

- **Lead steered DA challenge vectors.** The lead authored the 6 initial DA challenge vectors. This was disclosed mid-session. DA issued supplementary vectors (DA[#17-20]) targeting blind spots the lead's vectors missed — specifically the "keep" list was unchallengeable under the original vectors. Disclosure was the right process action; structural contamination remained.

- **SQ[1] herding: all agents read the feedback file, none checked current code.** All agents (TA, PS, CQA, IE) identified the never-advance loophole as the highest-priority gap based on feedback_never-advance-loophole.md. None checked phase-compliance-enforcer.py to see if it was already fixed. IE's r2 correction found Layer 1c (26.4.13) had already implemented the SendMessage BLOCK. "Independent discovery" of a documented gap via parallel reading of the same file is not independent analysis. File recall was labeled as convergence; convergence added no weight above the single correction file.

- **DA meta-observation (DA[#8/13]):** Single-model multi-agent analysis produces structural perspectives (different expertise domains) but not cognitive independence. Four Claude Opus 4.6 agents with the same training data, the same correction files, and the same analysis frame will converge on the same conclusions. Convergence among structurally identical agents is the definition of herding risk, not evidence of independent validation. XVERIFY (genuinely different model architectures) was the only external signal in this session. It produced two genuine revisions (ADR[2] status codes, DA value claim decomposition).

- **C1 self-reference operative throughout.** Agents assessing their own infrastructure have structural incentive to undervalue ΣComm complexity (conditioning vs. genuine clarity), overstate enforcement complexity as load-bearing, and recommend simplifications they find operationally convenient. DA[#1] identified the wrong bottleneck in ADR[2] (agent token savings vs. operator auditability). PS DA[#17] correction: Q/H/C prompt decomposition was rated Value=HIGH in r1; archive evidence showed the mechanism (prevent hypothesis confirmation) is not demonstrated. Downgraded to MEDIUM. Root cause: internal memory relied on without verification against archive evidence.

---

## A/B Comparison Methodology

**ANALYZE test:** Loan-admin KB coverage gap evaluation (existing review 26.3.13, operator has V1 ground truth). Task: "Evaluate loan-admin KB documentation coverage: identify gaps against LSTA-standard administrative requirements, prioritize by operational risk, and recommend remediation sequence." Rationale: (1) operator can evaluate output quality independently without process metadata; (2) not circular — neither system evaluates its own architecture; (3) TIER-2 complexity appropriate for comparison.

**BUILD test:** SQ[3] (drop markdown inbox boot step). Concrete implementation task. Metric is process compliance, not domain accuracy.

**Methodology:**
- N=3 paired comparisons per variant (not N=3 independent samples — paired controls between-session variance)
- Per-gate pass/fail measurement: 28 gate functions × N=3 sessions = ~84 binary gate observations per variant (CQA finding — gate-level signal, not session-level aggregate)
- User as blind evaluator of synthesis output quality (lead does NOT interpret comparison — raw outputs to user)
- Pre-registered pass threshold before running: V2 passes if (a) user cannot identify quality degradation in paired comparison AND (b) process compliance metrics equivalent or better
- N=3 is not a statistical equivalence proof — it is a regression detector for obvious degradation

**Sequencing:** V1 baseline runs FIRST (before Phase 3 commits). Phase 3 does not proceed until baseline established. If DA challenge evidence-rate specifically degrades in V2 → ADR[2] partial reversion (restore ¬ field; keep rest plain English).

**Phase 4 A/B extension:** Same loan-admin prompt, compare LLM-lead-driven (V1.5, post-Phase-1-3) vs. orchestrator-driven (V2, sigma-ui Phase C complete). This tests the architectural question (who should drive?) rather than only the notation question.

---

## Build Status
{empty — written by C2}

---

## Build Review Summary
{empty — written by C3}

---

## Close Status
{empty — written by C3}

---

## Verification (C2 boot)

Before implementing any SQ in C2:

- **CONDITION 5 (code-state verification):** Verify each SQ against current codebase state before implementing. SQ[1] example: IE found Layer 1c already exists (26.4.13). All SQs should be checked for current implementation status before treating as "implement from scratch."
- SQ[1]: grep phase-compliance-enforcer.py for TeamCreate agent-spawning coverage (verify gap, do not assume)
- SQ[2]: grep phase-compliance-enforcer.py:792-796 for XVERIFY-unused exit code (verify still WARN, not already BLOCK)
- SQ[3]: check _template.md Boot step 3 existence (verify still present)
- SQ[0]: verify no test_orchestrator_config.py exists yet
- SQ[4]: verify dead BUILD phases still in orchestrator-config.py

**Mechanical gate constraints:**
- SQ[9] MUST complete and pass tests BEFORE SQ[7] or SQ[8] go live
- V1 A/B baseline MUST be established BEFORE Phase 3 commits (SQ[7/8] + SQ[10])
- SQ[0] MUST complete BEFORE SQ[4] modifies orchestrator-config.py
- SQ[5] MCP verification MUST be confirmed BEFORE SQ[6] stub is written
- PyPI publish for sigma-mem (from SQ[4] pre-work) MUST precede SQ[5] submodule removal

**Open questions carried forward (not blocking, but unresolved):**
- Should workspace within-session state be tested against sigma-mem within-session project scope as an alternative? (DA[#17] finding — workspace uniqueness claim untested)
- Should ANALYZE adopt a simplified 3-phase model (matching BUILD's conversation structure)? (DA[#18] finding — phase-file model optimality untested; SQ[10] is the experiment)
- Should one A/B variant test automated exit-gate checks (checklist gate) vs. DA agent to isolate DA's marginal contribution? (DA[#19] XVERIFY finding — mechanical gate is separable from adversarial persona)
- Is N=3 even adequate as a regression detector once per-gate measurement is instrumented? Review after Phase 3 baseline data is available.
