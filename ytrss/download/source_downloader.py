"""
Module to download list of YouTube movie ulrs from codes.
"""
import abc
from typing import Iterable

from ytrss.core.typing import Url
from ytrss.database.entity.movie_task import MovieTask


class SourceDownloader(metaclass=abc.ABCMeta):
    """
    Class to download list of YouTube movie urls.
    """

    @property
    @abc.abstractmethod
    def source_url(self) -> Url:
        """
        Build url to rss source from id save in object.
        """

    @property
    @abc.abstractmethod
    def movies(self) -> Iterable[MovieTask]:
        """
        Get movie urls for object.
        """
