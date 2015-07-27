from django.test import TestCase
from django.core.files import File
import dpkt

from handlers.handlers import generate_json, MongoDBHandler
from captures.tasks import *
from probr import mongodb


class CaptureTaskTestCase(TestCase):
    def setUp(self):
        self.pcapfile = File(open('captures/tests/resources/proberequests_smallsample.pcap', 'rb'))

        self.capture = Capture.objects.create(file=self.pcapfile)
        self.capture.tags.add("test", "test2")

    def test_unpack_pcap(self):
        pcapReader = dpkt.pcap.Reader(self.capture.file)

        packetList = []

        for timestamp, packet in pcapReader:
            jsonObj = generate_json(self.capture, packet, timestamp)
            packetList.append(jsonObj)

        self.assertEqual(packetList[0]["capture_uuid"], self.capture.uuid)
        self.assertEqual(packetList[0]["mac_address_src"], "cc08e06156a1")
        self.assertEqual(packetList[0]["ssid"], "")
        self.assertEqual(packetList[0]["signal_strength"], -83)
        self.assertEqual(packetList[0]["mac_address_dst"], "ffffffffffff")

        self.assertEqual(packetList[1]["capture_uuid"], self.capture.uuid)
        self.assertEqual(packetList[1]["mac_address_src"], "0024d6799d8e")
        self.assertEqual(packetList[1]["ssid"], "public")
        self.assertEqual(packetList[1]["signal_strength"], -62)
        self.assertEqual(packetList[1]["mac_address_dst"], "ffffffffffff")

        self.assertEqual(packetList[2]["capture_uuid"], self.capture.uuid)
        self.assertEqual(packetList[2]["mac_address_src"], "e8150e460364")
        self.assertEqual(packetList[2]["ssid"], "eduroam")
        self.assertEqual(packetList[2]["signal_strength"], -49)
        self.assertEqual(packetList[1]["mac_address_dst"], "ffffffffffff")

    def test_insert_mongo(self):

        mongoHandler = MongoDBHandler()
        mongoHandler.handle(self.capture)


        self.capture.file.open()

        pcapReader = dpkt.pcap.Reader(self.capture.file)

        packetList = []
        dbList = []

        db = mongodb.db
        packets = db.packets


        for timestamp, packet in pcapReader:
            jsonObj = generate_json(self.capture, packet, timestamp)
            packetList.append(jsonObj)

        for packet in packets.find():
            dbList.append(packet)

        # check whether inserted packets exist & correspond to the inserted ones
        self.assertEqual(len(packetList), len(dbList))
        self.assertEqual(packetList[0]["mac_address_src"], dbList[0]["mac_address_src"])
        self.assertEqual(packetList[1]["mac_address_src"], dbList[1]["mac_address_src"])
        self.assertEqual(packetList[2]["mac_address_src"], dbList[2]["mac_address_src"])

        self.assertEqual(packetList[0]["tags"], dbList[0]["tags"])

    def tearDown(self):

        #self.capture.file.delete()

        db = mongodb.db
        packets = db.packets

        # clean up db after tests
        packets.remove({})



