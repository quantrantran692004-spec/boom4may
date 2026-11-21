"""Create-only gift card reload, card, and billing address, b32–b39."""
from __future__ import annotations

import math
import re
import time

from .account_flow import _bounds, _tap, _text, _visible
from .bulk_input import validate_card
from .cloud import cloud_adb
from .core import ToolError
from .marketplace_flow import _foreground, _read, _read_text_region
from .post_menu import AttemptDeadline, PostMenuStep


def _find(nodes, *labels):
    matches = {n['bounds']: n for n in nodes if _visible(n) and
               any(_text(n).rstrip(':') == label or _text(n).startswith(label)
                   for label in labels)}
    return next(iter(matches.values())) if len(matches) == 1 else None


def _target_crop(labels):
    if 'reload balance' in labels:
        return (.15, .85)
    if 'buy now' in labels:
        return (.30, .95)
    if 'add a credit or debit card' in labels:
        return (.20, .65)
    if 'add and continue' in labels:
        return (.55, .98)
    if 'use this address' in labels:
        return (.05, .50)
    return None


def _read_until(phone, deadline, stop, *labels, attempts=5):
    crop = _target_crop(labels)
    for attempt in range(attempts):
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        # Search only the part of the current image where this label appears.
        # Its bounds remain in full-screen coordinates for the immediate tap.
        if crop is not None:
            try:
                nodes = _read_text_region(phone, deadline, stop, crop)
                target = _find(nodes, *labels)
                if target:
                    return nodes, target
            except ToolError:
                if stop.is_set():
                    raise
        # A single cropped miss returns to the calling step so it can scroll
        # again without a full-screen or native WebView read.
        if crop is None or attempts != 1:
            for visual in ((True, False) if attempt == 0 else (() if crop else (True,))):
                try:
                    nodes = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                  notice=deadline.notice), stop, visual=visual)
                    target = _find(nodes, *labels)
                    if target:
                        return nodes, target
                except ToolError:
                    if stop.is_set():
                        raise
        deadline.recovering('Màn đang tải; đọc lại chữ đang hiện')
        if attempt + 1 < attempts and stop.wait(min(.5, deadline.remaining())):
            raise ToolError('Đã dừng máy này')
    raise ToolError('Chưa thấy mục cần bấm trên màn hiện tại; giữ bước máy này')


def _swipe(phone, deadline, *, short=False):
    _foreground(phone, deadline)
    result = cloud_adb(phone, 'shell', 'wm', 'size', timeout=4).stdout
    sizes = re.findall(r'(?:Physical|Override) size:\s*(\d+)x(\d+)', result)
    if not sizes:
        raise ToolError('Chưa đọc được kích thước màn hình để cuộn')
    width, height = map(int, sizes[-1])
    cloud_adb(phone, 'shell', 'input', 'swipe', str(width // 2),
              str(round(height * (.72 if short else .78))), str(width // 2),
              str(round(height * (.43 if short else .24))),
              '320' if short else '400', timeout=5)


def _card_parts(job):
    if job is None or job.account is None or not job.account.card:
        raise ToolError('Máy này chưa có thẻ để nhập; giữ b38')
    number, month, year = validate_card(job.account.card).split('|')
    return number, f'{int(month):02d}/{year[-2:]}', job.account.full_name.strip()


def _field_target(nodes, label, next_label, placeholders):
    headings = [n for n in nodes if _visible(n) and _text(n).rstrip(':') == label]
    heading = min(headings, key=lambda n: _bounds(n)[1]) if headings else None
    following = _find(nodes, next_label) if next_label else None
    if heading is None:
        return None
    x1, _, x2, bottom = _bounds(heading)
    next_top = _bounds(following)[1] if following else bottom + 105
    if next_top - bottom < 18:
        return None
    candidates = [n for n in nodes if _visible(n) and
                  bottom <= _bounds(n)[1] < next_top and
                  any(_text(n).startswith(p) for p in placeholders)]
    distinct = {n['bounds']: n for n in candidates}
    if len(distinct) == 1:
        return next(iter(distinct.values()))
    if distinct:
        return None
    # OCR can miss faint placeholders. Tap inside the single row below its label.
    x = (x1 + x2) // 2
    y = bottom + min(30, (next_top - bottom) // 2)
    return {'bounds': f'[{x-1},{y-1}][{x+1},{y+1}]'}


def _input(phone, target, value, deadline):
    _foreground(phone, deadline)
    _tap(phone, target, deadline)
    cloud_adb(phone, 'shell', 'input', 'text', value.replace(' ', '%s'),
              timeout=max(5, math.ceil(min(15, deadline.remaining()))))


def build_reload_payment_steps(phone, state):
    def step(number, job, outer, stop):
        if number in state.reload_completed:
            return
        if number == 32:
            if 31 not in state.create_address_completed:
                raise ToolError('Chưa bấm hình người ở b31')
        elif number - 1 not in state.reload_completed and not (
                number == 36 and 34 in state.reload_completed):
            raise ToolError(f'Chưa xong bước trước b{number}')
        deadline = AttemptDeadline(min(120, outer.remaining()), notice=outer.notice)
        if number == 32:
            _swipe(phone, deadline)
        elif number == 33:
            for attempt in range(4):
                try:
                    _, target = _read_until(phone, deadline, stop,
                                            'reload balance', attempts=1)
                except ToolError:
                    if stop.is_set():
                        raise
                    if attempt == 3:
                        raise ToolError('b33: đã cuộn tìm nhưng chưa thấy Reload Balance')
                    deadline.recovering('b33: chưa thấy Reload Balance; cuộn xuống tìm tiếp')
                    _swipe(phone, deadline)
                    continue
                _foreground(phone, deadline)
                _tap(phone, target, deadline)
                break
        elif number == 34:
            # Reload Balance was tapped in b33. Scroll the new page immediately.
            _swipe(phone, deadline, short=True)
        elif number == 36:
            # Search only after the immediate b34 swipe; tap on the first match.
            for attempt in range(4):
                try:
                    _, target = _read_until(phone, deadline, stop,
                                            'buy now', attempts=1)
                except ToolError:
                    if stop.is_set():
                        raise
                    if attempt == 3:
                        raise ToolError('b36: đã cuộn tìm nhưng chưa thấy Buy Now')
                    deadline.recovering('b36: chưa thấy Buy Now; cuộn xuống tìm tiếp')
                    _swipe(phone, deadline, short=True)
                    continue
                _foreground(phone, deadline)
                _tap(phone, target, deadline)
                break
        elif number == 37:
            _, target = _read_until(phone, deadline, stop,
                                    'add a credit or debit card')
            _foreground(phone, deadline)
            _tap(phone, target, deadline)
        elif number == 38:
            number_text, expiry, name = _card_parts(job)
            if not name:
                raise ToolError('Máy này thiếu tên trên thẻ; giữ b38')
            fields = (('card number', 'expiration date', ('card number',), number_text),
                      ('expiration date', 'name on card', ('mm / yy', 'mm/yy'), expiry),
                      ('name on card', 'add and continue',
                       ('first and last name', 'name on card'), name))
            for index, (label, following, placeholders, value) in enumerate(fields):
                if index in state.reload_card_fields_sent:
                    continue
                for attempt in range(5):
                    try:
                        nodes = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                      notice=outer.notice), stop, visual=True)
                        target = _field_target(nodes, label, following, placeholders)
                        if target:
                            break
                    except ToolError:
                        if stop.is_set():
                            raise
                    if stop.wait(min(2, deadline.remaining())):
                        raise ToolError('Đã dừng máy này')
                else:
                    raise ToolError(f'b38: chưa xác định được ô {label}; chưa nhập thẻ')
                _input(phone, target, value, deadline)
                state.reload_card_fields_sent.add(index)
            _, target = _read_until(phone, deadline, stop, 'add and continue')
            _foreground(phone, deadline)
            _tap(phone, target, deadline)
        elif number == 39:
            _, target = _read_until(phone, deadline, stop, 'use this address')
            _tap(phone, target, deadline)
        state.reload_completed.add(number)

    return tuple(PostMenuStep(label, lambda job, deadline, stop, n=number:
                              step(n, job, deadline, stop)) for number, label in (
        (32, 'b32 cuộn cuối trang hình người'),
        (33, 'b33 Reload Balance'),
        (34, 'b34 cuộn ngay sau Reload Balance'),
        (36, 'b36 Buy Now'),
        (37, 'b37 thêm phương thức thanh toán'),
        (38, 'b38 nhập thẻ và Add and continue'),
        (39, 'b39 Use this address')))
