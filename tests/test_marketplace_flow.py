import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from amazon_android import marketplace_flow as flow
from amazon_android.account_flow import screen
from amazon_android.cloud import CloudPhone
from amazon_android.core import ToolError
from amazon_android.desktop import POST_MENU_STEP_FACTORIES
from amazon_android.post_menu import AttemptDeadline, PostMenuSession, RegistrationState
from amazon_android.runner import RunJob


def node(text='', bounds='[20,100][380,140]', **attrs):
    return dict({'text': text, 'bounds': bounds}, **attrs)


TAB = node(**{'content-desc': 'Your Account Tab, 2 of 4'}, bounds='[110,810][190,860]')
FOREGROUND_CHECK = flow._foreground
BROWSE = node(**{'content-desc': 'Browse menu Tab, 4 of 4'}, bounds='[310,810][390,860]')
ACCOUNT = [node('Your Orders'), node('Orders'), node('Account'), node('Lists'),
           node('EN', '[350,100][390,125]'), TAB, BROWSE]
TOP = [node('Countries/Regions available in English'), node('Australia'), node('Canada')]
BOTTOM = [node('Countries/Regions available in English'),
          node('United Kingdom', '[50,340][260,380]'),
          node('United States', '[50,410][260,450]'),
          node('Japan (日本)', '[50,480][260,520]')]


def settings(country):
    return [node('Country/Region & Language', '[20,110][350,140]'),
            node('Country/Region:', '[50,240][180,260]'),
            node(country, '[50,263][190,285]'),
            node('Language:', '[50,340][140,360]'),
            node('English', '[50,363][190,385]'),
            node('United States - English', '[50,540][300,565]'),
            node('Done', '[30,690][380,740]'), TAB]


class MarketplaceFlowTests(unittest.TestCase):
    def setUp(self):
        self.phone = CloudPhone('127.0.0.1:5001')
        self.stop = threading.Event()
        text_reader = patch.object(
            flow, '_read_text_region',
            side_effect=lambda phone, deadline, stop, crop:
                flow._read(phone, deadline, stop, visual=True))
        text_reader.start(); self.addCleanup(text_reader.stop)
        self.clock = [100.0]
        ticker = patch.object(flow.time, 'monotonic', side_effect=lambda: self.clock[0])
        ticker.start(); self.addCleanup(ticker.stop)
        self.waiter = patch.object(flow, '_pause', side_effect=self.wait)
        self.waiter.start(); self.addCleanup(self.waiter.stop)
        fg = patch.object(flow, '_foreground')
        self.foreground = fg.start(); self.addCleanup(fg.stop)

    def wait(self, stop, seconds):
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        self.clock[0] += seconds

    def state(self):
        return RegistrationState(tail_completed={12, 13, 14, 15})

    def action(self, number, state):
        return flow.build_marketplace_steps(self.phone, state)[number-16].action

    def test_settings_previously_visited_us_is_not_selected_country(self):
        self.assertFalse(flow._us_selected(settings('Singapore')))
        self.assertTrue(flow._us_selected(settings('United States')))
        self.assertEqual(screen(settings('Singapore')), 'MARKET_SETTINGS')
        self.assertEqual(screen(TOP), 'MARKET_COUNTRIES')
        self.assertEqual(screen(BOTTOM), 'MARKET_COUNTRIES')
        self.assertEqual(screen(ACCOUNT), 'ACCOUNT')

    def test_b17_taps_visible_en_without_account_screen_conditions(self):
        state = self.state(); state.marketplace_completed.add(16)
        en = node('EN', '[372,103][400,122]', vision='true')
        with patch.object(flow, '_read_text_region', return_value=[en]) as read, \
             patch.object(flow, '_read', side_effect=AssertionError('full-screen read')), \
             patch.object(flow, '_tap_for_transition') as tap:
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        read.assert_called_once()
        tap.assert_called_once()
        self.assertIs(tap.call_args.args[1], en)
        self.assertIn(17, state.marketplace_completed)

    def test_all_twelve_factories_and_both_modes_run_shared_b16_to_b22(self):
        for mode in ('create', 'login'):
            for index, factory in POST_MENU_STEP_FACTORIES.items():
                with self.subTest(mode=mode, slot=index+1):
                    phone = CloudPhone(f'127.0.0.1:{5001+index}')
                    state = self.state(); state.flow_mode = mode
                    stages = ['page']; loading = [0]; taps = []; swipes = []
                    def read(active_phone, *_args, **_kwargs):
                        self.assertEqual(active_phone.serial, phone.serial)
                        stage = stages[0]
                        if stage == 'loading':
                            loading[0] += 1
                            if loading[0] < 3:
                                return []
                            stages[0] = 'page'
                            return [TAB, BROWSE]
                        return {'page': [TAB, BROWSE], 'account': ACCOUNT,
                                'settings': settings('Singapore'), 'top': TOP,
                                'bottom': BOTTOM, 'us': settings('United States')}[stage]
                    def tap(active_phone, target, *_args):
                        self.assertEqual(active_phone.serial, phone.serial)
                        label = target.get('text') or target.get('content-desc')
                        taps.append(label)
                        if target is TAB:
                            stages[0] = 'account'
                        elif label == 'EN':
                            stages[0] = 'settings'
                        elif label == 'Country/Region:':
                            stages[0] = 'top'
                        elif label == 'United States':
                            stages[0] = 'us'
                        elif label == 'Done':
                            stages[0] = 'loading'
                    def adb(active_phone, *args, **kwargs):
                        self.assertEqual(active_phone.serial, phone.serial)
                        if args[:3] == ('shell', 'input', 'swipe'):
                            swipes.append(args); stages[0] = 'bottom'
                        return SimpleNamespace(stdout='Physical size: 420x910')
                    steps = factory(phone, lambda _: None, registration=state)
                    start = next(i for i,s in enumerate(steps) if s.name.startswith('b16 '))
                    session = PostMenuSession('market-test', index, f'q{index+1}',
                                               next_step=start, registration=state)
                    with patch.object(flow, '_read', side_effect=read), \
                         patch.object(flow, '_tap_for_transition', side_effect=tap), \
                         patch.object(flow, 'cloud_adb', side_effect=adb):
                        session.run(RunJob(index, 'market-test', None), steps[:start+7],
                                    lambda *_: None, self.stop)
                    self.assertEqual(session.state, 'DONE', session.last_error)
                    self.assertEqual(state.marketplace_completed, set(range(16,23)))
                    self.assertTrue(state.marketplace_done_confirmed)
                    self.assertEqual(taps.count('Done'), 1)
                    self.assertEqual(taps.count('Your Account Tab, 2 of 4'), 2)
                    self.assertEqual(len(swipes), 1)
                    self.assertGreater(int(swipes[0][4]), int(swipes[0][6]))

    def test_b17_uses_ocr_when_native_account_tree_hides_locale_button(self):
        state = self.state(); state.marketplace_completed.add(16)
        tapped = []
        native = [n for n in ACCOUNT if n.get('text') != 'EN']
        def read(*args, **kwargs):
            if tapped:
                return settings('Singapore')
            return ACCOUNT if kwargs.get('visual') else native
        with patch.object(flow, '_read', side_effect=read) as reader, \
             patch.object(flow, '_tap_for_transition', side_effect=lambda *args: tapped.append(args[1])):
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(tapped[0]['text'], 'EN')
        self.assertTrue(any(c.kwargs.get('visual') for c in reader.call_args_list))

    def test_b17_taps_visible_locale_on_unrecognized_account_layout(self):
        state = self.state(); state.marketplace_completed.add(16)
        locale = node('EN', '[338,75][370,110]')
        unknown_layout = [node('Hello, customer', '[20,75][160,110]'), locale]
        tapped = []
        def read(*args, **kwargs):
            return settings('Singapore') if tapped else unknown_layout
        with patch.object(flow, '_read', side_effect=read) as reader, \
             patch.object(flow, '_tap_for_transition', side_effect=lambda *args: tapped.append(args[1])), \
             patch.object(flow, 'cloud_adb') as adb:
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        self.assertIs(tapped[0], locale)
        self.assertTrue(reader.call_args_list[0].kwargs.get('visual'))
        self.assertEqual(reader.call_count, 1)
        adb.assert_not_called()

    def test_b17_reads_en_from_image_before_reopening_account_tab(self):
        state = self.state(); state.marketplace_completed.add(16)
        native = [TAB, BROWSE, node('Loading', '[20,200][130,230]')]
        visual = [node('EN', '[373,101][401,124]'),
                  node('Your Orders', '[12,202][134,228]')]
        taps = []
        def read(*args, **kwargs):
            if taps:
                return settings('Singapore')
            return visual if kwargs.get('visual') else native
        with patch.object(flow, '_read', side_effect=read) as reader, \
             patch.object(flow, '_tap_for_transition',
                          side_effect=lambda _phone, target, _deadline: taps.append(target)), \
             patch.object(flow, 'cloud_adb') as adb:
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        self.assertIs(taps[0], visual[0])
        self.assertTrue(any(call.kwargs.get('visual') for call in reader.call_args_list))
        adb.assert_not_called()

    def test_missing_target_fallback_backs_then_uses_fresh_locale_text_on_all_modes_and_slots(self):
        broken = [n for n in ACCOUNT if n.get('text') != 'EN']
        label = node('Country and language', '[70,300][330,350]')
        alternate = [node('Different account layout'),label]
        self.assertEqual(screen(alternate),'UNKNOWN')
        for mode in ('create','login'):
            for index,factory in POST_MENU_STEP_FACTORIES.items():
                with self.subTest(mode=mode,slot=index+1):
                    state = self.state(); state.flow_mode = mode
                    state.marketplace_completed.add(16)
                    state.tail_choices = {13:'dogs',14:'cats',15:'pets'}
                    phone = CloudPhone(f'127.0.0.1:{5001+index}')
                    stage = ['broken']; actions = []; screenshot_after_back = []
                    def read(active_phone,*_args,**kwargs):
                        self.assertEqual(active_phone,phone)
                        if stage[0]=='alternate':
                            self.assertTrue(kwargs.get('visual'))
                            screenshot_after_back.append(True)
                            return alternate
                        return settings('Singapore') if stage[0]=='settings' else broken
                    def back(active_phone,*args,**_kwargs):
                        self.assertEqual(active_phone,phone)
                        self.assertEqual(args,('shell','input','keyevent','KEYCODE_BACK'))
                        actions.append('back'); stage[0]='alternate'
                    def tap(active_phone,target,*_args):
                        self.assertEqual(active_phone,phone)
                        self.assertIs(target,label)
                        self.assertEqual(actions,['back'])
                        self.assertEqual(screenshot_after_back,[True])
                        actions.append('locale'); stage[0]='settings'
                    step = next(s for s in factory(phone,lambda _:None,registration=state)
                                if s.name.startswith('b17 '))
                    with patch.object(flow,'_read',side_effect=read), \
                         patch.object(flow,'cloud_adb',side_effect=back), \
                         patch.object(flow,'_tap_for_transition',side_effect=tap):
                        step.action(RunJob(index,'text-backup',None),AttemptDeadline(None),self.stop)
                    self.assertEqual(actions,['back','locale'])
                    self.assertEqual(state.tail_choices,{13:'dogs',14:'cats',15:'pets'})
                    self.assertEqual(state.marketplace_completed,{16,17})
                    self.assertFalse(state.marketplace_done_sent)
                    self.assertEqual(state.flow_mode,mode)

    def test_normal_locale_target_does_not_enter_back_or_screenshot_fallback(self):
        state = self.state(); state.marketplace_completed.add(16)
        tapped = []
        with patch.object(flow,'_read',side_effect=lambda *_a,**_k:
                          settings('Singapore') if tapped else ACCOUNT) as read, \
             patch.object(flow,'cloud_adb') as adb, \
             patch.object(flow,'_tap_for_transition',side_effect=lambda *_:tapped.append(True)) as tap:
            self.action(17,state)(None,AttemptDeadline(None),self.stop)
        adb.assert_not_called()
        tap.assert_called_once()
        self.assertEqual(read.call_count, 1)
        self.assertTrue(read.call_args.kwargs.get('visual'))

    def test_text_back_fallback_does_not_rewind_after_done_was_sent(self):
        state = self.state(); state.marketplace_completed.update(range(16,21))
        state.marketplace_done_sent=True; state.marketplace_done_attempts=1
        state.marketplace_done_at=self.clock[0]
        incomplete = [n for n in settings('United States') if n.get('text')!='Done']
        with patch.object(flow,'_read',return_value=incomplete), \
             patch.object(flow,'cloud_adb') as adb, \
             patch.object(flow,'_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError,'75 giây'):
                self.action(21,state)(None,AttemptDeadline(None),self.stop)
        adb.assert_not_called(); tap.assert_not_called()
        self.assertEqual(state.marketplace_done_attempts,1)
        self.assertNotIn(21,state.marketplace_completed)

    def test_text_back_fallback_stops_if_new_screenshot_returns_to_authentication(self):
        state = self.state(); state.marketplace_completed.add(16)
        broken = [n for n in ACCOUNT if n.get('text')!='EN']
        backed = []
        def read(*_a,**_k):
            return [node('Verify mobile number'),node('Enter security code')] if backed else broken
        with patch.object(flow,'_read',side_effect=read), \
             patch.object(flow,'cloud_adb',side_effect=lambda *_a,**_k:backed.append(True)), \
             patch.object(flow,'_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError,'Back tới form xác minh'):
                self.action(17,state)(None,AttemptDeadline(None),self.stop)
        self.assertEqual(backed,[True])
        tap.assert_not_called()

    def test_country_text_backup_runs_only_after_existing_scroll_attempts_are_exhausted(self):
        state = self.state(); state.marketplace_completed.update(range(16,19))
        stage = ['list']; swipes = []; backs = []; taps = []; captured = []
        def read(*_args,**kwargs):
            if stage[0]=='settings':
                if kwargs.get('visual'):
                    captured.append(True)
                return settings('Singapore')
            return BOTTOM if stage[0]=='bottom' else TOP
        def adb(_phone,*args,**_kwargs):
            if args[:3]==('shell','input','swipe'):
                swipes.append(args)
            elif args[:3]==('shell','input','keyevent'):
                self.assertEqual(len(swipes),16)
                backs.append(args); stage[0]='settings'
            return SimpleNamespace(stdout='Physical size: 420x910')
        def tap(_phone,target,*_args):
            self.assertTrue(captured)
            taps.append(target['text']); stage[0]='bottom'
        with patch.object(flow,'_read',side_effect=read), \
             patch.object(flow,'cloud_adb',side_effect=adb), \
             patch.object(flow,'_tap_for_transition',side_effect=tap):
            self.action(19,state)(None,AttemptDeadline(None),self.stop)
        self.assertEqual(len(backs),1)
        self.assertEqual(taps,['Country/Region:'])
        self.assertIn(19,state.marketplace_completed)
        self.assertNotIn(20,state.marketplace_completed)  # Finding still does not select US.

    def test_text_backup_does_not_guess_between_duplicate_locale_labels(self):
        state = self.state(); state.marketplace_completed.add(16)
        broken = [n for n in ACCOUNT if n.get('text')!='EN']
        ambiguous = [node('Different layout'),node('Country and language','[20,250][330,280]'),
                     node('Country and language','[20,350][330,380]')]
        backs = []
        with patch.object(flow,'_read',side_effect=lambda *_a,**_k:ambiguous if backs else broken), \
             patch.object(flow,'cloud_adb',side_effect=lambda *_a,**_k:backs.append(True)), \
             patch.object(flow,'_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError,'ba lần Back'):
                self.action(17,state)(None,AttemptDeadline(None),self.stop)
        self.assertEqual(len(backs),3)
        tap.assert_not_called()

    def test_after_done_all_modes_slots_tap_person_on_first_available_tabs_while_content_loads(self):
        for mode in ('create','login'):
            for index, factory in POST_MENU_STEP_FACTORIES.items():
                with self.subTest(mode=mode, slot=index+1):
                    state = self.state(); state.flow_mode = mode
                    state.marketplace_completed.update(range(16,21))
                    phone = CloudPhone(f'127.0.0.1:{5001+index}')
                    person = (TAB if index % 3 == 0 else
                              node(bounds='[110,810][190,860]', **{
                                  'resource-id': 'com.amazon.app:id/bottom_nav_you'}))
                    visible = ([person] if index % 3 != 2 else [
                        node(bounds='[10,810][90,860]', **{'content-desc': 'Home Tab, 1 of 4'}),
                        node(bounds='[210,810][290,860]', **{'content-desc': 'Cart Tab, 3 of 4'})])
                    partial = [node('Loading recommendations...')] + visible
                    stage = ['settings']; after_done_reads = [0]; taps = []; seen = []
                    def read(active_phone, *_args, **kwargs):
                        self.assertEqual(active_phone, phone)
                        if stage[0] == 'settings':
                            return settings('United States')
                        self.assertTrue(kwargs.get('navigation'))
                        if stage[0] == 'account':
                            return ACCOUNT
                        after_done_reads[0] += 1
                        if after_done_reads[0] <= 2:
                            return [node('Loading...')]
                        seen.append(self.clock[0])
                        return partial
                    def tap(active_phone, target, *_args):
                        self.assertEqual(active_phone, phone)
                        if stage[0] == 'settings':
                            self.assertEqual(target['text'],'Done')
                            stage[0] = 'loading'; taps.append(('done',self.clock[0]))
                        else:
                            if index % 3 != 2:
                                self.assertIs(target,person)
                            else:
                                left,top,right,bottom = flow._bounds(target)
                                self.assertEqual(((left+right)/2,(top+bottom)/2),(150,835))
                            taps.append(('person',self.clock[0])); stage[0] = 'account'
                    steps = factory(phone,lambda _:None,registration=state)
                    start = next(i for i,s in enumerate(steps) if s.name.startswith('b21 '))
                    session = PostMenuSession('immediate-person',index,f'q{index+1}',
                                              next_step=start,registration=state)
                    with patch.object(flow,'_read',side_effect=read), \
                         patch.object(flow,'_size',return_value=(420,910)), \
                         patch.object(flow,'_tap_for_transition',side_effect=tap):
                        end = next(i for i,s in enumerate(steps) if s.name.startswith('b22 '))
                        session.run(RunJob(index,'immediate-person',None),steps[:end+1],lambda *_:None,self.stop)
                    self.assertEqual(session.state,'DONE',session.last_error)
                    self.assertEqual([t[0] for t in taps],['done','person'])
                    self.assertEqual(taps[1][1],seen[0])  # No delay after the tab first appears.
                    self.assertLess(taps[1][1]-taps[0][1],1)
                    self.assertEqual(state.marketplace_completed,set(range(16,23)))

    def test_navigation_native_tab_returns_without_any_ocr_on_partial_unknown_page(self):
        partial = [node('Loading...'),TAB]
        self.assertEqual(screen(partial),'UNKNOWN')
        with patch.object(flow,'_read_hierarchy',return_value=partial), \
             patch.object(flow,'_read_visual_nodes',side_effect=AssertionError('Must not wait for OCR')):
            self.assertIs(flow._read_navigation_nodes(self.phone,AttemptDeadline(12),self.stop),partial)

    def test_b22_newly_visible_person_does_not_wait_for_back_cooldown(self):
        state = self.state(); state.marketplace_completed.update(range(16,22))
        state.marketplace_done_confirmed = True
        stage = ['search']; seen = []; tapped = []
        def read(*_args, **_kwargs):
            if stage[0] == 'search':
                return [node('Search with photo')]
            if stage[0] == 'menu':
                seen.append(self.clock[0]); return [TAB,node('Loading images...')]
            return ACCOUNT
        def back(*_args, **_kwargs):
            stage[0] = 'menu'
        def tap(*_args):
            tapped.append(self.clock[0]); stage[0] = 'account'
        with patch.object(flow,'_read',side_effect=read), \
             patch.object(flow,'cloud_adb',side_effect=back) as adb, \
             patch.object(flow,'_tap_for_transition',side_effect=tap):
            self.action(22,state)(None,AttemptDeadline(None),self.stop)
        adb.assert_called_once()
        self.assertEqual(tapped,[seen[0]])
        self.assertLess(tapped[0]-100,1)

    def test_navigation_ocr_remains_fallback_when_native_cannot_expose_tab(self):
        with patch.object(flow,'_read_hierarchy',return_value=[node('Search Amazon')]), \
             patch.object(flow,'_read_visual_nodes',return_value=[TAB]) as visual:
            self.assertEqual(flow._read_navigation_nodes(
                self.phone,AttemptDeadline(12),self.stop),[TAB])
        visual.assert_called_once()

    def test_navigation_reader_is_bound_to_own_serial_and_stop(self):
        reader = Mock()
        reader.call.return_value = [TAB]
        with patch('amazon_android.isolated_reader.current',return_value=reader) as current:
            self.assertEqual(flow._read(self.phone,AttemptDeadline(12),self.stop,navigation=True),[TAB])
            self.assertEqual(current.call_args.args,(self.phone.serial,))
            self.assertEqual(reader.call.call_args.args[0],'navigation')
            self.stop.set()
            with self.assertRaisesRegex(ToolError,'Đã dừng'):
                flow._read(self.phone,AttemptDeadline(12),self.stop,navigation=True)
        reader.call.assert_called_once()

    def test_navigation_stop_during_native_read_does_not_trigger_ocr(self):
        def native(*_args):
            self.stop.set(); return [TAB]
        with patch.object(flow,'_read_hierarchy',side_effect=native), \
             patch.object(flow,'_read_visual_nodes') as visual:
            with self.assertRaisesRegex(ToolError,'Đã dừng'):
                flow._read_navigation_nodes(self.phone,AttemptDeadline(12),self.stop)
        visual.assert_not_called()

    def test_both_modes_all_slots_recover_search_then_finish_b16_to_b22_with_real_focus_guard(self):
        search = [node('Search Amazon.sg', **{'class': 'android.widget.EditText',
                                              'focused': 'true'}),
                  node('Search with photo'), node('Search with camera')]
        menu = [node('Books and Reading'), node('Office & Professional'), node('Your Stuff'),
                node(**{'content-desc': 'Home Tab, 1 of 4'}, bounds='[10,810][90,860]'),
                node(**{'content-desc': 'Cart Tab, 3 of 4'}, bounds='[210,810][290,860]'), BROWSE]
        viewer = [node('Search Amazon.sg'), node('Fullscreen detail'),
                  node('Image details'), node('Product details')]
        for mode in ('create', 'login'):
            for index, factory in POST_MENU_STEP_FACTORIES.items():
                with self.subTest(mode=mode, slot=index + 1):
                    phone = CloudPhone(f'127.0.0.1:{5001+index}')
                    state = self.state(); state.flow_mode = mode
                    stage = ['keyboard']; loading = [0]; backs = []; taps = []; swipes = []
                    def read(active_phone, *_args, **_kwargs):
                        self.assertEqual(active_phone, phone)
                        if stage[0] == 'loading':
                            loading[0] += 1
                            if loading[0] <= 3:
                                return [node('Loading...')]
                            stage[0] = 'viewer'
                        return {'keyboard': search, 'search': search, 'menu': menu,
                                'account': ACCOUNT, 'settings': settings('Singapore'),
                                'top': TOP, 'bottom': BOTTOM, 'us': settings('United States'),
                                'viewer': viewer}[stage[0]]
                    def adb(active_phone, *args, **kwargs):
                        self.assertEqual(active_phone, phone)
                        if args[:3] == ('shell', 'input', 'keyevent'):
                            self.assertEqual(args[-1], 'KEYCODE_BACK')
                            backs.append(stage[0])
                            stage[0] = {'keyboard': 'search', 'search': 'menu',
                                        'viewer': 'menu'}[stage[0]]
                        elif args[:3] == ('shell', 'input', 'swipe'):
                            swipes.append(args); stage[0] = 'bottom'
                        if args[:3] == ('shell', 'dumpsys', 'window'):
                            output = '' if len(args) > 3 else (
                                'mCurrentFocus=null\nmCurrentFocus=Window{u0 '
                                'com.amazon.mShop.android.shopping/MainActivity}')
                        else:
                            output = 'Physical size: 420x910'
                        return SimpleNamespace(returncode=0, stdout=output)
                    def tap(active_phone, target, *_args):
                        self.assertEqual(active_phone, phone)
                        text = target.get('text')
                        taps.append(text or 'person')
                        if stage[0] == 'menu':
                            left, top, right, bottom = flow._bounds(target)
                            self.assertEqual(((left+right)/2, (top+bottom)/2), (150,835))
                            stage[0] = 'account'
                        else:
                            stage[0] = {'EN': 'settings', 'Country/Region:': 'top',
                                        'United States': 'us', 'Done': 'loading'}[text]
                    steps = factory(phone, lambda _: None, registration=state)
                    start = next(i for i,s in enumerate(steps) if s.name.startswith('b16 '))
                    session = PostMenuSession('search-recovery', index, f'q{index+1}',
                                              next_step=start, registration=state)
                    with patch.object(flow, '_read', side_effect=read), \
                         patch.object(flow, 'cloud_adb', side_effect=adb), \
                         patch.object(flow, '_foreground', side_effect=FOREGROUND_CHECK), \
                         patch.object(flow, '_tap_for_transition', side_effect=tap):
                        session.run(RunJob(index, 'search-recovery', None), steps[:start+7],
                                    lambda *_: None, self.stop)
                    self.assertEqual(session.state, 'DONE', session.last_error)
                    self.assertEqual(state.marketplace_completed, set(range(16,23)))
                    self.assertEqual(backs, ['keyboard', 'search', 'viewer'])
                    self.assertEqual(taps, ['person', 'EN', 'Country/Region:',
                                            'United States', 'Done', 'person'])
                    self.assertEqual(len(swipes), 1)

    def test_b17_recovers_search_then_reopens_account_before_locale(self):
        state = self.state(); state.marketplace_completed.add(16)
        current = ['search']; events = []
        def read(*_a, **_k):
            return {'search': [node('Search with photo'), node('Search with camera')],
                    'menu': [TAB, BROWSE], 'account': ACCOUNT,
                    'settings': settings('Singapore')}[current[0]]
        def adb(phone, *args, **_kwargs):
            self.assertEqual(phone, self.phone)
            self.assertEqual(args, ('shell','input','keyevent','KEYCODE_BACK'))
            events.append('back'); current[0] = 'menu'
        def tap(_phone, target, *_args):
            if target is TAB:
                events.append('person'); current[0] = 'account'
            else:
                self.assertEqual(target['text'], 'EN')
                events.append('EN'); current[0] = 'settings'
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(flow, '_tap_for_transition', side_effect=tap):
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(events, ['back', 'person', 'EN'])
        self.assertIn(17, state.marketplace_completed)

    def test_search_recovery_is_bounded_and_does_not_tap_missing_person_icon(self):
        state = self.state()
        with patch.object(flow, '_read', return_value=[node('Search with photo')]), \
             patch.object(flow, 'cloud_adb') as adb, \
             patch.object(flow, '_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError, 'ba lần Back'):
                self.action(16, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(adb.call_count, 3)
        tap.assert_not_called()
        self.assertNotIn(16, state.marketplace_completed)

    def test_stop_during_search_recovery_does_not_send_back(self):
        state = self.state()
        def focus(*_args):
            self.stop.set()
        with patch.object(flow, '_read', return_value=[node('Search with camera')]), \
             patch.object(flow, '_foreground', side_effect=focus), \
             patch.object(flow, 'cloud_adb') as adb:
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                self.action(16, state)(None, AttemptDeadline(None), self.stop)
        adb.assert_not_called()

    def test_b20_reopens_correct_setting_after_accidental_page_change(self):
        state = self.state(); state.marketplace_completed.update(range(16,20))
        current = [ACCOUNT]
        def tap_action(_phone, target, *_args):
            current[0] = {'EN': settings('Singapore'), 'Country/Region:': BOTTOM,
                          'United States': settings('United States')}[target['text']]
        with patch.object(flow, '_read', side_effect=lambda *_a,**_k: current[0]), \
             patch.object(flow, '_tap_for_transition', side_effect=tap_action) as tap:
            self.action(20, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual([c.args[1]['text'] for c in tap.call_args_list],
                         ['EN', 'Country/Region:', 'United States'])
        self.assertIn(20, state.marketplace_completed)

    def test_b19_finds_us_without_selecting_and_b20_selects(self):
        state = self.state(); state.marketplace_completed.update(range(16,19))
        with patch.object(flow, '_read', return_value=BOTTOM), \
             patch.object(flow, '_tap_for_transition') as tap:
            self.action(19, state)(None, AttemptDeadline(None), self.stop)
        tap.assert_not_called()
        self.assertIn(19, state.marketplace_completed)

    def test_done_timeout_retains_dispatch_and_resume_does_not_tap_again(self):
        state = self.state(); state.marketplace_completed.update(range(16,21))
        calls = [0]
        def read(*_args, **_kwargs):
            calls[0] += 1
            return settings('United States') if calls[0] == 1 else []
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, '_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError, '75 giây'):
                self.action(21, state)(None, AttemptDeadline(None), self.stop)
        self.assertTrue(state.marketplace_done_sent)
        tap.assert_called_once()
        self.assertNotIn(21, state.marketplace_completed)
        with patch.object(flow, '_read', return_value=[TAB, BROWSE]), \
             patch.object(flow, '_tap_for_transition') as resumed_tap:
            self.action(21, state)(None, AttemptDeadline(None), self.stop)
        resumed_tap.assert_not_called()
        self.assertTrue(state.marketplace_done_confirmed)

    def test_repeated_done_still_visible_is_bounded_and_never_selects_other_country(self):
        state = self.state(); state.marketplace_completed.update(range(16,21))
        state.marketplace_done_sent = True
        state.marketplace_done_attempts = 1
        state.marketplace_done_at = self.clock[0]
        tap_times = []
        with patch.object(flow, '_read', return_value=settings('United States')), \
             patch.object(flow, '_tap_for_transition', side_effect=lambda *_:
                          tap_times.append(self.clock[0])) as tap:
            with self.assertRaisesRegex(ToolError, 'Done hai lần'):
                self.action(21, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual([c.args[1]['text'] for c in tap.call_args_list], ['Done'])
        self.assertGreaterEqual(tap_times[0], 120)  # Resume preserves the prior tap's wait.
        self.assertEqual(state.marketplace_done_attempts, 2)

    def test_authentication_screen_stops_instead_of_touching_account_tab(self):
        state = self.state()
        sms = [node('Verify mobile number'), node('Enter security code')]
        with patch.object(flow, '_read', return_value=sms), \
             patch.object(flow, '_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError, 'xác minh'):
                self.action(16, state)(None, AttemptDeadline(None), self.stop)
        tap.assert_not_called()

    def test_stop_and_prerequisites_do_not_allow_extra_actions(self):
        with self.assertRaisesRegex(ToolError, 'b12–b15'):
            self.action(16, RegistrationState())(None, AttemptDeadline(None), self.stop)
        self.stop.set()
        with patch.object(flow, '_read') as read:
            with self.assertRaisesRegex(ToolError, 'Đã dừng'):
                self.action(16, self.state())(None, AttemptDeadline(None), self.stop)
        read.assert_not_called()

    def test_native_account_tab_is_preferred_and_visual_fallback_uses_live_size(self):
        self.assertIs(flow._account_tab(self.phone, [TAB], AttemptDeadline(None)), TAB)
        with patch.object(flow, '_size', return_value=(420,910)):
            fallback = flow._account_tab(self.phone, [BROWSE], AttemptDeadline(None))
        left, top, right, bottom = flow._bounds(fallback)
        self.assertAlmostEqual((left+right)/2, 420*0.375, delta=1)
        self.assertEqual((top+bottom)/2, 835)

    def test_b16_clicks_person_from_menu_with_empty_short_focus_dump(self):
        menu = [node('Books and Reading'), node('Office & Professional'), node('Your Stuff'),
                node('Home', '[10,810][90,860]', **{'content-desc': 'Home Tab, 1 of 4'}),
                node('Cart', '[210,810][290,860]', **{'content-desc': 'Cart Tab, 3 of 4'}),
                node('Browse', '[310,810][390,860]', **{'content-desc': 'Browse menu Tab, 4 of 4'})]
        state = self.state(); pressed = []
        def read(*_args, **_kwargs):
            return ACCOUNT if pressed else menu
        def adb(_phone, *args, **_kwargs):
            self.assertEqual(_phone.serial, self.phone.serial)
            if args == ('shell','wm','size'):
                return SimpleNamespace(returncode=0, stdout='Physical size: 420x910')
            if args == ('shell','dumpsys','window','windows'):
                return SimpleNamespace(returncode=0, stdout='')
            self.assertEqual(args, ('shell','dumpsys','window'))
            return SimpleNamespace(returncode=0, stdout='mCurrentFocus=null\n'
                'mCurrentFocus=Window{u0 com.amazon.mShop.android.shopping/MainActivity}')
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(flow, '_foreground', side_effect=FOREGROUND_CHECK), \
             patch.object(flow, '_tap_for_transition', side_effect=lambda _p,target,*_:
                          pressed.append(target)):
            self.action(16, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(len(pressed), 1)
        left, top, right, bottom = flow._bounds(pressed[0])
        self.assertEqual(((left+right)/2, (top+bottom)/2), (150,835))
        self.assertEqual(state.marketplace_completed, {16})

    def test_b16_does_not_need_account_page_or_text_label_to_click_person(self):
        state = self.state(); pressed = []
        page = [node('Search Amazon.sg'), node('Looking for the app settings?')]
        with patch.object(flow, '_read', side_effect=lambda *_a,**_k: ACCOUNT if pressed else page), \
             patch.object(flow, '_size', return_value=(400,880)), \
             patch.object(flow, '_tap_for_transition', side_effect=lambda _p,target,*_:
                          pressed.append(target)):
            self.action(16, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(len(pressed), 1)
        left, top, right, bottom = flow._bounds(pressed[0])
        self.assertEqual((left+right)/2, 150)
        self.assertAlmostEqual((top+bottom)/2, 880*0.925, delta=1)
        self.assertIn(16, state.marketplace_completed)

    def test_b16_rereads_transient_missing_focus_before_sending_one_tap(self):
        state = self.state(); pressed = []
        with patch.object(flow, '_read', side_effect=lambda *_a,**_k:
                          ACCOUNT if pressed else [TAB, BROWSE]), \
             patch.object(flow, '_foreground', side_effect=[ToolError('focus'), ToolError('focus'), None]), \
             patch.object(flow, '_tap_for_transition', side_effect=lambda *_: pressed.append(True)) as tap:
            self.action(16, state)(None, AttemptDeadline(None), self.stop)
        tap.assert_called_once()
        self.assertIn(16, state.marketplace_completed)

    def test_unselected_previously_visited_us_cannot_trigger_done(self):
        state = self.state(); state.marketplace_completed.update(range(16,21))
        with patch.object(flow, '_read', side_effect=[settings('Singapore'),
                           [node('Verify mobile number'), node('Enter security code')]]), \
             patch.object(flow, '_tap_for_transition') as tap:
            with self.assertRaises(ToolError):
                self.action(21, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(tap.call_args.args[1]['text'], 'Country/Region:')
        self.assertFalse(state.marketplace_done_sent)

    def test_done_accepts_new_shop_layout_with_search_header_without_fixed_image(self):
        page = [node('Search Amazon.com'), node('New recommendations'),
                node('Seasonal picks'), node('Customer favorites')]
        self.assertEqual(screen(page), 'UNKNOWN')
        self.assertTrue(flow._destination(page))
        self.assertFalse(flow._destination([node('Amazon'), node('Loading...')]))

    def test_network_retry_button_is_used_when_locale_has_not_loaded(self):
        state = self.state(); state.marketplace_completed.add(16)
        failed = [n for n in ACCOUNT if n.get('text') != 'EN'] + [
            node('Retry', '[20,400][380,450]')]
        recovered = [False]
        def read(*_args, **_kwargs):
            return settings('Singapore') if recovered[0] else failed
        def tap(_phone, target, *_args):
            self.assertEqual(target['text'], 'Retry')
            recovered[0] = True
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, '_tap_for_transition', side_effect=tap):
            self.action(17, state)(None, AttemptDeadline(None), self.stop)
        self.assertIn(17, state.marketplace_completed)

    def test_transient_reader_failures_do_not_fail_before_page_loads(self):
        state = self.state()
        with patch.object(flow, '_read', side_effect=[ToolError('read'), ToolError('read'), ACCOUNT]), \
             patch.object(flow, '_tap_for_transition') as tap:
            self.action(16, state)(None, AttemptDeadline(None), self.stop)
        tap.assert_not_called()
        self.assertEqual(state.marketplace_completed, {16})

    def test_stuck_country_scroll_reverses_gently_then_finds_us(self):
        state = self.state(); state.marketplace_completed.update(range(16,19))
        swipes = []
        def read(*_args, **_kwargs):
            return BOTTOM if len(swipes) >= 3 else TOP
        def adb(_phone, *args, **_kwargs):
            if args[:3] == ('shell','input','swipe'):
                swipes.append(args)
            return SimpleNamespace(stdout='Physical size: 420x910')
        with patch.object(flow, '_read', side_effect=read), \
             patch.object(flow, 'cloud_adb', side_effect=adb), \
             patch.object(flow, '_tap_for_transition') as tap:
            self.action(19, state)(None, AttemptDeadline(None), self.stop)
        self.assertEqual(len(swipes), 3)
        self.assertLess(int(swipes[-1][4]), int(swipes[-1][6]))
        self.assertIn(19, state.marketplace_completed)
        tap.assert_not_called()

    def test_foreground_guard_failure_never_sends_navigation_tap(self):
        with patch.object(flow, '_read', return_value=[TAB, BROWSE]), \
             patch.object(flow, '_foreground', side_effect=ToolError('Amazon chưa ở phía trước')), \
             patch.object(flow, '_tap_for_transition') as tap:
            with self.assertRaisesRegex(ToolError, 'phía trước'):
                self.action(16, self.state())(None, AttemptDeadline(None), self.stop)
        tap.assert_not_called()


if __name__ == '__main__':
    unittest.main()
