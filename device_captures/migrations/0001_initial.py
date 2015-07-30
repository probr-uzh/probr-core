# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('captures', '0004_auto_20150727_1522'),
        ('devices', '0003_auto_20150727_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceCapture',
            fields=[
                ('capture_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='captures.Capture')),
                ('device', models.ForeignKey(to='devices.Device')),
            ],
            options={
                'abstract': False,
            },
            bases=('captures.capture',),
        ),
    ]
