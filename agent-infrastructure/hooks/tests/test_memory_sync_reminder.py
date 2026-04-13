"""Tests for memory-sync-reminder.py hook."""
import json
import os
import sys
import time
from pathlib import Path

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
memory_sync = importlib.import_module("memory-sync-reminder")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    """Ensure clean state for each test."""
    state_file = tmp_path / ".sigma-memory-sync-state"
    monkeypatch.setattr(memory_sync, "STATE_FILE", state_file)


# ---------------------------------------------------------------------------
# is_auto_memory_write
# ---------------------------------------------------------------------------

class TestIsAutoMemoryWrite:
    def test_detects_auto_memory_path(self):
        assert memory_sync.is_auto_memory_write(
            "/Users/bjgilbert/.claude/projects/-Users-bjgilbert/memory/feedback_test.md"
        ) is True

    def test_rejects_non_memory_path(self):
        assert memory_sync.is_auto_memory_write(
            "/Users/bjgilbert/Projects/myapp/src/main.py"
        ) is False

    def test_rejects_non_md_file(self):
        assert memory_sync.is_auto_memory_write(
            "/Users/bjgilbert/.claude/projects/-Users-bjgilbert/memory/state.json"
        ) is False


# ---------------------------------------------------------------------------
# is_sigma_mem_direct_write
# ---------------------------------------------------------------------------

class TestIsSigmaMemDirectWrite:
    def test_detects_sigma_mem_path(self):
        assert memory_sync.is_sigma_mem_direct_write(
            "/Users/bjgilbert/.claude/memory/patterns.md"
        ) is True

    def test_rejects_non_sigma_path(self):
        assert memory_sync.is_sigma_mem_direct_write(
            "/Users/bjgilbert/.claude/agents/tech-architect.md"
        ) is False


# ---------------------------------------------------------------------------
# is_globally_relevant
# ---------------------------------------------------------------------------

class TestIsGloballyRelevant:
    def test_feedback_file_is_relevant(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/feedback_anti-sycophancy.md"
        ) is True

    def test_project_file_is_relevant(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/project_sigma-ui.md"
        ) is True

    def test_reference_file_is_relevant(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/reference_api-limits.md"
        ) is True

    def test_user_file_is_relevant(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/user_hardware.md"
        ) is True

    def test_random_file_not_relevant_without_keywords(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/random-note.md", "some random text"
        ) is False

    def test_content_with_decision_keywords_is_relevant(self):
        assert memory_sync.is_globally_relevant(
            "/path/to/memory/note.md",
            "This decision was established as a settled pattern"
        ) is True


# ---------------------------------------------------------------------------
# classify_write
# ---------------------------------------------------------------------------

class TestClassifyWrite:
    def test_sigma_mem_direct_write_warns(self):
        result = memory_sync.classify_write(
            "/Users/test/.claude/memory/patterns.md"
        )
        assert result is not None
        assert "MCP tools" in result

    def test_auto_memory_feedback_suggests_correction(self):
        result = memory_sync.classify_write(
            "/Users/test/.claude/projects/-Users-test/memory/feedback_test.md",
            "correction content"
        )
        assert result is not None
        assert "log_correction" in result

    def test_auto_memory_project_suggests_decision(self):
        result = memory_sync.classify_write(
            "/Users/test/.claude/projects/-Users-test/memory/project_test.md",
            "project state"
        )
        assert result is not None
        assert "log_decision" in result or "store_memory" in result

    def test_non_memory_write_returns_none(self):
        result = memory_sync.classify_write(
            "/Users/test/Projects/app/src/main.py",
            "def hello(): pass"
        )
        assert result is None

    def test_non_relevant_auto_memory_returns_none(self):
        result = memory_sync.classify_write(
            "/Users/test/.claude/projects/-Users-test/memory/random-note.md",
            "just a note"
        )
        assert result is None


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

class TestState:
    def test_fresh_state_has_zero_count(self):
        state = memory_sync.read_state()
        assert state["reminder_count"] == 0

    def test_state_persists_after_write(self, tmp_path):
        memory_sync.write_state({"reminder_count": 2, "last_reset": time.time()})
        state = memory_sync.read_state()
        assert state["reminder_count"] == 2

    def test_state_resets_after_ttl(self, tmp_path):
        old_time = time.time() - (5 * 3600)  # 5 hours ago
        memory_sync.write_state({"reminder_count": 2, "last_reset": old_time})
        state = memory_sync.read_state()
        assert state["reminder_count"] == 0  # Reset


# ---------------------------------------------------------------------------
# Integration: main()
# ---------------------------------------------------------------------------

class TestMain:
    def test_fires_on_feedback_write(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/Users/test/.claude/projects/-Users-test/memory/feedback_test.md",
                "content": "---\ntype: feedback\n---\nDon't do that",
            },
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert "systemMessage" in output
        assert "log_correction" in output["systemMessage"]

    def test_fires_on_sigma_mem_direct_write(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/Users/test/.claude/memory/patterns.md",
                "content": "some pattern",
            },
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert "MCP tools" in output["systemMessage"]

    def test_silent_on_non_memory_write(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/Users/test/Projects/app/main.py",
                "content": "code",
            },
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        assert capsys.readouterr().out == ""

    def test_respects_max_reminders(self, monkeypatch, capsys):
        # Burn through max reminders
        memory_sync.write_state({
            "reminder_count": memory_sync.MAX_REMINDERS,
            "last_reset": time.time()
        })

        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": "/Users/test/.claude/projects/-test/memory/feedback_x.md",
                "content": "feedback",
            },
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        assert capsys.readouterr().out == ""  # Silent — max reached

    def test_ignores_non_write_tools(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file"},
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        assert capsys.readouterr().out == ""

    def test_handles_garbage_input(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO("not json"))
        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()
        assert exc_info.value.code == 0

    def test_handles_empty_input(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(""))
        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()
        assert exc_info.value.code == 0

    def test_handles_edit_tool(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Edit",
            "tool_input": {
                "file_path": "/Users/test/.claude/memory/decisions.md",
                "new_string": "new decision content",
                "old_string": "old content",
            },
        })))

        with pytest.raises(SystemExit) as exc_info:
            memory_sync.main()

        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert "MCP tools" in output["systemMessage"]
