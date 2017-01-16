__author__ = 'gmazlami'
from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from models import Device, Command, CommandTemplate
from models import Status


class DeviceSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        exclude = []
        model = Device


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Status


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Command


class CommandTemplateSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        exclude = []
        model = CommandTemplate
