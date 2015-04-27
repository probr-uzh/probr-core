from rest_framework.serializers import ModelSerializer, StringRelatedField
from taggit_serializer.serializers import TagListSerializerField,TaggitSerializer
from models import Capture

class CaptureSerializer(TaggitSerializer,ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Capture
