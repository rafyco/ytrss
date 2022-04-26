import json
import os
from datetime import datetime

from email.utils import parsedate_to_datetime
from typing import Any, Optional, Dict, Sequence

from ytrss.core.entity.movie import Movie
from ytrss.core.typing import Url, Path


class MovieFileError(Exception):
    pass


class MovieResourceFileError(MovieFileError):
    pass


class MovieJSONError(MovieFileError):
    pass


class DownloadedMovie:

    def __init__(self, destination_dir: Path, identity: str) -> None:
        self.__date: Optional[datetime] = None
        self.__data_cache: Optional[Dict[str, Any]] = None
        self.__movie: Optional[Movie] = None
        self.__destination_dir = destination_dir
        self.__identity = identity
        if not os.path.isfile(self.__json):
            raise MovieJSONError
        with open(self.__json) as data_file:
            self._data: Dict[str, Any] = json.load(data_file)
        for resource_file in self.resource_files:
            if not os.path.isfile(resource_file):
                raise MovieResourceFileError

    @property
    def __json(self) -> Url:
        return Url(os.path.join(self.__destination_dir,
                                f"{self.__identity}.json"))

    @property
    def resource_files(self) -> Sequence[Url]:
        return [
            Url(os.path.join(self.__destination_dir,
                             f"{self.__identity}.mp3"))
        ]

    @property
    def date(self) -> datetime:
        if self.__date is None:
            date_str = self._data.get("date", "")
            self.__date = parsedate_to_datetime(date_str)
        return self.__date

    @property
    def title(self) -> str:
        return self._data.get("title", "<no title>")

    @property
    def image(self) -> Url:
        return Url(self._data.get("image", ""))

    @property
    def url(self) -> Url:
        return Url(self._data.get("url", ""))

    @property
    def author(self) -> str:
        return self._data.get("uploader", "")

    @property
    def identity(self) -> str:
        return self.__identity

    @property
    def description(self) -> str:
        return self._data.get("description", "")
