import binascii
import json
import datetime
import dpkt
from bson import json_util
from captures.models import Capture
from utils.models import publishMessage
from probr import mongodb
from probr import socketioemitter
from probr.base_settings import WS4REDIS_CONNECTION

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

    jsonPacket['time'] = datetime.datetime.utcfromtimestamp(timestamp)
    jsonPacket['signal_strength'] = -(256-tap.ant_sig.db)
    jsonPacket['ssid'] = wlan.ies[0].info
    jsonPacket['mac_address_src'] = binascii.hexlify(wlan.mgmt.src)
    jsonPacket['mac_address_dst'] = binascii.hexlify(wlan.mgmt.dst)
    jsonPacket['inserted_at'] = datetime.datetime.utcnow()
    jsonPacket['location'] = { 'type': 'Point', 'coordinates': [capture.longitude, capture.latitude] }

    return jsonPacket

class MongoDBHandler(object):
    def handle(self, capture):
        if capture.file.size > 0:
            capture.file.open()
            pcapReader = dpkt.pcap.Reader(capture.file)

            for timestamp, packet in pcapReader:
                db = mongodb.db
                packets = db.packets
                jsonPacket = generate_json(capture, packet, timestamp)

                packets.insert_one(jsonPacket)

class WebsocketHandler(object):
    def handle(self, capture):
        if capture.file.size > 0:
            capture.file.open()
            pcapReader = dpkt.pcap.Reader(capture.file)

            for timestamp, packet in pcapReader:
                jsonPacket = generate_json(capture, packet, timestamp)

                # broadcast to socket
                jsonPacket["object_type"] = "packet:update"
                publishMessage("socket", message=json.dumps(jsonPacket, default=json_util.default))

class SocketIOHandler(object):
    def handle(self, capture):
        if capture.file.size > 0:
            capture.file.open()
            pcapReader = dpkt.pcap.Reader(capture.file)

            for timestamp, packet in pcapReader:
                jsonPacket = generate_json(capture, packet, timestamp)

                # broadcast to socket
                socketioemitter.io.Emit("packet:create", json.dumps(jsonPacket, default=json_util.default))
