from django.test import TestCase
from django.conf import settings

class SettingsTestCase(TestCase):
    def test_allowed_hosts(self):
        self.assertEqual(settings.ALLOWED_HOSTS, ['localhost', '127.0.0.1', 'testserver'])

    def test_time_zone(self):
        self.assertEqual(settings.TIME_ZONE, 'EET')
