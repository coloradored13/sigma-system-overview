"""Shared fixtures for hook script tests.

Two testing strategies:
1. Unit tests: import modules, monkeypatch Path constants to tmp dirs
2. Integration tests: set HOME to tmp dir, run scripts via subprocess
"""
import json
import os
import sys
import subprocess
from pathlib import Path

import pytest


HOOKS_DIR = Path(__file__).parent.parent


def get_infra_dir() -> Path:
    """Return the infrastructure directory for structural tests.

    Uses SIGMA_INFRA_DIR env var if set (for CI where ~/.claude doesn't exist),
    otherwise defaults to ~/.claude (for local runs with symlinks installed).
    """
    env_dir = os.environ.get("SIGMA_INFRA_DIR")
    if env_dir:
        return Path(env_dir)
    return Path.home() / ".claude"


@pytest.fixture
def tmp_home(tmp_path):
    """Create a fake HOME with .claude structure for integration tests."""
    home = tmp_path / "home"
    (home / ".claude" / "teams" / "sigma-review" / "shared").mkdir(parents=True)
    (home / ".claude" / "teams" / "sigma-build" / "shared").mkdir(parents=True)
    (home / ".claude" / "agents").mkdir(parents=True)
    (home / ".claude" / "skills").mkdir(parents=True)
    (home / ".claude" / "hooks").mkdir(parents=True)
    return home


@pytest.fixture
def review_workspace(tmp_home):
    """Create a sigma-review workspace with content."""
    ws = tmp_home / ".claude" / "teams" / "sigma-review" / "shared" / "workspace.md"

    def _write(content):
        ws.write_text(content, encoding="utf-8")
        return ws

    return _write


@pytest.fixture
def build_workspace(tmp_home):
    """Create a sigma-build workspace with content."""
    ws = tmp_home / ".claude" / "teams" / "sigma-build" / "shared" / "workspace.md"

    def _write(content):
        ws.write_text(content, encoding="utf-8")
        return ws

    return _write


@pytest.fixture
def patterns_file(tmp_home):
    """Path to patterns.md (may or may not exist)."""
    return tmp_home / ".claude" / "teams" / "sigma-review" / "shared" / "patterns.md"


# --- Sample workspace content for testing ---

SAMPLE_WORKSPACE_COMPLETE = """\
## task
Analyze competitive landscape for loan admin tech

## infrastructure
ΣVerify: openai:gpt-4o available

## prompt-decomposition
Q1: Who are the real competitors?
Q2: What technology capabilities create durable advantage?
H1: Technology is the primary differentiator
H2: Private credit is the entry point
H3: Incumbents have aging tech stacks
C1: Scope is third-party loan admin

## convergence
product-strategist: ✓ competitive landscape mapped |4 findings |→ ready
loan-ops-tech-specialist: ✓ operational depth reviewed |3 findings |→ ready
tech-architect: ✓ architecture patterns compared |2 findings |→ ready
reference-class-analyst: ✓ base rates calibrated |2 findings |→ ready
devils-advocate: ✓ challenges complete |→ synthesis

## findings
F[market-size]: $2.8-3.4B TAM |source:independent-research(WebSearch):T2(LSTA)|
F[tech-moat]: API-first architecture enables 3x faster integration |source:independent-research(code-read):T1|
F[entry-barrier]: Charter requirements create 18-month regulatory moat |source:skill(loan-agency/qr-operational-mechanics):T1|
Revised from initial assessment after DA challenge — outcome 1
CHECK CONFIRMS with acknowledged risk — outcome 2
gap: CLO trustee mechanics not covered — outcome 3
XVERIFY[openai:gpt-4o] market size corroborated
concede DA point on regulatory timeline
TIER-2 complexity assessment
"""

SAMPLE_WORKSPACE_NO_CONVERGENCE = """\
## task
Early research phase

## findings
Some preliminary findings
"""

SAMPLE_BUILD_WORKSPACE = """\
## build-track
Implementation phase active

## plan-track
Architecture locked

## 04-build
Building payment processing module
"""

SAMPLE_AGENT_MESSAGE_RICH = """\
product-strategist: ✓ findings complete
F[competitive-landscape]: 5 major competitors identified |source:independent-research(WebSearch):T2(Gartner)|
F[market-entry]: Window closing, 12-18 months |source:agent-inference|
F1: Technology differentiation confirmed |source:independent-research(code-read):T1|
DA grade: B+
§2a outcome 2: positioning confirmed with acknowledged risk
XVERIFY[openai:gpt-4o] market sizing verified
Revised per DA challenge on timeline estimate
"""

SAMPLE_AGENT_MESSAGE_SPARSE = """\
Some general status update without structured findings
"""


def run_hook(script_name, stdin_data, tmp_home=None):
    """Run a hook script via subprocess with JSON on stdin.

    Returns (exit_code, stdout, stderr).
    """
    script_path = HOOKS_DIR / script_name
    env = os.environ.copy()
    if tmp_home:
        env["HOME"] = str(tmp_home)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        input=json.dumps(stdin_data),
        capture_output=True,
        text=True,
        env=env,
        timeout=10,
    )
    return result.returncode, result.stdout, result.stderr
