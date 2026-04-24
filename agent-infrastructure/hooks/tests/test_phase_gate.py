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


# ---------------------------------------------------------------------------
# SQ[13g] + SQ[SS-2] — sed-i BLOCK 4 detection + shlex evasion matrix
# ---------------------------------------------------------------------------
#
# BLOCK 4 (phase-gate.py:235+) covers the R19 silent-overwrite failure mode:
# `sed -i` (no backup suffix) on workspace.md + /.claude/teams/sigma-*/shared/
# + /.claude/hooks/ paths. Tokenization via shlex.split(posix=True) (IC[1])
# is what makes the gate resistant to shell-quoting bypass.
#
# Evasion forms covered per CAL[4] + SS-2 matrix:
#   - env-var wrapper: `env FOO=bar sed -i 'x' workspace.md`
#   - xargs wrapper:   `echo workspace.md | xargs sed -i 'x'`
#   - absolute-path sed: `/usr/bin/sed -i ...`
#   - -i '' separated form (BSD-style, effectively no-backup)
#   - -i.bak joined form (ALLOWED, real suffix = recoverable)
#   - quoting tricks / mixed operand ordering


class TestSedInPlaceBlock4Detection:
    """Direct coverage of phase_gate.check_sed_in_place() on workspace paths."""

    def test_blocks_sed_i_on_workspace_md(self):
        blocked, reason = pg.check_sed_in_place(
            "sed -i 's/foo/bar/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is True
        assert "SED IN-PLACE BLOCKED" in reason

    def test_blocks_sed_i_on_hooks_directory(self):
        blocked, reason = pg.check_sed_in_place(
            "sed -i 's/old/new/' /Users/me/.claude/hooks/chain-evaluator.py"
        )
        assert blocked is True
        assert "/.claude/hooks/" in reason or "protected path" in reason

    def test_allows_sed_i_bak_backup_form(self):
        """-i.bak with real suffix creates a recoverable backup — allowed per CAL[4]."""
        blocked, reason = pg.check_sed_in_place(
            "sed -i.bak 's/foo/bar/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is False, f"Backup form must pass, got reason: {reason}"

    def test_blocks_sed_i_empty_suffix_separated_form(self):
        """BSD-style `sed -i '' file` is no-backup on BSD — must be blocked."""
        blocked, reason = pg.check_sed_in_place(
            "sed -i '' 's/foo/bar/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is True, (
            "`-i '' file` form is effectively no-backup on BSD — must be blocked"
        )

    def test_allows_sed_i_outside_protected_scope(self):
        """Tool calls on paths outside workspace/hooks scope are never blocked."""
        blocked, reason = pg.check_sed_in_place(
            "sed -i 's/foo/bar/' /tmp/random-file.txt"
        )
        assert blocked is False

    def test_allows_sed_without_i_flag(self):
        """Plain `sed` (non-in-place, reads to stdout) is never our concern."""
        blocked, reason = pg.check_sed_in_place(
            "sed 's/foo/bar/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is False


class TestSedShlexEvasionMatrix:
    """SS-2 matrix: argv-tokenization coverage vs raw-regex bypass attempts."""

    def test_env_wrapper_detected(self):
        """`env FOO=bar sed -i ...` — shlex walks all tokens for a `sed` node."""
        blocked, reason = pg.check_sed_in_place(
            "env LC_ALL=C sed -i 's/x/y/' ~/.claude/hooks/phase-gate.py"
        )
        assert blocked is True, (
            "env-wrapper must not bypass — shlex walk finds sed token at position 2"
        )

    def test_xargs_stdin_is_known_limitation_not_blocked(self):
        """`xargs sed -i` with target path via stdin is documented out-of-scope.

        Positive-contract test: phase-gate.py uses shlex.split to parse argv.
        When the target file reaches sed through xargs stdin rather than its
        own argv, the protected-path check has no operand to examine. This is
        a DELIBERATE argv-scope limitation per ADR[SS-1] + docstring at
        phase-gate.py:300 (post-BUILD-CONCERN[cqa] 26.4.24 resolution (a)).

        Rejected alternative: blocking any `xargs` + `sed -i` chain regardless
        of operand paths produces too-high false-positive rate on legitimate
        batch-edits outside the protected scope. Process convention covers
        the gap: reviewers must spot `xargs sed -i` in PR diffs on protected
        paths. When this test starts failing (i.e. the gate DOES block), the
        implementation has been extended — update this test to match the new
        contract.
        """
        blocked, _reason = pg.check_sed_in_place(
            "echo ~/.claude/hooks/x.py | xargs sed -i 's/a/b/'"
        )
        assert blocked is False, (
            "xargs stdin path is out-of-scope for argv-based shlex walk — "
            "if this starts blocking, ADR[SS-1] contract has been extended; update test"
        )

    def test_absolute_sed_path_detected(self):
        """`/usr/bin/sed -i ...` — detected via tok.endswith('/sed')."""
        blocked, reason = pg.check_sed_in_place(
            "/usr/bin/sed -i 's/foo/bar/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is True, (
            "Absolute sed path must be caught — tok.endswith('/sed') covers this"
        )

    def test_joined_iflag_with_empty_suffix_blocked(self):
        """`-i''` joined with quoted empty string — the suffix collapses; must block."""
        # shlex parses `sed -i'' 'pat' file` as [sed, -i, pat, file] after
        # posix quote-stripping. Confirm BLOCK fires in this form.
        blocked, reason = pg.check_sed_in_place(
            "sed -i'' 's/x/y/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is True, (
            "-i'' (empty-string join) must block — no real backup suffix"
        )

    def test_long_in_place_flag_blocked(self):
        """--in-place without suffix is equivalent to -i — must block."""
        blocked, reason = pg.check_sed_in_place(
            "sed --in-place 's/x/y/' ~/.claude/hooks/chain-evaluator.py"
        )
        assert blocked is True, (
            "`--in-place` long form must block — same semantics as `-i` no-backup"
        )

    def test_malformed_command_does_not_block(self):
        """shlex.split raises ValueError on unbalanced quotes; gate should return False, not error."""
        # Unterminated quoted string — shlex raises, check_sed_in_place must
        # fail-open (let the shell error naturally).
        blocked, reason = pg.check_sed_in_place(
            'sed -i "unterminated workspace.md'
        )
        assert blocked is False, (
            "Malformed command must not block — fail-open on shlex parse error"
        )

    def test_chained_command_second_sed_still_blocked(self):
        """Shell separators (&&, ||, ;) terminate; sed in second command still scanned."""
        blocked, reason = pg.check_sed_in_place(
            "cd /tmp && sed -i 's/a/b/' ~/.claude/teams/sigma-review/shared/workspace.md"
        )
        assert blocked is True, (
            "Second sed after && must still block — walker continues through separators"
        )

    def test_sigma_optimize_shared_scope_protected(self):
        """SED_I_PROTECTED_PATHS covers sigma-optimize/shared/ symmetric to sigma-review."""
        blocked, reason = pg.check_sed_in_place(
            "sed -i 's/x/y/' ~/.claude/teams/sigma-optimize/shared/something.md"
        )
        assert blocked is True, (
            "sigma-optimize/shared/ must be protected same as sigma-review/shared/"
        )
