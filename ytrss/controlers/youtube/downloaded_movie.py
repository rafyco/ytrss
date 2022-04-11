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
from ytrss.configuration.entity.destination import Destination
from ytrss.controlers.youtube.movie import YouTubeMovie
from ytrss.core.entity.downloaded_movie import DownloadedMovie, MovieJSONError, MovieMP3Error
from ytrss.core.entity.movie import Movie
from ytrss.core.typing import Path, Url


class YouTubeDownloadedMovie(DownloadedMovie):
    """
    YouTube Movie object.

    This class working on movie files and manage json's file.
    """

    def __init__(self, settings: Configuration, destination: Destination, name: str) -> None:
        """
        Object construction,
        """
        self.__date: Optional[datetime] = None
        self.__data: Optional[Dict[str, Any]] = None
        self.__movie: Optional[Movie] = None
        self.__settings = settings
        self.__destination = destination
        self.__name = name
        if not os.path.isfile(self.__json):
            raise MovieJSONError
        if not os.path.isfile(self.__mp3):
            raise MovieMP3Error

    @property
    def __json(self) -> Url:
        """
        Return path to json file.
        """
        return Url(os.path.join(self.__settings.conf.output,
                                self.__destination.destination_dir,
                                self.__name + ".json"))

    @property
    def __mp3(self) -> Url:
        """
        Return path to mp3 file.
        """
        return Url(os.path.join(self.__settings.conf.output,
                                self.__destination.destination_dir,
                                self.__name + ".mp3"))

    @property
    def data(self) -> Dict[str, Any]:
        """
        Return data array.
        """
        if self.__data is None:
            with open(self.__json) as data_file:
                self.__data = json.load(data_file)
        return self.__data

    @property
    def movie(self) -> Movie:
        """
        Element object.
        """
        if self.__movie is None:
            if 'url' not in self.data:
                raise TypeError()
            self.__movie = YouTubeMovie(self.data['url'])
        return self.__movie

    @property
    def destination(self) -> Destination:
        """
        destination object
        """
        return self.__destination

    @property
    def date(self) -> datetime:
        """
        Date object.
        """
        if self.__date is None:
            parsed_data = utils.parsedate(self.movie.date)
            self.__date = datetime(*(parsed_data[0:6])) if parsed_data is not None else datetime.now()
        return self.__date

    @property
    def title(self) -> str:
        return self.data.get("title", "<no title>")

    @property
    def image(self) -> Url:
        return self.data.get("image", "")

    @property
    def url(self) -> Url:
        return self.data.get("url", "")

    @property
    def author(self) -> str:
        return self.data.get("uploader", "")

    @property
    def filename(self) -> Path:
        return Path(self.__name)

    @property
    def description(self) -> str:
        return self.data.get("description", "")

    def delete(self) -> None:
        """
        Delete movie.
        @param self: object handle
        @type self: L{Movie<ytrss.core.movie.Movie>}
        """
        print("delete: {}[{}]".format(self.movie.date, self.movie.title))
        os.remove(self.__mp3)
        os.remove(self.__json)
