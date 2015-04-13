# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import uuid
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capture',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, verbose_name=b'ID', primary_key=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('pcap', models.FileField(upload_to=b'pcap')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
