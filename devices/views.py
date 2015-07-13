from django.views.generic import TemplateView
from rest_framework import generics, renderers
from rest_framework.mixins import DestroyModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from devices.renderers import PlainTextCommandRenderer, PlainTextCommandsRenderer
from models import Device, Status, Command, CommandTemplate
from serializers import DeviceSerializer, StatusSerializer, CommandSerializer, CommandTemplateSerializer

#Devices
##################################################
class DeviceListView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_object(self):
        uuid = self.kwargs['uuid']
        return Device.objects.get(uuid=uuid)

#Statuses
##################################################
class StatusListView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    filter_fields = ('device',)
    serializer_class = StatusSerializer

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def perform_create(self, serializer):
        serializer.save(ip=self.get_client_ip(self.request))

#Commands
##################################################
class CommandListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandsRenderer]
    serializer_class = CommandSerializer
    queryset = Command.objects.all()
    filter_fields = ('status','device',)


class CommandDetailsView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandRenderer]
    serializer_class = CommandSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_object(self):
        uuid = self.kwargs['uuid']
        return Command.objects.get(uuid=uuid)

    def post(self, request, *args, **kwargs):
        command = self.get_object()

        if request.META['CONTENT_TYPE'] == "application/json":
            command.status = request.data['status']
        else:
            command.result = request.FILES['result'].read()
            command.status = 2
        command.save()
        return Response('Command result saved')

class CommandTemplateListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer]
    serializer_class = CommandTemplateSerializer
    queryset = CommandTemplate.objects.all()
    filter_fields = ('name','execute',)

class CommandTemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer]
    serializer_class = CommandTemplateSerializer
    queryset = CommandTemplate.objects.all()
    parser_classes = (JSONParser,)