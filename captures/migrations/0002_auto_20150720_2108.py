# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('captures', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capture',
            fields=[
                ('uuid', utils.models.UUIDField(primary_key=True, serialize=False, editable=False, max_length=64, blank=True, verbose_name=b'ID')),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, db_index=True)),
                ('pcap', models.FileField(upload_to=b'pcap')),
                ('longitude', models.FloatField(default=0)),
                ('latitude', models.FloatField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedCapture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='captures.Capture')),
                ('tag', models.ForeignKey(related_name='captures_taggedcapture_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='capture',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='captures.TaggedCapture', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
