from django.contrib import admin
import time
from models import Device, Status, Command

# Register Device Model to be modifiable by the admin UI

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_timestamp')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    def creation_time_detailed(self, obj):
        return obj.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    creation_time_detailed.admin_order_field = 'creation_timestamp'
    creation_time_detailed.short_description = "Posted at"

    list_display = ('creation_time_detailed', 'device', 'ip')

    ordering = ['-creation_timestamp']

admin.site.register(Command)


