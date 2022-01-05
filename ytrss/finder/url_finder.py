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
from typing import Optional, Union, List, Sequence, Iterator

from ytrss.configuration.entity.source import Source
from ytrss.core.factory import CoreFactoryError
from ytrss.core.factory.source_downloader import create_source_downloader
from ytrss.download.source_downloader import SourceDownloader
from ytrss.core.movie import Movie


class URLFinder:
    """
    Finding YouTube movie urls from configuration.

    @ivar __sources: table with source's urls
    @type __sources: list
    """
    def __init__(self, sources: Optional[Sequence[Source]] = None) -> None:
        """
        URLFinder constructor.
        """
        self.__sources: List[SourceDownloader] = []
        if sources is not None:
            self.__add_source(sources)

    def __add_source(self, source: Union[Source, Sequence[Source]]) -> None:
        """
        Add subscription code url.

        @param self: handle object
        @type self: L{URLFinder}
        @param source: subscription's code
        @type source: str
        """
        if isinstance(source, Source):
            logging.debug("add user source: %s, [type: %s]", source.name, source.type)
            try:
                self.__sources.append(create_source_downloader(source))
            except CoreFactoryError:
                pass
        else:
            for elem in source:
                self.__add_source(elem)

    @property
    def movies(self) -> Iterator[Movie]:
        """
        Get urls to YouTube movies.

        @param self: handle object
        @type self: L{URLFinder}
        @return: List of elements to download
        @rtype: L{Element<ytrss.core.element.Element>}
        """
        for source in self.__sources:
            logging.debug("Container: %s", source)
            for movie in source.movies:
                logging.debug("El: %s", movie)
                yield movie
