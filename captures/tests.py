import binascii
from django.core.files import File
from django.test import TestCase

# Create your tests here.
from captures.models import Capture
import dpkt

class CaptureTestCase(TestCase):

    def setUp(self):
        self.pcapFile = File(open("testfiles/vm-5.pcap"))
        self.capture = Capture.objects.create(pcap=self.pcapFile)

    def test_unpacking(self):
        print self.capture.pcap
        counter=0
        ipcounter=0
        tcpcounter=0
        udpcounter=0

        pcapReader = dpkt.pcap.Reader(self.capture.pcap)
        for ts, pkt in pcapReader:
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


    def test_wireless(self):
        pc = dpkt.pcap.Reader(self.capture.pcap)
        dl=pc.datalink()
        print dl
        if pc.datalink() == 127: #Check if RadioTap
                for timestamp, rawdata in pc:
                        print timestamp
                        tap = dpkt.radiotap.Radiotap(rawdata)
                        signal_ssi=-(256-tap.ant_sig.db)        #Calculate signal strength
                        t_len=binascii.hexlify(rawdata[2:3])    #t_len field indicates the entire length of the radiotap data, including the radiotap header.
                        t_len=int(t_len,16)                     #Convert to decimal
                        wlan = dpkt.ieee80211.IEEE80211(rawdata[t_len:])
                        if wlan.type == 0 and wlan.subtype == 4: # Indicates a probe request
                            ssid = wlan.ies[0].info
                            mac=binascii.hexlify(wlan.mgmt.src)
                            print "%s, %s (%d dBm)"%(mac,ssid,signal_ssi)