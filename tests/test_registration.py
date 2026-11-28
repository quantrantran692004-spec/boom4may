import unittest
from types import SimpleNamespace
from unittest.mock import patch

from amazon_android.core import ToolError
from amazon_android.registration import _field_for_label, fill_signup_form


class RegistrationLocatorTests(unittest.TestCase):
    def test_name_and_password_bind_to_their_own_fields(self):
        nodes = [
            {"class": "android.widget.TextView", "text": "Your name", "bounds": "[20,10][300,40]"},
            {"class": "android.widget.EditText", "bounds": "[20,55][500,105]"},
            {"class": "android.widget.TextView", "text": "Password", "bounds": "[20,145][300,175]"},
            {"class": "android.widget.EditText", "bounds": "[20,190][500,240]"},
        ]
        self.assertEqual(_field_for_label(nodes, ("Your name",))["bounds"], "[20,55][500,105]")
        self.assertEqual(_field_for_label(nodes, ("Password",))["bounds"], "[20,190][500,240]")

    def test_unknown_field_stops_before_typing(self):
        with self.assertRaises(ToolError):
            _field_for_label([{"class": "android.widget.EditText", "bounds": "[0,0][100,50]"}],
                             ("Password",))

    def test_signup_sends_short_password_without_padding_or_replacement(self):
        phone = SimpleNamespace(serial="synthetic-device")
        nodes = [
            {"class": "android.widget.Button", "text": "Continue", "clickable": "true"},
            {"class": "android.widget.TextView", "text": "Your name", "bounds": "[20,10][300,40]"},
            {"class": "android.widget.EditText", "bounds": "[20,55][500,105]"},
            {"class": "android.widget.TextView", "text": "Password", "bounds": "[20,145][300,175]"},
            {"class": "android.widget.EditText", "bounds": "[20,190][500,240]"},
        ]
        with patch("amazon_android.registration.open_entry"), \
             patch("amazon_android.registration.fill_identifier"), \
             patch("amazon_android.registration._nodes", return_value=nodes), \
             patch("amazon_android.registration._wait_nodes", return_value=nodes), \
             patch("amazon_android.registration._tap"), \
             patch("amazon_android.registration._type_into") as type_into:
            for password in ("a", "1234567"):
                with self.subTest(length=len(password)):
                    result = fill_signup_form(phone, "First", "12025550123", password)
                    self.assertFalse(result["final_submit_pressed"])
                    type_into.assert_called_with(phone, nodes[4], password)

    def test_signup_still_rejects_blank_or_unsupported_password_before_device_io(self):
        with patch("amazon_android.registration.open_entry") as open_entry:
            for password in ("", "a b", "a\tb", "mật-khẩu"):
                with self.subTest(password=password), self.assertRaises(ToolError):
                    fill_signup_form(SimpleNamespace(serial="synthetic"), "First",
                                     "12025550123", password)
            open_entry.assert_not_called()


if __name__ == "__main__":
    unittest.main()
