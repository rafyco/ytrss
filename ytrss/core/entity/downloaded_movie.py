"""
Podcast's movie.
"""
import json
import os
from datetime import datetime

from email.utils import parsedate_to_datetime
from typing import Any, Optional, Dict

from ytrss.core.factory.movie import create_movie
from ytrss.core.entity.movie import Movie
from ytrss.core.logging import logger
from ytrss.core.typing import Url, Path


class MovieFileError(Exception):
    """ File movie exception. """


class MovieMP3Error(MovieFileError):
    """ MP3 movie exception. """


class MovieJSONError(MovieFileError):
    """ JSON file movie exception. """


class DownloadedMovie:
    """
    Movie object.

    This class working on movie files and manage json's file.
    """

    def __init__(self, destination_dir: Path, name: str) -> None:
        """
        Object construction,
        """
        self.__date: Optional[datetime] = None
        self.__data: Optional[Dict[str, Any]] = None
        self.__movie: Optional[Movie] = None
        self.__destination_dir = destination_dir
        self.__name = name
        if not os.path.isfile(self.__json):
            raise MovieJSONError
        if not os.path.isfile(self.__mp3):
            raise MovieMP3Error

    @property
    def __json(self) -> Url:
        """
        Return path to json file.
        """
        return Url(os.path.join(self.__destination_dir,
                                self.__name + ".json"))

    @property
    def __mp3(self) -> Url:
        """
        Return path to mp3 file.
        """
        return Url(os.path.join(self.__destination_dir,
                                self.__name + ".mp3"))

    @property
    def data(self) -> Dict[str, Any]:
        """
        Return data array.
        """
        if self.__data is None:
            with open(self.__json) as data_file:
                self.__data = json.load(data_file)
        return self.__data

    @property
    def date(self) -> datetime:
        """ Movie's date """
        if self.__date is None:
            date_str = self.data.get("date", "")
            self.__date = parsedate_to_datetime(date_str)
        return self.__date

    @property
    def title(self) -> str:
        """ Movie's title """
        return self.data.get("title", "<no title>")

    @property
    def image(self) -> Url:
        """ Movie's image """
        return self.data.get("image", "")

    @property
    def url(self) -> Url:
        """ Movie's url """
        return Url(self.data.get("url", ""))

    @property
    def author(self) -> str:
        """ Movie's author. """
        return self.data.get("uploader", "")

    @property
    def filename(self) -> Path:
        """ Movie's filename """
        return Path(self.__name)

    @property
    def description(self) -> str:
        """ Movie's description. """
        return self.data.get("description", "")

    def delete(self) -> None:
        """
        Delete movie.
        """
        movie = create_movie(self.url)
        logger.info("delete: [%s]", movie.title)
        os.remove(self.__mp3)
        os.remove(self.__json)
