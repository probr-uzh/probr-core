from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings


urlpatterns = [
    url(r'', include('devices.urls')),
    url(r'', include('captures.urls')),
    url(r'', include('device_captures.urls')),
    url(r'', include('accounts.urls')),

    # admin site
    url(r'^admin/', include(admin.site.urls)),

    # angular frontend
    url(r'^$', RedirectView.as_view(url='/web/', permanent=True)),
    url(r'^web/*', TemplateView.as_view(template_name='index.html')),

    # JSON Web Token authentication
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
]

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,}),
)

format_suffix_patterns(urlpatterns)
