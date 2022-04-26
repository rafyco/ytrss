import abc
from typing import Iterable

from ytrss.database.entity.movie_task import MovieTask


class SourceDownloader(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def movies(self) -> Iterable[MovieTask]:
        pass
