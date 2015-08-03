__author__ = 'gmazlami'

from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from models import Device

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

        return (user, None)