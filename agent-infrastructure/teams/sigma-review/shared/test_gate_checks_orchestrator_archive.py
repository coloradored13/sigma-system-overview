"""ARCHIVED: Orchestrator-dependent tests from test_gate_checks.py

These tests were written for orchestrator-config.py which was deleted in the
atomic checklist migration (2026-04-15). They test phase transition guards,
checkpoint persistence, and workflow advancement — none of which exist in the
checklist model.

Preserved as a historical record. To run, restore orchestrator-config.py
to the shared/ directory.

Original test classes:
- TestOrchestratorGuards (9 tests): phase transition guard integration
- TestAdvanceNoCrash (1 test): regression for AttributeError bug
- TestTransitionGuardCoverage (4 tests): hard cap, loop bounds, deadlocks
- TestCheckpointResilience (3 tests): atomic writes, corrupt recovery, mode mismatch
- TestAutoValidatePipeline (3 tests): context injection, overwrite guard, force restart

Total: 20 tests
"""

# These tests require orchestrator-config.py to be present in the shared/ directory.
# They are not runnable without it and are preserved for reference only.
#
# To make them runnable again:
# 1. Restore orchestrator-config.py to this directory
# 2. Uncomment the import block below
# 3. Run: pytest test_gate_checks_orchestrator_archive.py

# import json
# import os
# import sys
# from pathlib import Path
# import pytest
#
# _shared_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, _shared_dir)
#
# import gate_checks
# import importlib.util
#
# _orch_spec = importlib.util.spec_from_file_location(
#     "orchestrator_config",
#     os.path.join(_shared_dir, "orchestrator-config.py"),
# )
# _orch_mod = importlib.util.module_from_spec(_orch_spec)
# _orch_spec.loader.exec_module(_orch_mod)
# build_analyze_workflow = _orch_mod.build_analyze_workflow
# build_build_workflow = _orch_mod.build_build_workflow
#
#
# class TestOrchestratorGuards:
#     """Verify that guards block transitions when validation flags are missing."""
#     ... (9 tests — see git history for full source)
#
# class TestAdvanceNoCrash:
#     """Regression: Bug 1 — orch.advance must not crash with AttributeError."""
#     ... (1 test)
#
# class TestTransitionGuardCoverage:
#     """Regression: H1/H2/H3 — guard gaps and unbounded loops."""
#     ... (4 tests)
#
# class TestCheckpointResilience:
#     """Regression: H4/H5/H6 — atomic writes, corrupt recovery, mode validation."""
#     ... (3 tests)
#
# class TestAutoValidatePipeline:
#     """Regression: C1/C2/H7 — context injection, error handling, cb mapping."""
#     ... (3 tests)
