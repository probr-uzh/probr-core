from views import CommandTemplateListView, CommandTemplateDetailsView, DeviceListView, DeviceDetailsView,CommandList_Devices, CommandDetails_Devices, StatusList_Devices, \
    StatusList, CommandList, CommandDetails
from django.conf.urls import url


urlpatterns = [

    ### Endpoints accessed by frontend  ###

    #list of all devices
    url(r'^api/devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'^api/devices/(?P<uuid>[^/]+)/+$', DeviceDetailsView.as_view(), name='device-details'),

    #list of all commandtemplates
    url(r'^api/commandtemplates/$', CommandTemplateListView.as_view(), name='commandtemplate-list'),

    #details of a commandtempate by uuid
    url(r'^api/commandtemplates/(?P<pk>[^/]+)/+$', CommandTemplateDetailsView.as_view(), name='commandtemplate-details'),

    #list of all statuses that belong to device given by api-key
    url(r'^api/statuses/$', StatusList.as_view(), name='status-list'),

    #list of all commands that belong to device given by api-key
    url(r'^api/commands/$', CommandList.as_view(), name='command-list'),

    #details of a command given by api-key
    url(r'^api/commands/(?P<uuid>[^/]+)/+$', CommandDetails.as_view(), name='command-details'),



    ### Endpoints accessed by devices ###

    #list of all statuses that belong to device given by api-key
    url(r'^api-device/statuses/$', StatusList_Devices.as_view(), name='status-list-devices'),


    #list of all commands that belong to device given by api-key
    url(r'^api-device/commands/$', CommandList_Devices.as_view(), name='command-list-devices'),

    #details of a command given by api-key
    url(r'^api-device/commands/(?P<uuid>[^/]+)/+$', CommandDetails_Devices.as_view(), name='command-details-devices'),


]