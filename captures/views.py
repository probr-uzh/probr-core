from rest_framework.response import Response
from rest_framework import generics
from tasks import unpack_capture
from rest_framework.renderers import JSONRenderer
from serializers import CaptureSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from models import Capture
from serializers import CaptureSerializer


class CaptureUploadView(generics.ListCreateAPIView):

    #comment this in to disable Django Rest Framework Browsable API
    #renderer_classes = (JSONRenderer,)
    serializer_class = CaptureSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get(self, request, *args, **kwargs):
        captures = Capture.objects.all();
        serializer = CaptureSerializer(captures,many=True);
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        instance = Capture(pcap=request.FILES['pcap'],longitude=request.DATA['longitude'],latitude=request.DATA['latitude'])
        instance.save()
        tags = request.DATA['tags']
        tag_list = tags.split(",")
        for tag in tag_list:
            instance.tags.add(tag)
        instance.save()
        unpack_capture.delay(instance.pk)
        return Response('Capture upload successful')



