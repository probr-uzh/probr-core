from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture


@shared_task
def unpack_capture(captureUUID):
    capture = Capture.objects.get(pk=captureUUID)
    print capture.pcap
