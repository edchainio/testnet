#!/usr/bin/env python3

import json
import os
import re
import socket
from os.path import expanduser

import requests


# FIXME 1   Parameter hard-coded to expedite testing.

# TODO 1    Reduce the redundancy across variables `a_header`, `c_header`, and `headers`.
# TODO 2    Port the functionality of the `curl` command to the `requests.post()` function.


def format_command(cluster_name, vm_count):
    endpoint = 'https://api.digitalocean.com/v2/droplets'
    payload = {}
    # pat_path = input('pat_path: ')                                                # FIXME 1
    pat_path = '{0}/.pat/.digitalocean-edchain'.format(expanduser('~')) # FIXME 1
    pa_token = open('{pat_path}'.format(pat_path=pat_path)).read().strip()
    a_header = 'Authorization: Bearer {pa_token}'.format(pa_token=pa_token) # TODO 1
    c_header = 'Content-Type: application/json'                             # TODO 1
    if vm_count < 1:
        print(' Error: You cannot spin-up less than one server.')
        format_command(cluster_name)
    elif vm_count < 2:
        payload['name'] = cluster_name
    else:
        payload['names'] = ['{cluster_name} {_}'                   \
                                .format(cluster_name=cluster_name, \
                                        _=_)                       \
                                .replace(' ', '-')                 \
                                for _ in range(vm_count)]
    payload['region'] = 'nyc1'
    payload['size']   = '4gb'
    payload['image']  = 'ubuntu-16-04-x64'
    headers = {}                                                             # TODO 1
    headers['Authorization'] = 'Bearer {pa_token}'.format(pa_token=pa_token) # TODO 1
    headers['Content-Type'] = 'application/json'                             # TODO 1
    keys = json.loads(requests.get('https://api.digitalocean.com/v2/account/keys', headers=headers).text)['ssh_keys']
    payload['ssh_keys'] = [str(key['id']) for key in keys if key['name']==socket.gethostname()]
    payload['private_networking'] = 'true'
    payload['monitoring'] = 'true'
    # payload['tags'] = input('payload[\'tags\']: ') # FIXME 1
    payload['tags'] = ['testnet']                    # FIXME 1
    endstate = 'curl -X POST "{endpoint}"            \
                -d \'{payload}\'                     \
                -H "{a_header}"                      \
                -H "{c_header}"'                     \
                .format(endpoint=endpoint,           \
                        payload=json.dumps(payload), \
                        a_header=a_header.strip(),   \
                        c_header=c_header) # TODO 2
    return re.sub(' +', ' ', endstate)     # TODO 2

def get_host(droplet_id, writeout_file):
    pa_token = open('{0}/.pat/.digitalocean-edchain'.format(expanduser('~'))).read().strip() # FIXME redundant
    writeout_file_i = writeout_file.split('.')[0]     \
                        + writeout_file.split('.')[1] \
                        + '-'                         \
                        + str(droplet_id)             \
                        + '.json'
    os.system('curl -X GET "https://api.digitalocean.com/v2/droplets/{droplet_id}" \
                -H "Content-Type: application/json"                                \
                -H "Authorization: Bearer {pa_token}" > {writeout_file_i}'.format(droplet_id=droplet_id, \
                                                                                pa_token=pa_token,       \
                                                                                writeout_file_i=writeout_file_i))
    payload = json.load(open(writeout_file_i))
    ip_address = payload['droplet']['networks']['v4'][0]['ip_address']
    return ip_address