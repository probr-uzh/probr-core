# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('devices', '0011_auto_20150615_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandTemplate',
            fields=[
                ('uuid', utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID')),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=255)),
                ('execute', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedCommandTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='devices.CommandTemplate')),
                ('tag', models.ForeignKey(related_name='devices_taggedcommandtemplate_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='commandtemplate',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='devices.TaggedCommandTemplate', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
