---
name: Test execution pattern for long-running suites
description: Run live/model tests individually or by tier, never as a monolith — prevents timeouts and enables clean subprocess cleanup
type: feedback
---

Split long-running test suites into independently-runnable tiers. Run tier by tier, not as a monolith.

**Why:** Model inference tests take 30-60s each. Running 33 live tests together hits 10+ minute timeouts, causes background-process issues, and masks failures. Running individually gives clean subprocess lifecycle per test and visible progress.

**How to apply:** For ollama-mcp-bridge or any project with model-in-the-loop tests:
1. Split by speed tier (unit <1s, MCP-only ~1s, model ~30s, multistep ~60s)
2. Run tiers sequentially, not combined
3. Use `--tier=` flag or target specific test files
4. For report generation, use `run_e2e_report.py --tier=X` per tier then `--merge`
5. Never brute-force retry a timing-out command — pause and restructure the approach
