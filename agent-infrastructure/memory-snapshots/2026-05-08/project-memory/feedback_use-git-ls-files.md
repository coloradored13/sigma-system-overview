---
name: Use git ls-files not find
description: Use git ls-files or Grep (respects .gitignore) instead of find for repo file searches — avoids .venv clutter
type: feedback
---

Use `git ls-files` or the Grep tool for searching repo files, not `find` or `ls`. `find` traverses `.venv/`, `node_modules/`, etc. and produces noisy results.

**Why:** User flagged after a `find . -name "*spec*"` returned 20 lines of .venv garbage when the answer was "not in the repo." `git ls-files | grep spec` would have been one clean line.

**How to apply:** Any time searching for files in a git repo, prefer `git ls-files` (tracks only committed/staged files) or the Grep/Glob tools (respect .gitignore). Reserve `find` for system-level searches outside repos.
