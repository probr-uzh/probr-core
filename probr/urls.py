from django.conf.urls import patterns, include, url
from django.contrib import admin
from devices.views import DeviceListView, DeviceDetailsView, StatusListView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

    #list of all devices
    url(r'devices/$', DeviceListView.as_view(), name='device-list'),

    #details of a device by uuid
    url(r'devices/(?P<uuid>.+)/$', DeviceDetailsView.as_view(), name='device-details'),

    #list of all statuses
    url(r'statuses/$', StatusListView.as_view(), name='status-list'),

    #admin site
    url(r'^admin/', include(admin.site.urls)),
]

format_suffix_patterns(urlpatterns)
