from captures.models import Capture
from django.db import models
from devices.models import Device


class DeviceCapture(Capture):
    device = models.ForeignKey(Device)