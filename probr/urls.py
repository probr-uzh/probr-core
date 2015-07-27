from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

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

format_suffix_patterns(urlpatterns)
