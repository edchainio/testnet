#!/usr/bin/env python3

import json
import os
import sys
import time

import view
from utilities import replicate, edit
from wrappers import digital_ocean as do


# FIXME 1   Parameter hard-coded to expedite testing.

# HACK 1    Poll endpoints instead of waiting for IP address assignations.

# TODO 1    Port the build scripts to AWS.
# TODO 2    Write logic to handle unacceptable user input.
# TODO 3    Write control flow to spin-up peripheral node.


def provision(hostname, ssh_port, email, username, password, k):
    timestamp = time.time()
    res = 'logs/network-{0}.json'.format(timestamp)
    aws_lightsail = ['awsl', 'aws lightsail']                                  # TODO 1
    digital_ocean = ['do', 'digital ocean']
    iaas_platforms = aws_lightsail + digital_ocean
    # user_input = input('user_input: ')                                       # FIXME 1
    user_input = 'digital ocean'                                               # FIXME 1
    if user_input in iaas_platforms:
        if user_input in aws_lightsail:                                        # TODO 1
            pass                                                               # TODO 1
        elif user_input in digital_ocean:
            req = do.format_command(hostname, k)
            os.system('{0} > {1}'.format(req, res))
        time.sleep(60)                                                         # HACK 1
        return harden(hostname, ssh_port, email, username, password, res)
    else:
        pass                                                                   # TODO 2

def harden(hostname, ssh_port, email, username, password, res):
    arr = json.load(open(res))
    payloads = arr['droplets'] if 'droplets' in arr else [arr['droplet']]
    ip_addresses = [do.get_host(payload['id'], res) for payload in payloads]
    count = 0
    for ip_address in ip_addresses:
        replicate(count, hostname, 'docker', 'location')
        replicate(count, hostname, 'docker', 'installation')
        replicate(count, hostname, 'docker', 'configuration')

        replicate(count, hostname, 'elastic_search', 'location')
        replicate(count, hostname, 'elastic_search', 'installation')
        replicate(count, hostname, 'elastic_search', 'configuration')

        replicate(count, hostname, 'fail2ban', 'installation')
        replicate(count, hostname, 'fail2ban', 'configuration')

        # replicate(count, hostname, 'filebeat', 'location')                   # TODO 3
        # replicate(count, hostname, 'filebeat', 'installation')               # TODO 3
        # replicate(count, hostname, 'filebeat', 'configuration')              # TODO 3

        replicate(count, hostname, 'firewalld', 'installation')
        replicate(count, hostname, 'firewalld', 'configuration')

        replicate(count, hostname, 'kibana', 'location')
        replicate(count, hostname, 'kibana', 'installation')
        replicate(count, hostname, 'kibana', 'configuration')

        replicate(count, hostname, 'logstash', 'location')
        replicate(count, hostname, 'logstash', 'installation')
        replicate(count, hostname, 'logstash', 'configuration')

        replicate(count, hostname, 'nano', 'configuration')

        replicate(count, hostname, 'nginx', 'location')
        replicate(count, hostname, 'nginx', 'installation')
        replicate(count, hostname, 'nginx', 'configuration')

        replicate(count, hostname, 'ntp', 'installation')

        replicate(count, hostname, 'openssh', 'configuration')

        replicate(count, hostname, 'systemd', 'location')
        replicate(count, hostname, 'systemd', 'configuration')

        # replicate(count, hostname, 'topbeat', 'location')                    # TODO 3
        # replicate(count, hostname, 'topbeat', 'installation')                # TODO 3
        # replicate(count, hostname, 'topbeat', 'configuration')               # TODO 3

        edit(count, hostname, 'docker', 'configuration', username)
        edit(count, hostname, 'nano', 'configuration', username)
        edit(count, hostname, 'nginx', 'configuration', username)
        edit(count, hostname, 'openssh', 'configuration', username)
        edit(count, hostname, 'systemd', 'configuration', username)

        edit(count, hostname, 'fail2ban', 'configuration', hostname)

        edit(count, hostname, 'fail2ban', 'configuration', email)

        edit(count, hostname, 'firewalld', 'configuration', ssh_port)
        edit(count, hostname, 'openssh', 'configuration', ssh_port)

        edit(count, hostname, 'nginx', 'configuration', ip_address)

        edit(count, hostname, 'logstash', 'configuration', private_ip_address)

        # HACK
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < utilities/get-private-ip-address.sh > nodes/.private-ip-address-{1}-{0}'.format(count, hostname, ip_address))
        private_ip_address = open('nodes/.private-ip-address-{0}-{1}'.format(count, hostname), 'r').read().strip()
        edit(count, hostname, 'logstash', 'configuration', private_ip_address)

        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/docker/location-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/elastic_search/location-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/kibana/location-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/logstash/location-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/nginx/location-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/systemd/location-{1}-{0}.sh'.format(count, hostname, ip_address))

        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/docker/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/elastic_search/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/fail2ban/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/firewalld/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/kibana/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/logstash/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/nginx/installation-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/ntp/installation-{1}-{0}.sh'.format(count, hostname, ip_address))

        os.system('scp {0}/.ssh/id_rsa.pub root@{1}:/etc/ssh/{2}/authorized_keys'.format(expanduser('~'), ip_address, username))

        os.system('sh -c \'echo "{0}" > .htpasswd-credentials\''.format(password))
        os.system('sh -c \'echo "{1}:{0}" > .chpasswd-credentials\''.format(password, username))
        os.system('scp .htpasswd-credentials root@{0}:/home/{1}/'.format(ip_address, username))
        os.system('scp .chpasswd-credentials root@{0}:/home/{1}/'.format(ip_address, username))
        os.system('rm .htpasswd-credentials')
        os.system('rm .chpasswd-credentials')

        os.system('scp root@{0}:/etc/pki/tls/certs/logstash-forwarder.crt .'.format(ip_address)) # TODO Find a place to store the certificate

        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/docker/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/elastic_search/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/fail2ban/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/firewalld/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/kibana/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/logstash/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/nano/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/nginx/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/openssh/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))
        os.system('ssh -o "StrictHostKeyChecking no" root@{2} \'bash -s\' < procedures/systemd/configuration-{1}-{0}.sh'.format(count, hostname, ip_address))

        count += 1

    return ip_addresses


if __name__ == '__main__':
    (hostname, ssh_port, email, username, password, k) = view.main_menu()
    print(provision(hostname, ssh_port, email, username, password, k))
