#!/usr/bin/env bash

# Based on: http://wiki.openwrt.org/doc/howto/docker_openwrt_image
# BusyBox v1.19.4
# Requires ~5.5MB

import_image() {
  images=$(docker images)
  if [[ "$images" != *"openwrt-x86-generic-rootfs"* ]]; then
    docker import http://downloads.openwrt.org/attitude_adjustment/12.09/x86/generic/openwrt-x86-generic-rootfs.tar.gz openwrt-x86-generic-rootfs
  fi
}

import_image
docker run -it openwrt-x86-generic-rootfs /bin/ash
