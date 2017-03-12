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
"""
Tools for downloading mp3 from YouTube subscription and playlists.

Insallation
===========

There are a two metod of installation C{ytrss} module.

From PyPI repository::

    pip install ytrss

From sources::

    git clone git@bitbucket.org:rafyco/ytrss.git
    cd ytrss
    python setup.py install

Usage
=====

Before you using this tools you should create configuration file. More
information you can find L{here<ytrss.core.settings>}.

YTRSS allow you to run a few command-line tool.

    - L{ytrss_daemon<ytrss.daemon>}
    - L{ytdown<ytrss.ytdown>}
    - L{ytrss_subs<ytrss.subs>}

"""

from __future__ import unicode_literals


def get_version():
    """ Get version of ytrss package. """
    return "0.1.2"

__version__ = get_version()
