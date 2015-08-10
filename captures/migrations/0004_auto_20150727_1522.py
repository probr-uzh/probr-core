# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('captures', '0003_auto_20150727_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capture',
            name='file',
            field=models.FileField(upload_to=b'captures'),
        ),
    ]
