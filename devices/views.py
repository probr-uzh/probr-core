from rest_framework import generics, renderers
from models import Device, Status
from serializers import DeviceSerializer, StatusSerializer

#Devices
##################################################

class DeviceListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailsView(DeviceListView):
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return Device.objects.filter(uuid = uuid)


#Statuses
##################################################

class StatusListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer]
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
