import abc
from typing import Iterable, Tuple

from ytrss.configuration.entity.destination_info import DestinationId
from ytrss.core.entity.movie import Movie


class SourceDownloaderError(Exception):
    pass


class SourceDownloader(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def movies(self) -> Iterable[Tuple[Movie, DestinationId]]:
        pass
