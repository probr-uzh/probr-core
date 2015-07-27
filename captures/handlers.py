import binascii
import json
import datetime
import dpkt
from captures.models import Capture
from utils.models import publishMessage
from probr import mongodb

__author__ = 'ale'



def generate_json(capture, packet, timestamp):
    tap = dpkt.radiotap.Radiotap(packet)
    t_len = binascii.hexlify(packet[2:3])    #t_len field indicates the entire length of the radiotap data, including the radiotap header.
    t_len = int(t_len,16)

    wlan = dpkt.ieee80211.IEEE80211(packet[t_len:])

    # todo: this can be extended to all necessary fields / data we need, done even on demand
    jsonPacket = {}
    jsonPacket['capture_uuid'] = capture.uuid

    if len(capture.tags.all()) > 0:
       jsonPacket['tags'] = list(capture.tags.names())

    jsonPacket['time'] = timestamp
    jsonPacket['signal_strength'] = -(256-tap.ant_sig.db)
    jsonPacket['ssid'] = wlan.ies[0].info
    jsonPacket['mac_address_src'] = binascii.hexlify(wlan.mgmt.src)
    jsonPacket['mac_address_dst'] = binascii.hexlify(wlan.mgmt.dst)

    return jsonPacket

class MongoDBHandler(object):
    def handle(self, capture):
        capture.pcap.open()
        pcapReader = dpkt.pcap.Reader(capture.pcap)

        for timestamp, packet in pcapReader:
            db = mongodb.db
            packets = db.packets
            jsonPacket = generate_json(capture, packet, timestamp)
            jsonPacket['inserted_at'] = datetime.datetime.utcnow()
            jsonPacket['longitude'] = capture.longitude
            jsonPacket['latitude'] = capture.latitude
            packets.insert_one(jsonPacket)


class WebsocketHandler(object):
    def handle(self, capture):
        capture.pcap.open()
        pcapReader = dpkt.pcap.Reader(capture.pcap)

        for timestamp, packet in pcapReader:
            jsonPacket = generate_json(capture, packet, timestamp)

            # broadcast to socket
            jsonPacket["object_type"] = "packet:update"
            publishMessage("socket", message=json.dumps(jsonPacket))