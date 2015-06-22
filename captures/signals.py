from django.db.models.signals import post_save
from captures.models import Capture
from captures.tasks import processCapture

__author__ = 'ale'
def processAfterSave(sender, instance, **kwargs):
    processCapture.delay(instance.uuid)

post_save.connect(processAfterSave, sender=Capture)