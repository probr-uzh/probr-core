from django.db import models


from utils.models import BaseModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


DEVICE_TYPE_CHOICES = (
    ('RPA', 'Raspberry Pi Model A'),
    ('RPB', 'Raspberry Pi Model B'),
    ('DWR', 'DD-WRT Router'),
    ('OWR', 'OpenWRT Router'),
    ('UKW', 'Unknown'),
)

# Needed for taggit to work properly with non-integer primary keys, see Issue #1225 on Redmine
class TaggedDevice(TaggedItemBase):
    content_object = models.ForeignKey('Device')


class Device(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    type = models.CharField(max_length=3, choices=DEVICE_TYPE_CHOICES, default="UKW")

    wifi_chip = models.CharField(max_length=255, blank=True, default="")

    os = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    tags = TaggableManager(through=TaggedDevice)


class Status(BaseModel):
    device = models.ForeignKey(Device, related_name="statuses")

    ip = models.GenericIPAddressField(default="0.0.0.0")
    cpu_load = models.FloatField(default=0)

    total_memory = models.IntegerField(default=0)
    used_memory = models.IntegerField(default=0)

    total_disk = models.IntegerField(default=0)
    used_disk = models.IntegerField(default=0)

    def memory_usage(self):
        return self.used_memory/self.total_memory

    def disk_usage(self):
        return self.used_disky/self.total_disk