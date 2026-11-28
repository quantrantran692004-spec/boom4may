import unittest

from amazon_android.core import ToolError
from amazon_android.proxy_reserve import ProxyReserve
from amazon_android.swarmote_desktop import ProxyConfig


def proxy(number):
    return ProxyConfig("socks5", f"proxy{number}.example", 1000 + number,
                       "user", f"password{number}")


class ProxyReserveTests(unittest.TestCase):
    def test_fifo_take_removes_proxy_once_and_repeated_paste_does_not_restore_it(self):
        reserve = ProxyReserve("batch-1")
        self.assertEqual(reserve.add([proxy(1), proxy(2), proxy(1)]), 2)
        self.assertEqual(reserve.take("batch-1"), (proxy(1), 1))
        self.assertEqual(reserve.add([proxy(1), proxy(2)]), 0)
        self.assertEqual(reserve.snapshot(), (proxy(2),))
        self.assertEqual(reserve.take("batch-1"), (proxy(2), 0))
        self.assertIsNone(reserve.take("batch-1"))

    def test_new_batch_keeps_unused_but_rejects_old_worker(self):
        reserve = ProxyReserve("batch-1")
        reserve.add([proxy(1), proxy(2)])
        reserve.activate("batch-2")
        self.assertIsNone(reserve.take("batch-1"))
        self.assertEqual(reserve.snapshot(), (proxy(1), proxy(2)))
        self.assertEqual(reserve.take("batch-2"), (proxy(1), 1))

    def test_take_skips_current_proxy_without_consuming_it(self):
        reserve = ProxyReserve("batch-1")
        reserve.add([proxy(1), proxy(2)])
        self.assertEqual(reserve.take("batch-1", exclude=proxy(1)),
                         (proxy(2), 1))
        self.assertEqual(reserve.snapshot(), (proxy(1),))
        self.assertIsNone(reserve.take("batch-1", exclude=proxy(1)))
        self.assertEqual(reserve.snapshot(), (proxy(1),))

    def test_limit_is_atomic_and_active_proxy_is_not_added(self):
        reserve = ProxyReserve("batch-1")
        self.assertEqual(reserve.add([proxy(1), proxy(2)], forbidden=[proxy(1)]), 1)
        self.assertEqual(reserve.snapshot(), (proxy(2),))
        with self.assertRaises(ToolError):
            reserve.add([proxy(i) for i in range(3, 103)])
        self.assertEqual(reserve.snapshot(), (proxy(2),))


if __name__ == "__main__":
    unittest.main()
