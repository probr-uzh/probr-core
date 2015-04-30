from django.conf.urls import patterns, url
from views import CaptureUploadView

urlpatterns = patterns('captures.views',
    url('', CaptureUploadView.as_view()),
)