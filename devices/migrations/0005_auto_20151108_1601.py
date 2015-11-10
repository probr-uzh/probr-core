# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def initCommandTemplates(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    CommandTemplate = apps.get_model("devices", "CommandTemplate")
    CommandTemplate.objects.create(name="sniff wlan1",
                                   execute="sudo apt-get update\nsudo apt-get install -y tcpdump\nifconfig wlan1 down\niwconfig wlan1 mode monitor\niwconfig wlan1 channel 6\nifconfig wlan1 up\nmkdir -p captures\ntcpdump -e -ni wlan1 -s 0 -w captures/capture-%s.pcap -G 5 type mgt subtype probe-req\n")

    CommandTemplate.objects.create(name="sniff wlan0",
                                   execute="sudo apt-get update\nsudo apt-get install -y tcpdump\nifconfig wlan0 down\niwconfig wlan0 mode monitor\niwconfig wlan0 channel 6\nifconfig wlan0 up\nmkdir -p captures\ntcpdump -e -ni wlan0 -s 0 -w captures/capture-%s.pcap -G 5 type mgt subtype probe-req\n")

    CommandTemplate.objects.create(name="watch upload",
                                   execute="apt-get install -y inotify-tools\n\n# Upload existing and future pcaps\n\n# Make sure output folder exists\nmkdir -p captures\n\n# Upload Existing\nfor file in captures/*.pcap\ndo\n    post_file '/api-device/device-captures/' \"$file\" && rm \"$file\" \ndone\n\n# Upload future pcaps (blocking)\ninotifywait -m captures/ -e close_write -e move |\n    while read path action file; do\n        post_capture \"$file\" && rm \"captures/$file\" \n    done\n")


class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0004_auto_20150810_1838'),
    ]

    operations = [
        migrations.RunPython(initCommandTemplates),
    ]
