#!/usr/bin/env bash

# HACK

/sbin/ifconfig eth1 | grep Mask | awk '{print $2}'| cut -f2 -d: