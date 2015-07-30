from django.conf.urls import url
from views import CaptureUploadView, CaptureListView


urlpatterns = [

    #Devices
    url(r'^api-device/captures/$', CaptureUploadView.as_view(), name='capture-upload'),
    url(r'^api/captures/$', CaptureListView.as_view(), name='capture-list-view'),

]