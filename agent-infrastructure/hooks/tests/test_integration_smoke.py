"""Integration smoke tests — end-to-end subprocess tests.

Pipe realistic hook event JSON through each script via subprocess.
Verify correct exit codes and file side effects.
Tests the actual stdin→stdout contract against the Claude Code hooks API.
"""
import json
import os
import sys
import subprocess
from pathlib import Path

import pytest

HOOKS_DIR = Path(__file__).parent.parent


def run_hook(script_name, stdin_data, home_dir=None):
    """Run a hook script via subprocess with JSON on stdin."""
    script_path = HOOKS_DIR / script_name
    env = os.environ.copy()
    if home_dir:
        env["HOME"] = str(home_dir)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(stdin_data),
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )
    return result


# ─── sigma-retrospective.py ───


class TestRetroIntegration:
    def test_exits_clean_on_non_stop_event(self):
        result = run_hook("sigma-retrospective.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
        })
        assert result.returncode == 0

    def test_exits_clean_on_stop_without_workspace(self, tmp_path):
        """Stop event but no workspace → clean exit."""
        home = tmp_path / "home"
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)
        result = run_hook("sigma-retrospective.py", {"hook_event_name": "Stop"}, home)
        assert result.returncode == 0

    def test_exits_clean_on_invalid_json(self):
        """Garbage stdin → clean exit (not crash)."""
        script_path = HOOKS_DIR / "sigma-retrospective.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input="not valid json{{{",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0

    def test_fires_on_completed_review(self, tmp_path):
        """Stop event with converged workspace → writes retro."""
        home = tmp_path / "home"
        shared = home / ".claude" / "teams" / "sigma-review" / "shared"
        shared.mkdir(parents=True)

        workspace = shared / "workspace.md"
        workspace.write_text(
            "## task\nTest review\n\n## infrastructure\nΣVerify: unavailable\n\n"
            "## convergence\nagent-a: ✓ done |2 findings\nagent-b: ✓ done |1 finding\n\n"
            "## findings\nF[x]: some finding |source:independent-research:T1|\n"
            "CHECK CONFIRMS with risk — outcome 2\n"
            "TIER-1 complexity\n",
            encoding="utf-8",
        )

        patterns = shared / "patterns.md"
        patterns.write_text("# Patterns\n", encoding="utf-8")

        result = run_hook("sigma-retrospective.py", {"hook_event_name": "Stop"}, home)
        assert result.returncode == 0

        content = patterns.read_text()
        assert "## Retro: R1" in content
        assert "agent-a, agent-b" in content

    def test_dedup_prevents_double_retro(self, tmp_path):
        """Running twice with same workspace should only write one retro."""
        home = tmp_path / "home"
        shared = home / ".claude" / "teams" / "sigma-review" / "shared"
        shared.mkdir(parents=True)

        workspace = shared / "workspace.md"
        workspace.write_text(
            "## convergence\nagent: ✓ done\n",
            encoding="utf-8",
        )
        patterns = shared / "patterns.md"
        patterns.write_text("", encoding="utf-8")

        data = {"hook_event_name": "Stop"}
        run_hook("sigma-retrospective.py", data, home)
        run_hook("sigma-retrospective.py", data, home)

        content = patterns.read_text()
        assert content.count("## Retro:") == 1


# ─── agent-calibration-tracker.py ───


class TestCalibrationIntegration:
    def test_exits_clean_on_non_sendmessage(self):
        result = run_hook("agent-calibration-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file"},
        })
        assert result.returncode == 0

    def test_exits_clean_on_empty_message(self):
        result = run_hook("agent-calibration-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "SendMessage",
            "tool_input": {"to": "", "message": ""},
        })
        assert result.returncode == 0

    def test_tracks_rich_agent_message(self, tmp_path):
        home = tmp_path / "home"
        agent_dir = home / ".claude" / "agents" / "product-strategist"
        agent_dir.mkdir(parents=True)
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)

        result = run_hook("agent-calibration-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "SendMessage",
            "tool_input": {
                "to": "lead",
                "message": (
                    "product-strategist: ✓ findings complete\n"
                    "F[market]: 5 competitors |source:independent-research:T2|\n"
                    "DA grade: B+\n"
                    "XVERIFY[openai:gpt-4o] verified\n"
                ),
            },
        }, home)
        assert result.returncode == 0

        cal = agent_dir / "calibration.md"
        assert cal.exists()
        content = cal.read_text()
        assert "findings:" in content
        assert "da-grade: B+" in content


# ─── code-debt-watcher.py ───


class TestDebtWatcherIntegration:
    def test_exits_clean_on_non_code_file(self):
        result = run_hook("code-debt-watcher.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/some/readme.md", "content": "# Hello"},
        })
        assert result.returncode == 0

    def test_exits_clean_without_build_workspace(self, tmp_path):
        """No build workspace → exits without scanning."""
        home = tmp_path / "home"
        (home / ".claude" / "teams" / "sigma-build" / "shared").mkdir(parents=True)

        result = run_hook("code-debt-watcher.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/proj/auth.py", "content": "except:\n    pass"},
        }, home)
        assert result.returncode == 0

    def test_detects_debt_during_build(self, tmp_path):
        """With active build workspace, detects fragile patterns."""
        home = tmp_path / "home"
        shared = home / ".claude" / "teams" / "sigma-build" / "shared"
        shared.mkdir(parents=True)

        ws = shared / "workspace.md"
        ws.write_text("## build-track\nActive\n## 04-build\nBuilding\n", encoding="utf-8")

        result = run_hook("code-debt-watcher.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/proj/handler.py",
                "content": "def process():\n    try:\n        do_thing()\n    except:\n        pass\n",
            },
        }, home)
        assert result.returncode == 0

        content = ws.read_text()
        assert "code-debt-watch" in content
        assert "error-swallowing" in content


# ─── skill-evolution-tracker.py ───


class TestSkillTrackerIntegration:
    def test_exits_clean_on_non_skill_read(self):
        result = run_hook("skill-evolution-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/Users/test/project/src/main.py"},
        })
        assert result.returncode == 0

    def test_logs_skill_read(self, tmp_path):
        home = tmp_path / "home"
        skills_dir = home / ".claude" / "skills" / "loan-agency"
        skills_dir.mkdir(parents=True)

        result = run_hook("skill-evolution-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": str(skills_dir / "SKILL.md")},
        }, home)
        assert result.returncode == 0

        log = home / ".claude" / "skills" / ".skill-usage.jsonl"
        assert log.exists()
        entry = json.loads(log.read_text().strip())
        assert entry["skill"] == "loan-agency"
        assert entry["tier"] == "router"

    def test_ignores_index_read(self, tmp_path):
        home = tmp_path / "home"
        (home / ".claude" / "skills").mkdir(parents=True)

        result = run_hook("skill-evolution-tracker.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": str(home / ".claude" / "skills" / "INDEX.md")},
        }, home)
        assert result.returncode == 0

        log = home / ".claude" / "skills" / ".skill-usage.jsonl"
        assert not log.exists()


# ─── prompt-echo-detector.py ───


class TestEchoDetectorIntegration:
    def test_exits_clean_on_non_workspace_write(self):
        result = run_hook("prompt-echo-detector.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/proj/src/main.py", "content": "print('hello')"},
        })
        assert result.returncode == 0

    def test_exits_clean_without_review_workspace(self, tmp_path):
        home = tmp_path / "home"
        (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)

        result = run_hook("prompt-echo-detector.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/workspace.md", "content": "stuff " * 50},
        }, home)
        assert result.returncode == 0


# ─── shadow-mode.py ───


class TestShadowModeIntegration:
    def test_exits_clean_on_non_skill_read(self):
        result = run_hook("shadow-mode.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/Users/test/project/main.py"},
        })
        assert result.returncode == 0

    def test_exits_clean_on_skill_without_shadow(self, tmp_path):
        home = tmp_path / "home"
        (home / ".claude" / "skills" / "plain-skill").mkdir(parents=True)

        result = run_hook("shadow-mode.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": str(home / ".claude" / "skills" / "plain-skill" / "SKILL.md")},
        }, home)
        assert result.returncode == 0

    def test_tracks_shadow_invocation(self, tmp_path):
        home = tmp_path / "home"
        skill_dir = home / ".claude" / "skills" / "test-skill"
        shadow_dir = skill_dir / ".shadow"
        shadow_dir.mkdir(parents=True)

        (shadow_dir / "SKILL.md.current").write_text("# Current\nTrigger: test\n")
        (shadow_dir / "SKILL.md.proposed").write_text("# Proposed\nTrigger: test, new\n")
        (shadow_dir / "config.json").write_text(json.dumps({
            "status": "active",
            "started": "2026-04-01",
            "invocations": 0,
            "target_invocations": 5,
            "change_description": "Added trigger",
            "comparisons": [],
        }))

        result = run_hook("shadow-mode.py", {
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": str(skill_dir / "SKILL.md")},
        }, home)
        assert result.returncode == 0

        config = json.loads((shadow_dir / "config.json").read_text())
        assert config["invocations"] == 1
        assert len(config.get("comparisons", [])) == 1


# ─── Cross-cutting ───


class TestAllHooksHandleGarbage:
    """Every hook should handle garbage stdin gracefully."""

    @pytest.mark.parametrize("script", sorted([
        "sigma-retrospective.py",
        "agent-calibration-tracker.py",
        "code-debt-watcher.py",
        "skill-evolution-tracker.py",
        "prompt-echo-detector.py",
        "shadow-mode.py",
    ]))
    def test_garbage_stdin(self, script):
        script_path = HOOKS_DIR / script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input="not json at all {{{}}}",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0

    @pytest.mark.parametrize("script", sorted([
        "sigma-retrospective.py",
        "agent-calibration-tracker.py",
        "code-debt-watcher.py",
        "skill-evolution-tracker.py",
        "prompt-echo-detector.py",
        "shadow-mode.py",
    ]))
    def test_empty_stdin(self, script):
        script_path = HOOKS_DIR / script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0

    @pytest.mark.parametrize("script", sorted([
        "sigma-retrospective.py",
        "agent-calibration-tracker.py",
        "code-debt-watcher.py",
        "skill-evolution-tracker.py",
        "prompt-echo-detector.py",
        "shadow-mode.py",
    ]))
    def test_wrong_event_type(self, script):
        """Scripts should handle events they don't care about."""
        result = run_hook(script, {
            "hook_event_name": "SessionStart",
            "tool_name": "irrelevant",
        })
        assert result.returncode == 0


class TestAllHooksReturnValidJson:
    """When hooks produce output, it must be valid JSON."""

    def test_retro_output_is_json(self, tmp_path):
        home = tmp_path / "home"
        shared = home / ".claude" / "teams" / "sigma-review" / "shared"
        shared.mkdir(parents=True)
        (shared / "workspace.md").write_text("## convergence\na: ✓ done\n")
        (shared / "patterns.md").write_text("")

        result = run_hook("sigma-retrospective.py", {"hook_event_name": "Stop"}, home)
        if result.stdout.strip():
            parsed = json.loads(result.stdout)
            assert isinstance(parsed, dict)
