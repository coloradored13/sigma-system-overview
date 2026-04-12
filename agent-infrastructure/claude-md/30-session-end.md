session-end(modified code|docs|mem):
1→verify repos committed+pushed(if approved)
2→check_integrity → checksums+consistency
3→verify projects.md current(test counts,versions,status)
4→agents spawned → verify inboxes processed+workspace convergence ✓
5→!infra-commit(if agents/skills/team files modified): `git add+commit+push` from ~/Projects/sigma-system-overview
6→!freshness-check(if hateoas-agent|sigma-mem modified): run `~/Projects/sigma-system-overview/check-freshness.sh --update` → commit submodule updates
7→!memory-backup(if memory modified): run `~/Projects/sigma-system-overview/agent-infrastructure/scripts/backup-memory.sh` → commit snapshot
