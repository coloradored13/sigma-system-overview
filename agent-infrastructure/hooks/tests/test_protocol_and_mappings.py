"""Protocol and mapping validation tests.

Validates ΣComm notation rules, skill-agent mappings, roster patterns,
and INDEX.md ↔ directory consistency. These are drift-catching tests that
read real files from the filesystem.
"""
import re
from collections import Counter
from pathlib import Path

import pytest

CLAUDE_DIR = Path.home() / ".claude"
SKILLS_DIR = CLAUDE_DIR / "skills"
AGENTS_DIR = CLAUDE_DIR / "agents"
MEMORY_DIR = CLAUDE_DIR / "projects" / "-Users-bjgilbert" / "memory"
ROSTER_PATH = CLAUDE_DIR / "teams" / "sigma-review" / "shared" / "roster.md"
INDEX_PATH = SKILLS_DIR / "INDEX.md"
SIGMACOMM_SKILL = SKILLS_DIR / "sigmacomm" / "SKILL.md"
SIGMA_COMM_AGENT = AGENTS_DIR / "sigma-comm.md"


# ---------- Constants ----------

VALID_STATUS_CODES = {"✓", "◌", "!", "?", "✗", "↻"}

VALID_BODY_SYMBOLS = {"|", ",", ">", "→", "+", "!", "@", "^"}

VALID_ENTRY_PREFIXES = {"C[]", "C~[]", "R[]", "P[]", "F[]", "¬[]", "D[]"}

# Regex for entry types as they appear inline: prefix + content
ENTRY_PATTERN = re.compile(
    r"(C\[|C~\[|R\[|P\[|F\[|¬\[|D\[)"
)

# YY.M.D date format -- e.g. 26.3.14, 26.12.1
DATE_PATTERN = re.compile(r"\b(\d{2}\.\d{1,2}\.\d{1,2})\b")

# Count format |N| or |N|YY.M
COUNT_PATTERN = re.compile(r"\|(\d+)\|")

# Shared modules referenced in INDEX.md -- not standalone skill dirs
SHARED_MODULES = {"analytical-hygiene", "prompt-decomposition"}

# Skills excluded from INDEX completeness checks
EXCLUDED_FROM_INDEX = {"mcp-builder"}


# ---------- Helpers ----------

def read_file(path: Path) -> str:
    """Read a file and return its content, or empty string if missing."""
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def parse_index_mapping_table(content: str) -> list[dict]:
    """Parse the skill-agent mapping table from INDEX.md.

    Returns list of dicts with keys: agent, primary_skills, boot_skills
    """
    mappings = []
    in_table = False
    for line in content.splitlines():
        if "| Agent |" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cols = [c.strip() for c in line.split("|")]
            # cols[0] is empty (before first |), cols[-1] is empty (after last |)
            cols = [c for c in cols if c]
            if len(cols) >= 3:
                agent = cols[0].strip()
                primary = [s.strip() for s in cols[1].split(",")]
                # Strip parenthetical notes like "(router only)" or "(creative mode)"
                primary = [re.sub(r"\s*\(.*?\)", "", s).strip() for s in primary]
                boot = [s.strip() for s in cols[2].split(",")]
                boot = [re.sub(r"\s*\(.*?\)", "", s).strip() for s in boot]
                mappings.append({
                    "agent": agent,
                    "primary_skills": primary,
                    "boot_skills": boot,
                })
        elif in_table and not line.strip():
            break
    return mappings


def parse_roster(content: str) -> list[dict]:
    """Parse roster.md entries.

    Returns list of dicts with keys: name, domain, wake_for
    """
    entries = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("→") or line.startswith("#"):
            continue
        # Format: name |domain: ... |wake-for: ...
        parts = line.split("|")
        if len(parts) < 3:
            continue
        name = parts[0].strip()
        domain_str = ""
        wake_for_str = ""
        for part in parts[1:]:
            part = part.strip()
            if part.startswith("domain:"):
                domain_str = part[len("domain:"):].strip()
            elif part.startswith("wake-for:"):
                wake_for_str = part[len("wake-for:"):].strip()
        if name:
            entries.append({
                "name": name,
                "domain": [d.strip() for d in domain_str.split(",") if d.strip()],
                "wake_for": [w.strip() for w in wake_for_str.split(",") if w.strip()],
            })
    return entries


# ================================================================
# TestSigmaCommNotation
# ================================================================

class TestSigmaCommNotation:
    """Parse and validate ΣComm format rules against real content."""

    # --- Status code validation ---

    @pytest.mark.parametrize("code", sorted(VALID_STATUS_CODES))
    def test_valid_status_codes_recognized(self, code):
        """Each defined status code should be in the valid set."""
        assert code in VALID_STATUS_CODES

    def test_invalid_status_code_detected(self):
        """A made-up status code should not be in the valid set."""
        invalid_codes = {"#", "&", "~", "X", "OK", "DONE"}
        for code in invalid_codes:
            assert code not in VALID_STATUS_CODES, f"'{code}' should not be a valid status code"

    def test_status_codes_in_workspace_sample(self):
        """Workspace sample content should only use valid status codes."""
        from conftest import SAMPLE_WORKSPACE_COMPLETE

        # Find status codes at line starts (after agent name prefix)
        status_pattern = re.compile(r":\s*([✓◌!?✗↻])\s")
        found = status_pattern.findall(SAMPLE_WORKSPACE_COMPLETE)
        assert len(found) > 0, "No status codes found in sample workspace"
        for code in found:
            assert code in VALID_STATUS_CODES, f"Invalid status code '{code}' in workspace sample"

    # --- Date format validation ---

    def test_date_format_yy_m_d_valid(self):
        """YY.M.D dates should match the expected pattern."""
        valid_dates = ["26.3.14", "26.12.1", "25.1.30", "27.11.15"]
        for date in valid_dates:
            assert DATE_PATTERN.search(date), f"Valid date '{date}' not matched"

    def test_date_format_rejects_wrong_format(self):
        """Non-YY.M.D dates should not match the pattern."""
        invalid = ["2026-03-14", "March 14, 2026", "3/14/26"]
        for date in invalid:
            match = DATE_PATTERN.fullmatch(date)
            assert match is None, f"Invalid date format '{date}' should not fullmatch"

    def test_dates_in_memory_file(self):
        """Real memory file should contain YY.M.D formatted dates."""
        content = read_file(MEMORY_DIR / "MEMORY.md")
        if not content:
            pytest.skip("MEMORY.md not found")
        dates = DATE_PATTERN.findall(content)
        assert len(dates) > 5, f"Expected many YY.M.D dates in MEMORY.md, found {len(dates)}"

    # --- Count format validation ---

    def test_count_format_pipe_n_pipe(self):
        """Count format |N| should be parseable."""
        test_strings = [
            "C[detects perf, honest>polish|3|26.3]",
            "C[probes|5|26.3]",
            "|10|",
        ]
        for s in test_strings:
            matches = COUNT_PATTERN.findall(s)
            assert len(matches) > 0, f"Count not found in '{s}'"
            for m in matches:
                assert m.isdigit(), f"Count '{m}' is not numeric"

    # --- Entry type validation ---

    def test_known_entry_prefixes_parsed(self):
        """All known entry types should match the entry pattern regex."""
        test_entries = [
            "C[detects perf, honest>polish|3|26.3]",
            "C~[prefers-TDD]",
            "R[api-latency-p99=120ms|src:grafana|26.4.1]",
            "P[distribution>technology-for-finserv-moat]",
            "F[26.3.12] r1: 10 findings(4H,2MH,4M)",
            "¬[developer(leader learning to build)]",
            "D[build-sequence]: waterfall+distribution=STAGGERED",
        ]
        for entry in test_entries:
            assert ENTRY_PATTERN.search(entry), f"Entry not matched: '{entry}'"

    def test_unknown_entry_prefix_not_matched(self):
        """An unknown prefix like Z[] should not match known entry types."""
        assert ENTRY_PATTERN.search("Z[something]") is None

    def test_entry_types_in_sigmacomm_skill(self):
        """The sigmacomm SKILL.md should document all known entry types."""
        content = read_file(SIGMACOMM_SKILL)
        if not content:
            pytest.skip("sigmacomm/SKILL.md not found")
        for prefix in ["C[]", "C~[]", "R[]", "P[]", "F[]", "¬[]", "D[]"]:
            # Check the prefix appears as documented (in backticks or table)
            clean = prefix.replace("[", r"\[").replace("]", r"\]").replace("~", r"\~")
            pattern = re.compile(rf"`{clean}`|{clean}")
            assert pattern.search(content), f"Entry type {prefix} not documented in SKILL.md"

    # --- Anti-memory validation ---

    def test_anti_memory_entries_documented(self):
        """Anti-memory (NOT) entries should be documented in SKILL.md."""
        content = read_file(SIGMACOMM_SKILL)
        if not content:
            pytest.skip("sigmacomm/SKILL.md not found")
        assert "Anti-Memory" in content or "anti-memory" in content.lower()
        assert "¬[" in content

    def test_anti_memory_in_memory_file(self):
        """Real memory (MEMORY.md) should reference anti-memory concepts.

        A mature system should have ruled-out knowledge recorded somewhere.
        """
        content = read_file(MEMORY_DIR / "MEMORY.md")
        if not content:
            pytest.skip("MEMORY.md not found")
        # The memory index references ¬ concepts in correction entries
        has_not_symbol = "¬" in content
        assert has_not_symbol, "MEMORY.md should contain ¬ (NOT) references in a mature system"

    # --- Body notation validation ---

    def test_body_symbols_documented_in_skill(self):
        """All body notation symbols should be documented in SKILL.md."""
        content = read_file(SIGMACOMM_SKILL)
        if not content:
            pytest.skip("sigmacomm/SKILL.md not found")
        # Check the body notation table has all symbols
        for symbol_desc in ["|", ",", ">", "→", "+", "@", "^"]:
            assert symbol_desc in content, f"Body symbol '{symbol_desc}' not documented"

    def test_mandatory_sections_documented(self):
        """Mandatory sections (¬, →, #N) should be documented."""
        content = read_file(SIGMACOMM_SKILL)
        if not content:
            pytest.skip("sigmacomm/SKILL.md not found")
        assert "¬" in content, "¬ (NOT) section not documented"
        assert "→" in content, "→ (actions) section not documented"
        assert "#N" in content or "#count" in content, "#N (count) section not documented"


# ================================================================
# TestSigmaCommSkillFile
# ================================================================

class TestSigmaCommSkillFile:
    """Validate that sigmacomm/SKILL.md has all required content."""

    def test_skill_file_exists(self):
        assert SIGMACOMM_SKILL.exists(), "sigmacomm/SKILL.md not found"

    def test_has_frontmatter(self):
        content = read_file(SIGMACOMM_SKILL)
        assert content.startswith("---"), "Missing YAML frontmatter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, "Frontmatter not properly closed"

    def test_has_message_format_section(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "## Message Format" in content

    def test_has_status_codes_section(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "### Status Codes" in content or "Status Codes" in content

    def test_has_memory_entry_types_section(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "## Memory Entry Types" in content

    def test_has_writing_rules(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "## Writing Rules" in content or "Writing Rules" in content

    def test_has_quick_reference_card(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "Quick Reference" in content

    def test_has_practice_section(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "## Practice" in content or "Practice" in content

    def test_has_confidence_and_dates(self):
        content = read_file(SIGMACOMM_SKILL)
        assert "## Confidence" in content or "Confidence" in content
        assert "YY.M.D" in content

    def test_all_six_status_codes_listed(self):
        """SKILL.md should list all 6 status codes."""
        content = read_file(SIGMACOMM_SKILL)
        for code in VALID_STATUS_CODES:
            assert code in content, f"Status code '{code}' not found in SKILL.md"

    def test_sigma_comm_agent_consistent(self):
        """sigma-comm.md agent spec should have matching status codes."""
        content = read_file(SIGMA_COMM_AGENT)
        if not content:
            pytest.skip("sigma-comm.md not found")
        for code in VALID_STATUS_CODES:
            assert code in content, f"Status code '{code}' missing from sigma-comm.md agent spec"


# ================================================================
# TestSkillAgentMappings
# ================================================================

class TestSkillAgentMappings:
    """Validate INDEX.md agent-skill table against filesystem."""

    @pytest.fixture(scope="class")
    def mappings(self):
        content = read_file(INDEX_PATH)
        if not content:
            pytest.skip("INDEX.md not found")
        return parse_index_mapping_table(content)

    def test_mapping_table_not_empty(self, mappings):
        assert len(mappings) > 0, "No agent-skill mappings found in INDEX.md"

    def test_all_mapped_agents_have_files(self, mappings):
        """Every agent in the mapping table should have a .md file."""
        missing = []
        for m in mappings:
            agent_file = AGENTS_DIR / f"{m['agent']}.md"
            if not agent_file.exists():
                missing.append(m["agent"])
        assert not missing, f"Agents in INDEX.md without .md files: {missing}"

    def test_primary_skills_exist_as_directories(self, mappings):
        """Every primary skill in the mapping should be a skill directory."""
        missing = []
        for m in mappings:
            for skill in m["primary_skills"]:
                if skill and not (SKILLS_DIR / skill).is_dir():
                    missing.append(f"{m['agent']} -> {skill}")
        assert not missing, f"Primary skills without directories: {missing}"

    def test_boot_skills_exist_as_directories(self, mappings):
        """Every boot skill in the mapping should be a skill directory."""
        missing = []
        for m in mappings:
            for skill in m["boot_skills"]:
                if skill and not (SKILLS_DIR / skill).is_dir():
                    missing.append(f"{m['agent']} -> {skill}")
        assert not missing, f"Boot skills without directories: {missing}"

    def test_boot_skills_have_skill_md(self, mappings):
        """Every boot skill directory should contain a SKILL.md file."""
        missing = []
        for m in mappings:
            for skill in m["boot_skills"]:
                skill_md = SKILLS_DIR / skill / "SKILL.md"
                if skill and not skill_md.exists():
                    missing.append(f"{m['agent']} -> {skill}/SKILL.md")
        assert not missing, f"Boot skills without SKILL.md: {missing}"

    def test_boot_skills_subset_of_primary(self, mappings):
        """Boot skills should be a subset of primary skills."""
        violations = []
        for m in mappings:
            primary_set = set(m["primary_skills"])
            for boot_skill in m["boot_skills"]:
                if boot_skill and boot_skill not in primary_set:
                    violations.append(
                        f"{m['agent']}: boot skill '{boot_skill}' not in primary {primary_set}"
                    )
        assert not violations, f"Boot skills not in primary set: {violations}"

    def test_minimum_mapped_agents(self, mappings):
        """Should have at least 10 agents mapped (current count is 13)."""
        assert len(mappings) >= 10, f"Expected >=10 mapped agents, got {len(mappings)}"


# ================================================================
# TestRosterWakeForPatterns
# ================================================================

class TestRosterWakeForPatterns:
    """Validate roster pattern quality and consistency."""

    @pytest.fixture(scope="class")
    def roster(self):
        content = read_file(ROSTER_PATH)
        if not content:
            pytest.skip("roster.md not found")
        return parse_roster(content)

    def test_roster_not_empty(self, roster):
        assert len(roster) > 0, "Roster has no entries"

    def test_wake_for_not_empty(self, roster):
        """Every roster entry should have at least one wake-for keyword."""
        empty = [e["name"] for e in roster if not e["wake_for"]]
        assert not empty, f"Agents with empty wake-for: {empty}"

    def test_domain_not_empty(self, roster):
        """Every roster entry should have at least one domain."""
        empty = [e["name"] for e in roster if not e["domain"]]
        assert not empty, f"Agents with empty domain: {empty}"

    def test_agent_names_valid_identifiers(self, roster):
        """Agent names should be lowercase with hyphens, no spaces."""
        pattern = re.compile(r"^[a-z][a-z0-9-]*$")
        invalid = [e["name"] for e in roster if not pattern.match(e["name"])]
        assert not invalid, f"Invalid agent names: {invalid}"

    def test_no_overbroad_wake_for_keywords(self, roster):
        """No single wake-for keyword should appear in more than 3 agents.

        Over-broad keywords defeat selective waking.
        """
        keyword_counts = Counter()
        for entry in roster:
            for kw in entry["wake_for"]:
                keyword_counts[kw] += 1
        overbroad = {kw: cnt for kw, cnt in keyword_counts.items() if cnt > 3}
        assert not overbroad, (
            f"Wake-for keywords in >3 agents (too broad): {overbroad}"
        )

    def test_devils_advocate_in_roster(self, roster):
        """DA should be present in the roster."""
        names = [e["name"] for e in roster]
        assert "devils-advocate" in names, "devils-advocate missing from roster"

    def test_roster_has_minimum_agents(self, roster):
        """Should have at least 15 agents on roster (current ~20)."""
        assert len(roster) >= 15, f"Expected >=15 roster entries, got {len(roster)}"

    def test_wake_for_keywords_are_descriptive(self, roster):
        """Wake-for keywords should be multi-word or domain-specific, not single generic words."""
        too_short = []
        for entry in roster:
            for kw in entry["wake_for"]:
                # Single character or very generic single words are suspicious
                if len(kw) < 3:
                    too_short.append(f"{entry['name']}: '{kw}'")
        assert not too_short, f"Wake-for keywords too short/generic: {too_short}"


# ================================================================
# TestSkillsIndexCompleteness
# ================================================================

class TestSkillsIndexCompleteness:
    """Verify INDEX.md and skill directories stay in sync."""

    @pytest.fixture(scope="class")
    def index_content(self):
        content = read_file(INDEX_PATH)
        if not content:
            pytest.skip("INDEX.md not found")
        return content

    @pytest.fixture(scope="class")
    def skill_dirs(self):
        """All skill directories on disk."""
        return {
            d.name for d in SKILLS_DIR.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        }

    @pytest.fixture(scope="class")
    def non_sigma_skill_dirs(self, skill_dirs):
        """Non-sigma, non-excluded skill directories."""
        return {
            s for s in skill_dirs
            if not s.startswith("sigma-")
            and s != "sigmacomm"
            and s not in EXCLUDED_FROM_INDEX
        }

    @pytest.fixture(scope="class")
    def sigma_skill_dirs(self, skill_dirs):
        """All sigma-* and sigmacomm directories."""
        return {
            s for s in skill_dirs
            if s.startswith("sigma-") or s == "sigmacomm"
        }

    def test_non_sigma_skills_in_index(self, index_content, non_sigma_skill_dirs):
        """Every non-sigma skill directory should be mentioned in INDEX.md."""
        missing = [s for s in sorted(non_sigma_skill_dirs) if s not in index_content]
        assert not missing, f"Skill dirs not mentioned in INDEX.md: {missing}"

    def test_sigma_skills_in_index(self, index_content, sigma_skill_dirs):
        """Every sigma-* skill directory should be mentioned in INDEX.md."""
        missing = [s for s in sorted(sigma_skill_dirs) if s not in index_content]
        assert not missing, f"Sigma skill dirs not in INDEX.md: {missing}"

    def test_no_dead_references_in_skill_tables(self, index_content, skill_dirs):
        """Skills referenced in INDEX.md skill tables should exist as directories.

        Scans only the skill listing tables (not the agent mapping table).
        Stops before "## Agent Boot Integration" to avoid matching agent names.
        """
        dead = []
        # Only check the skill listing sections, not the agent mapping table
        cutoff = index_content.find("## Agent Boot Integration")
        check_content = index_content[:cutoff] if cutoff > 0 else index_content

        table_row_pattern = re.compile(r"^\|\s*([a-z][a-z0-9-]*)\s*\|", re.MULTILINE)
        for match in table_row_pattern.finditer(check_content):
            skill_name = match.group(1)
            # Skip header words and non-skill entries
            if skill_name in ("skill", "agent", "module", "parent"):
                continue
            if skill_name not in skill_dirs and skill_name not in SHARED_MODULES:
                dead.append(skill_name)
        assert not dead, f"INDEX.md references non-existent skill dirs: {dead}"

    def test_index_has_sigma_section(self, index_content):
        """INDEX.md should have a Sigma section."""
        assert "## Sigma" in index_content

    def test_index_has_shared_modules_section(self, index_content):
        """INDEX.md should document shared modules."""
        assert "## Shared Modules" in index_content

    def test_mcp_builder_exists_on_disk(self, skill_dirs):
        """mcp-builder should exist as a skill directory even if not in INDEX tables."""
        assert "mcp-builder" in skill_dirs, "mcp-builder skill directory missing"

    def test_all_skill_dirs_have_skill_md(self, skill_dirs):
        """Every skill directory should contain a SKILL.md file."""
        missing = [
            s for s in sorted(skill_dirs)
            if not (SKILLS_DIR / s / "SKILL.md").exists()
        ]
        assert not missing, f"Skill dirs without SKILL.md: {missing}"

    def test_index_has_execution_layer_section(self, index_content):
        """INDEX.md should have an Execution-Layer Skills section."""
        assert "## Execution-Layer Skills" in index_content

    def test_index_has_protocol_section(self, index_content):
        """INDEX.md should have a Protocol Skills section."""
        assert "## Protocol Skills" in index_content
