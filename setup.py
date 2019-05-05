#!/usr/bin/env python3
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

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 4)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

This version of YTRSS requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have Python {}.{} or newer, then try again:

    $ python3 -m pip install --upgrade pip setuptools
    $ pip3 install ytrss
    
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON + REQUIRED_PYTHON)))
    sys.exit(1)

package_name = 'ytrss'
version = __import__(package_name).get_version()

data_files = []

setup(
    name=package_name,
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description=read_description(package_name),
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    long_description=open("README.rst").read(),
    url="https://github.com/rafyco/ytrss",
    project_urls={
        "Source": "https://github.com/rafyco/ytrss",
        "Tracker": "https://github.com/rafyco/ytrss/issues",
        "Changelog": "https://github.com/rafyco/ytrss/blob/master/dosc/changelog.rst",
        "Documentation": "https://ytrss.readthedocs.io"
    },
    packages=find_packages(),
    include_package_data=True,
    package_dir={'ytrss': 'ytrss'},
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Topic :: Multimedia :: Sound/Audio',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires=[
        'astroid==1.5.3',
        'youtube_dl==2017.10.7',
        'Sphinx==1.8.4',
        'sphinx-epytext==0.0.4',
    ],
    test_suite='ytrss.tests.__main__',
    tests_require=[
        'pylint==1.7.4',
        'pep8==1.7.1',
    ],
    entry_points={
        'console_scripts': [
            'ytdown = ytrss.ytdown:main',
        ]
    },
    command_options={
        'build_spninx': {
            'project': ('setup.py', package_name),
            'version': ('setup.py', version),
            'release': ('setup.py', version),
            'source_dir': ('setup.py', 'docs')
        }
    },
    platforms="Any",
    keywords="youtube, console, download, rss, mp3, service"
)
