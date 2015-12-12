from __future__ import absolute_import

import importlib

from celery import shared_task

from captures.models import Capture
from probr.settings import PROBR_HANDLERS, STORE_CAPTURES

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

        try:
            handler = klass()
            handler.handle(capture)
        except:
            print handlerString + " handler failed"
    if not STORE_CAPTURES:
        capture.delete()
