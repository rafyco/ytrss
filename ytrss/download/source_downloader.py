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
import abc
from typing import Iterable

from ytrss.core.typing import Url
from ytrss.database.entity.movie_task import MovieTask


class SourceDownloader(metaclass=abc.ABCMeta):
    """
    Class to download list of YouTube movie urls.
    """

    @property
    @abc.abstractmethod
    def source_url(self) -> Url:
        """
        Build url to rss source from id save in object.
        """

    @property
    @abc.abstractmethod
    def movies(self) -> Iterable[MovieTask]:
        """
        Get movie urls for object.
        """
