from django.test import TestCase
from devices.models import Device, Status


class StatusTestCase(TestCase):

    def setUp(self):
        self.device = Device.objects.create(name="Pii")

    def test_usage_calculation(self):
        status = Status.objects.create(device=self.device, total_memory=128, used_memory=64, total_disk=4, used_disk=3)
        self.assertEqual(status.used_memory, 0.5)
        self.assertEqual(status.used_disk, 0.75)