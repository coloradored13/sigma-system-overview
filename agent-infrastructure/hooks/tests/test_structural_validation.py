"""Structural validation tests.

Verify the entire installed structure is consistent:
- All skills have valid SKILL.md with frontmatter
- settings.json hooks reference real executable scripts
- Agent-skill mappings reference real skills

Note: TestIndexMd, TestTemplateBootUpdate, and TestPreflightSocraticConditional
were removed when INDEX.md was retired (commit fd00a9d, 2026-04-15) and
phase-based sigma-review was retired in favor of the atomic checklist model
(commit 79bbae5, 2026-04-15).
"""
import json
import os
import re
import stat
from pathlib import Path

import pytest

from conftest import get_infra_dir

CLAUDE_DIR = get_infra_dir()
SKILLS_DIR = CLAUDE_DIR / "skills"
HOOKS_DIR = CLAUDE_DIR / "hooks"
AGENTS_DIR = CLAUDE_DIR / "agents"


# --- Expected skills from the v3 package ---

EXPECTED_SKILLS = {
    # Capability
    "research-analysis", "structured-writing", "review-critique",
    "process-design", "data-analysis", "planning-prioritization", "reporting",
    # Domain
    "loan-agency", "legal", "engineering", "finance-accounting", "bio-research",
    # Orchestrator
    "product-ops", "design-ops", "competitive-brief",
    # Execution-layer
    "query", "visualize", "financial-close", "bio-tools",
    # Behavioral
    "socratic-grill", "negotiation-coach",
    # Passive
    "passive-bootstrap", "skill-improver", "assumption-surfacer",
    "skill-identifier", "memory-compiler",
    # v3 new
    "sigmacomm", "persistent-wiki", "research-harvester",
}

EXPECTED_SIGMA_SKILLS = {
    "sigma-review", "sigma-build", "sigma-audit", "sigma-evaluate",
    "sigma-feedback", "sigma-research", "sigma-retrieve", "sigma-optimize",
    "sigma-dream", "sigma-single", "sigma-init",
}

EXPECTED_HOOKS = {
    "sigma-retrospective.py",
    "agent-calibration-tracker.py",
    "code-debt-watcher.py",
    "skill-evolution-tracker.py",
    "prompt-echo-detector.py",
    "shadow-mode.py",
}


class TestSkillsInstalled:
    def test_all_29_skills_present(self):
        installed = {d.name for d in SKILLS_DIR.iterdir()
                     if d.is_dir() and not d.name.startswith(".")}
        for skill in EXPECTED_SKILLS:
            assert skill in installed, f"Missing skill: {skill}"

    def test_sigma_skills_untouched(self):
        installed = {d.name for d in SKILLS_DIR.iterdir()
                     if d.is_dir() and d.name.startswith("sigma-")}
        for skill in EXPECTED_SIGMA_SKILLS:
            assert skill in installed, f"Missing sigma skill: {skill}"

    def test_mcp_builder_still_present(self):
        assert (SKILLS_DIR / "mcp-builder").is_dir()

    def test_total_skill_count(self):
        """29 new + 11 sigma + mcp-builder = 41 skill dirs."""
        dirs = [d for d in SKILLS_DIR.iterdir()
                if d.is_dir() and not d.name.startswith(".")]
        assert len(dirs) >= 41, f"Expected ≥41 skill dirs, got {len(dirs)}"


class TestSkillMdValidity:
    @pytest.fixture(params=sorted(EXPECTED_SKILLS))
    def skill_name(self, request):
        return request.param

    def test_skill_has_skill_md(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        assert skill_md.exists(), f"{skill_name}/SKILL.md missing"

    def test_skill_md_has_frontmatter(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{skill_name}/SKILL.md missing frontmatter"
        # Should have closing ---
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{skill_name}/SKILL.md frontmatter not closed"

    def test_skill_md_has_name_field(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        frontmatter = content.split("---")[1]
        assert "name:" in frontmatter, f"{skill_name}/SKILL.md missing name in frontmatter"

    def test_skill_md_has_description(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        frontmatter = content.split("---")[1]
        assert "description:" in frontmatter, f"{skill_name}/SKILL.md missing description"

    def test_skill_md_not_empty(self, skill_name):
        skill_md = SKILLS_DIR / skill_name / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        # Content after frontmatter should be substantive
        body = content.split("---", 2)[2] if len(content.split("---", 2)) > 2 else ""
        assert len(body.strip()) > 50, f"{skill_name}/SKILL.md body too short"


class TestLoanAgencyTieredRefs:
    """Loan-agency has the richest reference structure — verify tiers."""

    def test_has_quick_refs(self):
        refs = SKILLS_DIR / "loan-agency" / "references"
        qr_files = list(refs.glob("qr-*.md"))
        assert len(qr_files) >= 4, f"Expected ≥4 quick-ref files, got {len(qr_files)}"

    def test_has_full_docs(self):
        refs = SKILLS_DIR / "loan-agency" / "references"
        doc_files = list(refs.glob("Doc*.md"))
        assert len(doc_files) >= 6, f"Expected ≥6 Doc files, got {len(doc_files)}"

    def test_has_operational_refs(self):
        refs = SKILLS_DIR / "loan-agency" / "references"
        op_files = list(refs.glob("loan-agency-*.md"))
        assert len(op_files) >= 5, f"Expected ≥5 operational files, got {len(op_files)}"


class TestSettingsJsonHooks:
    def test_settings_valid_json(self):
        settings = CLAUDE_DIR / "settings.json"
        content = json.loads(settings.read_text(encoding="utf-8"))
        assert "hooks" in content

    def test_has_stop_hook(self):
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        assert "Stop" in content["hooks"]

    def test_has_post_tool_use_hooks(self):
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        assert "PostToolUse" in content["hooks"]

    def test_all_hook_scripts_exist(self):
        for script in EXPECTED_HOOKS:
            assert (HOOKS_DIR / script).exists(), f"Hook script missing: {script}"

    def test_all_hook_scripts_executable(self):
        for script in EXPECTED_HOOKS:
            path = HOOKS_DIR / script
            assert os.access(path, os.X_OK), f"Hook script not executable: {script}"

    def test_all_hook_scripts_compile(self):
        """All scripts should be syntactically valid Python."""
        import py_compile
        for script in EXPECTED_HOOKS:
            path = HOOKS_DIR / script
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as e:
                pytest.fail(f"{script} has syntax error: {e}")

    def test_hook_matchers_reference_valid_tools(self):
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        valid_tools = {"Read", "Write", "Edit", "Bash", "Glob", "Grep",
                       "SendMessage", "Agent", "WebFetch", "WebSearch"}
        for event_name, matchers in content["hooks"].items():
            for matcher_group in matchers:
                matcher = matcher_group.get("matcher", "")
                if matcher:  # Empty matcher = match all
                    for tool in matcher.split("|"):
                        # MCP tool names start with mcp__ — valid by convention
                        if tool.startswith("mcp__"):
                            continue
                        assert tool in valid_tools, \
                            f"Hook matcher references unknown tool '{tool}' in {event_name}"

    def test_hook_commands_reference_existing_scripts(self):
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        for event_name, matchers in content["hooks"].items():
            for matcher_group in matchers:
                for hook in matcher_group.get("hooks", []):
                    cmd = hook.get("command", "")
                    # Extract script path from command
                    parts = cmd.split()
                    if len(parts) >= 2:
                        raw = parts[-1]
                        # settings.json uses ~/.claude/... paths that resolve via
                        # symlink on the user's machine. For CI (or any machine
                        # without the symlink), rewrite to the in-repo location.
                        if raw.startswith("~/.claude/"):
                            script_path = CLAUDE_DIR / raw[len("~/.claude/"):]
                        else:
                            script_path = Path(os.path.expanduser(raw))
                        assert script_path.exists(), \
                            f"Hook command references missing script: {cmd} (resolved: {script_path})"

    def test_existing_settings_preserved(self):
        """Original settings should still be present."""
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        assert content.get("env", {}).get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
        assert content.get("effortLevel") == "high"
        assert content.get("autoDreamEnabled") is True
        assert content.get("voiceEnabled") is True
        assert "statusLine" in content
