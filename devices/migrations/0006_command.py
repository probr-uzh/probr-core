# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0005_auto_20150420_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('uuid', utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID')),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('execute', models.TextField()),
                ('result', models.TextField(default=b'', blank=True)),
                ('device', models.ForeignKey(related_name='commands', to='devices.Device')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
