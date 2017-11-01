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
Podcast's movie.
"""

from __future__ import unicode_literals
from __future__ import print_function
import json
import os


class MovieFileError(Exception):
    """ File movie exception. """
    pass


class MovieMP3Error(MovieFileError):
    """ MP3 movie exception. """
    pass


class MovieJSONError(MovieFileError):
    """ JSON file movie exception. """
    pass


class Movie(object):
    """
    Movie object.

    This class working on movie files and manage json's file.
    """

    def __init__(self, settings, dirname, name):
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
        self.__data = None
        self.__settings = settings
        self.dirname = dirname
        self.name = name
        if not os.path.isfile(self.json):
            raise MovieJSONError
        if not os.path.isfile(self.mp3):
            raise MovieMP3Error

    @property
    def json(self):
        """
        Return path to json file.

        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        @return path to json file
        @rtype: str
        """
        return os.path.join(self.__settings.output,
                            self.dirname,
                            self.name + ".json")

    @property
    def mp3(self):
        """
        Return path to mp3 file.

        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        @return path to mp3 file
        @rtype: str
        """
        return os.path.join(self.__settings.output,
                            self.dirname,
                            self.name + ".mp3")

    @property
    def data(self):
        """
        Return data array.

        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        @return data array
        @rtype: list
        """
        if self.__data is None:
            with open(self.json) as data_file:
                self.__data = json.load(data_file)
        return self.__data
