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
from ytrss.core import YTsettingsFile
from ytrss.core import SettingException
from ytrss.core import Downloader
from optparse import OptionParser
from ytrss.subs.url_finder import URLFinder 
import os
try:
    import optcomplete
except ImportError:
    pass

def option_args():
    parser = OptionParser(description="Save urls from Youtube's subscription or playlists to file.",
                          prog='ytrss_subs',
                          version='%prog {}'.format(get_version()))                          
    parser.add_option("-d", "--debug", action="store_true",
                      dest="debug_mode", default=False,
                      help="show debug information")
    parser.add_option("-s", "--show", action="store_true",
                      dest="show_config", default=False,
                      help="Write configuration")
    parser.add_option("-c", "--conf", dest="configuration", 
                      help="configuration file", default="", metavar="FILE")
    try:
        optcomplete.autocomplete(parser)
    except NameError:
        pass
    (options, args) = parser.parse_args()
    return options

def main():
    options = option_args()
    Debug.get_instance().set_debug(options.debug_mode)
    Debug.get_instance().debug_log("Debug mode: Run")
    try:
        settings = YTsettingsFile(options.configuration)
    except SettingException:
        print("Configuration file not exist.")
        exit(1)
        
    if options.show_config:
        print(settings)
        exit()
    
    finder = URLFinder(settings)
    urls = finder.getUrls()
    downloader = Downloader(settings)
    print(settings)
    for url in urls:
        downloader.download_mp3(url)
    
    Debug.get_instance().debug_log("End")
