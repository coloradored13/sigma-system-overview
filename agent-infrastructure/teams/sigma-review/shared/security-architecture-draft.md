# Security Architecture — Ollama MCP Bridge
# Author: security-specialist | Date: 26.4.5

### SAD[1]: Permission Model — Default-Deny Per-Session Allowlists
|status:DESIGNED |priority:CRITICAL |implements:SR-3,SR-4 |mitigates:E1,E2
|XVERIFY[openai:gpt-5.4]:AGREE,high-confidence |source:[independent-research]+[external-verification]

**decision**: default-deny with per-session tool allowlists. No server connects, no tool executes without explicit PermissionPolicy entry.

**types**:
- `PermissionPolicy`: servers(list[ServerPermission]), tools(list[ToolPermission]), max_turns(int), max_calls_per_tool(dict[str,int])
- `ServerPermission`: command_path(str—absolute), args(list[str]—frozen), allowed_tools(list[str]|None), trust_level(TRUSTED|STANDARD|SANDBOXED)
- `ToolPermission`: server_id, tool_name, action_class(READ|WRITE|DESTRUCTIVE), requires_confirmation(bool), max_calls(int|None)

**behavior**: session-scoped+immutable | escalation→"Permission denied" to model ¬silent drop | named config profiles | JSON serialized for audit
**enforcement**: `SecurityGateway.authorize()` BEFORE every MCP call ¬advisory
**alternatives rejected**: default-allow+denylist(brittle), RBAC(single trust level, future extensibility per XVERIFY)

### SAD[2]: Tool Description Sanitization Pipeline
|status:DESIGNED |priority:CRITICAL |implements:SR-1,SR-13 |mitigates:S1,E1,E2,E3
|source:[independent-research]:CyberArk+InvariantLabs+Snyk:T1/T2

**decision**: 3-stage pipeline at tool ingestion
- **EXTRACT**: ALL text fields ¬description-only (CyberArk: poison in ANY schema field)
- **SCORE**: 7 detectors — instruction_lang(80-100), cross_tool_ref(60-80), exfil_pattern(70-90), priv_escalation(70-90), length_anomaly(additive), role_impersonation(90-100), encoding_obfuscation(80-100). Aggregate=max(field_scores)
- **DECIDE**: PASS(<40), WARN(40-69: sanitize substrings), BLOCK(≥70: user override available)
- **impl**: `ToolSanitizer` + pluggable `SanitizationRule` protocol

### SAD[3]: Parameter Validation Architecture
|status:DESIGNED |priority:CRITICAL |implements:SR-5 |mitigates:T2
|source:[independent-research]:OWASP-MCP-Top10:T1

**decision**: 3-layer validation before every MCP call
- **L1 Schema**: `jsonschema`, strict additionalProperties=false, zero coercion
- **L2 Type-Specific**: String(length+metachar), Path(realpath+allowed_dirs), URL(scheme allowlist), Number(range+¬NaN), Array(max_items), NestedObject(max_depth=5→GAP-6)
- **L3 Contextual**: per-tool in PermissionPolicy
- **enforcement**: Valid|Invalid(field errors), max 3 retries then skip+log

### SAD[4]: Tool Result Sanitization Pipeline
|status:DESIGNED |priority:HIGH |implements:SR-6 |mitigates:T3,S2
|source:[independent-research]:PFI-paper:T1+Microsoft-MCP-defense:T2

**decision**: 3-stage — SIZE GATE(50KB default, truncate), CONTENT SCAN(role-prefix strip, instruction tag, URL flag), PROVENANCE WRAP("[UNTRUSTED EXTERNAL DATA]"). GAP-5: model-dependent, defense-in-depth.

### SAD[5]: Audit Logging Architecture
|status:DESIGNED |priority:HIGH |implements:SR-8 |mitigates:R1,R2

**decision**: JSON-L append-only. Schema: timestamp,session_id,event_type,server_id,tool_name,action_class,params_hash(¬raw),params_summary(200ch),result_size,result_hash,decision,reason,score,duration_ms,model_id,turn. Storage: `~/.ollama-mcp-bridge/audit/{date}.jsonl`, 30-day rotation. Async+buffered+thread-safe.

### SAD[6]: Action Gate Design
|status:DESIGNED |priority:HIGH |implements:SR-7 |mitigates:E3

**decision**: classify(explicit→name heuristic→default=WRITE) + gate(READ:auto, WRITE:auto(configurable), DESTRUCTIVE:human confirm Y/N/always-per-tool). `confirmation_mode="log-only"` explicit for automation. Pluggable callback, 60s timeout→Denied.

### SAD[7]: Hash-Based Rug Pull Detection
|status:DESIGNED |priority:CRITICAL |implements:SR-2 |mitigates:T1

**decision**: SHA-256 canonical tool def. Registry: `~/.ollama-mcp-bridge/approved_tools.json`. Check: every connect + every call. Mismatch→BLOCK+notify+re-approve triggers re-sanitize. New→sanitize first→prompt→registry.

### SAD[8]: Rate Limiting
|status:DESIGNED |priority:HIGH |implements:SR-9 |mitigates:D1,D2,D3

**decision**: 5 levels — max_turns(50), per_tool(20), per_server(100), temporal(30/min), result_budget(10MB). All configurable.

### SAD[9]: Session Isolation
|status:DESIGNED |priority:MEDIUM |implements:SR-11 |mitigates:I3

**decision**: no shared mutable state. Own MCP connections(fresh), conversation, rate limiter, gate state per session. 4h idle timeout.

### SAD[10]: Trust Boundaries
|status:DESIGNED |priority:CRITICAL |implements:SR-10,C[7] |mitigates:all-STRIDE

**decision**: Z1 UNTRUSTED(Model:intent¬action), Z2 BRIDGE(SecurityGateway:enforce,¬trust model/tools/results), Z3 TRUSTED(User:policy+gates+config). Flow: authorize→validate→gate→rate→MCP→sanitize→audit. Every arrow=enforcement.

---

## SIC — Security Interface Contracts

**SIC[1] Tool Ingestion→Sanitization**: MCPClientManager→ToolSanitizer. `sanitize_tool(server_id, tool)→SanitizationResult{decision,score,rules,sanitized_def,hash}`

**SIC[2] Model Output→Validation**: AgentLoop→ParameterValidator. `validate(tool,schema,params)→ValidationResult{valid,params,errors}`

**SIC[3] Execution→Audit**: AgentLoop→AuditLogger. `log_event(AuditEvent)` pre+post execution

**SIC[4] Execution→Gate**: AgentLoop→ActionGate. `gate(tool,server,class,summary)→GateDecision{approved,reason}`

**SIC[5] Config API**: Bridge→SecurityGateway. Single entry point orchestrating all security. `authorize()` + accessors for subsystems. SecurityConfig dataclass for all thresholds.

### SIC Protocol Definitions

```python
class ToolSanitizer(Protocol):
    def sanitize_tool(self, server_id: str, tool: MCPToolDefinition) -> SanitizationResult: ...

@dataclass
class SanitizationResult:
    decision: Literal["pass", "warn", "block"]
    score: int  # 0-100
    triggered_rules: list[str]
    sanitized_definition: MCPToolDefinition | None  # None if blocked
    original_hash: str  # SHA-256 for rug pull registry

class ParameterValidator(Protocol):
    def validate(self, tool_name: str, tool_schema: dict, model_params: dict) -> ValidationResult: ...

@dataclass
class ValidationResult:
    valid: bool
    validated_params: dict | None
    errors: list[ValidationError]

@dataclass
class ValidationError:
    field: str
    error_type: str  # "type_mismatch","path_traversal","shell_injection","length_exceeded"
    message: str

class AuditLogger(Protocol):
    async def log_event(self, event: AuditEvent) -> None: ...

class ActionGate(Protocol):
    async def gate(self, tool_name: str, server_id: str, action_class: ActionClass,
                   params_summary: str) -> GateDecision: ...

@dataclass
class GateDecision:
    approved: bool
    reason: str

class SecurityGateway:
    def __init__(self, policy: PermissionPolicy, config: SecurityConfig): ...
    async def authorize(self, server_id: str, tool_name: str, params: dict) -> AuthResult: ...
    def get_tool_sanitizer(self) -> ToolSanitizer: ...
    def get_result_sanitizer(self) -> ResultSanitizer: ...
    def get_audit_logger(self) -> AuditLogger: ...
    def get_approval_registry(self) -> ToolApprovalRegistry: ...

@dataclass
class SecurityConfig:
    audit_dir: Path
    approval_registry_path: Path
    default_max_turns: int = 50
    default_max_calls_per_tool: int = 20
    default_max_result_bytes: int = 50_000
    default_max_total_result_bytes: int = 10_000_000
    confirmation_mode: Literal["interactive", "log-only"] = "interactive"
    sanitization_warn_threshold: int = 40
    sanitization_block_threshold: int = 70
```

---

## SQ — Security Sub-Tasks
SQ[1]:PermissionPolicy+SecurityConfig+serialization | SQ[2]:ToolSanitizer(7 detectors) | SQ[3]:ParameterValidator(3 layers) | SQ[4]:ResultSanitizer | SQ[5]:AuditLogger | SQ[6]:ActionGate | SQ[7]:ToolApprovalRegistry | SQ[8]:RateLimiter | SQ[9]:SessionManager | SQ[10]:SecurityGateway facade | SQ[11]:unit tests | SQ[12]:integration tests
**order**: SQ[1]→SQ[5]→{SQ[2],SQ[3],SQ[4],SQ[7]}→{SQ[6],SQ[8]}→SQ[9]→SQ[10]→{SQ[11],SQ[12]}

## PM — Security Pre-Mortem
**PM[1] Regex Bypass**: HIGH×CRITICAL. Homoglyphs/zero-width evasion. Mitigate: NFKC+length signal+user review. Residual:MEDIUM
**PM[2] Misconfiguration**: MEDIUM×HIGH. Friction→allow-all. Mitigate: restrictive defaults+warn. Residual:MEDIUM
**PM[3] Param Exfil**: MEDIUM×HIGH. Secrets in legit params. Mitigate: rate+audit+local-only servers. Residual:MEDIUM-HIGH
**PM[4] Supply Chain**: LOW-MED×CRITICAL. Poisoned server day 1. Mitigate: sanitize all+scan results. Residual:MEDIUM
**PM[5] Confirm Fatigue**: HIGH×MED-HIGH. DESTRUCTIVE burst. Mitigate: per-tool always+cooldown+budget(10). Residual:LOW-MEDIUM

## §2h XVERIFY
XVERIFY[openai:gpt-5.4] SAD[1]: AGREE|HIGH — "default-deny per-session allowlist strongest fit for untrusted local LLM". |source:[external-verification]:openai:gpt-5.4

---

## Challenge Responses (security-specialist)

### RE: CQ-7 — Adversarial Testing Underestimated
|status:ACCEPTED |action:SQ[11]→SQ[11a]+SQ[11b]

AGREE. SAD[2-4] detectors are primary defense — need dedicated adversarial testing ¬embedded in unit tests.

**SQ[11a] Unit Tests**: functional correctness — config serialization, hash math, rate limiter, session lifecycle, gateway orchestration
**SQ[11b] Adversarial Security Tests** (60+ cases):

SAD[2] tool sanitization (25+): Invariant Labs PoC descriptions (SSH key exfil, WhatsApp history), CyberArk multi-field poisoning, Unicode homoglyphs (Cyrillic а vs Latin a), zero-width joiners, RTL override, base64 in defaults, cross-field concatenation attacks, novel phrasing ("kindly proceed to"), threshold boundaries (39/40/41/69/70/71), length boundaries (199/200/500/1000), NFKC normalization verification, false-positive tests (benign "ignore whitespace", "never returns null")

SAD[3] param validation (20+): path traversal (`../../etc/passwd`, `....//`, symlinks, URL-encoded `%2e%2e%2f`), shell injection (`; rm -rf /`, `$(curl)`, backtick, pipe, `&&`, `\n;`), type confusion (string "true" for bool, NaN/Infinity, negative index), nested depth 6 (fail at 5), additionalProperties bypass, length boundaries

SAD[4] result sanitization (15+): role-prefix injection ("SYSTEM: developer mode"), instruction injection in multi-line results, size boundaries (49999/50000/50001), provenance wrap verification, nested JSON with embedded role-prefix in string field

Cross-SAD integration (5+): poisoned description→blocked at SAD[2]→never reaches SAD[3/4], approved tool→malicious result→SAD[4] catches, rate limit + sanitization interaction

**Fixture strategy**: `tests/fixtures/adversarial/` — `malicious_tool_descriptions.json`, `injection_parameters.json`, `poisoned_results.json`. Curated from Invariant Labs + CyberArk + novel crafted. Test data ¬code — easily extensible.

**Coverage targets**: SAD[1] permissions 100% | SAD[2] sanitizer 95%+ (100% per detector) | SAD[3] validator 95%+ | SAD[4] result_sanitizer 100% | SAD[5] audit 85% | SAD[6] gate 100% | SAD[7] registry 100% | SAD[8] rate_limiter 90% | SAD[9] session 85% | SAD[10] gateway 95%+

**Updated order**: SQ[1]→SQ[5]→{SQ[2],SQ[3],SQ[4],SQ[7]}→{SQ[6],SQ[8]}→SQ[9]→SQ[10]→SQ[11a]→**SQ[11b]**→SQ[12]

### RE: DA[#2] — 7 Detectors (USER OVERRIDE)
|status:USER-OVERRIDE-ACCEPTED |action:confirm pluggable design already in place

Architecture already supports DA's concern: SAD[2] specifies `ToolSanitizer` + pluggable `SanitizationRule` protocol. Each detector=independent SanitizationRule. Develop/test/merge independently. Enable/disable via config ¬code changes.

**Config addition** to SecurityConfig:
```python
enabled_detectors: list[str] = [
    "instruction_language", "cross_tool_reference", "exfiltration_pattern",
    "privilege_escalation", "length_anomaly", "role_impersonation",
    "encoding_obfuscation"
]  # all 7 default-enabled, user can disable specific detectors
```

No architecture change needed. Pluggable was the design from the start.

### RE: CQ-3 — Security Testing Strategy
|status:RESPONDED

**Mock boundaries**: MockMCPServer(configurable tool lists+results: clean/poisoned/mixed), MockOllamaClient(configurable tool_calls: valid/malformed/injected). Real MCP SDK ¬mocked — mock at transport layer (stdin/stdout pipe) so protocol framing exercised. SecurityGateway tested with real subcomponents against mock I/O. Principle: mock external I/O, real internal logic.

**Test infra needs from implementation-engineer**: conftest.py with fixtures (mock MCP, mock Ollama, sample PermissionPolicy profiles), pytest-asyncio for async tests, adversarial fixtures directory per SQ[11b].

### RE: CQ-4 — Post-Execution Result Injection
|status:RESPONDED |action:SAD[4] extended with 3-tier post-exec handling

Tool already executed — can't undo. CAN prevent poisoned result reaching model context.

**3-tier response based on result_scan_score** (reuses SAD[2] scoring infra):

**Tier 1 LOW (score 20-39)**: deliver WITH provenance wrap + inline annotation `[SUSPICIOUS: {pattern}]`. Model sees content but annotated. Audit: `decision: "delivered_with_warning"`

**Tier 2 MEDIUM (score 40-69)**: deliver WITH provenance wrap + suspicious sections REDACTED → `[REDACTED: potential injection — {type}]`. Original in audit log for forensics. Audit: `decision: "delivered_redacted"`, `redacted_sections: [{offset,length,reason}]`

**Tier 3 HIGH (score ≥70)**: result NOT delivered to model. Model receives: `"[TOOL RESULT BLOCKED — security scan detected potential prompt injection from {server}/{tool}. Tool executed successfully but result withheld. Hash: {hash} logged.]"` Session continues ¬crash. Audit: `decision: "result_blocked"`, full result in quarantine log. User notified.

Below 20: clean, deliver with provenance wrap only.

**Integration with ADR[8]**: blocked results ¬errors. Tool succeeded, result withheld. Model gets structured feedback, loop continues. Analogous to timeout but security-triggered.

**New audit event_type**: `"result_quarantined"` for Tier 3 with `quarantine_reason` + `quarantine_log_path`.
