from django.db import models
import uuid
# Create your models here.


class BaseModel(models.Model):
    uuid = models.UUIDField("ID", primary_key=True, default=uuid.uuid4)
    creation_timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    modification_timestamp = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True