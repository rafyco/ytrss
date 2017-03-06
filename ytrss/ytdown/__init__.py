#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
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
from ytrss import get_version
from ytrss.core.sys.debug import Debug
from ytrss.core.settings import SettingException
from ytrss.core import Download_Queue
from ytrss.core.settings import YTSettings
from argparse import ArgumentParser
import os
try:
    import argcomplete
except ImportError:
    pass

def option_args():
    parser = ArgumentParser(description="Save one or more urls from Youtube to file.",
                            prog='ytdown',
                            version='%(prog)s {}'.format(get_version()))
    parser.add_argument("-d", "--debug", action="store_true",
                        dest="debug_mode", default=False,
                        help="show debug information")
    parser.add_argument("-c", "--conf", dest="configuration", 
                        help="configuration file", default="", metavar="FILE")
    parser.add_argument("urls", nargs='*', default=[], type=unicode,
                        help="Url to download.")
    try:
        argcomplete.autocomplete(parser)
    except NameError:
        pass
    options = parser.parse_args()

    return options

def main():
    options = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    try:
        settings = YTSettings(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    if len(options.urls) < 1:
        print("Require url to download")
        exit(1)
        
    queue = Download_Queue(settings)
    for url in options.urls:
        print("ARG: {}".format(url))
        #if queue.queue_mp3(url):
        #    print("Filmik zostanie pobrany: {}".format(url))
        #else:
        #    print("Filmik nie zostanie pobrany: {}".format(url))
