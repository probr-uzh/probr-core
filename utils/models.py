import json
from django.core import serializers
from django.db import models
import uuid


#automatically generated UUID field
from django.forms import model_to_dict
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import logging

logger = logging.getLogger(__name__)

class UUIDField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)

def publishMessage(topic, message="update", groups=[]):

    if not groups:
        redis_publisher = RedisPublisher(facility=topic, broadcast=True)
    else:
        redis_publisher = RedisPublisher(facility=topic, groups=groups)

    message = RedisMessage(message)
    redis_publisher.publish_message(message)

def publishPostSaveMessageDevice(sender, instance, created, **kwargs):
    payload = serializers.serialize('json', [instance, ])
    struct = json.loads(payload)
    struct[0]['fields']['object_type'] = instance._meta.verbose_name + ':update'
    struct[0]['fields']['apikey'] = instance.apikey # also send apikey
    payload = json.dumps(struct[0]['fields'])

    # also publish to foreign key fields, to enable grouping/filtering on client-side
    # for field in instance._meta.fields:
    #    if field.get_internal_type() == "ForeignKey":
    #        group = field.name + '-' + getattr(instance, field.name).uuid
    #        publishMessage(instance._meta.verbose_name_plural, message=payload, groups=[group])

    publishMessage("socket", message=payload)

def publishPostSaveMessage(sender, instance, created, **kwargs):
    payload = serializers.serialize('json', [instance, ])
    struct = json.loads(payload)
    struct[0]['fields']['object_type'] = instance._meta.verbose_name + ':update'
    struct[0]['fields']['uuid'] = instance.uuid # also send uuid
    payload = json.dumps(struct[0]['fields'])

    # also publish to foreign key fields, to enable grouping/filtering on client-side
    # for field in instance._meta.fields:
    #    if field.get_internal_type() == "ForeignKey":
    #        group = field.name + '-' + getattr(instance, field.name).uuid
    #        publishMessage(instance._meta.verbose_name_plural, message=payload, groups=[group])

    publishMessage("socket", message=payload)

class BaseModel(models.Model):
    #uuid = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    uuid = UUIDField("ID", primary_key=True, editable=False)
    creation_timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    modification_timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

