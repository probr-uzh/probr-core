# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('devices', '0001_initial'),
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
                ('status', models.IntegerField(default=0, choices=[(0, b'Not executed yet'), (1, b'Executing'), (2, b'Executed')])),
            ],
            options={
                'abstract': False,
            },
        ),
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
            name='Device',
            fields=[
                ('uuid', utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID')),
                ('apikey', models.CharField(unique=True, max_length=64, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('type', models.CharField(default=b'UKW', max_length=3, choices=[(b'RPA', b'Raspberry Pi Model A'), (b'RPB', b'Raspberry Pi Model B'), (b'ODR', b'ODROID'), (b'DWR', b'DD-WRT Router'), (b'OWR', b'OpenWRT Router'), (b'UKW', b'Unknown')])),
                ('wifi_chip', models.CharField(default=b'', max_length=255, blank=True)),
                ('os', models.CharField(default=b'', max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('uuid', utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID')),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('ip', models.GenericIPAddressField(default=b'0.0.0.0')),
                ('cpu_load', models.FloatField(default=0)),
                ('total_memory', models.IntegerField(default=0)),
                ('used_memory', models.IntegerField(default=0)),
                ('total_disk', models.IntegerField(default=0)),
                ('used_disk', models.IntegerField(default=0)),
                ('device', models.ForeignKey(related_name='statuses', to='devices.Device')),
            ],
            options={
                'ordering': ['-creation_timestamp'],
                'verbose_name_plural': 'statuses',
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
        migrations.CreateModel(
            name='TaggedDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='devices.Device')),
                ('tag', models.ForeignKey(related_name='devices_taggeddevice_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='device',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='devices.TaggedDevice', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commandtemplate',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='devices.TaggedCommandTemplate', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='command',
            name='device',
            field=models.ForeignKey(related_name='commands', to='devices.Device'),
        ),
    ]
