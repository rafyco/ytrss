import abc
from typing import Sequence

from ytrss.core.entity.movie import Movie

from ytrss.core.helpers.typing import Path


class DownloaderError(Exception):
    """
    Error in Downloaders.
    """


class Downloader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def download(
            self,
            movie: Movie
    ) -> Sequence[Path]:
        pass
