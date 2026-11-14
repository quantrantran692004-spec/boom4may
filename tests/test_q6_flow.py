import threading
import unittest
from unittest.mock import patch

from amazon_android.account_flow import route_list_menu
from amazon_android.cloud import CloudPhone
from amazon_android.desktop import POST_MENU_STEP_FACTORIES
from amazon_android.random_prefix import build_random_steps
from amazon_android.post_menu import AttemptDeadline, PostMenuSession
from amazon_android.q1_flow import build_q1_steps
from amazon_android.q6_flow import build_q6_steps
from amazon_android.runner import RunJob


class Q6FlowTests(unittest.TestCase):
    def test_prefix_has_home_cart_menu_card_then_unchanged_common_steps(self):
        phone = CloudPhone('127.0.0.1:5006')
        q6 = build_q6_steps(phone, lambda _: None)
        q1 = build_q1_steps(phone, lambda _: None)
        self.assertIs(POST_MENU_STEP_FACTORIES[5], build_random_steps)
        self.assertEqual([step.name for step in q6[:3]], [
            'b1 Trang chủ 2 giây', 'b2 Giỏ hàng 2 giây',
            'b3 Menu · b3a Electronics'])
        self.assertEqual([(step.name, step.action.__code__) for step in q6[3:]],
                         [(step.name, step.action.__code__) for step in q1[3:]])

    def test_b3a_uses_card_or_list_label_then_b4_can_recover_menu(self):
        phone = CloudPhone('127.0.0.1:5006')
        action = build_q6_steps(phone, lambda _: None)[2].action
        labels = []
        for layout, expected in [('CARDS', 'Devices and Electronics'),
                                 ('LIST', 'Electronics')]:
            with patch('amazon_android.q6_flow._read_nodes', return_value=[]), \
                 patch('amazon_android.q6_flow._at_or_after', return_value=False), \
                 patch('amazon_android.q6_flow._ensure_menu', return_value=[]), \
                 patch('amazon_android.q6_flow.menu_layout', return_value=layout), \
                 patch('amazon_android.q6_flow._find_scrolling',
                       side_effect=lambda _p, label, *_: labels.append(label) or
                       {'bounds': '[1,1][3,3]'}), \
                 patch('amazon_android.q6_flow._tap_for_transition') as tap, \
                 patch.object(threading.Event, 'wait', return_value=False):
                action(RunJob(5, 'batch', None), AttemptDeadline(None), threading.Event())
                tap.assert_called_once()
            self.assertEqual(labels[-1], expected)

    def test_list_menu_does_not_skip_q6_prefix(self):
        phone = CloudPhone('127.0.0.1:5006')
        steps = build_q6_steps(phone, lambda _: None)
        session = PostMenuSession('batch', 5, 'q6')
        self.assertIsNone(route_list_menu(phone, steps, 0, session,
                                          AttemptDeadline(None), threading.Event()))


if __name__ == '__main__':
    unittest.main()
