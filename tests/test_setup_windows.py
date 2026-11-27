import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import setup_windows


class SetupWindowsTests(unittest.TestCase):
    def test_existing_dependencies_do_not_prompt_after_non_dependency_project_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            python = root / ".venv" / "Scripts" / "python.exe"
            python.parent.mkdir(parents=True)
            python.touch()
            (root / "pyproject.toml").write_text("[project]\nname = 'amazon-android-tool'\n")
            old_ready = root / ".venv" / ".swarmote_tool_ready.json"
            old_ready.write_text(json.dumps({"root": str(root), "pyproject_mtime_ns": 0}))
            with patch.object(setup_windows, "ROOT", root), \
                 patch.object(setup_windows, "VENV_PYTHON", python), \
                 patch.object(setup_windows, "READY_FILE", old_ready, create=True), \
                 patch.object(setup_windows, "_installed_project_metadata_matches", return_value=True, create=True), \
                 patch.object(setup_windows, "_runtime_imports_work", return_value=True), \
                 patch("builtins.input", return_value="n") as prompt:
                self.assertTrue(setup_windows._install_python_dependencies())
            prompt.assert_not_called()

    def test_changed_declared_dependencies_still_require_install(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            python = root / ".venv" / "Scripts" / "python.exe"
            python.parent.mkdir(parents=True)
            python.touch()
            project = root / "pyproject.toml"
            project.write_text("[project]\nname = 'amazon-android-tool'\n")
            old_ready = root / ".venv" / ".swarmote_tool_ready.json"
            old_ready.write_text(json.dumps({
                "root": str(root), "pyproject_mtime_ns": project.stat().st_mtime_ns,
            }))
            with patch.object(setup_windows, "ROOT", root), \
                 patch.object(setup_windows, "VENV_PYTHON", python), \
                 patch.object(setup_windows, "READY_FILE", old_ready, create=True), \
                 patch.object(setup_windows, "_installed_project_metadata_matches", return_value=False, create=True), \
                 patch.object(setup_windows, "_runtime_imports_work", return_value=True), \
                 patch("builtins.input", return_value="n"):
                self.assertFalse(setup_windows._install_python_dependencies())


if __name__ == "__main__":
    unittest.main()
