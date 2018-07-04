#!/bin/sh

if [ $(whoami) != "root" ]; then
  sudo $0 $*
  exit
fi

apt install v4l2loopback-dkms libv4l-dev v4l-utils
