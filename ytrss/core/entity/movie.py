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
Element to download
"""
import abc
from typing import Dict, Any, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.configuration.entity.destination import Destination
from ytrss.core.typing import Url


class InvalidStringJSONParseError(Exception):
    """ Element Parse Exception """


class InvalidParameterMovieError(Exception):
    """ Element Exception - Invalid Parameter """


class Movie(metaclass=abc.ABCMeta):
    """
    Movie's data.
    """

    @property
    @abc.abstractmethod
    def identity(self) -> str:
        """
        Movie's ID
        """

    @property
    @abc.abstractmethod
    def url(self) -> Url:
        """
        URL to movie
        """

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """
        movie's title
        """

    @property
    @abc.abstractmethod
    def author(self) -> str:
        """
        movie's author
        """

    @property
    @abc.abstractmethod
    def desc(self) -> str:
        """
        movie's description
        """

    @property
    @abc.abstractmethod
    def date(self) -> str:
        """
        movie's create data
        """

    @property
    @abc.abstractmethod
    def img_url(self) -> Optional[Url]:
        """
        image's ULR
        """

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        """
        Is movie is ready to download
        """

    @abc.abstractmethod
    def download(self, settings: Configuration, destination: Destination) -> bool:
        """
        Download element
        """

    @property
    @abc.abstractmethod
    def json(self) -> Dict[str, Any]:
        """
        Return movie's description in JSON format
        """
