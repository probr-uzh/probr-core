from django.test import TestCase
from devices.models import Device, Status
import re


class StatusTestCase(TestCase):

    def setUp(self):
        self.device = Device.objects.create(name="Pii")

    def test_uuid(self):
        """
        :return: Tests uuid to be RFC 4122 conform
        """
        status = Status.objects.create(device=self.device)
        self.assertEqual(len(status.uuid), 36)
        p = re.compile('^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', re.IGNORECASE)
        self.assertTrue(p.match(status.uuid))

    def test_usage_calculation(self):
        status = Status.objects.create(device=self.device, total_memory=128, used_memory=64, total_disk=4, used_disk=3)
        self.assertEqual(status.total_memory, 128)
        self.assertEqual(status.used_memory, 64)
        self.assertEqual(status.total_disk, 4)
        self.assertEqual(status.used_disk, 3)
        self.assertEqual(status.memory_usage(), 0.5)
        self.assertEqual(status.disk_usage(), 0.75)