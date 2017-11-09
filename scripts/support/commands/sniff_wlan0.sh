sudo apt-get update
sudo apt-get install -y tcpdump
ifconfig wlan0 down
iwconfig wlan0 mode monitor
iwconfig wlan0 channel 6
ifconfig wlan0 up
mkdir -p captures
tcpdump -e -ni wlan0 -s 0 -w captures/capture-%s.pcap -G 5 type mgt subtype probe-req
