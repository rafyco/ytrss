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
Finding YouTube movie urls.
"""

import logging
from typing import Optional, Union, List, Sequence

from ytrss.configuration.entity.source import Source
from ytrss.core.ytdown import YTDown
from ytrss.core.movie import Movie


class URLFinder:
    """
    Finding YouTube movie urls from configuration.

    @ivar tab: table with source's urls
    @type tab: list
    """
    def __init__(self, sources: Optional[Sequence[Source]] = None) -> None:
        """
        URLFinder constructor.
        """
        self.tab: List[YTDown] = []
        if sources is not None:
            self.add_user_url(sources)

    def add_user_url(self, source: Union[Source, Sequence[Source]]) -> None:
        """
        Add subscription code url.

        @param self: handle object
        @type self: L{URLFinder}
        @param source: subscription's code
        @type source: str
        """
        if isinstance(source, Source):
            logging.debug("add user source: %s, [type: %s]", source.name, source.type)
            self.tab.append(YTDown(source))
        else:
            for elem in source:
                self.add_user_url(elem)

    @property
    def elements(self) -> List[Movie]:
        """
        Get urls to YouTube movies.

        @param self: handle object
        @type self: L{URLFinder}
        @return: List of elements to download
        @rtype: L{Element<ytrss.core.element.Element>}
        """
        urls = []
        for elem in self.tab:
            logging.debug("Contener: %s", elem)
            for movie in elem.movies:
                logging.debug("El: %s", movie.url)
                urls.append(movie)
        return urls
