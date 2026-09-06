---
name: Mock tests give false confidence
description: 132 mock-based tests passed but user audit found 8 real issues including broken Ollama contract. Empirical testing against real systems is non-negotiable.
type: feedback
---

Mock-only test suites give false confidence — 132 passing tests did not catch a broken Ollama tool-result contract (missing tool_name field), fake streaming (replay not live), or audit param leaks.

**Why:** SQ[0] empirical model testing was designed into the plan but never executed. All tests used mocked Ollama and MCP responses. The review round (4 agents on opus) also couldn't catch real-system contract issues because they reviewed against mocks too. User audit against actual Ollama docs found the core loop may not work.

**How to apply:** For any sigma-build that integrates with external systems (Ollama, MCP servers, APIs), empirical testing (SQ[0]) MUST run before declaring build complete. Mock tests validate internal logic. Only real-system tests validate the contract. If SQ[0] can't run in the build session, flag it as a blocking open item — don't ship "132 tests passing" as confidence signal.
