from rest_framework import generics, renderers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from devices.renderers import PlainTextCommandRenderer, PlainTextCommandsRenderer
from models import CommandTemplate
from serializers import CommandTemplateSerializer
from models import Device, Status, Command
from authentication import ApikeyAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from serializers import DeviceSerializer, StatusSerializer, CommandSerializer


### Endpoints for the frontend ###
class DeviceListView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated():
            user = request.user

        request.data[u'user'] = user.id
        return super(DeviceListView, self).post(request,*args,**kwargs)


class DeviceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        uuid = self.kwargs['uuid']
        return Device.objects.get(uuid=uuid)


class StatusList(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    authentication_classes = (JSONWebTokenAuthentication,)
    filter_fields = ('device',)

class CommandList(generics.ListCreateAPIView):
    queryset = Command.objects.all().order_by('-creation_timestamp')
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandsRenderer]
    serializer_class = CommandSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    filter_fields = ('device',)
    
class CommandDetails(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandRenderer]
    serializer_class = CommandSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        #get uuid from endpoint url
        uuid = self.kwargs.get('uuid',None)
        return Command.objects.get(uuid=uuid)

class CommandTemplateListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer]
    serializer_class = CommandTemplateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = CommandTemplate.objects.all()
    filter_fields = ('name','execute',)

class CommandTemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer]
    serializer_class = CommandTemplateSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = CommandTemplate.objects.all()
    parser_classes = (JSONParser,)



### Endpoints for the devices ###

class StatusList_Devices(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = (ApikeyAuthentication,)

    def list(self, request, *args, **kwargs):
        device = Device.objects.get(apikey=request.META.get('HTTP_API_KEY',None))
        queryset = Status.objects.filter(device_id=device.uuid)
        serializer = StatusSerializer(queryset, many=True)
        return Response(status=200, data=serializer.data)


    def post(self, request, *args, **kwargs):
        device = Device.objects.get(apikey=request.META['HTTP_API_KEY'])
        data_dict = request.data
        data_dict[u'ip'] = get_client_ip(self.request)
        data_dict[u'device'] = device.uuid
        serializer = StatusSerializer(data=data_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        else:
            return Response(status=400,data='Bad Request.')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CommandList_Devices(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandsRenderer]
    serializer_class = CommandSerializer
    authentication_classes = (ApikeyAuthentication,)

    def list(self, request, *args, **kwargs):

        device = Device.objects.get(apikey=request.META.get('HTTP_API_KEY',None))

        #try to get status from query parameters
        status = request.GET.get('status',None)

        #check if status query param was given or not, and act accordingly
        if status is None:
            queryset = Command.objects.filter(device_id=device.uuid)
        else:
            queryset = Command.objects.filter(status=status,device_id=device.uuid)

        serializer = CommandSerializer(queryset, many=True)
        return Response(status=200, data=serializer.data)



class CommandDetails_Devices(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandRenderer]
    serializer_class = CommandSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)
    authentication_classes = (ApikeyAuthentication,)


    def get(self, request, *args, **kwargs):

        #get uuid from endpoint url
        uuid = self.kwargs.get('uuid',None)

        #get the device that sent the request
        device = Device.objects.get(apikey=request.META.get('HTTP_API_KEY',None))

        #find the respective command
        try:
            command = Command.objects.get(uuid=uuid,device_id=device.uuid)
        except Command.DoesNotExist:
            return Response(status=404, data='There is no command for the given id.')

        serializer = CommandSerializer(command,many=False)
        return Response(status=200, data=serializer.data)



    def post(self, request, *args, **kwargs):

        #get uuid from endpoint url
        uuid = self.kwargs.get('uuid',None)

        #get the device that sent the request
        device = Device.objects.get(apikey=request.META.get('HTTP_API_KEY',None))

        #find the respective command
        try:
            command = Command.objects.get(uuid=uuid,device_id=device.uuid)
        except Command.DoesNotExist:
            return Response(status=404, data='There is no command for the given id.')


        if request.META['CONTENT_TYPE'] == "application/json":
            command.status = request.data['status']
        else:
            if hasattr(request.FILES,"result"):
                command.result = request.FILES['result'].read()
            else:
                command.result = request.body

        command.save()
        return Response('Command updated')
