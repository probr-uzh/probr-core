from django.db import models
import uuid
# Create your models here.
from taggit.managers import TaggableManager
from utils.models import BaseModel


DEVICE_TYPE_CHOICES = (
    ('RPA', 'Raspberry Pi Model A'),
    ('RPB', 'Raspberry Pi Model B'),
    ('DWR', 'DD-WRT Router'),
    ('OWR', 'OpenWRT Router'),
    ('UKW', 'Unknown'),
)

class Device(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    type = models.CharField(max_length=2, choices=DEVICE_TYPE_CHOICES, default="UKW")

    wifi_chip = models.CharField(max_length=255, blank=True, default="")

    os = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    tags = TaggableManager()


class Status(BaseModel):
    device = models.ForeignKey(Device, related_name="statuses")

    ip = models.GenericIPAddressField(default="0.0.0.0")
    cpu_load = models.FloatField(default=0)

    total_memory = models.IntegerField(default=0)
    used_memory = models.IntegerField(default=0)

    total_disk = models.IntegerField(default=0)
    used_disk = models.IntegerField(default=0)

    def memory_usage(self):
        return float(self.used_memory)/float(self.total_memory)

    def disk_usage(self):
        return float(self.used_disk)/float(self.total_disk);
