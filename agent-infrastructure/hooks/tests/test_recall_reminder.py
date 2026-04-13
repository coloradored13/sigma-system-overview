"""Tests for recall-reminder.py hook."""
import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

import pytest

# Import the module under test
sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
recall_reminder = importlib.import_module("recall-reminder")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def clean_state(tmp_path, monkeypatch):
    """Ensure clean state for each test."""
    session_file = tmp_path / ".sigma-recall-session"
    nudge_file = tmp_path / ".sigma-recall-nudged"
    monkeypatch.setattr(recall_reminder, "SESSION_STATE", session_file)
    monkeypatch.setattr(recall_reminder, "Path", type(session_file))
    # Patch the nudge file path by patching the function internals
    original_nudge_sent = recall_reminder.nudge_already_sent
    original_mark_nudge = recall_reminder.mark_nudge_sent

    def patched_nudge_sent():
        if not nudge_file.exists():
            return False
        try:
            mtime = nudge_file.stat().st_mtime
            age = time.time() - mtime
            return age < 1800
        except OSError:
            return False

    def patched_mark_nudge():
        nudge_file.write_text(str(time.time()), encoding="utf-8")

    monkeypatch.setattr(recall_reminder, "nudge_already_sent", patched_nudge_sent)
    monkeypatch.setattr(recall_reminder, "mark_nudge_sent", patched_mark_nudge)
    yield


# ---------------------------------------------------------------------------
# recall_done_recently
# ---------------------------------------------------------------------------

class TestRecallDoneRecently:
    def test_false_when_no_state_file(self):
        assert recall_reminder.recall_done_recently() is False

    def test_true_after_mark(self):
        recall_reminder.mark_recall_done()
        assert recall_reminder.recall_done_recently() is True

    def test_false_after_ttl(self, monkeypatch):
        recall_reminder.mark_recall_done()
        # Pretend time has advanced past TTL
        monkeypatch.setattr(recall_reminder, "RECALL_TTL_SECONDS", 0)
        # Need a tiny sleep so age > 0
        assert recall_reminder.recall_done_recently() is False


# ---------------------------------------------------------------------------
# check_memory_drift
# ---------------------------------------------------------------------------

class TestCheckMemoryDrift:
    def test_no_drift_when_both_recent(self, tmp_path, monkeypatch):
        auto_dir = tmp_path / "auto"
        sigma_dir = tmp_path / "sigma"
        auto_dir.mkdir()
        sigma_dir.mkdir()
        (auto_dir / "MEMORY.md").write_text("test")
        (sigma_dir / "patterns.md").write_text("test")

        monkeypatch.setattr(recall_reminder, "AUTO_MEMORY_DIR", auto_dir)
        monkeypatch.setattr(recall_reminder, "SIGMA_MEM_DIR", sigma_dir)

        assert recall_reminder.check_memory_drift() is None

    def test_drift_detected_when_stale(self, tmp_path, monkeypatch):
        auto_dir = tmp_path / "auto"
        sigma_dir = tmp_path / "sigma"
        auto_dir.mkdir()
        sigma_dir.mkdir()

        auto_file = auto_dir / "MEMORY.md"
        auto_file.write_text("test")
        sigma_file = sigma_dir / "patterns.md"
        sigma_file.write_text("test")

        # Make sigma-mem file appear 3 days old
        old_time = time.time() - (72 * 3600)
        os.utime(sigma_file, (old_time, old_time))

        monkeypatch.setattr(recall_reminder, "AUTO_MEMORY_DIR", auto_dir)
        monkeypatch.setattr(recall_reminder, "SIGMA_MEM_DIR", sigma_dir)

        result = recall_reminder.check_memory_drift()
        assert result is not None
        assert "sigma-mem" in result
        assert "drift" in result.lower()

    def test_no_drift_when_dirs_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(recall_reminder, "AUTO_MEMORY_DIR", tmp_path / "missing1")
        monkeypatch.setattr(recall_reminder, "SIGMA_MEM_DIR", tmp_path / "missing2")
        assert recall_reminder.check_memory_drift() is None


# ---------------------------------------------------------------------------
# get_newest_mtime
# ---------------------------------------------------------------------------

class TestGetNewestMtime:
    def test_returns_zero_for_missing_dir(self, tmp_path):
        assert recall_reminder.get_newest_mtime(tmp_path / "nope") == 0

    def test_finds_newest_file(self, tmp_path):
        (tmp_path / "old.md").write_text("old")
        old_time = time.time() - 3600
        os.utime(tmp_path / "old.md", (old_time, old_time))

        (tmp_path / "new.md").write_text("new")

        result = recall_reminder.get_newest_mtime(tmp_path)
        # Should be close to now (the new.md file)
        assert time.time() - result < 5

    def test_traverses_subdirs(self, tmp_path):
        sub = tmp_path / "sub" / "deep"
        sub.mkdir(parents=True)
        (sub / "file.md").write_text("deep")

        result = recall_reminder.get_newest_mtime(tmp_path)
        assert result > 0

    def test_ignores_non_md_files(self, tmp_path):
        (tmp_path / "file.txt").write_text("not md")
        assert recall_reminder.get_newest_mtime(tmp_path) == 0


# ---------------------------------------------------------------------------
# Integration: main() via subprocess
# ---------------------------------------------------------------------------

class TestMainPreToolUse:
    def test_nudge_fires_on_first_call(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.py"},
        })))

        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()

        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert "systemMessage" in output
        assert "recall" in output["systemMessage"].lower()

    def test_no_nudge_after_recall(self, tmp_path, monkeypatch, capsys):
        recall_reminder.mark_recall_done()

        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.py"},
        })))

        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr().out
        assert captured == ""  # No output = no nudge

    def test_no_double_nudge(self, tmp_path, monkeypatch, capsys):
        # First call sends nudge
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PreToolUse",
            "tool_name": "Read",
            "tool_input": {"file_path": "/some/file.py"},
        })))
        with pytest.raises(SystemExit):
            recall_reminder.main()
        first_output = capsys.readouterr().out
        assert "recall" in first_output.lower()

        # Second call should be silent (nudge already sent)
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "ls"},
        })))
        with pytest.raises(SystemExit):
            recall_reminder.main()
        second_output = capsys.readouterr().out
        assert second_output == ""


class TestMainPostToolUse:
    def test_marks_recall_done(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "mcp__sigma-mem__recall",
            "tool_input": {},
        })))

        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()

        assert exc_info.value.code == 0
        assert recall_reminder.recall_done_recently()

    def test_ignores_other_tools(self, tmp_path, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(json.dumps({
            "event": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {},
        })))

        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()

        assert exc_info.value.code == 0
        assert not recall_reminder.recall_done_recently()


class TestMainInvalidInput:
    def test_garbage_input(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO("not json"))
        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()
        assert exc_info.value.code == 0

    def test_empty_input(self, monkeypatch, capsys):
        monkeypatch.setattr("sys.stdin", __import__("io").StringIO(""))
        with pytest.raises(SystemExit) as exc_info:
            recall_reminder.main()
        assert exc_info.value.code == 0
