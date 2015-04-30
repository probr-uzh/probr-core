from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from utils.models import BaseModel

# Needed for taggit to work properly with non-integer primary keys, see Issue #1225 on Redmine
class TaggedCapture(TaggedItemBase):
    content_object = models.ForeignKey('Capture')

class Capture(BaseModel):
    pcap = models.FileField(upload_to="pcap")

    longitude = models.FloatField(default=0)

    latitude = models.FloatField(default=0)

    tags = TaggableManager(through=TaggedCapture)


