import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from amazon_android.otp import browser_launch_options


class PackagedBrowserTests(unittest.TestCase):
    def test_source_checkout_keeps_requested_channel(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(browser_launch_options('chrome'), {'channel': 'chrome'})

    def test_package_uses_existing_bundled_browser(self):
        with tempfile.TemporaryDirectory() as directory:
            browser = Path(directory) / 'chrome.exe'
            browser.touch()
            with patch.dict(os.environ, {'SWARMOTE_BUNDLED_BROWSER': str(browser)}):
                self.assertEqual(browser_launch_options('chrome'), {'executable_path': str(browser)})
                browser.unlink()
                self.assertEqual(browser_launch_options('chrome'), {'channel': 'chrome'})
