from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture
from probr.base_settings import PROBR_HANDLERS

def recursiveImport(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

@shared_task
def processCapture(captureUUID):
    capture = Capture.objects.get(pk=captureUUID)
    for handlerString in PROBR_HANDLERS:
        klass = recursiveImport(handlerString)
        handler = klass()
        handler.handle(capture)