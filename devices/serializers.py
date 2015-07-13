__author__ = 'gmazlami'
from taggit_serializer.serializers import TagListSerializerField,TaggitSerializer
from rest_framework import serializers
from models import Device, Command, CommandTemplate
from models import Status

class DeviceSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Device

class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status

class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command

class CommandTemplateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = CommandTemplate
