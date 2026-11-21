"""Create-only continuation: Account, find Your Addresses, open it."""
from __future__ import annotations

import time
import re

from .account_flow import _tap_for_transition, _text, _visible
from .cloud import cloud_adb
from .core import ToolError
from .marketplace_flow import _read_text_region
from .post_menu import AttemptDeadline, PostMenuStep


def _account_content(nodes):
    labels = {_text(n) for n in nodes if _visible(n)}
    return bool(labels & {'orders', 'your orders', 'buy again', 'account settings',
                          'your amazon highlights', 'your lists', 'lists',
                          'your payments', 'your account'} or
                any(label.startswith('gift card balance') for label in labels))


def build_create_address_steps(phone, state):
    def run(number, outer, stop):
        if number in state.create_address_completed:
            return
        if 22 not in state.marketplace_completed:
            raise ToolError('Chưa hoàn tất b22 trên máy này')
        if number > 23 and number - 1 not in state.create_address_completed:
            raise ToolError(f'Chưa hoàn tất b{number-1} trên máy này')
        if number == 23:
            # Keep the original three-second pause after b22, including across
            # Stop/Continue. Once the word Account appears, tap that word.
            ready_at = state.create_address_wait_until.setdefault(
                23, time.monotonic() + 3)
            outer.recovering('b23: chờ đủ 3 giây sau b22 rồi tìm chữ Account')
            if stop.wait(max(0, ready_at - time.monotonic())):
                raise ToolError('Đã dừng máy này')
            deadline = AttemptDeadline(min(120, outer.remaining()), notice=outer.notice)
            for _ in range(32):
                if stop.is_set():
                    raise ToolError('Đã dừng máy này')
                try:
                    nodes = _read_text_region(phone, deadline, stop, (.08, .30))
                except ToolError:
                    if stop.is_set():
                        raise
                    nodes = []
                matches = {n['bounds']: n for n in nodes if _visible(n) and
                           _text(n) == 'account'}
                if len(matches) == 1:
                    target = next(iter(matches.values()))
                    outer.recovering('b23: đã thấy chữ Account, bấm ngay')
                    _tap_for_transition(phone, target, deadline)
                    state.create_address_completed.add(23)
                    state.create_address_wait_until.pop(23, None)
                    return
                if stop.wait(min(.5, deadline.remaining())):
                    raise ToolError('Đã dừng máy này')
            raise ToolError('b23: chưa thấy duy nhất chữ Account; giữ bước máy này')
        deadline = AttemptDeadline(min(120, outer.remaining()), notice=outer.notice)
        outer.recovering(f'b{number}: chụp ảnh tìm chữ Your Addresses')
        last_rows = None
        unchanged = 0
        scrolls = 0
        backs = 0
        size = None
        for _ in range(32):
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            try:
                nodes = _read_text_region(phone, deadline, stop, (.05, .95))
            except ToolError:
                if stop.is_set():
                    raise
                outer.recovering(f'b{number}: chưa chụp/đọc được chữ; thử lại')
                if stop.wait(min(.5, deadline.remaining())):
                    raise ToolError('Đã dừng máy này')
                continue
            addresses = {n['bounds']: n for n in nodes if _visible(n) and
                         _text(n) == 'your addresses'}
            if len(addresses) == 1:
                if number == 24:
                    outer.recovering('b24: đã thấy chữ Your Addresses')
                    state.create_address_completed.add(24)
                    return
                outer.recovering('b25: đã thấy chữ Your Addresses, bấm ngay')
                _tap_for_transition(phone, next(iter(addresses.values())), deadline)
                state.create_address_completed.add(25)
                return
            rows = tuple(_text(n) for n in nodes if _visible(n) and _text(n))
            unchanged = unchanged + 1 if rows == last_rows else 0
            last_rows = rows
            if scrolls and not _account_content(nodes):
                if backs:
                    raise ToolError(f'b{number}: đã Back khỏi trang chen vào nhưng '
                                    'chưa thấy Your Addresses; giữ bước máy này')
                cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_BACK', timeout=4)
                backs += 1
                scrolls = 0
                outer.recovering(f'b{number}: trang chen vào sau Account; Back rồi chụp lại')
                if stop.wait(min(.25, deadline.remaining())):
                    raise ToolError('Đã dừng máy này')
                continue
            if scrolls >= 10:
                raise ToolError(f'b{number}: cuộn 10 lần chưa thấy Your Addresses; giữ bước máy này')
            if size is None:
                result = cloud_adb(phone, 'shell', 'wm', 'size', timeout=4).stdout
                dimensions = re.findall(r'(?:Physical|Override) size:\s*(\d+)x(\d+)', result)
                if not dimensions:
                    raise ToolError(f'b{number}: chưa đọc được kích thước màn hình')
                size = tuple(map(int, dimensions[-1]))
            width, height = size
            reverse = unchanged >= 2
            cloud_adb(phone, 'shell', 'input', 'swipe', str(width // 2),
                      str(int(height * (.38 if reverse else .75))), str(width // 2),
                      str(int(height * (.55 if reverse else .32))),
                      '650' if reverse else '400', timeout=5)
            scrolls += 1
            outer.recovering(f'b{number}: chưa thấy Your Addresses; '
                             f'cuộn rồi chụp lại ({scrolls}/10) '
                             f'({"vuốt ngược nhẹ" if reverse else "cuộn xuống"})')
            if stop.wait(min(.25, deadline.remaining())):
                raise ToolError('Đã dừng máy này')
        raise ToolError(f'b{number}: chưa thấy chữ Your Addresses; giữ bước máy này')

    return tuple(PostMenuStep(name, lambda job, deadline, stop, n=number:
                              run(n, deadline, stop)) for number, name in (
        (23, 'b23 mở Account'), (24, 'b24 tìm Your Addresses'),
        (25, 'b25 mở Your Addresses')))
