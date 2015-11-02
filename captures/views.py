from rest_framework.response import Response
from rest_framework import generics
from captures.tasks import processCapture
from rest_framework.parsers import MultiPartParser, FormParser
from models import Capture
from serializers import CaptureSerializer
from rest_framework import filters
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class CaptureUploadView(generics.ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Capture.objects.all()
    serializer_class = CaptureSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        instance = Capture.objects.create(file=request.FILES['pcap'],longitude=request.DATA['longitude'],latitude=request.DATA['latitude'])
        tags = request.DATA['tags']
        tag_list = tags.split(",")
        for tag in tag_list:
            instance.tags.add(tag)
        instance.save()
        processCapture.delay(instance.pk)
        return Response('Capture upload successful')

class CaptureListView(generics.ListCreateAPIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Capture.objects.all().order_by('-creation_timestamp')
    serializer_class = CaptureSerializer
    parser_classes = (MultiPartParser, FormParser,)
