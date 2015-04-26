# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('captures', '0002_auto_20150420_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedCapture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='capture',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='captures.TaggedCapture', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='taggedcapture',
            name='content_object',
            field=models.ForeignKey(to='captures.Capture'),
        ),
        migrations.AddField(
            model_name='taggedcapture',
            name='tag',
            field=models.ForeignKey(related_name='captures_taggedcapture_items', to='taggit.Tag'),
        ),
    ]
