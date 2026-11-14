import threading
import unittest
from unittest.mock import patch

from amazon_android import account_flow as flow
from amazon_android.cloud import CloudPhone
from amazon_android.post_menu import AttemptDeadline


class MenuReturnTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5003')
        self.stop = threading.Event()
        self.deadline = AttemptDeadline(None)

    def test_already_on_menu_does_not_tap_or_go_back(self):
        menu = [{'text': 'MENU'}]
        with patch.object(flow, '_read_nodes', return_value=menu), \
             patch.object(flow, 'screen', return_value='MENU'), \
             patch.object(flow, '_tap_for_transition') as tap, \
             patch.object(flow, 'cloud_adb') as adb:
            self.assertIs(flow._ensure_menu(self.phone, self.deadline, self.stop), menu)
        tap.assert_not_called()
        adb.assert_not_called()

    def test_category_back_to_home_then_browse_menu(self):
        category = [{'text': 'CATEGORY'}]
        home = [{'text': 'HOME'}, {'content-desc': 'Browse menu Tab',
                                  'bounds': '[1,1][50,50]'}]
        menu = [{'text': 'MENU'}]
        reads = iter([category, home, home, home, home, menu])
        with patch.object(flow, '_read_nodes', side_effect=lambda *_: next(reads)), \
             patch.object(flow, 'screen', side_effect=lambda nodes: nodes[0]['text']), \
             patch.object(flow, '_at_or_after', return_value=False), \
             patch.object(flow, '_tap_for_transition') as tap, \
             patch.object(flow, 'cloud_adb') as adb, \
             patch.object(self.stop, 'wait', return_value=False):
            self.assertIs(flow._ensure_menu(self.phone, self.deadline, self.stop), menu)
        adb.assert_called_once()
        tap.assert_called_once()
        self.assertEqual(tap.call_args.args[1]['content-desc'], 'Browse menu Tab')


if __name__ == '__main__':
    unittest.main()
