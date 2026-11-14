import threading
import unittest
from unittest.mock import patch

from amazon_android.cloud import CloudPhone
from amazon_android.desktop import POST_MENU_STEP_FACTORIES
from amazon_android.post_menu import AttemptDeadline, RegistrationState
from amazon_android.q5_flow import build_q5_steps
from amazon_android import profile_navigation as nav
from amazon_android.runner import RunJob


class Q5FlowTests(unittest.TestCase):
    def test_three_category_taps_use_menu_recovery_and_common_steps(self):
        phone = CloudPhone('127.0.0.1:5005')
        state = RegistrationState()
        steps = build_q5_steps(phone, lambda _: None, registration=state)
        self.assertIs(POST_MENU_STEP_FACTORIES[4], build_q5_steps)
        self.assertEqual([step.name for step in steps[:3]], [
            'b1 Toys, Kids and Baby', 'b2 Office & Professional',
            'b3 Sports & Outdoors'])
        self.assertEqual(steps[3].name, 'b4 Sign In')
        labels = []
        with patch.object(nav, '_read_nodes', return_value=[{'text': 'Shop by category.'}]), \
             patch.object(nav, '_at_or_after', return_value=False), \
             patch.object(nav, '_ensure_menu') as menu, \
             patch.object(nav, '_find_scrolling',
                   side_effect=lambda _phone, label, *_: labels.append(label) or
                   {'bounds': '[1,1][3,3]'}), \
             patch.object(nav, '_tap_for_transition') as tap, \
             patch.object(threading.Event, 'wait', return_value=False):
            for step in steps[:3]:
                step.action(RunJob(4, 'batch', None), AttemptDeadline(None), threading.Event())
        self.assertEqual(labels, ['Toys, Kids and Baby', 'Office & Professional',
                                  'Sports & Outdoors'])
        self.assertEqual(tap.call_count, 3)
        self.assertEqual(menu.call_count, 3)


if __name__ == '__main__':
    unittest.main()
