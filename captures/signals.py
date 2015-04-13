from django.db.models.signals import post_save
from captures.models import Capture
from captures.tasks import unpack_capture

__author__ = 'ale'
def unpack_after_save(sender, instance, **kwargs):
    unpack_capture.delay(instance.uuid)

post_save.connect(unpack_after_save, sender=Capture)