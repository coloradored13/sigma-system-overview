#!/usr/bin/env bash
# Validates that documentation stats match actual code
# Reports mismatches — does not fix them

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

ERRORS=0
WARNINGS=0

pass() { echo "  PASS: $1"; }
fail() { echo "  FAIL: $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "  WARN: $1"; WARNINGS=$((WARNINGS + 1)); }

echo "=== Sigma System Doc Validation ==="
echo ""

# --- hateoas-agent ---
echo "-- hateoas-agent --"

if [ -d "hateoas-agent/src" ]; then
  HA_LOC=$(find hateoas-agent/src -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  HA_TEST_LOC=$(find hateoas-agent/tests -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  HA_TESTS=$(cd hateoas-agent && python3 -m pytest tests/ --co -q 2>/dev/null | tail -1 | grep -oE '[0-9]+' | head -1) || HA_TESTS="?"

  echo "  Actual: src=${HA_LOC} LOC, tests=${HA_TEST_LOC} LOC, test_count=${HA_TESTS}"

  # Check README claims
  README_HA_LOC=$(grep -oP 'hateoas-agent.*?(\d[\d,]+)\s*LOC' README.md | head -1 | grep -oE '[0-9,]+' | head -1 | tr -d ',') || README_HA_LOC=""
  ARCH_HA_LOC=$(grep -oP 'hateoas-agent.*?(\d[\d,]+)' ARCHITECTURE.md | head -1 | grep -oE '[0-9,]+' | head -1 | tr -d ',') || ARCH_HA_LOC=""

  # README stats table
  README_TABLE_HA=$(grep 'hateoas-agent' README.md | grep '|' | head -1) || README_TABLE_HA=""
  if [ -n "$README_TABLE_HA" ]; then
    R_SRC=$(echo "$README_TABLE_HA" | awk -F'|' '{print $3}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    R_TESTS=$(echo "$README_TABLE_HA" | awk -F'|' '{print $5}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    echo "  README table claims: src=${R_SRC} LOC, test_count=${R_TESTS}"

    # Compare with tolerance (within 10%)
    if [ -n "$R_SRC" ] && [ -n "$HA_LOC" ]; then
      DIFF=$(( HA_LOC - R_SRC ))
      ABS_DIFF=${DIFF#-}
      THRESHOLD=$(( R_SRC / 10 ))
      if [ "$ABS_DIFF" -gt "$THRESHOLD" ]; then
        fail "hateoas-agent src LOC: actual=${HA_LOC} vs README=${R_SRC} (diff=${DIFF})"
      else
        pass "hateoas-agent src LOC within tolerance (actual=${HA_LOC}, claimed=${R_SRC})"
      fi
    fi

    if [ -n "$R_TESTS" ] && [ "$HA_TESTS" != "?" ]; then
      if [ "$R_TESTS" != "$HA_TESTS" ]; then
        fail "hateoas-agent test count: actual=${HA_TESTS} vs README=${R_TESTS}"
      else
        pass "hateoas-agent test count matches (${HA_TESTS})"
      fi
    fi
  fi

  # ARCHITECTURE stats table
  ARCH_TABLE_HA=$(grep 'hateoas-agent' ARCHITECTURE.md | grep '|' | head -1) || ARCH_TABLE_HA=""
  if [ -n "$ARCH_TABLE_HA" ]; then
    A_SRC=$(echo "$ARCH_TABLE_HA" | awk -F'|' '{print $3}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    A_TESTS=$(echo "$ARCH_TABLE_HA" | awk -F'|' '{print $5}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    echo "  ARCHITECTURE table claims: src=${A_SRC} LOC, test_count=${A_TESTS}"

    if [ -n "$A_SRC" ] && [ -n "$HA_LOC" ]; then
      DIFF=$(( HA_LOC - A_SRC ))
      ABS_DIFF=${DIFF#-}
      THRESHOLD=$(( A_SRC / 10 ))
      if [ "$ABS_DIFF" -gt "$THRESHOLD" ]; then
        fail "hateoas-agent src LOC: actual=${HA_LOC} vs ARCHITECTURE=${A_SRC} (diff=${DIFF})"
      else
        pass "hateoas-agent src LOC in ARCHITECTURE within tolerance (actual=${HA_LOC}, claimed=${A_SRC})"
      fi
    fi

    if [ -n "$A_TESTS" ] && [ "$HA_TESTS" != "?" ]; then
      if [ "$A_TESTS" != "$HA_TESTS" ]; then
        fail "hateoas-agent test count: actual=${HA_TESTS} vs ARCHITECTURE=${A_TESTS}"
      else
        pass "hateoas-agent test count in ARCHITECTURE matches (${HA_TESTS})"
      fi
    fi
  fi
else
  warn "hateoas-agent/src not found (submodule not initialized?)"
fi

echo ""

# --- sigma-mem ---
echo "-- sigma-mem --"

if [ -d "sigma-mem/src" ]; then
  SM_LOC=$(find sigma-mem/src -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  SM_TEST_LOC=$(find sigma-mem/tests -name "*.py" | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
  SM_TESTS=$(cd sigma-mem && PYTHONPATH=src python3 -m pytest tests/ --co -q 2>/dev/null | tail -1 | grep -oE '[0-9]+' | head -1) || SM_TESTS="?"

  echo "  Actual: src=${SM_LOC} LOC, tests=${SM_TEST_LOC} LOC, test_count=${SM_TESTS}"

  # README stats table
  README_TABLE_SM=$(grep 'sigma-mem' README.md | grep '|' | head -1) || README_TABLE_SM=""
  if [ -n "$README_TABLE_SM" ]; then
    R_SRC=$(echo "$README_TABLE_SM" | awk -F'|' '{print $3}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    R_TESTS=$(echo "$README_TABLE_SM" | awk -F'|' '{print $5}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    echo "  README table claims: src=${R_SRC} LOC, test_count=${R_TESTS}"

    if [ -n "$R_SRC" ] && [ -n "$SM_LOC" ]; then
      DIFF=$(( SM_LOC - R_SRC ))
      ABS_DIFF=${DIFF#-}
      THRESHOLD=$(( R_SRC / 10 ))
      if [ "$ABS_DIFF" -gt "$THRESHOLD" ]; then
        fail "sigma-mem src LOC: actual=${SM_LOC} vs README=${R_SRC} (diff=${DIFF})"
      else
        pass "sigma-mem src LOC within tolerance (actual=${SM_LOC}, claimed=${R_SRC})"
      fi
    fi

    if [ -n "$R_TESTS" ] && [ "$SM_TESTS" != "?" ]; then
      if [ "$R_TESTS" != "$SM_TESTS" ]; then
        fail "sigma-mem test count: actual=${SM_TESTS} vs README=${R_TESTS}"
      else
        pass "sigma-mem test count matches (${SM_TESTS})"
      fi
    fi
  fi

  # ARCHITECTURE stats table
  ARCH_TABLE_SM=$(grep 'sigma-mem' ARCHITECTURE.md | grep '|' | head -1) || ARCH_TABLE_SM=""
  if [ -n "$ARCH_TABLE_SM" ]; then
    A_SRC=$(echo "$ARCH_TABLE_SM" | awk -F'|' '{print $3}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    A_TESTS=$(echo "$ARCH_TABLE_SM" | awk -F'|' '{print $5}' | grep -oE '[0-9,]+' | head -1 | tr -d ',')
    echo "  ARCHITECTURE table claims: src=${A_SRC} LOC, test_count=${A_TESTS}"

    if [ -n "$A_SRC" ] && [ -n "$SM_LOC" ]; then
      DIFF=$(( SM_LOC - A_SRC ))
      ABS_DIFF=${DIFF#-}
      THRESHOLD=$(( A_SRC / 10 ))
      if [ "$ABS_DIFF" -gt "$THRESHOLD" ]; then
        fail "sigma-mem src LOC: actual=${SM_LOC} vs ARCHITECTURE=${A_SRC} (diff=${DIFF})"
      else
        pass "sigma-mem src LOC in ARCHITECTURE within tolerance (actual=${SM_LOC}, claimed=${A_SRC})"
      fi
    fi

    if [ -n "$A_TESTS" ] && [ "$SM_TESTS" != "?" ]; then
      if [ "$A_TESTS" != "$SM_TESTS" ]; then
        fail "sigma-mem test count: actual=${SM_TESTS} vs ARCHITECTURE=${A_TESTS}"
      else
        pass "sigma-mem test count in ARCHITECTURE matches (${SM_TESTS})"
      fi
    fi
  fi
else
  warn "sigma-mem/src not found (submodule not initialized?)"
fi

echo ""

# --- Cross-doc consistency (README vs ARCHITECTURE) ---
echo "-- Cross-doc consistency --"

README_TOTAL=$(grep -i 'total' README.md | grep '|' | head -1) || README_TOTAL=""
ARCH_TOTAL=$(grep -i 'total' ARCHITECTURE.md | grep '|' | head -1) || ARCH_TOTAL=""

if [ -n "$README_TOTAL" ] && [ -n "$ARCH_TOTAL" ]; then
  RT_LOC=$(echo "$README_TOTAL" | grep -oE '[0-9,]+' | head -1 | tr -d ',')
  AT_LOC=$(echo "$ARCH_TOTAL" | grep -oE '[0-9,]+' | head -1 | tr -d ',')
  RT_TESTS=$(echo "$README_TOTAL" | grep -oE '[0-9,]+' | tail -1 | tr -d ',')
  AT_TESTS=$(echo "$ARCH_TOTAL" | grep -oE '[0-9,]+' | tail -1 | tr -d ',')

  if [ "$RT_LOC" != "$AT_LOC" ]; then
    fail "Total LOC mismatch: README=${RT_LOC} vs ARCHITECTURE=${AT_LOC}"
  else
    pass "Total LOC consistent across README and ARCHITECTURE (${RT_LOC})"
  fi

  if [ "$RT_TESTS" != "$AT_TESTS" ]; then
    fail "Total test count mismatch: README=${RT_TESTS} vs ARCHITECTURE=${AT_TESTS}"
  else
    pass "Total test count consistent across README and ARCHITECTURE (${RT_TESTS})"
  fi
else
  warn "Could not find totals row in one or both docs"
fi

echo ""
echo "=== Results ==="
echo "  Errors: ${ERRORS}"
echo "  Warnings: ${WARNINGS}"

if [ "$ERRORS" -gt 0 ]; then
  echo "  Status: FAIL — doc stats are out of date"
  exit 1
else
  echo "  Status: PASS"
  exit 0
fi
