from rest_framework.serializers import ModelSerializer
from models import Capture

class CaptureSerializer(ModelSerializer):
    class Meta:
        model = Capture
