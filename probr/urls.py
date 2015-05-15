from django.conf.urls import patterns, include, url
from django.contrib import admin
from devices.views import DeviceListView, DeviceDetailsView, StatusListView, CommandListView, DeviceStatusesView
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

urlpatterns = [

    #Devices

    #list of all devices
    url(r'^api/devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'^api/devices/(?P<uuid>[^/]+)/+$', DeviceDetailsView.as_view(), name='device-details'),

    #statuses associated with a certain device
    url(r'^api/devices/(?P<uuid>[^/]+)/statuses/+$', DeviceStatusesView.as_view(), name='device-statuses'),

    ###########################################

    #Statuses

    #list of all statuses
    url(r'^api/statuses/$', StatusListView.as_view(), name='status-list'),

    ###########################################

    #Captures

    url(r'^api/captures/$', include('captures.urls')),

    ###########################################
    #details of a device by uuid
    url(r'^api/commands/(?P<device>.+)/$', CommandListView.as_view(), name='command-list'),

    #admin site
    url(r'^admin/', include(admin.site.urls)),

    #angular frontend
    url(r'^.*', TemplateView.as_view(template_name='index.html')),
]

format_suffix_patterns(urlpatterns)
