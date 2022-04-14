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
import abc
from typing import Sequence

from ytrss.core.entity.movie import Movie

from ytrss.core.typing import Path


class DownloaderError(Exception):
    """
    Error in Downloaders.
    """


class Downloader(metaclass=abc.ABCMeta):
    """
    A base class of Downloader objects.
    """

    @abc.abstractmethod
    def download(
            self,
            movie: Movie
    ) -> Sequence[Path]:
        """
        Download movie
        """
