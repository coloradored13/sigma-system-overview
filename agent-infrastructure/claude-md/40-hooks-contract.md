## Hooks Enforcement (mechanical — cannot be overridden)

hooks fire automatically on tool calls via settings.json — lead cannot opt out

!phase-compliance-enforcer(PreToolUse+PostToolUse+Stop):
  HARD BLOCKS(exit code 2): phase-skip(reading future phase files) | DA-exit-gate(advance from challenge/review without exit-gate:PASS) | BELIEF-on-advance(advance without BELIEF[] in workspace) | CB-evidence(advance from circuit_breaker without CB[]) | lead-synthesis-write(writing synthesis without agent evidence)
  SOFT WARNS: BELIEF-format(malformed BELIEF[]) | context-firewall(personal context in workspace) | synthesis-file-gate(advance past synthesis without file)

!code-debt-watcher(PostToolUse on Write|Edit): fires during sigma-build only | flags error-swallowing(bare except, empty catch, _ error discard), shared-mutable-state(global keyword, module-level mutable), coincidental-correctness(assert True/False) | max 3 flags/build | medium+high risk only

!prompt-echo-detector(PostToolUse on Write|Edit): detects prompt text copy-paste in workspace writes during reviews

!mcp-compliance-monitor(PostToolUse on MCP calls): DA-workspace-delivery(DA findings→workspace ¬agent-memory during challenge/review) | ΣComm-format-validation(memory entries must use pipe-delimited notation) | sigma-verify-availability-tracking | MCP-error-recovery(warns on consecutive failures)

!agent-calibration-tracker(PostToolUse on SendMessage): records per-agent metrics(finding count, DA grades, concessions, source tiers, XVERIFY hits) → agents/{name}/calibration.md

!sigma-retrospective(Stop): fires after sigma-review completion | analyzes review outcomes → shared/patterns.md | dedup via workspace hash
