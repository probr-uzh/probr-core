from django.conf.urls import url
from views import DeviceListView, DeviceDetailsView,CommandListView, CommandDetailsView, StatusList

urlpatterns = [
    #Devices

    #list of all devices
    url(r'^api/devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'^api/devices/(?P<uuid>[^/]+)/+$', DeviceDetailsView.as_view(), name='device-details'),
    ###########################################

    #Statuses

    #list of all statuses
    url(r'^api/statuses/$', StatusList.as_view(), name='status-list'),

    ###########################################

    #Commands

    #list of all commands
    url(r'^api/commands/$', CommandListView.as_view(), name='command-list'),

    #details of a command by uuid
    url(r'^api/commands/(?P<uuid>[^/]+)/+$', CommandDetailsView.as_view(), name='command-details'),
]