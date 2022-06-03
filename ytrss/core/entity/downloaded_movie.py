import json
import os
import time
from datetime import datetime
from email import utils

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

    def __init__(self, destination_dir: Path, data: Dict[Any, str]) -> None:
        self.__date: Optional[datetime] = None
        self.__destination_dir = destination_dir
        self._data = data

        for resource_file in self.data_paths:
            if not os.path.isfile(resource_file):
                raise MovieResourceFileError

    @property
    def data_paths(self) -> Sequence[Path]:
        """ List of full paths of files according movie """
        result = [
            Path(os.path.join(self.__destination_dir,
                              file_path)) for file_path in self.resources_files
        ]
        result.append(Path(os.path.join(self.__destination_dir, f"{self.identity}.json")))
        return result

    @property
    def resources_files(self) -> Sequence[Path]:
        """ List of files according movie """
        if "resources" in self._data:
            return [Path(x) for x in self._data.get("resources", [])]
        # for backward compatibility, where the resources are not present
        return [Path(f"{self.identity}.mp3")]

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
        return self._data.get("id", "")

    @property
    def description(self) -> str:
        """ movie's description """
        return self._data.get("description", "")

    @staticmethod
    def create_movie_desc(destination_path: Path, movie: Movie,
                          resource_list: Sequence[Path]) -> 'DownloadedMovie':
        """ Create DownloadedMovie from movie object and files. """
        metadata_path = os.path.join(destination_path, f"{movie.identity}.json")
        with open(metadata_path, 'w', encoding="utf-8") as file_handler:
            movie_data: Dict[str, Any] = {
                "id": movie.identity,
                "url": movie.url,
                "title": movie.title,
                "uploader": movie.author,
                "description": movie.description,
                "date": utils.formatdate(time.mktime(movie.date.timetuple()))
            }
            if movie.img_url is not None:
                movie_data["image"] = movie.img_url
            movie_data["resources"] = resource_list
            file_handler.write(json.dumps(movie_data, indent=4, sort_keys=True))
        return DownloadedMovie(destination_path, movie_data)

    @staticmethod
    def from_file(destination_dir: Path, filename_path: str) -> 'DownloadedMovie':
        """ Create DownloadedMovie from existed movie """
        json_file = os.path.join(destination_dir, filename_path)
        if not os.path.isfile(json_file):
            raise MovieJSONError
        with open(json_file, encoding="utf-8") as data_file:
            result = DownloadedMovie(destination_dir, json.load(data_file))
        return result
