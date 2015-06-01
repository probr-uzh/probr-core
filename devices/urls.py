from django.conf.urls import patterns, url
from views import DeviceListView, DeviceDetailsView,\
    StatusListView, CommandListView, CommandDetailsView

urlpatterns = [
    #Devices

    #list of all devices
    url(r'^api/devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'^api/devices/(?P<uuid>[^/]+)/+$', DeviceDetailsView.as_view(), name='device-details'),
    ###########################################

    #Statuses

    #list of all statuses
    url(r'^api/statuses/$', StatusListView.as_view(), name='status-list'),

    ###########################################

    #Commands

    #list of all commands
    url(r'^api/commands/$', CommandListView.as_view(), name='command-list'),

    #details of a command by uuid
    url(r'^api/commands/(?P<uuid>[^/]+)/+$', CommandDetailsView.as_view(), name='command-details'),
]