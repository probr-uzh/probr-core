# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0019_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(default=6, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
