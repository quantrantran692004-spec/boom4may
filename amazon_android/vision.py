"""In-memory OCR fallback for Amazon screens hidden inside Android WebViews.

OCR detections are converted to the same small node shape consumed by the
existing screen and field locators. Screenshot bytes and recognized strings
stay in memory; callers must not log node text because it may include account
or verification data.
"""
from __future__ import annotations

import difflib
import io
import queue
import copy
import threading
import unicodedata
from functools import lru_cache

from PIL import Image


AMAZON_PACKAGE = "com.amazon.mShop.android.shopping"
KNOWN_LABELS = (
    "Sign in or create account",
    "Enter mobile number or email",
    "Country/region code",
    "Create account",
    "Create an account",
    "Create your Amazon account",
    "Looks like you are new to Amazon",
    "Proceed to create an account",
    "Mobile number",
    "First and last name",
    "Verify with WhatsApp",
    "Send code by SMS",
    "Verify mobile number",
    "Enter security code",
    "Continue",
    "Create your Amazon account",
    "Shop by category",
    "Customer Service",
    "Sign In",
    "Browse menu Tab",
    "Sign in for the best experience",
    "Gifting",
    "Deals & Savings",
    "Be Inspired, Save More",
    "Health and Personal Care",
    "Pets",
    "Fashion and Beauty",
    "Groceries and Drinks",
    "Home and DIY",
    "Books and Reading",
    "Devices and Electronics",
    "Music, Video and Gaming",
    "Toys, Kids and Baby",
    "Office & Professional",
    "Sports & Outdoors",
    "Your Stuff",
    "Your Amazon Cart is empty",
    "Continue shopping",
    "Home Tab",
    "Books",
    "Electronics",
    "Home services",
    "See all",
    "Today's deals",
    "Try Prime",
    "United States +1",
    "US +1",
    "Country/Region and Language",
    "Country/Region & Language",
    "Country/Region:",
    "Language:",
    "Currency:",
    "Countries/Regions available in English",
    "Countries/Regions available in other languages",
    "United States",
    "Singapore",
    "English",
    "Done",
    "Your Orders",
    "Orders",
    "Account",
    "Lists",
    "EN",
    "Amazon.com",
    "Your Account Tab",
    "Retry",
    "Reload",
)
FIELD_LABELS = {
    "enter mobile number or email": "phone",
    "first and last name": "name",
    "enter security code": "otp",
}

WRAPPED_CARD_TITLES = (
    ("Deals &", "Savings", "Deals & Savings"),
    ("Be Inspired,", "Save More", "Be Inspired, Save More"),
    ("Groceries and", "Drinks", "Groceries and Drinks"),
    ("Health and", "Personal Care", "Health and Personal Care"),
    ("Fashion and", "Beauty", "Fashion and Beauty"),
    ("Home and", "DIY", "Home and DIY"),
    ("Devices and", "Electronics", "Devices and Electronics"),
    ("Music, Video", "and Gaming", "Music, Video and Gaming"),
    ("Books and", "Reading", "Books and Reading"),
    ("Toys, Kids and", "Baby", "Toys, Kids and Baby"),
    ("Office &", "Professional", "Office & Professional"),
    ("Sports &", "Outdoors", "Sports & Outdoors"),
)

_ocr_slots = queue.Queue()
for _slot in range(2):
    _ocr_slots.put(_slot)


@lru_cache(maxsize=2)
def _engine(slot=0):
    from rapidocr import RapidOCR

    # Each phone reader is a separate process. Without this limit, every
    # ONNX session can create a full CPU thread pool and later phones starve.
    return RapidOCR(params={
        "EngineConfig.onnxruntime.intra_op_num_threads": 1,
        "EngineConfig.onnxruntime.inter_op_num_threads": 1,
    })


def _recognize(raw, *, stop=None, remaining=None):
    from .core import ToolError

    def check():
        if stop is not None and stop.is_set():
            raise ToolError("Đã dừng máy này")
        if remaining is not None:
            remaining()

    while True:
        check()
        try:
            slot = _ocr_slots.get(timeout=0.1)
            break
        except queue.Empty:
            continue
    try:
        check()
        result = _engine(slot)(raw)
        check()  # Never act on an OCR result returned after Stop/deadline.
        # Own the result before another phone can borrow this engine.
        from types import SimpleNamespace
        return SimpleNamespace(**{key: copy.deepcopy(getattr(result, key, None))
                                  for key in ("boxes", "txts", "scores")})
    finally:
        _ocr_slots.put(slot)


def _normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return " ".join("".join(char for char in decomposed
                           if not unicodedata.combining(char)).split())


def _compact(value: str) -> str:
    return "".join(char for char in _normalize(value) if char.isalnum())


def _canonical_text(value: str) -> str:
    if _compact(value) in {_compact(first) for first, _, _ in WRAPPED_CARD_TITLES}:
        return value.strip()  # Wait for the next line of a wrapped card title.
    compact = _compact(value)
    if not compact:
        return value.strip()
    best = value.strip()
    best_score = 0.0
    for label in KNOWN_LABELS:
        candidate = _normalize(label)
        candidate_compact = _compact(candidate)
        score = difflib.SequenceMatcher(None, compact, candidate_compact).ratio()
        if compact in candidate_compact or candidate_compact in compact:
            score = max(score, min(len(compact), len(candidate_compact)) /
                        max(len(compact), len(candidate_compact)))
        if score > best_score:
            best, best_score = label, score
    return best if best_score >= 0.82 else value.strip()


def _join_wrapped_categories(detections: list[dict]) -> list[dict]:
    """Join known two-line card titles only within the same live card column."""
    titles = {_compact(label): label for _, _, label in WRAPPED_CARD_TITLES}
    joined = []
    next_id = max((item["index"] for item in detections), default=-1) + 1
    for upper in detections:
        ax1, ay1, ax2, ay2 = upper["box"]
        for lower in detections:
            bx1, by1, bx2, by2 = lower["box"]
            line_height = max(ay2 - ay1, by2 - by1)
            if not (-line_height * 0.35 <= by1 - ay2 <= line_height * 1.2 and
                    by1 - ay1 >= line_height * 0.5 and
                    abs(ax1 - bx1) <= line_height and min(ax2, bx2) > max(ax1, bx1)):
                continue
            text = " ".join((upper["raw"].strip(), lower["raw"].strip()))
            title = titles.get(_compact(text))
            if title:
                joined.append({"text": title, "raw": text,
                               "box": (min(ax1, bx1), ay1, max(ax2, bx2), by2),
                               "score": min(upper["score"], lower["score"]),
                               "index": next_id + len(joined)})
    return detections + joined


def _bounds(box) -> tuple[int, int, int, int]:
    import numpy as np

    points = np.asarray(box).reshape(-1, 2)
    return (max(0, int(points[:, 0].min())),
            max(0, int(points[:, 1].min())),
            max(0, int(points[:, 0].max())),
            max(0, int(points[:, 1].max())))


def _single_input_border(candidates: set[tuple[int, int, int, int]]
                         ) -> tuple[int, int, int, int] | None:
    if len(candidates) == 1:
        return next(iter(candidates))
    if not candidates:
        return None
    # A focused field can expose nested grey and blue outlines a few pixels
    # apart. They describe one control when every candidate almost overlaps.
    boxes = list(candidates)
    for first in boxes:
        for second in boxes:
            intersection = (max(0, min(first[2], second[2]) - max(first[0], second[0])) *
                            max(0, min(first[3], second[3]) - max(first[1], second[1])))
            area_first = (first[2] - first[0]) * (first[3] - first[1])
            area_second = (second[2] - second[0]) * (second[3] - second[1])
            if intersection / (area_first + area_second - intersection) < 0.9:
                return None
    return (min(box[0] for box in boxes), min(box[1] for box in boxes),
            max(box[2] for box in boxes), max(box[3] for box in boxes))


def _input_box(image: Image.Image, label_box: tuple[int, int, int, int],
               label_index: int, detections: list[dict]) -> tuple[int, int, int, int] | None:
    """Find a unique actual input border immediately below a known label."""
    import numpy as np

    width, height = image.size
    lx1, _, lx2, ly2 = label_box
    if not 0 <= label_index < len(detections):
        return None
    kind = FIELD_LABELS.get(_normalize(detections[label_index]["text"]))
    expected_actions = {"phone": {"continue"}, "name": {"continue"},
                        "otp": {"create your amazon account", "verify mobile number"}}
    actions = [item["box"] for item in detections
               if _normalize(item["text"]) in expected_actions.get(kind, set())
               and item["box"][1] > ly2]
    if kind is None:
        return None
    start_y = max(0, ly2 + 1)
    end_y = min(height, ly2 + max(8, int(width * 0.30)),
                min((box[1] for box in actions), default=height))
    if end_y <= start_y:
        return None

    # Analyze the full horizontal strip, rather than guessing input margins
    # from its label. RGB neutrality excludes a yellow button even when it has
    # the same dimensions as an input. Work is vectorized across image pixels.
    rgb = np.asarray(image.convert("RGB"))[start_y:end_y]
    low, high = rgb.min(axis=2), rgb.max(axis=2)
    neutral = (high - low <= 32) & (low >= 55) & (high <= 235)
    red, green, blue = (rgb[:, :, channel].astype(np.int16) for channel in range(3))
    focused_blue = ((red <= 180) & (green >= 65) & (blue >= 95) &
                    (blue <= 245) & (blue - red >= 25) &
                    (green - red >= 10) & (blue >= green - 10))
    border_pixels = neutral | focused_blue

    def runs(mask):
        edges = np.flatnonzero(np.diff(np.r_[False, mask, False]))
        return list(zip(edges[::2], edges[1::2]))

    min_width = max(30, int(width * 0.55))
    horizontal = []
    for row in np.flatnonzero(border_pixels.sum(axis=1) >= min_width * 0.80):
        wide = [(left, right) for left, right in runs(border_pixels[row])
                if right - left >= min_width * 0.80]
        if wide:
            left, right = max(wide, key=lambda pair: pair[1] - pair[0])
            horizontal.append((int(row) + start_y, int(left), int(right)))

    # Adjacent antialiased rows represent one top or bottom border stroke.
    strokes = []
    gap = max(2, int(width * 0.004))
    for row in horizontal:
        if not strokes or row[0] - strokes[-1][-1][0] > gap:
            strokes.append([row])
        else:
            strokes[-1].append(row)
    candidates = set()
    for index, upper in enumerate(strokes):
        top = upper[0][0]
        if top - ly2 > width * 0.12:
            continue
        for lower in strokes[index + 1:]:
            bottom = lower[-1][0] + 1
            field_height = bottom - top
            if not width * 0.055 <= field_height <= width * 0.19:
                continue
            inset = max(2, int(field_height * 0.28))
            inside_top, inside_bottom = top + inset, bottom - inset
            vertical = border_pixels[inside_top - start_y:inside_bottom - start_y].mean(axis=0)
            sides = [(int(left), int(right)) for left, right in runs(vertical >= 0.70)
                     if right - left <= max(4, width * 0.025)]
            stroke_left = min(row[1] for row in upper + lower)
            stroke_right = max(row[2] for row in upper + lower)
            # A rounded corner cannot extend beyond half the field height.
            # A tolerance based only on screen width also admits the sides of
            # Amazon's surrounding form card as competing input borders.
            tolerance = min(width * 0.10, field_height * 0.48)
            for left, left_end in sides:
                for right_start, right in sides:
                    if right - left < min_width or right_start <= left_end:
                        continue
                    if not (0 <= stroke_left - left <= tolerance and
                            0 <= right - stroke_right <= tolerance):
                        continue
                    if min(lx2, right) <= max(lx1, left):
                        continue
                    interior = rgb[inside_top - start_y:inside_bottom - start_y,
                                   left_end:right_start]
                    # Inputs are predominantly white inside; a solid neutral
                    # banner or dense paragraph panel is not an input border.
                    if not interior.size or (interior.min(axis=2) >= 235).mean() < 0.65:
                        continue
                    candidates.add((left, top, right, bottom))
    return _single_input_border(candidates)


def _field_contents(box: tuple[int, int, int, int], label_index: int,
                    detections: list[dict], kind: str) -> str | None:
    """Read a single text line contained by the confirmed field border."""
    x1, y1, x2, y2 = box
    contained = []
    for index, detection in enumerate(detections):
        if index == label_index:
            continue
        left, top, right, bottom = detection["box"]
        if x1 < (left + right) / 2 < x2 and y1 < (top + bottom) / 2 < y2:
            if left < x1 or right > x2 or top <= y1 or bottom >= y2:
                return None
            contained.append(detection)
    if not contained:
        return ""
    # A field value can be split into OCR words, but all words share one line.
    # Multiple lines are likely paragraph content or a wrong control.
    if max(item["box"][1] for item in contained) >= min(item["box"][3] for item in contained):
        return None
    contained.sort(key=lambda item: item["box"][0])
    values = [item["raw"].strip() for item in contained]
    return ("".join("".join(values).split()) if kind in {"phone", "otp"}
            else " ".join(values))


def _field_is_blank(image: Image.Image, box: tuple[int, int, int, int]) -> bool:
    """Do not let an OCR omission authorize typing over visible input text."""
    import numpy as np

    x1, y1, x2, y2 = box
    inset = max(3, int((y2 - y1) * 0.20))
    interior = np.asarray(image.convert("RGB"))[y1 + inset:y2 - inset,
                                                x1 + inset:x2 - inset]
    if not interior.size:
        return False
    ink = interior.min(axis=2) < 180
    if int(ink.sum()) <= max(3, interior.shape[0] * 0.20):
        return True
    columns = np.flatnonzero(ink.any(axis=0))
    # A caret is a narrow vertical stroke; visible words span a wider range.
    caret_width = max(2, int(image.width * 0.006))
    return bool(columns.size and int(columns[-1] - columns[0] + 1) <= caret_width)


def ocr_nodes(image_bytes: bytes, *, stop=None, remaining=None,
              crop: tuple[float, float] | None = None,
              text_only: bool = False) -> list[dict[str, str]]:
    """Return sanitized-shape UI nodes; text remains only in caller memory."""
    import numpy as np

    with Image.open(io.BytesIO(image_bytes)) as source:
        image = source.convert("RGB")
        offset_y = 0
        if crop is not None:
            if not text_only or not (0 <= crop[0] < crop[1] <= 1):
                raise ValueError('Text-only OCR crop must be within the screenshot')
            offset_y = int(image.height * crop[0])
            image = image.crop((0, offset_y, image.width,
                                min(image.height, int(image.height * crop[1]))))
        raw = np.asarray(image)[:, :, ::-1].copy()  # RapidOCR expects BGR arrays.
    result = _recognize(raw, stop=stop, remaining=remaining)
    boxes = getattr(result, "boxes", None)
    texts = getattr(result, "txts", None)
    scores = getattr(result, "scores", None)
    if boxes is None or texts is None or scores is None:
        return []
    detections: list[dict] = []
    for index, (box, text, score) in enumerate(zip(boxes, texts, scores)):
        text = str(text).strip()
        if not text or float(score) < 0.45:
            continue
        x1, y1, x2, y2 = _bounds(box)
        bounds = (x1, y1 + offset_y, x2, y2 + offset_y)
        detections.append({"text": _canonical_text(text), "raw": text,
                           "score": float(score), "box": bounds,
                           "index": index})

    detections = _join_wrapped_categories(detections)
    nodes: list[dict[str, str]] = []
    for index, item in enumerate(detections):
        x1, y1, x2, y2 = item["box"]
        nodes.append({"text": item["text"], "class": "android.widget.TextView",
                      "package": AMAZON_PACKAGE,
                      "bounds": f"[{x1},{y1}][{x2},{y2}]",
                      "ui_id": f"ocr-text-{index}", "ui_parent": "",
                      "visible-to-user": "true", "vision": "true"})

    if text_only:
        return nodes

    for index, item in enumerate(detections):
        field_kind = FIELD_LABELS.get(_normalize(item["text"]))
        if not field_kind or item["score"] < 0.60:
            continue
        box = _input_box(image, item["box"], index, detections)
        if box is None:
            continue
        x1, y1, x2, y2 = box
        field_text = _field_contents(box, index, detections, field_kind)
        if field_text is None or (not field_text and not _field_is_blank(image, box)):
            continue
        nodes.append({"text": field_text, "class": "android.widget.EditText",
                      "package": AMAZON_PACKAGE,
                      "bounds": f"[{x1},{y1}][{x2},{y2}]",
                      "ui_id": f"ocr-field-{field_kind}", "ui_parent": "",
                      "visible-to-user": "true", "enabled": "true",
                      "focused": "false", "focusable": "true", "vision": "true",
                      "vision-score": str(item["score"]),
                      "vision-field-kind": field_kind})
    return nodes
