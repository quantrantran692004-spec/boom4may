import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android import swarmote_desktop as sw, home_menu
from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE


class SharedFallbackTests(unittest.TestCase):
    def test_second_distinct_terminal_group_is_tried_after_first_does_nothing(self):
        first, second = Mock(), Mock()
        first.element_info.control_type = second.element_info.control_type = 'Group'
        first.element_info.runtime_id = (1,)
        second.element_info.runtime_id = (2,)
        labels = [SimpleNamespace(element_info=SimpleNamespace(name='Terminal', control_type='Text'),
                                  parent=lambda group=group: group, is_visible=lambda: True)
                  for group in (first, second)]
        tab = SimpleNamespace(element_info=SimpleNamespace(name='ADB Shell', control_type='TabItem'),
                              is_visible=lambda: True,
                              iface_selection_item=SimpleNamespace(Select=lambda: None))
        on = SimpleNamespace(element_info=SimpleNamespace(name='SHELL: On', control_type='Text'),
                             is_visible=lambda: True)
        port = SimpleNamespace(element_info=SimpleNamespace(name='localhost:5002', control_type='Text'))
        scans = iter([[on, *labels], [*labels], [*labels], [tab, on, port], [tab, on, port], [tab, on, port]])
        with patch.object(sw, '_phone_window', return_value=SimpleNamespace(handle=7)), \
             patch.object(sw, '_descendants', side_effect=lambda _: next(scans)), \
             patch.object(sw, '_wait_for') as wait:
            result = sw.open_adb_shell('q2', 'ACN2', stop=threading.Event())
        self.assertEqual(result['serial'], '127.0.0.1:5002')
        first.invoke.assert_called_once()
        second.invoke.assert_called_once()

    def test_menu_uses_existing_android_reader_when_adb_dump_omits_heading(self):
        phone = CloudPhone('127.0.0.1:5001')
        tab = {'package': AMAZON_PACKAGE, 'content-desc': 'Browse menu Tab',
               'selected': 'true', 'bounds': '[0,0][60,60]'}
        with patch.object(home_menu, '_nodes', return_value=[tab]), \
             patch.object(home_menu, '_confirm_menu_fallback', return_value=True) as fallback, \
             patch.object(home_menu, '_tap') as tap:
            self.assertEqual(home_menu.open_home_menu(phone, timeout=5)['stage'], 'HOME_MENU_OPEN')
        fallback.assert_called()
        tap.assert_not_called()
