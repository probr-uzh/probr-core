# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import audit_log.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0015_auto_20150706_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=audit_log.models.fields.CreatingUserField(editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
