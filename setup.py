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


def read_markdown(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    try:
        import pypandoc
        return pypandoc.convert(fpath, 'rst')
    except(IOError, ImportError, RuntimeError):
        return codecs.open(fpath).read().decode('utf-8')


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

if not(sys.platform.lower().startswith('win')):
    data_files.append(('/etc/init.d', ['scripts/ytrss']))

setup(
    name='ytrss',
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description=read_description('ytrss'),
    long_description=read_markdown("README.md"),
    url="http://bitbucket.org/rafyco/ytrss",
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
        'youtube_dl',
        'daemonocle',
        'pep8'
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'ytdown = ytrss.ytdown:main',
        ]
    },
    platforms='Any',
    keywords='youtube, console, download, rss, mp3, service'
)
