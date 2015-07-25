from rest_framework.response import Response
from rest_framework import generics
from captures.tasks import processCapture
from rest_framework.parsers import MultiPartParser, FormParser
from models import Capture
from serializers import CaptureSerializer

class CaptureUploadView(generics.ListCreateAPIView):

    queryset = Capture.objects.all()
    serializer_class = CaptureSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        instance = Capture(pcap=request.FILES['pcap'],longitude=request.DATA['longitude'],latitude=request.DATA['latitude'])
        instance.save()
        tags = request.DATA['tags']
        tag_list = tags.split(",")
        for tag in tag_list:
            instance.tags.add(tag)
        instance.save()
        processCapture.delay(instance.pk)
        return Response('Capture upload successful')
