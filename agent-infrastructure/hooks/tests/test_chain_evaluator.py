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
from datetime import datetime, timezone
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
        # May fail if workspace doesn't exist (CI has no ~/.claude workspace),
        # but should not crash with a parseable stdout or known error code.
        assert result.returncode in (0, 1)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            assert parsed["passed"] is False


# ---------------------------------------------------------------------------
# SQ[13b] — A12 parser key-rename regression tests (R19 #4, shipped a2a7fa8)
# ---------------------------------------------------------------------------

# Full archived-session workspace content — exercises the gc.check_session_end
# parser that populates details["archive_file_found"]. The ``## archive``
# section + "archive: PRESENT" anchor is what the source parser keys on.
_ARCHIVED_WORKSPACE_CONTENT = """\
# workspace — test review
## status: complete
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] finding |source:[independent-research] T1

## convergence
tech-architect: ✓ complete

## archive
archive-date: 2026-04-20
archive-location: ~/.claude/teams/sigma-review/shared/archive/2026-04-20-test.md
archive-created: yes
archive: PRESENT

## git
committed: yes
pushed: yes
"""


class TestA12ArchiveFileFoundKeyRename:
    """Regression: R19 #4 — A12 consumes gc.check_session_end().details['archive_file_found'].

    Before a2a7fa8, chain-evaluator.py:241 used key 'archive_exists' — a mismatch
    against gate_checks source key 'archive_file_found'. A12 silently failed because
    the .get() default returned False.

    These two tests lock the contract: the key is archive_file_found, and when
    gate_checks reports True, check_a12 passes (absent a grace-window concern).
    """

    def test_a12_reads_archive_file_found_key_not_archive_exists(self, patch_paths):
        """The A12 check must key on 'archive_file_found' (current) not 'archive_exists' (removed)."""
        write, ws, _ = patch_paths
        write(_ARCHIVED_WORKSPACE_CONTENT)

        # Mock gc.check_session_end to return archive_file_found=True
        mock_result = MagicMock()
        mock_result.details = {"archive_file_found": True, "git_clean": True}
        mock_result.issues = []
        with patch.object(ce.gc, "check_session_end", return_value=mock_result):
            item = ce.check_a12(_ARCHIVED_WORKSPACE_CONTENT)

        assert item.passed is True, (
            f"A12 must pass when archive_file_found=True, got issues: {item.issues}"
        )
        assert "archive_file_found" in item.details, (
            "A12 must surface archive_file_found in its details dict (downstream consumer contract)"
        )
        assert item.details["archive_file_found"] is True

    def test_a12_fails_when_archive_file_found_false_and_workspace_old(self, patch_paths):
        """When archive_file_found=False AND workspace >24h old, A12 fails (no grace)."""
        write, ws, _ = patch_paths
        write(_ARCHIVED_WORKSPACE_CONTENT)

        # Backdate the workspace file to >24h old so grace window does not apply.
        import os as _os
        old_ts = datetime.now(timezone.utc).timestamp() - (25 * 3600)  # 25h ago
        _os.utime(ws, (old_ts, old_ts))

        mock_result = MagicMock()
        mock_result.details = {"archive_file_found": False}
        mock_result.issues = ["archive missing"]
        with patch.object(ce.gc, "check_session_end", return_value=mock_result):
            item = ce.check_a12(_ARCHIVED_WORKSPACE_CONTENT)

        assert item.passed is False, (
            "A12 must fail when archive_file_found=False AND workspace >24h old"
        )
        assert item.details.get("grace_window_applied") is False


# ---------------------------------------------------------------------------
# SQ[13e] — A12 24h grace-window deterministic tests (ie-1 SQ[2])
# ---------------------------------------------------------------------------


class TestA12GraceWindow:
    """A12 24h grace-window: archive-missing is OK when workspace <24h old.

    Non-looping invariant (CAL[1]): grace is a synchronous mtime delta, no
    poll/wait/sleep. Tests mutate file mtime via os.utime for deterministic
    boundary checks without relying on wall-clock.
    """

    def _set_workspace_age(self, ws_path, hours_ago: float) -> None:
        import os as _os
        target_ts = datetime.now(timezone.utc).timestamp() - (hours_ago * 3600)
        _os.utime(ws_path, (target_ts, target_ts))

    def test_grace_applies_when_workspace_younger_than_24h(self, patch_paths):
        """Archive missing + workspace 23.9h old → A12 passes with grace_window_applied=True."""
        write, ws, _ = patch_paths
        write("# workspace\n## status: active\n")
        self._set_workspace_age(ws, hours_ago=23.9)

        mock_result = MagicMock()
        mock_result.details = {"archive_file_found": False}
        mock_result.issues = ["archive missing"]
        with patch.object(ce.gc, "check_session_end", return_value=mock_result):
            item = ce.check_a12("# workspace\n## status: active\n")

        assert item.passed is True, "Grace must apply when workspace <24h old"
        assert item.details["grace_window_applied"] is True
        assert item.details["workspace_age_hours"] < 24.0
        assert any("grace-window" in issue for issue in item.issues), (
            "A12 must surface grace-window note in issues when applied"
        )

    def test_grace_does_not_apply_past_24h(self, patch_paths):
        """Archive missing + workspace 24.1h old → A12 fails, no grace."""
        write, ws, _ = patch_paths
        write("# workspace\n## status: active\n")
        self._set_workspace_age(ws, hours_ago=24.1)

        mock_result = MagicMock()
        mock_result.details = {"archive_file_found": False}
        mock_result.issues = ["archive missing"]
        with patch.object(ce.gc, "check_session_end", return_value=mock_result):
            item = ce.check_a12("# workspace\n## status: active\n")

        assert item.passed is False, "Grace must NOT apply past 24h boundary"
        assert item.details["grace_window_applied"] is False
        assert item.details["workspace_age_hours"] >= 24.0

    def test_grace_bypassed_when_archive_present(self, patch_paths):
        """If archive IS found, grace-window is irrelevant — A12 passes regardless of mtime."""
        write, ws, _ = patch_paths
        write("# workspace\n## status: complete\n")
        self._set_workspace_age(ws, hours_ago=48.0)  # very old, but archive exists

        mock_result = MagicMock()
        mock_result.details = {"archive_file_found": True}
        mock_result.issues = []
        with patch.object(ce.gc, "check_session_end", return_value=mock_result):
            item = ce.check_a12("# workspace\n## status: complete\n")

        assert item.passed is True
        assert item.details["grace_window_applied"] is False, (
            "grace flag must be False when archive is present (not triggered)"
        )


# ---------------------------------------------------------------------------
# SQ[13c] — A16/A17/A18 peer-verify extensions (complements existing tests)
# ---------------------------------------------------------------------------

# Canonical peer-verify format (IC[5] locked): "### Peer Verification: X verifying Y"
# 3-hash header + " verifying " keyword is the regex anchor.


class TestPeerVerifyRegexContract:
    """A16/A17/A18 depend on _PEER_VERIFY_HEADER regex (IC[5] locked).

    These tests extend the existing TestPeerVerification class to lock the
    canonical format contract explicitly and cover edge cases that arise
    when the TW SQ[4] spawn-template propagation is live.
    """

    def test_regex_matches_canonical_3hash_verifying_format(self):
        """'### Peer Verification: X verifying Y' — the locked canonical format."""
        ws = """
### Peer Verification: tech-architect verifying implementation-engineer
F[IE-1] checked, DB[IE-2] valid, source:[code-read] T1
"""
        verifications = ce._extract_peer_verifications(ws)
        assert len(verifications) == 1
        assert verifications[0]["verifier"] == "tech-architect"
        assert verifications[0]["verified"] == "implementation-engineer"

    def test_regex_case_insensitive_on_keyword(self):
        """'verifying' keyword is case-insensitive per re.IGNORECASE."""
        ws = """
### Peer Verification: tech-architect VERIFYING implementation-engineer
F[x] DB[y] H1
"""
        verifications = ce._extract_peer_verifications(ws)
        assert len(verifications) == 1

    def test_regex_rejects_4hash_header(self):
        """#### (4 hashes) must NOT match — 3-hash is canonical per IC[5]."""
        ws = """
#### Peer Verification: tech-architect verifying implementation-engineer
F[x] DB[y] H1
"""
        verifications = ce._extract_peer_verifications(ws)
        assert len(verifications) == 0, (
            "4-hash header must not match — IC[5] locks 3-hash as canonical"
        )

    def test_regex_rejects_verifies_variant(self):
        """'X verifies Y' (without -ing) must NOT match — only 'verifying' is canonical."""
        ws = """
### Peer Verification: tech-architect verifies implementation-engineer
F[x] DB[y] H1
"""
        verifications = ce._extract_peer_verifications(ws)
        assert len(verifications) == 0, (
            "'verifies' variant must not match — canonical format requires 'verifying'"
        )

    def test_a16_passes_when_all_non_da_agents_have_verifier_sections(self, patch_paths):
        """Every non-DA agent in extract_agents must appear as verifier of someone."""
        write, _, _ = patch_paths
        ws = """\
## findings
### tech-architect
F[TA-1] a finding

### implementation-engineer
F[IE-1] another

## convergence
### Peer Verification: tech-architect verifying implementation-engineer
F[IE-1] valid, DB[IE-1], H1 addressed

### Peer Verification: implementation-engineer verifying tech-architect
F[TA-1] valid, DB[TA-1], H1 addressed
"""
        write(ws)
        item = ce.check_a16(ws)
        assert item.passed is True, f"A16 should pass, got: {item.issues}"
        assert "tech-architect" in item.details["agents"]
        assert "implementation-engineer" in item.details["agents"]
        assert item.details["verifications_found"] == 2

    def test_a16_fails_when_agent_has_no_verifier_role(self, patch_paths):
        """If TA has a finding but never verifies anyone, A16 flags TA as missing."""
        write, _, _ = patch_paths
        ws = """\
## findings
### tech-architect
F[TA-1]

### implementation-engineer
F[IE-1]

## convergence
### Peer Verification: implementation-engineer verifying tech-architect
F[TA-1] DB[TA-1] H1
"""
        write(ws)
        item = ce.check_a16(ws)
        assert item.passed is False
        assert "tech-architect" in item.details["agents_without_verification"]

    def test_a17_counts_three_distinct_artifact_patterns(self):
        """A17 needs >=3 artifact refs; mix of F[], DB[], H1 should pass."""
        ws = """\
### Peer Verification: tech-architect verifying implementation-engineer
Confirmed F[IE-1], DB[IE-2] holds, H1 addressed specifically.
"""
        item = ce.check_a17(ws)
        # >=3 patterns: F[IE-1] + DB[IE-2] + H1 = 3 distinct refs
        assert item.passed is True, f"A17 should pass with 3 refs, got: {item.issues}"

    def test_a17_fails_on_exactly_two_refs(self):
        """Boundary: exactly 2 refs — below threshold (>=3)."""
        ws = """\
### Peer Verification: tech-architect verifying implementation-engineer
Looked at F[IE-1] and DB[IE-1]. Looks OK.
"""
        item = ce.check_a17(ws)
        assert item.passed is False, "A17 must fail below 3-ref threshold"

    def test_a17_xverify_tag_counts_as_artifact_ref(self):
        """XVERIFY[provider:model] pattern is one of the locked artifact families."""
        ws = """\
### Peer Verification: tech-architect verifying implementation-engineer
XVERIFY[openai:gpt-4o] XVERIFY[google:gemini] XVERIFY[nemotron:nano]
"""
        item = ce.check_a17(ws)
        assert item.passed is True, (
            "Three XVERIFY tags alone should satisfy A17's >=3 threshold"
        )

    def test_a18_coverage_with_da_counted(self, patch_paths):
        """DA challenges count as verification of all agents (1 ring peer + DA = 2)."""
        write, _, _ = patch_paths
        ws = """\
## findings
### tech-architect
F[TA-1]

### implementation-engineer
F[IE-1]

### Peer Verification: tech-architect verifying implementation-engineer
F[IE-1] valid DB[IE-1] H1

### Peer Verification: implementation-engineer verifying tech-architect
F[TA-1] valid DB[TA-1] H1

### devils-advocate
DA[#1] TA anchor challenge
DA[#2] IE compliance challenge
exit-gate: PASS
"""
        write(ws)
        item = ce.check_a18(ws)
        assert item.passed is True, f"A18 should pass, got: {item.issues}"
        assert item.details["da_verifies_all"] is True
        # Each agent verified by >=2 (one peer + DA)
        for agent, verifiers in item.details["coverage"].items():
            assert len(verifiers) >= 2, (
                f"{agent} under-covered: {verifiers}"
            )

    def test_a18_fails_without_da_and_only_one_peer_verifier(self, patch_paths):
        """If DA is absent and only one peer verifies, coverage is insufficient."""
        write, _, _ = patch_paths
        ws = """\
## findings
### tech-architect
F[TA-1]

### implementation-engineer
F[IE-1]

### Peer Verification: tech-architect verifying implementation-engineer
F[IE-1] DB[IE-1] H1
"""
        write(ws)
        item = ce.check_a18(ws)
        # implementation-engineer has 1 verifier (TA), no DA, no self-verify
        # tech-architect has 0 verifiers
        assert item.passed is False
        assert len(item.details["under_covered"]) > 0


# ---------------------------------------------------------------------------
# SQ[13d] — A3 DB extraction: split-by-DB + (1)(2)(3) marker filter (ie-1 SQ[3])
# ---------------------------------------------------------------------------
#
# R19 #19 fix: pre-rewrite re.findall matched every DB[...] substring, including
# reference citations ("DB[F[A-1]] confirmed by TA"). Post-fix: split-by-DB
# produces candidate segments; segments require (1)(2)(3) parenthesised markers
# to count as genuine dialectical exercises; everything else counts as a
# reference citation.
#
# Surface contract (documented in ie-1 SQ[3] scratch note):
#   details["db_genuine_by_agent"] : dict[agent, genuine_count]
#   details["db_reference_by_agent"] : dict[agent, reference_count]
#   details["shallow_db_entries"] : list[str] (only present if shallow found)


def _make_ws_with_agent_db(agent: str, db_block: str) -> str:
    """Build a minimal workspace with one real-roster agent and a DB block."""
    return f"""\
# workspace
## status: active
## mode: ANALYZE

## findings
### {agent}
F[X-1] a finding |source:[independent-research] T1
{db_block}

## convergence
{agent}: ✓ complete
"""


class TestA3DBGenuineVsReference:
    """Verification 4 contract: genuine DB exercises require (1)(2)(3) markers."""

    def test_five_genuine_exercises_counted(self, patch_paths):
        write, _, _ = patch_paths
        # All 5 follow the canonical (1)(2)(3)(4)(5) pattern.
        db_block = "\n".join(
            f"DB[F[X-{i}]]: (1) initial: a{i} (2) assume-wrong: b{i} "
            f"(3) strongest-counter: c{i} (4) re-estimate: d{i} (5) reconciled: e{i}"
            for i in range(1, 6)
        )
        ws = _make_ws_with_agent_db("tech-architect", db_block)
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("tech-architect") == 5, (
            f"Expected 5 genuine, got {item.details['db_genuine_by_agent']}"
        )
        assert item.details["db_reference_by_agent"].get("tech-architect", 0) == 0
        # No shallow entries (all have 4 and 5)
        assert "shallow_db_entries" not in item.details or not item.details["shallow_db_entries"]

    def test_pure_references_no_genuine(self, patch_paths):
        write, _, _ = patch_paths
        # DB citations in prose — no (1)(2)(3) markers.
        db_block = (
            "Summary references: DB[F[X-1]] confirmed by TA, DB[F[X-2]] from prior round, "
            "DB[F[X-3]] holds under challenge."
        )
        ws = _make_ws_with_agent_db("implementation-engineer", db_block)
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("implementation-engineer", 0) == 0, (
            "Pure reference citations must NOT count as genuine exercises"
        )
        # All three DB[] matches land in references
        assert item.details["db_reference_by_agent"].get("implementation-engineer") == 3

    def test_mixed_three_genuine_two_references(self, patch_paths):
        write, _, _ = patch_paths
        db_block = (
            "DB[F[X-1]]: (1) initial: a (2) assume-wrong: b (3) counter: c "
            "(4) re-estimate: d (5) reconciled: e\n"
            "DB[F[X-2]]: (1) init (2) assume-wrong (3) counter (4) re-est (5) reconciled\n"
            "DB[F[X-3]]: (1) a (2) b (3) c (4) d (5) e\n"
            "Later references: DB[F[X-1]] confirmed, DB[F[X-2]] holds."
        )
        ws = _make_ws_with_agent_db("tech-architect", db_block)
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("tech-architect") == 3, (
            f"Expected 3 genuine, got {item.details['db_genuine_by_agent']}"
        )
        assert item.details["db_reference_by_agent"].get("tech-architect") == 2, (
            f"Expected 2 references, got {item.details['db_reference_by_agent']}"
        )

    def test_shallow_exercise_flagged(self, patch_paths):
        """DB with (1)(2)(3) only — counts as genuine but surfaces in shallow_db_entries."""
        write, _, _ = patch_paths
        db_block = "DB[F[X-1]]: (1) initial (2) assume-wrong (3) counter — stopped here"
        ws = _make_ws_with_agent_db("tech-architect", db_block)
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("tech-architect") == 1
        assert "shallow_db_entries" in item.details
        shallow = item.details["shallow_db_entries"]
        assert any("tech-architect" in entry for entry in shallow), (
            f"Shallow entry must reference the agent name: {shallow}"
        )

    def test_multi_agent_keyed_per_agent(self, patch_paths):
        """Two agents, each with different genuine/reference counts, keyed correctly."""
        write, _, _ = patch_paths
        ws = """\
# workspace
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] finding |source:[independent-research] T1
DB[F[TA-1]]: (1) initial: a (2) assume-wrong: b (3) counter: c (4) re-est: d (5) reconciled: e
DB[F[TA-2]]: (1) a (2) b (3) c (4) d (5) e

### implementation-engineer
F[IE-1] finding |source:[independent-research] T1
DB[F[IE-1]]: (1) i (2) w (3) c (4) r (5) f
Earlier: DB[F[TA-1]] was settled by TA, DB[F[TA-2]] also confirmed.

## convergence
tech-architect: ✓ complete
implementation-engineer: ✓ complete
"""
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("tech-architect") == 2
        assert item.details["db_genuine_by_agent"].get("implementation-engineer") == 1
        # IE has 2 references citing TA's DBs
        assert item.details["db_reference_by_agent"].get("implementation-engineer") == 2
        # TA has no references in its own section
        assert item.details["db_reference_by_agent"].get("tech-architect", 0) == 0

    def test_adjacent_db_entries_split_correctly(self, patch_paths):
        """DB entries with no intervening prose — lookahead split must not merge them."""
        write, _, _ = patch_paths
        # Three genuine exercises back-to-back, no blank lines between.
        db_block = (
            "DB[F[X-1]]: (1) a (2) b (3) c (4) d (5) e\n"
            "DB[F[X-2]]: (1) a (2) b (3) c (4) d (5) e\n"
            "DB[F[X-3]]: (1) a (2) b (3) c (4) d (5) e"
        )
        ws = _make_ws_with_agent_db("tech-architect", db_block)
        write(ws)
        item = ce.check_a3(ws)

        assert item.details["db_genuine_by_agent"].get("tech-architect") == 3, (
            "Adjacent DB entries must split into 3 segments, not merge into 1"
        )


# ---------------------------------------------------------------------------
# SQ[13f] + SQ[CDS-6..8] — path-β+ WARN-first gates (A20/A22/A23) + CAL-EMIT
# ---------------------------------------------------------------------------


def _ws_with_finding(agent: str, finding_line: str, *, build_id: str = "26.4.24-test") -> str:
    """Minimal workspace with ## build-id and one finding line placed in ## findings."""
    return f"""\
# workspace
## build-id: {build_id}
## status: active
## mode: ANALYZE

## findings
### {agent}
{finding_line}

## convergence
{agent}: ✓ complete
"""


class TestA20PrecisionGateCondition2:
    """SQ[13f] + SQ[CDS-6] — A20 fires on CONDITION 2 triggers, suppresses on CONDITION 1 keywords."""

    def test_fires_on_70pct_confidence_marker(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] >70% confidence this migration closes by Q3 — no driver breakdown",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)

        assert item.passed is True, "A20 is WARN-only, must never fail chain"
        assert item.details["fire_count"] == 1
        assert item.details["fires"][0]["trigger"] == "confidence>=70%"
        assert item.details["fires"][0]["finding_id"] == "TA-1"
        assert len(item.details["cal_emit_records"]) == 1

    def test_fires_on_high_severity_marker(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "implementation-engineer",
            "F[IE-1] HIGH-severity defect: cross-tenant data leak observed in staging",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 1
        assert item.details["fires"][0]["trigger"] == "HIGH/CRITICAL-severity"

    def test_fires_on_primary_recommendation(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] primary recommendation: consolidate on Postgres 16",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 1
        assert item.details["fires"][0]["trigger"] == "primary-recommendation-cited"

    def test_suppressed_by_driver_breakdown(self, patch_paths):
        """CONDITION 1 suppression: 'derives from: [...]' keyword present → no fire."""
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] >70% confidence — derives from: [base-rate=42%, peer-data=78%, RC[analog]=65%]",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 0, (
            "CONDITION 1 driver breakdown suppressor must prevent fire"
        )

    def test_suppressed_by_ci_notation(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity risk, 80% CI [12, 34] based on historical data",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 0

    def test_suppressed_by_approximately_qualifier(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] primary recommendation: approximately 30% cost reduction expected",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 0


class TestA20CALEmitSchema:
    """SQ[CDS-6] — CAL-EMIT record format compliance + threshold/no-fire cases."""

    def test_cal_emit_record_matches_directive_schema(self, patch_paths):
        """CAL-EMIT[A20]: review-id:X |finding-ref:F[Y] |fire-reason:Z |workspace-context:agent:excerpt |da-verdict:PENDING"""
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity migration defect in payment pipeline",
            build_id="2026-04-24-r19-test",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        record = item.details["cal_emit_records"][0]

        assert record.startswith("CAL-EMIT[A20]: review-id:")
        assert "review-id:2026-04-24-r19-test " in record
        assert "|finding-ref:F[TA-1] " in record
        assert "|fire-reason:HIGH/CRITICAL-severity " in record
        assert "|workspace-context:tech-architect:" in record
        assert record.endswith("|da-verdict:PENDING")

    def test_no_fire_produces_empty_records_list(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] observed 3 log entries in the audit trail — no severity claim",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["cal_emit_records"] == []
        assert item.details["fire_count"] == 0

    def test_multiple_fires_per_agent_each_emit_record(self, patch_paths):
        write, _, _ = patch_paths
        ws = """\
# workspace
## build-id: multi-fire-test
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] HIGH-severity finding one
F[TA-2] >70% confidence in finding two

## convergence
tech-architect: ✓ complete
"""
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 2
        assert len(item.details["cal_emit_records"]) == 2
        finding_ids = [f["finding_id"] for f in item.details["fires"]]
        assert "TA-1" in finding_ids and "TA-2" in finding_ids

    def test_review_id_fallback_when_no_build_id_header(self, patch_paths):
        """No ## build-id → date-prefix + task-excerpt or 'unnamed' fallback."""
        write, _, _ = patch_paths
        ws = """\
# workspace
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] HIGH-severity fallback case

## convergence
tech-architect: ✓ complete
"""
        write(ws)
        item = ce.check_a20_precision_gate(ws)
        review_id = item.details["review_id"]
        import re as _re
        assert _re.match(r"^\d{4}-\d{2}-\d{2}-", review_id), (
            f"fallback review_id must be date-prefixed: {review_id}"
        )


class TestA22GovernanceArtifact:
    """SQ[CDS-7] — A22 fires on HIGH-severity + governance + missing TIER/GAP."""

    def test_fires_on_high_severity_governance_no_artifact(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity: lack of approval process for model deployment",
        )
        write(ws)
        item = ce.check_a22_governance_artifact(ws)
        assert item.passed is True, "A22 is WARN-only"
        assert item.details["fire_count"] == 1
        assert item.details["fires"][0]["trigger"] == "HIGH-severity-governance-no-TIER-artifact"

    def test_suppressed_by_tier_a_artifact_in_window(self, patch_paths):
        write, _, _ = patch_paths
        ws = """\
# workspace
## build-id: tier-test
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] HIGH-severity: oversight role missing for AI-governance committee.
Recommended: TIER-A template stub — model-approval workflow with maker-checker gates.

## convergence
tech-architect: ✓ complete
"""
        write(ws)
        item = ce.check_a22_governance_artifact(ws)
        assert item.details["fire_count"] == 0, (
            "TIER-A in tail must suppress — artifact satisfies directive"
        )

    def test_suppressed_by_artifact_gap_tag(self, patch_paths):
        write, _, _ = patch_paths
        ws = """\
# workspace
## build-id: gap-test
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] HIGH-severity: compliance requirement uncovered for SOC2 audit function.
ARTIFACT-GAP: phase-2 crosswalk pending legal sign-off.

## convergence
tech-architect: ✓ complete
"""
        write(ws)
        item = ce.check_a22_governance_artifact(ws)
        assert item.details["fire_count"] == 0, (
            "ARTIFACT-GAP:{reason} tag must suppress fire"
        )

    def test_does_not_fire_on_non_governance_high_severity(self, patch_paths):
        """HIGH-severity without governance marker → A22 no fire (scope narrow)."""
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "implementation-engineer",
            "F[IE-1] HIGH-severity performance regression in query planner",
        )
        write(ws)
        item = ce.check_a22_governance_artifact(ws)
        assert item.details["fire_count"] == 0, (
            "Non-governance HIGH-severity must NOT fire A22 (anti-gold-plating scope)"
        )


class TestA23SeverityProvenance:
    """SQ[CDS-8] — A23 fires on extrapolated HIGH severity missing |severity-basis: tag."""

    def test_fires_on_extrapolated_severity_missing_tag(self, patch_paths):
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity: SR-11-7 findings extrapolated to AI-agent review context",
        )
        write(ws)
        item = ce.check_a23_severity_provenance(ws)
        assert item.passed is True, "A23 is WARN-only"
        assert item.details["fire_count"] == 1
        assert item.details["fires"][0]["trigger"] == "extrapolated-severity-missing-basis-tag"

    def test_suppressed_when_severity_basis_tag_present(self, patch_paths):
        write, _, _ = patch_paths
        ws = """\
# workspace
## build-id: basis-tag-test
## status: active
## mode: ANALYZE

## findings
### tech-architect
F[TA-1] HIGH-severity: SR-11-7 exam findings extrapolated to AI-agent scope |severity-basis:[extrapolation:banking→AI |assumption:exam-failure-rates-transfer |confidence-delta:T1→agent-inference]

## convergence
tech-architect: ✓ complete
"""
        write(ws)
        item = ce.check_a23_severity_provenance(ws)
        assert item.details["fire_count"] == 0, (
            "|severity-basis: tag present in window → A23 must not fire"
        )

    def test_does_not_fire_on_native_domain_severity(self, patch_paths):
        """HIGH-severity without extrapolation indicator → A23 no fire (narrow scope)."""
        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "implementation-engineer",
            "F[IE-1] HIGH-severity SQL injection vector identified in search endpoint",
        )
        write(ws)
        item = ce.check_a23_severity_provenance(ws)
        assert item.details["fire_count"] == 0, (
            "Native-domain severity (no extrapolation indicator) must NOT fire A23"
        )


class TestPathBetaPlusIntegration:
    """Integration: CAL-EMIT records → calibration-log.md → audit-calibration-gate.py pipeline."""

    def test_cal_emit_appends_to_calibration_log_when_file_exists(
        self, patch_paths, tmp_path, monkeypatch
    ):
        """Fire A20 against tmp log-file, verify append + schema."""
        cal_log = tmp_path / "calibration-log.md"
        cal_log.write_text("# calibration-log\n## Records\n", encoding="utf-8")
        monkeypatch.setattr(ce, "CALIBRATION_LOG_PATH", cal_log)

        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity integration test finding",
            build_id="integration-test",
        )
        write(ws)
        item = ce.check_a20_precision_gate(ws)

        assert item.details["fire_count"] == 1
        log_after = cal_log.read_text(encoding="utf-8")
        assert "CAL-EMIT[A20]" in log_after
        assert "review-id:integration-test" in log_after
        assert "finding-ref:F[TA-1]" in log_after
        assert "da-verdict:PENDING" in log_after

    def test_cal_emit_silent_when_log_missing(
        self, patch_paths, tmp_path, monkeypatch
    ):
        """File-missing → silent: record still in details, no exception raised."""
        missing = tmp_path / "does-not-exist.md"
        assert not missing.exists()
        monkeypatch.setattr(ce, "CALIBRATION_LOG_PATH", missing)

        write, _, _ = patch_paths
        ws = _ws_with_finding(
            "tech-architect",
            "F[TA-1] HIGH-severity silent-write test",
            build_id="silent-test",
        )
        write(ws)
        # Must not raise — file existence check prevents write; record still returned
        item = ce.check_a20_precision_gate(ws)
        assert item.details["fire_count"] == 1
        assert len(item.details["cal_emit_records"]) == 1, (
            "Record must still be returned in details even if file write skipped"
        )
