"""One spawned UI/OCR process per active phone; no shared frames or engines."""
from __future__ import annotations

import multiprocessing
import threading
import time
from contextlib import contextmanager

from .core import ToolError

_local = threading.local()
_owners_lock = threading.Lock()
_owners = set()


class ReaderResponseError(ToolError):
    """A live child rejected one read; retain its warmed-up backend for retry."""


def current(serial):
    reader = getattr(_local, 'reader', None)
    if reader is not None and reader.serial != serial:
        raise ToolError('Serial không khớp tiến trình của máy; đã chặn thao tác')
    return reader


def _serve(connection, serial):
    from .cloud import CloudPhone
    from .account_flow import _read_nodes_once, _read_visual_nodes
    from .post_menu import AttemptDeadline
    from . import ui_backend
    from . import vision
    import queue
    # This process serves only one phone, sequentially; one resident OCR model.
    vision._ocr_slots = queue.Queue()
    vision._ocr_slots.put(0)
    phone = CloudPhone(serial)
    visual_until = {}
    try:
        while True:
            request, operation, budget, options = connection.recv()
            try:
                if operation == 'read':
                    deadline = AttemptDeadline(budget, visual_until=visual_until)
                    result = _read_nodes_once(phone, deadline, threading.Event())
                elif operation == 'visual':
                    deadline = AttemptDeadline(budget, visual_until=visual_until)
                    result = _read_visual_nodes(phone, deadline, threading.Event())
                elif operation == 'visual_text':
                    deadline = AttemptDeadline(budget, visual_until=visual_until)
                    result = _read_visual_nodes(phone, deadline, threading.Event(),
                                                crop=options['crop'], text_only=True)
                elif operation == 'navigation':
                    from .marketplace_flow import _read_navigation_nodes
                    deadline = AttemptDeadline(budget, visual_until=visual_until)
                    result = _read_navigation_nodes(phone, deadline, threading.Event())
                elif operation == 'scroll':
                    result = ui_backend.country_scroll(phone, **options)
                else:
                    raise ValueError('Unknown reader operation')
                connection.send((request, serial, True, result))
            except Exception as exc:
                # Never transmit arbitrary native errors containing screen text.
                connection.send((request, serial, False, type(exc).__name__))
    except (EOFError, BrokenPipeError, OSError):
        pass
    finally:
        connection.close()


class PhoneReader:
    def __init__(self, serial, *, target=_serve):
        from .cloud import CloudPhone
        CloudPhone(serial)
        self.serial = serial
        self.target = target
        self.process = None
        self.connection = None
        self.sequence = 0
        self.stop = threading.Event()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        if self.process is not None:
            if self.process.pid is None:
                self.process.close()
                self.process = None
                return
            self.process.join(0.2)
            if self.process.is_alive():
                self.process.terminate()
                self.process.join(2)
            if self.process.is_alive():
                raise ToolError('Chưa dừng được tiến trình nhận diện cũ')
            self.process.close()
            self.process = None

    def call(self, operation, seconds, stop, **options):
        if stop.is_set() or seconds <= 0:
            raise ToolError('Đã dừng hoặc hết thời gian máy này')
        expires = time.monotonic() + seconds
        try:
            if self.process is None:
                context = multiprocessing.get_context('spawn')
                self.connection, child = context.Pipe()
                self.process = context.Process(target=self.target, args=(child, self.serial),
                                               daemon=True, name='phone-reader')
                try:
                    self.process.start()
                finally:
                    child.close()
            self.sequence += 1
            self.connection.send((self.sequence, operation, seconds, options))
            while True:
                if stop.is_set() or time.monotonic() >= expires:
                    raise ToolError('Đã dừng hoặc hết thời gian nhận diện máy này')
                if self.connection.poll(0.05):
                    request, serial, ok, result = self.connection.recv()
                    if stop.is_set() or time.monotonic() >= expires:
                        raise ToolError('Bỏ kết quả nhận diện đã hết hạn')
                    if serial != self.serial or request != self.sequence:
                        raise ToolError('Kết quả không khớp máy/lượt đọc; đã loại bỏ')
                    if not ok:
                        raise ReaderResponseError('Bộ đọc UI của máy chưa trả được kết quả hợp lệ')
                    return result
                if not self.process.is_alive():
                    raise ToolError('Tiến trình nhận diện máy này đã thoát')
        except ReaderResponseError:
            raise
        except Exception as exc:
            self.close()
            if isinstance(exc, ToolError):
                raise
            raise ToolError('Mất kết nối tiến trình nhận diện máy này') from exc


@contextmanager
def phone_reader(serial, stop=None):
    if getattr(_local, 'reader', None) is not None:
        raise ToolError('Máy đã có bộ đọc đang hoạt động trên luồng này')
    reader = PhoneReader(serial)
    with _owners_lock:
        if serial in _owners:
            raise ToolError('Serial này đã được một máy khác sử dụng; chưa chạy luồng trùng')
        _owners.add(serial)
    if stop is not None:
        reader.stop = stop
    _local.reader = reader
    try:
        yield reader
    finally:
        _local.reader = None
        try:
            reader.close()
        finally:
            with _owners_lock:
                _owners.discard(serial)
