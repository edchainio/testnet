#!/usr/bin/env bash

# HACK Set timezone of every node in the network

timedatectl set-timezone America/New_York

###

fallocate -l 3G /swapfile

chmod 600 /swapfile

mkswap /swapfile

sh -c "echo '/swapfile none swap sw 0 0' >> /etc/fstab"

sysctl vm.swappiness=10

sh -c "echo 'vm.swappiness=10' >> /etc/sysctl.conf"

sysctl vm.vfs_cache_pressure=30

sh -c 'echo "vm.vfs_cache_pressure=30" >> /etc/sysctl.conf'

###

adduser --disabled-password --gecos "" <username>

usermod -aG sudo <username>

mkdir -p /etc/ssh/<username>

###

cat /tmp/.chpasswd-credentials | chpasswd

rm /tmp/.chpasswd-credentials