from django.test import TestCase
from captures.tasks import *
from os import path
import dpkt

class TaskTestCase(TestCase):

    def setUp(self):
        self.capture = Capture.objects.create()

    def test_unpack_pcap(self):
        file = open(path.abspath('captures/tests/resources/proberequests_smallsample.pcap'))
        pcapReader = dpkt.pcap.Reader(file)

        for timestamp, packet in pcapReader:
            json = generate_json(packet)
            print(json)

    #def tearDown(self):
        #self.capture.pcap.delete()



