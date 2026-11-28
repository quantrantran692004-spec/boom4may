"""The separate Settings flow: Browse menu, then change marketplace to US.

Each step observes only its requested control. It never routes by a presumed
entry screen or resumes into the Create/Login flow.
"""
from __future__ import annotations

import io
import math
import re
import time
from pathlib import Path

from .account_flow import (NAME_FIELD, OTP_FIELD, PHONE_FIELD, _button,
                           _check_summary, _field, _form_action, _has,
                           _national_phone, _tap_input, _text, _type_field,
                           _visible)
from .cloud import cloud_adb, cloud_screenshot
from .core import ToolError
from .marketplace_flow import (_country_card, _en_button, _foreground, _is_account_tab,
                               _one, _read, _resolve, _scroll_country, _size, _us_row,
                               _us_selected, _pause, _tap_for_transition)
from .marketplace_flow import marketplace_screen
from .post_menu import AttemptDeadline, PostMenuStep
from .otp import wait_for_new_otp


class _StepBlocked(ToolError):
    terminal = True  # b1–b7 must pause for a person, not retry forever.


_ICON = Path(__file__).resolve().parent.parent / 'flow_images' / 'shared' / \
        'change_us_from_start' / 'account_tab_template.png'


def _account_icon_from_image(phone, deadline):
    """Match the supplied person icon in the live bottom bar, never a blind tap."""
    import cv2
    import numpy as np

    if not _ICON.is_file():
        return None
    from PIL import Image

    screenshot = cloud_screenshot(phone, timeout=max(1, math.ceil(min(6, deadline.remaining()))))
    frame = np.asarray(Image.open(io.BytesIO(screenshot)).convert('L'))
    template = np.asarray(Image.open(_ICON).convert('L'))
    height, width = frame.shape
    left, right = int(width * .20), int(width * .55)
    top, bottom = int(height * .78), int(height * .97)
    region = frame[top:bottom, left:right]
    if region.size == 0:
        return None
    best = (0.0, None)
    for scale in (.75, .9, 1., 1.15, 1.3, 1.5, 1.75, 2.):
        icon = cv2.resize(template, None, fx=scale, fy=scale,
                          interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
        ih, iw = icon.shape
        if ih > region.shape[0] or iw > region.shape[1]:
            continue
        _, score, _, where = cv2.minMaxLoc(cv2.matchTemplate(region, icon,
                                                            cv2.TM_CCOEFF_NORMED))
        if score > best[0]:
            best = (score, (left + where[0] + iw // 2, top + where[1] + ih // 2))
    if best[0] < .78 or best[1] is None:
        return None
    x, y = best[1]
    return {'bounds': f'[{x-1},{y-1}][{x+1},{y+1}]'}


def _person(phone, nodes, deadline):
    matches = [node for node in nodes if _visible(node) and _is_account_tab(node)]
    if matches:
        return _one(matches, lambda _: True, 'tab hình người')
    return _account_icon_from_image(phone, deadline)


def _browse(nodes):
    return _one(nodes, lambda node: (
        (node.get('content-desc') or node.get('text') or '').casefold().startswith(
            ('browse menu tab', 'browse menu'))), 'menu ba gạch')


def _menu_visible(nodes):
    labels = {_text(node) for node in nodes if _visible(node)}
    return 'shop by category' in labels or len(labels & {
        'gifting', 'pets', 'books and reading', 'groceries and drinks',
        'devices and electronics', 'fashion and beauty'}) >= 3


def _post_done_person(phone, nodes, deadline):
    """The tab exists on the picker too; wait until the picker has disappeared."""
    if marketplace_screen(nodes) in {'MARKET_SETTINGS', 'MARKET_COUNTRIES'}:
        return None
    if any(_visible(node) and ('country/region' in _text(node) or
                              _text(node) == 'done') for node in nodes):
        return None
    return _person(phone, nodes, deadline)


def _observe(phone, deadline, stop, locator, *, navigation=False, visual_only=False):
    """Read the current phone, then OCR if the exact target is absent."""
    if visual_only:
        nodes = _read(phone, deadline, stop, visual=True)
        return locator(nodes), nodes
    nodes = _read(phone, deadline, stop, navigation=navigation)
    target = locator(nodes)
    if target is not None:
        return target, nodes
    if navigation:
        return None, nodes
    visual = _read(phone, deadline, stop, visual=True)
    return locator(visual), visual


def _wait_target(phone, outer, stop, locator, label, *, navigation=False,
                 visual_only=False, seconds=60, interval=.5):
    deadline = AttemptDeadline(seconds, notice=outer.notice)
    until = time.monotonic() + seconds
    failures = 0
    while time.monotonic() < until:
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        try:
            target, nodes = _observe(phone, deadline, stop, locator,
                                     navigation=navigation, visual_only=visual_only)
            failures = 0
        except ToolError:
            if stop.is_set():
                raise
            failures += 1
            if failures >= 3:
                raise _StepBlocked('Đọc màn lỗi ba lần; kiểm tra kết nối rồi Tiếp tục')
            _pause(stop, interval)
            continue
        if target is not None:
            return target, nodes, deadline
        _pause(stop, interval)
    raise _StepBlocked(f'Chưa thấy {label} trên máy này; giữ bước để Tiếp tục')


def _raw_nodes(phone, deadline, stop):
    """Read a system sheet and Amazon together, without an Amazon focus gate."""
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    from .vision import ocr_nodes

    screenshot = cloud_screenshot(phone, timeout=max(1, math.ceil(min(6, deadline.remaining()))))
    return ocr_nodes(screenshot, stop=stop, remaining=deadline.remaining,
                     text_only=True)


def _passkey_page(nodes):
    return _has(nodes, 'Account created') and _has(nodes, 'Create a passkey')


def _google_sheet(nodes):
    labels = {_text(node) for node in nodes if _visible(node)}
    joined = ' '.join(labels)
    return ('google' in joined and ('llaves de acceso' in joined or
                                    'passkey' in joined) and
            (bool(labels & {'cancelar', 'cancel'}) or
             bool(labels & {'acceder', 'continue'})))


def _wait_raw(phone, outer, stop, locator, label, *, seconds=60, interval=.5):
    deadline = AttemptDeadline(seconds, notice=outer.notice)
    until = time.monotonic() + seconds
    failures = 0
    while time.monotonic() < until:
        try:
            nodes = _raw_nodes(phone, deadline, stop)
            failures = 0
        except ToolError:
            if stop.is_set():
                raise
            failures += 1
            if failures >= 3:
                raise _StepBlocked('Không đọc được ảnh máy này ba lần; kiểm tra kết nối rồi Tiếp tục')
            _pause(stop, interval)
            continue
        target = locator(nodes)
        if target is not None:
            return target, nodes, deadline
        _pause(stop, interval)
    raise _StepBlocked(f'Chưa thấy {label} trên máy này; giữ bước để Tiếp tục')


def _after_back(phone, outer, stop):
    """Allow a Google sheet to animate before deciding whether Back is needed again."""
    deadline = AttemptDeadline(8, notice=outer.notice)
    until = time.monotonic() + 8
    saw_sheet = False
    failures = 0
    while time.monotonic() < until:
        try:
            nodes = _raw_nodes(phone, deadline, stop)
            failures = 0
        except ToolError:
            if stop.is_set():
                raise
            failures += 1
            if failures >= 3:
                raise _StepBlocked('Không đọc được ảnh sau Back ba lần; kiểm tra máy này')
            _pause(stop, .5)
            continue
        if _passkey_page(nodes) and not _google_sheet(nodes):
            return 'ready'
        saw_sheet = saw_sheet or _google_sheet(nodes)
        _pause(stop, .5)
    if saw_sheet:
        return 'sheet'
    raise _StepBlocked('Chưa xác nhận màn passkey sau Back; giữ máy để Tiếp tục')


def build_change_us_steps(phone, state, on_otp=lambda _code: None,
                          on_status=lambda _status: None):
    """Build the independent b1–b17 path for one phone."""
    def guarded(action):
        def run(job, outer, stop):
            try:
                action(job, outer, stop)
            except Exception as exc:
                if stop.is_set() or isinstance(exc, _StepBlocked):
                    raise
                reason = str(exc) if isinstance(exc, ToolError) else type(exc).__name__
                raise _StepBlocked(reason) from exc
        return run

    def b1(job, outer, stop):
        if state.early_us_menu_until is None:
            target, nodes, deadline = _wait_target(
                phone, outer, stop, lambda ns: _resolve(_browse, ns),
                'menu ba gạch', navigation=True)
            if target.get('selected') != 'true' and not _menu_visible(nodes):
                _foreground(phone, deadline)
                _tap_for_transition(phone, target, deadline)
            state.early_us_menu_until = time.monotonic() + 4
        remaining = state.early_us_menu_until - time.monotonic()
        if remaining > 0:
            outer.recovering('b1: menu ba gạch · chờ đủ 4 giây')
            _pause(stop, remaining)

    def b2(job, outer, stop):
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        deadline = AttemptDeadline(10, notice=outer.notice)
        width, height = _size(phone, deadline)
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        cloud_adb(phone, 'shell', 'input', 'tap', str(round(width * .375)),
                  str(round(height * .925)),
                  timeout=max(1, math.ceil(min(6, deadline.remaining()))))

    def b3(job, outer, stop):
        target, _, deadline = _wait_target(phone, outer, stop,
            lambda ns: _resolve(_en_button, ns), 'cờ/EN')
        _foreground(phone, deadline)
        _tap_for_transition(phone, target, deadline)

    def b4(job, outer, stop):
        target, _, deadline = _wait_target(phone, outer, stop,
            lambda ns: _resolve(_country_card, ns), 'ô Country/Region')
        _foreground(phone, deadline)
        _tap_for_transition(phone, target, deadline)

    def b5(job, outer, stop):
        deadline = AttemptDeadline(75, notice=outer.notice)
        until = time.monotonic() + 75
        scrolls = 0
        failures = 0
        while time.monotonic() < until:
            try:
                target, nodes = _observe(phone, deadline, stop,
                                     lambda ns: _resolve(_us_row, ns))
                failures = 0
            except ToolError:
                if stop.is_set():
                    raise
                failures += 1
                if failures >= 3:
                    raise _StepBlocked('b5: đọc danh sách quốc gia lỗi ba lần; Tiếp tục sau khi sửa')
                _pause(stop, 1)
                continue
            if target is not None:
                return
            if marketplace_screen(nodes) != 'MARKET_COUNTRIES':
                _pause(stop, .5)
                continue
            if scrolls >= 16:
                break
            _scroll_country(phone, deadline, reverse=scrolls >= 12)
            scrolls += 1
            _pause(stop, 1)
        raise _StepBlocked('b5: chưa thấy United States sau khi cuộn; giữ máy để Tiếp tục')

    def b6(job, outer, stop):
        if not state.early_us_selected_sent:
            target, _, deadline = _wait_target(phone, outer, stop,
                lambda ns: True if _us_selected(ns) else _resolve(_us_row, ns),
                'United States')
            if target is not True:
                _foreground(phone, deadline)
                state.early_us_selected_sent = True  # uncertain ADB delivery: observe next UI
                _tap_for_transition(phone, target, deadline)
            else:
                state.early_us_selected_sent = True
        _wait_target(phone, outer, stop,
                     lambda ns: True if _us_selected(ns) else None,
                     'Country/Region = United States')

    def b7(job, outer, stop):
        if not state.early_us_done_sent:
            target, _, deadline = _wait_target(phone, outer, stop,
                lambda ns: _resolve(lambda items: _button(items, 'Done'), ns)
                if _us_selected(ns) else None, 'Done sau khi chọn United States')
            _foreground(phone, deadline)
            state.early_us_done_sent = True  # never send Done twice after uncertain delivery
            _tap_for_transition(phone, target, deadline)
        target, _, deadline = _wait_target(
            phone, outer, stop, lambda ns: _post_done_person(
                phone, ns, AttemptDeadline(8)),
            'tab hình người sau Done', visual_only=True, interval=.15)
        _foreground(phone, deadline)
        state.early_us_person_tapped_at = time.monotonic()
        _tap_for_transition(phone, target, deadline)

    def account(job):
        if job.account is None:
            raise _StepBlocked('Máy này chưa có hàng Amazon; nhập SĐT, tên và URL OTP rồi Tiếp tục')
        _national_phone(job)
        if not job.account.full_name.strip() or not job.account.otp_url:
            raise _StepBlocked('Hàng Amazon của máy này thiếu tên hoặc URL OTP')
        return job.account

    def field_target(label):
        return lambda nodes: (_resolve(lambda items: _field(items, label), nodes)
                              if _has(nodes, label) else None)

    def b8(job, outer, stop):
        if state.early_us_person_tapped_at is None:
            state.early_us_person_tapped_at = time.monotonic()
        remaining = state.early_us_person_tapped_at + 6 - time.monotonic()
        if remaining > 0:
            outer.recovering('b8: chờ đủ 6 giây sau tab hình người')
            _pause(stop, remaining)

        def create_entry(nodes):
            sign_in = _resolve(lambda items: _button(items, 'Sign in'), nodes)
            return (_resolve(lambda items: _button(items, 'Create account', below=sign_in), nodes)
                    if sign_in is not None else None)

        target, _, deadline = _wait_target(phone, outer, stop, create_entry,
                                           'Create account dưới Sign in')
        _foreground(phone, deadline)
        _tap_for_transition(phone, target, deadline)

    def b9(job, outer, stop):
        data = account(job)
        target, _, deadline = _wait_target(phone, outer, stop,
            field_target(PHONE_FIELD), 'ô nhập SĐT')
        _tap_input(phone, target, deadline, stop, label=PHONE_FIELD)
        _type_field(phone, PHONE_FIELD, data.phone, deadline, stop)

    def b10(job, outer, stop):
        account(job)
        if state.early_us_phone_continue_sent:
            _wait_target(phone, outer, stop,
                lambda ns: True if _has(ns, 'Proceed to create an account') else None,
                'màn xác nhận tạo tài khoản')
            return

        def continue_phone(nodes):
            if not (_has(nodes, PHONE_FIELD) and _has(nodes, 'US +1')):
                return None
            field = _resolve(lambda items: _field(items, PHONE_FIELD), nodes)
            return (_resolve(lambda items: _form_action(phone, items, 'Continue',
                        field, AttemptDeadline(8)), nodes) if field is not None else None)

        target, nodes, deadline = _wait_target(phone, outer, stop, continue_phone,
                                               'Continue dưới SĐT US +1')
        _check_summary(nodes, job)
        _foreground(phone, deadline)
        state.early_us_phone_continue_sent = True
        _tap_for_transition(phone, target, deadline)

    def b11(job, outer, stop):
        account(job)
        if state.early_us_proceed_sent:
            _wait_target(phone, outer, stop, field_target(NAME_FIELD),
                         'ô First and last name')
            return
        target, nodes, deadline = _wait_target(phone, outer, stop,
            lambda ns: _resolve(lambda items: _button(items,
                'Proceed to create an account'), ns), 'Proceed to create an account')
        _check_summary(nodes, job)
        _foreground(phone, deadline)
        state.early_us_proceed_sent = True
        _tap_for_transition(phone, target, deadline)

    def b12(job, outer, stop):
        account(job)
        target, nodes, deadline = _wait_target(phone, outer, stop,
            field_target(NAME_FIELD), 'ô First and last name')
        _check_summary(nodes, job)
        _tap_input(phone, target, deadline, stop, label=NAME_FIELD)

    def b13(job, outer, stop):
        data = account(job)
        if state.early_us_name_continue_sent:
            _wait_target(phone, outer, stop, field_target(OTP_FIELD),
                         'ô Enter security code')
            return
        target, nodes, deadline = _wait_target(phone, outer, stop,
            field_target(NAME_FIELD), 'ô First and last name')
        _check_summary(nodes, job)
        nodes = _type_field(phone, NAME_FIELD, data.full_name,
                            deadline, stop, nodes=nodes)
        field = _field(nodes, NAME_FIELD)
        if field.get('text', '') != data.full_name:
            raise _StepBlocked('Chưa xác nhận đúng tên của máy này trên form')
        button = _form_action(phone, nodes, 'Continue', field, deadline)
        _foreground(phone, deadline)
        state.early_us_name_continue_sent = True
        state.early_us_sms_requested_at = time.monotonic()
        _tap_for_transition(phone, button, deadline)

    def b14(job, outer, stop):
        data = account(job)
        target, nodes, deadline = _wait_target(phone, outer, stop,
            field_target(OTP_FIELD), 'ô Enter security code')
        _check_summary(nodes, job)
        current = _field(nodes, OTP_FIELD).get('text', '')
        if re.fullmatch(r'[0-9]{6}', current):
            state.code = current  # user may have entered this phone's code manually
        else:
            _tap_input(phone, target, deadline, stop, label=OTP_FIELD)
            if state.early_us_sms_requested_at is None:
                state.early_us_sms_requested_at = time.monotonic()
            on_status('Đang chờ mã')
            while not state.code:
                try:
                    state.code = data.browser_otp or wait_for_new_otp(
                        data.otp_url, None, timeout=30, stop=stop,
                        not_before=state.early_us_sms_requested_at + 4)
                except ToolError as exc:
                    if 'Hết thời gian chờ lượt đọc OTP' not in str(exc):
                        on_status('Không đọc được mã SMS')
                        raise
                    on_status('Chưa lấy được mã · tự mở lại trình duyệt')
            if not re.fullmatch(r'[0-9]{6}', state.code):
                raise _StepBlocked('OTP của máy này chưa đúng sáu chữ số')
            _type_field(phone, OTP_FIELD, state.code,
                        AttemptDeadline(90, notice=outer.notice), stop,
                        readback=False)
        on_otp(state.code)
        on_status('Đã nhập mã')

    def b15(job, outer, stop):
        account(job)
        if not state.early_us_create_sent:
            def create_button(nodes):
                if not (_has(nodes, OTP_FIELD) and _has(nodes,
                        'Create your Amazon account')):
                    return None
                field = _resolve(lambda items: _field(items, OTP_FIELD), nodes)
                return (_resolve(lambda items: _form_action(phone, items,
                        'Create your Amazon account', field, AttemptDeadline(8)), nodes)
                        if field is not None else None)

            target, nodes, deadline = _wait_target(phone, outer, stop,
                create_button, 'Create your Amazon account dưới ô mã')
            _check_summary(nodes, job)
            shown = _field(nodes, OTP_FIELD).get('text', '')
            if not (re.fullmatch(r'[0-9]{6}', shown) and shown == state.code):
                raise _StepBlocked('Chưa xác nhận đủ mã OTP của máy này trong ô')
            _foreground(phone, deadline)
            state.early_us_create_sent = True
            _tap_for_transition(phone, target, deadline)
        _wait_raw(phone, outer, stop,
                  lambda nodes: True if _passkey_page(nodes) else None,
                  'Account created và màn passkey')

    def b16(job, outer, stop):
        target, _, deadline = _wait_raw(phone, outer, stop,
            lambda nodes: 'sheet' if _google_sheet(nodes) else
            'ready' if _passkey_page(nodes) else None,
            'hộp Google hoặc màn passkey')
        while target == 'sheet':
            if state.early_us_back_attempts >= 2:
                raise _StepBlocked('Hộp Google chưa ẩn sau hai lần Back; kiểm tra máy này')
            state.early_us_back_attempts += 1
            cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_BACK',
                      timeout=max(1, math.ceil(min(6, deadline.remaining()))))
            target = _after_back(phone, outer, stop)

    def b17(job, outer, stop):
        if state.early_us_passkey_sent:
            return
        target, nodes, deadline = _wait_raw(phone, outer, stop,
            lambda ns: _resolve(lambda items: _button(items, 'Create a passkey'), ns)
            if _passkey_page(ns) and not _google_sheet(ns) else None,
            'nút vàng Create a passkey')
        _foreground(phone, deadline)
        state.early_us_passkey_sent = True
        _tap_for_transition(phone, target, deadline)

    names = ('b1 mở menu ba gạch, chờ 4 giây', 'b2 bấm tab hình người',
             'b3 tìm và bấm EN', 'b4 mở Country/Region',
             'b5 cuộn tìm United States', 'b6 chọn United States',
             'b7 Done rồi bấm ngay tab hình người',
             'b8 chờ 6 giây rồi Create account', 'b9 nhập SĐT',
             'b10 Continue dưới SĐT', 'b11 Proceed to create an account',
             'b12 chạm ô First and last name', 'b13 nhập tên rồi Continue',
             'b14 lấy và nhập OTP', 'b15 Create your Amazon account',
             'b16 Back ẩn hộp Google', 'b17 Create a passkey')
    return tuple(PostMenuStep(name, guarded(action)) for name, action in zip(
        names, (b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13,
                b14, b15, b16, b17)))
