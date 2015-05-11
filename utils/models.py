import json
from django.core import serializers
from django.db import models
import uuid


#automatically generated UUID field
from django.forms import model_to_dict
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

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

def publishMessage(topic, message="update"):
    redis_publisher = RedisPublisher(facility=topic, broadcast=True)
    message = RedisMessage(message)
    redis_publisher.publish_message(message)

def publishPostSaveMessage(sender, instance, created, **kwargs):
    payload = serializers.serialize('json', [instance, ])
    struct = json.loads(payload)
    payload = json.dumps(struct[0]['fields'])
    publishMessage(instance._meta.verbose_name_plural,message=payload)

class BaseModel(models.Model):
    #uuid = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    uuid = UUIDField("ID", primary_key=True, editable=False)
    creation_timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    modification_timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

