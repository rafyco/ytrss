import abc
from typing import Sequence

from ytrss.core.entity.movie import Movie

from ytrss.core.typing import Path


class DownloaderError(Exception):
    """
    Error in Downloaders.
    """


class Downloader(metaclass=abc.ABCMeta):
    """
    A base class of Downloader objects.
    """

    @abc.abstractmethod
    def download(
            self,
            movie: Movie
    ) -> Sequence[Path]:
        """
        Download movie
        """