import abc
from types import TracebackType

from typing import ContextManager, Optional, Iterable, Type

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie
from ytrss.database.entity.movie_task import MovieTask


class DatabaseGetOpen(metaclass=abc.ABCMeta):
    """
    TODO: documentation
    """

    @abc.abstractmethod
    def is_new(self, movie: Movie, destination: DestinationId) -> bool:
        """
        TODO: documentation
        """

    @abc.abstractmethod
    def down_next_time(self, movie: Movie, destination: DestinationId) -> None:
        """
        TODO: documentation
        """

    @abc.abstractmethod
    def add_to_history(self, movie: Movie, destination: DestinationId) -> None:
        """
        TODO: documentation
        """

    @abc.abstractmethod
    def mark_error(self, movie: Movie, destination: DestinationId) -> None:
        """
        TODO: documentation
        """

    @abc.abstractmethod
    def close(self, exc_value: Optional[BaseException]) -> None:
        """
        TODO: documentation
        """

    @abc.abstractmethod
    def movies(self) -> Iterable[MovieTask]:
        """
        TODO: documentation
        """


class DatabaseGet(ContextManager[DatabaseGetOpen], metaclass=abc.ABCMeta):
    """
    TODO: documentation
    """

    def __init__(self) -> None:
        self.__connection: Optional[DatabaseGetOpen] = None

    @abc.abstractmethod
    def open(self) -> DatabaseGetOpen:
        """
        TODO: documentation
        """

    def __enter__(self) -> DatabaseGetOpen:
        self.__connection = self.open()
        return self.__connection

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            exc_trackback: Optional[TracebackType]
    ) -> None:
        if self.__connection is not None:
            self.__connection.close(exc_value)
