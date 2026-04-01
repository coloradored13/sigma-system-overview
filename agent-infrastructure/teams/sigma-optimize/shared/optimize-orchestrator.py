#!/usr/bin/env python3
"""sigma-optimize orchestrator — state machine for experimental phases.

Phases:
  parallel_search → combinatorial → validation ⟲ → cross_model → synthesis → promotion → archive → complete

Usage:
  python3 optimize-orchestrator.py start --context '{"task": "...", "team_created": true}'
  python3 optimize-orchestrator.py advance --context '{"search_complete": true}'
  python3 optimize-orchestrator.py status
  python3 optimize-orchestrator.py checkpoint --file /tmp/optimize-orch.json
  python3 optimize-orchestrator.py restore --file /tmp/optimize-orch.json
"""

import argparse
import json
import sys
from pathlib import Path

from hateoas_agent import Orchestrator, AgentSlot
from hateoas_agent.conditions import (
    context_true,
    exit_gate_passed,
    round_limit,
)
from hateoas_agent.orchestrator_persistence import (
    load_orchestrator_checkpoint,
    save_orchestrator_checkpoint,
)

CHECKPOINT_PATH = Path.home() / ".sigma-optimize-checkpoint.json"


def build_optimize_workflow() -> Orchestrator:
    """Build the sigma-optimize state machine."""

    agents = [
        AgentSlot(name="search-conservative", role="Constrained evolutionary search"),
        AgentSlot(name="search-aggressive", role="Full-vocabulary evolutionary search"),
        AgentSlot(name="search-combinatorial", role="Combinatorial token testing", join_phase="combinatorial"),
        AgentSlot(name="statistical-analyst", role="Statistical validation + exit gate", join_phase="validation"),
        AgentSlot(name="cross-model-validator", role="Cross-model transfer testing", join_phase="cross_model"),
    ]

    orch = Orchestrator(
        name="sigma-optimize",
        agents=agents,
        gateway_name="start_optimize",
    )

    # --- Phases ---
    orch.phase("parallel_search", description="Phase 1: independent evolutionary search (conservative + aggressive)", parallel=True)
    orch.phase("combinatorial", description="Phase 2: systematic combination testing from search winners")
    orch.phase("validation", description="Phase 3: statistical validation + exit gate (SA controls)")
    orch.phase("cross_model", description="Phase 4: cross-model transfer testing via sigma-verify")
    orch.phase("synthesis", description="Phase 5: findings synthesis (separate agent, not lead)")
    orch.phase("promotion", description="Phase 6: promote validated findings to global memory")
    orch.phase("archive", description="Phase 7: archive workspace")
    orch.phase("complete", description="Experiment complete", terminal=True)

    # --- Transitions ---

    # Phase 1 → Phase 2: both search agents must have converged
    orch.transition(
        "parallel_search", "combinatorial",
        name="search_to_combinatorial",
        guard=context_true("search_conservative_converged") & context_true("search_aggressive_converged"),
    )

    # Phase 2 → Phase 3: combinatorial agent converged
    orch.transition(
        "combinatorial", "validation",
        name="combinatorial_to_validation",
        guard=context_true("combinatorial_converged"),
    )

    # Phase 3 → Phase 3 (loop back): exit gate FAIL + under round limit
    # SA can request more data; lead re-runs search agents with more generations
    orch.transition(
        "validation", "validation",
        name="validation_retry",
        guard=~exit_gate_passed() & round_limit(3),
    )

    # Phase 3 → Phase 4: exit gate PASS
    orch.transition(
        "validation", "cross_model",
        name="validation_to_cross_model",
        guard=exit_gate_passed(),
    )

    # Phase 3 → synthesis (skip cross-model): exit gate FAIL after max retries
    # Reports null result — this is a valid finding
    orch.transition(
        "validation", "synthesis",
        name="validation_exhausted",
        guard=~exit_gate_passed() & ~round_limit(3),
    )

    # Phase 4 → Phase 5: cross-model validator converged
    orch.transition(
        "cross_model", "synthesis",
        name="cross_model_to_synthesis",
        guard=context_true("cross_model_converged"),
    )

    # Phase 5 → Phase 6: synthesis written
    orch.transition(
        "synthesis", "promotion",
        name="synthesis_to_promotion",
        guard=context_true("synthesis_delivered"),
    )

    # Phase 6 → Phase 7: promotion complete
    orch.transition(
        "promotion", "archive",
        name="promotion_to_archive",
        guard=context_true("promotion_complete"),
    )

    # Phase 7 → complete: archive written
    orch.transition(
        "archive", "complete",
        name="archive_to_complete",
        guard=context_true("archive_written"),
    )

    return orch


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_start(args):
    orch = build_optimize_workflow()
    ctx = json.loads(args.context) if args.context else {}
    state = orch.start("parallel_search", context=ctx)
    _save(orch)
    _output(state, orch)


def cmd_advance(args):
    orch = build_optimize_workflow()
    _load(orch)
    ctx = json.loads(args.context) if args.context else {}
    state = orch.advance(context=ctx)
    _save(orch)
    _output(state, orch)


def cmd_status(args):
    orch = build_optimize_workflow()
    _load(orch)
    state = {
        "phase": orch._current_phase,
        "context": orch._context,
        "agents": {str(a): "registered" for a in orch._agents} if orch._agents else {},
    }
    print(json.dumps(state, indent=2, default=str))


def cmd_checkpoint(args):
    orch = build_optimize_workflow()
    _load(orch)
    data = save_orchestrator_checkpoint(orch)
    path = Path(args.file) if args.file else CHECKPOINT_PATH
    path.write_text(json.dumps(data, indent=2, default=str))
    print(json.dumps({"checkpoint": str(path), "phase": orch._current_phase}))


def cmd_restore(args):
    orch = build_optimize_workflow()
    path = Path(args.file) if args.file else CHECKPOINT_PATH
    data = json.loads(path.read_text())
    load_orchestrator_checkpoint(orch, data)
    _save(orch)
    print(json.dumps({"restored": str(path), "phase": orch._current_phase}))


def _save(orch: Orchestrator):
    data = save_orchestrator_checkpoint(orch)
    CHECKPOINT_PATH.write_text(json.dumps(data, indent=2, default=str))


def _load(orch: Orchestrator):
    if CHECKPOINT_PATH.exists():
        data = json.loads(CHECKPOINT_PATH.read_text())
        load_orchestrator_checkpoint(orch, data)
    else:
        print("No checkpoint found. Run 'start' first.", file=sys.stderr)
        sys.exit(1)


def _output(state, orch: Orchestrator):
    out = {
        "phase": orch._current_phase,
        "context": orch._context,
    }
    print(json.dumps(out, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="sigma-optimize orchestrator")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start")
    p_start.add_argument("--context", default="{}")

    p_advance = sub.add_parser("advance")
    p_advance.add_argument("--context", default="{}")

    sub.add_parser("status")

    p_cp = sub.add_parser("checkpoint")
    p_cp.add_argument("--file", default=None)

    p_rs = sub.add_parser("restore")
    p_rs.add_argument("--file", default=None)

    args = parser.parse_args()

    commands = {
        "start": cmd_start,
        "advance": cmd_advance,
        "status": cmd_status,
        "checkpoint": cmd_checkpoint,
        "restore": cmd_restore,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
