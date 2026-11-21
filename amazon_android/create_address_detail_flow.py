"""Create-only address entry after Your Addresses; native UI with OCR fallback."""
from __future__ import annotations

import json
import os
from difflib import SequenceMatcher
from pathlib import Path
import re
import secrets
import threading
import time

from .account_flow import _bounds, _button, _read_hierarchy, _tap, _tap_for_transition, _text, _visible
from .cloud import cloud_adb
from .core import ToolError
from .marketplace_flow import (_account_tab, _foreground, _kind,
                               _navigation_ready, _read, _read_text_region, AUTH)
from .post_menu import AttemptDeadline, PostMenuStep


_prefix_lock = threading.Lock()
_prefix_file = Path(os.environ.get('LOCALAPPDATA', str(Path.home() / 'AppData/Local'))) / 'Swarmote' / 'address_prefixes.json'
_zip = re.compile(r'\b\d{5}(?:-\d{4})?\b')


def _new_prefix():
    """Reserve a search prefix across tool restarts without storing addresses."""
    with _prefix_lock:
        try:
            used = set(json.loads(_prefix_file.read_text(encoding='utf-8')))
        except FileNotFoundError:
            used = set()
        except (ValueError, OSError) as exc:
            raise ToolError('Không đọc được lịch sử số địa chỉ; giữ b28 để tránh trùng phiên') from exc
        available = [str(n) for n in range(100, 10000) if str(n) not in used]
        if not available:
            raise ToolError('Đã dùng hết số tìm địa chỉ 3–4 chữ số')
        prefix = secrets.choice(available)
        used.add(prefix)
        _prefix_file.parent.mkdir(parents=True, exist_ok=True)
        temporary = _prefix_file.with_suffix('.tmp')
        temporary.write_text(json.dumps(sorted(used)), encoding='utf-8')
        os.replace(temporary, _prefix_file)
        return prefix


def _has(nodes, label):
    return any(_visible(n) and _text(n).rstrip(':') == label for n in nodes)


def _find(nodes, label):
    matches = {n['bounds']: n for n in nodes if _visible(n) and _text(n).rstrip(':') == label}
    return next(iter(matches.values())) if len(matches) == 1 else None


def _action(nodes, label):
    try:
        return _button(nodes, label.title())
    except ToolError:
        target = _find(nodes, label)
        if target:
            return target
        candidates = [n for n in nodes if _visible(n) and label in _text(n)]
        return candidates[0] if candidates else None


def _addresses(nodes):
    return (_has(nodes, 'your addresses') and _has(nodes, 'add a new address')) or _has(nodes, 'add a new address')


def _search(nodes):
    return (_has(nodes, 'search for an address') and _has(nodes, 'enter an address manually')) or _has(nodes, 'enter an address manually')


def _form(nodes):
    return (_street_label(nodes) is not None and
            any(_has(nodes, label) for label in
                ('country/region', 'unit or suite number', 'zip code', 'city')))


def _street_label(nodes):
    labels = {'street address', 'address line 1', 'address line one',
              'street and number', 'house number and street'}
    matches = {n['bounds']: n for n in nodes if _visible(n) and
               _text(n).rstrip(':') in labels}
    return next(iter(matches.values())) if len(matches) == 1 else None


def _address_form(nodes):
    labels = {'street address', 'zip code', 'city', 'state', 'full name (first and last name)',
              'phone number', 'make this my default address', 'add address'}
    return _form(nodes) or sum(_has(nodes, label) for label in labels) >= 2


def _saved(nodes):
    return _has(nodes, 'address saved') or (_has(nodes, 'personal addresses') and
                                            _has(nodes, 'your addresses'))


def _street_field(nodes):
    label = _street_label(nodes)
    if label is None:
        return None
    bottom = _bounds(label)[3]
    following = [_bounds(n)[1] for n in nodes if _visible(n) and
                 _text(n).startswith(('unit or suite', 'apt, suite', 'zip code')) and
                 _bounds(n)[1] > bottom]
    limit = min(following, default=bottom + 85)
    fields = [n for n in nodes if _visible(n) and
              bottom - 5 <= _bounds(n)[1] and _bounds(n)[3] < limit and (
                  'street address or p.o. box' in _text(n) or
                  'enter street address' in _text(n) or
                  'address line 1' in _text(n) and n is not label or
                  'streetaddress' in n.get('resource-id', '').casefold())]
    if not fields:
        label = _street_label(nodes)
        if label:
            bottom = _bounds(label)[3]
            next_labels = [_bounds(n)[1] for n in nodes if _visible(n) and
                           _text(n).startswith(('unit or suite number', 'unit or suite',
                                                 'apt, suite', 'zip code')) and
                           _bounds(n)[1] > bottom]
            limit = min(next_labels, default=bottom + 70)
            fields = [n for n in nodes if _visible(n) and
                      n.get('class') == 'android.widget.EditText' and
                      bottom - 30 <= _bounds(n)[1] < limit]
    distinct = {n['bounds']: n for n in fields}
    if len(distinct) == 1:
        return next(iter(distinct.values()))
    if not distinct:
        label = _street_label(nodes)
        if label:
            bottom = _bounds(label)[3]
            next_labels = [_bounds(n)[1] for n in nodes if _visible(n) and
                           _text(n).startswith(('unit or suite number', 'unit or suite',
                                                 'apt, suite', 'zip code')) and
                           _bounds(n)[1] > bottom]
            limit = min(next_labels, default=bottom + 70)
            candidates = [n for n in nodes if _visible(n) and
                          ('edittext' in n.get('class', '').lower() or 'edit' in n.get('class', '').lower()) and
                          bottom - 30 <= _bounds(n)[1] < limit]
            if candidates:
                return candidates[0]
    return None


def _street_saved_field(nodes, bounds):
    label = _street_label(nodes)
    if not label or not bounds:
        return None
    bottom = _bounds(label)[3]
    next_labels = [_bounds(n)[1] for n in nodes if _visible(n) and
                   _text(n).startswith(('unit or suite number', 'unit or suite',
                                         'apt, suite', 'zip code')) and
                   _bounds(n)[1] > bottom]
    limit = min(next_labels, default=bottom + 70)
    return next((n for n in nodes if _visible(n) and n['bounds'] == bounds and
                 bottom - 30 <= _bounds(n)[1] < limit), None)


def _street_tap_target(nodes, field):
    label = _street_label(nodes)
    if not label:
        return None
    label_bottom = _bounds(label)[3]
    following = [_bounds(n)[1] for n in nodes if _visible(n) and
                 _text(n).startswith(('unit or suite', 'apt, suite', 'zip code')) and
                 _bounds(n)[1] > label_bottom]
    next_top = min(following, default=label_bottom + 85)
    if next_top - label_bottom < 20:
        return None
    x1, field_top, x2, field_bottom = _bounds(field)
    x = (x1 + x2) // 2
    if field_top >= label_bottom - 5 and field_bottom < next_top:
        y = (field_top + field_bottom) // 2
    else:
        y = label_bottom + min(30, (next_top - label_bottom) // 2)
    return {'bounds': f'[{x-1},{y-1}][{x+1},{y+1}]'}


def _street_focused(nodes):
    label = _street_label(nodes)
    if not label:
        return False
    bottom = _bounds(label)[3]
    following = [_bounds(n)[1] for n in nodes if _visible(n) and
                 _text(n).startswith(('unit or suite', 'apt, suite', 'zip code')) and
                 _bounds(n)[1] > bottom]
    limit = min(following, default=bottom + 85)
    return any(_visible(n) and n.get('focused') == 'true' and
               'edittext' in n.get('class', '').casefold() and
               bottom - 20 <= _bounds(n)[1] and _bounds(n)[3] < limit
               for n in nodes)


def _street_has_address(nodes, field):
    """Do not replace an address already entered in the Street field."""
    if field is None:
        return False
    value = _text(field)
    return bool(re.match(r'^\d{1,6}\s+[^\d\s].+', value) and
                'street address or p.o. box' not in value)


def _suggestions(nodes, field, prefix=None):
    if field is not None:
        bottom = _bounds(field)[3]
    else:
        street = _street_label(nodes)
        if street is None or not prefix:
            return []
        street_bottom = _bounds(street)[3]
        entered = [n for n in nodes if _visible(n) and _text(n) == prefix and
                   street_bottom - 15 <= _bounds(n)[1] < street_bottom + 80]
        if len({n['bounds'] for n in entered}) != 1:
            return []
        bottom = _bounds(entered[0])[3]
    following = [_bounds(n)[1] for n in nodes if _visible(n) and
                 _text(n).startswith(('unit or suite', 'zip code',
                                       'full name', 'phone number')) and
                 _bounds(n)[1] > bottom]
    limit = min(following, default=float('inf'))
    matches = {n['bounds']: n for n in nodes if _visible(n) and
               (field is None or n['bounds'] != field['bounds']) and
               bottom <= _bounds(n)[1] < limit and
               re.match(r'^\d{1,6}\s+\S*?[a-z]', _text(n))}
    return list(matches.values())


def _populated(nodes, field=None):
    if any(_visible(n) and _zip.fullmatch(_text(n)) for n in nodes):
        return True
    return bool(field and _has(nodes, 'zip code') and _has(nodes, 'city') and
                re.search(r'\d.*[a-z]|[a-z].*\d', _text(field)) and
                'street address or p.o. box' not in _text(field))


def _default_visual_label(nodes):
    """Find the text beside the checkbox without relying on an exact OCR line."""
    expected = 'makethismydefaultaddress'
    matches = [n for n in nodes if _visible(n) and n.get('vision') == 'true' and
               SequenceMatcher(None, expected,
                   ''.join(ch for ch in _text(n) if ch.isalnum())).ratio() >= .82]
    distinct = {n['bounds']: n for n in matches}
    return next(iter(distinct.values())) if len(distinct) == 1 else None


def _default_box_target(label):
    left, top, _, bottom = _bounds(label)
    center_x, center_y = left - 19, (top + bottom) // 2
    if center_x < 12:
        return None
    return {'bounds': f'[{center_x-1},{center_y-1}][{center_x+1},{center_y+1}]'}


def _scroll(phone, deadline):
    _foreground(phone, deadline)
    result = cloud_adb(phone, 'shell', 'wm', 'size', timeout=4).stdout
    sizes = re.findall(r'(?:Physical|Override) size:\s*(\d+)x(\d+)', result)
    if not sizes:
        raise ToolError('Chưa đọc được kích thước máy để cuộn địa chỉ')
    width, height = map(int, sizes[-1])
    cloud_adb(phone, 'shell', 'input', 'swipe', str(width // 2), str(int(height * .86)),
              str(width // 2), str(int(height * .18)), '350', timeout=5)


def build_create_address_detail_steps(phone, state):
    def run(number, outer, stop):
        if number in state.create_address_completed:
            return
        if number - 1 not in state.create_address_completed:
            raise ToolError(f'Chưa hoàn tất b{number-1} trên máy này')
        deadline = AttemptDeadline(min(120, outer.remaining()), notice=outer.notice)
        expires = time.monotonic() + min(120, outer.remaining())
        taps = 0
        reads_failed = 0
        visual_misses = 0
        # These screens are WebViews; their accessibility dump often blocks.
        # b28 still starts with native nodes because it must verify Street focus.
        # b29 has a direct OCR path below; a native dump adds delay.
        prefer_visual = number in {26, 27, 30}
        scrolls = 0
        outer.recovering(f'b{number}: đọc chữ cần bấm trên màn hiện tại')
        if number == 31:
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            _foreground(phone, deadline)
            try:
                tabs = _read_hierarchy(phone, AttemptDeadline(
                    min(4, deadline.remaining()), notice=outer.notice), stop)
            except ToolError:
                tabs = []
            target = _account_tab(phone, tabs, deadline)
            _tap(phone, target, deadline)
            state.create_address_completed.add(31)
            return
        if number == 28 and state.create_address_suggestion_tapped_at is not None:
            state.create_address_completed.add(28)
            return
        if number == 29:
            # The guided form starts with this square empty. Locate the label,
            # tap its adjacent square once, then let b30 find Add address.
            for attempt in range(4):
                if stop.is_set():
                    raise ToolError('Đã dừng máy này')
                try:
                    visual = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                   notice=outer.notice), stop, visual=True)
                except ToolError:
                    if stop.is_set():
                        raise
                    visual = []
                if _saved(visual):
                    state.create_address_completed.add(29)
                    return
                checkbox = _default_visual_label(visual)
                if checkbox is not None:
                    target = _default_box_target(checkbox)
                    if target is None:
                        raise ToolError('b29: chưa xác định được ô vuông cạnh chữ địa chỉ mặc định')
                    _foreground(phone, deadline)
                    _tap(phone, target, deadline)
                    state.create_address_completed.add(29)
                    return
                if attempt < 3:
                    _scroll(phone, deadline)
                    outer.recovering(f'b29: cuộn tìm ô cạnh Make this my default address ({attempt+1}/3)')
            raise ToolError('b29: chưa thấy chữ Make this my default address; giữ bước máy này')
        while time.monotonic() < expires:
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            if number == 28 and state.create_address_prefix_sent:
                try:
                    visual = _read_text_region(
                        phone, AttemptDeadline(min(18, deadline.remaining()),
                        notice=outer.notice), stop, (.20, .68))
                except ToolError:
                    if stop.is_set():
                        raise
                    visual = []
                choices = _suggestions(visual, None, state.create_address_prefix)
                if choices:
                    outer.recovering('b28: đã hiện địa chỉ gợi ý; chọn ngay')
                    _foreground(phone, deadline)
                    _tap(phone, secrets.choice(choices), deadline)
                    state.create_address_suggestion_tapped_at = time.monotonic()
                    state.create_address_completed.add(28)
                    return
                if _populated(visual):
                    state.create_address_completed.add(28)
                    return
                # OCR missed the list; the existing native read below can
                # recover a filled form without waiting for a fixed timer.
            # Read the current screen once, then fall back to the other backend.
            nodes = None
            if prefer_visual:
                try:
                    if number in {26, 27}:
                        nodes = _read_text_region(
                            phone, AttemptDeadline(min(18, deadline.remaining()),
                            notice=outer.notice), stop, (.05, .55))
                        if number == 26 and not (_form(nodes) or _addresses(nodes)):
                            nodes = None
                        if number == 27 and not (_form(nodes) or _search(nodes)):
                            nodes = None
                    else:
                        nodes = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                      notice=outer.notice), stop, visual=True)
                except ToolError:
                    pass
            if not nodes:
                try:
                    nodes = _read_hierarchy(phone, AttemptDeadline(
                        min(4, deadline.remaining()), notice=outer.notice), stop)
                except ToolError:
                    pass
            if not nodes and not prefer_visual:
                try:
                    outer.recovering(f'b{number}: chụp ảnh màn hình để quét chữ ấn luôn')
                    nodes = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                  notice=outer.notice), stop, visual=True)
                except ToolError:
                    pass
            if number == 27 and nodes and not (_form(nodes) or _search(nodes)):
                try:
                    visual = _read(phone, AttemptDeadline(min(12, deadline.remaining()),
                                   notice=outer.notice), stop, visual=True)
                    if _form(visual) or _search(visual):
                        nodes = visual
                except ToolError:
                    if stop.is_set():
                        raise
            if not nodes:
                reads_failed += 1
                if number == 26 and reads_failed in (1, 3):
                    try:
                        _foreground(phone, deadline)
                        size_out = cloud_adb(phone, 'shell', 'wm', 'size', timeout=4).stdout
                        dims = re.findall(r'(?:Physical|Override) size:\s*(\d+)x(\d+)', size_out)
                        if dims:
                            w, h = map(int, dims[-1])
                            outer.recovering('b26: bấm trực tiếp vị trí Add a new address')
                            cloud_adb(phone, 'shell', 'input', 'tap', str(w // 2), str(int(h * 0.185)), timeout=4)
                    except ToolError:
                        pass
                if reads_failed >= 6:
                    raise ToolError(f'b{number}: đọc cây Android lỗi {reads_failed} lần; giữ bước máy này')
                wait_s = min(1 + reads_failed, 4)
                outer.recovering(f'b{number}: mạng/màn chậm; đọc lại cây Android ({reads_failed}/6)')
                if stop.wait(wait_s):
                    raise ToolError('Đã dừng máy này')
                continue
            reads_failed = 0
            if number in {26, 27} and _kind(nodes) in AUTH:
                raise ToolError(f'b{number}: trở về xác minh tài khoản; giữ bước máy này')
            target = None
            if number == 26:
                if _search(nodes) or _form(nodes):
                    state.create_address_completed.add(number); return
                if _addresses(nodes) or _has(nodes, 'add a new address'):
                    target = _action(nodes, 'add a new address')
            elif number == 27:
                if _form(nodes):
                    state.create_address_completed.add(number); return
                if _search(nodes) or _has(nodes, 'enter an address manually'):
                    target = _action(nodes, 'enter an address manually')
            elif number == 28:
                if _form(nodes):
                    if _populated(nodes):
                        state.create_address_completed.add(number); return
                    field = _street_field(nodes)
                    if field is None:
                        field = _street_saved_field(nodes, state.create_address_street_bounds)
                    if field is None:
                        try:
                            visual = _read(phone, AttemptDeadline(min(8, deadline.remaining()),
                                           notice=outer.notice), stop, visual=True)
                            field = _street_field(visual)
                            if field is not None:
                                nodes = visual
                        except ToolError:
                            if stop.is_set():
                                raise
                    if _populated(nodes, field):
                        state.create_address_completed.add(number); return
                    if _street_has_address(nodes, field):
                        raise ToolError('b28: Street address đã có địa chỉ nhưng chưa xác nhận ZIP; '
                                        'giữ bước, không nhập mã sang ô khác')
                    if field is None:
                        outer.recovering('b28: form đang tải ô Street address; đọc lại')
                    else:
                        choices = _suggestions(nodes, field, state.create_address_prefix)
                        if choices:
                            outer.recovering('b28: đã thấy gợi ý địa chỉ; chọn ngay')
                            _foreground(phone, deadline)
                            _tap(phone, secrets.choice(choices), deadline)
                            state.create_address_suggestion_tapped_at = time.monotonic()
                            state.create_address_completed.add(28)
                            return
                        elif not state.create_address_prefix_sent or (
                                state.create_address_prefix_sent_at is not None and
                                time.monotonic() - state.create_address_prefix_sent_at >= 15 and
                                state.create_address_prefix_attempts < 3):
                            if state.create_address_prefix is None:
                                state.create_address_prefix = (
                                    state.create_address_proxy_prefix or _new_prefix())
                            elif (state.create_address_prefix_attempts >= 1 and
                                  state.create_address_proxy_prefix and
                                  state.create_address_prefix == state.create_address_proxy_prefix):
                                outer.recovering('b28: mã bưu chính chưa có gợi ý; chuyển sang số ngẫu nhiên dự phòng')
                                state.create_address_prefix = _new_prefix()
                            elif state.create_address_prefix_attempts >= 2:
                                state.create_address_prefix = _new_prefix()
                            _foreground(phone, deadline)
                            try:
                                visual = nodes if nodes and all(n.get('vision') == 'true' for n in nodes) else _read(phone, AttemptDeadline(
                                    min(12, deadline.remaining()), notice=outer.notice),
                                    stop, visual=True)
                                tap_field = _street_field(visual)
                                tap_target = (_street_tap_target(visual, tap_field)
                                              if tap_field is not None else None)
                            except ToolError:
                                if stop.is_set():
                                    raise
                                tap_target = None
                            if tap_target is None:
                                visual_misses += 1
                                if visual_misses >= 3:
                                    raise ToolError('b28: ảnh chưa xác định được ô Street address '
                                                    'sau ba lượt; không nhập sang Unit')
                                outer.recovering(f'b28: ảnh chưa rõ ô Street; chờ tải rồi chụp lại '
                                                 f'({visual_misses}/3)')
                                if stop.wait(2):
                                    raise ToolError('Đã dừng máy này')
                                continue
                            visual_misses = 0
                            _tap(phone, tap_target, deadline)
                            if state.create_address_prefix_sent:
                                cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_MOVE_END', timeout=4)
                                for _ in range(max(len(state.create_address_prefix or ''), 10)):
                                    cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_DEL', timeout=4)
                            state.create_address_street_bounds = tap_field['bounds']
                            cloud_adb(phone, 'shell', 'input', 'text', state.create_address_prefix,
                                      timeout=5)
                            state.create_address_prefix_sent = True
                            state.create_address_prefix_sent_at = time.monotonic()
                            state.create_address_prefix_attempts += 1
                            outer.recovering('b28: đã nhập số tìm kiếm; chờ gợi ý địa chỉ')
                        elif (state.create_address_prefix_sent_at is not None and
                              time.monotonic() - state.create_address_prefix_sent_at >= 15):
                            raise ToolError('b28: đã nhập lại cùng số nhưng chưa thấy gợi ý; giữ bước máy này')
                elif _saved(nodes):
                    state.create_address_completed.add(number); return
            elif number == 30:
                if _saved(nodes):
                    state.create_address_saved_at = time.monotonic()
                    state.create_address_completed.add(number); return
                target = _find(nodes, 'add address')
                if target is None and scrolls < 10:
                    _scroll(phone, deadline); scrolls += 1
                    outer.recovering(f'b30: cuộn tìm Add address ({scrolls}/10)')
                elif target is None:
                    raise ToolError('b30: đã cuộn 10 lần vẫn chưa thấy Add address')
                elif state.create_address_submit_attempts >= 2:
                    raise ToolError('b30: đã thử Add address hai lần nhưng chưa xác nhận lưu')
                elif state.create_address_submit_sent_at is not None and (
                        time.monotonic() - state.create_address_submit_sent_at < 10):
                    target = None  # Let the save result arrive before retrying.
            if target is not None:
                if taps >= 3:
                    raise ToolError(f'b{number}: đã bấm ba lần mà màn chưa đổi; giữ bước máy này')
                _foreground(phone, deadline)
                if number == 30:
                    state.create_address_submit_attempts += 1
                    state.create_address_submit_sent_at = time.monotonic()
                _tap_for_transition(phone, target, deadline)
                taps += 1
                outer.recovering(f'b{number}: đã bấm, đang đọc lại để xác nhận')
            wait_s = (.4 if number == 28 and state.create_address_prefix_sent and
                      target is None else 1 if target is None else .25)
            if stop.wait(wait_s):
                raise ToolError('Đã dừng máy này')
        raise ToolError(f'b{number}: quá 2 phút chưa xác nhận được màn đích; giữ bước máy này')

    return tuple(PostMenuStep(name, lambda job, deadline, stop, n=number:
                              run(n, deadline, stop)) for number, name in (
        (26, 'b26 Add a new address'), (27, 'b27 Enter an address manually'),
        (28, 'b28 chọn gợi ý địa chỉ'), (29, 'b29 chọn địa chỉ mặc định'),
        (30, 'b30 Add address'), (31, 'b31 mở hình người')))
