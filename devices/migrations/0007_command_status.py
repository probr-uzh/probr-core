# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0006_command'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'Not executed yet'), (1, b'Executed')]),
        ),
    ]
