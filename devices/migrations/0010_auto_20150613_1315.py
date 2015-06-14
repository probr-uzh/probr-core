# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_auto_20150601_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['-creation_timestamp'], 'verbose_name_plural': 'statuses'},
        ),
    ]
