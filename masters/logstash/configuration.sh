#!/usr/bin/env bash

mkdir -p /etc/pki/tls/certs

mkdir -p /etc/pki/tls/private

sed -i '/\[ v3_ca \]/a subjectAltName = IP: <private_ip_address>' /etc/ssl/openssl.cnf

cd /etc/pki/tls && openssl req -config /etc/ssl/openssl.cnf -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt && cd

sh -c 'echo "input {" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "  beats {" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "    port => 5044" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "    ssl => true" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "    ssl_certificate => \"/etc/pki/tls/certs/logstash-forwarder.crt\"" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "    ssl_key => \"/etc/pki/tls/private/logstash-forwarder.key\"" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "  }" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "}" >> /etc/logstash/conf.d/02-beats-input.conf'

sh -c 'echo "filter {" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "  if [type] == \"syslog\" {" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "    grok {" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "      match => { \"message\" => \"%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:[%{POSINT:syslog_pid}])?: %{GREEDYDATA:syslog_message}\" }" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "      add_field => [ \"received_at\", \"%{@timestamp}\" ]" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "      add_field => [ \"received_from\", \"%{host}\" ]" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "    }" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "    syslog_pri { }" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "    date {" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "      match => [ \"syslog_timestamp\", \"MMM  d HH:mm:ss\", \"MMM dd HH:mm:ss\" ]" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "    }" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "  }" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "}" >> /etc/logstash/conf.d/10-syslog-filter.conf'

sh -c 'echo "output {" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "  elasticsearch {" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "    hosts => [\"localhost:9200\"]" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "    sniffing => true" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "    manage_template => false" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "    index => \"%{[@metadata][beat]}-%{+YYYY.MM.dd}\"" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "    document_type => \"%{[@metadata][type]}\"" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "  }" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

sh -c 'echo "}" >> /etc/logstash/conf.d/30-elasticsearch-output.conf'

service logstash configtest

service logstash restart

update-rc.d logstash defaults 96 9

mkdir -p /opt/logstash/patterns

chown logstash: /opt/logstash/patterns

sh -c 'echo "NGUSERNAME [a-zA-Z\\\.\\@\\-\\+_%]+" >> /opt/logstash/patterns/nginx'

sh -c 'echo "NGUSER %{NGUSERNAME}" >> /opt/logstash/patterns/nginx'

sh -c 'echo "NGINXACCESS %{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response} (?:%{NUMBER:bytes}|-) (?:\"(?:%{URI:referrer}|-)\"|%{QS:referrer}) %{QS:agent}" >> /opt/logstash/patterns/nginx'

chown logstash: /opt/logstash/patterns/nginx

sh -c 'echo "filter {" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "  if [type] == \"nginx-access\" {" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "    grok {" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "      match => { \"message\" => \"%{NGINXACCESS}\" }" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "    }" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "  }" >> /etc/logstash/conf.d/11-nginx-filter.conf'

sh -c 'echo "}" >> /etc/logstash/conf.d/11-nginx-filter.conf'