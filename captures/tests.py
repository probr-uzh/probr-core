from django.core.files import File
from django.test import TestCase

# Create your tests here.
from captures.models import Capture
import dpkt

class CaptureTestCase(TestCase):

    def setUp(self):
        self.pcapFile = File(open("testfiles/vm-2.pcap"))
        self.capture = Capture.objects.create(pcap=self.pcapFile)

    def test_unpacking(self):
        print self.capture.pcap
        counter=0
        ipcounter=0
        tcpcounter=0
        udpcounter=0

        pcapReader = dpkt.pcap.Reader(self.capture.pcap)
        for ts, pkt in pcapReader:
            print pcapReader.datalink()
            counter+=1
            eth=dpkt.ethernet.Ethernet(pkt)
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
               continue

            ip=eth.data
            ipcounter+=1

            if ip.p==dpkt.ip.IP_PROTO_TCP:
               tcpcounter+=1

            if ip.p==dpkt.ip.IP_PROTO_UDP:
               udpcounter+=1

        print "Total number of packets in the pcap file: ", counter
        print "Total number of ip packets: ", ipcounter
        print "Total number of tcp packets: ", tcpcounter
        print "Total number of udp packets: ", udpcounter