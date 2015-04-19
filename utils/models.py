from django.db import models
import uuid


#automatically generated UUID field
class UUIDField(models.CharField) :

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

class BaseModel(models.Model):
    #uuid = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    uuid = UUIDField("ID", primary_key=True, editable=False)
    creation_timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    modification_timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True