import threading
import unittest
from unittest.mock import patch
from amazon_android.post_menu import PostMenuSession, PostMenuStep, RecoverableStepError
from amazon_android.runner import RunJob


class SharedStepRecoveryTests(unittest.TestCase):
    def test_early_navigation_and_focus_retry_after_read_failure(self):
        for name in ('b1 Gifting', 'b4a chạm ô SĐT', 'b9 nhập tên'):
            with self.subTest(name=name):
                attempts = []
                def action(*args):
                    attempts.append(1)
                    if len(attempts) == 1:
                        raise RecoverableStepError('đọc màn tạm lỗi')
                session = PostMenuSession('batch', 0, 'q1')
                session.run(RunJob(0, 'batch', None), (PostMenuStep(name, action),),
                            lambda *e: None, threading.Event())
                self.assertEqual((session.state, len(attempts)), ('DONE', 2))

    def test_b4_self_recovers_temporary_recognition_failure(self):
        attempts = []
        events = []
        def action(job, deadline, stop):
            attempts.append(job.index)
            if len(attempts) == 1:
                raise RecoverableStepError('UI chưa ổn định')
        session = PostMenuSession('batch', 0, 'q1')
        session.run(RunJob(0, 'batch', None),
                    (PostMenuStep('b4 Sign In', action),),
                    lambda *e: events.append(e), threading.Event())
        self.assertEqual(attempts, [0, 0])
        self.assertEqual(session.state, 'DONE')
        self.assertIn('post_running', [e[2] for e in events])

    def test_b10_never_auto_replays_uncertain_send(self):
        attempts = []
        session = PostMenuSession('batch', 0, 'q1')
        def action(*args):
            attempts.append(1)
            raise RecoverableStepError('SMS không chắc chắn')
        session.run(RunJob(0, 'batch', None),
                    (PostMenuStep('b10 Send code by SMS', action),),
                    lambda *e: None, threading.Event())
        self.assertEqual(attempts, [1])
        self.assertEqual(session.state, 'PAUSED')

    def test_recoverable_read_error_waits_and_retries_same_step_until_success(self):
        attempts = []
        session = PostMenuSession('batch', 0, 'q1')
        def action(*args):
            attempts.append(1)
            if len(attempts) < 5:
                raise RecoverableStepError('Android đang tải')
        with patch('amazon_android.post_menu.time.sleep'), \
             patch('amazon_android.post_menu.threading.Event.wait', return_value=False):
            session.run(RunJob(0, 'batch', None),
                        (PostMenuStep('b5 nhập SĐT', action),),
                        lambda *_: None, threading.Event())
        self.assertEqual((session.state, len(attempts)), ('DONE', 5))

    def test_unknown_transient_error_keeps_step_running_for_same_step_retry(self):
        attempts = []
        session = PostMenuSession('batch', 0, 'q1')
        def action(*args):
            attempts.append(1)
            if len(attempts) < 3:
                raise RuntimeError('temporary provider fault')
        with patch('amazon_android.post_menu.threading.Event.wait', return_value=False):
            session.run(RunJob(0, 'batch', None),
                        (PostMenuStep('b8 Proceed', action),),
                        lambda *_: None, threading.Event())
        self.assertEqual((session.state, len(attempts)), ('DONE', 3))
