# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20150413_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='type',
            field=models.CharField(default=b'UKW', max_length=3, choices=[(b'RPA', b'Raspberry Pi Model A'), (b'RPB', b'Raspberry Pi Model B'), (b'DWR', b'DD-WRT Router'), (b'OWR', b'OpenWRT Router'), (b'UKW', b'Unknown')]),
        ),
    ]
