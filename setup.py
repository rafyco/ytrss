#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
from setuptools import setup
import codecs

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='ytrss',
    version='1.0.0',
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description="Tools for youtube downloading",
    long_description=read("README.md"),
    url="http://rafyco.pl",
    packages=['ytrss'],
    classifiers = [
        'Development Status :: 3 - Alpha'
    ],
    install_requires = [],
    entry_points = {
        'console_scripts': [
            'ytrss_subs = ytrss.subs:main'
        ]
    },
    platforms='Any',
    keywords='youtube, console'
)