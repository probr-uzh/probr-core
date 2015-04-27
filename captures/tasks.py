from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture
import json
import dpkt

@shared_task
def unpack_capture(captureUUID):
    capture = Capture.objects.get(pk=captureUUID)
    pcapReader = PcapReader(capture.pcap);

    for packet in pcapReader:
        json = generate_json(packet)
        #write_json(json)

def generate_json(packet):

    tap = dpkt.radiotap.Radiotap(packet)

    jsonPacket = {}
    jsonPacket['signal_strength'] = -(256-tap.ant_sig.db)

    return json.dumps(jsonPacket)

#def write_json(json):
