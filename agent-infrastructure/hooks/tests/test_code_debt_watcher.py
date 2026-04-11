"""Tests for code-debt-watcher.py — PostToolUse hook on Write|Edit."""
import sys
import json
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib
watcher = importlib.import_module("code-debt-watcher")


class TestScanContent:
    def test_detects_bare_except(self):
        code = "try:\n    do_thing()\nexcept:\n    pass"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "error-swallowing" in patterns_found

    def test_detects_empty_js_catch(self):
        code = "try { doThing(); } catch (e) {}"
        findings = watcher.scan_content(code, "test.js")
        patterns_found = [f["pattern"] for f in findings]
        assert "error-swallowing" in patterns_found

    def test_detects_global_mutable_state(self):
        code = "def update():\n    global counter\n    counter += 1"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "shared-mutable-state" in patterns_found

    def test_detects_assert_true(self):
        code = "def test_something():\n    assert True"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "coincidental-correctness" in patterns_found

    def test_detects_sleep_sync(self):
        code = "import time\ntime.sleep(5)\ncheck_result()"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "implicit-ordering" in patterns_found

    def test_detects_mutable_default_arg(self):
        code = "def process(items=[]):\n    items.append(1)\n    return items"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "load-bearing-defaults" in patterns_found

    def test_detects_blanket_type_ignore(self):
        code = "result = weird_func()  # type: ignore"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "invisible-invariants" in patterns_found

    def test_allows_specific_type_ignore(self):
        code = "result = weird_func()  # type: ignore[assignment]"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "invisible-invariants" not in patterns_found

    def test_detects_blanket_noqa(self):
        code = "x = 1  # noqa"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "invisible-invariants" in patterns_found

    def test_allows_specific_noqa(self):
        code = "x = 1  # noqa: E501"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "invisible-invariants" not in patterns_found

    def test_detects_nosec(self):
        code = "password = 'hardcoded'  # nosec"
        findings = watcher.scan_content(code, "test.py")
        patterns_found = [f["pattern"] for f in findings]
        assert "invisible-invariants" in patterns_found

    def test_clean_code_no_findings(self):
        code = "def process(items):\n    return [x * 2 for x in items]"
        findings = watcher.scan_content(code, "test.py")
        assert len(findings) == 0

    def test_high_risk_sorted_first(self):
        code = "except:\n    pass\nassert True\n"
        findings = watcher.scan_content(code, "test.py")
        if len(findings) >= 2:
            assert findings[0]["risk"] == "high"

    def test_go_error_discard(self):
        code = 'result, _ := doSomething("arg")'
        findings = watcher.scan_content(code, "test.go")
        patterns_found = [f["pattern"] for f in findings]
        assert "error-swallowing" in patterns_found


class TestFlagCount:
    def test_starts_at_zero(self, tmp_path, monkeypatch):
        monkeypatch.setattr(watcher, "STATE_FILE", tmp_path / ".count")
        assert watcher.get_flag_count() == 0

    def test_increments(self, tmp_path, monkeypatch):
        state = tmp_path / "shared" / ".count"
        state.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(watcher, "STATE_FILE", state)
        assert watcher.increment_flag_count() == 1
        assert watcher.increment_flag_count() == 2
        assert watcher.get_flag_count() == 2


class TestAppendToWorkspace:
    def test_appends_findings(self, tmp_path, monkeypatch):
        ws = tmp_path / "workspace.md"
        ws.write_text("## build-track\nActive\n", encoding="utf-8")
        monkeypatch.setattr(watcher, "WORKSPACE", ws)

        findings = [{
            "file": "src/auth.py",
            "line": 42,
            "pattern": "error-swallowing",
            "risk": "high",
            "suggestion": "Bare except catches everything",
            "code": "except:",
        }]
        watcher.append_to_workspace(findings)

        content = ws.read_text()
        assert "code-debt-watch" in content
        assert "src/auth.py:42" in content
        assert "error-swallowing" in content

    def test_skips_if_no_workspace(self, tmp_path, monkeypatch):
        ws = tmp_path / "nonexistent" / "workspace.md"
        monkeypatch.setattr(watcher, "WORKSPACE", ws)
        # Should not raise
        watcher.append_to_workspace([{"file": "x", "line": 1, "pattern": "p",
                                       "risk": "high", "suggestion": "s", "code": "c"}])
