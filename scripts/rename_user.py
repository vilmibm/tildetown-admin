#!/usr/bin/env python3
"""This script wraps the usermod command to allow user account renames via sudoers."""
import os
import sys
import subprocess


def rename_user(username, new_username):
    # usermod -l new_username -m -d /home/{new_username} username
    args = [
        'usermod',
        '-l',
        new_username,
        '-m',
        '-d',
        os.path.join('/home', new_username),
        username
    ]
    subprocess.run(args, check=True)


def main(argv):
    if len(argv) < 3:
        print('[rename_user] Too few arguments passed.', file=sys.stderr)
        return 1

    try:
        rename_user(argv[1], argv[2])
    except subprocess.CalledProcessError as e:
        print('[rename_user] {}'.format(e), file=sys.stderr)
        return 2

    return 0


if __name__ == '__main__':
    exit(main(sys.argv))
