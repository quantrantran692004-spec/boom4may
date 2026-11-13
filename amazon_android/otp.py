"""Read one profile's Amazon SMS code from its assigned APIFC URL.

The account flow reads this URL only after it has sent SMS and confirmed the
SMS entry screen. URLs and SMS bodies are never included in errors.
"""
from __future__ import annotations

import re
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .core import ToolError


CODE = re.compile(r"^yes\|Amazon:\s*(\d{6})\s+is your sign-in code\.", re.IGNORECASE)


def validate_otp_url(raw: str) -> str:
    """Accept only a tokenized HTTPS SMS-record endpoint."""
    url = raw.strip()
    if not url or len(url) > 2048 or any(char.isspace() for char in url):
        raise ToolError("URL OTP không hợp lệ")
    try:
        parts = urlsplit(url)
        tokens = parse_qs(parts.query, keep_blank_values=True).get("token", [])
        valid = (parts.scheme == "https" and parts.hostname == "apifc.net"
                 and parts.path == "/smsrecord" and parts.port is None
                 and not parts.username and not parts.password and not parts.fragment
                 and len(tokens) == 1 and bool(tokens[0]))
    except ValueError:
        valid = False
    if not valid:
        raise ToolError("URL OTP cần dạng https://apifc.net/smsrecord?token=...")
    return url


def otp_token(raw: str) -> str:
    """Return the identity of a validated URL for duplicate-row checks."""
    return parse_qs(urlsplit(validate_otp_url(raw)).query)["token"][0]


def extract_otp(body: str) -> str | None:
    """Extract only Amazon's sign-in code, never an unrelated digit sequence."""
    response = body.strip()
    match = CODE.match(response)
    if match:
        return match.group(1)
    if response.lower().startswith("yes|"):
        raise ToolError("Phản hồi OTP không đúng mẫu Amazon đã xác nhận")
    return None


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


_OPENER = build_opener(_NoRedirect)


def read_otp(url: str, *, timeout: float = 5) -> str | None:
    """GET the profile URL once and return its current code, if any."""
    url = validate_otp_url(url)
    request = Request(url, headers={"Accept": "text/plain",
                                   "Cache-Control": "no-cache",
                                   "Pragma": "no-cache"})
    try:
        with _OPENER.open(request, timeout=timeout) as response:
            payload = response.read(8193)
    except HTTPError as exc:
        raise ToolError(f"URL OTP trả HTTP {exc.code}") from None
    except (URLError, TimeoutError, OSError):
        raise ToolError("Không kết nối được URL OTP") from None
    if len(payload) > 8192:
        raise ToolError("Phản hồi OTP quá dài")
    return extract_otp(payload.decode("utf-8", errors="replace"))


def _read_otp_in_browser(url: str, previous_code: str | None, *,
                         deadline: float, interval: float,
                         stop: threading.Event, not_before: float = 0) -> str:
    prefix = "Không đọc được OTP bằng trình duyệt. "
    try:
        from playwright.sync_api import Error, sync_playwright
    except ImportError:
        raise ToolError(prefix + "Thiếu Playwright. Chạy python -m pip install -e .") from None

    def timeout_ms(until: float) -> int:
        remaining = until - time.monotonic()
        return max(1, int(min(remaining, 8) * 1000))

    # Give Chrome and Edge separate hidden windows, then reserve the rest of
    # this OTP deadline for a visible Chrome session and any browser challenge.
    started = time.monotonic()
    available = max(0.0, deadline - started)
    hidden_until = started + available * 0.4
    hidden_slice = max(0.0, (hidden_until - started) / 2)
    try:
        with sync_playwright() as playwright:
            for channel, headless, until in (
                    ("chrome", True, started + hidden_slice),
                    ("msedge", True, hidden_until),
                    ("chrome", False, deadline)):
                retry_visible = not headless
                while not stop.is_set() and time.monotonic() < until:
                    try:
                        browser = playwright.chromium.launch(
                            channel=channel, headless=headless,
                            timeout=timeout_ms(until))
                    except Error:
                        if not retry_visible or stop.wait(0.5):
                            break
                        continue
                    try:
                        page = browser.new_page()
                        delay = min(not_before, until) - time.monotonic()
                        if delay > 0 and stop.wait(delay):
                            raise ToolError("Đã dừng chờ OTP")
                        reload_page = True
                        while not stop.is_set() and time.monotonic() < until:
                            if reload_page:
                                response = page.goto(url, wait_until="domcontentloaded",
                                                     timeout=timeout_ms(until))
                                if response is None:
                                    break
                                challenge = response.headers.get("cf-mitigated") == "challenge"
                                if challenge or not response.ok or page.url != url:
                                    if headless:
                                        break
                                    # Keep real Chrome open through a challenge;
                                    # read again if it returns to the OTP URL.
                                    reload_page = False
                            if page.url == url:
                                body = page.locator("body").inner_text(
                                    timeout=timeout_ms(until))
                                code = extract_otp(body)
                                if code is not None and code != previous_code:
                                    return code
                                if body.lstrip().lower().startswith("no|"):
                                    reload_page = True
                            remaining = until - time.monotonic()
                            if remaining <= 0 or stop.wait(min(interval, remaining)):
                                break
                    except Error:
                        pass
                    finally:
                        try:
                            browser.close()
                        except Error:
                            pass
                    if not retry_visible or stop.is_set() or time.monotonic() >= until:
                        break
                    if stop.wait(0.5):
                        break
                if stop.is_set() or time.monotonic() >= deadline:
                    break
    except (Error, OSError):
        raise ToolError(prefix + "Bấm Tiếp tục để mở URL và nhập mã thủ công") from None
    if stop.is_set():
        raise ToolError("Đã dừng chờ OTP")
    raise ToolError("Hết thời gian chờ lượt đọc OTP; chưa có mã mới hoặc chưa đọc được URL")


def wait_for_new_otp(url: str, previous_code: str | None, *,
                     timeout: float = 30, interval: float = 1,
                     stop: threading.Event | None = None,
                     not_before: float = 0) -> str:
    """Poll one profile URL for a code after SMS was requested."""
    validate_otp_url(url)
    if timeout <= 0 or interval <= 0:
        raise ValueError("OTP timeout and interval must be positive")
    deadline = time.monotonic() + timeout
    stop = stop or threading.Event()
    if stop.is_set():
        raise ToolError("Đã dừng chờ OTP")
    while not_before > time.monotonic() and time.monotonic() < deadline:
        if stop.wait(min(0.1, not_before - time.monotonic(),
                         deadline - time.monotonic())):
            raise ToolError("Đã dừng chờ OTP")
    if stop.is_set() or time.monotonic() >= deadline:
        raise ToolError("Đã dừng chờ OTP" if stop.is_set() else
                        "Hết thời gian chờ mã OTP")
    return _read_otp_in_browser(url, previous_code, deadline=deadline,
                                interval=interval, stop=stop, not_before=not_before)
