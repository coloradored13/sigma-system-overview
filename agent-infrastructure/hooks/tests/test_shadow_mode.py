"""Tests for shadow-mode.py — PostToolUse hook on Read (SKILL.md)."""
import sys
import json
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
shadow = importlib.import_module("shadow-mode")


@pytest.fixture
def shadow_skill(tmp_path, monkeypatch):
    """Create a skill with active shadow config."""
    skills_dir = tmp_path / "skills"
    monkeypatch.setattr(shadow, "SKILLS_DIR", skills_dir)

    skill_dir = skills_dir / "test-skill"
    shadow_dir = skill_dir / ".shadow"
    shadow_dir.mkdir(parents=True)

    # Current version
    (shadow_dir / "SKILL.md.current").write_text(
        "---\nname: test-skill\n---\n# Test Skill\nTrigger: test, check\n## Mode: Standard\nStandard rigor level\n",
        encoding="utf-8",
    )

    # Proposed version (different triggers)
    (shadow_dir / "SKILL.md.proposed").write_text(
        "---\nname: test-skill\n---\n# Test Skill\nTrigger: test, check, validate\n## Mode: Standard\n## Mode: Rigorous\nStandard and rigorous rigor levels\n",
        encoding="utf-8",
    )

    # Config
    config = {
        "status": "active",
        "started": "2026-04-01",
        "invocations": 0,
        "target_invocations": 5,
        "change_description": "Added validate trigger and rigorous mode",
        "comparisons": [],
    }
    (shadow_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")

    return skills_dir, skill_dir


class TestGetShadowConfig:
    def test_reads_active_config(self, shadow_skill, monkeypatch):
        skills_dir, _ = shadow_skill
        config = shadow.get_shadow_config("test-skill")
        assert config is not None
        assert config["status"] == "active"
        assert config["target_invocations"] == 5

    def test_returns_none_for_no_shadow(self, tmp_path, monkeypatch):
        skills_dir = tmp_path / "skills"
        (skills_dir / "plain-skill").mkdir(parents=True)
        monkeypatch.setattr(shadow, "SKILLS_DIR", skills_dir)

        assert shadow.get_shadow_config("plain-skill") is None

    def test_returns_none_for_inactive(self, shadow_skill, monkeypatch):
        skills_dir, skill_dir = shadow_skill
        config_path = skill_dir / ".shadow" / "config.json"
        config = json.loads(config_path.read_text())
        config["status"] = "completed"
        config_path.write_text(json.dumps(config))

        assert shadow.get_shadow_config("test-skill") is None


class TestLogInvocation:
    def test_increments_count(self, shadow_skill, monkeypatch):
        skills_dir, _ = shadow_skill
        config = shadow.get_shadow_config("test-skill")
        assert config["invocations"] == 0

        count = shadow.log_invocation("test-skill", config)
        assert count == 1

        # Re-read config from disk
        config2 = shadow.get_shadow_config("test-skill")
        assert config2["invocations"] == 1


class TestCompareRouting:
    def test_detects_trigger_differences(self):
        current = "Trigger: test, check\n"
        proposed = "Trigger: test, check, validate\n"
        result = shadow.compare_routing(current, proposed)
        assert result["trigger_diff"] is True

    def test_no_diff_identical(self):
        content = "Trigger: test\n## Mode: Standard\nrigor level\n"
        result = shadow.compare_routing(content, content)
        assert result["trigger_diff"] is False
        assert result["rigor_diff"] is False
        assert result["mode_diff"] is False
        assert result["size_delta"] == 0

    def test_detects_mode_differences(self):
        current = "## Mode: Standard\nstuff\n"
        proposed = "## Mode: Standard\nstuff\n## Mode: Rigorous\nmore stuff\n"
        result = shadow.compare_routing(current, proposed)
        assert result["mode_diff"] is True

    def test_size_delta(self):
        current = "line 1\nline 2\n"
        proposed = "line 1\nline 2\nline 3\nline 4\n"
        result = shadow.compare_routing(current, proposed)
        assert result["size_delta"] == 2


class TestCheckGraduation:
    def test_not_ready(self, shadow_skill, monkeypatch):
        config = shadow.get_shadow_config("test-skill")
        config["invocations"] = 3  # Below target of 5
        report = shadow.check_graduation("test-skill", config)
        assert report is None

    def test_graduates_on_low_divergence(self, shadow_skill, monkeypatch):
        _, skill_dir = shadow_skill
        config = shadow.get_shadow_config("test-skill")
        config["invocations"] = 5
        config["comparisons"] = [
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
        ]
        report = shadow.check_graduation("test-skill", config)
        assert report is not None
        assert report["verdict"] == "graduate"

        # Check report file written
        report_path = skill_dir / ".shadow" / "report.md"
        assert report_path.exists()
        assert "graduate" in report_path.read_text().lower()

    def test_extends_on_high_divergence(self, shadow_skill, monkeypatch):
        config = shadow.get_shadow_config("test-skill")
        config["invocations"] = 5
        config["comparisons"] = [
            {"trigger_diff": True, "rigor_diff": True, "mode_diff": True},
            {"trigger_diff": True, "rigor_diff": True, "mode_diff": False},
            {"trigger_diff": True, "rigor_diff": False, "mode_diff": True},
            {"trigger_diff": True, "rigor_diff": True, "mode_diff": True},
            {"trigger_diff": False, "rigor_diff": True, "mode_diff": True},
        ]
        report = shadow.check_graduation("test-skill", config)
        assert report is not None
        assert report["verdict"] == "extend"

    def test_extends_on_moderate_divergence(self, shadow_skill, monkeypatch):
        config = shadow.get_shadow_config("test-skill")
        config["invocations"] = 5
        config["comparisons"] = [
            {"trigger_diff": True, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": True, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
            {"trigger_diff": False, "rigor_diff": False, "mode_diff": False},
        ]
        report = shadow.check_graduation("test-skill", config)
        assert report is not None
        assert report["verdict"] == "extend"


class TestReadSkillVersion:
    def test_reads_current(self, shadow_skill, monkeypatch):
        content = shadow.read_skill_version("test-skill", "current")
        assert "Test Skill" in content

    def test_reads_proposed(self, shadow_skill, monkeypatch):
        content = shadow.read_skill_version("test-skill", "proposed")
        assert "validate" in content

    def test_returns_empty_for_missing(self, shadow_skill, monkeypatch):
        content = shadow.read_skill_version("test-skill", "nonexistent")
        assert content == ""
