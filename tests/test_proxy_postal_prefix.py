import unittest
from types import SimpleNamespace

from amazon_android.swarmote_desktop import _proxy_postal_prefix


def controls(*names):
    return [SimpleNamespace(element_info=SimpleNamespace(name=name)) for name in names]


class ProxyPostalPrefixTests(unittest.TestCase):
    def test_reads_first_four_digits_beside_city_after_passed_test(self):
        nodes = controls('Host', 'us.cliproxy.io', 'Port', '3010', 'Test Passed',
                         'IP Address', '172.59.108.6', 'Country', 'United States (US)',
                         'Region', 'Alabama / AL', 'City', 'Gulf Shores', '36547',
                         'Timezone', 'America/Chicago', 'Account', 'user12345')
        self.assertEqual(_proxy_postal_prefix(nodes), '3654')

    def test_missing_or_failed_postal_result_is_optional(self):
        self.assertIsNone(_proxy_postal_prefix(controls('Test Failed', 'City', '36547')))
        self.assertIsNone(_proxy_postal_prefix(controls('Test Passed', 'City',
                                                        'Gulf Shores', 'Timezone', '36547')))


if __name__ == '__main__':
    unittest.main()
