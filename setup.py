#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
#                                                                         #
#  Copyright (C) 2017  Rafal Kobel <rafalkobel@rafyco.pl>                 #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                         #
###########################################################################

from __future__ import unicode_literals
import os
import sys
import codecs
from setuptools import setup
from setuptools import find_packages


def read_description(module_name):
    module_doc = __import__(module_name).__doc__.splitlines()
    result = ""
    for line in module_doc:
        if line:
            result = line
            break
    return result

version = __import__('ytrss').get_version()

data_files = []

setup(
    name='ytrss',
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description=read_description('ytrss'),
    long_description=open("README.rst").read(),
    url="https://github.com/rafyco/ytrss",
    packages=find_packages(),
    include_package_data=True,
    package_dir={'ytrss': 'ytrss'},
    test_suite='ytrss.tests.__main__',
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
        'astroid==1.5.3',
        'youtube_dl==2017.10.7',
        'pylint==1.7.4',
        'pep8==1.7.1'
    ],
    entry_points={
        'console_scripts': [
            'ytdown = ytrss.ytdown:main',
        ]
    },
    platforms="Any",
    keywords="youtube, console, download, rss, mp3, service"
)
