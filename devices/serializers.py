__author__ = 'gmazlami'

from rest_framework import serializers
from models import Device, Command
from models import Status

class DeviceSerializer(serializers.ModelSerializer):

    tags = serializers.StringRelatedField(many=True)


    class Meta:
        model = Device


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command