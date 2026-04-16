"""Tests for sigma-review hook and gate infrastructure.

Covers the failures discovered in R18 (2026-04-16):
- chain-evaluator CLI routing (Fix 2)
- pre-shutdown promotion gate (Fix 1)
- agent section parser (Fix 3)
- A14 circular dependency (Fix 4)
- silent failure detection
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

HOOKS_DIR = Path(__file__).resolve().parent
PHASE_GATE = HOOKS_DIR / "phase-gate.py"
CHAIN_EVALUATOR = HOOKS_DIR / "chain-evaluator.py"
GATE_CHECKS = HOOKS_DIR.parent / "teams/sigma-review/shared/gate_checks.py"
CHAIN_STATUS = HOOKS_DIR / ".chain-status.json"

# Add gate_checks to path for direct import
sys.path.insert(0, str(GATE_CHECKS.parent))
import gate_checks as gc


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_WORKSPACE = """# workspace

## status: active
## mode: ANALYZE
## date: 2026-04-16

## task
Test review

## scope-boundary
IS about: testing
NOT about: nothing

## prompt-decomposition

### questions
Q1: test question

### prompt-hypotheses (test)
H1: test hypothesis

### constraints
C1: test constraint

## infrastructure
ΣVerify: unavailable

## agents

### tech-architect

#### findings
F[TA-1] |T2-corroborated |test finding |source:independent-research|
DB[TA-1]: (1) initial: test (2) assume-wrong: test (3) strongest-counter: test (4) re-estimate: test (5) reconciled: test

### product-strategist

#### findings
F[PS-1] |T2-corroborated |test finding |source:independent-research|
DB[PS-1]: (1) initial: test (2) assume-wrong: test (3) strongest-counter: test (4) re-estimate: test (5) reconciled: test

### devils-advocate

#### DA challenges
DA[#1]: test challenge |target: tech-architect:F[TA-1] |type: crowding
exit-gate: PASS |engagement:B |unresolved:none |untested-consensus:none |hygiene:pass |prompt-contamination:pass |cqot:pass |xverify:not-attempted

## convergence
tech-architect: ✓ test
product-strategist: ✓ test
devils-advocate: ✓ test

## belief-state
BELIEF[r1]: P=0.85 |prior=0.5

## circuit-breaker
R1 divergence detected: test

## da-challenges
DA[#1]: test

## exit-gate
exit-gate: PASS |engagement:B

## contamination-check
CONTAMINATION-CHECK: session-topics-outside-scope: none |scan-result: clean

## sycophancy-check
SYCOPHANCY-CHECK: softened:none |selective-emphasis:none

## peer-verification
tech-architect verified product-strategist ✓

## promotion
auto-promote: tech-architect: test pattern |class:pattern
user-approve: product-strategist: test pattern |class:pattern |reason:generalizable
"""

WORKSPACE_NO_PROMOTION = MINIMAL_WORKSPACE.replace(
    "## promotion\nauto-promote: tech-architect: test pattern |class:pattern\nuser-approve: product-strategist: test pattern |class:pattern |reason:generalizable\n",
    "## promotion\n\n"
)

WORKSPACE_NO_CHECKS = MINIMAL_WORKSPACE.replace(
    "## contamination-check\nCONTAMINATION-CHECK: session-topics-outside-scope: none |scan-result: clean",
    "## contamination-check\n"
).replace(
    "## sycophancy-check\nSYNCOPHANCY-CHECK: softened:none |selective-emphasis:none",
    "## sycophancy-check\n"
)


# ---------------------------------------------------------------------------
# Fix 2: Chain evaluator CLI routing
# ---------------------------------------------------------------------------

class TestChainEvaluatorCLI:
    """Tests that chain-evaluator.py correctly routes CLI vs hook invocations."""

    def test_evaluate_produces_output(self):
        """CLI 'evaluate' command must produce JSON output, not exit silently."""
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR), "evaluate"],
            capture_output=True, text=True, timeout=15,
        )
        assert result.returncode == 0, f"evaluate failed: {result.stderr}"
        assert result.stdout.strip(), "evaluate produced no output (silent exit bug)"
        data = json.loads(result.stdout)
        assert "complete" in data, "evaluate output missing 'complete' field"
        assert "items" in data, "evaluate output missing 'items' field"

    def test_status_produces_output(self):
        """CLI 'status' command must produce JSON output."""
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR), "status"],
            capture_output=True, text=True, timeout=15,
        )
        assert result.returncode == 0, f"status failed: {result.stderr}"
        assert result.stdout.strip(), "status produced no output"
        data = json.loads(result.stdout)
        assert "complete" in data
        assert "passed" in data

    def test_no_args_no_crash(self):
        """No args must not crash — either shows usage or exits cleanly.

        When stdin is piped (subprocess default), isatty()=False so it
        routes to hook mode with empty data → exits 0. When stdin is
        truly a tty, it shows usage and exits 1. Both are acceptable.
        The key invariant: it must NOT produce corrupt output or hang.
        """
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR)],
            capture_output=True, text=True, timeout=15,
            input="",  # Empty stdin, not valid JSON
        )
        assert result.returncode in (0, 1), f"Unexpected exit code: {result.returncode}"
        # Must not produce corrupt JSON output
        if result.stdout.strip():
            json.loads(result.stdout)  # Should parse cleanly or be empty

    def test_hook_mode_with_stop_event(self):
        """Piped JSON with Stop event → calls enforce_stop path."""
        hook_data = json.dumps({"hook_event_name": "Stop"})
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR)],
            input=hook_data, capture_output=True, text=True, timeout=15,
        )
        assert result.returncode == 0

    def test_cli_args_override_stdin(self):
        """CLI args must take priority over stdin detection."""
        hook_data = json.dumps({"hook_event_name": "Stop"})
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR), "status"],
            input=hook_data, capture_output=True, text=True, timeout=15,
        )
        assert result.returncode == 0
        # Should produce status output, not hook output
        data = json.loads(result.stdout)
        assert "complete" in data, "CLI args did not override stdin hook detection"


# ---------------------------------------------------------------------------
# Fix 1: Pre-shutdown promotion gate
# ---------------------------------------------------------------------------

class TestShutdownGate:
    """Tests that SendMessage shutdown_request is blocked without promotion."""

    def _run_phase_gate(self, tool_name: str, tool_input: dict) -> tuple[int, str]:
        """Run phase-gate.py with simulated PreToolUse data."""
        hook_data = json.dumps({
            "hook_event_name": "PreToolUse",
            "tool_name": tool_name,
            "tool_input": tool_input,
        })
        result = subprocess.run(
            [sys.executable, str(PHASE_GATE)],
            input=hook_data, capture_output=True, text=True, timeout=5,
        )
        return result.returncode, result.stdout

    def test_shutdown_blocked_without_promotion(self):
        """Shutdown request must be blocked when ## promotion is empty."""
        # This test requires an active sigma session with empty promotion
        # We test the function directly instead of the full hook
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        with patch.object(pg, '_is_sigma_session', return_value=True):
            with patch.object(pg, '_workspace_section_has_content') as mock_content:
                mock_content.return_value = False
                blocked, reason = pg.check_premature_shutdown({
                    "message": {"type": "shutdown_request"}
                })
                assert blocked, "Shutdown should be blocked when promotion is empty"
                assert "promotion" in reason.lower()

    def test_shutdown_allowed_with_promotion(self):
        """Shutdown request allowed when promotion + checks are populated."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        with patch.object(pg, '_is_sigma_session', return_value=True):
            with patch.object(pg, '_workspace_section_has_content', return_value=True):
                blocked, reason = pg.check_premature_shutdown({
                    "message": {"type": "shutdown_request"}
                })
                assert not blocked, f"Shutdown should be allowed: {reason}"

    def test_plain_text_messages_not_blocked(self):
        """Plain text SendMessage (not shutdown) must not be blocked."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        blocked, reason = pg.check_premature_shutdown({
            "message": "Hello, how are you doing?"
        })
        assert not blocked, "Plain text messages should never be blocked"

    def test_non_sigma_session_not_blocked(self):
        """Shutdown outside sigma session must not be blocked."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        with patch.object(pg, '_is_sigma_session', return_value=False):
            blocked, reason = pg.check_premature_shutdown({
                "message": {"type": "shutdown_request"}
            })
            assert not blocked, "Should not block outside sigma sessions"


# ---------------------------------------------------------------------------
# Fix 3: Agent section parser
# ---------------------------------------------------------------------------

class TestAgentParser:
    """Tests that workspace parser correctly identifies agent vs non-agent sections."""

    def test_hypotheses_not_extracted_as_agent(self):
        """### hypotheses must NOT be treated as an agent section."""
        content = """## agents

### tech-architect
some findings

### hypotheses
H1: test

### product-strategist
some findings

## convergence
"""
        agents = gc.extract_agents_from_workspace(content)
        assert "hypotheses" not in agents, "'hypotheses' incorrectly extracted as agent"

    def test_prompt_hypotheses_not_extracted(self):
        """### prompt-hypotheses must NOT be treated as an agent section."""
        content = """## agents

### tech-architect
some findings

### prompt-hypotheses
H1: test

## convergence
"""
        agents = gc.extract_agents_from_workspace(content)
        assert "prompt-hypotheses" not in agents

    def test_known_agents_extracted(self):
        """Known roster agents must be correctly extracted."""
        content = """## agents

### tech-architect
findings here

### product-strategist
findings here

## convergence
"""
        agents = gc.extract_agents_from_workspace(content)
        assert "tech-architect" in agents
        assert "product-strategist" in agents

    def test_agents_section_boundary(self):
        """Parser must find agent region using ## agents, not just ## findings."""
        content = """## prompt-decomposition

### hypotheses
H1: should not be extracted

## agents

### tech-architect
findings

## convergence
"""
        agents = gc.extract_agents_from_workspace(content)
        assert "tech-architect" in agents
        assert "hypotheses" not in agents

    def test_findings_region_uses_agents_header(self):
        """_get_findings_region must match ## agents header."""
        content = """## agents

### tech-architect
F[TA-1] test finding

## convergence
done
"""
        region = gc._get_findings_region(content)
        assert "F[TA-1]" in region
        assert "done" not in region


# ---------------------------------------------------------------------------
# Fix 4: A14 circular dependency
# ---------------------------------------------------------------------------

class TestA14CircularDependency:
    """Tests that git-commit-gate allows commit when only A14 (git clean) fails."""

    def test_a14_only_allows_commit(self):
        """Chain status with only A14 failing must allow git commit."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        status = {
            "last_complete": False,
            "failed_items": {"A14": "Uncommitted changes in repo: 5 files"}
        }

        with patch.object(pg, 'CHAIN_STATUS_FILE') as mock_file:
            mock_file.read_text.return_value = json.dumps(status)
            assert pg._chain_is_complete(), "Should allow commit when only A14 fails"

    def test_other_failures_still_block(self):
        """Chain status with non-A14 failures must still block."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        status = {
            "last_complete": False,
            "failed_items": {
                "A5": "DA issued 0 challenges",
                "A14": "Uncommitted changes"
            }
        }

        with patch.object(pg, 'CHAIN_STATUS_FILE') as mock_file:
            mock_file.read_text.return_value = json.dumps(status)
            assert not pg._chain_is_complete(), "Should block when non-A14 items also fail"

    def test_complete_chain_still_passes(self):
        """Chain status with last_complete=True must pass."""
        sys.path.insert(0, str(HOOKS_DIR))
        import importlib
        pg = importlib.import_module("phase-gate")

        status = {"last_complete": True, "failed_items": {}}

        with patch.object(pg, 'CHAIN_STATUS_FILE') as mock_file:
            mock_file.read_text.return_value = json.dumps(status)
            assert pg._chain_is_complete()


# ---------------------------------------------------------------------------
# Integration: chain evaluator produces correct results
# ---------------------------------------------------------------------------

class TestChainEvaluatorIntegration:
    """Integration tests using workspace content to verify chain evaluation."""

    def test_evaluate_updates_chain_status(self):
        """Running evaluate must update .chain-status.json."""
        result = subprocess.run(
            [sys.executable, str(CHAIN_EVALUATOR), "evaluate"],
            capture_output=True, text=True, timeout=15,
        )
        assert result.returncode == 0
        # Verify .chain-status.json was updated
        assert CHAIN_STATUS.exists(), ".chain-status.json not created"
        data = json.loads(CHAIN_STATUS.read_text())
        assert "last_complete" in data
        assert "last_evaluation" in data
        assert "failed_items" in data
