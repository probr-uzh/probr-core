from rest_framework import generics, renderers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from devices.renderers import PlainTextCommandRenderer, PlainTextCommandsRenderer
from models import Device, Status, Command
from serializers import DeviceSerializer, StatusSerializer, CommandSerializer

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

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class StatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def list(self, request, *args, **kwargs):
        #check if apikey was set in the header
        api_key = request.META.get('HTTP_API_KEY',None)
        if api_key is None:
            return Response(status=403, data='You have to provide an Api-Key in the header.')

        queryset = Status.objects.filter(device_id=api_key)

        if not queryset:
            return Response(status=403, data='The Api-Key is wrong.')
        else:
            serializer = StatusSerializer(queryset, many=True)
            return Response(status=200, data=serializer.data)


    def post(self, request, *args, **kwargs):
        api_key = request.META['HTTP_API_KEY']

        try:
            Device.objects.get(apikey=api_key)
        except Device.DoesNotExist:
            return Response(status=403,data='The Api-Key does not exist.')

        data_dict = request.data
        data_dict[u'ip'] = get_client_ip(self.request)
        data_dict[u'device'] = api_key
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

#Commands
##################################################
class CommandListView(generics.ListCreateAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandsRenderer]
    serializer_class = CommandSerializer

    def list(self, request, *args, **kwargs):

        #check the Api-Key
        response = check_authentication(request)

        #check_auth function returns None if authentication was successful
        if response is not None:
            return response #if response is not None, return the determined response from the check_auth function

        #try to get status from query parameters
        status = request.GET.get('status',None)

        #check if status query param was given or not, and act accordingly
        if status is None:
            queryset = Command.objects.filter(device=request.META.get('HTTP_API_KEY',None))
        else:
            queryset = Command.objects.filter(status=status,device=request.META.get('HTTP_API_KEY',None))

        serializer = CommandSerializer(queryset, many=True)
        return Response(status=200, data=serializer.data)



class CommandDetailsView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [renderers.JSONRenderer,renderers.BrowsableAPIRenderer,PlainTextCommandRenderer]
    serializer_class = CommandSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get(self, request, *args, **kwargs):

        #check the Api-Key
        response = check_authentication(request)

        #check_auth function returns None if authentication was successful
        if response is not None:
            return response #if response is not None, return the determined response from the check_auth function

        uuid = self.kwargs.get('uuid',None)
        if uuid is None:
            return Response(status=400, data='You have to specify a command id in the URL.')

        #find the respective command
        try:
            command = Command.objects.get(uuid=uuid,device=request.META.get('HTTP_API_KEY',None))
        except Command.DoesNotExist:
            return Response(status=404, data='There is no command for the given id.')

        serializer = CommandSerializer(command,many=False)
        return Response(status=200, data=serializer.data)



    def post(self, request, *args, **kwargs):

        #check the Api-Key
        response = check_authentication(request)

        #check_auth function returns None if authentication was successful
        if response is not None:
            return response #if response is not None, return the determined response from the check_auth function

        uuid = self.kwargs.get('uuid',None)
        if uuid is None:
            return Response(status=400, data='You have to specify a command id in the URL.')

        #find the respective command
        try:
            command = Command.objects.get(uuid=uuid,device=api_key)
        except Command.DoesNotExist:
            return Response(status=404, data='There is no command for the given id.')



        if request.META['CONTENT_TYPE'] == "application/json":
            command.status = request.data['status']
        else:
            command.result = request.FILES['result'].read()
            command.status = 2
        command.save()
        return Response('Command result saved')


def check_authentication(request):
    #check if apikey was set in the header
    api_key = request.META.get('HTTP_API_KEY',None)
    if api_key is None:
        return Response(status=403, data='You have to provide an Api-Key in the header.')

    #check if device with given apikey exists
    try:
        Device.objects.get(apikey=api_key)
    except Device.DoesNotExist:
        return Response(status=403,data='The given Api-Key is wrong.')

    #if the checks succeed, return None
    return None

