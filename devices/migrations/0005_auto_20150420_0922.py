# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_auto_20150414_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='uuid',
            field=utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID'),
        ),
        migrations.AlterField(
            model_name='status',
            name='uuid',
            field=utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID'),
        ),
    ]
