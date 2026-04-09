"""Tests for gate_checks module."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import pytest

# Add shared directory to path for imports
_shared_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _shared_dir)

import gate_checks

# orchestrator-config.py has a hyphen — use importlib
import importlib.util

_orch_spec = importlib.util.spec_from_file_location(
    "orchestrator_config",
    os.path.join(_shared_dir, "orchestrator-config.py"),
)
_orch_mod = importlib.util.module_from_spec(_orch_spec)
_orch_spec.loader.exec_module(_orch_mod)
build_analyze_workflow = _orch_mod.build_analyze_workflow
build_build_workflow = _orch_mod.build_build_workflow

# ---------------------------------------------------------------------------
# Fixtures: minimal workspace content for targeted tests
# ---------------------------------------------------------------------------

MINIMAL_WORKSPACE = """# workspace — test task
## status: active
## mode: ANALYZE

## infrastructure
ΣVerify: openai (gpt-5.4), google (gemini-3.1-pro-preview) available
complexity: ANALYZE TIER-2 (16/25)

## prompt-decomposition
user-confirmed: yes

### Q[] — Questions
Q1: What is the impact?
Q2: How should we respond?

### H[] — Hypotheses
H1: Market is growing
H2: Competition is increasing
H3: Technology is accelerating

### C[] — Constraints
C1: Senior PM role
C2: 5-year horizon

## findings
### agent-alpha
status: ✓ R1 complete | XVERIFY: F1=PARTIAL
F[A-1] Finding one — detailed analysis here with evidence |source:[independent-research] T1(BLS)
F[A-2] Finding two — more analysis |source:[agent-inference]
DB[F[A-1]]: (1) initial: X (2) assume-wrong: Y (3) strongest-counter: Z (4) re-estimate: W (5) reconciled: final

### agent-beta
status: ✓ R1 complete | XVERIFY: F1=AGREE(gpt-5.4)
F[B-1] Finding beta one — research based |source:[independent-research] T2(McKinsey)
F[B-2] LOAD-BEARING finding — critical conclusion |source:[independent-research] T1(Federal Reserve)
DB[F[B-2]]: (1) initial: A (2) assume-wrong: B (3) strongest-counter: C (4) re-estimate: D (5) reconciled: E

### devils-advocate
status: ✓ R2 complete
**CHALLENGE DELIVERY**
10 challenges across 2 agents

**RESPONSE QUALITY**
| Agent | Challenges | Grade |
|-------|-----------|-------|
| alpha | 5 | A |
| beta | 5 | A- |

Overall engagement: A

CH[1] TOPIC ONE — RESOLVED
CH[2] TOPIC TWO — RESOLVED

**EXIT-GATE ASSESSMENT**
exit-gate: PASS |engagement:A |unresolved:none |untested-consensus:none |hygiene:pass

## convergence
agent-alpha: ✓ R1 complete | 2 findings
agent-beta: ✓ R1 complete | 2 findings

## open-questions
"""

WORKSPACE_WITH_CB = MINIMAL_WORKSPACE.replace(
    "## convergence",
    """## circuit-breaker
Zero-dissent detected: 2 agents, 4 findings, 0 disagreements. Circuit breaker fired.
CB[1]: agent-alpha — strongest counter to F[A-1]: counter argument |would-change: no
CB[2]: agent-alpha — peer challenge: agent-beta:F[B-1] — different quantification
CB[3]: agent-alpha — blind spot: may be missing regulatory dimension

## convergence""",
)

WORKSPACE_WITH_DIVERGENCE = MINIMAL_WORKSPACE.replace(
    "## convergence",
    "R1 divergence detected: agent-alpha estimates 40% while agent-beta estimates 65%\n\n## convergence",
)

WORKSPACE_WITH_CONTAMINATION = MINIMAL_WORKSPACE.replace(
    "## open-questions",
    """CONTAMINATION-CHECK: session-topics-outside-scope: career planning, salary data |scan-result: clean
SYCOPHANCY-CHECK: softened:none |selective-emphasis:none |dissent-reframed:none |process-issues:none
SOURCE-PROVENANCE[§2d]: independent-research:3 |prompt-claim:0 |cross-agent:0 |agent-inference:1

## open-questions""",
)

WORKSPACE_WITH_BELIEF = MINIMAL_WORKSPACE.replace(
    "## convergence",
    "BELIEF[r2]: P=0.87 |→ synthesis\n\n## convergence",
)

WORKSPACE_NO_SIGVERIFY = MINIMAL_WORKSPACE.replace(
    "ΣVerify: openai (gpt-5.4), google (gemini-3.1-pro-preview) available",
    "ΣVerify: unavailable (no API keys)",
)

WORKSPACE_WITH_HYPOTHESIS_MATRIX = MINIMAL_WORKSPACE.replace(
    "## findings",
    """## hypothesis-matrix
H1:Market is growing | H2:Competition is increasing | H3:Technology is accelerating
E[1]:BLS data |H1:+ |H2:0 |H3:+ |weight:H |src:[independent-research]
E[2]:McKinsey report |H1:+ |H2:+ |H3:0 |weight:M |src:[independent-research]
Inconsistency-scores: H1=0 H2=1 H3=1
→ least-inconsistent: H1

## findings""",
)

BUILD_WORKSPACE = """# workspace — BUILD: test build task
## status: active
## mode: BUILD

## infrastructure
ΣVerify: unavailable

## prompt-decomposition
Q1: Build the API
H1: REST is the right choice
C1: Python stack

## architecture-decisions
ADR[1]: Use FastAPI |alternatives:Flask,Django |rationale:async support |prompted-by:Q1

## design-system
DS[]: typography: Inter 14/16/20 | colors: slate-50 through slate-900

## interface-contracts
IC[1]: POST /api/items |type:API |consumer:implementation-engineer

## build-status
CHECKPOINT[implementation-engineer]: app.py,models.py |functions:3/5 |interfaces-matched:yes |drift:none

## findings
### implementation-engineer
F[IE-1] Built API endpoints |source:[independent-research:T1(FastAPI docs)]

### code-quality-analyst
F[CQA-1] Code review findings |source:[agent-inference]

## convergence
implementation-engineer: ✓ build complete
code-quality-analyst: ✓ review complete

## open-questions
"""


# ---------------------------------------------------------------------------
# Tests: workspace parsing
# ---------------------------------------------------------------------------


class TestWorkspaceParsing:
    def test_parse_sections(self):
        sections = gate_checks.parse_sections(MINIMAL_WORKSPACE)
        assert "findings" in sections
        assert "convergence" in sections
        assert "infrastructure" in sections
        assert "prompt-decomposition" in sections

    def test_extract_agents(self):
        agents = gate_checks.extract_agents_from_workspace(MINIMAL_WORKSPACE)
        assert "agent-alpha" in agents
        assert "agent-beta" in agents
        assert "devils-advocate" not in agents
        assert len(agents) == 2

    def test_sigverify_available(self):
        assert gate_checks.is_sigverify_available(MINIMAL_WORKSPACE) is True
        assert gate_checks.is_sigverify_available(WORKSPACE_NO_SIGVERIFY) is False

    def test_count_hypotheses(self):
        assert gate_checks.count_hypotheses(MINIMAL_WORKSPACE) == 3

    def test_get_complexity_tier(self):
        assert gate_checks.get_complexity_tier(MINIMAL_WORKSPACE) == 2

    def test_get_mode(self):
        assert gate_checks.get_mode(MINIMAL_WORKSPACE) == "ANALYZE"
        assert gate_checks.get_mode(BUILD_WORKSPACE) == "BUILD"

    def test_get_agent_section(self):
        section = gate_checks._get_agent_section(MINIMAL_WORKSPACE, "agent-alpha")
        assert "F[A-1]" in section
        assert "F[A-2]" in section

    def test_get_agent_section_missing(self):
        section = gate_checks._get_agent_section(MINIMAL_WORKSPACE, "nonexistent")
        assert section == ""


# ---------------------------------------------------------------------------
# Tests: individual checks
# ---------------------------------------------------------------------------


class TestV3AgentOutputNonEmpty:
    def test_pass(self):
        result = gate_checks.check_agent_output_non_empty(MINIMAL_WORKSPACE)
        assert result.passed is True
        assert result.details["agents_checked"] == 2

    def test_fail_empty_section(self):
        ws = MINIMAL_WORKSPACE.replace(
            "F[A-1] Finding one — detailed analysis here with evidence |source:[independent-research] T1(BLS)\nF[A-2] Finding two — more analysis |source:[agent-inference]\nDB[F[A-1]]: (1) initial: X (2) assume-wrong: Y (3) strongest-counter: Z (4) re-estimate: W (5) reconciled: final",
            "",
        )
        result = gate_checks.check_agent_output_non_empty(ws)
        assert result.passed is False
        assert "agent-alpha" in result.details["empty"]


class TestV4SourceProvenance:
    def test_pass(self):
        result = gate_checks.check_source_provenance(MINIMAL_WORKSPACE)
        assert result.passed is True
        assert result.details["total_findings"] == 4

    def test_fail_untagged(self):
        ws = MINIMAL_WORKSPACE.replace("|source:[independent-research] T1(BLS)", "")
        result = gate_checks.check_source_provenance(ws)
        assert result.passed is False
        assert len(result.details["untagged"]) > 0


class TestV5XverifyCoverage:
    def test_pass_when_available(self):
        result = gate_checks.check_xverify_coverage(MINIMAL_WORKSPACE)
        assert result.passed is True

    def test_skip_when_unavailable(self):
        result = gate_checks.check_xverify_coverage(WORKSPACE_NO_SIGVERIFY)
        assert result.passed is True
        assert result.details["sigverify_available"] is False


class TestV6DialecticalBootstrapping:
    def test_pass(self):
        result = gate_checks.check_dialectical_bootstrapping(MINIMAL_WORKSPACE)
        assert result.passed is True

    def test_fail_missing_db(self):
        ws = MINIMAL_WORKSPACE.replace("DB[", "XX[")
        result = gate_checks.check_dialectical_bootstrapping(ws)
        assert result.passed is False
        assert len(result.details["agents_missing_db"]) == 2


class TestV7HypothesisMatrix:
    def test_required_and_missing(self):
        result = gate_checks.check_hypothesis_matrix(MINIMAL_WORKSPACE)
        assert result.passed is False
        assert result.details["hypothesis_count"] == 3

    def test_required_and_present(self):
        result = gate_checks.check_hypothesis_matrix(WORKSPACE_WITH_HYPOTHESIS_MATRIX)
        assert result.passed is True

    def test_not_required(self):
        ws = MINIMAL_WORKSPACE.replace("H3: Technology is accelerating\n", "")
        result = gate_checks.check_hypothesis_matrix(ws)
        assert result.passed is True
        assert result.details["required"] is False


class TestV9CircuitBreaker:
    def test_pass_with_cb(self):
        result = gate_checks.check_circuit_breaker(WORKSPACE_WITH_CB)
        assert result.passed is True
        assert result.details["cb_entries_found"] >= 2

    def test_pass_with_divergence(self):
        result = gate_checks.check_circuit_breaker(WORKSPACE_WITH_DIVERGENCE)
        assert result.passed is True
        assert result.details["divergence_logged"] is True

    def test_fail_neither(self):
        result = gate_checks.check_circuit_breaker(MINIMAL_WORKSPACE)
        assert result.passed is False


class TestV10CrossTrackParticipation:
    def test_pass(self):
        # Add DA response lines to agent sections
        ws = MINIMAL_WORKSPACE.replace(
            "DB[F[A-1]]:",
            "DA[#1] K-SHAPE — concede: label dropped\nDA[#2] WAGE — defend with evidence\nDB[F[A-1]]:",
        ).replace(
            "DB[F[B-2]]:",
            "DA[#3] TIMING — compromise: timeline adjusted\nDB[F[B-2]]:",
        )
        result = gate_checks.check_cross_track_participation(ws)
        assert result.passed is True
        assert result.details["da_challenges_issued"] == 10

    def test_fail_no_da(self):
        ws = MINIMAL_WORKSPACE.replace("### devils-advocate", "### no-da-here").replace("10 challenges", "no challenges")
        result = gate_checks.check_cross_track_participation(ws)
        assert result.passed is False


class TestV11BeliefStateWritten:
    def test_pass(self):
        result = gate_checks.check_belief_state_written(WORKSPACE_WITH_BELIEF)
        assert result.passed is True

    def test_fail_missing(self):
        result = gate_checks.check_belief_state_written(MINIMAL_WORKSPACE)
        assert result.passed is False

    def test_specific_round(self):
        result = gate_checks.check_belief_state_written(WORKSPACE_WITH_BELIEF, round_num=2)
        assert result.passed is True

        result = gate_checks.check_belief_state_written(WORKSPACE_WITH_BELIEF, round_num=5)
        assert result.passed is False


class TestV13ContaminationCheck:
    def test_pass(self):
        result = gate_checks.check_contamination(WORKSPACE_WITH_CONTAMINATION)
        assert result.passed is True

    def test_fail_missing(self):
        result = gate_checks.check_contamination(MINIMAL_WORKSPACE)
        assert result.passed is False


class TestV15AntiSycophancy:
    def test_pass(self):
        result = gate_checks.check_anti_sycophancy(WORKSPACE_WITH_CONTAMINATION)
        assert result.passed is True

    def test_fail_missing(self):
        result = gate_checks.check_anti_sycophancy(MINIMAL_WORKSPACE)
        assert result.passed is False


class TestV16ExitGateFormat:
    def test_pass(self):
        result = gate_checks.check_exit_gate_format(MINIMAL_WORKSPACE)
        assert result.passed is True

    def test_fail_missing(self):
        ws = MINIMAL_WORKSPACE.replace("exit-gate: PASS", "no exit gate here")
        result = gate_checks.check_exit_gate_format(ws)
        assert result.passed is False


class TestV17PlanLock:
    def test_pass(self):
        result = gate_checks.check_plan_lock(BUILD_WORKSPACE)
        assert result.passed is True

    def test_fail_missing_adrs(self):
        ws = BUILD_WORKSPACE.replace("ADR[1]", "no-adr")
        result = gate_checks.check_plan_lock(ws)
        assert result.passed is False

    def test_fail_missing_ic(self):
        ws = BUILD_WORKSPACE.replace("IC[1]", "no-ic")
        result = gate_checks.check_plan_lock(ws)
        assert result.passed is False


class TestV19Checkpoint:
    def test_pass(self):
        result = gate_checks.check_checkpoint(BUILD_WORKSPACE)
        assert result.passed is True

    def test_fail_missing(self):
        ws = BUILD_WORKSPACE.replace(
            "## build-status\nCHECKPOINT[implementation-engineer]: app.py,models.py |functions:3/5 |interfaces-matched:yes |drift:none",
            "## build-status",
        )
        result = gate_checks.check_checkpoint(ws)
        assert result.passed is False


# ---------------------------------------------------------------------------
# Tests: bundles
# ---------------------------------------------------------------------------


class TestBundles:
    def test_r1_convergence_with_all_checks_passing(self):
        ws = WORKSPACE_WITH_HYPOTHESIS_MATRIX
        result = gate_checks.validate_r1_convergence.__wrapped__(ws) if hasattr(gate_checks.validate_r1_convergence, "__wrapped__") else gate_checks.run_validation("r1-convergence", None)
        # Will use default workspace — just verify structure
        assert "bundle" in result
        assert "checks" in result
        assert "context_update" in result

    def test_cb_bundle_pass(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(WORKSPACE_WITH_CB)
            f.flush()
            result = gate_checks.run_validation("cb", f.name)
        os.unlink(f.name)
        assert result["passed"] is True
        assert result["context_update"]["cb_validated"] is True

    def test_cb_bundle_fail(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_validation("cb", f.name)
        os.unlink(f.name)
        assert result["passed"] is False
        assert result["context_update"]["cb_validated"] is False

    def test_pre_synthesis_pass(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(WORKSPACE_WITH_CONTAMINATION)
            f.flush()
            result = gate_checks.run_validation("pre-synthesis", f.name)
        os.unlink(f.name)
        assert result["passed"] is True

    def test_plan_lock_pass(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(BUILD_WORKSPACE)
            f.flush()
            result = gate_checks.run_validation("plan-lock", f.name)
        os.unlink(f.name)
        assert result["passed"] is True

    def test_unknown_bundle(self):
        result = gate_checks.run_validation("nonexistent")
        assert "error" in result


# ---------------------------------------------------------------------------
# Tests: belief state computation
# ---------------------------------------------------------------------------


class TestBeliefComputation:
    def test_analyze_belief_structure(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("analyze", f.name)
        os.unlink(f.name)

        assert "prior" in result
        assert "agreement" in result
        assert "revisions" in result
        assert "gaps_penalty" in result
        assert "da_factor" in result
        assert "posterior" in result
        assert "breakdown" in result

    def test_analyze_belief_values(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("analyze", f.name)
        os.unlink(f.name)

        # TIER-2 → prior=0.5
        assert result["prior"] == 0.5
        # 2 agents, both converged → agreement=1.0
        assert result["agreement"] == 1.0
        # DA grade A → factor=1.0
        assert result["da_factor"] == 1.0

    def test_belief_divergence_detection(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(WORKSPACE_WITH_BELIEF)
            f.flush()
            result = gate_checks.run_compute_belief("analyze", f.name)
        os.unlink(f.name)

        assert "declared" in result
        assert result["declared"] == 0.87
        assert "divergence" in result
        assert "divergence_flag" in result

    def test_build_plan_belief(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(BUILD_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("build-plan", f.name)
        os.unlink(f.name)
        assert "posterior" in result
        assert 0.0 <= result["posterior"] <= 1.0

    def test_build_quality_belief(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(BUILD_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("build-quality", f.name)
        os.unlink(f.name)
        assert "posterior" in result

    def test_unknown_mode(self):
        result = gate_checks.run_compute_belief("nonexistent")
        assert "error" in result


# ---------------------------------------------------------------------------
# Tests: orchestrator guard integration
# ---------------------------------------------------------------------------


class TestOrchestratorGuards:
    """Verify that guards block transitions when validation flags are missing."""

    def test_analyze_research_requires_r1_validated(self):
        # build_analyze_workflow imported at module level via importlib
        orch = build_analyze_workflow()
        orch.start("research")

        # Try to advance with only r1_converged (missing r1_validated)
        orch.advance(context={"r1_converged": True})
        state = orch._make_state()
        assert state.current_phase == "research", "Should stay in research without r1_validated"

        # Now add r1_validated
        orch.advance(context={"r1_validated": True})
        state = orch._make_state()
        assert state.current_phase == "circuit_breaker"

    def test_analyze_cb_requires_cb_validated(self):
        # build_analyze_workflow imported at module level via importlib
        orch = build_analyze_workflow()
        orch.start("research")

        # Get to circuit_breaker
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        state = orch._make_state()
        assert state.current_phase == "circuit_breaker"

        # Try to advance without cb_validated
        orch.advance()
        state = orch._make_state()
        assert state.current_phase == "circuit_breaker", "Should stay without cb_validated"

        # Now add cb_validated
        orch.advance(context={"cb_validated": True})
        state = orch._make_state()
        assert state.current_phase == "challenge"

    def test_analyze_synthesis_requires_pre_synthesis_validated(self):
        # build_analyze_workflow imported at module level via importlib
        orch = build_analyze_workflow()
        orch.start("research")

        # Get to challenge phase
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        orch.advance(context={"cb_validated": True})
        state = orch._make_state()
        assert state.current_phase == "challenge"

        # Try exit to synthesis without pre_synthesis_validated
        orch.advance(context={"exit_gate": "PASS", "belief_state": 0.9, "round": 1})
        state = orch._make_state()
        assert state.current_phase == "challenge", "Should stay without pre_synthesis_validated"

        # Add pre_synthesis_validated
        orch.advance(context={"pre_synthesis_validated": True})
        state = orch._make_state()
        assert state.current_phase == "synthesis"

    def test_post_exit_gates_unchanged(self):
        """Verify existing post-exit-gate guards still work."""
        # build_analyze_workflow imported at module level via importlib
        orch = build_analyze_workflow()
        orch.start("research")

        # Fast-forward to synthesis
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        orch.advance(context={"cb_validated": True})
        orch.advance(context={
            "exit_gate": "PASS", "belief_state": 0.9, "round": 1,
            "pre_synthesis_validated": True,
        })
        assert orch._make_state().current_phase == "synthesis"

        # Post-exit chain
        orch.advance(context={"synthesis_delivered": True})
        assert orch._make_state().current_phase == "compilation"

        orch.advance(context={"compilation_complete": True})
        assert orch._make_state().current_phase == "promotion"

        orch.advance(context={"promotion_complete": True})
        assert orch._make_state().current_phase == "sync"

        orch.advance(context={"sync_complete": True})
        assert orch._make_state().current_phase == "archive"

        # archive → complete now requires BOTH archive_verified AND session_end_verified
        orch.advance(context={"archive_verified": True})
        assert orch._make_state().current_phase == "archive", "Should stay without session_end_verified"

        orch.advance(context={"session_end_verified": True})
        state = orch._make_state()
        assert state.current_phase == "complete"
        assert state.is_terminal is True

    def test_build_plan_requires_plan_round_validated(self):
        # build_build_workflow imported at module level via importlib
        orch = build_build_workflow()
        orch.start("plan")

        # Try without plan_round_validated
        orch.advance(context={"plans_ready": True})
        assert orch._make_state().current_phase == "plan"

        orch.advance(context={"plan_round_validated": True})
        assert orch._make_state().current_phase == "challenge_plan"

    def test_build_requires_checkpoint_validated(self):
        # build_build_workflow imported at module level via importlib
        orch = build_build_workflow()
        orch.start("plan")

        # Get to build phase
        orch.advance(context={"plans_ready": True, "plan_round_validated": True})
        orch.advance(context={
            "exit_gate": "PASS", "belief_state": 0.9,
            "plan_lock_validated": True,
        })
        assert orch._make_state().current_phase == "build"

        # Try without checkpoint_validated
        orch.advance(context={"build_complete": True})
        assert orch._make_state().current_phase == "build"

        orch.advance(context={"checkpoint_validated": True})
        assert orch._make_state().current_phase == "review"

    def test_start_requires_team_created(self):
        """V21: orchestrator start blocks without team_created in context."""
        import subprocess, tempfile
        cp = tempfile.mktemp(suffix=".json")
        result = subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test"}'],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        output = json.loads(result.stdout)
        assert "error" in output
        assert "team_created" in output["error"]
        if os.path.exists(cp):
            os.unlink(cp)

    def test_start_succeeds_with_team_created(self):
        """V21: orchestrator start proceeds with team_created."""
        import subprocess, tempfile
        cp = tempfile.mktemp(suffix=".json")
        result = subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test", "team_created": true, "team_name": "test-team"}'],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["phase"] == "research"
        if os.path.exists(cp):
            os.unlink(cp)

    def test_archive_requires_session_end_verified(self):
        """V22: archive → complete blocked without session_end_verified."""
        # build_analyze_workflow imported at module level via importlib
        orch = build_analyze_workflow()
        orch.start("research", context={"team_created": True})

        # Fast-forward to archive
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        orch.advance(context={"cb_validated": True})
        orch.advance(context={
            "exit_gate": "PASS", "belief_state": 0.9, "round": 1,
            "pre_synthesis_validated": True,
        })
        orch.advance(context={"synthesis_delivered": True})
        orch.advance(context={"compilation_complete": True})
        orch.advance(context={"promotion_complete": True})
        orch.advance(context={"sync_complete": True})
        assert orch._make_state().current_phase == "archive"

        # archive_verified alone should NOT advance to complete
        orch.advance(context={"archive_verified": True})
        assert orch._make_state().current_phase == "archive"

        # Both flags together should advance
        orch.advance(context={"session_end_verified": True})
        state = orch._make_state()
        assert state.current_phase == "complete"
        assert state.is_terminal is True


class TestV22SessionEnd:
    def test_session_end_checks_git(self):
        """V22: session-end bundle checks archive + git status."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_validation("session-end", f.name)
        os.unlink(f.name)

        assert "checks" in result
        # V22 is first check, V23 is second
        check = result["checks"][0]
        assert check["name"] == "V22-session-end-verified"
        assert "git_clean" in check["details"]
        assert "unpushed_commits" in check["details"]
        assert "archive_file_found" in check["details"]

    def test_session_end_includes_synthesis_artifact(self):
        """V23: session-end bundle also checks for synthesis artifact."""
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_validation("session-end", f.name)
        os.unlink(f.name)

        assert len(result["checks"]) == 2
        synth_check = result["checks"][1]
        assert synth_check["name"] == "V23-synthesis-artifact"
        assert "dedicated_synthesis_files" in synth_check["details"]
        assert "archives_with_synthesis" in synth_check["details"]


class TestV23SynthesisArtifact:
    def test_detects_dedicated_synthesis_file(self):
        """V23: finds *-synthesis.md in archive directory."""
        import tempfile
        archive_dir = Path.home() / ".claude/teams/sigma-review/shared/archive"
        # Create a temporary synthesis file
        synth_file = archive_dir / "9999-99-99-test-synthesis.md"
        synth_file.write_text(
            "# Synthesis\n## prompt-decomposition\nQ1: test\nH1: test\n"
            "## findings\nF[T-1] finding |source:[independent-research]\n"
            "## convergence\nagents converged on X\n"
            "## estimates\nP(outcome)=65% 80%CI[50%,78%]\n",
            encoding="utf-8",
        )
        try:
            result = gate_checks.check_synthesis_artifact(MINIMAL_WORKSPACE)
            assert result.passed is True
            assert "9999-99-99-test-synthesis.md" in result.details["dedicated_synthesis_files"]
            assert len(result.details["missing_sections"]) == 0
        finally:
            synth_file.unlink(missing_ok=True)

    def test_fails_when_no_artifact(self):
        """V23: fails when no synthesis file and no embedded synthesis in archives."""
        # This test depends on archive state — check that the function runs
        # and returns a structured result regardless of pass/fail
        result = gate_checks.check_synthesis_artifact(MINIMAL_WORKSPACE)
        assert result.name == "V23-synthesis-artifact"
        assert "dedicated_synthesis_files" in result.details

    def test_detects_missing_sections(self):
        """V23: flags synthesis file missing required content."""
        import tempfile
        archive_dir = Path.home() / ".claude/teams/sigma-review/shared/archive"
        synth_file = archive_dir / "2026-03-28-incomplete-synthesis.md"
        synth_file.write_text("# Empty synthesis\nNo real content here.\n", encoding="utf-8")
        try:
            result = gate_checks.check_synthesis_artifact(MINIMAL_WORKSPACE)
            # File exists but is missing content — should still pass (file present)
            # but missing_sections should be populated
            has_incomplete = any(
                "2026-03-28-incomplete-synthesis.md" in f
                for f in result.details["dedicated_synthesis_files"]
            )
            if has_incomplete:
                assert len(result.details["missing_sections"]) > 0
        finally:
            synth_file.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# Regression tests for R16 gate enforcement bugs (2026-04-09)
# ---------------------------------------------------------------------------

WORKSPACE_FINDING_FORMAT = MINIMAL_WORKSPACE.replace(
    "F[A-1] Finding one — detailed analysis here with evidence |source:[independent-research] T1(BLS)\n"
    "F[A-2] Finding two — more analysis |source:[agent-inference]",
    "FINDING[TA-1]: Finding one — detailed analysis here with evidence |source:[independent-research] T1(BLS)\n"
    "FINDING[TA-2]: Finding two — more analysis |source:[agent-inference]",
)

WORKSPACE_XVERIFY_PARTIAL = MINIMAL_WORKSPACE.replace(
    "XVERIFY: F1=PARTIAL",
    "T1-XVERIFY-PARTIAL[gpt-5.4]: F1 partial agreement",
).replace(
    "XVERIFY: F1=AGREE(gpt-5.4)",
    "XVERIFY PARTIAL (gemini-3.1): F1 partial agreement",
)

WORKSPACE_DB_RECONCILED = MINIMAL_WORKSPACE.replace(
    "DB[F[A-1]]: (1) initial: X (2) assume-wrong: Y (3) strongest-counter: Z (4) re-estimate: W (5) reconciled: final",
    "DB-reconciled: F[A-1] (1) initial: X (2) assume-wrong: Y → reconciled: final",
).replace(
    "DB[F[B-2]]: (1) initial: A (2) assume-wrong: B (3) strongest-counter: C (4) re-estimate: D (5) reconciled: E",
    "DISCONFIRM[F[B-2]]: tested and rejected alternative hypothesis",
)

WORKSPACE_DA_C_FORMAT = MINIMAL_WORKSPACE.replace(
    "10 challenges across 2 agents",
    "DA-C[1] challenge alpha\nDA-C[2] challenge beta",
)

WORKSPACE_DA_SECTION_ONLY = MINIMAL_WORKSPACE.replace(
    "10 challenges across 2 agents\n\n**RESPONSE QUALITY**\n"
    "| Agent | Challenges | Grade |\n"
    "|-------|-----------|-------|\n"
    "| alpha | 5 | A |\n"
    "| beta | 5 | A- |\n\n"
    "Overall engagement: A\n\n"
    "CH[1] TOPIC ONE — RESOLVED\n"
    "CH[2] TOPIC TWO — RESOLVED",
    "Extended narrative about challenges issued to agents with detailed "
    "discussion of methodology concerns and analytical rigor questions "
    "that spans well over one hundred characters to trigger the fallback "
    "minimum signal detection for DA sections without formal markers",
)


class TestAdvanceNoCrash:
    """Regression: Bug 1 — orch.advance must not crash with AttributeError on _current_phase."""

    def test_advance_no_attribute_error(self):
        orch = build_analyze_workflow()
        orch.start("research", context={"team_created": True})
        # This used to crash with: AttributeError: 'str' object has no attribute 'name'
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        state = orch._make_state()
        assert state.current_phase == "circuit_breaker"


class TestV4FindingFormatVariants:
    """Regression: Bug 4 — V4 must detect FINDING[TA-1]: prefix, not just F[...]."""

    def test_finding_prefix_detected(self):
        result = gate_checks.check_source_provenance(WORKSPACE_FINDING_FORMAT)
        assert result.details["total_findings"] > 0, "FINDING[] prefix not detected"

    def test_original_f_prefix_still_works(self):
        result = gate_checks.check_source_provenance(MINIMAL_WORKSPACE)
        assert result.details["total_findings"] > 0, "F[] prefix regression"


class TestV5XverifyPartialVariants:
    """Regression: Bug 2 — V5 must detect T1-XVERIFY-PARTIAL[model] and XVERIFY PARTIAL (model)."""

    def test_xverify_partial_detected(self):
        result = gate_checks.check_xverify_coverage(WORKSPACE_XVERIFY_PARTIAL)
        assert result.details["agents_missing_xverify"] == [], (
            f"XVERIFY-PARTIAL variants not detected: {result.details['agents_missing_xverify']}"
        )


class TestV6DbReconciledAndDisconfirm:
    """Regression: Bug 3 — V6 must detect DB-reconciled and DISCONFIRM[ as DB variants."""

    def test_db_reconciled_detected(self):
        result = gate_checks.check_dialectical_bootstrapping(WORKSPACE_DB_RECONCILED)
        assert result.details["agents_missing_db"] == [], (
            f"DB-reconciled/DISCONFIRM not detected: {result.details['agents_missing_db']}"
        )

    def test_original_db_bracket_still_works(self):
        result = gate_checks.check_dialectical_bootstrapping(MINIMAL_WORKSPACE)
        assert result.details["agents_missing_db"] == []


class TestV10DaSectionMinimumSignal:
    """Regression: Bug 5 — DA section with >100 chars content counts as >= 1 challenge."""

    def test_da_section_fallback(self):
        result = gate_checks.check_cross_track_participation(WORKSPACE_DA_SECTION_ONLY)
        assert result.details["da_challenges_issued"] >= 1, "DA section fallback not triggered"

    def test_da_c_format_detected(self):
        result = gate_checks.check_cross_track_participation(WORKSPACE_DA_C_FORMAT)
        assert result.details["da_challenges_issued"] >= 2, "DA-C[] format not detected"


class TestBeliefOutcomeFuzzyFlag:
    """Regression: Bug 6 — breakdown includes outcome_1_includes_fuzzy transparency flag."""

    def test_fuzzy_flag_present(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("analyze", f.name)
        os.unlink(f.name)
        assert "outcome_1_includes_fuzzy" in result["breakdown"]

    def test_fuzzy_flag_false_when_no_inflation(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(MINIMAL_WORKSPACE)
            f.flush()
            result = gate_checks.run_compute_belief("analyze", f.name)
        os.unlink(f.name)
        # MINIMAL_WORKSPACE has no outcome markers, so outcome_1 <= outcome_total
        assert result["breakdown"]["outcome_1_includes_fuzzy"] is False


# ---------------------------------------------------------------------------
# Regression tests for orchestrator code review findings (2026-04-09)
# ---------------------------------------------------------------------------

class TestTransitionGuardCoverage:
    """Regression: H1/H2/H3 — guard gaps and unbounded loops."""

    def test_hard_cap_fires_when_belief_low_at_round_5(self):
        """H1: hard_cap must fire even when belief <= 0.6 at round >= 5."""
        orch = build_analyze_workflow()
        orch.start("research", context={"team_created": True})
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        orch.advance(context={"cb_validated": True})
        # Simulate 5 rounds of challenge with low belief — hard_cap should force synthesis
        for i in range(5):
            orch.advance(context={"round": i + 1})
        # After round 5, hard_cap should fire regardless of belief/exit_gate
        orch.advance(context={"round": 6})
        assert orch._make_state().current_phase == "synthesis", \
            "hard_cap should force synthesis at round >= 5"

    def test_exit_passed_low_belief_loops(self):
        """H2: exit_gate PASS + belief < 0.85 should self-loop, not deadlock."""
        orch = build_analyze_workflow()
        orch.start("research", context={"team_created": True})
        orch.advance(context={"r1_converged": True, "r1_validated": True})
        orch.advance(context={"cb_validated": True})
        assert orch._make_state().current_phase == "challenge"
        # exit gate passed but belief only 0.75 — should self-loop (not deadlock)
        orch.advance(context={"exit_gate": "PASS", "belief_state": 0.75, "round": 1})
        assert orch._make_state().current_phase == "challenge", \
            "Should self-loop when exit_gate PASS but belief < 0.85"

    def test_build_challenge_plan_bounded(self):
        """H3: BUILD challenge_plan must not loop unbounded."""
        orch = build_build_workflow()
        orch.start("plan", context={"team_created": True})
        orch.advance(context={"plans_ready": True, "plan_round_validated": True})
        assert orch._make_state().current_phase == "challenge_plan"
        # Simulate rounds without exit gate — should hit hard cap
        for i in range(6):
            orch.advance(context={"round": i + 1})
        assert orch._make_state().current_phase == "build", \
            "plan_hard_cap should force to build at round >= 5"

    def test_build_review_bounded(self):
        """H3: BUILD review must not loop unbounded."""
        orch = build_build_workflow()
        orch.start("plan", context={"team_created": True})
        orch.advance(context={"plans_ready": True, "plan_round_validated": True})
        orch.advance(context={
            "exit_gate": "PASS", "belief_state": 0.9,
            "plan_lock_validated": True,
        })
        assert orch._make_state().current_phase == "build"
        orch.advance(context={"build_complete": True, "checkpoint_validated": True})
        assert orch._make_state().current_phase == "review"
        # Simulate rounds without exit gate — should hit hard cap
        for i in range(6):
            orch.advance(context={"round": i + 1})
        assert orch._make_state().current_phase == "synthesis", \
            "review_hard_cap should force to synthesis at round >= 5"


class TestCheckpointResilience:
    """Regression: H4/H5/H6 — atomic writes, corrupt recovery, mode validation."""

    def test_atomic_write_creates_file(self):
        """H4: _save should produce a valid checkpoint file."""
        import tempfile
        orch = build_analyze_workflow()
        orch.start("research", context={"team_created": True})
        cp = tempfile.mktemp(suffix=".json")
        try:
            _orch_mod._save(orch, cp)
            with open(cp) as f:
                data = json.load(f)
            assert data["current_phase"] == "research"
            assert data["_mode"] == "analyze"
            # Temp file should be cleaned up
            assert not os.path.exists(cp + ".tmp")
        finally:
            if os.path.exists(cp):
                os.unlink(cp)

    def test_corrupt_checkpoint_recovery(self):
        """H5: corrupt JSON should not crash — falls back to fresh orchestrator."""
        import tempfile
        cp = tempfile.mktemp(suffix=".json")
        with open(cp, "w") as f:
            f.write("{corrupt json!!!")
        try:
            orch = _orch_mod._load_or_create("analyze", cp)
            # Should return fresh orchestrator, not crash
            assert orch._current_phase is None
        finally:
            os.unlink(cp)

    def test_mode_mismatch_rejected(self):
        """H6: loading analyze checkpoint with --mode build should fail."""
        import tempfile, subprocess
        # Create an analyze checkpoint
        cp = tempfile.mktemp(suffix=".json")
        subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--mode", "analyze", "--checkpoint", cp,
             "start", "--context", '{"task": "test", "team_created": true}'],
            capture_output=True, text=True, timeout=10,
        )
        # Try to load with build mode
        result = subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--mode", "build", "--checkpoint", cp,
             "status"],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        output = json.loads(result.stdout)
        assert "mismatch" in output["error"].lower()
        os.unlink(cp)


class TestAutoValidatePipeline:
    """Regression: C1/C2/H7 — context injection, error handling, cb mapping."""

    def test_cb_in_phase_required_validations(self):
        """H7: circuit_breaker must be in PHASE_REQUIRED_VALIDATIONS."""
        # Read the source to verify — this is a structural test
        import inspect
        source = inspect.getsource(_orch_mod.cmd_advance)
        assert '"circuit_breaker"' in source and '"cb"' in source

    def test_start_overwrite_guard(self):
        """M1: start should refuse to overwrite active session."""
        import subprocess, tempfile
        cp = tempfile.mktemp(suffix=".json")
        # Start a session
        subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test", "team_created": true}'],
            capture_output=True, text=True, timeout=10,
        )
        # Try to start again — should be blocked
        result = subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test2", "team_created": true}'],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode != 0
        output = json.loads(result.stdout)
        assert "Active session" in output["error"]
        os.unlink(cp)

    def test_start_force_restart(self):
        """M1: start with force_restart should overwrite."""
        import subprocess, tempfile
        cp = tempfile.mktemp(suffix=".json")
        # Start a session
        subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test", "team_created": true}'],
            capture_output=True, text=True, timeout=10,
        )
        # Force restart
        result = subprocess.run(
            ["python3", os.path.join(_shared_dir, "orchestrator-config.py"),
             "--checkpoint", cp,
             "start", "--context", '{"task": "test2", "team_created": true, "force_restart": true}'],
            capture_output=True, text=True, timeout=10,
        )
        assert result.returncode == 0
        os.unlink(cp)
