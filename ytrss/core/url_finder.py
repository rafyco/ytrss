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
import logging
from ytrss.core.ytdown import YTDown


class URLFinder(object):
    def __init__(self, settings=None):
        self.tab = []
        if settings is not None:
            self.add_user_url(settings.urls)
            self.add_playlist_url(settings.playlists)

    def add_user_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_user_url(elem)
        else:
            logging.debug("add user url: %s", url)
            self.tab.append(YTDown(url, link_type="user"))

    def add_playlist_url(self, url):
        if isinstance(url, list):
            for elem in url:
                self.add_playlist_url(elem)
        else:
            logging.debug("add playlist url: %s", url)
            self.tab.append(YTDown(url, link_type="playlist"))

    def get_urls(self):
        urls = []
        for elem in self.tab:
            logging.debug("Contener: %s", elem)
            addresses = elem.get_urls()
            for address in addresses:
                logging.debug("El: %s", address)
                urls.append(address)
        return urls
