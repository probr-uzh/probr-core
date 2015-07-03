# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0013_auto_20150703_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='api_key',
            new_name='apikey',
        ),
    ]
