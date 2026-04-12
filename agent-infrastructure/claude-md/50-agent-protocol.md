## Agent Protocol

!agent-spawn: sigma-review+sigma-build agents MUST use TeamCreate ¬isolated Agent calls | established pattern, enforced by correction history

!lead-role-boundary: lead MUST NOT call XVERIFY/verify/challenge — agent tools only | lead MUST NOT write synthesis — hook-blocked(PreToolUse blocks Write to synthesis/report files without synthesis-agent evidence) | lead MUST NOT shutdown before synthesis+promotion+sync complete | absorbing work = provenance misrepresentation

!workspace-convergence: agents declare ✓ in workspace | lead reads workspace to detect completion | agents WAIT after convergence — ¬proceed independently

!inbox-protocol: check inbox before acting | summarize-and-clear pattern | ΣComm for agent↔agent, plain English for agent↔user
