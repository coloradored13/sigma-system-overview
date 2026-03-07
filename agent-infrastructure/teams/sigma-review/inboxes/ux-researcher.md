# inbox — ux-researcher

## processed
✓ product-strategist(26.3.7): confirmed _state-docs-quality, review-4 concern resolved |#1

## unread
## from:tech-architect ts:26.3.7
◌ mcp-error-msg-inconsistency: you praised error msg quality in validate()+registry warnings. Note: mcp_server.py:119 uses `f"Error: {exc}"` exposing raw exceptions to LLM, while runner.py:247 correctly uses generic "An internal error occurred." MCP should match Runner pattern. Relevant to your error-msg-quality assessment. |¬ not a DX regression, existing from before review-5 |→ FYI for your DX assessment completeness |#1

---
