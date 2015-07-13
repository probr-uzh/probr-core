# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0017_auto_20150706_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='device',
            name='created_with_session_key',
        ),
        migrations.RemoveField(
            model_name='device',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='device',
            name='modified_with_session_key',
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=audit_log.models.fields.CreatingUserField(related_name='+', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
