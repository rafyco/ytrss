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

from ytrss import get_version
from ytrss.core.sys.debug import Debug
from ytrss.core.settings import SettingException
from ytrss.core import Downloader
from ytrss.core.settings import YTsettingsFile
from optparse import OptionParser
import os
try:
    import optcomplete
except ImportError:
    pass

def option_args():
    parser = OptionParser(description="Save one or more urls from Youtube to file.",
                          prog='ytdown',
                          usage='%prog [options] [urls]',
                          version='%prog {}'.format(get_version()))
    parser.add_option("-d", "--debug", action="store_true",
                      dest="debug_mode", default=False,
                      help="show debug information")
    parser.add_option("-c", "--conf", dest="configuration", 
                      help="configuration file", default="", metavar="FILE")
                      
    parser
    try:
        optcomplete.autocomplete(parser)
    except NameError:
        pass
    (options, args) = parser.parse_args()

    return (options, args)

def main():
    (options, args) = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    try:
        settings = YTsettingsFile(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    if len(args) < 1:
        print("Require url to download")
        exit(1)
        
    downloader = Downloader(settings)
    for url in args:
        downloader.download_mp3(url)
    