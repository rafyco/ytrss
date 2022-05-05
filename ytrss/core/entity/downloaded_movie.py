import json
import os
from datetime import datetime

from email.utils import parsedate_to_datetime
from typing import Any, Optional, Dict, Sequence

from ytrss.core.entity.movie import Movie
from ytrss.core.helpers.typing import Url, Path


class MovieFileError(Exception):
    """ Error in Downloaded movie object """


class MovieResourceFileError(MovieFileError):
    """ Movie resource file error

    Error throws when the resource file not exists
    """


class MovieJSONError(MovieFileError):
    """ Movie Json Error

    Error throws when the json description file is invalid
    """


class DownloadedMovie:
    """ Downloaded movie

    The object that represents downloaded movie in destination. It has a field with description
    of movie and list of additional files.
    """

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
        """ List of full paths of files according movie """
        return [
            Url(os.path.join(self.__destination_dir,
                             file_path)) for file_path in self.files_paths
        ]

    @property
    def files_paths(self) -> Sequence[Url]:
        """ List of files according movie """
        return [
            Url(f"{self.__identity}.mp3")
        ]

    @property
    def date(self) -> datetime:
        """ create date """
        if self.__date is None:
            date_str = self._data.get("date", "")
            self.__date = parsedate_to_datetime(date_str)
        return self.__date

    @property
    def title(self) -> str:
        """ movie's title"""
        return self._data.get("title", "<no title>")

    @property
    def image(self) -> Optional[Url]:
        """ files image """
        image = self._data.get("image", "")
        return Url(image) if image != "" else None

    @property
    def url(self) -> Url:
        """ movie's url """
        return Url(self._data.get("url", ""))

    @property
    def author(self) -> str:
        """ author of downloaded movie """
        return self._data.get("uploader", "")

    @property
    def identity(self) -> str:
        """ movie's identity """
        return self.__identity

    @property
    def description(self) -> str:
        """ movie's description """
        return self._data.get("description", "")
