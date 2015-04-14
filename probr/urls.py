from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers, serializers, viewsets
from devices.models import Device

# Serializers
# define the API representation.

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        #fields = ('url', 'username', 'email', 'is_staff')




# ViewSets
# ViewSets define the view behavior.

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# Routers
# provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)


urlpatterns = patterns('',

    #include the above defined router in the url patterns
    url(r'^', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),
)
