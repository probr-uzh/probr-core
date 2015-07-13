# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0011_auto_20150615_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='uuid',
        ),
        migrations.AddField(
            model_name='device',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
