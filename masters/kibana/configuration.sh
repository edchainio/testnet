#!/usr/bin/env bash

sed -i -e '/^# server.host/s/^.*$/server.host: "localhost"/' /opt/kibana/config/kibana.yml

update-rc.d kibana defaults 96 9

service kibana start
