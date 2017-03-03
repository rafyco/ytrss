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

import sys,os
from setuptools import setup, find_packages
import codecs

def read_markdown(fname):
    fpath = os.path.join(os.path.dirname(__file__), fname)
    try:
        import pypandoc
        return pypandoc.convert(fpath, 'rst')
    except(IOError, ImportError, RuntimeError):
        return codecs.open(fpath).read()

version=__import__('ytrss').get_version()

console_scripts = [
            'ytrss_subs = ytrss.subs:main',
            'ytrss_daemon = ytrss.daemon:main',
            'ytdown = ytrss.ytdown:main'
        ]
if os.uname() == 'Linux':
    console_scripts.append('/etc/init.d/ytrss = ytrss.daemon:daemon')
        
setup(
    name='ytrss',
    version=version,
    license='GNU',
    author="Rafal Kobel",
    author_email="rafalkobel@rafyco.pl",
    description="Tools for youtube downloading",
    long_description=read_markdown("README.md"),
    url="http://bitbucket.org/rafyco/ytrss",
    packages=find_packages(),
    include_package_data=True,
    package_dir={'ytrss' : 'ytrss'},
    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    install_requires = [],
    entry_points = {
        'console_scripts': console_scripts
    },
    platforms='Any',
    keywords='youtube, console'
)
