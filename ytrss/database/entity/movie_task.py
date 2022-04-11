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
Movie task module
"""
import copy
import json
from typing import Optional, Dict, Any

from ytrss.core.factory.movie import create_movie

from ytrss.configuration.entity.destination import Destination
from ytrss.core.entity.movie import Movie
from ytrss.core.typing import Url


class MovieTask:
    """
    Movie task object
    """

    def __init__(self) -> None:
        self.identity: Optional[str] = None
        self.url: Optional[Url] = None
        self.destination_id: Optional[str] = None

        self.__movie: Optional[Movie] = None
        self.__destination: Optional[Destination] = None

    @property
    def json(self) -> Dict[str, Any]:
        """
        Dictionary representation of file
        """
        return {
            "id": self.identity,
            "url": self.url,
            "destination": self.destination_id
        }

    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> 'MovieTask':
        """ Create Source object from dictionary. """
        movie_task = MovieTask()
        if "id" in json_data and isinstance(json_data["id"], str):
            movie_task.identity = json_data["id"]
        if "url" in json_data and isinstance(json_data["url"], str):
            movie_task.url = Url(json_data["url"])
        if "destination" in json_data and isinstance(json_data["destination"], str):
            movie_task.destination_id = json_data["destination"]

        return movie_task

    @staticmethod
    def from_objects(movie: Movie, destination: Destination) -> 'MovieTask':
        """ Create object from movie and destination objects. """
        movie_task = MovieTask()

        movie_task.movie = movie
        movie_task.destination = destination

        return movie_task

    @property
    def movie(self) -> Movie:
        """ Movie object """
        if self.__movie is None:
            if self.url is None:
                raise ValueError()
            self.__movie = create_movie(self.url)
        if self.__movie is None:
            raise ValueError()
        return self.__movie

    @movie.setter
    def movie(self, value: Movie) -> None:
        """ Movie object setter. """
        self.__movie = value
        self.url = value.url
        self.identity = value.identity

    @property
    def destination(self) -> Destination:
        """ destination object. """
        if self.__destination is None:
            if self.destination_id is None:
                raise ValueError()
            self.__destination = Destination.from_json(self.destination_id)
        if self.__destination is None:
            raise ValueError()
        return self.__destination

    @destination.setter
    def destination(self, value: Destination) -> None:
        """ destination object setter. """
        self.__destination = value
        self.destination_id = value.identity

    @property
    def row(self) -> str:
        """ json row used in database. """
        data = self.json
        return json.dumps(data)

    def __eq__(self, other: object) -> bool:
        """
        Compare object with another object

        @param self: object handler
        @type self: L{Movie}
        @param other: other object handler or URL string
        @type other: L{Movie} or str
        @return: C{True} if object equal, C{False} otherwise
        @rtype: bool
        """
        if isinstance(other, MovieTask):
            return self.identity == other.identity
        if other == "":
            return False
        tmp_other = copy.deepcopy(other)
        return tmp_other == self
