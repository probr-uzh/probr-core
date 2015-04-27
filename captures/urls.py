from django.conf.urls import patterns, url

urlpatterns = patterns('captures.views',
    url('', 'upload_form'),
)