import unittest
from pathlib import Path
from unittest.mock import patch

from amazon_android import launcher


class LauncherTests(unittest.TestCase):
    def test_standard_shortcut_uses_project_runtime_with_installed_ocr(self):
        with patch.object(Path, "is_file", return_value=True), \
             patch.object(launcher.sys, "executable", "C:/other/pythonw.exe"), \
             patch.object(launcher.subprocess, "Popen") as launch:
            launcher.main()
        command = launch.call_args.args[0]
        self.assertEqual(Path(command[0]).parent.name, "Scripts")
        self.assertEqual(Path(command[0]).parent.parent.name, ".venv")
        self.assertEqual(command[1:], ["-m", "amazon_android.desktop"])

    def test_runtime_does_not_relaunch_itself_or_reset_existing_session(self):
        runtime = Path(launcher.__file__).resolve().parent.parent / ".venv" / "Scripts" / "pythonw.exe"
        with patch.object(Path, "is_file", return_value=True), \
             patch.object(launcher.sys, "executable", str(runtime)), \
             patch("amazon_android.desktop.main") as desktop, \
             patch.object(launcher.subprocess, "Popen") as launch:
            launcher.main()
        desktop.assert_called_once()
        launch.assert_not_called()
