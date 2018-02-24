#!/usr/bin/env python3

import os


def replicate(count, hostname, package, stem):
    os.system('cp masters/{2}/{3}.sh procedures/{2}/{3}-{1}-{0}.sh'.format(count, hostname, package, stem))


def edit(count, hostname, package, old_string, new_string):
	os.system()

