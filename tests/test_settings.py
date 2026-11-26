import tempfile
import unittest
from pathlib import Path

from amazon_android.core import ToolError
from amazon_android.settings import AppSettings, load_settings, save_settings


class SettingsTests(unittest.TestCase):
    def test_setting_persists_across_sessions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            self.assertEqual(load_settings(path).start_group_size, 1)
            self.assertFalse(load_settings(path).hide_profile_creation)
            self.assertEqual(load_settings(path).account_flow_mode, "create")
            self.assertEqual(load_settings(path).login_followup, "none")
            save_settings(AppSettings(12, True, "login"), path)
            self.assertEqual(load_settings(path), AppSettings(12, True, "login"))
            for choice in ("address_and_card", "card_only"):
                selected = AppSettings(2, False, "login", choice)
                save_settings(selected, path)
                self.assertEqual(load_settings(path), selected)

    def test_old_settings_file_keeps_creation_window_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text('{"start_group_size": 2}', encoding="utf-8")
            self.assertEqual(load_settings(path), AppSettings(2, False))

    def test_setting_requires_one_to_twelve(self):
        for value in (0, 13):
            with self.assertRaises(ToolError):
                AppSettings(value)
        with self.assertRaises(ToolError):
            AppSettings(2, "yes")
        with self.assertRaises(ToolError):
            AppSettings(2, False, "both")
        with self.assertRaises(ToolError):
            AppSettings(2, False, "login", "both")
        with self.assertRaises(ToolError):
            AppSettings(2, False, "login", ["card_only"])
        with self.assertRaises(ToolError):
            AppSettings(2, False, "create", "card_only")


if __name__ == "__main__":
    unittest.main()
