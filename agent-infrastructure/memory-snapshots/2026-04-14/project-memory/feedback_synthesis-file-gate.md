---
name: Synthesis file gate
description: Lead must write synthesis to file before setting synthesis_delivered — in-conversation delivery is not sufficient
type: feedback
---

Lead MUST write synthesis report to a file (archive/) before setting synthesis_delivered=true in orchestrator context. In-conversation message delivery does not satisfy the gate.

**Why:** 26.3.28 sigma-ui review — lead set synthesis_delivered after receiving synthesis agent's message and relaying it in conversation, without writing to file. User caught the bypass. The gate exists to ensure a durable artifact, not just a transient message.

**How to apply:** After synthesis agent returns report → (1) write to `shared/archive/{date}-{slug}-synthesis.md` → (2) verify file exists → (3) THEN set synthesis_delivered. The orchestrator advance should check for file existence, not just the context flag.
