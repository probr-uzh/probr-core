__author__ = 'gmazlami'

from rest_framework import serializers
from models import Device
from models import Status

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status