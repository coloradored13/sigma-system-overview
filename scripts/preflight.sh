#!/usr/bin/env bash
# preflight.sh — run ruff lint + format checks across submodule repos before pushing.
#
# Runs the same checks that each submodule's CI lint job runs, so local
# preflight catches formatting drift before the remote CI does.
#
# Usage: ./scripts/preflight.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v ruff >/dev/null 2>&1; then
  echo "ruff not installed. Install with: pip install ruff" >&2
  exit 2
fi

SUBMODULES=(hateoas-agent sigma-mem sigma-verify)
FAILED=()

for sub in "${SUBMODULES[@]}"; do
  if [[ ! -d "$sub" ]]; then
    echo "── $sub: directory not found, skipping"
    continue
  fi
  echo "── $sub"
  if ! (cd "$sub" && ruff check src/ tests/ && ruff format --check src/ tests/); then
    FAILED+=("$sub")
  fi
done

echo
if [[ ${#FAILED[@]} -eq 0 ]]; then
  echo "All submodules pass ruff check + format."
else
  echo "Failed: ${FAILED[*]}"
  echo "Fix with: cd <repo> && ruff check --fix src/ tests/ && ruff format src/ tests/"
  exit 1
fi
