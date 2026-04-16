"""Tests for phase-gate.py — the minimal PreToolUse/PostToolUse hook.

Tests cover:
- Session detection (_is_sigma_session, _is_build_session)
- Code write authorization (BUILD sessions only, plan-lock required)
- Git commit gating (sigma sessions only, chain must be complete)
- Context firewall leak detection
- Hook dispatch (enforce_pre_tool_use, enforce_post_tool_use)
- Integration: subprocess smoke tests matching Claude Code hooks API
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Import the module under test
HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "phase_gate", HOOKS_DIR / "phase-gate.py"
)
pg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pg)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_workspace(tmp_path):
    """Create a temp workspace file and patch DEFAULT_WORKSPACE to point to it."""
    ws = tmp_path / "workspace.md"

    def _write(content):
        ws.write_text(content, encoding="utf-8")
        return ws

    return _write, ws


@pytest.fixture
def tmp_chain_status(tmp_path):
    """Create a temp chain status file and patch CHAIN_STATUS_FILE."""
    return tmp_path / ".chain-status.json"


@pytest.fixture
def patch_paths(tmp_workspace, tmp_chain_status):
    """Patch both DEFAULT_WORKSPACE and CHAIN_STATUS_FILE."""
    _write, ws_path = tmp_workspace
    with patch.object(pg, "DEFAULT_WORKSPACE", ws_path), \
         patch.object(pg, "CHAIN_STATUS_FILE", tmp_chain_status):
        yield _write, ws_path, tmp_chain_status


# ---------------------------------------------------------------------------
# _is_sigma_session()
# ---------------------------------------------------------------------------

class TestIsSigmaSession:
    def test_returns_false_when_no_workspace(self, tmp_path):
        with patch.object(pg, "DEFAULT_WORKSPACE", tmp_path / "nonexistent.md"):
            assert pg._is_sigma_session() is False

    def test_returns_false_for_idle_workspace(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## status: idle\n")
        assert pg._is_sigma_session() is False

    def test_returns_true_for_task_marker(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## task\nSome analysis task\n")
        assert pg._is_sigma_session() is True

    def test_returns_true_for_mode_marker(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## mode: BUILD\n")
        assert pg._is_sigma_session() is True

    def test_case_insensitive(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## Task\nSomething\n")
        assert pg._is_sigma_session() is True


# ---------------------------------------------------------------------------
# _is_build_session()
# ---------------------------------------------------------------------------

class TestIsBuildSession:
    def test_returns_false_when_no_workspace(self, tmp_path):
        with patch.object(pg, "DEFAULT_WORKSPACE", tmp_path / "nonexistent.md"):
            assert pg._is_build_session() is False

    def test_returns_false_for_analyze(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## mode: ANALYZE\n## task\nReview something\n")
        assert pg._is_build_session() is False

    def test_returns_true_for_build(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## mode: BUILD\n## task\nBuild something\n")
        assert pg._is_build_session() is True

    def test_returns_true_for_lowercase_build(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\nmode: build\n")
        assert pg._is_build_session() is True


# ---------------------------------------------------------------------------
# _workspace_has_plan_lock()
# ---------------------------------------------------------------------------

class TestWorkspaceHasPlanLock:
    def test_returns_false_when_no_workspace(self, tmp_path):
        with patch.object(pg, "DEFAULT_WORKSPACE", tmp_path / "nonexistent.md"):
            assert pg._workspace_has_plan_lock() is False

    def test_returns_false_without_adr_or_ic(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## task\nBuild something\n")
        assert pg._workspace_has_plan_lock() is False

    def test_returns_false_with_only_adr(self, patch_paths):
        write, _, _ = patch_paths
        write("ADR[1]: Use pip deps\n")
        assert pg._workspace_has_plan_lock() is False

    def test_returns_false_with_only_ic(self, patch_paths):
        write, _, _ = patch_paths
        write("IC[1]: Agent output format\n")
        assert pg._workspace_has_plan_lock() is False

    def test_returns_true_with_both(self, patch_paths):
        write, _, _ = patch_paths
        write("ADR[1]: Use pip deps\nIC[1]: Agent output format\n")
        assert pg._workspace_has_plan_lock() is True


# ---------------------------------------------------------------------------
# _chain_is_complete()
# ---------------------------------------------------------------------------

class TestChainIsComplete:
    def test_returns_false_when_no_status_file(self, tmp_path):
        with patch.object(pg, "CHAIN_STATUS_FILE", tmp_path / "nonexistent.json"):
            assert pg._chain_is_complete() is False

    def test_returns_false_when_incomplete(self, patch_paths):
        _, _, status_file = patch_paths
        status_file.write_text(json.dumps({"last_complete": False}))
        assert pg._chain_is_complete() is False

    def test_returns_true_when_complete(self, patch_paths):
        _, _, status_file = patch_paths
        status_file.write_text(json.dumps({"last_complete": True}))
        assert pg._chain_is_complete() is True

    def test_handles_corrupt_json(self, patch_paths):
        _, _, status_file = patch_paths
        status_file.write_text("not json{{{")
        assert pg._chain_is_complete() is False


# ---------------------------------------------------------------------------
# check_code_write_authorization()
# ---------------------------------------------------------------------------

class TestCodeWriteAuthorization:
    def test_allows_outside_build_session(self, patch_paths):
        write, _, _ = patch_paths
        write("# workspace\n## status: idle\n")
        blocked, reason = pg.check_code_write_authorization("/some/code.py")
        assert blocked is False

    def test_allows_with_plan_lock(self, patch_paths):
        write, _, _ = patch_paths
        write("mode: BUILD\nADR[1]: test\nIC[1]: test\n")
        blocked, reason = pg.check_code_write_authorization("/some/code.py")
        assert blocked is False

    def test_blocks_code_write_without_plan_lock(self, patch_paths):
        write, _, _ = patch_paths
        write("mode: BUILD\n## task\nBuild something\n")
        blocked, reason = pg.check_code_write_authorization("/some/code.py")
        assert blocked is True
        assert "plan-lock" in reason.lower() or "ADR" in reason

    def test_allows_infrastructure_paths_without_plan_lock(self, patch_paths):
        write, _, _ = patch_paths
        write("mode: BUILD\n## task\nBuild something\n")
        for path in [
            "/Users/test/.claude/teams/sigma-review/shared/workspace.md",
            "/Users/test/.claude/agents/test.md",
            "/tmp/scratch.txt",
            "/Users/test/.claude/hooks/test.py",
        ]:
            blocked, reason = pg.check_code_write_authorization(path)
            assert blocked is False, f"Should allow infrastructure path: {path}"


# ---------------------------------------------------------------------------
# check_premature_git_operation() — CRITICAL: scoping tests
# ---------------------------------------------------------------------------

class TestPrematureGitOperation:
    def test_allows_non_git_commands(self, patch_paths):
        blocked, reason = pg.check_premature_git_operation("ls -la")
        assert blocked is False

    def test_allows_git_status(self, patch_paths):
        blocked, reason = pg.check_premature_git_operation("git status")
        assert blocked is False

    def test_allows_git_diff(self, patch_paths):
        blocked, reason = pg.check_premature_git_operation("git diff --cached")
        assert blocked is False

    def test_allows_git_commit_outside_sigma_session(self, patch_paths):
        """CRITICAL: git commit must be allowed when not in a sigma session."""
        write, _, _ = patch_paths
        write("# workspace\n## status: idle\n")
        blocked, reason = pg.check_premature_git_operation("git commit -m 'test'")
        assert blocked is False, "git commit must not be blocked outside sigma sessions"

    def test_allows_git_push_outside_sigma_session(self, patch_paths):
        """CRITICAL: git push must be allowed when not in a sigma session."""
        write, _, _ = patch_paths
        write("# workspace\n## status: idle\n")
        blocked, reason = pg.check_premature_git_operation("git push origin main")
        assert blocked is False, "git push must not be blocked outside sigma sessions"

    def test_allows_git_commit_when_no_workspace(self, tmp_path):
        """CRITICAL: git commit must work when workspace doesn't exist."""
        with patch.object(pg, "DEFAULT_WORKSPACE", tmp_path / "nonexistent.md"), \
             patch.object(pg, "CHAIN_STATUS_FILE", tmp_path / "nonexistent.json"):
            blocked, reason = pg.check_premature_git_operation("git commit -m 'test'")
            assert blocked is False

    def test_blocks_git_commit_during_incomplete_sigma_session(self, patch_paths):
        write, _, status_file = patch_paths
        write("# workspace\n## task\nReview something\n")
        status_file.write_text(json.dumps({"last_complete": False}))
        blocked, reason = pg.check_premature_git_operation("git commit -m 'test'")
        assert blocked is True
        assert "chain" in reason.lower() or "complete" in reason.lower()

    def test_allows_git_commit_when_chain_complete(self, patch_paths):
        write, _, status_file = patch_paths
        write("# workspace\n## task\nReview something\n")
        status_file.write_text(json.dumps({"last_complete": True}))
        blocked, reason = pg.check_premature_git_operation("git commit -m 'test'")
        assert blocked is False


# ---------------------------------------------------------------------------
# detect_context_firewall_leak()
# ---------------------------------------------------------------------------

class TestContextFirewallLeak:
    def test_no_warn_on_non_workspace_file(self):
        result = pg.detect_context_firewall_leak("/some/other/file.md", "my career goals")
        assert result is None

    def test_no_warn_on_clean_workspace_content(self):
        result = pg.detect_context_firewall_leak(
            "/path/to/workspace.md",
            "Agent findings: market analysis complete"
        )
        assert result is None

    def test_warns_on_career_leak(self):
        result = pg.detect_context_firewall_leak(
            "/path/to/workspace.md",
            "This aligns with my career goals in fintech"
        )
        assert result is not None
        assert "personal context" in result.lower() or "firewall" in result.lower()

    def test_warns_on_salary_leak(self):
        result = pg.detect_context_firewall_leak(
            "/path/to/workspace.md",
            "my salary expectations should inform this analysis"
        )
        assert result is not None


# ---------------------------------------------------------------------------
# enforce_pre_tool_use() — dispatch tests
# ---------------------------------------------------------------------------

class TestEnforcePreToolUse:
    def test_allows_read_tool(self, patch_paths):
        exit_code, output = pg.enforce_pre_tool_use({
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.py"},
        })
        assert exit_code == 0

    def test_routes_write_to_code_auth(self, patch_paths):
        write, _, _ = patch_paths
        write("mode: BUILD\n## task\nBuild\n")  # BUILD, no plan lock
        exit_code, output = pg.enforce_pre_tool_use({
            "tool_name": "Write",
            "tool_input": {"file_path": "/some/code.py"},
        })
        assert exit_code == 2  # BLOCK

    def test_routes_bash_git_to_git_check(self, patch_paths):
        write, _, status_file = patch_paths
        write("# workspace\n## task\nReview\n")  # sigma session
        status_file.write_text(json.dumps({"last_complete": False}))
        exit_code, output = pg.enforce_pre_tool_use({
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
        })
        assert exit_code == 2  # BLOCK

    def test_allows_bash_non_git(self, patch_paths):
        exit_code, output = pg.enforce_pre_tool_use({
            "tool_name": "Bash",
            "tool_input": {"command": "python3 test.py"},
        })
        assert exit_code == 0


# ---------------------------------------------------------------------------
# enforce_post_tool_use() — dispatch tests
# ---------------------------------------------------------------------------

class TestEnforcePostToolUse:
    def test_no_message_for_clean_write(self):
        output = pg.enforce_post_tool_use({
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/path/to/workspace.md",
                "content": "Clean analytical content",
            },
        })
        assert output == {} or "systemMessage" not in output

    def test_warns_on_context_leak_in_write(self):
        output = pg.enforce_post_tool_use({
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/path/to/workspace.md",
                "content": "This relates to my career advancement",
            },
        })
        assert "systemMessage" in output

    def test_no_message_for_read(self):
        output = pg.enforce_post_tool_use({
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.py"},
        })
        assert output == {}


# ---------------------------------------------------------------------------
# Integration: subprocess smoke tests
# ---------------------------------------------------------------------------

class TestPhaseGateIntegration:
    """Run phase-gate.py as subprocess, matching Claude Code hooks API."""

    def _run(self, stdin_data, home_dir=None):
        script = HOOKS_DIR / "phase-gate.py"
        env = os.environ.copy()
        if home_dir:
            env["HOME"] = str(home_dir)
        result = __import__("subprocess").run(
            [sys.executable, str(script)],
            input=json.dumps(stdin_data),
            capture_output=True, text=True, env=env, timeout=10,
        )
        return result

    def test_exits_clean_on_empty_json(self):
        result = self._run({})
        assert result.returncode == 0

    def test_exits_clean_on_read_event(self):
        result = self._run({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/test.py"},
        })
        assert result.returncode == 0

    def test_exits_clean_on_non_sigma_git_commit(self, tmp_path):
        """CRITICAL: git commit outside sigma session must exit 0."""
        home = tmp_path / "home"
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)
        # Write idle workspace
        ws = home / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"
        ws.write_text("# workspace\n## status: idle\n")

        result = self._run({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
        }, home_dir=home)
        assert result.returncode == 0, f"Should allow git commit outside sigma. stderr: {result.stderr}"

    def test_blocks_git_commit_during_sigma_session(self, tmp_path):
        home = tmp_path / "home"
        hooks_dir = home / ".claude" / "hooks"
        hooks_dir.mkdir(parents=True)
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)
        # Active sigma workspace
        ws = home / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"
        ws.write_text("# workspace\n## task\nReview something\n")
        # Chain not complete
        status = hooks_dir / ".chain-status.json"
        status.write_text(json.dumps({"last_complete": False}))

        result = self._run({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "git commit -m 'test'"},
        }, home_dir=home)
        assert result.returncode == 2, "Should block git commit during incomplete sigma session"
