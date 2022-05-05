import abc
from typing import Sequence

from ytrss.core.entity.movie import Movie

from ytrss.core.helpers.typing import Path


class DownloaderError(Exception):
    """
    Error in Downloaders.
    """


class Downloader(metaclass=abc.ABCMeta):
    """ An abstract class of downloader

    The class represents an object that can download movie. It should return a sequence of paths to
    objects that has an information about files.
    """

    @abc.abstractmethod
    def download(
            self,
            movie: Movie
    ) -> Sequence[Path]:
        """
        Download movie

        The method which should download movie and return a path sequence to the movie files.
        """
