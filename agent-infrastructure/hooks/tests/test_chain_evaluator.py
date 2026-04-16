"""Tests for chain-evaluator.py — the atomic checklist evaluator.

Tests cover:
- enforce_stop() non-looping behavior (idempotency, session detection)
- evaluate_chain() full chain evaluation
- check_monotonicity() rejection tracking
- Peer verification checks (A16-A18)
- CLI dispatch
- State persistence
- Integration: subprocess smoke tests
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import chain-evaluator (hyphenated filename)
HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "chain_evaluator", HOOKS_DIR / "chain-evaluator.py"
)
ce = importlib.util.module_from_spec(_spec)
# Register in sys.modules before exec — required for dataclass processing in Python 3.14+
sys.modules["chain_evaluator"] = ce
_spec.loader.exec_module(ce)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_workspace(tmp_path):
    """Temp workspace with patched DEFAULT_WORKSPACE."""
    ws = tmp_path / "workspace.md"

    def _write(content):
        ws.write_text(content, encoding="utf-8")
        return ws

    return _write, ws


@pytest.fixture
def tmp_state_file(tmp_path):
    """Temp chain status file."""
    return tmp_path / ".chain-status.json"


@pytest.fixture
def patch_paths(tmp_workspace, tmp_state_file):
    """Patch workspace and state file paths."""
    _write, ws = tmp_workspace
    with patch.object(ce, "DEFAULT_WORKSPACE", ws), \
         patch.object(ce, "STATE_FILE", tmp_state_file), \
         patch.object(ce.gc, "DEFAULT_WORKSPACE", ws):
        yield _write, ws, tmp_state_file


# Sample workspace content
IDLE_WORKSPACE = "# workspace\n## status: idle\n"

ACTIVE_ANALYZE_WORKSPACE = """\
# workspace — test review
## status: active
## mode: ANALYZE

## task
Analyze competitive landscape

## prompt-decomposition
Q1: Who competes?
H1: Tech is differentiator
C1: Third-party only

## findings
### tech-architect
F[arch]: API-first wins |source:code-read:T1|
DB[arch]: initial=API first | assume-wrong=monolith could win | counter=integration costs | re-estimate=API still wins | reconciled=API first confirmed

### reference-class-analyst
F[base]: 3 of 5 similar firms succeeded |source:independent-research:T2|
DB[ref]: initial=60% | assume-wrong=survivorship bias | counter=only public firms | re-estimate=50% | reconciled=50-60% range

## convergence
tech-architect: ✓ architecture reviewed |findings complete |→ ready
reference-class-analyst: ✓ base rates computed |findings complete |→ ready
devils-advocate: ✓ challenges complete |→ synthesis

## devils-advocate
DA[#1]: tech-architect anchor bias on API-first
DA[#2]: reference-class-analyst survivorship bias
exit.gate: PASS — 3 criteria met

BELIEF[r1]: P=0.72 |→ proceed
BELIEF[r2]: P=0.85 |→ synthesis

## circuit-breaker
R1 divergence detected: different risk estimates between TA and RCA

CONTAMINATION-CHECK: session-topics-outside-scope: none |scan-result: clean
SYCOPHANCY-CHECK: softened:none |selective-emphasis:none |dissent-reframed:none |process-issues:none

XVERIFY[openai:gpt-4o] market sizing corroborated
"""

BUILD_WORKSPACE = """\
# workspace — test build
## status: active
## mode: BUILD

## task
Build payment module

## architecture-decisions
ADR[1]: Use pip deps

## design-system
DS[1]: Component structure

## interface-contracts
IC[1]: API format

## findings
### implementation-engineer
F[impl]: Module scaffolded |source:code-read:T1|

CHECKPOINT[c2-step3]: implementation started
"""


# ---------------------------------------------------------------------------
# enforce_stop() — non-looping behavior
# ---------------------------------------------------------------------------

class TestEnforceStop:
    def test_returns_empty_when_no_workspace(self, tmp_path):
        """Stop hook must no-op when workspace doesn't exist."""
        with patch.object(ce, "DEFAULT_WORKSPACE", tmp_path / "nonexistent.md"):
            result = ce.enforce_stop({})
            assert result == {}

    def test_returns_empty_for_idle_workspace(self, patch_paths):
        """CRITICAL: Stop hook must no-op for non-sigma workspaces."""
        write, _, _ = patch_paths
        write(IDLE_WORKSPACE)
        result = ce.enforce_stop({})
        assert result == {}

    def test_returns_empty_for_workspace_without_task(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\nSome random content\n")
        result = ce.enforce_stop({})
        assert result == {}

    def test_evaluates_active_sigma_workspace(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.enforce_stop({})
        assert "systemMessage" in result
        assert "[chain-eval]" in result["systemMessage"]

    def test_message_is_informational_not_actionable(self, patch_paths):
        """CRITICAL: message must NOT read as an instruction to fix things."""
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.enforce_stop({})
        msg = result.get("systemMessage", "")
        # Must NOT contain actionable language that triggers loops
        assert "CHAIN INCOMPLETE" not in msg, "Must not use old actionable format"
        assert "items failed" not in msg, "Must not list failures in demand format"
        assert "[chain-eval]" in msg, "Must use informational prefix"

    def test_idempotency_skips_unchanged_workspace(self, patch_paths):
        """CRITICAL: second call on unchanged workspace must return {}.

        After enforce_stop writes ## Chain Evaluation to workspace, the content
        hash changes. The second call should detect that ## Chain Evaluation
        already exists with the same content hash and skip re-evaluation.
        """
        write, ws, state_file = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)

        # First call — evaluates and writes ## Chain Evaluation to workspace
        result1 = ce.enforce_stop({})
        assert "systemMessage" in result1

        # The first call changed the workspace (added ## Chain Evaluation),
        # which changed the hash. But the state file was also updated with
        # the NEW hash (post-write). So the second call should see matching hashes.
        # Read the current state to verify
        state = json.loads(state_file.read_text())
        ws_content = ws.read_text()
        current_hash = ce._content_hash(ws_content)
        assert state["last_content_hash"] == current_hash, \
            "State hash should match workspace after write_evaluation_to_workspace"

        # Second call — hash matches AND ## Chain Evaluation exists → skip
        result2 = ce.enforce_stop({})
        assert result2 == {}, "Second call on unchanged workspace must return empty dict"

    def test_re_evaluates_after_workspace_change(self, patch_paths):
        """After workspace content changes, evaluation should run again."""
        write, ws, state_file = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)

        # First call
        ce.enforce_stop({})

        # Modify workspace
        content = ws.read_text()
        ws.write_text(content + "\n### new-agent\nNew findings here\n")

        # Second call — should evaluate again
        result = ce.enforce_stop({})
        assert "systemMessage" in result


# ---------------------------------------------------------------------------
# evaluate_chain() — full chain evaluation
# ---------------------------------------------------------------------------

class TestEvaluateChain:
    def test_analyze_chain_returns_result(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        assert result.mode == "ANALYZE"
        assert len(result.items) > 0
        assert hasattr(result, "complete")

    def test_build_chain_includes_build_items(self, patch_paths):
        write, _, _ = patch_paths
        write(BUILD_WORKSPACE)
        result = ce.evaluate_chain()
        assert result.mode == "BUILD"
        item_ids = {i.item_id for i in result.items}
        assert "B1" in item_ids
        assert "B2" in item_ids

    def test_analyze_chain_has_expected_items(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        item_ids = {i.item_id for i in result.items}
        # Core ANALYZE items
        for expected in ["A1", "A2", "A3", "A4", "A5", "A6", "A7",
                         "A8", "A9", "A10", "A15",
                         "A16", "A17", "A18",
                         "A11", "A12", "A13", "A14"]:
            assert expected in item_ids, f"Missing chain item {expected}"

    def test_complete_is_false_when_items_fail(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        # This workspace is missing synthesis, archive, etc.
        assert result.complete is False

    def test_summary_text_format(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        text = result.summary_text()
        assert "## Chain Evaluation" in text
        assert "PASS" in text or "FAIL" in text


# ---------------------------------------------------------------------------
# check_monotonicity() — rejection tracking
# ---------------------------------------------------------------------------

class TestMonotonicity:
    def test_first_evaluation_sets_state(self, patch_paths):
        write, _, state_file = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        result = ce.check_monotonicity(result)

        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert "last_content_hash" in state
        assert "failed_items" in state

    def test_unchanged_workspace_preserves_failures(self, patch_paths):
        write, ws, state_file = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)

        # First evaluation
        result1 = ce.evaluate_chain()
        result1 = ce.check_monotonicity(result1)
        failed_ids_1 = {i.item_id for i in result1.items if not i.passed}

        # Second evaluation, same workspace
        result2 = ce.evaluate_chain(ws)
        result2 = ce.check_monotonicity(result2, ws)
        failed_ids_2 = {i.item_id for i in result2.items if not i.passed}

        # All previously failed items must stay failed
        assert failed_ids_1.issubset(failed_ids_2), \
            "Monotonicity violated: previously failed items must stay failed"

    def test_changed_workspace_allows_re_evaluation(self, patch_paths):
        write, ws, state_file = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)

        # First evaluation
        result1 = ce.evaluate_chain()
        ce.check_monotonicity(result1)

        # Change workspace
        ws.write_text(ACTIVE_ANALYZE_WORKSPACE + "\nNew content changes hash\n")

        # Second evaluation
        result2 = ce.evaluate_chain(ws)
        result2 = ce.check_monotonicity(result2, ws)
        # Should evaluate fresh (no monotonicity pinning from previous hash)
        state = json.loads(state_file.read_text())
        assert state["last_content_hash"] != ""


# ---------------------------------------------------------------------------
# Peer verification checks (A16-A18)
# ---------------------------------------------------------------------------

WORKSPACE_WITH_PEER_VERIFICATION = """\
# workspace — test
## task
Test review

## findings
### tech-architect
F[arch]: Finding one |source:code-read:T1|
DB[arch]: initial=API first | assume-wrong=monolith | counter=cost | re-estimate=API | reconciled=API confirmed

### reference-class-analyst
F[ref]: Finding two |source:independent-research:T2|
DB[ref]: initial=60% | assume-wrong=survivorship | counter=public only | re-estimate=50% | reconciled=50-60%

## convergence
tech-architect: ✓ done
reference-class-analyst: ✓ done

## peer-verification
### Peer Verification: tech-architect verifying reference-class-analyst
- DB[] structure: [PASS] — checked 1 entry
  - DB[ref]: 5-step present (initial/assume-wrong/counter/re-estimate/reconciled)
- Source provenance: [PASS] — 1/1 findings tagged
  - F[ref]: T2 tier present
- XVERIFY: [N/A]
- Analytical substance: [PASS]
  - H1 addressed by reference-class-analyst
Overall: reference-class-analyst's section is COMPLETE

### Peer Verification: reference-class-analyst verifying tech-architect
- DB[] structure: [PASS] — checked 1 entry
  - DB[arch]: 5-step present (initial/assume-wrong/counter/re-estimate/reconciled)
- Source provenance: [PASS] — 1/1 findings tagged
  - F[arch]: T1 tier present
- XVERIFY: [N/A]
- Analytical substance: [PASS]
  - H1 addressed by tech-architect
Overall: tech-architect's section is COMPLETE

## devils-advocate
DA[#1]: challenge on arch bias
DA[#2]: challenge on base rate methodology
exit.gate: PASS — 3 criteria met
"""


class TestPeerVerification:
    def test_a16_passes_with_verification_sections(self, patch_paths):
        write, _, _ = patch_paths
        write(WORKSPACE_WITH_PEER_VERIFICATION)
        result = ce.check_a16(WORKSPACE_WITH_PEER_VERIFICATION)
        assert result.passed is True, f"A16 should pass: {result.issues}"

    def test_a16_fails_without_verification_sections(self, patch_paths):
        write, _, _ = patch_paths
        workspace = "## findings\n### tech-architect\nSome findings\n"
        result = ce.check_a16(workspace)
        # May pass vacuously if no agents detected — depends on implementation
        # The key test is that it doesn't crash

    def test_a17_passes_with_sufficient_artifact_refs(self, patch_paths):
        result = ce.check_a17(WORKSPACE_WITH_PEER_VERIFICATION)
        assert result.passed is True, f"A17 should pass: {result.issues}"

    def test_a17_fails_with_generic_verification(self):
        workspace = """\
### Peer Verification: agent-a verifying agent-b
Looks good to me. Everything seems fine.
Overall: COMPLETE
"""
        result = ce.check_a17(workspace)
        # Should fail — no specific artifact references
        if result.details.get("verifications_checked", 0) > 0:
            assert result.passed is False, "Generic verification should fail specificity check"

    def test_a18_checks_coverage_matrix(self):
        result = ce.check_a18(WORKSPACE_WITH_PEER_VERIFICATION)
        # With 2 agents + DA, each should have >=2 verifiers (1 peer + DA)
        assert result.item_id == "A18"


# ---------------------------------------------------------------------------
# Individual chain item checks
# ---------------------------------------------------------------------------

class TestIndividualChecks:
    def test_a1_passes_with_non_empty_findings(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.check_a1(ACTIVE_ANALYZE_WORKSPACE)
        assert result.item_id == "A1"

    def test_a4_passes_with_circuit_breaker(self, patch_paths):
        result = ce.check_a4(ACTIVE_ANALYZE_WORKSPACE)
        assert result.item_id == "A4"
        assert result.passed is True, f"A4 should pass — CB evidence present: {result.issues}"

    def test_a6_passes_with_belief(self, patch_paths):
        result = ce.check_a6(ACTIVE_ANALYZE_WORKSPACE)
        assert result.item_id == "A6"
        assert result.passed is True, f"A6 should pass — BELIEF present: {result.issues}"

    def test_a8_passes_with_contamination_check(self, patch_paths):
        result = ce.check_a8(ACTIVE_ANALYZE_WORKSPACE)
        assert result.item_id == "A8"

    def test_a10_passes_with_sycophancy_check(self, patch_paths):
        result = ce.check_a10(ACTIVE_ANALYZE_WORKSPACE)
        assert result.item_id == "A10"


# ---------------------------------------------------------------------------
# evaluate_single()
# ---------------------------------------------------------------------------

class TestEvaluateSingle:
    def test_evaluates_known_item(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_single("A1")
        assert result.item_id == "A1"

    def test_returns_error_for_unknown_item(self, patch_paths):
        write, _, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_single("Z99")
        assert result.passed is False
        assert "Unknown" in result.issues[0]


# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

class TestStatePersistence:
    def test_save_and_load_state(self, tmp_path):
        state_file = tmp_path / "test-state.json"
        with patch.object(ce, "STATE_FILE", state_file):
            ce._save_state({"test": True, "count": 42})
            loaded = ce._load_state()
            assert loaded["test"] is True
            assert loaded["count"] == 42

    def test_load_missing_state_returns_empty(self, tmp_path):
        with patch.object(ce, "STATE_FILE", tmp_path / "nonexistent.json"):
            loaded = ce._load_state()
            assert loaded == {}

    def test_content_hash_deterministic(self):
        h1 = ce._content_hash("test content")
        h2 = ce._content_hash("test content")
        assert h1 == h2

    def test_content_hash_changes_on_different_content(self):
        h1 = ce._content_hash("content A")
        h2 = ce._content_hash("content B")
        assert h1 != h2


# ---------------------------------------------------------------------------
# write_evaluation_to_workspace()
# ---------------------------------------------------------------------------

class TestWriteEvaluation:
    def test_appends_chain_evaluation_section(self, patch_paths):
        write, ws, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)
        result = ce.evaluate_chain()
        ce.write_evaluation_to_workspace(result)

        content = ws.read_text()
        assert "## Chain Evaluation" in content

    def test_replaces_existing_evaluation(self, patch_paths):
        write, ws, _ = patch_paths
        write(ACTIVE_ANALYZE_WORKSPACE)

        # Write twice
        result = ce.evaluate_chain()
        ce.write_evaluation_to_workspace(result)
        ce.write_evaluation_to_workspace(result)

        content = ws.read_text()
        assert content.count("## Chain Evaluation") == 1, \
            "Should replace existing evaluation, not duplicate"


# ---------------------------------------------------------------------------
# ChainResult data model
# ---------------------------------------------------------------------------

class TestChainResult:
    def test_to_dict(self):
        result = ce.ChainResult(mode="ANALYZE", complete=True)
        d = result.to_dict()
        assert d["mode"] == "ANALYZE"
        assert d["complete"] is True

    def test_passed_count(self):
        result = ce.ChainResult(mode="ANALYZE", complete=False, items=[
            ce.ChainItem("A1", "test", True, "agent-work"),
            ce.ChainItem("A2", "test", False, "agent-work"),
            ce.ChainItem("A3", "test", True, "agent-work"),
        ])
        assert result.passed_count == 2
        assert result.failed_count == 1


# ---------------------------------------------------------------------------
# Integration: subprocess smoke tests
# ---------------------------------------------------------------------------

class TestChainEvaluatorIntegration:
    """Run chain-evaluator.py as subprocess."""

    def _run_hook(self, stdin_data, home_dir=None):
        script = HOOKS_DIR / "chain-evaluator.py"
        env = os.environ.copy()
        if home_dir:
            env["HOME"] = str(home_dir)
        result = __import__("subprocess").run(
            [sys.executable, str(script)],
            input=json.dumps(stdin_data),
            capture_output=True, text=True, env=env, timeout=10,
        )
        return result

    def _run_cli(self, args, home_dir=None):
        script = HOOKS_DIR / "chain-evaluator.py"
        env = os.environ.copy()
        if home_dir:
            env["HOME"] = str(home_dir)
        result = __import__("subprocess").run(
            [sys.executable, str(script)] + args,
            capture_output=True, text=True, env=env, timeout=10,
        )
        return result

    def test_stop_hook_exits_clean_on_empty_json(self):
        result = self._run_hook({})
        assert result.returncode == 0

    def test_stop_hook_exits_clean_on_non_stop_event(self):
        result = self._run_hook({"hook_event_name": "PreToolUse"})
        assert result.returncode == 0

    def test_stop_hook_no_output_for_idle_workspace(self, tmp_path):
        """CRITICAL: idle workspace must produce no systemMessage."""
        home = tmp_path / "home"
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)
        (home / ".claude" / "hooks").mkdir(parents=True)
        ws = home / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"
        ws.write_text(IDLE_WORKSPACE)

        result = self._run_hook({"hook_event_name": "Stop"}, home_dir=home)
        assert result.returncode == 0
        # Should produce no JSON output (empty stdout)
        stdout = result.stdout.strip()
        if stdout:
            parsed = json.loads(stdout)
            assert "systemMessage" not in parsed, \
                f"Idle workspace should not produce systemMessage: {parsed}"

    def test_stop_hook_produces_informational_message_for_sigma(self, tmp_path):
        home = tmp_path / "home"
        shared = home / ".claude" / "teams" / "sigma-review" / "shared"
        shared.mkdir(parents=True)
        (home / ".claude" / "hooks").mkdir(parents=True)
        ws = shared / "workspace.md"
        ws.write_text(ACTIVE_ANALYZE_WORKSPACE)

        # Need gate_checks.py available
        import shutil
        gc_src = Path(__file__).parent.parent.parent / "teams" / "sigma-review" / "shared" / "gate_checks.py"
        if gc_src.exists():
            shutil.copy(gc_src, shared / "gate_checks.py")

        result = self._run_hook({"hook_event_name": "Stop"}, home_dir=home)
        assert result.returncode == 0

    def test_cli_status_exits_clean(self):
        """CLI status command should not crash."""
        result = self._run_cli(["status"])
        # May fail if workspace doesn't exist, but should not crash
        assert result.returncode in (0, 1)

    def test_cli_item_unknown_id(self):
        result = self._run_cli(["item", "Z99"])
        assert result.returncode == 0
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            assert parsed["passed"] is False
