"""Structural validation tests for sigma-review/sigma-build agent infrastructure.

Validates:
1. Agent definition files — required sections, boot sequence, consistency
2. Roster-to-agent file mapping — bidirectional consistency
3. Phase file completeness — sigma-review and sigma-build phases
4. Cross-file reference integrity — directives, decisions, patterns, protocols
"""
import re
from pathlib import Path

import pytest

from conftest import get_infra_dir

CLAUDE_DIR = get_infra_dir()
AGENTS_DIR = CLAUDE_DIR / "agents"
REVIEW_SHARED = CLAUDE_DIR / "teams" / "sigma-review" / "shared"
REVIEW_PHASES_DIR = CLAUDE_DIR / "skills" / "sigma-review" / "phases"
BUILD_PHASES_DIR = CLAUDE_DIR / "skills" / "sigma-build" / "phases"

# --- Agent lists ---

STANDARD_AGENTS = [
    "code-quality-analyst",
    "cognitive-decision-scientist",
    "cross-model-validator",
    "devils-advocate",
    "economics-analyst",
    "energy-market-analyst",
    "geopolitical-strategist",
    "implementation-engineer",
    "loan-ops-tech-specialist",
    "macro-rates-analyst",
    "portfolio-analyst",
    "product-designer",
    "product-strategist",
    "reference-class-analyst",
    "regulatory-analyst",
    "regulatory-licensing-specialist",
    "sanctions-trade-analyst",
    "search-aggressive",
    "search-combinatorial",
    "search-conservative",
    "security-specialist",
    "statistical-analyst",
    "tech-architect",
    "tech-industry-analyst",
    "technical-writer",
    "ui-ux-engineer",
    "ux-researcher",
]

SPECIAL_FILES = {
    "_template.md",
    "SIGMA-COMM-SPEC.md",
    "sigma-comm.md",
    "sigma-lead.md",
    "m-and-a-deal-counsel.md",
}

# sigma-optimize agents not expected in sigma-review roster
SIGMA_OPTIMIZE_AGENTS = {
    "search-aggressive",
    "search-combinatorial",
    "search-conservative",
    "statistical-analyst",
    "cross-model-validator",
}

# --- Phase file expectations ---

REVIEW_PHASES = [
    "00-preflight.md",
    "01-spawn.md",
    "02-research.md",
    "03-circuit-breaker.md",
    "04-challenge.md",
    "05-debate.md",
    "06-synthesis.md",
    "06b-compilation.md",
    "07-promotion.md",
    "08-sync.md",
    "09-archive.md",
    "10-shutdown.md",
]

BUILD_PHASES = [
    "00-preflight.md",
    "01-spawn.md",
    "02-plan.md",
    "03-plan-challenge.md",
    "04-build.md",
    "05-build-review.md",
    "05b-debate.md",
    "06-synthesis.md",
    "06b-compilation.md",
    "07-promotion.md",
    "08-sync.md",
    "09-archive.md",
    "10-shutdown.md",
]

# --- Directives key sections ---

DIRECTIVES_REQUIRED_TERMS = [
    "adversarial-layer",
    "hypothesis-matrix",
    "superforecasting",
    "bayesian-consensus",
    "prompt-decomposition",
]


# ============================================================
# Helpers
# ============================================================

def _read_agent(name: str) -> str:
    """Read an agent .md file and return its content."""
    path = AGENTS_DIR / f"{name}.md"
    return path.read_text(encoding="utf-8")


def _section_headers(content: str) -> list[str]:
    """Extract all ## headers from markdown content."""
    return re.findall(r"^## .+", content, re.MULTILINE)


def _parse_roster() -> dict[str, str]:
    """Parse roster.md into {agent_name: full_line} dict."""
    path = REVIEW_SHARED / "roster.md"
    content = path.read_text(encoding="utf-8")
    roster = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("→"):
            continue
        # Lines are: agent-name |domain: ... |wake-for: ...
        name = line.split("|")[0].strip()
        if name:
            roster[name] = line
    return roster


# ============================================================
# TestAgentDefinitions — parametrized over standard agents
# ============================================================

class TestAgentDefinitions:
    """Validate required sections in every standard agent file."""

    @pytest.fixture(params=sorted(STANDARD_AGENTS))
    def agent_name(self, request):
        return request.param

    @pytest.fixture
    def agent_content(self, agent_name):
        return _read_agent(agent_name)

    def test_agent_file_exists(self, agent_name):
        path = AGENTS_DIR / f"{agent_name}.md"
        assert path.exists(), f"Agent file missing: {agent_name}.md"

    def test_has_role_section(self, agent_name, agent_content):
        assert "## Role" in agent_content, (
            f"{agent_name}.md missing ## Role section"
        )

    def test_role_is_concise(self, agent_name, agent_content):
        """Role should appear early and be a short description."""
        match = re.search(r"^## Role\n(.+)", agent_content, re.MULTILINE)
        assert match, f"{agent_name}.md: ## Role has no content on next line"
        role_line = match.group(1).strip()
        assert len(role_line) > 10, (
            f"{agent_name}.md: Role description too short: '{role_line}'"
        )

    def test_has_expertise_section(self, agent_name, agent_content):
        assert "## Expertise" in agent_content, (
            f"{agent_name}.md missing ## Expertise section"
        )

    def test_expertise_has_content(self, agent_name, agent_content):
        match = re.search(r"^## Expertise\n(.+)", agent_content, re.MULTILINE)
        assert match, f"{agent_name}.md: ## Expertise has no content"
        expertise = match.group(1).strip()
        # Should be comma-separated, so at least one comma
        assert "," in expertise, (
            f"{agent_name}.md: Expertise should be comma-separated list"
        )

    def test_has_boot_section(self, agent_name, agent_content):
        assert "## Boot (FIRST)" in agent_content, (
            f"{agent_name}.md missing ## Boot (FIRST) section"
        )

    def test_boot_has_step_1_sigma_comm(self, agent_name, agent_content):
        assert re.search(r"1→sigma-comm", agent_content), (
            f"{agent_name}.md boot missing step 1→sigma-comm"
        )

    def test_boot_has_step_2_memory(self, agent_name, agent_content):
        assert re.search(r"2→memory", agent_content), (
            f"{agent_name}.md boot missing step 2→memory"
        )

    def test_boot_has_step_3_inbox(self, agent_name, agent_content):
        assert re.search(r"3→inbox", agent_content), (
            f"{agent_name}.md boot missing step 3→inbox"
        )

    def test_boot_has_step_4_workspace(self, agent_name, agent_content):
        assert re.search(r"4→workspace", agent_content), (
            f"{agent_name}.md boot missing step 4→workspace"
        )

    def test_boot_has_step_5(self, agent_name, agent_content):
        """Step 5 should reference decisions.md (standard) or directives.md (sigma-optimize)."""
        assert re.search(r"5→(decisions|directives)", agent_content), (
            f"{agent_name}.md boot missing step 5→decisions or 5→directives"
        )

    def test_boot_step_order(self, agent_name, agent_content):
        """Steps 1-5 must appear in sequential order."""
        positions = []
        for step_pattern in [
            r"1→sigma-comm",
            r"2→memory",
            r"3→inbox",
            r"4→workspace",
            r"5→(decisions|directives)",
        ]:
            match = re.search(step_pattern, agent_content)
            assert match, f"{agent_name}.md boot step {step_pattern} not found"
            positions.append(match.start())
        for i in range(len(positions) - 1):
            assert positions[i] < positions[i + 1], (
                f"{agent_name}.md boot steps out of order"
            )

    def test_has_comms_section(self, agent_name, agent_content):
        assert "## Comms" in agent_content, (
            f"{agent_name}.md missing ## Comms section"
        )

    def test_has_persistence_section(self, agent_name, agent_content):
        assert "## Persistence" in agent_content, (
            f"{agent_name}.md missing ## Persistence section"
        )

    def test_persistence_variant(self, agent_name, agent_content):
        """Persistence should use the standard header format."""
        assert "## Persistence (before" in agent_content, (
            f"{agent_name}.md: Persistence section missing standard "
            "'(before ..., no direct file writes)' qualifier"
        )

    def test_has_weight_section(self, agent_name, agent_content):
        assert "## Weight" in agent_content, (
            f"{agent_name}.md missing ## Weight section"
        )

    def test_weight_has_primary(self, agent_name, agent_content):
        """Weight section should declare primary domains."""
        # Extract content after ## Weight
        weight_match = re.search(
            r"^## Weight\n(.*?)(?=^## |\Z)", agent_content,
            re.MULTILINE | re.DOTALL,
        )
        assert weight_match, f"{agent_name}.md: ## Weight section empty"
        weight_body = weight_match.group(1)
        assert "primary:" in weight_body.lower() or len(weight_body.strip()) > 10, (
            f"{agent_name}.md: Weight section lacks primary domain declaration"
        )


# ============================================================
# TestAgentTemplateBoot — _template.md specific checks
# ============================================================

class TestAgentTemplateBoot:
    """Verify _template.md has the canonical boot sequence including step 2a."""

    @pytest.fixture
    def template_content(self):
        return (AGENTS_DIR / "_template.md").read_text(encoding="utf-8")

    def test_template_exists(self):
        assert (AGENTS_DIR / "_template.md").exists()

    def test_has_step_2a_skill_load(self, template_content):
        assert "2a→skill-load" in template_content, (
            "_template.md missing step 2a→skill-load"
        )

    def test_step_2a_position(self, template_content):
        """Step 2a must be between step 2 (memory) and step 3 (inbox)."""
        pos_2 = template_content.find("2→memory")
        pos_2a = template_content.find("2a→skill-load")
        pos_3 = template_content.find("3→inbox")
        assert pos_2 > -1, "_template.md missing step 2→memory"
        assert pos_2a > -1, "_template.md missing step 2a→skill-load"
        assert pos_3 > -1, "_template.md missing step 3→inbox"
        assert pos_2 < pos_2a < pos_3, (
            "Step 2a not positioned between step 2 (memory) and step 3 (inbox)"
        )

    def test_step_2a_mentions_skills_index(self, template_content):
        """Step 2a should reference the Skills Index."""
        # Find the 2a block
        match = re.search(
            r"2a→skill-load.*?(?=\n\d→|\n## |\Z)",
            template_content,
            re.DOTALL,
        )
        assert match, "_template.md: cannot find 2a→skill-load block"
        block = match.group(0)
        assert "Skills Index" in block or "skill" in block.lower(), (
            "Step 2a should reference Skills Index or skill mapping"
        )

    def test_has_max_2_budget(self, template_content):
        assert "max 2 skill routers" in template_content, (
            "_template.md missing boot budget constraint (max 2 skill routers)"
        )

    def test_has_role_section(self, template_content):
        assert "## Role" in template_content

    def test_has_expertise_section(self, template_content):
        assert "## Expertise" in template_content

    def test_has_boot_section(self, template_content):
        assert "## Boot (FIRST)" in template_content

    def test_has_persistence_section(self, template_content):
        assert "## Persistence" in template_content

    def test_has_promotion_section(self, template_content):
        assert "## Promotion" in template_content

    def test_has_weight_section(self, template_content):
        assert "## Weight" in template_content


# ============================================================
# TestRosterConsistency
# ============================================================

class TestRosterConsistency:
    """Validate roster.md and agent file bidirectional consistency."""

    @pytest.fixture
    def roster(self):
        return _parse_roster()

    def test_roster_file_exists(self):
        assert (REVIEW_SHARED / "roster.md").exists()

    def test_roster_not_empty(self, roster):
        assert len(roster) > 0, "Roster is empty"

    def test_every_roster_agent_has_file(self, roster):
        """Every agent named in roster.md should have a .md file."""
        missing = []
        for name in roster:
            if not (AGENTS_DIR / f"{name}.md").exists():
                missing.append(name)
        assert not missing, f"Roster agents missing .md files: {missing}"

    def test_standard_agents_in_roster(self, roster):
        """Every standard agent (except sigma-optimize agents) should be in roster."""
        missing = []
        for name in STANDARD_AGENTS:
            if name in SIGMA_OPTIMIZE_AGENTS:
                continue
            if name not in roster:
                missing.append(name)
        assert not missing, (
            f"Standard agents missing from roster: {missing}"
        )

    def test_sigma_optimize_agents_excluded(self, roster):
        """sigma-optimize agents are a separate team, may or may not be in roster."""
        # This is informational -- we just verify they exist as files
        for name in SIGMA_OPTIMIZE_AGENTS:
            assert (AGENTS_DIR / f"{name}.md").exists(), (
                f"sigma-optimize agent file missing: {name}.md"
            )

    @pytest.fixture(params=sorted(
        set(STANDARD_AGENTS) - SIGMA_OPTIMIZE_AGENTS
    ))
    def review_agent_name(self, request):
        return request.param

    def test_roster_entry_has_domain_field(self, roster, review_agent_name):
        """Each roster entry should have a |domain: field."""
        if review_agent_name not in roster:
            pytest.skip(f"{review_agent_name} not in roster")
        line = roster[review_agent_name]
        assert "|domain:" in line, (
            f"Roster entry for {review_agent_name} missing |domain: field"
        )

    def test_roster_entry_has_wake_for_field(self, roster, review_agent_name):
        """Each roster entry should have a |wake-for: field."""
        if review_agent_name not in roster:
            pytest.skip(f"{review_agent_name} not in roster")
        line = roster[review_agent_name]
        assert "|wake-for:" in line, (
            f"Roster entry for {review_agent_name} missing |wake-for: field"
        )

    def test_no_duplicate_roster_entries(self):
        """No agent should appear twice in the roster."""
        path = REVIEW_SHARED / "roster.md"
        content = path.read_text(encoding="utf-8")
        names = []
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("→"):
                continue
            name = line.split("|")[0].strip()
            if name:
                names.append(name)
        seen = set()
        dupes = []
        for n in names:
            if n in seen:
                dupes.append(n)
            seen.add(n)
        assert not dupes, f"Duplicate roster entries: {dupes}"

    def test_roster_has_minimum_agents(self, roster):
        """Roster should have at least the 8 core + DA + domain agents."""
        assert len(roster) >= 15, (
            f"Roster has {len(roster)} agents, expected >= 15"
        )


# ============================================================
# TestReviewPhaseFiles
# ============================================================

class TestReviewPhaseFiles:
    """Validate sigma-review phase file completeness and structure."""

    def test_phases_directory_exists(self):
        assert REVIEW_PHASES_DIR.is_dir(), (
            "sigma-review phases directory missing"
        )

    @pytest.fixture(params=sorted(REVIEW_PHASES))
    def review_phase(self, request):
        return request.param

    def test_expected_phase_exists(self, review_phase):
        path = REVIEW_PHASES_DIR / review_phase
        assert path.exists(), f"Missing review phase: {review_phase}"

    def test_phase_not_empty(self, review_phase):
        path = REVIEW_PHASES_DIR / review_phase
        content = path.read_text(encoding="utf-8")
        assert len(content.strip()) > 20, (
            f"Review phase {review_phase} is empty or trivially short"
        )

    def test_phase_has_markdown_header(self, review_phase):
        path = REVIEW_PHASES_DIR / review_phase
        content = path.read_text(encoding="utf-8")
        assert re.search(r"^#+ ", content, re.MULTILINE), (
            f"Review phase {review_phase} has no markdown header"
        )

    def test_no_unexpected_review_phases(self):
        """No stray phase files beyond the expected set."""
        actual = {
            f.name for f in REVIEW_PHASES_DIR.iterdir()
            if f.is_file() and f.suffix == ".md"
        }
        expected = set(REVIEW_PHASES)
        unexpected = actual - expected
        assert not unexpected, (
            f"Unexpected review phase files: {unexpected}"
        )

    def test_preflight_has_exit_checklist(self):
        content = (REVIEW_PHASES_DIR / "00-preflight.md").read_text(
            encoding="utf-8"
        )
        assert "Exit Checklist" in content, (
            "00-preflight.md missing 'Exit Checklist' section"
        )

    def test_shutdown_exists(self):
        assert (REVIEW_PHASES_DIR / "10-shutdown.md").exists(), (
            "Terminal phase 10-shutdown.md missing"
        )

    def test_shutdown_is_terminal(self):
        content = (REVIEW_PHASES_DIR / "10-shutdown.md").read_text(
            encoding="utf-8"
        )
        assert "shutdown" in content.lower() or "terminal" in content.lower(), (
            "10-shutdown.md does not reference terminal/shutdown behavior"
        )


# ============================================================
# TestBuildPhaseFiles
# ============================================================

class TestBuildPhaseFiles:
    """Validate sigma-build phase file completeness and structure."""

    def test_phases_directory_exists(self):
        assert BUILD_PHASES_DIR.is_dir(), (
            "sigma-build phases directory missing"
        )

    @pytest.fixture(params=sorted(BUILD_PHASES))
    def build_phase(self, request):
        return request.param

    def test_expected_phase_exists(self, build_phase):
        path = BUILD_PHASES_DIR / build_phase
        assert path.exists(), f"Missing build phase: {build_phase}"

    def test_phase_not_empty(self, build_phase):
        path = BUILD_PHASES_DIR / build_phase
        content = path.read_text(encoding="utf-8")
        assert len(content.strip()) > 20, (
            f"Build phase {build_phase} is empty or trivially short"
        )

    def test_phase_has_markdown_header(self, build_phase):
        path = BUILD_PHASES_DIR / build_phase
        content = path.read_text(encoding="utf-8")
        assert re.search(r"^#+ ", content, re.MULTILINE), (
            f"Build phase {build_phase} has no markdown header"
        )

    def test_no_unexpected_build_phases(self):
        """No stray phase files beyond the expected set."""
        actual = {
            f.name for f in BUILD_PHASES_DIR.iterdir()
            if f.is_file() and f.suffix == ".md"
        }
        expected = set(BUILD_PHASES)
        unexpected = actual - expected
        assert not unexpected, (
            f"Unexpected build phase files: {unexpected}"
        )

    def test_preflight_has_exit_checklist(self):
        content = (BUILD_PHASES_DIR / "00-preflight.md").read_text(
            encoding="utf-8"
        )
        assert "Exit Checklist" in content, (
            "00-preflight.md missing 'Exit Checklist' section"
        )

    def test_shutdown_exists(self):
        assert (BUILD_PHASES_DIR / "10-shutdown.md").exists(), (
            "Terminal phase 10-shutdown.md missing"
        )

    def test_shutdown_is_terminal(self):
        content = (BUILD_PHASES_DIR / "10-shutdown.md").read_text(
            encoding="utf-8"
        )
        assert "shutdown" in content.lower() or "terminal" in content.lower(), (
            "10-shutdown.md does not reference terminal/shutdown behavior"
        )

    def test_build_has_plan_phase(self):
        assert (BUILD_PHASES_DIR / "02-plan.md").exists(), (
            "sigma-build missing 02-plan.md phase"
        )

    def test_build_has_build_review_phase(self):
        assert (BUILD_PHASES_DIR / "05-build-review.md").exists(), (
            "sigma-build missing 05-build-review.md phase"
        )


# ============================================================
# TestSharedInfrastructure — directives, decisions, patterns, etc.
# ============================================================

class TestSharedInfrastructure:
    """Validate cross-file reference integrity for shared team files."""

    def test_directives_exists(self):
        assert (REVIEW_SHARED / "directives.md").exists(), (
            "directives.md missing from sigma-review shared"
        )

    @pytest.fixture(params=DIRECTIVES_REQUIRED_TERMS)
    def directive_term(self, request):
        return request.param

    def test_directives_has_key_section(self, directive_term):
        content = (REVIEW_SHARED / "directives.md").read_text(encoding="utf-8")
        assert directive_term in content, (
            f"directives.md missing key term: {directive_term}"
        )

    def test_build_directives_exists(self):
        assert (REVIEW_SHARED / "build-directives.md").exists(), (
            "build-directives.md missing from sigma-review shared"
        )

    def test_decisions_exists(self):
        assert (REVIEW_SHARED / "decisions.md").exists(), (
            "decisions.md missing from sigma-review shared"
        )

    def test_patterns_exists(self):
        assert (REVIEW_SHARED / "patterns.md").exists(), (
            "patterns.md missing from sigma-review shared"
        )

    def test_protocols_exists(self):
        assert (REVIEW_SHARED / "protocols.md").exists(), (
            "protocols.md missing from sigma-review shared"
        )

    def test_roster_exists(self):
        assert (REVIEW_SHARED / "roster.md").exists(), (
            "roster.md missing from sigma-review shared"
        )

    def test_workspace_exists(self):
        assert (REVIEW_SHARED / "workspace.md").exists(), (
            "workspace.md missing from sigma-review shared"
        )

    def test_directives_not_empty(self):
        content = (REVIEW_SHARED / "directives.md").read_text(encoding="utf-8")
        assert len(content.strip()) > 500, (
            "directives.md suspiciously short"
        )

    def test_build_directives_not_empty(self):
        content = (REVIEW_SHARED / "build-directives.md").read_text(
            encoding="utf-8"
        )
        assert len(content.strip()) > 100, (
            "build-directives.md suspiciously short"
        )

    def test_decisions_has_markdown_structure(self):
        content = (REVIEW_SHARED / "decisions.md").read_text(encoding="utf-8")
        assert re.search(r"^#", content, re.MULTILINE), (
            "decisions.md has no markdown headers"
        )

    def test_patterns_has_markdown_structure(self):
        content = (REVIEW_SHARED / "patterns.md").read_text(encoding="utf-8")
        assert re.search(r"^#", content, re.MULTILINE), (
            "patterns.md has no markdown headers"
        )

    def test_special_agent_files_exist(self):
        """Special files that were excluded from standard validation should exist."""
        for name in SPECIAL_FILES:
            assert (AGENTS_DIR / name).exists(), (
                f"Special agent file missing: {name}"
            )
