from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture
from probr.base_settings import PROBR_HANDLERS

import importlib

def recursiveImport(full_class_string):
    """
    dynamically load a class from a string
    """
    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

@shared_task
def processCapture(captureUUID):
    capture = Capture.objects.get(pk=captureUUID)
    for handlerString in PROBR_HANDLERS:
        klass = recursiveImport(handlerString)
        handler = klass()
        handler.handle(capture)