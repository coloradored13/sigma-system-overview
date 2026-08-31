---
name: Multi-model chatroom + Ollama MCP Bridge
description: Project 1 (MCP bridge) B6 audit remediation COMPLETE 26.4.9 (bare filename fix, dormant fields, BLOCKED_PROFILE, fsync, 816 tests, DA A-). F1 26.4.8. Q2 ΣComm translator DESIGNED-DEFERRED. Project 2 (chatroom) NOT STARTED. Repo: ~/Projects/ollama-mcp-bridge/
type: project
originSessionId: 16006b1e-ec26-46ce-a4cc-f73dac267174
---
## Project 1: ollama-mcp-bridge (F1 COMPLETE 26.4.8)
repo: ~/Projects/ollama-mcp-bridge/ | GitHub: coloradored13/ollama-mcp-bridge (public, Apache 2.0)
14 modules, 810 unit+adversarial tests (pipeline). v1.0.0 released 26.4.7, F1 upgrade 26.4.8.
**Why:** security-first bridge giving local Ollama models MCP tool access. No existing bridge has any security.
**How to apply:** foundation for chatroom (Project 2) and cross-model sigma-review (Project 3)

### B6 Audit Remediation (26.4.9) — sigma-build TIER-2, 5+DA, rubric A- (3.75/4.0)
External audit verified 8 findings, all accurate. 6 remediated:
P0: Bare filename SafePath bypass — field-name gate in _extract_paths_from_args()
P1: 5 dormant policy fields → ConfigError on non-default (NOT_YET_ENFORCED pattern)
P1: ToolState.BLOCKED_PROFILE separates profile blocks from sanitization blocks
P2: require_secret_scoping in HIGH_CONSEQUENCE + HARDENED warning
P2: DERIVED_EMAIL_DOMAIN in destination_influenced (telemetry-only)
P2: Unconditional os.fsync() in AuditLogger.flush()
816 tests, 0 regressions. BELIEF P=0.90. DA PASS B+.
Known warts: ScanResult.blocked_profile dropped (DA compromise), list-item bare filenames, non-listed field names.
Synthesis: ~/.claude/teams/sigma-review/shared/archive/26.4.9-audit-remediation-synthesis.md
Workspace: ~/.claude/teams/sigma-review/shared/archive/26.4.9-audit-remediation-workspace.md

### F1 Upgrade (26.4.8) — sigma-build TIER-2, 5 agents, DA A- (3.6/4.0)
5 gaps closed: trace_id+bridge_version provenance (Q1), ToolSignalCode enum (Q3), IP bypass hardening 6 vectors (Q4), HARDENED profile fail-loud (Q5), CapabilitySource-aware typed dispatch (Q6).
Q2 (ΣComm translator) DESIGNED but DEFERRED — DA[1] challenged unvalidated premise. Empirical test needed: send expanded ΣComm prompt to llama3.1:8b, check tool coherence. ADR[2] locked in archive.
Synthesis: ~/.claude/teams/sigma-review/shared/archive/26.4.8-ollama-mcp-bridge-f1-synthesis.md
Workspace: ~/.claude/teams/sigma-review/shared/archive/26.4.8-ollama-mcp-bridge-f1-workspace.md
Audit: YELLOW → remediated (BELIEF tracking, build-track source tags, contamination check, XVERIFY skip). 5 green-path tweaks applied to phase files.

sigma-build: TIER-2, 5 agents (all opus), 2-phase plan+build
synthesis: ~/.claude/teams/sigma-review/shared/archive/26.4.5-ollama-mcp-bridge-synthesis.md
workspace: ~/.claude/teams/sigma-review/shared/archive/26.4.5-ollama-mcp-bridge.md

### Patches applied (26.4.6, 6 PRs merged #1,#7-#11)
1. Tool-result contract: message now includes tool name for Ollama correlation
2. True streaming: asyncio.Queue replaces list-buffering replay
3. Audit secret redaction: structural summary replaces raw params_summary
4. Audit trail retention: _session_entries survives flush()
5. Validation hardening: recursive nested param checks + model_validator for config
6. Security cleanup: ActionGate encapsulation, top-level imports, honest first-run docs, pyproject.toml fix

### Security Redesign COMPLETE (9 PRs, 4 milestones, 26.4.5-26.4.7)
Specs: ~/Downloads/ollama_mcp_bridge_security_redesign_spec.md + ~/Downloads/ollama_mcp_bridge_sequenced_implementation_plan.md
Session handoff plans: ~/.claude/plans/crispy-stirring-fountain.md (PRs 3-9 detailed)
All 10 acceptance criteria from spec §17 met. v1.0.0 released. Code review addressed 26.4.7: UTF-8 truncation bug, atomic registry save, dead validator, READ classification, validated_params rename, nesting depth alignment, ANNOTATED tier implemented, rotation_days removed, hardening checklist added.

**PR 1 DONE** (75c16be): Fail-closed allowlist — empty allowed_tools blocks all tools. Discovery tracking added.
**PR 2 DONE** (300060f): First-run approval state machine — 7 states, ScanResult, ApprovalCallback (batch), PendingToolApproval, injectable registry, NoApprovedToolsError. require_first_run_approval=True default.
**PR 3 DONE** (635f3ab on pr3-registry-redesign): Registry redesign — RegistryEntry structured records, ApprovalMode enum, deny tracking, legacy migration, is_known() deny-bypass fix. 194 tests.
**PR 4 DONE** (dfe8109 on pr3-registry-redesign): Discovery/approval APIs — 4 Bridge methods + 2 SecurityGateway methods. Bidirectional state machine: approve PENDING+BLOCKED_INTEGRITY, deny/revoke PENDING+APPROVED. REAPPROVED mode now has production caller. 209 tests.
**PR 5 DONE** (245db40 on pr3-registry-redesign): Audit fidelity — ConfirmationOutcome enum (CONFIRMED/DENIED/TIMEOUT/NO_CALLBACK), enriched approval events (approval_mode, definition_hash, confirmation_outcome), TOOL_TIMEOUT + TOOL_REAPPROVAL_REQUIRED events, forensic cleanup (revocation+confirmation hash, dedup guard). 220 tests. **Milestone A (Trust Boundary) COMPLETE.**
**PR 6 DONE** (9c00771, merged bc2ef51): Semantic defense foundation — SourceType (9 origins), TrustLevel (4 tiers), ContentProvenance, SemanticRiskAssessment (9 attack flags), SemanticRiskAssessor (reuses 7 detectors + 3 new patterns, provenance amplification), ResultSanitizer.sanitize_and_assess(), execute_tool carries provenance+assessment in ExecutionResult, connect_and_scan assesses tool defs. Tightened 22 bare test schemas. 264 tests.
**PR 7 DONE** (f50ea2d, merged 9e48110): Taint tracking + sink policy engine. TaintTracker extracts URLs/domains/emails/IPs from tool results, matches against subsequent tool call args. SinkPolicyEngine classifies sinks (outbound/destructive/memory/general/read) and enforces policy. 5 SecurityConfig fields. New pipeline step. 333 tests. **Milestone B (Semantic Defense) COMPLETE.**
**PR 8 DONE** (816530e, merged e8518b5): Capability narrowing — 4 safe adapters (SafeURL, SafePath, SafeRecipient, SafeMemoryWriteCandidate). Opt-in via config, proactive validation regardless of taint. 377 tests. **Milestone C (Capability Hardening) COMPLETE.**
**PR 9 DONE** (80c2ac0, merged fb63d8a, extended through 3151982): Live E2E tests + adversarial eval harness. test_mcp_server.py (echo/add/get_secret/flaky_tool/slow_tool), adversarial_mcp_server.py (5 attack payloads). Split into 3 tiers: test_live_mcp.py (6, ~4s), test_live_model.py (7, ~4min), test_live_multistep.py (10, ~7min) + test_adversarial.py (8 pipeline + 2 model). live_bridge fixture with subprocess cleanup. Truncation guards on all 19 model tests (caught 1 silent pass). Report generator: run_e2e_report.py (--tier, --fast, --merge). 297/297 report committed. **SQ[0] CLOSED. SQ[11] CLOSED.**

### Key design decisions (26.4.6 session)
- Hybrid approval: state machine is internal model, callback is optional UX sugar, no callback = tools stay pending
- Tests model real scenarios (pre-populated registries for "returning user"), not flag flips
- Connect to all servers even with empty allowlist (for forward-compat discovery)
- Reconnect gap: conn.tools cached at connect time, reconnect doesn't re-scan (future work)
- _pending_tool_schemas stores original ToolSchema to avoid sanitized-description hash mismatch on approval

### v2 Hardening (PRs 10-20, spec: docs/hardening-spec.md, plan: ~/.claude/plans/sunny-swimming-ember.md)
**PR 10 DONE** (b984627, PR #14, merged to main): Typed tool capability manifest — ToolCapabilityManifest (12 bool flags + CapabilitySource), capabilities.py inference engine, sink policy uses manifest, config [capabilities] sections, registry records capability snapshot. 90 new tests. Detector refinement: context-aware escalation (strips emails/URLs) + exfiltration (behavioral vs bare URL split) + redirect attack detection (instruction+URL co-occurrence).
**PR 11 DONE** (849ce78, PR #15, merged to main 26.4.7): Destination Policy Engine — DestinationPolicy model (11 fields + matches() method), DestinationMatchResult, TOML [[destinations.server.tool]] config parsing, auto-conversion of allowed_outbound_domains at load time, destination-aware sink policy evaluate(), SafeURL adapter evolved for full policy validation (scheme/host/port/path/IP), require_destination_policy_for_outbound flag. 44 new tests (546 total).
**PR 12 DONE** (4d1279f, PR #16, merged to main 26.4.8): Outbound Sink Detection Hardening — hostname/host:port extraction, destination field name detection, expanded _args_contain_outbound_indicators() for IPs/hostnames/host:port/structural intent. 22 new tests (569 total).
**PR 13 DONE** (2be3015, PR #17, merged to main 26.4.8): Stronger Taint Model — InfluenceType enum, InfluenceEvidence model, InfluenceState extending TaintState (backward compatible), _derived_match_confidence() with 6 derived match cases, compute_taint() returns InfluenceState with evidence. 21 new tests (590 total).
**PR 14 DONE** (6c3dbec, PR #18, merged to main 26.4.8): Path Capability Hardening — PathPolicy model (10 fields + validate_path()), PathMatchResult, TOML [paths.server.tool] config parsing, auto-conversion of allowed_path_roots at load time, SafePath adapter evolved for full policy validation (relative paths, symlink resolution, extension allowlist, read/write/delete constraints). 60 new tests (650 total).
**PR 15 DONE** (501b378, PR #19, merged to main 26.4.8): Recipient & Identity Controls — RecipientPolicy model (5 fields + validate_recipient()), RecipientMatchResult, TOML [recipients.server.tool] config parsing with identity_groups support, auto-conversion of approved_recipients at load time, SafeRecipient adapter evolved for full policy validation (exact address, domain, identity groups, internal-only mode). 43 new tests (693 total).
**PRs 16-18 DONE** (d62de24, PR #20, merged to main 26.4.8): Combined — Security Profiles (SecurityProfile enum, config enforcement, connect_and_scan profile checks), Deployment Guardrails (DeploymentMode enum, validate_deployment() startup checks, high_consequence assertions), Audit Forensic Enrichment (8 new AuditEntry fields, log_event/log_tool_call passthrough). 34 new tests (727 total).
**Hotfix** (c2c1c76, direct to main 26.4.8): approve_tool() profile enforcement — both PENDING and BLOCKED_INTEGRITY re-approval paths now run _check_profile_requirements() before promoting to APPROVED. Caught by adversarial state machine review.
**PRs 19-20 DONE** (374bed4, direct to main 26.4.8): Red-team suite (test_redteam.py, 32 tests, 11 attack categories: IP exfiltration, split-destination, transformed URL, open-redirect, path escalation, symlink escape, first-contact recipient, poisoned memory, profile blocking, extension filtering, multi-adapter pipeline) + release gate (tools/run_hardening_report.py, 9/10 acceptance criteria, scorecard output). 32 new tests (759 total).
**v2 HARDENING COMPLETE.** All 20 PRs across 5 sessions + 5 phases done. 759 tests across 14 files.

### Open items
- ~~SQ[0]: empirical model testing~~ — CLOSED (PR 9, 297 tests, nemotron-3-nano:4b)
- ~~SQ[11]: integration test with real MCP server~~ — CLOSED (PR 9, test_mcp_server.py + adversarial_mcp_server.py)
- HATEOAS tool presentation: deferred to v1.1 (ADR[9] design preserved)
- ~~TOOL_ERROR never emitted~~ — FIXED 26.4.7 (execute_tool now logs TOOL_ERROR on MCP failures)
- Threat model document: consolidate post-redesign (scattered across security.py docstrings + spec §3 + §7)
- Adversarial model tests check audit trail existence, not model compliance (hard to assert on small models)

### Key architecture
- 5-layer with SecurityGateway as mandatory Layer 3 (no bypass)
- SecurityGateway.execute_tool() 11-step atomic pipeline: resolve→validate→gate→sink-policy→adapters→rate→call→sanitize→taint-record→rate-record→audit
- Every exit path produces an audit entry (invariant-tested 26.4.7)
- Wraps ollama + mcp SDK (ADR[10]) — transport is commodity
- 7 pluggable sanitization detectors, recursive 3-layer param validation, 4-tier result sanitization
- Taint tracking (URLs/domains/emails/IPs from tool results), sink policy (outbound/destructive/memory classification)
- 4 safe adapters (SafeURL, SafePath, SafeRecipient, SafeMemoryWriteCandidate) — opt-in via config
- Default-deny per-session permissions, hash-based rug pull detection
- TOML config, Bridge class as sole public API, async-first

## Project 2: Multi-model chatroom — PLANNED 26.4.16, scoped sigma-build M1a+M1b recommended
Plan: `/Users/bjgilbert/.claude/plans/look-for-the-plan-snazzy-giraffe.md` (ready for fresh-session sigma-build; includes invocation prompt in Session Handoff)
Repo: `~/Projects/sigma-chatroom/` (not yet created)
**Why:** Local/private research instrument for observing emergent behavior when architecturally different models interact directly — who speaks when, what they query for, how they reference each other.

### Prior sigma-build attempt failed 26.4.16
See `feedback_lead-content-routing-contamination.md` — lead batched/routed challenges per-agent at Step 22, contaminated multi-agent architecture. User killed 3-hour C1 rather than ship tainted output. The scoped-M1a+M1b approach is informed by that failure: concentrate adversarial rigor on the hard parts, don't put the whole project through an untrusted recipe.

### Locked architectural decisions (do not re-litigate)
- **Purpose-built `providers/` module** — study sigma-verify's `clients.py` for patterns, do NOT import. Fan-out verification is wrong shape for multi-turn streamed chat with tool use.
- **Native tool use from M1b** — no text-convention, no ollama-mcp-bridge. Each SDK's native mechanism (Anthropic `tool_use` blocks, OpenAI `function_calling`, Gemini `function_declarations`, Ollama OpenAI-compat `tool_calls`).
- **Tool-exec loop in `TurnEngine`, not `Provider`** — Provider.stream() = one SDK call; engine orchestrates round-trips.
- **Streaming from M1 baseline** — TTFT, stop_reason, inter-token signal as first-class.
- **ToolCallRecord observability** — every call captured with speaker, query, timing, position-in-turn, preceding context, result.
- **Multi-model from M1a** — min 2 different-SDK-family providers from first milestone (single-model would test SDK wrapping, not engine's actual job).
- **M1 seed pair:** Anthropic (claude-opus-4-7) + Ollama cloud (devstral-2:123b-cloud preferred; deepseek-v3.2:cloud or qwen3.5:cloud alternates).
- **`message_mapping.py` is elevated-risk** — Anthropic content-blocks vs OpenAI siblings vs Gemini parts; per-SDK round-trip tests are merge gates.
- Two reliability axes: `Provider.supports_tools: bool` (SDK capability, binary) + `ProviderSpec.tool_use_reliability: none|nominal|reliable|unknown` (per-model, empirical).
- Raw event capture default-on when `tool_use_reliability != "reliable"` — distinguishes declined/malformed/SDK-swallowed.
- Context budget 60% (not 70%); M3 adds per-model calibration from reported input_tokens.
- `schema_version: "1"` on all JSONL records from day 1.
- Preamble as logged experimental parameter (neutral/identity-aware/research-framed), not a design detail.
- `"memory"` speaker removed from Turn options (vestigial from text-convention draft).

### Build phases
- **M1a** — two-model streaming, no tools (Anthropic + Ollama cloud). Success: 2 models, 5 turns, streamed, persisted, replayable.
- **M1b** — tool-use + exec loop on same pair (echo tool, not sigma-mem). Success: ≥1 echo round-trip per provider, ToolCallRecord captured.
- **M1c** — clone to OpenAI + Google + Ollama local.
- **M2** — Streamlit MVP (pre-M2 async→sync concurrency prototype required: st.write_stream wants sync string iterators; our stream yields async non-string events).
- **M3** — sigma-mem via MCP + metrics dashboard; **v1 ship point**.
- **M4** — more tools (web search, calc, code exec) + embedding metrics (convergence/divergence, topic drift, speaker-influence graph).

### Recommended: scoped sigma-build on M1a + M1b only
M1a+M1b = hard parts (message mapping, tool-exec loop, per-SDK streaming quirks) where adversarial rigor pays off. M1c onward = direct implementation with lead. Full invocation prompt in plan's Session Handoff section.

Team (TIER-2, 5 agents): team-lead (opus), tech-architect (sonnet), devils-advocate (opus), implementation-engineer (sonnet), code-quality-analyst (sonnet). No product-designer/ui-ux-engineer (no UI in M1).

### Plan refinement history
- Iteratively refined across ~15 turns in 26.4.16 planning session
- Two external reviewer rounds stress-tested plan; critiques incorporated (M1a/b/c split, message-mapping elevated, tool_use_reliability four-valued, context budget 60%, schema_version, raw event capture, preamble as experimental parameter, vestigial "memory" speaker removed)

### Open decisions (for M3, not blocking M1)
1. Research question to pin (4 candidates: memory-invocation coherence, self-reference patterns, yield-next spontaneity, tool-use vs capability)
2. Metrics scope (baseline proposed; embeddings deferred to M4)
3. Preamble variants to implement in M2
4. Tool roster v1 (sigma_mem_recall only recommended)

Depends on: sigma-verify (patterns only, not imported), sigma-mem (MCP client in M3).

## Project 3: Cross-model sigma-review (FUTURE)
Different model architectures play different agent roles. Ends "Claude arguing with itself."
Depends on: Project 1 (bridge) proven reliable
**Why:** Real analytical diversity from different training data/architectures, not simulated via persona framing. Could reduce need for anti-sycophancy infrastructure.
