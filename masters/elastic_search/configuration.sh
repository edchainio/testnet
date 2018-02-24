#!/usr/bin/env bash

sed -i -e '/^# network.host/s/^.*$/network.host: localhost/' /etc/elasticsearch/elasticsearch.yml

service elasticsearch restart

update-rc.d elasticsearch defaults 95 10

unzip beats-dashboards-*.zip

cd beats-dashboards-* && ./load.sh && cd