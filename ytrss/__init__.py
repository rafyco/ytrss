#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2021 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
"""
Tools for downloading mp3 from YouTube subscription and playlists.

Installation
===========

There are a two method of installation C{ytrss} module.

From PyPI repository::

    pip install ytrss

From sources::

    git clone git@github.com:rafyco/ytrss.git
    cd ytrss
    python setup.py install

Usage
=====

Before you using this tools you should create configuration file. More
information you can find L{here<ytrss.core.settings>}.

YTRSS allow you to run a few command-line tool.

    - L{ytrss.daemon}
    - L{ytrss.ytdown}
    - L{ytrss.subs}
    - L{ytrss.rssgenerate}

"""


def get_version() -> str:
    """ Get version of ytrss package. """
    return "0.2.8"


def get_name() -> str:
    """ Get name of module. """
    return 'ytrss'


__version__ = get_version()
