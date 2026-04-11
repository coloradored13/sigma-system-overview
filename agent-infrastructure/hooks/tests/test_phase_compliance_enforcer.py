"""Tests for phase-compliance-enforcer.py — PreToolUse/PostToolUse/Stop hook.

Tests the mechanical enforcement layer for sigma-review and sigma-build:
  1. Phase skip detection (blocks reading future phase files)
  2. BELIEF tracking (warns when missing during challenge/review)
  3. Synthesis file gate (warns when advancing past synthesis without file)
  4. State tracking (validation runs, advance resets)
  5. Fast exit when not in active session
  6. Both ANALYZE and BUILD mode enforcement
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
enforcer = importlib.import_module("phase-compliance-enforcer")

HOOKS_DIR = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_checkpoint(tmp_path, monkeypatch):
    """Create a temporary checkpoint file and wire it up."""
    cp = tmp_path / "checkpoint.json"
    monkeypatch.setattr(enforcer, "DEFAULT_CHECKPOINT", cp)

    def _write(data):
        cp.write_text(json.dumps(data), encoding="utf-8")
        return cp

    return _write


@pytest.fixture
def tmp_state(tmp_path, monkeypatch):
    """Wire state file to tmp."""
    sf = tmp_path / ".phase-compliance-state.json"
    monkeypatch.setattr(enforcer, "STATE_FILE", sf)
    return sf


@pytest.fixture
def analyze_checkpoint(tmp_checkpoint):
    """Active ANALYZE checkpoint in challenge phase."""
    return tmp_checkpoint({
        "_mode": "analyze",
        "current_phase": "challenge",
        "phase_history": ["research", "circuit_breaker", "challenge"],
        "context": {"r1_converged": True, "cb_validated": True},
    })


@pytest.fixture
def build_checkpoint(tmp_checkpoint):
    """Active BUILD checkpoint in review phase."""
    return tmp_checkpoint({
        "_mode": "build",
        "current_phase": "review",
        "phase_history": ["plan", "challenge_plan", "build", "review"],
        "context": {"plans_ready": True, "build_complete": True},
    })


# ---------------------------------------------------------------------------
# Phase ordering helpers
# ---------------------------------------------------------------------------

class TestPhaseOrdering:
    def test_analyze_phase_order_has_all_phases(self):
        assert "research" in enforcer.ANALYZE_PHASE_ORDER
        assert "synthesis" in enforcer.ANALYZE_PHASE_ORDER
        assert "complete" in enforcer.ANALYZE_PHASE_ORDER
        assert enforcer.ANALYZE_PHASE_ORDER[-1] == "complete"

    def test_build_phase_order_has_all_phases(self):
        assert "plan" in enforcer.BUILD_PHASE_ORDER
        assert "review" in enforcer.BUILD_PHASE_ORDER
        assert "complete" in enforcer.BUILD_PHASE_ORDER
        assert enforcer.BUILD_PHASE_ORDER[-1] == "complete"

    def test_phase_index_returns_correct_position(self):
        assert enforcer.phase_index("research", enforcer.ANALYZE_PHASE_ORDER) == 1
        assert enforcer.phase_index("challenge", enforcer.ANALYZE_PHASE_ORDER) == 3

    def test_phase_index_unknown_returns_negative(self):
        assert enforcer.phase_index("nonexistent", enforcer.ANALYZE_PHASE_ORDER) == -1

    def test_analyze_map_covers_all_files(self):
        assert len(enforcer.ANALYZE_PHASE_MAP) == 12

    def test_build_map_covers_all_files(self):
        assert len(enforcer.BUILD_PHASE_MAP) == 13


class TestExtractPhaseFromPath:
    def test_review_phase_file(self):
        stem, mode = enforcer.extract_phase_from_path(
            "/Users/x/.claude/skills/sigma-review/phases/04-challenge.md"
        )
        assert stem == "04-challenge"
        assert mode == "analyze"

    def test_build_phase_file(self):
        stem, mode = enforcer.extract_phase_from_path(
            "/Users/x/.claude/skills/sigma-build/phases/02-plan.md"
        )
        assert stem == "02-plan"
        assert mode == "build"

    def test_non_phase_file(self):
        stem, mode = enforcer.extract_phase_from_path("/Users/x/project/src/main.py")
        assert stem is None
        assert mode is None

    def test_skill_md_not_phase(self):
        stem, mode = enforcer.extract_phase_from_path(
            "/Users/x/.claude/skills/sigma-review/SKILL.md"
        )
        assert stem is None


# ---------------------------------------------------------------------------
# Phase skip detection (PreToolUse BLOCK)
# ---------------------------------------------------------------------------

class TestPhaseSkipDetection:
    def test_allows_current_phase_file(self, analyze_checkpoint):
        """Reading the file for the current phase is fine."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-review/phases/04-challenge.md", cp
        )
        assert not should_block

    def test_allows_past_phase_file(self, analyze_checkpoint):
        """Reading a phase file we've already completed is fine."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-review/phases/02-research.md", cp
        )
        assert not should_block

    def test_allows_next_phase_file(self, analyze_checkpoint):
        """Reading the NEXT phase (valid transition) is allowed."""
        cp = json.loads(analyze_checkpoint.read_text())
        # challenge → debate is the next phase
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-review/phases/05-debate.md", cp
        )
        assert not should_block

    def test_blocks_skipping_multiple_phases(self, analyze_checkpoint):
        """Reading a phase 2+ ahead is blocked."""
        cp = json.loads(analyze_checkpoint.read_text())
        # challenge → synthesis (skipping debate) = skip
        should_block, reason = enforcer.check_phase_skip(
            "/x/sigma-review/phases/06-synthesis.md", cp
        )
        assert should_block
        assert "PHASE SKIP BLOCKED" in reason
        assert "challenge" in reason
        assert "synthesis" in reason

    def test_blocks_skipping_to_shutdown(self, analyze_checkpoint):
        """Can't jump from challenge to shutdown."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, reason = enforcer.check_phase_skip(
            "/x/sigma-review/phases/10-shutdown.md", cp
        )
        assert should_block

    def test_blocks_post_exit_gate_skip(self, tmp_checkpoint):
        """Can't skip from synthesis to archive (skipping compilation+promotion+sync)."""
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, reason = enforcer.check_phase_skip(
            "/x/sigma-review/phases/09-archive.md", cp
        )
        assert should_block

    def test_allows_preflight_always(self, analyze_checkpoint):
        """00-preflight is always allowed."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-review/phases/00-preflight.md", cp
        )
        assert not should_block

    def test_allows_spawn_always(self, analyze_checkpoint):
        """01-spawn is always allowed."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-review/phases/01-spawn.md", cp
        )
        assert not should_block

    def test_build_mode_phase_skip(self, build_checkpoint):
        """BUILD mode: can't skip from review to archive."""
        cp = json.loads(build_checkpoint.read_text())
        should_block, reason = enforcer.check_phase_skip(
            "/x/sigma-build/phases/09-archive.md", cp
        )
        assert should_block
        assert "review" in reason

    def test_build_allows_next_phase(self, build_checkpoint):
        """BUILD mode: reading the next phase (synthesis) is allowed."""
        cp = json.loads(build_checkpoint.read_text())
        # review → debate is allowed as next in BUILD ordering
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-build/phases/05b-debate.md", cp
        )
        assert not should_block

    def test_ignores_non_phase_reads(self, analyze_checkpoint):
        """Non-phase files are never blocked."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip("/Users/x/project/main.py", cp)
        assert not should_block

    def test_ignores_mode_mismatch(self, analyze_checkpoint):
        """Reading build phases during analyze is ignored (not blocked)."""
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_phase_skip(
            "/x/sigma-build/phases/02-plan.md", cp
        )
        assert not should_block


# ---------------------------------------------------------------------------
# BELIEF tracking (PostToolUse WARN)
# ---------------------------------------------------------------------------

class TestBeliefTracking:
    def test_detects_belief_in_workspace_write(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md",
            "Some findings\nBELIEF[P(viable)=0.72]\nMore content",
            cp,
        )
        assert result is None  # No warning — BELIEF was written
        state = enforcer.read_state()
        assert state.get("belief_written_current_phase") is True

    def test_warns_missing_belief(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md",
            "Some findings without belief scores, just regular content padding out the workspace",
            cp,
        )
        assert result is not None
        assert "BELIEF[] MISSING" in result

    def test_no_warn_outside_belief_phases(self, tmp_checkpoint, tmp_state):
        """BELIEF not required during synthesis."""
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md",
            "Synthesis content without BELIEF",
            cp,
        )
        assert result is None

    def test_no_warn_non_workspace_write(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/project/src/main.py",
            "Code without BELIEF",
            cp,
        )
        assert result is None

    def test_belief_required_in_build_review(self, build_checkpoint, tmp_state):
        cp = json.loads(build_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md",
            "Review findings but no belief",
            cp,
        )
        assert result is not None
        assert "BELIEF" in result

    def test_belief_required_in_challenge_plan(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "build",
            "current_phase": "challenge_plan",
            "phase_history": ["plan", "challenge_plan"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md",
            "Plan challenge without belief",
            cp,
        )
        assert result is not None


# ---------------------------------------------------------------------------
# Synthesis file gate (PostToolUse WARN)
# ---------------------------------------------------------------------------

class TestSynthesisFileGate:
    def test_tracks_synthesis_write(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        enforcer.track_synthesis_write("/x/shared/synthesis-report.md", "Full synthesis", cp)
        state = enforcer.read_state()
        assert state.get("synthesis_file_written") is True

    def test_warns_advance_without_synthesis_file(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        result = enforcer.check_synthesis_before_advance(
            "python3 orchestrator-config.py --mode analyze advance", cp
        )
        assert result is not None
        assert "SYNTHESIS FILE GATE" in result

    def test_no_warn_after_synthesis_written(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        enforcer.update_state(synthesis_file_written=True)
        result = enforcer.check_synthesis_before_advance(
            "python3 orchestrator-config.py --mode analyze advance", cp
        )
        assert result is None

    def test_no_warn_non_synthesis_phase(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.check_synthesis_before_advance(
            "python3 orchestrator-config.py --mode analyze advance", cp
        )
        assert result is None


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

class TestStateManagement:
    def test_read_empty_state(self, tmp_state):
        assert enforcer.read_state() == {}

    def test_write_and_read_state(self, tmp_state):
        enforcer.write_state({"key": "value", "count": 42})
        state = enforcer.read_state()
        assert state["key"] == "value"
        assert state["count"] == 42

    def test_update_state_merges(self, tmp_state):
        enforcer.write_state({"a": 1, "b": 2})
        enforcer.update_state(b=3, c=4)
        state = enforcer.read_state()
        assert state == {"a": 1, "b": 3, "c": 4}

    def test_advance_resets_per_phase_state(self, analyze_checkpoint, tmp_state):
        enforcer.update_state(
            validations_this_phase=["r1-convergence"],
            belief_written_current_phase=True,
        )
        cp = json.loads(analyze_checkpoint.read_text())
        enforcer.track_advance("python3 orchestrator-config.py advance", cp)
        state = enforcer.read_state()
        assert state["validations_this_phase"] == []
        assert state["belief_written_current_phase"] is False

    def test_validation_tracking(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        enforcer.track_validation_run(
            "python3 orchestrator-config.py validate --check challenge-round", cp
        )
        state = enforcer.read_state()
        assert "challenge-round" in state["validations_this_phase"]

    def test_validation_tracking_deduplicates(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        enforcer.track_validation_run(
            "python3 orchestrator-config.py validate --check challenge-round", cp
        )
        enforcer.track_validation_run(
            "python3 orchestrator-config.py validate --check challenge-round", cp
        )
        state = enforcer.read_state()
        assert state["validations_this_phase"].count("challenge-round") == 1


# ---------------------------------------------------------------------------
# Checkpoint reading
# ---------------------------------------------------------------------------

class TestCheckpointReading:
    def test_no_checkpoint_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(enforcer, "DEFAULT_CHECKPOINT", tmp_path / "nope.json")
        assert enforcer.read_checkpoint() is None

    def test_completed_session_returns_none(self, tmp_checkpoint):
        tmp_checkpoint({"_mode": "analyze", "current_phase": "complete"})
        assert enforcer.read_checkpoint() is None

    def test_null_phase_returns_none(self, tmp_checkpoint):
        tmp_checkpoint({"_mode": "analyze", "current_phase": None})
        assert enforcer.read_checkpoint() is None

    def test_active_session_returns_data(self, analyze_checkpoint):
        cp = enforcer.read_checkpoint()
        assert cp is not None
        assert cp["current_phase"] == "challenge"

    def test_corrupt_checkpoint_returns_none(self, tmp_checkpoint):
        Path(enforcer.DEFAULT_CHECKPOINT).write_text("not json{{{")
        assert enforcer.read_checkpoint() is None


# ---------------------------------------------------------------------------
# DA exit-gate BLOCK
# ---------------------------------------------------------------------------

class TestDAExitGateBlock:
    def test_blocks_advance_without_exit_gate(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        """BLOCK advance from challenge when no exit-gate: PASS in workspace."""
        ws = tmp_path / "workspace.md"
        ws.write_text("## findings\nSome findings\n## convergence\nagent: ✓\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(analyze_checkpoint.read_text())
        should_block, reason = enforcer.check_da_exit_gate_in_workspace(
            "python3 orchestrator-config.py --mode analyze advance", cp
        )
        assert should_block
        assert "DA EXIT-GATE BLOCKED" in reason

    def test_allows_advance_with_exit_gate_pass(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## DA-assessment\nexit-gate: PASS |engagement:B+ |unresolved:none\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_da_exit_gate_in_workspace(
            "python3 orchestrator-config.py --mode analyze advance", cp
        )
        assert not should_block

    def test_ignores_non_advance_commands(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_da_exit_gate_in_workspace(
            "python3 orchestrator-config.py status", cp
        )
        assert not should_block

    def test_ignores_non_da_phases(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## synthesis\nNo exit gate here\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.check_da_exit_gate_in_workspace(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_build_mode_review_phase(self, build_checkpoint, tmp_state, tmp_path, monkeypatch):
        """BUILD mode review also requires DA exit-gate."""
        ws = tmp_path / "workspace.md"
        ws.write_text("## review\nNo exit gate\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(build_checkpoint.read_text())
        should_block, reason = enforcer.check_da_exit_gate_in_workspace(
            "python3 orchestrator-config.py advance", cp
        )
        assert should_block
        assert "DA EXIT-GATE" in reason


# ---------------------------------------------------------------------------
# BELIEF on advance BLOCK
# ---------------------------------------------------------------------------

class TestBeliefOnAdvanceBlock:
    def test_blocks_advance_without_belief(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## findings\nNo belief scores\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(analyze_checkpoint.read_text())
        should_block, reason = enforcer.check_belief_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert should_block
        assert "BELIEF BLOCKED" in reason

    def test_allows_advance_with_belief_in_workspace(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## gate-log\nBELIEF[P(viable)=0.72]\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_belief_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_allows_advance_with_belief_in_state(self, analyze_checkpoint, tmp_state):
        enforcer.update_state(belief_written_current_phase=True)
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_belief_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_ignores_non_belief_phases(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.check_belief_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_build_challenge_plan(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "build", "current_phase": "challenge_plan",
            "phase_history": ["plan", "challenge_plan"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## plan-track\nNo belief\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, reason = enforcer.check_belief_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert should_block


# ---------------------------------------------------------------------------
# CB evidence BLOCK
# ---------------------------------------------------------------------------

class TestCBEvidenceBlock:
    def test_blocks_advance_without_cb_evidence(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "circuit_breaker",
            "phase_history": ["research", "circuit_breaker"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## convergence\nAll agents agreed on everything\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, reason = enforcer.check_cb_evidence_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert should_block
        assert "CB EVIDENCE BLOCKED" in reason

    def test_allows_with_divergence_log(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "circuit_breaker",
            "phase_history": ["research", "circuit_breaker"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## circuit-breaker\nR1 divergence detected: agent-a disagrees on market sizing\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.check_cb_evidence_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_allows_with_cb_entries(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "circuit_breaker",
            "phase_history": ["research", "circuit_breaker"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("CB[1] tech-architect: strongest counter to own position\nCB[2] product-strategist: strongest counter\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.check_cb_evidence_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block

    def test_ignores_non_cb_phase(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.check_cb_evidence_before_advance(
            "python3 orchestrator-config.py advance", cp
        )
        assert not should_block


# ---------------------------------------------------------------------------
# Lead synthesis write BLOCK
# ---------------------------------------------------------------------------

class TestLeadSynthesisBlock:
    def test_blocks_synthesis_write_without_agent(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## convergence\nagent-a: ✓\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, reason = enforcer.block_lead_synthesis_write(
            "/x/shared/synthesis-report.md", cp
        )
        assert should_block
        assert "LEAD SYNTHESIS BLOCKED" in reason

    def test_allows_with_synthesis_agent_evidence(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## convergence\n### synthesis-agent\nsynthesis-agent: ✓ complete\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.block_lead_synthesis_write(
            "/x/shared/synthesis-report.md", cp
        )
        assert not should_block

    def test_ignores_non_synthesis_files(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        cp = json.loads(Path(enforcer.DEFAULT_CHECKPOINT).read_text())
        should_block, _ = enforcer.block_lead_synthesis_write("/x/src/main.py", cp)
        assert not should_block

    def test_ignores_non_synthesis_phase(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        should_block, _ = enforcer.block_lead_synthesis_write(
            "/x/shared/synthesis-report.md", cp
        )
        assert not should_block


# ---------------------------------------------------------------------------
# BELIEF format WARN
# ---------------------------------------------------------------------------

class TestBeliefFormatWarn:
    def test_warns_malformed_belief(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md", "BELIEF[high confidence]", cp
        )
        assert result is not None
        assert "BELIEF FORMAT" in result

    def test_no_warn_valid_belief(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md", "BELIEF[P(viable)=0.72]", cp
        )
        assert result is None

    def test_no_warn_multiple_valid(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.track_belief_write(
            "/x/workspace.md", "BELIEF[P(plan-ready)=0.88] and BELIEF[P(quality)=0.75]", cp
        )
        assert result is None


# ---------------------------------------------------------------------------
# Context firewall WARN
# ---------------------------------------------------------------------------

class TestContextFirewallWarn:
    def test_detects_career_context(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.detect_context_firewall_leak(
            "/x/workspace.md", "Analysis shows my career path requires this pivot", cp
        )
        assert result is not None
        assert "CONTEXT FIREWALL" in result

    def test_detects_role_context(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.detect_context_firewall_leak(
            "/x/workspace.md", "Given my role at the company, this makes sense", cp
        )
        assert result is not None

    def test_ignores_analytical_content(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.detect_context_firewall_leak(
            "/x/workspace.md", "The market analysis shows technology differentiation is key", cp
        )
        assert result is None

    def test_ignores_non_workspace(self, analyze_checkpoint, tmp_state):
        cp = json.loads(analyze_checkpoint.read_text())
        result = enforcer.detect_context_firewall_leak(
            "/x/src/main.py", "my career context here", cp
        )
        assert result is None


# ---------------------------------------------------------------------------
# Integration: PreToolUse dispatch (expanded)
# ---------------------------------------------------------------------------

class TestPreToolUseDispatch:
    def test_no_session_passes(self, tmp_path, monkeypatch):
        monkeypatch.setattr(enforcer, "DEFAULT_CHECKPOINT", tmp_path / "nope.json")
        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/x/sigma-review/phases/10-shutdown.md"},
        })
        assert exit_code == 0

    def test_blocks_phase_skip(self, analyze_checkpoint):
        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/x/sigma-review/phases/06-synthesis.md"},
        })
        assert exit_code == 2
        assert "PHASE SKIP" in output.get("reason", "")

    def test_allows_valid_read(self, analyze_checkpoint):
        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/x/sigma-review/phases/04-challenge.md"},
        })
        assert exit_code == 0

    def test_blocks_advance_without_da_exit_gate(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## findings\nNo exit gate\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "python3 orchestrator-config.py --mode analyze advance"},
        })
        assert exit_code == 2
        assert "DA EXIT-GATE" in output.get("reason", "")

    def test_blocks_advance_without_belief(self, analyze_checkpoint, tmp_state, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## findings\nexit-gate: PASS\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "python3 orchestrator-config.py advance"},
        })
        assert exit_code == 2
        assert "BELIEF BLOCKED" in output.get("reason", "")

    def test_blocks_synthesis_write_by_lead(self, tmp_checkpoint, tmp_state, tmp_path, monkeypatch):
        tmp_checkpoint({
            "_mode": "analyze", "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        ws = tmp_path / "workspace.md"
        ws.write_text("## convergence\nagent: ✓\n", encoding="utf-8")
        monkeypatch.setattr(enforcer, "DEFAULT_WORKSPACE", ws)

        exit_code, output = enforcer.enforce_pre_tool_use({
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/x/shared/synthesis-report.md", "content": "Lead synthesis"},
        })
        assert exit_code == 2
        assert "LEAD SYNTHESIS" in output.get("reason", "")


# ---------------------------------------------------------------------------
# Integration: PostToolUse dispatch
# ---------------------------------------------------------------------------

class TestPostToolUseDispatch:
    def test_no_session_returns_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(enforcer, "DEFAULT_CHECKPOINT", tmp_path / "nope.json")
        output = enforcer.enforce_post_tool_use({
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/x/workspace.md", "content": "stuff"},
        })
        assert output == {}

    def test_warns_on_missing_belief(self, analyze_checkpoint, tmp_state):
        output = enforcer.enforce_post_tool_use({
            "hook_event_name": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {"file_path": "/x/workspace.md", "content": "findings no belief"},
        })
        assert "BELIEF" in output.get("systemMessage", "")


# ---------------------------------------------------------------------------
# Integration: Stop dispatch
# ---------------------------------------------------------------------------

class TestStopDispatch:
    def test_no_session_returns_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(enforcer, "DEFAULT_CHECKPOINT", tmp_path / "nope.json")
        output = enforcer.enforce_stop({"hook_event_name": "Stop"})
        assert output == {}

    def test_warns_missing_belief_at_stop(self, analyze_checkpoint, tmp_state):
        output = enforcer.enforce_stop({"hook_event_name": "Stop"})
        assert "BELIEF" in output.get("systemMessage", "")

    def test_no_warn_when_belief_written(self, analyze_checkpoint, tmp_state):
        enforcer.update_state(belief_written_current_phase=True)
        output = enforcer.enforce_stop({"hook_event_name": "Stop"})
        assert output == {}

    def test_no_warn_outside_belief_phase(self, tmp_checkpoint, tmp_state):
        tmp_checkpoint({
            "_mode": "analyze",
            "current_phase": "synthesis",
            "phase_history": ["research", "circuit_breaker", "challenge", "synthesis"],
        })
        output = enforcer.enforce_stop({"hook_event_name": "Stop"})
        assert output == {}


# ---------------------------------------------------------------------------
# Integration: subprocess smoke tests
# ---------------------------------------------------------------------------

def run_enforcer(stdin_data, home_dir=None):
    script = HOOKS_DIR / "phase-compliance-enforcer.py"
    env = os.environ.copy()
    if home_dir:
        env["HOME"] = str(home_dir)
    result = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(stdin_data),
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )
    return result


class TestSubprocessSmoke:
    def test_garbage_stdin(self):
        script = HOOKS_DIR / "phase-compliance-enforcer.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            input="not json",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0

    def test_empty_stdin(self):
        script = HOOKS_DIR / "phase-compliance-enforcer.py"
        result = subprocess.run(
            [sys.executable, str(script)],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0

    def test_no_checkpoint_exits_clean(self):
        result = run_enforcer({
            "hook_event_name": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/x/sigma-review/phases/10-shutdown.md"},
        })
        assert result.returncode == 0

    def test_unknown_event_exits_clean(self):
        result = run_enforcer({
            "hook_event_name": "SessionStart",
            "tool_name": "irrelevant",
        })
        assert result.returncode == 0

    def test_phase_skip_blocks_via_subprocess(self, tmp_path):
        """Full subprocess test: checkpoint exists → phase skip → exit code 2."""
        # Create checkpoint in /tmp (default location)
        cp = Path("/tmp/sigma-review-orchestrator.json")
        backup = None
        if cp.exists():
            backup = cp.read_text()

        try:
            cp.write_text(json.dumps({
                "_mode": "analyze",
                "current_phase": "research",
                "phase_history": ["research"],
            }))

            result = run_enforcer({
                "hook_event_name": "PreToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "/x/sigma-review/phases/06-synthesis.md"},
            })
            assert result.returncode == 2
            output = json.loads(result.stdout)
            assert "PHASE SKIP" in output.get("reason", "")
        finally:
            if backup:
                cp.write_text(backup)
            elif cp.exists():
                cp.unlink()
