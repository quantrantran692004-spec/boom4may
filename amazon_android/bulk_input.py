"""Pure parsing for indexed bulk paste; no secrets are written or logged."""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field, replace

from .batch import parse_proxy_line
from .core import ToolError
from .otp import otp_token, validate_otp_url
from .registration import PHONE
from .swarmote_desktop import ProxyConfig

MAX_PROFILES = 12
MAX_PROXY_CANDIDATES = 100
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CARD = re.compile(
    r"(\d{12,19})\|(\d{1,2})\|(\d{2,4})"
    r"(?:\|live=>√【[^】\r\n]{1,100}】)?"
)
PROXY_TOKEN = re.compile(r"(?<!\S)[^\s|:,]+:\d{1,5}:[^\s|:,]+:[^\s|:,]+(?!\S)")


def _markdown_cell_text(cell: str) -> str:
    """Remove whole-cell bold markup without changing the contained value."""
    for marker in ("**", "__"):
        if cell.startswith(marker) and cell.endswith(marker):
            value = cell[2:-2]
            if value and not value[0].isspace() and not value[-1].isspace():
                return value
    return cell


def _table_cells(line: str) -> list[str]:
    """Split Markdown columns without treating escaped pipes as separators."""
    if line.startswith("|") and line.endswith("|"):
        body = line[1:-1]
        return [_markdown_cell_text(cell.strip().replace(r"\|", "|"))
                for cell in re.split(r"(?<!\\)\|", body)]
    if "\t" in line:
        return [cell.strip() for cell in line.split("\t")]
    return [cell.strip() for cell in next(csv.reader([line]))]


def _url_from_cell(cell: str) -> str:
    """Use the actual Markdown link target, if the cell contains a link."""
    match = MARKDOWN_LINK.fullmatch(cell)
    if match:
        label, url = match.groups()
        label = _markdown_cell_text(label)
        if label.startswith(("http://", "https://")) and label != url:
            raise ToolError("Chữ và đích của link URL OTP không khớp")
        cell = url
    if cell.startswith((r"http\://", r"https\://")):
        cell = cell.replace(r"\:", ":")
        if cell.endswith("\\"):
            cell = cell[:-1]
    return cell


def validate_card(raw: str) -> str:
    """Keep the user's card reference in memory without echoing its value."""
    card = raw.strip()
    match = CARD.fullmatch(card)
    if not match or not 1 <= int(match.group(2)) <= 12:
        raise ToolError("Thẻ cần dạng số thẻ|tháng|năm")
    return "|".join(match.groups())

@dataclass(frozen=True)
class BulkRecord:
    profile_name: str
    phone: str
    full_name: str
    password: str = field(repr=False)
    proxy: ProxyConfig | None = field(default=None, repr=False)
    otp_url: str = field(default="", repr=False)
    card: str = field(default="", repr=False)


def parse_records(text: str, *, three_columns_only: bool = False,
                  account_table: bool = False) -> list[BulkRecord]:
    """Read 1–12 Markdown, tab or CSV rows, including the desktop OTP format."""
    if three_columns_only and account_table:
        raise ValueError("Choose one account table format")
    raw_rows = [line.strip() for line in text.splitlines() if line.strip()]
    rows = []
    for line in raw_rows:
        cells = _table_cells(line)
        if cells and all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        if cells and cells[0].casefold() in {"profile", "profile name", "tên profile", "sđt", "số điện thoại", "phone"}:
            continue
        rows.append(cells)
    if not 1 <= len(rows) <= MAX_PROFILES:
        raise ToolError("Bảng cần 1–12 dòng dữ liệu")
    result = []
    for index, cells in enumerate(rows, 1):
        if three_columns_only and len(cells) != 3:
            raise ToolError(f"Bảng dòng {index}: dán đúng 3 cột SĐT | Mật khẩu | Tên")
        if account_table and len(cells) < 4:
            raise ToolError(f"Bảng dòng {index}: cần ít nhất 4 cột SĐT | Mật khẩu | Tên | URL OTP")
        otp_url = ""
        card = ""
        if account_table:
            profile = f"q{index}"
            phone, password, name = cells[:3]
            url_cells = []
            urls = []
            for cell in cells[3:]:
                if not cell:
                    continue
                try:
                    cleaned = _url_from_cell(cell)
                except ToolError:
                    continue  # Discard an unrelated or inconsistent export cell.
                url_cells.append(cleaned)
                try:
                    urls.append(validate_otp_url(cleaned))
                except ToolError:
                    pass
            if len(urls) != 1:
                raise ToolError(f"Bảng dòng {index}: cần đúng 1 URL OTP trong hàng")
            otp_url = urls[0]
            other = [cell for cell in url_cells if cell not in urls]
            if other:
                # Card is optional reference data. An unrelated export column
                # or malformed card must not reject an otherwise valid row.
                raw_card = "|".join(other)
                match = CARD.search(raw_card)
                try:
                    card = validate_card(match.group(0)) if match else ""
                except ToolError:
                    card = ""
        elif len(cells) == 3:
            profile = f"q{index}"
            phone, password, name = cells
        elif len(cells) in {4, 5}:
            profile, phone, password, name = cells[:4]
        else:
            raise ToolError(f"Bảng dòng {index}: cần SĐT | Mật khẩu | Tên")
        if not profile or len(profile) > 80:
            raise ToolError(f"Bảng dòng {index}: tên Profile không hợp lệ")
        if not PHONE.fullmatch(phone):
            raise ToolError(f"Bảng dòng {index}: số điện thoại không hợp lệ")
        if not password or any(ord(c) < 33 or ord(c) > 126 for c in password):
            raise ToolError(f"Bảng dòng {index}: mật khẩu không được trống, chỉ nhận ASCII không dấu cách")
        if not name or len(name) > 100:
            raise ToolError(f"Bảng dòng {index}: tên Amazon không hợp lệ")
        if account_table:
            try:
                otp_url = validate_otp_url(otp_url)
            except ToolError as exc:
                raise ToolError(f"Bảng dòng {index}: {exc}") from exc
        try:
            proxy = (parse_proxy_line(cells[4])
                     if not account_table and len(cells) == 5 and cells[4] else None)
        except ToolError as exc:
            raise ToolError(f"Bảng dòng {index}: {exc}") from exc
        result.append(BulkRecord(profile, phone, name, password, proxy, otp_url, card))
    if len({item.profile_name.casefold() for item in result}) != len(result):
        raise ToolError("Bảng có tên Profile trùng nhau")
    tokens = [otp_token(item.otp_url) for item in result if item.otp_url]
    if len(tokens) != len(set(tokens)):
        raise ToolError("Bảng có URL OTP trùng nhau giữa các máy")
    return result


def parse_bulk_payload(text: str) -> tuple[list[ProxyConfig], list[BulkRecord]]:
    """Keep valid proxy/account rows from either paste box; discard surplus text."""
    proxies: list[ProxyConfig] = []
    accounts: list[BulkRecord] = []
    seen_tokens: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            records = parse_records(line, account_table=True)
        except ToolError:
            records = []
        if records:
            record = records[0]
            token = otp_token(record.otp_url)
            if token not in seen_tokens:
                if len(accounts) >= MAX_PROFILES:
                    raise ToolError("Bảng có hơn 12 hàng Amazon hợp lệ; dữ liệu chưa được gán")
                seen_tokens.add(token)
                accounts.append(replace(record, profile_name=f"q{len(accounts) + 1}"))
            continue
        try:
            found = parse_column("proxy", line)
        except ToolError:
            found = []
            for candidate in PROXY_TOKEN.findall(line):
                try:
                    found.append(parse_proxy_line(candidate))
                except ToolError:
                    pass
        if len(proxies) + len(found) > MAX_PROXY_CANDIDATES:
            raise ToolError("Danh sách có hơn 100 proxy hợp lệ; dữ liệu chưa được gán")
        proxies.extend(found)
    if not proxies and not accounts:
        raise ToolError("Clipboard không có proxy hoặc hàng Amazon hợp lệ")
    return proxies, accounts


def lines(text: str, label: str) -> list[str]:
    rows = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while rows and rows[-1] == "":
        rows.pop()
    if not rows:
        raise ToolError(f"Danh sách {label} đang trống")
    limit = MAX_PROXY_CANDIDATES if label == "proxy" else MAX_PROFILES
    if len(rows) > limit:
        raise ToolError(f"Danh sách {label} có {len(rows)} dòng; giới hạn là {limit}")
    for index, row in enumerate(rows, 1):
        if not row.strip():
            raise ToolError(f"Danh sách {label}: dòng {index} đang trống")
    return rows


def _proxy_rows(text: str) -> list[str]:
    """Accept pasted proxies separated by lines or whitespace on one line."""
    rows = []
    for line in lines(text, "proxy"):
        # Split only before another host:port:user: prefix so an existing
        # password containing ordinary spaces keeps its old meaning.
        rows.extend(re.split(r"\s+(?=[^\s:]+:[^\s:]+:[^\s:]+:)", line.strip()))
    if len(rows) > MAX_PROXY_CANDIDATES:
        raise ToolError(f"Danh sách proxy có {len(rows)} mục; giới hạn là {MAX_PROXY_CANDIDATES}")
    return rows


def parse_column(kind: str, text: str) -> list:
    label = {"proxy": "proxy", "name": "tên", "phone": "số điện thoại",
             "password": "mật khẩu"}.get(kind)
    if label is None:
        raise ValueError("Unknown column")
    rows = _proxy_rows(text) if kind == "proxy" else lines(text, label)
    if kind == "proxy":
        parsed = []
        for index, row in enumerate(rows, 1):
            try:
                parsed.append(parse_proxy_line(row.strip()))
            except ToolError as exc:
                raise ToolError(f"Proxy thứ {index}: {exc}") from exc
        return parsed
    if kind == "phone":
        for index, row in enumerate(rows, 1):
            if not PHONE.fullmatch(row.strip()):
                raise ToolError(f"Số điện thoại dòng {index} sai định dạng")
        return [row.strip() for row in rows]
    if kind == "name":
        return [row.strip() for row in rows]
    # Password whitespace is preserved intentionally; no echo of its value.
    return rows
