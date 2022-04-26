import copy
import json
from typing import Optional, Dict, Any

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.factory.movie import create_movie

from ytrss.core.entity.movie import Movie
from ytrss.core.typing import Url


class MovieTask:
    """
    Movie task object
    """

    def __init__(self) -> None:
        self.identity: Optional[str] = None
        self.url: Optional[Url] = None
        self.destination_id: Optional[DestinationId] = None

        self.__movie: Optional[Movie] = None
        self.__destination: Optional[DestinationId] = None

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
            movie_task.destination_id = DestinationId(json_data["destination"])

        return movie_task

    @staticmethod
    def from_objects(movie: Movie, destination: DestinationId) -> 'MovieTask':
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
    def destination(self) -> DestinationId:
        """ destination object. """
        if self.__destination is None:
            if self.destination_id is None:
                raise ValueError()
            self.__destination = DestinationId(self.destination_id)
        if self.__destination is None:
            raise ValueError()
        return self.__destination

    @destination.setter
    def destination(self, value: DestinationId) -> None:
        """ destination object setter. """
        self.__destination = value
        self.destination_id = value

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
