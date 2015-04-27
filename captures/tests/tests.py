from django.test import TestCase
from django.core.files import File
from captures.tasks import *
import dpkt

class TaskTestCase(TestCase):

    def setUp(self):
        self.pcapfile = File(open('captures/tests/resources/proberequests_smallsample.pcap'))
        self.capture = Capture.objects.create(pcap=self.pcapfile)

    def test_unpack_pcap(self):
        pcapReader = dpkt.pcap.Reader(self.capture.pcap)

        for timestamp, packet in pcapReader:
            json = generate_json(packet)
            print(json)

    #def tearDown(self):
        #self.capture.pcap.delete()



