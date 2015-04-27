from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture
from scapy.all import *
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
    jsonPacket['timestamp'] = packet.timestamp * 1000 # mongo expects 64-bit signed integer representation
    jsonPacket['signal_strength'] = -(256-tap.ant_sig.db)

    return json.dumps(jsonPacket)

#def write_json(json):
