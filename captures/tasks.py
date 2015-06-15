from __future__ import absolute_import

from celery import shared_task
from captures.models import Capture
import dpkt
import binascii
import datetime
from utils.models import publishMessage
import json
from probr import mongodb

@shared_task
def unpack_capture(captureUUID):
    capture = Capture.objects.get(pk=captureUUID)
    pcapReader = dpkt.pcap.Reader(capture.pcap)

    for timestamp, packet in pcapReader:
        jsonPacket = generate_json(packet, timestamp)
        write_to_mongo(jsonPacket)

        # broadcast to socket
        jsonPacket["object_type"] = "packet:update"
        publishMessage("socket", message=json.dumps(jsonPacket))

def generate_json(packet, timestamp):

    tap = dpkt.radiotap.Radiotap(packet)

    t_len = binascii.hexlify(packet[2:3])    #t_len field indicates the entire length of the radiotap data, including the radiotap header.
    t_len = int(t_len,16)

    wlan = dpkt.ieee80211.IEEE80211(packet[t_len:])

    # todo: this can be extended to all necessary fields / data we need, done even on demand
    jsonPacket = {}
    jsonPacket['time'] = timestamp
    jsonPacket['signal_strength'] = -(256-tap.ant_sig.db)
    jsonPacket['ssid'] = wlan.ies[0].info
    jsonPacket['mac_address_src'] = binascii.hexlify(wlan.mgmt.src)
    jsonPacket['mac_address_dst'] = binascii.hexlify(wlan.mgmt.dst)

    return jsonPacket

def write_to_mongo(jsonPacket):
    db = mongodb.db
    packets = db.packets

    jsonPacket['inserted_at'] = datetime.datetime.utcnow()
    packets.insert_one(jsonPacket)





