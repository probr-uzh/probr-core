# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20150720_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='device',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
