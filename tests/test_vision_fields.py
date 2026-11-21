import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from PIL import Image, ImageDraw

from amazon_android.vision import _input_box, _single_input_border, ocr_nodes


def detection(text, box, index=0):
    return {"text": text, "raw": text, "box": box, "score": 0.99, "index": index}


class VisionFieldTests(unittest.TestCase):
    def _form(self, *, scale=1, left=12, right=348, value="Example User"):
        width, height = 360 * scale, 640 * scale
        box = tuple(item * scale for item in (left, 140, right, 182))
        label = tuple(item * scale for item in (30, 110, 180, 124))
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(box, radius=9 * scale, outline="#999999", width=scale)
        draw.rounded_rectangle((left * scale, 300 * scale, right * scale, 340 * scale),
                               radius=16 * scale, fill="#ffd814")
        items = [detection("First and last name", label, 0),
                 detection("Continue", (150 * scale, 310 * scale,
                                         210 * scale, 325 * scale), 1)]
        if value:
            items.append(detection(value, ((left + 12) * scale, 151 * scale,
                                            (left + 120) * scale, 169 * scale), 2))
        return image, box, label, items

    def test_detects_actual_field_sides_with_varied_margins_scales_and_filled_text(self):
        for scale, left, right in ((1, 12, 348), (2, 55, 325),
                                   (4, 25, 310), (1, 65, 332)):
            with self.subTest(scale=scale, left=left, right=right):
                image, expected, label, items = self._form(
                    scale=scale, left=left, right=right)
                found = _input_box(image, label, 0, items)
                self.assertIsNotNone(found)
                for actual, wanted in zip(found, expected):
                    self.assertLessEqual(abs(actual - wanted), 3 * scale)

    def test_login_verify_button_keeps_otp_field_detection(self):
        image, expected, label, items = self._form(value="222222")
        items[0]["text"] = "Enter security code"
        items[1]["text"] = "Verify mobile number"
        found = _input_box(image, label, 0, items)
        self.assertIsNotNone(found)
        for actual, wanted in zip(found, expected):
            self.assertLessEqual(abs(actual - wanted), 3)

    def _nodes(self, image, items):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        result = SimpleNamespace(
            boxes=[[(box[0], box[1]), (box[2], box[1]),
                    (box[2], box[3]), (box[0], box[3])] for box in
                   (item["box"] for item in items)],
            txts=[item["text"] for item in items],
            scores=[item["score"] for item in items])
        with patch("amazon_android.vision._engine", return_value=lambda _raw: result):
            return ocr_nodes(buffer.getvalue())

    def test_filled_field_retains_value_and_excludes_paragraph_below(self):
        image, _, _, items = self._form(left=12, right=348)
        items.append(detection("By enrolling you consent to automated notifications",
                               (30, 202, 330, 216), 3))
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["text"], "Example User")

    def test_600_pixel_form_keeps_field_after_name_was_entered(self):
        image = Image.new("RGB", (600, 1100), "white")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((30, 270, 565, 335), radius=18,
                               outline="#999999", width=2)
        draw.rounded_rectangle((30, 420, 565, 485), radius=18, fill="#ffd814")
        items = [detection("First and last name", (30, 229, 265, 249), 0),
                 detection("Example User", (42, 290, 190, 312), 1),
                 detection("Continue", (240, 438, 355, 465), 2)]
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["text"], "Example User")

    def test_focused_blue_outline_is_retained_for_readback(self):
        image, box, label, items = self._form()
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(box, radius=9, outline="#007eb9", width=2)
        found = _input_box(image, label, 0, items)
        self.assertIsNotNone(found)
        self.assertLessEqual(abs(found[0] - box[0]), 2)
        self.assertLessEqual(abs(found[2] - box[2]), 2)

    def test_nested_focused_outlines_are_one_otp_field(self):
        self.assertEqual(_single_input_border({
            (23, 229, 358, 282), (26, 229, 362, 282),
            (23, 229, 362, 282),
        }), (23, 229, 362, 282))
        self.assertIsNone(_single_input_border({
            (23, 229, 362, 282), (23, 330, 362, 382),
        }))

    def test_outer_form_card_sides_do_not_make_input_border_ambiguous(self):
        image = Image.new("RGB", (327, 559), "white")
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((12, 45, 316, 474), radius=6,
                               outline="#bbbbbb", width=1)
        draw.rounded_rectangle((26, 120, 302, 155), radius=10,
                               outline="#b6b6b6", width=1)
        items = [detection("First and last name", (28, 102, 146, 116), 0),
                 detection("Continue", (136, 331, 194, 347), 1)]
        field = _input_box(image, items[0]["box"], 0, items)
        self.assertIsNotNone(field)
        self.assertLessEqual(abs(field[0] - 26), 2)
        self.assertLessEqual(abs(field[2] - 303), 2)

    def test_yellow_band_is_not_an_input_and_does_not_trigger_proportional_guess(self):
        image, _, label, items = self._form(value="")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 130, 359, 190), fill="white")
        draw.rounded_rectangle((12, 140, 348, 182), radius=9, fill="#ffd814")
        self.assertIsNone(_input_box(image, label, 0, items))

    def test_separator_lines_without_vertical_sides_are_not_an_input(self):
        image, _, label, items = self._form(value="")
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 130, 359, 190), fill="white")
        draw.line((12, 140, 348, 140), fill="#999999")
        draw.line((12, 182, 348, 182), fill="#999999")
        self.assertIsNone(_input_box(image, label, 0, items))

    def test_unknown_label_cannot_make_a_field(self):
        image, _, label, items = self._form(left=20, right=322, value="")
        items[0]["text"] = "Notification preferences"
        self.assertIsNone(_input_box(image, label, 0, items))

    def test_confirmed_border_remains_readable_when_keyboard_covers_action(self):
        image, _, _, items = self._form()
        items = [item for item in items if item["text"] != "Continue"]
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["text"], "Example User")

    def test_multiline_paragraph_inside_bordered_control_is_not_a_field_value(self):
        image, _, _, items = self._form(value="")
        items.extend([detection("Terms and conditions apply", (30, 145, 300, 156), 2),
                      detection("Please read before continuing", (30, 164, 310, 175), 3)])
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(fields, [])

    def test_visible_value_missed_by_ocr_is_not_reported_as_an_empty_field(self):
        image, _, _, items = self._form(value="")
        draw = ImageDraw.Draw(image)
        draw.text((30, 151), "Example User", fill="black")
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(fields, [])

    def test_empty_field_with_narrow_caret_can_still_be_focused(self):
        image, _, _, items = self._form(value="")
        ImageDraw.Draw(image).line((30, 149, 30, 173), fill="black", width=1)
        fields = [node for node in self._nodes(image, items)
                  if node["class"] == "android.widget.EditText"]
        self.assertEqual(len(fields), 1)
        self.assertEqual(fields[0]["text"], "")


if __name__ == "__main__":
    unittest.main()
