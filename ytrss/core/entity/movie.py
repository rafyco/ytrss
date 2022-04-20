"""
Element to download
"""
import abc
from typing import Dict, Any, Optional

from ytrss.core.typing import Url


class InvalidStringJSONParseError(Exception):
    """ Element Parse Exception """


class InvalidParameterMovieError(Exception):
    """ Element Exception - Invalid Parameter """


class Movie(metaclass=abc.ABCMeta):
    """
    Movie's data.
    """

    @property
    @abc.abstractmethod
    def identity(self) -> str:
        """
        Movie's ID
        """

    @property
    @abc.abstractmethod
    def url(self) -> Url:
        """
        URL to movie
        """

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """
        movie's title
        """

    @property
    @abc.abstractmethod
    def author(self) -> str:
        """
        movie's author
        """

    @property
    @abc.abstractmethod
    def desc(self) -> str:
        """
        movie's description
        """

    @property
    @abc.abstractmethod
    def date(self) -> str:
        """
        movie's create data
        """

    @property
    @abc.abstractmethod
    def img_url(self) -> Optional[Url]:
        """
        image's ULR
        """

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        """
        Is movie is ready to download
        """

    @property
    @abc.abstractmethod
    def json(self) -> Dict[str, Any]:
        """
        Return movie's description in JSON format
        """
