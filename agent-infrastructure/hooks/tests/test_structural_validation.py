"""Structural validation tests.

Verify the entire installed structure is consistent:
- All skills have valid SKILL.md with frontmatter
- INDEX.md categories reference actual skill dirs
- _template.md has step 2a in correct boot position
- 00-preflight.md has socratic-session conditional
- settings.json hooks reference real executable scripts
- Agent-skill mappings reference real skills
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


class TestIndexMd:
    def test_index_exists(self):
        assert (SKILLS_DIR / "INDEX.md").exists()

    def test_has_capability_section(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Capability Skills" in content

    def test_has_domain_section(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Domain Skills" in content

    def test_has_orchestrator_section(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Orchestrator Skills" in content

    def test_has_passive_section(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Passive Skills" in content

    def test_has_behavioral_section(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Behavioral Skills" in content

    def test_has_agent_boot_integration(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "## Agent Boot Integration" in content

    def test_has_agent_skill_mapping(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        assert "loan-ops-tech-specialist" in content
        assert "product-strategist" in content
        assert "tech-architect" in content

    def test_all_new_skills_in_index(self):
        content = (SKILLS_DIR / "INDEX.md").read_text(encoding="utf-8")
        for skill in EXPECTED_SKILLS:
            assert skill in content, f"Skill {skill} not found in INDEX.md"


class TestTemplateBootUpdate:
    def test_template_exists(self):
        assert (AGENTS_DIR / "_template.md").exists()

    def test_has_step_2a(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        assert "2a→skill-load" in content

    def test_step_2a_between_memory_and_inbox(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        pos_2 = content.find("2→memory.md")
        pos_2a = content.find("2a→skill-load")
        pos_3 = content.find("3→inbox")
        assert pos_2 < pos_2a < pos_3, "Step 2a not between step 2 (memory) and step 3 (inbox)"

    def test_has_progressive_disclosure_rules(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        assert "## Skill Progressive Disclosure" in content
        assert "Tier 1" in content or "Tier 2" in content

    def test_has_skill_source_tagging(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        assert "|source:skill(" in content

    def test_has_max_2_budget(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        assert "max 2 skill routers" in content

    def test_has_conflict_rule(self):
        content = (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")
        assert "CONFLICT" in content


class TestPreflightSocraticConditional:
    def test_preflight_exists(self):
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        assert preflight.exists()

    def test_has_socratic_conditional(self):
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        assert "socratic-session" in content

    def test_has_warm_decomposition_path(self):
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        assert "socratic-warm" in content

    def test_has_cold_extraction_fallback(self):
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        assert "IF no socratic-session" in content

    def test_still_hard_gate(self):
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        assert "HARD GATE" in content

    def test_original_steps_preserved(self):
        """Original preflight steps should still exist."""
        preflight = SKILLS_DIR / "sigma-review" / "phases" / "00-preflight.md"
        content = preflight.read_text(encoding="utf-8")
        assert "### Step 1: Memory Recall" in content
        assert "### Step 5: Complexity Assessment" in content
        assert "### Step 9: Cost Estimate" in content
        assert "## Exit Checklist" in content


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
                        script_path = Path(os.path.expanduser(parts[-1]))
                        assert script_path.exists(), \
                            f"Hook command references missing script: {cmd}"

    def test_existing_settings_preserved(self):
        """Original settings should still be present."""
        content = json.loads((CLAUDE_DIR / "settings.json").read_text())
        assert content.get("env", {}).get("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS") == "1"
        assert content.get("effortLevel") == "high"
        assert content.get("autoDreamEnabled") is True
        assert content.get("voiceEnabled") is True
        assert "statusLine" in content
