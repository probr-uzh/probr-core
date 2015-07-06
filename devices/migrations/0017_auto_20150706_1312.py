# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0016_auto_20150706_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='user',
        ),
        migrations.AddField(
            model_name='device',
            name='created_by',
            field=audit_log.models.fields.CreatingUserField(related_name='created_devices_device_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='device',
            name='created_with_session_key',
            field=audit_log.models.fields.CreatingSessionKeyField(max_length=40, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='device',
            name='modified_by',
            field=audit_log.models.fields.LastUserField(related_name='modified_devices_device_set', editable=False, to=settings.AUTH_USER_MODEL, null=True, verbose_name='modified by'),
        ),
        migrations.AddField(
            model_name='device',
            name='modified_with_session_key',
            field=audit_log.models.fields.LastSessionKeyField(max_length=40, null=True, editable=False),
        ),
    ]
