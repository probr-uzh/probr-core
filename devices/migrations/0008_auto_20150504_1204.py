# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0007_command_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
    ]
