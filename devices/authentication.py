__author__ = 'gmazlami'


from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from models import Device
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER

class ApikeyAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        api_key = request.META.get('HTTP_API_KEY',None)
        if api_key is None:
            return None

        #check if device with given apikey exists
        try:
            device = Device.objects.get(apikey=api_key)
        except Device.DoesNotExist:
            raise exceptions.AuthenticationFailed('Api-Key is wrong: No device with such an Api-Key exists.')

        #find out which user owns this device
        try:
            user = User.objects.get(id=device.user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Api-Key is wrong: The given user that the device belongs to doesnt exist.')

        print("Authentication:  Apikey=" + api_key)
        print("Authentication:  User=" + str(user))
        return (user,None)


class WebTokenAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)

        payload = jwt_decode_handler(jwt_value)

        user = self.authenticate_credentials(payload)

        print("User for given WebToken: " + str(user))

        return super(WebTokenAuthentication,self).authenticate(request)