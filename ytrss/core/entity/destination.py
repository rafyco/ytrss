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
