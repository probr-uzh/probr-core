from rest_framework.serializers import ModelSerializer, StringRelatedField
from models import Capture

class CaptureSerializer(ModelSerializer):

    tags = StringRelatedField(many=True)

    class Meta:
        model = Capture
