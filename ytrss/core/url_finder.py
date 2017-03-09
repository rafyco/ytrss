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
from ytrss.core.system.debug import Debug
from ytrss.core.ytdown import YTDown

class URLFinder:
    def __init__(self, settings = None):
        self.tab = []
        if settings != None:
            self.add_user_url(settings.get_user_urls())
            self.add_playlist_url(settings.get_playlist_urls())

    def add_user_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_user_url(elem)
        else:
            Debug().debug_log("add user url: %s" % url)
            self.tab.append(YTDown(url, type="user"))

    def add_playlist_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_playlist_url(elem)
        else:
            Debug().debug_log("add playlist url: %s" % url)
            self.tab.append(YTDown(url, type="playlist"))

    def getUrls(self):
        urls = []
        for elem in self.tab:
            Debug().debug_log("Contener: %s" % elem)
            addresses = elem.getUrls()
            for address in addresses:
                Debug().debug_log("El: %s" % address)
                urls.append(address)
        return urls
