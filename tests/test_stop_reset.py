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
from amazon_android.runner import _prepare_phone, RunJob, retry_preparation


class StopResetTests(unittest.TestCase):
    def window(self):
        w=Window.__new__(Window)
        w.cancel=threading.Event(); w.running=True; w.attach_in_progress=False
        w.post_menu_stops={}; w.phone_stop_after_step={}; w.post_menu_resume_after_stop=set()
        w.manual_slots=set(); w.preparation_retry_workers={}
        w.post_menu_sessions={}; w.post_menu_workers={}
        w.post_menu_steps={}; w.menu_opened_at={}; w.phone_serials={}; w.jobs={0:object()}
        w.batch_worker=Mock(is_alive=Mock(return_value=True)); w.attach_worker=None
        w._draining_workers=[]; w._pending_retries=set()
        w._refresh_after_id=None
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
        with patch.object(w,'_launch') as launch, \
             patch.object(w,'_start_preparation_retry') as retry:
            w._continue_profile(0)
        self.assertEqual(w._pending_retries,set())
        retry.assert_called_once_with(0)
        launch.assert_not_called()

    def test_uncreated_profile_continue_creates_during_busy_batch(self):
        w = self.window()
        w.jobs = {0: RunJob(0, 'batch', None)}
        w.registry = Mock()
        w.registry.get.return_value = {'stage': 'RESERVED', 'state': 'ERROR',
                                       'device_id': None}
        w.status = [('focus failed', 'error')]
        with patch.object(w, '_start_profile_creation_retry') as create, \
             patch.object(w, '_launch') as launch:
            w._continue_profile(0)
        self.assertEqual(w._pending_retries, set())
        create.assert_called_once_with(0)
        launch.assert_not_called()

    def test_uncreated_profile_continue_restarts_creation_when_batch_idle(self):
        w = self.window()
        w.running = False
        w.jobs = {0: RunJob(0, 'batch', None)}
        w.registry = Mock()
        w.registry.get.return_value = {'stage': 'RESERVED', 'state': 'ERROR',
                                       'device_id': None}
        w.status = [('focus failed', 'error')]
        with patch.object(w, '_start_profile_creation_retry') as create, \
             patch.object(w, '_launch') as launch:
            w._continue_profile(0)
        create.assert_called_once_with(0)
        launch.assert_not_called()
        self.assertIn(('batch', 0), w.manual_slots)

    def test_queued_phone_continue_starts_manual_preparation(self):
        w = self.window()
        w.jobs = {0: RunJob(0, 'batch', None)}
        w.registry = Mock()
        w.registry.get.return_value = {'name': 'q1', 'stage': 'PROFILE_CONFIRMED',
                                       'state': 'READY', 'device_id': 'device-one'}
        self.assertTrue(w._may_continue(0, 'queued', False))
        with patch.object(w, '_start_preparation_retry') as prepare:
            w._continue_profile(0)
        prepare.assert_called_once_with(0)
        self.assertIn(('batch', 0), w.manual_slots)

    def test_single_row_paste_and_clear_touch_only_selected_failed_machine(self):
        class Cell:
            def __init__(self, value=''):
                self.value = value
            def get(self):
                return self.value
            def set(self, value):
                self.value = value

        w = self.window()
        w.selected = 4
        w.values = [{key: Cell('keep' if index != 4 else 'old')
                     for key in ('host', 'port', 'username', 'proxy_password',
                                 'phone', 'amazon_password', 'full_name', 'card',
                                 'otp_url', 'profile_name')}
                    for index in range(6)]
        w.jobs = {}
        w.otp_codes = ['old'] * 6
        w.otp_status = ['old'] * 6
        w.single_account_line = Mock()
        w.single_account_line.get.return_value = (
            '12025550123 | Example456! | Fifth | | '
            'https://apifc.net/smsrecord?token=fifth')
        w.proxy_line = Mock()
        w._can_edit_locked_row = Mock(return_value=True)
        w._mark_locked_row_dirty = Mock()
        w._apply_single_account_line()
        self.assertEqual(w.values[4]['phone'].get(), '12025550123')
        self.assertEqual(w.values[0]['phone'].get(), 'keep')
        self.assertEqual(w.values[5]['phone'].get(), 'keep')
        w._clear_selected_data()
        self.assertEqual(w.values[4]['phone'].get(), '')
        self.assertEqual(w.values[4]['host'].get(), '')
        self.assertEqual(w.values[4]['profile_name'].get(), 'old')
        self.assertEqual(w.values[0]['host'].get(), 'keep')
        self.assertEqual(w.otp_codes[4], '')
        self.assertEqual(w.otp_codes[0], 'old')

    def test_single_row_paste_accepts_tab_and_csv_with_extra_columns(self):
        class Cell:
            def __init__(self):
                self.value = ''
            def get(self):
                return self.value
            def set(self, value):
                self.value = value

        url = 'https://apifc.net/smsrecord?token=synthetic'
        card = '4000000000000001|12|2030'
        samples = (
            f'12025550123\tExample456!\tFirst\textra\t{card}\t{url}',
            f'12025550123,Example456!,First,extra,{card},{url}',
        )
        for sample in samples:
            with self.subTest(separator='tab' if '\t' in sample else 'csv'):
                w = self.window()
                w.draft.locked = False
                w.selected = 0
                w.jobs = {}
                w.count.get.return_value = '1'
                w.values = [{key: Cell() for key in
                             ('phone', 'amazon_password', 'full_name', 'card', 'otp_url')}]
                w.otp_codes = ['old']
                w.otp_status = ['old']
                w.single_account_line = Mock()
                w.single_account_line.get.return_value = sample
                w._apply_single_account_line()
                self.assertEqual(w.values[0]['card'].get(), card)
                self.assertEqual(w.values[0]['otp_url'].get(), url)
                self.assertEqual(w.otp_codes[0], '')
                self.assertEqual(w.run_note.configure.call_args.kwargs['text'],
                                 'Đã điền hàng Amazon vào Máy 1')

    def test_retry_starts_while_batch_is_busy_and_double_continue_does_not_duplicate(self):
        w = self.window()
        w.registry = Mock()
        w.jobs = {0: RunJob(0, 'batch', None)}
        w.status = [('failed', 'error')]
        entered = threading.Event()
        release = threading.Event()
        def retry(*args, **kwargs):
            entered.set()
            release.wait(3)
        with patch('amazon_android.desktop.retry_preparation', side_effect=retry) as prepare:
            try:
                w._continue_profile(0)
                self.assertTrue(entered.wait(2))
                self.assertTrue(w.running)
                self.assertTrue(w.batch_worker.is_alive())
                w._continue_profile(0)
                self.assertEqual(prepare.call_count, 1)
                self.assertEqual(w._pending_retries, set())
                self.assertEqual(w.status[0][1], 'running')
            finally:
                release.set()
                for worker in getattr(w, 'preparation_retry_workers', {}).values():
                    worker.join(3)

    def test_continue_uses_connected_phone_immediately_without_preparation_queue(self):
        w = self.window()
        w.phone_serials = {0: '127.0.0.1:5001'}
        with patch.object(w, '_start_post_menu') as start, \
             patch.object(w, '_start_preparation_retry') as prepare:
            w._continue_profile(0)
        start.assert_called_once_with(0)
        prepare.assert_not_called()
        self.assertEqual(w._pending_retries, set())

    def test_confirmed_phone_retry_uses_saved_device_without_new_batch(self):
        job = RunJob(2, 'batch', None)
        registry = Mock()
        registry.get.return_value = {'name': 'q3', 'device_id': 'device-three',
                                     'stage': 'APP_INSTALLED', 'state': 'ERROR'}
        emit = Mock(); stop = threading.Event(); selected = threading.Event()
        with patch('amazon_android.runner._prepare_phone', return_value='done') as prepare:
            retry_preparation(job, registry, emit, stop, stop_after_step=selected)
        prepare.assert_called_once_with(job, 'q3', 'device-three', registry,
                                         emit, stop, None, selected)

    def test_manual_retry_starts_offline_confirmed_phone(self):
        job = RunJob(2, 'batch', None)
        registry = Mock()
        registry.get.return_value = {'name': 'q3', 'device_id': 'device-three',
                                     'stage': 'PROFILE_CONFIRMED', 'state': 'READY'}
        with patch('amazon_android.runner.profile_status', return_value={
                'state': 'Offline', 'device_id': 'device-three'}), \
             patch('amazon_android.runner._start_and_confirm', return_value={
                'state': 'Starting', 'device_id': 'device-three'}) as start, \
             patch('amazon_android.runner._prepare_phone', return_value='done') as prepare:
            retry_preparation(job, registry, Mock(), threading.Event(),
                              start_if_offline=True)
        start.assert_called_once()
        prepare.assert_called_once()

    def test_menu_retry_reconnects_without_reinstalling_or_reopening_amazon(self):
        job = RunJob(2, 'batch', None)
        registry = Mock()
        registry.get.return_value = {'name': 'q3', 'device_id': 'device-three',
                                     'stage': 'MENU_OPEN', 'state': 'STOPPED'}
        emit = Mock(); ready = Mock()
        with patch('amazon_android.runner.open_adb_shell', return_value={
                'serial': '127.0.0.1:5003'}) as shell, \
             patch('amazon_android.runner._prepare_phone') as prepare:
            retry_preparation(job, registry, emit, threading.Event(), ready)
        self.assertEqual(shell.call_args.args, ('q3', 'device-three'))
        ready.assert_called_once_with(2, 'q3', 'device-three', '127.0.0.1:5003')
        prepare.assert_not_called()
        self.assertEqual(emit.call_args.args[2], 'done')

    def test_reset_quarantines_retry_worker_and_its_queues(self):
        w = self.window()
        retry_worker = Mock(is_alive=Mock(return_value=True))
        w.preparation_retry_workers = {0: retry_worker}
        old_events = w.events
        w.cancel.set()
        w._reset()
        self.assertIn(retry_worker, w._draining_workers)
        self.assertEqual(w.preparation_retry_workers, {})
        self.assertIsNot(w.events, old_events)

    def test_preparation_guard_blocks_same_phone_but_not_other_phones(self):
        from concurrent.futures import ThreadPoolExecutor
        for second_slot in (0, 1):
            with self.subTest(second_slot=second_slot):
                first = RunJob(0, f'lock-test-{second_slot}', None)
                second = RunJob(second_slot, first.batch_id, None)
                registry = Mock()
                registry.get.return_value = {'name': f'q{second_slot+1}',
                    'device_id': f'device-{second_slot}', 'stage': 'APP_INSTALLED', 'state': 'ERROR'}
                entered = threading.Event(); resumed = threading.Event(); release = threading.Event()
                calls = []
                def prepare(job, *args):
                    calls.append(job.index)
                    if len(calls) == 1:
                        entered.set()
                        release.wait(3)
                    else:
                        resumed.set()
                    return 'done'
                with patch('amazon_android.runner._prepare_phone_locked', side_effect=prepare), \
                     ThreadPoolExecutor(max_workers=2) as pool:
                    old = pool.submit(_prepare_phone, first, 'q1', 'device-0', registry,
                                      Mock(), threading.Event())
                    self.assertTrue(entered.wait(2))
                    retry = pool.submit(retry_preparation, second, registry, Mock(), threading.Event())
                    try:
                        self.assertEqual(resumed.wait(0.2 if second_slot == 0 else 2), second_slot == 1)
                    finally:
                        release.set()
                    self.assertEqual(old.result(3), 'done')
                    self.assertEqual(retry.result(3), 'done')
                self.assertEqual(calls, [0, second_slot])

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

    def test_row_stop_targets_its_machine_without_changing_selection(self):
        w=self.window(); w.jobs={0:object(), 1:object()}; w.selected=0
        w.status=[('running','running'),('running','running')]
        w._request_stop_phone(1)
        self.assertEqual(w.selected,0)
        self.assertFalse(w.cancel.is_set())
        self.assertTrue(w.phone_stop_after_step[1].is_set())
        self.assertNotIn(0,w.phone_stop_after_step)
        self.assertEqual(w.status[0],('running','running'))
        self.assertFalse(w._can_stop_phone(1))
        self.assertTrue(w._can_stop_phone(0))

    def test_menu_only_phone_can_stop_without_resetting_other_phone(self):
        w=self.window(); w.jobs={0:object(), 1:object()}
        w.status=[('q1 đang chạy','running'),
                  ('q2 đã tới menu nhưng thiếu hàng Amazon','menu_only')]
        self.assertTrue(w._can_stop_phone(1))
        w._request_stop_phone(1)
        self.assertEqual(w.status[1][1], 'stopped')
        self.assertTrue(w.phone_stop_after_step[1].is_set())
        self.assertEqual(w.status[0][1], 'running')
        self.assertFalse(w.cancel.is_set())
        self.assertFalse(w._can_stop_phone(1))

    def test_continue_can_queue_while_phone_stop_is_finishing(self):
        w=self.window(); w.status=[('Đang tự động hóa','post_running')]
        w.post_menu_sessions[0]=PostMenuSession('batch',0,'q1',state='RUNNING')
        w._request_stop_phone(0)
        self.assertTrue(w.phone_stop_after_step[0].is_set())
        self.assertTrue(w._may_continue(0,'stop_requested',False))
        w._continue_profile(0)
        self.assertEqual(w.post_menu_resume_after_stop,{0})
        self.assertTrue(w.phone_stop_after_step[0].is_set())
        self.assertEqual(w.status[0][1],'resume_queued')
        self.assertFalse(w._may_continue(0,'resume_queued',False))

    def test_continue_queue_starts_after_stop_event_and_keeps_status(self):
        w=self.window(); w.status=[('Đang tự động hóa','post_running')]
        session=PostMenuSession('batch',0,'q1',state='RUNNING')
        w.post_menu_sessions[0]=session
        w.values=[{'profile_name':Mock()}]
        w.selected=0; w.detail_status=Mock(); w.root=Mock()
        w._request_stop_phone(0)
        w.events.put((0,'bước cũ','post_running','q1'))
        w._poll()
        self.assertEqual(w.status[0][1],'stop_requested')
        w._continue_profile(0)
        session.state='PAUSED'
        w.events.put((0,'Đã dừng riêng q1','post_stopped','q1'))
        with patch.object(w,'_start_post_menu') as start:
            w._poll()
        start.assert_called_once_with(0)
        self.assertEqual(w.status[0][1],'resume_queued')
        self.assertEqual(w.post_menu_resume_after_stop,{0})

    def test_global_stop_cancels_queued_phone_resume(self):
        w=self.window(); w.post_menu_resume_after_stop={0}
        w._request_stop()
        self.assertEqual(w.post_menu_resume_after_stop,set())

    def test_late_stop_event_cannot_mark_resumed_phone_stopped(self):
        w=self.window(); w.status=[('Đang tự động hóa','post_running')]
        w.post_menu_sessions[0]=PostMenuSession('batch',0,'q1',state='RUNNING')
        w.values=[{'profile_name':Mock()}]
        w.selected=0; w.detail_status=Mock(); w.root=Mock()
        w.events.put((0,'Đã dừng riêng q1','post_stopped','q1'))
        w._poll()
        self.assertEqual(w.status[0],('Đang tự động hóa','post_running'))

    def test_row_stop_cancels_only_that_queued_retry(self):
        w=self.window(); w.jobs={0:object(),1:object()}; w.selected=0
        w.status=[('running','running'),('waiting','retry_queued')]
        w._pending_retries={1}
        self.assertTrue(w._can_stop_phone(1))
        w._request_stop_phone(1)
        self.assertEqual(w._pending_retries,set())
        self.assertEqual(w.status[1][1],'stopped')
        self.assertEqual(w.status[0],('running','running'))
        self.assertFalse(w.cancel.is_set())
        self.assertTrue(w.phone_stop_after_step[1].is_set())

    def test_each_table_row_has_its_own_stop_command(self):
        w=Window.__new__(Window)
        w.main=Mock(); w.table_rows=[]; w.table_actions=[]
        w.row_buttons=[]; w.row_stop_buttons=[]
        w._label=Mock(side_effect=lambda *args,**kwargs: Mock())
        w._continue_profile=Mock(); w._request_stop_phone=Mock()
        with patch('amazon_android.desktop.ctk.CTkFrame',side_effect=lambda *args,**kwargs: Mock()), \
             patch('amazon_android.desktop.ctk.CTkFont',return_value=Mock()), \
             patch('amazon_android.desktop.tk.Label',side_effect=lambda *args,**kwargs: Mock()), \
             patch('amazon_android.desktop.ctk.CTkButton',side_effect=lambda *args,**kwargs: Mock()) as make_button:
            w._build_preview_table()
        self.assertEqual(len(w.row_stop_buttons),12)
        stop_calls=[call for call in make_button.call_args_list if call.kwargs.get('text')=='Dừng']
        self.assertEqual(len(stop_calls),12)
        stop_calls[1].kwargs['command']()
        stop_calls[8].kwargs['command']()
        self.assertEqual(w._request_stop_phone.call_args_list,[((1,),{}),((8,),{})])


if __name__=='__main__': unittest.main()
