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


def cmd_watch(args):
    """C3: Watch workspace ## convergence for agent ✓ declarations and auto-advance.
    Polls workspace file every N seconds, detects convergence signals,
    and auto-advances the orchestrator when all required agents have converged.
    """
    import re
    import time

    orch = build_optimize_workflow()
    _load(orch)
    workspace_path = Path(args.workspace)
    interval = int(args.interval)

    # Map phases to their required convergence agents
    PHASE_AGENTS = {
        "parallel_search": {"search-conservative", "search-aggressive"},
        "combinatorial": {"search-combinatorial"},
        "validation": {"statistical-analyst"},
        "cross_model": {"cross-model-validator"},
    }

    # Map phases to their advance context keys
    PHASE_CONTEXT = {
        "parallel_search": {"search_conservative_converged": True, "search_aggressive_converged": True},
        "combinatorial": {"combinatorial_converged": True},
        "cross_model": {"cross_model_converged": True},
    }

    print(f"Watching {workspace_path} every {interval}s for convergence signals...", flush=True)
    print(f"Current phase: {orch._current_phase}", flush=True)

    while True:
        if not workspace_path.exists():
            time.sleep(interval)
            continue

        content = workspace_path.read_text()

        # Extract convergence section
        conv_match = re.search(r"## convergence\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        if not conv_match:
            time.sleep(interval)
            continue

        conv_section = conv_match.group(1)
        current_phase = orch._current_phase

        # Check if current phase has auto-advance requirements
        required = PHASE_AGENTS.get(current_phase, set())
        if not required:
            time.sleep(interval)
            continue

        # Check for ✓ declarations from required agents
        converged = set()
        for agent in required:
            # Match patterns like "search-conservative: ✓" or "search-conservative ✓"
            if re.search(rf"{re.escape(agent)}\s*:?\s*✓", conv_section):
                converged.add(agent)

        if converged == required:
            print(f"\nAll agents converged for {current_phase}: {converged}", flush=True)
            ctx = PHASE_CONTEXT.get(current_phase, {})
            if ctx:
                state = orch.advance(context=ctx)
                _save(orch)
                print(f"Auto-advanced to: {orch._current_phase}", flush=True)
                _output(state, orch)

                # Check if terminal
                if hasattr(orch, '_current_phase') and orch._current_phase == "complete":
                    print("Experiment complete. Exiting watch.", flush=True)
                    break
            else:
                print(f"No auto-context for phase {current_phase} — manual advance required.", flush=True)

        time.sleep(interval)


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

    p_watch = sub.add_parser("watch", help="Watch workspace for convergence and auto-advance (C3)")
    p_watch.add_argument("--workspace", default=str(Path(__file__).parent / "workspace.md"),
                         help="Path to workspace.md")
    p_watch.add_argument("--interval", default="10", help="Poll interval in seconds (default: 10)")

    args = parser.parse_args()

    commands = {
        "start": cmd_start,
        "advance": cmd_advance,
        "status": cmd_status,
        "checkpoint": cmd_checkpoint,
        "restore": cmd_restore,
        "watch": cmd_watch,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
