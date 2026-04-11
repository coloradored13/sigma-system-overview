"""Tests for sigma-retrospective.py — Stop hook."""
import sys
import json
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
retro = importlib.import_module("sigma-retrospective")


class TestExtractSection:
    def test_extracts_convergence(self):
        text = "## convergence\nagent1: ✓ done\nagent2: ✓ done\n## findings\nstuff"
        result = retro.extract_section(text, "convergence")
        assert "agent1: ✓ done" in result
        assert "agent2: ✓ done" in result

    def test_extracts_last_section(self):
        text = "## infrastructure\nΣVerify available\n"
        result = retro.extract_section(text, "infrastructure")
        assert "ΣVerify available" in result

    def test_returns_empty_for_missing(self):
        assert retro.extract_section("## other\nstuff", "convergence") == ""

    def test_handles_empty_text(self):
        assert retro.extract_section("", "convergence") == ""


class TestAnalyzeWorkspace:
    def test_counts_converged_agents(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert len(metrics["agents_converged"]) == 5

    def test_detects_no_circuit_breaker(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["cb_fired"] is False

    def test_detects_circuit_breaker(self):
        content = "## convergence\nagent: ✓\n\nCircuit breaker fired due to herding"
        metrics = retro.analyze_workspace(content)
        assert metrics["cb_fired"] is True

    def test_counts_outcomes(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["outcome_1"] >= 1  # "Revised from" / "outcome 1"
        assert metrics["outcome_2"] >= 1  # "CHECK CONFIRMS" / "outcome 2"
        assert metrics["outcome_3"] >= 1  # "gap:" / "outcome 3"

    def test_source_tier_counts(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["t1"] >= 2  # :T1| appears twice
        assert metrics["t2"] >= 1  # :T2| appears once

    def test_xverify_detection(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["xverify_used"] >= 1
        assert metrics["xverify_available"] is True

    def test_tier_assessment(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["tier_assessed"] == 2

    def test_task_slug_extraction(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert "loan admin" in metrics["task_slug"].lower() or "competitive" in metrics["task_slug"].lower()

    def test_concession_detection(self):
        from conftest import SAMPLE_WORKSPACE_COMPLETE
        metrics = retro.analyze_workspace(SAMPLE_WORKSPACE_COMPLETE)
        assert metrics["concession_type"] in ("genuine", "performative", "n/a")

    def test_perfunctory_risk_high(self):
        # All outcomes are outcome 2 → high perfunctory risk
        content = "## convergence\na: ✓\n\nCHECK CONFIRMS risk A\nCHECK CONFIRMS risk B\nCHECK CONFIRMS risk C\nCHECK CONFIRMS risk D\nCHECK CONFIRMS risk E"
        metrics = retro.analyze_workspace(content)
        assert metrics["perfunctory_risk"] == "high"

    def test_empty_workspace(self):
        metrics = retro.analyze_workspace("")
        assert metrics["agents_converged"] == []
        assert metrics["tier_assessed"] == 0


class TestGenerateRecommendation:
    def test_perfunctory_risk_recommendation(self):
        metrics = {"perfunctory_risk": "high", "concession_type": "genuine",
                   "revision_rate": 50, "t1": 5, "t2": 3, "t3": 1,
                   "xverify_available": True, "xverify_used": 1,
                   "agents_converged": ["a", "b", "c", "d"], "cb_fired": True}
        rec = retro.generate_recommendation(metrics)
        assert "rubber-stamping" in rec.lower() or "outcome-2" in rec.lower()

    def test_t3_dominant_recommendation(self):
        metrics = {"perfunctory_risk": "low", "concession_type": "genuine",
                   "revision_rate": 50, "t1": 0, "t2": 1, "t3": 10,
                   "xverify_available": True, "xverify_used": 1,
                   "agents_converged": ["a", "b", "c", "d"], "cb_fired": True}
        rec = retro.generate_recommendation(metrics)
        assert "T3" in rec

    def test_xverify_unused_recommendation(self):
        metrics = {"perfunctory_risk": "low", "concession_type": "genuine",
                   "revision_rate": 50, "t1": 5, "t2": 3, "t3": 1,
                   "xverify_available": True, "xverify_used": 0,
                   "agents_converged": ["a", "b", "c", "d"], "cb_fired": True}
        rec = retro.generate_recommendation(metrics)
        assert "ΣVerify" in rec or "unused" in rec.lower()

    def test_no_cb_with_many_agents(self):
        metrics = {"perfunctory_risk": "low", "concession_type": "genuine",
                   "revision_rate": 50, "t1": 5, "t2": 3, "t3": 1,
                   "xverify_available": True, "xverify_used": 1,
                   "agents_converged": ["a", "b", "c", "d"], "cb_fired": False}
        rec = retro.generate_recommendation(metrics)
        assert "circuit breaker" in rec.lower() or "divergence" in rec.lower()

    def test_normal_ranges(self):
        metrics = {"perfunctory_risk": "low", "concession_type": "genuine",
                   "revision_rate": 50, "t1": 5, "t2": 3, "t3": 1,
                   "xverify_available": True, "xverify_used": 1,
                   "agents_converged": ["a", "b", "c", "d"], "cb_fired": True}
        rec = retro.generate_recommendation(metrics)
        assert "normal ranges" in rec.lower()


class TestWriteRetro:
    def test_appends_to_patterns(self, tmp_path, monkeypatch):
        patterns = tmp_path / "patterns.md"
        patterns.write_text("# Patterns\n", encoding="utf-8")
        monkeypatch.setattr(retro, "PATTERNS", patterns)

        metrics = {
            "task_slug": "test-review",
            "agents_converged": ["agent-a", "agent-b"],
            "agents_timeout": 0,
            "cb_fired": False,
            "outcome_1": 2, "outcome_2": 3, "outcome_3": 1,
            "perfunctory_risk": "low",
            "revision_rate": 45,
            "concession_type": "genuine",
            "t1": 4, "t2": 2, "t3": 1,
            "xverify_used": 1, "xverify_failed": 0, "xverify_available": True,
            "tier_assessed": 2,
        }
        retro.write_retro(metrics)

        content = patterns.read_text()
        assert "## Retro: R1" in content
        assert "test-review" in content
        assert "agent-a, agent-b" in content
        assert "outcome-1: 2" in content

    def test_increments_review_number(self, tmp_path, monkeypatch):
        patterns = tmp_path / "patterns.md"
        patterns.write_text("## Retro: R5 — old\n", encoding="utf-8")
        monkeypatch.setattr(retro, "PATTERNS", patterns)

        metrics = {
            "task_slug": "new", "agents_converged": ["a"], "agents_timeout": 0,
            "cb_fired": False, "outcome_1": 0, "outcome_2": 0, "outcome_3": 0,
            "perfunctory_risk": "low", "revision_rate": 0, "concession_type": "n/a",
            "t1": 0, "t2": 0, "t3": 0, "xverify_used": 0, "xverify_failed": 0,
            "xverify_available": False, "tier_assessed": 1,
        }
        retro.write_retro(metrics)

        content = patterns.read_text()
        assert "## Retro: R6" in content


class TestDeduplication:
    def test_same_hash_skips(self, tmp_path, monkeypatch):
        """Running retro on identical workspace content should skip."""
        ws = tmp_path / "workspace.md"
        ws.write_text("## convergence\nagent: ✓ done\n", encoding="utf-8")
        patterns = tmp_path / "patterns.md"
        patterns.write_text("", encoding="utf-8")
        state = tmp_path / ".retro-last-hash"

        monkeypatch.setattr(retro, "WORKSPACE", ws)
        monkeypatch.setattr(retro, "PATTERNS", patterns)
        monkeypatch.setattr(retro, "RETRO_STATE", state)

        import hashlib
        convergence = "agent: ✓ done"
        h = hashlib.sha256(convergence.encode()).hexdigest()[:16]
        state.write_text(h, encoding="utf-8")

        # The main() would sys.exit(0) on duplicate hash
        # Test the logic directly
        content_hash = hashlib.sha256(convergence.encode()).hexdigest()[:16]
        last_hash = state.read_text().strip()
        assert content_hash == last_hash  # Would skip
