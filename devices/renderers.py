__author__ = 'ale'
from django.utils.encoding import smart_unicode
from rest_framework import renderers

class PlainTextCommandRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, dict) and data.has_key('execute'):
            return data['execute']
        else:
            return data

class PlainTextCommandsRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        responseListString = ""
        for result in data['results']:
            responseListString += result['uuid']+"\n"
        return responseListString