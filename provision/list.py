from __future__ import print_function
from __future__ import absolute_import

import sys
import argparse

import provision.config as config
import provision.nodelib as nodelib

def parser():
    parser = argparse.ArgumentParser()
    config.add_auth_args(parser, config)
    return parser

def print_list():
    parsed = config.reconfig(parser)
    driver = nodelib.get_driver(parsed.secret_key, parsed.userid, parsed.provider)
    [print('%s %s' % (n.name, n.public_ips)) for n in nodelib.list_nodes(driver)]

def main():
    return config.handle_errors(print_list)

if __name__ == '__main__':
    sys.exit(main())
