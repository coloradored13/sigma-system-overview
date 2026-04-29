#!/usr/bin/env bash
#
# A25 template-drift sync utility (per ADR[5]/IC[5]).
#
# Recomputes SHA256 baseline for all templates in
# ~/.claude/teams/sigma-review/shared/templates/ and writes the manifest to
# .templates-hash-baseline.json (sidecar). Run after legitimate template
# updates; commit the new baseline alongside the template change.
#
# Hash-identity normalization (must match chain-evaluator._a25_normalize):
#   1. CRLF/CR → LF (cross-platform parity per PM[4])
#   2. strip leading BOM
#   3. rstrip each line (trailing whitespace)
#
set -euo pipefail

TEMPLATES_DIR="${SIGMA_TEMPLATES_DIR:-$HOME/.claude/teams/sigma-review/shared/templates}"
BASELINE="$TEMPLATES_DIR/.templates-hash-baseline.json"

if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "ERROR: templates directory not found: $TEMPLATES_DIR" >&2
    exit 1
fi

# Use Python for hashing — guarantees byte-identical normalization with
# chain-evaluator's _a25_normalize (avoids shell-vs-Python rstrip drift).
python3 - "$TEMPLATES_DIR" "$BASELINE" <<'PY'
import hashlib
import json
import re
import sys
from pathlib import Path

templates_dir = Path(sys.argv[1])
baseline_path = Path(sys.argv[2])

BOM_RE = re.compile(r"^﻿")


def normalize(text: str) -> str:
    text = BOM_RE.sub("", text).replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.split("\n"))


manifest: dict[str, str] = {}
for path in sorted(templates_dir.iterdir()):
    if not path.is_file():
        continue
    if path.name.startswith("."):
        continue  # exclude dotfiles like the baseline itself
    text = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()
    manifest[path.name] = digest

baseline_path.write_text(
    json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(f"Wrote {len(manifest)} template hashes to {baseline_path}")
for name, h in sorted(manifest.items()):
    print(f"  {name}: {h[:16]}...")
PY

echo ""
echo "Recovery (if A25 fires WARN):"
echo "  1. Confirm template change is intentional"
echo "  2. Re-run: $0"
echo "  3. Commit: git add $BASELINE && git commit -m 'Update template hash baseline'"
