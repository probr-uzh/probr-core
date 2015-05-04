from django.test import TestCase
from devices.models import Device, Status
from django.db import IntegrityError
import re


class StatusTestCase(TestCase):
    def test_uuid(self):
        """ Tests uuid to be RFC 4122 conform """
        test_device = Device.objects.create(name="Test Device")
        test_status = Status.objects.create(device=test_device)
        test_device.save()
        test_status.save()
        uuid = test_status.uuid
        retrieved_status = Status.objects.get(uuid=uuid)
        self.assertEqual(len(retrieved_status.uuid), 36)
        p = re.compile('^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', re.IGNORECASE)
        self.assertTrue(p.match(retrieved_status.uuid))

    def test_status_without_device(self):
        """ Status cannot exist without device """
        with self.assertRaises(IntegrityError):
            test_status = Status.objects.create()


    def test_usage_calculation(self):
        test_device = Device.objects.create(name="Test Device")
        test_status = Status.objects.create(device=test_device, total_memory=128, used_memory=64, total_disk=4, used_disk=3)
        test_device.save()
        test_status.save()
        uuid = test_status.uuid
        retrieved_status = Status.objects.get(uuid=uuid)
        self.assertEqual(retrieved_status.total_disk, 4)
        self.assertEqual(retrieved_status.used_disk, 3)
        self.assertEqual(retrieved_status.disk_usage(), 0.75)
        self.assertEqual(retrieved_status.total_memory, 128)
        self.assertEqual(retrieved_status.used_memory, 64)
        self.assertEqual(retrieved_status.memory_usage(), 0.5)

    def test_cpu_load(self):
        test_device = Device.objects.create(name="Test Device")
        test_status = Status.objects.create(device=test_device, cpu_load=65.487364538193746)
        test_device.save()
        test_status.save()
        uuid = test_status.uuid
        retrieved_status = Status.objects.get(uuid=uuid)
        self.assertAlmostEqual(retrieved_status.cpu_load, 65.487361111111111, 5)



class DeviceTestCase(TestCase):   <
    def test_uuid(self):
        """ Tests uuid to be RFC 4122 conform """
        test_device = Device.objects.create(name="Test Device")
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(len(test_device.uuid), 36)
        p = re.compile('^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', re.IGNORECASE)
        self.assertTrue(p.match(test_device.uuid))

    def test_statuses(self):
        test_device = Device.objects.create(name="Test Device")
        test_status1 = Status.objects.create(device=test_device)
        test_status2 = Status.objects.create(device=test_device)
        test_status3 = Status.objects.create(device=test_device)
        test_device.save()
        uuid = test_device.uuid
        retrieved_device = Device.objects.get(uuid=uuid)
        self.assertEqual(len(retrieved_device.statuses.all()), 3)

    def test_tags(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.tags.add("one","two","three","complicated,tag")
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(len(test_device.tags.names()), 4)
        self.assertTrue("one" in test_device.tags.names())
        self.assertTrue("two" in test_device.tags.names())
        self.assertTrue("three" in test_device.tags.names())
        self.assertTrue("complicated,tag" in test_device.tags.names())
        print(test_device.tags.names())

    def test_name(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(test_device.name, "Test Device")

    def test_type(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.type = "ABC"
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(test_device.type, "ABC")

    def test_wifi_chip(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.wifi_chip = "BCM2835"
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(test_device.wifi_chip, "BCM2835")

    def test_os(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.os = "Free BSD"
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(test_device.os, "Free BSD")

    def test_description(self):
        test_device = Device.objects.create(name="Test Device")
        test_device.description = "Device on upper floor. Used to track people across the office."
        test_device.save()
        uuid = test_device.uuid
        test_device = Device.objects.get(uuid=uuid)
        self.assertEqual(test_device.description, "Device on upper floor. Used to track people across the office.")
