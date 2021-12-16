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
Module to download list of YouTube movie ulrs from codes.
"""

import logging
from typing import List, Iterable
from urllib.request import urlopen
from xml.dom import minidom

from ytrss.configuration.entity.source import Source
from ytrss.core.movie import Movie


class SourceDownloader:
    """
    Class to download list of YouTube movie urls.

    @ivar code: Code for parsing source
    @type code: str
    @ivar destination_dir: Name of directory where movie should be save
    @type destination_dir: str
    @ivar link_type: type of parsing source.
    @type link_type: str
    """

    def __init__(self, source: Source) -> None:
        """
        YTDown constructor.

        @param self: object handle
        @type self: L{SourceDownloader}
        @param source: parameter for youtube movie
        @type source: dict
        @raise AttributeError: lint_type is not user or playlist
        """
        self.code = source.code
        self.destination_dir = source.destination_dir
        self.link_type = source.type
        if self.link_type != "user" and self.link_type != "playlist" and self.link_type != "default":
            raise AttributeError("link_type must be 'user' or 'playlist'")

    @property
    def source_url(self) -> str:
        """
        Build url to rss source from id save in object.
        """
        pattern = "channel_id"
        if self.link_type == 'playlist':
            pattern = "playlist_id"
        return f"https://www.youtube.com/feeds/videos.xml?{pattern}={self.code}"

    @property
    def movies(self) -> Iterable[Movie]:
        """
        Get movie urls for object.
        """
        logging.debug("URL: %s", self.source_url)

        result: List[Movie] = []
        try:
            xml_str = urlopen(self.source_url).read()
            xmldoc = minidom.parseString(xml_str)
            tags = xmldoc.getElementsByTagName('link')
        # We want catch every exception in ulr like invalid channel or web
        except Exception:  # pylint: disable=W0703
            logging.error("Problem with url: %s", self.source_url)
            return result
        for elem in tags:
            url: str = elem.getAttribute("href")
            if "watch?v=" in url:
                yield Movie(url, destination_dir=self.destination_dir)
            else:
                logging.debug("Not valid url from rss: %s", url)
        return result
