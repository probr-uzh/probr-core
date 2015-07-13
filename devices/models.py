from django.db import models
from django.db.models import signals

from utils.models import BaseModel, publishPostSaveMessage
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

DEVICE_TYPE_CHOICES = (
    ('RPA', 'Raspberry Pi Model A'),
    ('RPB', 'Raspberry Pi Model B'),
    ('ODR', 'ODROID'),
    ('DWR', 'DD-WRT Router'),
    ('OWR', 'OpenWRT Router'),
    ('UKW', 'Unknown'),
)


COMMAND_STATUS_CHOICES = (
    (0, 'Not executed yet'),
    (1, 'Executing'),
    (2, 'Executed')
)



# Needed for taggit to work properly with non-integer primary keys, see Issue #1225 on Redmine
class TaggedDevice(TaggedItemBase):
    content_object = models.ForeignKey('Device')

class Device(BaseModel):
    name = models.CharField(max_length=255)

    type = models.CharField(max_length=3, choices=DEVICE_TYPE_CHOICES, default="UKW")

    wifi_chip = models.CharField(max_length=255, blank=True, default="")

    os = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")

    tags = TaggableManager(through=TaggedDevice)

    def __unicode__(self):
        return self.name

signals.post_save.connect(publishPostSaveMessage, sender=Device)

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
        return float(self.used_disk)/float(self.total_disk)

    def __unicode__(self):
        return unicode(self.device)+" memory:"+unicode(self.memory_usage())+""

    class Meta:
        verbose_name_plural = "statuses"
        ordering = ['-creation_timestamp']

signals.post_save.connect(publishPostSaveMessage, sender=Status)

class Command(BaseModel):
    device = models.ForeignKey(Device, related_name="commands")

    execute = models.TextField()
    result = models.TextField(blank=True, default="")

    status = models.IntegerField(default=0, choices=COMMAND_STATUS_CHOICES)

    def save(self, *args, **kwargs):
        """
        We don't want carriage returns in a shell script,
        make sure all lines are separated by \n
        """
        self.execute = "\n".join(self.execute.splitlines())
        super(Command, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.execute

signals.post_save.connect(publishPostSaveMessage, sender=Command)

class TaggedCommandTemplate(TaggedItemBase):
    content_object = models.ForeignKey('CommandTemplate')

class CommandTemplate(BaseModel):
    name = models.CharField(max_length=255)

    execute = models.TextField()

    tags = TaggableManager(through=TaggedCommandTemplate)

    def __unicode__(self):
        return self.execute