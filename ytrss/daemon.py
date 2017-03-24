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
Command line program to automatic downloading files.

Program checking file and download all file descripe in it. It's recomended to
add this file to crontab or call it manualy.

Example usage
=============

To invoke program type in your console::

    ytrss_deamon

or::

    python -m ytrss.daemon

for more option call program with flag C{--help}
"""

from __future__ import unicode_literals
from __future__ import print_function
from ytrss.ytdown import daemon

if __name__ == "__main__":
    daemon()
