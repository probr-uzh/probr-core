from django.contrib import admin
from models import Device, Status, Command

# Register Device Model to be modifiable by the admin UI

admin.site.register(Device)
admin.site.register(Command)
admin.site.register(Status)

