import abc
from datetime import datetime
from typing import Dict, Any, Optional

from ytrss.core.typing import Url


class InvalidStringJSONParseError(Exception):
    pass


class InvalidParameterMovieError(Exception):
    pass


class Movie(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def identity(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def url(self) -> Url:
        pass

    @property
    @abc.abstractmethod
    def title(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def author(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def description(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def date(self) -> datetime:
        pass

    @property
    @abc.abstractmethod
    def img_url(self) -> Optional[Url]:
        pass

    @property
    @abc.abstractmethod
    def is_ready(self) -> bool:
        return True

    @property
    @abc.abstractmethod
    def json(self) -> Dict[str, Any]:
        pass
