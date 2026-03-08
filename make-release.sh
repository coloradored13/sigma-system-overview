#!/usr/bin/env bash
# Creates a distributable zip of the Sigma System with all submodule contents included.
# GitHub's "Download ZIP" button does NOT include submodule files — use this instead.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure submodules are initialized
echo "Initializing submodules..."
git submodule update --init --recursive

# Verify critical files exist
for f in hateoas-agent/src/hateoas_agent/__init__.py sigma-mem/src/sigma_mem/__init__.py; do
    if [ ! -f "$f" ]; then
        echo "ERROR: $f missing — submodules not properly initialized"
        exit 1
    fi
done

# Verify imports work
echo "Verifying packages..."
PYTHONPATH="hateoas-agent/src:sigma-mem/src" python3 -c "import hateoas_agent; print(f'  hateoas-agent {hateoas_agent.__version__}')"
PYTHONPATH="hateoas-agent/src:sigma-mem/src" python3 -c "import sigma_mem; print('  sigma-mem OK')"

# Create zip
VERSION=$(date +%Y%m%d)
OUTFILE="sigma-system-${VERSION}.zip"

echo "Creating ${OUTFILE}..."
git archive --format=zip --prefix=sigma-system-overview/ HEAD -o "/tmp/${OUTFILE}"

# Add submodule contents (git archive doesn't include them)
cd hateoas-agent
git archive --format=zip --prefix=sigma-system-overview/hateoas-agent/ HEAD -o /tmp/ha-sub.zip
cd ../sigma-mem
git archive --format=zip --prefix=sigma-system-overview/sigma-mem/ HEAD -o /tmp/sm-sub.zip
cd ..

# Merge zips
python3 -c "
import zipfile, sys, os

# Start with main archive
with zipfile.ZipFile('/tmp/${OUTFILE}', 'a') as main_zip:
    for sub_zip_path in ['/tmp/ha-sub.zip', '/tmp/sm-sub.zip']:
        with zipfile.ZipFile(sub_zip_path, 'r') as sub_zip:
            for item in sub_zip.namelist():
                if item not in main_zip.namelist():
                    main_zip.writestr(item, sub_zip.read(item))

print('  Merged submodule archives')
"

# Move to current directory
mv "/tmp/${OUTFILE}" "${SCRIPT_DIR}/${OUTFILE}"
rm -f /tmp/ha-sub.zip /tmp/sm-sub.zip

# Verify the zip
echo "Verifying ${OUTFILE}..."
CRITICAL_FILES=(
    "sigma-system-overview/hateoas-agent/src/hateoas_agent/__init__.py"
    "sigma-system-overview/hateoas-agent/src/hateoas_agent/errors.py"
    "sigma-system-overview/hateoas-agent/src/hateoas_agent/validation.py"
    "sigma-system-overview/hateoas-agent/src/hateoas_agent/mcp_server.py"
    "sigma-system-overview/sigma-mem/src/sigma_mem/__init__.py"
    "sigma-system-overview/sigma-mem/src/sigma_mem/handlers.py"
    "sigma-system-overview/setup.sh"
    "sigma-system-overview/SETUP.md"
)

MISSING=0
for f in "${CRITICAL_FILES[@]}"; do
    if ! unzip -l "${OUTFILE}" "$f" > /dev/null 2>&1; then
        echo "  MISSING: $f"
        MISSING=$((MISSING + 1))
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo "ERROR: ${MISSING} critical files missing from zip"
    exit 1
fi

SIZE=$(du -h "${OUTFILE}" | awk '{print $1}')
echo ""
echo "Created: ${OUTFILE} (${SIZE})"
echo "Share this file — recipient runs: unzip ${OUTFILE} && cd sigma-system-overview && ./setup.sh"
