from worker_helpers import on_worker
import queue
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android.desktop import Window
from amazon_android.batch_state import BatchDraft
from amazon_android.core import ToolError
from amazon_android.post_menu import PostMenuSession
from amazon_android.runner import _prepare_phone, RunJob


class StopResetTests(unittest.TestCase):
    def window(self):
        w=Window.__new__(Window)
        w.cancel=threading.Event(); w.running=True; w.attach_in_progress=False
        w.post_menu_stops={}; w.phone_stop_after_step={}; w.post_menu_sessions={}; w.post_menu_workers={}
        w.post_menu_steps={}; w.menu_opened_at={}; w.phone_serials={}; w.jobs={0:object()}
        w.batch_worker=Mock(is_alive=Mock(return_value=True)); w.attach_worker=None
        w._draining_workers=[]; w._pending_retries=set()
        w.registry=None; w.draft=BatchDraft(); w.draft.locked=True
        w.events=queue.Queue(); w.otp_events=queue.Queue(); w.otp_status_events=queue.Queue(); w.attach_events=queue.Queue()
        w.values=[]; w.proxy_fallbacks=[]; w.bulk_boxes={}
        w.bulk_feedback={key:Mock() for key in ('proxy','account')}
        w.count=Mock(); w.run_note=Mock(); w._select=Mock(); w._set_editing=Mock(); w._refresh_devices=Mock()
        return w

    def test_reset_after_stop_opens_new_draft_and_quarantines_old_queue(self):
        w=self.window(); old_events=w.events; old_serials=w.phone_serials; old_stop=w.cancel
        w.cancel.set()
        w._reset()
        self.assertFalse(w.draft.locked)
        self.assertFalse(w.running)
        self.assertFalse(w.cancel.is_set()); self.assertTrue(old_stop.is_set())
        self.assertIsNot(w.events,old_events); self.assertIsNot(w.phone_serials,old_serials)
        self.assertTrue(w._previous_work_busy())
        w._set_editing.assert_called_with(True)

    def test_reset_discards_only_ram_state_of_q7_pilot(self):
        w=self.window()
        session=PostMenuSession('batch',6,'q7')
        session.registration.prefix_completed.update({1,2,3})
        session.registration.q7_prefix_started_at[2]=1.0
        w.post_menu_sessions[6]=session
        w.cancel.set(); w._reset()
        self.assertEqual(w.post_menu_sessions,{})
        self.assertEqual(w.post_menu_steps,{})
        self.assertEqual(session.registration.prefix_completed,{1,2,3})

    def test_reset_without_stop_does_not_clear_running_job(self):
        w=self.window(); old_jobs=w.jobs
        w._reset()
        self.assertIs(w.jobs,old_jobs)
        w._set_editing.assert_not_called()

    def test_failed_row_can_request_retry_while_another_machine_is_running(self):
        w=self.window(); w.status=[('failed','error')]
        self.assertTrue(w._may_continue(0,'error',False))
        with patch.object(w,'_launch') as launch:
            w._continue_profile(0)
        self.assertEqual(w._pending_retries,{0})
        launch.assert_not_called()

    def test_stopped_install_is_reported_stopped_instead_of_error(self):
        stop=threading.Event(); registry=Mock(); registry.get.return_value={'stage':'STARTED'}
        events=[]
        def install(*args,**kwargs):
            self.assertIs(kwargs['stop'],stop); stop.set(); raise ToolError('stopped')
        with patch('amazon_android.runner.install_amazon',side_effect=install), \
             patch('amazon_android.runner.open_adb_shell') as shell:
            outcome=on_worker(_prepare_phone, RunJob(0,'batch',None),'q1','device',registry,
                                   lambda *e:events.append(e),stop)
        self.assertEqual(outcome,'stopped')
        self.assertEqual(events[-1][2],'stopped')
        shell.assert_not_called()

    def test_selected_stop_finishes_install_before_stopping_that_phone(self):
        stop=threading.Event(); selected_stop=threading.Event()
        registry=Mock(); registry.get.return_value={'stage':'STARTED'}
        events=[]

        def install(*args,**kwargs):
            self.assertFalse(stop.is_set())
            selected_stop.set()

        with patch('amazon_android.runner.install_amazon',side_effect=install), \
             patch('amazon_android.runner.open_adb_shell') as shell:
            outcome=on_worker(_prepare_phone, RunJob(0,'batch',None),'q1','device',registry,
                              lambda *event:events.append(event),stop,
                              stop_after_step=selected_stop)
        self.assertEqual(outcome,'stopped')
        self.assertFalse(stop.is_set())
        self.assertEqual(events[-1][2],'stopped')
        shell.assert_not_called()

    def test_canceled_wait_exits_before_reading_ui(self):
        from amazon_android.swarmote_desktop import _wait_for
        stop=threading.Event(); stop.set()
        with patch('amazon_android.swarmote_desktop._descendants') as read:
            with self.assertRaises(ToolError):
                _wait_for(object(),'Amazon Shopping','Text',60,stop=stop)
        read.assert_not_called()

    def test_late_batch_result_does_not_write_serial_or_events_into_new_draft(self):
        w=self.window(); old_events=w.events; old_serials=w.phone_serials; old_stop=w.cancel
        context={'registry':w.registry,'events':old_events,'serials':old_serials,
                 'opened':w.menu_opened_at,'stop':old_stop,'group':1,'hide':False}
        w.cancel.set(); w._reset()

        def old_batch(jobs,registry,emit,stop,**kwargs):
            self.assertIs(stop,old_stop)
            kwargs['menu_ready'](0,'q1','device','127.0.0.1:5001')
            emit(0,'old done','done','q1')
            return {'menu_open':1,'error':0,'stopped':0}

        with patch('amazon_android.desktop.run_batch',side_effect=old_batch):
            on_worker(w._run, [RunJob(0,'old',None)],context)
        self.assertEqual(old_serials,{0:'127.0.0.1:5001'})
        self.assertEqual(w.phone_serials,{})
        self.assertFalse(old_events.empty()); self.assertTrue(w.events.empty())

    def test_new_batch_cannot_start_while_old_worker_is_draining(self):
        w=self.window(); w.cancel.set(); w._reset()
        with patch('amazon_android.desktop.threading.Thread') as thread:
            w._launch([0])
        thread.assert_not_called()

    def test_pending_retry_is_removed_by_stop(self):
        w=self.window(); w._pending_retries={0,1}
        w._request_stop()
        self.assertEqual(w._pending_retries,set())
        self.assertTrue(w.cancel.is_set())

    def test_selected_stop_keeps_other_phone_running(self):
        w=self.window(); w.jobs={0:object(), 1:object()}; w.selected=1
        w.status=[('running','running'),('running','running')]
        w._pending_retries={1}
        w._request_stop_selected()
        self.assertFalse(w.cancel.is_set())
        self.assertTrue(w.phone_stop_after_step[1].is_set())
        self.assertNotIn(0,w.phone_stop_after_step)
        self.assertEqual(w._pending_retries,set())
        self.assertEqual(w.status[0],('running','running'))


if __name__=='__main__': unittest.main()
