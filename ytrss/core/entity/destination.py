import abc
from typing import Iterator, Sequence

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie

from ytrss.core.helpers.typing import Path
from ytrss.core.managers.templates_manager import TemplatesManager


class DestinationError(Exception):
    """ Destination error

    The error raised when Destination object cannot be created
    """


class Destination(metaclass=abc.ABCMeta):
    """ Destination object

    This object represents a place where the file should be saved after download.
    """

    @property
    @abc.abstractmethod
    def identity(self) -> DestinationId:
        """ Identity of destination

        A string representation of object, that can be defined in json file by user.
        """

    @property
    @abc.abstractmethod
    def info(self) -> DestinationInfo:
        """ Information about destination. """

    @property
    @abc.abstractmethod
    def saved_movies(self) -> Iterator[DownloadedMovie]:
        """ A list of movies saved in destination. """

    def on_finish(self, templates_manager: TemplatesManager) -> None:
        """ An optional method that generate additional files, or make an additional
         things after download like sending to external service. """

    @abc.abstractmethod
    def save(self, files: Sequence[Path], templates_manager: TemplatesManager) -> None:
        """ Save file from downloader cache to destination. """
