from django.conf.urls import url
from views import DeviceCaptureUploadView

urlpatterns = [

    #Devices
    url(r'^api-device/device-captures/$', DeviceCaptureUploadView.as_view(), name='device-capture-upload'),

]