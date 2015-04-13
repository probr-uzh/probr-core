from django.contrib.gis.db import models

# Create your models here.
from taggit.managers import TaggableManager
from utils.models import BaseModel


class Capture(BaseModel):
    pcap = models.FileField(upload_to="pcap")
    location = models.PointField()

    tags = TaggableManager()