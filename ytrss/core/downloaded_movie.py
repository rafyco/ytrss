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

import json
import os
from datetime import datetime
from email import utils
from typing import Any, Dict, Optional

from ytrss.configuration.configuration import Configuration
from ytrss.core.movie import Movie


class MovieFileError(Exception):
    """ File movie exception. """


class MovieMP3Error(MovieFileError):
    """ MP3 movie exception. """


class MovieJSONError(MovieFileError):
    """ JSON file movie exception. """


class DownloadedMovie:
    """
    Movie object.

    This class working on movie files and manage json's file.
    """

    def __init__(self, settings: Configuration, dirname: str, name: str) -> None:
        """
        Object construction,

        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        @param settings: settings handle
        @type settings: L{YTSettings<ytrss.core.settings.YTSettings>}
        @param dirname: Name of directory
        @type dirname:  str
        @param name: Name of movie
        @type name: str
        """
        self.__date: Optional[datetime] = None
        self.__data: Optional[Dict[str, Any]] = None
        self.__movie: Optional[Movie] = None
        self.__settings = settings
        self.dirname = dirname
        self.name = name
        if not os.path.isfile(self.json):
            raise MovieJSONError
        if not os.path.isfile(self.mp3):
            raise MovieMP3Error

    @property
    def json(self) -> str:
        """
        Return path to json file.
        """
        return os.path.join(self.__settings.output,
                            self.dirname,
                            self.name + ".json")

    @property
    def mp3(self) -> str:
        """
        Return path to mp3 file.
        """
        return os.path.join(self.__settings.output,
                            self.dirname,
                            self.name + ".mp3")

    @property
    def data(self) -> Dict[str, Any]:
        """
        Return data array.
        """
        if self.__data is None:
            with open(self.json) as data_file:
                self.__data = json.load(data_file)
        return self.__data

    @property
    def element(self) -> Movie:
        """
        Element object.
        """
        if self.__movie is None:
            self.__movie = Movie(self.data, self.dirname)
        return self.__movie

    @property
    def date(self) -> datetime:
        """
        Date object.
        """
        if self.__date is None:
            parsed_data = utils.parsedate(self.element.date)
            self.__date = datetime(*(parsed_data[0:6])) if parsed_data is not None else datetime.now()
        return self.__date

    def delete(self) -> None:
        """
        Delete movie.
        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        """
        print("delete: {}[{}]".format(self.element.date, self.element.title))
        os.remove(self.mp3)
        os.remove(self.json)
