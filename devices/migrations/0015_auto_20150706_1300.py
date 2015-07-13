# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import audit_log.models.fields
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0014_auto_20150703_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='user',
            field=audit_log.models.fields.CreatingUserField(related_name='+', editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='uuid',
            field=utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID'),
        ),
        migrations.AlterField(
            model_name='device',
            name='apikey',
            field=models.CharField(unique=True, max_length=64, editable=False),
        ),
    ]
