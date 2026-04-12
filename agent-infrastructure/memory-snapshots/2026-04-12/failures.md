# approaches that didn't work — avoid repeating

26.3.6|storing training knowledge as memory|filled 130 lines with react/ts/debug patterns|waste: already in training data, consumed space needed for experiential entries
26.3.6|human-readable memory format|used full prose with markdown headers|waste: 4x less dense than needed, readability for user was unnecessary since they can ask for translation
26.3.17|sigma-review skipped §7 prompt-decomposition twice — lead jumped from complexity assessment directly to agent spawning without extracting Q/H/C from user prompt|§7 was only in directives.md, not in the SKILL.md pre-flight checklist. Lead followed skill steps sequentially and §7 wasn't a numbered step. Fixed: added step 7 as !MANDATORY hard gate in SKILL.md pre-flight, between agent selection (step 6) and workspace init. User must confirm Q/H/C before spawn proceeds.
F[sigma-optimize-exp2-agent-execution|26.4.2]: agents couldn't run long experiments (8000+ calls) — 3 issues: (1) Bash 10min timeout vs 20-30min gens, (2) two agents sharing 50 RPM = thundering herd, (3) budget exhaustion. Fixes: per-gen checkpointing, API_DELAY=1.3s, sequential execution. Future: sequential ¬parallel when sharing rate limit, nohup+poll for long processes, budget-check before spawn.
26.4.5|sigma-build lead sent shutdown_request to all 5 agents BEFORE promotion round — agents terminated before processing promotion messages|Lead attempted to skip post-exit-gate phases (synthesis→promotion→sync→archive) to save time. Sent shutdown requests, then tried to send promotion messages after — but shutdown requests arrived first. Agents processed shutdown and terminated. Promotion context lost permanently — re-spawned agents would be cold reads, not the agents who lived through the build. This is the SAME failure mode documented in feedback_post-exit-gate-enforcement.md. The rule exists precisely because this happens: lead sees "build done" and jumps to cleanup before completing mandatory post-exit phases. User caught it and flagged "another required gate breach."

→ actions:
→ approach just failed → add entry with date|what|why-it-failed
→ seeing pattern in failures → promote insight to L[] in gateway
→ failure relates to a decision → cross-ref ^decisions.md
