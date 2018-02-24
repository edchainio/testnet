#!/usr/bin/env bash

systemctl start firewalld

firewall-cmd --add-port <ssh_port>/tcp --permanent

firewall-cmd --add-port 9200/tcp --permanent

firewall-cmd --add-port 5601/tcp --permanent

firewall-cmd --add-port 5044/tcp --permanent

firewall-cmd --permanent --zone=public --add-service=http

firewall-cmd --permanent --zone=public --add-service=https

firewall-cmd --reload

systemctl enable firewalld

systemctl restart fail2ban