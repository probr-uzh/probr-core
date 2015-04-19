from rest_framework import generics
from models import Device, Status
from serializers import DeviceSerializer, StatusSerializer

#Devices
##################################################

class DeviceListView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDetailsView(DeviceListView):
    def get_queryset(self):
        uuid = self.kwargs['uuid']
        return Device.objects.filter(uuid = uuid)


#Statuses
##################################################

class StatusListView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer