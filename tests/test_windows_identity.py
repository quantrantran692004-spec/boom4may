import unittest
from unittest.mock import patch, Mock
from amazon_android import windows_identity as identity


class WindowsIdentityTests(unittest.TestCase):
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
