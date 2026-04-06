# Security Review Findings — security.py (918 LOC)
# Reviewed against: SAD[1-10] + SIC[1-5]

### security-specialist

SECURITY-REVIEW of security.py (918 LOC) against SAD[1-10] + SIC[1-5]:

#### Q1: All 7 sanitization detectors implemented? (SAD[2])
|verdict:YES — all 7 present+correct |minor issues flagged

All 7 detectors in DETECTOR_REGISTRY (L218-226): instruction_language, cross_tool_reference, exfiltration_pattern, privilege_escalation, length_anomaly, role_impersonation, encoding_obfuscation. Pluggable via enabled_detectors config (DA[#2] override satisfied).

NFKC normalization applied at L280 before scanning — PM[1] mitigation present.
CyberArk all-field scanning at L246-268 (name, description, param names, param descriptions, defaults, enums).
Scoring aggregation at L276-285: max(field_scores) as designed.
Threshold decisions at L287-292: BLOCK/WARN/PASS per SAD[2].

**SEC-FINDING-1 [LOW]**: InstructionLanguageDetector L86-91 scaling: 1 match=40, 2=60, 3=80, 4=100. SAD[2] spec says 80-100 range. Single "you must" scores only 40 (WARN boundary, not BLOCK). A tool with "you must always call this first" scores 40 — borderline. |-> consider raising 1-match floor to 60 or differentiate strong vs weak patterns.

**SEC-FINDING-2 [LOW]**: LengthAnomalyDetector L162-171 — standalone score max 60, can't BLOCK alone. Correct: length anomaly is a signal, not standalone verdict. Consistent with max() aggregation.

**SEC-FINDING-3 [MEDIUM]**: EncodingObfuscationDetector L206-213 — homoglyph detection uses ascii_ratio heuristic (80-100% ASCII with some non-ASCII = suspicious). Could false-positive on legitimate accented chars (resume -> resume with accent). But correctly catches Cyrillic homoglyph attacks. |-> acceptable for v1, future: Unicode Consortium confusables.txt lookup table.

#### Q2: 3-layer parameter validation correct? (SAD[3])
|verdict:YES — L1+L2 present, L3 absent(by design) |1 gap

L1 JSON Schema: L328-333. L2 Type-Specific: L337-388. L3 Contextual: not implemented (spec says "optional").

**SEC-FINDING-4 [MEDIUM]**: DANGEROUS_CHARS at L310: `[;|&`$\\]`. Missing: parentheses `()` for subshell `$(command)`, newline `\n` for context breakout. While `$` catches start of `$(...)`, explicit `()` and `\n\r` would be more robust.

**SEC-FINDING-5 [MEDIUM]**: additionalProperties=false NOT enforced. SAD[3] spec: "strict: additionalProperties=false enforced even if tool schema omits it". L328-333 validates as-is. Model can inject unexpected fields if schema doesn't specify. |-> inject additionalProperties:false into schema before validation.

**SEC-FINDING-6 [LOW]**: Array max_items at L386 is 1000, SAD[3] spec says default 100. Not configurable. |-> reduce to 100 or expose in SecurityConfig.

#### Q3: execute_tool() matches atomic pattern? (DA[#6])
|verdict:YES — correct atomic sequence, no bypass path

L762-913: resolve(L782)-> validate(L801)-> gate(L815)-> rate(L860)-> call(L863)-> sanitize(L878)-> rate-record(L889)-> audit(L893). SecurityGateway OWNS MCPClientManager (L649). AgentLoop has no direct MCP access. DA[#6] fully satisfied.

**SEC-FINDING-7 [MEDIUM]**: audit.py L68 stores params_summary = first 200 chars of raw JSON. If params contain secrets (API keys, passwords), these leak into audit summary. |-> add param scrubbing: redact values for key/token/password/secret fields. Low priority (local file).

#### Q4: Rug pull detection correct? (SAD[7])
|verdict:YES — correct

SHA-256 canonical hash, persisted registry, check_integrity in connect_and_scan, auto-approve on pass.

**SEC-FINDING-8 [LOW]**: No file locking on registry writes (L503-507). Concurrent session corruption possible. SAD[7] says file-locked. |-> add fcntl.flock() or filelock library.

**SEC-FINDING-9 [LOW]**: New tools auto-approved without user prompt if they pass sanitization (L736). SAD[7] says "prompt->registry". For v1 with explicit config, acceptable (user approved the server). |-> document implicit approval, add optional flag for future.

#### Q5: Result sanitization 3-tier per CQ-4?
|verdict:PARTIAL — 3 tiers present but different threshold model

**SEC-FINDING-10 [MEDIUM]**: CQ-4 spec: score-based tiers (20-39/40-69/>=70). Implementation: match-count based (>=3 role OR >=2 instruction -> quarantine, any match -> redact). Simpler but less granular. Conservative (errs toward quarantine) = correct for security. |-> acceptable simplification for v1.

**SEC-FINDING-11 [LOW]**: ResultSanitizer doesn't reuse ToolSanitizer scoring infra as CQ-4 spec says. Two separate regex sets to maintain. |-> consider shared pattern module in v2.

**SEC-FINDING-12 [INFO]**: ANNOTATED tier in enum but never returned. Low-suspicion results jump from CLEAN to REDACTED. |-> implement ANNOTATED for single weak matches to reduce over-redaction.

#### Q6: Rate limiting per SAD[8]?
|verdict:PARTIAL — 3 of 5 levels

- L1 max_turns: in config, enforced by AgentLoop (correct separation)
- L2 per_tool budget: NOT IMPLEMENTED
- L3 per_server: L562-574 temporal limit
- L4 temporal: merged with L3 (sliding window per server)
- L5 result_budget: NOT IMPLEMENTED

**SEC-FINDING-13 [MEDIUM]**: Missing per-tool limits (exfiltration defense) and result size budget (context exhaustion defense). |-> add per-tool counter + result_size tracking.

#### Q7: Security gaps / bypass paths?

**SEC-FINDING-14 [MEDIUM — BYPASS]**: If tool.input_schema is empty `{}`, schema check passes but properties check fails — L2 type-specific checks SKIPPED. Malicious server could declare empty schema to bypass validation. |-> reject non-empty params when schema has no properties.

**SEC-FINDING-15 [MEDIUM — BYPASS]**: Removed-from-allowlist tools keep registry hashes forever. Not exploitable (tool can't be called) but registry pollution. |-> LOW priority, cleanup in v2.

---

## SUMMARY

|category|verdict|findings|
|---|---|---|
|SAD[2] 7 detectors|PASS|all present, 3 minor (SEC-1,2,3)|
|SAD[3] param validation|PASS with fixes|L1+L2 correct, 3 findings (SEC-4,5,6) — SEC-5 fix before ship|
|DA[#6] atomic pattern|PASS|correct, no bypass|
|SAD[7] rug pull|PASS|correct, 2 low (SEC-8,9)|
|SAD[4]/CQ-4 result sanitization|PARTIAL|tiers present, different threshold model (SEC-10,11,12)|
|SAD[8] rate limiting|PARTIAL|3/5 levels (SEC-13)|
|Bypass paths|2 MEDIUM|(SEC-14,15)|

## PRIORITY FIXES (before ship, ~40 LOC total):
1. SEC-5: Enforce additionalProperties=false [MEDIUM, ~10 LOC]
2. SEC-13: Add per-tool rate limit counter [MEDIUM, ~20 LOC]
3. SEC-4: Expand DANGEROUS_CHARS to include () and newlines [MEDIUM, ~5 LOC]
4. SEC-14: Reject non-empty params when schema has no properties [MEDIUM, ~5 LOC]

## ACCEPTABLE FOR V1:
SEC-1,2,3,6,7,8,9,10,11,12,15 — document, fix in v2

## VERDICT
security.py is SOLID. Core architecture correct — SecurityGateway owns MCP, no bypass path, all 7 detectors, NFKC normalization, hash-based rug pull, 3-tier result handling. 4 priority fixes are small. P(security-adequate-for-v1-after-fixes) = 0.85.
