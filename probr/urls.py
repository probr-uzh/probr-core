from django.conf.urls import patterns, include, url
from django.contrib import admin
from devices.views import DeviceListView, DeviceDetailsView, StatusListView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    #Devices

    #list of all devices
    url(r'^api/devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'^api/devices/(?P<uuid>.+)/$', DeviceDetailsView.as_view(), name='device-details'),

    ###########################################

    #Statuses

    #list of all statuses
    url(r'^api/statuses/$', StatusListView.as_view(), name='status-list'),

    ###########################################

    #Captures

    url(r'^api/captures/$', include('captures.urls')),

    ###########################################
    #admin site
    url(r'^admin/', include(admin.site.urls)),
]

format_suffix_patterns(urlpatterns)
