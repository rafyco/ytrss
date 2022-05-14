import abc
from typing import Iterable, Tuple

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie


class SourceDownloaderError(Exception):
    """ This is source downloader error """


class SourceDownloader(metaclass=abc.ABCMeta):
    """ Source downloader abstract class.

    This class represents a source of movies. It should check a source and returns an iterable
    list of movies available to download.
    """

    @property
    @abc.abstractmethod
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        """ A list of movies available to download with destination id of this movie"""
