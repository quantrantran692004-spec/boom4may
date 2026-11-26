"""Per-phone random menu visits before registration and after Create."""
from __future__ import annotations

import re
import hashlib
import random
import secrets
import threading
import time

from .account_flow import (MENU_CARD_LABELS, _bounds, _read_nodes, _read_nodes_once,
                           _read_visual_nodes, _scroll_up,
                           _tap, _text, _visible, build_common_steps, screen)
from .cloud import CloudPhone, cloud_adb, amazon_is_foreground
from .core import AMAZON_PACKAGE, ToolError
from .browse_view_scroll import scroll_view, wait_until
from .post_menu import (AttemptDeadline, PostMenuStep, RecoverableStepError,
                        RegistrationState)
from .q7_random_prefix import CHILD_LABELS
from .runner import RunJob
from .marketplace_flow import (build_marketplace_steps, build_account_preview_step,
                               _navigation_ready, _search_active)
from .create_address_flow import build_create_address_steps
from .create_address_detail_flow import build_create_address_detail_steps
from .reload_payment_flow import build_reload_payment_steps


SIZE = re.compile(r"(?:Physical|Override) size:\s*(\d+)x(\d+)")
COLUMNS = (0.16, 0.50, 0.84)
ROWS = (0.20, 0.42, 0.62, 0.79)
POINTS = tuple((x, y) for y in ROWS for x in COLUMNS)
TAIL_NUMBERS = (13, 14, 15)
TAIL_LIST_LABELS = frozenset({'books', 'electronics', 'home services', 'see all',
                              "today's deals", 'try prime'})
TAIL_MENU_LABELS = MENU_CARD_LABELS | CHILD_LABELS | TAIL_LIST_LABELS
_tail_choice_lock = threading.Lock()
_tail_sequences: dict[str, dict[int, set[tuple[str, ...]]]] = {}


class _TailChoicesExhausted(ToolError):
    """The current menu has no unused target for this step across phones."""


class _PrefixRecoveryStop(ToolError):
    """Pause this phone when the bounded Browse recovery cannot proceed."""
    terminal = True


def _tail_input_action(node):
    """Inputs/camera/permission controls are not random shopping navigation."""
    labels = [_text(node), node.get('content-desc', '').casefold()]
    if node.get('class') in {'android.widget.EditText', 'android.widget.CheckBox',
                            'android.widget.Switch'}:
        return True
    if any(label in {'search', 'camera', 'scan it', 'lens', 'microphone', 'not now',
                     'allow access', 'close', 'dismiss'} or label.startswith((
                         'search amazon', 'search with ', 'search by ', 'scan with ',
                         'scan a ', 'scan barcode',
                         'scan products', 'allow camera', 'open camera', 'voice search',
                         'camera button', 'lens ')) for label in labels):
        return True
    resource = node.get('resource-id', '').casefold()
    return bool(re.search(r'(?:^|[/_])(?:camera|lens|voice_search|microphone|search_box|'
                          r'search_field|search_src_text)(?:$|_)', resource))


def _tail_overlay(nodes):
    return (_search_active(nodes) or any(_visible(n) and (
        n.get('class') == 'android.widget.EditText' and n.get('focused') == 'true' or
        any(term in _text(n) for term in ('allow camera access', 'scan a barcode',
                                         'lens ai', 'allow access'))) for n in nodes))


def _tail_candidates(nodes, state):
    """Choose only category cards and child entries in the open Browse menu."""
    candidates = {}
    ambiguous = set()
    for node in nodes:
        if not _visible(node) or _tail_input_action(node):
            continue
        description = node.get("content-desc", "").casefold()
        label = _text(node)
        if (not label or label in state.tail_attempted or
                description.startswith(("home tab", "browse menu tab", "cart tab", "account tab")) or
                label.startswith(("home tab", "browse menu tab", "cart tab", "account tab")) or
                label in {"home", "trang chủ", "menu", "browse", "shop by category",
                          "sign in", "sign out", "continue", "verify mobile number"} or
                any(word in label for word in ("buy now", "place order", "checkout",
                                               "delete", "remove", "subscribe",
                                               "payment", "address", "password",
                                               "security", "credit card"))):
            continue
        if label not in TAIL_MENU_LABELS:
            continue
        if label in candidates and _bounds(candidates[label]) != _bounds(node):
            ambiguous.add(label)
        else:
            candidates[label] = node
    return {label: node for label, node in candidates.items() if label not in ambiguous}


def _tail_safe_page_choices(nodes, state):
    """Navigation choices usable when Browse's card layout is not recognized."""
    safe = {'orders', 'buy again', 'interests', 'lists', 'cart', 'account'}
    return {label: node for label, node in _tail_candidates(nodes, state).items()
            if label in safe or label in TAIL_MENU_LABELS}


def _choose_tail_target(job, number, available, state, *, allow_cross_phone_repeat=False):
    """Reserve a different live target per step across concurrent phones."""
    with _tail_choice_lock:
        phones = _tail_sequences.setdefault(job.batch_id, {})
        own = phones.setdefault(job.index, set())
        for step in TAIL_NUMBERS:
            if step in state.tail_choices:
                own.add(tuple(state.tail_choices[n] for n in TAIL_NUMBERS if n <= step))
        used = {sequence for index, sequences in phones.items() if index != job.index
                for sequence in sequences}
        prefix = tuple(state.tail_choices[n] for n in TAIL_NUMBERS if n < number)
        used_labels = {sequence[-1] for sequence in used if len(sequence) == number - 12}
        prior = [slots[job.index] for batch, slots in _tail_sequences.items()
                 if batch != job.batch_id and job.index in slots]
        previous_labels = {sequence[number - 13] for sequence in prior[-1]
                           if len(sequence) >= number - 12} if prior else set()
        choices = [label for label in available if (allow_cross_phone_repeat or label not in used_labels) and
                   label not in state.tail_attempted and
                   (allow_cross_phone_repeat or label not in previous_labels)]
        if not choices:
            raise _TailChoicesExhausted(
                f"b{number}: mục đang hiện trùng máy khác hoặc mẻ trước; cần đọc/cuộn thêm mục mới")
        label = secrets.choice(choices)
        own.add(prefix + (label,))
        return label


def _first_point(job: RunJob) -> tuple[float, float]:
    """A new batch shuffles 12 positions, giving every phone a unique b1."""
    seed = int.from_bytes(hashlib.sha256(job.batch_id.encode("utf-8")).digest())
    positions = list(POINTS)
    random.Random(seed).shuffle(positions)
    return positions[job.index]


def _size(phone: CloudPhone, deadline: AttemptDeadline) -> tuple[int, int]:
    output = cloud_adb(phone, "shell", "wm", "size",
                       timeout=max(1, int(min(5, deadline.remaining()))))
    sizes = SIZE.findall(output.stdout)
    if not sizes:
        raise RecoverableStepError("Chưa đọc được kích thước màn hình máy này")
    width, height = map(int, sizes[-1])
    if width < 100 or height < 200:
        raise RecoverableStepError("Kích thước màn hình máy này chưa hợp lệ")
    return width, height


def _menu(phone: CloudPhone, width: int, height: int,
          deadline: AttemptDeadline) -> None:
    # One tap at the live device's bottom Browse tab; b4 still verifies UI.
    try:
        cloud_adb(phone, "shell", "input", "tap", str(round(width * 0.86)),
                  str(round(height * 0.93)),
                  timeout=max(1, int(min(5, deadline.remaining()))))
    except ToolError:
        pass  # A browse tap can be delivered despite an ADB response error.


def _tail_menu(phone: CloudPhone, deadline: AttemptDeadline,
               stop: threading.Event, fallback_state=None) -> list[dict[str, str]]:
    """Read the live Browse menu, allowing three reads for a slow page."""
    for attempt in range(4):  # Three recovery actions plus a final fresh confirmation.
        if stop.is_set():
            raise ToolError("Đã dừng máy này")
        try:
            nodes = _read_nodes(phone, AttemptDeadline(min(12, deadline.remaining()),
                                notice=deadline.notice), stop, max_attempts=1)
        except ToolError:
            if stop.is_set() or attempt >= 2:
                raise
            stop.wait(deadline.allowance(0.4 * (attempt + 1)))
            continue
        kind = screen(nodes)
        if kind in {"SMS", "WHATSAPP", "CREATE_FORM", "NEW_ACCOUNT",
                    "IDENTIFIER", "COUNTRY"}:
            if attempt >= 2:
                raise ToolError("Máy này còn ở form đăng ký/xác minh; giữ nguyên b12–b15")
            if stop.wait(deadline.allowance(2 * (attempt + 1))):
                raise ToolError("Đã dừng máy này")
            continue
        focused = amazon_is_foreground(phone, timeout=3, adb=cloud_adb) if nodes else False
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        if kind == 'MENU' and not _tail_overlay(nodes) and focused:
            return nodes
        if attempt == 3:
            break
        browse = {node["bounds"]: node for node in nodes if _visible(node) and
                  node.get("content-desc", "").casefold().startswith("browse menu tab")}
        if len(browse) > 1:
            raise ToolError("Không xác định được duy nhất tab Browse của máy này")
        if nodes and (_tail_overlay(nodes) or not focused or
                      (not browse and not _navigation_ready(nodes) and kind != 'ACCOUNT')):
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            declines = {n['bounds']: n for n in nodes if _visible(n) and _text(n) == 'not now'}
            try:
                if focused and len(declines) == 1:
                    _tap(phone, next(iter(declines.values())), deadline)
                else:
                    cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_BACK', timeout=4)
            except ToolError:
                deadline.recovering('Đang đọc lại sau thao tác thoát chưa xác nhận')
            deadline.recovering('b12–b15: đóng bàn phím/tìm kiếm/Lens rồi đọc lại menu')
            if stop.wait(deadline.allowance(0.6)):
                raise ToolError('Đã dừng máy này')
            continue
        if browse and focused:
            try:
                _tap(phone, next(iter(browse.values())), deadline)
            except ToolError:
                deadline.recovering("Tab Browse chưa xác nhận · đang đọc lại máy này")
        elif nodes and focused:
            # Some signed-in layouts omit the tab label. Use this phone's
            # dimensions only after verifying Amazon is foreground.
            width, height = _size(phone, deadline)
            _menu(phone, width, height, deadline)
        if attempt < 3 and stop.wait(deadline.allowance(2 * (attempt + 1))):
            raise ToolError("Đã dừng máy này")
    raise RecoverableStepError("Menu Browse chưa trở lại sau ba lần khôi phục")


def build_tail_steps(phone: CloudPhone, state: RegistrationState) -> tuple[PostMenuStep, ...]:
    """Open Browse at b12, then make three distinct random navigation visits."""
    def visit_seconds(number):
        return (16.0 if state.flow_mode == 'create' else 1.0) + (4.0 if number == 15 else 0.0)

    def read_menu(number, deadline, stop):
        started = state.tail_menu_wait_started.setdefault(number, time.monotonic())
        limit = 90 if number == 12 else 60
        retries = 0
        while time.monotonic() - started < limit and retries < (8 if number == 12 else 5):
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            try:
                nodes = _tail_menu(phone, deadline, stop,
                                   state if number in TAIL_NUMBERS else None)
                state.tail_menu_wait_started.pop(number, None)
                return nodes
            except RecoverableStepError:
                retries += 1
                if stop.is_set():
                    raise ToolError('Đã dừng máy này')
                deadline.recovering(f'b{number}: màn chưa có mục phù hợp; '
                                    'thử ba gạch/Back rồi đọc lại')
                if stop.wait(min(2, max(0, limit - (time.monotonic() - started)))):
                    raise ToolError('Đã dừng máy này')
        state.tail_menu_wait_started.pop(number, None)
        raise ToolError(f'b{number}: sau {limit} giây vẫn chưa thấy menu Browse; '
                        'giữ bước máy này để kiểm tra màn rồi Tiếp tục')

    def view(number, deadline, stop, seconds=None):
        if seconds is not None:
            state.tail_view_until[number] = time.monotonic() + seconds
        until = state.tail_view_until.get(number)
        if until is None:
            return False
        if number in TAIL_NUMBERS:
            if number not in state.tail_viewed:
                duration = visit_seconds(number)
                wait_until(until - duration / 2, deadline, stop)
                state.tail_viewed.add(number)
            return True
        wait_until(until, deadline, stop)
        state.tail_view_until.pop(number, None)
        state.tail_completed.add(number)
        return True

    def return_to_menu(number, deadline, stop):
        if number not in state.tail_viewed:
            return
        if stop.is_set():
            raise ToolError('Đã dừng máy này')
        try:
            nodes = _read_nodes(phone, AttemptDeadline(min(4, deadline.remaining()),
                                notice=deadline.notice), stop, max_attempts=1)
        except ToolError:
            if stop.is_set():
                raise
            nodes = []  # A slow child page must not block its scroll and Back.
        if screen(nodes) in {'SMS', 'WHATSAPP', 'CREATE_FORM', 'NEW_ACCOUNT',
                             'IDENTIFIER', 'COUNTRY'}:
            raise ToolError(f'b{number}: gặp form tài khoản sau khi mở thẻ con; giữ máy này')
        if screen(nodes) == 'MENU':
            if number not in state.tail_page_scrolled:
                if not amazon_is_foreground(phone, timeout=3, adb=cloud_adb):
                    raise ToolError(f'b{number}: Amazon chưa ở phía trước; giữ máy này')
                _scroll_up(phone, [], deadline, browsing=True)
                state.tail_page_scrolled.add(number)
            wait_until(state.tail_view_until.get(number, time.monotonic()), deadline, stop)
            state.tail_view_until.pop(number, None)
            state.tail_completed.add(number)
            return
        if not amazon_is_foreground(phone, timeout=3, adb=cloud_adb):
            raise ToolError(f'b{number}: Amazon chưa ở phía trước; giữ máy này')
        if number not in state.tail_page_scrolled and number not in state.tail_back_sent:
            deadline.recovering(f'b{number}a: trang con đã mở · cuộn một lượt')
            _scroll_up(phone, [], deadline, browsing=True)
            state.tail_page_scrolled.add(number)
        wait_until(state.tail_view_until.get(number, time.monotonic()), deadline, stop)
        state.tail_view_until.pop(number, None)
        if number not in state.tail_back_sent:
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            deadline.recovering(f'b{number}c: Back khỏi trang con')
            cloud_adb(phone, 'shell', 'input', 'keyevent', 'KEYCODE_BACK', timeout=4)
            state.tail_back_sent.add(number)
        read_menu(number, deadline, stop)
        state.tail_completed.add(number)
        if number == 15:
            deadline.recovering('b15 đã trở về menu · chuyển sang b16 hình người')

    def open_menu(job, deadline, stop):
        if 12 in state.tail_completed:
            return
        if view(12, deadline, stop):
            return
        if not (state.create_pressed or state.login_verify_pressed or state.manual_sms_completed):
            raise ToolError("Chưa xác nhận hành động cuối ở máy này; không chạy b12–b15")
        deadline.recovering('b12: OTP đã xác nhận · chờ Trang chủ tải rồi mở menu')
        read_menu(12, deadline, stop)
        view(12, deadline, stop, seconds=2)

    def visit(number: int):
        def action(job: RunJob, deadline: AttemptDeadline,
                   stop: threading.Event) -> None:
            if number in state.tail_completed:
                return  # A confirmed tap must not be sent again after a pause.
            if number in state.tail_viewed:
                return_to_menu(number, deadline, stop)
                return
            if number in state.tail_view_until:
                view(number, deadline, stop)
                return_to_menu(number, deadline, stop)
                return
            if not (state.create_pressed or state.login_verify_pressed or state.manual_sms_completed):
                raise ToolError("Chưa xác nhận hành động cuối ở máy này; không chạy b12–b15")
            for attempt in range(3):
                nodes = read_menu(number, deadline, stop)
                candidates = _tail_candidates(nodes, state)
                if not candidates and screen(nodes) == 'MENU':
                    try:
                        visual = _read_visual_nodes(phone, AttemptDeadline(
                            min(12, deadline.remaining()), notice=deadline.notice), stop)
                        if screen(visual) == 'MENU':
                            nodes = visual
                            candidates = _tail_candidates(nodes, state)
                    except ToolError:
                        if stop.is_set():
                            raise
                top_level = sorted(set(candidates) & (MENU_CARD_LABELS | TAIL_LIST_LABELS))
                available = top_level + sorted(set(candidates) - set(top_level))
                if available:
                    try:
                        label = _choose_tail_target(job, number, available, state,
                                                    allow_cross_phone_repeat=attempt == 2)
                        break
                    except _TailChoicesExhausted:
                        pass  # Reveal fresh live targets; never fall back to a duplicate.
                if attempt == 2:
                    raise ToolError(f"b{number}: chưa thấy mục mới khác lựa chọn các máy; "
                                    "dừng riêng máy này để đọc lại, không bấm trùng")
                _scroll_up(phone, nodes, deadline)
                if stop.wait(deadline.allowance(0.4)):
                    raise ToolError("Đã dừng máy này")
            state.tail_attempted.add(label)  # Keep an uncertain tap out of later choices.
            if stop.is_set():
                raise ToolError('Đã dừng máy này')
            try:
                _tap(phone, candidates[label], deadline)
            except ToolError as exc:
                raise ToolError(f"b{number}: cú bấm danh mục chưa xác nhận; "
                                "giữ nguyên bước để kiểm tra máy này") from exc
            state.tail_choices[number] = label
            view(number, deadline, stop, seconds=visit_seconds(number))
            return_to_menu(number, deadline, stop)
        return action

    return (PostMenuStep("b12 mở menu ba gạch", open_menu),) + tuple(
        PostMenuStep(f"b{number} điều hướng ngẫu nhiên", visit(number))
        for number in TAIL_NUMBERS)


def build_post_auth_steps(phone: CloudPhone, state: RegistrationState) -> tuple[PostMenuStep, ...]:
    """Single shared continuation after Create/Verify for every phone.

    b12–b22 are shared; b23–b39 are create-only address/reload actions.
    """
    marketplace = build_marketplace_steps(phone, state)
    with_preview = (marketplace[:1] + (build_account_preview_step(phone, state),) +
                    marketplace[1:]) if marketplace else ()
    steps = build_tail_steps(phone, state) + with_preview
    if state.flow_mode == 'create':
        steps += (build_create_address_steps(phone, state) +
                  build_create_address_detail_steps(phone, state) +
                  build_reload_payment_steps(phone, state))
    elif state.flow_mode == 'login' and state.login_followup == 'address_and_card':
        steps += (build_create_address_steps(phone, state) +
                  build_create_address_detail_steps(phone, state) +
                  build_reload_payment_steps(phone, state))
    elif state.flow_mode == 'login' and state.login_followup == 'card_only':
        steps += build_reload_payment_steps(phone, state)
    return steps


def build_random_steps(phone: CloudPhone, on_otp,
                       on_status=lambda _status: None,
                       registration: RegistrationState | None = None,
                       ) -> tuple[PostMenuStep, ...]:
    """Visit three random category positions long enough to see each one."""
    state = registration if registration is not None else RegistrationState()

    def finish_view(number):
        state.prefix_view_until.pop(number, None)
        state.prefix_scroll_at.pop(number, None)
        state.prefix_completed.add(number)

    def browse_view(number, deadline, stop):
        until = state.prefix_view_until[number]
        if number in (1, 2) and number not in state.prefix_view_scrolled:
            wait_until(state.prefix_scroll_at.get(number, until), deadline, stop)
            width, height = _size(phone, deadline)
            scroll_view(phone, width, height, deadline, stop, number, cloud_adb)
            state.prefix_view_scrolled.add(number)
        wait_until(until, deadline, stop)
        finish_view(number)

    def browse(number: int):
        def action(job: RunJob, deadline: AttemptDeadline,
                   stop: threading.Event) -> None:
            if stop.is_set():
                raise ToolError("Đã dừng máy này")
            if number in state.prefix_completed:
                return
            if number in state.prefix_view_until:
                browse_view(number, deadline, stop)
                return
            width, height = _size(phone, deadline)
            candidates = list(POINTS)
            used = set(state.prefix_choices.values())
            for attempt in range(4):
                if stop.is_set():
                    raise ToolError("Đã dừng máy này")
                nodes = _prefix_nodes(phone, deadline, stop)
                if number > 1 or attempt:
                    if screen(nodes) != "MENU":
                        nodes = _restore_prefix_menu(phone, width, height, deadline, stop, nodes)
                    elif stop.wait(deadline.allowance(0.6)):
                        raise ToolError("Đã dừng máy này")
                if number in (1, 2) and attempt >= 2:
                    # Reveal another row if the first two taps were not sent.
                    try:
                        cloud_adb(phone, "shell", "input", "swipe",
                                  str(width // 2), str(round(height * 0.73)),
                                  str(width // 2), str(round(height * 0.35)), "280",
                                  timeout=max(1, int(min(5, deadline.remaining()))))
                    except ToolError:
                        pass
                    nodes = _prefix_nodes(phone, deadline, stop)
                available = [point for point in candidates if point not in used]
                preferred = (_first_point(job) if number == 1 and attempt == 0
                             else None)
                point = (preferred if preferred in available else
                         secrets.choice(available or candidates))
                candidates.remove(point)
                x, y = point
                live = (_tail_candidates(nodes, RegistrationState(
                    tail_attempted=state.prefix_attempted)) if screen(nodes) == "MENU" else {})
                label = secrets.choice(sorted(live)) if live else None
                if label is not None:
                    x1, y1, x2, y2 = _bounds(live[label])
                    x, y = (x1 + x2) / (2 * width), (y1 + y2) / (2 * height)
                    point = (x, y)
                    state.prefix_attempted.add(label)
                try:
                    cloud_adb(phone, "shell", "input", "tap",
                              str(round(width * x)), str(round(height * y)),
                              timeout=max(1, int(min(5, deadline.remaining()))))
                except ToolError:
                    deadline.recovering(f"b{number}: cú bấm chưa xác nhận, thử vị trí khác")
                    continue
                state.prefix_choices[number] = point
                deadline.recovering(f"b{number}: đã bấm vị trí danh mục ngẫu nhiên")
                view_seconds = 3 + secrets.randbelow(3)
                started = time.monotonic()
                state.prefix_view_until[number] = started + view_seconds
                if number in (1, 2):
                    state.prefix_scroll_at[number] = started + 2.0
                browse_view(number, deadline, stop)
                return
            raise RecoverableStepError(
                f"b{number}: chưa gửi được cú bấm; đang tự thử lại đúng máy")
        return action

    common = build_common_steps(phone, on_otp, on_status, state)

    def sign_in(job: RunJob, deadline: AttemptDeadline,
                stop: threading.Event) -> None:
        if not {1, 2, 3} <= state.prefix_completed:
            raise RecoverableStepError("Chưa đủ ba lượt bấm ngẫu nhiên")
        width, height = _size(phone, deadline)
        _restore_prefix_menu(phone, width, height, deadline, stop, [])
        common[0].action(job, deadline, stop)

    return (tuple(PostMenuStep(f"b{number} ngẫu nhiên", browse(number))
                  for number in (1, 2, 3)) +
            (PostMenuStep(common[0].name, sign_in,
                          within_attempt=common[0].within_attempt),) + common[1:] +
            build_post_auth_steps(phone, state))


def _prefix_nodes(phone, deadline, stop):
    """One UI/OCR read with a worker budget; never enter the retrying reader."""
    from .isolated_reader import current
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    reader = current(phone.serial)  # A serial mismatch must never become a fallback tap.
    try:
        budget = min(6, deadline.remaining())
        if reader is not None:
            return reader.call('read', budget, stop)
        return _read_nodes_once(phone, AttemptDeadline(budget), stop)
    except ToolError:
        if stop.is_set():
            raise
        return []


def _restore_prefix_menu(phone, width, height, deadline, stop, nodes):
    """Return from a random page through Browse, with one checked Back fallback."""
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    if screen(nodes) in {'SMS','WHATSAPP','IDENTIFIER','COUNTRY','NEW_ACCOUNT','CREATE_FORM'}:
        raise _PrefixRecoveryStop('B1–b3 đã tới form tài khoản; dừng riêng để kiểm tra')
    if not amazon_is_foreground(phone, timeout=2, adb=cloud_adb):
        cloud_adb(phone, 'shell','input','keyevent','KEYCODE_BACK', timeout=4)
        if stop.wait(0.6):
            raise ToolError('Đã dừng máy này')
        if not amazon_is_foreground(phone, timeout=2, adb=cloud_adb):
            raise _PrefixRecoveryStop('Chưa quay lại được Amazon sau trang ngoài; kiểm tra máy này')
        nodes = []  # The previous app's navigation controls are no longer valid.
    if stop.is_set():
        raise ToolError('Đã dừng máy này')
    tabs = {n['bounds']: n for n in nodes if _visible(n) and
            (n.get('content-desc') or _text(n)).casefold().startswith('browse menu tab')}
    if len(tabs) == 1:
        try:
            _tap(phone, next(iter(tabs.values())), deadline)
        except ToolError:
            pass  # Read the result before the Back fallback.
    else:
        _menu(phone, width, height, deadline)
    if stop.wait(0.6):
        raise ToolError('Đã dừng máy này')
    observed = _prefix_nodes(phone, deadline, stop)
    if screen(observed) == 'MENU' or not observed:
        return observed
    if screen(observed) in {'SMS','WHATSAPP','IDENTIFIER','COUNTRY','NEW_ACCOUNT','CREATE_FORM'}:
        raise _PrefixRecoveryStop('Đang ở form tài khoản; không phát lại thao tác ngẫu nhiên')
    deadline.recovering('Trang ngẫu nhiên chưa về menu · Back một lần rồi mở ba gạch')
    cloud_adb(phone, 'shell','input','keyevent','KEYCODE_BACK', timeout=4)
    if stop.wait(0.6):
        raise ToolError('Đã dừng máy này')
    if not amazon_is_foreground(phone, timeout=2, adb=cloud_adb):
        raise _PrefixRecoveryStop('Amazon chưa ở trước sau khi Back; dừng riêng máy này')
    _menu(phone, width, height, deadline)
    if stop.wait(0.6):
        raise ToolError('Đã dừng máy này')
    observed = _prefix_nodes(phone, deadline, stop)
    if screen(observed) not in {'MENU','UNKNOWN'}:
        raise _PrefixRecoveryStop('Chưa về menu sau dự phòng; giữ bước để kiểm tra máy này')
    return observed
