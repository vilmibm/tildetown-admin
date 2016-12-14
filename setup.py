#!/usr/bin/env python

from setuptools import setup

setup(
    name='tildetown-admin',
    version='1.0.0',
    description='administrative webapp for tilde.town',
    url='https://github.com/nathanielksmith/prosaic',
    author='vilmibm shaksfrpease',
    author_email='vilmibm@protonmail.ch',
    license='AGPL',
    classifiers=[
        'Topic :: Artistic Software',
        'License :: OSI Approved :: Affero GNU General Public License v3 (AGPLv3)',
    ],
    packages=['ttadmin'],
    install_requires = ['Django==1.10.2',
                        'sshpubkeys==2.2.0',],
    include_package_data = True,
)
