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
try:
    # This library should be using by Python2
    from urllib.request import urlopen  # pylint: disable=E0611,F0401
except ImportError:
    from urllib import urlopen
from xml.dom import minidom


class YTDown(object):
    """
    Class to download list of YouTube movie urls.

    @ivar code: Code for parsing source
    @type code: str
    @ivar destination_dir: Name of directory where movie should be save
    @type destination_dir: str
    @ivar link_type: type of parsing source.
    @type link_type: str
    """

    def __init__(self, url, link_type='user'):
        """
        YTDown constructor.

        @param self: object handle
        @type self: L{YTDown}
        @param url: parameter for youtube movie
        @type url: dict
        @param link_type: type of source [user|playlist]
        @type link_type: str
        @raise AttributeError: lint_type is not user or playlist
        """
        assert isinstance(url, dict)
        self.code = url['code']
        if 'destination_dir' in url:
            self.destination_dir = url['destination_dir']
        else:
            self.destination_dir = "other"
        self.link_type = link_type
        if self.link_type != "user" and self.link_type != "playlist":
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
        return ("https://www.youtube.com/feeds/videos.xml?"
                "{}={}".format(patern, self.code))

    @staticmethod
    def __youtube_list_from_address(address):
        """
        Get movie urls from rss address.

        @param address: address to playlist or subscription rss.
        @type address: list
        @return: list of movie urls
        @rtype: list
        """
        result = []
        try:
            xml_str = urlopen(address).read()
            xmldoc = minidom.parseString(xml_str)
            tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logging.error("Problem with url: %s", address)
            return result
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
