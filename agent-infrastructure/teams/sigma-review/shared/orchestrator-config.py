#!/usr/bin/env python3
"""Sigma-review workflow definition using hateoas-agent Orchestrator.

Defines the ANALYZE and BUILD review workflows as formal state machines.
The lead agent calls this script via Bash to:
  - Start a workflow
  - Advance to the next phase (guards evaluated automatically)
  - Check current status
  - Save/restore checkpoints for session persistence

Usage (from lead agent via Bash):
  python3 orchestrator-config.py start --mode analyze --context '{"task": "...", "tier": 2}'
  python3 orchestrator-config.py advance --context '{"converged": true, "belief_state": 0.75}'
  python3 orchestrator-config.py status
  python3 orchestrator-config.py checkpoint --file /tmp/review-checkpoint.json
  python3 orchestrator-config.py restore --file /tmp/review-checkpoint.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile

# Allow importing gate_checks from same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hateoas_agent import AgentSlot, Orchestrator
from hateoas_agent.conditions import (
    all_converged,
    belief_above,
    context_true,
    exit_gate_passed,
    round_limit,
)
from hateoas_agent.orchestrator_persistence import (
    load_orchestrator_checkpoint,
    save_orchestrator_checkpoint,
)

import gate_checks

# Default checkpoint location
DEFAULT_CHECKPOINT = os.path.join(
    tempfile.gettempdir(), "sigma-review-orchestrator.json"
)


# ------------------------------------------------------------------
# Workflow definitions
# ------------------------------------------------------------------


def build_analyze_workflow(agents: list[AgentSlot] | None = None) -> Orchestrator:
    """Build the ANALYZE mode workflow.

    Phases:
      research → circuit_breaker → challenge ⟲ → synthesis
                                  ↘ debate ↗

    Maps sigma-review concepts:
      R1 = research (parallel, all agents except DA)
      CB = circuit_breaker (sequential, zero-dissent check)
      R2+ = challenge (parallel, DA joins, self-loop on FAIL)
      Toulmin = debate (sequential, deep disagreement)
      Final = synthesis (terminal)
    """
    orch = Orchestrator(
        name="sigma-review-analyze",
        agents=agents or _default_analyze_agents(),
        gateway_name="start_review",
    )

    # Phases
    orch.phase("research", description="R1: independent domain analysis", parallel=True)
    orch.phase("circuit_breaker", description="Zero-dissent check after R1")
    orch.phase(
        "challenge",
        description="R2+: DA challenges + agent integration",
        parallel=True,
    )
    orch.phase("debate", description="Toulmin structured debate for deep disagreement")
    orch.phase("synthesis", description="Final synthesis and report")

    # Post-exit-gate phases (mandatory — mechanical enforcement)
    orch.phase("promotion", description="Memory promotion: agents classify and submit generalizable learnings")
    orch.phase("sync", description="Infrastructure sync: detect drift and sync installed files to repo")
    orch.phase("archive", description="Workspace archive: copy workspace to shared/archive/")
    orch.phase("complete", description="Review complete", terminal=True)

    # Transitions
    orch.transition(
        "research",
        "circuit_breaker",
        name="r1_complete",
        guard=context_true("r1_converged") & context_true("r1_validated"),
    )

    orch.transition(
        "circuit_breaker",
        "challenge",
        name="cb_complete",
        guard=context_true("cb_validated"),
    )

    orch.transition(
        "challenge",
        "synthesis",
        name="exit_to_synthesis",
        guard=exit_gate_passed() & belief_above(0.85) & context_true("pre_synthesis_validated"),
    )

    orch.transition(
        "challenge",
        "debate",
        name="deep_disagreement",
        guard=~exit_gate_passed() & ~belief_above(0.6),
    )

    orch.transition(
        "challenge",
        "challenge",
        name="another_round",
        guard=~exit_gate_passed() & belief_above(0.6) & round_limit(5, key="round"),
    )

    orch.transition(
        "debate",
        "challenge",
        name="debate_resolved",
    )  # unguarded — debate feeds back to challenge

    # Hard cap: if stuck in challenge at round 5, force synthesis
    orch.transition(
        "challenge",
        "synthesis",
        name="hard_cap",
        guard=~round_limit(5, key="round"),  # round >= 5
    )

    # Post-exit-gate transitions (guarded — lead must set completion flags)
    orch.transition(
        "synthesis",
        "promotion",
        name="synthesis_delivered",
        guard=context_true("synthesis_delivered"),
    )

    orch.transition(
        "promotion",
        "sync",
        name="promotion_complete",
        guard=context_true("promotion_complete"),
    )

    orch.transition(
        "sync",
        "archive",
        name="sync_complete",
        guard=context_true("sync_complete"),
    )

    orch.transition(
        "archive",
        "complete",
        name="archive_verified",
        guard=context_true("archive_verified"),
    )

    return orch


def build_build_workflow(agents: list[AgentSlot] | None = None) -> Orchestrator:
    """Build the BUILD mode workflow.

    Phases:
      plan → challenge_plan → build → review → synthesis
    """
    orch = Orchestrator(
        name="sigma-review-build",
        agents=agents or _default_build_agents(),
        gateway_name="start_build",
    )

    orch.phase("plan", description="R1: agents write implementation plans", parallel=True)
    orch.phase(
        "challenge_plan",
        description="R2: DA challenges plans before code",
        parallel=True,
    )
    orch.phase("build", description="R3: parallel build with checkpoint", parallel=True)
    orch.phase("review", description="R4: adversarial review of completed build", parallel=True)
    orch.phase("synthesis", description="Final review report")

    # Post-exit-gate phases (mandatory — mechanical enforcement)
    orch.phase("promotion", description="Memory promotion: agents classify and submit generalizable learnings")
    orch.phase("sync", description="Infrastructure sync: detect drift and sync installed files to repo")
    orch.phase("archive", description="Workspace archive: copy workspace to shared/archive/")
    orch.phase("complete", description="Build complete", terminal=True)

    orch.transition(
        "plan",
        "challenge_plan",
        name="plans_ready",
        guard=context_true("plans_ready") & context_true("plan_round_validated"),
    )
    orch.transition(
        "challenge_plan",
        "build",
        name="plans_approved",
        guard=exit_gate_passed() & belief_above(0.85) & context_true("plan_lock_validated"),
    )
    orch.transition(
        "challenge_plan",
        "challenge_plan",
        name="revise_plans",
        guard=~exit_gate_passed(),
    )
    orch.transition(
        "build",
        "review",
        name="build_complete",
        guard=context_true("build_complete") & context_true("checkpoint_validated"),
    )
    orch.transition(
        "review",
        "synthesis",
        name="review_done",
        guard=exit_gate_passed() & context_true("pre_synthesis_validated"),
    )
    orch.transition("review", "review", name="review_revisions", guard=~exit_gate_passed())

    # Post-exit-gate transitions (guarded — lead must set completion flags)
    orch.transition(
        "synthesis",
        "promotion",
        name="synthesis_delivered",
        guard=context_true("synthesis_delivered"),
    )

    orch.transition(
        "promotion",
        "sync",
        name="promotion_complete",
        guard=context_true("promotion_complete"),
    )

    orch.transition(
        "sync",
        "archive",
        name="sync_complete",
        guard=context_true("sync_complete"),
    )

    orch.transition(
        "archive",
        "complete",
        name="archive_verified",
        guard=context_true("archive_verified"),
    )

    return orch


def _default_analyze_agents() -> list[AgentSlot]:
    """Default agent roster for ANALYZE — overridden by lead's tier selection."""
    return [
        AgentSlot("tech-architect", role="Architecture analysis"),
        AgentSlot("product-strategist", role="Market viability"),
        AgentSlot("reference-class-analyst", role="Base rates and calibration"),
        AgentSlot("devils-advocate", role="Adversarial challenge", join_phase="challenge"),
    ]


def _default_build_agents() -> list[AgentSlot]:
    """Default agent roster for BUILD."""
    return [
        AgentSlot("tech-architect", role="Architecture and implementation"),
        AgentSlot("code-quality-analyst", role="Code quality and testing"),
        AgentSlot("reference-class-analyst", role="Effort estimation and calibration"),
        AgentSlot("devils-advocate", role="Plan challenge and review", join_phase="challenge_plan"),
    ]


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------


def _load_or_create(mode: str, checkpoint_file: str) -> Orchestrator:
    """Load orchestrator from checkpoint, or create fresh."""
    builder = build_analyze_workflow if mode == "analyze" else build_build_workflow
    orch = builder()

    if os.path.exists(checkpoint_file):
        with open(checkpoint_file) as f:
            data = json.load(f)
        load_orchestrator_checkpoint(orch, data)

    return orch


def _save(orch: Orchestrator, checkpoint_file: str) -> None:
    """Save orchestrator state to checkpoint file."""
    data = save_orchestrator_checkpoint(orch)
    with open(checkpoint_file, "w") as f:
        json.dump(data, f, indent=2)


def _output_state(orch: Orchestrator) -> None:
    """Print orchestrator state as JSON."""
    state = orch._make_state()
    agents = orch.get_agents_for_phase(state.current_phase) if state.current_phase else []
    output = {
        "phase": state.current_phase,
        "is_terminal": state.is_terminal,
        "phase_history": state.phase_history,
        "context": state.context,
        "agents": [a.name for a in agents],
        "agent_statuses": {name: a.status.value for name, a in orch._agents.items()},
    }
    print(json.dumps(output, indent=2))


def cmd_start(args: argparse.Namespace) -> None:
    mode = args.mode
    ctx = json.loads(args.context) if args.context else {}
    checkpoint_file = args.checkpoint or DEFAULT_CHECKPOINT

    orch = build_analyze_workflow() if mode == "analyze" else build_build_workflow()
    initial_phase = "research" if mode == "analyze" else "plan"
    orch.start(initial_phase, context=ctx)
    _save(orch, checkpoint_file)
    _output_state(orch)


def cmd_advance(args: argparse.Namespace) -> None:
    mode = args.mode
    ctx = json.loads(args.context) if args.context else None
    checkpoint_file = args.checkpoint or DEFAULT_CHECKPOINT

    orch = _load_or_create(mode, checkpoint_file)
    if orch._current_phase is None:
        print(json.dumps({"error": "Orchestrator not started. Run 'start' first."}))
        sys.exit(1)

    orch.advance(context=ctx)
    _save(orch, checkpoint_file)
    _output_state(orch)


def cmd_status(args: argparse.Namespace) -> None:
    mode = args.mode
    checkpoint_file = args.checkpoint or DEFAULT_CHECKPOINT

    orch = _load_or_create(mode, checkpoint_file)
    if orch._current_phase is None:
        print(json.dumps({"phase": None, "message": "Not started"}))
    else:
        _output_state(orch)


def cmd_checkpoint(args: argparse.Namespace) -> None:
    src = args.checkpoint or DEFAULT_CHECKPOINT
    dest = args.file or src
    if os.path.exists(src):
        if src != dest:
            import shutil

            shutil.copy2(src, dest)
        print(json.dumps({"saved": dest}))
    else:
        print(json.dumps({"error": f"No checkpoint at {src}"}))
        sys.exit(1)


def cmd_restore(args: argparse.Namespace) -> None:
    mode = args.mode
    src = args.file
    checkpoint_file = args.checkpoint or DEFAULT_CHECKPOINT

    if not os.path.exists(src):
        print(json.dumps({"error": f"File not found: {src}"}))
        sys.exit(1)

    with open(src) as f:
        data = json.load(f)

    orch = build_analyze_workflow() if mode == "analyze" else build_build_workflow()
    load_orchestrator_checkpoint(orch, data)
    _save(orch, checkpoint_file)
    _output_state(orch)


def cmd_validate(args: argparse.Namespace) -> None:
    """Run a validation bundle against the workspace."""
    bundle = args.check
    workspace = args.workspace
    kwargs = {}
    if args.round:
        kwargs["round_num"] = args.round

    result = gate_checks.run_validation(bundle, workspace, **kwargs)
    print(json.dumps(result, indent=2))


def cmd_compute_belief(args: argparse.Namespace) -> None:
    """Compute belief state mechanically from workspace content."""
    belief_mode = args.belief_mode
    workspace = args.workspace
    round_num = args.round

    result = gate_checks.run_compute_belief(belief_mode, workspace, round_num)
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Sigma-review orchestrator CLI")
    parser.add_argument("--mode", choices=["analyze", "build"], default="analyze")
    parser.add_argument("--checkpoint", help=f"Checkpoint file path (default: {DEFAULT_CHECKPOINT})")

    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Start a new workflow")
    p_start.add_argument("--context", help="JSON context string")

    p_advance = sub.add_parser("advance", help="Advance to next phase")
    p_advance.add_argument("--context", help="JSON context update string")

    p_status = sub.add_parser("status", help="Show current state")

    p_checkpoint = sub.add_parser("checkpoint", help="Save checkpoint to file")
    p_checkpoint.add_argument("--file", help="Destination file path")

    p_restore = sub.add_parser("restore", help="Restore from checkpoint file")
    p_restore.add_argument("--file", required=True, help="Source file path")

    p_validate = sub.add_parser("validate", help="Run validation bundle against workspace")
    p_validate.add_argument(
        "--check",
        required=True,
        choices=list(gate_checks.BUNDLES.keys()),
        help="Validation bundle to run",
    )
    p_validate.add_argument(
        "--workspace",
        default=None,
        help=f"Workspace path (default: {gate_checks.DEFAULT_WORKSPACE})",
    )
    p_validate.add_argument("--round", type=int, default=None, help="Round number (for round-specific checks)")

    p_belief = sub.add_parser("compute-belief", help="Compute belief state from workspace")
    p_belief.add_argument(
        "--belief-mode",
        required=True,
        choices=list(gate_checks.BELIEF_MODES.keys()),
        help="Belief computation mode",
    )
    p_belief.add_argument(
        "--workspace",
        default=None,
        help=f"Workspace path (default: {gate_checks.DEFAULT_WORKSPACE})",
    )
    p_belief.add_argument("--round", type=int, default=None, help="Round number")

    args = parser.parse_args()

    commands = {
        "start": cmd_start,
        "advance": cmd_advance,
        "status": cmd_status,
        "checkpoint": cmd_checkpoint,
        "restore": cmd_restore,
        "validate": cmd_validate,
        "compute-belief": cmd_compute_belief,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
