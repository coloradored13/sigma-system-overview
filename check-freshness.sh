#!/bin/bash
# Check that all submodules are up-to-date with their remote main branches.
# Run from sigma-system-overview root.
#
# Usage:
#   ./check-freshness.sh          # check only
#   ./check-freshness.sh --update # check + update stale submodules
#   ./check-freshness.sh --ci     # check only, exit 1 if stale (for CI)

set -euo pipefail

UPDATE=false
CI=false
STALE=false

for arg in "$@"; do
  case "$arg" in
    --update) UPDATE=true ;;
    --ci) CI=true ;;
  esac
done

echo "Checking submodule freshness..."
echo ""

for sub in hateoas-agent sigma-mem sigma-verify; do
  if [ ! -d "$sub" ]; then
    echo "  $sub: NOT FOUND (submodule not initialized)"
    STALE=true
    continue
  fi

  cd "$sub"
  git fetch origin --quiet 2>/dev/null || true

  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "unknown")

  if [ "$REMOTE" = "unknown" ]; then
    echo "  $sub: UNKNOWN (could not fetch remote)"
    cd ..
    continue
  fi

  if [ "$LOCAL" = "$REMOTE" ]; then
    SHORT=$(echo "$LOCAL" | cut -c1-7)
    echo "  $sub: OK ($SHORT)"
  else
    LOCAL_SHORT=$(echo "$LOCAL" | cut -c1-7)
    REMOTE_SHORT=$(echo "$REMOTE" | cut -c1-7)
    BEHIND=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")
    echo "  $sub: STALE (local=$LOCAL_SHORT, remote=$REMOTE_SHORT, $BEHIND commits behind)"
    STALE=true

    if $UPDATE; then
      cd ..
      git submodule update --remote "$sub"
      echo "    → Updated to $(cd "$sub" && git rev-parse --short HEAD)"
      cd "$sub"
    fi
  fi
  cd ..
done

echo ""

if $STALE; then
  if $UPDATE; then
    echo "Submodules updated. Review with 'git diff' then commit."
  elif $CI; then
    echo "STALE: Run './check-freshness.sh --update' or 'git submodule update --remote'"
    exit 1
  else
    echo "STALE: Run './check-freshness.sh --update' to update, or 'git submodule update --remote' manually."
  fi
else
  echo "All submodules current."
fi
