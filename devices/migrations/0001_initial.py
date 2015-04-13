# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('type', models.CharField(default=b'UKW', max_length=2, choices=[(b'RPA', b'Raspberry Pii Model A'), (b'RPB', b'Raspberry Pii Model B'), (b'DWR', b'DD-WRT Router'), (b'OWR', b'OpenWRT Router'), (b'UKW', b'Unknown')])),
                ('wifi_chip', models.CharField(default=b'', max_length=255, blank=True)),
                ('os', models.CharField(default=b'', max_length=255, blank=True)),
                ('description', models.TextField(default=b'', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, verbose_name=b'ID', primary_key=True)),
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
                'abstract': False,
            },
        ),
    ]
