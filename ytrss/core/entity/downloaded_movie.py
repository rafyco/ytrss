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
Podcast's movie.
"""
import abc
from datetime import datetime

from ytrss.core.entity.movie import Movie


class MovieFileError(Exception):
    """ File movie exception. """


class MovieMP3Error(MovieFileError):
    """ MP3 movie exception. """


class MovieJSONError(MovieFileError):
    """ JSON file movie exception. """


class DownloadedMovie(metaclass=abc.ABCMeta):
    """
    Movie object.

    This class working on movie files and manage json's file.
    """

    @property
    @abc.abstractmethod
    def element(self) -> Movie:
        """
        Element object.
        """

    @property
    @abc.abstractmethod
    def date(self) -> datetime:
        """
        Date object.
        """

    @abc.abstractmethod
    def delete(self) -> None:
        """
        Delete movie.
        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        """

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """
        Title of movie
        """

    @property
    @abc.abstractmethod
    def image(self) -> str:
        """
        image of movie
        """

    @property
    @abc.abstractmethod
    def url(self) -> str:
        """
        url of movie
        """

    @property
    @abc.abstractmethod
    def author(self) -> str:
        """
        author of the movie
        """

    @property
    @abc.abstractmethod
    def filename(self) -> str:
        """
        filename of movie
        """

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """
        description of the movie
        """
