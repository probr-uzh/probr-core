# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0003_auto_20150727_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Not executed yet'), (1, b'Executing'), (2, b'Executed'), (3, b'Aborted')]),
        ),
    ]
