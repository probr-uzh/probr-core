from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from audit_log.models.fields import CreatingUserField

from utils.models import BaseModel, publishPostSaveMessage,publishPostSaveMessageDevice, UUIDField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

import uuid
import hashlib

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
    (2, 'Executed'),
    (3, 'Aborted'),
)



# Needed for taggit to work properly with non-integer primary keys, see Issue #1225 on Redmine
class TaggedDevice(TaggedItemBase):
    content_object = models.ForeignKey('Device')

class Device(models.Model):
    uuid = UUIDField("ID", primary_key=True, editable=False)

    user = models.ForeignKey(User)

    apikey = models.CharField(max_length=64, unique=True, editable=False)

    name = models.CharField(max_length=255)

    creation_timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    modification_timestamp = models.DateTimeField(auto_now=True, db_index=True)

    type = models.CharField(max_length=3, choices=DEVICE_TYPE_CHOICES, default="UKW")

    wifi_chip = models.CharField(max_length=255, blank=True, default="")

    os = models.CharField(max_length=255, blank=True, default="")

    description = models.TextField(blank=True, default="")

    tags = TaggableManager(through=TaggedDevice)

    longitude = models.FloatField(default=0)

    latitude = models.FloatField(default=0)

    def __unicode__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.apikey:
            #generate random seed for the api-key
            seed = uuid.uuid4()

            #hash the random seed to obtain an api-key
            self.apikey = hashlib.sha256(str(seed)).hexdigest()

        super(Device, self).save(*args, **kwargs)


signals.post_save.connect(publishPostSaveMessageDevice, sender=Device)

class Status(BaseModel):
    device = models.ForeignKey(Device, related_name="statuses")

    ip = models.GenericIPAddressField(default="0.0.0.0")
    cpu_load = models.FloatField(default=0)

    total_memory = models.IntegerField(default=0)
    used_memory = models.IntegerField(default=0)

    total_disk = models.IntegerField(default=0)
    used_disk = models.IntegerField(default=0)

    def memory_usage(self):
        if float(self.total_disk)>0:
            return float(self.used_memory)/float(self.total_memory)
        else:
            return 0
        
    def disk_usage(self):
        if float(self.total_disk)>0:
            return float(self.used_disk)/float(self.total_disk)
        else:
            return 0

    def __unicode__(self):
        return unicode(self.device)+" memory:"+unicode(self.memory_usage())+""

    class Meta:
        verbose_name_plural = "statuses"
        ordering = ['-creation_timestamp']

def statusThrottler(sender, instance, **kwargs):
    statuses = Status.objects.order_by('-modification_timestamp')[:1000].values_list("uuid", flat=True)  # only retrieve ids.
    Status.objects.exclude(pk__in=list(statuses)).delete()
signals.post_save.connect(statusThrottler, sender=Status)

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