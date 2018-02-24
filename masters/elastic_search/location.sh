#!/usr/bin/env bash

add-apt-repository -y ppa:webupd8team/java

echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections

echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections

wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | apt-key add -

echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list

curl -L -O https://download.elastic.co/beats/dashboards/beats-dashboards-1.1.0.zip

curl -O https://gist.githubusercontent.com/thisismitch/3429023e8438cc25b86c/raw/d8c479e2a1adcea8b1fe86570e42abab0f10f364/filebeat-index-template.json
