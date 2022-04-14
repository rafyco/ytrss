#!/usr/bin/env python3
###########################################################################
#                                                                         #
#  Copyright (C) 2017-2022 Rafal Kobel <rafalkobel@rafyco.pl>             #
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
from typing import Iterator, Sequence

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie

from ytrss.core.typing import Path


class Destination(metaclass=abc.ABCMeta):
    """
    A base class of destination object.
    """

    @property
    @abc.abstractmethod
    def identity(self) -> DestinationId:
        """
        Identity of Destination
        """

    @property
    @abc.abstractmethod
    def info(self) -> DestinationInfo:
        """
        Data object of destination.
        """

    @property
    @abc.abstractmethod
    def dir_path(self) -> Path:
        """
        Path of destination.
        """

    @property
    @abc.abstractmethod
    def saved_movies(self) -> Iterator[DownloadedMovie]:
        """
        List of saved movies from in destination
        """

    @abc.abstractmethod
    def generate_output(self) -> None:
        """
        A method invoked after saved movie.
        """

    @abc.abstractmethod
    def save(self, files: Sequence[Path]) -> None:
        """
        Save a files to destination file.
        """
