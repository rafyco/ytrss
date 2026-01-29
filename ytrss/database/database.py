from datetime import datetime
import abc

from enum import Enum

from typing import Iterable, Tuple, Optional, Union

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.downloaded_movie import DownloadedMovie
from ytrss.core.entity.movie import Movie

MovieSelect = Union[Movie, DownloadedMovie, str]


def get_movie_id(movie: MovieSelect) -> str:
    """ Get movie id. """
    if isinstance(movie, DownloadedMovie):
        return movie.identity
    if isinstance(movie, Movie):
        return movie.identity
    return movie


class DatabaseStatus(Enum):
    """
    Database status types
    """
    WAIT = "wait"
    PROGRESS = "progress"
    DONE = "done"
    ERROR = "error"
    DELETED = "deleted"


class Database(metaclass=abc.ABCMeta):
    """
    Abstract database class
    """

    @abc.abstractmethod
    def is_new(self, movie: MovieSelect, destination: DestinationId) -> bool:
        """ Check if movie is ready to download. """

    @abc.abstractmethod
    def change_type(self, movie: MovieSelect, db_type: DatabaseStatus) -> None:
        """ Change type of movie task. """

    @abc.abstractmethod
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        """ Get list of movies to download. """

    @abc.abstractmethod
    def queue_mp3(self, movie: Movie, destination: DestinationId) -> bool:
        """ Add movie task to queue. """

    @abc.abstractmethod
    def get_created_data(self, movie: MovieSelect) -> Optional[datetime]:
        """ Get date of movie create. """
