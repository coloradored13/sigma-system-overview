# ollama-mcp-bridge: Security Architecture

Source: [B6, 26.4.9] (audit remediation build — 6 verified findings, A- rubric, 816 tests, 0 regressions)

---

## Overview

ollama-mcp-bridge's security layer is organized around a single enforcement chokepoint (SecurityGateway) backed by a family of typed adapter objects. The architecture separates the concerns of policy declaration, tool state tracking, and enforcement execution across distinct layers — with a deliberate gap in dormant policy fields that was surfaced and partially remediated in B6.

---

## SecurityGateway: Single Enforcement Chokepoint

The SecurityGateway is the sole enforcement surface in the bridge. All MCP tool calls pass through it; there is no parallel or secondary enforcement path. This single-chokepoint design is intentional — it means security logic is not distributed across handlers and cannot be bypassed by routing around a particular layer.

The consequence of this design is that any gap in the gateway is a full bypass, not a degraded path. The P0 finding in B6 (bare filename extraction) was dangerous precisely because the extraction step was the precondition for the gateway's path policy to fire: the gateway itself was correct, but the adapter feeding it was incomplete. [B6, 26.4.9]

---

## SafePath / SafeURL / SafeRecipient: The Adapter Pattern

The bridge uses typed adapter objects — SafePath, SafeURL, SafeRecipient — as the interface between raw MCP tool arguments and the SecurityGateway's policy evaluation. These adapters perform extraction and normalization before policy runs.

SafePath wraps file system paths. Its extraction is handled by `_extract_paths_from_args()` in `adapters.py`. SafeURL and SafeRecipient follow the same pattern for network destinations and email recipients respectively.

The adapters enforce a contract: the gateway receives typed, normalized values; it does not receive raw argument dicts. This keeps extraction logic separated from policy logic, and ensures that changes to how arguments are parsed do not require touching policy code. [B6, 26.4.9]

---

## Policy-Surface vs. Enforcement-Surface: The Core Audit Finding

The central architectural finding of B6 was the distinction between a field that *appears* in a policy object and a field that is *actively checked* at enforcement time.

Five fields in DestinationPolicy and RecipientPolicy existed in the type definition but were not read by any enforcement code: `allow_first_contact`, `query_constraints`, `allowed_methods`, `max_payload_bytes`, `allow_redirects`. An operator who configured these fields would receive no error and no enforcement — their intent would be silently discarded.

This is the policy-surface / enforcement-surface mismatch. The policy surface is what operators can configure; the enforcement surface is what the runtime actually checks. When these diverge, operators have false confidence in controls that don't exist.

The remediation in B6 was to annotate these fields as `NOT_YET_ENFORCED` and add Pydantic validators that raise ConfigError on any non-default value. The fields are not removed (to avoid breaking existing configs) but are now fail-loud rather than fail-silent. The validators follow the same philosophy as SecurityConfig's `extra="forbid"` — reject configurations that cannot be honored rather than accepting them silently. [B6, 26.4.9]

---

## ToolState Lifecycle

Tools transition through a defined state machine:

- **DISCOVERED** — tool has been observed from an MCP server
- **ALLOWLISTED** — tool has passed policy checks and is approved for invocation
- **BLOCKED_SANITIZATION** — tool was blocked because its arguments failed sanitization checks (e.g., path policy violation, unsafe URL)
- **BLOCKED_PROFILE** — tool was blocked because it matches a security profile (e.g., filesystem_access, network_egress) that is not permitted under the active configuration

The BLOCKED_PROFILE state was added in B6. Prior to B6, profile-blocked tools were recorded as BLOCKED_SANITIZATION, making them indistinguishable in the get_tool_states() API from sanitization failures. The split enables programmatic consumers to distinguish poisoned tools (sanitization block) from legitimately restricted tools (profile block). [B6, 26.4.9]

Note: ScanResult.blocked_sanitization still receives both types at the ScanResult level — the profile/sanitization distinction is only available via get_tool_states() or the audit log. This is a known wart from a DA compromise (see Known Limitations below).

---

## Field-Name Gate Pattern: Bare Filename Extraction

The P0 finding in B6 was that `_extract_paths_from_args()` only extracted string values that began with a slash or contained path separators. A tool argument like `{"filename": "db.sqlite"}` or `{"config_file": "secrets.txt"}` would not be extracted, and therefore PathPolicy.validate_path() would never run on it — a clean bypass.

The fix introduces a field-name gate: a `_FILESYSTEM_FIELD_NAMES` frozenset of known filesystem argument names (`file`, `filename`, `path`, `filepath`, `source_file`, `dest_file`, `output_file`, `input_file`, `config_file`, `db`, `database`). When a field's key matches this frozenset, its string value is extracted as a path candidate regardless of whether it contains a slash.

An initial design included a secondary layer: an independent extension-based heuristic that would extract any value ending in a recognizable extension (`.txt`, `.sqlite`, etc.) even from non-filesystem-named fields. This was dropped after adversarial challenge — it would fire on generic fields like `{"input": "report.csv"}`, generating false positives and potentially blocking legitimate operations. The field-name gate is the sole discriminator. [B6, 26.4.9]

A negative filter (`_is_non_path_value()`) prevents URL, email, and IP patterns from being extracted even if they appear in a filesystem-named field (e.g., `{"filename": "192.168.1.1"}`).

PathPolicy.validate_path() with `allow_relative_paths=False` is what actually enforces the policy — the extraction fix enables detection, the policy provides the enforcement.

---

## Dormant Field Handling: NOT_YET_ENFORCED + ConfigError

The standard pattern established in B6 for fields that exist in a policy type but are not yet enforced at runtime:

1. Annotate the field with a `# NOT_YET_ENFORCED — raises ConfigError if set` comment
2. Add a Pydantic v2 `@field_validator` (mode="after") that raises ValueError (surfaced as ConfigError) if the field is set to a non-default value
3. The field remains in the type — it is not removed — to preserve forward compatibility with configs that may be written before enforcement is implemented

This pattern makes the gap explicit to operators at config load time (startup failure) rather than runtime (silent non-enforcement). It also documents the intent: the field will eventually be enforced, and configs should be written assuming enforcement. [B6, 26.4.9]

The allow_redirects field received an additional fix: config.py's auto-conversion logic was setting `allow_redirects=True` as a default, which would have fired the ConfigError validator. This was corrected to `allow_redirects=False` to match the field's un-enforced default.

---

## Known Limitations

**List-item bare filenames** [B6, 26.4.9]: The field-name gate in `_extract_paths_from_args()` applies to top-level string values in the argument dict. It does not apply to items inside list values. A tool with `{"files": ["db.sqlite", "secrets.txt"]}` would not have those filenames extracted. This is a known architectural scope boundary — the fix addresses the common single-value case; the list-item case is a future ADR.

**Non-listed field names** [B6, 26.4.9]: Fields not in `_FILESYSTEM_FIELD_NAMES` are not caught regardless of their values. `{"source": "db.sqlite"}` would not trigger path extraction if "source" is not in the frozenset. The frozenset can be extended as new MCP tool patterns are observed.

**ScanResult.blocked_profile absent** [B6, 26.4.9]: ScanResult.blocked_sanitization receives both sanitization-blocked and profile-blocked tools. The distinction is available via get_tool_states() and the audit log, but not directly on ScanResult. This is a known wart from a deliberate DA compromise — the ScanResult API surface was not expanded for marginal consumer value. If operators report confusion, a follow-up can add blocked_profile to ScanResult.

**hardening-spec.md documentation** [B6, 26.4.9]: The dormant field behavior (NOT_YET_ENFORCED + ConfigError) is not yet reflected in hardening-spec.md. This was out-of-scope for B6.

**HARDENED + credential_access warning test coverage** [B6, 26.4.9]: validate_deployment() now emits a warning for HARDENED-profile tools that also have credential_access, but the warning path has minimal test coverage. No enforcement consequence; informational only.

---

## Cross-Agent Convergence Notes

Four findings in B6 reached multi-agent convergence independently, lending higher confidence:

- **Field-name gate direction**: tech-architect, security-specialist, and XVERIFY (gpt-5.4) all converged on field-name detection as superior to extension-only heuristics. XVERIFY additionally confirmed the extension-only approach was too narrow. [B6, 26.4.9]
- **ConfigError over removal for dormant fields**: tech-architect and security-specialist independently concluded that silent non-enforcement is worse than a breaking config error, from different analytical starting points. [B6, 26.4.9]
- **DERIVED_EMAIL_DOMAIN as telemetry-only gap**: both security-specialist and tech-architect traced the full sink classification path and independently reached the same conclusion — enforcement fires independently, the fix is audit fidelity only. [B6, 26.4.9]
- **Always-fsync for audit events**: DA, CQA, and tech-architect all reached the same conclusion independently; the two-path design was dropped unanimously. [B6, 26.4.9]
