#!/usr/bin/env python3

import os
import time


def render_header():
    os.system('clear')
    print(' _____________________________________________________________________________')
    print(' . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .')
    print(' . .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . .')
    print(' .   .   .   .   .   .   .   .  .  .  . .  .  .  .   .   .   .   .   .   .   .')
    print(' .    .     .     .     .      .  ___________  .      .     .     .     .    .')
    print(' .     .       .       .   .  .  /           \  .  .   .       .       .     .')
    print(' . .     .  .     .  .       .  /             \  .       .  .     .  .     . .')
    print(' .       . .   ?   . .      .  /               \  .      . .   *   . .       .')
    print(' .    .      .   .      .  .  /     edChain     \  .  .      .   .      .    .')
    print(' ____________________________/                   \____________________________')
    print('\n\n\n\n')

def render_footer():
    print('\n\n\n')
    print(' .    .          .          .          .          .          .          .    .')
    print(' .       .         .         .                   .         .         .       .')
    print(' . .        .        .        .    2017-2018    .        .        .        . .')
    print(' .     .       .       .       .               .       .       .       .     .')
    print(' .    .     .     .     .     .     .     .     .     .     .     .     .    .')
    print(' .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .')
    print(' . .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . .')
    print(' . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .')
    print(' .............................................................................')

def main_menu():
    render_header()
    print(' Welcome.\n\n\n')
    print(' Enter the following information.\n\n')
    remote_username  = input(' Remote username: ')
    remote_password  = input(' Remote password: ')
    email_address    = input(' E-mail address: ')
    defined_ssh_port = input(' Defined SSH port: ')
    cluster_name     = input(' Hostname: ')
    vm_count = int(input(' Number of nodes: '))
    # number_of_core_nodes = int(input(' Number of core nodes: '))  # TODO
    # number_of_peripheral_nodes = int(input(' Number of peripheral nodes: '))  # TODO
    render_footer()
    time.sleep(1)
    return cluster_name, defined_ssh_port, email_address, remote_username, remote_password, vm_count