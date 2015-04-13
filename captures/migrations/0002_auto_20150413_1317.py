# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('captures', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capture',
            name='location',
        ),
        migrations.AddField(
            model_name='capture',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='capture',
            name='longitude',
            field=models.FloatField(default=0),
        ),
    ]
