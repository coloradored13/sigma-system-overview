---
name: API budget pause on failure
description: Stop experiment and notify user on API failures rather than pushing through — user wants to top up budget before continuing
type: feedback
---

On API failures during sigma-optimize experiments, STOP and notify user immediately. Do not push through errors or let generations run with -5 error scores.

**Why:** Earlier runs wasted generations 7-10 of conservative search by continuing through budget exhaustion — all new candidates scored -5, only elites survived. That data is useless. User wants to top up budget before it contaminates results.

**How to apply:** After launching experiment, check logs for rate limit or budget errors. If errors appear, kill the process, report to user, wait for confirmation before restarting. Do not assume errors are transient.
