# server setup for ttadmin

## stuff to install

* autoconf?
* python3-dev
* postgresql-server-dev-9.5
* python 3.5+
* postgresql
* virtualenv
* nginx

## steps

* create ttadmin user
* ttadmin db user (or just rely on ident..?) / database created
* copy `create_keyfile.py` from `scripts/` and put it in `/opt/bin/`. 
* `chmod o+x /opt/bin/create_keyfile.py``
* add to sudoers: 

    ttadmin ALL=(ALL)NOPASSWD:/usr/sbin/adduser,/bin/mkdir,/opt/bin/create_keyfile.py

* have virtualenv with python 3.5+ ready, install tildetown-admin package into it
* run django app as wsgi container through gunicorn as the ttadmin user with venv active
* nginx proxy pass at /ttadmin
