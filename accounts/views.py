from rest_framework import generics
from serializers import UserSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

### Endpoints for the frontend ###
class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_object(self):
        return self.request.user