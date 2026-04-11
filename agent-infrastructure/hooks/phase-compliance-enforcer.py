#!/usr/bin/env python3
"""Phase Compliance Enforcer — PreToolUse + PostToolUse hook.

Mechanical enforcement layer for sigma-review and sigma-build.
Fires on every Read and Bash (PreToolUse, can BLOCK) and every
Write/Edit/Bash (PostToolUse, observe + track).

HARD BLOCKS (PreToolUse exit code 2 — lead cannot proceed):
  1. Phase skip — blocks reading phase files ahead of orchestrator
  2. DA exit-gate — blocks advance from challenge/review without exit-gate: PASS in workspace
  3. BELIEF on advance — blocks advance from challenge/review without BELIEF[] in workspace
  4. CB evidence — blocks advance from circuit_breaker without CB[]/divergence in workspace
  5. Lead synthesis write — blocks writing synthesis/report during synthesis without agent evidence

SOFT WARNS (PostToolUse/Stop systemMessage — guidance):
  6. BELIEF format — warns when BELIEF[] present but malformed
  7. Context firewall — warns when personal context detected in workspace writes
  8. Synthesis file gate — warns when advancing past synthesis without file written

The lead agent cannot opt out — hooks fire automatically on tool calls.
Design principle: if a WARN can be ignored like a directive, and there's no legitimate
override, it must be a BLOCK.
"""
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CHECKPOINT = Path("/tmp/sigma-review-orchestrator.json")
STATE_FILE = Path.home() / ".claude" / "hooks" / ".phase-compliance-state.json"

# Phase file → orchestrator phase name mapping
# "pre" phases (00, 01) run before orchestrator starts — always allowed
ANALYZE_PHASE_MAP = {
    "00-preflight": "pre",
    "01-spawn": "pre",
    "02-research": "research",
    "03-circuit-breaker": "circuit_breaker",
    "04-challenge": "challenge",
    "05-debate": "debate",
    "06-synthesis": "synthesis",
    "06b-compilation": "compilation",
    "07-promotion": "promotion",
    "08-sync": "sync",
    "09-archive": "archive",
    "10-shutdown": "complete",
}

BUILD_PHASE_MAP = {
    "00-preflight": "pre",
    "01-spawn": "pre",
    "02-plan": "plan",
    "03-plan-challenge": "challenge_plan",
    "04-build": "build",
    "05-build-review": "review",
    "05b-debate": "debate",
    "06-synthesis": "synthesis",
    "06b-compilation": "compilation",
    "07-promotion": "promotion",
    "08-sync": "sync",
    "09-archive": "archive",
    "10-shutdown": "complete",
}

# Ordered phase sequences (orchestrator progression order)
ANALYZE_PHASE_ORDER = [
    "pre", "research", "circuit_breaker", "challenge", "debate",
    "synthesis", "compilation", "promotion", "sync", "archive", "complete",
]

BUILD_PHASE_ORDER = [
    "pre", "plan", "challenge_plan", "build", "review", "debate",
    "synthesis", "compilation", "promotion", "sync", "archive", "complete",
]

# Phases where BELIEF[] must be written before advancing
BELIEF_REQUIRED_PHASES = {"challenge", "challenge_plan", "review"}

# Validation bundles required per phase (from orchestrator-config.py)
PHASE_REQUIRED_VALIDATIONS = {
    "research": "r1-convergence",
    "circuit_breaker": "cb",
    "challenge": "challenge-round",
    "plan": "plan-convergence",
    "challenge_plan": "challenge-round",
    "build": "build-checkpoint",
    "review": "pre-synthesis",
}

# Phases where DA exit-gate PASS is required before advancing
DA_EXIT_GATE_PHASES = {"challenge", "challenge_plan", "review"}

# Phase file path patterns
REVIEW_PHASES_PATH = "sigma-review/phases/"
BUILD_PHASES_PATH = "sigma-build/phases/"

# Default workspace for reading DA exit-gate / BELIEF / CB evidence
DEFAULT_WORKSPACE = Path.home() / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"

# Personal context keywords for firewall detection
CONTEXT_FIREWALL_KEYWORDS = [
    r"\bmy career\b", r"\bmy role\b", r"\bmy experience\b",
    r"\bmy salary\b", r"\bmy family\b", r"\bmy job\b",
    r"\bI should\b.*(?:career|job|position|role)",
    r"\bpersonally I\b",
]


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def read_checkpoint():
    """Read orchestrator checkpoint. Returns dict or None if no active session."""
    if not DEFAULT_CHECKPOINT.exists():
        return None
    try:
        with open(DEFAULT_CHECKPOINT) as f:
            data = json.load(f)
        phase = data.get("current_phase")
        if not phase or phase == "complete":
            return None
        return data
    except (json.JSONDecodeError, OSError):
        return None


def read_state():
    """Read compliance tracking state."""
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def write_state(state):
    """Write compliance tracking state (atomic)."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(STATE_FILE) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, str(STATE_FILE))


def update_state(**kwargs):
    """Merge keys into state."""
    state = read_state()
    state.update(kwargs)
    write_state(state)
    return state


def read_workspace_content():
    """Read the sigma-review workspace. Returns content or empty string."""
    try:
        return DEFAULT_WORKSPACE.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError):
        return ""


# ---------------------------------------------------------------------------
# Phase ordering logic
# ---------------------------------------------------------------------------

def get_mode_and_maps(checkpoint):
    """Get mode, phase map, and phase order from checkpoint."""
    mode = checkpoint.get("_mode", "analyze")
    if mode == "build":
        return mode, BUILD_PHASE_MAP, BUILD_PHASE_ORDER
    return mode, ANALYZE_PHASE_MAP, ANALYZE_PHASE_ORDER


def phase_index(phase_name, phase_order):
    """Get the index of a phase in the ordering. Returns -1 if not found."""
    try:
        return phase_order.index(phase_name)
    except ValueError:
        return -1


def extract_phase_from_path(file_path):
    """Extract phase file stem from a path. Returns (stem, mode_hint) or (None, None).

    Examples:
      .../sigma-review/phases/04-challenge.md → ("04-challenge", "analyze")
      .../sigma-build/phases/02-plan.md → ("02-plan", "build")
    """
    if REVIEW_PHASES_PATH in file_path:
        basename = os.path.basename(file_path)
        stem = basename.replace(".md", "")
        return stem, "analyze"
    if BUILD_PHASES_PATH in file_path:
        basename = os.path.basename(file_path)
        stem = basename.replace(".md", "")
        return stem, "build"
    return None, None


# ---------------------------------------------------------------------------
# Enforcement: PreToolUse (can BLOCK)
# ---------------------------------------------------------------------------

def check_phase_skip(file_path, checkpoint):
    """Check if reading a phase file that's ahead of the orchestrator.

    Returns (should_block: bool, reason: str).
    """
    stem, file_mode = extract_phase_from_path(file_path)
    if not stem:
        return False, ""

    mode, phase_map, phase_order = get_mode_and_maps(checkpoint)

    # Mode mismatch: reading build phases during analyze or vice versa
    if file_mode != mode:
        # Not necessarily wrong — lead might reference the other mode's structure
        # Don't block, just ignore
        return False, ""

    target_phase = phase_map.get(stem)
    if not target_phase:
        return False, ""  # Unknown phase file — don't block

    # "pre" phases are always allowed
    if target_phase == "pre":
        return False, ""

    current_phase = checkpoint.get("current_phase", "")
    phase_history = checkpoint.get("phase_history", [])

    # Already visited this phase? Always allowed (re-reading)
    if target_phase in phase_history or target_phase == current_phase:
        return False, ""

    # Check ordering
    current_idx = phase_index(current_phase, phase_order)
    target_idx = phase_index(target_phase, phase_order)

    if target_idx < 0 or current_idx < 0:
        return False, ""  # Can't determine ordering

    # Allow reading the NEXT phase (valid transition) but not skipping multiple
    if target_idx <= current_idx + 1:
        return False, ""

    # Skipping ahead!
    return True, (
        f"PHASE SKIP BLOCKED: Orchestrator is in '{current_phase}' but you're reading "
        f"'{stem}.md' (phase '{target_phase}'). You cannot skip phases. "
        f"Complete '{current_phase}' first, then advance the orchestrator. "
        f"Run: python3 orchestrator-config.py --mode {mode} advance"
    )


def check_da_exit_gate_in_workspace(command, checkpoint):
    """BLOCK advance from challenge/review if DA exit-gate PASS not in workspace.

    The orchestrator's exit_gate_passed() checks context, which the lead sets
    manually. This hook validates the WORKSPACE EVIDENCE — DA must have actually
    written "exit-gate: PASS" to workspace.

    Returns (should_block: bool, reason: str).
    """
    if "orchestrator-config.py" not in command or "advance" not in command:
        return False, ""

    current_phase = checkpoint.get("current_phase", "")
    if current_phase not in DA_EXIT_GATE_PHASES:
        return False, ""

    workspace = read_workspace_content()
    if not workspace:
        return False, ""  # No workspace — can't validate

    has_exit_gate = bool(re.search(r"exit.gate:.*PASS", workspace, re.IGNORECASE))
    if has_exit_gate:
        return False, ""

    return True, (
        f"DA EXIT-GATE BLOCKED: Cannot advance from '{current_phase}' — "
        f"no 'exit-gate: PASS' found in workspace. DA must write explicit "
        f"exit-gate verdict to workspace before advancing to synthesis. "
        f"The lead cannot self-certify this gate."
    )


def check_belief_before_advance(command, checkpoint):
    """BLOCK advance from BELIEF-required phases without BELIEF[] in workspace.

    Returns (should_block: bool, reason: str).
    """
    if "orchestrator-config.py" not in command or "advance" not in command:
        return False, ""

    current_phase = checkpoint.get("current_phase", "")
    if current_phase not in BELIEF_REQUIRED_PHASES:
        return False, ""

    # Check state first (cheaper than reading workspace)
    state = read_state()
    if state.get("belief_written_current_phase"):
        return False, ""

    # Double-check workspace content
    workspace = read_workspace_content()
    if re.search(r"BELIEF\[", workspace):
        update_state(belief_written_current_phase=True)
        return False, ""

    return True, (
        f"BELIEF BLOCKED: Cannot advance from '{current_phase}' — "
        f"no BELIEF[] scores found in workspace. Write BELIEF[P(x)=N.NN] "
        f"to workspace before advancing. This is the most consistently "
        f"missed protocol element."
    )


def check_cb_evidence_before_advance(command, checkpoint):
    """BLOCK advance from circuit_breaker without CB evidence in workspace.

    Returns (should_block: bool, reason: str).
    """
    if "orchestrator-config.py" not in command or "advance" not in command:
        return False, ""

    current_phase = checkpoint.get("current_phase", "")
    if current_phase != "circuit_breaker":
        return False, ""

    workspace = read_workspace_content()
    if not workspace:
        return False, ""

    # Same patterns as gate_checks.py V9
    has_divergence = bool(re.search(
        r"divergence.detected|divergence.found|R1.divergence|divergence.logged",
        workspace, re.IGNORECASE,
    ))
    has_cb_entries = len(re.findall(r"CB\[\d\]", workspace)) >= 2
    has_cb_section = bool(re.search(
        r"circuit.breaker|zero.dissent.*fired|CB.*fired",
        workspace, re.IGNORECASE,
    ))

    if has_divergence or has_cb_entries or has_cb_section:
        return False, ""

    return True, (
        "CB EVIDENCE BLOCKED: Cannot advance from 'circuit_breaker' — "
        "no divergence log, CB[] entries, or circuit breaker section found in workspace. "
        "The zero-dissent check must produce evidence (divergence detected or CB responses) "
        "before advancing to the challenge phase."
    )


def block_lead_synthesis_write(file_path, checkpoint):
    """BLOCK the lead from writing synthesis/report files during synthesis phase
    without synthesis-agent evidence in workspace.

    Returns (should_block: bool, reason: str).
    """
    current_phase = checkpoint.get("current_phase", "")
    if current_phase != "synthesis":
        return False, ""

    # Only block synthesis/report file writes
    lower_path = file_path.lower()
    if "synthesis" not in lower_path and "report" not in lower_path:
        return False, ""

    # Check workspace for synthesis-agent evidence
    workspace = read_workspace_content()
    has_synthesis_agent = bool(re.search(
        r"###\s*synthesis.agent|synthesis.agent:\s*✓|synthesis.agent.*converge",
        workspace, re.IGNORECASE,
    ))

    if has_synthesis_agent:
        return False, ""  # Synthesis agent was spawned — write is legitimate

    return True, (
        "LEAD SYNTHESIS BLOCKED: Cannot write synthesis/report file directly — "
        "no synthesis-agent evidence found in workspace. The lead must spawn a "
        "synthesis agent to write synthesis content. Writing synthesis directly "
        "contaminates provenance (conversation context leaks into what should be "
        "agent-firewalled analysis)."
    )


def enforce_pre_tool_use(data):
    """PreToolUse enforcement. Returns (exit_code, output_dict)."""
    checkpoint = read_checkpoint()
    if not checkpoint:
        return 0, {}  # No active session

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        should_block, reason = check_phase_skip(file_path, checkpoint)
        if should_block:
            return 2, {"reason": reason}

    elif tool_name == "Bash":
        command = tool_input.get("command", "")

        # Check all advance-time BLOCKs
        for check_fn in (check_da_exit_gate_in_workspace,
                         check_belief_before_advance,
                         check_cb_evidence_before_advance):
            should_block, reason = check_fn(command, checkpoint)
            if should_block:
                return 2, {"reason": reason}

    elif tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        should_block, reason = block_lead_synthesis_write(file_path, checkpoint)
        if should_block:
            return 2, {"reason": reason}

    return 0, {}


# ---------------------------------------------------------------------------
# Enforcement: PostToolUse (observe + warn)
# ---------------------------------------------------------------------------

def track_validation_run(command, checkpoint):
    """Track when orchestrator validate is run."""
    if "orchestrator-config.py" not in command:
        return

    if "validate" not in command:
        return

    # Extract which bundle was validated
    bundle_match = re.search(r"--check\s+(\S+)", command)
    if bundle_match:
        bundle = bundle_match.group(1)
        state = read_state()
        current_phase = checkpoint.get("current_phase", "")

        validations = state.get("validations_this_phase", [])
        if bundle not in validations:
            validations.append(bundle)

        update_state(
            validations_this_phase=validations,
            last_validated_phase=current_phase,
        )


def track_advance(command, checkpoint):
    """Track when orchestrator advance is run — reset per-phase state."""
    if "orchestrator-config.py" not in command:
        return

    if "advance" not in command:
        return

    # Phase may have changed — reset per-phase tracking
    update_state(
        validations_this_phase=[],
        belief_written_current_phase=False,
        last_advance_time=datetime.now().isoformat(),
    )


def track_belief_write(file_path, content, checkpoint):
    """Track BELIEF[] writes to workspace. Warn on missing or malformed format."""
    if "workspace" not in file_path.lower():
        return None

    current_phase = checkpoint.get("current_phase", "")
    if current_phase not in BELIEF_REQUIRED_PHASES:
        return None

    belief_matches = re.findall(r"BELIEF\[([^\]]*)\]", content)
    if belief_matches:
        update_state(belief_written_current_phase=True)
        # Check format: should be BELIEF[P(x)=N.NN]
        for match in belief_matches:
            if not re.search(r"P\(.+\)\s*=\s*\d+\.\d+", match):
                return (
                    f"BELIEF FORMAT: Found BELIEF[{match}] but expected format "
                    f"BELIEF[P(description)=N.NN]. Example: BELIEF[P(viable)=0.72]. "
                    f"The probability value enables mechanical tracking."
                )
        return None

    # Writing to workspace during a BELIEF-required phase without BELIEF[]
    state = read_state()
    if not state.get("belief_written_current_phase"):
        return (
            f"BELIEF[] MISSING: You're writing to workspace during '{current_phase}' phase "
            f"but haven't included BELIEF[] scores. BELIEF tracking is mandatory during "
            f"challenge/review phases. Write BELIEF[P(x)=N.NN] to workspace before advancing."
        )
    return None


def detect_context_firewall_leak(file_path, content, checkpoint):
    """WARN if personal context markers detected in workspace writes."""
    if "workspace" not in file_path.lower():
        return None

    for pattern in CONTEXT_FIREWALL_KEYWORDS:
        if re.search(pattern, content, re.IGNORECASE):
            return (
                "CONTEXT FIREWALL: Possible personal context leak detected in workspace "
                "write. Personal context (career, role, family, salary) must not appear "
                "in analytical workspace — it contaminates agent analysis. Review and "
                "strip before writing."
            )
    return None


def track_synthesis_write(file_path, content, checkpoint):
    """Track synthesis file writes."""
    current_phase = checkpoint.get("current_phase", "")
    if current_phase != "synthesis":
        return

    # Check if this looks like a synthesis file
    if "synthesis" in file_path.lower() or "report" in file_path.lower():
        update_state(synthesis_file_written=True, synthesis_file_path=file_path)


def check_synthesis_before_advance(command, checkpoint):
    """Warn if advancing past synthesis without writing synthesis file."""
    if "orchestrator-config.py" not in command or "advance" not in command:
        return None

    current_phase = checkpoint.get("current_phase", "")
    if current_phase != "synthesis":
        return None

    state = read_state()
    if not state.get("synthesis_file_written"):
        return (
            "SYNTHESIS FILE GATE: You're advancing past synthesis but haven't written "
            "the synthesis to a file. Synthesis must be saved as an artifact before "
            "advancing. Write the synthesis document, then advance."
        )
    return None


def enforce_post_tool_use(data):
    """PostToolUse enforcement. Returns output_dict with optional systemMessage."""
    checkpoint = read_checkpoint()
    if not checkpoint:
        return {}

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
    warnings = []

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        track_validation_run(command, checkpoint)
        track_advance(command, checkpoint)

        warn = check_synthesis_before_advance(command, checkpoint)
        if warn:
            warnings.append(warn)

    elif tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "") if tool_name == "Write" else tool_input.get("new_string", "")

        belief_warn = track_belief_write(file_path, content, checkpoint)
        if belief_warn:
            warnings.append(belief_warn)

        firewall_warn = detect_context_firewall_leak(file_path, content, checkpoint)
        if firewall_warn:
            warnings.append(firewall_warn)

        track_synthesis_write(file_path, content, checkpoint)

    if warnings:
        return {"systemMessage": " | ".join(warnings)}

    return {}


# ---------------------------------------------------------------------------
# Stop hook: end-of-turn compliance check
# ---------------------------------------------------------------------------

def enforce_stop(data):
    """Stop hook — check end-of-turn compliance. Returns output_dict."""
    checkpoint = read_checkpoint()
    if not checkpoint:
        return {}

    current_phase = checkpoint.get("current_phase", "")
    state = read_state()
    warnings = []

    # Check BELIEF tracking at end of turn during challenge/review
    if current_phase in BELIEF_REQUIRED_PHASES:
        if not state.get("belief_written_current_phase"):
            warnings.append(
                f"BELIEF[] NOT WRITTEN: Phase '{current_phase}' requires BELIEF[] scores "
                f"in workspace. This is the most consistently missed protocol element. "
                f"Write BELIEF[P(x)=N.NN] to workspace before declaring convergence."
            )

    # Check sigma-verify usage (reads MCP monitor state if available)
    if current_phase in BELIEF_REQUIRED_PHASES:
        mcp_state_file = STATE_FILE.parent / ".mcp-compliance-state.json"
        try:
            if mcp_state_file.exists():
                mcp_state = json.loads(mcp_state_file.read_text())
                if mcp_state.get("xverify_available") and not mcp_state.get("xverify_calls_this_phase", 0):
                    warnings.append(
                        "XVERIFY UNUSED: ΣVerify is available but no verify_finding calls "
                        "were made this phase. Agents must verify top load-bearing finding."
                    )
        except (json.JSONDecodeError, OSError):
            pass

    if warnings:
        return {"systemMessage": " | ".join(warnings)}

    return {}


# ---------------------------------------------------------------------------
# Main dispatch
# ---------------------------------------------------------------------------

def main():
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    event = data.get("hook_event_name", "")

    if event == "PreToolUse":
        exit_code, output = enforce_pre_tool_use(data)
        if output:
            print(json.dumps(output))
        sys.exit(exit_code)

    elif event == "PostToolUse":
        output = enforce_post_tool_use(data)
        if output:
            print(json.dumps(output))
        sys.exit(0)

    elif event == "Stop":
        output = enforce_stop(data)
        if output:
            print(json.dumps(output))
        sys.exit(0)

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
