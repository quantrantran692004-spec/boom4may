import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from amazon_android.desktop import Window


class PreparationProgressTests(unittest.TestCase):
    def test_table_shows_each_phone_stage_instead_of_generic_running(self):
        window = Window.__new__(Window)
        fields = ['host', 'port', 'otp_url', 'card', 'full_name', 'phone',
                  'amazon_password', 'profile_name']
        window.values = [{key: SimpleNamespace(get=lambda: '') for key in fields} for _ in range(2)]
        window.table_rows = [{'status': Mock()} for _ in range(2)]
        window.draft = SimpleNamespace(locked=False)
        window.jobs = {}
        window.selected = 0
        window.count = SimpleNamespace(get=lambda: '2')
        window.otp_status = ['Chưa yêu cầu mã'] * 2
        window.status = [('Đang mở Apps / App Store · 3s · q1', 'running'),
                         ('Đang chờ SHELL: On · 6s · q2', 'running')]
        window._refresh_table()
        for index in range(2):
            text = window.table_rows[index]['status'].configure.call_args.kwargs['text']
            self.assertIn(window.status[index][0], text)
            self.assertIn('OTP: Chưa yêu cầu mã', text)
