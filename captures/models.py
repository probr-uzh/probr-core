from django.db import models
from django.db.models import signals
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from utils.models import BaseModel, publishPostSaveMessage

# Needed for taggit to work properly with non-integer primary keys, see Issue #1225 on Redmine
class TaggedCapture(TaggedItemBase):
    content_object = models.ForeignKey('Capture')

class Capture(BaseModel):
    file = models.FileField(upload_to="captures")

    longitude = models.FloatField(default=0)

    latitude = models.FloatField(default=0)

    tags = TaggableManager(through=TaggedCapture)

signals.post_save.connect(publishPostSaveMessage, sender=Capture)