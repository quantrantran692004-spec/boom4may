import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android import swarmote_desktop as sw, home_menu
from amazon_android.cloud import CloudPhone
from amazon_android.core import AMAZON_PACKAGE
from amazon_android.core import ToolError
from subprocess import TimeoutExpired


class ParallelNavigationRegressionTests(unittest.TestCase):
    def test_duplicate_terminal_labels_for_one_group_open_shell_once(self):
        group = Mock()
        group.element_info.control_type = 'Group'
        group.element_info.runtime_id = (1, 2, 3)
        labels = [SimpleNamespace(element_info=SimpleNamespace(name='Terminal', control_type='Text'),
                                  parent=lambda: group, is_visible=lambda: True) for _ in range(2)]
        tab = SimpleNamespace(element_info=SimpleNamespace(name='ADB Shell', control_type='TabItem'),
                              is_visible=lambda: True,
                              iface_selection_item=SimpleNamespace(Select=lambda: None))
        shell_on = SimpleNamespace(element_info=SimpleNamespace(name='SHELL: On', control_type='Text'),
                                   is_visible=lambda: True)
        port = SimpleNamespace(element_info=SimpleNamespace(name='localhost:5001', control_type='Text'))
        window = SimpleNamespace(handle=5)
        with patch.object(sw, '_phone_window', return_value=window), \
             patch.object(sw, '_descendants', side_effect=[[shell_on, *labels], [*labels],
                                                             [tab, shell_on, port], [tab, shell_on, port],
                                                             [tab, shell_on, port]]), \
             patch.object(sw, '_wait_for'):
            result = sw.open_adb_shell('q1', 'ACN1', stop=threading.Event())
        self.assertEqual(result['serial'], '127.0.0.1:5001')
        group.invoke.assert_called_once()

    def test_menu_tab_may_be_retried_after_confirmed_unselected_state(self):
        phone = CloudPhone('127.0.0.1:5001')
        tab = {'package': AMAZON_PACKAGE, 'content-desc': 'Browse menu Tab',
               'selected': 'false', 'bounds': '[0,0][60,60]'}
        menu = {'package': AMAZON_PACKAGE, 'text': 'Shop by category.'}
        with patch.object(home_menu, '_nodes', side_effect=[[tab], [tab], [tab], [menu]]), \
             patch.object(home_menu, '_tap') as tap, \
             patch.object(home_menu.time, 'sleep'):
            result = home_menu.open_home_menu(phone, timeout=5)
        self.assertEqual(result['stage'], 'HOME_MENU_OPEN')
        self.assertEqual(tap.call_count, 2)

    def test_category_cards_confirm_menu_when_heading_is_missing(self):
        phone = CloudPhone('127.0.0.1:5001')
        nodes = [{'package': AMAZON_PACKAGE, 'text': item} for item in
                 ('Gifting', 'Pets', 'Fashion and Beauty')]
        with patch.object(home_menu, '_nodes', return_value=nodes), \
             patch.object(home_menu, '_tap') as tap:
            self.assertEqual(home_menu.open_home_menu(phone, timeout=2)['stage'], 'HOME_MENU_OPEN')
        tap.assert_not_called()

    def test_menu_tap_timeout_reads_result_before_trying_again(self):
        phone = CloudPhone('127.0.0.1:5001')
        tab = {'package': AMAZON_PACKAGE, 'content-desc': 'Browse menu Tab',
               'selected': 'false', 'bounds': '[0,0][60,60]'}
        heading = {'package': AMAZON_PACKAGE, 'text': 'Shop by category'}
        timeout = ToolError('ADB timed out')
        timeout.__cause__ = TimeoutExpired('adb', 5)
        with patch.object(home_menu, '_nodes', side_effect=[[tab], [heading]]), \
             patch.object(home_menu, '_tap', side_effect=timeout) as tap, \
             patch.object(home_menu.time, 'sleep'):
            result = home_menu.open_home_menu(phone, timeout=5)
        self.assertEqual(result['stage'], 'HOME_MENU_OPEN')
        tap.assert_called_once()
