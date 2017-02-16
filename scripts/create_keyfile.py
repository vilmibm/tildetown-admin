#!/usr/bin/env python3
import sys

KEYFILE_PATH = '/home/{}/.ssh/authorized_keys2'


def main(argv):
    username = argv[1]
    with open(KEYFILE_PATH.format(username), 'w') as f:
        f.write(sys.stdin.read())


if __name__ == '__main__':
    exit(main(sys.argv))
