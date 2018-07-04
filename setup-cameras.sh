#!/bin/sh

if [ $(whoami) != "root" ]; then
  sudo $0 $*
  exit
fi

rmmod v4l2loopback 2>/dev/null
modprobe v4l2loopback devices=${1:-1} exclusive_caps=1 card_label='VCamera'
v4l2-ctl --list-devices
