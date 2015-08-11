#!/bin/bash
ssid=CSG
key=csg112358


if [ "$(id -u)" != "0" ]; then
    echo "Run with sudo."
    exit 1
fi

diskutil list
read -p "/dev/disk1 will be formatted. Are you sure? [y/n]: " -n 1 -r
echo 
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Enter hostname: "
    read hostname

    echo "Unmounting..."
    diskutil umountDisk /dev/disk1s2

    echo "Flashing SD Card (Takes about 6 min)"
    sleep 5
    sudo dd if=ubuntu-14.04.2lts-lubuntu-odroid-c1-20150401.img of=/dev/rdisk1 bs=1m

    sleep 1
    echo "Unmounting..."
    diskutil umountDisk /dev/disk1s1
    diskutil umountDisk /dev/disk1s2

    say "Finished"
    echo "Please eject and re-enter SD card and press enter"
    read something
    sleep 1

    echo "Adding wlan config..."
    echo -e "\n\nauto eth0\niface eth0 inet dhcp\n\nauto wlan1\niface wlan1 inet dhcp\n\twpa-ssid $ssid\n\twpa-psk $key" >> /Volumes/trusty/etc/network/interfaces
    sleep 1

    echo "Setting up hostname..."
    echo $hostname > /Volumes/trusty/etc/hostname 
    sed -i ".bak" "s/odroid/$hostname/g" /Volumes/trusty/etc/hosts
    sleep 1

    echo "Unmounting..."
    diskutil umountDisk /dev/disk1s1
    diskutil umountDisk /dev/disk1s2

    echo "Done. Insert next SD Card."
fi
