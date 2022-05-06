import abc
from datetime import datetime
from typing import Optional

from ytrss.core.helpers.typing import Url


class MovieError(Exception):
    """ Movie error

    An error raised when the movie cannot be created or there are some issue with creation.
    """


class Movie(metaclass=abc.ABCMeta):
    """ A movie abstract class

    This class represents a movie data. It should have an information about it, and be serialized to
    and from url.
    """

    @property
    @abc.abstractmethod
    def identity(self) -> str:
        """ A unique identity of the movie

        This identity is used to check if the two movies are the same.
        """

    @property
    @abc.abstractmethod
    def url(self) -> Url:
        """ Movie's url """

    @property
    @abc.abstractmethod
    def title(self) -> str:
        """ Movie's title """

    @property
    @abc.abstractmethod
    def author(self) -> str:
        """ Movie's author """

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """ Movie's description """

    @property
    @abc.abstractmethod
    def date(self) -> datetime:
        """ Create data """

    @property
    @abc.abstractmethod
    def img_url(self) -> Optional[Url]:
        """ An Url to movie's image """

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        """ Tell if movie is ready to download """
        return True
