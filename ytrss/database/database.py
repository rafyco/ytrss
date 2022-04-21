import abc

from enum import Enum

from typing import Iterable

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie
from ytrss.database.entity.movie_task import MovieTask


class DatabaseStatus(Enum):
    """
    Database status types
    """
    WAIT = "wait"
    PROGRESS = "progress"
    DONE = "done"
    ERROR = "error"


class Database(metaclass=abc.ABCMeta):
    """
    Abstract database class
    """

    @abc.abstractmethod
    def is_new(self, movie: Movie, destination: DestinationId) -> bool:
        """ Check if movie is ready to download. """

    @abc.abstractmethod
    def change_type(self, movie: Movie, db_type: DatabaseStatus) -> None:
        """ Change type of movie task. """

    @abc.abstractmethod
    def movies(self) -> Iterable[MovieTask]:
        """ Get list of movies to download. """

    @abc.abstractmethod
    def queue_mp3(self, movie: Movie, destination: DestinationId) -> bool:
        """ Add movie task to queue. """
