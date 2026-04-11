"""Tests for orchestrator-config.py workflow state machines and gate_checks.py edge cases.

Covers:
  - ANALYZE workflow structure, phases, transitions, guards
  - BUILD workflow structure, phases, transitions, guards
  - Orchestrator CLI guards (team_created, force_restart, mode mismatch)
  - Checkpoint persistence (save/load, mode tag, atomic write)
  - gate_checks parsing edge cases (malformed workspace, empty sections)
  - gate_checks dataclass serialization (CheckResult, ValidationResult, BeliefComponents)
  - gate_checks bundle registry completeness
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import gate_checks (stdlib only -- always available)
# ---------------------------------------------------------------------------

_shared_dir = str(Path.home() / ".claude" / "teams" / "sigma-review" / "shared")
sys.path.insert(0, _shared_dir)

import gate_checks

# ---------------------------------------------------------------------------
# Conditionally import orchestrator-config.py (needs hateoas_agent)
# ---------------------------------------------------------------------------

_hateoas_available = True
try:
    from hateoas_agent import AgentSlot, Orchestrator
    from hateoas_agent.conditions import (
        belief_above,
        context_true,
        exit_gate_passed,
        round_limit,
    )
    from hateoas_agent.orchestrator_persistence import (
        load_orchestrator_checkpoint,
        save_orchestrator_checkpoint,
    )

    _orch_spec = importlib.util.spec_from_file_location(
        "orchestrator_config",
        os.path.join(_shared_dir, "orchestrator-config.py"),
    )
    _orch_mod = importlib.util.module_from_spec(_orch_spec)
    _orch_spec.loader.exec_module(_orch_mod)
    build_analyze_workflow = _orch_mod.build_analyze_workflow
    build_build_workflow = _orch_mod.build_build_workflow
    _load_or_create = _orch_mod._load_or_create
    _save = _orch_mod._save
    cmd_start = _orch_mod.cmd_start
    cmd_advance = _orch_mod.cmd_advance
    PHASE_REQUIRED_VALIDATIONS = None  # loaded lazily inside cmd_advance
    DEFAULT_CHECKPOINT = _orch_mod.DEFAULT_CHECKPOINT
except ImportError:
    _hateoas_available = False

needs_hateoas = pytest.mark.skipif(
    not _hateoas_available,
    reason="hateoas_agent not installed -- skipping orchestrator tests",
)


# ===================================================================
# ANALYZE WORKFLOW TESTS
# ===================================================================


@needs_hateoas
class TestAnalyzeWorkflowStructure:
    """Validate the ANALYZE state machine phases and transitions."""

    @pytest.fixture(autouse=True)
    def _build(self):
        self.orch = build_analyze_workflow()

    def test_name(self):
        assert self.orch.name == "sigma-review-analyze"

    def test_phase_count(self):
        """ANALYZE has 10 phases: research through complete."""
        phases = list(self.orch._phases.keys())
        assert len(phases) == 10

    def test_phase_ordering(self):
        expected = [
            "research", "circuit_breaker", "challenge", "debate",
            "synthesis", "compilation", "promotion", "sync", "archive", "complete",
        ]
        phases = list(self.orch._phases.keys())
        assert phases == expected

    def test_terminal_phase_is_complete(self):
        assert "complete" in self.orch._terminal_phases

    def test_only_complete_is_terminal(self):
        assert self.orch._terminal_phases == {"complete"}

    def test_parallel_phases(self):
        """research and challenge should be parallel."""
        assert self.orch._phases["research"].parallel is True
        assert self.orch._phases["challenge"].parallel is True

    def test_sequential_phases(self):
        """circuit_breaker, debate, synthesis should be sequential."""
        assert self.orch._phases["circuit_breaker"].parallel is False
        assert self.orch._phases["debate"].parallel is False
        assert self.orch._phases["synthesis"].parallel is False

    def test_challenge_self_loop_exists(self):
        """challenge -> challenge transitions must exist (self-loop for more rounds)."""
        challenge_transitions = [
            t for t in self.orch._transitions
            if t.from_phase == "challenge" and t.to_phase == "challenge"
        ]
        assert len(challenge_transitions) >= 2, (
            "Expected at least two self-loop transitions on challenge "
            "(exit_passed_low_belief and another_round)"
        )

    def test_challenge_to_synthesis_transitions(self):
        """challenge -> synthesis must exist for both normal exit and hard cap."""
        to_synth = [
            t for t in self.orch._transitions
            if t.from_phase == "challenge" and t.to_phase == "synthesis"
        ]
        assert len(to_synth) == 2  # exit_to_synthesis + hard_cap

    def test_debate_feeds_back_to_challenge(self):
        """debate -> challenge (unguarded) feeds disagreement back."""
        debate_to_ch = [
            t for t in self.orch._transitions
            if t.from_phase == "debate" and t.to_phase == "challenge"
        ]
        assert len(debate_to_ch) == 1

    def test_post_exit_gate_chain(self):
        """synthesis -> compilation -> promotion -> sync -> archive -> complete."""
        chain = [
            ("synthesis", "compilation"),
            ("compilation", "promotion"),
            ("promotion", "sync"),
            ("sync", "archive"),
            ("archive", "complete"),
        ]
        for src, dst in chain:
            matches = [
                t for t in self.orch._transitions
                if t.from_phase == src and t.to_phase == dst
            ]
            assert len(matches) == 1, f"Missing transition {src} -> {dst}"

    def test_default_agents_count(self):
        agents = list(self.orch._agents.keys())
        assert len(agents) == 4

    def test_default_agents_names(self):
        agent_names = set(self.orch._agents.keys())
        expected = {"tech-architect", "product-strategist", "reference-class-analyst", "devils-advocate"}
        assert agent_names == expected

    def test_da_joins_at_challenge(self):
        da = self.orch._agents["devils-advocate"]
        assert da.join_phase == "challenge"

    def test_start_at_research_phase(self):
        self.orch.start("research", context={"test": True})
        state = self.orch._make_state()
        assert state.current_phase == "research"
        assert not state.is_terminal

    def test_research_to_circuit_breaker_guard(self):
        """Advancing from research requires r1_converged AND r1_validated."""
        self.orch.start("research", context={})
        # Without the flags, should stay at research
        self.orch.advance(context={})
        assert self.orch._current_phase == "research"

        # With both flags, should advance
        self.orch.advance(context={"r1_converged": True, "r1_validated": True})
        assert self.orch._current_phase == "circuit_breaker"


# ===================================================================
# BUILD WORKFLOW TESTS
# ===================================================================


@needs_hateoas
class TestBuildWorkflowStructure:
    """Validate the BUILD state machine phases and transitions."""

    @pytest.fixture(autouse=True)
    def _build(self):
        self.orch = build_build_workflow()

    def test_name(self):
        assert self.orch.name == "sigma-review-build"

    def test_phase_count(self):
        """BUILD has 10 phases: plan through complete."""
        phases = list(self.orch._phases.keys())
        assert len(phases) == 10

    def test_phase_ordering(self):
        expected = [
            "plan", "challenge_plan", "build", "review",
            "synthesis", "compilation", "promotion", "sync", "archive", "complete",
        ]
        phases = list(self.orch._phases.keys())
        assert phases == expected

    def test_terminal_phase_is_complete(self):
        assert "complete" in self.orch._terminal_phases

    def test_only_complete_is_terminal(self):
        assert self.orch._terminal_phases == {"complete"}

    def test_challenge_plan_self_loop_exists(self):
        """challenge_plan -> challenge_plan for plan revision rounds."""
        loops = [
            t for t in self.orch._transitions
            if t.from_phase == "challenge_plan" and t.to_phase == "challenge_plan"
        ]
        assert len(loops) == 1

    def test_review_self_loop_exists(self):
        """review -> review for revision rounds."""
        loops = [
            t for t in self.orch._transitions
            if t.from_phase == "review" and t.to_phase == "review"
        ]
        assert len(loops) == 1

    def test_plan_hard_cap_exists(self):
        """challenge_plan -> build hard cap when round >= 5."""
        to_build = [
            t for t in self.orch._transitions
            if t.from_phase == "challenge_plan" and t.to_phase == "build"
        ]
        assert len(to_build) == 2  # plans_approved + plan_hard_cap

    def test_review_hard_cap_exists(self):
        """review -> synthesis hard cap when round >= 5."""
        to_synth = [
            t for t in self.orch._transitions
            if t.from_phase == "review" and t.to_phase == "synthesis"
        ]
        assert len(to_synth) == 2  # review_done + review_hard_cap

    def test_default_build_agents(self):
        agent_names = set(self.orch._agents.keys())
        expected = {"tech-architect", "code-quality-analyst", "reference-class-analyst", "devils-advocate"}
        assert agent_names == expected

    def test_da_joins_at_challenge_plan(self):
        da = self.orch._agents["devils-advocate"]
        assert da.join_phase == "challenge_plan"

    def test_start_at_plan_phase(self):
        self.orch.start("plan", context={"test": True})
        state = self.orch._make_state()
        assert state.current_phase == "plan"

    def test_plan_to_challenge_requires_both_flags(self):
        """plan -> challenge_plan needs plans_ready AND plan_round_validated."""
        self.orch.start("plan", context={})
        self.orch.advance(context={"plans_ready": True})  # missing plan_round_validated
        assert self.orch._current_phase == "plan"

        self.orch.advance(context={"plans_ready": True, "plan_round_validated": True})
        assert self.orch._current_phase == "challenge_plan"

    def test_build_to_review_requires_both_flags(self):
        """build -> review needs build_complete AND checkpoint_validated."""
        self.orch.start("build", context={})
        self.orch.advance(context={"build_complete": True})  # missing checkpoint_validated
        assert self.orch._current_phase == "build"

        self.orch.advance(context={"build_complete": True, "checkpoint_validated": True})
        assert self.orch._current_phase == "review"

    def test_post_exit_gate_chain(self):
        """Identical chain as ANALYZE: synthesis -> ... -> complete."""
        chain = [
            ("synthesis", "compilation"),
            ("compilation", "promotion"),
            ("promotion", "sync"),
            ("sync", "archive"),
            ("archive", "complete"),
        ]
        for src, dst in chain:
            matches = [
                t for t in self.orch._transitions
                if t.from_phase == src and t.to_phase == dst
            ]
            assert len(matches) == 1, f"Missing transition {src} -> {dst}"


# ===================================================================
# ORCHESTRATOR CLI GUARDS
# ===================================================================


@needs_hateoas
class TestOrchestratorCLIGuards:
    """Test cmd_start guards: team_created, force_restart, mode mismatch."""

    def test_load_or_create_no_checkpoint(self, tmp_path):
        """Fresh start when no checkpoint file exists."""
        cp = str(tmp_path / "nonexistent.json")
        orch = _load_or_create("analyze", cp)
        assert orch.name == "sigma-review-analyze"
        assert orch._current_phase is None  # not started yet

    def test_load_or_create_mode_mismatch_exits(self, tmp_path):
        """Checkpoint says analyze, but --mode build -> sys.exit(1)."""
        cp = str(tmp_path / "ck.json")
        # Create a checkpoint with analyze mode
        orch = build_analyze_workflow()
        orch.start("research", context={"test": True})
        data = save_orchestrator_checkpoint(orch)
        data["_mode"] = "analyze"
        with open(cp, "w") as f:
            json.dump(data, f)

        with pytest.raises(SystemExit) as exc_info:
            _load_or_create("build", cp)
        assert exc_info.value.code == 1

    def test_load_or_create_corrupt_checkpoint_starts_fresh(self, tmp_path):
        """Corrupt JSON in checkpoint file -> start fresh (not crash)."""
        cp = str(tmp_path / "ck.json")
        with open(cp, "w") as f:
            f.write("{invalid json!!!")

        orch = _load_or_create("analyze", cp)
        assert orch.name == "sigma-review-analyze"
        assert orch._current_phase is None

    def test_save_writes_mode_tag(self, tmp_path):
        """_save persists _mode key in checkpoint data."""
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={})
        _save(orch, cp)

        with open(cp) as f:
            data = json.load(f)
        assert data["_mode"] == "analyze"

    def test_save_build_mode_tag(self, tmp_path):
        """BUILD workflow saves _mode = 'build'."""
        cp = str(tmp_path / "ck.json")
        orch = build_build_workflow()
        orch.start("plan", context={})
        _save(orch, cp)

        with open(cp) as f:
            data = json.load(f)
        assert data["_mode"] == "build"

    def test_save_atomic_write(self, tmp_path):
        """_save uses atomic rename -- no .tmp file left behind."""
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={})
        _save(orch, cp)

        assert os.path.exists(cp)
        assert not os.path.exists(cp + ".tmp")


# ===================================================================
# CHECKPOINT PERSISTENCE
# ===================================================================


@needs_hateoas
class TestCheckpointPersistence:
    """Test round-trip save/load of orchestrator state."""

    def test_roundtrip_preserves_phase(self, tmp_path):
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={"r1_converged": True, "r1_validated": True})
        orch.advance()
        assert orch._current_phase == "circuit_breaker"

        _save(orch, cp)
        orch2 = _load_or_create("analyze", cp)
        assert orch2._current_phase == "circuit_breaker"

    def test_roundtrip_preserves_context(self, tmp_path):
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={"task": "test-task", "tier": 2})
        _save(orch, cp)

        orch2 = _load_or_create("analyze", cp)
        state = orch2._make_state()
        assert state.context["task"] == "test-task"
        assert state.context["tier"] == 2

    def test_roundtrip_preserves_phase_history(self, tmp_path):
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={"r1_converged": True, "r1_validated": True})
        orch.advance()
        _save(orch, cp)

        orch2 = _load_or_create("analyze", cp)
        state = orch2._make_state()
        assert "research" in state.phase_history
        assert "circuit_breaker" in state.phase_history

    def test_save_overwrite_existing(self, tmp_path):
        """Saving twice to same path overwrites cleanly."""
        cp = str(tmp_path / "ck.json")
        orch = build_analyze_workflow()
        orch.start("research", context={"version": 1})
        _save(orch, cp)

        orch.advance(context={"r1_converged": True, "r1_validated": True, "version": 2})
        _save(orch, cp)

        with open(cp) as f:
            data = json.load(f)
        # Should have the updated state
        assert data.get("current_phase") == "circuit_breaker"


# ===================================================================
# GATE_CHECKS PARSING EDGE CASES
# ===================================================================


class TestGateChecksParsing:
    """Test parse_sections, parse_agent_subsections, extract_agents edge cases."""

    def test_parse_sections_empty_content(self):
        result = gate_checks.parse_sections("")
        # Empty content produces empty dict (no lines to accumulate)
        assert result == {}

    def test_parse_sections_no_headers(self):
        """Content with no ## headers goes entirely into _preamble."""
        content = "Some plain text\nAnother line\nNo headers at all"
        result = gate_checks.parse_sections(content)
        assert "_preamble" in result
        assert len(result) == 1
        assert "Some plain text" in result["_preamble"]

    def test_parse_sections_only_preamble_text(self):
        content = "# Title\nSome intro text\nMore text"
        result = gate_checks.parse_sections(content)
        assert "_preamble" in result
        assert "# Title" in result["_preamble"]

    def test_parse_sections_h3_not_treated_as_section(self):
        """### headers should NOT create new sections."""
        content = "## findings\nSome findings\n### agent-alpha\nAlpha stuff"
        result = gate_checks.parse_sections(content)
        assert "findings" in result
        assert "### agent-alpha" in result["findings"]

    def test_parse_sections_case_normalization(self):
        """Section headers are lowercased."""
        content = "## Infrastructure\nStuff\n## FINDINGS\nMore stuff"
        result = gate_checks.parse_sections(content)
        assert "infrastructure" in result
        assert "findings" in result

    def test_parse_sections_adjacent_headers(self):
        """Two ## headers with no content between them -- first gets no entry
        because no lines accumulated before the second header."""
        content = "## first\n## second\nContent here"
        result = gate_checks.parse_sections(content)
        # parse_sections only writes when lines is non-empty; adjacent headers
        # means first header has zero accumulated lines -> no entry
        assert "first" not in result
        assert "second" in result
        assert "Content here" in result["second"]

    def test_parse_agent_subsections_empty_findings(self):
        result = gate_checks.parse_agent_subsections("")
        assert result == {}

    def test_parse_agent_subsections_no_h3_headers(self):
        """Content with no ### headers returns empty dict."""
        content = "Some general findings text\nWith multiple lines"
        result = gate_checks.parse_agent_subsections(content)
        assert result == {}

    def test_parse_agent_subsections_agent_with_empty_body(self):
        """### header followed immediately by another ### header -- first agent
        gets no entry because no lines accumulated (same pattern as parse_sections)."""
        content = "### agent-alpha\n### agent-beta\nBeta content here"
        result = gate_checks.parse_agent_subsections(content)
        assert "agent-alpha" not in result  # no accumulated lines
        assert "agent-beta" in result
        assert "Beta content here" in result["agent-beta"]

    def test_parse_agent_subsections_agent_with_content(self):
        """### header with actual content between headers."""
        content = "### agent-alpha\nAlpha findings here\n### agent-beta\nBeta content here"
        result = gate_checks.parse_agent_subsections(content)
        assert "agent-alpha" in result
        assert "Alpha findings here" in result["agent-alpha"]
        assert "agent-beta" in result

    def test_extract_agents_zero_agents(self):
        """Workspace with no ### headers in findings region."""
        content = "## findings\nGeneral text only\n## convergence\nDone"
        agents = gate_checks.extract_agents_from_workspace(content)
        assert agents == []

    def test_extract_agents_single_agent(self):
        content = "## findings\n### tech-architect\nSome findings\n## convergence\nDone"
        agents = gate_checks.extract_agents_from_workspace(content)
        assert agents == ["tech-architect"]

    def test_extract_agents_excludes_devils_advocate(self):
        """devils-advocate is excluded from the agent list by design."""
        content = "## findings\n### tech-architect\nStuff\n### devils-advocate\nDA stuff\n## convergence"
        agents = gate_checks.extract_agents_from_workspace(content)
        assert "tech-architect" in agents
        assert "devils-advocate" not in agents

    def test_extract_agents_with_hyphens_and_underscores(self):
        content = "## findings\n### code-quality-analyst\nStuff\n### loan_ops_specialist\nMore\n## convergence"
        agents = gate_checks.extract_agents_from_workspace(content)
        assert "code-quality-analyst" in agents
        # Note: regex uses \w- so underscores in agent names should also work
        assert "loan_ops_specialist" in agents

    def test_extract_agents_deduplicates(self):
        """Same agent name appearing twice should only appear once."""
        content = (
            "## findings\n### tech-architect\nRound 1\n"
            "## DA R2 RESPONSES\n### tech-architect\nRound 2\n## convergence"
        )
        agents = gate_checks.extract_agents_from_workspace(content)
        assert agents.count("tech-architect") == 1

    def test_extract_agents_excludes_known_non_agents(self):
        """Headers like 'questions', 'constraints', 'claims' are not agents."""
        content = "## findings\n### questions\nQ1\n### constraints\nC1\n### tech-architect\nStuff\n## convergence"
        agents = gate_checks.extract_agents_from_workspace(content)
        assert "questions" not in agents
        assert "constraints" not in agents
        assert "tech-architect" in agents

    def test_read_workspace_missing_file(self, tmp_path):
        """read_workspace raises FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            gate_checks.read_workspace(tmp_path / "nonexistent.md")


# ===================================================================
# GATE_CHECKS DATACLASS TESTS
# ===================================================================


class TestGateChecksDataClasses:
    """Test CheckResult, ValidationResult, BeliefComponents serialization."""

    def test_check_result_to_dict_basic(self):
        cr = gate_checks.CheckResult(
            name="V3-test", passed=True, details={"count": 5}, issues=[]
        )
        d = cr.to_dict()
        assert d["name"] == "V3-test"
        assert d["passed"] is True
        assert d["details"]["count"] == 5
        assert d["issues"] == []

    def test_check_result_to_dict_with_issues(self):
        cr = gate_checks.CheckResult(
            name="V4-test", passed=False, issues=["Problem A", "Problem B"]
        )
        d = cr.to_dict()
        assert d["passed"] is False
        assert len(d["issues"]) == 2

    def test_check_result_default_fields(self):
        """details and issues default to empty."""
        cr = gate_checks.CheckResult(name="minimal", passed=True)
        assert cr.details == {}
        assert cr.issues == []

    def test_validation_result_to_dict(self):
        cr1 = gate_checks.CheckResult(name="c1", passed=True)
        cr2 = gate_checks.CheckResult(name="c2", passed=False, issues=["bad"])
        vr = gate_checks.ValidationResult(
            bundle="test-bundle",
            passed=False,
            checks=[cr1, cr2],
            context_update={"validated": False},
        )
        d = vr.to_dict()
        assert d["bundle"] == "test-bundle"
        assert d["passed"] is False
        assert len(d["checks"]) == 2
        assert d["checks"][0]["name"] == "c1"
        assert d["context_update"]["validated"] is False

    def test_validation_result_json_serializable(self):
        cr = gate_checks.CheckResult(name="c1", passed=True)
        vr = gate_checks.ValidationResult(
            bundle="b", passed=True, checks=[cr], context_update={"key": True}
        )
        # Must not raise
        serialized = json.dumps(vr.to_dict())
        assert isinstance(serialized, str)

    def test_belief_components_to_dict_no_declared(self):
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=0.8, revisions=0.7,
            gaps_penalty=0.9, da_factor=0.85, posterior=0.2142,
        )
        d = bc.to_dict()
        assert d["prior"] == 0.5
        assert d["agreement"] == 0.8
        assert d["posterior"] == 0.214  # rounded to 3
        assert "declared" not in d
        assert "divergence_flag" not in d

    def test_belief_components_to_dict_with_declared(self):
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=0.8, revisions=0.7,
            gaps_penalty=0.9, da_factor=0.85, posterior=0.30,
            declared=0.55, divergence=0.25,
        )
        d = bc.to_dict()
        assert d["declared"] == 0.55
        assert d["divergence"] == 0.25
        assert d["divergence_flag"] is True  # > 0.15

    def test_belief_components_divergence_flag_below_threshold(self):
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=0.8, revisions=0.7,
            gaps_penalty=0.9, da_factor=0.85, posterior=0.30,
            declared=0.35, divergence=0.05,
        )
        d = bc.to_dict()
        assert d["divergence_flag"] is False  # 0.05 <= 0.15

    def test_belief_components_divergence_flag_at_boundary(self):
        """Exactly 0.15 should NOT flag (> 0.15, not >=)."""
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=0.8, revisions=0.7,
            gaps_penalty=0.9, da_factor=0.85, posterior=0.30,
            declared=0.45, divergence=0.15,
        )
        d = bc.to_dict()
        assert d["divergence_flag"] is False

    def test_belief_components_declared_none_divergence_none(self):
        """When declared is None, divergence fields should not appear."""
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=1.0, revisions=0.5,
            gaps_penalty=1.0, da_factor=1.0, posterior=0.25,
            declared=None, divergence=None,
        )
        d = bc.to_dict()
        assert "declared" not in d
        assert "divergence" not in d
        assert "divergence_flag" not in d

    def test_belief_components_json_serializable(self):
        bc = gate_checks.BeliefComponents(
            prior=0.5, agreement=0.8, revisions=0.7,
            gaps_penalty=0.9, da_factor=0.85, posterior=0.2142,
            declared=0.3, divergence=0.0858,
            breakdown={"tier": 2, "agent_count": 4},
        )
        serialized = json.dumps(bc.to_dict())
        assert isinstance(serialized, str)


# ===================================================================
# GATE_CHECKS BUNDLES REGISTRY
# ===================================================================


class TestGateChecksBundles:
    """Verify BUNDLES and BELIEF_MODES registries are complete."""

    def test_expected_bundle_keys(self):
        expected = {
            "r1-convergence", "cb", "pre-synthesis",
            "plan-convergence", "plan-lock", "build-checkpoint",
            "challenge-round", "compilation", "session-end",
            "tier-a-coverage",
        }
        assert expected.issubset(set(gate_checks.BUNDLES.keys()))

    def test_all_bundle_values_are_callable(self):
        for name, fn in gate_checks.BUNDLES.items():
            assert callable(fn), f"Bundle '{name}' value is not callable"

    def test_expected_belief_mode_keys(self):
        expected = {"analyze", "build-plan", "build-quality", "analyze-tier-a"}
        assert expected.issubset(set(gate_checks.BELIEF_MODES.keys()))

    def test_all_belief_modes_callable(self):
        for name, fn in gate_checks.BELIEF_MODES.items():
            assert callable(fn), f"Belief mode '{name}' value is not callable"

    def test_run_validation_unknown_bundle(self):
        """Unknown bundle name returns error dict, not exception."""
        result = gate_checks.run_validation("nonexistent-bundle", None)
        assert "error" in result
        assert "nonexistent-bundle" in result["error"]

    def test_run_compute_belief_unknown_mode(self):
        """Unknown belief mode returns error dict, not exception."""
        result = gate_checks.run_compute_belief("nonexistent-mode", None)
        assert "error" in result

    def test_phase_required_validations_mapping(self):
        """Verify the PHASE_REQUIRED_VALIDATIONS dict inside cmd_advance
        maps to known bundle names."""
        # This dict is defined inline in cmd_advance -- replicate it to test
        phase_validations = {
            "plan": "plan-convergence",
            "challenge_plan": "challenge-round",
            "build": "build-checkpoint",
            "review": "pre-synthesis",
            "research": "r1-convergence",
            "circuit_breaker": "cb",
            "challenge": "challenge-round",
        }
        for phase, bundle in phase_validations.items():
            assert bundle in gate_checks.BUNDLES, (
                f"Phase '{phase}' maps to bundle '{bundle}' which is not in BUNDLES"
            )

    def test_run_validation_with_workspace_file(self, tmp_path):
        """run_validation with a real workspace file and simple bundle."""
        ws = tmp_path / "workspace.md"
        ws.write_text(
            "## findings\n\n## convergence\n"
            "CB[1] divergence detected\nCB[2] confirmed\n"
            "divergence logged\n",
            encoding="utf-8",
        )
        result = gate_checks.run_validation("cb", str(ws))
        assert "passed" in result
        # cb checks for divergence_logged or CB entries -- our content has both
        assert result["passed"] is True

    def test_run_validation_cb_fails_on_empty_workspace(self, tmp_path):
        """Circuit breaker validation fails when no CB markers present."""
        ws = tmp_path / "workspace.md"
        ws.write_text("## findings\nSome generic text\n## convergence\n", encoding="utf-8")
        result = gate_checks.run_validation("cb", str(ws))
        assert result["passed"] is False


# ===================================================================
# ORCHESTRATOR-CONFIG STRUCTURAL TESTS (no hateoas needed)
# ===================================================================


class TestOrchestratorConfigFileStructure:
    """Structural tests that parse the file as text -- always run."""

    @pytest.fixture(autouse=True)
    def _load_source(self):
        source_path = Path(_shared_dir) / "orchestrator-config.py"
        self.source = source_path.read_text(encoding="utf-8")

    def test_file_exists(self):
        assert (Path(_shared_dir) / "orchestrator-config.py").exists()

    def test_defines_build_analyze_workflow(self):
        assert "def build_analyze_workflow" in self.source

    def test_defines_build_build_workflow(self):
        assert "def build_build_workflow" in self.source

    def test_defines_load_or_create(self):
        assert "def _load_or_create" in self.source

    def test_defines_save(self):
        assert "def _save" in self.source

    def test_defines_cmd_start(self):
        assert "def cmd_start" in self.source

    def test_defines_cmd_advance(self):
        assert "def cmd_advance" in self.source

    def test_defines_cmd_validate(self):
        assert "def cmd_validate" in self.source

    def test_defines_cmd_watch(self):
        assert "def cmd_watch" in self.source

    def test_team_created_guard_in_cmd_start(self):
        """cmd_start must enforce team_created in context."""
        assert "team_created" in self.source

    def test_force_restart_guard(self):
        """cmd_start must check for force_restart before overwriting active session."""
        assert "force_restart" in self.source

    def test_mode_mismatch_check(self):
        """_load_or_create checks saved mode vs current mode."""
        assert "Mode mismatch" in self.source

    def test_atomic_write_pattern(self):
        """_save uses atomic rename pattern."""
        assert "os.replace" in self.source

    def test_phase_required_validations_defined(self):
        """PHASE_REQUIRED_VALIDATIONS dict exists in cmd_advance."""
        assert "PHASE_REQUIRED_VALIDATIONS" in self.source

    def test_hard_cap_round_limit_5(self):
        """Round limit of 5 is used as hard cap."""
        assert "round_limit(5" in self.source
