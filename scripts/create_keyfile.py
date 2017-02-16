#!/usr/bin/env python3
"""this script allows django to add public keys for a user. it's in its own
script so that a specific command can be added to the ttadmin user's sudoers
file."""
import sys

KEYFILE_PATH = '/home/{}/.ssh/authorized_keys2'


def main(argv):
    username = argv[1]
    with open(KEYFILE_PATH.format(username), 'w') as f:
        f.write(sys.stdin.read())


if __name__ == '__main__':
    exit(main(sys.argv))
