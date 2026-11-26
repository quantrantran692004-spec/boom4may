"""Shared b16–b22: account tab, United States marketplace, Done, account tab.

The marketplace picker is separate from b6's telephone country-code picker.
All observations and dispatch markers belong to the supplied phone/session.
"""
from __future__ import annotations

import math
import re
import time

from .account_flow import (_bounds, _button, _read_hierarchy, _read_nodes_once,
                           _read_visual_nodes, _tap_for_transition, _text, _visible)
from .cloud import cloud_adb, amazon_is_foreground
from .core import ToolError
from .post_menu import AttemptDeadline, PostMenuStep


COUNTRIES = {'australia', 'belgium (belgique)', 'canada', 'germany (deutschland)',
             'egypt', 'spain (españa)', 'france', 'india', 'ireland', 'south africa',
             'sweden (sverige)', 'united arab emirates', 'united kingdom',
             'united states', 'japan (日本)', 'brazil (brasil)', 'mexico (méxico)',
             'poland (polska)'}
AUTH = {'SMS', 'WHATSAPP', 'IDENTIFIER', 'COUNTRY', 'CREATE_FORM', 'NEW_ACCOUNT'}


def marketplace_screen(nodes):
    labels = {_text(n).replace('&', 'and').rstrip(':') for n in nodes}
    if any('country/region and language' == label for label in labels):
        return 'MARKET_SETTINGS'
    if (any(label.startswith('countries/regions available') for label in labels) or
            len(labels & COUNTRIES) >= 2):
        return 'MARKET_COUNTRIES'
    if ('your orders' in labels and 'orders' in labels and
            ('account' in labels or 'lists' in labels)):
        return 'ACCOUNT'
    return 'UNKNOWN'


def _one(nodes, predicate, description):
    matches = {n['bounds']: n for n in nodes if _visible(n) and predicate(n)}
    if len(matches) != 1:
        raise ToolError(f'Chưa xác định duy nhất {description} trên máy này')
    return next(iter(matches.values()))


def _resolve(locator, nodes):
    try:
        return locator(nodes)
    except ToolError:
        return None


def _text_recovery_kind(nodes):
    """Recognize the locale entry even when surrounding account panels differ."""
    kind = _kind(nodes)
    if kind == 'UNKNOWN' and not _search_active(nodes) and _resolve(_locale_button, nodes):
        return 'ACCOUNT'
    return kind


def _size(phone, deadline):
    result = cloud_adb(phone, 'shell', 'wm', 'size',
                       timeout=max(1, math.ceil(min(4, deadline.remaining()))))
    matches = re.findall(r'(?:Physical|Override) size:\s*(\d+)x(\d+)', result.stdout)
    if not matches:
        raise ToolError('Chưa đọc được kích thước Android của máy này')
    return tuple(map(int, matches[-1]))


def _foreground(phone, deadline):
    if not amazon_is_foreground(phone,
            timeout=max(1, math.ceil(min(4, deadline.remaining()))), adb=cloud_adb):
        raise ToolError('Amazon chưa ở phía trước; giữ nguyên máy này')


def _read_navigation_nodes(phone, deadline, stop):
    """Return native navigation immediately, without waiting for OCR or content."""
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    try:
        nodes = _read_hierarchy(phone, deadline, stop)
    except ToolError:
        if stop.is_set():
            raise
        nodes = []
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    if nodes and (_navigation_ready(nodes) or _kind(nodes) != 'UNKNOWN' or
                  _resolve(_locale_button, nodes)):
        return nodes
    try:
        return _read_visual_nodes(phone, deadline, stop)
    except ToolError:
        if stop.is_set() or not nodes:
            raise
        return nodes


def _read(phone, deadline, stop, *, visual=False, navigation=False):
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    budget = AttemptDeadline(min(12, deadline.remaining()), notice=deadline.notice)
    if visual:
        from .isolated_reader import current
        reader = current(phone.serial)
        if reader is not None:
            return reader.call('visual', budget.remaining(), stop)
        return _read_visual_nodes(phone, budget, stop)
    if navigation:
        from .isolated_reader import current
        reader = current(phone.serial)
        if reader is not None:
            return reader.call('navigation', budget.remaining(), stop)
        return _read_navigation_nodes(phone, budget, stop)
    return _read_nodes_once(phone, budget, stop)


def _read_text_region(phone, deadline, stop, crop, *, direct_visual=False):
    """Read only visible text in a screen region, keeping original tap bounds."""
    from .isolated_reader import current

    budget = AttemptDeadline(min(45 if direct_visual else 18, deadline.remaining()),
                             notice=deadline.notice)
    if direct_visual:
        # The address WebView uses the two bounded OCR engines in this process
        # rather than cold-starting one OCR process per phone at b28.
        return _read_visual_nodes(phone, budget, stop, crop=crop, text_only=True)
    reader = current(phone.serial)
    if reader is not None:
        return reader.call('visual_text', budget.remaining(), stop, crop=crop)
    return _read_visual_nodes(phone, budget, stop, crop=crop, text_only=True)


def _pause(stop, seconds):
    if stop.wait(seconds):
        raise ToolError('Đã dừng máy này')


def _kind(nodes):
    from .account_flow import screen
    return screen(nodes)


def _tab_label(node):
    return ' '.join((node.get('content-desc') or _text(node)).split()).casefold()


def _is_account_tab(node):
    if _tab_label(node).startswith(('your account tab', 'account tab', 'you tab', 'profile tab')):
        return True
    resource = node.get('resource-id', '').rsplit('/', 1)[-1].casefold()
    return resource in {'account_tab', 'you_tab', 'profile_tab', 'tab_account',
                        'tab_you', 'tab_profile', 'bottom_nav_account',
                        'bottom_nav_you', 'bottom_nav_profile'}


def _search_active(nodes):
    labels = {_text(n) for n in nodes if _visible(n)}
    if labels & {'search with photo', 'search with camera'}:
        return True
    return any(_visible(n) and n.get('class') == 'android.widget.EditText' and
               n.get('focused') == 'true' and
               ('search' in _tab_label(n) or 'search' in n.get('resource-id', '').casefold())
               for n in nodes)


def _navigation_ready(nodes):
    if _search_active(nodes):
        return False  # The keyboard/search overlay occupies the old tab coordinates.
    if any(_visible(n) and (_is_account_tab(n) or _tab_label(n).startswith(
            ('home tab', 'cart tab', 'browse menu tab', 'your account tab',
             'account tab', 'you tab', 'profile tab'))) for n in nodes):
        return True
    # OCR cannot name a bare icon. A live Browse menu still anchors its tab bar.
    return _kind(nodes) == 'MENU' or any(
        'looking for the app settings' in _text(n) for n in nodes)


def _account_tab(phone, nodes, deadline):
    label = _tab_label
    matches = [n for n in nodes if _visible(n) and _is_account_tab(n)]
    if matches:
        return _one(matches, lambda n: True, 'tab hình người')
    # Anchor the icon to live bottom tabs when accessibility omits its label.
    tabs = [n for n in nodes if _visible(n) and any(label(n).startswith(prefix)
            for prefix in ('home tab', 'cart tab', 'browse menu tab'))]
    width, height = _size(phone, deadline)
    x = width * 0.375
    if tabs:
        y = sum((_bounds(n)[1] + _bounds(n)[3]) / 2 for n in tabs) / len(tabs)
        centers = {}
        for prefix in ('home tab', 'cart tab', 'browse menu tab'):
            values = {(_bounds(n)[0] + _bounds(n)[2]) / 2 for n in tabs
                      if label(n).startswith(prefix)}
            if len(values) == 1:
                centers[prefix] = next(iter(values))
        if 'home tab' in centers and 'cart tab' in centers:
            x = (centers['home tab'] + centers['cart tab']) / 2
        elif 'home tab' in centers and 'browse menu tab' in centers:
            x = centers['home tab'] + (centers['browse menu tab'] - centers['home tab']) / 3
        elif 'cart tab' in centers and 'browse menu tab' in centers:
            x = 2 * centers['cart tab'] - centers['browse menu tab']
    else:
        y = height * 0.925  # Documented bottom tab on this phone, above system navigation.
    if not (0 < x < width and 0 < y < height):
        raise ToolError('Thanh tab hình người chưa có vị trí hợp lệ trên máy này')
    return {'bounds': f'[{int(x)-1},{int(y)-1}][{int(x)+1},{int(y)+1}]'}


def _locale_button(nodes):
    return _one(nodes, lambda n: (
        _text(n) == 'en' or
        bool(re.search(r'\ben$', _text(n))) or
        _text(n) in {'country and language', 'country/region and language',
                     'change country or region', 'country/region & language'}),
        'nút cờ quốc gia / EN')


def _en_button(nodes):
    return _one(nodes, lambda n: bool(re.search(r'(?:^|\s)en$', _text(n))) and
                len(_text(n)) <= 8, 'nút EN')


def _country_card(nodes):
    language = [_bounds(n)[1] for n in nodes if _visible(n) and
                (_text(n).startswith('language') or _text(n) == 'english')]
    boundary = min(language, default=float('inf'))
    return _one(nodes, lambda n: _bounds(n)[1] < boundary and
                (_text(n).startswith('country/region:') or
                 _text(n).rstrip(':') == 'country/region'), 'ô Country/Region')


def _us_selected(nodes):
    if marketplace_screen(nodes) != 'MARKET_SETTINGS':
        return False
    language = [_bounds(n)[1] for n in nodes if _visible(n) and
                (_text(n).startswith('language') or _text(n) == 'english')]
    boundary = min(language, default=0)
    return any(_visible(n) and _bounds(n)[1] < boundary and
               (_text(n) == 'united states' or
                ('country/region' in _text(n) and 'united states' in _text(n))) for n in nodes)


def _us_row(nodes):
    return _button(nodes, 'United States')


def _destination(nodes):
    return bool(nodes) and _kind(nodes) not in AUTH | {'MARKET_SETTINGS', 'MARKET_COUNTRIES'} and (
        _kind(nodes) in {'ACCOUNT', 'MENU'} or _navigation_ready(nodes) or (len(nodes) >= 4 and any(
            _text(n).startswith('search amazon') for n in nodes)))


def _scroll_country(phone, deadline, reverse=False):
    _foreground(phone, deadline)
    width, height = _size(phone, deadline)
    cloud_adb(phone, 'shell', 'input', 'swipe', str(width//2),
              str(int(height*(0.32 if reverse else 0.76))), str(width//2),
              str(int(height*(0.58 if reverse else 0.28))), '650', timeout=5)


def build_marketplace_steps(phone, state):
    """One common b16–b22 implementation for Create, Login and q7."""
    def run(number, outer, stop):
        if number in state.marketplace_completed:
            return
        if not {12, 13, 14, 15} <= state.tail_completed:
            raise ToolError('Chưa hoàn tất b12–b15 của máy này')
        if number > 16 and number - 1 not in state.marketplace_completed:
            raise ToolError(f'Chưa hoàn tất b{number-1} trên máy này')
        deadline = AttemptDeadline(75, notice=outer.notice)
        expires = time.monotonic() + min(75, outer.remaining())
        next_tap = ((state.marketplace_done_at + 20)
                    if number == 21 and state.marketplace_done_at is not None else 0.0)
        taps = 0
        stable_destination = 0
        read_failures = 0
        focus_failures = 0
        scrolls = 0
        navigation_backs = 0
        previous_rows = None
        unchanged = 0
        pending_text_nodes = None
        missing_targets = 0
        stalled_nav_reads = 0
        country_text_fallback_used = False

        def foreground_ready():
            nonlocal focus_failures
            try:
                _foreground(phone, deadline)
                focus_failures = 0
                return True
            except ToolError:
                if stop.is_set():
                    raise
                focus_failures += 1
                if focus_failures >= 3:
                    raise
                outer.recovering('Đang kiểm tra lại focus Android của máy này')
                _pause(stop, 2)
                return False

        def back_and_read_text():
            nonlocal navigation_backs, next_tap, pending_text_nodes
            if navigation_backs >= 3:
                raise ToolError('Chưa khôi phục được điều hướng sau ba lần Back; giữ bước máy này')
            if not foreground_ready():
                return None
            _pause(stop, 0)
            cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_BACK', timeout=4)
            navigation_backs += 1
            next_tap = time.monotonic() + 2
            outer.recovering(f'b{number}: dự phòng Back rồi đọc chữ trên ảnh mới '
                             f'({navigation_backs}/3)')
            _pause(stop, 0.5)
            if not foreground_ready():
                return None
            try:
                fresh = _read(phone, deadline, stop,
                              navigation=number in {16, 22}, visual=number not in {16, 22})
                if number in {16, 22} and not _navigation_ready(fresh):
                    fresh = _read(phone, deadline, stop, visual=True)
            except ToolError:
                if stop.is_set():
                    raise
                return None  # Keep the original reader as fallback on the next iteration.
            if _kind(fresh) in AUTH:
                raise ToolError('Back tới form xác minh; giữ bước máy này, không phát lại xác minh')
            pending_text_nodes = fresh
            return fresh

        def account_target(nodes):
            nonlocal next_tap, pending_text_nodes, stalled_nav_reads
            if _navigation_ready(nodes):
                stalled_nav_reads = 0
                if number == 22 and taps == 0:
                    next_tap = 0.0  # A newly visible tab need not finish a Back/Reload wait.
                return _account_tab(phone, nodes, deadline)
            labels = {_text(n) for n in nodes if _visible(n) and _text(n)}
            if (not _search_active(nodes) and (len(labels) < 2 or any(
                    label.startswith(('loading', 'please wait')) for label in labels))):
                stalled_nav_reads += 1
                if stalled_nav_reads < (6 if number == 22 else 2) or not nodes:
                    return None
                # A persistent loading page can cover the bottom tabs; Back
                # exposes the live Android navigation instead of waiting 75s.
            else:
                stalled_nav_reads = 0
            if time.monotonic() < next_tap:
                return None
            fresh = back_and_read_text()
            if fresh and _navigation_ready(fresh):
                pending_text_nodes = None  # This fresh frame is used for the tap below.
                if number == 22 and taps == 0:
                    next_tap = 0.0
                return _account_tab(phone, fresh, deadline)
            return None

        def recover_country_list():
            nonlocal country_text_fallback_used, scrolls, previous_rows, unchanged
            if country_text_fallback_used or state.marketplace_done_sent:
                return False
            if back_and_read_text() is None:
                return False
            country_text_fallback_used = True
            scrolls, previous_rows, unchanged = 0, None, 0
            return True

        outer.recovering('b16: b15 đã xem xong · tìm tab hình người và thấy là mở ngay'
                         if number == 16 else
                         'b17: tìm cờ/EN · thấy là mở ngay' if number == 17 else
                         'b22: đang tìm tab hình người · thấy là mở ngay' if number == 22 else
                         f'b{number}: đang đọc màn và chờ Amazon tải')
        if number == 17:
            # Keep the viewing interval from b16's person-tab tap across Stop/Resume.
            tapped_at = state.marketplace_person_tapped_at
            if tapped_at is not None:
                remaining = tapped_at + 10 - time.monotonic()
                if remaining > 0:
                    outer.recovering('b17: chờ đủ 10 giây sau tab hình người rồi bấm EN')
                    _pause(stop, remaining)
            # EN alone is the target; do not require an Account page layout.
            try:
                en_nodes = _read_text_region(phone, deadline, stop, (.08, .25))
                en_target = _resolve(_en_button, en_nodes)
            except ToolError:
                if stop.is_set():
                    raise
                en_target = None
            if en_target is not None:
                if stop.is_set():
                    raise ToolError('Đã dừng máy này')
                _tap_for_transition(phone, en_target, deadline)
                state.marketplace_completed.add(17)
                return
        while time.monotonic() < expires:
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            try:
                if pending_text_nodes is not None:
                    nodes, pending_text_nodes = pending_text_nodes, None
                    kind = _text_recovery_kind(nodes)
                    if number == 17 and _resolve(_locale_button, nodes) is not None:
                        next_tap = 0.0  # Fresh post-Back frame already shows EN.
                else:
                    nodes = (_read(phone, deadline, stop, navigation=True)
                             if number in {16, 17, 22} or (number == 21 and state.marketplace_done_sent)
                             else _read(phone, deadline, stop))
                    kind = _text_recovery_kind(nodes) if number == 17 else _kind(nodes)
                read_failures = 0
            except ToolError:
                if stop.is_set():
                    raise
                read_failures += 1
                if read_failures >= 3:
                    raise ToolError('Đọc màn máy này lỗi ba lần; kiểm tra kết nối rồi Tiếp tục')
                _pause(stop, 2)
                continue
            if kind in AUTH:
                raise ToolError('Máy này còn/đã quay về xác minh tài khoản; không đổi quốc gia')
            target = None
            if number in {16, 22}:
                if number == 16 and kind in {'MARKET_SETTINGS', 'MARKET_COUNTRIES'}:
                    state.marketplace_completed.add(number)
                    return  # The user already advanced this machine.
                if number == 16 and kind == 'ACCOUNT':
                    if state.marketplace_person_tapped_at is None:
                        state.marketplace_person_tapped_at = time.monotonic()
                    state.marketplace_completed.add(number)
                    return
                if number == 22 and taps > 0 and kind == 'ACCOUNT':
                    state.marketplace_completed.add(number)
                    return
                if nodes and (number == 22 or kind not in {'MARKET_SETTINGS', 'MARKET_COUNTRIES'}):
                    target = account_target(nodes)
            elif number in {17, 18}:
                if kind == 'MARKET_COUNTRIES' or (number == 17 and kind == 'MARKET_SETTINGS'):
                    state.marketplace_completed.add(number)
                    return
                if number == 18 and _us_selected(nodes):
                    state.marketplace_completed.add(number)
                    return
                if number == 17 and nodes and not _search_active(nodes):
                    # Native navigation can be ready while the locale control is
                    # absent from accessibility. Read its visible EN text before
                    # treating this frame as a page that needs recovery.
                    target = _resolve(_locale_button, nodes)
                    if target is None:
                        try:
                            visual = _read(phone, deadline, stop, visual=True)
                            if _kind(visual) not in AUTH and not _search_active(visual):
                                target = _resolve(_locale_button, visual)
                                if target is not None:
                                    nodes, kind = visual, _text_recovery_kind(visual)
                        except ToolError:
                            if stop.is_set():
                                raise
                if target is None and kind in {'ACCOUNT', 'MARKET_SETTINGS'}:
                    try:
                        target = _country_card(nodes) if kind == 'MARKET_SETTINGS' else _locale_button(nodes)
                    except ToolError:
                        try:
                            nodes = _read(phone, deadline, stop, visual=True)
                            target = _country_card(nodes) if _kind(nodes) == 'MARKET_SETTINGS' else _locale_button(nodes)
                        except ToolError:
                            target = None
                elif nodes and target is None:
                    target = account_target(nodes)
            elif number in {19, 20}:
                if _us_selected(nodes):
                    state.marketplace_completed.add(number)
                    return
                if kind == 'MARKET_COUNTRIES':
                    try:
                        target = _us_row(nodes)
                    except ToolError:
                        if scrolls >= 16:
                            if recover_country_list():
                                continue
                            raise ToolError('Chưa thấy United States sau khi cuộn; giữ nguyên máy để Tiếp tục')
                        rows = tuple(sorted(_text(n) for n in nodes if _text(n) in COUNTRIES))
                        unchanged = unchanged + 1 if rows and rows == previous_rows else 0
                        previous_rows = rows
                        _scroll_country(phone, deadline, reverse=unchanged >= 2)
                        scrolls += 1
                        _pause(stop, 1)
                        continue
                    if number == 19:
                        state.marketplace_completed.add(number)
                        return  # b19 finds; b20 selects.
                elif kind == 'MARKET_SETTINGS':
                    target = _resolve(_country_card, nodes)
                elif kind == 'ACCOUNT':
                    target = _resolve(_locale_button, nodes)
                elif nodes:
                    target = account_target(nodes)
            elif number == 21:
                if state.marketplace_done_sent and _navigation_ready(nodes):
                    state.marketplace_done_confirmed = True
                    state.marketplace_completed.add(number)
                    return
                if state.marketplace_done_sent and _destination(nodes):
                    stable_destination += 1
                    if _navigation_ready(nodes) or stable_destination >= 2:
                        state.marketplace_done_confirmed = True
                        state.marketplace_completed.add(number)
                        return
                    _pause(stop, 2)
                    continue
                stable_destination = 0
                if kind == 'MARKET_SETTINGS':
                    if not _us_selected(nodes):
                        target = _resolve(_country_card, nodes)
                    else:
                        try:
                            target = _button(nodes, 'Done')
                        except ToolError:
                            target = None
                elif kind == 'MARKET_COUNTRIES':
                    try:
                        target = _us_row(nodes)
                    except ToolError:
                        if scrolls >= 16:
                            if recover_country_list():
                                continue
                            raise ToolError('Chưa tìm lại được United States ở b21; giữ máy để Tiếp tục')
                        _scroll_country(phone, deadline)
                        scrolls += 1
                        _pause(stop, 1)
                        continue
                elif not state.marketplace_done_sent and kind == 'ACCOUNT':
                    target = _resolve(_locale_button, nodes)
                elif not state.marketplace_done_sent and nodes:
                    target = account_target(nodes)
            if target is None and kind in {'ACCOUNT', 'MARKET_SETTINGS'} and number in range(17,22):
                try:
                    visual = _read(phone, deadline, stop, visual=True)
                    visual_kind = _kind(visual)
                    if visual_kind == 'ACCOUNT' and not state.marketplace_done_sent:
                        target = _locale_button(visual)
                    elif visual_kind == 'MARKET_SETTINGS':
                        if number == 21 and _us_selected(visual):
                            target = _button(visual, 'Done')
                        else:
                            target = _country_card(visual)
                    if target is not None:
                        nodes, kind = visual, visual_kind
                except ToolError:
                    if stop.is_set():
                        raise
            if target is not None and time.monotonic() >= next_tap:
                missing_targets = 0
                if taps >= 6:
                    raise ToolError(f'b{number}: màn chưa đổi sau các lần kiểm tra và khôi phục; dừng riêng máy')
                if not foreground_ready():
                    continue
                _pause(stop, 0)
                done_tap = number == 21 and kind == 'MARKET_SETTINGS' and _us_selected(nodes)
                if done_tap:
                    if state.marketplace_done_attempts >= 2:
                        raise ToolError('Đã thử Done hai lần; giữ nguyên để kiểm tra mạng rồi Tiếp tục')
                    state.marketplace_done_sent = True
                    state.marketplace_done_attempts += 1
                    state.marketplace_done_at = time.monotonic()
                    next_tap = time.monotonic() + 20
                    outer.recovering('b21: Done đã bấm · tìm thanh dưới để sang hình người ngay')
                else:
                    next_tap = time.monotonic() + 8
                taps += 1
                _tap_for_transition(phone, target, deadline)
                if number == 16:
                    if state.marketplace_person_tapped_at is None:
                        state.marketplace_person_tapped_at = time.monotonic()
                    state.marketplace_completed.add(16)
                    return  # b17 waits for EN; Account content need not finish loading.
                if done_tap:
                    state.marketplace_done_confirmed = True
                    state.marketplace_completed.add(21)
                    return
            elif target is None and nodes and time.monotonic() >= next_tap:
                # Retry a visible network error only when it has a unique button.
                retry_sent = False
                for label in ('Try again', 'Retry', 'Reload'):
                    try:
                        retry = _button(nodes, label)
                    except ToolError:
                        continue
                    _foreground(phone, deadline)
                    _tap_for_transition(phone, retry, deadline)
                    next_tap = time.monotonic() + 8
                    retry_sent = True
                    missing_targets = 0
                    break
                if (not retry_sent and kind in {'ACCOUNT', 'MARKET_SETTINGS'} and
                        number in range(17,22) and not state.marketplace_done_sent):
                    missing_targets += 1
                    if missing_targets >= 2:
                        back_and_read_text()
                        missing_targets = 0
            _pause(stop, 0.3 if number == 22 or
                   (number == 21 and state.marketplace_done_sent) else
                   0.5 if number == 17 else 2)
        raise ToolError(f'b{number}: Amazon chưa tải/đổi đúng màn sau 75 giây; giữ bước để Tiếp tục')

    names = ('b16 mở tab hình người', 'b17 mở quốc gia và ngôn ngữ',
             'b18 mở danh sách quốc gia', 'b19 cuộn tìm United States',
             'b20 chọn United States', 'b21 Done đổi quốc gia',
             'b22 thấy tab hình người thì mở ngay')
    return tuple(PostMenuStep(name, lambda job, deadline, stop, n=number:
                             run(n, deadline, stop))
                 for number, name in enumerate(names, 16))
