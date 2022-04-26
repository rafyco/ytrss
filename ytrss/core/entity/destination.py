import abc
from typing import Iterator, Sequence

from ytrss.configuration.entity.destination_info import DestinationId, DestinationInfo
from ytrss.core.entity.downloaded_movie import DownloadedMovie

from ytrss.core.typing import Path


class Destination(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def identity(self) -> DestinationId:
        pass

    @property
    @abc.abstractmethod
    def info(self) -> DestinationInfo:
        pass

    @property
    @abc.abstractmethod
    def saved_movies(self) -> Iterator[DownloadedMovie]:
        pass

    @abc.abstractmethod
    def on_finish(self) -> None:
        pass

    @abc.abstractmethod
    def save(self, files: Sequence[Path]) -> None:
        pass
