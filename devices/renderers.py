__author__ = 'ale'
from django.utils.encoding import smart_unicode
from rest_framework import renderers


class PlainTextCommandRenderer(renderers.BaseRenderer):
    """
    Renders a single command object to a shell script
    """
    shebang = '#!/usr/bin/env sh'
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, dict) and data.has_key('execute'):
            output = "%s\n%s\n" % (self.shebang, data['execute'])
            return output
        else:
            return data

class PlainTextCommandsRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        responseListString = ""
        for command in data:
            responseListString += command['uuid']+"\n"
        return responseListString
