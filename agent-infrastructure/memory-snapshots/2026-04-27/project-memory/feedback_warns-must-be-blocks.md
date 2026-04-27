---
name: WARNs that can be ignored are no better than directives
description: If a hook WARN has no legitimate override, promote to BLOCK — WARNs have the same failure mode as prose directives under pressure
type: feedback
originSessionId: d7eadd85-5bd2-4be5-8e47-6169aa3c139b
---
A WARN the lead can ignore has the same failure mode as a directive it can ignore.

**Why:** During the hook enforcement build (26.4.11), initial design used WARNs for DA exit-gate, BELIEF tracking, CB evidence, and lead synthesis write. User challenged this: "if it's worth detecting is it worth blocking since warns can be ignored the same as directives?" This is correct — the entire point of hooks is involuntary enforcement.

**How to apply:** For each enforcement, ask: "Is there a legitimate reason to override this?" If no → BLOCK (PreToolUse exit code 2). If yes (heuristic detection, false positive risk) → WARN. Three checks were promoted from WARN to BLOCK in this session: BELIEF on advance, CB evidence on advance, lead synthesis write.
