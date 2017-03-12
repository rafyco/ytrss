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
Module to download list of YouTube movie ulrs from codes.
"""

from __future__ import unicode_literals
import logging
from urllib import urlopen
from xml.dom import minidom


class YTDown(object):
    """
    Class to download list of YouTube movie urls.

    @ivar code: Code for parsing source
    @type code: str
    @ivar link_type: type of parsing source.
        (I{user} for subscription or I{playlist} for playlist)
    @type link_type: str
    """

    def __init__(self, code, link_type='user'):
        """
        YTDown constructor.

        @param self: object handle
        @type self: L{YTDown}
        @param code: code for parsing source
        @type code: str
        @param link_type: type of source [user|playlist]
        @type link_type: str
        @raise AttributeError: lint_type is not user or playlist
        """
        self.code = code
        self.link_type = link_type
        if self.link_type is not "usr" and self.link_type is not "playlist":
            raise AttributeError("link_type must be 'user' or 'playlist'")

    def __build_url(self):
        """
        Build url to rss source from id save in object.

        @param self: object handle
        @type self: L{YTDown}
        @return: url to rss
        @rtype: str
        """
        patern = "channel_id"
        if self.link_type == 'playlist':
            patern = "playlist_id"
        return "https://www.youtube.com/feeds/videos.xml?{}={}".format(patern, self.code)

    @staticmethod
    def __youtube_list_from_address(address):
        """
        Get movie urls from rss address.

        @param address: address to playlist or subscription rss.
        @type address: list
        @return: list of movie urls
        @rtype: list
        """
        xml_str = urlopen(address).read()
        xmldoc = minidom.parseString(xml_str)
        tags = xmldoc.getElementsByTagName('link')
        result = []
        iterator = 0
        for elem in tags:
            if iterator != 0 and iterator != 1:
                url = elem.getAttribute("href")
                result.append(url)
            iterator = iterator + 1
        return result

    def get_urls(self):
        """
        Get movie urls for object.

        @param self: object handle
        @type self: L{YTDown}
        @return: list of movie urls
        @rtype: list
        """
        url = self.__build_url()
        logging.debug("URL: %s", url)
        return YTDown.__youtube_list_from_address(url)
