# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('devices', '0003_auto_20150413_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='device',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='devices.TaggedDevice', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='taggeddevice',
            name='content_object',
            field=models.ForeignKey(to='devices.Device'),
        ),
        migrations.AddField(
            model_name='taggeddevice',
            name='tag',
            field=models.ForeignKey(related_name='devices_taggeddevice_items', to='taggit.Tag'),
        ),
    ]
