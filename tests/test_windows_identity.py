import unittest
from unittest.mock import patch, Mock
from PIL import Image
from amazon_android import windows_identity as identity


class WindowsIdentityTests(unittest.TestCase):
    def test_taskbar_icon_is_square_and_visible_at_small_sizes(self):
        icon_path = identity.ROOT / 'amazon_android' / 'assets' / 'swarmote_tool.ico'
        with Image.open(icon_path) as icon:
            self.assertTrue({(16, 16), (32, 32), (48, 48)}.issubset(icon.info['sizes']))
            small = icon.ico.getimage((16, 16)).convert('RGBA')
        self.assertEqual(small.getpixel((0, 0))[3], 255)

    def test_tk_window_receives_project_icon(self):
        root = Mock()
        with patch.object(identity.sys, 'platform', 'win32'):
            identity.set_tk_icon(root)
        root.iconbitmap.assert_called_once_with(str(
            identity.ROOT / 'amazon_android' / 'assets' / 'swarmote_tool.ico'))

    def test_relaunch_command_opens_workspace_module_with_project_runtime(self):
        command = identity.relaunch_command()
        self.assertIn('pythonw.exe', command)
        self.assertIn('-m amazon_android.desktop', command)
        self.assertNotIn('idlelib', command)

    def test_relaunch_properties_are_written_before_identity_refresh(self):
        from win32com.propsys import propsys, pscon
        store = Mock()
        with patch.object(propsys, 'SHGetPropertyStoreForWindow', return_value=store), \
             patch('win32gui.GetAncestor', return_value=99):
            identity.set_window_identity(42)
        keys = [call.args[0] for call in store.SetValue.call_args_list]
        self.assertEqual(keys[-1], pscon.PKEY_AppUserModel_ID)
        self.assertIn(pscon.PKEY_AppUserModel_RelaunchCommand, keys[:-1])
        self.assertIn(pscon.PKEY_AppUserModel_RelaunchDisplayNameResource, keys[:-1])
        store.Commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
