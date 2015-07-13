from django.contrib import admin
import time
from models import Device, Status, Command, CommandTemplate

# Register Device Model to be modifiable by the admin UI

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'creation_timestamp','apikey')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):

    def creation_time_detailed(self, obj):
        return obj.creation_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    creation_time_detailed.admin_order_field = 'creation_timestamp'
    creation_time_detailed.short_description = "Posted at"

    list_display = ('creation_time_detailed', 'device', 'ip')
    ordering = ['-creation_timestamp']

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):

    def modification_time_detailed(self, obj):
        return obj.modification_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    modification_time_detailed.admin_order_field = 'modification_timestamp'
    modification_time_detailed.short_description = "Last modified at"

    list_display = ('modification_time_detailed', 'execute', 'device', 'status')
    ordering = ['-modification_timestamp']

@admin.register(CommandTemplate)
class CommandTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'execute',)
