---
name: Sigma-Review Infrastructure Issues (R19 post-mortem)
description: 18 infrastructure issues surfaced during R19 (AI agent rollout playbook vet, 2026-04-22) — prioritized list with fixes, for planning a remediation session
type: project
originSessionId: 07852628-a0da-4183-81e6-9f2c8cb8bfef
---
# Sigma-Review Infrastructure Issues — R19 Session Post-Mortem

**Source:** R19 sigma-review session 2026-04-22 (AI agent rollout playbook vet). Issues surfaced organically during execution — some caused data loss, others required manual lead workarounds. Commit 7ecc72e + 2d8c9a3 documents the session.

**Session outcome:** audit GREEN (process sound); evaluation B / 3.14 (output quality strong-not-exceptional). Forecast accuracy: GREEN prediction correct (70-75%); A prediction wrong (landed B, predicted 75-80% A — overconfident on frame-anchoring + false-precision issues). Recovery was transparent, DA caught anti-sycophancy failures including lead grep-error, severity graduation resolved debates. Scope Integrity scored 4/4 (perfect) — recovery transparency validated. Six other criteria scored 3/4 consistently.

**Why:** We need to remediate these before the next major sigma-review or the same problems will recur. Most are chain-evaluator or spawn-template fixes; two are deeper MCP infrastructure issues. Process integrity requires fixing the mechanical enforcement, not adding to agent instructions.

**How to apply:** When starting a remediation session, spawn a sigma-build (or single-instance if scoped down) with this list. Priority order: fix CRITICAL first (ΣVerify agent-context, sed -i ban, A12 parser bug), then HIGH, then bundle MEDIUM + LOW.

---

## CRITICAL (caused data loss or prevented chain completion)

### 1. macOS BSD `sed -i` footgun
- **What happened:** CDS-2 invoked `sed -i` without backup-extension argument. macOS BSD sed requires `sed -i ''` or `sed -i.bak` — absent that, the command silently truncated workspace.md to 0 bytes.
- **Impact:** Lost 4 agent findings sections + all `##` scaffolding mid-R1. Recovery required ~30 min of re-paste coordination.
- **Fix:** Add hard rule to every agent spawn prompt template + agent definition: "NEVER use `sed -i`, `awk -i`, or raw Bash redirects for workspace edits — Edit tool only." Also add to `~/.claude/teams/sigma-review/shared/directives.md` as a non-negotiable rule.
- **Status:** Not remediated. Current spawn prompts don't explicitly ban sed -i.

### 2. Concurrent-write race on workspace.md
- **What happened:** Multiple agents writing simultaneously caused "file modified since read" errors on Edit tool and silent clobbers on Bash append.
- **Impact:** TIA was blocked on re-paste, required lead to coordinate a 2-minute write-window freeze. RCA hit Edit collisions during promotion and fell back to Bash heredoc appends.
- **Fix options:** (a) File-lock protocol on workspace writes (advisory, agents honor), (b) restrict agents to Edit tool only (read-before-write protection handles single-writer but not multi-writer races), (c) implement write-window arbitration in team infrastructure, (d) queue workspace writes through a lead-proxy.
- **Status:** Not remediated.

### 3. ΣVerify sub-tools not deferred-loadable in spawned agent contexts
- **What happened:** Agents calling `ToolSearch("select:mcp__sigma-verify__verify_finding")` from spawned Agent subprocess contexts returned "No matching deferred tools found." Only `init` and `check_quotas` registered. 5 agents independently reported XVERIFY-FAIL.
- **Impact:** Agent §2h verification was systematically broken. Compensated in-session by DA doing XVERIFY from DA's own context (which DOES have access), covering 3 load-bearing findings across 3 architecturally distinct providers. Without DA XVERIFY, severity-graduation debate couldn't have resolved.
- **Fix:** Deferred-tool registry needs to inherit to spawned Agent subprocess contexts. Or sigma-verify sub-tools should be pre-loaded in agent spawns. Or sigma-verify MCP should register all tools at init, not defer them.
- **Status:** Not remediated. Systematic gap documented in workspace `## infrastructure`.

---

## HIGH (required manual workarounds, risk of audit YELLOW)

### 4. Chain-evaluator A12 parser bug (one-line fix)
- **What:** `check_a12` in `~/.claude/hooks/chain-evaluator.py:241` reads `details['archive_exists']` but `gate_checks.check_session_end` returns `details['archive_file_found']`. Key-name mismatch → A12 never passes regardless of actual archive state.
- **Impact:** Blocks git commit via phase-gate hook's chain-complete check. Required manual_override in `.chain-status.json`.
- **Fix:** One-line change in `chain-evaluator.py` line 241: `archive_exists` → `archive_file_found`. Or in `gate_checks.py` line 1517: rename returned key to `archive_exists`.
- **Status:** Worked around with manual_override. Not fixed.

### 5. Chain-evaluator peer-verification regex rigidity
- **What:** `_PEER_VERIFY_HEADER` regex in `chain-evaluator.py:278` requires `### Peer Verification: X verifying Y` (3 hashes + literal "verifying" keyword). Our spawn prompt told agents to use `#### Peer Verification: Y` (4 hashes, target-only).
- **Impact:** All 7 first-pass peer-verifications didn't match. Lead had to add a `## peer-verification-index` section with reformatted headers pointing to the agents' actual analytical work.
- **Fix options:** (a) Update sigma-lead spawn prompt template to use canonical 3-hash "verifying" format, (b) make chain-evaluator regex accept both formats, (c) both.
- **Status:** Worked around with lead-authored index. Not fixed at source.

### 6. DA triggers full agent-requirements in chain-evaluator
- **What:** Adding `### devils-advocate` stub to findings region (needed for A5/A18 detection) caused chain-evaluator to treat DA as an 8th agent requiring DB[] (A3), own peer-verification section (A16), and 2+ verifiers (A18). DA's role is adversarial layer, not domain agent.
- **Impact:** Required lead to add DB[] in DA section + 7 DA-verifying-each-agent subsections + lead-verifying-DA entry. ~200 lines of scaffolding to satisfy format.
- **Fix:** Chain-evaluator should recognize DA as role-exempt from some agent requirements. Or DA work should live entirely outside findings region with specific DA-section checks.
- **Status:** Worked around with scaffolding. Not fixed.

### 7. Sigma-mem `store_agent_memory` write contention
- **What:** RA's UP[RA-B] and UP[RA-C] hit "persistent internal errors" on store_agent_memory global. RCA hit same issue on first 3 attempts, fell back to `store_memory` → patterns.md.
- **Impact:** 2 of 24 user-approved findings couldn't persist globally. Content preserved in workspace archive for future session recovery.
- **Fix:** Add retry/backoff to sigma-mem writes. Or enforce `store_memory` → patterns.md fallback consistently in agent promotion protocol. Or add transactional semantics.
- **Status:** Not remediated. 2 items pending: RA UP[RA-B] (SOC 2 TSC→AI mapping), RA UP[RA-C] (GDPR Art 22 design fork).

### 8. Phase-gate pre-shutdown hook requires literal `##` section names
- **What:** Hook at `~/.claude/hooks/phase-gate.py:208-214` checks for `## contamination-check` and `## sycophancy-check` as top-level `##` headers. Lead wrote content inline in `## pre-synthesis-checks` with `CONTAMINATION-CHECK:` / `SYCOPHANCY-CHECK:` markers.
- **Impact:** Hook blocked all 8 shutdown_requests. Required adding explicit `##` headers pointing to inline content.
- **Fix:** Either hook accepts inline markers, OR sigma-lead directives + spawn prompts require exact `##` header format, OR hook scans for `CONTAMINATION-CHECK:` / `SYCOPHANCY-CHECK:` content regardless of header level.
- **Status:** Worked around with explicit headers. Not fixed at source.

### 9. Multi-agent spawn produces silent collision suffixes
- **What:** TeamCreate appends `-2` (and `-3`, etc.) when spawn-name collides with existing team config members. Lead isn't warned. Ring assignments and roster-based chain-evaluator parsing assume base names.
- **Impact:** Required 3 post-spawn correction SendMessages + workspace ring rewrite + section-header renames. Also created CDS-2's stale-context peer-verify of TA-2 (wrong because TA-2 hadn't been restored yet).
- **Fix options:** (a) Auto-purge dormant team members from config.json on TeamCreate, (b) warn lead on name collision at spawn, (c) chain-evaluator roster-matcher handles `-\d+` suffix, (d) all three.
- **Status:** Not remediated.

---

## MEDIUM (friction, not blocking)

### 10. Roster-based agent extractor fails on suffixed names
- Related to #9. `extract_agents_from_workspace` uses roster base names; spawn produces suffixed instances. Required `### tech-architect-2` → `### tech-architect` section-header rename. Fix: strip `-\d+` suffix when matching against roster in `gate_checks.py:229`.

### 11. Chain-evaluator DB[] step-count check too aggressive
- Counts ANY `DB[...]` pattern and flags "missing X of 5 steps" on references that aren't bootstrapping exercises. TA had 6 flagged as shallow; RCA and RA had 3 each. Most were legitimate inline references. Fix: tighten detection to require at least 2-3 of the 5 markers ("initial", "assume.wrong", "counter", "re.estimate", "reconcile") present before qualifying as a DB[] entry.

### 12. `## findings` region too large for primary-finding detection
- Chain-evaluator treats everything between `## findings` and `## convergence` as findings content. Our workspace included r1-convergence, BELIEF, peer-verification-index, r2-da-challenges all in that range. F[TA-A5] reference inside DA challenge triggered A2 untagged-finding flag. Fix: scope findings region more narrowly, OR require primary finding declarations to use specific markers that distinguish from references.

### 13. Lead-side line-range grep overlap
- My `sed -n '123,500p' | grep -c` spans multiple agent sections, not just one. DA caught the error when I claimed "TA responded with 5 concede/defend/compromise" (actually zero). Fix: provide a lead-helper tool or Bash pattern for "section-scoped content check" using agent-section boundaries.

### 14. Peer-verification spawn-prompt template wrong format
- Related to #5. My spawn-prompt template told agents to use `#### Peer Verification: Y` — chain-evaluator expects `### Peer Verification: X verifying Y`. Fix: update sigma-lead spawn prompts in templates.

### 15. Promotion workflow inconsistent across agents
- Agents used different approaches: some called `store_agent_memory tier:global`, some fell back to `store_memory` → patterns.md, some only wrote to workspace. 2 items couldn't persist at all. Fix: standardize promotion flow with explicit fallback chain in agent definition `## Promotion` section: primary store_agent_memory → fallback store_memory patterns.md → last-resort workspace-only with retention note.

---

## LOW (edge cases)

### 16. Sigma-mem MCP disconnects mid-session
- Late in session, MCP tool list refresh showed sigma-mem tools disconnected (get_agent_memory, get_decisions, get_project, etc.). Agents relied on these for promotion checks. Fix: MCP health monitoring + auto-reconnect, or agent graceful-degrade when MCP unavailable.

### 17. Phase-gate git commit A14 circular dependency (masked by #4)
- Hook blocks git commit until chain complete; A14 is "git clean" — only satisfied BY the commit. Hook has A14-only-failure exception, but A12 parser bug (#4) left A12 also listed, so exception didn't apply. Fixing #4 resolves this automatically.

### 18. No mid-session chain health dashboard
- Issues compound invisibly until audit runs at end. Would help to have a mid-session "chain health" dashboard showing progress against A1-A19 criteria. Lead currently has to run `python3 ~/.claude/hooks/chain-evaluator.py status` manually.

---

## Systematic patterns worth naming

**Pattern 1: Chain-evaluator format contract is strict but not enforced at spawn.** Every format mismatch (roster names, header formats, section names, DB structure, peer-verify format) became a lead-workaround. The contract should be surfaced in spawn prompts so agents produce compliant output on first write. Candidate: add a "chain-evaluator compliance checklist" to sigma-lead spawn template.

**Pattern 2: Write contention is the dominant mid-session failure mode.** `sed -i` truncation, concurrent Edit races, sigma-mem write errors. Tightening to Edit-tool-only + proper MCP retry handles most. Candidate: hard-block `sed -i` / `awk -i` / Bash-redirect writes to workspace.md via phase-gate PreToolUse.

**Pattern 3: Agent-context infrastructure is discoverably thin.** Tools, suffixes, section names, ΣVerify availability aren't surfaced to spawning lead. Observability into what agents CAN and CAN'T do would prevent XVERIFY systematic failure from being a surprise. Candidate: lead pre-flight check that actually spawns a test agent and reports its tool inventory.

---

## Issues added from audit (R19 audit, 2026-04-22)

### 19. Chain-evaluator A3 DB-step parser false negatives
- **What:** A3 check counts DB[] entries with "missing X of 5 steps" flags. Auditor verified 5 sections (TA L144-156, RLS L435-447, RA L645-661, RCA L1056-1077, DA L1616) — all 5/5 steps present. Parser false-negative, not agent violation.
- **Impact:** 14 DB entries flagged as shallow during review; would have caused YELLOW audit if auditor hadn't caught the bug.
- **Fix:** Loosen DB step-marker detection pattern, or inspect a representative sample and calibrate marker tolerance.
- **Status:** Not remediated.

### 20. A12 workspace-archive gate timing window
- **What:** Different angle than #4 (key-mismatch). Chain-evaluator ran BEFORE archive completed writing. Auditor recommends: "archived within 24h of exit-gate PASS" tolerance in gate logic.
- **Impact:** Chain-evaluator A12/A14 FAILs stale at session end; required manual override.
- **Fix:** Either (a) phase-gate waits on archive-complete signal, (b) A12 check re-runs after synthesis archive write, or (c) 24h grace window per auditor suggestion.
- **Status:** Not remediated (workaround via manual_override).

## Patterns worth formalizing as directive updates

### Pattern A: Corruption-recovery template (§8e candidate)
Auditor flagged R19's recovery-log as "exemplary" and worth formalizing. The template:
1. Backup corrupted state immediately (preserve artifact with explicit name)
2. Extract preserved sections via read-only means (sed without -i, cat, awk without -i)
3. Rebuild scaffolding from lead conversation context (admin work, not analytical)
4. Coordinate re-paste with strict Edit-tool-only rule + write-window freeze if needed
5. Each restored section carries provenance-attestation line (verbatim-from-pre-corruption)
6. Document what was lost, what preserved, what re-pasted in `## recovery-log`
7. Never silently restore — transparency is the audit requirement

### Pattern B: DA[#N] not-discussed probe
Auditor noted DA[#6] produced 2 entirely new findings (F[CDS-C1] firm-size floor + F[CDS-C2] adoption-oversight-overhead) from a single challenge. The pattern: "what is the team systematically NOT discussing?" is high-yield, worth adding to DA challenge framework standards (already #7 in framework but underweighted in practice).

### Pattern C: DA XVERIFY as severity calibrator
Already promoted. DA-context XVERIFY from 3 architecturally distinct providers compensates when agent-context XVERIFY is unavailable. Caught 5 HIGH → graduated severity + 2 withdrawn quantifications.

## Evaluator-recommended improvements (from evaluation B feedback)

### 21. Premise-audit step pre-dispatch (NEW)
- **What:** H1-H12 tested rigorously but premises under them (tier-structure necessity, firm-size floor, data-readiness baseline, adoption likelihood) accepted as frame. DA did the job that initial framing should have done.
- **Impact:** "Most structurally significant weakness" per evaluator. Frame-anchoring limits even tight reasoning.
- **Fix:** Add premise-audit step to sigma-lead workflow BEFORE H-level agent spawning. Test tier-structure necessity, firm-size applicability, data-readiness baseline, adoption likelihood as distinct from the H-hypotheses the agents receive.
- **Status:** Not in protocol. NEW directive candidate.

### 22. Pre-publication precision gate (NEW)
- **What:** False precision on quantified claims — F[TA-C2] FTE range 0.55-1.1 withdrawn under DA pressure; F[TA-A2] $200K-$2M with no driver breakdown; H2 10-13mo with no CI; pre-mortem probabilities (35/20/25%) without Bayesian structure. Quantification preceded justification.
- **Impact:** Calibration 3/4 instead of 4/4. Accuracy 3/4 instead of 4/4. Compounding quality loss across 2 criteria.
- **Fix:** Any quantified claim above specificity threshold must carry driver breakdown OR confidence interval with reference class, else state qualitatively. Add to chain-evaluator as §2i precision gate (or analytical-hygiene §2f).
- **Status:** NEW directive candidate.

### 23. HIGH-severity governance findings need minimum artifact (NEW)
- **What:** F[CDS-A1] and F[CDS-B1] HIGH severity but recommendations stopped at gap-ID without templates, specimen exam-crosswalks, or decision trees.
- **Impact:** Actionability 3/4 instead of 4/4. Governance findings are actionable in principle but not in practice.
- **Fix:** HIGH-severity governance/compliance findings require minimum artifact — template stub, decision tree, or specimen of recommended gate artifact.
- **Status:** NEW directive candidate.

### 24. Source-tag severity ratings not just claims
- **What:** SR 11-7 → AI-agent severity extrapolations (e.g., F[RL-F1]) should carry their own agent-inference tag at the severity level, not just at the claim level.
- **Impact:** Evidence + Calibration cross-evaluator disagreement flagged this.
- **Fix:** Extend §2d source provenance to severity ratings. When severity is extrapolated (e.g., "SR 11-7 exam-findings rate → AI-agent exam-findings severity HIGH"), the extrapolation itself carries agent-inference tag with assumption stated explicitly.
- **Status:** NEW §2d extension candidate.

### 25. MITRE ATLAS citation fix (R19-specific artifact)
- **What:** `AML.T0051.002` cited in TA's DA[#4] response doesn't exist in published MITRE ATLAS taxonomy.
- **Impact:** Substance (chain-of-agent prompt injection as production technique category) accurate; citation detail wrong.
- **Fix:** Edit archived workspace + synthesis to correct citation before sharing with firms.
- **Status:** Not fixed. One-off artifact cleanup.

## Top-5 ROI priorities for remediation session

**Infrastructure-layer (lift: fix once, benefits every future review):**

1. **#3 ΣVerify agent-context gap** — systematically broken verification across 5 agents. Breaks §2h. High-impact infrastructure fix.
2. **#1 sed -i ban** — one-line update to spawn templates + directives. Prevents recurrence of the corruption event.
3. **#4 A12 parser bug + #20 A12 timing window** — key-mismatch fix + 24h tolerance on archive-complete. Unblocks GREEN audit cleanly.
4. **#19 A3 DB-step parser** — loosen marker detection; would have caused YELLOW audit this session.
5. **#5 + #14 peer-verify regex + spawn template alignment** — canonical format alignment. Prevents ~30 min of lead-reformatting per review.

**Protocol-layer (lift: improve output quality toward A, not just GREEN):**

6. **#21 Premise-audit step pre-dispatch** (NEW from evaluator) — biggest structural weakness. Add premise-testing layer before H-level agent spawning.
7. **#22 Pre-publication precision gate** (NEW from evaluator) — driver breakdown OR CI on quantified claims, else qualitative. Fixes Calibration + Accuracy scores together.
8. **#23 HIGH-severity governance minimum artifact** (NEW from evaluator) — template/decision-tree/specimen required. Fixes Actionability score.
9. **#24 Source-tag severity ratings** (NEW from evaluator) — extend §2d to severity extrapolations.

**Artifact cleanup:**
10. **#25 MITRE ATLAS citation fix** (R19-specific) — edit archive + synthesis before sharing with firms.

Remaining issues (#2, #6, #7, #8, #10-18) bundled into follow-up passes: chain-evaluator hardening (#6, #10, #11, #12, #17), spawn/hook hardening (#2, #8, #13, #15, #16, #18).

## Validated patterns worth formalizing (from audit)

- **§8e recovery template** — corruption-event handling per Pattern A above. Auditor flagged R19 recovery as exemplary.
- **DA not-discussed probe (challenge framework #7)** — DA[#6] produced 2 new findings from single challenge. Underweighted in practice, strengthen directive.
- **DA XVERIFY as severity calibrator** — already promoted globally. Document as canonical severity-calibration pattern when agent-context XVERIFY unavailable.

## Agent calibration notes (from audit)

- **reference-class-analyst-2**: consistent outcome-1 discipline, withdrew 2 quantifications under warrant audit. Model calibration behavior.
- **regulatory-licensing-specialist**: borderline methodology flag on F[RL-F1] DB step-5 — watch for confirmation-bias-on-own-domain in future regulatory reviews.
- **devils-advocate**: exemplary role-boundary discipline — caught lead grep-error and forced correction. Anti-sycophancy working bidirectionally.

---

## Pending artifacts from R19 (recoverable in future session)

- **RA UP[RA-B]** SOC 2 TSC→AI control draft mapping — workspace archive `2026-04-22-ai-agent-rollout-playbook-vet.md` `## promotion → ### regulatory-analyst` section. Needs manual promotion to global sigma-mem.
- **RA UP[RA-C]** GDPR Art 22 B2B SaaS design fork — same location. Needs manual promotion.

## Session reference

- Commit: 7ecc72e (primary) + 2d8c9a3 (follow-up) on main in sigma-system-overview
- Archive: `~/.claude/teams/sigma-review/shared/archive/2026-04-22-ai-agent-rollout-playbook-vet.md` (2143 lines)
- Synthesis: `~/.claude/teams/sigma-review/shared/archive/2026-04-22-ai-agent-rollout-playbook-vet-synthesis.md` (417 lines)
- INDEX.md row: 2026-04-22 | ai-agent-rollout-playbook-vet | ANALYZE | 2 | TA,SS,RLS,RA,RCA,TIA,CDS,DA | PASS (A-avg engagement, corruption-recovered-transparently, severity-graduated via 3-provider XVERIFY)
- Portfolio entry: written to `~/.claude/teams/sigma-review/shared/portfolio.md`
